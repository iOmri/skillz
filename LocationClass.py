"""
This class contains the most basic Location class, both the engine PythonRunner use it
"""
import MapObject


class Location(MapObject.MapObject):
    """
    This is the most basic Location class, both the engine and the runner use it.
    """
    def __init__(self, row, col):
        """
        Creates a new instance of the Location class.

        :param row: the row of the location
        :type row: int
        :param col: the col of the location
        :type col: int
        """
        self.__row = row
        """:type : int"""
        self.__col = col
        """:type : int"""

        MapObject.MapObject.__init__(self)

    @property
    def row(self):
        """
        Gets the row of the location ( x value).

        :return: The row.
        :rtype: int
        """
        return self.__row

    @row.setter
    def row(self, value):
        """
        This property sets the new row.

        :param value: The new row.
        :type value: int
        """
        self.__row = value

    @property
    def col(self):
        """
        Gets the col of the location ( y value).

        :return: The col.
        :rtype: int
        """
        return self.__col

    @col.setter
    def col(self, value):
        """
        This property sets the new col.

        :param value: The new col.
        :type value: int
        """
        self.__col = value

    @property
    def as_tuple(self):
        """
        Gets the location as a (row, col) tuple

        :return: the location as a (row, col) tuple
        :type: (int, int)
        """
        return self.row, self.col

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        # repr is defined and not str because it works when printing lists, and undefined str is always equal to repr.
        return '({row}, {col})'.format(col=self.col, row=self.row)

    def __hash__(self):
        """
        Returns a hash code for the location.

        .. warning::
            This forces the map to be smaller than 100 rows.

        :return: A hash code for the location
        :rtype: int
        """
        return self.col * 100 + self.row

    def get_location(self):
        """
        Gets the location.

        :return: the location.
        :rtype: Location
        """
        return self
