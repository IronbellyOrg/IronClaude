# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-10-29T19:55:00Z
- Variants compared: 2
  - Variant A = `variant-1-original.md` (reviewer 1, sonnet:analyzer, 11 findings, calibrated C 0.80)
  - Variant B = `variant-2-original.md` (reviewer 2, haiku/glm-5.3:qa, 7 findings, calibrated C 0.74)
- Input type: YAML reviewer cards (not markdown; proceeding with a logged warning)
- Focus: correctness, coverage, deviation-classification
- Total differences found: 26
- Categories: structural (4), content (4), contradictions (4), unique (10), shared assumptions (4: UNSTATED 2 promoted, STATED 1, CONTRADICTED 1)
- Orchestrator pre-checks (run before the debate, read-only):
  - plan:48 under `bash -o pipefail`: clean input (`src/a.py`) exit 1; `.claude/settings.json` only exit 1; violation (`.claude/skills/x/SKILL.md`) prints the path and exit 0; the real `HEAD~1..HEAD` diff exit 1. The exit code is inverted relative to the "prints nothing" criterion.
  - `bash -euo pipefail -c 'false && true; ...; true && ! true; ...'` keeps running and exits 0: errexit ignores a failing left side of `&&` and any `! cmd` (R1-07 mechanism confirmed).
  - `pyproject.toml` lists `pyyaml>=6.0` as a project dependency (R1-08 premise confirmed).
  - source.md:101 puts the `claude --version` check in the phase function (install_mcp.py, Task 5), while source.md:466 lists U11 under T1 (R1-05: inherited from spec).
  - coverage-matrix.yaml:319-325 INF-037 cites source.md:289 (U4) -> Task 7; :454-461 INF-056 cites source.md:308 (U23) -> Task 3 (P2R2-5 holds with the calibrator's U23 correction).
  - source.md:374-375 (layer 2 step 5) has the negative `disconnected|not connected|failed` check; source.md:714 (T12) does not (R1-09: inherited).
  - source.md:706: T12 "Files: none in the repository"; plan:272 writes `./artifacts/t16-live-verify.txt` (calibrator note on P2R2-7).

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Taxonomy |
|---|------|-----------|-----------|----------|----------|
| S-001 | Self-audit block | Has a `self_audit` field listing what was checked and one UNVERIFIED item | No self-audit field | Low | L1 |
| S-002 | Finding granularity | Bundles several defects into one finding (R1-04 covers ./artifacts paths, Task 3 hash, Task 14 copy) | One defect per finding (P2R2-3 Task 3 hash, P2R2-4 paths split) | Medium | L2 |
| S-003 | Non-defect entries | Lists only defects | Includes a non-defect `authorized` entry (P2R2-7, fix "None") | Low | L1 |
| S-004 | Citation style | Every finding cites spec lines (source.md) | Cites plan lines plus reflect artifacts (coverage-matrix.yaml) | Low | L1 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Taxonomy |
|---|-------|-------------------|-------------------|----------|----------|
| C-001 | Task 16 local-scope `jq -e` inside the exit-0 block (plan:278 vs plan:286) | R1-02: drift, important; move out as its own reported criterion with `|| echo LOCAL_SCOPE_HIT` | P2R2-1: drift, important; move out as a report-only criterion recorded in the t16 artifact | Low (agree on defect and fix) | L3 (guard) |
| C-002 | Task 3 real `.mcpServers` hash criterion (plan:86) | Folded into R1-04 (important): "give Task 3 an explicit H0 before and a final equality test after" | P2R2-3 (minor): H0 only exists in Leg B; add H0 first and a closing equality test | Low | L3 (guard) |
| C-003 | Audit scope | Plan vs spec only | Plan vs spec plus the T1 reflect artifacts (coverage matrix false attributions, under-sampling) | Medium | L2 |
| C-004 | Fix approach for `./artifacts/` | Define `ART=<package>/artifacts` once in Constraints with `mkdir -p`, use `$ART` everywhere | Spell out the full package path in Tasks 3, 14 and 16 | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Taxonomy |
|---|-------------------|-------------------|-------------------|--------|----------|
| X-001 | Task 1 `.claude/` guard at plan:48 | R1-01: drift, important; exits 1 under pipefail in the success case, contradicting plan:21 "every line exits 0"; fix with `test -z "$(... || true ...)"` | P2R2-7: authorized, minor, benign addition, fix "None" | High | L3 (exit-status guard) |
| X-002 | Class of the undefined `$E` (plan:107) | R1-03: necessary, minor | P2R2-2: drift, minor (adds: aborts under `set -u`) | Medium | L2 |
| X-003 | Severity of the `./artifacts/` path defect | R1-04: important | P2R2-4: minor | Medium | L2 |
| X-004 | Task 14/16 evidence files | R1-04: Task 14 requires `./artifacts/t14-*.txt` but its block writes only /tmp, no copy line; paths resolve to the never-staged project root | P2R2-7: Tasks 14/16 evidence files are benign authorized additions | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | R1-05: U11 (`claude --version` fails) tests the phase function Task 5 creates, so Task 4 cannot pass it; move U11 to Task 5 (calibrator: confirmed, inherited from source.md:466) | High |
| U-002 | A | R1-06: Task 6's `--list` block prints the Ready line that needs `codegraph_ready()` from Task 7 (calibrator: overstated, ordering ambiguity only) | Low |
| U-003 | A | R1-07: `A && B` / `A && ! B` lines are non-gating under `-e` (plan:162, 165, 202-203, 244; calibrator: plan:84 wrongly cited; inherited from source.md:601, 604, 636, 675) | High |
| U-004 | A | R1-08: `uv run --no-project python -c 'import yaml'` likely fails; make `uv run python` primary (inherited from source.md:649-651) | Low |
| U-005 | A | R1-09: `grep -i connected` also matches "Disconnected"/"not connected" in Task 16 (inherited from source.md:714; layer 2 step 5 has the negative check at source.md:375) | Medium |
| U-006 | A | R1-10: Task 2 drops the T0b "reported to the coordinator in this task's completion message" duty (source.md:448) | Low |
| U-007 | A | R1-11: Task 13 omits the sandbox fallback for `claude mcp get` (calibrator: overstated, included by reference via plan:19, plan:223) | Low |
| U-008 | B | P2R2-5: two containment matches in the T1 coverage matrix are false attributions (INF-037 U4 -> Task 7; INF-056 U23 -> Task 3); true carriers Task 4 and Task 5 | Low |
| U-009 | B | P2R2-6: the matrix under-samples the spec (calibrator: overstated, §6 and §8 do have rows) | Low |
| U-010 | B | P2R2-7: Task 2 "commit only if a file changed" is a benign authorized addition | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | X-001, X-002 (both reviewers judge acceptance commands by exit status) | Single-line bullet acceptance commands outside fenced blocks (plan:46-48, 82-86, 95-98) are run and judged under the plan:21 rule "every acceptance block runs under `bash -euo pipefail`: every line must exit 0" | UNSTATED | Yes |
| A-002 | C-001, X-002 (both label R1-02/P2R2-1 drift; R1 labels several verbatim spec copies necessary, R2 labels them drift) | A defect the plan copied verbatim from the spec is a plan "drift" (rather than an inherited spec defect whose fix is a necessary deviation from the spec text) | UNSTATED | Yes |
| A-003 | C-001, C-004, X-004 (both keep a t16 artifact file, only arguing about its path) | Post-merge Task 16 may write an in-repository artifact file | CONTRADICTED by source.md:706 ("Files: none in the repository; the outputs go only into the issue-#323 comment") | No (flagged for debate) |
| A-004 | X-003, C-004 | Acceptance commands run with the repository root as the working directory | STATED (R1-04 "Acceptance commands run from the repo root"; P2R2-4 "when run from the repo root") | No |

Promoted shared-assumption diff points:

| A-NNN | Assumption | Source Agreement | Impact | Status | Taxonomy |
|-------|------------|------------------|--------|--------|----------|
| A-001 | Bullet-form acceptance commands inherit the plan:21 exit-0 rule | X-001, X-002 | High: decides whether plan:48 is a false failure or merely a mis-specified check | [SHARED-ASSUMPTION] open | L3 (guard) |
| A-002 | Verbatim spec copies classify as plan drift | C-001, X-002 | Medium: decides the `class` and `origin` fields of at least 6 merged findings | [SHARED-ASSUMPTION] open | L2 |

## Summary
- Total structural differences: 4
- Total content differences: 4
- Total contradictions: 4
- Total unique contributions: 10
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 1, CONTRADICTED: 1)
- Convergence denominator: S(4) + C(4) + X(4) + A(2) = 14 diff points
- Taxonomy coverage: L1 = S-001, S-003, S-004; L2 = S-002, C-003, C-004, X-002, X-003, X-004, A-002; L3 = C-001, C-002, X-001, A-001
- Highest-severity items: X-001 (High), A-001 (High), U-001 (High value), U-003 (High value)
- Similarity check: 26 differences across 18 findings; variants are not substantially identical, debate proceeds.
