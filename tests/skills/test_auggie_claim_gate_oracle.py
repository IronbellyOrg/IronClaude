"""Test-only admission oracle over explicit verified facts, not a model evaluator."""

import copy
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
REF = REPO / "src/superclaude/skills/sc-auggie-review-protocol/refs/claim-gate.md"
RUBRIC = REPO / "src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md"
FIXTURES = Path(__file__).parent / "fixtures/auggie_claim_gate"
CORPUS = FIXTURES / "corpus"
BASELINE = "713d8e423bd9a2469ea1418fafd6edccbb88caaa"
HELD_BACK_SHA256 = "2751e86cf5b3b5ddb323981aa7607bd6e0324d2a6736abaa609bd28acedfe50d"

# Full conditions are independent literals: changing a condition in the ref must fail.
ADMISSION_TABLE = [
    ("A1", "A verified guard on every verified entrypoint blocks the trigger, or the only path to `observed_at` is a seam whose documented caller precondition the claim violates", "`rejected`"),
    ("A2", "The triggering input is shown refused or not produced by the verified producer or schema", "`rejected`"),
    ("A3", "`intent_finding = deliberate_policy` verified, the claimed harm is the trade-off the policy states, and no higher-precedence requirement is shown violated through a supported input", "`intentional_limitation`"),
    ("A4", "`intent_finding = documented_prerequisite` verified, and no evidence shows the prerequisite unmet in an actual supported rollout", "`documented_prerequisite`"),
    ("A5", "The mechanism is fixed at the attribution reference and the target is current state (`target.mode` is `diff` or `snapshot`)", "`rejected` with reason `not_present_in_target`"),
    ("A6", "Any of: `evidence_kind = speculative`; class-required evidence missing or not verified (REQ-006, REQ-007); every consequence excluded; `harm` equal to the cited `evidence` text; `violated_requirement` empty; `qualification` present without a verified `scope_citation`; `confidence: low` without `hedge_resolved`; category `security` or `data-integrity` without a `severity_basis` naming the rubric definition the harm meets", "`unproven`"),
    ("A7", "Everything else holds and the refutation record is complete with no blocking entry", "`defect`"),
]
CLASS_TABLE = [
    ("`behavioral`", "security, data-integrity, correctness, concurrency, resource-leak, error-handling, api-contract, performance, logging", "`reachability.entrypoint` (plus `reachability.producer` for input-shape claims) and the guards checked"),
    ("`structural`", "architecture, layering, coupling, anti-pattern, dead-code, tests, docs, naming, style", "The violating site plus a convention source, or a mechanical fact (line count, or a zero-hit Grep with pattern and roots)"),
]
BEHAVIORAL = frozenset(CLASS_TABLE[0][1].split(", "))
STRUCTURAL = frozenset(CLASS_TABLE[1][1].split(", "))
CLASS_RULES = [
    "A structural claim that asserts a runtime consequence must meet the behavioral requirements for that consequence, or the consequence is excluded (see Claim scope).",
    "Mocked-only dispatch does not count as an entrypoint.",
    'For evidence kind `protocol_literal` the "entrypoint" is the `path:line` of the instruction that prescribes the step, inside a protocol path that is actually invoked. The "producer" is the `path:line` of the consumer\'s precondition or contract that the step must satisfy. This makes literal contract defects admissible without a model run (see Narrow contract defects).',
]
TIERS = ("nit", "low", "medium", "high", "critical")
BASIS_COUNTS = {"critical": 4, "high": 6, "medium": 5, "low": 3, "nit": 3}
VALID_BASES = {f"{tier}:{n}" for tier, count in BASIS_COUNTS.items() for n in range(1, count + 1)}


def required_evidence(facts, runtime):
    """REQ-006/007: structural site, behavioral path, and literal anchors."""
    structural = facts["category"] in STRUCTURAL
    if facts["category"] not in BEHAVIORAL | STRUCTURAL:
        return False
    if structural and not (facts["site_verified"] and
                           (facts["convention_verified"] or facts["mechanical_verified"])):
        return False
    if (not structural or runtime or facts["evidence_kind"] == "protocol_literal") and not (
        facts["entrypoint_verified"] and not facts["mocked_only"] and facts["guards_verified"]
        and (not facts["input_shape"] or facts["producer_verified"])
    ):
        return False
    return facts["evidence_kind"] != "protocol_literal" or facts["producer_verified"]


def supported_consequences(facts):
    return [c for c in facts["consequences"]
            if c["supported"] and required_evidence(facts, c["runtime"])]


def admit(record):
    """Return disposition, row reasons, and exclusions using fixture facts only."""
    f = record["facts"]
    supported = supported_consequences(f)
    incomplete = (
        f["evidence_kind"] == "speculative" or not supported
        or f["harm_equals_evidence"] or not f["requirement_verified"]
        or (f["qualification"] and not f["scope_verified"])
        or (f["confidence_low"] and not f["hedge_resolved"])
        or (f["category"] in {"security", "data-integrity"} and not f["severity_basis_verified"])
        or not f["refutation_complete"] or f["blocking_entry"]
    )
    missing_required_input = any(
        f.get("input_fields", {}).get(field) is None
        for field in f.get("required_input_fields", [])
    )
    matches = (
        (f["guard_blocks"] and f["guards_verified"] and f["entrypoint_verified"]
         and not f["mocked_only"])
        or (f["seam_violates_precondition"] and f["entrypoint_verified"] and f["producer_verified"]),
        f["producer_verified"] and (f["producer_refuses"] or missing_required_input),
        f["policy_verified"] and f["policy_tradeoff"] and not f["policy_challenge_verified"],
        f["prerequisite_verified"] and not f["rollout_violation_verified"],
        f["mechanism_fixed"] and f["target_mode"] in {"diff", "snapshot"},
        incomplete,
        True,
    )
    for (row, _, disposition_text), matches_row in zip(ADMISSION_TABLE, matches, strict=True):
        if not matches_row:
            continue
        disposition = disposition_text.split("`")[1]
        reason = row + (" not_present_in_target" if row == "A5" else "")
        excluded = [
            {"consequence": c["text"], "reason": row if disposition != "defect" else "A6"}
            for c in f["consequences"] if disposition != "defect" or c not in supported
        ]
        return disposition, [reason], excluded
    raise AssertionError("A7 is the fallback")


def grade(record):
    """Rubric steps 1, 2, 4; only admitted harm sets floors and qualification."""
    if admit(record)[0] != "defect":
        return {"severity": None, "reasons": [], "trace": [], "harm": [], "label": None}
    f = record["facts"]
    consequences = supported_consequences(f)
    harm_tier = max(TIERS.index(c["tier"]) for c in consequences)
    severity = TIERS.index(f["severity_hint"])
    trace = [("step1", TIERS[severity])]
    reasons = []
    category = f["category"]
    floor, ceiling = {
        "security": ("critical" if f["exploitable"] else "high", "critical"),
        "data-integrity": ("high", "critical" if f["persists_corruption"] else "high"),
        "correctness": ("medium", "critical" if f["default_path"] else "high"),
        "concurrency": ("medium", "high" if f["realistic_trigger"] else "medium"),
        "resource-leak": ("medium", "high"),
        "api-contract": ("medium", "high" if f["in_repo_consumers"] else "medium"),
        "performance": ("low", "high" if f["measured_impact"] else "medium"),
        "architecture": ("medium", "high" if f["new_violation"] else "low"),
        "layering": ("medium", "high" if f["new_violation"] else "low"),
        "coupling": ("medium", "high" if f["new_violation"] else "low"),
        "anti-pattern": ("low", "medium" if f["smell_worsened"] else "low"),
        "dead-code": ("low", "low"),
        "tests": ("medium" if f["critical_path"] else "low",
                  "high" if f["breaking_change"] else "medium" if f["critical_path"] else "low"),
        "docs": ("low", "medium" if f["public_api_change"] else "low"),
        "logging": ("low", "high" if f["pii"] else "medium"),
        "naming": ("nit", "low"), "style": ("nit", "low"),
    }.get(category, ("nit", "critical"))
    if harm_tier >= TIERS.index(floor):
        severity = max(severity, TIERS.index(floor))
    else:
        reasons.append("harm_below_floor")
    # A verified Critical criterion is the explicit reason to exceed a category ceiling.
    critical_harm = any(c["basis"].startswith("critical:") for c in consequences)
    if critical_harm:
        ceiling = "critical"
    # Step 2 never imports a stronger criterion from an excluded consequence.
    severity = min(severity, TIERS.index(ceiling), harm_tier)
    if f["qualification"] and category not in {"security", "data-integrity"} and not critical_harm:
        severity = min(severity, TIERS.index("medium"))
        reasons.append("qualification_cap")
    trace.append(("step2", TIERS[severity]))
    # Step 3 is deliberately absent: resolved hedges are not graded down.
    pre_existing = f["introduced_in"] == "base"
    affected = category in {"correctness", "security"} and f["affected_callsite"]
    if f["target_mode"] in {"pr", "diff"} and not f["in_diff"] and pre_existing and not affected:
        severity = max(0, severity - 1)
        reasons.append("pre_existing_tier_drop")
    trace.append(("step4", TIERS[severity]))
    return {"severity": TIERS[severity], "reasons": reasons, "trace": trace,
            "harm": [c["text"] for c in consequences],
            "label": "pre-existing" if pre_existing else None}


def load_items(filename):
    return json.loads((CORPUS / filename).read_text())


DEVELOPMENT = load_items("development.json")
FROZEN_TOKENS = json.loads((FIXTURES / "frozen-tokens.json").read_text())


def table_rows(text, heading):
    table = text.split(heading + "\n", 1)[1].split("\n\n", 1)[0]
    return [tuple(cell.strip() for cell in line.strip("|").split("|"))
            for line in table.splitlines()[1:]]


def assert_admission_table(rows):
    assert rows == ADMISSION_TABLE


def test_at16_full_table_and_class_rules_equal_canonical_ref():
    text = REF.read_text()
    assert_admission_table(table_rows(text, "| Row | Condition | Disposition |"))
    assert table_rows(text, "| Class | Categories | Required verified evidence |") == CLASS_TABLE
    assert all(rule in text for rule in CLASS_RULES)
    assert [row[0] for row in ADMISSION_TABLE] == [f"A{n}" for n in range(1, 8)]
    assert ADMISSION_TABLE[-1][2] == "`defect`"


def test_at16_table_disposition_mutation_fails(tmp_path):
    scratch = tmp_path / "claim-gate.md"
    mutated, count = re.subn(r"(^\| A1 \|.*\| )`rejected`( \|$)",
                             r"\1`defect`\2", REF.read_text(), flags=re.MULTILINE)
    assert count == 1
    scratch.write_text(mutated)
    with pytest.raises(AssertionError):
        assert_admission_table(table_rows(scratch.read_text(), "| Row | Condition | Disposition |"))


def test_at16_table_condition_and_order_mutations_fail():
    for rows in [list(reversed(ADMISSION_TABLE)),
                 [("A1", "A guard sometimes blocks", "`rejected`")] + ADMISSION_TABLE[1:]]:
        with pytest.raises(AssertionError):
            assert_admission_table(rows)


def assert_item(item):
    expected = item["expected"]
    disposition, reasons, excluded = admit(item)
    assert disposition == expected["disposition"]
    assert reasons[0].split()[0] == expected["row"]
    assert [c["consequence"] for c in excluded] == expected["excluded"]
    assert all(re.match(r"^(A[1-6]|other:)", c["reason"]) for c in excluded)
    result = grade(item)
    assert result["severity"] == expected["severity"]
    if disposition == "defect":
        assert [step for step, _ in result["trace"]] == ["step1", "step2", "step4"]
        assert all(c["basis"] in VALID_BASES for c in supported_consequences(item["facts"]))
    if "label" in expected:
        assert result["label"] == expected["label"]
        assert "pre_existing_tier_drop" in result["reasons"]
    if "retention_list" in item:
        assert disposition == "defect"
    if item.get("bundled") and excluded:
        assert disposition == "defect"
        assert set(result["harm"]).isdisjoint(c["consequence"] for c in excluded)
        assert result["harm"]


@pytest.mark.parametrize("item", DEVELOPMENT, ids=lambda item: item["name"])
def test_at17_at18_at19_development_outcomes(item):
    assert_item(item)


def differing_facts(left, right, prefix=""):
    if isinstance(left, dict) and isinstance(right, dict):
        assert left.keys() == right.keys()
        return [difference for key in left
                for difference in differing_facts(left[key], right[key], prefix + key + ".")]
    if isinstance(left, list) and isinstance(right, list):
        assert len(left) == len(right)
        return [difference for n, (a, b) in enumerate(zip(left, right, strict=True))
                for difference in differing_facts(a, b, prefix + str(n) + ".")]
    return [prefix.rstrip(".")] if left != right else []


def test_at17_corpus_coverage_and_single_factor_pairs():
    # Held-back bytes are data here: never call admit/grade or inspect their results.
    held_back = load_items("held-back.json")
    items = DEVELOPMENT + held_back
    assert all(item["held_back"] for item in held_back)
    assert not any(item["held_back"] for item in DEVELOPMENT)
    families = {item["family"] for item in items if "family" in item}
    assert families == {f"F{n}" for n in range(1, 17)}
    held_families = {item["family"] for item in held_back if "family" in item}
    assert len(held_families) >= 4
    assert held_families.isdisjoint({"F10", "F15", "F16"})
    for family in families:
        members = [item for item in items if item.get("family") == family]
        positives = [item for item in members if item["role"] == "positive"]
        negatives = [item for item in members if item["role"] == "negative"]
        assert len(positives) == (2 if family == "F10" else 1)
        assert len(negatives) == (0 if family == "F16" else 2 if family == "F10" else 1)
        for negative in negatives:
            positive_name = negative.get("contrast_with", positives[0]["name"])
            positive = next(item for item in positives if item["name"] == positive_name)
            assert differing_facts(positive["facts"], negative["facts"]) == [negative["factor"]]
    required = {
        "base": {"availability", "visibility", "automatic_retry", "diagnostic_contract", "persisted_state", "security_sink"},
        "classic": {"null_deref", "sql_injection", "resource_leak", "off_by_one", "broken_invariant", "swallowed_exception", "race", "missing_authz"},
        "publish": {"batch_stall", "readable_duplicate", "qualified_static", "omitted_input"},
    }
    for group, kinds in required.items():
        retained = [item for item in items if item.get("retention_list") == group]
        assert {item["retention"] for item in retained} == kinds
        assert any(item.get("retention_list") == group for item in held_back)
    security = [item for item in items
                if item.get("retention_list") == "base" and item["retention"] == "security_sink"]
    assert any(item["facts"]["category"] == "security" and item["facts"]["default_path"]
               and item["facts"]["exploitable"]
               and any(c["supported"] and c["tier"] == "critical"
                       for c in item["facts"]["consequences"]) for item in security)
    assert all(item["unknown_frequency"] for item in items if item.get("retention_list") == "publish")


def test_at17_held_back_digest_is_frozen():
    assert hashlib.sha256((CORPUS / "held-back.json").read_bytes()).hexdigest() == HELD_BACK_SHA256


@pytest.mark.parametrize("refutation,verification,row", [
    ("guard_blocks", "guards_verified", "A1"),
    ("guard_blocks", "entrypoint_verified", "A1"),
    ("seam_violates_precondition", "producer_verified", "A1"),
    ("producer_refuses", "producer_verified", "A2"),
])
def test_at16_refutations_require_verified_evidence(refutation, verification, row):
    item = copy.deepcopy(next(i for i in DEVELOPMENT if i["name"] == "F3-positive"))
    item["facts"][refutation] = True
    assert admit(item)[:2] == ("rejected", [row])
    item["facts"][verification] = False
    assert admit(item)[:2] == ("unproven", ["A6"])


def test_at17_provenance_family_has_known_and_unknown_input_facts():
    positive = next(i for i in DEVELOPMENT if i["name"] == "F13-positive")
    negative = next(i for i in DEVELOPMENT if i["name"] == "F13-negative")
    assert positive["facts"]["input_fields"] == {"author": "known-valid-author"}
    assert negative["facts"]["input_fields"] == {"author": None}
    for item in (positive, negative):
        facts = item["facts"]
        assert facts["required_input_fields"] == ["author"]
        assert facts["producer_verified"] and facts["entrypoint_verified"]
        assert facts["operation_refused"]
        assert not facts["policy_verified"]
        assert not facts["producer_refuses"]  # The schema decides from the actual field.
    assert differing_facts(positive["facts"], negative["facts"]) == ["input_fields.author"]
    assert admit(positive)[:2] == ("defect", ["A7"])
    assert admit(negative)[:2] == ("rejected", ["A2"])
    unverified = copy.deepcopy(negative)
    unverified["facts"]["producer_verified"] = False
    assert admit(unverified)[:2] == ("unproven", ["A6"])


def test_at17_structural_family_has_cycles_and_missing_abstraction():
    current = next(i for i in DEVELOPMENT if i["name"] == "F10-positive")
    existing = next(i for i in DEVELOPMENT if i["name"] == "F10-negative")
    for item in (current, existing):
        facts = item["facts"]
        assert facts["import_cycle"] and not facts["missing_abstraction"]
        assert facts["convention_verified"] and facts["site_verified"]
        assert not facts["in_diff"]
        assert "import cycle" in facts["consequences"][0]["text"]
        assert admit(item)[0] == "defect"
    assert current["facts"]["introduced_in"] == "head"
    assert existing["facts"]["introduced_in"] == "base"
    assert grade(existing)["label"] == "pre-existing"
    assert TIERS.index(grade(existing)["severity"]) == TIERS.index(grade(current)["severity"]) - 1
    positive = next(i for i in DEVELOPMENT if i["name"] == "F10-positive-abstraction")
    negative = next(i for i in DEVELOPMENT if i["name"] == "F10-negative-no-convention")
    for item in (positive, negative):
        facts = item["facts"]
        assert facts["missing_abstraction"] and not facts["import_cycle"]
        assert facts["site_verified"] and not facts["mechanical_verified"]
        assert "lack the abstraction" in facts["consequences"][0]["text"]
    assert positive["facts"]["convention_verified"]
    assert not negative["facts"]["convention_verified"]
    assert differing_facts(positive["facts"], negative["facts"]) == ["convention_verified"]
    assert admit(positive)[:2] == ("defect", ["A7"])
    assert admit(negative)[:2] == ("unproven", ["A6"])


def test_at16_first_matching_row_wins():
    item = copy.deepcopy(DEVELOPMENT[0])
    item["facts"].update(guard_blocks=True, producer_refuses=True, policy_verified=True,
                         policy_tradeoff=True, prerequisite_verified=True,
                         mechanism_fixed=True, evidence_kind="speculative")
    assert admit(item)[:2] == ("rejected", ["A1"])
    item["facts"]["guard_blocks"] = False
    assert admit(item)[:2] == ("rejected", ["A2"])
    item["facts"]["producer_refuses"] = False
    assert admit(item)[:2] == ("intentional_limitation", ["A3"])
    item["facts"]["policy_verified"] = False
    assert admit(item)[:2] == ("documented_prerequisite", ["A4"])
    item["facts"]["prerequisite_verified"] = False
    assert admit(item)[:2] == ("rejected", ["A5 not_present_in_target"])
    item["facts"]["mechanism_fixed"] = False
    assert admit(item)[:2] == ("unproven", ["A6"])


def test_at19_harm_floors_qualification_exceptions_and_locality():
    item = copy.deepcopy(next(i for i in DEVELOPMENT if i["name"] == "hedge-resolved"))
    result = grade(item)
    assert result["severity"] == "high"  # No step-3 confidence penalty.
    f = item["facts"]
    f.update(severity_hint="low", category="correctness", consequences=[{
        "text": "A minor maintenance cost", "supported": True, "runtime": True,
        "tier": "low", "basis": "low:1"}])
    assert grade(item)["severity"] == "low"
    assert "harm_below_floor" in grade(item)["reasons"]
    f.update(severity_hint="high", qualification=True, consequences=[{
        "text": "Supported optional processing fails", "supported": True, "runtime": True,
        "tier": "high", "basis": "high:2"}])
    assert grade(item)["severity"] == "medium"
    f.update(category="security", exploitable=True, consequences=[{
        "text": "An unauthorized read is reachable", "supported": True, "runtime": True,
        "tier": "critical", "basis": "critical:1"}])
    assert grade(item)["severity"] == "critical"
    f.update(category="data-integrity", persists_corruption=True, severity_hint="critical",
             consequences=[{"text": "A valid write loses stored data", "supported": True,
                            "runtime": True, "tier": "critical", "basis": "critical:2"}])
    assert grade(item)["severity"] == "critical"
    f.update(category="logging", pii=True, consequences=[{
        "text": "A regulated audit trail is bypassed", "supported": True, "runtime": True,
        "tier": "critical", "basis": "critical:4"}])
    assert grade(item)["severity"] == "critical"  # Compliance is exempt from the cap too.
    f.update(category="correctness", qualification=False, severity_hint="high",
             introduced_in="base", in_diff=False, affected_callsite=True,
             consequences=[{"text": "An affected callsite fails", "supported": True,
                            "runtime": True, "tier": "high", "basis": "high:2"}])
    assert grade(item)["severity"] == "high"
    f["affected_callsite"] = False
    assert grade(item)["severity"] == "medium"
    f["target_mode"] = "snapshot"
    assert grade(item)["severity"] == "high"


def test_at16_oracle_is_pure_and_class_evidence_is_required(monkeypatch):
    import socket

    item = copy.deepcopy(next(i for i in DEVELOPMENT if i["name"] == "hedge-resolved"))
    before = copy.deepcopy(item)

    def forbidden(*args, **kwargs):
        raise AssertionError("The oracle must not access files, git, or network")

    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    assert admit(item)[0] == "defect"
    assert grade(item)["severity"] == "high"
    assert item == before
    for field in ("entrypoint_verified", "producer_verified", "guards_verified"):
        changed = copy.deepcopy(item)
        changed["facts"][field] = False
        assert admit(changed)[0] == "unproven"
    item["facts"].update(category="architecture", entrypoint_verified=False,
                          producer_verified=False, convention_verified=False,
                          mechanical_verified=True, input_shape=False)
    item["facts"]["consequences"][0]["runtime"] = False
    assert admit(item)[0] == "defect"
    item["facts"]["site_verified"] = False
    assert admit(item)[0] == "unproven"


def test_at16_rubric_basis_ids_match_live_bullet_counts():
    text = RUBRIC.read_text().split("## The five tiers\n", 1)[1].split("## Admission precedes grading", 1)[0]
    sections = re.split(r"^### .+$", text, flags=re.MULTILINE)[1:]
    assert len(sections) == len(BASIS_COUNTS)
    for (tier, count), section in zip(BASIS_COUNTS.items(), sections, strict=True):
        assert len(re.findall(r"^- ", section, re.MULTILINE)) == count, tier
    assert all(f"`{basis}`" in REF.read_text() for basis in VALID_BASES)


def assert_no_tokens(text, tokens, *, fixture):
    banned = list(tokens["symbols"])
    if fixture:
        banned += tokens["case_ids"]
    for token in banned:
        assert not re.search(r"\b" + re.escape(str(token)) + r"\b", text), f"Forbidden token: {token}"
    for number in tokens["pr_numbers"]:
        assert not re.search(r"(?:\b|#|\bPR)" + str(number) + r"\b", text), f"Forbidden PR number: {number}"


def added_source_lines(root, baseline=BASELINE):
    diff = subprocess.run(["git", "diff", "-U0", baseline, "--", "src/"],
                          cwd=root, check=True, capture_output=True, text=True).stdout
    added = [line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++")]
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", "src/"],
                               cwd=root, check=True, capture_output=True, text=True).stdout.splitlines()
    added.extend((root / path).read_text() for path in untracked)
    return "\n".join(added)


def baseline_available():
    return subprocess.run(["git", "cat-file", "-e", BASELINE], cwd=REPO,
                          capture_output=True).returncode == 0


def test_at20_fixture_and_added_source_anti_overfit():
    for path in FIXTURES.rglob("*"):
        if path.is_file() and path.name != "frozen-tokens.json":
            assert_no_tokens(path.read_text(), FROZEN_TOKENS, fixture=True)
    if not baseline_available():
        pytest.skip("Baseline commit absent; cannot inspect added source lines")
    assert_no_tokens(added_source_lines(REPO), FROZEN_TOKENS, fixture=False)
    # Case ids are fixture-only: the existing protocol heading must remain legal.
    assert_no_tokens("#### C1. <Short title>", FROZEN_TOKENS, fixture=False)


def test_at20_frozen_source_sha():
    source = REPO / FROZEN_TOKENS["source_file"]
    if not source.exists():
        pytest.skip("Diagnostic source file absent; cannot check frozen source SHA")
    if not baseline_available():
        pytest.skip("Baseline commit absent; cannot check frozen source SHA")
    assert hashlib.sha256(source.read_bytes()).hexdigest() == FROZEN_TOKENS["source_sha256"]


def test_at20_added_line_token_mutation_fails(tmp_path):
    tokens_path = tmp_path / "tokens.json"
    tokens_path.write_text(json.dumps({"symbols": ["syntheticForbiddenIdentifier"], "case_ids": [], "pr_numbers": []}))
    tokens = json.loads(tokens_path.read_text())
    for args in [["init", "-q"], ["config", "user.email", "test@example.invalid"],
                 ["config", "user.name", "Fixture"], ["commit", "--allow-empty", "-qm", "baseline"]]:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)
    source = tmp_path / "src/example.py"
    source.parent.mkdir()
    source.write_text("syntheticForbiddenIdentifier = True\n")
    # Exercise both untracked source and an actual single-plus diff line.
    for staged in (False, True):
        if staged:
            subprocess.run(["git", "add", "src/example.py"], cwd=tmp_path, check=True)
        with pytest.raises(AssertionError, match="syntheticForbiddenIdentifier"):
            assert_no_tokens(added_source_lines(tmp_path, "HEAD"), tokens, fixture=False)


@pytest.mark.parametrize("text", ["266", "#267", "PR269", "path.py:270"])
def test_at20_pr_number_forms_fail(text):
    with pytest.raises(AssertionError, match="Forbidden PR number"):
        assert_no_tokens(text, FROZEN_TOKENS, fixture=False)


if os.environ.get("AUGGIE_CLAIM_GATE_ACCEPTANCE") == "1":
    @pytest.mark.parametrize("item", load_items("held-back.json"), ids=lambda item: "held-back-" + item["name"])
    def test_at17_at18_held_back_acceptance(item):
        assert_item(item)
