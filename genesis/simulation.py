"""
Simulation engine for the Genesis Generation Simulator.
"""

import random
import sys
import termios
import tty
import csv

from collections.abc import Callable

from genesis import family
from genesis.config import Config
from genesis.person import Person
from genesis.family import Family
from genesis.pairing import PairingEngine
from genesis.year_result import YearResult
from pathlib import Path


class Simulation:
    """Runs the year-by-year simulation."""

    def __init__(self, config: Config, population: dict[str, Person]) -> None:
        self.config = config
        self.population = population
        self.families: dict[str, Family] = {}
        self.current_year = 0

        self.married_person_ids: set[str] = set()

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

    def child_desire_score(
        self,
        family: Family,
    ) -> int:
        """Return the child decision score for a family."""

        husband = self.population[family.husband_id]
        wife = self.population[family.wife_id]

        combined_desire = (
            husband.desire_for_children
            + wife.desire_for_children
        )

        spark = random.randint(
            self.config.child_decision_spark_min,
            self.config.child_decision_spark_max,
        )
        return combined_desire + spark

    def family_wants_child(
        self,
        family: Family,
    ) -> bool:
        """Return True if the family decides to have a child."""

        score = self.child_desire_score(family)

        return score >= self.config.child_decision_threshold

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

        desire_for_children = round(
            random.gauss(
                self.config.desire_for_children_mean,
                self.config.desire_for_children_stddev,
            )
        )

        desire_for_children = max(
            self.config.desire_for_children_min,
            min(
                self.config.desire_for_children_max,
                desire_for_children,
            ),
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

        father = self.population[family.husband_id]
        mother = self.population[family.wife_id]

        hair_color = self._inherit_color_trait(
            father.hair_color,
            mother.hair_color,
            self.config.hair_color_inheritance,
        )
        hair_tone = self._inherit_hair_tone(father, mother)
        eye_color = self._inherit_eye_color(father, mother)
        eye_shade = self._inherit_eye_shade(father, mother)

        child = Person(
            id=person_id,
            name=name,
            sex=sex,
            birth_year=self.current_year,
            father_id=family.husband_id,
            mother_id=family.wife_id,
            hair_color=hair_color,
            hair_tone=hair_tone,
            eye_color=eye_color,
            eye_shade=eye_shade,
            reproduction_start_age=reproduction_start_age,
            desire_for_children=desire_for_children,
        )

        father.desire_for_children = max(
            0,
            father.desire_for_children
            - self.config.desire_reduction_per_child,
        )

        mother.desire_for_children = max(
            0,
            mother.desire_for_children
            - self.config.desire_reduction_per_child,
        )

        family.add_child(child.id)

        return child

    def _inherit_color_trait(
        self,
        father_trait: str,
        mother_trait: str,
        inheritance_table: dict[str, dict[str, dict[str, int]]],
        normalize: Callable | None = None,
    ) -> str:
        if normalize is not None:
            father_trait = normalize(father_trait)
            mother_trait = normalize(mother_trait)

        if father_trait == mother_trait:
            return father_trait

        weights = self._trait_weights(
            father_trait, mother_trait, inheritance_table
        )
        if weights is not None:
            return self._weighted_choice(list(weights.items()))

        return random.choice([father_trait, mother_trait])

    def _trait_weights(
        self,
        father_trait: str,
        mother_trait: str,
        inheritance: dict[str, dict[str, dict[str, int]]],
    ) -> dict[str, int] | None:
        if father_trait in inheritance:
            if mother_trait in inheritance[father_trait]:
                weights = inheritance[father_trait][mother_trait]
                if sum(weights.values()) > 0:
                    return weights
        if mother_trait in inheritance:
            if father_trait in inheritance[mother_trait]:
                weights = inheritance[mother_trait][father_trait]
                if sum(weights.values()) > 0:
                    return weights
        return None

    def _weighted_choice(self, options: list[tuple[str, int]]) -> str:
        total = sum(weight for _, weight in options)
        pick = random.randrange(total)
        current = 0
        for value, weight in options:
            current += weight
            if pick < current:
                return value
        return options[-1][0]

    def _inherit_hair_tone(self, father: Person, mother: Person) -> int:
        return random.randint(
            min(father.hair_tone, mother.hair_tone),
            max(father.hair_tone, mother.hair_tone),
        )

    def _inherit_eye_color(self, father: Person, mother: Person) -> str:
        return self._inherit_color_trait(
            father.eye_color,
            mother.eye_color,
            self.config.eye_color_inheritance,
        )

    def _inherit_eye_shade(self, father: Person, mother: Person) -> int:
        return random.randint(
            min(father.eye_shade, mother.eye_shade),
            max(father.eye_shade, mother.eye_shade),
        )

    def get_family(self, family_id: str) -> Family:
        """Return a family by its ID."""
        return self.families[family_id]
        
    def add_family(self, family: Family) -> None:
        """Add a family to the simulation."""

        self.families[family.id] = family

        self.married_person_ids.add(family.husband_id)
        self.married_person_ids.add(family.wife_id)

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
    def eligible_people_by_sex(
        self,
    ) -> tuple[list[Person], list[Person]]:
        """Return eligible unmarried males and females."""

        males: list[Person] = []
        females: list[Person] = []

        for person in self.population.values():
            age = person.age(self.current_year)

            if age < self.config.minimum_marriage_age:
                continue
            if self.is_married(person):
                continue

            if person.sex == "M":
                males.append(person)
            elif person.sex == "F":
                females.append(person)

        return males, females    
    
    def find_family_candidates(self) -> list[tuple[Person, Person, int]]:
        """Return the list of marriages for the current year."""

        eligible_males, eligible_females = (
            self.eligible_people_by_sex()
        )

        return self.pairing_engine.find_matches(
            eligible_males,
            eligible_females,
            self.current_year,
        )
    
    def is_married(self, person: Person) -> bool:
        """Return True if the person is already a spouse in a family."""

        return person.id in self.married_person_ids

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

    def wait_for_key(self) -> None:
        """Pause until the user presses any key."""

        print("\nPress any key to continue...", end="", flush=True)

        if not sys.stdin.isatty():
            input()
            return

        file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)

        try:
            tty.setcbreak(file_descriptor)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(
                file_descriptor,
                termios.TCSADRAIN,
                old_settings,
            )

        print()

    def run(self) -> None:
        """Run the simulation using the terminal interface."""

        if self.config.debug_mode:
            random.seed(self.config.random_seed)

        print("\nStarting simulation...\n")

        end_year = self.config.simulation_end_year

        for year in range(end_year + 1):
            result = self.run_year(year)

            print("=" * 60)
            print(f"Year {year}")
            print("=" * 60)

            # Display births.
            for child, family in result.births:
                sex = "Male" if child.sex == "M" else "Female"

                print(
                    f"\nBirth: {child.name} ({sex}) "
                    f"[Family: {family.id}]"
                )
                print(
                    f"    Hair: {child.hair_color} "
                    f"(Tone {child.hair_tone})"
                )
                print(
                    f"    Eyes: {child.eye_color} "
                    f"(Shade {child.eye_shade})"
                )

            # Display marriages.
            for family in result.families_created:
                husband = self.population[family.husband_id]
                wife = self.population[family.wife_id]

                husband_father = self.population.get(husband.father_id)
                husband_mother = self.population.get(husband.mother_id)

                wife_father = self.population.get(wife.father_id)
                wife_mother = self.population.get(wife.mother_id)

                print(f"\nFamily Created: {family.id}")

                print(
                    f"    Husband: {husband.name} "
                    f"(Male, Age {husband.age(year)})"
                )
                print(
                    f"        Father: "
                    f"{husband_father.name if husband_father else 'Unknown'}"
                )
                print(
                    f"        Mother: "
                    f"{husband_mother.name if husband_mother else 'Unknown'}"
                )

                print(
                    f"\n    Wife: {wife.name} "
                    f"(Female, Age {wife.age(year)})"
                )
                print(
                    f"        Father: "
                    f"{wife_father.name if wife_father else 'Unknown'}"
                )
                print(
                    f"        Mother: "
                    f"{wife_mother.name if wife_mother else 'Unknown'}"
                )

            # End-of-year summary.
            print(f"\nYear {year} Summary")
            print()
            print(f"{'Current Year':<25}{'Total':<25}")
            print(f"{'-' * 20:<25}{'-' * 20:<25}")
            print(
                f"{'Births:':<12}{result.birth_count:<13}"
                f"{'Population:':<15}{result.population_count}"
            )
            print(
                f"{'Marriages:':<12}{result.marriage_count:<13}"
                f"{'Families:':<15}{result.family_count}"
            )

            #self.wait_for_key()
            print()

        print("=" * 60)
        print("Simulation Complete")
        print("=" * 60)
        print(f"Total population: {self.population_count}")
        print(f"Total families:   {len(self.families)}")

    def run_year(self, year: int) -> YearResult:
        """Run one year of the simulation and return the results."""

        self.current_year = year

        births_this_year: list[tuple[Person, Family]] = []
        families_created_this_year: list[Family] = []

        # Process births for existing families.
        for family in list(self.families.values()):
            if self.family_wants_child(family):
                child = self.create_child(family)
                self.add_person(child)
                births_this_year.append((child, family))

        # Find and create new families.
        candidates = self.find_family_candidates()

        for husband, wife, score in candidates:
            family = self.create_family(husband, wife)
            self.add_family(family)
            families_created_this_year.append(family)

        result = YearResult(
            year=year,
            births=births_this_year,
            families_created=families_created_this_year,
            population_count=self.population_count,
            family_count=len(self.families),
        )      

        self.log_year_result(result)

        return result
      
    def log_year_result(
        self,
        result: YearResult,
        filename: str = "simulation_yearly.csv",
    ) -> None:
        """Append one year's simulation results to a CSV file."""

        file_exists = Path(filename).exists()

        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(
                    [
                        "year",
                        "population",
                        "families",
                        "births",
                        "marriages",
                    ]
                )

            writer.writerow(
                [
                    result.year,
                    result.population_count,
                    result.family_count,
                    result.birth_count,
                    result.marriage_count,
                ]
            )