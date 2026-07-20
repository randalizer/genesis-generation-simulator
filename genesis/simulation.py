"""
Simulation engine for the Genesis Generation Simulator.
"""

import random

from genesis.config import Config
from genesis.person import Person


class Simulation:
    """Runs the year-by-year simulation."""

    def __init__(self, config: Config, population: dict[str, Person]) -> None:
        self.config = config
        self.population = population
        self.current_year = 0

        # Determine the next available person number.
        self.next_person_number = max(
            int(person.id[1:]) for person in self.population.values()
        )

    @property
    def population_count(self) -> int:
        """Return the current population."""
        return len(self.population)

    def create_child(self) -> Person:
        """Create one child for Adam and Eve."""

        self.next_person_number += 1

        person_id = f"P{self.next_person_number:05d}"
        name = f"Child-{self.next_person_number:05d}"

        sex = (
            "M"
            if random.random() < self.config.male_birth_probability
            else "F"
        )

        return Person(
            id=person_id,
            name=name,
            sex=sex,
            birth_year=self.current_year,
            father_id="P00001",
            mother_id="P00002",
        )

    def run(self) -> None:
        """Run the simulation."""

        random.seed(self.config.random_seed)

        print("\nStarting simulation...\n")

        end_year = self.config.simulation_end_year

        for year in range(end_year + 1):
            self.current_year = year

            # First birth only.
            if year == self.config.first_birth_year:
                child = self.create_child()
                self.population[child.id] = child

                sex = "Male" if child.sex == "M" else "Female"

                print(f"    Birth: {child.name} ({sex})")

            print(
                f"Year {year:3}  Population: {self.population_count}"
            )

        print("\nSimulation complete.")