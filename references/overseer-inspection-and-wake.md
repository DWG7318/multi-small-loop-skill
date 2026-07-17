# MSLK Overseer Inspection And Wake

This reference belongs only to MSLK and continues the mandatory Overseer stage
from `SKILL.md`. It never authorizes SLK, hidden work, replacement roles, or a
detached monitoring task.

## Quick Inspection

For every unfinished Worker, inspect only what is needed:

1. Supervisor board state and planned CELL total.
2. Passed/blocked final queue records.
3. Checker and Worker thread status and latest turn.
4. Latest formal task, repair record, or completion receipt.
5. Method-log/artifact timestamp when thread state is ambiguous.

Classify the Worker as `active_worker`, `active_checker`,
`waiting_for_worker_delivery`, `waiting_for_checker_validation`, `blocked`,
`stalled`, or `complete`.

## Wake Rule

If the Worker is incomplete and neither role is active, notify the Checker to
continue unless a real blocker or plan defect exists. Do not tell the Worker to
self-select work. Cross-Worker dependency waiting means invalid decomposition or
premature role creation, not a healthy active state.

Route the observed situation:

- Worker delivered but Checker stopped: wake that Checker to validate and route.
- Checker accepted but sent no next CELL: wake it to send one formal task.
- Worker ended without delivery: Checker inspects and repairs usable partial
  output; only with no usable result may it re-dispatch the original CELL.
- Receipt was lost: Checker inspects artifacts and performs one routing repair.
- Another Worker's future output is required: record `PLAN_DEFECT`, revoke the
  premature pair, and redesign or defer it; never keep an idle loop.
- `CONDITION_BLOCKED` exists: Supervisor makes the Owner-assistance decision;
  after `SUPERVISOR_RESOLVED`, record `RESUME_AUTHORIZED` and wake the same
  Checker for prerequisite revalidation.
- A role is active: do not interrupt it.
- A passed queue exists and final acceptance succeeds: stop monitoring it.

A wake message names the current CELL, cites the observed stop, and requires the
Checker to send or validate exactly one next action. It must not become a Worker
task package.

## Overseer Record

Update the supervisor board after each inspection:

```md
| Worker | Checker | State | Current CELL | Final queue | Next signal |
|---|---|---|---|---|---|
```

Report active Workers, repaired Workers, blockers, and the next expected signal
to the Owner in one compact status update.
