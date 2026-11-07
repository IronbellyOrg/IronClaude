# Reviewer brief 1 (pre-execution plan audit, read-only)

## T1 card excerpt

Verbatim contents of .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/reflection-card.yaml:

```yaml
card_version: "1.0"
mode: pre
subject: "Plan TASK-WF-brainstormFixBri-20261106-021737 (7 tasks, 4 phases), the regenerated plan that applies 17 review corrections, checked against its source brief (source.md, Parts 1 to 5)"
claim: >
  The plan covers the five original brief items and applies all 17 corrections (F-1 to F-17) with the
  replacement wording copied verbatim. Its anchors match the files on disk. It is ready for /sc:implement,
  with the P2 notes below.
self_reported_confidence: 0.88
blind_calibration: {calibrated_confidence: PENDING}
tier_routing: "Forced to Tier 2: strict Pass 1 finds no labelled ID (F-n and INV-n do not match ID_REGEX), 28 inferred rows, so the parse-density guard (coverage_degraded: parsed-sparse) forbids the Tier 1 stop."
coverage:
  parsed_rows: 0
  inferred_rows: 28
  matched_by_containment_rule: 23
  coverage_pct: null
  coverage_pct_union: 0.8214
  s_dev_density: 0.1786
  manual_review_of_the_5_unmatched_rows: "INF-002 (brief item 2, covered by Tasks 4 and 5), INF-007 (F-1, covered by Task 6), INF-009 (F-3, covered by Tasks 1 to 5), INF-018 (F-12, covered by the shared phrases in Tasks 1 to 5) are covered in different words; INF-022 (F-16) is a deliberate narrowing, see F-1 below."
  artifact: artifacts/coverage-matrix.yaml
grounded_checks_passed:
  - "SKILL.md line 195 tail, line 196 blank, line 197 'Quality-tier tracking' heading (artifacts/grounding.txt:9-13)"
  - "handoff-routing.md anchors: Tier 1 line 16, quality_tier line 22, Tier 2 line 24, Activation line 31, Final fallback line 33 (artifacts/grounding.txt:1-8)"
  - "brainstorm.md line 157 ends 'so a nested directory is never reused.' (artifacts/grounding.txt:14-15)"
  - "spec line 62 ends with the sentence Task 6 appends to; spec line 286 is the 7.2 step 4 line ending 'At P0, AC-0.4 replaces this step.' (artifacts/grounding.txt:16-20)"
  - "No test file reads the spec, so the two spec edits cannot break a test (artifacts/grounding.txt:21)"
  - "HEAD copies of the three primitives contain none of the new pins, so the 'fails on pre-change text' claims hold (artifacts/grounding.txt:22-25)"
  - "All five test files named by Task 7 exist; make targets exist (artifacts/grounding.txt:26-46)"
  - "The package passes the workflow quality gate (7 tasks, 4 phases, contiguous, acceptance bullets in every task, no checkbox or numbered lines)"
findings:
  - id: F-1
    priority: P2
    claim: "The plan's Constraints line for correction F-16 says the edits reach the next live plan 'only after they are committed to a branch the live-check worktree is built from'. The brief's correction F-16 asks for 'only after the owner commits and merges them'. The narrowing is deliberate (the earlier review's evidence check found 'merges' unsupported by spec line 282), but the plan does not record the departure."
    evidence: "plan Constraints (line 28); source.md:199; spec:282"
  - id: F-2
    priority: P2
    claim: "Task 7 says 'it writes only the logs and the status snapshot under ./artifacts/'. The brief's correction F-13 gives the sentence 'it writes only the logs under ./artifacts/'. The extension is needed because correction F-2 adds the status-after snapshot, but the departure is not recorded."
    evidence: "plan Task 7 body; source.md:169"
  - id: F-3
    priority: P2
    claim: "Task 7's third acceptance bullet passes only if no new line appears in git status outside the six files and the package folder. If /sc:implement or its final reviewer writes anywhere else under .dev/ (for example a new .dev/reflect or .dev/implement folder), the bullet fails on a correct run. Not verified either way."
    evidence: "plan Task 7 acceptance bullet 3; source.md:53"
  - id: F-4
    priority: P2
    claim: "Task 6 describes the step 4 line as one that 'begins Check the contract (PyYAML ...'; the line actually begins '4. Check the contract'. The anchor is still findable."
    evidence: "plan Task 6 body; artifacts/grounding.txt:19"
risk_surface:
  blast_radius: "Documentation and test text only: six files, no runtime code. A wrong pin turns a test red; a wrong sentence misleads a live-plan author."
  interaction_effects: "Task 4 and Task 5 pins depend on the exact text written by Tasks 1 to 3 (order declared by Depends on). The skill uses the form 'write', the ref and command use 'writes'; the shared phrase 'no nested directory and no nested contract' is a substring of both."
  residual_risks_recorded_in_plan: "Four false-PASS risks of the live-check sentence are listed in Task 6, including the inferred tool names Skill, Agent and Task."
  open_conflict_recorded_in_plan: "Research enrichment from P2 is not covered (Constraints)."
recommendations:
  - id: R-1
    priority: P2
    file: "TASK-WF-brainstormFixBri-20261106-021737.md (Constraints, Task 7 body)"
    change: "Add one sentence to the Constraints saying the F-16 line and the Task 7 'writes only' sentence are deliberately narrower or wider than the brief's, and why."
    verifier: "The Constraints block names both departures."
  - id: R-2
    priority: P2
    file: "TASK-WF-brainstormFixBri-20261106-021737.md (Task 7, third acceptance bullet)"
    change: "State that new lines under .dev/reflect/ or .dev/implement/ created by the executor itself are also allowed, or run a dry check of what the executor writes."
    verifier: "The bullet names every folder the executor is known to write to."
unverified:
  - "make lint-architecture baseline and the two extra test files were not run; the planned text was read against them, not executed"
  - "How /sc:implement and its final reviewer change git status (finding F-3)"
  - "The tool names Skill, Agent and Task in the Task 6 live-check sentence (recorded as a residual risk in the plan)"
```

## Grounding hunks

codegraph run state: index_state=unchecked checked_at=2026-11-06T02:24Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 (codegraph not used in this run; audit with Read/Grep/Glob only)

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:195-197

```markdown
   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`.

2. **Quality-tier tracking** (mandatory per enrichment source):
```

### src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:16-35

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

### Research enrichment (light)
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

### tests/skills/test_codegraph_adoption.py:52-83

```python
def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, end_pattern: str) -> str:
    after = text.split(start, 1)
    assert len(after) == 2, f"missing anchor {start!r}"
    return re.split(end_pattern, after[1], maxsplit=1, flags=re.M)[0]


def _rel(path: Path) -> str:
    return str(path.relative_to(_REPO))


def test_validate_roadmap_step05_puts_codegraph_above_grep_and_never_skips():
    step = _section(_text(_VR_SKILL), "#### Step 0.5", r"^#### |^### ")
    assert "codegraph_search" in step and "Grep" in step
    assert step.index("codegraph_search") < step.index("call `Grep` for its definition")
    assert "skip" not in step.lower(), (
        "Step 0.5 must never skip where the Grep floor exists"
    )


def test_brainstorm_tier2_names_codegraph_files_and_search():
    tier2 = _section(
        _text(_BS_ROUTING), "**Tier 2 (fallback_1)**: codegraph", r"^\*\*Final fallback"
    )
    assert "codegraph_files" in tier2 and "codegraph_search" in tier2
    assert "Glob for files matching topic keywords" in tier2, (
        "native Glob/Grep floor must stay"
    )

```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md:1-120

```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-brainstormFixBri-20261106-021737
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Brainstorm: nested analyze folder only when /sc:analyze ran (corrected plan)

Source: ./source.md
Goal: `/sc:brainstorm` under `--unattended` says, in its skill, its command file and its routing ref, that the nested `analyze` directory is written only by a `/sc:analyze` call, and that the auggie scan and the `fallback_1` scan (codegraph, then Glob and Grep) write no nested directory and no nested contract. Tests pin both halves of that rule, and the worker-contract spec carries a live-check sentence that does not decide the folder by `quality_tier`.

## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces an earlier plan for the same work (package `TASK-WF-brainstormFixBri-20261106-001016`) that an independent review found not ready to run: its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned. This plan applies those corrections. The earlier package is left as it is.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after they are committed to a branch the live-check worktree is built from; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.

## Phase 1: Say it in the installed primitives

## Task 1: State in the skill that the auggie scan and the fallback tier write no nested directory

First, before any edit, save the output of `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 compares against that file.

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under `--unattended`" (line 195) currently ends: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace everything after "(`<n>` starts at 1)" with this exact text, copied character for character:

```text
; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
```

The wording names the writer (a tool or a tier), never a recorded `quality_tier` or a run. A clean `/sc:analyze` run is also `primary`, and `enrichment_used` records `source` and `quality_tier` as separate fields that do not name the tool, so a statement that depended on the tier would be wrong for an analyze run. It states no tier for any `/sc:analyze` outcome and keeps the nested contract listed unconditionally, a failed call's included. Change nothing else in the file.

Acceptance criteria:
- `./artifacts/status-before.txt` exists and was written before the first edit of this plan.
- The paragraph with the bold lead-in "Under `--unattended`" in the Wave 2A section of `SKILL.md` contains `fallback_1`, `write no nested directory and no nested contract`, ``only by a `/sc:analyze` call``, `nested/analyze-` and `skipped`, ends with "The nested contract is listed in `artifacts`, also when the call failed.", and does not contain "only for a nested command that ran".
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` shows one line changed (one insertion, one deletion).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` still passes before Task 4 changes the tests.

## Task 2: State the same rule in the routing ref for both codebase tiers

In `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, the "Codebase enrichment" section has two tier lists. The list under `**Tier 1 (primary)**` (line 16) ends with the line `- quality_tier: ` followed by `primary` in backticks (line 22). The list under `**Tier 2 (fallback_1)**: codegraph, then native Glob/Grep` (line 24) ends with the line `- Activation: if Tier 1 returns error OR empty result` (line 31), and the line `**Final fallback**` (line 33) follows it. Add the bullet below, identical text, as the last bullet of each of the two lists: once after the Tier 1 `quality_tier` line, and once after the Tier 2 `Activation` line, both before the next `**Final fallback**` or `**Tier 2` anchor. The Tier 2 bullet must stay inside the span that `tests/skills/test_codegraph_adoption.py` reads in `test_brainstorm_tier2_names_codegraph_files_and_search` (from `**Tier 2 (fallback_1)**: codegraph` to the line starting `**Final fallback`).

```text
- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
```

The bullet names `/sc:analyze` as the only writer so that a reader of this ref alone does not conclude that codebase enrichment never nests. Do not touch the research tiers (line 35 onward) or the `nested/adversarial-` text.

Acceptance criteria:
- `grep -c 'writes no nested directory' src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2 (kept as a smoke check; Task 4 pins each tier separately).
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` shows two lines added and none deleted; one added bullet follows the Tier 1 `quality_tier` line and the other follows the Tier 2 `Activation` line.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes with the edit in place.

## Task 3: State the same rule in the command file's Unattended mode section

In `src/superclaude/commands/brainstorm.md`, the `## Unattended mode` section has a bullet `**Nested invocations.**` (line 157) that says the `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`. Append this text to the end of that bullet, after "so a nested directory is never reused.", copied character for character:

```text
A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists.
```

Leave the existing sentence "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" unchanged. Do not edit `plugins/superclaude/commands/brainstorm.md`.

Acceptance criteria:
- The `**Nested invocations.**` bullet of `src/superclaude/commands/brainstorm.md` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and still contains `nested/analyze-`, `nested/adversarial-` and "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`".
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes with the edit in place.
- `git diff --stat -- plugins` prints nothing.

## Phase 2: Pin the wording with tests

## Task 4: Pin the skill and routing-ref wording in test_brainstorm_protocol.py

Depends on: Task 1, Task 2

In `tests/skills/test_brainstorm_protocol.py`, the test `test_brainstorm_unattended_nested_directories_are_named` starts at line 39. It asserts `nested/analyze-` and `skipped` in the Wave 2A section (`_wave2a_section()`, line 44) and `nested/adversarial-` in `refs/handoff-routing.md` (line 47). Keep every existing assertion unchanged. Add a sibling test next to it, using the file's own helpers (`_wave2a_section`, `_BRAINSTORM`) and, for the routing ref, the slicing pattern of the `_section(text, start, end_pattern)` helper in `tests/skills/test_codegraph_adoption.py` (it splits the text at `start`, then splits the rest at `end_pattern` with `re.M` and keeps the first part). The new test asserts:

- Paragraph slice: take `_wave2a_section()`, split at the bold lead-in ``**Under `--unattended`**``, and keep the text up to the next blank line. The slice contains `fallback_1`, `write no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and the text `Quality-tier tracking` is not in it, so a slicer that returns the whole section fails.
- Tier slices of `refs/handoff-routing.md` (the file next to the SKILL file): the Tier 1 slice runs from the first `**Tier 1 (primary)**` to the line starting `**Tier 2 (fallback_1)**: codegraph`; the Tier 2 slice runs from there to the line starting `**Final fallback`. Each slice contains `writes no nested directory and no nested contract` exactly once and ``only by a `/sc:analyze` call`` exactly once.

All pins are exact substring checks. On the pre-change text every paragraph-slice pin and every tier-slice pin fails; only the `Quality-tier tracking` absence check passes there, because it guards the slice boundary and not the new wording.

Acceptance criteria:
- `tests/skills/test_brainstorm_protocol.py` contains the new sibling test with the paragraph-slice pins and both tier-slice pins above, and every earlier assertion of `test_brainstorm_unattended_nested_directories_are_named` is unchanged.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/SKILL.md | grep -c 'write no nested directory and no nested contract'` and the same command for `refs/handoff-routing.md` with `writes no nested directory and no nested contract` both print 0, which shows the pins fail on the pre-change text.

## Task 5: Pin the command-file wording in test_worker_contract.py

Depends on: Task 3

In `tests/skills/test_worker_contract.py`, `UNATTENDED_EXPECT["brainstorm"]` is the entry that starts at line 286; its `phrases` list opens at line 288 and holds `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`.

First, before editing, save the output of `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -p no:cacheprovider --collect-only -q -k brainstorm` to `./artifacts/t5-collect-before.txt`. Today the summary line reports 17 collected cases, but that number is not a constant; the saved file is the baseline.

Then add the two phrases `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call`` to that `phrases` list. The removed-token tests (`_removals`, built from `UNATTENDED_EXPECT`) pick up both phrases and add one case for each; do not add a separate mutation by hand. The mutation list near line 711 (lines 704 to 724) rewrites a made-up section and does not read the real brainstorm text, so it needs no change.

Acceptance criteria:
- `UNATTENDED_EXPECT["brainstorm"]["phrases"]` in `tests/skills/test_worker_contract.py` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``.
- The collect-only command above, run again after the edit, reports a collected count equal to the count in `./artifacts/t5-collect-before.txt` plus 2; the plan does not hard-code that number.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/commands/brainstorm.md | grep -c 'writes no nested directory and no nested contract'` prints 0, which shows the new phrase fails on the pre-change command file.

## Phase 3: Record the corrected live-check wording

## Task 6: Add the corrected wording to the worker-contract spec in two places

In `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` make two edits, each on one existing line.

First, the section 2.1 bullet `**Nested propagation rule**` (line 62) ends with "Each command's `## Unattended mode` section names its nested invocations." Append this sentence to that line, copied character for character:

```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Brief item 2 and corrections F-3, F-4, F-5, F-8, F-10, F-12 (tests pin the wording) | Tasks 4, 5 | matched | .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/artifacts/coverage-matrix.yaml |
| Correction F-2 and F-6 (checks and test set) | Task 7 | matched | plan Task 7 |
