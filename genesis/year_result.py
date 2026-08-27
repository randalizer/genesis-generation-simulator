"""
Year result model for the Genesis Generation Simulator.
"""

from dataclasses import dataclass, field

from genesis.family import Family
from genesis.person import Person


@dataclass(slots=True)
class YearResult:
    """Represents the results of one simulated year."""

    year: int

    births: list[tuple[Person, Family]] = field(default_factory=list)
    families_created: list[Family] = field(default_factory=list)

    population_count: int = 0
    family_count: int = 0

    @property
    def birth_count(self) -> int:
        """Return the number of births this year."""
        return len(self.births)

    @property
    def marriage_count(self) -> int:
        """Return the number of marriages this year."""
        return len(self.families_created)