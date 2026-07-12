---
name: multi-small-loop-skill
description: Run large projects through multiple independent, concurrently startable Workers under one Supervisor, with one persistent Checker paired to each Worker. The official abbreviation is MSLK; use this skill when the user says MSLK or multi-small-loop-skill, or when work can be divided into Workers that independently receive GO/CELL tasks, produce separately verifiable and acceptable results, and start without waiting for another Worker's future output. Use SLK instead when the combined Supervisor/Checker needs exactly one Worker.
---

# Multi Small Loop Skill (MSLK)

Use `MSLK` as the official abbreviation. Keep `$multi-small-loop-skill` as the
Codex invocation name.

## Canonical Identity

- Product name: `Multi Small Loop`.
- Abbreviation: `MSLK`.
- Canonical repository: `https://github.com/DWG7318/multi-small-loop-skill`.
- GitHub repository ID: `1298120736`.
- Default branch: `main`.
- Version source: repository `VERSION` file and matching `v*` tag.

Before publishing an MSLK update, verify the repository owner/name, repository
ID, default branch, and current HEAD. Never publish MSLK changes to the SLK
repository, a compatibility alias repository, or another similarly named skill.

Use one Supervisor to organize and oversee multiple independent Workers.

```text
                         +-> Checker A <-> Worker A
Owner -> Supervisor -----+-> Checker B <-> Worker B
                         +-> Checker C <-> Worker C
```

Each Worker is one persistent execution owner paired with one stable Checker.
The three external roles are always Supervisor, Checker, and Worker.

```text
Project
  -> Checker A <-> Worker A -> GO(s) -> CELL(s)
  -> Checker B <-> Worker B -> GO(s) -> CELL(s)
```

The number of independently acceptable and concurrently startable work units
determines the Worker count and Checker count. Both conditions are strict and
must hold at the same time. GO and CELL counts, project size, or a desire for
speed do not justify multiple Workers.

## Mode Selection Gate

The Supervisor must prove that multiple Workers are necessary during solution
planning, before creating roles.

For every candidate Worker, verify both:

1. Acceptance independence: its result can be inspected and accepted without
   another Worker's future output or evidence, and concurrent writes, state,
   fixtures, tests, or external side effects cannot invalidate that acceptance.
2. Launch independence: its first CELL can be dispatched immediately and does
   not wait for another Worker's future output, decision, or mutation.

These conditions are intentionally difficult. If fewer than two Workers pass
both, do not launch MSLK. Return to SLK and keep using SLK until the project
actually satisfies the MSLK gate.

If an active plan no longer satisfies the gate, stop issuing new CELLs,
preserve accepted evidence, record the mode change, and replan as SLK. If an
SLK plan later proves that at least two necessary Workers satisfy both
conditions, it may upgrade to MSLK after the same stop, evidence, and replan
procedure. Never change modes silently inside an executable CELL.

## Fresh Role Requirement

Every new project must create fresh Worker and Checker agents. Do not reuse
roles from another project, even when their scope looks similar; prior context
can contaminate planning, execution, and acceptance.

Treat "new project" narrowly: reuse is allowed only for an explicit upgrade or
continuation of the same project identity, objective lineage, coordination
records, and evidence chain. A renamed, copied, adjacent, or merely similar
project is new and must receive fresh roles.

## Model Policy

Use `gpt-5.6-sol` with `xhigh` reasoning for the Supervisor and every Checker.
This is the recommended controlling-role configuration.

Workers may use only:

- `gpt-5.6-terra` with `medium` reasoning or higher;
- `gpt-5.6-sol` with `medium` reasoning or higher.

During planning, assign a Worker model and reasoning level to every CELL based
on its difficulty, risk, and validation burden. Record the assignment in the
CELL plan before launch.

The Supervisor or controlling Checker may raise or lower a Worker's model or
reasoning level as execution evidence changes the difficulty estimate. Record
the change before dispatch or rework. Never go below `medium`, use a model
outside the two allowed 5.6 Worker models, or fall back to 5.5/5.4-era models.

## Role Contract

### Supervisor

The Supervisor owns the whole project, not the middle of ordinary cell work.

- Translate Owner intent into the overall solution and acceptance target.
- Split the project into mutually independent, concurrently startable Workers.
- Produce or approve each Worker's solution, GO map, and CELL plan.
- Create one stable Checker for each Worker.
- Maintain the supervisor board and final result queue.
- Act as the mandatory Overseer (`监工`) through periodic quick inspections.
- Resolve plan defects, Owner decisions, shared-resource conflicts, and genuine
  blockers that a Checker cannot resolve inside its fixed plan.
- Perform final local acceptance after a Checker writes a passed result.

The Supervisor must not be the normal relay for Checker/Worker messages and
must not silently take over a Worker's cell.

### Checker

One Checker controls exactly one Worker.

- Read the complete fixed plan for its Worker.
- Select and package one fixed CELL at a time.
- Send formal tasks and rework directly to its paired Worker.
- Inspect files, diffs, tests, scans, method logs, and boundaries locally.
- Directly repair a Worker-caused defect when the repair is bounded, safe, and
  within the current CELL and the Checker's available authority.
- Route `NEXT`, `REDO`, `COMPLETE`, `BLOCKED`, or `PLAN_DEFECT`.
- Send the next CELL after accepting the current CELL.
- Write the Worker's final passed or blocked queue record.

The Checker may internally perform planning and routing, but it remains one
external role. It must not change GO/CELL scope or acceptance rules after
launch; plan defects go to the Supervisor.

## Checker Direct Repair Rule

When a Worker makes a concrete implementation or evidence mistake, the Checker
may fix it directly instead of returning the same simple correction to the
Worker.

Use direct Checker repair only when:

- The defect is inside the current CELL's allowed scope.
- The expected correction is unambiguous and small enough to inspect fully.
- The Checker has the tools, permissions, and evidence needed to repair safely.
- The repair does not change the GO/CELL objective, acceptance standard,
  architecture ownership, or Owner decision.
- The repair does not require private credentials, manual Owner action, or an
  unauthorized external side effect.

The Checker must:

1. Preserve the Worker's original delivery and record the detected defect.
2. Make the minimum correction inside the current CELL.
3. Run the same focused and regression checks required for Worker delivery.
4. Record files changed, commands, results, and the route in Checker evidence;
   never rewrite the Worker's append-only method history.
5. Accept the current CELL only after the repaired result passes locally.
6. Send the next formal CELL directly to the Worker.
7. Include a concise `Checker repair update` in that same next-task message:
   previous CELL, defect, Checker fix, and verification result.

The combined repair update and next CELL assignment must be one message whose
first line is the next `Formal task:` heading. Do not send a separate status
message and then leave the Worker without work.

If direct repair is unsafe, broad, ambiguous, outside the CELL, or changes the
plan, the Checker must use formal rework or escalate to the Supervisor instead.
If the repaired CELL was the final CELL, the Checker writes the final queue
instead of inventing another task.

### Worker

One Worker belongs to exactly one Checker.

- Remain the persistent execution thread for the whole assigned work unit.
- Execute every dependency-authorized GO/CELL assigned to that Worker; do not
  create or request a replacement Worker when a GO ends.
- Execute only a formal task or formal rework from its controlling Checker.
- Work on one CELL at a time and only within the allowed scope.
- Preserve unrelated changes made by other loops or the Owner.
- Maintain append-only method evidence.
- Run required checks and return evidence to the Checker.
- Never self-select the next CELL and never declare its own work accepted.

## Small Loop Protocol

The normal path is direct:

```text
Checker -> Worker -> Checker -> Worker -> ... -> final queue
```

Worker tasks must start with one of:

```text
Formal task: GO-01/CELL-01.01/R01
Formal rework: GO-01/CELL-01.01/R02
```

Messages without one of these headings are discussion, not executable work.

After finishing a CELL, the Worker must directly send the controlling Checker:

```text
完成，请检验
```

The Worker's final visible reply must also be exactly `完成，请检验`. This
receipt means only "ready for validation". The Checker must still verify the
delivery before routing the next CELL.

Do not actively wait or continuously poll after sending a task or receipt.
Direct delivery should activate the receiving thread.

## Worker, GO, And CELL

Use this canonical hierarchy only:

```text
Project -> independent Worker/Checker -> GO -> CELL
```

- Worker: one persistent execution owner with an independent work domain.
- Checker: the persistent planner, validator, and router paired to that Worker.
- GO: a fixed outcome within the Worker, not a phase, wave, or thread.
- CELL: the smallest inspectable work package inside one GO.
- Round: `GO-01/CELL-01.01/R01`.

A Worker is valid only when both conditions hold:

1. Independence: it can receive its own GO/CELL tasks and produce results that
   can be inspected and accepted without borrowing another Worker's evidence
   or suffering acceptance interference from concurrent writes or side effects.
2. Parallel start: its first CELL has no prerequisite on another Worker's
   future output, so all Workers in the active MSLK can start together.

Never renumber GO/CELL after launch.

### Derive Worker Count Correctly

1. Identify materially independent work units by ownership, authoritative
   files, contracts, and side effects.
2. Confirm every candidate Worker can start now and be accepted independently.
3. Create exactly one Worker and one Checker for each valid work unit.
4. Assign one or more GO to each persistent Worker.
5. Count Workers from independent, concurrently startable work units, never
   from GO count, CELL count, schedules,
   dependency depth, phases, waves, or desired visual symmetry.
6. Keep the same Worker when one assigned GO ends and the next assigned GO
   is an internal continuation owned by the same Worker.
7. At launch, every created Worker must have a dependency-ready first CELL
   that can be dispatched immediately.
8. If Worker B must wait for Worker A's future output, B is not a valid Worker
   in the current MSLK. Do not create B, its Checker, or an Overseer row yet.
9. If only one candidate remains valid, switch to SLK instead of manufacturing
   another Worker.

Do not invent stages or waves unless the Owner explicitly asks for them. GO
dependencies are sufficient to determine when a Checker may dispatch a CELL.

### Required Assignment Table

Before launch, produce one machine-checkable table:

```text
| Worker | Checker | Assigned GO | GO count | CELL count |
```

Validate all of these:

- Worker count = Checker count.
- Every GO is assigned exactly once.
- Every CELL is assigned exactly once through its GO.
- Sum of per-Worker GO counts equals the project GO count.
- Sum of per-Worker CELL counts equals the project CELL count.
- Each Worker has one direct receipt target: its controlling Checker.
- Method-log and final-queue names are unique per Worker.

### Design GO

- Define GO as a verifiable outcome owned by one Worker.
- Let one Worker own multiple related GO when they share the same write domain.
- Express ordering as GO dependencies; do not create another project layer.
- Keep GO fixed after launch; route plan defects to Supervisor.
- Do not distribute GO evenly merely to make Worker totals look symmetrical.

### Design CELL

Every CELL must define:

- objective;
- authoritative inputs;
- allowed write scope;
- forbidden scope;
- output artifacts;
- focused checks and broader regression;
- evidence and append-only method log;
- dependencies;
- Worker model and reasoning assignment;
- completion criteria.

Size CELLs by implementation risk, cross-owner impact, and evidence burden.
Uneven CELL counts are expected. A Worker still executes one CELL at a time.

Before launching a Worker, provide:

1. A solution file with objective, boundaries, architecture, risks, and
   acceptance.
2. A GO file with outcomes and dependencies.
3. A CELL index plus one detailed CELL file per GO.
4. The Worker/Checker assignment and exact GO/CELL totals.

## Multi-Worker Decomposition

Use MSLK only when Workers are materially independent and concurrently
startable.

Independence is a launch-time execution property, not a future intention. All
Workers in one active MSLK must be dependency-ready and independently
executable when the MSLK starts. A different write directory or business name
does not make a Worker independent if its first CELL still needs another
active Worker's future output.

For every Worker:

- Assign one unique business/module/write-domain owner.
- Assign one persistent Checker and one persistent Worker.
- Use distinct method logs and final queue names.
- Define disjoint write scopes or explicit shared-file serialization.
- Define cross-Worker contracts as refs/events/interfaces rather than informal
  assumptions.
- Keep one Worker's completion evidence separate from every other Worker.

Do not run Workers concurrently against the same authoritative files without a
declared serialization or merge policy. If a shared dependency blocks several
Workers, the Supervisor resolves it once and authorizes the affected Checkers.

Do not create idle Workers for later dependent work. Resolve cross-Worker
dependencies in exactly one of these ways:

1. Merge the dependent GO into the same persistent Worker.
2. Complete and freeze the shared prerequisite with one loop before launching
   the independent MSLK Workers.
3. Launch the dependent work later as a separate SLK or MSLK after its
   prerequisites pass Supervisor acceptance.

### Dependency-Waiting Anti-Pattern

This is invalid:

```text
Worker A: starts GO-01 now
Worker B: created now, waits for Worker A to finish GO-01
Worker C: created now, waits for Worker B to finish
```

Only Worker A exists as executable work. B and C are future assignments, not
parallel Workers. Labeling them `waiting_for_go_dependency`, pre-creating their
threads, or counting them in the current Worker total does not make the launch
parallel. Stop the launch as `PLAN_DEFECT`, archive or revoke the premature
pairs, finish/freeze the prerequisite, and recalculate Worker count from the
Workers that can start immediately.

The number of GO and CELL does not need to be equal between Workers. Allocate
them according to ownership, complexity, risk, dependencies, and evidence.

## Mandatory Overseer Rule (`监工`)

The Supervisor must periodically perform a quick inspection while any Worker
has unfinished CELLs. This prevents a Checker or Worker from ending a turn and
silently abandoning the loop.

### Cadence

- Starting this skill requires creating one recurring Overseer task for the
  current Supervisor thread. Monitoring is not optional while any loop remains
  unfinished.
- Select exactly one interval: 15, 30, or 60 minutes.
- Use 15 minutes for small projects with few loops and short/light CELLs.
- Use 30 minutes for medium projects or mixed CELL sizes.
- Use 60 minutes for large projects, many loops, or long/heavy CELLs.
- Larger projects and larger CELL capacity use the longer interval because
  normal work needs more time before a useful inspection.
- If the Owner explicitly selects one of the three intervals, use it.
- Create a heartbeat attached to the existing Supervisor thread. The heartbeat
  may wake only that Supervisor; it must never create a new conversation,
  detached task, worktree task, replacement loop, Checker, or Worker.
- Record the heartbeat name/id and selected interval on the supervisor board.
- A check is a short inspection pass, not active waiting or continuous polling.

### Recurring Task Lifecycle

At skill start:

1. Estimate project size from Worker count, total remaining CELLs, average CELL
   duration, evidence burden, and shared-resource risk.
2. Select 15, 30, or 60 minutes using the cadence rules.
3. Create one same-thread heartbeat whose task is the Quick Inspection and Wake
   Rule below.
4. Confirm the heartbeat is active before considering multi-loop supervision
   started.

At every heartbeat:

1. Wake the existing Supervisor in the same conversation.
2. Inspect all unfinished Workers once.
3. Wake only stalled Checkers as required.
4. Update the supervisor board and report a compact status.
5. End the turn; do not wait for another interval.

When every planned loop has a passed queue and the Supervisor's final audit has
accepted every result, delete or disable the heartbeat in that same Supervisor
turn. Record that monitoring ended. Do not leave an orphan periodic task and do
not let the completion check create a new conversation.

If the environment cannot create a same-thread heartbeat, report the missing
capability explicitly. Do not substitute a detached cron job or new task.

### Quick Inspection

For every unfinished Worker, inspect only what is needed:

1. Supervisor board state and planned CELL total.
2. Passed/blocked final queue records.
3. Checker and Worker thread status and latest turn.
4. Latest formal task, formal rework, or completion receipt.
5. Method-log/artifact timestamp when thread state is ambiguous.

Classify the Worker as:

- `active_worker`
- `active_checker`
- `waiting_for_worker_delivery`
- `waiting_for_checker_validation`
- `blocked`
- `stalled`
- `complete`

### Wake Rule

If the Worker is not complete and neither role is genuinely active, notify the
Checker to continue unless a real blocker or plan defect is recorded. Do not
tell the Worker to self-select work. Cross-Worker dependency waiting is not a
healthy active state; it means the launch decomposition was invalid or the
dependent Worker was created too early.

Use the observed situation:

- Worker delivered but Checker stopped: tell Checker to validate and route.
- Checker accepted but did not send the next CELL: tell Checker to resume
  planner/router duty and send the next formal task.
- Worker ended without delivery: tell Checker to inspect the partial work and
  issue a bounded formal rework.
- Receipt was lost: tell Checker to inspect Worker artifacts and perform a
  one-time routing repair.
- Another Worker's future output is required: record `PLAN_DEFECT`, revoke the
  premature pair, and redesign or defer that work; do not keep an idle loop.
- A blocked record exists: Supervisor resolves the plan/Owner/shared-resource
  decision, then tells Checker how to resume.
- A role is active: do not interrupt it.
- A passed queue exists and final acceptance succeeds: stop monitoring that
  Worker.

A wake message must be concise, name the current CELL, cite the observed stop,
and require the Checker to send or validate exactly one next action. It must
not become a replacement task package for the Worker.

### Overseer Record

Update the supervisor board after each check:

```md
| Worker | Checker | State | Current CELL | Final queue | Next signal |
|---|---|---|---|---|---|
```

Report active Workers, repaired Workers, blockers, and the next expected signal
to the Owner in a compact status update.

## Evidence And Queue

Use project-local coordination paths unless the project defines others:

```text
coordination/
  plans/
  checker-messages/
  worker-method-logs/
  supervisor-board.md
```

Method logs are append-only. Rotate to a new numbered shard before 999 lines or
when an old shard must be sealed; never rewrite history to make evidence look
clean. Every new shard cites the prior shard and its hash.

Only the Checker writes a final Worker record:

```text
MSLK_YYYYMMDD-HHMMSS_<worker>_<plan-version>_<result>.md
```

Valid results are `passed`, `blocked`, `plan-defect`, `owner-decision`, and
`stopped`. A Worker is complete only after the passed record exists and the
Supervisor's final audit accepts it.

No generated planning, log, queue, or coordination Markdown file may exceed
999 lines. Split rather than remove necessary detail.

## Recovery Rules

- Delayed thread registration: confirm a returned thread ID with `read_thread`
  before creating a replacement; temporary list/title failure does not prove
  creation failed.
- Duplicate Checker: choose one controlling Checker, stop/archive the other,
  and ensure the Worker executes each CELL once.
- Thread `systemError`: Checker inspects partial outputs and issues the same
  CELL as a bounded rework; do not discard valid work.
- Damaged method log: seal it, authorize a new shard, preserve the incident,
  and revalidate current artifacts without fabricating history.
- Dynamic shared data: distinguish legitimate external drift from writes by
  the current CELL through short-window semantic and writer-attribution checks;
  do not chase perpetual fixed hashes.
- Repeated same defect: Checker follows the fixed retry policy and escalates a
  real plan defect or blocker to the Supervisor.

## Launch Checklist

Before launching multiple loops, the Supervisor confirms:

- Each Worker has complete solution/GO/CELL plans.
- Every created Worker's first CELL is dependency-ready and can be dispatched
  immediately in the launch turn.
- No Worker needs another active Worker's future output to begin or continue its
  current authorized work.
- Ownership and write scopes do not collide.
- Every Checker/Worker pair and receipt target is correct.
- Method-log and final-queue paths are unique.
- Tests, scans, safety boundaries, and external-action gates are explicit.
- Every CELL declares an allowed Worker model and reasoning level.
- The supervisor board lists every Worker and its persistent Checker.
- The 15/30/60-minute Overseer interval is selected from project/CELL size.
- The same-thread heartbeat is active, recorded on the board, and configured to
  remove itself after all loops pass Supervisor acceptance.
- No Worker relies on another Worker's passed record as its own evidence.

Then send each full Worker plan to its Checker. The Checker sends the first
formal CELL to its Worker. The Supervisor begins periodic oversight and remains
outside ordinary Checker/Worker traffic.
