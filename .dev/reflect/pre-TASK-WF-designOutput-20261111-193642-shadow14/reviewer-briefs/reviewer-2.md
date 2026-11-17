# Reviewer brief — reviewer-2 (persona: qa, model class: haiku, model: claude-haiku-5-5)

You audit a workflow-plan package (UC-1 pre-execution audit of a tasklist against its driving spec). Repository root: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`. The package is archived under `.dev/tasks/done/`; the planned change already landed. Audit coverage and acceptance criteria.

## T1 card excerpt

(from `<output>/t1-card.md`, qa slice)

## Extraction result
- Pass 1 (regex): 0 requirement IDs in spec and tasklist (8th consecutive parsed-sparse run in this workspace).
- Pass 2 (inference): 8 rows INF-001..INF-008; parsed=0 < inferred=8 → coverage_degraded: parsed-sparse; T1 stop forbidden; Tier 2 forced.

## Coverage verdict
All 8 inferred rows map into the tasklist by containment. coverage_pct: null (0 parsed), coverage_pct_union: 1.0, unmapped union: []. S_dev_density: 0.0.

## Grounded observations (qa-relevant)
1. Pinned-phrase risk retired: tests/skills/test_worker_contract.py:550 pins `design-report.md`, `no gate`, `consent is never given` for design; all three survive on HEAD.
2. Task 2 AC3 carries the escape-hatch shape: "or any failure is shown in ./artifacts/t2-checks.log and is not attributable to design.md" — attribution judgment makes the AC unable to fail mechanically. Latent only: the recorded run passed clean.
3. Task 2 AC1 "git diff ... shows no edit inside them" requires a baseline diff that no longer exists for an archived package. Contemporaneous artifacts substitute: t2-checks.log:38 shows 1167 tests passed, rc=0.
4. Spec §4 bullet 3 ("no agent is spawned... no brief carries it") is descriptive, restated nowhere in the tasklist; non-imperative, not counted as unmapped.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-designOutput-20261111-193642/source.md:34-67 (spec 3.3 through risks — acceptance criteria section)

```markdown
### 3.3 Edits to existing sections

- Behavioral Flow step 1 and step 4: add a short clause pointing to the Code-graph grounding section. Keep the five step names and the "Key behaviors" bullets.
- Tool Coordination: add one bullet for the codegraph tools (names listed once: `mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`) and keep the Read, Grep/Glob, Write, Bash bullets unchanged.
- Boundaries: unchanged except the existing "Will" list gains nothing; add no new Will Not.
- Unattended mode: unchanged. The `.codegraph/` report-directory exclusion stays.

## 4. Interfaces and contracts

- Input: unchanged (`[target] [--type ...] [--format ...] [--output <file>] [--unattended] [--report-dir <dir>]`). No new flag.
- Output: the design document gains one `Grounding` line (index_state or `graph:*` token). Nothing else changes.
- Readiness state flows only within the run; no agent is spawned by this command, so no brief carries it.

## 5. Constraints

- Edit only `src/superclaude/commands/design.md`. A test that pins it may change only if it must (`tests/skills/test_worker_contract.py` pins the phrases `design-report.md`, `no gate`, `consent is never given`; all stay).
- `grep -n 'src/superclaude' src/superclaude/commands/design.md` must show no read-instruction hit.
- Then `make sync-dev` and `make verify-sync` pass; never stage `.claude/`.

## 6. Acceptance criteria

1. design.md instructs exactly one codegraph readiness check per run and maps tools to steps (section 3.2 item 4).
2. Codegraph used only when `index_state: fresh`; otherwise Glob/Grep/Read with a recorded `graph:*` note; never halts.
3. Frontmatter lists `codegraph` in `mcp-servers`; Tool Coordination names the codegraph tools as reflect.md does.
4. No new `src/superclaude` read-instruction in design.md.
5. `make sync-dev` and `make verify-sync` pass.
6. The related tests pass (`tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`).

## 7. Risks

- Other sessions edit the same checkout: `verify-sync` may name files this change does not own; re-run `make sync-dev` once and never edit them.
- A worker-contract test may pin frontmatter or section order; run it after the edit.
```

### .dev/tasks/done/TASK-WF-designOutput-20261111-193642/artifacts/t2-checks.log:29-39 (verification evidence)

```text
=== Installer Registration ===
  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
verify-sync rc=0
## pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py
============================= 1167 passed in 3.92s =============================
pytest rc=0
```

### tests/skills/test_worker_contract.py:540-575 (pinned-phrase evidence)

```python
        "phrases": ["analyze-report.md", "no gate", "consent is never given"],
        "phrases": ["build-report.md", "no gate"],
        "phrases": ["design-report.md", "no gate", "consent is never given"],
        "phrases": ["knowledge-base mode", "index-report.md", "consent is never given"],
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001: frontmatter mcp-servers: [codegraph] | Task 1 | covered | tasklist:28 |
| INF-002: Code-graph grounding section (7 text reqs) | Task 1 | covered | tasklist:28 |
| INF-003: Behavioral Flow step 1/4 clause | Task 2 | covered | tasklist:41 |
| INF-004: Tool Coordination bullet | Task 2 | covered | tasklist:41 |
| INF-005: edit-only-design.md constraint | Task 1+2 | covered | tasklist:19-22 |
| INF-006: one readiness check, fresh-only, fallback tokens | Task 1 | covered | tasklist:28 |
| INF-007: frontmatter + tool naming as reflect.md | Task 1 | covered | tasklist:31-33 |
| INF-008: sync/verify/pytest checks | Task 2 | covered | tasklist:41-46 |

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.
