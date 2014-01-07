from sphinx_typesafe.typesafe import typesafe


@typesafe
def function_a1():
    """Function without arguments, returning void.

    :rtype: None
    """

    pass

@typesafe
def function_a2():
    """Function without arguments, returning one value.

    :rtype: int
    """
    return 42

@typesafe
def function_a3(a):
    """Function with one argument, returning void.

    :type a: int
    :rtype: None
    """
    pass

@typesafe
def function_a4(a):
    """Function with one argument, returning one value.

    :type a: types.IntType
    :rtype:  types.StringType
    """
    return '{}'.format(a)

@typesafe
def function_a5(a, b, c):
    """Function with various argument, returning one value.

    :type a: types.IntType
    :type b: types.IntType
    :type c: types.IntType
    :rtype:  types.StringType
    """
    return '{},{},{}'.format(a, b, c) 

@typesafe
def function_a6(p, q):
    """Function with various argument, returning one value.

    :type p: sphinx_typesafe.tests.geometry.Point
    :type q: sphinx_typesafe.tests.geometry.Point
    :rtype:  str
    """
    return '({},{}) - ({},{}) = {}'.format(p.x, p.y, q.x, q.y, p.distance(q))

@typesafe
def function_a7(c):
    """Function with various argument, returning one value.

    :type c: sphinx_typesafe.tests.geometry.Circle
    :rtype:  str
    """
    return '({},{}, {}) = {}'.format(c.x, c.y, c.r, c.area())

@typesafe
def function_a8(c, p):
    """Function with various argument, returning one value.

    :type c: sphinx_typesafe.tests.geometry.Circle
    :type p: sphinx_typesafe.tests.geometry.Point
    :rtype:  str
    """
    return '({},{},{}) - ({},{}) = {}'.format(c.x, c.y, c.r, p.x, p.y, c.distance(p))




@typesafe( {} )
def function_b1():
    """Function without arguments, returning void."""
    pass

@typesafe( { 'return': 'int' } )
def function_b2():
    """Function without arguments, returning one value."""
    return 42

@typesafe( { 'a' : 'int' } )
def function_b3(a):
    """Function with one argument, returning void."""
    pass

@typesafe( { 'a'     : 'types.IntType', 
             'return': 'types.StringType' } )
def function_b4(a):
    """Function with one argument, returning one value."""
    return '{}'.format(a)

@typesafe( { 'a'     : 'types.IntType', 
             'b'     : 'types.IntType', 
             'c'     : 'types.IntType', 
             'return': 'types.StringType' } )
def function_b5(a, b, c):
    """Function with various arguments, returning one value."""
    return '{},{},{}'.format(a, b, c) 

@typesafe( { 'p'     : 'sphinx_typesafe.tests.geometry.Point', 
             'q'     : 'sphinx_typesafe.tests.geometry.Point', 
             'return': 'str' } )
def function_b6(p, q):
    """Function with various arguments, returning one value."""
    return '({},{}) - ({},{}) = {}'.format(p.x, p.y, q.x, q.y, p.distance(q))



def test_function_a1():
    function_a1()

def test_function_a2():
    assert(function_a2() == 42)

def test_function_a3():
    function_a3(5)

def test_function_a4():
    assert(function_a4(42) == '42')

def test_function_a5():
    assert(function_a5(1,2,3) == '1,2,3')

def test_function_a6():
    from sphinx_typesafe.tests.geometry import Point
    p = Point(-2.0, -1.0)
    q = Point( 1.0,  3.0)
    assert(function_a6(p, q) == '(-2.0,-1.0) - (1.0,3.0) = 5.0')


def test_function_a7():
    from sphinx_typesafe.tests.geometry import Circle
    c = Circle(-2.0, -1.0, 5.0)
    assert(function_a7(c) == '(-2.0,-1.0, 5.0) = 78.5398163397')

def test_function_a8():
    from sphinx_typesafe.tests.geometry import Circle
    from sphinx_typesafe.tests.geometry import Point
    c = Circle(-2.0, -1.0, 5.0)
    p = Point( 1.0,  4.0)
    assert(function_a8(c, p) == '(-2.0,-1.0,5.0) - (1.0,4.0) = 0.830951894845')


def test_function_b1():
    function_b1()

def test_function_b2():
    assert(function_b2() == 42)

def test_function_b3():
    function_b3(5)

def test_function_b4():
    assert(function_b4(42) == '42')

def test_function_b5():
    assert(function_b5(1,2,3) == '1,2,3')

def test_function_b6():
    from sphinx_typesafe.tests.geometry import Point
    p = Point(-2.0, -1.0)
    q = Point( 1.0,  3.0)
    assert(function_b6(p, q) == '(-2.0,-1.0) - (1.0,3.0) = 5.0')
