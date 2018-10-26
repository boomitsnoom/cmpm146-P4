import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging


def attack_weakest_enemy_planet(state):
   
    #Find the 5 closest planets to the weakest planet
    #logging.info('######### I am here!')
    planets = state.my_planets()
    #logging.info('######## I am here!')
    
    # (2) Find my strongest planet.3`````
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    #logging.info('#######I am here!')

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    #logging.info('###### I am here!')
    if weakest_planet == None:
        return False

    neighbors = []
    #logging.info('##### I am here!')

    for planet in planets:
        #neighbors[planet] = state.distance(planet.ID,weakest_planet.ID)
        neighbors.append((planet, state.distance(planet.ID, weakest_planet.ID)))
        #logging.info('##### I am here!')

    neighbors = sorted(neighbors, key=lambda k: k[1])

    #logging.info('### I am here!')
    stop = min(5,len(neighbors))
    #logging.info('## I am here!')
    for x in range(0,stop):
       # logging.info('# I am here!')
        best_ship = neighbors[x]
       # logging.info('I am here!')
        required_ships = weakest_planet.num_ships + state.distance(best_ship[0].ID,weakest_planet.ID)* weakest_planet.growth_rate + 1
        #logging.info('I just calcualted required ships')
        #logging.info(required_ships < best_ship.num_ships)
       # logging.info(not any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()))
        if((required_ships < best_ship[0].num_ships) and (not any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()))):
            logging.info("in the if")
            issue_order(state,best_ship[0].ID,weakest_planet.ID,required_ships)
            logging.info("issued an order")
            logging.info("Almost done")
            return True
        
    return False


def attack_highest_growth_enemy_planet(state):
    #Find the 5 closest planets to the weakest planet

    planets = state.my_planets()
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    fastest_growing_planet = max(state.enemy_planets(), key=lambda t: t.growth_rate, default=None)
    if fastest_growing_planet == None:
        return False


    neighbors = []


    for planet in planets:
        #neighbors[planet] = state.distance(planet.ID,fastest_growing_planet.ID)
        neighbors.append((planet, state.distance(planet.ID, fastest_growing_planet.ID)))

    neighbors = sorted(neighbors, key=lambda k: k[1])

    stop = min(5,len(neighbors))

    for x in range(0,stop):
        source = neighbors[x]
        required_ships = fastest_growing_planet.num_ships + state.distance(neighbors[x][0].ID,fastest_growing_planet.ID)* fastest_growing_planet.growth_rate + 1
        if((required_ships < strongest_planet.num_ships) and (not any(fleet.destination_planet == fastest_growing_planet.ID for fleet in state.my_fleets()))):
            issue_order(state,strongest_planet.ID,fastest_growing_planet.ID,required_ships)
            return True
    return False

def spread_to_weakest_neutral_planet(state):
    planets = state.my_planets()
    while len(planets) > 0:
        strongest_planet = max(planets, key=lambda t: t.num_ships, default=None)
        if strongest_planet is None:    #not sure how this happens, but it does so deal with it
            logging.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            logging.info(str(len(planets)))
            return False
        neighbors = []
        for planet in state.neutral_planets():
            #logging.info('###########################STRONGEST: ' + str(strongest_planet) + ' PLANET: ' + str(planet))
            #neighbors[planet] = state.distance(strongest_planet.ID, planet.ID)
            neighbors.append((planet, state.distance(strongest_planet.ID, planet.ID)))
        neighbors = sorted(neighbors, key=lambda k: k[1])   #sort neighbors by distance
        stop = min(5, len(neighbors))   #stop at either 5 planets or the total number of possible targets
        for val in range(0,stop):  #look at the 5 nearest planets
            target = neighbors[val]
            logging.info('TARGETING ' + str(target))
            required_ships = target[0].num_ships + 1
            if((required_ships < strongest_planet.num_ships) and (not any(fleet.destination_planet == target[0].ID for fleet in state.my_fleets()))):
                issue_order(state, strongest_planet.ID, target[0].ID, required_ships)
                return True
        planets.remove(strongest_planet)

    return False

def reinforce_weak_planet(state):
    if len(state.my_planets()) < 2: #cannot reinforce if we only have 1 planet
        return False

    #sort my planet by number of ships
    sorted_planets = []
    for planet in state.my_planets():
        #sorted_planets[planet] = planet.num_ships
        sorted_planets.append((planet, planet.num_ships))
    sorted_planets = sorted(sorted_planets, key=lambda k: k[1])

    sample_size = min((int(len(sorted_planets) / 2)), 5)   #how many of the strongest/weakest planets to look at

    #identify 5 strongest planets
    #strongest_planets = sorted_planets[(-1 * sample_size):]
    #identify our 5 weakest planets
    weakest_planets = sorted_planets[:sample_size]
    #narrow down the weak planets to those with growth rate of 3 or more
    for target in weakest_planets:
        if target[0].growth_rate < 3:  #not worth reinforcing a low-growth planet
            break
        elif(any(fleet.destination_planet == target[0].ID for fleet in state.my_fleets())):
            break
        else:   #send half the ships from our strongest planets to the weakest planets
            #source = strongest_planets[-1]
            source = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
            fleet_size = int(source.num_ships / 2)
            issue_order(state, source.ID, target[0].ID, fleet_size)
            #logging.info('#########REINFORCED '+str(target) + ' WITH ' + str(fleet_size) + ' SHIPS FROM ' + str(source))
            return True
            #strongest_planets.remove(source)    #source already donated ships - we don't want it to send any more

    return False    #reinforcing failed

def modified_reinforce(state):
    #send ships from the planet with the highest growth rate and most ships to the planet with the smallest growth rate
    #and fewest ships
    highest_growth_rate = (max(state.my_planets(), key=lambda t: t.growth_rate, default=None)).growth_rate
    lowest_growth_rate = (min(state.my_planets(), key=lambda t: t.num_ships, default=None)).growth_rate

    if highest_growth_rate == lowest_growth_rate:
        return False  # don't bother with reinforcing if everyone has the same growth rate

    #find all the planets with the highest and lowest growth rates
    low_growths = []
    high_growths = []
    for planet in state.my_planets():
        if planet.growth_rate == highest_growth_rate:
            high_growths.append(planet)
        elif planet.growth_rate == lowest_growth_rate:
            low_growths.append(planet)
    low_growths = sorted(low_growths, key=lambda k: k.num_ships)    #sort the lowest growth planets by their ships

    #pick a low-growth planet to reinforce
    for target in low_growths:
        if (any(fleet.destination_planet == target.ID for fleet in state.my_fleets())):
            break  # don't bother reinforcing if reinforcements already en route
        else:
            #send ships from the high-growth planet with the most ships
            source = max(high_growths, key=lambda t: t.num_ships)
            fleet_size = int(source.num_ships / 2)
            logging.info('#########REINFORCED ' + str(target) + ' WITH ' + str(fleet_size) + ' SHIPS FROM ' + str(source))
            return issue_order(state, source.ID, target.ID, fleet_size)

    return False