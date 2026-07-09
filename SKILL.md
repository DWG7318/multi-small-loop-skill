---
name: small-loop-method
version: 0.2.0
description: Small-loop method for planning and supervising reliable GO/cell work. Use when the user asks to design, refine, dispatch, QC, or review WLflow/WellLinkflow work; split GO nodes into small cells; assign model levels; route worker tasks; enforce terminal worker dispatch, same-method worker reply, QC-before-next-cell routing, supervisor-owned blocker repair, and default Owner authorization; handle repeated failures; or apply Loop Engineering style supervisor/planner/checker/router execution. Formerly wlflow-loop-construction.
---

# Small-loop Method

Use this skill to keep WLflow work small, checkable, and reliable.

The main thread acts as supervisor, planner, checker, and router. `WLflow worker`
executes one bounded cell at a time and returns evidence.

## Supervisor And Worker Boundary

The supervisor must not degrade into a passive messenger. The supervisor owns
judgment, diagnosis, repair routing, QC, and next-step decisions.

Default split:

- `WLflow worker` executes normal bounded construction cells.
- The supervisor designs the cell, sends the task, checks evidence, records
  decisions, and routes the next step.
- The supervisor directly handles abnormal diagnostics and blocker repairs that
  are within tool reach and do not require Owner hands-on action.

When a worker reports `blocked`:

1. Diagnose the blocker as supervisor.
2. If the supervisor can safely fix or narrow the blocker, do it directly with
   backup, minimum change, evidence, and verification.
3. If the blocker is cleared, route the next normal construction cell back to
   `WLflow worker`; do not continue locally as the executor unless that next
   cell is itself another blocker repair.
4. If the blocker cannot be solved without Owner hands-on action, ask the
   Owner only for that hands-on action.

Owner authorization is assumed for WLflow-scoped supervisor decisions and
repairs. Do not stop to ask for generic permission. Ask the Owner only when the
action requires their manual work or private external input, such as restarting
hardware, changing cables, scanning a code, logging in, entering a one-time
code, visually confirming a UI, providing unknown credentials, or making a
business/content choice that cannot be inferred from project rules.

Default authorization does not override hard safety boundaries. Do not read
secrets, mutate old LC assets, restore Docker, clean Docker, touch sessions or
SQLite, or disturb Codex sidebar/app state unless the relevant current rule and
Owner instruction explicitly allow that exact action.

## Source Of Truth

When working in `C:\WellLinkflow`, use these project files as authoritative:

- `docs/MASTER_PLAN.md`
- `docs/CONSTRUCTION_GO_MAP.md`
- `docs/CELL_PLAN_INDEX.md`
- `docs/CELL_GRANULARITY_MODEL_POLICY.md`
- the matching `docs/go-cells/*_CELL_PLAN.md`

Do not copy the whole plan into the prompt. Read only the current GO/cell plan
needed for the task.

## Cell Rule

Before dispatching or doing work:

1. Identify one GO.
2. Identify one exact cell.
3. Confirm the cell has one primary outcome.
4. Confirm the cell has concrete work, acceptance standard, model level, and
   escalation rule.
5. If the cell is still broad, split it before dispatch.

Do not run a worker task against a whole GO when a cell can be selected.

## Model Levels

Use the requested level as a planning label. If the current surface cannot
actually switch model parameters, record the requested level and use the
strongest available equivalent.

- `5.4中`: routine read-only checks, counts, simple document edits, indexing.
- `5.4高`: multi-document consistency, schemas, checklists, moderate ambiguity.
- `5.5高`: cross-system contracts, runtime design, old-LC boundaries, security.
- `5.5超高`: installs, incident debugging, irreversible risk, repeated failure.

Risk shortcuts:

- Docker, Kubernetes, publishing, account, credential, or old-LC write risk:
  start at `5.5高` or `5.5超高`.
- Repeated failure on the same cell: raise model level and split smaller.

## Failure Escalation

- First failure: keep level only if the cause is missing input or mechanical.
- Second failure: raise one level and split the cell smaller.
- Third failure: use `5.5超高` or route `blocked` / `owner-decision`.

Never loop indefinitely on the same failing cell.

## Worker Task Package

Before sending work to `WLflow worker`, include:

- task id
- GO id and cell id
- source supervisor thread id or exact return target
- requested model level
- objective
- allowed scope
- forbidden scope
- inputs
- expected output
- evidence path or evidence format
- acceptance standard
- stop condition
- failure route

Direct worker dispatch is terminal. If the supervisor sends a direct thread
message to `WLflow worker`, that send must be the final action of the
supervisor turn. After sending, the supervisor does not wait, poll, inspect the
worker thread, run follow-up commands, or continue other work in the same turn.

Worker final phrase `完成，请检验` means only "ready for checking"; it does not
mean accepted.

## Worker Reply Protocol

Every cell must end with a worker reply to the supervisor/checker.

Normal completion:

```text
完成，请检验
```

The worker must also provide or reference the delivery evidence before using
that phrase.

If direct thread messaging is available, the worker must send the same pure
text `完成，请检验` back to the source supervisor/checker thread by the same
thread messaging method used for dispatch. The worker then ends its own visible
reply with exactly `完成，请检验`.

If the worker cannot send that same-method return message, the cell is not a
normal completion. The worker must write the delivery evidence to the agreed
path and reply `blocked: direct return unavailable`.

For blocked work, do not use the completion phrase. Reply with:

```text
blocked: <short reason>
```

and include the evidence, missing input, or safety reason.

## Checker And Router

Check evidence, not completion claims.

After a worker reply, QC is mandatory. The supervisor must compare the delivery
against the task objective, allowed scope, forbidden scope, evidence
requirement, and acceptance standard before treating the cell as done.

Choose exactly one route:

- `passed`
- `rework`
- `continue`
- `blocked`
- `owner-decision`

If QC is `passed` and work remains, prepare the next exact GO/cell task and
dispatch it only as the final action of the supervisor turn.

If QC is `rework`, dispatch a correction task to the worker as the final action
of the supervisor turn. Include the QC defects, required fix, unchanged scope,
and acceptance standard.

If QC is `blocked` or `owner-decision`, do not invent the next task. Record the
blocker or ask the Owner.

Use `owner-decision` for unresolved Owner choices. Do not silently assume them.

If QC is `blocked` because of a local infrastructure/runtime/tooling issue that
the supervisor can inspect or fix, the supervisor should repair or narrow it
directly before asking the Owner. After a supervisor repair, send the next
normal construction cell to `WLflow worker` as the final action.

## Safety

- Keep every Markdown file at or below 999 lines; split files, do not compress
  useful content.
- Do not install or clean Docker without fresh Owner approval.
- Do not silently mutate old LCFlow assets, sessions, SQLite, or sidebar state.
- Do not copy large media into WLflow; record paths, hashes, manifests, and
  evidence instead.
- Do not put credentials, cookies, tokens, or private account material in logs.
