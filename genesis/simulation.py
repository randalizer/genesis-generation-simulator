"""
Simulation engine for the Genesis Generation Simulator.
"""

from typing import Dict

from genesis.person import Person


class Simulation:
    """Runs the year-by-year simulation."""

    def __init__(self, config: dict, people: Dict[str, Person]) -> None:
        self.config = config
        self.people = people
        self.current_year = 0

    @property
    def population(self) -> int:
        """Return the current population."""
        return len(self.people)

    def run(self) -> None:
        """Run the simulation."""

        end_year = self.config.simulation_end_year

        print("\nStarting simulation...\n")

        for year in range(end_year + 1):
            self.current_year = year
            print(f"Year {year:3}  Population: {self.population}")

        print("\nSimulation complete.")