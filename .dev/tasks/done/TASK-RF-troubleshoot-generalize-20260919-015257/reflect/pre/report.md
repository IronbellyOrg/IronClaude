# Reflect PRE Report — TASK-RF-troubleshoot-generalize-20260919-015257

```yaml
contract_version: 1.7.0
status: partial                 # forced: citations_dropped = 1 (M-02 grep-hit clause, snippet-mismatch)
mode: pre
tier_reached: 2
confidence_calibrated: 0.864
citations_total: 97
citations_revalidated: 97
citations_dropped: 1
citations_inferred: 6           # policy-unverified (Bash-output / hooks-state / absent-grep claims)
citation_budget_policy: full_reread
coverage_degraded: null
```

**Inputs.** Tasklist `TASK-RF-troubleshoot-generalize-20260919-015257.md` (246 items, 11 phases); spec `merged-report-v2.md` §(d) R-01..R-19. Tree sha `efee40387e3d5b09…` (2 files, `artifacts/input-snapshot.yaml`). No input drift detected at Wave 5.

**Verdict.** APPROVE-WITH-AMENDMENTS. Coverage 0.989 parsed (141 rows: 138 covered / 3 partial / 0 unmapped), 0.982 after the merged ensemble moved R-04.3, R-04.9 and the inferred D2/SKILL:471 row to partial. Best-practice grade 4/5. Six MEDIUM findings (2 Drift, 3 Regression, 1 Refinement) must land before or during execution; nine LOW findings are optional tightenings. No HIGH finding survived calibration.

**Pipeline.** Wave 1 T1 card (requirements-analyst, self 0.90 → calibrated 0.88, ESCALATE) → Wave 2 tier 2 (rule 4 + `--depth deep`) → Wave 3 three `reflect-reviewer` briefs (analyzer / qa / refactorer; calibrated 0.88 / 0.87 / 0.84) → Wave 4 `sc-adversarial --compare` (convergence 0.946, base reviewer-1, `merge_method: adversarial`, EV-1 disk check passed) → Wave 5 evidence-validator (97 cites, 90 verified, 1 dropped, 6 unverified-by-policy).

**Degradations (recorded, not hidden).** `t2_model_class_diversity: degraded` (the Agent tool exposes no per-call model selector — all three reviewers ran on the session class; diversity is persona-only). `calibrator_diversity: degraded` (same class). Advocates in Wave 4 ran inline inside the debate-orchestrator (no Task tool exposed to it); every contested point was resolved by a file Read, never by vote.

## Coverage

| Metric | Value | Source |
|---|---|---|
| parsed rows | 141 | `artifacts/coverage-matrix.yaml:12` |
| inferred rows (Pass 2) | 14 | `:13` |
| coverage_pct (parsed) | 0.989 | `:17` |
| coverage_pct_union | 0.990 | `:18` |
| coverage_pct (merged assessment) | 0.982 | `merged-verdict.yaml` `coverage_pct` |
| unmapped | [] | `:16` |
| partial (T1) | R-01.13, R-16.1, R-19.7 | matrix |
| partial (merged, added) | R-04.3 (M-01), R-04.9 (M-02), INF D2/SKILL:471 (M-14) | merged-verdict |

## Inferred requirements (Pass 2)

14 `INF-NNN` rows were emitted (D2 status enum, D9 fold, HOC:68 latch pin, T11 inversion, harness errata, OQ defaults, etc.); all matched a tasklist item except the D2 site-table row for `SKILL:471`, which is the subject of M-14. No INF row was dropped by the evidence-validator.

## Deviations (pre-execution: defects in the tasklist as written)

Class taxonomy after merge: Drift 2 · Regression 3 · Refinement 9 · Aligned 1. Each block below is Grounded unless a line carries `[INFERRED]`.

### Deviation M-01: R-04.3 probe-safety clause has no landing text

- **Location:** merged-report-v2.md:298; src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:545
- **Mapped tasklist item:** 2.46 (also 9.16 spec-pointer list)
- **Spec section:** §(d) R-04.3
- **Evidence:** v2:298 `exit-status only` / `no secrets` — 0 grep hits in TASK and in research/07-gap-fill-reconcile.md:125; SKILL:545 already carries the invocation-site phrase.
- **Classification:** drift (MEDIUM)
- **Classification rationale:** spec constraint silently dropped at landing; not authorised anywhere in the tasklist.
- **Default remediation:** Item 2.46: append ` Probes are exit-status only and capture no secrets.` to the step-5 insertion; `Verify: grep -cF 'exit-status only' ${SKILL}` == 1; add v2:298 to 9.16's pointer list.

### Deviation M-02: report-template.md:208 keeps the `issue_slug` / "hard-stopped 3 times" cap paragraph after the counter is re-keyed

- **Location:** src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md:208
- **Mapped tasklist item:** Phase 3E (TASK:863-891) — no item targets RT:208
- **Spec section:** §(d) R-04.9 / R-05.8
- **Evidence:** RT:208 (Read, verbatim) still keys on `issue_slug` and says "hard-stopped"; items 2.19 (TASK:425), 2.27, 2.44, 3.17 re-key the counter to `<branch>:<repro-venue-id>` and de-refuse the cap. Phase 3E edits RT:260/:146/:73/:67 only.
- **Classification:** regression (MEDIUM)
- **Classification rationale:** shipped two-source contradiction the 9.18 cross-source lens will either FAIL on (loop) or miss.
- **Default remediation:** Add item 3.25b editing RT:208 to the venue-keyed, non-refusing wording; `Verify: grep -cF 'issue_slug' ${REFS}report-template.md` == 0; add `report-template.md` to 9.18's contradiction scope.

### Deviation M-03: items 9.5 and 9.17 restate an unsatisfiable R-19.7 literal

- **Location:** TASK:1697; TASK:1805-1807; merged-report-v2.md:556-562, :590
- **Mapped tasklist item:** 9.5, 9.17
- **Spec section:** §(d) R-19.7
- **Evidence:** v2:590's `{io,nonio}×{pos,neg}` rule is satisfiable only for producers/discriminator procedures (v2:556-562); both lens Contexts quote the unrestricted form.
- **Classification:** refinement (MEDIUM)
- **Classification rationale:** either lens can return FAIL and drive the Phase 9 loop to its 3-cycle cap.
- **Default remediation:** Rewrite 9.5 and 9.17 Context to the layout-qualified rule; optionally add 7.54 `test_fixture_layout_coverage_rule()` (UD-5).

### Deviation M-07: item 7.2 Verify opens an absolute Coder worktree path

- **Location:** TASK:1250; research/07-gap-fill-test-harness.md:2235
- **Mapped tasklist item:** 7.2
- **Spec section:** §(d) R-19.5
- **Evidence:** 7.2 Verify reads `/config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/…calibration.md`; the harness self-sufficiency invariant (TASK:1460-1463 MANIFEST) requires the vendored copy.
- **Classification:** regression (MEDIUM)
- **Classification rationale:** environment-dependent completion gate; halts Phase 7 on any machine without that worktree.
- **Default remediation:** Point the Verify at `${FIX}regression/sysbox-20260918/GLM-RUN2/run2-tier2-root-cause-analyst-calibration.md` (after 7.32) or drop it (7.48 already asserts A5 ∈ GLM-RUN2); add `grep -c '/config/workspace/Coder/'` == 0 over Phase 7.

### Deviation M-08: `.sh` fixtures exposed to shellcheck / trailing-whitespace hooks

- **Location:** .pre-commit-config.yaml:9-11,20-21,97-98,128-130; research/07-gap-fill-test-harness.md:1897-1941; TASK:226-231
- **Mapped tasklist item:** 0.6 (OQ-3), 10.15
- **Spec section:** §(d) R-19.4 / R-19.6
- **Evidence:** item 0.6 excludes `tests/troubleshoot/fixtures/` from markdownlint only; verbatim `.sh` bodies fail shellcheck (SC2034) and carry trailing whitespace. `[INFERRED]` hooks are not installed in this clone (`.git/hooks` / `core.hooksPath` state is a Bash observation, unverified by the citation gate) — latent until a contributor with hooks touches the tree.
- **Classification:** regression (MEDIUM)
- **Classification rationale:** fixtures are byte-pinned by MANIFEST; any hook rewrite breaks T15.
- **Default remediation:** Add `exclude: ^tests/troubleshoot/fixtures/` to shellcheck + trailing-whitespace at 0.6 (Verify ≥ 3 hits) and run `pre-commit run --files $(git ls-files tests/troubleshoot/fixtures) && git diff --quiet -- tests/troubleshoot/fixtures` explicitly in 10.15 (remedy shape open: UD-2).

### Deviation M-14: SKILL:471 still enumerates `success|partial|failed` after D2 adds `blocked`

- **Location:** src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:471; research/07-gap-fill-decisions.md:75-84
- **Mapped tasklist item:** unmapped (research-origin miss; nearest 2.27 / 3.16)
- **Spec section:** §(d) R-16 (D2 fold)
- **Evidence:** SKILL:471 step 4.5 `(values `success|partial|failed`)` with no `blocked → halt` tie-break; the D2 site table omits this site.
- **Classification:** drift (MEDIUM)
- **Classification rationale:** shipped contract/derivation contradiction no lens is positioned to catch.
- **Default remediation:** Add item 2.27a editing SKILL:471 to `success|partial|blocked|failed` and `status=blocked → halt`; note in 9.18 that the D2 table is not authoritative for this site.

### LOW findings (optional)

| id | class | one-line | remedy |
|---|---|---|---|
| M-04 | Refinement | OQ defaults gate 0.2/0.3/0.6 but live only on the OQ side | prepend `Assumes OQ-N default (TASK:177-181).` to those Contexts |
| M-05 | Refinement | 2.44/2.45/2.46/3.17 new_strings live in reconcile:125/131/155 | inline the paragraphs (copy) |
| M-06 | Refinement | 9.18 authorised-divergence list lacks HOC:68 pin, D9 fold, T11 inversion, D2 gap | extend list #5-#8 |
| M-09 | Refinement | six prose-landed R-rows untested; 9.17 may FAIL on them | list as "prose-landed, untested by design" in 9.17 |
| M-10 | Refinement | 7.48 imports `EXPECTED_IDS` from test module 7.46 | move constant to `_assertions.py` |
| M-11 | Refinement | 8.4 duplicates 8.5's guard; 9.6 sees 20 vs 21 file totals | fold 8.4; state "20 + hc-rename guard = 21" |
| M-12 | Refinement | Phase 2 preamble claims bottom-up; `SKILL:NNN` titles are stale hints | one-sentence preamble rewrite |
| M-13 | Refinement | five same-anchor Edit pairs sequenced by prose only | optional merges; add "run AFTER 2.45" to 2.46 |
| M-15 | Aligned | duplicate-line and co-location handling correct | none |

## Grounding Gaps

None (`grounding-gaps.yaml` not emitted). The six policy-unverified citations are Bash/hook-state observations tagged `[INFERRED]` inline; none is load-bearing for a finding's class.

## Unresolved disagreements (carried, executor's call)

UD-1 keep `test_hc_rename_guard.py` as 21st file vs fold into T14 · UD-2 remedy shape for M-08 (hook excludes vs documented `pre-commit run`) · UD-3 calibration record discrepancy (resolved for this run: audit.log corrected to the file values 0.88/0.87/0.84) · UD-4 246-item session-rollover risk (INV-03 MEDIUM, no remedy proposed) · UD-5 two optional new tests (7.54) in scope or not.

## Inferred-claim audit

citations_total 97 > 20; citations_inferred 6 < 48.5 — no WARN.

## Recommendations

### Recommendation R-001: Land the six MEDIUM amendments before executing Phase 2

Apply M-01 (2.46 clause), M-02 (new 3.25b), M-03 (9.5/9.17 Context), M-07 (7.2 Verify path), M-08 (0.6 excludes + 10.15 explicit run), M-14 (new 2.27a). All are single-Edit changes to the tasklist with exact old_string/new_string given in `merged-verdict.yaml`; none needs new research. Surfaced additively in the tasklist's `### Open Questions` (OQ-4..OQ-9) per the A.10.7 no-auto-mutation rule.

### Recommendation R-002: Add a session-rollover checkpoint (INV-03)

Before resuming at any item ≥ 0.2 after a context rollover, re-read TASK:177-181 (OQ defaults) and the Phase 2 preamble. Cheapest form: one sentence in the Phase 0 preamble.

### Recommendation R-003: Treat the LOW set as executor discretion

M-04..M-06, M-09..M-13 tighten QA-lens Contexts and reduce item count; apply opportunistically when the affected item is next opened.
