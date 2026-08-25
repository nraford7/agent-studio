"""Structural regression tests for the evidence-gated redesign docs."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text()
REFS = ROOT / "references"

NEW_REFS = [
    "evidence-gate.md", "job-description.md", "work-sample.md",
    "roster.md", "doit-handoff.md", "voice.md",
]
ALL_REFS = NEW_REFS + [
    "hard-rules.md", "recipes.md", "synthesis-modes.md",
    "diagnose-rubric.md", "harden-checklist.md", "persona-template.md",
]


def test_all_reference_files_exist():
    for name in ALL_REFS:
        assert (REFS / name).is_file(), f"references/{name} missing"


def test_skill_points_at_every_reference():
    for name in ALL_REFS:
        assert f"references/{name}" in SKILL, f"SKILL.md never references {name}"


def test_four_doors_present():
    for door in ["Design the work", "Existing workflow",
                 "Consider a specialist", "One-off panel"]:
        assert door in SKILL, f"door missing from SKILL.md: {door}"


def test_eleven_stages_present():
    for n in range(1, 12):
        assert re.search(rf"Stage {n}\b", SKILL), f"Stage {n} missing"


def test_evidence_conclusions_verbatim():
    gate = (REFS / "evidence-gate.md").read_text()
    for c in ["Research supports trying this",
              "Supported only for a narrower analogous use",
              "Promising, but experimental",
              "No research-backed reason to create a role"]:
        assert c in gate, f"conclusion missing: {c}"


def test_roster_consent_and_waiver():
    roster = (REFS / "roster.md").read_text()
    assert "CONSENT PRECEDES ANY WRITE" in roster
    assert "Counterfactual check" in roster
    assert "agent-roster" in SKILL


def test_blind_protocol_present():
    ws = (REFS / "work-sample.md").read_text()
    assert "sample-A.md" in ws and "sample-B.md" in ws
    assert "verdict.md" in ws


def test_no_retired_architecture():
    assert "six stages" not in SKILL
    assert "Mode: Diagnose" not in SKILL and "Mode: Harden" not in SKILL


def test_voice_layer_maps_canonical_to_warm():
    voice = (REFS / "voice.md").read_text()
    gate = (REFS / "evidence-gate.md").read_text()
    # canonical verdicts still live in the gate (internal keys preserved)
    for c in ["Research supports trying this",
              "No research-backed reason to create a role"]:
        assert c in gate, f"canonical verdict lost from gate: {c}"
    # and the voice layer carries the warm presentations
    for warm in ["Green light", "No specialist needed here",
                 "On trial", "Made it worse"]:
        assert warm in voice, f"warm phrasing missing from voice.md: {warm}"
    # SKILL routes user-facing speech through the voice layer
    assert "references/voice.md" in SKILL


def test_no_banned_word():
    for path in [ROOT / "SKILL.md", ROOT / "README.md", *REFS.glob("*.md")]:
        text = path.read_text()
        assert not re.search(r"\bship(ped|ping|s)?\b", text, re.I), \
            f"banned word in {path.name}"
