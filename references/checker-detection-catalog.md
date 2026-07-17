# MSLK Checker Detection Catalog

This reference belongs only to MSLK. It does not authorize SLK topology,
subagents, hidden roles, or a combined Supervisor/Checker. Read it before any
Checker defines a `GO_DETECTION_PROFILE`.

## Mature Detection Skills

Provision mature detection skills for every Checker with Checker-specific tool
access. The baseline catalog is `superpowers:verification-before-completion`,
`superpowers:systematic-debugging`, `superpowers:test-driven-development`,
`security-best-practices`, and `playwright`, plus trusted official or established
language/framework inspection skills selected for each Worker's stack.

Record each skill source, version, and compatibility with the Checker domain and
current Codex environment. Confirm it is installed and readable. Any skill that
requires subagents is incompatible with MSLK and must not be loaded. A skill
guides one visible Checker but never becomes a hidden role or transfers
acceptance authority.

## Mature Detection Tools

CodeGraph is mandatory for code or repository work when relevant source can be
indexed. Each Checker establishes the structural and dependency baseline,
ownership boundary, entry points, call/dependency paths, and affected closure for
its Worker before the first CELL. Refresh the changed graph slice after each CELL
and the broader domain baseline at GO and final acceptance. One Checker's graph
or evidence never counts as another Worker's acceptance evidence.

Build a task-fit layered detection stack from mature tools:

- native compiler, type checker, formatter, linter, and test runner;
- CodeGraph, diff, and ownership-boundary inspection;
- Semgrep or CodeQL with pinned project rules;
- Gitleaks with reviewed allowlists;
- OSV-Scanner or Trivy, with SBOM/container checks when relevant;
- focused/regression tests plus coverage and mutation testing;
- Playwright or an equivalent real runtime harness;
- Spectral, Schemathesis, or another API or schema contract validator.

Record tool version, configuration, and omission rationale in the GO plan. An
unselected catalog layer needs a risk-based plan rationale; convenience, speed,
or Worker confidence is not a rationale.

## Precision And Learning

Every Checker maintains an acceptance matrix mapping every criterion to an
independent action, expected result, and evidence path. Maintain a false-positive
register with reviewed suppressions and expiry/revisit conditions; never silence
a finding only to make a scan green.

Record focused, graph-impact, regression, security, and runtime results as
`REGRESSION_EVIDENCE` linked to CELL, Worker, GO profile, and manifest versions.
A Checker must not accept a CELL from Worker self-report alone. Tool output is
evidence, not the acceptance decision: reconcile conflicts and preserve redacted
raw summaries or stable references.

After every accepted CELL and GO, calibrate from escaped defects, noisy rules,
new dependencies, and changed risk. Detection evidence may update the next CELL,
GO revision, or supplementary GO only through the versioned planning rules.

If a required skill, tool, permission, or safe execution capacity is unavailable,
the affected Checker records `CONDITION_BLOCKED` and reports the gap to the
Supervisor. The Supervisor provisions or resolves shared capability, or requests
specific Owner assistance. Never silently substitute a weaker capability,
borrow another Checker's evidence, or accept an incomplete detection system.
