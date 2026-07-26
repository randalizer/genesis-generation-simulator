# Genesis Generation Simulator Assumptions

## Purpose

The purpose of this simulator is to explore possible population growth during the
early chapters of Genesis.

The simulator distinguishes between:

- **Biblical Facts** — statements explicitly supported by Scripture.
- **Modeling Decisions** — choices made to represent Scripture within a computer simulation.
- **Simulation Assumptions** — configurable values used where Scripture does not provide specific details.

Changing a simulation assumption does **not** change the Biblical record. It simply
allows different scenarios to be explored.

---

# Biblical Facts

The following are treated as facts because they are explicitly stated in Scripture.

## Adam

- Adam was the first man.
- Adam was created by God.

## Eve

- Eve was the first woman.
- Eve was created from Adam.

## Family

- Adam and Eve had Cain.
- Adam and Eve had Abel.
- Adam and Eve later had Seth.
- Adam and Eve had many other sons and daughters.

## Lifespans

- Genealogies and ages recorded in Genesis are treated as accurate for the simulation.

---

# Modeling Decisions

These are design decisions made so the Biblical account can be represented in a
computer simulation.

## Time

The simulator measures time beginning with Creation.

Simulation Year 0 represents the creation of Adam and Eve.

## Adam and Eve

Adam and Eve are treated as being created as mature adults.

Although they begin at **Simulation Year 0**, they are **not** treated as newborns.

They enter the simulation already capable of reproduction.

This reflects the belief that God created Adam and Eve fully formed rather than as infants.

## Subsequent Generations

Every person after Adam and Eve enters the simulation through birth.

For these individuals:

```
Age = Current Simulation Year − Birth Year
```

Adam and Eve are the only exception to this rule.

---

# Simulation Assumptions

The following values are configurable because Scripture does not specify them.

## First Birth Year

Determines when Adam and Eve begin having children.

Default:

```
1
```

---

## Birth Interval

Determines the number of years between successive births for a reproducing couple.

Default:

```
2 years
```

---

## Reproduction Mode

Determines how a person's reproduction start age is selected.

Supported modes:

- fixed
- random

---

## Reproduction Start Age

Determines the age at which a person begins reproducing.

### Fixed Mode

Every person begins reproduction at the configured default age.

### Random Mode

Each person is assigned a random reproduction start age between:

- Minimum
- Maximum

Once assigned, this value remains constant throughout that person's lifetime.

---

## Pairing Strategy

Determines how reproductive pairs are formed.

Planned strategies include:

- oldest_first
- random

Additional strategies may be added in future versions.

---

## Birth Probability

Current assumption:

Every eligible couple produces a child at each birth interval.

Future versions may include fertility models.

---

# Guiding Principles

The simulator follows these principles:

1. Scripture takes precedence over simulation.
2. Modeling decisions are documented.
3. Assumptions are configurable whenever practical.
4. The simulator explores possibilities—it does not claim historical certainty where Scripture is silent.

---

# Future Assumptions

Possible future configuration options include:

- Lifespan modeling
- Twin births
- Multiple births
- Infertility
- Marriage age models
- Pairing algorithms
- Population limits
- Mortality before the Flood

These features are not currently implemented.

---

# Summary

Whenever Scripture provides information, the simulator follows Scripture.

Whenever Scripture is silent, the simulator uses configurable assumptions.

The goal of the Genesis Generation Simulator is to provide a transparent and
configurable framework for exploring population growth in early Genesis while
clearly distinguishing between Biblical facts, modeling decisions, and simulation
assumptions.

### First Generation Marriages

The simulation begins with Adam and Eve as the only founding family. As a result,
their children must marry one another in order for the population to continue.

For the initial implementation, sibling marriages are permitted. Future versions
of the simulator may introduce configurable marriage rules to support different
starting populations or genealogical constraints.