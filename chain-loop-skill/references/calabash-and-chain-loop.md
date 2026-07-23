# CLK Calabash and Multi-Chain Reference

## 1. Purpose

CLK does not begin from an ungrounded engineering plan. It begins from a frozen
product-definition source, then turns that source into a restricted multi-chain
execution plan.

The order is:

```text
Owner intent and project evidence
        ↓
Full or Minimum Calabash
        ↓
Fixed Chain roster and ordered Level plan
        ↓
GO Calabash traces and Verification Contracts
        ↓
Checker/Worker CELL execution
        ↓
Independent GO Verification
        ↓
Full Level barrier
        ↓
Next Level
```

CLK uses Calabash for definition and staged multi-chain execution for delivery. It
does not import Grapher or free-form graph routing.

## 2. Calabash Gate

### 2.1 Full Calabash

Use the project's complete Calabash when it is current, authoritative, internally
consistent, and applicable to the intended CLK scope.

### 2.2 Minimum Calabash

When no complete Calabash exists, the minimum acceptable definition is:

```text
Grandpa
→ Product Architecture
→ Ontology
```

#### Grandpa

Grandpa records:

- Owner intent;
- why the product or project exists;
- intended users and value;
- non-negotiable principles;
- hard boundaries;
- success direction;
- release or safety constraints that cannot be inferred by an implementation role.

#### Product Architecture

Product Architecture records:

- users and roles;
- product entry points;
- core business or operational journey;
- major modules and responsibilities;
- back-office or operational surfaces;
- data and evidence flow;
- external capabilities;
- final product outcome.

It is not a list of folders or code modules. It must show how the product works.

#### Ontology

Ontology records:

- authoritative domain concepts;
- one canonical name per concept;
- relationships;
- ownership;
- states and lifecycles;
- distinctions that later contracts and evidence must preserve.

### 2.3 Establishing a missing Calabash

If the project has no Calabash, Supervisor must derive Minimum Calabash from:

- explicit Owner statements;
- approved product documents;
- current UI and business journeys;
- existing domain models and data;
- stable contracts and workflows;
- verified behavior and audit evidence.

Supervisor may reconcile duplicate names or fill facts that have one uniquely
supported interpretation. It may not invent product intent.

When two or more materially different product definitions remain possible and no
existing authority resolves them, record:

```text
CALABASH_DEFINITION_BLOCKED
```

Only the irreducible Owner-exclusive decision may be requested. Routine engineering
uncertainty is not a Calabash block.

### 2.4 Freeze and traceability

The accepted definition is recorded as:

```text
PROJECT_CALABASH_BASELINE
baseline_version
baseline_hash
source_artifacts
Grandpa
Product Architecture
Ontology
known_constraints
approval_or_derivation_record
```

Every GO records `GO_CALABASH_TRACE`:

```text
GO_ID
Calabash baseline version/hash
Grandpa source
Product Architecture source
Ontology concepts/states
Derived GO outcome
Verification implications
```

A GO Verification Contract without a current trace is invalid because Verification
would have no authoritative definition of success.

## 3. Multi-Chain Model

### 3.1 Two dimensions

CLK has two explicit dimensions:

```text
Horizontal: one Level's concurrently startable GOs
Vertical:   one persistent Chain's ordered GOs
```

Example:

```text
              CHAIN-A     CHAIN-B     CHAIN-C     CHAIN-D
LEVEL-01      GO-01-A     GO-01-B     GO-01-C     GO-01-D
LEVEL-02      GO-02-A     GO-02-B     GO-02-C     GO-02-D
LEVEL-03      GO-03-A     GO-03-B     GO-03-C     GO-03-D
```

`LEVEL-01` means “these GOs may start together.” It is not a GO and does not have
CELLs.

### 3.2 Chain

One Chain is one stable ownership stream:

```text
CHAIN-A
Checker-A ↔ Worker-A
GO-01-A → GO-02-A → GO-03-A
```

The pair remains stable so that ownership, write scope, and local planning do not
move between roles.

A Chain may end after a verified GO. It may not skip a Level and later reappear,
and no new Chain may appear after Level 01. A plan needing that behavior belongs to
GLK.

### 3.3 Level

One Level is a frozen set of independently acceptable GOs that are all launch-ready
when the Level opens.

A Level opens only after:

- every prior Level is `LEVEL_VERIFIED`;
- all required upstream GO outputs are frozen;
- every listed GO's first CELL is ready;
- each GO has one active Checker/Worker pair;
- each GO has a pre-established fresh Verification attempt;
- no GO in the Level depends on another GO in that same Level;
- environments, tools, autonomy, and safety gates are ready.

Record:

```text
LEVEL_START_GATE_PASS
```

Then all first CELLs are dispatched in the same activation cycle.

### 3.4 Full barrier

Each GO may finish at a different time. A verified GO freezes its outputs and waits.
The next Level does not partially open.

```text
GO-01-A  GO_VERIFIED
GO-01-B  GO_VERIFIED
GO-01-C  GO_REWORK_REQUIRED
GO-01-D  GO_VERIFIED

Result: LEVEL-01 remains ACTIVE.
Only Chain C performs rework.
```

When every required member is verified:

```text
LEVEL-01_VERIFIED
```

Only then may Level 02 start.

### 3.5 Dependency boundary

Within one GO, CELLs may depend on earlier CELLs in that same GO.

Across GOs, a CELL may never consume an unfinished CELL result.

Forbidden:

```text
GO-01-A/CELL-02 -> GO-01-B/CELL-03
GO-01-A/CELL-02 -> GO-02-B/CELL-01
```

Allowed:

```text
GO-01-A GO_VERIFIED
→ output contract frozen
→ LEVEL-01 fully verified
→ GO-02-B may consume that frozen output
```

This boundary preserves error attribution: a failed GO Verification can be traced to
that GO rather than to mutable work hidden inside another GO.

## 4. Verification Binding and Direct Handoff

### 4.1 Project-plan freeze

For every planned GO, Supervisor freezes:

```text
GO_VERIFICATION_BINDING
GO and version
Verification Contract and hash
role identity policy
model binding policy
environment template
evidence path
direct Checker receipt target
verdict recipients
```

### 4.2 Level activation

Before the GO's first CELL, Supervisor creates the fresh Verification attempt,
passes readiness/preflight, binds the isolated workspace/runtime, and leaves it
uncontaminated until intake.

### 4.3 Direct handoff

After Checker accepts all CELLs:

```text
Checker
→ GO_READY_FOR_VERIFICATION
→ pre-established Verification
```

Supervisor is not a relay and must not summarize, rewrite, or add a pass suggestion.

Verification sends its signed verdict directly to:

```text
Checker + Supervisor
```

Checker handles local evidence work or Worker rework. Supervisor updates GO/Level
state and handles only plan, shared, safety, autonomy, or Owner-exclusive matters.

### 4.4 Fresh attempts

A changed GO candidate invalidates the old verdict. Rework uses a new Verification
attempt with a new conversation/context/workspace/evidence identity. The binding
remains traceable to the same GO version or an explicit revision.

## 5. Owner-Free Autonomy

CLK freezes `PROJECT_AUTONOMY_ENVELOPE` before execution. It authorizes routine
work without Owner checkpoints, including scoped implementation, local tests,
scans, evidence collection, safe local service operations, temporary test data, and
non-destructive repository operations declared by the plan.

Owner is not:

- a fallback Checker;
- a per-CELL approver;
- a per-GO approver;
- a Level-start button;
- a routine permission source;
- a troubleshooting assistant.

Only Supervisor may request an action that is genuinely and irreducibly Owner-only.
Platform permission friction must first be solved by provisioning or preauthorization;
it must not be presented as a product decision.

## 6. CLK Versus GLK

CLK is a restricted layered structure:

- fixed Chains;
- ordered Levels;
- all members of one Level start together;
- every GO verified independently;
- full Level barrier;
- deterministic next Level.

GLK is required when work needs:

- conditional GO routes;
- partial downstream unlock;
- arbitrary merge or split;
- cycles or feedback edges;
- runtime creation of new branches or Chains;
- path selection based on a verdict;
- a Grapher that navigates the project graph.

CLK is therefore a multi-chain method with graph-like structure, but it is not a
free graph method.
