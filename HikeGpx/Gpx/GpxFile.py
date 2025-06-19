import bs4
from .Track import Track
from .Waypoint import Waypoint


class GpxFile:
    def __init__(self, name):
        self.bs = bs4.BeautifulSoup()
        self.root = self.bs.new_tag("gpx", attrs={
            "version": "1.1",
            "xmlns": "http://www.topografix.com/GPX/1/1",
            "creator": "HikeGpx Python Module by Samuel Stauber",
        })
        self.bs.append(self.root)
        self.metadata_tag = self.bs.new_tag("metadata")
        self.name_tag = self.bs.new_tag("name")
        self.root.append(self.metadata_tag)
        self.metadata_tag.append(self.name_tag)
        self.set_name(name)
        self.tracks: list[Track] = []
        self.waypoints: list[Waypoint] = []

    def set_name(self, name: str):
        self.name_tag.append(name)

    # TODO: assemble gpx together on request 
    # to force certain structure, e.g. waypoints
    # appear before tracks even tough added after
    # the track to the gpx object

    def add_track(self, track: Track):
        existing_numbers = [x.number for x in self.tracks]
        if track.number in existing_numbers:
            raise ValueError(f"Track number '{track.number}' already exists")
        self.tracks.append(track)
        self.root.append(track.get_soup(self.bs))

    def add_waypoint(self, waypoint: Waypoint):
        self.root.append(waypoint.get_soup(self.bs))
        self.waypoints.append(waypoint)

    def save(self, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(self.bs.prettify())
    