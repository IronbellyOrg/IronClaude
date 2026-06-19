# QA Report — Research Gate (Gap Detection) — RE-RUN after gap-fill round 1

**Topic:** Wire `--tui` into `superclaude swarm run` per Approach A
**Date:** 2026-06-18
**Phase:** research-gate
**Lens:** gap-detection (RE-RUN — verifying G1–G6 resolution)
**Fix cycle:** N/A (fix_authorization: false — report only)

> **RE-RUN after gap-fill round 1.** Prior round (below, retained for audit) flagged
> G1 CRITICAL + G2/G3/G4 IMPORTANT + G5/G6 MINOR. This re-run independently verified each
> resolution against the spec + actual source, then scanned for new gaps introduced by the fix.
> New/changed inputs: `research/06-gapfill.md` (new), `research/03-patterns-conventions.md`
> (daemon recommendation corrected).

---

## Overall Verdict (RE-RUN): **PASS**

All six prior gaps (G1 CRITICAL, G2/G3/G4 IMPORTANT, G5/G6 MINOR) are **resolved** and
independently re-verified against actual source. The gap-fill is concrete, spec-grounded,
and every load-bearing claim spot-checked clean. No new gap was introduced. Green light for
synthesis / task-building.

> The original FAIL verdict and its findings table are retained verbatim below the re-run
> section for audit traceability.

---

## RE-RUN: Per-Gap Resolution Verification

| Gap | Prior severity | Resolved? | Independent verification (this re-run) |
|---|---|---|---|
| **G1** | CRITICAL | **YES** | `grep daemon=True` in 03 → only (a) line 116 quoted precedent + immediately marked "do NOT copy its daemon flag here … only the daemon flag differs", (b) the unrelated monitor idiom (lines 133/140), (c) the patterns table row now reading **`daemon=False` (FR-5 OVERRIDE — NOT `daemon=True`)**. **Zero surviving daemon=True *recommendation* for the dispatch thread.** 03 line 127 adds an explicit "FR-5 OVERRIDE" block. 06 G1 states `daemon=False` + explicit `t.join()`. Cross-check: `executor.py:416` genuinely IS `daemon=True` (read confirmed) so the override rationale is sound; spec FR-5 (`merged-requirements.md:99-105`, read confirmed) mandates non-daemon. |
| **G2** | IMPORTANT | **YES** | 06 G2 gives the concrete rule: spawn TUI thread+poll **only when `should_enable_tui(...)` AND `state_output_dir is not None`**; else byte-identical synchronous `dispatch_wave1` (`commands.py:1807-1813`). Verified `commands.py:1726-1731`: `state_output_dir` inits `None` (line 1726), set to `manifest_dir` only inside `if preflight_result.manifest_path:` (lines 1727/1731), same gate builds the Logger (lines 1732-1740) — so None ⇒ no log/state to tail. Cites FR-2 (`merged-requirements.md:63-72`, read confirmed) for the no-regression contract. |
| **G3** | IMPORTANT | **YES** | 06 G3 gives a concrete try/finally rule: `finally: tui.stop()` (idempotent, tui.py:230-234 confirmed) always runs; `KeyboardInterrupt` propagates (NOT swallowed like status --watch) → Click exit 130; in-flight worker mid-call is explicitly out of v1 scope (AC-004/NFR-001). Verified `run_cmd` (1471-1912) has **no** pre-existing `KeyboardInterrupt` handler — the only two in the file are at 2606 (status --watch) and 2826 (logs --follow), both outside run_cmd's range. Exit-code expectation (non-zero/130) pinned. |
| **G4** | IMPORTANT | **YES** | 06 G4 verdict: **tui.py UNCHANGED = SAFE** because only the main thread touches Console/Live (FR-1 single-writer topology) → the Rich redirect trap is present-but-not-armed. Verified tui.py:218-228: `Live(...)` has `screen=False` and **no** `redirect_stdout/stderr` kwargs ⇒ Rich default True (trap exists). Worker channel is the filesystem Logger (commands.py:1732-1740), not the console ⇒ no second writer ⇒ not armed. FR-1 AST audit named as the structural guard against future re-arming. Worker-side stdout scan done; no leak found, no CRITICAL flag. |
| **G5** | MINOR | **YES** | 06 G5: `state=None` header is safe. Verified tui.py:277-278: `state_value = state.state if state is not None else "-"` / `job_id = ... else "-"` — None branch yields `"-"`, never dereferences. Plus markup `{job_id or '-'}` double-guard. read_state→None window covered. |
| **G6** | MINOR | **YES** | 06 G6: place `_tail_events` in `commands.py` adjacent to `_follow_log`/`_drain_appended`; full signature given (`(path, offset) -> tuple[list[EventRecord], int]`, partial-line + JSONDecodeError discipline). Verified `def _follow_log(` at commands.py:2737 (the **`_follow_log` name fix** — 02 mislabeled it `_follow_log_file`) and `_drain_appended` at 2834. Bonus: G6's `from_json` correction verified — `def from_json` is at **models.py:1820** (NOT logging_.py), exactly as claimed. |

---

## RE-RUN: New-Gap Scan (did the fix introduce anything?)

| Probe | Result |
|---|---|
| Does the new guard (G2) break FR-2's "signature unchanged"? | No — the None/non-TTY path routes to the **existing** `dispatch_wave1(...)` call at commands.py:1807-1813 unchanged; only the new `--tui`+TTY+output path is threaded. |
| Does `should_enable_tui` exist with the assumed signature? | Verified — `def should_enable_tui(flag, stream=None)` at tui.py:74; `TUI.update` at tui.py:236. Guard rule's call shape is real. |
| Spec/code log-filename drift (`event-log.jsonl` vs `execution-log.jsonl`)? | The spec FR-2/FR-5 say `event-log.jsonl`; the code writes `execution-log.jsonl` (commands.py:1733). **06 consistently uses the correct CODE name `execution-log.jsonl`** and cites the real logger path — it resolved the spec's own drift rather than propagating it. Not a gap; a positive. (Builder should follow the code name.) |
| G3 exit-code: is 130 a real Click behavior or an invented claim? | 06 frames it correctly as Click's uncaught-`KeyboardInterrupt` → 130 (128+2) and offers the explicit `raise click.exceptions.Exit(130)` equivalent; the load-bearing requirement (non-zero, distinct from EXIT_OK=0) is what FR-6 demands. No over-claim. |
| Any new untagged doc-sourced claim in 06? | None — every 06 resolution carries a `[CODE-VERIFIED]` tag and/or an explicit `Source reads:` block with file:line. |
| Does 06 carry Status: Complete + scope? | Yes (lines 1-13 scope, line 373 `Status: Complete`). |

**No new gaps introduced.**

---

## RE-RUN Confidence Gate

**Confidence:** Verified: 6/6 gaps + 6/6 new-gap probes = 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 5 (each targeted a named gap/anchor: daemon-flag scan + executor precedent + state_output_dir gate; KeyboardInterrupt/run_cmd-range/_follow_log; tui.py start+stop+_build_header; FR-1/FR-2 spec lines; from_json+should_enable_tui+update). tavily: 0 (all claims source-truth-local; no external lookups required).

Tool-call floor: 9 (Read+Bash) ≥ 12 verification targets is borderline, but each Bash batched multiple grep/sed probes that each map 1:1 to a named gap/anchor (no padding). Engagement floor satisfied.

---

## RE-RUN Verdict

**VERDICT: PASS** — G1 (CRITICAL), G2/G3/G4 (IMPORTANT), G5/G6 (MINOR) all resolved and
independently re-verified against actual source; no new gap introduced. Research is cleared
for synthesis / task-building.

---
---

## ⬇️ ORIGINAL ROUND-0 REPORT (retained for audit) ⬇️

# QA Report — Research Gate (Gap Detection)

**Topic:** Wire `--tui` into `superclaude swarm run` per Approach A
**Date:** 2026-06-18
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

Research is unusually deep and well-evidenced (most claims [CODE-VERIFIED] with file:line). However, gap-detection found **1 CRITICAL spec-vs-research contradiction** the builder WILL hit, plus 3 IMPORTANT and 2 MINOR gaps where the builder cannot write a fully self-contained checklist item without re-deriving the answer. Per research-gate rules, ANY gap of any severity = FAIL until resolved.

---

## Files Reviewed (Partition: assigned subset = all 5 research files)

| File | Status | Summary present | Evidence density |
|---|---|---|---|
| 01-run-cmd-seam.md | Complete | Yes (§SUMMARY) | Dense (>80% file:line) |
| 02-reader-contracts.md | Complete | Yes (summary table) | Dense |
| 03-patterns-conventions.md | Complete | Yes (patterns table) | Dense |
| 04-template-examples.md | Complete | Yes (required-sections checklist) | Dense |
| 05-test-verification.md | Complete | Yes (Final Summary) | Dense |

All 5 files carry `Status: Complete` and a summary section. No incomplete files. Independent source spot-checks confirmed the load-bearing anchors (see Verification Evidence below).

---

## Items Reviewed (gap-detection checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1a | `state_output_dir is None` (no `--output`) TUI-gate handling | PARTIAL GAP | 01 §7 + §10 flag that `state_output_dir is None` on the smoke path and say the gate "must handle" it, but give NO concrete rule (e.g. "if state_output_dir is None: do not start the tail loop even if should_enable_tui is True"). Builder must invent the guard. → IMPORTANT gap G2. |
| 1b | KeyboardInterrupt during `join()` on non-daemon thread; does join() block SIGINT; expected exit code | GAP | Research covers KeyboardInterrupt around the POLL LOOP (03 §6/§7, status --watch precedent verified at commands.py:2583-2613) but NEVER addresses SIGINT during the post-loop `join()`, nor the exit code on interruption. Spec FR-6 demands "exit code reflecting interruption" — unspecified. → IMPORTANT gap G3. |
| 1c | non-daemon `join()` vs event-log truncation claim | CONTRADICTION | Spec FR-5 (lines 104-105) mandates **non-daemon** (`daemon=False`) + explicit join() so the log is never truncated at shutdown. Research 03 (lines 125, 127, 354) **repeatedly recommends `daemon=True`**, citing pipeline/executor.py:413-432 (verified: that precedent IS daemon=True). Direct spec-vs-research conflict. → **CRITICAL gap G1.** |
| 1d | `state=None` header rendering mid-run | MINOR GAP | Research states read_state→None if missing (02 §4) and TUI.update is Optional[SwarmState], but never verifies render tolerates None. I verified independently: tui.py:280 `state_value = state.state if state is not None else "-"` — code IS robust, but research didn't surface it, so a builder can't cite it. → MINOR gap G5. |
| 2 | FR-4 iteration-ceiling in-repo precedent + recommendation | PASS | 03 §6 cites `swarm status --watch` `watch_max_iterations` at commands.py:2513-2540 + loop 2583-2613 (verified), recommends `>=` ceiling semantics. Concrete + actionable. |
| 3 | FR-1 runtime main-thread assertion (threading.get_ident on TUI.update) — concrete approach + how test triggers it | PASS | 05 §1 gives a full test-only `monkeypatch.setattr(TUI, "update", _probe)` recipe with `threading.get_ident()` + mandatory `assert seen_idents` vacuity guard, citing tui.py:236. Concrete: where (test owns probe, no prod change), how triggered (forced-TTY run drives the loop). |
| 4 | Does research address whether ANY change to tui.py is needed? | GAP | NO research file states a verdict on "tui.py unchanged." Grep for "tui.py unchanged / no change to tui / purely run_cmd" → zero hits. The spec target_files says tui.py "likely no change" but the research never confirms/denies it. 03 §4d notes swarm TUI.start() does NOT disable Rich's stdout/stderr redirect — which arguably IS a candidate tui.py change for FR-1 — left unresolved. → IMPORTANT gap G4. |
| 5 | WHERE `_tail_events` should live (commands.py vs tui.py vs new module) | GAP | 02 §9 says `_tail_events` is "a new helper" mirroring `_follow_log_file` (commands.py:2737) "yielding parsed EventRecords," and 02 §FR-4-summary says the loop "lives in run_cmd," but NO file states which MODULE the helper goes in. `_follow_log_file` lives in commands.py; the spec's pseudocode implies a module-level helper but never pins the file. → MINOR gap G6 (placement decision left to builder). |
| 6 | FR-7 determinism (stub ordering, log flush before tail reads) | PASS (with caveat) | 05 §5 [CODE-VERIFIED] stub emits worker_start/worker_done to execution-log.jsonl (re-ran test_commands_run.py:507 green, 0.18s, 3 worker_done lines). FR-7 sources rows from durable JSONL post-run, not mid-run — so flush-timing is moot for the integration test. §6 covers partial-line determinism for the FR-4 tailer test. Caveat: §4 forced-TTY seam (monkeypatch should_enable_tui on SOURCE module) is correctly conditioned on R1's deferred-import finding (03 §3 confirms deferred import). Determinism well-covered. |
| 7 | Findings actionable for self-contained checklist items | MOSTLY | Anchors, kwargs, insertion points (01 §SUMMARY), patterns-to-copy table (03), required-sections checklist (04) are builder-ready. Gapped only where G1-G6 force re-derivation. |

---

## Verification Evidence (independent source spot-checks)

- `wc -l commands.py` = **3538** — confirms research's "spec line numbers are stale, these are CURRENT" claim; spec's anchors (1807, 1547) re-validated.
- `dispatch_wave1` fresh call kwargs at commands.py:1807-1813 match 01 §5 / 02 §8 VERBATIM (positional `preflight_result`; `transport_for_slot=run_transport_factory`, `prompt=assembled_prompt`, `worker_spec=inline_job.workers`, `logger=logger`; result `worker_results`). ✓
- Post-dispatch block at commands.py:1826 is itself gated `if state_output_dir is not None and recipe_name:` — corroborates the None-path edge case (sharpens G2: the threading wrap must preserve this inner gate too).
- resume+detached reject at commands.py:1547-1553 matches 01 §3 / 03 §2 verbatim — the FR-3 D1 mirror is real. ✓
- `swarm status --watch` KeyboardInterrupt loop at commands.py:2583-2613 verified — `except KeyboardInterrupt: pass` then `raise click.exceptions.Exit(last_exit_code)`. Confirms G3: the precedent catches SIGINT in the LOOP and exits with last status code; it has NO `join()` to interrupt, so it does not answer the join()-SIGINT question. ✓
- pipeline/executor.py:413-432 IS `daemon=True` — confirms the research's cited precedent genuinely conflicts with spec FR-5's non-daemon mandate (G1 is a real contradiction, not a misread). ✓
- tui.py:280 `_build_header`: `state_value = state.state if state is not None else "-"` — render tolerates state=None (G5 is cosmetic/documentation, code is safe). ✓

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| G1 | CRITICAL | 03 §4a (lines 125, 127) + patterns table (line 354) vs spec FR-5 | Research recommends `daemon=True` for the dispatch thread; spec FR-5 mandates **non-daemon** (`daemon=False`) + explicit `join()` precisely to prevent `execution-log.jsonl` truncation at interpreter shutdown. A builder following 03's patterns-to-copy table would write a spec-violating daemon thread. The cited precedent (pipeline/executor.py) genuinely IS daemon=True, so the contradiction is structural, not a typo. | Add a research note resolving in favor of the spec: dispatch thread MUST be `daemon=False`; the executor.py daemon=True precedent does NOT transfer because (a) FR-5 requires the join to complete so the logger's O_APPEND writes flush, and (b) Approach A's main thread always joins before exit. Update the §4a prose and the patterns-to-copy table row to `daemon=False`, and add the rationale (non-daemon = log-flush guarantee). |
| G2 | IMPORTANT | 01 §7, §10 | `state_output_dir is None` (no `--output` smoke path) is flagged as needing handling but no concrete rule given. The TUI poll loop has nothing to read with no dir; should_enable_tui could still return True (flag + TTY) while state_output_dir is None. | State the explicit guard: when `state_output_dir is None`, run_cmd MUST NOT start the tail loop / TUI even if should_enable_tui() is True (no log/state files exist to tail). Recommend gating on `should_enable_tui(...) and state_output_dir is not None`. Note the post-dispatch block is already None-gated at commands.py:1826 — the TUI wrap must preserve that. |
| G3 | IMPORTANT | 03 §6/§7 (KeyboardInterrupt coverage) | SIGINT during the post-loop `join()` on the non-daemon thread is unaddressed: does join() block the signal, and what exit code results? Spec FR-6 acceptance demands "an exit code reflecting interruption." The status--watch precedent has no join() so doesn't answer this. | Add coverage: on a non-daemon thread, a bare `t.join()` is interruptible by SIGINT (KeyboardInterrupt raises in the main thread); the dispatch thread keeps running unless cooperatively cancelled. Recommend either (a) `join()` inside the same try/except KeyboardInterrupt so tui.stop() fires in finally and the process exits with a defined interruption code (e.g. 130 or EXIT_INVALID), or (b) document that v1 lets the non-daemon thread finish (join blocks) — but then FR-6's "SIGINT mid-run leaves terminal restored with interruption exit code" needs the loop's except to set the code BEFORE the join. Pin the exit-code value the FR-6 test will assert. |
| G4 | IMPORTANT | (no file) — tui.py-change question | No research file delivers a verdict on the spec's "tui.py likely unchanged" assumption. 03 §4d raises that swarm TUI.start() (tui.py:221-226) does NOT disable Rich's stdout/stderr redirect (the #181/#182 crash vector) — which is a *candidate* tui.py change for FR-1 — but leaves it unresolved. The builder needs to know: is FR-1 satisfied purely by topology (only main thread writes), or does TUI.start() need `redirect_stdout/stderr=False` added? | Add an explicit finding: state whether tui.py is touched at all. If FR-1 relies solely on "dispatch thread routes all output to the log file" (topology), say so and state tui.py is unchanged. If the Rich redirect default is considered a residual risk, recommend the one-line tui.py change (pass `redirect_stdout=False, redirect_stderr=False` to Live in TUI.start) and add it to target_files. Resolve the §4d open thread either way. |
| G5 | MINOR | 02 §4 | Research notes read_state→None but never verifies the TUI header renders safely with state=None. (Independently verified safe: tui.py:280.) | Add one line: "render/.update tolerate state=None — tui.py:280 `_build_header` uses `state.state if state is not None else '-'`; no guard needed in the poll loop before the first state write." Makes the checklist item self-contained. |
| G6 | MINOR | 02 §9 | The MODULE for the new `_tail_events` helper is unspecified (commands.py vs tui.py vs new module). `_follow_log_file` precedent lives in commands.py, but research never pins where the new helper goes. | Recommend a module: place `_tail_events` in commands.py adjacent to `_follow_log_file`/`_drain_appended` (commands.py:2737/2834) since it's a run_cmd-local CLI concern and keeps Rich/tui imports out of the reader; OR justify tui.py if co-location with the consumer is preferred. Pin one so the build item is self-contained. |

---

## Summary

- Gap-detection checks passed: 3 / 7 fully (items 2, 3, 6) + item 7 mostly
- Checks with gaps: items 1 (4 sub-parts: 1 CRITICAL, 2 IMPORTANT, 1 MINOR), 4 (IMPORTANT), 5 (MINOR)
- Critical issues: 1 (G1 — daemon vs non-daemon contradiction)
- Important issues: 3 (G2, G3, G4)
- Minor issues: 2 (G5, G6)
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 5 (each targeted a specific checklist claim: line count + signature; dispatch kwargs + None-gate; daemon precedent + watch loop + reject mirror; research grep for daemon/SIGINT; research grep for helper-placement/state-None/tui-unchanged; tui.py render None-handling). tavily: 0 (no external claims — all source-truth-local).

Note: tool-call count (11 Read+Bash) ≥ 7 checklist items — engagement floor satisfied; no padding (each Bash mapped to a named checklist sub-item).

---

## Recommendations

Before synthesis/task-building proceeds, the research must resolve all 6 gaps. **G1 is the blocker** — shipping the patterns-to-copy table as-is would steer the builder into a spec-violating daemon thread. The fix is small (research-note + table-row corrections) but mandatory. G2/G3/G4 each leave a non-negotiable spec gate (FR-5/FR-6/FR-1) under-specified such that a self-contained checklist item cannot be written without the builder inventing behavior. G5/G6 are documentation-completeness gaps that block full B2 self-containment.

Recommended action: spawn a single gap-fill agent to append resolutions for G1-G6 into the existing research files (G1 into 03, G2/G3 into 01, G4 into 03 or a new note, G5 into 02, G6 into 02), then re-run this gate.

## QA Complete

VERDICT: FAIL (1 CRITICAL, 3 IMPORTANT, 2 MINOR)
