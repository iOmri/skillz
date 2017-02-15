from Pirates import *


def init(game):
    global pirategame
    pirategame = game


def move(aircraft, location):
    global pirategame
    sail_options = pirategame.get_sail_options(aircraft, location)
    pirategame.set_sail(aircraft, sail_options[-1])
