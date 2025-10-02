import numpy as np

def compute_pairwise_distance(pos1, pos2):
    return np.linalg.norm(pos1 - pos2, axis=0)

def detect_conjunction(distance_km, threshold=50):
    return np.where(distance_km < threshold)[0]
from src.tle_loader import load_tle_from_celestrak
from src.orbit_simulator import compute_positions
from src.collision_model import compute_pairwise_distance, detect_conjunction
from src.visualizer import plot_distance

def main():
    # Load satellites
    sats = load_tle_from_celestrak()
    
    # Choose two satellites by name
    iss = sats.get('ISS (ZARYA)')
    goes = sats.get('GOES 15')

    if iss is None or goes is None:
        print("[ERROR] One or both satellites not found.")
        return

    # Simulate their positions over time
    pos1, t = compute_positions(iss)
    pos2, _ = compute_positions(goes)

    # Compute pairwise distances
    dist = compute_pairwise_distance(pos1, pos2)

    # Detect risky close approaches
    risky = detect_conjunction(dist)

    print(f"[RESULT] Risky events: {len(risky)}")

    # Plot the distance over time
    plot_distance(range(len(dist)), dist, 'ISS', 'GOES 15')

if __name__ == "__main__":
    main()

