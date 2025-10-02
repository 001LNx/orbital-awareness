"""
Space Debris Risk Pipeline

Tracks ISS and GOES 15 satellites, computes distances, 
and detects potential close approaches (conjunctions).
"""

import logging
from typing import Dict, Tuple, List

from src.tle_loader import load_tle_from_celestrak
from src.orbit_simulator import compute_positions
from src.collision_model import compute_pairwise_distance, detect_conjunction
from src.visualizer import plot_distance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main() -> None:
    """
    Main function for the space debris risk pipeline.
    Loads TLE data, computes satellite positions, detects
    risky events, and plots distances over time.
    """
    logging.info("Starting the space debris risk pipeline...")

    try:
        # Load satellite TLE data
        sats: Dict[str, object] = load_tle_from_celestrak()
        iss = sats.get('ISS (ZARYA)')
        goes = sats.get('GOES 15')

        if iss is None or goes is None:
            logging.error("One or both satellites not found.")
            return

        # Compute satellite positions
        pos1, t = compute_positions(iss)
        pos2, _ = compute_positions(goes)

        # Compute pairwise distances and detect risky events
        dist: List[float] = compute_pairwise_distance(pos1, pos2)
        risky: List[int] = detect_conjunction(dist)

        # Output results
        logging.info("Number of risky events detected: %d", len(risky))

        # Plot distances over time
        plot_distance(range(len(dist)), dist, 'ISS', 'GOES 15')

    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)

if __name__ == "__main__":
    main()

