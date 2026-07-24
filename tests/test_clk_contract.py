from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "chain-loop-skill"


def contract() -> dict:
    return json.loads((SKILL / "contracts" / "clk-control-kernel.json").read_text(encoding="utf-8"))


def test_version_and_identity() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert version == "2.0.0"
    assert f"Current version: **{version}**" in (ROOT / "README.md").read_text(encoding="utf-8")
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "# Chain Loop Skill (CLK)" in text
    assert "name: chain-loop-skill" in text
    assert "$chain-loop-skill" in text
    assert f"Current specification version: `{version}`." in text


def test_contract_and_legacy() -> None:
    c = contract()
    assert c["method"] == "CLK"
    assert c["product_name"] == "Chain Loop Skill"
    assert c["version"] == "2.0.0"
    assert c["legacy_identity"]["abbreviation"] == "MSLK"
    assert c["legacy_identity"]["formal_new_runs_allowed"] is False


def test_roles_calabash_and_chain_model() -> None:
    c = contract()
    assert c["role_types"] == ["SUPERVISOR", "CHECKER", "WORKER", "VERIFICATION"]
    assert c["calabash_gate"]["required"] is True
    assert c["calabash_gate"]["minimum_layers"] == ["GRANDPA", "PRODUCT_ARCHITECTURE", "ONTOLOGY"]
    model = c["multi_chain"]
    assert model["go_id_pattern"] == "GO-<LEVEL>-<CHAIN>"
    assert model["fixed_chain_roster"] is True
    assert model["full_level_barrier"] is True
    assert model["partial_unlock"] is False
    assert model["grapher"] is False


def test_authority_verification_and_autonomy() -> None:
    c = contract()
    assert c["product_write_authority"] == ["WORKER"]
    assert c["cell_acceptance_authority"] == ["CHECKER"]
    assert c["go_verdict_authority"] == ["VERIFICATION"]
    assert c["verification_policy"]["direct_checker_handoff"] is True
    assert c["verification_policy"]["supervisor_relay"] is False
    assert c["autonomy"]["routine_owner_authorization_required"] is False


def test_go_boundary_and_detection() -> None:
    c = contract()
    assert c["cross_go_rule"]["cell_to_cell_dependency_allowed"] is False
    assert c["cross_go_rule"]["same_level_dependency_allowed"] is False
    assert c["detection_tiers"] == ["CELL_ALWAYS", "CELL_TRIGGERED", "GO_BOUNDARY", "PROJECT_FINAL"]


def test_line_budgets() -> None:
    paths = [ROOT / "README.md", ROOT / "CHANGELOG.md", SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]
    for path in paths:
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 1000, path


def test_readiness_count() -> None:
    q = json.loads((SKILL / "evals" / "clk-readiness-questions.json").read_text(encoding="utf-8"))
    a = json.loads((SKILL / "evals" / "clk-readiness-answer-key.json").read_text(encoding="utf-8"))
    assert len(q["questions"]) == 25
    assert len(a["answers"]) == 25
    assert {x["id"] for x in q["questions"]} == set(a["answers"])
