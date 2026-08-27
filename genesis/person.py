"""
Person model for the Genesis Generation Simulator.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Person:
    """Represents one person in the simulation."""

    id: str
    name: str
    sex: str

    birth_year: int

    father_id: str | None = None
    mother_id: str | None = None

    alive: bool = True

    # Physical traits are inherited like DNA and can be extended later.
    hair_color: str = "brown"
    hair_tone: int = 5
    eye_color: str = "brown"
    eye_shade: int = 5

    # Age (in years) when this person begins reproducing.
    # Adam and Eve are special cases and do not use this value.
    reproduction_start_age: int | None = None

    def age(self, current_year: int) -> int:
        """Return the person's age in simulation years."""

        return current_year - self.birth_year

    def can_reproduce(self, current_year: int) -> bool:
        """
        Return True if this person has reached their
        reproduction start age.
        """

        if self.reproduction_start_age is None:
            return False

        return self.age(current_year) >= self.reproduction_start_age