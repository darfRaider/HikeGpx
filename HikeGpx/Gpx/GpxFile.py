import bs4
from .Track import Track
from .Waypoint import Waypoint
from HikeGpx.Coordinates.WGS84 import WGS84
from HikeGpx.geoadmin import get_height_from_coordinate
from typing import Self
from copy import deepcopy

class GpxFile:
    def __init__(self, name):
        self.root = bs4.BeautifulSoup()
        self.name = name
        self.gpx_tag = self.root.new_tag("gpx", 
            attrs={
                "xmlns": "http://www.topografix.com/GPX/1/1",
                "version": "1.1",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" 

            })
        self.root.append(self.gpx_tag)
        # self.name_tag = self.root.new_tag("name")
        # self.gpx_tag.append(self.name_tag)
        # self.set_name(name)
        self.tracks: list[Track] = []
        self.waypoints: list[Waypoint] = []

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

    def assemble(self):
        for waypoint in self.waypoints:
            self.gpx_tag.append(waypoint.get_soup(self.root))
        for track in self.tracks:
            self.gpx_tag.append(track.get_soup(self.root))

    def save(self, path):
        root_cpy = deepcopy(self.root)
        with open(path, "wb") as f:
            f.write(self.root.encode())
    
    @staticmethod
    def from_swisstopo_file(path: str) -> Self:
        pass

    @classmethod
    def from_geoadmin_file(cls, path: str, name: str) -> Self:
        with open(path, "rb") as f:
            data = bs4.BeautifulSoup(f.read())
        if not len(data.find_all("rte")) == 1:
            raise Exception("There seem to exist multiple routes in the file!")
        waypoints = [WGS84(float(pt.attrs['lat']), float(pt.attrs['lon'])) for pt in data.find_all("rtept")]
        elevation = [get_height_from_coordinate(wp, override_error=True) for wp in waypoints]
        track = Track.from_wpt_list(name, [(wpt.latitude, wpt.longitude, el) for wpt, el in zip(waypoints, elevation)])
        gpx_file = GpxFile(name)
        gpx_file.add_track(track)
        return gpx_file
