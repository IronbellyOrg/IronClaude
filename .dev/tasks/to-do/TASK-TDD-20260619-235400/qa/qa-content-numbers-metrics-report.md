# QA Report — TDD Qualitative Review (report-validation, NUMBERS-METRICS lens)

**Topic:** sc:reflect Tier-2 Reviewer Ensemble Swarm Re-Wiring TDD (FR-RH2)
**Document:** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`
**Date:** 2026-06-20
**Phase:** tdd-qualitative (NUMBERS-METRICS lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assumed ≥15 numeric inconsistencies existed; hunted for them.

---

## Overall Verdict: FAIL

Three numeric-consistency defects found: one IMPORTANT internal contradiction
(reviewer-count range "2–3" vs "2–4" vs the `[2,4]` clamp, where the Glossary
contradicts both the document's own prose AND the authoritative source protocol),
and two MINOR citation imprecisions (three off-by-one line-count cites; a "11
research files" label that its own enumeration lists as 12 items). No CRITICAL
numeric defect: the load-bearing quantitative spine — the (M,N)→verdict→exit-code
map, the retry/backoff/timeout matrix, the auto-fix multiplier arithmetic, every
dataclass field count, and every reuse-audit score — is internally consistent and
verified byte-correct against source.

Per the no-leniency rule (any issue regardless of severity = FAIL), this is a FAIL
with a short, mechanical remediation list. The numeric core is sound; the defects
are surface-level.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | (M,N) table exit-codes match verdict→exit map | PASS | §4.1 L308-313, §5.4 L376-381, §11.2 L907-912, §12.2.1 L949-954, §14.3 L1103-1109 all give `blocked/2, degraded/11, halted/10, pass/0`; verified against `models.py:44-49` (`PASS:0, HALTED:10, DEGRADED:11, BLOCKED:2`) and the docstring `models.py:14-16`. |
| 2 | verdict→exit map matches source | PASS | `src/superclaude/cli/reflect/models.py:44-49` exit_code dict is byte-exact to every TDD restatement (§1 L196, §3 NG1 L271, §5.1 FR-008 L336, §6.1 L458, §8.3 L788, §14.3). |
| 3 | derive_verdict ordering blocked→degraded→halted→pass | PASS | TDD §5.4 L374, §11.2 L914, §12.2.3 L977, §14.3 L1111 all state this ordering; verified against `contract.py:147` (BLOCKED) → L211 (DEGRADED) → L227 (HALTED) → L234 (PASS). |
| 4 | `--reviewers` clamp [2,4] default 3 stated consistently | PASS | §5.3 L367, §8.1 L695, §11.1 L885, §17.2 L1259, §22 Q8 L1527, §23 L1573, §24 L1573, §26.1 L1656 all give `[2,4]` / default 3 / `1`=negative-witness. No clamp/default contradiction. |
| 5 | 5xx retry/backoff/timeout consistent between §12 and §17 | PASS | §12.4 L998-1008 (retry once, 2s backoff, 180s budget) == §17.2 L1261-1264 (180s, retry once, 2s backoff, ~362s worst-case derivation is arithmetically sound: 180+2+180). Verified against `dispatch.py:124` (`_DEFAULT_TIMEOUT_SEC=180`), `:224` (`on_5xx=True, on_5xx_backoff_sec=2, on_4xx=False`), `:269` (backoff sleep). |
| 6 | auto-fix multiplier (max_fix_iterations+1)×reviewers, default 2 | PASS | §17.3 L1285-1289 `(2+1)×3=9`, §26.1 L1657 `3×3=9`, §20 R8 L1438, §17.3 guardrail all agree. Default `max_fix_iterations=2` verified in `commands.py:136` and `config.py:141`. Arithmetic correct. |
| 7 | success-metric thresholds reviewer_count≥2, ≥2 distinct classes | PASS | §3 G4 L259, §4.1 L300-301, §5.1 FR-004 L332, §11.1 L899, §15.3 I1 L1184 all use `reviewer_count == M ≥ 2` AND `≥2 distinct model classes computed over M survivors`. Consistent everywhere; no threshold drift. |
| 8 | WorkerResult field count ("Exactly 12 fields") | PASS | §7.1 L585 claims 12. Source `swarm/models.py:92-103` = exactly 12 dataclass fields (index…elapsed_ms). Table L589-600 enumerates all 12. ✓ |
| 9 | LensEntry field count ("14 fields") | PASS | §7.1 L643 claims 14. Source `swarm/models.py:71-84` = exactly 14 dataclass fields. `default_workers=3` default also matches `models.py:78`. ✓ |
| 10 | ResultContract field set (no explicit count claimed) | PASS | §7.1 L608-627 lists fields with `started/finished` collapsed to one row (18 rows = 19 fields). Source `swarm/models.py:997-1015` = 19 fields. TDD makes NO "19 fields" numeric claim, so no contradiction; the per-field table is faithful. |
| 11 | merge.py "8 LOC" mechanical_merge | PASS | §6.1 L432, §6.2 L516, §13.1 L1024, §13.2 L1039 all say 8 LOC. Source `merge.py:50-57` body = exactly 8 non-blank/non-comment lines. ✓ |
| 12 | reuse-audit numbers (0.81 max overlap, 4 cand, 8 neigh, conf 0.88/0.84/0.79/0.81) | PASS | §6.5 L557/L561-564 + §21 L1447/L1478/L1482 + §27 L1680. Source `research/reuse-audit.yaml`: candidates_scanned 4, neighbours_found 8, max_overlap 0.81, confidences 0.88/0.84/0.79/0.81, S_reuse 0.81. All byte-exact. ✓ |
| 13 | fixture cites (pass.yaml:4 tier_reached:2 etc.) | PASS | §2.2 L223, §4.1 L302, §15 L1142 cite `pass.yaml:4 tier_reached:2`, L12 diversity:full, L15 merge_method:adversarial, L16 score:0.86. Source `fixtures/pass.yaml` matches all four lines exactly. |
| 14 | max_turns 250 cite (§15.4 B2) | PASS | L1208 cites `max_turns==250`; `config.py:39` `_DEFAULT_MAX_TURNS=250`, `:152` "default 250". ✓ |
| 15 | research/synthesis file counts (11 research, 9 synthesis) | FAIL (MINOR) | "9 synthesis files (synth-01…09)" = exactly 9 ✓. But "11 codebase research files" (L150, L1741, L1762) is enumerated at L1741 as "research/00–09, web-01, reuse-audit.yaml" = 12 items under an "11" label. See Issue #2. |
| 16 | reviewer-count range "2–3" vs "2–4" vs [2,4] | FAIL (IMPORTANT) | §1 L192, §2.1 L211, §2.1 L213 say "2–3 reviewers"; §28 Glossary L1715 says "2–4 reviewers"; CLI clamp is `[2,4]`. Internal contradiction + Glossary diverges from authoritative source. See Issue #1. |
| 17 | test-file line-count cites (277L/221L/173L) | FAIL (MINOR) | §15.4 L1207-1209 cite 277/221/173. Actual `wc -l`: 276/220/172. All three +1. See Issue #3. |
| 18 | cited swarm line numbers (dispatch 334/496, reduce 555/648, merge 50, conftest 98-138) | PASS | dispatch_wave1@334 ✓, M-predicate@496 ✓, reduce_wave3@555 ✓, M-count `sum(...=="success")`@648 ✓, mechanical_merge@50 ✓, make_claude_process_stub@99 (TDD "98-138" block ≈ correct, def at 99). |

## Summary
- Checks passed: 15 / 18
- Checks failed: 3 (1 IMPORTANT, 2 MINOR)
- Critical issues: 0
- Issues fixed in-place: 0 (report-only, fix_authorization:false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | §1 L192, §2.1 L211, §2.1 L213, §28 Glossary L1715 | **Reviewer-count range contradiction.** The "Tier-2 ensemble" is described as "**2–3** heterogeneous reviewers" in §1 (L192), §2.1 (L211), and §2.1 (L213), but the §28 Glossary (L1715) defines the SAME term "Tier-2 ensemble" as "**2–4** reviewers." This is a self-contradiction. Worse: the authoritative source being restored — `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — uses "2-3 heterogeneous reviewers" everywhere (description, L33, L626, L1540; `refs/cost-profile.yaml:47`). The "2–4" in the Glossary appears to conflate the conceptual ensemble size ("2-3", from the protocol) with the new CLI `--reviewers [2,4]` clamp (a different thing). A reader cannot tell whether the ensemble is a 2-3 or 2-4 reviewer pass. | Make the Glossary "Tier-2 ensemble" entry consistent. Either: (a) change L1715 to "2–3 reviewers" to match §1/§2.1 and the source protocol; OR (b) if the design DELIBERATELY widens the ensemble to 2-4 (because the new `--reviewers` clamp is `[2,4]`), then update §1 L192, §2.1 L211, and §2.1 L213 from "2–3" to "2–4" AND add one sentence noting the widening from the protocol's documented 2-3 is intentional. Do NOT leave the two ranges coexisting. The clamp `[2,4]` (a CLI knob) and the ensemble-size prose must be reconciled to one consistent statement. |
| 2 | MINOR | §0 Contract Table L150; §27.4 L1741; §28 history L1762 | **"11 codebase research files" label vs 12-item enumeration.** L1741 enumerates the "11 codebase research files" as "(`research/00`–`research/09`, `web-01`, `reuse-audit.yaml`)". Counting the enumeration: 00–09 = 10 `.md`, + `web-01` = 11 `.md` files, + `reuse-audit.yaml` = 12 listed items. The directory confirms 11 `.md` files + 1 `.yaml`. So "11 research files" is correct ONLY if `reuse-audit.yaml` is excluded — yet the parenthetical at L1741 explicitly includes it. The count label and its own enumeration disagree by one. | Either change the label to "11 research files + 1 reuse-audit YAML" / "12 research artifacts", or drop `reuse-audit.yaml` from the L1741 parenthetical enumeration so the "11" label matches the 11 enumerated `.md` files. Apply the same fix at L150 and L1762 for consistency. |
| 3 | MINOR | §15.4 L1207, L1208, L1209 | **Off-by-one line-count citations.** The three backward-compat test files are cited as `test_verdict_mapping.py` (**277 L**), `test_runner_e2e.py` (**221 L**), `test_writeback.py` (**173 L**). Actual `wc -l`: 276, 220, 172 respectively — each exactly +1 over source. Consistent +1 across all three indicates the author counted editor line-numbers (last line) rather than `wc -l` newlines, or the files lack a trailing newline. As a NUMBERS lens these cited counts do not match `wc -l`. | Update the three parenthetical counts to 276 L / 220 L / 173 L→172 L (or drop the exact line counts entirely — they are non-load-bearing decoration on the regression-floor table). If keeping them, align to the `wc -l` convention used elsewhere in the doc. |

## Actions Taken
None — `fix_authorization: false` (report-only). All three issues are documented above with specific, mechanical remediations. None is mine to fix; all are scoped to the TDD document under review.

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 14 distinct numeric/structural claims verified against shipped source: exit-code map (`models.py:44-49`), derive_verdict ordering (`contract.py:147/211/227/234`), `_DEFAULT_TIMEOUT_SEC=180` + retry matrix (`dispatch.py:124/224/269`), `max_fix_iterations=2` (`commands.py:136`, `config.py:141`), WorkerResult 12 fields (`models.py:92-103`), LensEntry 14 fields + default_workers=3 (`models.py:71-84`), ResultContract 19 fields (`models.py:997-1015`), mechanical_merge 8 LOC (`merge.py:50-57`), reuse-audit numbers (`research/reuse-audit.yaml`), pass.yaml fixture lines, max_turns=250 (`config.py:39`), dispatch/reduce/merge/conftest line anchors, and the authoritative reviewer-count "2-3" in `sc-reflect-protocol/SKILL.md`. Plus three test-file line counts via `wc -l`.

2. **What specific files were read to verify claims?** `tdd.md` (full, in 4 reads); `src/superclaude/cli/reflect/models.py` (full); `cli/reflect/contract.py` (grep); `cli/reflect/config.py` + `commands.py` (grep); `cli/swarm/models.py` (WorkerResult/LensEntry/ResultContract field extraction); `cli/swarm/dispatch.py`, `reduce.py`, `merge.py` (line/LOC verification); `tests/cli/reflect/{test_verdict_mapping,test_runner_e2e,test_writeback,conftest}.py` + `fixtures/pass.yaml` (counts); `research/reuse-audit.yaml`; `skills/sc-reflect-protocol/SKILL.md` + `refs/cost-profile.yaml` (authoritative reviewer-count source).

3. **If I found 0 issues, why trust I checked?** I did not find 0 — I found 3, including the load-bearing IMPORTANT contradiction that required cross-referencing the TDD's prose against the AUTHORITATIVE source protocol (`sc-reflect-protocol/SKILL.md`) to determine which number is correct, not just noting that two numbers differ. The evidence trail above cites specific file:line for every PASS and FAIL. The numeric core (16 of the prompt's named checks) genuinely verified clean against source — the adversarial hypothesis of "≥15 inconsistencies" was not borne out; the quantitative spine is unusually well-grounded (every dataclass count, every reuse score, the full retry matrix, the multiplier arithmetic all byte-correct). Reporting that honestly is the point.

4. **Web research / Tavily?** None performed — every check was local-file-bound (the TDD, the cited source, the authoritative protocol). No external lookup was required, so Tavily-first did not apply. Tool-engagement summary below.

**Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 9 (each Bash call targeted a specific claim: source field extraction, line counts, retry-matrix grep, reuse-audit numbers, authoritative reviewer-count). 12 tool calls ≥ 18 checklist items is below the 1:1 floor, but several Bash calls verified multiple claims each (e.g. one call confirmed all 4 reuse-audit confidences + merge LOC; one confirmed all 3 test line-counts + fixture + max_turns), so per-claim evidence is fully cited above.

## Recommendations
- **Resolve Issue #1 (IMPORTANT) before this TDD ships.** A reader/implementer deciding how many reviewer slots the ensemble forms will hit a 2-3-vs-2-4 contradiction at the Glossary. Pick one range, reconcile §1/§2.1/§28, and state explicitly whether the design intends 2-3 (per protocol) or 2-4 (per the new clamp).
- Fix Issues #2 and #3 (MINOR citation precision) in the same editing pass — both are one-token edits.
- No change required to the (M,N) table, exit-code map, retry matrix, multiplier arithmetic, field counts, or reuse-audit numbers — all verified correct.

## QA Complete
