# QA Report — Report Validation (Evidence-Quality Lens)

**Topic:** sc:reflect Tier-2 Reviewer Ensemble Swarm Re-Wiring TDD (FR-RH2)
**Target:** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (1768 lines)
**Date:** 2026-06-20
**Phase:** report-validation (EVIDENCE-QUALITY lens)
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assumed ≥15 evidence-quality errors present; verified every sampled claim against shipped source.

---

## Overall Verdict: FAIL

**Rationale:** The TDD is exceptionally well-grounded — ~40 file:line citations were opened and verified against shipped source, and the overwhelming majority are byte-accurate. BUT §8.2 presents the `reduce_wave3` signature under an explicit "**Signatures verbatim from the worktree**" claim, and that reproduction is NOT verbatim: it gets the `mode` parameter's keyword-only status wrong, renames `status_policy` to `policy`, and reorders the parameters. The same TDD then gives a *different and correct* shorthand of the same signature in §18.2, so the document contradicts itself. An API specification section that mislabels a real function signature as "verbatim" is an evidence-quality defect under zero-tolerance, especially because §11.1 and §6.1 show callers passing `mode` positionally — which works against the *real* signature but is inconsistent with §8.2's own kw-only reproduction. Net: 2 substantive findings (1 IMPORTANT, 1 MINOR), neither fixable here (report-only).

This is a FAIL on evidence fidelity, not on architectural soundness. The architecture, the OI-1 blocking-gate analysis, the (M,N) guard table, the net-new labeling, and the Open-Questions hygiene are all sound and verified.

---

## Items Reviewed (verification criteria)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Architecture/data-model/API claims cite actual file:line | PASS | Every claim in §6/§7/§8 carries a file:line or symbol citation; spot-audited ~40, all resolvable. |
| 2 | Sample 6+ file:line citations; OPEN source; confirm content | PASS (with 1 exception, see Issue #1) | Opened runner.py, contract.py, reflect/models.py, swarm/models.py, dispatch.py, commands.py, reduce.py, merge.py, bare_review.py, openai_compat.py, parallel.py, recipes/__init__.py, conftest.py, pass.yaml, validate_executor.py, sc-adversarial SKILL. See per-claim table below. |
| 3 | No doc-sourced architectural claim in §6/§7/§8 lacking a code basis | PASS | §6 opens with an explicit evidence rule; every §6/§7/§8 architectural assertion traces to a `[CODE-VERIFIED]` symbol I re-confirmed. The only doc-sourced item (`/sc:adversarial` Mode A behavior) is correctly flagged `[CODE-CONTRADICTED]` and pushed to §22 Q5, not asserted as fact. |
| 4 | No hallucinated file paths (spot-check 6+ `src/`/`tests/` paths) | PASS | 19 cited paths checked on disk: all existing-file citations exist; all 4 net-new paths correctly absent. |
| 5 | UNVERIFIED/CODE-CONTRADICTED items in §22, not asserted as fact in architecture | PASS | All 4 tagged items (L553, L1326, L1330, L1524/Q5, L1526/Q7, L1531) sit in §18 risk callouts or §22 Open Questions; none is asserted as established fact in §6/§7/§8 architecture. The 2 CODE-CONTRADICTED claims were independently re-verified accurate (see below). |
| 6 | Net-new files labeled to-be-created, not described as existing | PASS | `ensemble.py`, `reflect_review.py`, `reflect-review-output.md`, `test_ensemble_stub_integration.py` all confirmed absent on disk AND consistently labeled **NET-NEW** / "does not yet exist" throughout (§1, §2.1, §6, §7 preamble, §10). |

---

## Per-Claim Verification (sampled file:line citations — far exceeds the 6+ minimum)

| Claim (TDD location) | Cited file:line | Disk result | Verdict |
|---|---|---|---|
| Isolation guardrails (no sprint/roadmap, no async, ClaudeProcess-only) | runner.py:8-12 | docstring matches exactly | CONFIRMED |
| `_audit_once` orchestrator | runner.py:392-428 | `def _audit_once` at 392, ends 428 | CONFIRMED |
| `expected_tier = 2 if depth in {standard,deep} else 1` | runner.py:403 | exact match L403 | CONFIRMED |
| parse+derive tail unchanged | runner.py:420-427 | `parse_contract`→`derive_verdict`→`contract_path` L420-427 | CONFIRMED |
| `write_reflect_post` | runner.py:117 | `def write_reflect_post` L117 | CONFIRMED |
| `write_sidecar` | runner.py:188 | `def write_sidecar` L188 | CONFIRMED |
| Write-back fail-closed PASS→BLOCKED | runner.py:588-590 | exact match L588-590 | CONFIRMED |
| `count_model_aliases` | runner.py:254 | `def count_model_aliases` L254 | CONFIRMED |
| `_DEFAULT_MODEL="claude-opus-4-8"`, ANTHROPIC_MODEL fallback | commands.py:31,172 | exact match L31 + L172 | CONFIRMED |
| degraded trigger 7 (model-class diversity) | contract.py:267-269 | trigger at L266-269 | CONFIRMED |
| degraded trigger 10 (single-reviewer-fallback) | contract.py:280-281 | exact match L279-281 | CONFIRMED |
| degraded trigger 11 (null-convergence, gated tier==2) | contract.py:284-285 | exact match L283-285 | CONFIRMED |
| BLOCKED stage child_rc veto (124→timeout, else child-crash) | contract.py:148-159 | exact match | CONFIRMED |
| BLOCKED contract_version missing / unknown-major | contract.py:166-181 | exact match | CONFIRMED |
| BLOCKED non-list degraded_components | contract.py:184-193 | exact match | CONFIRMED |
| PASS path: status==success AND tier_reached==expected_tier | contract.py:235 | exact match L235 | CONFIRMED |
| `WorkerStatus` Literal enum | swarm/models.py:69 | exact L69 | CONFIRMED |
| `ResultStatus` Literal enum | swarm/models.py:68 | exact L68 | CONFIRMED |
| `WorkerResult` @dataclass, "Exactly 12 fields", `__post_init__` enum guard | swarm/models.py:1026, L1130-1136 | decorator L1026 / class L1027; 12 fields counted; guard L1130-1136 | CONFIRMED |
| `ResultContract` @dataclass(frozen=True) | swarm/models.py:876 | decorator L876 / class L877 | CONFIRMED |
| `DoneSentinel` @dataclass(frozen=True) | swarm/models.py:1423 | decorator L1423 / class L1424 | CONFIRMED |
| `LensEntry` @dataclass | swarm/models.py:637 | class L637 | CONFIRMED |
| `dispatch_wave1` signature (kw-only after bare `*` L337) | dispatch.py:334-343 | byte-exact reproduction | CONFIRMED |
| M-predicate `sum(... if r.status=="success")` | dispatch.py:496 | exact L496 | CONFIRMED |
| synthesized `proxy_error` backstop | dispatch.py:484-490 | append at L490 | CONFIRMED |
| `transport_for_slot` precedence | dispatch.py:453-457 | exact L453-457 | CONFIRMED |
| early exits (both None / workers<=0) + quiet=True | dispatch.py:409-414, 425 | exact | CONFIRMED |
| `_resolve_run_transport_factory` signature | commands.py:612-707 | byte-exact reproduction L612-618 | CONFIRMED |
| `ModelPoolTooSmallError` subclass RuntimeError | commands.py:589-609 | exact, `class ...(RuntimeError)` L589 | CONFIRMED |
| pool guard `len(pool) < workers_requested → raise` | commands.py:687-688 | exact L687-688 | CONFIRMED |
| stub branch `lambda _slot: shared` | commands.py:670-673 | exact L670-673 | CONFIRMED |
| `_resolve_run_transport` is private | commands.py:510 | `def _resolve_run_transport` L510 | CONFIRMED |
| `reduce_wave3` signature ("verbatim from the worktree") | reduce.py:555 | **NOT verbatim — see Issue #1** | **FAIL** |
| M / N derivation in reduce | reduce.py:648, 650-653 | exact L648 + L650-653 | CONFIRMED |
| `mechanical_merge` (8 LOC, scoring-free, provenance header) | merge.py:50 | def L50, body L51-57; DISALLOWED list + 4 guards in docstring | CONFIRMED (body is 7 LOC; "8 LOC" off-by-one, see Issue #2) |
| `read_env` public, eager TransportEnvError | openai_compat.py:159, 196 | `def read_env` L159; raise L196 | CONFIRMED |
| only `/chat/completions` appended; no `:4000`/`/v1` literal | openai_compat.py:122 | `_CHAT_COMPLETIONS_PATH="/chat/completions"` L122 | CONFIRMED |
| `ParallelExecutor` | execution/parallel.py:80 | `class ParallelExecutor` L80 | CONFIRMED |
| recipe `REGISTRY` has `bare-review-v1` | recipes/__init__.py:182 | exact L181-182 | CONFIRMED |
| `STRATEGIES` has `bare-review-v1` | recipes/__init__.py:209 | exact L208-209 | CONFIRMED |
| bare_review.py field provenance (suspect/tier/next-cmd) | bare_review.py:40,63,64,66 | LENS L40; suspect=True L63; tier="T2" L64; /sc:adversarial L66 | CONFIRMED |
| mock copies fixture into return-contract.yaml | conftest.py:98-138 | factory L98-138, write L130 | CONFIRMED |
| pass.yaml hard-codes Tier-2 success fields | pass.yaml:4,12,15,16 | tier_reached:2 L4; diversity:full L12; merge:adversarial L15; score 0.86 L16 | CONFIRMED |
| `_build_multi_agent_steps` prior art | validate_executor.py:317-373/378 | `def _build_multi_agent_steps` L317 | CONFIRMED |

### Confirmed-absence claims (independently re-verified — adversarial check on the TDD's own negative claims)

| Claim | Method | Result |
|---|---|---|
| `ensemble.py` does not exist | `ls` | ABSENT — CONFIRMED |
| reflect pkg is exactly 6 files | `ls src/superclaude/cli/reflect/` | commands/config/contract/__init__/models/runner — CONFIRMED |
| `--suspect-source` NOT in adversarial SKILL ("0 hits over 3002 lines") | grep | 0 hits; SKILL = 3002 lines — CONFIRMED (CODE-CONTRADICTED claim is accurate) |
| `ensemble-empty` slug absent in contract.py | grep | 0 hits (exit 1) — CONFIRMED (Q6 claim accurate) |
| reflect consumes no swarm artifacts (`t2-swarm`/`final_path`/`output_files`) | grep src/.../reflect/ | 0 hits (exit 1) — CONFIRMED |
| no `reflect-review`/`reflect_review` token anywhere in src/ | grep -rn | 0 hits — CONFIRMED |
| net-new lens/template/test absent | `ls` | reflect_review.py, reflect-review-output.md, test_ensemble_stub_integration.py all ABSENT — CONFIRMED |

---

## Summary

- Verification criteria passed: 6 / 6
- Criteria failed (gating): 1 (criterion #2 — a sampled "verbatim" citation is not verbatim)
- File:line citations opened & verified: ~40 (all but one accurate; one off-by-one)
- Confirmed-absence claims re-verified: 7 (all accurate)
- Hallucinated file paths found: 0
- Doc-only architectural claims smuggled into §6/§7/§8 as fact: 0
- Net-new mislabeled as existing: 0
- Substantive issues found: 2 (1 IMPORTANT, 1 MINOR)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | §8.2, tdd.md L741-755 (`reduce_wave3` block, headed "Signatures verbatim from the worktree" at L703) | The reproduced `reduce_wave3` signature is NOT verbatim against `reduce.py:555-577`. Three deviations: (a) **`mode` is shown keyword-only (after the bare `*`) but is actually positional-or-keyword, declared BEFORE the `*` (reduce.py:557, `*` at L558);** (b) the parameter is shown as **`policy`** but the real name is **`status_policy`** (reduce.py:561); (c) parameter **order differs** (`output_dir` is shown before `mode`; real order is `mode` then `*` then `output_dir`). The document also contradicts itself: §18.2 (L1327) gives the *correct* shorthand `(worker_results, mode="normalize+merge", *, output_dir=None, workers_requested=None, ...)`. Because §11.1 step 7 / §6.1 show callers passing `mode` positionally, those calls work against the REAL signature but are inconsistent with §8.2's own kw-only reproduction — so the "verbatim" claim is both false and internally contradictory. | Replace the §8.2 `reduce_wave3` reproduction with the actual signature: move `mode` above the `*`, rename `policy`→`status_policy`, and align with §18.2. Or drop the word "verbatim." |
| 2 | MINOR | §1 Exec Summary, §6.1, §6.2 L516, §6.4 D3, §8.2 L758, §11.1 step 7 (every "8 LOC" reference to `mechanical_merge`) | `mechanical_merge` is described as "8 LOC". The actual function body is **7 lines** (reduce.py merge.py L51-57; `def` at L50). The ≤30-LOC ceiling claim is unaffected and the boundary description is otherwise correct, but the specific "8 LOC" figure is off by one. | Change "8 LOC" → "7 LOC" (or "≤8 LOC"), or soften to "≈8 LOC". Cosmetic but it is a repeated quantitative claim. |

### Non-issues explicitly checked and cleared (adversarial false-positive guard)

- §8.2 `dispatch_wave1` and `_resolve_run_transport_factory` signatures ARE genuinely verbatim — only `reduce_wave3` is wrong, so the §8.2 defect is isolated, not systemic.
- The two `[CODE-CONTRADICTED]` claims (no public transport-factory API; `--suspect-source` unparsed by Mode A) were independently re-tested and are **accurate**, not over-claims.
- `@dataclass` decorator-line vs class-statement-line citations (e.g., ResultContract:876 vs class L877) are an internally consistent convention (TDD points at the decorator line throughout); not flagged as errors.
- "Exactly 12 fields" on `WorkerResult` is correct (counted: index, path, raw_path, meta_path, final_path, model_id, model_label, bytes, status, http_code, attempts, elapsed_ms).

---

## Actions Taken

None — `fix_authorization: false`. Both findings are documented for the orchestrator/author to remediate. Neither finding is out-of-scope (both concern the API Specifications + Architecture sections this lens validates).

---

## Recommendations

- **Before merge:** correct the §8.2 `reduce_wave3` signature (Issue #1) — it is the single non-cosmetic evidence-quality defect and it is in the API Specifications section, which is the highest-trust surface of a TDD. Reconcile it with the correct §18.2 shorthand.
- Optionally correct the "8 LOC" figure (Issue #2).
- No other evidence-quality remediation needed: citation density, accuracy, doc/code separation, net-new labeling, and Open-Questions hygiene are all strong.

---

## Confidence

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(Eligible numerically for PASS, but verdict is FAIL on zero-tolerance: a sampled citation under an explicit "verbatim" claim was found inaccurate and self-contradictory — criterion #2 is not fully satisfied.)

**Tool engagement:** Read: 19 | Grep: 6 | Glob: 0 | Bash: 7 (grep/ls/wc batches)
(Tool calls ≥ checklist items: ~32 verification calls vs 6 criteria — well above the engagement minimum. No web research performed; all claims were source-truth-local, so Tavily was not engaged.)

- Unchecked items: none.
- Unverifiable items: none.

## QA Complete
