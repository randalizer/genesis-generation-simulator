"""
Family model for the Genesis Generation Simulator.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Family:
    """
    Represents a family established by a married couple.
    """

    id: str

    husband_id: str
    wife_id: str

    marriage_year: int

    reproduction_start_age: int | None = None

    first_birth_year: int | None = None

    birth_interval: int | None = None

    children: list[str] = field(default_factory=list)

    @property
    def child_count(self) -> int:
        """Return the number of children in the family."""
        return len(self.children)
    
    def add_child(self, child_id: str) -> None:
        """Add a child to the family."""
        self.children.append(child_id)

    def marriage_duration(self, current_year: int) -> int:
        """Return the number of years this family has been married."""
        return current_year - self.marriage_year