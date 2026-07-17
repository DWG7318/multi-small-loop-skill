import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_mslk_readiness_eval.py"


def load_module():
    spec = importlib.util.spec_from_file_location("mslk_readiness_eval", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_answers(key):
    return {item["question_id"]: item["answer"] for item in key["answers"]}


def metadata(role, conversation_id, pair_id=None, attempt=1, **overrides):
    controller = role in {"supervisor", "checker"}
    base = {
        "candidate_role": role,
        "pair_id": pair_id,
        "conversation_id": conversation_id,
        "model": "gpt-5.6-sol" if controller else "gpt-5.5",
        "reasoning": "xhigh" if controller else "high",
        "attempt": attempt,
        "answer_key_not_opened": True,
    }
    base.update(overrides)
    return base


class MslkReadinessEvalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.questions, cls.key = cls.module.load_assets(ROOT)
        cls.answers = canonical_answers(cls.key)

    def test_bank_and_key_have_24_unique_mslk_questions(self):
        question_ids = [item["id"] for item in self.questions["questions"]]
        answer_ids = [item["question_id"] for item in self.key["answers"]]
        self.assertEqual(question_ids, [f"MSLK-Q{i:02d}" for i in range(1, 25)])
        self.assertEqual(len(set(question_ids)), 24)
        self.assertEqual(set(question_ids), set(answer_ids))
        self.assertEqual(self.questions["mode"], "MSLK")
        self.assertEqual(self.key["mode"], "MSLK")

    def test_question_output_hides_answer_material(self):
        payload = self.module.question_payload(seed=7318, root=ROOT)
        serialized = json.dumps(payload).lower()
        self.assertEqual(len(payload["questions"]), 24)
        self.assertNotIn('"answer"', serialized)
        self.assertNotIn("rationale", serialized)
        self.assertNotIn("forbidden_interpretations", serialized)

    def test_every_role_can_pass_only_with_24_correct(self):
        roles = (
            metadata("supervisor", "sup-1"),
            metadata("checker", "checker-a", pair_id="pair-a"),
            metadata("worker", "worker-a", pair_id="pair-a"),
        )
        for item in roles:
            with self.subTest(role=item["candidate_role"]):
                receipt = self.module.grade(
                    self.answers, item, seed=7318, root=ROOT
                )
                self.assertEqual(receipt["result"], "MSLK_READINESS_EVAL_PASS")
                self.assertEqual(receipt["score"], "24/24")

    def test_one_wrong_answer_fails_entire_attempt(self):
        answers = dict(self.answers)
        answers["MSLK-Q22"] = ["WRONG"]
        receipt = self.module.grade(
            answers,
            metadata("checker", "checker-a", pair_id="pair-a"),
            seed=7318,
            root=ROOT,
        )
        self.assertEqual(receipt["result"], "MSLK_READINESS_EVAL_FAIL")
        self.assertEqual(receipt["score"], "23/24")
        self.assertEqual(receipt["review_question_ids"], ["MSLK-Q22"])

    def test_missing_extra_and_misordered_answers_fail(self):
        missing = dict(self.answers)
        missing.pop("MSLK-Q03")
        extra = dict(self.answers)
        extra["MSLK-Q99"] = ["A"]
        misordered = dict(self.answers)
        misordered["MSLK-Q09"] = list(reversed(misordered["MSLK-Q09"]))
        meta = metadata("worker", "worker-a", pair_id="pair-a")
        for candidate in (missing, extra, misordered):
            receipt = self.module.grade(candidate, meta, seed=7318, root=ROOT)
            self.assertEqual(receipt["result"], "MSLK_READINESS_EVAL_FAIL")

    def test_multiselect_order_is_not_significant(self):
        answers = dict(self.answers)
        answers["MSLK-Q01"] = list(reversed(answers["MSLK-Q01"]))
        receipt = self.module.grade(
            answers,
            metadata("supervisor", "sup-1"),
            seed=7318,
            root=ROOT,
        )
        self.assertEqual(receipt["result"], "MSLK_READINESS_EVAL_PASS")

    def test_role_model_and_pair_identity_are_enforced(self):
        bad_checker = metadata(
            "checker", "checker-a", pair_id=None, model="gpt-5.5", reasoning="high"
        )
        receipt = self.module.grade(
            self.answers, bad_checker, seed=7318, root=ROOT
        )
        self.assertEqual(receipt["result"], "MSLK_READINESS_EVAL_FAIL")
        self.assertEqual(receipt["failure_reason"], "invalid_role_model")
        missing_pair = metadata("worker", "worker-a", pair_id=None)
        receipt = self.module.grade(
            self.answers, missing_pair, seed=7318, root=ROOT
        )
        self.assertEqual(receipt["failure_reason"], "missing_pair_id")

    def test_retry_requires_new_seed(self):
        meta = metadata(
            "worker", "worker-a", pair_id="pair-a", attempt=2, previous_seed=7318
        )
        receipt = self.module.grade(self.answers, meta, seed=7318, root=ROOT)
        self.assertEqual(receipt["failure_reason"], "retry_seed_reused")

    def test_receipt_verification_detects_stale_pair_or_hash(self):
        meta = metadata("checker", "checker-a", pair_id="pair-a")
        receipt = self.module.grade(self.answers, meta, seed=7318, root=ROOT)
        self.assertTrue(self.module.verify_receipt(receipt, meta, root=ROOT)["valid"])
        reassigned = metadata("checker", "checker-a", pair_id="pair-b")
        self.assertFalse(
            self.module.verify_receipt(receipt, reassigned, root=ROOT)["valid"]
        )
        stale = dict(receipt)
        stale["answer_key_sha256"] = "0" * 64
        self.assertFalse(self.module.verify_receipt(stale, meta, root=ROOT)["valid"])

    def test_complete_frozen_roster_is_required(self):
        expected = [
            metadata("supervisor", "sup-1"),
            metadata("checker", "checker-a", pair_id="pair-a"),
            metadata("worker", "worker-a", pair_id="pair-a"),
            metadata("checker", "checker-b", pair_id="pair-b"),
            metadata("worker", "worker-b", pair_id="pair-b"),
        ]
        receipts = [
            self.module.grade(self.answers, item, seed=7318 + index, root=ROOT)
            for index, item in enumerate(expected)
        ]
        self.assertTrue(
            self.module.verify_roster(receipts, expected, root=ROOT)["valid"]
        )
        missing = self.module.verify_roster(receipts[:-1], expected, root=ROOT)
        self.assertFalse(missing["valid"])
        self.assertEqual(missing["reason"], "missing_roster_receipt")

    def test_duplicate_conversation_or_pair_role_fails_roster(self):
        expected = [
            metadata("supervisor", "sup-1"),
            metadata("checker", "same", pair_id="pair-a"),
            metadata("worker", "same", pair_id="pair-a"),
            metadata("checker", "checker-b", pair_id="pair-b"),
            metadata("worker", "worker-b", pair_id="pair-b"),
        ]
        receipts = [
            self.module.grade(self.answers, item, seed=7400 + index, root=ROOT)
            for index, item in enumerate(expected)
        ]
        self.assertFalse(
            self.module.verify_roster(receipts, expected, root=ROOT)["valid"]
        )

    def test_receipt_path_and_git_optional_behavior(self):
        meta = metadata("worker", "worker-a", pair_id="pair-a")
        receipt = self.module.grade(self.answers, meta, seed=7318, root=ROOT)
        with self.assertRaises(ValueError):
            self.module.write_receipt(receipt, ROOT / "receipt.json", root=ROOT)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "receipt.json"
            self.module.write_receipt(receipt, target, root=ROOT)
            self.assertEqual(
                json.loads(target.read_text(encoding="utf-8"))["score"], "24/24"
            )
            self.assertIsNone(self.module.source_commit(Path(directory)))


if __name__ == "__main__":
    unittest.main()
