from src.tle_loader import load_tle_from_celestrak
from src.orbit_simulator import compute_positions
from src.collision_model import compute_pairwise_distance, detect_conjunction
from src.visualizer import plot_distance

def main():
    sats = load_tle_from_celestrak()
    iss = sats.get('ISS (ZARYA)')
    goes = sats.get('GOES 15')

    if iss is None or goes is None:
        print("[ERROR] One or both satellites not found.")
        return

    pos1, t = compute_positions(iss)
    pos2, _ = compute_positions(goes)

    dist = compute_pairwise_distance(pos1, pos2)
    risky = detect_conjunction(dist)

    print(f"[RESULT] Risky events: {len(risky)}")
    plot_distance(range(len(dist)), dist, 'ISS', 'GOES 15')

if __name__ == "__main__":
    main()
print("[INFO] Starting the space debris risk pipeline...")

