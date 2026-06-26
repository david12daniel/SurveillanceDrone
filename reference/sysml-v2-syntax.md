# SysML v2 Textual Notation — Working Reference

A practical syntax guide for editing this project's system model. Geared to the
constructs actually used in [`model.sysml`](../model.sysml). For the full normative
grammar see the OMG SysML v2 Beta spec; for a complete, **extension-validated**
example of every construct see [`sysml-v2-cheatsheet-examples.sysml`](sysml-v2-cheatsheet-examples.sysml)
in this folder (open it in VS Code — Syside highlights and checks it live).

Targets **SysML v2.0 Beta 4** (the version the tooling and cheat sheet track).

## Tooling

- **Extension:** Syside Editor — `sensmetry.syside-editor` (installed). Provides
  live diagnostics, semantic highlighting, completion, hover, go-to-definition,
  rename, outline, and formatting. Language id `sysml`, normally bound to
  `.sysml` files. Free; no Java dependency.
- **Model file:** the system model is [`model.sysml`](../model.sysml) (renamed
  from `model.md` so the extension activates natively on the `.sysml` extension).
  It is a protected artifact — see `MEMORY.md` before editing.
- **Restart the server** via the command palette → “Restart language server”
  if diagnostics get stale.
- Alternative extension considered: `JamieD.sysml-v2-support` (adds diagram
  export + a built-in MCP server). Don't run both at once — two `sysml` LSPs
  conflict.

## Top-level structure

A model is a tree of `package`s. Names with spaces or punctuation are single-quoted.

```sysml
package DroneSystemModel {
    package Requirements { /* ... */ }
    package Architecture { /* ... */ }
    package Analysis     { /* ... */ }
}
```

Definitions (`*def`) declare types; **usages** (no `def`) declare instances/roles
typed by a definition. This def/usage split is the core mental model:
`part def Battery` is the kind; `part battery : Battery` is one used in a context.

## Definition vs. usage keywords

| Definition        | Usage                          | Used for                          |
|-------------------|--------------------------------|-----------------------------------|
| `part def`        | `part x : T;`                  | physical/logical components       |
| `item def`        | `item x : T;`                  | things that flow (data, fuel)     |
| `port def`        | `port p : T;` / bare `port p;` | interaction points                |
| `connection def`  | `connection c : T { ... }`     | typed connectors between ends     |
| `interface def`   | `interface i : T { ... }`      | connector between ports           |
| `constraint def`  | `constraint c : T { ... }`     | boolean/numeric constraints       |
| `requirement def` | `requirement <id> r : T { }`   | requirements                      |
| `action def`      | `action a : T;`                | behavior                          |
| `state def`       | `state s : T;`                 | states                            |
| `analysis def`    | (used as analysis case)        | trade studies / evaluations       |
| `attribute`/`attribute def` | `attribute x : T;`    | values / properties               |
| `enum def`        | `enum e : T;`                  | enumerations                      |

## Attributes, types, and values

```sysml
attribute cost_USD : ScalarValues::Real;
attribute mass     : ISQBase::MassValue;
attribute power    : ISQMechanics::PowerValue;

// Derived attribute (computed from other features):
attribute specificEnergy : ISQMechanics::SpecificEnergyValue = energy / mass;

// Default / literal with unit (quantity values use bracketed units):
attribute :>> mass = 1500 [kg];
```

Common library types this project uses: `ScalarValues::Real`, `ScalarValues::Integer`,
`ScalarValues::Boolean`, `string`, and ISQ quantity kinds `ISQBase::MassValue`,
`ISQBase::LengthValue`, `ISQBase::DurationValue`, `ISQMechanics::PowerValue`,
`ISQThermodynamics::EnergyValue`, `ISQThermodynamics::TemperatureValue`.

## Ports and connections

```sysml
part def CameraSubsystem {
    port video_out;     // bare port (untyped) — used heavily in model.sysml
    port power;
}

// Inside a composing part, wire usages together. Three flavors appear here:
connect a.p to b.q;             // generic connector
interface connect a.p to b.q;   // connector specifically between ports
connection connect a.p to b.q;  // connection usage (e.g. wireless RF links)
```

In `model.sysml`, internal subsystem wiring uses `interface connect`, while the
top-level RF links in `AerialThermalObservationSystem` use `connection connect`.

## Requirements and traceability — the conventions that matter here

```sysml
requirement R3 {
    doc /* Free-text requirement statement. */
}

// Subsystem requirement that decomposes a parent — use `refines`:
requirement R3_CAM_FOV {
    doc /* HFOV >= 30 deg. */
    refines R3;
}
```

- **`refines`** links a finer requirement up to the one it decomposes
  (e.g. cost requirements `refines R4`, thermal-derived ones `refines R3`).
- **`satisfy`** declares that a part fulfills a requirement. This project uses the
  short in-part form inside `part def`s:

  ```sysml
  part def Battery {
      satisfy R4_BAT_VOLT;
      satisfy R4_BAT_COST;
  }
  ```

  The cheat-sheet / spec also supports the explicit `satisfy R1 by vehicle;`
  form at the composing level. Keep using the project's short form for
  consistency unless modeling a satisfy-by-instance relationship.
- **ID convention:** `R<n>` for mission requirements; `R<n>_<SUBSYS>_<NAME>`
  for subsystem requirements (e.g. `R4_AF_PAYLOAD`). `<shortName>` in angle
  brackets gives an element an alias.

When adding/changing a requirement or part, preserve the web: new requirement →
`refines` its parent; new/changed part → `satisfy` what it covers and feed the
derived rollups (`totalCost`, `totalPower`, `subTotalCost`).

## Constraints, calculations, and analysis (verification layer)

Three distinct constructs — don't confuse them (the model originally did):

- **`constraint def`** — a *boolean predicate*. Its body is a boolean expression
  with **no** trailing `;` and **no** computed `out` value. Use for requirement checks.
- **`calc def`** — a *parametric calculation* (a function). Has typed `in`
  parameters and a single `return`. Use to compute a value (flight time, score).
- **`analysis def`** — a *case definition* that orchestrates calcs + constraints
  against a `subject`. See the subject rule below.

```sysml
// CALCULATION: a function with a return (NOT a constraint def).
calc def FlightTimeCalc {
    in batteryEnergy : ISQThermodynamics::EnergyValue;
    in totalPower    : ISQMechanics::PowerValue;
    // ISQ '/' returns the generic Quantities::ScalarQuantityValue — it does NOT
    // narrow to DurationValue, so type the result as ScalarQuantityValue.
    return flightTime : ScalarQuantityValue = batteryEnergy / totalPower;
}

// PREDICATE: boolean body, no trailing ';'. Compares dimensionally — a
// ScalarQuantityValue can be compared to a unit literal (`>=` returns Boolean).
constraint def MinFlightTimeReq {
    in flightTime : ScalarQuantityValue;
    flightTime >= 1800 [s]
}

// ANALYSIS CASE: subject FIRST, then bind calcs and assert constraints.
analysis def MinFlightTimeCheck {
    subject system : Architecture::AerialThermalObservationSystem;

    calc ftc : FlightTimeCalc {
        in batteryEnergy = system.drone.battery.energy;
        in totalPower    = system.drone.totalPower;
    }
    attribute computedFlightTime : ScalarQuantityValue = ftc.flightTime;

    assert constraint budgetCheck : BudgetLimit {
        in total_cost = system.totalCost;
        in limit = 2500.0;
    }
    assert constraint minCheck : MinFlightTimeReq {
        in flightTime = computedFlightTime;
    }

    return verdict : ScalarValues::Boolean =
        (system.totalCost <= 2500.0) and (computedFlightTime >= 1800 [s]);
}
```

Key rules learned (all were real errors — see MODEL_ISSUES.md §A10):

- **`subject` must be the first input parameter** of a case definition
  (`analysis def`, `case def`, `requirement def`). Declaring `in part x` as the
  first input without `subject` triggers `case-definition-subject-parameter-position`.
  Use the `subject` keyword.
- **Dimensional division returns `ScalarQuantityValue`**, not a specific subtype.
  Type computed quantities as `Quantities::ScalarQuantityValue`; compare them to
  unit literals (`flightTime >= 1800 [s]`) rather than assigning to `DurationValue`.
- **Don't use `constraint def` to compute values** — it must return Boolean. Use
  `calc def` with a `return` for computations.
- To get a plain magnitude for non-dimensional math (e.g. score = time / cost),
  import `QuantityCalculations::ToReal` and call `ToReal(flightTime)`.

## Specialization / redefinition operators

| Operator | Meaning                          | Example                         |
|----------|----------------------------------|---------------------------------|
| `:`      | typed by                         | `part battery : Battery;`       |
| `:>`     | specializes / subsets            | `part def SportsCar :> Vehicle` |
| `:>>`    | redefines (override a feature)   | `:>> wheels = 4;`               |
| `::>`    | references (bind a usage to one) | `end part hub ::> mainSwitch;`  |

## Instance tables (documenting computed results)

SysML v2 has no special "instance table" keyword, but a set of **part usages with
all values bound via `:>>`** is exactly that — each usage is one concrete instance
(row), the attributes are the columns. This is how `candidates.sysml` stores
component options, and how `analysis/flight_time_instances.sysml` (auto-generated
by `flight_time_model.py`) records each configuration's computed flight time:

```sysml
part def FlightTimeResult {        // the "schema" (columns)
    attribute configId : String;
    attribute allUpMass_g : Real;
    attribute maxFlightTimeHover_min : Real;
    attribute meetsR6_30min : Boolean;
}
part inst_C0001 : FlightTimeResult {   // one instance (row)
    :>> configId = "C0001";
    :>> allUpMass_g = 1347.7;
    :>> maxFlightTimeHover_min = 53.9;
    :>> meetsR6_30min = true;
}
```

This is the idiom for "compute outside SysML (Python/solver), document the result
back in the model." Keep such files self-contained (own `part def` + `private
import ScalarValues::*;`) so they validate independently and can be regenerated.

## Comments and documentation

```sysml
// line comment
/* block comment */
doc /* Documentation that attaches to the owning element (shows in hover). */
comment /* free-standing comment element */
```

## Imports / standard library

`model.sysml` now imports what it needs, so primitives, units, and cross-package
requirement names resolve:

```sysml
package DroneSystemModel {
 private import ScalarValues::*;   // Boolean, String, Real, Integer
 private import SI::*;             // unit symbols for [g], [mm], [W], [V], ...
 ...
 package Architecture {
  private import Requirements::**; // so `satisfy R3_CAM_WT;` resolves
 }
}
```

ISQ quantity types are still written fully-qualified (e.g. `ISQBase::MassValue`,
`ISQMechanics::PowerValue`) and resolve without an explicit ISQ import.
`candidates.sysml` adds `private import DroneSystemModel::Architecture::*;` to
reach the part defs.

### Units actually available

Predefined SI symbols usable in `[ ]` here: `g, mm, cm, km, nm, m, s, W, V, A, K,
Hz`. **Not** predefined: `mW, mA, mK, µm` — bind these in base units and note the
original in a comment (e.g. `100 mW` → `0.1 [W]`, `50 mK` → `0.05 [K]`,
`12 µm` → `0.012 [mm]`). Celsius is an offset unit the bracket notation doesn't
handle, so absolute temperatures are modeled as plain `Real` (`_C` suffix).

Quantity-kind type names verified against the bundled ISQ library: voltage =
`ISQElectromagnetism::ElectricPotentialDifferenceValue`, current =
`ISQBase::ElectricCurrentValue`, frequency = `ISQSpaceTime::FrequencyValue`,
specific energy = `ISQThermodynamics::SpecificEnergyValue` (**not**
`ISQMechanics::SpecificEnergyValue` — that does not exist).

**Dimensional arithmetic caveat**: The `'/'` operator defined in
`QuantityCalculations.sysml` returns `ScalarQuantityValue[1]`, not a specific
subtype — so `energyValue / powerValue` cannot be assigned to a
`ISQBase::DurationValue` attribute directly. Typed dimensional results require
parametric execution tooling beyond what the Syside LSP provides.

## Quick gotchas (several of these were real bugs in this model — see MODEL_ISSUES.md)

- The primitive string type is `String` (capital S), not `string`.
- There is **no `refines` keyword** for requirements — use `subsets Parent;`
  (or a `dependency`). Inline `subsets`/`:>` work in a usage body.
- Requirement/identifier names can't contain `.` (`R3.1` lexes as a number → use
  `R3_1`).
- An attribute and a port in the same def can't share a name (e.g. `attribute
  power` + `port power` collides — rename the port `power_in`).
- A `constraint` body holds a boolean expression with **no** trailing `;`
  (parameter `in`/`out` bindings do take `;`).
- Watch for name collisions between a requirements *package* and a *part def*
  (e.g. `CameraSubsystem`); give them distinct names.
- Definitions need a body `{ }` or a terminating `;` (e.g. `part def Engine;`).
- Units are written in brackets: `1500 [kg]`, `120 [m]`.
- Quote any identifier containing spaces: `package 'Trade studies'`.
