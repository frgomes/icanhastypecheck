#
# Module containing the main typesafe decorator.
# Author: khz
# Date: 03 / 2013
# Hosted on Github:  https://github.com/pythononwheels/icanhastype
# 

from __future__ import print_function

import inspect
import functools
import re
import sys
from itertools import chain


types_re = re.compile(r":type[\s]+(\w+):[\s]+([\w\.]+)", re.IGNORECASE)	
rtype_re = re.compile(r":rtype:[\s]+([\w\.]+)", re.IGNORECASE)	


def print_list(name, alist):
    """ just printing a parameter list in a readable way
    :type name: 	types.StringType
    :type alist: 	types.ListType
    """
    print("%s" % (name))
    print("--------------------")
    for elem in alist:
        print(elem)
    print()


def print_func_spec(func):
    """ print a function specification including function arguments and type specs.
    :type func: types.FunctionType
    """
    # spec = inspect.getargspec(func)
    doc = inspect.getdoc(func)
    header = "Printing specification for function: {}".format(func.__name__)
    print(header)
    print("="*len(header))
    print()
    # print("getargspec: %s" % (str(spec)))
    # print("Parameter Type spec in docstring: %s" % (doc))
	
    res = types_re.findall(doc)
    print_list("Listing parameter types", res)
    res = rtype_re.findall(doc)
    print_list("return type", res)

	
def get_class_type(kls):
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


def typesafe(parameter_spec = None):
    def __typesafe(func):
        """ Decorator to verify function argument types inspired and partly take from the book:
        Pro Python. (Expert's Voice in Open Source) from Marty Alchin

        See: http://www.amazon.de/Python-Experts-Voice-Open-Source/dp/1430227575

        :type func:  types.FunctionType
        :rtype:      types.FunctionType
        """
        error = "Wrong type for %s: expected: %s, actual: %s."
        if sys.version_info[0] == 3:
            ##########################
            # Handle Python3
            ##########################
            #spec = inspect.getfullargspec(func)
            #doc = inspect.getdoc(func)
            #annotations = spec.annotations
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Not implemented for Python3 yet
                return func
                # handle keyword args
                #for name, arg in chain(zip(spec.args,args), kwargs.items()):
                #    if name in annotations and not isinstance(arg, annotations[name]):
                #        raise TypeError( error % ( name, 
                #                                   annotations[name].__name__, 
                #                                   type(arg).__name__ ) )
                #return func
            return wrapper
        else:
            ############################
            # Handle Python2
            ############################
            spec = inspect.getargspec(func)
            doc = inspect.getdoc(func)
            type_dict = {}
            print('parameter_spec: ', parameter_spec)
            if parameter_spec:
                # the parameter specification is passed as a parameter to the decorator
                types = parameter_spec.items()
            else:
                # the parameter spec is defined as docstring.
                types = types_re.findall(doc)
                types.append( ('return', rtype_re.search(doc).group(1)) )
                print('types: ', types)
                for name, atype in types:
                    #print("trying to get Type %s for: %s" % (name, atype))
                    obj = get_class_type(atype)
                    #print("got: %s" % (obj))
                    type_dict[name] = obj
                print('type_dict: ', type_dict)
			
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # handle keyword args
                for name, arg in chain(zip(spec.args, args), kwargs.items()):
                    if name in type_dict and not isinstance(arg, type_dict[name]):
                        raise TypeError( error % ( name, 
                                                   type_dict[name], 
                                                   type(arg).__name__ ) )
                    else:
                        #fine = "Right type for %s: expected: %s, and successfully got %s."
                        #print(fine %  ( name, type_dict[name], type(arg).__name__ ) )
                        pass
                result = func(*args, **kwargs)
                if 'return' in type_dict:
                    # print('check returned type ', type(result), 'against', type_dict['return'])
                    if not isinstance(result, type_dict['return']):
                        raise TypeError( error % ( 'return', 
                                                   type_dict['return'], 
                                                   type(result).__name__ ))
                    else:
                        # print('check returned type ', type(result), 'against <NoneType>')
                        if result is not None:
                            raise TypeError( error % ( 'return', 
                                                       'None', 
                                                       type(result).__name__ ))

                return result

            return wrapper
    return __typesafe


if __name__ == "__main__":
    print("not intended to be used on the cli ;)")
    print("usage: see: https://github.com/frgomes/sphinx_typesafe")
