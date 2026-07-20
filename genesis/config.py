"""
Configuration loader.
"""
from pathlib import Path
from dataclasses import dataclass
import json


@dataclass(slots=True)
class Config:
    simulation_end_year: int
    first_birth_year: int
    birth_interval: int

    minimum_childbearing_age: int
    maximum_childbearing_age: int

    childbearing_mode: str
    default_childbearing_age: int

    pairing_strategy: str

    male_birth_probability: float

    random_seed: int


def load_config(path: str | Path) -> Config:
    """
    Load configuration from a JSON file.
    """

    path = Path(path)

    with path.open("r", encoding="utf-8") as infile:
        data = json.load(infile)

    return Config(**data)