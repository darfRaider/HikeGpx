import unittest
import os
from HikeGpx.Gpx.GpxFile import GpxFile
from HikeGpx.Gpx.Track import Track
from HikeGpx.Gpx.Waypoint import Waypoint
from HikeGpx.Gpx.TrackPoint import TrackPoint
from HikeGpx.Coordinates.WGS84 import WGS84
from HikeGpx.Coordinates.LV95 import LV95
from HikeGpx.Coordinates import wgs84_from_lv95
from HikeGpx.Coordinates import lv95_from_wgs84
from HikeGpx.geoadmin import get_height_from_coordinate

class TestCoordinates(unittest.TestCase):

    def test_coordinate_transformation_lv95_to_wgs84(self):
        northing = 1261565.2416109731
        easting = 2618483.9105565315
        lv95_coord = LV95(N=northing, E=easting)
        expected_longitude = 7.683959
        expected_latitude = 47.504579
        wgs84_coord = wgs84_from_lv95(lv95_coord)
        self.assertAlmostEqual(wgs84_coord.latitude, expected_latitude, 4)
        self.assertAlmostEqual(wgs84_coord.longitude, expected_longitude, 4)

    def test_coordinate_transformation_wgs84_to_lv95(self):
        expected_northing = 1261565.2416109731
        expected_easting = 2618483.9105565315
        longitude = 7.683959
        latitude = 47.504579
        wgs84_coord = WGS84(longitude=longitude, latitude=latitude)
        lv95_coord = lv95_from_wgs84(wgs84_coord)
        self.assertAlmostEqual(lv95_coord.N, expected_northing, 0)
        self.assertAlmostEqual(lv95_coord.E, expected_easting, 0)

    def test_coordinate_transformation_wgs84_to_lv95_2(self):
        expected_northing = 1099999.97
        expected_easting = 2699999.76
        longitude = 8+43/60+49.79/3600
        latitude = 46+2/60+38.87/3600
        wgs84_coord = WGS84(longitude=longitude, latitude=latitude)
        lv95_coord = lv95_from_wgs84(wgs84_coord)
        self.assertAlmostEqual(lv95_coord.N, expected_northing, 2)
        self.assertAlmostEqual(lv95_coord.E, expected_easting, 2)

    def test_trackpoint_equality(self):
        p1 = TrackPoint(WGS84(1,2),3,None)
        p2 = TrackPoint(WGS84(1,2),3,None)
        self.assertEqual(p1, p2)

    def test_trackpoint_subtraction(self):
        p1 = TrackPoint(WGS84(1,2),3,None)
        p2 = TrackPoint(WGS84(1,2),3,None)
        self.assertEqual(p1 - p2, 0)

    def test_lat_lon_subtraction(self):
        p1 = WGS84(longitude=7.72028, latitude=47.482689)
        p2 = WGS84(longitude=7.831972, latitude=47.512093)
        actual_distance = 9028.8
        self.assertAlmostEqual(p1 - p2, actual_distance, -2)

    def test_altitude_retrieval_lv95(self):
        northing = 1261565.2416109731
        easting = 2618483.9105565315
        lv95_coord = LV95(N=northing, E=easting)
        actual_altitude = 408.1
        self.assertEqual(get_height_from_coordinate(lv95_coord), actual_altitude)

    def test_altitude_retrieval_wgs84(self):
        longitude = 7.683959
        latitude = 47.504579
        actual_altitude = 408.1
        wgs84_coord = WGS84(latitude=latitude, longitude=longitude)
        self.assertEqual(get_height_from_coordinate(wgs84_coord), actual_altitude)


