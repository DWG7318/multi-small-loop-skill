from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_contract() -> dict:
    return json.loads(
        (ROOT / "multi-small-loop-skill" / "contracts" / "mslk-control-kernel.json").read_text(
            encoding="utf-8"
        )
    )


def test_version_consistency() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert version == "1.9.0"
    assert f"Current version: **{version}**" in (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"Current specification version: `{version}`." in (
        ROOT / "multi-small-loop-skill" / "SKILL.md"
    ).read_text(encoding="utf-8")


def test_contract_roles_routes_and_authority() -> None:
    contract = load_contract()
    assert contract["role_types"] == ["SUPERVISOR", "CHECKER", "WORKER", "VERIFICATION"]
    assert "REDO" not in contract["cell_routes"]
    assert contract["product_write_authority"] == ["WORKER"]
    assert contract["cell_acceptance_authority"] == ["CHECKER"]
    assert contract["go_verdict_authority"] == ["VERIFICATION"]
    assert contract["level_barrier_authority"] == ["SUPERVISOR"]


def test_calabash_gate() -> None:
    gate = load_contract()["calabash_gate"]
    assert gate["required"] is True
    assert gate["minimum_layers"] == ["GRANDPA", "PRODUCT_ARCHITECTURE", "ONTOLOGY"]
    assert gate["supervisor_must_establish_when_missing"] is True
    assert gate["go_trace_required"] is True


def test_multi_chain_is_restricted_not_free_graph() -> None:
    model = load_contract()["multi_chain"]
    assert model["go_id_pattern"] == "GO-<LEVEL>-<CHAIN>"
    assert model["fixed_chain_roster"] is True
    assert model["full_level_barrier"] is True
    assert model["partial_unlock"] is False
    assert model["conditional_routing"] is False
    assert model["cycles"] is False
    assert model["grapher"] is False
    assert model["method_boundary_for_dynamic_graph"] == "GLK"


def test_verification_direct_handoff_and_freshness() -> None:
    policy = load_contract()["verification_policy"]
    assert policy["binding_frozen_before_level"] is True
    assert policy["fresh_attempt_created_before_first_cell"] is True
    assert policy["direct_checker_handoff"] is True
    assert policy["supervisor_relay"] is False
    assert policy["reuse"] is False


def test_owner_free_autonomy() -> None:
    autonomy = load_contract()["autonomy"]
    assert autonomy["project_autonomy_envelope_required"] is True
    assert autonomy["routine_owner_authorization_required"] is False
    assert autonomy["cell_owner_approval_required"] is False
    assert autonomy["go_owner_approval_required"] is False
    assert autonomy["level_owner_approval_required"] is False


def test_go_boundaries_and_level_barrier() -> None:
    rule = load_contract()["cross_go_rule"]
    assert rule["cell_to_cell_dependency_allowed"] is False
    assert rule["same_level_dependency_allowed"] is False
    assert rule["required_predecessor_state"] == "GO_VERIFIED"
    assert rule["required_predecessor_level_state"] == "LEVEL_VERIFIED"


def test_skill_and_reference_line_budget() -> None:
    governed = [
        ROOT / "multi-small-loop-skill" / "SKILL.md",
        *sorted((ROOT / "multi-small-loop-skill" / "references").glob("*.md")),
        ROOT / "README.md",
        ROOT / "CHANGELOG.md",
    ]
    for path in governed:
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 1000, path


def test_question_count() -> None:
    bank = json.loads(
        (ROOT / "multi-small-loop-skill" / "evals" / "mslk-readiness-questions.json").read_text(
            encoding="utf-8"
        )
    )
    key = json.loads(
        (ROOT / "multi-small-loop-skill" / "evals" / "mslk-readiness-answer-key.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(bank["questions"]) == 25
    assert len(key["answers"]) == 25
    assert {q["id"] for q in bank["questions"]} == set(key["answers"])
