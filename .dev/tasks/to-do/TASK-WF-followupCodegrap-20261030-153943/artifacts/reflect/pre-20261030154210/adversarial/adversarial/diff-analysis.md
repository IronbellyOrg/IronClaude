# Diff Analysis: reviewer-card comparison (sc:reflect UC-1 Wave 4)

## Metadata
- Generated: 2026-10-30T16:10:00Z
- Variants compared: 3
  - V1 = reviewer-1-card.yaml (sonnet, analyzer, calibrated C 0.82)
  - V2 = reviewer-2-card.yaml (haiku slot = glm-5.3, qa, calibrated C 0.76)
  - V3 = reviewer-3-card.yaml (fable, refactorer, calibrated C 0.81)
- Context audited: t1-card.md (T1-01..T1-43), plan `TASK-WF-followupCodegrap-20261030-153943.md` (plan:N), spec `source.md` (source.md:N)
- Focus: correctness, coverage, deviation-classification
- Total differences found: 27
- Categories: structural (2), content (18), contradictions (4), unique (12), shared assumptions (3 promoted; 1 stated)

Orchestrator grounding (read-only checks made before the debate, available to every advocate):
- G1: `tests/cli/test_install_codegraph.py:306` is `def _bump(monkeypatch, version="1.6.3")` and `:320` is `new = vdir(box.home, "v1.6.3")`. `:699` holds `"9.9.9"`, but it is a user-managed entry whose version is ignored (`:700` comment). So R1-01 holds and the 9.9.9 mutation value does not collide.
- G2: `git log --all --grep 'docs(plan): codegraph release monitor'` returns nothing. The spec, decisions and task package are untracked (`git status --short`). T1-01 holds.
- G3: `git log origin/master` shows `2f10a0e1 feat: replace codebase-memory and Serena with codegraph (#323) (#329)`. T1-28 holds.
- G4: `gh api --help` (gh 2.103.3) says: "Each page is a separate JSON array or object. Pass `--slurp` to wrap all pages". R1-06 is confirmed, not inferred. With 30 releases and per_page=100 it is latent today.
- G5: source.md:278 (`check`) and :280 / :332 (`prove`) pass `--github-output`. :279 (`fetch`) does not. plan:118 (Task 7 `prove`) does not. plan:81 says "the prove output contains result=pass". plan:122 says "`./artifacts/final-prove.log` and the prove output show `result=pass`". source.md:100 says `key=value` lines go only to the `--github-output` file.
- G6: Fact 3 (source.md:24) lists 22 sites: 15 in tests and 5 in docs, plus CHANGELOG.md:35 and install_codegraph.py:39, which §1 (source.md:49,51) keeps on purpose. 15 + 5 = 20 = the sites T1 rewrites (source.md:419).
- G7: source.md:143 sets `HOME=<tmp>` with `PATH=<tmp>/home/.local/bin`. source.md:281-282 run `"$H/.local/bin/codegraph"` with `H` = the reported `home=`. Those two lines are consistent with HOME=<tmp> and PATH=<tmp>/.local/bin.
- G8: plan:26 (Constraints) states "negative checks as `if cmd; then exit 1; fi`". plan:53, :96 and :121 phrase their criteria as "`<cmd>` prints nothing".

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Partition of T1 checks | T1-14..T1-33 (20) | T1-01..T1-13, T1-26, T1-34..T1-39 (20) | T1-40..T1-43 (4) | Medium. Only T1-26 is checked twice; V3 covers 4 T1 items and spends its effort on new findings. |
| S-002 | Card granularity | compact one-line entries, `[INFERRED]` tags, 9 new findings | compact, 4 new findings, model_note | multi-line notes with corrections, 6 new findings, calibrator `missed_gap` | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | T1-26 severity (checkout token persisted while `prove` runs third-party code) | confirmed, critical (source.md:112,115; test.yml:133-144) | corrected to important ("spec-level hardening; hash+attestation is the primary control") | not checked | High |
| C-002 | §2.1 `tests` stage unanchored | R1-08: no file list, no `stage=tests` value; spec-inherited, minor | R2-02: plan, important, drift; the gap behind INF-042..047 | R3-02: plan, important, drift, with a spec-inherited sub-gap; concrete file list | Medium |
| C-003 | Sandbox HOME/PATH (T1-16) | confirmed T1-16 (two fix options) | R2-03: HOME=<tmp>, PATH=<tmp>/.local/bin (matches :282) | — | Medium |
| C-004 | `result=` lines vs `--github-output` | R1-03: Tasks 4/7 lack `--github-output`; minor drift (calibrator: overstated for check/prove) | — | R3-03: plan:81/:122 grep the .log; minor, **authorized** (calibrator: plan:81 says prove output) | Medium |
| C-005 | Dropped Task 5/6 acceptance lines (T1-13) | R1-04: pull-link check dropped | T1-13 corrected: pull-link only; YAML parse subsumed by static test | R3-05: pull-link check dropped | Low |
| C-006 | Task 5 omissions (T1-35) | — | T1-35 confirmed | R3-04: fetch-depth, commit author/message, step summary (a subset of T1-35) | Low |
| C-007 | `dry_run` gating | R1-09: no static check or R-case in the spec (spec-inherited) | T1-34 confirmed (plan drops rules) | missed_gap note: matrix `max-parallel: 1` (already T1-34) | Low |
| C-008 | Stdlib import check | R1-05: allow-list omits needed stdlib modules | T1-09 confirmed (grep misses lazy imports) | — | Low |
| C-009 | T1-22 count (20 vs 22) | corrected: 20 defensible (rewritten sites), nit | — | — | Medium (refutation candidate, G6) |
| C-010 | T1-30 ruff on PATH | corrected: ruff in dev extras and on the venv PATH; nit | — | — | Low (refutation candidate) |
| C-011 | T1-42 test.yml unnamed | — | — | partly refuted: plan:92 names test.yml; missing path/role and `--repo` on dispatch | Low |
| C-012 | T1-41 citation | — | — | corrected; calibrator: install_mcp.py:804-806 (`_run_argv`) relevance not shown | Low |
| C-013 | T1-38 scope | — | corrected: log cap and process-group kill dropped; fetch order carried by the §2.2 pointer | — | Low |
| C-014 | T1-15 scope | corrected wider: importing `superclaude.cli` runs `__init__` (click, rich) | — | — | Low |
| C-015 | T1-17 (b) | (b) inferred from the exit-1 contract, not stated | — | — | Low |
| C-016 | Acceptance-command semantics under `bash -e` | — | — | R3-01: plan:53/:96 invert, plan:121 always passes; important, regression | Medium |
| C-017 | `make sync-dev` wording (source.md:51 vs :224,:329,:340) | — | R2-04: minor, necessary | — | Low |
| C-018 | Hardcoded v1.6.2 in Tasks 4/8 | R1-08 part b: read the pin with read_pin | T1-18 confirmed by V1 | — | Low |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | T1-26 severity | critical ("confirmed") | important (attestation is the primary control) | — | High: it decides whether the verdict has 1 or 2 criticals |
| X-002 | Deviation class of the `--github-output` defect | drift (R1-03) | — | authorized (R3-03) | Medium: "authorized" means an approved expansion, which a broken criterion is not |
| X-003 | Origin of the `tests`-stage gap | spec-inherited (R1-08) | plan (R2-02) | plan, with a spec sub-gap (R3-02) | Medium: it decides where the fix lands |
| X-004 | Sandbox layout fix direction | T1-16 offers HOME=<tmp>/home or drop `/home` | R2-03: drop `/home` (HOME=<tmp>) | — | Low: same defect, different fix |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | R1-01: `_bump` default `1.6.3` and `vdir "v1.6.3"` (test_install_codegraph.py:306,320) are outside the literal list. The first patch bump to v1.6.3 breaks test_u21 and the new guard test. The 9.9.9 mutation cannot reveal it (G1). | High |
| U-002 | V1 | R1-02: the idempotency gate has no owner (check emits no branch/PR state; route runs post-outcome). Existing-branch push is non-fast-forward, and a declined tag is re-proved daily. | High |
| U-003 | V1 | R1-05: the import allow-list is narrower than the stdlib the design may use | Low |
| U-004 | V1 | R1-06: `gh api --paginate` emits one array per page (G4) | Low |
| U-005 | V1 | R1-07: `uv run` vs the activated venv in the workflow [INFERRED] | Low |
| U-006 | V1 | R1-09: no static check or R-case that dry_run gates push/PR/issue | Medium |
| U-007 | V1 | T1-15 widening (`superclaude.cli.__init__` side effects) | Medium |
| U-008 | V2 | R2-01: plan:55 requires `t2-mutation.log` but nothing writes it | Low |
| U-009 | V2 | R2-04: source.md:51 "no sync-dev step" vs T0/T6 running it | Low |
| U-010 | V3 | R3-01: inverted and vacuous negative checks (plan:53,96,121) | High |
| U-011 | V3 | R3-06: Task 2 omits the locate-by-literal rule (source.md:35) | Low |
| U-012 | V3 | T1-40 fifth instance (plan:35) and the `<id>` placeholder at plan:132 | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|---|---|---|---|---|---|
| A-001 | `/sc:implement` checks each task only against its own body plus Constraints, so spec text a task drops is a real defect, not a pointer the executor follows | All 3 confirm T1-34..T1-43-style "plan drops X" findings | UNSTATED (asserted by T1-40, never verified against the executor protocol) | It decides whether "plan drops spec text" items are important or minor | Promoted |
| A-002 | Spec-inherited findings are in scope for fixing before `/sc:implement` (the spec is editable in the revise loop) | All 3 file spec-inherited findings with spec-side fixes | UNSTATED | If the spec is frozen, spec-inherited fixes must move into plan tasks | Promoted |
| A-003 | The impact of a leaked `contents: write` token does not depend on branch protection on `master` | V1 and V2 both accept the T1-26 mechanism without checking protection | UNSTATED (no reviewer checked branch protection) | Bounds the T1-26 severity: push to master vs only to unprotected branches | Promoted |
| — | Live state from T1 (#329 merged, no plan commit) still holds | All 3 (V1 states it could not re-check) | STATED; verified by orchestrator G2/G3 | — | Not promoted |

## Summary
- Total structural differences: 2
- Total content differences: 18
- Total contradictions: 4
- Total unique contributions: 12
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001 / X-001 (T1-26), U-001 (R1-01), U-002 (R1-02), U-010 (R3-01), C-002 / X-003 (tests stage)
- Convergence denominator: S 2 + C 18 + X 4 + A 3 = 27 diff points
- Similarity check: differences far exceed 10%; the debate proceeds.
