"""
This module holds the base classes for any object with a location on the map, and the location itself
"""
from abc import ABCMeta, abstractmethod

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass


class MapObject(object):
    """
    This is a base class for all objects with a location in the game map
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_location(self):
        """
        Gets the object's location.

        :return: the object's location
        :rtype: LocationClass.Location
        """
        raise NotImplemented('must implement get_location method')

    def distance(self, other):
        """
        Gets the distance between this object and another object

        :param other: another map object
        :type other: MapObject
        :return: the distance between this object and the other object
        :rtype: int
        """
        location1 = self.get_location()
        location2 = other.get_location()

        d_row = abs(location1.row - location2.row)
        d_col = abs(location1.col - location2.col)

        return d_row + d_col

    def in_range(self, other, manhattan_range):
        """
        Determines whether or not this object and the other object are within the given range or not

        :param other: the second map object
        :type other: MapObject
        :param manhattan_range: the distance between the two objects
        :type manhattan_range: int
        :return: whether or not the objects are within the given distance of each other
        :rtype: bool
        """
        return self.distance(other) <= manhattan_range
