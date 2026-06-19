# Research Completeness Verification — swarm `--tui` wiring

**Analysis type:** completeness-verification
**Lens:** completeness (BREADTH — does every build-needed area have research coverage?)
**Topic:** Wire `--tui` into `superclaude swarm run` per Approach A (threaded dispatch + main-thread file-tailing poller)
**Driving spec:** `/config/workspace/IronClaude/.dev/brainstorms/swarm-tui-wiring/merged-requirements.md` (FR-1..FR-7)
**Date:** 2026-06-18
**Files analyzed:** 5 research files (01-run-cmd-seam.md, 02-reader-contracts.md, 03-patterns-conventions.md, 04-template-examples.md, 05-test-verification.md) + the driving spec
**Depth tier:** Standard/Deep (code wiring — exact line anchors + signatures expected)

---

## Methodology

Read each of the 5 assigned research files in full plus the driving spec. For each of the 7 FRs and each of the 5 extra criteria in the spawn brief, mapped which research file(s) provide actionable, builder-ready coverage. This is a BREADTH check: every area a builder needs to author per-item task instructions must have corresponding research. Evidence quality and depth noted but the gate question is "is there enough here to build each FR as a checklist item?"

No web research performed or required (all checks operate over on-disk research files and the spec).

---

## Per-FR Coverage Audit

| FR | Need (from spec) | Covered by | Status |
|----|------------------|-----------|--------|
| FR-1 | Single-writer Console topology + vacuous-test tightening (AST reachability audit) | 03 §4d (single-writer discipline + crash class) + 05 §1 (AST audit recipe, `_ShellDispatchVisitor` reuse, runtime `get_ident()` probe) + 02 §2 (TUI lifecycle, main-thread requirement) | PASS |
| FR-2 | INV-012 gate + non-TUI no-regression | 02 §1 (`should_enable_tui` semantics) + 05 §4 (INV-012 companion: zero-ANSI on non-TTY via `_assert_no_ansi`) + 01 §7 (gate must handle `state_output_dir is None`) | PASS |
| FR-3 | Scope guards (`--tui --detached` reject mirror; resume excluded) with exact line anchors | 01 §3 (verbatim resume+detached reject at 1547-1553) + 01 §10 (recommended insertion at 1581, suggested guard text) + 01 §9 (resume dispatch 2264 LEAVE UNTOUCHED) + 03 §2 (reject idiom + EXIT_USAGE) | PASS |
| FR-4 | Event/state read path: `read_state` + byte-offset tail of CORRECT jsonl + `from_json` import | 02 §4/§5/§7 (readers + filename + from_json location) + 02 §9 (`_follow_log_file`/`_drain_appended` byte-offset primitive) + 03 §5 (`_read_new_chunk`/`_process_chunk` partial-line idiom) + 03 §6 (poll loop + ceiling) + 05 §6 (partial-line exactly-once test recipe) | PASS |
| FR-5 | Thread exception not masked (stop() before re-raise) | spec impl shape (exc_box, re-raise AFTER stop) + 03 §4a (result-box + add exception-box, re-raise on main after join) + 01 §5 (worker wrapper closure, re-raise AFTER tui.stop) | PASS |
| FR-6 | Idempotent teardown on all exit paths (finally) | 03 §7 (`finally` teardown idiom, cleanup_audit/executor template + hardened sprint form) + 02 §2 (`stop()` idempotent, tui.py:230-234) | PASS |
| FR-7 | Forced-TTY run→tui integration test (≥1 worker row + stub event-emission feasibility) | 05 §2/§3/§4/§5 (forced-TTY seam, CliRunner scaffold, stub emission CODE-VERIFIED, ≥1 worker row recipe) + 02 §3 (`_project_workers` non-vacuous-row definition) | PASS |

**All 7 FRs have actionable, builder-ready research coverage.**

---

## Extra-Criteria Coverage (spawn-brief checklist 1–5)

### Criterion 1 — Exact insertion points in commands.py (CURRENT line numbers)

**PASS.** Research 01 provides every insertion point the brief enumerates, with CURRENT (re-read 2026-06-18) line numbers and an explicit note that the spec's numbers are stale:

| Insertion point | Anchor (current) | Evidence |
|---|---|---|
| `--tui` Click option | after `commands.py:1469` (end of `--detached`), before `@auto_inject_guard_option` (1470) | 01 §1, §SUMMARY-1 |
| `tui: bool` signature param | between `detached:` (1484) and `auto_inject_guard:` (1485) | 01 §2, §SUMMARY-2 |
| `--tui --detached` reject guard | `commands.py:1581` (after `_resolve_input_mode`, before `if detached:` at 1589) | 01 §10, §SUMMARY-4 |
| dispatch call to thread-wrap | `commands.py:1807-1813` (verbatim kwargs given) | 01 §5, §SUMMARY-5 |
| post-dispatch continuation | first active line `commands.py:1826` (normalize/reduce 1827-1893; EXIT_OK 1912) | 01 §6, §SUMMARY-6 |

All five brief-named seams (option, signature, reject guard, dispatch call, post-dispatch continuation) are present with current anchors. The verbatim `dispatch_wave1` kwargs are recorded (positional `preflight_result`; `transport_for_slot=run_transport_factory`, `prompt=assembled_prompt`, `worker_spec=inline_job.workers`, `logger=logger`; result name `worker_results`) so the C3 no-signature-change constraint is buildable. The `state_output_dir is None` smoke-path edge (01 §7) is flagged for the gate — a real builder trap, well covered.

### Criterion 2 — execution-log.jsonl vs event-log.jsonl discrepancy resolved with CODE-VERIFIED verdict

**PASS.** Resolved decisively in TWO research files with a CODE-VERIFIED verdict and an explicit `[CODE-CONTRADICTED]` tag on the stale name:
- 02 §7 (and TL;DR #2): `execution-log.jsonl` is the real write path **[CODE-VERIFIED]** (`commands.py:1733` literal `manifest_dir / "execution-log.jsonl"` + reader const at `commands.py:99` + test fixture `test_dual_log_emission.py:69,88`). `event-log.jsonl` is **[CODE-CONTRADICTED]** — docstring-only (`logging_.py:7,44,92`; `models.py:1219`), zero write-path/constant hits.
- 05 §5 step 1 independently corroborates `<output>/execution-log.jsonl` via the live call chain and a green re-run of `test_run_cmd_stub_transport_dispatches_workers_not_noop`.

Note: the **spec itself uses the stale `event-log.jsonl`** in FR-4 prose and the impl-shape comment. Research 02/05 correctly OVERRIDE the spec with code evidence and instruct `_tail_events` + the FR-7 test to point at `execution-log.jsonl`. This is the single most important discrepancy for a builder and it is airtight.

### Criterion 3 — from_json import source resolved

**PASS.** Resolved with a `[CODE-CONTRADICTED]` on the spec's claim:
- Spec/impl-shape and FR-4 reference `from_json` at `logging_.py:46`. 02 §5 + TL;DR #1: **WRONG** — true definition is `src/superclaude/cli/swarm/models.py:1820` `def from_json(cls: Type[T], payload: str) -> T`. `logging_.py` imports only `to_json` and `logging_.py:46` is a docstring line. Exact import line given: `from superclaude.cli.swarm.models import EventRecord, from_json`; usage `from_json(EventRecord, line)`.
- Independently corroborated by 05 §5 note + §6 (test_logging.py:57,83 precedent; test_dual_log_emission.py:41,115,215). There is NO `EventRecord.from_json` classmethod — module-level function only. Fully buildable.

### Criterion 4 — Template 02 rules + POST reflect gate item shape documented

**PASS.** Research 04 is comprehensive:
- Template 02 identified as the correct template (`.claude/templates/workflow/02_mdtm_template_complex_task.md`), PART 1 (instructions) vs PART 2 (skeleton) split, with Sections A/B/C/D/E/I/L/M summarized and the required-sections checklist (lines 161-184).
- B2 six-element self-contained-item contract, M3 8-step lens gate, I19/I22 agent floors, I20 serialized fix, D3 anti-orphaning all captured.
- POST reflect-gate item shape (04 final section) given verbatim with the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard and `superclaude reflect run <task-file> --depth deep --fix --promote`, exit-0-only gate semantics, and the explicit prohibitions. Correctly notes this task has NO `spec_path` → PRE reflect skipped, POST reflect required.
- Two prior task-folder examples (A: pr167-verdict-regex code+test+reflect with `QA_GATE_REQUIREMENTS: NONE` waiver precedent; B: adversarial rf-qa gates) give the builder a real-world QA-shape decision.

### Criterion 5 — Any area lacking actionable research for a builder?

**No CRITICAL or IMPORTANT gap.** Every FR and every brief criterion maps to concrete, cited, mostly CODE-VERIFIED research. See Minor observations below for non-blocking notes.

---

## Evidence Quality

| File | Evidenced claims | Unsupported claims | Rating |
|------|-----------------|-------------------|--------|
| 01-run-cmd-seam.md | Pervasive `commands.py:NNN` anchors, verbatim code blocks, current line numbers re-read 2026-06-18 | None material | Strong |
| 02-reader-contracts.md | Every signature file:line; 2 discrepancies tagged `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]` with corroboration | None | Strong |
| 03-patterns-conventions.md | Every idiom cites file:LINE with copy-from template; patterns-to-copy summary table | None | Strong |
| 04-template-examples.md | Template line-ranges, section IDs, two real prior-task paths | None | Strong |
| 05-test-verification.md | Live re-run proof (0.18s green), `[CODE-VERIFIED]` on stub emission, AST visitor anchors | 1 self-tagged `[UNVERIFIED]` (whole-program AST walk feasibility — correctly scoped, backstopped by runtime probe) | Strong |

All five files carry `Status: Complete` with summary/TL;DR sections and embedded gaps/coordination notes. Evidence density is high and consistent with a Deep-tier code-wiring investigation.

---

## Documentation Staleness Check

The spec (`merged-requirements.md`) is itself the primary stale-doc source, and the research correctly cross-validated against code rather than trusting it:

| Spec claim | Verification tag in research | Status |
|---|---|---|
| `from_json` at `logging_.py:46` | `[CODE-CONTRADICTED]` → `models.py:1820` (02 §5) | Surfaced + corrected |
| `event-log.jsonl` (FR-4 prose + impl shape) | `[CODE-CONTRADICTED]` → `execution-log.jsonl` (02 §7, 05 §5) | Surfaced + corrected |
| commands.py line numbers (1807, 1547, 2264) | "spec's numbers are stale" → current numbers re-read (01 header + §) | Surfaced + corrected |

No doc-sourced architectural claim is reported as current fact without a code verdict. No `[CODE-CONTRADICTED]` claim is left unflagged. This is exemplary stale-doc handling.

---

## Contradictions Between Research Files

**None.** The files are mutually consistent and explicitly cross-reference each other (02 ↔ 01 on filename/dir; 05 ↔ 02 on `from_json`/filename; 05 ↔ 01 on the deferred-import seam for the FR-7 monkeypatch target; 03 ↔ 01 on insertion anchors). Where one file defers to another's deliverable (e.g. 05 §6 defers the reader API to 02's "R2" track; 05 §4 conditions the monkeypatch target on 01's import-style finding), the hand-off is named and consistent. The filename and `from_json` resolutions agree across 02 and 05 to the exact line.

---

## Depth Assessment

**Expected:** Deep tier — exact insertion anchors, verbatim signatures, idiom templates, test recipes.
**Achieved:** Meets Deep tier. Data-flow trace present (05 §5 stub→logger→dispatch→`_run_worker`→log_event chain), integration-point mapping present (01 seam map, 02 reader contracts), pattern analysis present (03 copy-from table). A live test was actually executed (05, 0.18s green) — exceeding typical research rigor.
**Missing depth elements:** None blocking.

---

## Compiled Gaps

### Critical Gaps (block task-file build)
- None.

### Important Gaps (affect quality)
- None.

### Minor Gaps / Observations (non-blocking; builder should be aware)

1. **`_tail_events` is specified by idiom, not as a frozen API.** Research gives two valid byte-offset patterns to mirror — 02 §9 (`_drain_appended` rb/seek/tell at `commands.py:2834`) and 03 §5 (`_read_new_chunk`/`_process_chunk` line-buffer at `sprint/monitor.py:541-563`). Both are partial-line tolerant; 03's line-buffer form is the cleaner direct match for "buffer partial trailing line." 05 §6 names the reader as "R2's deliverable." There is no single canonical `_tail_events` signature handed to the builder — the builder must synthesize the helper from the idioms. This is acceptable for a "mechanical wiring" task (the idioms are concrete and proven) but the task file should pick ONE pattern explicitly rather than leave it open.

2. **FR-7 monkeypatch target is conditional on the landed import style.** 05 §4 recommends patching `should_enable_tui` on the SOURCE module (`superclaude.cli.swarm.tui`) assuming a deferred function-local import, with a documented fallback to patching `superclaude.cli.swarm.commands.should_enable_tui` if a module-top import is used. 03 §3 strongly favors the deferred-import idiom (matches every other `run_cmd` collaborator). The dependency is named and resolvable, but the task file must pin the import style as a build decision so the test target is unambiguous — the builder should make the FR-4 import-site item and the FR-7 test-target item reference the same chosen style.

3. **`watch_max_iterations`-style ceiling for the poll loop is optional per the spec** (FR-4: "an optional iteration ceiling"). 03 §6 supplies the exact in-file precedent (`status --watch` loop, `>=` ceiling at `commands.py:2583-2613`). Builder should decide whether to include the ceiling (recommended for test determinism per the precedent) — not a research gap, a design choice with research backing.

4. **M4 fidelity gate applicability** is correctly pre-resolved by 04 §M4 ("not applicable — code change, no consumed source documents"). No gap; noted so the builder records the waiver rather than omitting silently.

None of the above blocks per-item task creation; each is a "pick the documented option" decision, not missing research.

---

## Recommendations

1. **Proceed to task-file build.** All 7 FRs and all 5 brief criteria have actionable coverage.
2. In the task file, **pin the `_tail_events` pattern** to the 03 §5 line-buffer form (cleanest partial-line handling) in a single self-contained build item citing `sprint/monitor.py:541-563`.
3. **Pin the import style to deferred function-local** (`from superclaude.cli.swarm.tui import TUI, should_enable_tui` inside `run_cmd`) so the FR-7 monkeypatch target is unambiguously `superclaude.cli.swarm.tui.should_enable_tui` (matches 03 §3 idiom + 05 §4 recommendation).
4. **Carry the spec-override notes forward verbatim** into the relevant build items: `execution-log.jsonl` (NOT event-log.jsonl) and `from_json` from `models.py` (NOT logging_.py) — these are the two places a builder working from the spec text alone would go wrong.
5. Use current commands.py anchors from 01 (NOT the spec's stale numbers); have the build items re-verify anchors against the file at edit time since this is a 3538-line file under active development.

---

## VERDICT: PASS

All seven functional requirements (FR-1..FR-7) and all five extra spawn-brief criteria have actionable, builder-ready research coverage. The two highest-risk discrepancies — `execution-log.jsonl` vs `event-log.jsonl` and the `from_json` source — are resolved with explicit CODE-VERIFIED / CODE-CONTRADICTED verdicts and independent corroboration across files 02 and 05. All commands.py insertion points carry current (re-read 2026-06-18) line anchors. Template 02 rules and the POST reflect-gate item shape are fully documented. No contradictions between research files. No critical or important gaps. Four minor observations are "pick the documented option" decisions, not missing research, and are captured as recommendations for the builder.

**Gap count: 0 critical, 0 important, 4 minor (non-blocking).**
