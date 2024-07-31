from ..Coordinates.WGS84 import WGS84

from dataclasses import dataclass
import bs4
import warnings
from enum import Enum


class WaypointType(Enum):
    """
    Waypoints that can be used with SUUNTO watches
    https://apizone.suunto.com/route-description
    """
    Waypoint = "Waypoint"
    Water = "Water"
    Begin = "Begin"
    Building = "Building"
    Hill = "Hill"
    Home = "Home"
    Emergency = "Emergency"
    Info = "Info"
    Lake = "Lake"
    Meadow = "Meadow"
    Peak = "Peak"
    Camp = "Camp"
    Camping = "Camping"
    Restaurant = "Restaurant"
    End = "End"
    Car = "Car" 
    Cafe = "Cafe"
    Cave = "Cave"
    Cliff = "Cliff"
    Coast = "Coast" 
    Crossroads = "Crossroads"
    Food = "Food"
    Forest = "Forest"
    Geocache = "Geocache"
    Hostel = "Hostel"
    Hotel = "Hotel"
    Lodging = "Lodging"
    Mountain = "Mountain"
    Parking = "Parking"
    River = "River"
    Road = "Road"
    Rock = "Rock"
    Sight = "Sight"
    Trail = "Trail"
    Valley = "Valley"
    Waterfall = "Waterfall"

    

 
    def from_string(waypoint_type: str):
        try:
            return WaypointType(waypoint_type)
        except Exception:
            warnings.warn(f"Invlaid waypoint type specified: {waypoint_type}")


@dataclass
class Waypoint:
    coordinate: WGS84
    name: str = None
    elevation: float = None
    wpt_type: WaypointType = None
    
    @staticmethod
    def from_gpx(tag: bs4.element.Tag):
        return 
    
    def get_soup(self, soup: bs4.BeautifulSoup = None) -> bs4.element.Tag:
        if soup is None:
            soup = bs4.BeautifulSoup()
        tag = soup.new_tag("wpt", attrs=self.coordinate.to_dict(as_string=True))
        if self.name is not None:
            name_tag = soup.new_tag("name")
            name_tag.string = self.name
            tag.append(name_tag)
        if self.elevation is not None:
            elevation_tag = soup.new_tag("ele")
            elevation_tag.string = str(self.elevation)
            tag.append(elevation_tag)
        if self.wpt_type:
            type_tag = soup.new_tag("type")
            type_tag.string = self.wpt_type.name
            tag.append(type_tag)
        return tag
