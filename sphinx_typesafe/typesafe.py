###################################################################################
#
# Module containing the main typesafe decorator.
#
# Author: Klaas <khz@tzi.org> 
# Date: 03 / 2013
# Hosted on Github:  https://github.com/pythononwheels/icanhastype
#
# Maintainer: Richard Gomes<rgomes.info@gmail.com>
# See: CHANGES.rst for full list of modifications
# Hosted on Github:  https://github.com/frgomes/sphinx_typesafe
###################################################################################

from __future__ import unicode_literals
from __future__ import print_function



class typesafe(object):
    """Decorator which verifies function argument types"""
    ###
    # Inspired and partly taken from the book:
    #
    #    Pro Python. (Expert's Voice in Open Source) from Marty Alchin
    #
    # see: http://www.amazon.com/Python-Experts-Voice-Open-Source/dp/1430227575
    ###

    import re
    __types_re = re.compile(r":type[\s]+(\w+):[\s]+([\w\.]+)", re.IGNORECASE)
    __rtype_re = re.compile(r":rtype:[\s]+([\w\.]+)", re.IGNORECASE)
    __error    = 'Wrong type for {}: expected: {}, actual: {}.'

    def __init__(self, *args, **kwargs):
        import types
        self.noparams = len(args) == 1 and not kwargs and callable(args[0])
        if self.noparams:
            #-- decorator called without parameters
            self.func = args[0]
            assert(type(self.func) == types.FunctionType)
            self.types = self.inspect_function(self.func)
        else:
            #-- decorator called with parameters
            self.func   = None
            self.types  = self.parse_params(*args, **kwargs)
            # store parameters so that they can be checked later against
            # actual values passed to user's function or method
            self.args   = args
            self.kwargs = kwargs

    def __get__(self, instance, klass):
        # only called when the decorator is applied to a method
        return self.get_wrapper(instance, klass, None, None)

    def __call__(self, *args, **kwargs):
        # only called when the decorator is applied to a function
        f = self.get_wrapper(None, None, *args, **kwargs)
        return f(*args, **kwargs)

    def get_wrapper(self, instance, klass, *args, **kwargs):
        # print('INSTANCE = {}'.format(instance))
        if self.noparams:
            def decorate(func, instance, klass):
                def wrapped(*a, **kw):
                    self.validate_function(func, instance, klass, *a, **kw)
                    if instance:
                        result = func(instance, *a, **kw)
                    else:
                        result = func(*a, **kw)
                    self.validate_result(result)
                    return result
                return wrapped
            #-- print('--> prepare function received in this __call__')
            self.wrapped = decorate(self.func, instance, klass)
            return self.wrapped
        else:
            # NOT TESTED == NOT TESTED == NOT TESTED == NOT TESTED 
            def decorate(func, instance, klass, *args, **kwargs):
                def wrapped(*a, **kw):
                    self.validate_function(func, instance, klass, *args, **kwargs)
                    if instance:
                        result = func(instance, *a, **kw)
                    else:
                        result = func(*a, **kw)
                    self.validate_result(result)
                    return result
                return wrapped
            #-- print('--> prepare function stored at constructor')
            self.func = args[0]
            self.wrapped = decorate(self.func, instance, klass, *(self.args), **(self.kwargs))
            return self.wrapped

    def get_type(self, obj):
        import types
        if obj is type or isinstance(obj, ( types.TypeType, 
                                            types.ClassType, 
                                            types.FunctionType )):
            return obj
        else:
            return type(obj)

    def check_type(self, name, obj, cls):
        if obj is None and cls is None: return
        import types
        from zope.interface.verify import verifyObject
        if obj is type or isinstance(obj, ( types.TypeType, 
                                            types.ClassType, 
                                            types.FunctionType )):
            # print('Check argument {} type {} against {}'.format(name, obj, cls))
            if not issubclass(obj, cls) and not verifyObject(cls, obj):
                raise TypeError(self.__error.format(name, obj, cls))
        else:
            # print('Check argument {} type {} against {}'.format(name, type(obj), cls))
            if not isinstance(obj, cls):
                raise TypeError(self.__error.format(name, type(obj), cls))

    def get_class_type(self, kls):
        """Get and return the type of a class 
        :type kls: types.StringType
        """
        if type(kls) == str: kls = unicode(kls)
        if type(kls) == unicode:
            if kls.count('.') > 0:
                parts = kls.rpartition('.')
                import importlib
                m = importlib.import_module(parts[0])
                t = getattr(m, parts[2])
                return self.get_type(t)
            else:
                import importlib
                m = importlib.import_module('__builtin__')
                t = getattr(m, kls)
                return self.get_type(t)
        else:
            raise NameError('Type name must be an unicode literal instead of {}'.format(type(kls)))

    def convert_entries_to_types(self, types):
        #-- print('types: ', types)
        import collections
        result = collections.OrderedDict()
        for name, atype in types:
            #print('trying to get Type {} for: {}'.format(name, atype))
            obj = self.get_class_type(atype)
            #print('got: {}'.format(obj))
            result[name] = obj
        #-- print('result: ', result)
        return result

    def parse_params(self, *args, **kwargs):
        import sys
        if sys.version_info[0] == 2:
            return self.parse_params2(*args, **kwargs)
        else:
            return self.parse_params3(*args, **kwargs)

    def parse_params2(self, *args, **kwargs):
        """Obtain argument types of a decorated function from parameters passed to the decorator itself.
        This behavior is only valid in Python2 paltforms.
        """
        # the parameter spec is passed as a dictionary in args[0]
        if len(args) != 1 or kwargs:
            raise AttributeError('@typesafe: illegal number of parameters')
        if isinstance(args[0], dict):
            return self.convert_entries_to_types(args[0].items())
        else:
            raise AttributeError('@typesafe: parameter must be a dictionary')

    def parse_params3(self, *args, **kwargs):
        """Obtain argument types of a decorated function by instrospecting the function itself.
        This behavior is only valid in Python3 paltforms.
        """
        raise NotImplementedError('Sorry... Python3 support is not available at the moment. :(')

    def inspect_function(self, func):
        """Obtain argument types of a decorated function by instrospecting its Sphinx docstring.""" 
        import inspect
        # the parameter spec is defined as docstring.
        doc = inspect.getdoc(func)
        entries = self.__types_re.findall(doc)
        try:
            entries.append( ('return', self.__rtype_re.search(doc).group(1)) )
        except:
            entries.append( ('return', 'types.NoneType') )
        return self.convert_entries_to_types(entries)

    def validate_function(self, func, instance, klass, *args, **kwargs):
        """Validate formal parameters before calling a decorated function."""
        # check instance against class type
        self.check_type('self', instance, klass)
        # obtain function specification
        import inspect
        argspec = inspect.getargspec(func)
        spec = argspec.args[1:] if instance else argspec.args
        # check arguments
        from itertools import chain
        for name, arg in chain(zip(spec, args), kwargs.items()):
            # print('Verifying ... {} -- {}'.format(name, arg))
            if not name in self.types:
                raise NameError('Argument {} is not specified in docstring'.format(name))
            self.check_type(name, arg, self.types[name])

    def validate_result(self, result):
        """Validate returned value of a decorated function."""
        if 'return' in self.types:
            self.check_type('return', result, self.types['return'])
        else:
            self.check_type('return', result, None)


if __name__ == "__main__":
    print('Not intended to be used on the cli ;)')
    print('Usage: see: https://github.com/frgomes/sphinx_typesafe')
