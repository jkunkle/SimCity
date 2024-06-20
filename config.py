from shapely.geometry import Polygon, Point

from products import ProductCollection, Product

import functions
from definitions import zone_types, needs, skills, terrain

# Square board, diagonals allowed
BOARD_TRANSLATIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
]

JOBS_MULTIPLIER = 0.05

HOUSING_COMMERCIAL_SLOTS = [1, 2, 3]

ATTRACTION_FARM = functions.sigmoid(offset=0.0, slope=40, scale=0.1, intercept=0)
DISTANCE_SCORE_FARM = functions.sigmoid(offset=3, slope=3, scale=-1, intercept=1)
PATH_SCORE_FARM = functions.lookup({1:1}, 0)

AGE_PDF_FARM = functions.GaussPDF(40, 5, 18, 65)
DEFAULT_TERRAIN_TYPE = terrain.meadow

DEFAULT_EXCESS_OUTPUT_FARM = 0.1
FARM_OUTPUT_VAR = 0.2

DEFAULT_NEED_RATES = {
    needs.water: 0.3/12,
    needs.food : 0.05/12,
    needs.shelter : 0.01/12,
    needs.friend : 0.01/12,
    needs.partner : 0.005/12,
    needs.happiness : 0.02/12,
}

DEFAULT_SKILL_DISTS = {
    skills.hunting : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.gathering : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.forestry : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.plants : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.animal_husbandry : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.building : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.creativity : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.medical : functions.ConstPDF(0),
    skills.learning : functions.GaussPDF(0.1, 0.05, 0, 1),
    skills.selling : functions.GaussPDF(0.1, 0.05, 0, 1),
}

SKILL_MODS = {
    zone_types.farm : {
        skills.plants : 0.2,
        skills.animal_husbandry: 0.2,
        skills.building : 0.1,
        skills.learning : -0.1,
        skills.selling : 0.1,
    }
}

TERRAIN_COSTS = {
    terrain.meadow : 0.5,
    terrain.marsh : 0.25,
    terrain.forest : 0.25,
    terrain.stone : 0.5,
    terrain.beach : 0.3,
    terrain.water : 0.05,
    terrain.built_path : 1,
}

TERRAIN_PROVIDES = {
    needs.water : terrain.water,
}

TERRAIN_BUILD_EFFICIENCY = {

    zone_types.residential: {
        terrain.meadow : 1,
        terrain.marsh : 0.5,
        terrain.forest : 0.5,
        terrain.stone : 0.25,
        terrain.beach : 0.5,
        terrain.water : 0,
        terrain.built_path : 0,
    },
    zone_types.commercial: {
        terrain.meadow : 1,
        terrain.marsh : 0.5,
        terrain.forest : 0.5,
        terrain.stone : 0.25,
        terrain.beach : 0.5,
        terrain.water : 0,
        terrain.built_path : 0,
    },
    zone_types.industrial: {
        terrain.meadow : 1,
        terrain.marsh : 0.5,
        terrain.forest : 0.5,
        terrain.stone : 0.25,
        terrain.beach : 0.5,
        terrain.water : 0,
        terrain.built_path : 0,
    },
    zone_types.farm : {
        terrain.meadow : 1,
        terrain.marsh : 0.5,
        terrain.forest : 0.5,
        terrain.stone : 0.25,
        terrain.beach : 0.5,
        terrain.water : 0,
        terrain.built_path : 0,
    },

}




    


# NOTE -- add configuration for time-dependent generation
# NOTE -- climate is configurable?

site_shapes = [
    Point(0,0),
]
#site_shapes = [
#    Polygon([(0,0), (0,1), (1,1), (1,0), (0,0)]),
#    Polygon([(0,0), (0,2), (1,2), (1,0), (0,0)]),
#    Polygon([(0,0), (0,1), (2,1), (2,0), (0,0)]),
#    Polygon([(0,0), (0,2), (2,2), (2,0), (0,0)]),
#]

distance_match = functions.exp(1, 40, 0.001)

EMPTY_BLOCK = '\u2591'
ZONE_BLOCK = {
    'farm' : 'f',
    'residential' : 'r',
    'commercial' : 'c',
    'industrial' : 'i',
}
SITE_BLOCK = {
    'farm' : 'F',
    'residential' : 'R',
    'commercial'  : 'C',
    'industrial' : 'I'
}
ROAD_DIRT_BLOCK = 'x'
WATER_BLOCK = 'w'

ProdColl = ProductCollection()
ProdColl.add(Product('farm_product_1',zone_types.farm))
ProdColl.add(Product('farm_product_2',zone_types.farm))
ProdColl.add(Product('farm_product_3',zone_types.farm))

