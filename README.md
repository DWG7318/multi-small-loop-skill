# small-loop-method

Small-loop method skill for WLflow/WellLinkflow planning, worker dispatch,
supervisor-owned blocker repair, QC, and routing.

Current version: `0.2.0`

## Files

- `SKILL.md`: skill instructions.
- `VERSION`: release version.
- `agents/openai.yaml`: agent metadata.

## Boundary

The supervisor owns judgment, diagnostics, blocker repair, QC, and routing.
`WLflow worker` executes normal bounded construction cells.
