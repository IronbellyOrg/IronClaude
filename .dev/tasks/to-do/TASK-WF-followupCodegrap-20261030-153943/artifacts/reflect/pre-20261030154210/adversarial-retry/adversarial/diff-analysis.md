# Diff Analysis: reviewer-card comparison (UC-1 Tier 2 merge, F1 retry)

## Metadata
- Generated: 2026-10-31T00:45:00Z
- Variants compared: 3
  - Variant 1 = reviewer-1-card.yaml (sonnet, analyzer, calibrated C 0.82); checked T1-14..T1-33; new R1-01..R1-09
  - Variant 2 = reviewer-2-card.yaml (glm-5.3, qa, calibrated C 0.76); checked T1-01..T1-13, T1-26, T1-34..T1-39; new R2-01..R2-04
  - Variant 3 = reviewer-3-card.yaml (fable, refactorer, calibrated C 0.81); checked T1-40..T1-43; new R3-01..R3-06
- Audited artifacts: T1 card `O/t1-card.md` (T1-01..T1-43), plan `TASK-WF-followupCodegrap-20261030-153943.md` (cited `plan:N`), spec `source.md` (cited `source.md:N`).
- Facts verified by the orchestrator before this run (binding on all advocates):
  - F-a: `actions/checkout` action.yml has `persist-credentials` default `true` (T1-26 mechanism is real).
  - F-b: PR #329 is merged as 2f10a0e1.
  - F-c: `tests/cli/test_install_codegraph.py:306,320` hardcode `1.6.3` (R1-01 is real).
  - F-d: no `docs(plan): codegraph release monitor` commit exists yet (T1-01 is real today); the planner WILL create it with that subject before execution.
- Facts verified during Step 1 (this run): `src/superclaude/cli/__init__.py:13` is `from .main import main` (R1's T1-15 widening holds); `pyproject.toml:46,54` puts `ruff==0.15.20` in the `dev` extra; `.github/workflows/test.yml:137-144` uses `permissions: contents: read` plus `persist-credentials: false` for the job that runs the codegraph binary; spec `source.md:278,280,332` pass `--github-output` to check/prove, `source.md:279` (fetch) does not, `plan:118` (Task 7 prove) does not; `source.md:419` says "fact 3 shows 20 literal copies" while fact 3 (`source.md:24`) lists 22 locations, of which `CHANGELOG.md:35` and `install_codegraph.py:39` are declared not-changed (`source.md:49,51`), leaving 20 rewritten sites (12+2+1+3+2).
- Total differences found: 30 (structural 2, content 20, contradictions 5, shared assumptions 3 promoted)
- Focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card format | Flow-style T1 checks, block-style new findings with folded claims | Flow-style throughout, terse | Block-style throughout with long corrections | Low |
| S-002 | Partition breadth | 20 T1 checks + 9 new | 20 T1 checks + 4 new | 4 T1 checks + 6 new (narrow partition, deeper per item) | Medium |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | T1-26 token in `.git/config` during `prove` | confirmed, severity left at critical | corrected critical -> important (hash + attestation is the primary control) | not checked | High |
| C-002 | T1-22 literal count (Decisions row says 20; T1 says 22) | corrected: 20 defensible (rewritten sites), nit | not checked | not checked | Medium |
| C-003 | `tests` stage of §2.1 unanchored in Task 5 / static test | R1-08 minor (no file list, no stage value, Tasks 4/8 hardcode v1.6.2) | R2-02 important | R3-02 important, with exact pytest command | Medium |
| C-004 | Sandbox HOME/PATH layout (`source.md:142-143` vs `:281-283`) | T1-16 confirmed; T1 fix = `HOME=<tmp>/home` | R2-03 important; fix = `HOME=<tmp>`, `PATH=<tmp>/.local/bin` | not checked | Medium |
| C-005 | Live harness outputs lack `--github-output` | R1-03 minor (calibrator: overstated, only fetch and plan Task 7 omit it) | T1-12 confirmed | R3-03 minor, class authorized (calibrator: plan:81 says prove output, only plan:122 names the .log) | Medium |
| C-006 | Dropped negative `SuperClaude-Org/.../pull` check (Task 6) | R1-04 minor | T1-13 corrected: pull-link missing, YAML parse check subsumed by static test | R3-05 minor | Low |
| C-007 | `dry_run` no push/PR/issue has no static check | R1-09 minor | T1-34 confirmed (includes the static-check fix) | (calibrator missed_gap: max-parallel already T1-34) | Medium |
| C-008 | Task 5 omits checkout `fetch-depth: 0`, commit author/message, step summary | not raised | T1-35 confirmed | R3-04 minor | Low |
| C-009 | stdlib-only import check | R1-05 allow-list omits needed stdlib (select/threading/dataclasses...) ; T1-15 widened | T1-09 confirmed (grep misses lazy imports) | not raised | Medium |
| C-010 | Acceptance polarity of "prints nothing" criteria (plan:53,96,121) | not raised | not raised | R3-01 important, class regression | High |
| C-011 | `1.6.3` literals outside the replace list (R1-01) | important, spec-inherited, regression | not raised | not raised | High |
| C-012 | Idempotency gate has no owner (R1-02) | important, drift | not raised | not raised | High |
| C-013 | T1-01 planning commit absent | not checked | confirmed critical | not checked | Medium |
| C-014 | §1 "no make sync-dev needed" vs T0/T6 run it (R2-04) | not raised | minor, class necessary (calibrator flagged vocabulary) | not raised | Low |
| C-015 | T1-30 ruff not on bare PATH | corrected to nit (ruff pinned in dev extra, on venv PATH) | not checked | not checked | Low |
| C-016 | T1-42 Task 5 does not name test.yml | not checked | not checked | partly refuted (plan:92 names test.yml) + plan:92 drops `--repo "$GITHUB_REPOSITORY"` from the dispatch | Low |
| C-017 | T1-41 Tasks 3/4 do not name files read | not checked | not checked | corrected; calibrator: `install_mcp.py:804-806` relevance not shown | Low |
| C-018 | Task 2 evidence log `t2-mutation.log` never written (R2-01) | not raised | minor | not raised (T1-40 covers the missing command) | Low |
| C-019 | Infra counter (T1-17) | corrected: (b) inferred, not stated | not checked | not checked | Medium |
| C-020 | T1-15 stdlib vs install_mcp import | corrected wider: importing `superclaude.cli` runs `__init__` -> `main` (click, rich) | not checked | not checked | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | T1-26 severity | critical (confirmed as written) | important | silent | High |
| X-002 | Fix direction for the sandbox layout | HOME=<tmp>/home (T1-16 fix, confirmed) | HOME=<tmp>, PATH=<tmp>/.local/bin (matches `source.md:142` mkdtemp HOME and `:282` `$H/.local/bin`) | silent | Medium |
| X-003 | Which live calls lack `--github-output` | R1-03: Task 4/7 criteria read `result=` lines the commands do not produce | T1-12: only fetch | R3-03: fetch, plus plan:81/122 grep `.log` | Low |
| X-004 | Literal count in Decisions row | 20 defensible | (T1 baseline: 22) | silent | Low |
| X-005 | Severity of the unanchored `tests` stage | minor (R1-08) | important (R2-02) | important (R3-02) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | R1-01 `1.6.3` literals break the first patch bump (F-c verified) | High |
| U-002 | 1 | R1-02 idempotency gate unowned: daily rerun re-pushes an existing branch | High |
| U-003 | 1 | R1-05 allow-list too narrow for the MCP client | Medium |
| U-004 | 1 | R1-06 `gh api --paginate` emits one array per page | Low |
| U-005 | 1 | R1-07 `uv run` vs activated venv in the workflow | Low |
| U-006 | 2 | R2-01 mutation log never written | Low |
| U-007 | 2 | R2-04 sync-dev statement contradiction (class necessary) | Low |
| U-008 | 3 | R3-01 polarity of three "prints nothing" criteria | High |
| U-009 | 3 | R3-06 Task 2 drops "locate by literal, not by line" | Low |
| U-010 | 3 | T1-42 correction: plan:92 drops `--repo` on the in-workflow `gh workflow run` | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | `/sc:implement` transcribes each prose acceptance criterion into a literal bash line run under `bash -euo pipefail` (plan:26), so prose like "prints nothing" is executed, not eyeballed | All three treat plan acceptance prose as executable (R3-01, T1-11, T1-40 confirmations) | Sets the severity of R3-01, T1-11, T1-40 | UNSTATED -> promoted |
| A-002 | The missing planning commit is a defect of the plan, not an ordering step the planner owns | R2 confirms T1-01 critical; R1 confirms T1-27 depends on the T1-01 fix | F-d says the planner will create the commit with that subject; T1-01 severity and T1-27's live failure mode depend on this | CONTRADICTED by F-d -> promoted |
| A-003 | Removing the token from `.git/config` (persist-credentials: false) is sufficient to keep the job token from the third-party binary run by `prove` | R1 confirms T1-26 incl. its fix; R2 only changes severity | Same-job steps share the runner filesystem (`.git/hooks` of the workspace) and user; a process left by the binary can outlive the step; separate-job isolation may be the only sufficient fix | UNSTATED -> promoted |

STATED (not promoted): the codegraph binary is treated as untrusted third-party code at prove time (`source.md:115`).

## Summary
- Total structural differences: 2
- Total content differences: 20
- Total contradictions: 5
- Total unique contributions: 10
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 1, CONTRADICTED: 1); promoted: 3
- Highest-severity items: C-001/X-001 (T1-26), C-010 (R3-01), C-011 (R1-01), C-012 (R1-02)
- Taxonomy tags: L1 = S-001, C-002, C-006, C-014, C-015, X-004; L2 = S-002, C-003, C-005, C-007(?), C-008, C-009, C-013, C-016, C-017, C-018, C-020, X-003, X-005; L3 = C-001, C-004, C-007, C-010, C-011, C-012, C-019, X-001, X-002, A-001, A-002, A-003 (C-007 tagged L3: guard on dry_run)
- Similarity check: differences far exceed 10% of comparable items; debate proceeds.
