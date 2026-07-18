# MSLK Control Operations

This reference belongs only to MSLK. It never authorizes SLK, a combined role,
hidden work, replacement pairs, late pair creation, or detached monitoring.

## Command Surface

Accept only these explicit forms:

```text
MSLK START
MSLK STATUS ALL
MSLK STATUS PAIR <pair-id>
MSLK PAUSE ALL NOW
MSLK PAUSE PAIR <pair-id> NOW
MSLK PAUSE ALL AFTER <accepted-cell-count>
MSLK PAUSE PAIR <pair-id> AFTER <accepted-cell-count>
MSLK PAUSE ALL AT <RFC3339-time>
MSLK PAUSE PAIR <pair-id> AT <RFC3339-time>
MSLK RESUME ALL NOW
MSLK RESUME PAIR <pair-id> NOW
MSLK RESUME ALL AT <RFC3339-time>
MSLK RESUME PAIR <pair-id> AT <RFC3339-time>
MSLK CANCEL SCHEDULE ALL
MSLK CANCEL SCHEDULE PAIR <pair-id>
```

`MSLK START` is manual only. Before it, the full frozen roster has at least two
acceptance-independent and launch-independent pairs; every visible role has a
current `MSLK_READINESS_EVAL_PASS`; every first CELL is ready; plans and GO
detection profiles are approved; and exact-roster simulation has passed. START
authorizes all prepared pairs in one launch turn. It creates no late or
replacement pair.

Status is read-only and never creates, wakes, archives, schedules, or dispatches
a role. Unscoped commands and unknown pair IDs are rejected.

## Scoped Pause

`PAUSE ALL AFTER N` uses the absolute project-wide accepted CELL count.
`PAUSE PAIR <pair-id> AFTER N` uses that pair's absolute accepted CELL count.
Neither is a relative increment.

A trigger may mature while one or more targeted Workers have active CELLs. Each
targeted pair independently enters `PAUSE_PENDING`; its Worker finishes normally,
its Checker validates and performs any Checker-owned repair, then the pair enters
`PAUSED`. Archive a pair when no next authorized work is ready. Never interrupt
an active CELL.

An `ALL` command is best effort over the frozen roster. Validate and transition
each pair independently. The aggregate result is `PARTIAL` unless every eligible
target succeeds. Always display explicit per-pair outcomes; never report false
global success.

## Same-Pair Resume

Resume only an existing paused pair. Wake the same Checker and Worker, then have
the Checker revalidate the plan, readiness receipts, simulation, GO profile, and
continuation conditions before dispatch. A replacement pair, late pair, unknown
pair, or resume before initial start is rejected.

Cancel changes only the pending schedule in its explicit `ALL` or `PAIR` scope.
It never interrupts active work, changes the frozen roster, or reopens
`COMPLETE`.

## Project State

Project state is derived from pair states:

1. `COMPLETE` only when all pairs are complete.
2. `PAUSED` when every incomplete pair is paused.
3. `PARTIALLY_PAUSED` when paused and dispatchable incomplete pairs coexist.
4. `BLOCKED` when no incomplete pair is dispatchable and at least one is blocked.
5. Otherwise `RUNNING` after start.

Pair-level scheduled and pending states remain visible in status and receipts.

## Rejection And Receipt

Canonical failures are `INVALID_COMMAND`, `INVALID_STATE`,
`PRECONDITION_FAILED`, `UNKNOWN_PAIR`, `SCHEDULE_CONFLICT`, and
`ALREADY_APPLIED`. Rejection changes no pair/project state, schedule, roster,
progress, visibility, or dispatch.

Every command emits one `MSLK_CONTROL_RECEIPT` with command ID, normalized
command, actor, explicit target scope, pre-state, trigger, prerequisite evidence,
action, aggregate result, post-state, schedule version, per-target results, and
project-wide progress. Command IDs are idempotent and cannot duplicate a
transition or assignment.

## Owner Assistance Boundary

A Worker never asks the Owner for confirmation or help. It solves within its
CELL authority or sends a formal blocker to its paired Checker. A Checker also
never asks the Owner; it resolves pair-local issues or reports a precise
condition to the Supervisor. Only the Supervisor may contact the Owner, after
exhausting safe authorization repair, provisioning, versioned plan repair, and
work-method repair. Owner assistance is minimized and restricted to one specific
Owner-exclusive decision, credential, consent, external action, scope or
acceptance change, Goal change, or safety boundary.

## Supervisor Safeguard Patrol

The patrol is the last guarantee that work continues, not passive monitoring.
Its actor is the distinct Supervisor, which has highest on-site decision
authority inside the Owner objective, safety rules, MSLK topology, and external
action boundaries. The Supervisor may:

1. Inspect the minimum status and evidence needed to classify progress.
2. Perform authorization repair or provision a missing approved capability.
3. Approve or initiate a versioned plan revision and its required simulation.
4. Improve the work method when evidence shows the current method stalls or
   misroutes work.

Patrol never executes an ordinary Worker CELL, performs Checker acceptance, or
wakes a healthy Checker in `OFFLINE_WAITING_WORKER_SIGNAL`. When a Worker is
genuinely active, record that fact and leave the pair untouched. When a real
stall, blocker, lost receipt, permission defect, or plan defect exists, take the
smallest authorized action that restores progress. Only an Owner-exclusive
condition may cross the Owner Assistance Boundary.

## Quick Inspection

Quick inspection belongs to the distinct Supervisor. It never wakes or uses a
Checker in `OFFLINE_WAITING_WORKER_SIGNAL` merely to inspect an active Worker.
For every unfinished Worker, the Supervisor inspects only what is needed:

1. Supervisor board state and planned CELL total.
2. Passed/blocked final queue records.
3. Checker and Worker conversation status and latest turn.
4. Latest formal task, repair record, or completion receipt.
5. Method-log/artifact timestamp when conversation state is ambiguous.

Classify each Worker as `active_worker`, `active_checker`,
`waiting_for_worker_delivery`, `waiting_for_checker_validation`, `blocked`,
`condition_blocked`, `stalled`, or `complete`.

## Wake Rule

Before a paired Checker's final dispatch action, require
`WORKER_EXECUTION_GATE_PASS`: the canonical assignment workspace equals that
Worker's bound workspace, and every routine allowlisted edit and command is
pre-authorized. A routine approval prompt is `WORKER_EXECUTION_FAILURE`, never
an Owner click task.

The Supervisor provisions a usable pair permission mechanism. The Checker
verifies the canonical path without treating a sibling worktree, junction,
symlink, or equivalent Git content as the bound workspace. The allowlist covers
only declared file writes, evidence creation, local checks, and an explicitly
authorized commit. It never expands CELL scope or weakens platform safety.

If binding or permission cannot be proven, the Checker records
`CONDITION_BLOCKED` and reports the exact gap; the Supervisor repairs it before
dispatch. Credentials, external side effects, destructive or security-sensitive
operations, out-of-allowlist writes, and scope, acceptance, or Goal changes stay
behind the existing Owner-decision boundary.

An offline Checker waiting on its Worker is healthy and must remain offline.
Wake the same Checker only after `WORKER_COMPLETION_RECEIPT`,
`WORKER_BLOCKER_RECEIPT`, or `WORKER_EXECUTION_FAILURE`. Never tell the Worker to
self-select work. Cross-Worker dependency waiting means invalid decomposition or
premature role creation, not a healthy active state.

Route the observation:

- Worker delivered a formal receipt: wake that Checker to validate and route.
- Checker accepted but sent no next CELL: wake it to send one formal task.
- Worker ended without delivery: Checker inspects and repairs usable partial
  output; only with no usable result may it re-dispatch the original CELL.
- Receipt was lost: Checker inspects artifacts and performs one routing repair.
- Another Worker's future output is required: record `PLAN_DEFECT`, revoke the
  premature pair, and redesign or defer it; never keep an idle loop.
- `CONDITION_BLOCKED` exists: Supervisor makes the Owner-assistance decision;
  after `SUPERVISOR_RESOLVED`, record `RESUME_AUTHORIZED` and wake the same
  Checker for prerequisite revalidation.
- A Worker is active and its Checker is offline: do not wake the Checker.
- A passed queue exists and final acceptance succeeds: stop monitoring it.

A wake message names the current CELL, cites the observed stop, and requires the
Checker to send or validate exactly one next action. It never becomes a Worker
task package.

## Overseer Record

Update the Supervisor board after each inspection:

```md
| Worker | Checker | State | Current CELL | Final queue | Next signal |
|---|---|---|---|---|---|
```

Report active Workers, repaired Workers, blockers, and the next expected signal
to the Owner in one compact status update.
