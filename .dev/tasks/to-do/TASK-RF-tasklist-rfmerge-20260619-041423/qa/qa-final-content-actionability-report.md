# QA Report — doc-qualitative (Final Actionability / Determinism Lens)

**Topic:** RFMerger P1–P5 — COMPLETE build, final-state determinism + actionability over the assembled generator
**Date:** 2026-06-19
**Phase:** doc-qualitative (Final actionability / determinism lens; adversarial)
**Fix cycle:** N/A (report-only; `fix_authorization: false`)
**Target under review:** `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1764 lines)
**Cross-phase summary read:** `.dev/tasks/.../phase-outputs/reports/final-cross-phase-summary.md`

---

## Overall Verdict: FAIL

12 issues found (0 CRITICAL, 7 IMPORTANT, 5 MINOR). Per the doc-qualitative rule, ANY issue → FAIL. None block the four core determinism guarantees in their *intended* form, but several introduce dangling/contradictory references and one ambiguity that a generator agent would have to resolve by interpretation — which is exactly what the determinism lens forbids.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Determinism: same roadmap → same scored tiers | PASS | §5.3 pure-function fence (L581) + P5 advisory read-only fence (L883, L901) verified — scored-tier compute path never reads feedback-log/advisory. |
| 2 | Determinism: same roadmap → same P1 `## Execution Context` block | PASS-with-caveat | §4.1d emission rule (L228-249) is a pure function of roadmap text; form-selection table is exhaustive + mutually exclusive. See Issue 7 (extraction-predicate ambiguity). |
| 3 | Determinism: same gate → same P4 gate-results.txt | PASS-with-caveat | §Gate-Results (L1262-1269) pins description + offender strings deterministically. See Issue 4 (PASS/FAIL line-format inconsistency). |
| 4 | Determinism: same (roadmap, feedback-log) → same P5 advisory | PASS | §P5 advisory (L885-901): per-(Task ID, Override Tier) row, ascending order, Observed-count = row-count. Byte-deterministic for fixed feedback-log. |
| 5 | P4 emit format executable without interpretation | FAIL | Issue 4 (line-format), Issue 1 (Section 3.1 dangling ref reachable from gate path). |
| 6 | P1 emission rule executable without interpretation | FAIL | Issue 7 (Source-areas extraction predicate is partly discretionary). |
| 7 | P3 merge step executable without interpretation | PASS | Stage-7 1a (L1379-1388) + branch (L1406-1411) fully specified. |
| 8 | P2 loop executable without interpretation | FAIL | Issue 2 (worked-example arithmetic is self-contradictory → mis-teaches the guard). |
| 9 | P5 advisory executable without interpretation | PASS | §P5 (L885-901). |
| 10 | No discretionary/ambiguous prose introduced | FAIL | Issues 5, 6, 7, 9 (interpretation-required phrasings). |
| 11 | Cross-reference accuracy | FAIL | Issues 1, 3, 8 (dangling §3.1 ref, stale Stage-8 first-create claim, "this skill" self-ref). |
| 12 | Internal numeric/stage consistency | FAIL | Issue 8 (Stage-8 dir-creation claim contradicts §Gate-Results), Issue 11 (11-stages count vs reflect-post stage). |

## Summary
- Checks passed: 4 / 12 (PASS), 2 PASS-with-caveat, 6 FAIL
- Critical issues: 0
- Important issues: 7
- Minor issues: 5
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | L722 | **Dangling cross-reference `<computed per Section 3.1>`.** The index Metadata table tells the generator to compute `TASKLIST_ROOT` "per Section 3.1". No `Section 3.1` / `### 3.1` heading exists in the file — the actual algorithm lives under `### Tasklist Root (deterministic)` (L77-86). A generator agent following the table literally has no §3.1 to resolve. This is the determinism-killing case: the value (TASKLIST_ROOT) is the most determinism-load-bearing token in the whole bundle, and its authoritative pointer is broken. | Change `<computed per Section 3.1>` to reference the actual heading, e.g. "per `### Tasklist Root (deterministic)` above" or add the missing §3.1 anchor. |
| 2 | IMPORTANT | L1568-1572 | **P2 loop-state worked example is self-contradictory** and mis-teaches the monotonicity guard. Pass 1 row: `\|F_k\|=2` (two FAILING items) but PASS-set = `T01.01, T02.03` — the *same two task IDs* are simultaneously the failing-set-of-2 and the PASS-set. Pass 2 PASS-set = `T01.01, T02.03, T05.09`. An item cannot be both in `F_k` and the PASS-set in the same pass. The example a generator/reader uses to calibrate `\|F_k\|` vs PASS-set is internally inconsistent, so the very ordering it illustrates (`regression → monotonicity`) is demonstrated on contradictory data. | Rewrite the example so the PASS-set and `F_k` are disjoint per pass (e.g. pass 1: `\|F_1\|=2`, FAIL = `T03.04, T05.09`, PASS = `T01.01, T02.03`; pass 2: `\|F_2\|=1`, the previously-failing T03.04 now PASS). |
| 3 | IMPORTANT | L1512 vs L1262 | **Contradictory "who first creates `validation/`" claim.** §Gate-Results (L1262) states the gate-results artifact "moves its creation earlier" and creates `validation/` at Stage 6. But the Stage-8 gate (L1512) says the directory "already exists from Stage 6 (the gate-results artifact creates it earlier)" — consistent there — yet L1262 *also* parenthetically says "today that directory is **first created at Stage 8**". After the edit, Stage 6 is the first creator, so the L1262 "first created at Stage 8" clause is now stale/false and contradicts its own surrounding sentence. A generator reading L1262 sees both "Stage 8 first-creates it" and "I create it at Stage 6 now". | Delete/rephrase the "(today that directory is first created at Stage 8...)" parenthetical so the single source of truth is "Stage 6 (gate-results) creates `validation/` first; Stage 8 `mkdir -p` is an idempotent no-op." |
| 4 | IMPORTANT | L1262 | **P4 gate-results line-format under-specifies the PASS line, breaking byte-reproducibility.** The format pins PASS lines to `CHECK <n> PASS: <check description>` and FAIL lines to `CHECK <n> FAIL: <offending task/file>` — but L1266 then says for PASS lines use "the verbatim leading clause … up to the first colon for table-row checks (13-20), or the first sentence's leading clause for prose checks (1-12)." Checks 1-12 are prose with NO colon and variable leading-clause boundaries ("first sentence's leading clause" is not a deterministic tokenizer — where does a "leading clause" end in check 9 "Every task in every phase file has non-empty values for: Effort, …"?). Two readers will serialize different bytes for the same passing gate → violates the stated "same gate → same bytes" guarantee. | Pin each of the 20 checks to an explicit, frozen description string (a literal table mapping check# → exact string) rather than a "leading clause" extraction rule, OR define a deterministic boundary (e.g., "text up to first colon; if no colon, the full check title line verbatim"). |
| 5 | IMPORTANT | L1266 | **"first sentence's leading clause" is discretionary extraction prose** (same root as Issue 4). The determinism lens explicitly bans undefined extraction predicates; "leading clause" has no pinned delimiter for the 12 prose checks. | As Issue 4 — replace with a frozen per-check string table or an exact delimiter rule. |
| 6 | IMPORTANT | L236 | **P1 Source-areas extraction predicate is partially discretionary.** Rule: list "only literal noun phrases the roadmap explicitly tags as a module/subsystem/component (e.g. a backticked name or an explicit `module:`/`component:` label) — never a file path. Do not classify free prose." The "e.g." makes the trigger set open-ended: is a backticked name that is actually a function (`rateLimit()`) a "module"? The rule says "do not classify free prose" but a backticked token is not self-evidently a module vs a function vs a variable. Two generators will disagree on which backticked tokens qualify → non-deterministic `Source areas:` content. | Pin an exhaustive, closed trigger set: e.g. "a token matched by an explicit `module:`/`component:`/`subsystem:` label, OR a backticked token whose immediately-preceding word is one of {module, component, subsystem, service}; nothing else qualifies." |
| 7 | IMPORTANT | L234, L236, L238 | **P1 resolve/extraction predicates lean on undefined existence-gate reuse.** L234 says a roadmap ref "resolves iff non-None after the existence check — reusing the same resolve/None existence-gate semantics applied to auto-wired inputs in 4.1c". But §4.1c's existence gate is a *filesystem* check (`os.path.exists` on a TDD/PRD path). A `R-###` roadmap ref is not a filesystem path — there is no "file" to existence-check. The reused predicate is type-mismatched; "resolves iff present in the task's roadmap-derived metadata" (the parenthetical) is the real rule, and the "existence-check / None gate from 4.1c" framing is a misleading borrow that a literal implementer cannot apply. | Drop the §4.1c existence-gate analogy; state directly: "a `R-###` ref resolves iff it appears in the task's `Roadmap Item IDs` metadata field (non-empty); absent → does not resolve." |
| 8 | MINOR | L1658 | **"11 stages" count is ambiguous vs the per-phase post-reflect task.** The Stage Completion Contract enumerates Stages 1–10.5 (11 entries counting 10.5). The reflect-POST gate (L1111-1168) is a *templated terminal task inside each phase file*, not a generator stage — correct — but a reader counting "11 stages" then finding a "reflect-post/" output dir (L99, L135) and a POST gate may conflate them. | Add one clause to L1658: "(the per-phase post-execution reflection is an executed task templated into each phase file, NOT a generator stage)." |
| 9 | MINOR | L962 | **"a divergence is a halt condition" is an unactionable assertion in generator prose.** The Execution Context block says introducing a second incompatible meaning of "Execution Context" "is a halt condition" — but the generator has no halt mechanism defined for this; it is a design constraint on the author, not a runtime check the generator executes. Reads as a runtime gate that doesn't exist. | Reword to "MUST NOT" design constraint, or wire it to an actual Self-Check item if a runtime guard is intended. |
| 10 | MINOR | L962 | **"this skill MUST NOT introduce" self-reference** — minor, but "this skill" appears in deterministic generator prose where every other rule addresses the generator imperatively. Cosmetic consistency only. | Optional: rephrase to imperative ("Do NOT introduce a second meaning of Execution Context"). |
| 11 | MINOR | L1672 / L1690 | **Stage 10.5 is in the dependency chain and TaskCreate list but the "11 stages" sentence + the 11 `TaskCreate` calls (L1697-1707) enumerate exactly 11 task entries including 10.5** — consistent count, BUT the prose "11 stages" while IDs run 1,2,3,4,5,6,7,8,9,10,10.5 invites an off-by-one read (a reader expects stage "11"). | Optional: say "11 stage entries (1–10 plus 10.5)". |
| 12 | MINOR | L1410 | **"report the validation error / halts" zero-success terminal is under-pinned.** The all-agents-fail branch routes to "the generator's existing report-validation-error terminal" and explicitly says no `StageError` symbol exists. The behavior ("do not return a clean bundle") is clear, but "the generator's existing … terminal" implies a concrete mechanism that the same sentence admits is unimplemented — a forward-looking reference dressed as an existing one. | Reword to "report the validation error and do not return a clean bundle (no typed-error symbol is required by this prose)." |

## Determinism Guarantee Audit (the 4 core claims)

| Claim | Verdict | Note |
|-------|---------|------|
| same roadmap → same scored tiers | **HOLDS** | §5.3 fence (L581) + advisory read-only fence (L883/L901) are airtight: compute path provably never reads feedback-log. Strongest part of the build. |
| same roadmap → same P1 Execution Context block | **HOLDS in intent, leaky in spec** | Form-selection table (L242-247) is exhaustive/mutually-exclusive ✓. BUT `Source areas:` extraction (Issue 6) and the resolve predicate (Issue 7) admit reader disagreement. Same roadmap *could* yield different `Source areas:` across conforming implementations. |
| same gate → same P4 gate-results.txt | **HOLDS for FAIL offenders, LEAKY for PASS descriptions** | Offender ordering pinned ✓ (Issue resolved by L1267 ascending sort). PASS-line description extraction is non-deterministic for the 12 prose checks (Issues 4, 5). |
| same (roadmap, feedback-log) → same P5 advisory | **HOLDS** | Per-(Task ID, Override Tier) rows, ascending sort, Observed-count = row count, <2 → omit whole section. Byte-deterministic. |

Net: 2 of 4 guarantees are airtight; 2 (P1 Source-areas, P4 PASS-line descriptions) have specification leaks that permit non-determinism across conforming implementations. These are the load-bearing failures for this lens.

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source?** 12 — every issue cites a verified line number in the actual SKILL.md (re-read full file L1-1764 across two reads + targeted greps). Verified: §3.1 absence (grep returned only L142 `### 3.x` and L722 the dangling ref); "17" residue (grep confirmed L1253 is check-17 the bar-format check, NOT a stale 17-check count — correctly migrated to 20); discretionary-prose grep (only L998 "if applicable" — benign, in optional Notes).
2. **What specific files did I read?** `SKILL.md` (full, 1764 lines, two paginated Reads) and `final-cross-phase-summary.md` (full). Grep sweeps for `Section 3.1`, `\b17\b`, discretionary phrases, stage-count, date-determinism.
3. **If I found issues, why trust the check was thorough?** I traced each of the 4 named determinism guarantees to its specific fencing prose and tested each for an interpretation gap (form tables, extraction predicates, sort keys). The two HOLDS verdicts (scored tiers, P5 advisory) were stress-tested for a feedback-back-channel and found genuinely closed. The two leaks (Source-areas, PASS-line) were each reproduced as "two conforming readers diverge" scenarios.
4. **Web research?** None required — review is entirely local-file-bound. No Tavily/WebSearch invoked.

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 3 | Grep: 3 | Glob: 0 | Bash: 3 (grep batches)

## Recommendations
- Fix Issues 1, 3 (dangling/contradictory cross-refs) and Issues 4–7 (the two true determinism leaks: P4 PASS-line description extraction + P1 Source-areas/resolve predicates) BEFORE this build is considered actionable. These four are the only ones that materially threaten "same input → same output".
- Issues 2, 8–12 are correctness/clarity hygiene; resolve in the same pass.
- The scored-tier fence and P5 advisory fence are exemplary — leave untouched.

## QA Complete
