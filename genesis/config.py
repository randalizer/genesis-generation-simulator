"""
Configuration loader.
"""

from dataclasses import dataclass, field
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

    minimum_marriage_age: int

    pairing_strategy: str
    male_birth_probability: float
    random_seed: int

    hair_color_inheritance: dict[str, dict[str, dict[str, int]]]
    eye_color_inheritance: dict[str, dict[str, dict[str, int]]]

    pairing_debug: bool = False

    hair_colors: list[str] = field(default_factory=lambda: ["brown", "black", "blonde", "red"])
    eye_colors: list[str] = field(default_factory=lambda: ["brown", "blue", "green", "hazel"])
    hair_tone_min: int = 1
    hair_tone_max: int = 10
    eye_shade_min: int = 1
    eye_shade_max: int = 10

    desire_for_children_min: int = 0
    desire_for_children_max: int = 100
    child_decision_threshold: int = 100
    desire_reduction_per_child: int = 1
    child_decision_spark_min: int = -25
    child_decision_spark_max: int = 25
    desire_for_children_min: int = 0
    desire_for_children_max: int = 100
    desire_for_children_mean: int = 50
    desire_for_children_stddev: int = 15

    match_partner_hair_color: bool = False
    match_partner_eye_color: bool = False
    preferred_partner_traits: dict[str, dict[str, dict[str, int]]] = field(default_factory=dict)
    minimum_preference_score: int = 0
    preference_score_relaxation_per_year: int = 0
    preference_score_relaxation_age_start: int | None = None
    spark_min: int = -15
    spark_max: int = 15

    preferred_husband_age_min: int | None = None
    preferred_wife_age_min: int | None = None

    maximum_age_difference: int | None = None
    debug_mode: bool = False


def load_config(path: str | Path) -> Config:
    """
    Load configuration from a JSON file.
    """

    path = Path(path)

    with path.open("r", encoding="utf-8") as infile:
        data = json.load(infile)

    return Config(**data)