#!/usr/bin/env python3
"""
Genesis Generation Simulator
"""

from pathlib import Path
import json

from genesis.version import __version__
from genesis.config import load_config
from genesis.person import Person


def load_seed_people(path: Path) -> list[Person]:
    """
    Load initial seed population.
    """

    with path.open("r", encoding="utf-8") as infile:
        data = json.load(infile)

    return [Person(**person) for person in data]


def main() -> None:
    """
    Application entry point.
    """

    print()
    print("=" * 60)
    print(f"Genesis Generation Simulator v{__version__}")
    print("=" * 60)

    print("\nLoading configuration...")

    config = load_config(Path("config.json"))

    print("✓ Configuration loaded.")

    print("\nLoading seed population...")

    people = load_seed_people(Path("seed_people.json"))

    print(f"✓ Loaded {len(people)} people.\n")

    print("ID       Name     Sex  Birth Year")
    print("---------------------------------")

    for person in people:
        print(
            f"{person.id:<8} "
            f"{person.name:<8} "
            f"{person.sex:<4} "
            f"{person.birth_year}"
        )

    print("\nReady to simulate.\n")


if __name__ == "__main__":
    main()
