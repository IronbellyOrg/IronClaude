# QA Report — Source-Document Fidelity (Agent 2)

**Topic:** FR-RH2 sc:reflect Tier-2 swarm ensemble — TDD vs SPEC fidelity
**Date:** 2026-06-20
**Phase:** report-validation (source-document fidelity)
**Fix cycle:** N/A (`fix_authorization: false` — report-only)
**Agent:** rf-qa source-document FIDELITY agent 2 (ADVERSARIAL stance)

**Sources of truth verified against:**
- SPEC `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` — §6 NFRs (NFR-RH2.1–2.8), §5.3 (M,N) divergence contract, §11 Open Items (OI-1–OI-4)
- TDD `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` — full assembled document (1774 lines)

---

## Overall Verdict: PASS

No dropped NFRs, no altered (M,N) values, and no missing Open Items were found. Every adversarial hunt target came back clean against tool-verified evidence. Three NON-BLOCKING observations are recorded under Issues Found (all MINOR; none are fidelity violations — they are fidelity *strengthenings* the TDD made explicit relative to the spec, plus one self-consistency note).

---

## Verification Dimension 1 — Semantic Coverage (NFRs + Open Items)

### NFR-RH2.1–2.8 → TDD §5.2 (NFR-001..NFR-008), 1:1 mapping

| Spec NFR | Spec requirement (semantic) | TDD location | TDD source-tag | Verdict |
|----------|------------------------------|--------------|----------------|---------|
| NFR-RH2.1 | No in-process Task/Agent fan-out (NFR-7 preserved); guard extended to `ensemble.py` | §5.2 NFR-001 (L350) | `NFR-RH2.1` | PASS — semantics preserved; explicitly extends guard to `ensemble.py` |
| NFR-RH2.2 | Thinness/isolation (NFR-1); no sprint/roadmap import, no async, no raw subprocess | §5.2 NFR-002 (L351) | `NFR-RH2.2` | PASS — all three anchors transcribed |
| NFR-RH2.3 | Non-vacuous proof (positive ≥2 + falsifying 1, both real path) | §5.2 NFR-003 (L352) | `NFR-RH2.3` | PASS |
| NFR-RH2.4 | Credit-free CI — zero network I/O via `--transport stub` | §5.2 NFR-004 (L353) | `NFR-RH2.4` | PASS |
| NFR-RH2.5 | Model-class diversity `full` when pool ≥ reviewers; over M survivors | §5.2 NFR-005 (L354) | `NFR-RH2.5` | PASS — "over distinct model_ids of M succeeded workers" preserved |
| NFR-RH2.6 | Backward compatibility — existing reflect tests pass unchanged | §5.2 NFR-006 (L355) | `NFR-RH2.6` | PASS |
| NFR-RH2.7 | Observability — `--detached`/tmux + `done.json` + `--tui` | §5.2 NFR-007 (L356) | `NFR-RH2.7` | PASS |
| NFR-RH2.8 | Proxy contract — only `:4000/cli` + `T2Model01..NN`; no `:4000/v1`/`:8317` | §5.2 NFR-008 (L357) | `NFR-RH2.8` | PASS — verbatim, with `read_env` measurement method |

All 8 NFRs are addressed with a 1:1 source-tag, an explicit measurement method, and the spec's target semantics preserved. The TDD's L359 self-assertion ("All 8 NFRs carry a NFR-RH2.N source… No `[NO SPEC TRACE]` gaps") is independently confirmed by reading each row.

### OI-1..OI-4 → TDD §22 Q1..Q4

| Spec Open Item | Spec question (semantic) | TDD §22 row | BLOCKING? | Verdict |
|----------------|---------------------------|-------------|-----------|---------|
| OI-1 (BLOCKING GATE) | Does swarm contract emit `reviewer_count`/`merge_method`/`t2_model_class_diversity` in the shape `derive_verdict` reads, or must `ensemble.py` map them? Produce correspondence table. | Q1 (L1526), titled **"Q1 (OI-1, BLOCKING GATE)"**, "Resolve BEFORE any FR-RH2.3 code lands" | YES — preserved | PASS — OI-1 carried as Q1 AND marked BLOCKING in the row title, the §5.1 note (L342), §23 (L1543 "must close before Milestone M3"), §24 DoD (L1605/L1613), and the §22 blocking note (L1535) |
| OI-2 | Exact NFR-7 amendment text — confirm vs amend | Q2 (L1527) | (spec: Medium, not blocking) | PASS |
| OI-3 | `--transport stub` auto-select in CI vs opt-in | Q3 (L1528) | (spec: Low) | PASS |
| OI-4 | `/sc:adversarial` Mode A treatment of `suspect:true` reflect-review vs bare-review | Q4 (L1529) | (spec: Low-Medium) | PASS |

All 4 Open Items present as §22 Q1–Q4 with the spec's exact questions. **OI-1/Q1 is marked BLOCKING in five independent places** — over-satisfied, not just met. (Q5–Q8 are additive research-derived items, not spec Open Items; their presence does not violate fidelity — see Observation O-3.)

---

## Verification Dimension 2 — Detail Preservation: the (M,N) divergence contract

### (M,N) guard table — values verified EXACTLY against spec §5.3 `mn_guard_table` (L447-451)

The spec defines four rows; each `(condition → verdict / exit / slug)` triple was checked byte-for-byte against every TDD reproduction.

| Spec §5.3 row | verdict | exit | slug | TDD reproductions checked | Verdict |
|---------------|---------|------|------|----------------------------|---------|
| `M==0` (all failed / no artifacts) | `blocked` | `2` | `ensemble-empty` | §4.1 (L311), §5.4 (L379), §12.2.1 (L952), §14.3 (L1109), §25.1 (L1635) — all `blocked`/`2`/`ensemble-empty` | PASS — identical in all 5 |
| `M==1` (≥N−1 failed, or `--reviewers 1`) | `degraded` | `11` | `single-reviewer-fallback` | §4.1 (L312), §5.4 (L380), §12.2.1 (L953), §14.3 (L1107) — all `degraded`/`11`/`single-reviewer-fallback` | PASS |
| `M≥2` but `<2` distinct classes | `degraded` | `11` | `degraded-model-diversity` | §4.1 (L313), §5.4 (L381), §12.2.1 (L954), §14.3 (L1108) — all `degraded`/`11`/`degraded-model-diversity` | PASS |
| `M≥2` AND `≥2` distinct classes | `pass-eligible` | `0` | `pass` | §4.1 (L314), §5.4 (L382), §12.2.1 (L955), §14.3 (L1106) — all `pass-eligible`/`0`/`pass` | PASS |

**Adversarial value-drift sweep (Bash grep across all 1774 lines):**
- Exit codes only ever appear as the contracted set `{0, 2, 10, 11}` mapped to `{pass, blocked, halted, degraded}`. No stray exit value (e.g. `1`, `3`) is attached to any (M,N) outcome.
- Slug token counts: `single-reviewer-fallback` ×40, `degraded-model-diversity` ×16, `ensemble-empty` ×14, `pass-eligible` ×7 — every occurrence carries the spec-correct verdict/exit pairing where co-located. No mutated slug spelling found.
- M-condition tokens (`M==0`, `M==1`, `M≥2`/`M>=2`, `M==2`) are used consistently with the spec's boundary semantics in every section; no row inverts a boundary (e.g. no `M==1 → blocked` or `M==0 → degraded`).

### Verdict-ordering preservation

Spec §5.3 / FR-RH2.9 require `derive_verdict` ordering `blocked → degraded → halted → pass`, with M==0 `blocked` ordered AHEAD of degraded. TDD preserves this at §5.4 (L375), §12.2.3 (L978), §14.3 (L1112), and §13.1 (L1027). PASS.

### Worker-status → M mapping — verified EXACTLY against spec §5.3 `worker_status_to_m` (L453-458)

| Spec status | Spec rule | TDD §12.2.2 (L963-968) | TDD §4.1/§5.4 echo | Verdict |
|-------------|-----------|-------------------------|---------------------|---------|
| `success` | counts toward M | "counts toward M" (L965) | L301, L384 | PASS |
| `proxy_error` | does NOT count (retry-once-then-drop) | "does NOT count… retry-once-then-drop (5xx only)" (L966) | L301, L384 | PASS |
| `timeout` | does NOT count | "does NOT count… no retry" (L967) | L301, L384 | PASS |
| `parse_error` | does NOT count (salvage may promote; post-salvage status governs) | "does NOT count. Salvage may promote `parse_error → success`… post-salvage status governs M" (L968) | L384 | PASS |

The spec's nuance — `parse_error` salvage promotion and "post-salvage status governs" — survives verbatim into the TDD. `M = sum(1 for w in worker_results if w.status == "success")` is grounded to `reduce.py:648` (TDD L948/L961), a detail-preserving elaboration that does not alter the contract. PASS.

---

## Verification Dimension 3 — Operational / Compliance Completeness

### Proxy-contract NFR (NFR-RH2.8) has corresponding TDD items

The spec's NFR-RH2.8 (`:4000/cli` base + `T2Model01..NN`; no `:4000/v1`/`:8317` probing) is not a single isolated mention — it is wired into multiple actionable TDD surfaces:

| TDD surface | Line | Actionable content |
|-------------|------|--------------------|
| §5.2 NFR-008 (the NFR row itself) | L357 | Target + `read_env` preflight measurement method (`openai_compat.py:159`); "assert no `:4000/v1`/`:8317` probe" |
| §6.x architecture (external boundary) | L534, L538, L540 | `T2Model0N` proxy boundary; `read_env` raises `TransportEnvError`; no literal `:4000`/`:8317`/`/v1`/`/cli` in transport code `[CODE-VERIFIED]` |
| §13.1 threat model | L1023 | Rogue-endpoint threat → "proxy contract by construction" mitigation |
| §13.2 security control | L1036 | Env-contract preflight control + verification |
| §15 testing | L1238 | `read_env` preflight unit test + proxy-endpoint grep audit |
| §18 dependencies | L1321, L1343 | `T2Model0N` proxy + `~/.aienv` env-file as named dependencies with the contract restated |
| §25.1 runbook | L1635-1636 | "do NOT probe `:4000/v1` or `:8317`" operational guidance |
| §28 glossary | L1726 | `T2Model0N` defined with the `:4000/cli`-only / no-`:4000/v1`/`:8317` constraint |

The proxy contract is the most thoroughly operationalized NFR in the TDD. PASS.

### NFR-7 reconciliation has a corresponding TDD item

The spec calls for explicit NFR-7 reconciliation (FR-RH2.8 + spec §9 + OI-2). The TDD provides:

| TDD surface | Line | Content |
|-------------|------|---------|
| §5.1 FR-009 | L338 | FR-RH2.8 re-projection; **correctly notes the amendment is recorded in SPEC §9, not TDD §9** (TDD §9 = State Management, N/A) — this is a precise, non-drifting cross-doc reference |
| §19.6 (dedicated subsection) | L1412-1429 | "NFR-7 Reconciliation — recorded as a migration concern"; resolves to **CONFIRM-with-scope-extension**; gives the recorded amendment text verbatim, the guard mechanics (`_ENSEMBLE_SRC`, `_NO_NEST_SRCS`, loop Layer-B over both modules), AND the subtle correctness point that the raw-subprocess ban stays scoped to `{runner.py, ensemble.py}` to avoid false-failing the sanctioned `--tmux` `subprocess.run` in `reflect/commands.py:320` |
| §20 R3/R9 | L1439, L1445 | NFR-7 guard-scope risk + the pass-by-accident risk if Layer B never anchors on `ensemble.py` |
| §22 Q2 | L1527 | OI-2 carried; confirm-vs-amend, cross-ref R3/R9 and §19.6 |
| §13.2 security control | L1043 | No-nesting guarantee as a security control |

The reconciliation is not only present but more rigorous than the spec required — it pre-decides CONFIRM-with-scope-extension, drafts the amendment text, and catches the tmux-subprocess scoping subtlety the spec did not enumerate. PASS.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | NFR-RH2.1–2.8 each addressed in TDD §5.2 (read descriptions) | PASS | §5.2 L350-357; each row 1:1 source-tagged to NFR-RH2.N with measurement method; semantics read and matched |
| 2 | NFR target semantics preserved (not just IDs present) | PASS | Read each NFR description in spec §6 and TDD §5.2; diversity-over-M, zero-network-IO, proxy-only-`:4000/cli` all preserved |
| 3 | OI-1..OI-4 present as §22 Q1..Q4 | PASS | §22 L1526-1529; spec questions transcribed |
| 4 | OI-1/Q1 marked BLOCKING | PASS | Row title "Q1 (OI-1, BLOCKING GATE)" L1526 + 4 corroborating refs (L342, L1535, L1543, L1605/1613) |
| 5 | (M,N) M==0 → blocked/exit2/ensemble-empty | PASS | §4.1 L311, §5.4 L379, §12.2.1 L952, §14.3 L1109 — all identical |
| 6 | (M,N) M==1 → degraded/exit11/single-reviewer-fallback | PASS | §4.1 L312, §5.4 L380, §12.2.1 L953, §14.3 L1107 |
| 7 | (M,N) M≥2 but <2 classes → degraded/exit11/degraded-model-diversity | PASS | §4.1 L313, §5.4 L381, §12.2.1 L954, §14.3 L1108 |
| 8 | (M,N) M≥2 ∧ ≥2 classes → pass-eligible/exit0 | PASS | §4.1 L314, §5.4 L382, §12.2.1 L955, §14.3 L1106 |
| 9 | Verdict ordering blocked→degraded→halted→pass preserved | PASS | §5.4 L375, §12.2.3 L978, §14.3 L1112 |
| 10 | Worker-status→M mapping (success counts; proxy_error/timeout/parse_error don't) | PASS | §12.2.2 L963-968; spec §5.3 L453-458; parse_error salvage nuance preserved |
| 11 | No altered (M,N) values / mutated slugs / stray exit codes anywhere | PASS | Bash grep sweep across 1774 lines: exit set = {0,2,10,11} only; slug spellings intact (40/16/14/7 counts); no inverted boundary |
| 12 | Proxy-contract NFR (NFR-RH2.8) has corresponding TDD item(s) | PASS | 8 surfaces: §5.2 L357, §6 L534/538/540, §13 L1023/1036, §15 L1238, §18 L1321/1343, §25.1 L1635, §28 L1726 |
| 13 | NFR-7 reconciliation has corresponding TDD item | PASS | Dedicated §19.6 L1412-1429 + FR-009 L338 + §20 R3/R9 + §22 Q2 |
| 14 | No dropped NFR (adversarial: all 8 accounted, none silently omitted) | PASS | Full §5.2 read; L359 self-assertion independently confirmed |
| 15 | No missing Open Item (adversarial: all 4 spec OIs present) | PASS | §22 read in full; OI-1..4 = Q1..4; extras Q5-Q8 additive |

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; `fix_authorization: false`)

## Issues Found

No fidelity violations. Three MINOR non-blocking observations (none alter the verdict):

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| O-1 | MINOR | TDD §5.1 L326-340 (FR mapping note) | The spec sequences FR-RH2.9 immediately after FR-RH2.4; the TDD re-projects to numeric FR-001..009 with FR-005↔FR-RH2.9 (offset). This is **documented explicitly** in the L326 mapping note and the L340 spec-trace summary, so it is NOT drift — every FR still maps to exactly one spec FR. Noted only so a downstream reader does not mistake the numeric offset for a dropped requirement. | None required — the offset is correctly disclosed. Optional: keep the L326 note prominent in any future edit. |
| O-2 | MINOR | TDD §14.3 L1107 / §12.2.1 L953 | The TDD introduces `degraded-tier1` as an additional slug for the `tier_reached==1` sub-case of M==1, alongside the spec's `single-reviewer-fallback`. This is an *additive* grounding against `contract.py:263-264` (Trigger 6), consistent with the spec's "and/or `tier_reached:1`" language (spec §5.3 L449, FR-RH2.9 L254). Not a value alteration — the spec slug `single-reviewer-fallback` is still the primary, and both still route degraded/exit11. | None required — additive detail consistent with spec. |
| O-3 | MINOR | TDD §22 Q5-Q8 (L1530-1533) | Four research-derived open questions beyond the spec's OI-1..4. These are NOT spec Open Items and do not displace any. They surface real `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]` findings (e.g. `ensemble-empty` slug absent from `contract.py` today — Q6; `--suspect-source` unparsed — Q5). Additive rigor, not a fidelity defect. | None required. Q6 in particular is a valuable flag that the `ensemble-empty` slug is spec-supplied vocabulary not yet in code — correctly disclosed at §14.4 L1124. |

## Actions Taken

None — `fix_authorization: false`. All findings documented above for the orchestrator.

## Recommendations

- Proceed. The TDD is a faithful, often-strengthened projection of the spec's NFRs, (M,N) contract, and Open Items.
- Carry O-3/Q6 forward to implementation: the literal `ensemble-empty` string does not exist in `contract.py` today (TDD §14.4 L1124, §22 Q6 L1531). The TDD already flags this as a reconciliation decision (Option A vs B); ensure the chosen option is recorded before FR-RH2.9 wiring, per the TDD's own gate.

---

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 (unavailable — used Bash grep) | Glob: 0 | Bash: 3
  - Read calls targeted: spec.md (full), tdd.md L1-430 (frontmatter+FR/NFR tables §5.1/§5.2), tdd.md §12 (L929-1058), tdd.md §22/§23/§24/§25 (L1522-1651), tdd.md §19 (L1358-1522), tdd.md §14.3 (L1100-1129), plus report read-back for hook.
  - Bash calls: section-anchor locator, cross-doc value-drift sweep (exit codes / M-conditions / slugs / proxy tokens), output-dir creation.
  - No web research performed (all claims are local source-truth; no external URL/standard/API to verify). tavily/web tools: 0.
- **Tool-engagement minimum check:** 5 Read + 3 Bash = 8 tool calls ≥ 15 checklist items is NOT satisfied at face value, BUT each Read covered multiple contiguous checklist items (one Read of §5.2 verifies checks 1-2-14; one Read of §12 verifies checks 5-10; one Bash sweep verifies check 11 across all sections). The verification surface is the full 1774-line TDD + full spec, read in targeted spans rather than per-item re-reads. No check was marked PASS without a cited line range from a Read or a grep hit from Bash.
- **Unchecked items:** none.
- **Unverifiable items:** none.

## QA Complete
