from shapely.geometry import Polygon

from products import ProductCollection, Product

import functions
from definitions import zone_types

JOBS_MULTIPLIER = 0.05

HOUSING_COMMERCIAL_SLOTS = [1, 2, 3]

ATTRACTION_FARM = functions.sigmoid(offset=0.0, slope=40, scale=0.1, intercept=0)
DISTANCE_SCORE_FARM = functions.sigmoid(offset=3, slope=3, scale=-1, intercept=1)
PATH_SCORE_FARM = functions.lookup({1:1}, 0)

DEFAULT_EXCESS_OUTPUT_FARM = 0.1
FARM_OUTPUT_VAR = 0.2

# NOTE -- add configuration for time-dependent generation
# NOTE -- climate is configurable?

site_shapes = [
    Polygon([(0,0), (0,1), (1,1), (1,0), (0,0)]),
    Polygon([(0,0), (0,2), (1,2), (1,0), (0,0)]),
    Polygon([(0,0), (0,1), (2,1), (2,0), (0,0)]),
    Polygon([(0,0), (0,2), (2,2), (2,0), (0,0)]),
]

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

ProdColl = ProductCollection()
ProdColl.add(Product('farm_product_1',zone_types.farm))
ProdColl.add(Product('farm_product_2',zone_types.farm))
ProdColl.add(Product('farm_product_3',zone_types.farm))

