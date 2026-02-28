## Ambulance Dispatch System

This project contains two prototype dispatch engines for emergency vehicle routing.

## Project Structure

<!-- directories not included; see implementation files below -->
- `data/` - CSV simulation files
- `documentation/` - Project documentation
- `testing/` - Performance testing results

## Prototypes

### Prototype 1 (Dijkstra)
- Implements Dijkstra's shortest-path search for weighted road networks.

### Prototype 2 (A*)
- Implements the A* algorithm with heuristics for faster route planning.

## Data Files

The `data/` directory contains CSV files used for simulation:

- `ambulances.csv` - staging locations
- `routes.csv` - road network distances and travel times
- `call_priority.csv` - emergency call priorities
- `calls.csv` - sample call logs