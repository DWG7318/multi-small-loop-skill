# small-loop-method

Project-neutral method skill for constructing and operating supervisor-worker
Loops with small cells, evidence-based QC, blocker repair, and routing.

Current version: `0.2.3`

## Files

- `SKILL.md`: skill instructions.
- `VERSION`: release version.
- `agents/openai.yaml`: agent metadata.

## Boundary

The supervisor owns judgment, diagnostics, blocker repair, QC, and routing.
The designated worker executes one bounded cell at a time. Project names,
paths, models, infrastructure, and safety boundaries are supplied by the
active Loop or project and are not embedded in this method.

Version `0.2.3` makes worker-caused QC repair supervisor-owned. After repairing
and verifying the current cell, the supervisor sends one combined repair update
and next-cell assignment instead of returning the correction to the worker.
