---
name: multi-small-loop-skill
description: Use when the user says MSLK or multi-small-loop-skill, or when one project needs multiple independent, concurrently startable visible Worker conversations with one persistent visible Checker per Worker. Never trigger together with SLK.
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
both, record `METHOD_SELECTION_FAILED`, do not launch MSLK, and return the
method decision to the Owner.

## Exclusive Mode Lock

Choose exactly one method before role creation: SLK or MSLK. Once MSLK is
selected for a project run:

- invoke MSLK exactly once;
- do not load, invoke, nest, repeat, alternate with, or switch to SLK;
- do not borrow SLK's combined Supervisor/Checker topology, single-Worker
  behavior, or any other SLK capability;
- do not present SLK and MSLK as interchangeable or generally combinable.

Shared rules never transfer role ownership, topology, messages, state, or
capabilities between MSLK and SLK. Implement every common requirement entirely
inside the selected MSLK role structure. Mentioning SLK for prohibition does not
load it or authorize any of its behavior.

If MSLK is the wrong method or an active plan stops satisfying its gate,
preserve accepted evidence, record `METHOD_SELECTION_FAILED`, stop without new
formal work, and ask the Owner to start a new, separate run with an explicit
method choice. The current run never converts itself into SLK.

## Visible Conversation Only

Every Supervisor, Checker, and Worker role must be a visible Codex conversation
under the same project. Hidden execution is forbidden.

- Never use a subagent, sub-agent, background agent, hidden worker,
  `delegate_task`, or any subagent-dispatch capability.
- Never represent an internal tool call, background job, or invisible execution
  context as a Supervisor, Checker, or Worker.
- Confirm every role conversation belongs to the current project before
  assigning formal work.
- Keep assignments, receipts, repair records, routing, and completion messages in the
  visible project conversations.

### Visible Conversation Lifecycle

- Create or unarchive a role conversation only when an authorized formal task
  is ready for that role.
- Keep the conversation visible while that task is active.
- Archive it immediately when its authorized work is complete and no formal
  task remains assigned.
- If later work is authorized for the same role in the same project, unarchive
  the existing conversation instead of creating a duplicate.
- Unarchiving a conversation does not repeat the MSLK invocation and does not
  permit SLK activation.
- An archived conversation performs no hidden or background work.

## Mandatory Simulation Gate

Run a no-side-effect simulation before formal work. Planning and simulation may
inspect metadata, but must not edit project files, execute implementation
commands, call external services, create formal role assignments, or start a
CELL.

The simulation must:

1. confirm MSLK is the sole selected method and has not been invoked already;
2. model one visible same-project Supervisor plus every visible Checker/Worker
   pair;
3. prove at least two Workers are acceptance-independent and can receive their
   first CELL immediately;
4. rehearse one assignment, delivery, Checker decision, and `NEXT`, `REDO`, or
   `BLOCKED` route per pair;
5. prove no subagent or SLK capability is used;
6. validate ownership, write isolation, evidence paths, model assignments,
   tests, safety gates, heartbeat behavior, and archive/unarchive lifecycle.

Record either `SIMULATION_PASS` with the checked facts or `SIMULATION_FAIL` with
the reason. Formal work may begin only after `SIMULATION_PASS`. A failed or
missing simulation forbids role launch and CELL execution.

## Fresh Role Requirement

Every new project must create fresh visible Worker and Checker conversations
under that same project. Do not reuse roles from another project, even when
their scope looks similar; prior context can contaminate planning, execution,
and acceptance.

Treat "new project" narrowly: reuse is allowed only for a continuation of the
same project identity, objective lineage, coordination records, and evidence
chain. A renamed, copied, adjacent, or merely similar project is new and must
receive fresh roles.

## Model Policy

The Supervisor and every Checker must use `gpt-5.6-sol` with `xhigh` reasoning.

Workers may use only:

- `gpt-5.5` with `high` reasoning as the minimum;
- `gpt-5.6-sol` with `high` reasoning as the maximum.

During planning, assign a Worker model and reasoning level to every CELL based
on task type, difficulty, risk, tool burden, and validation burden. Prefer
`gpt-5.5 high` for routine bounded implementation and `gpt-5.6-sol high` for
complex integration, architecture-sensitive work, or difficult diagnosis.
Record the assignment in the CELL plan before launch.

The controlling Checker may change the Worker model as evidence changes the task
classification. Record the change before dispatch. Never assign a Worker below
`gpt-5.5 high`, above `gpt-5.6-sol high`, or at a reasoning level other than
`high`.

## Role Contract

### Role Authority Matrix

| Responsibility | MSLK owner |
| --- | --- |
| Method gate, project decomposition, cross-Worker contracts, Supervisor board, and final audit | Supervisor |
| Each Worker's initial solution, GO/CELL plan, and evidence-driven GO revision | Its paired Checker |
| CELL assignment, validation, repair, routing, progress display, and per-Worker queue | Its paired Checker |
| Optional Goal management, gap allocation, and final Goal validation | Supervisor |
| CELL execution | Worker |

MSLK has one distinct Supervisor plus multiple persistent Checker/Worker pairs.
It never combines Supervisor and Checker, never uses the SLK single-Worker
topology, and never lets the Supervisor replace ordinary Checker work.

### Supervisor

The Supervisor owns the whole project, not the middle of ordinary cell work.

- Translate Owner intent into the overall solution and acceptance target.
- Split the project into mutually independent, concurrently startable Workers.
- Define Worker ownership boundaries and cross-Worker contracts; approve only
  cross-Worker, acceptance, safety, and Owner-decision boundaries of
  Checker-owned plans.
- Create one stable Checker for each Worker.
- Maintain the supervisor board and final result queue.
- Manage and independently validate the optional project Goal completion gate.
- Act as the mandatory Overseer (`监工`) through periodic quick inspections.
- Resolve plan defects, Owner decisions, shared-resource conflicts, and genuine
  blockers that a Checker cannot resolve inside its current authorized plan.
- Perform final local acceptance after a Checker writes a passed result.

The Supervisor must not be the normal relay for Checker/Worker messages and
must not silently take over a Worker's cell.

### Checker

One Checker controls exactly one Worker.

- The Checker owns and maintains its Worker's initial solution, GO map, CELL plan,
  and detailed CELL files.
- Read the complete current versioned plan for its Worker.
- Own its Worker's evidence-driven GO review and revision proposals as part of
  the Checker's planning responsibility.
- Select and package one fixed CELL at a time.
- Send formal tasks directly to its paired Worker.
- Inspect files, diffs, tests, scans, method logs, and boundaries locally.
- Repair every defect found in its Worker's delivered result; never return a
  repair task to the Worker.
- Route `NEXT`, `REDO`, `COMPLETE`, `BLOCKED`, or `PLAN_DEFECT`.
- Send the next CELL after accepting the current CELL.
- Write the Worker's final passed or blocked queue record.

The Checker may internally perform planning and routing, but it remains one
external role. It must not change GO/CELL scope or acceptance rules ad hoc;
after GO completion it may propose an evidence-driven revision to the
Supervisor under the rule below.

## Checker Direct Repair Rule

The Checker must repair every defect found in its Worker's delivered result and
must not send a repair task back to the Worker.

For Checker repair:

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

If repair is broad or ambiguous, the Checker splits it into bounded
Checker-owned repair steps. If safe repair exceeds the Checker's authority or
changes the plan, it escalates to the Supervisor as `PLAN_DEFECT`, `BLOCKED`, or
an Owner decision; it never returns the repair to the Worker. If no usable
Worker result exists at all, the original CELL may be re-dispatched as an
original task, not as a repair task. If the repaired CELL was the final CELL,
the Checker writes the final queue instead of inventing another task.

### Worker

One Worker belongs to exactly one Checker.

- Remain the persistent execution thread for the whole assigned work unit.
- Execute every dependency-authorized GO/CELL assigned to that Worker; do not
  create or request a replacement Worker when a GO ends.
- Execute only a formal task from its controlling Checker.
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

Worker tasks must start with:

```text
Formal task: GO-01/CELL-01.01/R01
```

Checker-owned repair evidence starts with `Repair record:` and is never a
Worker assignment. `REDO` means the Checker repairs and revalidates the
delivery; it does not send correction work back to the Worker. Messages without
the formal task heading are discussion, not executable Worker work.

## Mandatory Project Progress Display

Every formal task assignment from a Checker to its Worker must include exactly
one project-wide progress line after the task details:

```text
正在完成 GO-03：35/231
```

The GO identifier is the GO of the newly assigned CELL. The numerator counts
accepted CELLs only across every Checker/Worker pair, after any required Checker
repair and local validation. It is not a per-Worker subtotal. Assigned, running,
delivered-but-unchecked, blocked, revoked, and duplicate CELLs do not count as
complete. Count each accepted CELL identifier exactly once.

The denominator is the total CELL count in the current versioned plan across all
Workers and GO, including accepted historical CELLs and every active remaining
CELL. After an approved GO revision or historical-GO supplement, recompute the
denominator, record the old and new totals in the revision ledger and Supervisor
board, and never reduce it below the accepted count. The numerator never
decreases.

Before every formal task assignment, the Checker recomputes the snapshot from
the project plan and append-only accepted-CELL records and includes it in the
task evidence. The Supervisor remains the sole writer of the Supervisor board
and reconciles those snapshots by CELL identifier. Concurrent Checkers may show
the same point-in-time snapshot, but must never double-count a CELL. Continue
displaying progress until all loops finish. When every CELL is accepted and no
next task exists, the Supervisor's final queue may display the following only
when no Goal is configured or the optional Goal has passed:

```text
全部完成：231/231
```

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
- Checker: the persistent planning, validation, and routing role paired to that
  Worker.
- GO: a verifiable outcome within the Worker, not a phase, wave, or thread.
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
9. If only one candidate remains valid, record `METHOD_SELECTION_FAILED`, stop
   MSLK launch, and return the method decision to the Owner.

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
- GO scope follows project need and must not be reduced for device capacity.
- Let one Worker own multiple related GO when they share the same write domain.
- Express ordering as GO dependencies; do not create another project layer.
- Keep GO changes versioned and evidence-driven; route every revision through
  the Supervisor.
- Do not distribute GO evenly merely to make Worker totals look symmetrical.

### Evidence-Driven GO Revision

After every GO is completed and checked, its Checker compares the accepted plan
with the actual result, including delivered scope, defects, residual risk, new
dependencies, changed estimates, and incomplete outcomes.

The Checker owns the resulting GO revision proposal and may:

- adjust any subsequent GO that has not started;
- add a supplementary GO for a historical GO when the completed result exposes
  missing, corrective, or follow-up work;
- revise affected CELL maps, dependencies, model assignments, and the Worker
  assignment table.

The Checker sends the proposal and evidence to the Supervisor. The Supervisor
may approve, reject, or return it for revision based on cross-Worker dependency,
ownership, acceptance, safety, or Owner-decision boundaries, but must not author
ordinary GO revisions in place of the Checker. The Worker must not revise GO or
CELL plans.

GO revision is append-only and versioned:

- never rewrite the historical GO, its evidence, or its acceptance result;
- retain existing identifiers and add a revision or supplement identifier such
  as `GO-03-R1` or `GO-03-S1`;
- keep a historical-GO supplement with the same owning Worker unless the Owner
  explicitly authorizes a new project run;
- do not create an extra Worker or Checker merely because a GO changed;
- record the triggering evidence, reason, old/new scope, dependencies,
  acceptance criteria, affected CELLs, and Owner decision when required;
- preserve MSLK acceptance independence, parallel safety, method exclusivity,
  visible-conversation rules, and existing safety gates.

Before dispatching a revised or supplementary GO, run a no-side-effect delta
simulation for every affected Checker/Worker pair and record
`GO_REVISION_SIMULATION_PASS`. Without that record, the revision remains
proposed and no formal CELL may start.

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
CELL size must be kept modest enough for the current computer to execute and
verify reliably. Reduce files touched, command fan-out, runtime, and evidence
volume when device capacity is limited. Split the same GO into more CELLs rather
than shrinking the GO or weakening acceptance. Uneven CELL counts are expected.
A Worker still executes one CELL at a time.

Before launching a Worker, its Checker must provide:

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
3. Defer the dependent work until its prerequisites pass Supervisor acceptance;
   the Owner must explicitly choose the method for a separate future run.

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
- Use 30 minutes for medium projects or mixed device-safe CELL runtimes.
- Use 60 minutes for large projects, many loops, or an inherently long
  verification command that cannot be split safely.
- Larger project coordination or unavoidable verification runtime uses the
  longer interval; do not enlarge CELL workload merely to justify it.
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
turn only if no Goal is configured or `GOAL_SATISFIED` exists. An untested Goal
or `GOAL_GAP` remains unfinished Supervisor work. Record when monitoring ends.
Do not leave an orphan periodic task and do not let the completion check create
a new conversation.

If the environment cannot create a same-thread heartbeat, report the missing
capability explicitly. Do not substitute a detached cron job or new task.

### Quick Inspection

For every unfinished Worker, inspect only what is needed:

1. Supervisor board state and planned CELL total.
2. Passed/blocked final queue records.
3. Checker and Worker thread status and latest turn.
4. Latest formal task, repair record, or completion receipt.
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
- Checker accepted but did not send the next CELL: tell Checker to resume its
  planning/routing duty and send the next formal task.
- Worker ended without delivery: tell Checker to inspect and repair any usable
  partial result; only if none exists may it re-dispatch the original task.
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

## Optional Goal Gate

The Owner may define one optional Goal. A Goal is active only when the Owner
explicitly supplies or approves its identifier, objective, measurable success
criteria, required evidence, and safety boundaries. The Supervisor must not
invent, broaden, or silently change it. Owner-authorized Goal changes are
versioned and append-only.

If no Goal is configured, this section adds no completion gate and ordinary
MSLK acceptance applies.

Checker completion is provisional. Every controlling Checker must first accept
the current PLAN/GO/CELL work and submit its passed queue. The Supervisor must
independently validate the Goal against fresh project-wide evidence:

- record `GOAL_SATISFIED` only when every Goal criterion is proven;
- otherwise record `GOAL_GAP` with each unmet criterion, evidence, residual
  risk, affected ownership domains, and required outcome;
- while `GOAL_GAP` exists, the Supervisor must not declare project completion or
  write the final passed queue.

After `GOAL_GAP`, the Supervisor allocates each missing outcome to the existing
independent ownership domains. Each affected Checker designs its own
PLAN/GO/CELL continuation for its persistent Worker. The Supervisor must not
author those detailed Checker plans; it approves only cross-Worker, acceptance,
safety, and Owner-decision boundaries.
Each Checker preserves accepted history, appends new identifiers, and obtains
`GO_REVISION_SIMULATION_PASS` before dispatching new CELLs. Recompute the
project-wide denominator, unarchive roles only when formal work is ready, and
continue until the Supervisor records `GOAL_SATISFIED`.

If the Goal gap cannot preserve MSLK acceptance and launch independence, or
cannot proceed within Owner authority, safety gates, or available evidence,
record `METHOD_SELECTION_FAILED`, `BLOCKED`, `PLAN_DEFECT`, or an Owner decision.
Do not claim completion, combine SLK, or switch methods inside the current run.

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
Supervisor's final audit accepts it. Project completion with a configured Goal
also requires `GOAL_SATISFIED`.

No generated planning, log, queue, or coordination Markdown file may exceed
999 lines. Split rather than remove necessary detail.

## Recovery Rules

- Delayed thread registration: confirm a returned thread ID with `read_thread`
  before creating a replacement; temporary list/title failure does not prove
  creation failed.
- Duplicate Checker: choose one controlling Checker, stop/archive the other,
  and ensure the Worker executes each CELL once.
- Thread `systemError`: Checker inspects and repairs usable partial outputs; only
  when none exist may it re-dispatch the original CELL unchanged.
- Damaged method log: seal it, authorize a new shard, preserve the incident,
  and revalidate current artifacts without fabricating history.
- Dynamic shared data: distinguish legitimate external drift from writes by
  the current CELL through short-window semantic and writer-attribution checks;
  do not chase perpetual fixed hashes.
- Repeated same defect: Checker continues bounded Checker-owned repair and
  escalates a real plan defect or blocker to the Supervisor; it never sends the
  correction back to the Worker.

## Launch Checklist

Before launching multiple loops, the Supervisor confirms:

- `SIMULATION_PASS` exists for this exact plan and role roster.
- MSLK is the sole method, was invoked once, and no SLK capability is present.
- Every role is a visible conversation under the same project; no subagent,
  hidden worker, or background agent exists.
- Every role conversation has work ready, and every no-work conversation is
  archived with an explicit unarchive path for later same-project work.
- Each Worker has complete solution/GO/CELL plans.
- The GO revision ledger is present; every completed GO has an evidence review,
  and every revised or supplementary GO has `GO_REVISION_SIMULATION_PASS`.
- Every created Worker's first CELL is dependency-ready and can be dispatched
  immediately in the launch turn.
- No Worker needs another active Worker's future output to begin or continue its
  current authorized work.
- Ownership and write scopes do not collide.
- Every Checker/Worker pair and receipt target is correct.
- Method-log and final-queue paths are unique.
- Tests, scans, safety boundaries, and external-action gates are explicit.
- Every CELL declares an allowed Worker model and reasoning level.
- The Supervisor and every Checker are `gpt-5.6-sol xhigh`; every Worker is from
  `gpt-5.5 high` through `gpt-5.6-sol high` according to task type.
- GO scope follows project need; every CELL is sized for reliable execution on
  the current computer without weakening GO acceptance.
- Every Checker task displays project-wide `正在完成 GO-NN：accepted/total`, and
  the Supervisor final queue displays `全部完成：total/total`.
- The optional Goal is either absent or explicitly defined; a configured Goal
  blocks project completion until the Supervisor records `GOAL_SATISFIED`.
- The supervisor board lists every Worker and its persistent Checker.
- The 15/30/60-minute Overseer interval is selected from project/CELL size.
- The same-thread heartbeat is active, recorded on the board, and configured to
  remove itself after all loops pass Supervisor acceptance.
- No Worker relies on another Worker's passed record as its own evidence.
- The role authority matrix is unchanged; no SLK combined role, single-Worker
  behavior, state, or message route has been borrowed.

Then send each full Worker plan to its Checker. The Checker sends the first
formal CELL to its Worker. The Supervisor begins periodic oversight and remains
outside ordinary Checker/Worker traffic.
