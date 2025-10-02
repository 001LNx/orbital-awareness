from skyfield.api import load

ts = load.timescale()

def compute_positions(sat_obj, minutes=60, interval=1):
    t = ts.utc(2025, 10, 1, 0, range(0, minutes, interval))
    geocentric = sat_obj.at(t)
    return geocentric.position.km, t
