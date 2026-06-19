# QA Report — Research Depth Review (swarm-tui-wiring)

**Topic:** Wire `--tui` into `superclaude swarm run` per Approach A
**Date:** 2026-06-18
**Phase:** research-depth (qualitative)
**Lens:** Is the research DEEP ENOUGH to write the code without re-reading source?
**Fix authorization:** false
**Stance:** ADVERSARIAL — assume research is superficial until proven otherwise

---

## Overall Verdict: PASS

The five assigned research files are deep enough to write the `--tui` wiring,
the `_tail_events` helper, both scope guards, and the FR-1/FR-4/FR-7 tests
**without re-reading source**. Every load-bearing claim I independently
re-verified against the actual code held. The research notably *self-corrected*
two stale spec claims (`from_json` location and the JSONL filename) by citing
real code — the opposite of the "lists symbols without understanding behavior"
shallowness the adversarial stance was hunting for.

---

## Depth-Checklist Results (the 7 lens questions)

| # | Depth question | Verdict | Evidence |
|---|----------------|---------|----------|
| 1 | run_cmd glue writable from research alone? | PASS | 01 §5/§6/§10 + the spec's worked `_worker`/`result_box`/`exc_box` block give the verbatim dispatch kwargs (1807-1813), the thread-wrapper shape, the join+re-raise ordering, and the exact insertion anchors. A builder can transcribe it. |
| 2 | Data flow traced end-to-end w/ byte-offset mechanics? | PASS | 02 §5/§9 + 03 §5 trace worker→`log_event`→`execution-log.jsonl`→seek/read/`\n`-split/buffer-partial→`from_json`→`_project_workers`→`TUI.update`→render. `_drain_appended` (commands.py:2834-2847) + sprint `_read_new_chunk`/`_process_chunk` are the concrete primitives to copy. |
| 3 | FR-5 result-box/exc-box + stop()-before-reraise concrete w/ in-repo precedent? | PASS | 03 §4a cites `pipeline/executor.py:413-432` (result-box + daemon + join, verified at 421/426/432) and explicitly flags it lacks an exc-box, prescribing the extension. 05 + 01 give the `tui.stop()`-then-`raise exc_box["e"]` ordering. |
| 4 | FR-1 audit concrete enough to write a non-vacuous test? | PASS | 05 §1 names the exact visitor to copy (`_ShellDispatchVisitor`/`_scan_module`/`_iter_swarm_py_sources`, test_concurrency_python_only.py:145-230, verified), the forbidden symbols, the mutation-guard to defeat vacuity, AND the `threading.get_ident()` runtime probe with the mandatory `assert seen_idents` vacuity guard. |
| 5 | FR-7 stub emission VERIFIED (not assumed)? forced-TTY target unambiguous? | PASS | 05 §5 traces `_run_worker` emission (dispatch.py:302/311, verified) and I **re-ran** `test_run_cmd_stub_transport_dispatches_workers_not_noop` → 1 passed 0.19s. Forced-TTY seam = monkeypatch `should_enable_tui` on the SOURCE module (deferred-import idiom), with the module-top fallback explicitly conditionalized. |
| 6 | Threading crash-class mechanics understood (won't reintroduce #181/#182/#184)? | PASS | 03 §4d quotes the sprint crash-probe (sprint/tui.py:108-128) and the load-bearing fact I verified: swarm `TUI.start()` (tui.py:221-226) does NOT disable Rich's default `redirect_stdout/stderr=True`, so FR-1's "dispatch output goes to the log file only" is the structural fix, not discipline. |
| 7 | Per-FR checklist items writable without opening commands.py/tui.py/dispatch.py? | PASS | 04 maps every new code element to a copy-from anchor + the MDTM Template 02 section rules; 01's "SUMMARY — exact insertion-point line anchors" is a builder-ready manifest. |

---

## Independent Verification Performed (adversarial — did NOT trust `[CODE-VERIFIED]` tags)

| Research claim | Independently checked | Result |
|---|---|---|
| commands.py = 3538 lines | `wc -l` | MATCH |
| Zero `TUI(`/`Live`/`should_enable_tui` in commands.py today (FR-1 vacuity) | grep | MATCH (no output) |
| `--detached` block 1452-1469; run_cmd sig 1471-1486 (detached@1484, guard@1485) | Read | MATCH verbatim |
| resume+detached reject 1547-1553 (the FR-3 D1 mirror) | Read | MATCH verbatim |
| `_resolve_input_mode` @1581; fresh `if detached:` @1589 returns @1607 | Read | MATCH |
| Logger construction 1732-1740, `execution-log.jsonl` literal @1733 | Read | MATCH verbatim |
| Fresh `dispatch_wave1` 1807-1813 verbatim kwargs, result name `worker_results` | Read | MATCH verbatim |
| `from_json` at **models.py:1820** NOT logging_.py:46 (logging_.py:46 = docstring) | grep + sed | MATCH — spec self-correction is CORRECT |
| `dispatch_wave1` signature FROZEN (AC-004) | Read 334-343 | MATCH verbatim |
| `_run_worker` emits worker_start@302 / worker_done@311 (FR-5/FR-7 trace) | Read 300-331 | MATCH — emission is real, not assumed |
| `TUI.start()` does NOT pass redirect_stdout/stderr (crash hazard) | Read 218-228 | MATCH — Rich default True applies |
| `TUI.stop()` idempotent (`if self._live is not None`) | Read 230-234 | MATCH |
| `_project_workers` skips wave_transition/terminal, folds worker_* | Read 145-189 | MATCH |
| Resume `dispatch_wave1` @2264-2268 (untouched, v1) | sed | MATCH verbatim |
| `read_state` → None on FileNotFoundError | Read 178-196 | MATCH |
| Byte-offset precedent `_drain_appended` seek/tell @2834-2847 | grep | MATCH |
| AST visitor `_ShellDispatchVisitor`/`_scan_module` @145-230 | grep | MATCH |
| Vacuous test early-return @578 (`TUI(` not in source) | Read 543-583 | MATCH — genuinely vacuous + weak substring check |
| **Stub test live-runnable** (FR-7 headline) | re-ran pytest | **1 passed 0.19s** |
| `from_json` on truncated line raises JSONDecodeError (FR-4) | live python probe | RAISED JSONDecodeError |
| `status --watch` ceiling `iterations >= ` @2603 + KeyboardInterrupt @2606 | grep | MATCH (and `>` vs `>=` divergence @2802 correctly noted by research) |
| pipeline executor result-box + daemon + join @421/426/432 | grep | MATCH |

**Zero discrepancies found between the research and the actual source.**

---

## Issues Found

None at CRITICAL/IMPORTANT severity. Two MINOR observations (non-blocking — they
are *acknowledged caveats already in the research*, recorded here for the builder):

| # | Severity | Location | Observation | Note |
|---|----------|----------|-------------|------|
| 1 | MINOR | 02 §9 / 05 §1 | `_tail_events` cannot literally reuse `_follow_log_file` (it prints to stdout) and the AST audit is per-file not whole-program. | Research already flags BOTH explicitly ("must be a new helper that yields parsed EventRecords"; "do not over-claim whole-program reachability… the runtime probe is the transitive backstop"). Honest, not a gap. |
| 2 | MINOR | 05 §4 | The forced-TTY monkeypatch target is *conditional* on whether the landed import is deferred (source-module patch) vs module-top (commands-module patch). | Research prescribes the deferred form (matches every other run_cmd collaborator) AND gives the fallback + a verify-after-landing instruction. The ambiguity is intrinsic to test-before-implement, correctly handled. |

Neither blocks per-item task authoring; both are surfaced *by the research itself* with the correct resolution, which is the mark of deep (not shallow) research.

---

## Self-Audit

**(a) Reliance list — items I did NOT independently re-verify (relied on research assertion):**
- 04 (MDTM Template 02 section line-numbers, e.g. PART 1 lines 85-145) — out of my depth-lens scope (template structure is rf-qa structural territory); I verified 04's *copy-from anchors* into source indirectly via the other four files.
- A handful of secondary line cites (e.g. tui.py:251 render, models.py:1209 EventRecord fields) — read in context during the signature greps but not byte-matched field-by-field.

**(b) Independent semantic checks (≥1 required) — where I did my own tool work:**
- Re-ran the FR-7 stub-emission test (`test_run_cmd_stub_transport_dispatches_workers_not_noop`) → green 0.19s, confirming worker rows are sourceable from the durable log (the single highest-risk depth claim).
- Live-probed `from_json` on a truncated string → confirmed `JSONDecodeError`, validating the FR-4 partial-line buffering requirement is load-bearing, not theoretical.
- Independently Read 11 source regions (commands.py ×5, tui.py ×3, dispatch.py ×2, state.py, models.py via grep) and grepped 6 precedent sites; every byte-anchor matched.

**Confidence:** Verified: 7/7 depth questions | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 11 | Grep/Bash: 8 (incl. 1 live pytest run + 1 live python probe) | Glob: 0
**Web research:** None required (all verification was local-source-bound). Tavily not invoked.

---

## VERDICT: PASS

---
