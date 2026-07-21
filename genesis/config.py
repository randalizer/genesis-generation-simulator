"""
Configuration loader.
"""

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(slots=True)
class Config:
    simulation_end_year: int

    first_birth_year: int
    birth_interval: int

    reproduction_mode: str

    minimum_reproduction_start_age: int
    maximum_reproduction_start_age: int
    default_reproduction_start_age: int

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