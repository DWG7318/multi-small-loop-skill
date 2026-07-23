# MSLK Control Operations

## Manual project start

`MSLK START` authorizes the frozen Calabash baseline, persistent Chain roster,
ordered Level plan, autonomy envelope, and Level-01 activation preparation. It does
not require Owner approval for each CELL, GO, Verification, or later Level.

## Level activation

Before opening one Level, Supervisor:

1. verifies every prior Level is `LEVEL_VERIFIED`;
2. verifies all listed GOs are launch-ready together;
3. confirms no peer GO dependency exists;
4. creates every GO's fresh Verification attempt;
5. binds isolated environments, model identities, evidence paths, and direct routes;
6. obtains role readiness and Verification preflight;
7. records `LEVEL_START_GATE_PASS`;
8. authorizes all Checkers to dispatch first CELLs in the same activation cycle.

No partial Level start is allowed.

## Direct Verification handoff

After a Checker accepts all CELLs, it sends the frozen neutral package directly to
the pre-established Verification. Supervisor must not relay, rewrite, summarize, or
add a verdict suggestion.

Verification sends its signed verdict directly to Checker and Supervisor. Checker
handles evidence work or Worker rework. Supervisor updates GO/Level state and handles
only plan, shared, safety, autonomy, or Owner-exclusive issues.

## Level barrier

Verified early GOs freeze outputs and wait. The next Level opens only after all
required current-Level GOs are `GO_VERIFIED`, at which point Supervisor records
`LEVEL_VERIFIED` and runs the next Level start gate.

## Safe pause

Pause new dispatch at a CELL or GO-verdict boundary. Do not interrupt an active
Worker or Verification. A pause is not acceptance and does not open a later Level.

## Resume

Supervisor records `RESUME_AUTHORIZED`. The same persistent Checker revalidates
conditions; a changed GO candidate uses a new Verification attempt. Resume never
requires routine Owner approval.

## Safeguard patrol

Supervisor may inspect control state, resolve provisioning, repair authorization,
prepare versioned plan correction, and restore progress. It must not execute Worker
work, perform Checker validation, issue a GO verdict, partially open a Level, inject
suggestions into Verification, or ask Owner for routine authorization.

## Owner-free autonomy

`PROJECT_AUTONOMY_ENVELOPE` pre-authorizes routine plan-scoped work. Only Supervisor
may emit `OWNER_ASSISTANCE_REQUIRED`, and only for one proven Owner-exclusive item.
A generic confirmation request is `AUTONOMY_VIOLATION`.

Platform permission friction is first handled by provisioning/preauthorization. If
unavoidable, record `EXECUTION_PERMISSION_BLOCKED` with exact evidence.

## Control receipts

Every control action records an idempotent receipt with Calabash/plan version, Level,
Chain and role IDs, candidate identity where relevant, old/new state, evidence, and
result.
