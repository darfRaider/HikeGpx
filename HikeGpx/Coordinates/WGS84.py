from dataclasses import dataclass
from HikeGpx.constants import MEAN_EARTH_RADIUS
from typing import Self
import math
math.pi

@dataclass
class WGS84:
    latitude: float
    longitude: float

    def to_dict(self, as_string: bool = False):
        if not as_string:
            return {
                "lat": self.latitude,
                "lon": self.longitude,
            }
        return {
            "lat": str(self.latitude),
            "lon": str(self.longitude)
        }
    
    def __sub__(self, other: Self):
        """https://www.movable-type.co.uk/scripts/latlong.html
        """
        phi1 = self.latitude * math.pi/180
        phi2 = other.latitude * math.pi/180
        delta_phi = (other.latitude-self.latitude) * math.pi/180
        delta_lambda = (other.longitude-self.longitude) * math.pi/180
        a = math.sin(delta_phi/2)**2 +\
            math.sin(delta_lambda/2)**2 * math.cos(phi1) * math.cos(phi2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return MEAN_EARTH_RADIUS * c
