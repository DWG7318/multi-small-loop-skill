# MSLK Control Kernel And Hardening Design

## Objective

Make MSLK control explicit without weakening its independent, concurrently
executable Checker/Worker topology. Add one MSLK-only CLI-like control contract,
remove initial timed start and late pair creation, and close the release,
reference, and context-index gaps found in the 1.7.0 audit.

This design belongs only to MSLK. It does not import SLK files, schemas, states,
tests, role ownership, or commands.

## Non-Goals

- No executable terminal binary.
- No shared control kernel or third repository.
- No subagents, hidden roles, combined Supervisor/Checker, or single-Worker mode.
- No new Checker/Worker pair through a control command.
- No initial timed start.

## Files And Boundaries

- `contracts/mslk-control-kernel.json`: canonical machine-readable project/pair
  states, commands, transitions, errors, and audit fields.
- `references/mslk-control-operations.md`: human instructions for Supervisor and
  paired Checkers, including inspection and wake behavior.
- `SKILL.md`: concise mandatory summary and conditional reference link.
- `tests/test_control_kernel.py`: model-based positive and negative scenarios
  loaded from the MSLK JSON contract.
- `tests/test_contract.py`: role, documentation, link, version, and line-budget
  contracts.

No file in this list is shared with SLK. Similar behavior is intentionally
defined and tested again under MSLK ownership.

## Public Command Contract

MSLK accepts only:

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

`MSLK START` is the only initial-start command and is never scheduled. It is
valid only when the complete frozen roster has at least two independent Workers,
every first CELL is ready, plans and detection profiles are approved, and
`SIMULATION_PASS` covers the same roster. It creates and dispatches all roster
pairs in that launch turn.

Timed commands apply only to existing pairs after project start:

- `PAUSE ...` stops targeted Checker dispatch at safe CELL boundaries.
- `PAUSE ALL AFTER <accepted-cell-count>` uses the absolute project-wide accepted
  CELL count; `PAUSE PAIR ... AFTER` uses that pair's absolute accepted count.
- A time or count trigger may mature during active CELL work, but affected pairs
  first enter `PAUSE_PENDING` and finish their active CELLs normally.
- `RESUME ...` applies only to targeted paused pairs and reuses them.
- `CANCEL SCHEDULE ...` cancels pending control for its explicit scope.
- `STATUS ...` is read-only and never creates, wakes, archives, or dispatches a
  role.
- No control command adds, replaces, or reassigns a pair.

Any SLK-prefixed, generic `LOOP`, timed `START`, unscoped MSLK control, unknown
pair, or unknown command is rejected.

## State Model

Project states are `NOT_STARTED`, `RUNNING`, `PARTIALLY_PAUSED`, `PAUSED`,
`BLOCKED`, `COMPLETE`, and no others. Each frozen pair has `PLANNED`, `RUNNING`,
`PAUSE_SCHEDULED`, `PAUSE_PENDING`, `PAUSED`, `RESUME_SCHEDULED`,
`BLOCKED`, and `COMPLETE`.

Key invariants:

- `NOT_STARTED -> RUNNING` requires one manual `MSLK START` for the frozen roster.
- Before start, every frozen pair is `PLANNED`; `MSLK START` moves the complete
  roster to `RUNNING` in one launch turn.
- No pair may join the roster after start through the control kernel.
- Active CELL work is never interrupted.
- Each targeted Checker validates and repairs before pause becomes effective.
- Resume wakes the same Checker, which revalidates before dispatching to the same
  Worker.
- `ALL` operates as one command with per-pair receipts; unaffected pairs remain
  independent.
- `ALL` is best-effort across the frozen roster: each pair is validated and
  transitioned independently, while the aggregate result is `PARTIAL` unless
  every eligible target succeeds. It can never report false global success.
- Invalid transitions change no project/pair state and dispatch no work.

After start, project state is derived from pair states: `COMPLETE` only when all
pairs are complete; `PAUSED` when every incomplete pair is paused;
`PARTIALLY_PAUSED` when paused and dispatchable incomplete pairs coexist;
`BLOCKED` when no incomplete pair is dispatchable and at least one is blocked;
otherwise it is `RUNNING`. Pair-level scheduled and pending states remain visible
in status and receipts without inventing extra project states.

## Execution Receipt

Every command produces one `MSLK_CONTROL_RECEIPT` plus a per-target result table
containing command ID, normalized command, actor, target scope, pre-state,
trigger, prerequisites, action, result, post-state, schedule version, and
project-wide progress. Repeating the same command ID is idempotent.

Rejected targets use one canonical outcome: `INVALID_COMMAND`, `INVALID_STATE`,
`PRECONDITION_FAILED`, `UNKNOWN_PAIR`, `SCHEDULE_CONFLICT`, or `ALREADY_APPLIED`.
Rejection preserves that target's state, schedule, progress, and role visibility.

## Scenario Verification

Tests load the JSON contract and verify at least:

- valid manual start of the complete frozen roster;
- rejection of timed initial start and late pair creation;
- all-scope and one-pair safe pauses;
- accepted-CELL threshold without overshoot;
- same-pair resume after prerequisite revalidation;
- unknown pair, missing scope, SLK, and generic command rejection;
- unaffected independent pair continuation;
- `ALL` partial failure produces explicit per-pair outcomes without false global
  success;
- cancellation and duplicate-command idempotency;
- completion cannot be reopened by a control command.

The tests must validate state transitions and roster invariants, not only string
presence.

## Context And Release Hardening

`WORK_CONTINUATION_INDEX` becomes a bounded mutable current-state pointer, not an
append-only history. Keep it below 200 lines with plan/version, active semantic
shard per pair, current Worker/GO/CELL, invariants, blockers, latest accepted
evidence, and next action. Historical detail remains in linked semantic shards.

Generic relative-Markdown-link tests start from `SKILL.md` and the contract
manifest and ensure every reachable reference exists, remains inside the
repository, is at most 1000 lines, and is MSLK-only. Every governed reference
must be reachable. The existing inspection/wake reference becomes part of the
MSLK control operations reference so one operational stage has one entry point.

README must not hardcode a rule count. Canonical metadata remains authoritative,
and publication requires matching `VERSION`, README version, repository ID,
pushed HEAD, and annotated `v1.8.0` tag.

## Acceptance

- All MSLK Markdown files are at most 1000 lines; target `SKILL.md` below 900.
- No initial timed start or late pair creation remains.
- Frozen roster, pair ownership, progress, and evidence remain stable.
- Command and scenario tests pass independently of SLK.
- Global install equals the repository by tracked-file hash.
- Remote `main` and annotated `v1.8.0` identify the same release commit.
