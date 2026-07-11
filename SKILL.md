---
name: small-loop-method
description: Project-neutral small-loop method for designing and running reliable supervisor-worker Loops. Use only when constructing or operating a Loop with GO/cell slicing, worker dispatch, evidence-based QC, repair routing, progress replies, and failure escalation. Do not trigger it merely because a particular project or repository is in scope.
---

# Small-loop Method

Use this skill to keep Loop work small, checkable, and reliable.

The supervising thread acts as supervisor, planner, checker, and router. The
designated worker executes one bounded cell at a time and returns evidence.

## Applicability

This is a Loop-construction method, not a project policy. Apply it only when a
supervisor-worker Loop is being designed or operated. Project names,
repositories, directories, tools, asset boundaries, infrastructure rules,
credentials, model locks, and release policies must come from the active
project or the Owner; this skill must not invent or permanently embed them.

## Supervisor And Worker Boundary

The supervisor must not degrade into a passive messenger. The supervisor owns
judgment, diagnosis, repair routing, QC, and next-step decisions.

Default split:

- The designated worker executes normal bounded construction cells.
- The supervisor designs the cell, sends the task, checks evidence, records
  decisions, and routes the next step.
- The supervisor directly repairs worker-caused QC defects, abnormal
  diagnostics, and blockers that are within tool reach and do not require
  Owner hands-on action.

### Supervisor-Owned QC Repair

When a worker delivery fails QC because the worker made an error, the
supervisor must repair it directly. Do not return the same correction to the
worker.

1. Keep the current cell and `X/Y` unchanged.
2. Back up or preserve the pre-repair state, make the minimum correction, and
   rerun the relevant acceptance checks.
3. Record the original worker task, QC defects, supervisor changes, checks, and
   final route in durable evidence.
4. After the repair passes, include a concise `supervisor repair update` in the
   next new-cell task package, then assign that next cell in the same message.
   Do not send a separate update-only message.
5. The combined update plus next-cell dispatch is still a direct worker
   dispatch and must be the final action of the supervisor turn.

If the supervisor cannot safely perform the repair with available tools and
authority, route `blocked` or `owner-decision` as appropriate. Do not transfer
the worker's correction back to that worker merely because the supervisor is
blocked.

When a worker reports `blocked`:

1. Diagnose the blocker as supervisor.
2. If the supervisor can safely fix or narrow the blocker, do it directly with
   backup, minimum change, evidence, and verification.
3. If the blocker is cleared, route the next normal construction cell back to
   the designated worker; do not continue locally as the executor unless that next
   cell is itself another blocker repair.
4. If the blocker cannot be solved without Owner hands-on action, ask the
   Owner only for that hands-on action.

Within the authority granted by the active Loop, the supervisor should not stop
to ask for generic permission. Ask the Owner only when the
action requires their manual work or private external input, such as restarting
hardware, changing cables, scanning a code, logging in, entering a one-time
code, visually confirming a UI, providing unknown credentials, or making a
business/content choice that cannot be inferred from project rules.

Loop authority never overrides the active project's safety and ownership
boundaries.

## Source Of Truth

Use the active Loop specification, GO map, cell registry, model policy, and
matching cell plan supplied by the current project as authoritative. This skill
does not define their filenames or locations. Do not copy a whole plan into a
worker prompt; read and send only what the current cell needs.

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

The supervisor model and worker model are independent. Use the model family and
allowed reasoning tiers declared by the active Loop; do not hardcode a project
model in this method. Every direct dispatch must explicitly select the worker
model/profile required by that Loop and one appropriate reasoning level:

- `medium`: routine read-only checks, counts, simple document edits,
  indexing, and low-ambiguity bounded work.
- `high`: multi-document consistency, cross-system contracts, runtime design,
  project boundaries, security-sensitive checks, and moderate
  ambiguity.
- `xhigh`: installs, incident debugging, irreversible risk,
  repeated failure, and difficult blocker repair.

Risk shortcuts:

- Infrastructure, publishing, account, credential, or protected-asset write
  risk: start at `high` or `xhigh`.
- Repeated failure on the same cell: raise model level and split smaller.

## Failure Escalation

- First worker-caused failure: the supervisor repairs the current cell and
  records the defect. Missing input or a mechanical mistake need not raise the
  next worker model level.
- Second worker-caused failure: the supervisor still repairs directly, raises
  the next new-cell worker level, and splits that next cell smaller.
- Third worker-caused failure: the supervisor still owns the correction; use
  the highest allowed worker level for the next new cell or route `blocked` /
  `owner-decision` when continued delegation is not reliable.

Never loop the same correction back to the worker. Failure history changes the
design and model of future new-cell assignments; it does not transfer QC repair
ownership away from the supervisor.

## Worker Task Package

Before sending work to the designated worker, include:

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
- exact worker completion text when progress numbering is active, such as
  `完成X/Y，请检验`

Before dispatch, validate the return route:

- The delegation envelope `source_thread_id` and the task package's source
  supervisor/checker thread id must be identical.
- The source supervisor/checker thread id must not equal the destination worker
  thread id.
- If either check fails, do not dispatch. Correct the route first.

Direct worker dispatch is terminal. If the supervisor sends a direct thread
message to the designated worker, that send must be the final action of the
supervisor turn. After sending, the supervisor does not wait, poll, inspect the
worker thread, run follow-up commands, or continue other work in the same turn.

Worker completion replies mean only "ready for checking"; they do not mean
accepted.

## Worker Reply Protocol

Every cell must end with a worker reply to the supervisor/checker.

For normal cell completion, the supervisor must include the exact current
ordinal and executable-cell total in the worker task package. The completion
reply must use:

```text
完成X/Y，请检验
```

Rules:

1. `X` is the current executable cell's fixed ordinal assigned by the
   supervisor.
2. `Y` is the authoritative executable-cell total from the cell plan; parent GO
   headings and non-executing grouping headings do not count.
3. The supervisor must write the exact `X/Y` into every worker task package.
   The worker must not guess, calculate, or modify the numbers.
4. Rework, repair, or QC closeout for the same current cell keeps the same
   `X/Y`.
5. `X/Y` increments only after supervisor QC accepts the current cell and the
   supervisor dispatches the next cell.
6. If the plan changes, only the supervisor recalculates `Y`; the worker must
   not change it locally.
7. The same-thread return message and the worker's own final visible reply must
   use the exact same completion text supplied by the task, including `X/Y`
   exactly.
8. Before returning, the worker must verify that the return target is not its
   own worker thread. If the delegation envelope and textual return target
   disagree, or the return target equals the worker thread, do not self-send;
   reply `blocked: return target mismatch` with durable evidence.

If direct thread messaging is available, the worker must send the same pure
completion text back to the source supervisor/checker thread by the same
thread messaging method used for dispatch. The worker then ends its own visible
reply with exactly that same text.

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

If QC is `rework`, the supervisor performs the correction directly inside the
same cell and `X/Y`, then reruns QC. The supervisor must not dispatch that
correction back to the worker.

After supervisor repair passes, prepare the next exact GO/cell task. Include a
concise repair update naming the previous cell, defect, supervisor fix, and
verification result, then dispatch the next cell in that same message as the
final action of the supervisor turn.

If QC is `blocked` or `owner-decision`, do not invent the next task. Record the
blocker or ask the Owner.

Use `owner-decision` for unresolved Owner choices. Do not silently assume them.

If QC is `blocked` because of a local infrastructure/runtime/tooling issue that
the supervisor can inspect or fix, the supervisor should repair or narrow it
directly before asking the Owner. After a supervisor repair, send the next
normal construction cell to the designated worker as the final action.

## Formal Blocker Closure

A cell may intentionally produce formal blocked evidence when its acceptance
standard is to prove that continuing would be unsafe, unsupported, or missing
required external proof. If QC accepts that blocked evidence:

- record the blocker as the current route state;
- preserve the worker's progress ordinal for the blocked cell;
- do not dispatch the nominal next cell;
- do not turn a blocked gate into `passed` just to keep the loop moving;
- list the exact missing evidence, Owner/manual action, or external proof
  needed;
- route only to a blocker-repair cell, Owner/manual input, or a future task
  explicitly allowed by the blocked evidence.

If accepted evidence says future cells are not unblocked, the supervisor must
treat that as authoritative until a later accepted repair/proof cell changes
it. A worker completion phrase means "ready for checking", not "accepted"; the
supervisor's QC route is the only route state.

## Safety

- Inherit safety, filesystem, infrastructure, asset, and approval boundaries
  from the active project; do not define project-specific exceptions here.
- Do not put credentials, cookies, tokens, or private account material in logs.
- A Loop method never broadens the authority granted by the Owner or project.
