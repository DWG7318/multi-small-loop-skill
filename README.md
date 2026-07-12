# Multi Small Loop Skill (MSLK)

A Codex skill for running large projects as multiple independent small loops.

Canonical repository: `DWG7318/multi-small-loop-skill`
GitHub repository ID: `1298120736`

The official abbreviation is **MSLK**. Use `MSLK` in conversation and
documentation; use `$multi-small-loop-skill` as the Codex invocation name.

Each loop uses two working roles:

```text
Checker <-> Worker
```

One Supervisor splits the project into independent Blocks, launches one fixed
pair per Block, periodically acts
as Overseer (`监工`), wakes stalled Checkers, and performs final acceptance.

```text
Project -> Block -> persistent Checker/Worker -> one or more GO -> CELL
```

The Block count determines the Worker count. GO and CELL counts never create
Workers, stages, waves, or replacement threads. A Worker remains assigned to
its Block across every dependency-authorized GO and executes one CELL at a
time.

Starting the skill also creates a heartbeat attached to the same Supervisor
conversation. Its interval is selected from 15, 30, or 60 minutes according to
project size and CELL duration. It never creates a new conversation, and it is
removed automatically after every loop passes Supervisor acceptance.

## Roles

- Supervisor: project planning, decomposition, periodic oversight, blocker
  resolution, and final acceptance.
- Checker: one stream's CELL planning, validation, bounded direct repair,
  routing, and final queue. After repairing a Worker mistake, the Checker
  explains the fix inside the next formal CELL assignment.
- Worker: one bounded CELL at a time with append-only evidence.

Install the `multi-small-loop-skill` folder under your Codex skills directory,
then invoke `$multi-small-loop-skill` when a project should run through several
parallel Checker/Worker loops.

Current version: `1.2.0`.

Version `1.2.0` formalizes Block -> persistent Worker/Checker -> GO -> CELL
design, Worker/GO/CELL arithmetic validation, dependency-waiting supervision,
and the canonical repository identity guard.
