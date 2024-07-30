from dataclasses import dataclass
from datetime import datetime
import bs4


@dataclass
class TrackPoint:
    latitude: float
    longitude: float
    elevation: float
    time: datetime = None

    def get_soup(self, soup: bs4.BeautifulSoup):
        trkpt = soup.new_tag(name="trkpt", attrs={
            "lat": str(self.latitude),
            "lon": str(self.longitude)}
        )
        ele = soup.new_tag("ele")
        ele.append(str(self.elevation))
        trkpt.append(ele)
        if self.time is not None:
            time = soup.new_tag("time")
            time.append(self.time)
            trkpt.append(time)
        return trkpt
