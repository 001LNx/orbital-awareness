## Purpose

Short, actionable guidance for an AI coding assistant working on this repository (space-debris-risk-platform).
Focus: where to look, how data flows, project-specific conventions, and known oddities to avoid wasting time.

## Big picture (architecture & data flow)
- TLEs -> orbit states -> pairwise distances -> conjunction detection -> (visualization).
- Key modules:
  - `src/tle_loader.py` — fetches TLE text from Celestrak and returns a dict mapping satellite names to Skyfield satellite objects.
  - `src/orbit_simulator.py` — computes positions with Skyfield. Returns `geocentric.position.km` and the time array.
  - `src/collision_model.py` — computes distances with NumPy and finds indices where distance < threshold (default 50 km).
  - `run_pipeline.py` — example end-to-end script that ties the above together and expects `src.visualizer.plot_distance` to exist.

Data shapes / units you will see often:
- Satellite objects: Skyfield `EarthSatellite` instances (from `load.tle_file`).
- Positions: NumPy arrays in kilometers (returned by `compute_positions`).
- Distances: 1-D NumPy array (km); `detect_conjunction` returns indices where distance < threshold.

## Setup & common workflows
- Install pinned deps from `requirements.txt` (this project expects a virtualenv and internet access for Celestrak):

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Run the example pipeline from the repository root (important: run from repo root so `src` is importable):

  ```bash
  python run_pipeline.py
  ```

- If you encounter import errors for `src`, run with PYTHONPATH set to the repo root: `PYTHONPATH=. python run_pipeline.py`.

## Project-specific conventions & patterns
- Imports use the `src.` package prefix even though `src` is a plain folder — assume scripts are executed from the repo root.
- Exact satellite name keys are used when selecting satellites (e.g., `'ISS (ZARYA)'`, `'GOES 15'`). Use `.get(name)` and guard for `None`.
- Time axis is hard-coded in `compute_positions` via `ts.utc(2025, 10, 1, 0, range(...))`. Be aware of the fixed date when adding tests or changing behavior.
- Distance computation uses `np.linalg.norm(pos1 - pos2, axis=0)` — positions are array-shaped so axis=0 is the time axis.
- Conjunction threshold default is 50 km in `detect_conjunction(distance_km, threshold=50)` — callers depend on that default.

## Integration points & external dependencies
- Celestrak TLE URL pattern (used by `load_tle_from_celestrak`):
  `https://celestrak.org/NORAD/elements/{group}.txt`
  Code expects network access; tests that rely on live fetches will be flaky. Prefer mocking `load.tle_file` in tests.
- Primary third-party libraries: `skyfield`, `numpy`, `sgp4`. Versions are pinned in `requirements.txt`.

## Known quirks / things to watch for
- Missing module: `src.visualizer` is imported by `run_pipeline.py` and `collision_model.py` but there is no `src/visualizer.py` in the repo. Either add it or remove/replace the import before running.
- Duplicate/embedded script: `src/collision_model.py` contains both function definitions and a duplicated `main()` script block (and extra imports) appended to the file. This is a maintenance issue and can confuse static analysis tools — prefer extracting the script into `run_pipeline.py` (which already exists).
- Module import side-effects: `run_pipeline.py` prints `"[INFO] Starting the space debris risk pipeline..."` at the bottom of the file after the `if __name__ == "__main__"` block, which causes output on import. Avoid importing that module from tests.
- No tests currently present (`tests/` is empty). Add unit tests for `compute_pairwise_distance` and `detect_conjunction` using small deterministic arrays and mock Skyfield loads.

## Examples of safe edits an AI agent can make
- Add a lightweight `src/visualizer.py` implementing `plot_distance(x, dist, name1, name2)` using `matplotlib` to make `run_pipeline.py` runnable.
- Move the duplicate `main()` from `collision_model.py` into `run_pipeline.py` (or remove the duplicate block) to avoid repeating logic.
- Replace the hard-coded date in `compute_positions` with parameters and sensible defaults to make the simulator reusable in tests.

## Testing & debugging tips
- When testing code that uses `skyfield.load.tle_file(url)`, patch that call to return a small list of fake satellite objects to avoid network dependency.
- Quick smoke test (after creating a `visualizer` stub): `python run_pipeline.py` (from repo root) should load TLEs and print the result counter.

## When to ask for human help
- If satellite names from Celestrak don't match the hard-coded names used by the scripts, ask the repo maintainer which canonical names to use.
- If you need to add long-running simulation features (many minutes or smaller intervals), confirm expected performance targets — current code assumes small arrays and in-memory processing.

---
If any section is unclear or you want me to expand examples (tests, a `visualizer` stub, or a clean-up PR removing duplicated code), tell me which part and I'll update accordingly.
