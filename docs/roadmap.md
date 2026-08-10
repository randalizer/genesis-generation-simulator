Genesis Generation Simulator Roadmap

## Current focus
- Refine family formation and pairing rules.
- Clarify birth scheduling and reproduction assumptions.
- Prepare the project for a configurable rules-based simulation engine.

## Phase 1 - Foundation
- [x] Project structure
- [x] Configuration
- [x] Population model
- [x] Simulation engine

## Phase 2 - Population Growth
- [x] Adam and Eve reproduction
- [ ] Multi-generation reproduction
- [ ] Pairing engine
- [ ] Family relationships

## Phase 3 - Reporting
- [ ] Population statistics
- [ ] Generation reports
- [ ] Family tree reports
- [ ] Export to CSV

## Phase 4 - Advanced Modeling
- [ ] Lifespans
- [ ] Mortality
- [ ] Alternative pairing strategies
- [ ] Configurable assumptions

## Phase 5 - Visualization
- [ ] Family tree
- [ ] Population graphs
- [ ] Timeline

## Planned Features
These items are planned for future work once the core population and pairing
model are stable.

- Multiple pairing strategies
- Pregnancy
- Widowhood
- Adoption
- Mortality
- Multiple seed populations
- Compatibility scoring
- Geographic regions
- Household model

## Architectural improvements
- Move seed data creation out of `Simulation.__init__()`
- Centralize ID generation
- Separate reporting from simulation logic
- Replace `print` statements with a reporting interface

## Ideas Under consideration
- Engagement
- Marriage ceremony
- Birth events
- Weaning
- Adoption
- Widowhood
- Divorce (if ever applicable to a different simulation)
- Multiple births (twins, triplets, etc.)
- Infertility
- Lifespan and death
- Migration between communities
