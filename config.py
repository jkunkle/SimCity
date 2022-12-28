from shapely.geometry import Polygon

import functions
JOBS_MULTIPLIER = 0.05

HOUSING_COMMERCIAL_SLOTS = [1, 2, 3]

ATTRACTION_FARM = functions.sigmoid(offset=0.4, slope=20, scale=0.1, intercept=0)
DISTANCE_SCORE_FARM = functions.sigmoid(offset=3, slope=3, scale=-1, intercept=1)
PATH_SCORE_FARM = functions.lookup({1:1}, 0)

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
    'residentail' : 'R',
    'commercial'  : 'C',
    'industrial' : 'I'
}
ROAD_DIRT_BLOCK = 'x'
