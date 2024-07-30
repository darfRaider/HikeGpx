from dataclasses import dataclass
from .WGS84 import WGS84

@dataclass
class LV95:
    N: float
    E: float

    @staticmethod
    def from_wgs84(coord: WGS84):
        phi_dash = (coord.latitude - 169028.66) * 1e-4
        lambda_dash = (coord.longitude - 26782.5) * 1e-4
        E = 2600072.37 +\
            211455.93 * lambda_dash -\
            10938.51 * lambda_dash * phi_dash -\
            0.36 * lambda_dash * phi_dash**2 -\
            44.54 * lambda_dash**3
        N = 1200147.07 +\
            308807.95 * phi_dash +\
            3745.25 * lambda_dash **2 +\
                76.63 * phi_dash**2 -\
                194.56 * lambda_dash**2 * phi_dash +\
                119.79 * phi_dash**3
        return LV95(N, E)