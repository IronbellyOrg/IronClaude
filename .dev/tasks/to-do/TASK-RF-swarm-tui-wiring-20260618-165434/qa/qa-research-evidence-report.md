# QA Report — Research Gate (Evidence-Quality Lens)

**RE-RUN after gap-fill round 1**

**Topic:** Wire `--tui` into `superclaude swarm run` (Approach A)
**Date:** 2026-06-18
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** 2 (re-run after gap-fill round 1)
**Fix authorization:** false

---

## Scope of this re-run

Adversarial re-verification of gap-fill round 1 outputs only:
- `research/06-gapfill.md` (NEW) — 100% file:line citation spot-check (small + load-bearing)
- `research/03-patterns-conventions.md` (CORRECTED daemon text) — precedent-line re-check
- Prior MINOR resolution: `_follow_log` vs `_follow_log_file` (02-reader-contracts.md §9)
- Hunt for NEW unsupported claims introduced by the gap-fill

Verification method: zero-trust. Every citation Read/grepped against actual source in
`/config/workspace/IronClaude/`.

---

## Part 1 — 06-gapfill.md citation spot-check (100% of file:line claims)

Every code citation below was independently Read/grepped against source. **All EXACT.**

| 06 claim | Source verified | Result |
|---|---|---|
| `executor.py:416` `threading.Thread(...daemon=True)` precedent (G1) | sed 413-432 | EXACT (`daemon=True` at :416) |
| `executor.py:434-449` defensive None-replacement (G1) | sed 434-449 | EXACT |
| `commands.py:1726` `state_output_dir: Optional[Path] = None` init (G2) | sed 1722-1740 | EXACT (:1726) |
| `commands.py:1727` `if preflight_result.manifest_path:` gate; assign `:1731` (G2) | sed 1722-1740 | EXACT |
| `commands.py:1732-1740` Logger w/ `jsonl_path=.../execution-log.jsonl` `:1733` (G2/G4) | sed 1722-1740 | EXACT |
| `commands.py:1722-1725` docstring "spec-only smoke path… without a materialised output directory" (G2) | sed 1722-1725 | EXACT (quoted phrase present) |
| `commands.py:1807-1813` synchronous `dispatch_wave1` (G2) | sed 1807-1813 | EXACT (verbatim kwargs) |
| `tui.py:230-234` idempotent `stop()` (G3) | sed 230-234 | EXACT byte-for-byte |
| `commands.py:2585-2613` `status --watch` SIGINT swallow + `Exit(last_exit_code)` (G3) | sed 2585-2613 | EXACT |
| `commands.py:1471` `def run_cmd(` / `:1912` terminal `Exit(EXIT_OK)` / `:188` `EXIT_OK=0` (G3) | grep + sed | EXACT |
| run_cmd has NO `except KeyboardInterrupt` (G3) — only `:2606` (status --watch), `:2826` (logs --follow) | grep KeyboardInterrupt | CONFIRMED (no hit in 1471-1912) |
| `tui.py:218-228` `Live(...)` `screen=False`, NO redirect kwargs → Rich default redirect on (G4) | sed 218-228 | EXACT |
| `tui.py:272-285` `_build_header(Optional[SwarmState])` (G5) | sed 272-285 | EXACT |
| `tui.py:277` `state_value = state.state if state is not None else "-"` (G5) | sed 277 | EXACT |
| `tui.py:278` `job_id = state.job_id if state is not None else "-"` (G5) | sed 278 | EXACT |
| `tui.py:236-245` `update(Optional[SwarmState], ...)` / `:251-270` render pure (G5) | sed 236-270 | EXACT (render docstring "Pure" at :256-260) |
| `tui.py:287+` `_build_worker_table` events-only (G5) | grep `def _build_worker_table` | EXACT (:287) |
| `state.py` `read_state` → `None` on missing file (G5, "state.py:190-193") | sed 185-200 | EXACT (FileNotFoundError → return None) |
| `commands.py:2737` `def _follow_log(` (G6) — the CORRECT name | grep `def _follow_log` | EXACT (`_follow_log_file` = ZERO hits) |
| `commands.py:2834-2858` `_drain_appended` seek/read/tell + `click.echo(...nl=False)` `:2857` (G6) | sed 2834-2858 | EXACT (seek 2845, read 2846, tell 2847, echo 2857) |

**Result: 21/21 06 citations EXACT. Zero mis-cited line numbers, zero phantom symbols.**

---

## Part 2 — `_follow_log` name fix (prior MINOR resolution)

- **06 states the correct name.** G6 (06 lines 357-363) explicitly: *"`02-reader-contracts.md`
  refers to the follow helper as `_follow_log_file` (lines 141, 147, 168). That name is WRONG.
  The actual function is named `_follow_log` (commands.py:2737). [CODE-VERIFIED]"* — and
  uses `_follow_log` throughout (lines 321, 359, 366). **VERIFIED CORRECT.**
- **06 explicitly fixes the 02 mislabel for the builder.** ✅ (the prompt's standing rule —
  "02 mislabel may remain as long as 06 corrects it" — is satisfied.)
- **02 still says `_follow_log_file`** at lines 141, 147, 168 (grep confirmed), and still tags
  it `[CODE-VERIFIED]` (line 141) on a name that has zero source hits. Per the prompt this is
  *tolerated* because 06 corrects it. Noting it as **resolved-via-06**, not re-failed.

---

## Part 3 — 03-patterns-conventions.md corrected daemon text

- **03 §4a + §4 reuse table now carry the FR-5 OVERRIDE.** Lines 125-127 / 356 explicitly:
  precedent uses `daemon=True`; swarm dispatch thread MUST be `daemon=False` + explicit
  `join()`; only the daemon flag differs, result-box/exception-box pattern is reused.
- **Cited precedent lines are real.** `pipeline/executor.py:413-432` quoted block matches
  source (faithful, with `...` elisions); `:416` `daemon=True`, `:434-449` None-replacement,
  `monitor.py:448-478` daemon-monitor idiom — all consistent with source. FR-5 citation
  `merged-requirements.md:99-105` resolves to the real FR-5 block.
- **03's daemon correction is accurate and well-grounded.** No defect in 03's daemon text.

---

## Part 4 — NEW unsupported-claim scan (adversarial)

One NEW defect found, introduced by the gap-fill.

### NEW MINOR — 06 G1 labels a NON-verbatim FR-5 quote as "verbatim"

06 line 30-35 introduces the quote as: *"spec **FR-5**, `merged-requirements.md:99-105` —
verbatim:"* and then quotes:

> *"(Worker thread is non-daemon with an explicit `join()` so **`execution-log.jsonl`** is
> never truncated at interpreter shutdown.)"*

The spec FR-5 (merged-requirements.md:99-105, Read this pass) actually says **`event-log.jsonl`**,
not `execution-log.jsonl`:

> *"…so **`event-log.jsonl`** is never truncated at interpreter shutdown."* (spec verbatim)

06 silently substituted the token inside a block it labeled "verbatim".

**Severity = MINOR (not IMPORTANT), because:**
- The substituted token is the *correct real-world filename*. Prior round established
  `event-log.jsonl` is the **stale docstring name** and `execution-log.jsonl` is the **real
  write-path** (`commands.py:1733`, re-confirmed this pass). So 06 points the builder at the
  RIGHT path — it does not mislead toward a wrong file.
- 06 is internally consistent everywhere else (`execution-log.jsonl` at lines 32, 69, 71, 152,
  325 — all the real path).
- The defect is purely citation-honesty: a "verbatim" label on text that is not byte-identical
  to the source. An adversarial reader cross-checking the quote against the spec finds a
  mismatch.

**Required fix (non-blocking; fix_authorization=false this lens):** quote FR-5 verbatim with the
spec's actual `event-log.jsonl`, then append a bracketed correction, e.g.
`[spec FR-5 says event-log.jsonl — that is the STALE name; real write-path is
execution-log.jsonl per commands.py:1733, see 02 CODE-CONTRADICTED]`. OR drop the word
"verbatim" and present it as a paraphrase-with-correction. Either makes the citation honest.

No other new unsupported claims. Every G1-G6 resolution carries a verifiable file:line that
survived spot-check; the two DECISION recommendations (G2 guard rule, G3 SIGINT pattern) are
explicitly flagged as decisions/recommendations, not asserted as existing code; the G4 "tui.py
unchanged = SAFE" verdict is correctly conditioned on FR-1's single-writer audit (honest hedge,
not over-claim).

---

## Confidence Gate

**Checklist categorization (evidence-quality re-run lens):**
- [x] 06 — 100% file:line spot-check — VERIFIED (21/21 citations Read, all EXACT)
- [x] 06 — `_follow_log` name now correct + 02 mislabel fixed-for-builder — VERIFIED
- [x] 02 — does it still say `_follow_log_file`? — VERIFIED (yes, lines 141/147/168; tolerated per prompt rule)
- [x] 03 — corrected daemon text cites real precedent lines — VERIFIED (executor.py:413-432/416/434-449 EXACT)
- [x] NEW unsupported-claim scan — VERIFIED (1 NEW MINOR found: G1 "verbatim" misquote of FR-5 filename token)
- [x] 06 DECISION/recommendation honesty (G2/G3/G4 hedges) — VERIFIED (decisions flagged as such, not asserted as code)

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 2 | Grep: 4 | Glob: 0 | Bash: 6 (sed/grep against source) | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
(No external web lookups required — all claims are intrinsically local code/spec citations.)
Tool calls (12) vs checklist items (6): each call targeted specific cited claims (21 source
citations verified across the batched calls). Not padding.

---

## Overall Verdict

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 06 file:line citations exist as cited (100% spot-check) | PASS | 21/21 EXACT |
| 2 | `_follow_log` (not `_follow_log_file`) stated correctly in 06; 02 mislabel fixed-for-builder | PASS | 06 G6 explicit + [CODE-VERIFIED]; `_follow_log` at :2737, `_follow_log_file`=0 hits |
| 3 | 03 corrected daemon text cites real precedent lines | PASS | executor.py:413-432/416/434-449 EXACT; FR-5 override accurate |
| 4 | No NEW unsupported claim from gap-fill | FAIL | 1 NEW MINOR: 06 G1 labels a non-verbatim FR-5 quote ("execution-log.jsonl" substituted for spec's "event-log.jsonl") as "verbatim" |

**Summary:** Checks 1-3 PASS. Check 4 found 1 NEW MINOR. Prior MINOR (`_follow_log_file`) is
RESOLVED for the builder via 06's explicit correction. CRITICAL: 0. IMPORTANT: 0. MINOR: 1 (new).

The gap-fill is otherwise excellent: all six gaps (G1-G6) are resolved with verifiable,
spot-check-EXACT file:line evidence, the prior `_follow_log` mislabel is correctly fixed, the
daemon/non-daemon FR-5 nuance is handled precisely in both 06 and 03, and the recommendations
are honestly framed as decisions rather than asserted code. The single new defect is a
citation-honesty slip — a "verbatim" label on a quote whose filename token was silently
corrected to the (correct) real path.

Per RF research-gate rule "ALL gaps regardless of severity = FAIL", this MINOR technically
blocks. The fix is a one-line edit to 06 G1 (re-quote FR-5 with the spec's actual
`event-log.jsonl` token + bracketed stale-name correction, or drop the "verbatim" label).
fix_authorization is false for this lens, so the consolidation/orchestration step should apply
it. The builder is NOT blocked on substance — every implementation-critical anchor (state_output_dir
gate, dispatch_wave1 call, daemon=False mandate, _follow_log/_drain_appended byte-offset pattern,
idempotent stop(), None-safe header, run_cmd's absent KbdInterrupt handler) is EXACT and correct.

**VERDICT: FAIL** — 1 MINOR (NEW): 06 G1's FR-5 quote is labeled "verbatim" but substitutes
`execution-log.jsonl` for the spec's actual `event-log.jsonl`. Zero CRITICAL, zero IMPORTANT.
Prior MINOR (`_follow_log_file`) RESOLVED-via-06.

## QA Complete
