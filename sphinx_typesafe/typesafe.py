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

from __future__ import print_function
from __future__ import unicode_literals

import sys, re
import inspect
from itertools import chain


class typesafe(object):
    """Decorator to verify function argument types inspired and partly take from the book:
    
        Pro Python. (Expert's Voice in Open Source) from Marty Alchin

    See: http://www.amazon.com/Python-Experts-Voice-Open-Source/dp/1430227575
    """

    __types_re = re.compile(r":type[\s]+(\w+):[\s]+([\w\.]+)", re.IGNORECASE)
    __rtype_re = re.compile(r":rtype:[\s]+([\w\.]+)", re.IGNORECASE)

    __error = "Wrong type for '{}': expected: '{}', actual: '{}'."

    def __init__(self, *args, **kwargs):
        self.noparams = len(args) == 1 and not kwargs and callable(args[0])
        if self.noparams:
            # decorator called without parameters
            self.func = args[0]
            self.types = self.inspect_function(self.func)
        else:
            # decorator called with parameters
            self.func = None
            if sys.version_info[0] == 2:
                self.types = self.parse_params2(*args, **kwargs)
            else:
                self.types = self.parse_params3(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.noparams:
            # decorator called without parameters
            # --> call function stored at constructor
            self.validate_function(self.func, *args, **kwargs)
            result = self.func(*args, **kwargs)
            self.validate_result(result)
            return result
        else:
            # decorator called with parameters
            # --> return wrapper to function received in this __call__
            self.func = args[0]
            def wrapped(*a, **kw):
                self.validate_function(self.func, *a, **kw)
                result = self.func(*a, **kw)
                self.validate_result(result)
                return result
            return wrapped

    def get_class_type(self, kls):
        """
        get and return the type of a class 
        :type kls: types.StringType
        """
        #print("get_class_type for %s" % (kls), type(kls))
        if type(kls) == str:
            if kls.count(".") > 0:
                #kls_instance = reduce(getattr, str.split("."), sys.modules[__name__])
                #print("partitioned: ", kls.rpartition("."))
                module = kls.rpartition(".")[0]
                mod = __import__(module, globals(), locals(), [], -1)
                klass = kls.rpartition(".")[2]
                #print(module, mod, klass)
                kls_instance = getattr(mod, klass)
            else:
                #print(dir(sys.modules[__name__]))
                #print(sys.modules[__name__])
                kls_instance = getattr(sys.modules[__name__], kls)
                #print(kls_instance)
                #print(type(kls_instance))
        else:
            print("type was not str")
            kls_instance = kls
        return kls_instance

    def convert_entries_to_types(self, types):
        #-- print('types: ', types)
        import collections
        result = collections.OrderedDict()
        for name, atype in types:
            #print("trying to get Type %s for: %s" % (name, atype))
            obj = self.get_class_type(atype)
            #print("got: %s" % (obj))
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
        raise NotImplementedError()

    def inspect_function(self, func):
        """Obtain argument types of a decorated function by instrospecting its Sphinx docstring.""" 
        # the parameter spec is defined as docstring.
        doc = inspect.getdoc(func)
        entries = self.__types_re.findall(doc)
        entries.append( ('return', self.__rtype_re.search(doc).group(1)) )
        return self.convert_entries_to_types(entries)

    def validate_function(self, func, *args, **kwargs):
        """Validate formal parameters before calling a decorated function."""
        spec = inspect.getargspec(func)
        for name, arg in chain(zip(spec.args, args), kwargs.items()):
            if name in self.types and not isinstance(arg, self.types[name]):
                raise TypeError(self.__error.format(name, self.types[name], type(arg).__name__))

    def validate_result(self, result):
        """Validate returned value of a decorated function."""
        if 'return' in self.types:
            print('check returned type ', type(result), 'against', self.types['return'])
            if not isinstance(result, self.types['return']):
                raise TypeError(self.__error.format('return', self.types['return'], type(result).__name__ ))
        else:
            print('check returned type ', type(result), 'against <NoneType>')
            if result is not None:
                raise TypeError(self.__error.format('return', 'None', type(result).__name__ ))


if __name__ == "__main__":
    print("Not intended to be used on the cli ;)")
    print("Usage: see: https://github.com/frgomes/sphinx_typesafe")
