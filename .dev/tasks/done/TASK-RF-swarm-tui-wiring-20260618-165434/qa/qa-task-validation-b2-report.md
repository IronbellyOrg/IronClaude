# QA Report — Task Integrity Check (B2 Self-Containment Lens)

**Topic:** Wire `--tui` into `superclaude swarm run` (Approach A)
**Date:** 2026-06-18
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

Five issues found. Four are MINOR/IMPORTANT B2-self-containment defects; one (FR-3
resume-rejection coverage) is IMPORTANT. The task is overwhelmingly well-formed against
the B2 contract — every item carries context + action + output + verification + completion
gate, every command is fully embedded, and every stale-spec reference was correctly
corrected — but the issues below must be resolved (zero-tolerance gate: any gap = FAIL).

---

## Adversarial-stance note

This task file is unusually high-quality for the B2 lens: it is the rare case where the
self-containment discipline is genuinely strong. I therefore checked HARDER on the two
places where a defect is most likely to hide: (a) spec-coverage completeness vs the 7 FRs,
and (b) the exact frozen-call kwargs / stale-name corrections. The findings below are the
result of that targeted scrutiny, not a generic skim.

---

## Verification evidence (source-truth-first)

| Claim checked | Tool | Result |
|---|---|---|
| Frozen `dispatch_wave1` signature | `sed dispatch.py:334-343` | positional `preflight_result`, `transport=None`, kw-only `transport_for_slot`/`prompt`/`parallel_executor`/`worker_spec`/`logger` → list[WorkerResult]. Matches task's frozen claim. |
| Fresh-run call-site kwargs | `sed commands.py:1807-1813` | `dispatch_wave1(preflight_result, transport_for_slot=run_transport_factory, prompt=assembled_prompt, worker_spec=inline_job.workers, logger=logger)` → **EXACT match** to the kwargs the threaded-glue item (Step 2.5) and Step 1.3 embed. CONFIRMED. |
| `from_json` location | `grep models.py` | `from_json` at `models.py:1820` — NOT `logging_.py:46`. Task correctly targets `models.py:1820`. CONFIRMED stale-name correction. |
| `from_json(EventRecord, line)` call shape | `grep from_json( usages` | signature is `from_json(cls, payload)`; all repo callers pass `from_json(Manifest, payload)` etc. → `from_json(EventRecord, line)` is the CORRECT call shape. CONFIRMED. |
| Log filename | `grep commands.py` | `EXECUTION_LOG_JSONL_FILENAME = "execution-log.jsonl"` at :99; dispatch writes `manifest_dir / "execution-log.jsonl"` at :1733. NO `event-log.jsonl` in source. Task correctly targets `execution-log.jsonl`. CONFIRMED stale-name correction. |
| Spec staleness | `Read merged-requirements.md` | Spec FR-4 references `event-log.jsonl` and `from_json(...) (logging_.py:46)` — BOTH STALE. Task's Key-Constraints block flags both as `[CODE-CONTRADICTED]`/STALE and overrides them. CONFIRMED — no stale propagation into items. |
| `_drain_appended`/`_follow_log` precedent | `grep commands.py` | `_follow_log` @2737, `_drain_appended` @2834. Task Step 2.4 cites `_follow_log` (correct name) and notes research mislabel `_follow_log_file` was fixed in G6. CONFIRMED. |
| Vacuous FR-1 audit | `sed test_inv012:543-583` | `test_commands_module_does_not_construct_tui_outside_gate` returns early at `if "TUI(" not in source: return`. Step 3.1's "vacuous early-return" characterization is ACCURATE. CONFIRMED. |
| `_run_worker` location | `grep dispatch.py` | `def _run_worker` @ dispatch.py:279 — Step 3.1's claim that `_run_worker` lives in dispatch.py is CONFIRMED. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Key Objectives §2 / Step 2.3 / spec FR-3 | **FR-3 is split across the spec into TWO acceptance criteria** — `--tui --detached` reject AND `--tui` on a resume/non-fresh invocation reject. The task implements ONLY the `--tui --detached` reject (Step 2.3). The resume-`--tui` reject is scoped OUT ("resume call site LEFT UNTOUCHED in v1"). Consequence: a user passing `--tui` on a resume run gets a silent no-op (no TUI, no error), violating FR-3's second acceptance bullet ("both invocations exit with UsageError naming the incompatibility"). This is a real spec-coverage gap, NOT just a B2 phrasing issue — and per lens item 6 (each FR element its own item) the missing FR-3b element has no item at all. | Either (a) add a Step 2.3b item that rejects `--tui` on a resume/non-fresh invocation with a UsageError before the resume `dispatch_wave1` at ~2264 (preferred — closes FR-3), or (b) if v1 truly defers it, the scope note must be promoted into the task's Open-Questions / Follow-Up and the FR-3 acceptance contract explicitly amended so a later auditor does not read FR-3 as fully satisfied. As written, the task claims to "implement FR-1..FR-7" (description line 4) while silently dropping half of FR-3. |
| 2 | MINOR | Step 2.5 | **Largest item; borderline self-containment via embedding 5 sub-clauses (a)-(e).** The single item embeds: closure-on-thread, gated poll loop, TUI deferred imports, finally-teardown, exception re-raise, AND the byte-identical fallback. It is self-contained (all context+action+verification present) and atomic to ONE refactor site, so it does not fail B2 outright — but it is the one item that a reader cannot execute "without scrolling" (lens item 10 / atomicity reference). The (a)-(e) lettering is the only thing keeping it parseable. | Acceptable to keep as one item given it is a single indivisible refactor of one call site, but flag for the executor: if any sub-clause (a)-(e) cannot land atomically, the verification ("post-dispatch continuation runs ONLY after join + re-raise") is the gate. No structural rewrite required; documenting as a known density hot-spot. |
| 3 | MINOR | Step 3.2, 3.4, 3.5, 3.6, 3.8 | **Output file path is conditional / "or the FR-7 file if cleaner" / "<chosen file>".** Several test items leave the destination test file ambiguous (`tests/swarm/<chosen file>`, "or the FR-7 file if cleaner", "or appended to an existing swarm test file"). The verification capture path IS fixed (e.g. `fr2-noregression.txt`), so the item is verifiable, but lens item 4 (file paths specific, not "the relevant file") is partially violated for the SOURCE test file. | Pin each new test to a named file (e.g. Step 3.4 → `tests/swarm/test_run_tui_noregression.py`). Low risk because the pytest capture target is concrete, but the executor currently has discretion that could fragment the suite. |
| 4 | MINOR | Step 3.2 / Step 3.7 | **Branch instruction "(or the FR-7 file if cleaner)" + Step 3.7 patch-target conditional ("if Step 2.5 used a module-top import instead, patch `...commands.should_enable_tui`").** These are correct defensive instructions (the monkeypatch target depends on whether the import is deferred or module-top), and they DO restate both branches inline (so they are self-contained), but they make the verification criterion conditional on a Phase-2 decision not yet pinned. | Acceptable — the conditional is fully restated inline (both patch targets named), so B2 self-containment holds. Noted only because lens item 5 (measurable verification) is weakened when the assertion target is "whichever import style landed". The item correctly handles it; no fix mandatory. |
| 5 | MINOR | Step 2.4 vs Step 3.3 `from_json` call shape | **No defect — verified clean.** Both items use `from_json(EventRecord, line)`. I flagged this for scrutiny because the source signature is `from_json(cls, payload)` and a naive reading could mistake `EventRecord` for an instance. Confirmed against repo usage (`from_json(Manifest, payload)` everywhere) that `from_json(EventRecord, line)` is the CORRECT class-first call shape. Listing here as an explicitly-cleared adversarial check, not an open issue. | None — cleared. |

---

## Lens checklist results (B2 self-containment, 7 items)

| # | Lens check | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Every item has all 5 B2 components | PASS | Every `- [ ]` item carries: context (Read X / prior research §), action (add/insert/run), output (file path or edit), verification ("ensuring ..."), and completion gate ("This item cannot be marked as done until ... Once done, mark this item as complete."). Verified across all 23 items. |
| 2 | No item references prior context without restating | PASS | Items that depend on earlier work (3.1 reads `wiring-inventory.md`; 2.6 reads "poll loop added in 2.5"; 3.8 reads `frozen-signatures.md`) all RESTATE the needed anchor inline and name the source file by absolute path. No bare "see above". |
| 3 | Spawning/command items fully embed the command | PASS | Every Bash item embeds the exact `cd /config/workspace/IronClaude && uv run pytest ... 2>&1`, `uv run ruff check ...`, `uv run ruff format --check src/ tests/`, `git diff 300c06a6... -- ...`, and the full reflect-wrapper shell-out with the recursion-breaker guard. No "run the tests". |
| 4 | File paths specific | PARTIAL → see Issue #3 | Production/research/capture paths are absolute and exact. SOURCE test-file destinations for 3.2/3.4/3.5/3.6/3.8 are left as `<chosen file>`. |
| 5 | Verification measurable | MOSTLY PASS → see Issue #4 | Verifications are concrete (exit code, pass count ≥ baseline, zero ANSI, idempotent stop, exactly-once delivery). One conditional (3.7 patch target) is fully restated inline. |
| 6 | No batch items — each FR/element its own item | PARTIAL → see Issue #1 | Each FR test IS its own item (FR-1 audit 3.1, FR-1 runtime 3.2, FR-2 3.4, FR-4 3.3, FR-5 3.5, FR-6 3.6, FR-7 3.7, no-sig-change 3.8). `--tui` option (2.1), param (2.2), reject (2.3), `_tail_events` (2.4), threaded glue (2.5), main-thread assertion (2.6) each distinct. **BUT FR-3b (resume reject) has no item.** lint (4.1), format-check (4.2), full-suite (4.3), signature-diff (4.4) each distinct. |
| 7 | No stale-spec propagation (`execution-log.jsonl` not `event-log.jsonl`; `models.py` not `logging_.py`) | PASS | CRITICAL check. Spec FR-4 is stale (`event-log.jsonl`, `logging_.py:46`). Task Key-Constraints (line 138) flags BOTH as `[CODE-CONTRADICTED]`/STALE and every item targets `execution-log.jsonl` + `from superclaude.cli.swarm.models import EventRecord, from_json`. Source-verified: filename @ commands.py:99/1733, from_json @ models.py:1820. NO stale name appears in any item. |

### Frozen-call-kwargs confirmation (lens-mandated)

CONFIRMED. Step 1.3, Step 2.5, and Step 3.8 all reference the frozen call as
`dispatch_wave1(preflight_result, transport_for_slot=run_transport_factory,
prompt=assembled_prompt, worker_spec=inline_job.workers, logger=logger)` with result name
`worker_results` — byte-matching the live call site at commands.py:1807-1813. No item
instructs changing `dispatch_wave1`/`ParallelExecutor` signatures; Phase-2 header and Key
Constraints both FREEZE them, and Step 4.4 adds a `git diff` proof + Step 3.8 adds an
`inspect.signature` pin. The poll loop lives in the caller (`run_cmd`), not in
`dispatch_wave1`. PASS.

---

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 4 (grep/sed via Bash)
- All 7 lens-checklist items verified with source-truth tool evidence (signatures, filenames, call site, vacuous-test body all read directly from source). Tool-call count (7 Read/Bash) ≥ 7 checklist items — engagement minimum met.

---

## Summary

- Lens checks passed: 5/7 fully PASS, 2 PARTIAL (items 4 and 6)
- Issues: 5 found (1 IMPORTANT, 4 MINOR — one MINOR is a cleared adversarial check)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Recommendations (before execution)

1. **Resolve Issue #1 (FR-3 resume reject)** — add a Step 2.3b resume-`--tui` reject OR
   amend the FR-3 acceptance contract + promote the deferral to Follow-Up. The task
   currently claims "Implements FR-1..FR-7" while dropping FR-3's second acceptance bullet.
2. **Pin the ambiguous test-file destinations (Issue #3)** so the suite does not fragment.
3. Issues #2, #4, #5 require no action (documented density hot-spot / correctly-handled
   conditional / cleared adversarial check).

## QA Complete

---

VERDICT: FAIL
