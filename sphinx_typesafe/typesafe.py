###################################################################################
#
# Module containing the main typesafe decorator.
#
# Author: Richard Gomes<rgomes.info@gmail.com>
# See: CHANGES.rst for full list of modifications
# Hosted on Github:  https://github.com/frgomes/sphinx_typesafe
#
# Based on previous work from Klaas <khz@tzi.org> 
# Date: 03 / 2013
# Hosted on Github:  https://github.com/pythononwheels/icanhastype
#
# Inspired and partly taken from the book:
# Pro Python. (Expert's Voice in Open Source) from Marty Alchin
# see: http://www.amazon.com/Python-Experts-Voice-Open-Source/dp/1430227575
#
###################################################################################

from __future__ import unicode_literals
from __future__ import print_function


class typesafe(object):
    """Decorator which verifies function argument types"""

    def __init__(self, *args, **kwargs):
        import copy
        self.noparams = len(args) == 1 and not kwargs and callable(args[0])
        if self.noparams:
            # Decorator called without parameters.
            # User's function or class method is passed as arg[0].
            # Initialize decorator arguments as emptly values.
            self.f = args[0]
            self.dargs   = list()
            self.dkwargs = dict()
        else:
            # Decorator called with parameters.
            # User's function or class method will be passed later.
            # Store decorator arguments for being processed later.
            self.f = None
            self.dargs   = copy.copy(args)
            self.dkwargs = copy.copy(kwargs)

        # The descriptor initialization is delayed as much as possible
        self.descriptor = None

    def __get__(self, instance, klass):
        '''Called when a decorator is applied to a class method only.

        This method is actually called twice:

        1st time: At decoration time, trying to obtain a decorated class method.
                  We purposedly return an unbound wrapper, which unconditionally
                  fails if the Python runtime calls its __call__ method.
        2nd time: At runtime, when we substitute the unbound wrapper by a bounded
                  wrapper, which contains the decorated class method. When the
                  Python runtime calls its __call__ method, the decorator logic
                  will execute.
        '''
        # it's time to build a descriptor now
        self.descriptor = self.__descriptor(self.f, *(self.dargs), **(self.dkwargs))
        # delegate __get__ to the descriptor
        return self.descriptor.__get__(instance, klass)

    def __call__(self, *args, **kwargs):
        '''This method is called in when:

        1. a decorator without arguments is applied to a function
        2. a decorator with arguments was delayed by Python runtime
        '''
        if self.f:
            # This case applies to function calls only, not method calls
            self.descriptor = self.__descriptor(self.f)
            return self.descriptor.__call__(*args, **kwargs)
        else:
            # This case applies to decorator with arguments
            self.f = args[0]
            self.descriptor = self.__descriptor(self.f, *(self.dargs), **(self.dkwargs))
            return self.descriptor

    def __descriptor(self, f, *args, **kwargs):
        '''This method returns a descriptor which is responsible to coordinate
        when the Python runtime will receive an actual callable, so that the
        Python runtime will them call it. More precisely, the descriptor returns
        a wrapper function which, on the right moment, will be able to perform
        the decorator logic which surrounds the decorated user's function or
        user's class method.
    
        In other words, the a descriptor is meant to delay the definition of the
        method wrapper, because (1) the Python runtime delays the user's function or
        class method to the decorator and (2) the actual instance method to be
        decorated in only knowable later, at execution time.
        '''
        return self.descript(f, self.checker(f, *args, **kwargs))



    class descript(object):
        '''This class is intended to delay the definition of the method wrapper
        which surrounds the user's function or user's class method. This is
        necessary for two reasons:

        1. the Python runtime may pass lately the user's function or class method
           to be decorated. It happens when the decorator itself accepts arguments.
           In this case, the decorator must wait until its __get__ or its __call__
           methods are called and, since that happens, then instantiate ``this``
           class since that the user's function or users's class method will be
           known at that point.

        2. the Python runtime executes decorated functions in different ways,
           depending whether they are functions or actually class methods.
           a. In the case of functions, the Python runtime calls the ``__call__``
              method directly. In this case, a wrapper is built and called
              immediately, returning its results to the Python runtime.
           b. In the case of class methods, the Python runtime calls ``__get__``
              and passes an instance object, in order to obtain a bounded
              callable to that instance. Then, the Python runtime calls the
              ``__call__`` method in order to execute the class method.


        Notice that, in the extreme case of a decorator with arguments, applied to
        a class method, the Python runtime will (1) first call ``__get__`` in order
        to obtain an unbounded reference to the users' class method, at decoration
        time (compilation time), then (2) call ``__get__`` at runtime when the
        ``instance`` object is passed and a bounded reference to the user's class
        method and then (3) finally, method ``__call__`` is called, in order to
        executed the bounded class method.
        '''
        def __init__(self, f, checker):
            self.f = f
            self.checker = checker

        def __get__(self, instance, klass):
            '''A decorated class method is requested for being called later.
            In other words, this method is called only for class methods, not functions.

            When an ``instance`` is received, the Python runtime wishes to obtain the
            actual callable method which will be called later. In this case, this method
            returns a wrapper which contains the decorator logic for the specific case of
            class methods, not functions.

            When ``instance`` is None, the Python runtime is interested on obtained an
            unbounded (not callable yet) method for its own purposes. In this case, this
            method returns a wrapper which pursposedly throws an exception in case it is
            called by mistake, since it is by definition unbound and should never be
            called.

            Note: Either way, this method returns a partial function, which later will be
                  called by the Python runtime. In other words, it means that, calling
                  ``__get__`` we intentionaly avoid ``__call__`` to be called later, because
                  the Python runtime will call the wrapped function we return, whatever
                  case it is.
            '''
            if instance is None:
                # Unbounded (not callable) class method was requested
                return self.__method_unbound(klass)
            else:
                # Callable instance method was requested
                return self.__method_bound(instance, klass)

        def __call__(self, *args, **kwargs):
            '''A decorated function was requested to be called.
            In other words, this method is called only for functions, not class methods.

            This method returns a wrapper which contains the decorator logic for the
            specific case of functions, not class methods.
            '''
            from functools import wraps
            @wraps(self.f)
            def wrapper(*args, **kwargs):
                #-- print('Called the decorated function {}'.format(self.f.__name__))
                self.checker.validate_params(self.f, False, *args, **kwargs)
                result = self.f(*args, **kwargs)
                self.checker.validate_result(result)
                return result
            return wrapper(*args, **kwargs)

        def __method_unbound(self, klass):
            from functools import wraps
            @wraps(self.f)
            def wrapper(*args, **kwargs):
                raise TypeError('unbound method {}() must be called with {} instance '.format(
                        self.f.__name__, klass.__name__))
            return wrapper

        def __method_bound(self, instance, klass):
            from functools import wraps
            @wraps(self.f)
            def wrapper(*args, **kwargs):
                #-- print('Called the decorated method {} of {}'.format(self.f.__name__, instance))
                self.checker.check_type('self', instance, klass)
                self.checker.validate_params(self.f, True, *args, **kwargs)
                result = self.f(instance, *args, **kwargs)
                self.checker.validate_result(result)
                return result
            # This instance does not need the descriptor anymore,
            # let it find the wrapper directly next time:
            setattr(instance, self.f.__name__, wrapper)
            return wrapper

    
    class checker(object):

        import re
        __types_re = re.compile(r":type[\s]+(\w+)[\s]*:[\s]*([\w\.]+)", re.IGNORECASE)
        __rtype_re = re.compile(r":rtype[\s]*:[\s]*([\w\.]+)", re.IGNORECASE)
        __error    = 'Wrong type for {}: expected: {}, actual: {}.'

        def __init__(self, f, *args, **kwargs):
            if len(args) == 0:
                self.types = self.inspect_function(f)
            else:
                self.types = self.parse_params(*args, **kwargs)
    
        def inspect_function(self, func):
            """Obtain argument types of a decorated function by instrospecting its Sphinx docstring.""" 
            import inspect
            # the parameter spec is defined as docstring.
            doc = inspect.getdoc(func)
            if doc is None: doc = ''
            entries = self.__types_re.findall(doc)
            try:
                entries.append( ('return', self.__rtype_re.search(doc).group(1)) )
            except:
                entries.append( ('return', 'types.NoneType') )
            return self.convert_entries_to_types(entries)

        def parse_params(self, *args, **kwargs):
            import sys
            if sys.version_info[0] == 2:
                return self.parse_params2(*args, **kwargs)
            else:
                return self.parse_params3(*args, **kwargs)

        def validate_params(self, func, ismethod, *args, **kwargs):
            """Validate formal parameters before calling a decorated function."""
            # obtain function specification
            import inspect
            argspec = inspect.getargspec(func)
            spec = argspec.args[1:] if ismethod else argspec.args
            # check arguments
            from itertools import chain
            names = list()
            # check argument against specification
            for name, arg in chain(zip(spec, args), kwargs.items()):
                if name in self.types:
                    names.append(name)
                    self.check_type(name, arg, self.types[name])
                else:
                    raise AttributeError('specification of variable "{}" is expected.'.format(name))
            # check specification against arguments
            snames = set(names)
            for name, atype in self.types.items():
                if name != 'return' and not name in snames:
                    raise AttributeError('surplus specification variable "{}" detected.'.format(name))

        def validate_result(self, result):
            """Validate returned value of a decorated function."""
            if 'return' in self.types:
                self.check_type('return', result, self.types['return'])
            else:
                self.check_type('return', result, None)

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
                if not issubclass(obj, cls):
                    if not 'providedBy' in cls or not verifyObject(cls, obj):
                        raise TypeError(self.__error.format(name, obj, cls))
            else:
                # print('Check argument {} type {} against {}'.format(name, type(obj), cls))
                if not isinstance(obj, cls):
                    raise TypeError(self.__error.format(name, type(obj), cls))

        def get_unicode(self, s):
            if type(s) == str: s = unicode(s)
            if type(s) == unicode:
                s = s.strip()
            else:
                raise NameError(
                    'Type name must be an unicode literal instead of {}'.format(
                        self.get_type(s)))
            return s

        def get_class_type(self, klass):
            kls = self.get_unicode(klass)
            if kls.count('.') > 0:
                parts = kls.rpartition('.')
                import importlib
                m = importlib.import_module(parts[0])
                # print('--->>> {} {} {}'.format(parts[0], parts[2], m))
                # print(dir(m))
                t = getattr(m, parts[2])
                return self.get_type(t)
            else:
                import importlib
                m = importlib.import_module('__builtin__')
                t = getattr(m, kls)
                return self.get_type(t)

        def convert_entries_to_types(self, types):
            # print('types: ', types)
            import collections
            result = collections.OrderedDict()
            for n, t in types:
                name  = self.get_unicode(n)
                atype = self.get_unicode(t)
                name  = name.strip()
                atype = atype.strip()
                #-- print('trying to get Type {} for: {}'.format(name, atype))
                obj = self.get_class_type(atype)
                #-- print('got: {}'.format(obj))
                result[name] = obj
            #-- print('result: ', result)
            return result

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


if __name__ == "__main__":
    raise NotImplementedError('See: https://github.com/frgomes/sphinx_typesafe')
