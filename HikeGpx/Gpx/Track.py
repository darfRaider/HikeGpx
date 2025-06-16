from dataclasses import dataclass
from .TrackSegment import TrackSegment
from .TrackPoint import TrackPoint
from HikeGpx.Coordinates.WGS84 import WGS84
import bs4


@dataclass
class Track:
    name: str
    number: int
    track_segment: TrackSegment

    def get_soup(self, soup: bs4.BeautifulSoup):
        trk = soup.new_tag("trk")
        name = soup.new_tag("name")
        name.append(self.name)
        trk.append(name)
        number = soup.new_tag("number")
        number.append(str(self.number))
        trk.append(number)
        trk.append(self.track_segment.get_soup(soup))
        return trk

    @staticmethod
    def from_wpt_list(name: str, waypoints: list[tuple], number: int = 1):
        trackpoints = [TrackPoint(WGS84(latitude=x[0], longitude=x[1]), elevation=x[2]) for x in waypoints]
        track_segment = TrackSegment(trackpoints)
        return Track(name=name, number=number, track_segment=track_segment)
