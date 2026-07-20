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