"""
definitions.py

Basic enumerations and mapping between them.
Should be independent of other modules
"""

from enum import Enum

class zone_types(Enum):

    residential = 1
    commercial = 2
    industrial = 3
    farm = 4

class skills(Enum):

    hunting = 1
    gathering = 2
    forestry = 3
    plants = 4
    animal_husbandry = 5
    building = 6
    creativity = 7
    medical = 8 # need?
    learning = 9
    selling = 10
    cleaning = 11

class needs(Enum):

    water = 1
    food = 2
    shelter = 3
    friend = 4
    partner = 5
    happiness = 6

class health_elements(Enum):

    movement = 1
    manipulation = 2
    sight = 3
    talking = 4

class terrain(Enum):

    meadow = 1
    marsh = 2
    forest = 3
    stone = 4
    beach = 5
    water = 6
    built_path = 7

class connection_types(Enum):

    dirt_road = 1
    stone_road = 2
    asphalt_road = 3
    concrete_road = 4






