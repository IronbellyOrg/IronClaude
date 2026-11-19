"""TEST-008 — Inherited Structural Verdict freshness / INV-002 2-cycle fixture
(R-064 / FR-CONV.3 PR-04 — Phase-3 / T03.13 deliverable D-0036).

Asserts that the orchestrator's A.10.5 fix-cycle re-entry procedure (SKILL.md
§A.10.5 "Fix-cycle re-entry (INV-002 freshness — stale-verdict rejection)",
7-step block) yields a cycle-2 spawn prompt whose ``## Inherited Structural
Verdict`` region carries the cycle-2 producer verdict — never a stale cycle-1
verdict — when the producer artifact is rewritten between cycles.

The fixture exercises the procedure synthetically: it creates two consecutive
``qa-task-validation-report.md`` artifacts (cycle 1 + cycle 2) whose
"Items Reviewed" tables differ (TB-Add-3 FAIL → PASS), runs the documented
re-extract → re-assemble → re-splice pipeline on each, and compares the two
assembled spawn prompts at the verdict-table region.

Acceptance reference (phase-3-tasklist.md L636-640):
- ``uv run pytest tests/audit/test_inherited_verdict_freshness_inv_002.py -v`` exits 0.
- 2-cycle byte-diff shows cycle-2 verdict in cycle-2 spawn prompt.
- Stale cycle-1 verdict NOT present in cycle-2 spawn.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0036/evidence.md``.

Companion shell fixture: ``D-0030/fixture-2cycle.sh`` (static demonstration).
This pytest module is the merge-gate fixture (per D-0030 §5 deferral note).

Run: ``uv run pytest tests/audit/test_inherited_verdict_freshness_inv_002.py -v``
"""

from __future__ import annotations

import difflib
import hashlib
import re
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"
SKILL_MIRROR = REPO_ROOT / ".claude" / "skills" / "task-builder" / "SKILL.md"

BLOCK_HEADER = "## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)"
FIX_CYCLE_HEADER = (
    "**Fix-cycle re-entry (INV-002 freshness — stale-verdict rejection):**"
)
INV002_LOG_TOKEN = "INV-002: re-extracted verdict for"


# ---------------------------------------------------------------------------
# Synthetic producer artifacts (cycle-1 + cycle-2) — TB-Add-3 FAIL → PASS.
# ---------------------------------------------------------------------------

CYCLE1_PRODUCER = """# qa-task-validation-report.md (cycle 1 — pre-fix)

## Items Reviewed

| Item ID  | Check                                  | Verdict | Notes                                  |
|----------|----------------------------------------|---------|----------------------------------------|
| TB-Add-1 | Placeholder scan (no TBD/TODO/FIXME)   | PASS    | clean                                  |
| TB-Add-2 | Item count bounds                      | PASS    | 28 items, within bounds                |
| TB-Add-3 | Clarification adjacency                | FAIL    | items 4, 7 missing Open-Question refs  |
| TB-Add-4 | Circular dependency detection          | PASS    | DAG verified                           |
| TB-Add-5 | Granularity / XL splitting             | PASS    | no XL items                            |

## Verdict

VERDICT: FAIL (TB-Add-3 unfixable in single pass)
"""

CYCLE2_PRODUCER = """# qa-task-validation-report.md (cycle 2 — post-fix)

## Items Reviewed

| Item ID  | Check                                  | Verdict | Notes                                  |
|----------|----------------------------------------|---------|----------------------------------------|
| TB-Add-1 | Placeholder scan (no TBD/TODO/FIXME)   | PASS    | clean                                  |
| TB-Add-2 | Item count bounds                      | PASS    | 28 items, within bounds                |
| TB-Add-3 | Clarification adjacency                | PASS    | items 4, 7 now reference OQ-1/OQ-2     |
| TB-Add-4 | Circular dependency detection          | PASS    | DAG verified                           |
| TB-Add-5 | Granularity / XL splitting             | PASS    | no XL items                            |

## Verdict

VERDICT: PASS
"""

CYCLE1_FAIL_ROW = "| TB-Add-3 | Clarification adjacency                | FAIL    | items 4, 7 missing Open-Question refs  |"
CYCLE2_PASS_ROW = "| TB-Add-3 | Clarification adjacency                | PASS    | items 4, 7 now reference OQ-1/OQ-2     |"


# ---------------------------------------------------------------------------
# A.10.5 re-extract + re-splice helpers — port of SKILL.md §A.10.5 procedure
# (steps 2-5 + step 7). Keeps the orchestrator logic in a single tested place.
# ---------------------------------------------------------------------------


def extract_items_reviewed_span(text: str) -> str:
    """Extract the ``## Items Reviewed`` span contiguously, per SKILL.md:1206
    step 3 / step-3 of the directive at SKILL.md:1101.

    The span runs from the ``## Items Reviewed`` heading to the next
    top-level ``## `` heading (exclusive).
    """
    lines = text.splitlines()
    out: list[str] = []
    capture = False
    for line in lines:
        if line.startswith("## Items Reviewed"):
            capture = True
            out.append(line)
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            out.append(line)
    # Strip trailing blank lines so byte-diffs do not flap on whitespace.
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def assemble_spawn_prompt(task_dir: Path, span: str) -> str:
    """Assemble the rf-qa-qualitative spawn prompt with the verbatim span
    spliced at the API-002 wire-contract position (after TARGET FILES +
    PROJECT CONVENTIONS, before ADVERSARIAL STANCE / INSTRUCTIONS).

    Mirrors SKILL.md:1104-1191 (the QA prompt template) at the structural
    level — the verdict-table region is the substantive payload under test.
    """
    return (
        "QA_PHASE: task-qualitative\n"
        "fix_authorization: true\n"
        "\n"
        f"TASK FILE: {task_dir}/TASK-DEMO.md\n"
        "\n"
        "TARGET FILES (verify ALL — no spot-checking):\n"
        f"- {task_dir}/TASK-DEMO.md\n"
        "\n"
        "PROJECT CONVENTIONS:\n"
        "None identified.\n"
        "\n"
        f"{BLOCK_HEADER}\n"
        f"{span}\n"
        "\n"
        "**ADVERSARIAL STANCE:** Assume the work contains errors.\n"
        "\n"
        "INSTRUCTIONS:\n"
        "Apply the 15-item Task File Qualitative Review checklist.\n"
    )


def short_sha(data: str | bytes) -> str:
    """First 16 hex chars of sha256 — matches the SKILL.md:1209 log convention."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16]


def emit_inv002_log(
    task_dir: Path, cycle: int, mtime: float, prod_sha: str, block_sha: str
) -> str:
    """Emit SKILL.md:1210 step-7 structured log line (verbatim format)."""
    iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(mtime))
    return (
        f"INV-002: re-extracted verdict for {task_dir}/ cycle={cycle} "
        f"producer_mtime={iso} producer_sha256={prod_sha} block_sha256={block_sha}"
    )


def verdict_table_region(prompt: str) -> str:
    """Return the slice of ``prompt`` from the block-header line through
    the next blank line preceding the ``**ADVERSARIAL STANCE:**`` directive.

    This is the "verdict-table region" referenced in the acceptance criteria.
    """
    lines = prompt.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln == BLOCK_HEADER), -1)
    assert start != -1, "block header missing from prompt"
    end = start + 1
    while end < len(lines) and not lines[end].startswith("**ADVERSARIAL STANCE:"):
        end += 1
    # Strip trailing blank line so diff focuses on payload.
    while end > start and lines[end - 1] == "":
        end -= 1
    return "\n".join(lines[start:end])


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def task_dir(tmp_path: Path) -> Path:
    d = tmp_path / "TASK-DEMO"
    (d / "qa").mkdir(parents=True)
    return d


@pytest.fixture
def two_cycle_artifacts(task_dir: Path) -> dict:
    """Run the full 2-cycle re-extract pipeline and capture per-cycle witnesses,
    spans, assembled prompts, and step-7 log lines.

    Returns a dict with keys ``cycle1`` / ``cycle2`` (each a sub-dict of
    ``producer_path``, ``producer_sha``, ``producer_mtime``, ``span``,
    ``block_sha``, ``prompt``, ``log_line``) plus ``ledger`` recording the
    last_injected_verdict_sha256 entry (step-6 defense-in-depth).
    """
    producer = task_dir / "qa" / "qa-task-validation-report.md"

    # --- Cycle 1 -----------------------------------------------------------
    producer.write_text(CYCLE1_PRODUCER, encoding="utf-8")
    p1_mtime = producer.stat().st_mtime
    p1_sha = short_sha(producer.read_bytes())
    span1 = extract_items_reviewed_span(producer.read_text(encoding="utf-8"))
    prompt1 = assemble_spawn_prompt(task_dir, span1)
    block_sha1 = short_sha(span1)
    log1 = emit_inv002_log(
        task_dir, cycle=1, mtime=p1_mtime, prod_sha=p1_sha, block_sha=block_sha1
    )
    ledger = {str(task_dir): block_sha1}

    # --- Cycle 2 (after producer rewrite) ---------------------------------
    # Force a strictly-newer mtime so the freshness witness moves.
    time.sleep(0.05)
    producer.write_text(CYCLE2_PRODUCER, encoding="utf-8")
    # Bump mtime explicitly in case the FS clock resolution is coarse.
    new_mtime = max(p1_mtime + 1.0, producer.stat().st_mtime)
    import os

    os.utime(producer, (new_mtime, new_mtime))

    # Step 1: discard cached state — re-read from disk below (no reuse).
    # Step 2: re-stat + re-sha256.
    p2_mtime = producer.stat().st_mtime
    p2_sha = short_sha(producer.read_bytes())
    # Step 3: re-extract span contiguously (do NOT reuse span1).
    span2 = extract_items_reviewed_span(producer.read_text(encoding="utf-8"))
    # Step 5: re-assemble + re-splice.
    prompt2 = assemble_spawn_prompt(task_dir, span2)
    block_sha2 = short_sha(span2)
    # Step 6: stale-verdict-rejection — contradiction = producer-changed AND
    # block-sha unchanged. Legitimate case = both unchanged (no-op).
    contradiction = (p1_sha != p2_sha) and (block_sha2 == ledger[str(task_dir)])
    ledger_post = dict(ledger)
    ledger_post[str(task_dir)] = block_sha2
    # Step 7: log line.
    log2 = emit_inv002_log(
        task_dir, cycle=2, mtime=p2_mtime, prod_sha=p2_sha, block_sha=block_sha2
    )

    return {
        "cycle1": {
            "producer_path": producer,
            "producer_sha": p1_sha,
            "producer_mtime": p1_mtime,
            "span": span1,
            "block_sha": block_sha1,
            "prompt": prompt1,
            "log_line": log1,
        },
        "cycle2": {
            "producer_path": producer,
            "producer_sha": p2_sha,
            "producer_mtime": p2_mtime,
            "span": span2,
            "block_sha": block_sha2,
            "prompt": prompt2,
            "log_line": log2,
            "contradiction_detected": contradiction,
        },
        "ledger_pre": ledger,
        "ledger_post": ledger_post,
    }


# ---------------------------------------------------------------------------
# Static SKILL.md procedure checks — guards against accidental regression of
# the A.10.5 fix-cycle re-entry block landed by T03.05 (D-0030).
# ---------------------------------------------------------------------------


class TestFreshnessProcedureWiredInSkill:
    """SKILL.md §A.10.5 contains the 7-step fix-cycle re-entry block, names
    INV-002 in the heading, specifies the step-7 log format, and lives in
    both source-of-truth and ``.claude/`` mirror surfaces."""

    @pytest.fixture(scope="class")
    def src_text(self) -> str:
        return SKILL_SRC.read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def mirror_text(self) -> str:
        return SKILL_MIRROR.read_text(encoding="utf-8")

    def test_fix_cycle_header_present_in_source(self, src_text: str):
        assert FIX_CYCLE_HEADER in src_text, (
            f"Fix-cycle re-entry header missing from {SKILL_SRC}"
        )

    def test_fix_cycle_header_present_in_mirror(self, mirror_text: str):
        assert FIX_CYCLE_HEADER in mirror_text, (
            f"Fix-cycle re-entry header missing from {SKILL_MIRROR}"
        )

    def test_skill_source_mirror_byte_identical(self, src_text: str, mirror_text: str):
        assert src_text == mirror_text, (
            "SKILL.md source and mirror diverged; run `make sync-dev`"
        )

    def test_seven_step_procedure_present(self, src_text: str):
        """Steps 1..7 numbered, each named with the action verb from D-0030 §2."""
        required = [
            "1. **Discard cached state.**",
            "2. **Re-read the producer artifact from disk.**",
            '3. **Re-extract the "Items Reviewed" span contiguously.**',
            "4. **Re-enumerate the TB-Add-* catalogue (INV-010).**",
            "5. **Re-assemble and re-splice.**",
            "6. **Stale-verdict-rejection (defense-in-depth).**",
            "7. **Log the re-extract.**",
        ]
        missing = [step for step in required if step not in src_text]
        assert not missing, f"missing fix-cycle steps in SKILL.md: {missing}"

    def test_inv002_log_format_specified(self, src_text: str):
        """Step 7 publishes the structured-log token TEST-008 asserts against."""
        assert INV002_LOG_TOKEN in src_text, (
            f"INV-002 step-7 log token missing from SKILL.md ({INV002_LOG_TOKEN!r})"
        )

    def test_test_008_cross_reference_present(self, src_text: str):
        """The procedure block names TEST-008 / T03.13 as its merge-gate fixture."""
        assert "TEST-008" in src_text and "T03.13" in src_text, (
            "TEST-008 / T03.13 cross-reference missing from SKILL.md A.10.5 procedure"
        )


# ---------------------------------------------------------------------------
# 2-cycle freshness assertions
# ---------------------------------------------------------------------------


class TestFreshnessTwoCycleSpawnPrompt:
    """Acceptance: cycle-2 spawn carries cycle-2 verdict; cycle-1 stale row
    is not present; byte-diff at verdict-table region surfaces cycle-2 content."""

    def test_cycle2_prompt_contains_cycle2_pass_row(self, two_cycle_artifacts: dict):
        prompt2 = two_cycle_artifacts["cycle2"]["prompt"]
        assert CYCLE2_PASS_ROW in prompt2, (
            "AC-fail: cycle-2 spawn prompt does NOT contain the cycle-2 "
            "TB-Add-3 PASS row.\n"
            f"--- cycle-2 prompt ---\n{prompt2}"
        )

    def test_cycle2_prompt_does_not_contain_cycle1_fail_row(
        self, two_cycle_artifacts: dict
    ):
        prompt2 = two_cycle_artifacts["cycle2"]["prompt"]
        assert CYCLE1_FAIL_ROW not in prompt2, (
            "AC-fail: cycle-2 spawn prompt still contains the cycle-1 stale "
            "TB-Add-3 FAIL row — INV-002 freshness violated.\n"
            f"--- cycle-2 prompt ---\n{prompt2}"
        )

    def test_cycle1_prompt_contains_cycle1_fail_row(self, two_cycle_artifacts: dict):
        """Negative-case anchor: cycle-1 prompt MUST carry the cycle-1 verdict
        (proves the cycle-2 absence is real, not a coincidence of construction)."""
        prompt1 = two_cycle_artifacts["cycle1"]["prompt"]
        assert CYCLE1_FAIL_ROW in prompt1, (
            "cycle-1 spawn prompt missing cycle-1 TB-Add-3 FAIL row "
            "(fixture construction error)"
        )

    def test_cycle1_prompt_does_not_contain_cycle2_pass_row(
        self, two_cycle_artifacts: dict
    ):
        """Symmetric negative anchor — cycle-1 cannot contain cycle-2 content."""
        prompt1 = two_cycle_artifacts["cycle1"]["prompt"]
        assert CYCLE2_PASS_ROW not in prompt1, (
            "cycle-1 spawn prompt contains cycle-2 PASS row (fixture leakage)"
        )

    def test_block_sha_changes_between_cycles(self, two_cycle_artifacts: dict):
        """The block-sha256 ledger entry MUST move when the producer changes —
        defense-in-depth signal that re-extract actually happened."""
        sha1 = two_cycle_artifacts["cycle1"]["block_sha"]
        sha2 = two_cycle_artifacts["cycle2"]["block_sha"]
        assert sha1 != sha2, (
            f"block_sha unchanged across cycles ({sha1} == {sha2}) — re-extract "
            "did not run or producer change was not picked up"
        )

    def test_producer_witness_changes_between_cycles(self, two_cycle_artifacts: dict):
        """SKILL.md:1205 step-2 witness (producer_sha256) MUST differ when the
        producer is rewritten between cycles."""
        s1 = two_cycle_artifacts["cycle1"]["producer_sha"]
        s2 = two_cycle_artifacts["cycle2"]["producer_sha"]
        assert s1 != s2, (
            f"producer_sha256 unchanged across cycles ({s1} == {s2}) — "
            "step-2 freshness witness inert"
        )


class TestFreshnessByteDiff:
    """Byte-diff between cycle-1 and cycle-2 spawn prompts surfaces cycle-2
    content at the verdict-table region (phase-3-tasklist AC L638)."""

    def test_full_prompts_differ(self, two_cycle_artifacts: dict):
        p1 = two_cycle_artifacts["cycle1"]["prompt"]
        p2 = two_cycle_artifacts["cycle2"]["prompt"]
        assert p1 != p2, "cycle-1 and cycle-2 prompts are byte-identical"

    def test_verdict_table_region_differs(self, two_cycle_artifacts: dict):
        r1 = verdict_table_region(two_cycle_artifacts["cycle1"]["prompt"])
        r2 = verdict_table_region(two_cycle_artifacts["cycle2"]["prompt"])
        assert r1 != r2, (
            "verdict-table region byte-identical between cycles — "
            "re-splice did not pick up cycle-2 content"
        )

    def test_byte_diff_surfaces_cycle2_pass_row(self, two_cycle_artifacts: dict):
        """A unified-diff between the two prompts MUST add the cycle-2 PASS row
        and remove the cycle-1 FAIL row."""
        p1_lines = two_cycle_artifacts["cycle1"]["prompt"].splitlines()
        p2_lines = two_cycle_artifacts["cycle2"]["prompt"].splitlines()
        diff = list(
            difflib.unified_diff(
                p1_lines,
                p2_lines,
                fromfile="cycle-1",
                tofile="cycle-2",
                lineterm="",
            )
        )
        added = [
            ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")
        ]
        removed = [
            ln[1:] for ln in diff if ln.startswith("-") and not ln.startswith("---")
        ]
        assert CYCLE2_PASS_ROW in added, (
            f"cycle-2 PASS row not in diff additions: {added!r}"
        )
        assert CYCLE1_FAIL_ROW in removed, (
            f"cycle-1 FAIL row not in diff removals: {removed!r}"
        )

    def test_diff_line_count_nonzero(self, two_cycle_artifacts: dict):
        """Mirrors the shell fixture's PASS (c) assertion: at least one diff
        line at the verdict-table region (``DIFF_BYTES > 0``)."""
        p1 = two_cycle_artifacts["cycle1"]["prompt"]
        p2 = two_cycle_artifacts["cycle2"]["prompt"]
        diff_lines = [
            ln
            for ln in difflib.ndiff(p1.splitlines(), p2.splitlines())
            if ln.startswith(("+ ", "- "))
        ]
        assert len(diff_lines) > 0, "ndiff produced zero +/- lines"


class TestFreshnessLogLine:
    """SKILL.md:1210 step-7 log line is emitted on every fix-cycle boundary
    with the four required witness fields (mtime, producer_sha256, block_sha256,
    cycle counter)."""

    LOG_RE = re.compile(
        r"^INV-002: re-extracted verdict for .+ cycle=(?P<cycle>\d+) "
        r"producer_mtime=(?P<mtime>\S+) "
        r"producer_sha256=(?P<psha>[0-9a-f]{16}) "
        r"block_sha256=(?P<bsha>[0-9a-f]{16})$"
    )

    def test_cycle1_log_matches_format(self, two_cycle_artifacts: dict):
        log1 = two_cycle_artifacts["cycle1"]["log_line"]
        m = self.LOG_RE.match(log1)
        assert m, f"cycle-1 log line malformed: {log1!r}"
        assert m.group("cycle") == "1"

    def test_cycle2_log_matches_format(self, two_cycle_artifacts: dict):
        log2 = two_cycle_artifacts["cycle2"]["log_line"]
        m = self.LOG_RE.match(log2)
        assert m, f"cycle-2 log line malformed: {log2!r}"
        assert m.group("cycle") == "2"

    def test_cycle2_log_sha_matches_block(self, two_cycle_artifacts: dict):
        """Step-7 block_sha256 in the log MUST equal the re-assembled block's sha."""
        log2 = two_cycle_artifacts["cycle2"]["log_line"]
        block_sha2 = two_cycle_artifacts["cycle2"]["block_sha"]
        m = self.LOG_RE.match(log2)
        assert m and m.group("bsha") == block_sha2, (
            f"cycle-2 log block_sha {m.group('bsha') if m else '?'} "
            f"!= recomputed {block_sha2}"
        )

    def test_cycle_logs_distinct(self, two_cycle_artifacts: dict):
        log1 = two_cycle_artifacts["cycle1"]["log_line"]
        log2 = two_cycle_artifacts["cycle2"]["log_line"]
        assert log1 != log2, "cycle-1 and cycle-2 log lines identical"


class TestFreshnessStaleVerdictRejection:
    """Step-6 defense-in-depth: contradiction case (producer-changed AND
    block-sha unchanged) must be detectable from the captured witnesses."""

    def test_no_contradiction_under_genuine_change(self, two_cycle_artifacts: dict):
        """In the happy path (producer rewritten with NEW content), step-6
        MUST NOT flag a contradiction."""
        assert two_cycle_artifacts["cycle2"]["contradiction_detected"] is False, (
            "step-6 false-positive: genuine producer change wrongly flagged as stale"
        )

    def test_contradiction_signature_synthesisable(self):
        """Verify the step-6 detector formula on a synthetic contradiction:
        prior producer-sha != new producer-sha, but block-sha unchanged."""
        prior_producer_sha = "deadbeefdeadbeef"
        new_producer_sha = "f00df00df00df00d"
        prior_block_sha = "abc1234567890abc"
        new_block_sha = (
            "abc1234567890abc"  # contradiction: producer moved, block didn't
        )
        contradiction = (
            prior_producer_sha != new_producer_sha and prior_block_sha == new_block_sha
        )
        assert contradiction is True

    def test_no_op_signature_allowed(self):
        """The legitimate no-op (witnesses identical, block identical) must
        NOT trigger step-6 rejection — only the contradiction case is illegal."""
        producer_sha = "deadbeefdeadbeef"
        block_sha = "abc1234567890abc"
        contradiction = (producer_sha != producer_sha) and (block_sha == block_sha)
        assert contradiction is False


class TestFreshnessLedgerUpdate:
    """The last_injected_verdict_sha256 ledger MUST advance on a successful
    fix-cycle re-injection — proves cycle-2 wrote its block-sha back."""

    def test_ledger_entry_moves_to_cycle2_sha(self, two_cycle_artifacts: dict):
        task_dir_key = str(two_cycle_artifacts["cycle2"]["producer_path"].parent.parent)
        pre = two_cycle_artifacts["ledger_pre"][task_dir_key]
        post = two_cycle_artifacts["ledger_post"][task_dir_key]
        cycle2_sha = two_cycle_artifacts["cycle2"]["block_sha"]
        assert pre != post, "ledger entry did not advance after cycle 2"
        assert post == cycle2_sha, (
            f"ledger entry mismatch: post={post} cycle2_block_sha={cycle2_sha}"
        )
