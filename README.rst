sphinx-typesafe
===============

*previously named IcanHasTypeCheck (ICHTC)*


is a small and easy to use decorator to enable dynamic type checking for python 
method and function calls. Working and tested for Python2.7 but should run in other Python2 as well.
Create an [issue](https://github.com/pythononwheels/icanhastypecheck/issues) on github if you encounter any problems using it.


* Function type specification is based on a naming/docstring convention for Python3.

* Typechecking is implemented as a decorator that can be attached to any function or method and will perform the according (dynamic) typechecking. It will raise a TypeError if the arguments don't match the function specification.

* A tentative implementation for Python3 is included, but not tested.


Python2
-------

Since function annotations are not available in Python2 the way I chose to implement typechecking for Python2 is a documentation convention for parameters based on [the info field lists of sphinx](http://sphinx-doc.org/markup/desc.html#info-field-lists). So even when you don't use typechecking you can use it to auto-generate a function documentation.

There is an alternative approach for those of you who don't like docstings in sphinx format which úses a naming convention. (See Alternatives below)


Syntax for Python2 using decorator arguments
''''''''''''''''''''''''''''''''''''''''''''

::

	@typesafe( { "param_a" : str, 
		     "param_b" : types.IntType, 
		     "param_c" : own_module.OwnType
		     "return"  : bool }
		     )
	def foo(param_a, param_b, param_c):
		""" Some Docstring Info		 """
		# Do Something 
		return True

.. note::

   Observe the use of ``return`` to specify the type returned by the function.



Syntax for Python2using (sphinx style) docstrings
'''''''''''''''''''''''''''''''''''''''''''''''''

::

	@typesafe
	def foo(param_a, param_b):
		"""
		:type param_a: 	types.StringType
		:type param_b: 	types.IntType
		:rtype:         types.BooleanType	
		"""
		# Do Something 
		return True


.. note::

    Observe the use of ``rtype`` to specify the type returned by the function.



You can use any Python type
'''''''''''''''''''''''''''

So if you have defined a Point() class in mod1 then  you could specify is like:

::

    class Point(object):
        # File: mod1.py
	def __init__(self, x = None, y = None):
            """ Initialize the Point. Can be used to give x,y directly."""
	    self.x = x
	    self.y = y

and utilize what you've defined like this:

::

   # another module.py
   from mod1 import Point

   def foo(afunc):
       """ 
       :type afunc: 	mod1.Point
       :rtype: 		types.BooleanType
       """
       return True


The decorator typesafe will first check if it is running in a Python3 or Pyton2 environment and 
react accordingly.


Python3
-------

.. warning::

    This is a tentative implementation which is not tested yet!!


The base technique is the Function Annotations proposed in [PEP 3107](http://www.python.org/dev/peps/pep-3107/) which is 
implemented in [Python3](http://docs.python.org/3.0/whatsnew/3.0.html) (see section New Syntax).



Syntax for Python3
''''''''''''''''''

::

	@typesafe
	def foo(param_a: str, param_b: int) -> bool:
		# Do Something 
		return True


* The @typesafe decorator will then check all arguments dynamically whenever the foo is called for valid types.

* As a quoting remark from the PEP 3107: "All annotated parameter types can be any python expression.", but for typechecking only types make sense, though.

The idea and parts of the implementation were inspired by the book: [Pro Python (Expert's Voice in Open Source)](http://www.amazon.de/Python-Experts-Voice-Open-Source/dp/1430227575)


FAQ
---

Why it was called IcanHasTypeCheck ?
''''''''''''''''''''''''''''''''''''

BTW: The project name "IcanHasTypeCheck" refers to the [famous lolcats](http://en.wikipedia.org/wiki/I_Can_Has_Cheezburger%3F)


Why is now called sphinx-typesafe ?
'''''''''''''''''''''''''''''''''''

Because *typesafe* tells immediatelly what it is about. Unfortunately, *typesafe* was already taken on PyPI, so *sphinx_typesafe* seemed to be a good altenative name which also relates to the documentation standard adopted.
