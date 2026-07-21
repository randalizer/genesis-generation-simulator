# Genesis Generation Simulator Glossary

## Purpose

This glossary defines the terminology used throughout the Genesis Generation Simulator.
Using consistent terminology helps keep the code, documentation, and configuration
easy to understand.

---

## Birth

The event in which a new person is added to the simulation.

Example:

- Child-00003 is born in simulation year 1.

---

## Birth Interval

The number of years between successive births for a reproducing couple.

Example:

A birth interval of 2 means children are born every two years after reproduction begins.

---

## Reproduction

The process of producing children.

This simulator models reproduction using configurable assumptions.

---

## Reproduction Start Age

The age at which a person begins having children.

Depending on the configured reproduction mode, this age may be fixed or randomly
chosen within a configured range.

---

## Reproduction Mode

Determines how a person's reproduction start age is selected.

Current planned modes:

- fixed
- random

---

## Population

Every person currently tracked by the simulator.

Future versions may distinguish between:

- Living Population
- Historical Population

---

## Person

An individual within the simulation.

Each person has:

- Unique ID
- Name
- Sex
- Birth Year
- Father ID
- Mother ID
- Alive status

---

## Pair

A male and female selected to reproduce together.

The pairing strategy determines how pairs are formed.

---

## Pairing Strategy

The algorithm used to determine reproductive pairs.

Examples include:

- oldest_first
- random

Additional strategies may be added later.

---

## Generation

A genealogical generation.

This is not the same as a simulation year.

Example:

Adam is Generation 0.

His children are Generation 1.

Their children are Generation 2.

---

## Simulation Year

A single year within the simulation timeline.

Example:

Year 25

does not necessarily correspond to a person's age.

---

## Assumption

A configurable rule used where Scripture does not provide specific details.

Examples include:

- Birth interval
- Reproduction start age
- Pairing strategy

The simulator attempts to keep assumptions separate from Biblical facts.