"""Pairing engine for marriage rules and strategy selection."""

import random
from dataclasses import dataclass, field
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
class AppearanceMatchRule:
    match_traits: list[str] = field(default_factory=list)

    def allows(self, husband: Person, wife: Person, current_year: int) -> bool:
        for trait in self.match_traits:
            if getattr(husband, trait) != getattr(wife, trait):
                return False

        return True


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
class PreferenceMatchRule:
    preferred_partner_traits: dict[str, dict[str, dict[str, int]]]

    def score(self, husband: Person, wife: Person) -> int:
        _, _, total_score, _ = self.score_breakdown(husband, wife)
        return total_score

    def score_breakdown(
        self,
        husband: Person,
        wife: Person,
    ) -> tuple[int, int, int, list[tuple[str, str | None, str | None, int, int]]]:
        husband_score = 0
        wife_score = 0
        breakdown: list[tuple[str, str | None, str | None, int, int]] = []

        for trait, preferences in self.preferred_partner_traits.items():
            husband_value = getattr(husband, trait, None)
            wife_value = getattr(wife, trait, None)

            husband_points = 0
            wife_points = 0
            if husband_value in preferences:
                husband_points = preferences[husband_value].get(wife_value, 0)
            if wife_value in preferences:
                wife_points = preferences[wife_value].get(husband_value, 0)

            husband_score += husband_points
            wife_score += wife_points
            breakdown.append((trait, husband_value, wife_value, husband_points, wife_points))

        return husband_score, wife_score, husband_score + wife_score, breakdown


@dataclass(slots=True)
class PairingEngine:
    strategy: str
    rules: list[PairingRule]
    preference_rule: PreferenceMatchRule | None = None
    minimum_preference_score: int = 0
    preference_score_relaxation_per_year: int = 0
    preference_score_relaxation_age_start: int | None = None
    spark_min: int = -15
    spark_max: int = 15
    debug: bool = False

    @classmethod
    def from_config(cls, config: Config) -> "PairingEngine":
        rules: list[PairingRule] = []
        preference_rule: PreferenceMatchRule | None = None

        if config.maximum_age_difference is not None:
            rules.append(MaxAgeDifferenceRule(config.maximum_age_difference))

        match_traits: list[str] = []
        if config.match_partner_hair_color:
            match_traits.append("hair_color")
        if config.match_partner_eye_color:
            match_traits.append("eye_color")

        if match_traits:
            rules.append(AppearanceMatchRule(match_traits=match_traits))

        if config.preferred_partner_traits:
            preference_rule = PreferenceMatchRule(
                preferred_partner_traits=config.preferred_partner_traits
            )

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

        return cls(
            strategy=config.pairing_strategy,
            rules=rules,
            preference_rule=preference_rule,
            minimum_preference_score=config.minimum_preference_score,
            preference_score_relaxation_per_year=
                config.preference_score_relaxation_per_year,
            preference_score_relaxation_age_start=
                config.preference_score_relaxation_age_start,
            spark_min=config.spark_min,
            spark_max=config.spark_max,
            debug=config.pairing_debug,
        )

    def find_matches(
        self,
        males: list[Person],
        females: list[Person],
        current_year: int,
    ) -> list[tuple[Person, Person, int]]:
        males = sorted(males, key=lambda person: person.birth_year)
        females = sorted(females, key=lambda person: person.birth_year)

        if self.strategy == "youngest_first":
            males = sorted(males, key=lambda person: person.birth_year, reverse=True)
            females = sorted(females, key=lambda person: person.birth_year, reverse=True)

        matches: list[tuple[Person, Person, int]] = []
        available_females = list(females)

        if self.debug:
            print("Pairing debug:")
            print(f"  strategy={self.strategy} year={current_year}")
            print(f"  males={len(males)} females={len(females)}")

        for husband in males:
            result = self._find_partner(husband, available_females, current_year)
            if result is not None:
                wife, score = result
                matches.append((husband, wife, score))
                available_females.remove(wife)

        return matches

    def _find_partner(
        self,
        husband: Person,
        candidates: list[Person],
        current_year: int,
    ) -> tuple[Person, int] | None:
        age = husband.age(current_year)
        threshold = self._preference_threshold(age)

        # Only print husband header if we later find a candidate that passes
        # all rules (user requested debug show only passing candidates).
        printed_husband_header = False

        if self.preference_rule is None:
            for wife in candidates:
                # Evaluate rules first; only print debug for candidates that pass
                allowed = True
                failed_rules: list[str] = []
                for rule in self.rules:
                    if not rule.allows(husband, wife, current_year):
                        allowed = False
                        failed_rules.append(rule.__class__.__name__)

                if not allowed:
                    continue

                if self.debug and not printed_husband_header:
                    printed_husband_header = True
                    print(f"  Husband {husband.name} ({husband.id}) age={age}")
                    print(
                        f"    hair={husband.hair_color} tone={husband.hair_tone} "
                        f"eye={husband.eye_color} shade={husband.eye_shade}"
                    )
                    if self.preference_rule is not None:
                        print(f"    threshold={threshold}")

                if self.debug:
                    print(
                        f"    Trying wife {wife.name} ({wife.id}) "
                        f"hair={wife.hair_color} tone={wife.hair_tone} "
                        f"eye={wife.eye_color} shade={wife.eye_shade}"
                    )
                    print(
                        f"      rules_pass=True failed=none"
                    )

                if self.debug:
                    print(f"    Selected {wife.name} ({wife.id})")
                return wife, 0

        chosen_partner: Person | None = None
        best_score: int | None = None

        for wife in candidates:
            # Evaluate rules first; skip silent for those that fail
            allowed = True
            failed_rules = []
            for rule in self.rules:
                if not rule.allows(husband, wife, current_year):
                    allowed = False
                    failed_rules.append(rule.__class__.__name__)

            if not allowed:
                continue

            if self.debug and not printed_husband_header:
                printed_husband_header = True
                print(f"  Husband {husband.name} ({husband.id}) age={age}")
                print(
                    f"    hair={husband.hair_color} tone={husband.hair_tone} "
                    f"eye={husband.eye_color} shade={husband.eye_shade}"
                )
                if self.preference_rule is not None:
                    print(f"    threshold={threshold}")

            if self.debug:
                print(
                    f"    Trying wife {wife.name} ({wife.id}) "
                    f"hair={wife.hair_color} tone={wife.hair_tone} "
                    f"eye={wife.eye_color} shade={wife.eye_shade}"
                )
                print(
                    f"      rules_pass=True failed=none"
                )

            husband_score, wife_score, score, breakdown = self.preference_rule.score_breakdown(husband, wife)
            if self.debug:
                print(
                    f"      husband->wife_score={husband_score} "
                    f"wife->husband_score={wife_score} "
                    f"total_score={score}"
                )
                for trait, husband_value, wife_value, husband_points, wife_points in breakdown:
                    print(
                        f"        {trait}: "
                        f"husband({husband_value})->wife({wife_value})={husband_points} "
                        f"wife({wife_value})->husband({husband_value})={wife_points}"
                    )

            final_score = self._final_compatibility_score(score)

            if final_score < threshold:
                if self.debug:
                    print(
                        f"      rejected: below threshold {threshold}"
                    )
                continue

            if chosen_partner is None or final_score > best_score:
                chosen_partner = wife
                best_score = final_score
                if self.debug:
                    print(
                        f"      new best partner {wife.name} ({wife.id}) "
                        f"score={final_score}"
                    )

        if chosen_partner is not None:
            if self.debug:
                print(
                    f"    Selected {chosen_partner.name} ({chosen_partner.id}) "
                    f"score={best_score or 0}"
                )
            return chosen_partner, best_score or 0

        return None

    def _final_compatibility_score(self, attraction_score: int) -> int:
        return attraction_score + random.randint(self.spark_min, self.spark_max)

    def _preference_threshold(self, age: int) -> int:
        threshold = self.minimum_preference_score
        if (
            self.preference_score_relaxation_age_start is not None
            and age > self.preference_score_relaxation_age_start
        ):
            years_over = age - self.preference_score_relaxation_age_start
            threshold = max(
                0,
                threshold - self.preference_score_relaxation_per_year * years_over,
            )
        return threshold
