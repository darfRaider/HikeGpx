import requests
from typing import Tuple
from HikeGpx.Coordinates import lv95_from_wgs84
from HikeGpx.Coordinates.LV95 import LV95
from HikeGpx.Coordinates.WGS84 import WGS84

def get_height_from_coordinate(coord: Tuple[LV95, WGS84]) -> float:
    if isinstance(coord, WGS84):
        coord = lv95_from_wgs84(coord)
    # coord is of type LV95
    BASE_URL = "https://api3.geo.admin.ch/rest/services/height"
    QUERY = f"?easting={coord.E}&northing={coord.N}"
    URI = BASE_URL + QUERY
    try:
        resp = requests.get(URI).json()
    except Exception as e:
        raise Exception(f"Unable to perform GET-Request for altitude retrieval ({repr(e)}).")
    try:
        height = float(resp["height"])
    except Exception as e:
        raise Exception(f"Unable to obtain altitude from GET-Response ({URI}): {resp} ({repr(e)}).")
    return height
