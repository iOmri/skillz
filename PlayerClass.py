"""
This is the base player class which the runner and game use.
"""
# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import DroneClass
    import PirateClass
    import Aircraft


class BasePlayer(object):
    """
    The player object, and all of it's attributes.
    """
    def __init__(self, player_id, bot_name):
        """
        Initiates the player.

        :param player_id: the ID of the player
        :type player_id: int
        :param bot_name: the name of the the bot that belongs to the player
        :type bot_name: unicode
        """
        self.__id = player_id
        """:type : int"""
        self.__bot_name = bot_name
        """:type : unicode"""
        self.__score = 0
        """:type : int"""

        self.__living_drones = []  # drones that are currently alive
        """:type : list[DroneClass.BaseDrone]"""
        self.__living_pirates = []  # pirates that are currently alive
        """:type : list[PirateClass.BasePirate]"""
        self.__all_pirates = []  # all pirates that have been created
        """:type : list[PirateClass.BasePirate]"""

    @property
    def id(self):
        """
        Gets the player's id.

        :return: The id.
        :rtype: int
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        This property sets the new id.

        :param value: The new id.
        :type value: int
        """
        self.__id = value

    @property
    def bot_name(self):
        """
        Gets the player's bot name.

        :return: The bot_name.
        :rtype: str
        """
        return self.__bot_name

    @bot_name.setter
    def bot_name(self, value):
        """
        This property sets the new bot_name.

        :param value: The new bot_name.
        :type value: str
        """
        self.__bot_name = value

    @property
    def score(self):
        """
        Gets the player's score.

        :return: The score.
        :rtype: int
        """
        return self.__score

    @score.setter
    def score(self, value):
        """
        This property sets the new score.

        :param value: The new score.
        :type value: int
        """
        self.__score = value

    @property
    def living_drones(self):
        """
        Gets the player's living drones.

        .. warning::
            The list is not duplicated and directly modifying this can cause problems!

        :return: The living_drones.
        :rtype: list[DroneClass.BaseDrone]
        """
        return self.__living_drones

    @living_drones.setter
    def living_drones(self, value):
        """
        This property sets the new living_drones.

        .. warning::
            The list is not duplicated and directly modifying this can cause problems!

        :param value: The new living_drones.
        :type value: list[DroneClass.BaseDrone]
        """
        self.__living_drones = value

    @property
    def living_pirates(self):
        """
        Gets the player's living pirates.

        .. warning::
            The list is not duplicated and directly modifying this can cause problems!

        :return: The living_pirates.
        :rtype: list[PirateClass.BasePirate]
        """
        return self.__living_pirates

    @living_pirates.setter
    def living_pirates(self, value):
        """
        This property sets the new living_pirates.

        .. warning::
            The list is not duplicated and directly modifying this can cause problems!

        :param value: The new living_pirates.
        :type value: list[PirateClass.BasePirate]
        """
        self.__living_pirates = value

    @property
    def all_pirates(self):
        """
        Gets all of the player's pirates.

        .. warning::
            The list is not duplicated and directly modifying this can cause problems!

        :return: The all_pirates.
        :rtype: list[PirateClass.BasePirate]
        """
        return self.__all_pirates

    @all_pirates.setter
    def all_pirates(self, value):
        """
        This property sets the new all_pirates.

        .. warning::
            The list is not duplicated and directly modifying this can cause problems!

        :param value: The new all_pirates.
        :type value: list[PirateClass.BasePirate]
        """
        self.__all_pirates = value

    def get_living_aircrafts(self):
        """
        Returns all living aircrafts of a player. Both pirates and drones.

        :return: A list of all aircrafts.
        :rtype: list[Aircraft.Aircraft]
        """
        living_aircrafts = []
        """:type : list[Aircraft.Aircraft]"""
        living_aircrafts.extend(self.living_pirates)
        living_aircrafts.extend(self.living_drones)
        return living_aircrafts

    def __repr__(self):
        # repr is defined and not str because it works when printing lists, and undefined str is always equal to repr.
        return '{{Player {id}, score: {score}, bot name: {bot_name}}}'.format(id=self.id, score=self.score,
                                                                              bot_name=self.bot_name)

    def __eq__(self, other):
        if isinstance(other, BasePlayer):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id
