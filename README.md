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

One Supervisor splits the project into independent Workers, pairs each Worker
with one fixed Checker, periodically acts
as Overseer (`监工`), wakes stalled Checkers, and performs final acceptance.

```text
Project -> persistent Checker/Worker -> one or more GO -> CELL
```

Worker count comes from independently acceptable work units that can all start
together. GO and CELL counts never create Workers, stages, waves, or
replacement threads. A Worker remains assigned across every
dependency-authorized GO and executes one CELL at a time.

Every Worker created in one MSLK must be able to receive its first CELL
immediately. If one Worker must wait for another Worker's future output, they
are not independent parallel Workers: merge the dependent work, finish the
shared prerequisite first, or launch the dependent loop later. MSLK never
pre-creates idle Workers for future GO dependencies.

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

Current version: `1.2.5`.

Version `1.2.5` adds CELL-level Worker model planning: Workers use only 5.6
Terra or Sol at `medium` or higher, while Supervisor and Checkers are
recommended to use 5.6 Sol at `xhigh`.
