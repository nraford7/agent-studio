"""Structural regression tests for the evidence-gated redesign docs."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text()
REFS = ROOT / "references"
# The lifecycle detail moved out of SKILL.md (2026-10-17); SKILL.md loads it.
LIFECYCLE = (REFS / "full-lifecycle.md").read_text()
SKILL_ALL = SKILL + LIFECYCLE

NEW_REFS = [
    "evidence-gate.md", "job-description.md", "work-sample.md",
    "roster.md", "doit-handoff.md", "voice.md",
]
TEAM_REFS = ["team-charter.md", "team-package.md"]
ALL_REFS = NEW_REFS + [
    "hard-rules.md", "recipes.md", "synthesis-modes.md",
    "diagnose-rubric.md", "harden-checklist.md", "persona-template.md",
    "field-evidence.md", "full-lifecycle.md",
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
        assert re.search(rf"Stage {n}\b", SKILL_ALL), f"Stage {n} missing"


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
        assert token in SKILL_ALL, f"SKILL.md/full-lifecycle.md missing: {token}"


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


def test_core_skill_stays_short():
    assert len(SKILL.splitlines()) <= 150, "SKILL.md core grew past 150 lines"


def test_description_states_triggers_only():
    desc = SKILL.split("description:", 1)[1].split("\n", 1)[0]
    assert desc.strip().startswith("Use when")
    assert len(desc) <= 1024


def test_source_check_rule_and_prompt():
    hr = (REFS / "hard-rules.md").read_text()
    assert "## Check every sourced output against its sources" in hr
    assert "## SOURCE CHECK PROMPT" in hr
    assert "SOURCE CHECK" in SKILL
    gate = (REFS / "evidence-gate.md").read_text()
    assert "## Output bound to sources" in gate


def test_second_family_critic_command():
    hr = (REFS / "hard-rules.md").read_text()
    assert "CODEX SEAT COMMAND" in hr
    assert "< /dev/null" in hr, "codex must run with stdin closed"
    assert "--model" in hr and "Do not pass `--model`" in hr


def test_door4_runs_a_baseline_and_offers_trials():
    door4 = SKILL.split("## One-off panel (door 4)", 1)[1].split("## Reference map", 1)[0]
    assert "baseline.md" in door4
    assert "**Trial:**" in door4
    assert "coverage_report.py" in door4


def test_field_evidence_seeded_and_read_by_gate():
    fe = (REFS / "field-evidence.md").read_text()
    assert fe.count("\n### 20") >= 2, "field-evidence.md needs its seed rows"
    gate = (REFS / "evidence-gate.md").read_text()
    assert "## Field override" in gate and "field-evidence.md" in gate


def test_claim_coverage_check_documented():
    sm = (REFS / "synthesis-modes.md").read_text()
    assert "## Claim coverage check" in sm
    assert "coverage_report.py" in sm
    assert '"status": "kept|dropped|contradicted"' in sm


def test_coverage_review_recipe_row():
    rec = (REFS / "recipes.md").read_text()
    assert "| Coverage review" in rec


# --- Citation resolution -----------------------------------------------------
# A `file.md #anchor` citation asserts that the anchor exists in the cited file.
# Renaming a heading or moving a rule leaves the citation behind, and no
# existence test notices: every file still exists and every token still appears.
CITATION_RE = re.compile(r'([A-Za-z0-9._-]+\.md)`?\s*#\s*"?([^"\n;)\]]+)"?', re.M)


def _citation_targets():
    files = [ROOT / "SKILL.md", *REFS.glob("*.md"), *METHODOLOGY.glob("*.md"),
             *(METHODOLOGY / "overlays").glob("*.md")]
    return {p.name: p.read_text() for p in files}


def test_cross_file_citations_resolve():
    """Every cited anchor must appear in the file it cites."""
    targets = _citation_targets()
    unresolved = []
    for name, text in sorted(targets.items()):
        for m in CITATION_RE.finditer(text):
            cited, anchor = m.group(1), m.group(2)
            if cited not in targets or cited == name:
                continue
            anchor = anchor.strip().strip('`"\'. ,').lower()
            flat = " ".join(targets[cited].lower().split())
            if anchor and anchor not in flat:
                unresolved.append(f"{name} -> {cited} #{anchor}")
    assert not unresolved, "citations that no longer resolve:\n" + "\n".join(unresolved)
