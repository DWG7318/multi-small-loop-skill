# small-loop-method

Small-loop method skill for WLflow/WellLinkflow planning, worker dispatch,
supervisor-owned blocker repair, QC, and routing.

Current version: `0.2.1`

## Files

- `SKILL.md`: skill instructions.
- `VERSION`: release version.
- `agents/openai.yaml`: agent metadata.

## Boundary

The supervisor owns judgment, diagnostics, blocker repair, QC, and routing.
`WLflow worker` executes normal bounded construction cells.

Worker execution is pinned to `gpt-5.5` with only `medium`, `high`, and
`xhigh` reasoning levels. The supervisor's model may change independently.
