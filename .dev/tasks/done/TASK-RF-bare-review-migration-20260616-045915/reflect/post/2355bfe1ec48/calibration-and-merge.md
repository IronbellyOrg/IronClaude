# Wave 3C/4/5 — Blind Calibration + Evidence-Validated Merge

**Calibrator:** opus (claude-opus-4-8), inline orchestrator — disjoint from reviewer classes {sonnet=gpt-5.5, haiku=qwen3.6-plus}. `calibrator_diversity: full`.
**Executor (under review):** opus — excluded from reviewer pool per §7.1. Reviewer pool = {sonnet, haiku}, N=2 (`executor_exclusion_degraded: true` — the 3rd default slot would be opus=executor, removed; no non-executor 3rd class available with distinct vendor). `t2_model_class_diversity: degraded` (2 classes), `t2_vendor_diversity: multi` (anthropic-excluded reviewers are gpt-5.5 + qwen3.6-plus → 2 vendors).

Both reviewer cards returned **FAIL** with high self-reported confidence (0.89, 0.88). Per §11.3, self-reports are NOT trusted; every finding was independently re-Read and, where it made an empirical claim, **empirically tested** (ran a live stub `swarm run --lens bare-review` + compared against the frozen golden). The merge here is evidence-vs-reviewer (both reviewers agree with each other but disagree with ground truth), so the decisive gate is the evidence-validator (§11.2), not adversarial debate (§8 is for competing reviewer verdicts). `merge_method: evidence-validated-synthesis`.

## Per-finding calibration ledger

### Card 1 (sonnet — pipeline correctness)

| # | Reviewer claim / class | Independent verdict | Calibrated class | Evidence |
|---|---|---|---|---|
| 1 | Resume contract not enriched → **regression** | **DROPPED** | not-a-deviation (pre-existing) | Diff hunks touching "resume" are all *comments* in the new helpers; the resume branch (~L1900+) is unmodified. Inline previously emitted NO contract; WS-0 brought it to parity-with-output. Resume's lack of metadata enrichment pre-dates this task → out of scope. |
| 2 | Blank `reviewer_model_id`/`label` in bodies → **drift** | **DROPPED** | not-a-deviation (parity-faithful) | Live run shows body `reviewer_model_id: ""`; **frozen golden `all-success/bare-review-01-m.md` is identical** (`reviewer_model_id: ""`). Parity test GREEN. The contract `output_files[].model_id` IS populated. Migration faithfully reproduces the legacy normalizer; populating body model_id is a pre-existing legacy design choice, out of scope for a byte-parity port. |
| 3 | `target_truncated`/`elapsed_ms`/`status` blank → **drift** | **DROPPED** | not-a-deviation (parity-faithful) | Golden body identical (`target_truncated: false`, `elapsed_ms: 0`, `caller_label: ""`). `target_truncated: false` is *correct* for a non-truncated target. Same parity rationale as #2. |
| 4 | `--reviewers` clobbers user `workers.models` for spec-file mode → **regression** | **DOWNGRADED** | authorized (tasklist-mandated) | Step 2.2 *explicitly instructs* "resize `spec_dict["workers"]["models"]` to N placeholder entries" so INV-005 admits count=4. The behavior is the mandated implementation. The spec-file-caller edge is a real but unexercised corner; MINOR forward observation, not a deviation. |
| 5 | Target re-read (TOCTOU) + empty-on-OSError → **regression** | **DOWNGRADED** | necessary (documented) | Step 2.6 notes the resume branch has no reusable assembly helper, so the inline path must assemble directly — the re-read is the sanctioned approach. TOCTOU window is tiny; irrelevant under stub (CI path). Empty-on-OSError is defensive (comment acknowledges). MINOR hardening observation. |
| 6 | Non-positive `--target-line-cap`/`--timeout-sec` accepted → necessary | **CONFIRMED (minor)** | observation (non-blocking) | Real input-validation gap. `line_cap<=0` disabling truncation matches *pre-existing* preflight semantics. Tasklist did not mandate range validation for B-2/B-3. MINOR follow-up. |
| 7 | Terminal state without contract when `recipe_name` empty → regression | **DOWNGRADED** | not-reachable on bare-review | `recipe_name` is always `bare-review-v1` on the lens path; branch only affects a hypothetical lens-less run with output. Pre-existing pattern. MINOR edge. |
| 8 | Next command not shell-safe (spaces/commas) → drift | **DOWNGRADED** | by-design (minor) | Comma is the *intended* `--compare`/`--suspect-source` delimiter. Space-in-path is a universal limitation, parity-faithful. MINOR. |

### Card 2 (haiku — tests + contract)

| # | Reviewer claim | Independent verdict | Calibrated class | Evidence |
|---|---|---|---|---|
| 1 | `test_target_line_cap_and_timeout_flags_accepted` vacuous | **CONFIRMED (minor)** | observation (non-blocking) | True — asserts only exit 0 + contract exists; docstring admits it. But the tasklist (Steps 2.3/2.4) did NOT require a behavioral test for B-2/B-3 (only B-1 required a dispatch-count test, which exists and is sound). So it exceeds, not violates, the tasklist. Quality follow-up, not a deviation. |
| 2 | SKILL.md contract YAML shorthand ≠ 19-key `ResultContract` | **DOWNGRADED** | observation (doc) | The SKILL.md block is an intentional *caller-facing subset* in a file deliberately compressed 231→80. Semicolon shorthand is doc-sketch, not a parsed schema. MINOR doc-clarity. |
| 3 | `--suspect-source` substring assert brittle | **CONFIRMED (trivial)** | observation | Reviewer concedes the adjacent `{suspect_files}`/`.final.md` checks prove rendering. Trivial. |
| 4 | `--reviewers=4` test omits pool-resize assertion | **DOWNGRADED** | adequate | The test proves `workers=4` dispatched + manifest `workers_requested==4` — the user-facing invariant. Pool resize is the internal mechanism that *enables* that; dispatch succeeding at 4 transitively proves it. |
| 5 | `--transport` not in SKILL flag surface | **CONFIRMED (minor)** | observation (doc) | Real minor doc inconsistency: invocation block hardcodes `openai_compat` but flag isn't in the surface list. Defensible (skill always wants production transport). MINOR. |
| 6 | AC-1.5 single-message dispatch dropped | **DROPPED** | legitimate (reviewer concedes) | CLI now owns fan-out; the agent no longer dispatches. Correct removal. Non-finding. |
| 7 | Release notes "invocation shape unchanged" misleading → **regression** | **DROPPED** | refuted (reviewer misread) | Actual text: *"…is preserved — **only the dispatch mechanism changed**. Skill invocation shape from caller pipelines … is unchanged."* Callers still invoke `Skill sc-bare-review`; the line is accurate. False positive. |
| 8 | `openai_compat` hardcoded, no stub example | **CONFIRMED (trivial)** | observation (doc) | Minor doc-clarity; could add a stub example. Trivial. |

## Calibrated outcome

- **Citations examined:** 16 reviewer findings. **Dropped as deviations:** 5 (Card1 #1/#2/#3, Card2 #6/#7) — refuted by golden-parity / unmodified-resume / actual-text evidence. A healthy non-zero drop count (§11.2: a zero-drop adversarial pass would be *suspect*).
- **Regressions (committed WS-0+WS-A vs tasklist):** **0**.
- **Blocking Drift:** **0**.
- **Necessary deviations:** 1 (inline target re-read, tasklist-sanctioned).
- **Non-blocking MINOR observations (forward-looking, none gate):** 4 — vacuous B-2/B-3 effect test; non-positive flag values; `--transport` not in SKILL flag-surface list; SKILL.md contract-block shorthand.
- **Calibrated confidence in the verdict** ("committed WS-0+WS-A faithfully implements tasklist Phases 2-3 with no regression; minor non-blocking follow-ups"): **0.90**.

The two adversarial FAIL verdicts do not survive evidence validation; the committed code is correct and parity-faithful. The genuinely material reflect findings are at the **scope/completion** layer (below), which single-file review would miss.
