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
