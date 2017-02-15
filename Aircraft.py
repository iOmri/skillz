"""
All objects that can move should inherit from this base class
"""
import GameObject

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass
    import PlayerClass


class Aircraft(GameObject.GameObject):
    """
    This is a base class for all moving objects in the game
    """
    def __init__(self, location, owner, aircraft_id, unique_id, max_speed, initial_location, health):
        """
        :param location: the aircraft's location
        :type location: LocationClass.Location
        :param owner: the aircraft's owner
        :type owner: PlayerClass.BasePlayer
        :param aircraft_id: the aircraft's id
        :type aircraft_id: int
        :param unique_id: the aircraft's unique id
        :type unique_id: int
        :param max_speed: the aircraft's max speed (max number of steps each turn)
        :type max_speed: int
        :param initial_location: the initial location of the aircraft
        :type initial_location: LocationClass.Location
        :param health: the aircraft's health
        :type health: int
        """
        GameObject.GameObject.__init__(self, location, owner, aircraft_id, unique_id)

        self.__max_speed = max_speed
        self.__initial_location = initial_location
        self.__current_health = health

    @property
    def max_speed(self):
        """
        Gets the aircraft's max speed.

        :return: The max_speed.
        :rtype: int
        """
        return self.__max_speed

    @max_speed.setter
    def max_speed(self, value):
        """
        This property sets the new max_speed.

        :param value: The new max_speed.
        :type value: int
        """
        self.__max_speed = value

    @property
    def initial_location(self):
        """
        Gets the aircraft's initial location.

        :return: The initial_location.
        :rtype: LocationClass.Location
        """
        return self.__initial_location

    @initial_location.setter
    def initial_location(self, value):
        """
        This property sets the new initial_location.

        :param value: The new initial_location.
        :type value: LocationClass.Location
        """
        self.__initial_location = value

    @property
    def current_health(self):
        """
        Gets the aircraft's current health

        :return: the aircraft's current health
        :rtype: int
        """
        return self.__current_health

    @current_health.setter
    def current_health(self, value):
        """
        Sets the aircraft's current health

        :param value: the new current health
        :type value: int
        """
        self.__current_health = value
