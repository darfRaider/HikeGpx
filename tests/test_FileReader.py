import unittest
import os
from HikeGpx.Gpx.GpxFile import GpxFile
from HikeGpx.Gpx.Track import Track
from HikeGpx.Gpx.Waypoint import Waypoint
from HikeGpx.Gpx.Waypoint import WaypointType
from HikeGpx.Coordinates.WGS84 import WGS84

class TestFileReader(unittest.TestCase):


    def test_example(self):
        gfile = GpxFile.from_geoadmin_file("tests/assets/testtrack.gpx", "Test Track Name")
        
        gfile.add_waypoint(
            Waypoint(WGS84(47.550760, 7.599493), "TestWaypoint", 
                     wpt_type=WaypointType.Camp)
            )
        gfile.save("tests/output/test_example.gpx")
