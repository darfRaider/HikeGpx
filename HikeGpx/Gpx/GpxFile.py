import bs4
from .Track import Track
from .Waypoint import Waypoint


class GpxFile:
    def __init__(self, name):
        self.root = bs4.BeautifulSoup(features='xml')
        self.gpx_tag = self.root.new_tag("gpx", attrs={"version": "1.0"})
        self.root.append(self.gpx_tag)
        self.name_tag = self.root.new_tag("name")
        self.gpx_tag.append(self.name_tag)
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
        self.gpx_tag.append(track.get_soup(self.root))

    def add_waypoint(self, waypoint: Waypoint):
        self.gpx_tag.append(waypoint.get_soup(self.root))
        self.waypoints.append(waypoint)

    def save(self, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(self.root.prettify())
    