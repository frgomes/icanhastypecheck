from sphinx_typesafe.typesafe import typesafe

class Point(object):

    @typesafe
    def __init__(self, x=0.0, y=0.0):
        """Initialize the Point.
        :type x: float
        :type y: float
        """
        self.x = x
        self.y = y

    @typesafe
    def distance(self, p):
        """Calculates the distance to another Point p.

        :type p: sphinx_typesafe.tests.mod1.Point
        :rtype:  float
        """
        import math
        return math.sqrt( math.pow((self.x - p.x), 2) + math.pow((self.y - p.y), 2) )

