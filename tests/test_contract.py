from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
PROMPT = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
ALL_TEXT = "\n".join((SKILL, README, PROMPT))
NORMALIZED_SKILL = " ".join(SKILL.split())


class MultiSmallLoopContractTest(unittest.TestCase):
    def test_mode_is_strictly_exclusive(self):
        self.assertIn("invoke MSLK exactly once", SKILL)
        self.assertIn("do not borrow SLK's combined Supervisor/Checker", SKILL)
        self.assertIn("Shared rules never transfer role ownership", SKILL)
        self.assertIn("current run never converts itself into SLK", SKILL)
        self.assertIn("Never load, borrow, combine, or switch to SLK", PROMPT)

    def test_topology_and_role_ownership(self):
        self.assertIn(
            "one distinct Supervisor plus multiple persistent Checker/Worker pairs",
            SKILL,
        )
        self.assertIn(
            "project decomposition, cross-Worker contracts, Supervisor board, and final audit | Supervisor",
            SKILL,
        )
        self.assertIn(
            "initial solution, GO/CELL plan, and evidence-driven GO revision | Its paired Checker",
            SKILL,
        )
        self.assertIn(
            "CELL assignment, validation, repair, routing, progress display, and per-Worker queue | Its paired Checker",
            SKILL,
        )
        self.assertNotIn("Produce or approve each Worker", SKILL)
        self.assertNotIn("fixed retry policy", SKILL)
        self.assertIn("Send formal tasks directly to its paired Worker", SKILL)
        self.assertIn("never subagents or a combined role", PROMPT)

    def test_optional_goal_gate_preserves_checker_planning(self):
        required = (
            "## Optional Goal Gate",
            "The Owner may define one optional Goal",
            "Checker completion is provisional",
            "The Supervisor must independently validate the Goal",
            "GOAL_SATISFIED",
            "GOAL_GAP",
            "must not declare project completion",
            "Each affected Checker designs its own PLAN/GO/CELL continuation",
            "The Supervisor must not author those detailed Checker plans",
            "If no Goal is configured",
            "An untested Goal or `GOAL_GAP` remains unfinished Supervisor work",
        )
        for rule in required:
            with self.subTest(rule=rule):
                self.assertIn(rule, NORMALIZED_SKILL)

    def test_continuation_condition_gate_stops_checker_dispatch(self):
        required = (
            "## Continuation Condition Gate",
            "The Checker must stop dispatching formal tasks",
            "CONDITION_BLOCKED",
            "report the condition to the Supervisor",
            "The Supervisor decides whether Owner assistance is required",
            "OWNER_ASSISTANCE_REQUIRED",
            "OWNER_ASSISTANCE_RECEIVED",
            "SUPERVISOR_RESOLVED",
            "RESUME_AUTHORIZED",
            "wake the same Checker",
            "The Checker must revalidate every blocked condition before dispatching",
        )
        for rule in required:
            with self.subTest(rule=rule):
                self.assertIn(rule, NORMALIZED_SKILL)

    def test_optional_overseer_schedule_controls_selected_loops_safely(self):
        required = (
            "## Optional Overseer Control Schedule",
            "The Owner may preconfigure one optional Overseer control schedule",
            "accepted CELL threshold",
            "target all loops or named Checker/Worker pairs",
            "SCHEDULED_START",
            "SCHEDULED_PAUSE",
            "PAUSED_BY_POLICY",
            "RESUMED_BY_POLICY",
            "must not interrupt an active CELL",
            "does not pre-create idle Workers",
            "wake the same Checker",
            "A paused loop is not complete",
        )
        for rule in required:
            with self.subTest(rule=rule):
                self.assertIn(rule, NORMALIZED_SKILL)

    def test_checker_detection_system_and_supervisor_capability_supply(self):
        required = (
            "## Checker Detection System",
            "Every Checker must maintain one evolving detection system",
            "The Supervisor must provision every Checker",
            "DETECTION_CAPABILITY_MANIFEST",
            "mature detection skills",
            "`superpowers:verification-before-completion`",
            "`superpowers:systematic-debugging`",
            "`superpowers:test-driven-development`",
            "`security-best-practices`",
            "`playwright`",
            "skill source, version, and compatibility",
            "Any skill that requires subagents is incompatible",
            "CodeGraph is mandatory for code or repository work",
            "layered detection stack",
            "Semgrep or CodeQL",
            "Gitleaks",
            "OSV-Scanner or Trivy",
            "Playwright",
            "coverage and mutation testing",
            "API or schema contract",
            "tool version, configuration, and omission rationale",
            "split or serialize the detection commands",
            "not acceptance quality",
            "structural and dependency baseline",
            "acceptance matrix",
            "false-positive",
            "REGRESSION_EVIDENCE",
            "CONDITION_BLOCKED",
            "must not accept a CELL from Worker self-report alone",
            "update the next CELL, GO revision, or supplementary GO",
            "Checker-specific tool access",
        )
        for rule in required:
            with self.subTest(rule=rule):
                self.assertIn(rule, NORMALIZED_SKILL)

    def test_shared_rules_remain_inside_mslk(self):
        required = (
            "Never use a subagent",
            "SIMULATION_PASS",
            "Archive it immediately",
            "GO_REVISION_SIMULATION_PASS",
            "must not send a repair task back to the Worker",
            "`gpt-5.5` with `high` reasoning as the minimum",
            "`gpt-5.6-sol` with `high` reasoning as the maximum",
            "GO scope follows project need and must not be reduced for device capacity",
            "CELL size must be kept modest enough for the current computer",
            "正在完成 GO-03：35/231",
            "全部完成：231/231",
            "not a per-Worker subtotal",
            "Supervisor remains the sole writer of the Supervisor board",
        )
        for rule in required:
            with self.subTest(rule=rule):
                self.assertIn(rule, ALL_TEXT)

        self.assertNotIn("Formal rework:", ALL_TEXT)
        self.assertNotIn("planner", ALL_TEXT.lower())


if __name__ == "__main__":
    unittest.main()
