from dataclasses import dataclass
from datetime import datetime
from HikeGpx.Coordinates.WGS84 import WGS84
from typing import Self
import bs4


@dataclass
class TrackPoint:
    coordinate: WGS84
    elevation: float
    time: datetime = None

    def get_soup(self, soup: bs4.BeautifulSoup):
        trkpt = soup.new_tag(name="trkpt", attrs={
            "lat": str(self.coordinate.latitude),
            "lon": str(self.coordinate.longitude)}
        )
        ele = soup.new_tag("ele")
        ele.append(str(self.elevation))
        trkpt.append(ele)
        if self.time is not None:
            time = soup.new_tag("time")
            time.append(self.time)
            trkpt.append(time)
        return trkpt
    
    def __sub__(self, other: Self):
        return self.coordinate - other.coordinate
