from skyfield.api import load

def load_tle_from_celestrak(group='active'):
    url = f"https://celestrak.org/NORAD/elements/{group}.txt"
    sats = load.tle_file(url)
    print(f"[INFO] Loaded {len(sats)} satellites from Celestrak")
    return {sat.name: sat for sat in sats}
