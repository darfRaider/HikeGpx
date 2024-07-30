import bs4
from .Track import Track


class GpxFile:
    def __init__(self, name):
        self.root = bs4.BeautifulSoup(features='xml')
        self.gpx_tag = self.root.new_tag("gpx", attrs={"version": "1.0"})
        self.root.append(self.gpx_tag)
        self.name_tag = self.root.new_tag("name")
        self.gpx_tag.append(self.name_tag)
        self.set_name(name)
        self.tracks: list[Track] = []

    def set_name(self, name: str):
        self.name_tag.append(name)

    def add_track(self, track: Track):
        existing_numbers = [x.number for x in self.tracks]
        if track.number in existing_numbers:
            raise ValueError(f"Track number '{track.number}' already exists")
        self.tracks.append(track)
        self.gpx_tag.append(track.get_soup(self.root))
    