# Changelog

## v0.1.0

- Initial project structure.
- Configuration loader.
- Seed population loader.
- Person dataclass.

## v0.2.0
- Create a Simulation class that advances through the years.

## v0.3.0
- Adam and Eve have children.

## [0.4.0] - 2026-07-21

### Changed
- Renamed childbearing configuration to reproduction terminology.
- Added reproduction_start_age to the Person model.
- Assigned a reproduction start age when each child is created.

### Internal
- Improved configuration naming for clarity and consistency.

## [0.5.0] - 2026-07-21

### Added
- Added `Person.age()` method to calculate a person's age in simulation years.
- Added `Person.can_reproduce()` method to determine when a person reaches their configured reproduction start age.
- Added a `reproduction_start_age` attribute to each newly created person.
- Configurable reproduction start age is now assigned to each child at birth using either:
  - Fixed mode (`default_reproduction_start_age`)
  - Random mode (`minimum_reproduction_start_age` to `maximum_reproduction_start_age`)

### Changed
- Continued refactoring toward an object-oriented simulation model by moving age and eligibility logic into the `Person` class.
- Added temporary diagnostic output showing each child's assigned reproduction start age and when individuals become eligible to reproduce.

### Notes
- This release does **not** implement pairing, marriage, or second-generation births.
- Eligibility tracking has been added as groundwork for future multi-generation simulation.
- During this sprint, it became clear that "reproduction_start_age" may not accurately represent the long-term simulation model. Future design work will distinguish between:
  - Pairing (marriage) eligibility
  - First child after pairing
  - Birth interval
  - End of reproductive years

  ## [0.6.0] - 2026-07-21

### Added
- Added the initial simulation model documentation.
- Defined the core architectural concepts of the simulator.
- Documented the responsibilities of the primary domain objects:
  - Simulation
  - Person
  - Family
- Added project design principles to guide future development.
- Added a roadmap section for future life events and simulation enhancements.

### Changed
- Refined the simulation terminology to better reflect the Genesis narrative.
- Adopted **Marriage** as the preferred term over **Pairing**.
- Established **Family** as the central long-lived entity for modeling generational growth.
- Clarified that data should be owned by the object it logically belongs to (Person vs. Family).

### Notes
- This release contains design and documentation improvements only.
- No simulation behavior or functionality changed.
- These architectural decisions establish the foundation for implementing multi-generational family simulation in future releases.