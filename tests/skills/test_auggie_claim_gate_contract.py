"""Protocol-text presence/absence checks for the auggie-review claim gate.

Every check reads the canonical src/ files (AT-25) through ``load(root)``, so a test can point
the same check at a modified temporary copy and see it fail. Acceptance tests covered:
AT-01 to AT-07, AT-10 to AT-15, AT-23, AT-24 and AT-25.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SK = "src/superclaude/skills/sc-auggie-review-protocol"
FILES = {
    "skill": f"{SK}/SKILL.md",
    "gate": f"{SK}/refs/claim-gate.md",
    "prompts": f"{SK}/refs/auggie-prompts.md",
    "rubric": f"{SK}/refs/severity-rubric.md",
    "handoff": f"{SK}/refs/remediation-handoff.md",
    "agent": "src/superclaude/agents/auggie-reviewer.md",
    "command": "src/superclaude/commands/auggie-review.md",
}
BASELINE = "713d8e423bd9a2469ea1418fafd6edccbb88caaa"
CLAIM_KEYS = [
    "observed", "observed_at", "expected", "violated_requirement", "intent_sources", "intent_finding",
    "reachability", "entrypoint", "producer", "guards_checked", "caller_search", "harm", "consequences",
    "counterevidence", "evidence_kind", "qualification", "disposition_hint",
]
INTENT_FINDINGS = ["none_found", "supports_claim", "contradicts_claim", "deliberate_policy", "documented_prerequisite"]
DISPOSITIONS = ["defect", "unproven", "rejected", "intentional_limitation", "documented_prerequisite"]
EVIDENCE_KINDS = ["runtime_reproduced", "static_traced", "protocol_literal", "speculative"]
BEHAVIORAL = ["security", "data-integrity", "correctness", "concurrency", "resource-leak", "error-handling",
              "api-contract", "performance", "logging"]
STRUCTURAL = ["architecture", "layering", "coupling", "anti-pattern", "dead-code", "tests", "docs", "naming", "style"]


def load(root: Path) -> dict[str, str]:
    return {k: (root / rel).read_text(encoding="utf-8") for k, rel in FILES.items()}


def section(text: str, start: str, end: str | None = None) -> str:
    """Text from the line starting with ``start`` to the line starting with ``end`` (or the end)."""
    m = re.search(rf"^{re.escape(start)}.*$", text, flags=re.M)
    assert m, f"heading not found: {start!r}"
    rest = text[m.start():]
    if end is None:
        return rest
    e = re.search(rf"^{re.escape(end)}", rest[len(m.group(0)):], flags=re.M)
    assert e, f"end heading not found: {end!r}"
    return rest[: len(m.group(0)) + e.start()]


def gate_section(t: dict[str, str], name: str) -> str:
    text = t["gate"]
    m = re.search(rf"^(#{{2,3}}) {re.escape(name)}\s*$", text, flags=re.M)
    assert m, f"claim-gate.md section not found: {name}"
    level = len(m.group(1))
    rest = text[m.end():]
    e = re.search(rf"^#{{1,{level}}} ", rest, flags=re.M)
    return rest[: e.start()] if e else rest


def need(text: str, *needles: str, where: str = "") -> None:
    for n in needles:
        assert n in text, f"missing {n!r}" + (f" in {where}" if where else "")


def wave3(t):
    return section(t["skill"], "### Wave 3: Validate & Synthesize", "### Wave 4")


# ---------------------------------------------------------------- checks


def check_at01(t):
    p = t["prompts"]
    contract = section(p, "## Output contract", "## Claim block")
    assert contract.count('"claim":') >= 2, "the claim object must appear under findings[] and cross_cutting_observations[]"
    for key in CLAIM_KEYS:
        assert contract.count(f'"{key}":') >= 2, f"claim key {key!r} must appear under both arrays"
    need(contract, *EVIDENCE_KINDS, *DISPOSITIONS, *INTENT_FINDINGS, "consequences", "scope_citation", where="output contract")
    assert "scope_condition" not in p
    for old in ("title", "category", "severity_hint", "file", "line", "line_range_end", "in_diff",
                "evidence", "why", "recommendation", "cross_references", "confidence"):
        assert f'"{old}":' in contract, f"existing field {old!r} missing"
    block = section(p, "## Claim block", "## Quality bar")
    need(block, "lists each distinct consequence you claim as its own string", "`harm` is the single consequence",
         where="Claim block")


def check_at02(t):
    bar = section(t["prompts"], "## Quality bar", "Return only the JSON object")
    need(bar, "trace a production entrypoint or prescribing instruction", where="quality bar")
    need(bar, "Search for intent and documented prerequisites", "record what you found", "none_found",
         "Grep pattern and roots", where="quality bar")
    need(bar, "`disposition_hint: unproven` or `harm: null`, never as a lower `severity_hint`", where="quality bar")
    need(bar, "Never claim live frequency", where="quality bar")


def check_at03(t):
    a = t["agent"]
    assert "Flag every one" not in a
    need(a, "record every one as a candidate with a `claim`; a mismatch is not a defect until "
            "violated requirement and harm are shown")
    out = section(a, "## Output Format", "## Tools")
    need(out, "must carry the `claim` block", "`cross_cutting_observations`", where="Output Format")
    r5 = next(line for line in a.splitlines() if line.startswith("5. **Head mismatch**"))
    need(r5, "cite only the new side of `diff_path`", "`in_diff: false`", "orchestrator's admission decides")
    assert "Put out-of-diff concerns in `cross_cutting_observations`" not in a


def check_at04(t):
    g = t["gate"]
    rows = re.findall(r"^\| (A[1-7]) \| .* \| (.*) \|$", g, flags=re.M)
    assert [r for r, _ in rows] == [f"A{i}" for i in range(1, 8)], "rows A1-A7 must appear in order"
    expected = ["`rejected`", "`rejected`", "`intentional_limitation`", "`documented_prerequisite`",
                "`rejected` with reason `not_present_in_target`", "`unproven`", "`defect`"]
    assert [d for _, d in rows] == expected
    for heading in ("## Claim classes", "## Claim scope", "## Narrow contract defects", "## Admission table"):
        assert re.search(rf"^{re.escape(heading)}$", g, flags=re.M), heading
    classes = gate_section(t, "Claim classes")
    behavioral = re.search(r"^\| `behavioral` \| (.*?) \|", classes, flags=re.M)
    structural = re.search(r"^\| `structural` \| (.*?) \|", classes, flags=re.M)
    assert behavioral and structural, "class table rows missing"
    for cat in BEHAVIORAL:
        assert cat in behavioral.group(1), f"behavioral category {cat!r} missing"
    for cat in STRUCTURAL:
        assert cat in structural.group(1), f"structural category {cat!r} missing"
    need(classes, "The violating site plus a convention source, or a mechanical fact",
         "`reachability.entrypoint` (plus `reachability.producer` for input-shape claims) and the guards checked",
         "must meet the behavioral requirements for that consequence, or the consequence is excluded",
         "Mocked-only dispatch does not count as an entrypoint", where="Claim classes")
    proto = gate_section(t, "Protocol and instruction claims")
    need(proto, 'the "entrypoint" is the `path:line` of the instruction that prescribes the step',
         'The "producer" is the `path:line` of the consumer\'s precondition or contract that the step must satisfy',
         where="Protocol and instruction claims")
    scope = gate_section(t, "Claim scope")
    need(scope, "The admitted record keeps only supported consequences in `claim.harm`.",
         "at least one consequence is supported and every other table condition holds",
         "and all consequences are listed in `excluded_consequences[]`", where="Claim scope")
    need(scope, "evaluates each entry of `claim.consequences[]` separately", "`excluded_consequences[]`",
         "as `{consequence, reason}`, where `reason` starts with an admission row id (`A1` to `A6`) or `other:`",
         "Every other consequence goes to",
         "A candidate is a `defect` when at least one consequence is supported",
         "Severity is graded only on the admitted harm",
         "An excluded consequence never contributes to severity, the summary, inline comment text or remediation scope",
         "When no consequence is supported, the disposition comes from the first matching table row",
         "Not established: <consequence> (<reason row>)",
         "`NOT-ADMITTED.md` lists the same lines", where="Claim scope")
    narrow = gate_section(t, "Narrow contract defects")
    need(narrow, "is admissible as a `defect` with harm \"the prescribed step cannot be completed as written\"",
         "Both anchors must be verified",
         "A downstream stop that catches the failure does not refute the narrow defect; it only bounds its harm",
         "Claims of additional consequences (wrong success, data loss, silent pass) are evaluated separately "
         "under Claim scope and are excluded unless they are traced", where="Narrow contract defects")
    assert len(re.findall(r"^```jq$", g, flags=re.M)) == 1


def check_at05(t):
    w3 = wave3(t)
    steps = re.findall(r"^(\d+[a-c]?)\. (.*)$", w3, flags=re.M)
    heads = [body[:70].lower() for _, body in steps]
    order = ["parse", "validation", "admission", "attribution", "dedupe", "remap", "ledger", "compose", "invariant", "audit.log"]
    positions = []
    for word in order:
        hits = [i for i, h in enumerate(heads) if word in h]
        assert hits, f"no Wave 3 step names {word!r}"
        positions.append(hits[0])
    assert positions == sorted(set(positions)), f"Wave 3 steps are out of order: {dict(zip(order, positions))}"
    remap = next(body for _, body in steps if "remap" in body[:70].lower())
    assert "unmerged defects only" in remap
    grounding = next(body for _, body in steps if "validation" in body[:70].lower())
    need(grounding, 'section "Location grounding"', "refs/claim-gate.md", where="Wave 3 step 3")
    lg = gate_section(t, "Location grounding")
    need(lg, "head_mismatch_context_unavailable", "`unproven`", "is not a mismatch", "git show <headRefOid>:<path>",
         "head_object_check: match", "In-diff lines are still validated", where="Location grounding")
    need(w3,"A line outside the diff is kept as a candidate with `in_diff: false`; admission decides")


def check_at06(t):
    s = t["skill"]
    oc = section(s, "## Output Contract", "## Wave Structure")
    for field in ("candidates_path", "not_admitted_path", "disposition_count", "remediation_count",
                  "coverage_complete"):
        assert f"| `{field}` |" in oc, field
    need(oc, "`{critical: N, high: N, medium: N, low: N, nit: N}`", "equals the ledger's `findings_count`",
         "{defect: N, unproven: N, rejected: N, intentional_limitation: N, documented_prerequisite: N, merged: N}",
         "{critical: N, high: N}", where="Output Contract")
    coverage_row = next(ln for ln in oc.splitlines() if ln.startswith("| `coverage_complete`"))
    need(coverage_row, "skipped", "truncated")
    summary = section(s, "<!-- SC:AUGGIE-REVIEW:SUMMARY", "-->")
    need(summary, "unproven:", "rejected:", "intentional_limitation:", "documented_prerequisite:",
         "coverage_complete:", "status: <success|partial|failed>", where="SUMMARY header")


def check_at07(t):
    s = t["skill"]
    w0 = section(s, "### Wave 0: Resolve & Validate Target", "### Wave 1")
    header = section(w0, "<!-- SC:AUGGIE-REVIEW:TARGET", "-->")
    need(header, "mode:", "base:", "head:", "head_match:", "local_sha:", "worktree_dirty:", "head_object_check:",
         "evidence_source:", where="TARGET header")
    need(w0, 'section "Attribution"', "refs/claim-gate.md")
    assert ("snapshot mode records `introduced_in: not_applicable_snapshot` for every candidate and never "
            'says "introduced", "regression" or "this PR"') in w0.replace("Snapshot mode", "snapshot mode")
    need(w0, "keep out-of-diff findings as candidates with `in_diff: false`")
    attr = gate_section(t, "Attribution")
    need(attr, "`evidence_source` is `local_read`, `head_object` or `diff_new_side`",
         "`local_read` is not used when `target.mode == pr` and `head_match == false`",
         "use the head object only when `head_object_check == match`",
         "`match` requires `headRefOid` equal before and after `gh pr diff`", "git cat-file -e",
         "agreement of every cited in-diff line", "diff_new_side",
         "use `git show HEAD:<path>`, not the working tree", "worktree_dirty",
         "`head`, `base`, `unknown` or `not_applicable_snapshot`", "`present`, `absent` or `unchecked`",
         "never says \"introduced\", \"regression\" or \"this PR\"", "Mode-derived scope",
         "`remediation_eligible: false`",
         "Hunks absent from `HEAD` get `unknown`",
         "Scope comes from `target.mode`: `pr` is as-submitted; `diff` and `snapshot` are current state",
         "`current_status: absent` on a defect requires `target.mode == pr`",
         "A pre-existing defect (`introduced_in: base`) stays admissible and is labeled pre-existing",
         where="Attribution")
    need(gate_section(t, "Evidence-source rules"),
         "any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`",
         where="Evidence-source rules")
    assert re.search(r"^### Mode-derived scope$", t["gate"], flags=re.M)


def check_at10(t):
    r = t["rubric"]
    assert r.index("## Admission precedes grading") < r.index("## Severity-remap algorithm")
    sec = section(r, "## Admission precedes grading", "## Severity-remap algorithm")
    need(sec, "Only admitted defects", "Step 3 (the low-confidence drop) is not applied",
         "Step 4 (diff locality) still applies", "Steps 1 to 4 below are unchanged", "capped at Medium",
         "`security` or `data-integrity`", "regulatory or compliance", "unknown frequency is not a qualification",
         "A category floor applies only when the admitted harm meets that floor's tier definition",
         "Otherwise the floor is not applied and `harm_below_floor` is recorded",
         "whose category is not `security` or `data-integrity` and whose harm does not meet a Critical definition",
         "Demonstrated harm with unknown frequency is not a qualification and is not capped",
         where="Admission precedes grading")
    table = [ln for ln in section(r, "## Decision-mode summary").splitlines() if ln.startswith("| ")]
    first = table[1]
    assert first.startswith("| Inconclusive — review incomplete"), "Inconclusive must be the first data row"
    need(first, "coverage.complete == false", "regardless of counts", where="Inconclusive row")
    assert any(ln.startswith("| No defects admitted") and "non-empty ledger with zero defects" in ln for ln in table)


def check_at11(t):
    h = t["handoff"]
    need(h, "`remediation_count.critical + remediation_count.high >= 1`",
         "set of unmerged, `remediation_eligible`, Critical/High defects",
         "WHERE: <list of the files of the `remediation_ids` records>")
    phase_a = section(h, "## Phase A", "## Phase B (plan route)")
    assert ("address only findings whose id is in `remediation_ids`; ignore every other part of the report"
            in phase_a.lower())


def check_at12(t):
    s = t["skill"]
    w3 = wave3(t)
    tpl = re.search(r"````markdown\n(.*?)\n````", w3, flags=re.S)
    assert tpl, "report template not found"
    tpl = tpl.group(1)
    entry = section(tpl, "#### C1. <Short title> (id: <id>)", "(repeat per finding")
    need(entry, "- **Evidence kind**:", "- Not established: <consequence> (<reason row>)", "- **Qualification**:",
         where="heading entry")
    nits = section(tpl, "### 💬 Nits", "## Architectural")
    need(nits, "- <!-- id: <id> -->", "**Evidence kind**", where="Nits")
    cross = section(tpl, "## Architectural / Cross-Cutting Observations", "## Audit")
    need(cross, "- <!-- id: <id> -->", "**Evidence kind**", "never list items here", where="Cross-Cutting")
    need(tpl, "Not admitted: <U> unproven, <R> rejected, <L> intentional limitations, <P> documented prerequisites, <M> merged (see NOT-ADMITTED.md)")
    for kept in ("# Code Review:", "## Findings", "## Audit"):
        assert re.search(rf"^{re.escape(kept)}", tpl, flags=re.M), kept
    assert not re.search(r"^#{1,6}\s+Not Admitted", s, flags=re.M | re.I)


def check_at13(t):
    w3 = wave3(t)
    need(w3, "`NOT-ADMITTED.md` is mandatory", "never posted to a PR and never passed to `/sc:design`",
         "id, title, disposition, reason row and citation", "Merged into", "excluded consequences")


def check_at14(t):
    s = t["skill"]
    w2 = section(s, "### Wave 2: Review Agent Pass", "### Wave 3")
    need(w2, "or every chunk skipped", "`jq --version`", "`invariant_check_unavailable`", "before Wave 3",
         "`REVIEW.md` and `audit.log` are still written", where="Wave 2")
    w3 = wave3(t)
    need(w3, "Wave 2 complete", "`coverage.complete == false` never yields `success`",
         "empty-diff short-circuit", "stays `success`", "`REVIEW.md` and `audit.log` are written on every status",
         "A non-zero or missing `jq_exit`, or a missing `candidates.json`, makes the status `failed`",
         "The reported status is the ledger's `run_status` when `jq_exit` is 0", where="Wave 3")
    status = gate_section(t, "Status mapping")
    need(status, "`failed` only for a ledger or invariant failure", "`invariant_check_unavailable`",
         "`partial` keeps the baseline causes", "`coverage.complete == false`", "never yields `success`",
         "The reported status equals the ledger's `run_status` when `jq_exit == 0`, and is `failed` otherwise",
         where="Status mapping")
    need(w2, "the status is `failed` with reason `invariant_check_unavailable`",
         "`allowed-tools` is not a prerequisite check", where="Wave 2")
    need(status, "or `jq` absent at the preflight (reason `invariant_check_unavailable`)", where="Status mapping")
    need(gate_section(t, "Invariant check"),
         "If it is not, the status is `failed` with reason `invariant_check_unavailable`", where="Invariant check")
    assert "Candidates not finished are `unproven`" in gate_section(t, "Refutation record")


def check_at15(t):
    w4 = section(t["skill"], "### Wave 4: Post & Handoff", "## Will Do")
    steps = {m.group(1): m.group(0) for m in re.finditer(r"^(\d)\. .*$", w4, flags=re.M)}
    post, offer = steps["1"], steps["3"]
    need(post, "status is not `failed`", "Nothing is posted when the status is `failed`",
         "read only the unmerged defects in `candidates.json`", where="Wave 4 step 1")
    need(w4, "The posted bytes are the `REVIEW.md` that passed the invariant check",
         "each unmerged Critical and High defect")
    need(offer, "status is not `failed`", "`remediation_count.critical + remediation_count.high >= 1`",
         where="Wave 4 step 3")


def check_at23(t):
    c = t["command"]
    boundaries = section(c, "## Boundaries", "## Related Commands")
    will, will_not = boundaries.split("**Will Not:**")
    need(will, "Publish only admitted defects; keep unproven, rejected, intentional-limitation and "
               "documented-prerequisite records locally")
    need(will_not, "Promote an unproven, rejected, limitation or prerequisite candidate to a finding, or express "
                   "doubt as a lower severity")


def check_at24(t):
    g = t["gate"]
    ref = gate_section(t, "Refutation record")
    need(ref, "`checked: <path:line>`", "`not_applicable: <reason>`", "`mechanical: <fact>`", "`blocks`",
         "`does_not_block`", "`refutation_citation: <path:line>` is required on every `rejected`, "
         "`intentional_limitation` and `documented_prerequisite` record",
         "Caller search runs only when no entrypoint is cited", "`admission_budget{", where="Refutation record")
    dedupe = gate_section(t, "Mechanism dedupe")
    need(dedupe, "`runtime_reproduced` > `static_traced` = `protocol_literal` > `speculative`",
         "the decider strictly outranks every non-defect member", "`unproven` with reason `other:mechanism_conflict`",
         "Equal rank gives `unproven` with `other:mechanism_conflict`", "`merged_into: <id>`",
         "take the group's final `disposition`", "copy the decider's final `severity`",
         "never as a maximum of hints", "unioned into the group", "evaluated by rows A3 and A4",
         "Refutation union", "Strict dominance", "does_not_block",
         "`mechanism_key = <root-cause path>::<enclosing symbol or heading>::<normalized expected behavior>`",
         "group by it across chunks, personas and lines",
         "Two candidates on one line with different keys stay separate",
         where="Mechanism dedupe")
    rules = {
        "Policy challenge": ["A3 does not apply", "higher-precedence requirement", "policy_challenge: <path:line>"],
        "Availability and visibility": ["silently stalls, hides or discards valid work is harm without data corruption",
                                        "A fail-closed refusal of unsupported or ambiguous input is not harm by itself"],
        "Unknown evidence": ["never treated as positive evidence for a less-safe path"],
        "Synthetic input": ["accepted by the verified producer", "No record claims live frequency"],
        "Low confidence": ["`confidence: low` is `unproven` unless", "`hedge_resolved: <path:line>`"],
        "Qualification": ["`scope_citation`",
                          "whose category is not `security` or `data-integrity` and whose harm does not meet a "
                          "rubric Critical criterion is capped at Medium",
                          "An unestablished condition is `unproven` (A6)",
                          "Demonstrated harm with unknown frequency is not a qualification and is not capped"],
    }
    for name, needles in rules.items():
        need(gate_section(t, name), *needles, where=name)


# ------------------------------------------------------------------ tests


@pytest.fixture(scope="module")
def texts():
    return load(REPO)


def test_at01_prompts_output_contract(texts):
    """AT-01"""
    check_at01(texts)


def test_at02_quality_bar(texts):
    """AT-02"""
    check_at02(texts)


def test_at03_reviewer_agent(texts):
    """AT-03"""
    check_at03(texts)


def test_at04_claim_gate_contents(texts):
    """AT-04"""
    check_at04(texts)


def test_at05_wave3_step_order_and_location_grounding(texts):
    """AT-05"""
    check_at05(texts)


def test_at06_output_contract_and_summary(texts):
    """AT-06"""
    check_at06(texts)


def test_at07_wave0_target_provenance(texts):
    """AT-07"""
    check_at07(texts)


def test_at10_rubric_admission_precedes_grading(texts):
    """AT-10"""
    check_at10(texts)


def test_at11_remediation_handoff(texts):
    """AT-11 (the existing remediation-template test module runs separately in the regression set)"""
    check_at11(texts)


def test_at12_report_template(texts):
    """AT-12"""
    check_at12(texts)


def test_at13_not_admitted_file(texts):
    """AT-13"""
    check_at13(texts)


def test_at14_wave2_exit_and_status(texts):
    """AT-14"""
    check_at14(texts)


def test_at15_wave4_defect_only(texts):
    """AT-15"""
    check_at15(texts)


def test_at23_command_boundaries(texts):
    """AT-23"""
    check_at23(texts)


def test_at23_command_frontmatter_and_flags_unchanged():
    """AT-23: frontmatter and option table equal the baseline (skipped with a reason if the baseline commit is absent)."""
    probe = subprocess.run(["git", "cat-file", "-e", f"{BASELINE}:{FILES['command']}"], cwd=REPO, capture_output=True)
    if probe.returncode != 0:
        pytest.skip(f"baseline commit {BASELINE} is not in this checkout")
    base = subprocess.run(["git", "show", f"{BASELINE}:{FILES['command']}"], cwd=REPO, capture_output=True,
                          text=True, check=True).stdout
    now = (REPO / FILES["command"]).read_text(encoding="utf-8")

    def head_and_options(text):
        return text.split("## Behavioral Flow")[0]

    assert head_and_options(now) == head_and_options(base)


def test_at24_claim_gate_rules_and_merge_fixtures(texts):
    """AT-24"""
    check_at24(texts)
    fixtures = Path(__file__).parent / "fixtures/auggie_claim_gate/jq"
    names = {p.name for p in fixtures.glob("*.candidates.json")}
    assert any(n.startswith("invalid-j07-") for n in names) and any(n.startswith("invalid-j08-") for n in names)
    assert "valid-merged-does-not-block.candidates.json" in names


def test_at25_module_placement_canonical_paths_and_jq_absent_failure():
    """AT-25: modules live in tests/skills/, read canonical src/ files, run real jq, fail (not skip) without jq."""
    here = Path(__file__).resolve().parent
    for name in ("contract", "jq"):
        assert (here / f"test_auggie_claim_gate_{name}.py").is_file(), name
    for rel in FILES.values():
        assert (REPO / rel).is_file() and rel.startswith("src/superclaude/"), rel
    jq_src = (here / "test_auggie_claim_gate_jq.py").read_text(encoding="utf-8")
    need(jq_src, "refs/claim-gate.md", "src/superclaude", 'shutil.which("jq")', "pytest.fail(", "subprocess.run")
    assert "pytest.skip" not in jq_src and "importorskip" not in jq_src and "skipif" not in jq_src
    # run the jq test with jq hidden from PATH: it must FAIL and the message must name jq (not skip)
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"{here / 'test_auggie_claim_gate_jq.py'}::test_valid_pair_passes[valid-heading-defect]"],
        cwd=REPO, capture_output=True, text=True, env={"PATH": "/nonexistent"}, timeout=120,
    )
    out = res.stdout + res.stderr
    assert res.returncode != 0, out
    assert "jq is not on PATH" in out and "1 failed" in out and "skipped" not in out, out


# -------------------------------------------- the checks fail on a modified copy


def _copy_tree(dest: Path) -> None:
    for rel in FILES.values():
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, target)


MUTATIONS = [
    ("prompts", '"claim": {', check_at01),
    ("prompts", "Never claim live frequency", check_at02),
    ("agent", "record every one as a candidate with a `claim`", check_at03),
    ("gate", "## Narrow contract defects", check_at04),
    ("gate", "Both anchors must be verified", check_at04),
    ("gate", "is not a mismatch", check_at05),
    ("skill", "{critical: N, high: N}", check_at06),
    ("gate", "use the head object only when `head_object_check == match`", check_at07),
    ("rubric", "No defects admitted", check_at10),
    ("rubric", "Step 3 (the low-confidence drop) is not applied", check_at10),
    ("handoff", "`remediation_count.critical + remediation_count.high >= 1`", check_at11),
    ("skill", "- **Evidence kind**: runtime_reproduced | static_traced | protocol_literal", check_at12),
    ("skill", "`NOT-ADMITTED.md` is mandatory", check_at13),
    ("skill", "or every chunk skipped", check_at14),
    ("gate", "`partial` keeps the baseline causes", check_at14),
    ("skill", "Nothing is posted when the status is `failed`", check_at15),
    ("command", "Publish only admitted defects", check_at23),
    ("gate", "silently stalls, hides or discards valid work", check_at24),
    ("gate", "the decider strictly outranks every non-defect member", check_at24),
    ("gate", "is admissible as a `defect` with harm", check_at04),
    ("gate", "Mocked-only dispatch does not count as an entrypoint", check_at04),
    ("gate", "Hunks absent from `HEAD` get `unknown`", check_at07),
    ("gate", "`pr` is as-submitted; `diff` and `snapshot` are current state", check_at07),
    ("rubric", "Otherwise the floor is not applied and `harm_below_floor` is recorded", check_at10),
    ("gate", "Demonstrated harm with unknown frequency is not a qualification and is not capped", check_at24),
    ("gate", "is not harm by itself", check_at24),
    ("gate", "group by it across chunks, personas and lines", check_at24),
    ("gate", ", and all consequences are listed in `excluded_consequences[]`", check_at04),
    ("gate", " and every other table condition holds", check_at04),
    ("skill", "the status is `failed` with reason `invariant_check_unavailable`", check_at14),
    ("gate", "or `jq` absent at the preflight (reason `invariant_check_unavailable`)", check_at14),
    ("rubric", "whose category is not `security` or `data-integrity` and whose harm does not meet a Critical definition", check_at10),
    ("gate", ", and any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`", check_at07),
]


@pytest.mark.parametrize("key,sentence,check", MUTATIONS, ids=[f"{m[2].__name__}-{m[1][:28]}" for m in MUTATIONS])
def test_removing_an_asserted_sentence_fails_the_check(tmp_path, key, sentence, check):
    """T11.AC3: a modified temporary copy fails; src/ is never edited."""
    _copy_tree(tmp_path)
    check(load(tmp_path))  # the unmodified copy passes
    path = tmp_path / FILES[key]
    text = path.read_text(encoding="utf-8")
    assert sentence in text
    path.write_text(text.replace(sentence, "", 1), encoding="utf-8")
    with pytest.raises(AssertionError):
        check(load(tmp_path))
    assert sentence in (REPO / FILES[key]).read_text(encoding="utf-8")
