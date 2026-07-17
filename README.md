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

MSLK and SLK are mutually exclusive. Select MSLK exactly once for a project
run; never load both skills, switch methods, repeat the invocation, or borrow
SLK capabilities. If MSLK is not suitable, stop and return the method decision
to the Owner instead of converting the active run.

Common rules do not make the skills composable. MSLK implements all nine rules
only through one distinct Supervisor and multiple persistent Checker/Worker
pairs; it never imports SLK's combined role or single-Worker topology.

All roles must be visible Codex conversations under the same project. MSLK
never uses subagents, background agents, hidden workers, or `delegate_task`.
Create or unarchive a role conversation only when formal work is ready; archive
it immediately when that work finishes. Later same-project work should
unarchive the existing conversation instead of creating a duplicate.

Before formal role launch or CELL execution, run a no-side-effect simulation of
each pair's first assignment, delivery, validation, and routing cycle. Formal
work is allowed only after the simulation records `SIMULATION_PASS`.

After each GO, the paired Checker reviews the actual accepted result and may
propose adjustments to unstarted GO or an append-only supplementary GO for
historical work. The Supervisor gates cross-Worker and safety boundaries without
taking over the Checker's planning responsibility. Preserve all historical
evidence and identifiers, keep ownership and parallel independence intact, and
require `GO_REVISION_SIMULATION_PASS` before executing the revised plan.

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
  resolution, cross-Worker boundary approval, and final acceptance. It does not
  replace ordinary Checker planning or routing.
- Checker: one stream's initial GO/CELL planning and revision, validation,
  mandatory result repair, routing, and final queue. Repair tasks never return
  to the Worker. After
  repairing a Worker mistake, the Checker
  explains the fix inside the next formal CELL assignment.
- Worker: one bounded CELL at a time with append-only evidence.

The Supervisor and every Checker use `gpt-5.6-sol xhigh`. Workers range from
`gpt-5.5 high` to `gpt-5.6-sol high`, selected by task type. GO scope follows
project need and ignores device limits; CELLs are made smaller as needed for
reliable execution on the current computer.

Every Checker assignment shows project-wide accepted CELL progress, for example
`正在完成 GO-03：35/231`, not a per-Worker subtotal. The count continues through
every assignment and ends only when the Supervisor final queue shows
`全部完成：231/231`.

The Owner may optionally define a measurable project Goal. In that case,
Checker completion is provisional until the Supervisor independently records
`GOAL_SATISFIED`. A `GOAL_GAP` is allocated to the affected existing domains;
their Checkers design append-only PLAN/GO/CELL continuations without transferring
planning ownership to the Supervisor or importing SLK.

Before each assignment, every Checker verifies continuation conditions. A clear
failure stops that Checker's Worker dispatch and reports evidence to the
Supervisor. The Supervisor either requests specific Owner assistance or resolves
the supervisory condition and wakes the same Checker for revalidation.

Install the `multi-small-loop-skill` folder under your Codex skills directory,
then invoke `$multi-small-loop-skill` when a project should run through several
parallel Checker/Worker loops.

Current version: `1.4.1`.

Version `1.4.1` adds the continuation-condition stop, escalation, resolution,
and verified-resume gate for every Checker/Worker pair.
