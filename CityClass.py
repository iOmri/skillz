"""
This is the City base class, used by both the engine and the runner
"""
import GameObject

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass
    import MapObject
    import PlayerClass


class BaseCity(GameObject.GameObject):
    """
    This is the base city class, should be inherited from in the engine and the runner.
    Cities are used by players to generate points by sending there drones
    """
    def __init__(self, location, city_id, unique_id, unload_range, value_multiplier=1, owner=None):
        """
        :param location: the city's location
        :type location: LocationClass.Location
        :param city_id: the city's id
        :type city_id: int
        :param unique_id: the city's unique id
        :type unique_id: int
        :param unload_range: the city's unload range (drones within this range are unloaded to grant points)
        :type unload_range: int
        :param value_multiplier: each time a drone arrives to the city, it generates a number of points equal to its
          value times the city's value multiplier
        :type value_multiplier: int
        :param owner: the city's owner
        :type owner: PlayerClass.BasePlayer
        """
        GameObject.GameObject.__init__(self, location, owner, city_id, unique_id)

        self.__unload_range = unload_range
        self.__value_multiplier = value_multiplier

    def in_unload_range(self, map_object):
        """
        Returns whether the given map object is within this city's unload range.

        :param map_object: the map object to check.
        :type map_object: MapObject.MapObject
        :return: whether the map object is within the city's unload range.
        :rtype: bool
        """
        return self.in_range(map_object, self.unload_range)

    @property
    def unload_range(self):
        """
        Gets the city's unload range.

        :return: The city's unload range.
        :rtype: int
        """
        return self.__unload_range

    @unload_range.setter
    def unload_range(self, value):
        """
        Sets the city's unload range

        :param value: The new unload range.
        :type value: int
        """
        self.__unload_range = value

    @property
    def value_multiplier(self):
        """
        Gets the city's value multiplier.

        :return: The value_multiplier.
        :rtype: int
        """
        return self.__value_multiplier

    @value_multiplier.setter
    def value_multiplier(self, value):
        """
        This property sets the new value_multiplier.

        :param value: The new value_multiplier.
        :type value: int
        """
        self.__value_multiplier = value
