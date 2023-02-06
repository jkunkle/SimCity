import random 
from scipy.spatial.distance import cityblock
from shapely.geometry import Point

def generate_points_in_polygon(polygon, n_points):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < n_points:
        pnt = Point(random.randint(minx, maxx), random.randint(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points

def calc_distance(sitea, siteb):
    
    coords_a = sitea.get_corner_coordinates()
    coords_b = siteb.get_corner_coordinates()
    return cityblock(coords_a, coords_b)



