# Changelog

## 1.9.0

- Defined MSLK as staged, barrier-synchronized multi-chain execution.
- Added fixed `LEVEL`, `CHAIN`, and `GO-<LEVEL>-<CHAIN>` semantics.
- Added mandatory full/Minimum Calabash and `GO_CALABASH_TRACE`.
- Added pre-bound, pre-established Verification with direct Checker handoff and
  direct verdict delivery to Checker and Supervisor.
- Added full Level start/completion barriers and prohibited partial unlock.
- Added `PROJECT_AUTONOMY_ENVELOPE`; routine Owner authorization is forbidden.
- Required Checker/Verification isolation across conversation, context, workspace,
  runtime state, model binding, input, evidence, and lifecycle.
- Restored Worker ownership of product rework.
- Replaced `REDO` with `CELL_REWORK` and `PLAN_DEFECT`.
- Separated CELL acceptance, GO Verification, Level completion, and project audit.
- Prohibited cross-GO CELL dependencies and same-Level peer dependencies.
- Added tiered detection.
- Renamed optional Goal to `PROJECT_GOAL`.
- Kept Grapher, conditional routing, partial unlock, cycles, and dynamic Chains in
  GLK rather than MSLK.
