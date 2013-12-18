###
#
# This modules demonstrates some common use cases.
#
# More detailed tests, exploring little details, are provided in other modules.
#
###


from sphinx_typesafe.typesafe import typesafe


@typesafe
def f_5(a, b, c):
    """
    :type a: types.StringType
    :type b: types.StringType
    :type c: types.StringType
    :rtype:  types.StringType
    """
    return '{}+{}+{}'.format(a, b, c) 



class ClassA(object):

    def __init__(self):
        self.x = 'ClassA:'

    @typesafe
    def method_5(self, a, b, c):
        """
        :type a: types.StringType
        :type b: types.StringType
        :type c: types.StringType
        :rtype:  types.StringType
        """
        return '{} {}+{}+{}'.format(self.x, a, b, c) 


class ClassB(object):

    @typesafe
    def __init__(self, a, b):
        """
        :type a: types.StringType
        :type b: types.StringType
        """
        self.x = 'ClassB:'
        self.a = a
        self.b = b
    
    @typesafe
    def method_5(self, c):
        """
        :type c: types.StringType
        :rtype:  types.StringType
        """
        return '{} {}+{}+{}'.format(self.x, self.a, self.b, c) 


def test_function():
    assert(f_5('a', 'b', 'c') == 'a+b+c')


def test_classA():
    c = ClassA()
    assert(c.method_5('a', 'b', 'c') == 'ClassA: a+b+c')


def test_classB():
    c = ClassB('a', 'b')
    assert(c.method_5('c') == 'ClassB: a+b+c')
