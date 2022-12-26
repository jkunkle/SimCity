from shapely.geometry import box, Polygon, LineString, MultiLineString

from base import shape

l = LineString([(0, 0), (0, 1), (0, 2), (0, 3)])
print (l.bounds)

#s = shape(box(0, 50, 20, 60))
s = shape(l)

test = 0
for x, y in s.iter_points():
    print (x, y)
    test += 1
print (s.get_area())
print (test)
