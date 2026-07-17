import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "mslk-control-kernel.json"


def command_for(contract, command):
    for item in contract["commands"]:
        pattern = re.escape(item["syntax"])
        pattern = pattern.replace(re.escape("<pair-id>"), r"[A-Za-z0-9._-]+")
        pattern = pattern.replace(re.escape("<accepted-cell-count>"), r"[1-9][0-9]*")
        pattern = pattern.replace(re.escape("<RFC3339-time>"), r"\S+")
        if re.fullmatch(pattern, command):
            return item
    return None


def apply_pair(
    contract,
    command,
    state,
    *,
    pair_known=True,
    active_cell=False,
    prerequisites=True,
    duplicate=False,
):
    if duplicate:
        return "ALREADY_APPLIED"
    item = command_for(contract, command)
    if item is None:
        return "INVALID_COMMAND"
    if item["scope"] == "pair" and not pair_known:
        return "UNKNOWN_PAIR"
    if item.get("read_only"):
        return state
    if state not in item["allowed_pair_states"]:
        return "INVALID_STATE"
    if not prerequisites:
        return "PRECONDITION_FAILED"
    if active_cell and item.get("safe_boundary"):
        return "PAUSE_PENDING"
    return item.get("to_by_state", {}).get(state, item["to"])


def apply_all(contract, command, pair_states):
    outcomes = {
        pair_id: apply_pair(contract, command, state)
        for pair_id, state in pair_states.items()
    }
    successes = {
        "PAUSED",
        "PAUSE_SCHEDULED",
        "PAUSE_PENDING",
        "RUNNING",
        "RESUME_SCHEDULED",
    }
    aggregate = "SUCCESS" if all(value in successes for value in outcomes.values()) else "PARTIAL"
    return {"aggregate": aggregate, "pairs": outcomes}


class MslkControlKernelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_public_command_surface_is_explicit(self):
        expected = {
            "MSLK START",
            "MSLK STATUS ALL",
            "MSLK STATUS PAIR <pair-id>",
            "MSLK PAUSE ALL NOW",
            "MSLK PAUSE PAIR <pair-id> NOW",
            "MSLK PAUSE ALL AFTER <accepted-cell-count>",
            "MSLK PAUSE PAIR <pair-id> AFTER <accepted-cell-count>",
            "MSLK PAUSE ALL AT <RFC3339-time>",
            "MSLK PAUSE PAIR <pair-id> AT <RFC3339-time>",
            "MSLK RESUME ALL NOW",
            "MSLK RESUME PAIR <pair-id> NOW",
            "MSLK RESUME ALL AT <RFC3339-time>",
            "MSLK RESUME PAIR <pair-id> AT <RFC3339-time>",
            "MSLK CANCEL SCHEDULE ALL",
            "MSLK CANCEL SCHEDULE PAIR <pair-id>",
        }
        self.assertEqual(
            {item["syntax"] for item in self.contract["commands"]}, expected
        )

    def test_manual_start_requires_complete_frozen_ready_roster(self):
        start = command_for(self.contract, "MSLK START")
        self.assertTrue(start["manual_only"])
        self.assertTrue(self.contract["roster_frozen_after_start"])
        self.assertEqual(
            start["requires"],
            [
                "MSLK_READINESS_EVAL_PASS_EXACT_ROSTER",
                "AT_LEAST_TWO_INDEPENDENT_PAIRS",
                "ALL_FIRST_CELLS_READY",
                "ALL_PLANS_AND_DETECTION_PROFILES_APPROVED",
                "SIMULATION_PASS_EXACT_ROSTER",
                "CONTINUATION_CONDITIONS_PASS",
            ],
        )
        self.assertEqual(
            apply_pair(
                self.contract,
                "MSLK START",
                "PLANNED",
                prerequisites=False,
            ),
            "PRECONDITION_FAILED",
        )
        serialized = json.dumps(self.contract, sort_keys=True)
        self.assertNotIn("START AT", serialized)
        self.assertNotIn("START AFTER", serialized)

    def test_all_is_best_effort_without_false_success(self):
        result = apply_all(
            self.contract,
            "MSLK PAUSE ALL NOW",
            {"pair-a": "RUNNING", "pair-b": "COMPLETE"},
        )
        self.assertEqual(result["aggregate"], "PARTIAL")
        self.assertEqual(result["pairs"]["pair-a"], "PAUSED")
        self.assertEqual(result["pairs"]["pair-b"], "INVALID_STATE")

    def test_threshold_scope_differs_for_all_and_pair(self):
        all_pause = command_for(self.contract, "MSLK PAUSE ALL AFTER 35")
        pair_pause = command_for(
            self.contract, "MSLK PAUSE PAIR pair-a AFTER 12"
        )
        self.assertEqual(all_pause["threshold_scope"], "project_accepted_absolute")
        self.assertEqual(pair_pause["threshold_scope"], "pair_accepted_absolute")

    def test_active_cells_reach_safe_boundary(self):
        self.assertEqual(
            apply_pair(
                self.contract,
                "MSLK PAUSE PAIR pair-a NOW",
                "RUNNING",
                active_cell=True,
            ),
            "PAUSE_PENDING",
        )

    def test_resume_reuses_same_persistent_pair(self):
        resume = command_for(self.contract, "MSLK RESUME PAIR pair-a NOW")
        self.assertTrue(resume["same_pair"])
        self.assertTrue(resume["revalidate"])
        self.assertEqual(
            apply_pair(
                self.contract, "MSLK RESUME PAIR pair-a NOW", "PAUSED"
            ),
            "RUNNING",
        )

    def test_unknown_pair_and_unscoped_commands_fail_closed(self):
        self.assertEqual(
            apply_pair(
                self.contract,
                "MSLK PAUSE PAIR missing NOW",
                "RUNNING",
                pair_known=False,
            ),
            "UNKNOWN_PAIR",
        )
        for command in (
            "MSLK STATUS",
            "MSLK PAUSE NOW",
            "SLK START",
            "LOOP START",
            "MSLK ADD PAIR pair-c",
        ):
            with self.subTest(command=command):
                self.assertEqual(
                    apply_pair(self.contract, command, "RUNNING"),
                    "INVALID_COMMAND",
                )

    def test_status_is_read_only(self):
        for command in ("MSLK STATUS ALL", "MSLK STATUS PAIR pair-a"):
            for state in self.contract["pair_states"]:
                with self.subTest(command=command, state=state):
                    self.assertEqual(
                        apply_pair(self.contract, command, state), state
                    )

    def test_cancel_and_duplicate_do_not_dispatch(self):
        cancel = command_for(
            self.contract, "MSLK CANCEL SCHEDULE PAIR pair-a"
        )
        self.assertFalse(cancel["dispatch"])
        self.assertEqual(
            apply_pair(
                self.contract,
                "MSLK CANCEL SCHEDULE PAIR pair-a",
                "RESUME_SCHEDULED",
            ),
            "PAUSED",
        )
        self.assertEqual(
            apply_pair(
                self.contract,
                "MSLK PAUSE PAIR pair-a NOW",
                "RUNNING",
                duplicate=True,
            ),
            "ALREADY_APPLIED",
        )

    def test_project_state_derivation_is_canonical(self):
        rules = self.contract["project_state_derivation"]
        self.assertEqual(rules[0]["state"], "COMPLETE")
        self.assertEqual(rules[1]["state"], "PAUSED")
        self.assertEqual(rules[2]["state"], "PARTIALLY_PAUSED")
        self.assertEqual(rules[3]["state"], "BLOCKED")
        self.assertEqual(rules[-1]["state"], "RUNNING")

    def test_receipts_and_errors_are_pair_explicit(self):
        self.assertEqual(
            set(self.contract["errors"]),
            {
                "INVALID_COMMAND",
                "INVALID_STATE",
                "PRECONDITION_FAILED",
                "UNKNOWN_PAIR",
                "SCHEDULE_CONFLICT",
                "ALREADY_APPLIED",
            },
        )
        self.assertIn("per_target_results", self.contract["receipt_fields"])
        self.assertIn("project_progress", self.contract["receipt_fields"])
        for error in self.contract["errors"].values():
            self.assertFalse(error["state_change"])
            self.assertFalse(error["dispatch"])
            self.assertFalse(error["roster_change"])


if __name__ == "__main__":
    unittest.main()
