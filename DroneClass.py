"""
This is the Drone base class, used by both the engine and the runner
"""
import Aircraft

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass
    import PlayerClass


class BaseDrone(Aircraft.Aircraft):
    """
    This is the base drone class, should be inherited from in the engine and the runner.
    Drones are used by players to generate points. Drones are made in islands, and once they arrive in a city they
    generate points for their owner.
    """
    def __init__(self, location, owner, drone_id, unique_id, max_speed, initial_location, health, value):
        """
        :param location: the drone's location
        :type location: LocationClass.Location
        :param owner: the drone's owner
        :type owner: PlayerClass.BasePlayer
        :param drone_id: the drone's id
        :type drone_id: int
        :param unique_id: the drone's unique id
        :type unique_id: int
        :param: max_speed: the drone's max speed
        :type max_speed: int
        :param initial_location: the initial location of the drone
        :type initial_location: LocationClass.Location
        :param health: the drone's health
        :type health: int
        :param value: the drone's base value (number of points it generate when it arrives in a city)
        :type value: int
        """
        Aircraft.Aircraft.__init__(self, location, owner, drone_id, unique_id, max_speed, initial_location, health)

        self.__value = value
        """:type : int"""

    @property
    def value(self):
        """
        Gets the drone's value (in points).

        :return: The value.
        :rtype: int
        """
        return self.__value

    @value.setter
    def value(self, value):
        """
        This property sets the drone's value.

        :param value: The drone's new value.
        :type value: int
        """
        self.__value = value
