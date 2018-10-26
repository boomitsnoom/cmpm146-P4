#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    early_game_plan = Sequence(name='Early Game Strategy') #Offensive Plan
    neutral_planet_check = Check(if_neutral_planet_available)
    early_behaviors = Selector(name="Early Behaviors")
    spread = Action(spread_to_weakest_neutral_planet)
    attack = Action(attack_weakest_enemy_planet)
    reinforce = Action(reinforce_weak_planet)
    early_game_plan.child_nodes = [neutral_planet_check,early_behaviors]
    early_behaviors.child_nodes = [spread,attack,reinforce]

    mid_game_plan = Sequence(name='Mid Game Strategy')
    attack_production = Action(attack_highest_growth_enemy_planet)
    reinforce_modified = Action(modified_reinforce)
    mid_game_plan.child_nodes = [attack_production,reinforce_modified,attack.copy()]

<<<<<<< HEAD
    root.child_nodes = [early_game_plan,mid_game_plan,attack.copy()]
=======
    root.child_nodes = [early_game_plan,mid_game_plan, attack.copy()]
>>>>>>> ad507e159704d05e5266cd306a9d833083d1457b

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
