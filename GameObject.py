"""
All objects that are interactable in the game should inherit from this base class
"""
import MapObject

# enable type hinting without causing a real circular imports loop
# WARNING: THIS DOES NOT ACTUALLY IMPORT THESE CLASSES. EVER!
if __name__ == '__main__':
    import LocationClass
    import PlayerClass


class GameObject(MapObject.MapObject):
    """
    This is a base class for all interactable objects with a location in the game map
    """
    def __init__(self, location, owner, object_id, unique_id):
        """
        :param location: the object's location
        :type location: LocationClass.Location
        :param owner: the object's owner
        :type owner: PlayerClass.BasePlayer
        :param object_id: the object's id
        :type object_id: int
        :param unique_id: the object's unique id
        :type unique_id: int
        """
        MapObject.MapObject.__init__(self)

        self.__location = location
        self.__owner = owner
        self.__id = object_id
        self.unique_id = unique_id

    @property
    def location(self):
        """
        Gets the object's location.

        :return: The location.
        :rtype: LocationClass.Location
        """
        return self.__location

    @location.setter
    def location(self, value):
        """
        This property sets the new location.

        :param value: The new location.
        :type value: LocationClass.Location
        """
        self.__location = value

    @property
    def owner(self):
        """
        Gets the object's owner.

        :return: The owner.
        :rtype: PlayerClass.BasePlayer
        """
        return self.__owner

    @owner.setter
    def owner(self, value):
        """
        This property sets the new owner.

        :param value: The new owner.
        :type value: PlayerClass.BasePlayer
        """
        self.__owner = value

    @property
    def id(self):
        """
        Gets the object's id.

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
    def type(self):
        """
        Gets the Game Object's type in a string form.

        :return: Game Object's type.
        :rtype: str
        """
        return type(self).__name__

    def get_location(self):
        """
        Gets the object's location.

        :return: the object's location.
        :rtype: LocationClass.Location
        """
        return self.location

    def __eq__(self, other):
        if isinstance(other, GameObject):
            return self.unique_id == other.unique_id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.unique_id

    def __repr__(self):
        # repr is defined and not str because it works when printing lists, and undefined str is always equal to repr.
        return '{{{type} {id}, Owner: {owner}, Loc: {loc}}}'.format(type=self.type,
                                                                    id=self.id,
                                                                    owner=self.owner.id,
                                                                    loc=self.location)
