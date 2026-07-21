# Genesis Generation Simulator Architecture

## Project Goal

The Genesis Generation Simulator explores population growth described in the
early chapters of Genesis.

The simulator intentionally separates Biblical facts from configurable
assumptions so that different scenarios can be explored.

---

# Design Principles

1. Small, incremental development
2. One feature per sprint
3. Working code at the end of every sprint
4. Explicit assumptions
5. Simple code over clever code

---

# Current Architecture

```
main.py
    │
    ▼
Load Configuration
    │
    ▼
Load Seed Population
    │
    ▼
Create Simulation
    │
    ▼
Run Simulation
```

---

# Current Components

## config.py

Loads configuration from `config.json`.

Provides a strongly typed Config object.

---

## person.py

Defines the Person data model.

Each Person contains:

- ID
- Name
- Sex
- Birth Year
- Parent IDs
- Alive flag

---

## simulation.py

Controls the simulation loop.

Responsible for:

- Advancing simulation years
- Creating births
- Maintaining the population

---

## main.py

Application entry point.

Responsible for:

- Loading configuration
- Loading seed population
- Starting the simulation

---

# Configuration Philosophy

All assumptions should exist in `config.json`.

The simulation engine should avoid hard-coded assumptions whenever possible.

Examples include:

- Reproduction mode
- Birth interval
- Reproduction start age
- Pairing strategy

---

# Future Architecture

As the project grows, responsibilities will likely move into dedicated modules.

Example:

```
genesis/

    config.py

    person.py

    simulation.py

    reproduction.py

    pairing.py

    reporting.py
```

These modules will only be introduced when they simplify the code.

The project should avoid unnecessary complexity.

---

# Development Workflow

Each sprint should:

1. Implement one feature.
2. Keep the application working.
3. Update documentation.
4. Update CHANGELOG.
5. Update version.
6. Commit.
7. Tag.
8. Push.

---

# Long-Term Goal

Produce a configurable simulation capable of exploring different assumptions
about early population growth while clearly distinguishing between:

- Biblical facts
- Simulation assumptions