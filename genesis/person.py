"""
Person model.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Person:
    """
    Represents a single individual in the simulation.
    """

    id: str
    name: str
    sex: str
    birth_year: int
