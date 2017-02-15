"""
This class contains the most basic Pirate class, both the engine Pirate class and the PythonRunner Pirate class inherit
from it.
"""
import Aircraft

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass
    import MapObject
    import PlayerClass


class BasePirate(Aircraft.Aircraft):
    """
    This is the most basic Pirate class, both the engine Pirate class and the PythonRunner Pirate class inherit from it.
    """
    def __init__(self, location, owner, pirate_id, unique_id, max_speed, initial_location, health, attack_range):
        """
        :param location: the location of the pirate
        :type location: LocationClass.Location
        :param owner: the id of the owner of the pirate
        :type owner: PlayerClass.BasePlayer
        :param pirate_id: the id of the pirate
        :type pirate_id: int
        :param unique_id: the pirate's unique id
        :type unique_id: int
        :param max_speed: the pirate's speed
        :type max_speed: int
        :param initial_location: the initial location of the pirate
        :type initial_location: LocationClass.Location
        :param health: the pirates's health
        :type health: int
        :param attack_range: the pirate's attack range
        :type attack_range: int
        """
        Aircraft.Aircraft.__init__(self, location, owner, pirate_id, unique_id, max_speed, initial_location, health)

        # turns until the pirate respawn
        self.__turns_to_revive = 0
        """:type : int"""
        self.__attack_range = attack_range
        """:type : int"""

    def in_attack_range(self, map_object):
        """
        Returns whether the given map object is within this pirate's attack range.

        :param map_object: the map object to check.
        :type map_object: MapObject.MapObject
        :return: whether the map object is within the pirate's attack range.
        :rtype: bool
        """
        return self.in_range(map_object, self.attack_range)

    def is_alive(self):
        """
        Returns whether the pirate is alive.

        :return: Whether the pirate is alive.
        :rtype: bool
        """
        return self.__turns_to_revive == 0

    @property
    def turns_to_revive(self):
        """
        Gets the number of turns left for he pirate to revive. 0 if it's alive.

        :return: The turns_to_revive.
        :rtype: int
        """
        return self.__turns_to_revive

    @turns_to_revive.setter
    def turns_to_revive(self, value):
        """
        This property sets the new turns_to_revive.

        :param value: The new turns_to_revive.
        :type value: int
        """
        self.__turns_to_revive = value

    @property
    def attack_range(self):
        """
        Gets the attack range of the pirate.

        :return: The pirate's attack range.
        :rtype: int
        """
        return self.__attack_range

    @attack_range.setter
    def attack_range(self, value):
        """
        This property sets the pirate's attack range.

        :param value: The new attack range.
        :type value: int
        """
        self.__attack_range = value
