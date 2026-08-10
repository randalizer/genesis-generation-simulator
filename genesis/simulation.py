"""
Simulation engine for the Genesis Generation Simulator.
"""

import random

from genesis import family
from genesis.config import Config
from genesis.person import Person
from genesis.family import Family
from genesis.pairing import PairingEngine


class Simulation:
    """Runs the year-by-year simulation."""

    def __init__(self, config: Config, population: dict[str, Person]) -> None:
        self.config = config
        self.population = population
        self.families: dict[str, Family] = {}
        self.current_year = 0

        # Determine the next available person number.
        self.next_person_number = max(
            int(person.id[1:]) for person in self.population.values()
        )

        self.pairing_engine = PairingEngine.from_config(config)

        self.add_family(
            Family(
                id="F00001",
                husband_id="P00001",
                wife_id="P00002",
                marriage_year=0,
            )
        )

        self.next_family_number = max(
            int(family.id[1:]) for family in self.families.values()
        )
        

    @property
    def population_count(self) -> int:
        """Return the current population."""
        return len(self.population)

    def create_child(self, family: Family) -> Person:
        """Create one child for Adam and Eve."""

        self.next_person_number += 1

        person_id = f"P{self.next_person_number:05d}"
        name = f"Person-{self.next_person_number:05d}"
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

        child = Person(
            id=person_id,
            name=name,
            sex=sex,
            birth_year=self.current_year,
            father_id=family.husband_id,
            mother_id=family.wife_id,
            reproduction_start_age=reproduction_start_age,
        )

        family.add_child(child.id)

        return child
    
    def get_family(self, family_id: str) -> Family:
        """Return a family by its ID."""
        return self.families[family_id]
    
    def add_family(self, family: Family) -> None:
        """Add a family to the simulation."""
        self.families[family.id] = family

    def add_person(self, person: Person) -> None:
        """Add a person to the simulation."""
        self.population[person.id] = person

    def eligible_for_marriage(self) -> list[Person]:
        """Return all people eligible for marriage."""

        eligible: list[Person] = []

        for person in self.population.values():
            age = person.age(self.current_year)

            if age < self.config.minimum_marriage_age:
                continue
            if self.is_married(person):
                continue
            if (
                person.reproduction_start_age is not None
                and not person.can_reproduce(self.current_year)
            ):
                continue

            eligible.append(person)

        return eligible
    
    def eligible_males(self) -> list[Person]:
        """Return all eligible unmarried males."""

        return [
            person
            for person in self.eligible_for_marriage()
                if person.sex == "M"
        ]

    def eligible_females(self) -> list[Person]:
        """Return all eligible unmarried females."""

        return [
            person
            for person in self.eligible_for_marriage()
            if person.sex == "F"
        ]
    
    def find_family_candidates(self) -> list[tuple[Person, Person]]:
        """Return the list of marriages for the current year."""

        return self.pairing_engine.find_matches(
            self.eligible_males(),
            self.eligible_females(),
            self.current_year,
        )

    def is_married(self, person: Person) -> bool:
        """Return True if the person is already a spouse in a family."""

        for family in self.families.values():
            if (
                family.husband_id == person.id
                or family.wife_id == person.id
            ):
                return True

        return False
    
    def create_family(
        self,
        husband: Person,
        wife: Person,
    ) -> Family:
        """Create a new family."""

        self.next_family_number += 1

        family = Family(
            id=f"F{self.next_family_number:05d}",
            husband_id=husband.id,
            wife_id=wife.id,
            marriage_year=self.current_year,
        )

        return family

    def run(self) -> None:
        """Run the simulation."""

        random.seed(self.config.random_seed)

        print("\nStarting simulation...\n")

        end_year = self.config.simulation_end_year

        for year in range(end_year + 1):
            self.current_year = year

            births_this_year: list[tuple[Person, Family]] = []

            print(f"Year {year:3}  Population: {self.population_count}")

            for family in self.families.values():
                print(
                    f"    {family.id}: "
                    f"Married {family.marriage_duration(year)} years"
                )   

                if (
                    year >= self.config.first_birth_year
                    and (year - self.config.first_birth_year)
                    % self.config.birth_interval
                    == 0
                ):
                    child = self.create_child(family)
                    self.add_person(child)
                    births_this_year.append((child, family))

                    sex = "Male" if child.sex == "M" else "Female"
                    print(
                        f"        Birth: {child.name} ({sex}) "
                        f"[Family: {family.id}]"
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

            candidates = self.find_family_candidates()
            print(f"Year {year}: {len(candidates)} family candidates")
            for husband, wife in candidates:
                family = self.create_family(husband, wife)
                self.add_family(family)
                print(
                    f"    Created family {family.id}:"
                    f"\n        Husband: {husband.name} "
                    f"(Male, Age {husband.age(year)})"
                    f"\n        Wife: {wife.name} "
                    f"(Female, Age {wife.age(year)})"
                )

        print("\nSimulation complete.")
        print(
            f"Total population: {self.population_count}  "
            f"Total families: {len(self.families)}"
        )