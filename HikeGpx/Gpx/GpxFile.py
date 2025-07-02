import bs4
from .Track import Track
from .Waypoint import Waypoint
from HikeGpx.Gpx.TrackPoint import TrackPoint
from HikeGpx.Gpx.TrackSegment import TrackSegment
from HikeGpx.Coordinates.WGS84 import WGS84
from HikeGpx.geoadmin import get_height_from_coordinate
from typing import Self
from copy import deepcopy
from HikeGpx.constants import GPX_ATTRIBUTES

class GpxFile:
    def __init__(self, name):
        self.name = name
        self.tracks: list[Track] = []
        self.waypoints: list[Waypoint] = []

    def calculate_track_distance(self, track_id: int = 0) -> float:
        if len(self.tracks) == 0:
            raise IndexError(f"Track index not found "
                             f"({len(self.tracks)} tracks availabe)")
        distance = 0
        track = self.tracks[track_id]
        for i in range(len(track.track_segment.trackpoints) - 1):
            distance += (track.track_segment.trackpoints[i+1]-track.track_segment.trackpoints[i])
        return distance

    # def set_name(self, name: str):
    #     self.name_tag.append(name)

    # TODO: assemble gpx together on request 
    # to force certain structure, e.g. waypoints
    # appear before tracks even tough added after
    # the track to the gpx object

    def add_track(self, track: Track):
        existing_numbers = [x.number for x in self.tracks]
        if track.number in existing_numbers:
            raise ValueError(f"Track number '{track.number}' already exists")
        self.tracks.append(track)
        

    def add_waypoint(self, waypoint: Waypoint):
        self.waypoints.append(waypoint)

    def assemble(self, root: bs4.BeautifulSoup, gpx_tag: bs4.BeautifulSoup):
        for waypoint in self.waypoints:
            gpx_tag.append(waypoint.get_soup(root))
        for track in self.tracks:
            gpx_tag.append(track.get_soup(root))

    def save(self, path):
        root = bs4.BeautifulSoup()
        gpx_tag = root.new_tag("gpx", attrs=GPX_ATTRIBUTES)
        root.append(gpx_tag)
        self.assemble(root, gpx_tag)
        with open(path, "wb") as f:
            f.write(root.encode())
    
    @staticmethod
    def _get_trackpoint_from_swisstopo(trkpt: bs4):
        wgs84_coord = WGS84(
            float(trkpt.attrs['lat']),
            float(trkpt.attrs['lon']))
        ele = float(trkpt.find("ele").text)
        return TrackPoint(wgs84_coord, ele)

    @classmethod
    def from_swisstopo_file(cls, path: str, name: str = None) -> Self:
        with open(path, "rb") as f:
            data = bs4.BeautifulSoup(f.read())
        track = data.find_all("trk")
        # TODO: check if this is == 1 per default (given by xsd)
        if len(track) != 1:
            raise Exception("Track the gpx-file")
        trackseg = track[0].find_all("trkseg")
        if len(trackseg) != 1:
            raise Exception("There should only be one track segment"
                            " in the gpx-file")
        if name is None:
            name = track[0].find("name")
            if not name:
                raise ValueError("No tag named 'name' found.")
            name = name.text
        trackpoints = trackseg[0].find_all("trkpt")
        trackpoints_obj = [GpxFile._get_trackpoint_from_swisstopo(x) 
                           for x in trackpoints]
        track_segment = TrackSegment(trackpoints_obj)
        track = Track(name=name, number=1, track_segment=track_segment)
        gpx = GpxFile(name=name)
        gpx.add_track(track)
        return gpx

    @classmethod
    def from_geoadmin_file(cls, path: str, name: str) -> Self:
        with open(path, "rb") as f:
            data = bs4.BeautifulSoup(f.read())
        if not len(data.find_all("rte")) == 1:
            raise Exception("There seem to exist multiple routes in the file!")
        waypoints = [WGS84(float(pt.attrs['lat']), float(pt.attrs['lon'])) 
                     for pt in data.find_all("rtept")]
        elevation = [get_height_from_coordinate(wp, override_error=True) 
                     for wp in waypoints]
        track = Track.from_wpt_list(name, [(wpt.latitude, wpt.longitude, el) 
                                           for wpt, el in zip(waypoints, elevation)])
        gpx_file = GpxFile(name)
        gpx_file.add_track(track)
        return gpx_file
