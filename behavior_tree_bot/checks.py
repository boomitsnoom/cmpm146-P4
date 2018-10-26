

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def if_neutral_planet_with_high_growth_5(state):
		return any(state.neutral_planets().growth_rate(5))

def if_neutral_planet_with_high_growth_4(state):
		return any(state.neutral_planets().growth_rate(4))

def if_neutral_planet_with_high_growth_3(state):
		return any(state.neutral_planets().growth_rate(3))

def if_neutral_planet_with_high_growth_2(state):
		return any(state.neutral_planets().growth_rate(2))

def if_neutral_planet_with_high_growth_1(state):
		return any(state.neutral_planets().growth_rate(1))

def is_weakest_under_attack(state):
    weakest_planet = min(state.my_planets(), key=lambda t: t.num_ships, default=None)
    return any(fleet.destination_planet == weakest_planet.ID for fleet in state.enemy_fleets())

