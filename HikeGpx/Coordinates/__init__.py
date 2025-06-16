from .WGS84 import WGS84
from .LV95 import LV95

"""
https://backend.swisstopo.admin.ch/fileservice/sdweb-docs-prod-swisstopoch-files/files/2023/11/14/2bd5f57e-1109-40d6-8430-cbdfc9f42203.pdf
"""

def prettify_degree(deg: float) -> str:
    degrees = int(deg)
    minutes_decimal = (deg-degrees)*60
    minutes = int(minutes_decimal)
    seconds = round((minutes_decimal-minutes)*60,2)
    return f"{degrees}° {minutes}' {seconds}\""

def lv95_from_wgs84(coord: WGS84) -> LV95:
    phi_dash = (coord.latitude*3600 - 169028.66) * 1e-4
    lambda_dash = (coord.longitude*3600 - 26782.5) * 1e-4
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

def wgs84_from_lv95(coord: LV95) -> WGS84:
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
