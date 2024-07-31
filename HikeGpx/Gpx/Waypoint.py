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
    Begin = "Begin"
    Building = "Building"
    Cafe = "Cafe"
    Camp = "Camp"
    Camping = "Camping"
    Car = "Car"
    Cave = "Cave"
    Cliff = "Cliff"
    Coast = "Coast"
    Crossroads = "Crossroads"
    Emergency = "Emergency"
    End = "End"
    Food = "Food"
    Forest = "Forest"
    Geocache = "Geocache"
    Hill = "Hill"
    Home = "Home"
    Hostel = "Hostel"
    Hotel = "Hotel"
    Info = "Info"
    Lake = "Lake"
    Lodging = "Lodging"
    Meadow = "Meadow"
    Mountain = "Mountain"
    Parking = "Parking"
    Peak = "Peak"
    Restaurant = "Restaurant"
    River = "River"
    Road = "Road"
    Rock = "Rock"
    Sight = "Sight"
    Trail = "Trail"
    Valley = "Valley"
    Water = "Water"
    Waterfall = "Waterfall"
    Waypoint = "Waypoint"


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
