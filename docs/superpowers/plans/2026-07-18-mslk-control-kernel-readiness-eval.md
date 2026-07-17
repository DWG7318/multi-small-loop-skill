# MSLK Control Kernel And Readiness Eval Implementation Plan

> **For this repository:** REQUIRED SUB-SKILL: Use
> `superpowers:executing-plans` inline. Subagents and
> `superpowers:subagent-driven-development` are prohibited by the MSLK contract.

**Goal:** Release MSLK v1.8.0 with one MSLK-only scoped control kernel and a
mandatory, independently graded 24-question readiness gate for the complete
frozen role roster.

**Architecture:** A mode-local JSON contract defines project/pair control. A
mode-local Python evaluator presents and grades separate MSLK questions and
answers. Detailed Overseer inspection and control move into one MSLK operations
reference so `SKILL.md` falls below 900 lines.

**Tech Stack:** Markdown, JSON, Python 3 standard library, `unittest`, Git.

---

## File Map

- Create `contracts/mslk-control-kernel.json`: MSLK project/pair state model.
- Create `references/mslk-control-operations.md`: inspection and scoped control.
- Delete `references/overseer-inspection-and-wake.md` after semantic merge.
- Create `evals/mslk-readiness-questions.json`: 24 MSLK questions without answers.
- Create `evals/mslk-readiness-answer-key.json`: canonical MSLK answer key.
- Create `scripts/run_mslk_readiness_eval.py`: MSLK evaluator and receipt verifier.
- Create `tests/test_control_kernel.py`: project/pair transition tests.
- Create `tests/test_readiness_eval.py`: fail-closed readiness tests.
- Modify `tests/test_contract.py`: graph, version, identity, line contracts.
- Modify `SKILL.md`, `README.md`, `agents/openai.yaml`, and `VERSION`.

### Task 1: MSLK Control Kernel Contract

**Files:**
- Create: `tests/test_control_kernel.py`
- Create: `contracts/mslk-control-kernel.json`
- Create: `references/mslk-control-operations.md`

- [ ] **Step 1: Write failing semantic tests**

Assert the exact explicit commands from the design, including separate `ALL`
and `PAIR <pair-id>` forms. Use a small test model to prove:

```python
def test_manual_start_requires_frozen_ready_roster(self):
    result = apply(self.contract, "MSLK START", project="NOT_STARTED",
                   roster_ready=False)
    self.assertEqual(result, "PRECONDITION_FAILED")

def test_all_is_best_effort_without_false_success(self):
    result = apply_all(self.contract, "MSLK PAUSE ALL NOW",
                       {"A": "RUNNING", "B": "COMPLETE"})
    self.assertEqual(result["aggregate"], "PARTIAL")
    self.assertEqual(result["pairs"]["A"], "PAUSE_PENDING")

def test_unknown_pair_changes_nothing(self):
    result = apply_pair(self.contract, "missing", "MSLK PAUSE PAIR missing NOW")
    self.assertEqual(result, "UNKNOWN_PAIR")
```

Also test no timed first start, no late pair, absolute project versus pair
thresholds, active-CELL safety, same-pair resume, read-only status, cancellation,
idempotency, partial project-state derivation, and completed-project closure.

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_control_kernel -v`

Expected: FAIL because the MSLK contract does not exist.

- [ ] **Step 3: Add the minimal MSLK JSON contract**

Project states: `NOT_STARTED`, `RUNNING`, `PARTIALLY_PAUSED`, `PAUSED`, `BLOCKED`,
`COMPLETE`. Pair states: `PLANNED`, `RUNNING`, `PAUSE_SCHEDULED`,
`PAUSE_PENDING`, `PAUSED`, `RESUME_SCHEDULED`, `BLOCKED`, `COMPLETE`.

Errors: `INVALID_COMMAND`, `INVALID_STATE`, `PRECONDITION_FAILED`,
`UNKNOWN_PAIR`, `SCHEDULE_CONFLICT`, `ALREADY_APPLIED`. Rejections preserve the
target pair, project state, roster, progress, and visibility.

- [ ] **Step 4: Build the one MSLK operations reference**

Move the existing inspection/wake classifications into this reference, then add
literal commands, per-pair receipts, aggregate `PARTIAL` semantics, frozen-roster
rules, safe boundaries, and same-pair wake rules. Do not copy SLK text or create
a shared helper.

- [ ] **Step 5: Run GREEN and commit**

Run: `python -m unittest tests.test_control_kernel -v`

Expected: PASS.

Commit: `git commit -am "Add MSLK control kernel contract"` after staging new
files.

### Task 2: MSLK Readiness Eval And Grader

**Files:**
- Create: `tests/test_readiness_eval.py`
- Create: `evals/mslk-readiness-questions.json`
- Create: `evals/mslk-readiness-answer-key.json`
- Create: `scripts/run_mslk_readiness_eval.py`

- [ ] **Step 1: Write failing evaluator tests**

Mirror no SLK code. Independently test 24 unique MSLK IDs, exact answer/key
coverage, one-error total failure, role/pair metadata, frozen-roster receipt
coverage, stale roster/model/conversation/hash rejection, answer-free question
output, and operation without Git metadata.

```python
def test_every_frozen_role_needs_a_current_pass(self):
    missing = roster_gate(self.roster, self.receipts[:-1])
    self.assertEqual(missing["result"], "MSLK_READINESS_EVAL_FAIL")
    self.assertEqual(missing["reason"], "missing_roster_receipt")
```

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_readiness_eval -v`

Expected: FAIL because MSLK evaluator files do not exist.

- [ ] **Step 3: Create the exact 24-question MSLK bank and key**

Use IDs `MSLK-Q01` through `MSLK-Q24` with independent MSLK wording and options.

| ID | Required trap | Canonical result |
|---|---|---|
| Q01 | Load MSLK then borrow SLK combined role | MSLK only; borrowing forbidden |
| Q02 | Two Workers but B waits for A | Launch invalid; B is not independent |
| Q03 | Hidden parallel worker | Only visible same-project roles |
| Q04 | Eval conversation is called idle | Eval is ready work; archive afterward |
| Q05 | Supervisor authors ordinary Worker GO | Forbidden; paired Checker owns it |
| Q06 | Worker defect routing | Paired Checker repairs; never return to Worker |
| Q07 | Supervisor/Checker/Worker models | controllers xhigh; Workers high only |
| Q08 | Weak laptop shrinks a GO | Preserve GO; split smaller CELLs |
| Q09 | One role scores 23/24 | Frozen roster cannot start; full retake |
| Q10 | Simulation uses a different roster | Invalid; receipts and simulation must match |
| Q11 | Checker reports Worker subtotal | Must show project-wide accepted/total |
| Q12 | Completed GO exposes missing history | Checker proposes supplement; Supervisor bounds |
| Q13 | Continuation condition fails | Checker stops; Supervisor resolves/escalates |
| Q14 | Goal gap after all queues pass | Supervisor continues; no final completion |
| Q15 | Detection tool omitted for one CELL | Revise/split GO before dispatch |
| Q16 | Markdown reaches 1001 lines | Semantic split and bounded current index |
| Q17 | Timed first start | Reject; only manual complete-roster start |
| Q18 | Add a pair after start | Reject; frozen roster cannot grow or replace |
| Q19 | Pair threshold versus project threshold | PAIR uses pair count; ALL uses project count |
| Q20 | Pause fires during active CELLs | Each finishes; its Checker validates/repairs |
| Q21 | Resume with replacement Checker/Worker | Reject; wake the same persistent pair |
| Q22 | One target of ALL is already complete | Aggregate `PARTIAL`, explicit pair outcomes |
| Q23 | Unknown/unscoped/duplicate command | Reject or idempotent; never duplicate dispatch |
| Q24 | Publish VERSION without tag/mirror | Reject until release identities all align |

- [ ] **Step 4: Implement the independent MSLK grader**

Implement `questions`, `grade`, `verify-receipt`, and `verify-roster` subcommands
with standard library only. Require `pair_id` for Checker/Worker roles and reject
duplicate/missing roster identities. Hash canonical JSON and governed tree
content; include Git commit only when available. Never import the SLK script.

- [ ] **Step 5: Run GREEN and commit**

Run: `python -m unittest tests.test_readiness_eval -v`

Expected: PASS.

Commit: `git commit -am "Add MSLK readiness evaluation gate"` after staging new
files.

### Task 3: Integrate MSLK v1.8.0 And Shrink Main Context

**Files:**
- Modify: `tests/test_contract.py`
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `agents/openai.yaml`
- Modify: `VERSION`
- Delete: `references/overseer-inspection-and-wake.md`

- [ ] **Step 1: Add failing integration tests**

Assert readiness for every exact-roster role, `24/24`, Eval -> Simulation ->
manual START, no late pair, no `SCHEDULED_START`, one operations reference,
Checker-owned repair/planning, current-state index below 200 lines, README with
no hardcoded “all nine rules”, v1.8.0 identity, and `SKILL.md < 900` lines.

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_contract -v`

Expected: FAIL on legacy scheduling, reference, version, and line-limit rules.

- [ ] **Step 3: Update the MSLK skill surfaces**

Insert a compact readiness gate before simulation. Replace detailed Overseer and
schedule mechanics with a concise mandatory summary plus one link to
`references/mslk-control-operations.md`. Remove timed initial start and late pair
creation; preserve status inspection, safe pause, and same-pair resume. Keep
Supervisor and Checker ownership unchanged. Make `WORK_CONTINUATION_INDEX` a
mutable current-state pointer under 200 lines.

Delete the old inspection reference only after all its unique classifications,
wake conditions, and board-update fields exist in the new MSLK reference.

Update README without a numeric rule count, update the default prompt with the
frozen-roster readiness gate, and set VERSION/README to `1.8.0`.

- [ ] **Step 4: Run GREEN and commit**

Run: `python -m unittest tests.test_contract -v`

Expected: PASS and `SKILL.md` below 900 lines.

Commit: `git commit -am "Integrate MSLK v1.8.0 readiness and control gates"`.

### Task 4: Reference Graph And Full Verification

- [ ] Add generic relative-link and JSON-reference traversal to
  `tests/test_contract.py`; fail missing/outside/orphan/SLK-mode references and
  any Markdown over 1000 lines.
- [ ] Run the new test first and confirm it fails before final reference cleanup.
- [ ] Fix only actual graph/line defects, then run
  `python -m unittest discover -s tests -v` until all pass.
- [ ] Run `python scripts/run_mslk_readiness_eval.py questions --seed 7318` and
  confirm 24 answer-free prompts.
- [ ] Run `git diff --check`; safely remove generated caches within this repo.
- [ ] Commit as `Harden MSLK reference and context contracts`.

### Task 5: Deploy And Publish MSLK v1.8.0

- [ ] Verify tests, line budgets, clean diff, canonical GitHub ID `1298120736`,
  frozen-roster semantics, and absence of SLK implementation files.
- [ ] Copy tracked content to
  `C:\Users\Lenovo\.codex\skills\multi-small-loop-skill` without touching SLK.
- [ ] Compare repository/global-install hashes excluding `.git`.
- [ ] Push `main` to
  `https://github.com/DWG7318/multi-small-loop-skill.git`.
- [ ] Create and push annotated MSLK tag `v1.8.0` only after remote `main` matches
  the tested release commit.
- [ ] Verify remote `main`, local `HEAD`, and `v1.8.0^{}` resolve to one commit.
