---
name: multi-small-loop-skill
description: Run large projects as multiple independent small loops under one supervising thread. Use when work must be split into disjoint streams, each with one Checker and one Worker, while one Supervisor plans, periodically oversees progress, wakes stalled Checkers, and performs final acceptance. Also use for GO/CELL planning, concurrent checker-worker pairs, anti-early-stop supervision, completion queues, and reliable cross-thread receipts.
---

# Multi Small Loop Skill

Use one Supervisor to organize and oversee multiple independent small loops.

```text
                         +-> Checker A <-> Worker A
Owner -> Supervisor -----+-> Checker B <-> Worker B
                         +-> Checker C <-> Worker C
```

Each small loop is one stable `Checker <-> Worker` pair. The three external
roles are always Supervisor, Checker, and Worker.

## Role Contract

### Supervisor

The Supervisor owns the whole project, not the middle of ordinary cell work.

- Translate Owner intent into the overall solution and acceptance target.
- Split the project into mutually independent streams.
- Produce or approve each stream's solution, GO map, and CELL plan.
- Create one stable Checker/Worker pair for each stream.
- Maintain the supervisor board and final result queue.
- Act as the mandatory Overseer (`监工`) through periodic quick inspections.
- Resolve plan defects, Owner decisions, shared-resource conflicts, and genuine
  blockers that a Checker cannot resolve inside its fixed plan.
- Perform final local acceptance after a Checker writes a passed result.

The Supervisor must not be the normal relay for Checker/Worker messages and
must not silently take over a Worker's cell.

### Checker

One Checker controls exactly one small loop.

- Read the complete fixed plan for its stream.
- Select and package one fixed CELL at a time.
- Send formal tasks and rework directly to its paired Worker.
- Inspect files, diffs, tests, scans, method logs, and boundaries locally.
- Directly repair a Worker-caused defect when the repair is bounded, safe, and
  within the current CELL and the Checker's available authority.
- Route `NEXT`, `REDO`, `COMPLETE`, `BLOCKED`, or `PLAN_DEFECT`.
- Send the next CELL after accepting the current CELL.
- Write the stream's final passed or blocked queue record.

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

## GO And CELL

Use GO for a phase and CELL for the smallest inspectable work package.

- GO: `GO-01`, `GO-02`.
- CELL: `CELL-01.01`, `CELL-01.02`, `CELL-02.01`.
- Round: `GO-01/CELL-01.01/R01`.
- Never renumber after launch.

Before launching a stream, provide:

1. A solution file with objective, boundaries, architecture, risks, and
   acceptance.
2. A GO file with all phases and dependencies.
3. A CELL index plus one detailed CELL file per GO.

Every CELL must define objective, inputs, allowed scope, forbidden scope,
outputs, checks, evidence, dependencies, and completion criteria.

## Multi-Loop Decomposition

Use multiple small loops only when streams are materially independent.

For every stream:

- Assign a unique module/stream owner.
- Assign one Checker and one Worker.
- Use distinct method logs and final queue names.
- Define disjoint write scopes or explicit shared-file coordination.
- Define cross-stream contracts as refs/events/interfaces rather than shared
  informal assumptions.
- Keep one stream's completion evidence separate from every other stream.

Do not launch parallel loops that edit the same authoritative files without a
declared serialization or merge policy. If a shared dependency blocks several
loops, the Supervisor resolves it once and then wakes affected Checkers.

The number of CELLs does not need to be equal between streams. Allocate CELLs
according to complexity, risk, dependencies, and evidence burden.

## Mandatory Overseer Rule (`监工`)

The Supervisor must periodically perform a quick inspection while any stream
has unfinished CELLs. This prevents a Checker or Worker from ending a turn and
silently abandoning the loop.

### Cadence

- Use the Owner's requested interval.
- If no interval is provided, use one hour.
- Prefer a heartbeat attached to the current supervising thread when the host
  supports it.
- Do not create detached conversations or duplicate loops merely to monitor.
- A check is a short inspection pass, not active waiting or continuous polling.

### Quick Inspection

For every unfinished stream, inspect only what is needed:

1. Supervisor board state and planned CELL total.
2. Passed/blocked final queue records.
3. Checker and Worker thread status and latest turn.
4. Latest formal task, formal rework, or completion receipt.
5. Method-log/artifact timestamp when thread state is ambiguous.

Classify the stream as:

- `active_worker`
- `active_checker`
- `waiting_for_worker_delivery`
- `waiting_for_checker_validation`
- `blocked`
- `stalled`
- `complete`

### Wake Rule

If the stream is not complete and neither role is genuinely active, notify the
Checker to continue. Do not tell the Worker to self-select work.

Use the observed situation:

- Worker delivered but Checker stopped: tell Checker to validate and route.
- Checker accepted but did not send the next CELL: tell Checker to resume
  planner/router duty and send the next formal task.
- Worker ended without delivery: tell Checker to inspect the partial work and
  issue a bounded formal rework.
- Receipt was lost: tell Checker to inspect Worker artifacts and perform a
  one-time routing repair.
- A blocked record exists: Supervisor resolves the plan/Owner/shared-resource
  decision, then tells Checker how to resume.
- A role is active: do not interrupt it.
- A passed queue exists and final acceptance succeeds: stop monitoring that
  stream.

A wake message must be concise, name the current CELL, cite the observed stop,
and require the Checker to send or validate exactly one next action. It must
not become a replacement task package for the Worker.

### Overseer Record

Update the supervisor board after each check:

```md
| Stream | Checker | Worker | State | Current CELL | Final queue | Next signal |
|---|---|---|---|---|---|---|
```

Report active streams, repaired streams, blockers, and the next expected signal
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

Only the Checker writes a final stream record:

```text
LE_YYYYMMDD-HHMMSS_<stream>_<plan-version>_<result>.md
```

Valid results are `passed`, `blocked`, `plan-defect`, `owner-decision`, and
`stopped`. A stream is complete only after the passed record exists and the
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

- Each stream has complete solution/GO/CELL plans.
- Ownership and write scopes do not collide.
- Every Checker/Worker pair and receipt target is correct.
- Method-log and final-queue paths are unique.
- Tests, scans, safety boundaries, and external-action gates are explicit.
- The supervisor board lists every stream.
- The Overseer interval and wake route are configured.
- No stream relies on another stream's passed record as its own evidence.

Then send each full stream plan to its Checker. The Checker sends the first
formal CELL to its Worker. The Supervisor begins periodic oversight and remains
outside ordinary Checker/Worker traffic.
