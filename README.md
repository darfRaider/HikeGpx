# HikeGpx

## Example
``` python 
from HikeGpx.Gpx.GpxFile import GpxFile
from HikeGpx.Gpx.Track import Track
from HikeGpx.Gpx.Waypoint import Waypoint
from HikeGpx.Gpx.Waypoint import WaypointType
from HikeGpx.Coordinates.WGS84 import WGS84

data = [(46.57608333, 8.89241667, 2376),
        (46.57619444, 8.89252778, 2375),
        (46.57641667, 8.89266667, 2372),
        (46.57650000, 8.89280556, 2373),
        (46.57638889, 8.89302778, 2374),
        (46.57652778, 8.89322222, 2375),
        (46.57661111, 8.89344444, 2376)]

f = GpxFile("TestRoute")
f.add_track(Track.from_wpt_list("Testtrack", data, 1))
wpt = Waypoint(
    WGS84(46.57650000, 8.89280556),
    "TestWaypoint",
    2373,
    WaypointType.Water)
f.add_waypoint(wpt)
f.save("test.gpx")
```