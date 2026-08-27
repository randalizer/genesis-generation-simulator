"""
Genesis Generation Simulator
"""

import json
import random
from pathlib import Path

from genesis.config import Config, load_config
from genesis.person import Person
from genesis.simulation import Simulation
from genesis.version import __version__


def load_seed_people(filename: str, config: Config) -> dict[str, Person]:
    """Load the initial population from a JSON file."""

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    people = {}

    for item in data:
        person = Person(
            id=item["id"],
            name=item["name"],
            sex=item["sex"],
            birth_year=item["birth_year"],
            hair_color=item.get("hair_color", "brown"),
            hair_tone=item.get("hair_tone", 5),
            eye_color=item.get("eye_color", "brown"),
            eye_shade=item.get(
                "eye_shade",
                random.randint(config.eye_shade_min, config.eye_shade_max),
            ),
        )
        people[person.id] = person

    return people


def main() -> None:
    print("=" * 60)
    print(f"Genesis Generation Simulator v{__version__}")
    print("=" * 60)

    print("\nLoading configuration...")
    config = load_config("config.json")
    print("✓ Configuration loaded.")

    print("\nLoading seed population...")
    people = load_seed_people("seed_people.json", config)
    print(f"✓ Loaded {len(people)} people.\n")

    print("ID       Name     Sex  Birth Year")
    print("---------------------------------")

    for person in people.values():
        print(
            f"{person.id:<8} "
            f"{person.name:<8} "
            f"{person.sex:<4} "
            f"{person.birth_year}"
        )

    simulation = Simulation(config, people)
    simulation.run()


if __name__ == "__main__":
    main()