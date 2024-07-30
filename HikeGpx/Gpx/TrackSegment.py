from dataclasses import dataclass
from .TrackPoint import TrackPoint
import bs4


@dataclass
class TrackSegment:
    trackpoints: list[TrackPoint]
    
    def get_soup(self, soup: bs4.BeautifulSoup):
        trkseg = soup.new_tag("trkseg")
        for pt in self.trackpoints:
            trkseg.append(pt.get_soup(soup))
        return trkseg
