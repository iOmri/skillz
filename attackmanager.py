from Pirates import *


def init(game):
    global pirategame
    pirategame = game


def try_attack(pirate):
    global pirategame

    pirate_targets = pirategame.get_enemy_living_pirates()
    pirate_targets = sorted(pirate_targets, lambda a, b: a.current_health - b.current_health)
    drone_targets = pirategame.get_enemy_living_drones()
    drone_targets = sorted(drone_targets, lambda a, b: a.current_health - b.current_health)

    for aircraft in pirate_targets + drone_targets:
        if pirate.in_attack_range(aircraft):
            pirategame.attack(pirate, aircraft)
            pirategame.debug('pirate ' + str(pirate) + ' attacks ' + str(aircraft))
            return True
    return False
