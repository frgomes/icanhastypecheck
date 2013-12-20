from sphinx_typesafe.typesafe import typesafe


@typesafe
def function_f1a(x):
    """Function with one argument, returning one value.

    :type x: types.IntType
    :rtype:  types.StringType
    """
    return '{}'.format(x)


@typesafe({ 'x': 'types.IntType', 
            'return': 'types.StringType'} )
def function_f1b(x):
    """Function with one argument, returning one value.
    """
    return '{}'.format(x)



def test_function_fail_01():
    import pytest
    with pytest.raises(AttributeError):
        @typesafe( 'rubbish' )
        def function_fail():
            pass
        function_fail()

def test_function_fail_02():
    import pytest
    with pytest.raises(AttributeError):
        @typesafe( {}, 'rubbish' )
        def function_fail():
            pass
        function_fail()


def test_function_fail_03():
    import pytest
    with pytest.raises(NameError):
        @typesafe( { 'a' : None } )
        def function_fail(x):
            print(x)
        function_fail(42)

def test_function_fail_04():
    import pytest
    with pytest.raises(AttributeError):
        @typesafe( { 'a' : '' } )
        def function_fail(x):
            print(x)
        function_fail(42)

def test_function_fail_05a():
    import pytest
    with pytest.raises(NameError):
        @typesafe( { 'a' : 5 } )
        def function_fail(x):
            print(x)
        function_fail(42)

def test_function_fail_05b():
    import pytest
    with pytest.raises(NameError):
        @typesafe( { 'a' : int } )
        def function_fail(x):
            print(x)
        function_fail(42)

def test_function_fail_05c():
    import pytest
    with pytest.raises(NameError):
        @typesafe( { str : int } )
        def function_fail(x):
            print(x)
        function_fail(42)

def test_function_fail_a5d():
    import pytest
    from sphinx_typesafe.tests.mod1 import Point
    p = Point(3.0, 4.0)
    with pytest.raises(NameError):
        @typesafe( { p : int } )
        def function_fail(x):
            print(x)
        function_fail(42)

def test_function_fail_06a():
    import pytest
    with pytest.raises(TypeError):
        assert(function_f1a('rubbish') == '42')

def test_function_fail_06b():
    import pytest
    with pytest.raises(TypeError):
        assert(function_f1b('rubbish') == '42')

def test_function_fail_07a():
    import pytest
    with pytest.raises(TypeError):
        from sphinx_typesafe.tests.mod1 import Point
        assert(function_f1a(Point(3.0, 4.0)) == '42')

def test_function_fail_07b():
    import pytest
    with pytest.raises(TypeError):
        from sphinx_typesafe.tests.mod1 import Point
        assert(function_f1b(Point(3.0, 4.0)) == '42')

def test_function_fail_08a():
    import pytest
    with pytest.raises(TypeError):
        from sphinx_typesafe.tests.mod1 import Point
        assert(function_f1a(type(Point(3.0, 4.0))) == '42')

def test_function_fail_08b():
    import pytest
    with pytest.raises(TypeError):
        from sphinx_typesafe.tests.mod1 import Point
        assert(function_f1b(type(Point(3.0, 4.0))) == '42')
