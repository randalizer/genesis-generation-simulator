# Changelog

## [v0.13.0] - Sprint 13

### Added
- Added a direct index of married person IDs for constant-time marriage-status checks.
- Added a single-pass eligibility scan that collects eligible males and females together.
- Added a lightweight preference scoring path for normal simulation runs.

### Changed
- Replaced repeated family scans in `is_married()` with direct set membership.
- Reduced population scanning during marriage eligibility processing.
- Removed duplicate sorting of eligible males and females during pairing.
- Replaced generator-based pairing rule checks with explicit short-circuit loops.
- Separated normal preference scoring from detailed debug score breakdown generation.
- Removed redundant trait normalization during inherited color processing.

### Performance
- Reduced marriage eligibility processing from a major simulation bottleneck to a negligible cost.
- Reduced unnecessary function calls, population scans, sorting, generator creation, and debug-data allocation.
- Established a deterministic performance benchmark using `debug_mode` and the configured random seed.
- Sprint 13 deterministic benchmark at Year 130:
  - Population: 9,924
  - Families: 1,853
  - Function calls: 2,709,621
  - Profiled runtime: approximately 1.47 seconds.
- Pairing remains the primary simulation cost and is intentionally deferred for architectural review rather than changing simulation behavior solely for performance.

### Notes
- Sprint 13 performance changes preserve the existing simulation model.
- Pairing currently evaluates all valid candidates when preference scoring is enabled in order to select the highest-scoring partner.
- Future pairing work should distinguish hard marriage eligibility from partner preferences and relationship decision-making.
- Potential future relationship modeling includes candidate encounters, courtship over time, age preferences rather than strictly fixed age limits, and remarriage behavior.
- These relationship-model changes are intentionally deferred to a future sprint because they would change simulation behavior rather than simply improve performance.

### Status
**Sprint 13 complete.**

## [v0.12.0] - Sprint 12

### Added
- Added `desire_for_children` as a Person personality trait.
- Added configurable minimum and maximum desire-for-children values.
- Added configurable bell-curve generation for newborn desire-for-children values.
- Added configurable desire-for-children mean and standard deviation.
- Added yearly family child-decision scoring.
- Added configurable child-decision threshold.
- Added configurable child-decision Spark range.
- Added configurable desire reduction after each child.
- Added yearly simulation CSV logging.
- Added `debug_mode` for reproducible simulations using `random_seed`.

### Changed
- Reproduction decisions are now made independently by each family every year.
- Removed the old global birth-interval schedule from yearly birth processing.
- Child decisions now use the combined desire-for-children values of both parents plus a yearly random Spark.
- Both parents' desire-for-children values decrease after the birth of a child.
- Newborn desire-for-children values now use a configurable normal distribution instead of a uniform random distribution.
- Normal simulation runs no longer automatically reset the random number generator to the configured seed.
- `random_seed` is applied only when `debug_mode` is enabled.

### Fixed
- Restored child IDs to the Family record when children are created.
- Restored family child counts and child listings in the GUI.
- Prevented normal CLI simulations from unintentionally producing identical repeated runs.

### Notes
- Testing showed that the desire-for-children distribution has a significant effect on long-term population growth.
- Bell-curve generation reduced the frequency of extreme initial desire values and produced more natural clustering around the configured mean.
- Independent randomized runs demonstrated substantial population variation caused by compounding early simulation events.
- Debug mode provides deterministic runs for reproducing and investigating simulation behavior.
- Performance and scalability work is deferred to Sprint 13.

### Status
**Sprint 12 complete.**

## [v0.11.0] - Sprint 11

### Added

- New `YearResult` model for structured yearly simulation results.
- New `Simulation.run_year()` method to process one simulation year independently of the user interface.
- New Tkinter graphical interface in `gui.py`.
- Current Year and Total two-column GUI layout.
- Scrollable lists for:
  - Births this year
  - Families created this year
  - All people
  - All families
- Person detail windows.
- Family detail windows.
- `Next Year`, `Run`, and `Pause` simulation controls.
- Adjustable delay between automatically simulated years.

### Changed

- Separated yearly simulation processing from terminal presentation.
- Updated terminal simulation flow to use structured yearly results.
- GUI treats Year 0 as the initial simulation state and begins advancement with Year 1.
- Person and family detail views can be opened from both current-year and total lists.

### Notes

- Sprint 11 focused on separating simulation logic from presentation and introducing the first graphical interface.
- The GUI now provides both current-year activity and cumulative simulation data.
- GUI testing exposed synchronized marriage waves caused by the existing global birth schedule.
- Family-specific reproduction timing is intentionally deferred to a future sprint.

### Status

**Sprint 11 complete.**

## [v0.10.0] - Sprint 10

### Added
- New rule-based marriage pairing engine in `genesis/pairing.py`.
- Support for `maximum_age_difference` as the primary spouse age-gap constraint.

### Changed
- Simplified config schema and removed gender-specific max-age caps.
- Integrated pairing logic into simulation via `PairingEngine.from_config()`.

### Notes
- Sprint 10 focused on marriage pairing architecture and eligibility rules.
- The simulator now supports maximum age gap constraints while keeping future remarriage rules open for death/remarriage behavior.

## [v0.9.0] - Sprint 9

### Added
- Dynamic family creation during simulation.
- Support for second-generation family formation.
- Family count included in the simulation summary.
- Methods supporting family creation and marriage candidate selection.

### Changed
- Refactored the simulation architecture to separate responsibilities between `Simulation`, `Person`, and `Family`.
- Shifted project design from a Genesis-specific simulation toward a reusable population simulation engine.
- Established that `Family` is responsible for family behavior, while `Simulation` coordinates yearly events.
- Clarified that future individual preferences and personality traits belong to `Person`.

### Architecture
- Established the guiding principle: **Store facts; calculate decisions.**
- Defined ownership of responsibilities:
  - `Simulation` advances time and coordinates events.
  - `Person` represents an individual and will eventually own preferences and personality.
  - `Family` represents the relationship between spouses and owns family-level behavior.
- Identified that future reproduction logic should be implemented as family behavior rather than simulation logic.

### Notes
Sprint 9 became an architecture-focused sprint rather than a feature-focused sprint.

The most significant accomplishment was defining a long-term architecture that supports future enhancements without requiring major redesign. This foundation prepares the simulator for features such as:
- Personality traits
- Family planning behavior
- Widowhood
- Remarriage
- Adoption
- Configurable reproduction models
- Additional family lifecycle events

The simulator now supports creating new families beyond the founding family, marking the transition from a single-family simulation to a true multi-generational population simulator.

## [0.8.0] - 2026-07-22

### Added
- Added `Simulation.add_family()` to centralize family management.
- Added `Simulation.add_person()` to centralize population management.

### Changed
- Refactored `create_child()` to accept a `Family` parameter.
- Updated the simulation loop to process families instead of relying on a hardcoded founding family.
- Removed the remaining hardcoded family dependency from the simulation engine.

### Notes
- This release focuses on internal refactoring only.
- Simulation behavior and output remain unchanged.
- The simulator is now prepared to support multiple families in future releases.

## [0.7.0] - 2026-07-22

### Added
- Added the new `Family` class to represent the family unit.
- Added support for tracking children within a family.
- Added `add_child()` to encapsulate child management.
- Added `child_count` property for family statistics.

### Changed
- Updated the simulation engine to maintain a collection of families.
- Created the initial family for Adam and Eve during simulation initialization.
- Updated child creation to register each child with its family.
- Improved the project architecture by separating individual (`Person`) data from family (`Family`) data.

### Notes
- This release introduces the foundation for family-based simulation while preserving the existing simulation behavior.
- No changes were made to the simulation output or reproduction logic.

## [0.6.0] - 2026-07-21

### Added
- Added the initial simulation model documentation.
- Defined the core architectural concepts of the simulator.
- Documented the responsibilities of the primary domain objects:
  - Simulation
  - Person
  - Family
- Added project design principles to guide future development.

### Changed
- Refined the simulation terminology to better reflect the Genesis narrative.
- Adopted **Marriage** as the preferred term over **Pairing**.
- Established **Family** as the central long-lived entity for modeling generational growth.
- Clarified that data should be owned by the object it logically belongs to (Person vs. Family).

### Notes
- This release contains design and documentation improvements only.
- No simulation behavior or functionality changed.
- These architectural decisions establish the foundation for implementing multi-generational family simulation in future releases.

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

## [0.4.0] - 2026-07-21

### Changed
- Renamed childbearing configuration to reproduction terminology.
- Added reproduction_start_age to the Person model.
- Assigned a reproduction start age when each child is created.

### Internal
- Improved configuration naming for clarity and consistency.

## [0.3.0]
- Adam and Eve have children.

## [0.2.0]
- Create a Simulation class that advances through the years.

## [0.1.0]
- Initial project structure.
- Configuration loader.
- Seed population loader.
- Person dataclass.
