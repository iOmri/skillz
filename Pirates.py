# !/usr/bin/env python2
"""
The runner module. Used to run python bots.
"""
from __future__ import unicode_literals
import sys
import traceback
import base64
import time
import os
import imp
from PirateClass import BasePirate
from PlayerClass import BasePlayer
from DroneClass import BaseDrone
from IslandClass import BaseIsland
from CityClass import BaseCity
from LocationClass import Location
from Aircraft import Aircraft
from MapObject import MapObject
from GameObject import GameObject

import json  # Used for serializing the data communication.


DEFAULT_BOT_FILE = 'MyBot.py'


def format_data(data, prettify=False):
    """
    This function formats the data to send using json.

    .. warning::
        Tuples will be turned into lists by the json.

    :param data: The data to format using Json.
    :type data: list or tuple or int or str or dict
    :param prettify: Whether or not to format the data prettily, default is False.
    :type prettify: bool
    :return: The formatted data.
    :rtype: str
    """
    if prettify:
        return json.dumps(data, indent=4, sort_keys=True) + '\n'
    else:
        data_str = json.dumps(data)
        return data_str + '\n'


def parse_data(data_str):
    """
    This turns the received data into a dictionary or list using json.

    .. warning::
        Tuples will be turned into lists by the json.


    :param data_str: The input data to un format.
    :type data_str: str
    :return: A json dictionary of the data. Or an empty dictionary if none was received.
    :rtype: dict
    """
    # Json data might be incorrect so try and catch is used.
    try:
        return json.loads(data_str)
    except (ValueError, TypeError):
        return dict()


class PirateGame(object):
    """
    The pirates game class, this holds all of the game data and basic API for the bots.

    :param out_stream: the output stream to send the data to at the end of the turn
    :type out_stream: file | None

    .. note::
        The most important api is:
            * :func:`get_sail_options`
            * :func:`set_sail`
            * :func:`attack`
            * :func:`get_my_living_pirates`
            * :func:`get_all_islands`
            * :func:`get_my_living_drones`
            * :func:`get_my_cities`
    """

    def __init__(self, out_stream):
        # generic game settings
        self.__max_turn_time = 0
        """:type : int"""
        self.__turn_start_time = None
        """:type : float"""
        self.__num_players = 0
        """:type : int"""
        self.__max_turns = 0
        """:type : int"""
        self.__max_points = 0
        """:type : int"""
        self.__max_drones_count = 0
        """:type : int"""
        self.__pirate_max_speed = 0
        """:type : int"""
        self.__drone_max_speed = 0
        """:type : int"""
        self.__turn = 0
        """:type : int"""
        self._recover_errors = True
        """:type : bool"""

        # map attributes
        self.__col_count = None
        """:type : int"""
        self.__row_count = None
        """:type : int"""

        # map objects
        self.__all_islands = []
        """:type : list[Island]"""
        self.__all_cities = []
        """:type : list[City]"""

        # attack settings
        self.__attack_range = 0
        """:type : int"""
        self.__pirate_max_health = 0
        """:type : int"""
        self.__drone_max_health = 0
        """:type : int"""

        # island and city settings
        self.__island_control_range = 0
        self.__max_drone_creation_turns = 0
        self.__city_unload_range = 0

        # other settings
        self.__spawn_turns = 0
        """:type : int"""

        # player stats
        self.__all_players = []
        """:type : list[Player]"""
        self.__me = None
        """:type : Player"""
        # this is only true for 1 vs 1
        self.__enemy = None
        """:type : Player"""
        self.__neutral = Player(player_id=-1, bot_name='neutral')
        """:type : Player"""

        # The orders the bot wants to run.
        self._orders = []
        """:type : list[dict[str | unicode, any]]"""
        # The debug messages the bot wants to send.
        self.__debug_messages = []
        """:type : list[dict[str | unicode, str]]"""

        # Remember if the runner has been initiated yet.
        self._initiated = False
        """:type : bool"""

        # save the output stream to which we should send data at the end of the turn
        self.__out_stream = out_stream

    def _setup(self, data):
        """
        This method parses the initial setup starting game consts and data.

        :param data: The data to initiate from, should be data dictionary from the engine.
        :type data: dict[unicode, any]
        """
        conversion_dictionary = {
            'cols': '_PirateGame__col_count',
            'rows': '_PirateGame__row_count',
            'spawn_turns': '_PirateGame__spawn_turns',
            'turn_time': '_PirateGame__max_turn_time',
            'attack_range': '_PirateGame__attack_range',
            'max_turns': '_PirateGame__max_turns',
            'max_points': '_PirateGame__max_points',
            'max_drones': '_PirateGame__max_drones_count',
            'turn': '_PirateGame__turn',
            'num_players': '_PirateGame__num_players',
            'bot_names': '',
            'recover_errors': '_recover_errors',
            'drone_max_speed': '_PirateGame__drone_max_speed',
            'pirate_max_speed': '_PirateGame__pirate_max_speed',
            'island_control_range': '_PirateGame__island_control_range',
            'drone_creation_turns': '_PirateGame__max_drone_creation_turns',
            'city_unload_range': '_PirateGame__city_unload_range',
            'player_id': '',
            'pirate_max_health': '_PirateGame__pirate_max_health',
            'drone_max_health': '_PirateGame__drone_max_health'
        }
        # Check that no data is missing from the input data.
        for key, value in conversion_dictionary.iteritems():
            if key not in data.keys():
                raise ValueError('Missing key {key} from json dict.'.format(key=key))
            if value and not hasattr(self, value):
                raise ValueError('Missing key {key} from self.'.format(key=value))

        # this attributes are used to create the all_players list later, and not saved in the runner object itself
        bot_names = data.pop('bot_names')
        my_id = int(data.pop('player_id'))

        for key, value in data.iteritems():
            setattr(self, conversion_dictionary[key], value)

        for player_id in xrange(self.__num_players):
            player = Player(player_id, bot_names[player_id])
            self.__all_players.append(player)

        self.__me = self.__all_players[my_id]
        self.__enemy = self.__all_players[(my_id + 1) % self.__num_players]

        # Make sure the runner knows it has been initiated.
        self._initiated = True

    def _update(self, data):
        """
        This method updates the state of the game objects.

        :param data: The data to update from, should be data dictionary from the engine.
        :type data: dict[unicode, any]
        """
        # start timer
        self.__turn_start_time = time.time()

        expected = ['players',
                    'pirates',
                    'dead_pirates',
                    'drones',
                    'islands',
                    'cities'
                    ]

        # Check that all expected keys are here.
        for expected_key in expected:
            if expected_key not in data.keys():
                raise ValueError('Expected key {key} missing from json data dictionary.'.format(key=expected_key))

        self.__all_islands = []
        self.__all_cities = []
        self._orders = []
        self.__debug_messages = []
        self.__turn += 1

        for player in self.__all_players:
            player.all_pirates = []
            player.living_pirates = []
            player.living_drones = []

        # update map and create new pirate lists
        for key, value in data.iteritems():
            if key == 'players':
                for player in value:
                    player_id = player['id']
                    player_score = player['score']
                    self.__all_players[player_id].score = player_score

            elif key == 'pirates':
                for pirate in value:
                    pirate_id = pirate['id']
                    unique_id = pirate['unique_id']
                    location = Location(*pirate['location'])
                    owner = self.__get_owner(pirate['owner'])
                    initial_location = Location(*pirate['initial_location'])
                    attack_range = pirate['attack_range']
                    max_speed = pirate['max_speed']
                    current_health = pirate['current_health']
                    pirate_object = Pirate(location, owner, pirate_id, unique_id, max_speed, initial_location,
                                           current_health, attack_range)

                    owner.all_pirates.append(pirate_object)
                    owner.living_pirates.append(pirate_object)

            elif key == 'dead_pirates':
                for dead_pirate in value:
                    pirate_id = dead_pirate['id']
                    unique_id = dead_pirate['unique_id']
                    location = Location(*dead_pirate['location'])
                    owner = self.__get_owner(dead_pirate['owner'])
                    initial_location = Location(*dead_pirate['initial_location'])
                    attack_range = dead_pirate['attack_range']
                    max_speed = dead_pirate['max_speed']
                    # dead pirates always have 0 health
                    current_health = 0
                    pirate_object = Pirate(location, owner, pirate_id, unique_id, max_speed, initial_location,
                                           current_health, attack_range)
                    pirate_object.turns_to_revive = dead_pirate['turns_to_revive']

                    owner.all_pirates.append(pirate_object)

            elif key == 'drones':
                for drone in value:
                    drone_id = drone['id']
                    unique_id = drone['unique_id']
                    initial_location = Location(*drone['initial_location'])
                    location = Location(*drone['location'])
                    owner = self.__get_owner(drone['owner'])
                    max_speed = drone['max_speed']
                    value = drone['value']
                    current_health = drone['current_health']

                    drone_object = Drone(location, owner, drone_id, unique_id, max_speed, initial_location,
                                         current_health, value)

                    owner.living_drones.append(drone_object)

            elif key == 'islands':
                for island in value:
                    island_id = island['id']
                    unique_id = island['unique_id']
                    location = Location(*island['location'])
                    owner = self.__get_owner(island['owner'])
                    control_range = island['control_range']
                    turns_to_drone_creation = island['turns_to_drone_creation']

                    island_object = Island(location, island_id, unique_id, control_range, turns_to_drone_creation,
                                           owner)

                    self.__all_islands.append(island_object)

            elif key == 'cities':
                for city in value:
                    city_id = city['id']
                    unique_id = city['unique_id']
                    location = Location(*city['location'])
                    owner = self.__get_owner(city['owner'])
                    unload_range = city['unload_range']
                    value_multiplier = city['value_multiplier']

                    city_object = City(location, city_id, unique_id, unload_range, value_multiplier, owner)

                    self.__all_cities.append(city_object)

            else:
                raise ValueError('Unrecognized key "{key}" in the json dict.'.format(key=key))

        # update player pirate lists
        for player in self.__all_players:
            player.all_pirates.sort(key=lambda player_pirate: player_pirate.id)
            player.living_drones.sort(key=lambda player_drone: player_drone.id)
            player.living_pirates.sort(key=lambda player_pirate: player_pirate.id)

    def __get_owner(self, owner_id):
        """
        Returns the Player owner with the given id, or natural Player if the id is -1.
        Otherwise, raises IndexError.

        :param owner_id: the id of the owner
        :type owner_id: int
        :return: the player which the id belongs to
        :rtype: Player
        """
        if owner_id == -1:
            return self.__neutral
        if self.__all_players[owner_id] is not None:
            return self.__all_players[owner_id]
        raise IndexError('Get owner by id was attempted with illegal id of {}.'.format(owner_id))

    ''' Player related API '''
    def get_all_players(self):
        """
        Gets all the players in the game.

        :return: list of all players in the game.
        :rtype: list[Player]
        """
        return self.__all_players[:]

    def get_myself(self):
        """
        Gets my player object.

        :return: my player object.
        :rtype: Player
        """
        return self.__me

    def get_enemy(self):
        """
        Gets the enemy player object.

        :return: the enemy player object.
        :rtype: Player
        """
        return self.__enemy

    def get_neutral(self):
        """
        Gets the neutral 'player'.

        :return: the neutral 'player'
        :rtype: Player
        """
        return self.__neutral

    ''' Pirate related API '''

    def get_all_my_pirates(self):
        """
        Returns a list of all friendly pirates.

        :return: list of all my pirates sorted by ID.
        :rtype: list[Pirate]
        """
        return self.__me.all_pirates[:]

    def get_my_living_pirates(self):
        """
        Returns a list of all friendly pirates that are currently in the game (on screen).

        :return: list of all friendly pirates that are currently in the game.
        :rtype: list[Pirate]
        """
        return self.__me.living_pirates[:]

    def get_all_enemy_pirates(self):
        """
        Returns a list of all enemy pirates.

        :return: list of all enemy pirates sorted by ID.
        :rtype: list[Pirate]
        """
        return self.__enemy.all_pirates[:]

    def get_enemy_living_pirates(self):
        """
        Returns a list of all enemy pirates that are currently in the game (on screen).

        :return: list of all enemy pirates that are currently in the game.
        :rtype: list[Pirate]
        """
        return self.__enemy.living_pirates[:]

    def get_my_pirate_by_id(self, pirate_id):
        """
        Returns a friendly pirate by id.

        :param pirate_id: the id of the pirate.
        :type pirate_id: int
        :return: the friendly pirate that has the given id.
        :rtype: Pirate
        """
        if pirate_id < 0 or pirate_id >= len(self.get_all_my_pirates()):
            return None
        return self.get_all_my_pirates()[pirate_id]

    def get_enemy_pirate_by_id(self, pirate_id):
        """
        Returns an enemy pirate by id.

        :param pirate_id: the id of the pirate.
        :type pirate_id: int
        :return: the enemy pirate that has the given id.
        :rtype: Pirate
        """
        if pirate_id < 0 or pirate_id >= len(self.get_all_enemy_pirates()):
            return None
        return self.get_all_enemy_pirates()[pirate_id]

    def get_aircrafts_on(self, map_object):
        """
        Returns the aircrafts on the given location.

        :param map_object: the given location.
        :type map_object: MapObject
        :return: the list of aircrafts on the location.
        :rtype: list[Aircraft]
        """
        location = map_object.get_location()
        aircrafts = [aircraft for aircraft in self.get_my_living_aircrafts() if aircraft.location == location]
        aircrafts += [aircraft for aircraft in self.get_enemy_living_aircrafts() if aircraft.location == location]
        return aircrafts

    ''' Objects API '''

    def get_my_living_drones(self):
        """
        Gets all the drones of the current player.

        :return: list of all current player's drones.
        :rtype: list[Drone]
        """
        return self.__me.living_drones[:]

    def get_enemy_living_drones(self):
        """
        Gets all the drones of the opponent.

        :return: list of all opponent's drones.
        :rtype: list[Drone]
        """
        return self.__enemy.living_drones[:]

    def get_my_drone_by_id(self, drone_id):
        """
        Gets the current player's drone with the given id.

        :param drone_id: the id of the drone.
        :type drone_id: int
        :return: the drone with the given id.
        :rtype: Drone
        """
        for drone in self.get_my_living_drones():
            if drone.id == drone_id:
                return drone
        return None

    def get_enemy_drone_by_id(self, drone_id):
        """
        Gets the opponent's drone with the given id.

        :param drone_id: the id of the drone.
        :type drone_id: int
        :return: the drone with the given id.
        :rtype: Drone
        """
        for drone in self.get_enemy_living_drones():
            if drone.id == drone_id:
                return drone
        return None

    def get_my_living_aircrafts(self):
        """
        Gets all the living drones and pirates of the current player.

        :return: all the living drones and pirates of the current player.
        :rtype: list[Aircraft]
        """
        return self.__me.get_living_aircrafts()

    def get_enemy_living_aircrafts(self):
        """
        Gets all the living drones and pirates of the enemy player.

        :return: all the living drones and pirates of the enemy player.
        :rtype: list[Aircraft]
        """
        return self.__enemy.get_living_aircrafts()

    def get_all_islands(self):
        """
        Returns all islands in the game.

        :return: all islands in the game.
        :rtype: list[Island]
        """
        return self.__all_islands[:]

    def get_my_islands(self):
        """
        Returns all islands under the current player's control.

        :return: all islands under the current player's control.
        :rtype: list[Island]
        """
        return [island for island in self.__all_islands if island.owner == self.__me]

    def get_enemy_islands(self):
        """
        Returns all islands under the opponent's control.

        :return: all islands under the opponent's control.
        :rtype: list[Island]
        """
        return [island for island in self.__all_islands if island.owner == self.__enemy]

    def get_neutral_islands(self):
        """
        Returns all islands under no player's control.

        :return: all island's under no player's control.
        :rtype: list[Island]
        """
        return [island for island in self.__all_islands if island.owner == self.__neutral]

    def get_not_my_islands(self):
        """
        Returns all islands whose not under the current player's control.

        :return: all islands whose not under the current player's control.
        :rtype: list[Island]
        """
        return [island for island in self.__all_islands if island.owner != self.__me]

    def get_all_cities(self):
        """
        Returns all cities in the game.

        :return: all cities in the game.
        :rtype: list[City]
        """
        return self.__all_cities[:]

    def get_my_cities(self):
        """
        Returns all cities under the current player's control.

        :return: all cities under the current player's control.
        :rtype: list[City]
        """
        return [city for city in self.__all_cities if city.owner == self.__me]

    def get_enemy_cities(self):
        """
        Returns all cities under the opponent's control.

        :return: all cities under the opponent's control.
        :rtype: list[City]
        """
        return [city for city in self.__all_cities if city.owner == self.__enemy]

    ''' Action API '''

    # noinspection PyMethodMayBeStatic
    def get_sail_options(self, aircraft, destination):
        """
        Returns the different location options for a given aircraft (pirate or drone) to get as close as it can with the
        aircraft's max speed.

        :param aircraft: the aircraft (pirate or drone) to go to the destination.
        :type aircraft: Aircraft
        :param destination: the destination for the aircraft to go to.
        :type destination: MapObject
        :return: list of locations that will get the pirate as close as it can to the destination.
        :rtype: list[Location]
        """
        # limit the moves by the distance between the aircraft and its destination
        moves = min(aircraft.max_speed, aircraft.distance(destination))

        start_location = aircraft.get_location()
        end_location = destination.get_location()

        # calculate the direction in which we are moving
        row_delta_sign = 1 if end_location.row > start_location.row else -1
        col_delta_sign = 1 if end_location.col > start_location.col else -1

        # calculate the boundaries in which we can move
        min_row = min(start_location.row, end_location.row)
        min_col = min(start_location.col, end_location.col)
        max_row = max(start_location.row, end_location.row)
        max_col = max(start_location.col, end_location.col)

        sail_options = []
        # calculate the "zig-zag" from the start to the end, using a delta which moves from 0 to "moves"
        for delta in xrange(moves + 1):
            new_row = start_location.row + (moves - delta) * row_delta_sign
            new_col = start_location.col + delta * col_delta_sign

            # if we didn't overshoot, add the new location
            if min_row <= new_row <= max_row and min_col <= new_col <= max_col:
                sail_options.append(Location(new_row, new_col))

        return sail_options

    def set_sail(self, aircraft, destination):
        """
        Moves a given aircraft to the given destination.

        :param aircraft: the aircraft to move to the destination.
        :type aircraft: Aircraft
        :param destination: the location to move the pirate to.
        :type destination: MapObject
        """
        # already in destination
        if aircraft.location == destination.get_location():
            self.debug("WARNING: %s %d tried to set sail to its current location." % (aircraft.type, aircraft.id))
            return
        self._orders.append({'type': 'order', 'order_type': 'move', 'acting_aircraft': aircraft.unique_id,
                             'order_args': {'destination': destination.get_location().as_tuple}})

    def attack(self, pirate, target):
        """
        Orders a given pirate to attack a given target.

        :param pirate: the pirate that will attack.
        :type pirate: Pirate
        :param target: the aircraft that will be attacked.
        :type target: Aircraft
        """
        self._orders.append({'type': 'order', 'order_type': 'attack', 'acting_aircraft': pirate.unique_id,
                             'order_args': {'target': target.unique_id}})

    ''' Debug related API '''

    def debug(self, *args):
        """
        Debugs a message.

        :param args: the message parts.
        :type args: list[any]
        """
        if len(args) == 0:
            return
        message = '\n'.join(map(str, args))
        # encode to base64 to avoid people printing weird stuff.
        self.__debug_messages.append({'type': 'message', 'message': base64.b64encode(message)})

    ''' MetaGame API '''

    def get_scores(self):
        """
        Returns game scores to the client-side such that it is ordered - first score is his.

        :return: the game scores.
        :rtype: list[int]
        """
        return [player.score for player in self.__all_players]

    def get_my_score(self):
        """
        Returns my score.

        :return: my score.
        :rtype: int
        """
        return self.__me.score

    def get_enemy_score(self):
        """
        Returns enemy score.

        :return: enemy score.
        :rtype: int
        """
        return self.__enemy.score

    def get_turn(self):
        """
        Returns the current turn number.

        :return: The current turn number.
        :rtype: int
        """
        return self.__turn

    def get_max_turns(self):
        """
        Returns the maximum number of turns in this game.

        :return: the maximum number of turns in this game.
        :rtype: int
        """
        return self.__max_turns

    def get_max_points(self):
        """
        Returns number of points needed to end the game.

        :return: number of points needed to end the game.
        :rtype: int
        """
        return self.__max_points

    def get_max_drones_count(self):
        """
        Returns the maximum number of drones possible for a player at the same time.

        :return: the maximum number of drones possible for a player at the same time.
        :rtype: int
        """
        return self.__max_drones_count

    def get_attack_range(self):
        """
        Returns the attack range.

        :return: the attack range.
        :rtype: int
        """
        return self.__attack_range

    def get_pirate_max_health(self):
        """
        Returns the pirate max health.

        :return: the pirate max health.
        :rtype: int
        """
        return self.__pirate_max_health

    def get_drone_max_health(self):
        """
        Returns the drone max health.

        :return: the drone max health.
        :rtype: int
        """
        return self.__drone_max_health

    def get_unload_range(self):
        """
        Returns the city unload range.

        :return: the city unload range.
        :rtype: int
        """
        return self.__city_unload_range

    def get_control_range(self):
        """
        Returns the island control range.

        :return: the island control range.
        :rtype: int
        """
        return self.__island_control_range

    def get_max_drone_creation_turns(self):
        """
        Returns the number of turns it takes an island to create a drone.

        :return: the number of turns it takes an island to create a drone.
        :rtype: int
        """
        return self.__max_drone_creation_turns

    def get_pirate_max_speed(self):
        """
        Returns the pirate speed.

        :return: the pirate speed.
        :rtype: int
        """
        return self.__pirate_max_speed

    def get_drone_max_speed(self):
        """
        Returns the drone speed.

        :return: the drone speed.
        :rtype: int
        """
        return self.__drone_max_speed

    def get_spawn_turns(self):
        """
        Returns the number of turns it takes a pirate to respawn after it died.

        :return: the number of turns it takes a pirate to respawn.
        :rtype: int
        """
        return self.__spawn_turns

    def get_time_remaining(self):
        """
        Returns the remaining time until the bot times out.

        :return: the remaining time until the bot times out in milliseconds.
        :rtype: int
        """
        return ((self.__turn == 1) * 9 + 1) * self.__max_turn_time - int(1000 * (time.time() - self.__turn_start_time))

    def get_max_turn_time(self):
        """
        Gets the total time for a single turn.

        :return: the total time for a single turn in milliseconds.
        :rtype: int
        """
        return self.__max_turn_time

    def get_opponent_name(self):
        """
        Returns the opponent's name.

        :return: the opponent's name.
        :rtype: str
        """
        return self.__enemy.bot_name

    ''' Terrain API '''

    def get_row_count(self):
        """
        Returns the number of rows in the board.

        :return: the number of rows.
        :rtype: int
        """
        return self.__row_count

    def get_col_count(self):
        """
        Returns the number of cols in the board.

        :return: the number of cols.
        :rtype: int
        """
        return self.__col_count

    ''' Inner API functions '''

    def _finish_turn(self, crashed=False):
        """
        This method returns the wanted orders to the engine after formatting them.

        :param crashed: Whether the bot died due to an exception, and only debug messages should be sent.
        :type crashed: bool
        """
        orders_to_send = self._orders
        if crashed:
            orders_to_send = []
        messages_to_send = self.__debug_messages
        if self.__out_stream:
            self.__out_stream.write(format_data({'type': 'bot_orders',
                                                 'data': {'orders': orders_to_send,
                                                          'debug_messages': messages_to_send},
                                                 'crashed': crashed}))
            self.__out_stream.flush()

    # static methods are not tied to a class and don't have self passed in
    # this is a python decorator
    @staticmethod
    def _run(bot):
        """
        Parses input, updates game state and calls the bot classes do_turn method.

        :param bot: the bot to call do_turn on
        :type bot: _BotController
        """
        # redirect stdout to null so bots can't use print to kill themselves
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull

            pirates = PirateGame(old_stdout)
            while True:
                received_data = parse_data(sys.stdin.readline())  # string new line char
                try:
                    if not received_data:
                        break
                    if 'type' not in received_data.keys():
                        raise TypeError('Missing type parameter from json dictionary.')
                    if 'data' not in received_data.keys():
                        raise TypeError('Missing data parameter from json dictionary.')

                    if received_data['type'] == 'setup':
                        pirates._setup(received_data['data'])
                    elif received_data['type'] == 'turn':
                        # Make sure the runner has been initiated correctly.
                        if not pirates._initiated:
                            raise Exception('Attempt to run runner without initiating it first.')

                        pirates._update(received_data['data'])
                        # call the do_turn method of the class passed in
                        if pirates._recover_errors:
                            # catch all exceptions of the bot
                            # noinspection PyBroadException
                            try:
                                bot.do_turn(pirates)
                            except Exception:
                                error_msg = "Exception occurred during do_turn: \n" + traceback.format_exc()
                                pirates.debug(error_msg)
                        else:
                            bot.do_turn(pirates)
                    else:
                        raise ValueError(
                            'Unrecognized json dictionary type, {type}.'.format(type=received_data['type']))
                    pirates._finish_turn()
                except:
                    pirates._finish_turn(True)
                    raise


class Pirate(BasePirate):
    """
    The Pirate class. Pirates are controlled by the players.
    """
    pass


class Drone(BaseDrone):
    """
    Drones are used to gain points by sending them to a city
    """
    pass


class Island(BaseIsland):
    """
    Islands create drones for their controller once in a few turns
    """
    pass


class City(BaseCity):
    """
    Cities are used to gain points by sending drones to them
    """
    pass


class Player(BasePlayer):
    """
    Players are the bots in the game.
    """
    pass


class _BotController(object):
    """ Wrapper class for bot. May accept either a file or a directory and will add correct folder to path """

    def __init__(self, runner_bot_path):
        # add alias for this module (pythonRunner as Pirates)
        _BotController.load_file_as(__file__, 'Pirates')

        if runner_bot_path.endswith('.py'):
            self.bot = _BotController.load_file_as(runner_bot_path, 'bot')
            """:type : module"""
        else:
            self.bot = imp.load_compiled('bot', runner_bot_path)
            """:type : module"""

    def do_turn(self, game):
        """
        Calls the main function in the bot.

        :param game: the game object to pass to the bot.
        :type game: PirateGame
        """
        self.bot.do_turn(game)
        # Make sure no self collisions
        # game.cancel_collisions()

    @staticmethod
    def load_file_as(file_path, new_name):
        """
        Loads (and imports) the file given, as the name given

        :param file_path: the path to the file to import
        :type file_path: unicode
        :param new_name: the name to import the file as
        :type new_name: unicode
        :return: the imported module
        :rtype: module
        """
        file_directory, file_name = os.path.split(file_path)
        name, _ = os.path.splitext(file_name)
        name = name.encode(sys.getfilesystemencoding())

        module_file, file_name, description = imp.find_module(name, [file_directory])
        new_module = imp.load_module(new_name, module_file, file_name, description)
        module_file.close()
        return new_module


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    # try to initiate bot from file path or directory path
    try:
        try:
            # Check if we are on debug mode.
            debug_option = sys.argv[2]
            if debug_option == 'test_python_runner_json_communication_pipe_data_transfer':
                while True:
                    data_dict = parse_data(sys.stdin.readline())
                    if not data_dict:
                        continue
                    sys.stdout.write(format_data(data_dict))
                    sys.stdout.flush()
        except IndexError:
            pass

        # verify we got correct number of arguments
        try:
            bot_file_path = base64.b64decode(sys.argv[1]).decode('utf8')
        except IndexError:
            sys.stderr.write('Usage: pythonRunner.py <bot_path or bot_directory>\n')
            sys.exit(-1)
        except TypeError:
            sys.stderr.write("Couldn't decode bot's name from base 64: '" + sys.argv[1] + "'\n" +
                             traceback.format_exc())
            sys.exit(-2)

        # add python to path and start the BotController
        if os.path.isdir(bot_file_path):
            sys.path.append(bot_file_path)
            bot_path = os.path.join(bot_file_path, DEFAULT_BOT_FILE)
        else:
            sys.path.append(os.path.dirname(bot_file_path))
            bot_path = bot_file_path

        # noinspection PyProtectedMember
        PirateGame._run(_BotController(bot_path))

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')

# Set all classes to be imported more easily by the bots.
__all__ = [
    # Basic objects.
    'Location',
    'MapObject',
    'GameObject',
    'Player',

    # Game objects.
    'City',
    'Island',

    # Aircrafts
    'Aircraft',
    'Drone',
    'Pirate',

    # Game object.
    'PirateGame'
]
