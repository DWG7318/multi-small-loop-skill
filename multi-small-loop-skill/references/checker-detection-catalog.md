# MSLK Checker Detection Catalog

## Capability inventory versus allocation

`DETECTION_CAPABILITY_MANIFEST` records what a Checker can truly execute.

`GO_DETECTION_PROFILE` allocates required capabilities to one GO and assigns each
to exactly one execution tier.

## Tiers

### CELL_ALWAYS

Fast, high-signal checks required for every candidate, such as:

- native formatter/linter/type checker for affected code;
- focused unit or contract checks;
- secret scan on changed content;
- artifact identity and write-scope checks;
- method-log and Markdown line-budget checks.

### CELL_TRIGGERED

Checks with frozen predicates, such as:

- CodeGraph impact analysis when source topology changes;
- Semgrep/CodeQL rules when relevant languages or paths change;
- dependency or container scans when lockfiles/manifests change;
- Playwright when user-facing flows change;
- migration checks when schemas change;
- permission/security checks when policy surfaces change.

A false predicate produces `NOT_TRIGGERED` with evidence. Plain “not applicable” is
invalid.

### GO_BOUNDARY

The GO's pre-established fresh Verification executes complete Calabash-grounded outcome checks, such as:

- end-to-end user or business flow;
- full GO contract and state-transition suite;
- GO-wide regression;
- required screenshots, events, audit trail, or reproducible evidence;
- frozen-output compatibility;
- mutation, performance, reliability, or safety checks assigned to the GO.

### PROJECT_FINAL

A fresh project-final Verification executes cross-Level and cross-GO technical checks when allocated,
such as:

- integrated end-to-end path;
- cross-domain contract compatibility;
- full security/dependency scan;
- release/build/deployment candidate checks;
- project-wide performance or recovery exercises.

Supervisor consumes these independent receipts during final composition audit; they do not replace GO verdicts or Level barriers.

## Receipts

Each execution records:

```text
capability_id
tier
version
configuration_hash
trigger_predicate
trigger_result
command_or_action
candidate_identity
environment_id
result
evidence_reference
```

Valid results:

```text
RUN_PASS
RUN_FAIL
NOT_TRIGGERED
BLOCKED
```

Worker checks do not replace Checker checks. Checker checks do not replace
Verification checks. Another domain's evidence never satisfies the local receipt.
