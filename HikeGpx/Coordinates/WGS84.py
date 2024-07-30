from dataclasses import dataclass
from .LV95 import LV95

@dataclass
class WGS84:
    latitude: float
    longitude: float

    @staticmethod
    def from_lv95(coord: LV95):
        x = coord.N
        y = coord.E
        y_dash = (y - 2.6e6) / 1e6
        x_dash = (x - 1.2e6) / 1e6

        lambda_dash = 2.6779094 \
            + 4.728982 * y_dash \
            + 0.791484 * y_dash * x_dash \
            + 0.1306 * y_dash * x_dash**2 \
            - 0.0436 * y_dash**3

        phi_dash = 16.9023892 \
            + 3.238272 * x_dash \
            - 0.270978 * y_dash**2 \
            - 0.002528 * x_dash**2 \
            - 0.0447 * y_dash**2 *x_dash \
            - 0.0140 * x_dash**3 
        
        return WGS84(phi_dash * 100 / 36,  lambda_dash * 100 / 36)
