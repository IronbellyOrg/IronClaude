# Reviewer brief 1 (pre-execution plan audit, read-only)

## T1 card excerpt

Verbatim contents of .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/reflection-card.yaml:

```yaml
card_version: "1.0"
mode: pre
subject: "Plan TASK-WF-brainstormFixBri-20261106-001016 (7 tasks, 4 phases) checked against its source brief"
claim: >
  The plan covers all five work items of the brief and its constraints, its quoted
  strings match the files on disk (two plan line numbers are slightly off, F-4),
  and it is ready to hand to /sc:implement after one acceptance-check fix (F-1).
self_reported_confidence: 0.88
blind_calibration:
  calibrated_confidence: 0.84
  note: "Below the 0.85 floor, so the tier rubric escalated to Tier 2 (rule 6). Calibrator also noted the stale line numbers (F-4) and that the brief's line-711 reference was not explained."
inputs_read:
  - source.md (13 lines)
  - TASK-WF-brainstormFixBri-20261106-001016.md (99 lines)
  - SKILL.md line 195, handoff-routing.md lines 5-35, commands/brainstorm.md lines 148-161
  - tests/skills/test_brainstorm_protocol.py lines 1-57, tests/skills/test_worker_contract.py lines 280-301 and 499-568
  - orca-worker-contract-spec.md lines 60-63, 142, 443
  - diagnostics.txt (git status grouping, ruff, collect-only count, lint recipe)
coverage:
  parsed_requirements: 5
  parsed_matched: 5
  inferred_requirements: 5
  inferred_matched: 5
  coverage_pct: 1.0
  coverage_pct_union: 1.0
findings:
  - id: F-1
    priority: P1
    claim: "Task 7 third acceptance bullet says git status lists nothing under .dev/tasks/done/ is modified, but 950 staged additions already exist there on the baseline tree."
    evidence: "REPORT.md grounding; diagnostics.txt:3-7; plan:97-98"
  - id: F-2
    priority: P2
    claim: "Task 2 says each tier list ends with its quality_tier line; the Tier 2 list actually ends with the Activation bullet (line 31)."
    evidence: "handoff-routing.md:16-31; plan:39"
  - id: F-3
    priority: P2
    claim: "make lint runs lint-architecture then ruff; only ruff was checked (passes). lint-architecture baseline is unverified."
    evidence: "diagnostics.txt:9, 12-15"
  - id: F-4
    priority: P2
    claim: "Plan line numbers are slightly off: Task 4 says the test is at line 37 (it starts at line 39); Task 5 says the phrases list is at line 286 (the brainstorm entry starts at 286, its phrases list at 288). The implementer finds both by name, so this is wording only."
    evidence: "plan:60, plan:71; tests/skills/test_brainstorm_protocol.py:39; tests/skills/test_worker_contract.py:286-292"
notes:
  - "The brief names test_worker_contract.py line 711. That line is a synthetic-defect mutation list that rewrites a made-up section (tests/skills/test_worker_contract.py:704-723); it does not read the real brainstorm text and needs no change."
unverified:
  - "make lint-architecture baseline"
  - "No test run to prove no test reads plugins/superclaude/commands/brainstorm.md"
  - "Contents of the final text the plan's tasks will write (plan not executed)"
```

## Grounding hunks

codegraph run state: index_state=unchecked checked_at=2026-11-06T00:17Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 (codegraph not used in this run; audit with Read/Grep/Glob only)

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:195-195

```markdown
   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`.
```

### src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:16-33

```markdown
**Tier 1 (primary)**: `mcp__auggie__codebase-retrieval`

- Two parallel queries (per existing brainstorm v1 pattern):
  - Query 1: `"{topic} - find relevant code, existing implementations, related components, and integration points"`
  - Query 2: `"Project architecture, structure, patterns, and conventions related to {topic_domain_area}"`
- Output budget: ~800-1200 tokens summary per query
- quality_tier: `primary`

**Tier 2 (fallback_1)**: codegraph, then native Glob/Grep

- codegraph first (Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`)): run the guide's readiness check once; only when `index_state` is `fresh` and the tools are listed, call `codegraph_files {format: "grouped", maxDepth: 2, path: <relevant dir>, projectPath}` on the relevant directories and `codegraph_search {query: <entity>, limit: 10, projectPath}` for each entity name the topic names. Graph rows are leads (Read before quoting); record any `graph:*` token in the seed-brief Note section. When codegraph is unusable or returns nothing, the native steps below run unchanged.
- Glob for files matching topic keywords
- Grep for symbol/entity names mentioned in topic (for a named function or class, Grep for `def name|class name|function name`, then Read the range)
- Output budget: ~300-500 tokens (raw file list + grep hits)
- quality_tier: `fallback_1`
- Activation: if Tier 1 returns error OR empty result

**Final fallback**: skip enrichment, set quality_tier: `skipped`, log to seed-brief Note section.
```

### src/superclaude/commands/brainstorm.md:157-157

```markdown
- **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused.
```

### tests/skills/test_brainstorm_protocol.py:24-47

```python
def _wave2a_section() -> str:
    text = _BRAINSTORM.read_text(encoding="utf-8")
    parts = re.split(r"###\s*Wave 2A", text, maxsplit=1)
    assert len(parts) == 2, "brainstorm SKILL missing the 'Wave 2A' section"
    # Up to the next '### Wave ' heading.
    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]


def _wave_section(n: str) -> str:
    text = _BRAINSTORM.read_text(encoding="utf-8")
    parts = re.split(rf"###\s*Wave {n}\b", text, maxsplit=1)
    assert len(parts) == 2, f"brainstorm SKILL missing the 'Wave {n}' section"
    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]


def test_brainstorm_unattended_nested_directories_are_named():
    """Under --unattended the nested calls get their own directories (P1 worker contract)."""
    wave3 = _wave_section("3")
    assert "--unattended" in wave3 and "nested/adversarial-" in wave3
    wave2a = _wave2a_section()
    assert "nested/analyze-" in wave2a and "skipped" in wave2a
    assert "exactly as passed" in _wave_section("0")
    refs = _BRAINSTORM.parent / "refs" / "handoff-routing.md"
    assert "nested/adversarial-" in refs.read_text(encoding="utf-8")
```

### tests/skills/test_worker_contract.py:280-297

```python
UNATTENDED_EXPECT: dict = {
    "adversarial": {
        "flags": ["--output", "-o", "--interactive", "-i"],
        "phrases": ["<output>/adversarial/return-contract.yaml", "artifacts"],
        "nested": [],
    },
    "brainstorm": {
        "flags": ["--output", "-o", "--interactive", "-i"],
        "phrases": [
            "research enrichment is off",
            "exactly as passed",
            "never reused",
            "nested/analyze-",
            "nested/adversarial-",
            "dry-run",
        ],
        "nested": ["analyze", "adversarial"],
    },
```

### tests/skills/test_worker_contract.py:499-527

```python
def _check_unattended_section(text: str, expect: dict) -> None:
    for need in (
        "return-contract.yaml",
        "~/.claude/WORKER-CONTRACT.md",
        "--report-dir",
    ):
        assert need in text, f"section lacks {need!r}"
    for tok in expect.get("flags", []):
        assert _token_re(tok).search(text), f"section lacks flag {tok!r}"
    for phrase in expect.get("phrases", []):
        assert phrase in text, f"section lacks {phrase!r}"
    nested = expect.get("nested", [])
    for name in nested:
        assert f"nested/{name}-" in text, f"section lacks nested/{name}-"
    if not nested:
        assert "nested/" not in text, "section names a nested directory"
    assert "src/superclaude/" not in text, "section names a src/superclaude/ path"
    assert not _ORCA_NAME_RE.search(text), "section names an Orca command"


def _removals() -> list:
    """Every (command, kind, token) of UNATTENDED_EXPECT, for the removed-token tests."""
    out = []
    for cmd in sorted(UNATTENDED_EXPECT):
        entry = UNATTENDED_EXPECT[cmd]
        out += [(cmd, "flag", t) for t in entry.get("flags", [])]
        out += [(cmd, "phrase", t) for t in entry.get("phrases", [])]
        out += [(cmd, "nested", f"nested/{n}-") for n in entry.get("nested", [])]
    return out
```

### tests/skills/test_worker_contract.py:704-724

```python
@pytest.mark.parametrize(
    "mutate",
    [
        lambda s: s.replace("return-contract.yaml", "the-file"),
        lambda s: s.replace("~/.claude/WORKER-CONTRACT.md", "the-contract"),
        lambda s: s.replace("--report-dir", "--dir"),
        lambda s: s.replace("alpha-gate", "beta"),
        lambda s: s.replace("nested/analyze-", "nested/other-"),
        lambda s: s + "See src/superclaude/skills/x.\n",
        lambda s: s + "Then run orca worktree create.\n",
    ],
    ids=[
        "no-contract-file",
        "no-contract-path",
        "no-report-dir",
        "no-phrase",
        "no-nested-name",
        "src-path",
        "orca-name",
    ],
)
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62-62

```markdown
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
```

### .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/artifacts/diagnostics.txt (whole file)

```text
# diagnostics captured 2026-11-06T00:14:31Z in /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1
## git status --porcelain, grouped by status letter and first 40 chars of path
    950 A .dev/tasks/done/TASK-WF-p1LivePlanBrief-
      3 R .dev/tasks/to-do/TASK-WF-p1LivePlanBrief
      2 ?? .dev/reflect/pre-TASK-WF-p1LivePlanBrief
      1 ?? .dev/tasks/to-do/TASK-WF-brainstormFixBr
      1 ?? .dev/reflect/pre-TASK-WF-brainstormFixBr
## ruff check . (repo wide)
All checks passed!
## pytest --collect-only -k brainstorm (tests/skills/test_worker_contract.py), last line
=============== 17/394 tests collected (377 deselected) in 0.04s ===============
## make lint recipe
lint: lint-architecture
	@echo "Running linter..."
	uv run ruff check .
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Brief item 2: pin the wording in tests (source.md:7) | Task 4, Task 5 | matched | tests/skills/test_brainstorm_protocol.py:39-47, tests/skills/test_worker_contract.py:286-297 |
| Brief item 5: run affected tests and lint (source.md:10) | Task 7 | matched | .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/artifacts/diagnostics.txt:12-15 |
| Plan acceptance bullets that must be able to pass | F-1, F-3 | finding | plan lines 97-98 |
