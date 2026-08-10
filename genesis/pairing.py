"""Pairing engine for marriage rules and strategy selection."""

from dataclasses import dataclass
from typing import Protocol

from genesis.person import Person
from genesis.config import Config


class PairingRule(Protocol):
    def allows(self, husband: Person, wife: Person, current_year: int) -> bool:
        ...


@dataclass(slots=True)
class MaxAgeDifferenceRule:
    max_age_difference: int

    def allows(self, husband: Person, wife: Person, current_year: int) -> bool:
        return abs(husband.age(current_year) - wife.age(current_year)) <= self.max_age_difference


@dataclass(slots=True)
class PreferredAgeRangeRule:
    min_age: int | None = None
    max_age: int | None = None
    target_sex: str = "F"

    def allows(self, husband: Person, wife: Person, current_year: int) -> bool:
        if self.target_sex == "M":
            age = husband.age(current_year)
        else:
            age = wife.age(current_year)

        if self.min_age is not None and age < self.min_age:
            return False
        if self.max_age is not None and age > self.max_age:
            return False

        return True


@dataclass(slots=True)
class PairingEngine:
    strategy: str
    rules: list[PairingRule]

    @classmethod
    def from_config(cls, config: Config) -> "PairingEngine":
        rules: list[PairingRule] = []

        if config.maximum_age_difference is not None:
            rules.append(MaxAgeDifferenceRule(config.maximum_age_difference))

        if config.preferred_husband_age_min is not None:
            rules.append(
                PreferredAgeRangeRule(
                    min_age=config.preferred_husband_age_min,
                    target_sex="M",
                )
            )

        if config.preferred_wife_age_min is not None:
            rules.append(
                PreferredAgeRangeRule(
                    min_age=config.preferred_wife_age_min,
                    target_sex="F",
                )
            )

        return cls(strategy=config.pairing_strategy, rules=rules)

    def find_matches(
        self,
        males: list[Person],
        females: list[Person],
        current_year: int,
    ) -> list[tuple[Person, Person]]:
        males = sorted(males, key=lambda person: person.birth_year)
        females = sorted(females, key=lambda person: person.birth_year)

        if self.strategy == "youngest_first":
            males = sorted(males, key=lambda person: person.birth_year, reverse=True)
            females = sorted(females, key=lambda person: person.birth_year, reverse=True)

        matches: list[tuple[Person, Person]] = []
        available_females = list(females)

        for husband in males:
            partner = self._find_partner(husband, available_females, current_year)
            if partner is not None:
                matches.append((husband, partner))
                available_females.remove(partner)

        return matches

    def _find_partner(
        self,
        husband: Person,
        candidates: list[Person],
        current_year: int,
    ) -> Person | None:
        for wife in candidates:
            if all(rule.allows(husband, wife, current_year) for rule in self.rules):
                return wife

        return None
