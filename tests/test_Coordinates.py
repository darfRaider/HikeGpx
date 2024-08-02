import unittest
import os
from HikeGpx.Gpx.GpxFile import GpxFile
from HikeGpx.Gpx.Track import Track
from HikeGpx.Gpx.Waypoint import Waypoint
from HikeGpx.Gpx.TrackPoint import TrackPoint
from HikeGpx.Coordinates.WGS84 import WGS84

class TestCoordinates(unittest.TestCase):

    def test_trackpoint_equality(self):
        p1 = TrackPoint(1,2,3,None)
        p2 = TrackPoint(1,2,3,None)
        self.assertEquals(p1, p2)

    def test_trackpoint_subtraction(self):
        p1 = TrackPoint(1,2,3,None)
        p2 = TrackPoint(1,2,3,None)
        self.assertEquals(p1 - p2, 0)