# Reviewer brief 3 (pre-execution plan audit, read-only)

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

### tests/skills/test_brainstorm_protocol.py:39-47

```python
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

### tests/skills/test_worker_contract.py:286-297

```python
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

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62-62

```markdown
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:142-142

```markdown
| brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | Under `--unattended`, automatic research enrichment (`sk/sc-brainstorm-protocol/SKILL.md:185`) is off (P1); from P2 it passes `--unattended` and a nested report directory (P2) | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:443-443

```markdown
8. How `plugins/superclaude/commands/` (which holds copies such as `agent.md`, `analyze.md`, `brainstorm.md`) is kept in step with `src/superclaude/commands/`; `CLAUDE.md:76` names it as a mirror and `Makefile:68-74` builds plugin artefacts, but the update rule for a command edit was not read. Each phase's plan must resolve this before editing.
```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md:17-24

```markdown
## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker (record: `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/p1-owner-decisions-20261105.md` and `lc10-result.md` in the same folder). Those archived files are read, never edited.
- Edit only these files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill), and the spec lists the sync mechanism as an open item (spec line 443). It is not edited by this plan; Task 7 confirms it is untouched.
- No new text in the two installed primitives (the skill and its refs, the command file) may name a `src/superclaude/` path or an Orca command (`tests/skills/test_worker_contract.py` `_check_unattended_section` fails on both).
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the installed copies under `~/.claude/` are updated later by the owner).
- No git commit, push, merge or PR.
```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md:28-52

```markdown
## Task 1: State in the skill that the fallback tier writes no nested folder

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under --unattended" (line 195) ends with: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace the part after `(<n>` starts at 1)` so it reads, in substance: the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract; a nested `analyze` directory exists only when `/sc:analyze` ran; `enrichment_used` records the tier that did run; a nested contract is listed in `artifacts` only for a nested command that ran. Use the exact phrase `write no nested directory` and keep the existing strings `nested/analyze-` and `skipped` in the paragraph. Change nothing else in the file.

Acceptance criteria:
- The Wave 2A paragraph under `--unattended` in `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` contains the phrases `fallback_1`, `write no nested directory` and `nested/analyze-`, and states that the nested directory exists only when `/sc:analyze` ran.
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` shows only that paragraph changed (one line replaced).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` still passes before the test change of Task 4.

## Task 2: State the same rule in the routing ref for both codebase tiers

In `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, the codebase enrichment section has a Tier 1 (primary) heading for `mcp__auggie__codebase-retrieval` (line 16) and a Tier 2 (fallback_1) heading for codegraph, then native Glob and Grep (line 24), each with a bullet list that ends with its `quality_tier` line. Add one bullet to each tier's list, worded: Under --unattended this tier writes no nested directory and no nested contract; the scan is recorded in enrichment_used with this tier's quality_tier. The exact phrase `writes no nested directory` must appear in both bullets. Do not touch the research tiers (lines 36 onward) or the `nested/adversarial-` text.

Acceptance criteria:
- `grep -c 'writes no nested directory' src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2, one in the Tier 1 list and one in the Tier 2 list of the codebase section.
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` shows two added lines and no deletion.

## Task 3: State the same rule in the command file's Unattended mode section

In `src/superclaude/commands/brainstorm.md`, the `## Unattended mode` section has a bullet `**Nested invocations.**` (line 157) that says the `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`. Append to that bullet: a codebase scan done through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command; it writes no nested directory and no nested contract, `enrichment_used` records its tier, and the nested `analyze` directory exists only when `/sc:analyze` ran. Use the exact phrase `writes no nested directory`. Do not name a `src/superclaude/` path or an Orca command, and keep the strings `nested/analyze-` and `nested/adversarial-`. Do not edit `plugins/superclaude/commands/brainstorm.md`.

Acceptance criteria:
- The `**Nested invocations.**` bullet of `src/superclaude/commands/brainstorm.md` contains the phrase `writes no nested directory` and still contains `nested/analyze-` and `nested/adversarial-`.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes with the edit in place.
- `git diff --stat -- plugins` prints nothing.
```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md:56-75

```markdown
## Task 4: Pin the skill and routing-ref wording in test_brainstorm_protocol.py

Depends on: Task 1, Task 2

In `tests/skills/test_brainstorm_protocol.py`, the test `test_brainstorm_unattended_nested_directories_are_named` (line 37) asserts `nested/analyze-` and `skipped` in the Wave 2A section (line 44) and `nested/adversarial-` in `refs/handoff-routing.md`. Extend it, or add a sibling test next to it with the same helpers (`_wave2a_section`, `_BRAINSTORM`), so that it also asserts: the Wave 2A section contains `fallback_1` and `write no nested directory`; and `refs/handoff-routing.md` contains `writes no nested directory` at least twice. Keep every existing assertion.

Acceptance criteria:
- `tests/skills/test_brainstorm_protocol.py` asserts the three new facts above, and every earlier assertion of that test is unchanged.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` passes.
- The new assertions are exact-substring checks (no pattern that the old sentence could also satisfy), so the pre-change text of the skill, which lacks `write no nested directory`, fails them.

## Task 5: Pin the command-file wording in test_worker_contract.py

Depends on: Task 3

In `tests/skills/test_worker_contract.py`, the `UNATTENDED_EXPECT["brainstorm"]["phrases"]` list (line 286) holds `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`. Add the phrase `writes no nested directory` to that list. The removed-token tests (`_removals`, built from `UNATTENDED_EXPECT`) pick the new phrase up on their own; do not add a separate mutation by hand unless the existing parametrized tests fail to cover it.

Acceptance criteria:
- `UNATTENDED_EXPECT["brainstorm"]["phrases"]` in `tests/skills/test_worker_contract.py` contains `writes no nested directory`.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes, and the parametrized removed-token tests include a case for the new phrase: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -p no:cacheprovider --collect-only -q -k brainstorm` lists more cases than it did before the edit.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| 1. Same rule stated in three installed primitives (source.md:6) | Task 1, 2, 3 | matched | SKILL.md:195, handoff-routing.md:16-33, brainstorm.md:157 |
| 4. Corrected live-check wording recorded once (source.md:9) | Task 6 | matched | spec line 62 and line 142 |
| Task order and dependencies | Task 4 after 1,2; Task 5 after 3; Task 7 after all | matched | plan Depends on lines |
