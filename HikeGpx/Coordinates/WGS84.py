from dataclasses import dataclass

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
