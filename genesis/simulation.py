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

        if self.config.reproduction_mode == "fixed":
            reproduction_start_age = (
                self.config.default_reproduction_start_age
            )
        else:
            reproduction_start_age = random.randint(
                self.config.minimum_reproduction_start_age,
                self.config.maximum_reproduction_start_age,
            )

        return Person(
            id=person_id,
            name=name,
            sex=sex,
            birth_year=self.current_year,
            father_id="P00001",
            mother_id="P00002",
            reproduction_start_age=reproduction_start_age,
        )

    def run(self) -> None:
        """Run the simulation."""

        random.seed(self.config.random_seed)

        print("\nStarting simulation...\n")

        end_year = self.config.simulation_end_year

        for year in range(end_year + 1):
            self.current_year = year

            births_this_year: list[Person] = []

            # Adam and Eve continue having children.
            if (
                year >= self.config.first_birth_year
                and (year - self.config.first_birth_year)
                % self.config.birth_interval
                == 0
            ):
                child = self.create_child()
                self.population[child.id] = child
                births_this_year.append(child)

            print(f"Year {year:3}  Population: {self.population_count}")

            for child in births_this_year:
                sex = "Male" if child.sex == "M" else "Female"
                print(
                    f"    Birth: {child.name} ({sex}) "
                    f"[Reproduction Start Age: "
                    f"{child.reproduction_start_age}]"
                )

            # Show when someone first becomes eligible to reproduce.
            for person in self.population.values():
                if (
                    person.reproduction_start_age is not None
                    and person.age(year)
                    == person.reproduction_start_age
                ):
                    print(
                        f"    Eligible: {person.name} "
                        f"(Age {person.age(year)})"
                    )

        print("\nSimulation complete.")