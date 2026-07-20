# Genesis Generation Simulator

A configurable population simulation engine for exploring early Genesis genealogical assumptions.

## Current Version

v0.1.0

## Goals

- Load simulation configuration from JSON.
- Load an initial seed population from JSON.
- Display the loaded population.
- Provide a clean foundation for future population simulation logic.

## Requirements

- Python 3.12+

## Running

```bash
python3 main.py
```

## Expected Output

```text
============================================================
Genesis Generation Simulator v0.1.0
============================================================

Loading configuration...
Configuration loaded.

Loading seed population...
Loaded 2 people.

ID       Name    Sex  Birth Year
--------------------------------
P00001   Adam     M      0
P00002   Eve      F      0

Ready to simulate.
```

## Project Structure

```text
genesis-generation-simulator/
├── README.md
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── config.json
├── seed_people.json
├── main.py
├── genesis/
│   ├── __init__.py
│   ├── version.py
│   ├── person.py
│   └── config.py
├── output/
└── tests/
```

## Next Milestones

- Add simulation engine.
- Add deterministic pairing.
- Add birth generation.
- Add CSV reporting.
- Add timeline reporting.
