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
TEAM_REFS = ["team-charter.md", "team-package.md"]
ALL_REFS = NEW_REFS + [
    "hard-rules.md", "recipes.md", "synthesis-modes.md",
    "diagnose-rubric.md", "harden-checklist.md", "persona-template.md",
] + TEAM_REFS
METHODOLOGY = ROOT / "methodologies"


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
    paths = [
        ROOT / "SKILL.md", ROOT / "README.md", ROOT / "THIRD_PARTY_NOTICES.md",
        *REFS.glob("*.md"),
        *METHODOLOGY.glob("*.md"),
        *(METHODOLOGY / "overlays").glob("*.md"),
        *(ROOT / "templates").glob("*.md"),
    ]
    for path in paths:
        text = path.read_text()
        assert not re.search(r"\bship(ped|ping|s)?\b", text, re.I), \
            f"banned word in {path.name}"


def test_methodology_kernel_and_overlays_exist():
    assert (METHODOLOGY / "kernel.md").is_file(), "methodologies/kernel.md missing"
    kernel = (METHODOLOGY / "kernel.md").read_text()
    assert "Kernel version: 1.0.0" in kernel
    for ov in ["scenario-planning", "terrain-mapping", "root-cause"]:
        p = METHODOLOGY / "overlays" / f"{ov}.md"
        assert p.is_file(), f"overlay missing: {ov}"
        assert f"Overlay id: {ov}" in p.read_text()


def test_overlays_are_staff_neutral():
    for ov in ["scenario-planning", "terrain-mapping", "root-cause"]:
        text = (METHODOLOGY / "overlays" / f"{ov}.md").read_text()
        flat = " ".join(text.split())  # tolerate line wrapping
        assert "does not guarantee that a specialist" in flat, \
            f"overlay {ov} missing staff-neutral statement"
        assert "## Cast" not in text, f"overlay {ov} pre-stages a cast"


def test_skill_has_durability_and_team_machinery():
    for token in ["Durability gate", "methodology-selection.md", "Team Charter",
                  "Durable teams", "methodologies/kernel.md",
                  "scripts/team_validate.py", "references/team-charter.md",
                  "references/team-package.md", "templates/team.json.md",
                  "templates/team-readme.md"]:
        assert token in SKILL, f"SKILL.md missing: {token}"


def test_persona_three_layer_and_mode_switch():
    pt = (REFS / "persona-template.md").read_text()
    assert "Three-layer persona contract" in pt
    assert "Domain retrieval kit" in pt
    assert "Vocabulary is not proof" in pt
    assert "caricature probe" in pt
    assert "Judgment mode" in pt and "Creative mode" in pt


def test_team_templates_and_charter_exist():
    assert (REFS / "team-charter.md").is_file()
    assert (REFS / "team-package.md").is_file()
    tj_path = ROOT / "templates" / "team.json.md"
    assert tj_path.is_file() and (ROOT / "templates" / "team-readme.md").is_file()
    tj = tj_path.read_text()
    for state in ["calibrating", "active", "dormant", "retired"]:
        assert state in tj, f"lifecycle state missing from team.json template: {state}"


def test_charter_separates_approval():
    charter = (REFS / "team-charter.md").read_text()
    assert "Charter approval is never candidate approval" in charter


def test_third_party_notices_attribution():
    tp = ROOT / "THIRD_PARTY_NOTICES.md"
    assert tp.is_file(), "THIRD_PARTY_NOTICES.md missing"
    text = tp.read_text()
    assert "Agent Designer" in text
    assert "MIT" in text
    assert "Braydon McCormick" in text
