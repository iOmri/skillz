"""
This is the Island base class, used by both the engine and the runner
"""
import GameObject

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass
    import MapObject
    import PlayerClass


class BaseIsland(GameObject.GameObject):
    """
    This is the base island class, should be inherited from in the engine and the runner.
    Islands are captured by a player, and generate drones for that player over time.
    """
    def __init__(self, location, island_id, unique_id, control_range, turns_to_drone_creation=0,
                 owner=None):
        """
        :param location: the island's location
        :type location: LocationClass.Location
        :param island_id: the island's id
        :type island_id: int
        :param unique_id: the island's unique id
        :type unique_id: int
        :param control_range: the island's control range (pirate ships within this range can capture it)
        :type control_range: int
        :param turns_to_drone_creation: the number of turns before the island creates a drone
        :type turns_to_drone_creation: int
        :param owner: the island's owner
        :type owner: PlayerClass.BasePlayer
        """
        GameObject.GameObject.__init__(self, location, owner, island_id, unique_id)

        self.__control_range = control_range
        self.__turns_to_drone_creation = turns_to_drone_creation

    def in_control_range(self, map_object):
        """
        Returns whether the given map object is within this island's control range.

        :param map_object: the map object to check.
        :type map_object: MapObject.MapObject
        :return: whether the map object is within the island's control range.
        :rtype: bool
        """
        return self.in_range(map_object, self.control_range)

    @property
    def control_range(self):
        """
        Gets the island's control range.

        :return: The island's control range.
        :rtype: int
        """
        return self.__control_range

    @control_range.setter
    def control_range(self, value):
        """
        Sets the island's control range.

        :param value: The new control range.
        :type value: int
        """
        self.__control_range = value

    @property
    def turns_to_drone_creation(self):
        """
        Gets the number of turns left before this island creates a new drone.

        :return: The number of turns left before the island creates a new drone.
        :rtype: int
        """
        return self.__turns_to_drone_creation

    @turns_to_drone_creation.setter
    def turns_to_drone_creation(self, value):
        """
        This property Sets the number of turns left before this island creates a new drone.

        :param value: The new turns to drone creation.
        :type value: int
        """
        self.__turns_to_drone_creation = value
