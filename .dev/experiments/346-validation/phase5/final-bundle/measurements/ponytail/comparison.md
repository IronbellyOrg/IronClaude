# Ponytail S1 comparison (descriptive only)

## Draft table per round
This is one measured run, not a success verdict. All figures come from `metrics.json`; its source pointers refer to byte-preserved reports and reused comparator metrics under `reviews/`. Counts follow the original CRITICAL+MAJOR severity-label proxy, not a newly preferred blocking grade. `New total` excludes carried aliases; carried prior findings are shown separately.

| Round | Run | New total | Critical+major proxy | Blocking / nonblocking grade | Bytes seen by review | Growth versus 57,763-byte start |
|---|---|---:|---:|---|---:|---:|
| 1 | Historical original | 24 | 18 | Not regraded | 57,763 | 0% |
| 1 | Ponytail | 16 | 9 | 8 / 8 | 57,763 | 0% |
| 2 | Historical original | 13 | 10 | Not regraded | 82,643 | 43.1% |
| 2 | Ponytail | 15 | 7 | 7 / 8 | 65,568 | 13.5121% |
| 3 | Historical original | 14 | 8 | Not regraded | 92,194 | 59.6% |
| 3 | Ponytail, after audit | 0 | 0 | 0 new; 1 carried MINOR | 70,488 | 22.0297% |

Ponytail report verdicts are FAIL / FAIL / FAIL. No clean-pass round exists. At round 2, two prior blockers remain open, but they are already represented by NF1/F1 and NF7/F3 within the seven new rows, so adding them again would double-count. Round 3's seven resolution rows all say resolved; its one carried prior MINOR is M3. Independently checked the named correction text in the exact endpoint, without performing another substantive review. The separately conservative all-round owner count is **1 critical+major**: the partly rejected round-1 MAJOR note N1 is retained. The audit-held M3 is MINOR and contributes zero to that count (`metrics.json.owner_carry_forward`).

| Reused run | New totals by round | Original proxies by round | Blocking grades by round | Bytes after cycle 1 / cycle 2 | Final growth |
|---|---|---|---|---|---:|
| Control 1 | 19 / 15 / 11 | 11 / 9 / 8 | 11 / 9 / 8 | 71,528 / 91,102 | 57.72% |
| Control 2 | 21 / 17 / 7 | 12 / 7 / 4 | 12 / 7 / 4 | 76,214 / 97,814 | 69.30% |
| Arm B 1, flags added | 22 / 12 / 10 | 16 / 5 / 6 | 11 / 4 / 4 | 67,886 / 73,807 | 27.78% |
| Arm B 2, flags added | 22 / 11 / 4 | 17 / 6 / 1 | 13 / 6 / 1 | 70,255 / 76,328 | 32.14% |
| Ponytail, flags plus inserted audit | 16 / 15 / 0 (plus carried M3 at final) | 9 / 7 / 0 | 8 / 7 / 0 | 65,568 / 70,579 before audit | 22.1872% before audit; 22.0297% after |

Fix-origin figures must not be mistaken for the label proxy: round 2 tags all 15 findings changed, but conservative source-text attribution splits them into 7 strict fix-caused and 8 partial/residual, with none wholly pre-existing-only. That gives strict share 46.67%, strict-plus-partial 100%, not proof that every changed-line finding was caused by a fix. The historical round-2 report called 13/13 introduced or exposed without a strict split; historical round 3 was 10 strict, 3 partial, 1 pre-existing (71.4% strict, 92.9% linked). Ponytail round 3 has no new findings, so its new-finding shares are undefined, not zero. Per-ID mappings, ambiguity and changed-line containment are in `metrics.json.rounds[].M3` and `reviews/scope-diffs.json`.

## Last-round arithmetic against fixed thresholds
The pre-fixed control means are proxy **6** and growth **63.51%**. Their arithmetic bars are `6 × 0.5 = 3` and `63.51% × 0.7 = 44.457%`.

| Quantity | Measured value | Fixed reference | Arithmetic only |
|---|---:|---:|---|
| Final report's original label proxy | 0 | At most 3 | 0 <= 3; 100% below control mean 6 |
| Conservative all-round owner count | 1 | Same numeric reference 3 | 1 <= 3; 83.33% below control mean 6; not interchangeable with report proxy |
| Final byte growth, including audit | 22.0297% | At most 44.457% | 22.0297 <= 44.457; 41.4803 percentage points below control mean |
| Growth before the inserted audit | 22.1872% | At most 44.457% | Already numerically below the bar before auditing |
| Versus Arm B mean | Proxy 0 versus 3.5; growth 22.0297% versus 29.96% | Reused flagged runs | Proxy difference -3.5; growth difference -7.9303 percentage points |
| Versus historical original | Proxy 0 versus 8; growth 22.0297% versus 59.6% | Historical arithmetic bars 4 and 41.72% | Numbers only, not a controlled attribution |

The inserted audit itself changes growth by only **-0.15754 percentage points** (91 bytes). Most measured growth restraint therefore predates its edit; this run does not isolate an audit-induced effect from earlier review/revision variation. Control proxy spread is 4, Arm B spread 5, but ponytail's within-arm spread is unknown. One run cannot satisfy the two-replicate repeatability/spread requirement, and final-review model continuity failed. **No verdict on variant success is given.**

## Audit changes and cost
The audit was its own session, with actual Skill calls to `sc:spec-panel-ponytail` and `ponytail:ponytail-review`; it was not a fourth panel review. It used 18 calls, 18,713 logged output tokens and 3.2537 elapsed minutes. Total original-loop cost, excluding setup and later reuse of the first-review terminal, is 274 calls and 239,628 logged output tokens. Final-review elapsed time includes rate-limit waits and its resumed model change; cross-provider billing equivalence is not established.

Two actual audit edits are verified against `current-before-audit.md`, state, apply log and exact endpoint diff:

| Edit | Hunk | Source line | Bytes in logged span | Net |
|---|---|---:|---:|---:|
| Revert prior MINOR M3 template expansion to saved baseline | H8 | 158 | 788 to 749 | -39 |
| Delete repeated release-only citation clause, related to MINOR M6 | H2 | 68 | 90 to 38 | -52 |

Total 70,579 to 70,488 bytes, **-91 bytes (-0.128934%)**, two changed source lines and two separated zero-context diff hunks. The script's `reverted=1 shrunk=1 kept=12` is a hunk summary; its apply log has 2 applied operation rows and 21 skipped rows, so these counts describe different units. All seven blocking fixes were retained. Three proposed additional shrink operations were skipped because a keep on the same hunk wins: the repeated nested-read prose in H1 and H9, and the extra run-dir collision-check paragraph in H14. The old-span lengths 82/80/290 in the log are NOT all proposed savings, because the first two replacements retain text (`reviews/fix-audit/audit.md:22-25`; `apply-log.md:20-24`).

The first revision applied 7 MINOR-labelled fixes and partly applied/rejected one nonblocking MAJOR note; the second revision applied all 8 new MINOR-labelled fixes before auditing. The audit reversed M3, leaving 14 MINOR-labelled fixes across the two cycles, with M6's citation trimmed but substantive correction retained. Those are separate from the critical+major owner carry-forward.

**Recorded failure, not repaired:** the verdict script returned exit 2, then the coordinator driver returned 11. Preserved output calls the 37 citation rows C01-C37 blockers, says no resolution rows parsed, and prints an owner critical+major count of zero. That automated zero is invalid. Independent report-text counts are zero new critical+major, zero unresolved prior blocking findings, and one carried prior MINOR; the broader all-round owner carry-forward is 1 (round-1 N1). The final report remains **FAIL**, not a clean PASS.

**Contradiction retained:** report line 29 promises `R3-N1`, yet its new-findings section says none; lines 110,111,174 reject that retry hypothesis. The orphan reference is recorded as one ungraded uncertain candidate, not silently converted to a confirmed blocker or silently discarded. No report formatting fix, parser repair, fourth review or new fix pass was run.

## What could not be measured
The exact final source was recovered and hash verified, so there is no endpoint-recovery gap. Missing or unprovable: a second independent ponytail run; within-variant spread; uninterrupted hashes of additive command files; a whole-machine write audit; the orphan candidate's authorial intent; coordinator-token attribution; active model time excluding cooldowns; and billing-equivalent usage across the changed provider. See `metrics.json.not_recoverable` and `validity.md` for the bounded searches and negative evidence.

## Limitations (at most eight)
1. **One run:** no repeatability or ponytail spread estimate; comparison runs are earlier, not concurrent.
2. **Model changed in final review:** launch requested Opus, but resumed response records are labelled `gpt-6.1-sol` after a local model action; the controlled same-model condition fails.
3. **Different available environment:** finished master WORKER-CONTRACT was present. No explicit answer-key read/reuse was found, but presence and installed current primitives differ from controls.
4. **Incomplete continuous integrity proof:** command hashes match install endpoints, not a continuous variant-file watch. Human text reached an earlier completed terminal; no resulting source write was observed. The expected verdict artifact was written after final worker delivery.
5. **Invalid automation:** verdict parsing fails on the final report's prose-first resolution rows and misreads citation rows; printed owner zero cannot be used as measured success.
6. **Grade and report inconsistencies:** original final gate says FAIL for M3, while the blocking-only count is zero; round-1 MAJOR N1 is retained under the broader owner rule; the orphan R3-N1 reference remains uncertain.
7. **Origin is not cause:** changed tags include old residuals and dependent unchanged lines; strict/partial attribution is interpretive, and the final scoped re-review is not a new whole-document audit.
8. **Added work and cost:** the audit adds a session and script operations, saves only 91 bytes, and exposes applied audit results to the last reviewer via apply-log/fix-list/state (no audit.md content read found). Token/time comparisons include provider differences and cooldowns.

## Evidence-package quality verdict
**PASS: evidence-package quality only.** All four requested outputs are present, JSON parses, copied evidence and source hashes are verified, and the original parser failure is preserved rather than repaired. Counts and arithmetic passed the executable checks in `reviews/count-and-integrity-checks.json`; final package checks and a complete evidence inventory are also retained under `reviews/`. This verdict concerns a complete, candid measurement package. The original final report is still FAIL, same-model validity failed, and no verdict that the variant succeeds is issued.

## Self-Audit
Actively challenged the flattering zero: independently counted both numbered severity tables, resolved-status rows and the carried minor; retained the earlier partly rejected MAJOR; investigated the orphan new-finding reference; compared pre-audit and final bytes and exact edits; traced actual Skill calls and model metadata; separated rate-limit waits, terminal reuse and expected later verdict writes; checked fixed arithmetic against reused comparator files. This found material limitations, not a perfect loop. No further model review or repair was used to force agreement. The 74 assertion results document evidence fidelity; they are not product tests or an implementation acceptance run. No action is needed from this recorder; the coordinator can use this local comparison with the recorded limits.
