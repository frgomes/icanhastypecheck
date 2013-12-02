#
# Example Script for IcanHasType  
# typecheck library for python 
# 


import re, sys
import inspect
from sphinx_typesafe.typesafe import typesafe
from sphinx_typesafe.typesafe import print_func_spec
import mod1


@typesafe()
def foo(param_a, param_b):
	""" 
		:type param_a: 	types.IntType
		:type param_b: 	types.StringType
		:rtype:         types.BooleanType	
	"""
	# Do Something 
	print "foo"
	return True


#{ "param_a" : "mod1.Point"}
@typesafe({"param_a": str})
def mod_test( param_a ):
	"""
		:type param_a: mod1.Point
	"""	
	print "Yeah, I was called"


if __name__ == "__main__":
	# passes successfully (see function  spec above)
	foo(1, "test")
	# fails 'successfully' (see function  spec above)
	#foo(1, 2)
	p = mod1.Point()
	mod_test("test")
	print_func_spec(foo)
	# the following call of foo will fail because it passes 
	# an int as second parameter instead of the specified str
	foo(1,2)