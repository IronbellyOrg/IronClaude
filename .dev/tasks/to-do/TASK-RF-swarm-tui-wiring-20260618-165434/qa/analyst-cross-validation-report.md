# Cross-Validation Report — swarm `--tui` wiring research

**Topic:** Wire `--tui` into `superclaude swarm run` (Approach A)
**Date:** 2026-06-18
**Lens:** Cross-validation (claims BETWEEN research files must agree)
**Files analyzed:** 01-run-cmd-seam.md, 02-reader-contracts.md, 03-patterns-conventions.md, 04-template-examples.md, 05-test-verification.md
**Spec:** /config/workspace/IronClaude/.dev/brainstorms/swarm-tui-wiring/merged-requirements.md

---

## Methodology

Each cross-check below names an anchor that two or more research files touch. For each, I record what each file claims, whether they agree, and (where contested) the result of a spot-verification against the actual source.

---

## Checklist 1 — Same-anchor line-number agreement across files

### 1a. dispatch_wave1 fresh call site (R1: commands.py:1807-1813)

| File | Claim | Agrees? |
|---|---|---|
| R1 §5 / SUMMARY #5 | fresh `dispatch_wave1` at 1807-1813; verbatim kwargs `transport_for_slot=run_transport_factory, prompt=assembled_prompt, worker_spec=inline_job.workers, logger=logger`; result name `worker_results` | — |
| R2 §8 | does not give the call-site line; cites dispatch.py:334 signature (FROZEN) — complementary, not conflicting | AGREE (no conflict) |
| R3 §4a | "the work the dispatch thread wraps is the `dispatch_wave1(...)` call ... at commands.py:1807-1893" | AGREE |
| R5 §5 | "`run_cmd` calls `dispatch_wave1(..., logger=logger)` — commands.py:1807-1813" | AGREE |

**SPOT-VERIFIED:** `sed -n '1807,1813p'` confirms the call site, kwargs, and `worker_results` name EXACTLY as R1/R5 state. **CONSISTENT.**

### 1b. Logger filename + directory (R1: execution-log.jsonl at commands.py:1733; manifest_dir/state_output_dir)

| File | Claim | Agrees? |
|---|---|---|
| R1 §7 | `jsonl_path=manifest_dir / "execution-log.jsonl"` (1733), `md_path=...` (1734), `manifest_dir = Path(preflight_result.manifest_path).parent` (1730), `state_output_dir = manifest_dir` (1731) | — |
| R2 §7 | `commands.py:1733 jsonl_path=manifest_dir / "execution-log.jsonl"`; `manifest_dir` (1730) == `state_output_dir` (1731) | AGREE |
| R3 §5 | "the swarm log is `execution-log.jsonl` ... commands.py:1733" | AGREE |
| R5 §5 | `logger = _Logger(jsonl_path=manifest_dir / "execution-log.jsonl", ...)` commands.py:1727-1740; manifest_dir parent (1730) | AGREE |

**SPOT-VERIFIED:** `sed -n '1730,1734p'` confirms lines 1730 (manifest_dir), 1731 (state_output_dir), 1732 (`_Logger(`), 1733 (jsonl), 1734 (md). **CONSISTENT across all four files.**

### 1c. --tui option insertion point (R1: after :1469 / before @auto_inject_guard_option :1470)

| File | Claim | Agrees? |
|---|---|---|
| R1 §1 | insert after end of `--detached` block (commands.py:1469) and before `@auto_inject_guard_option` (1470) | — |
| R3 §1 / table | "place ABOVE `@auto_inject_guard_option` (`:1470`)" | AGREE |

**SPOT-VERIFIED:** `@auto_inject_guard_option` is at line 1470, `def run_cmd(` at 1471, `)` closing the `--detached` help at 1469. **CONSISTENT.**

> MINOR framing note (NOT a contradiction): R1 §1 labels the `--detached` block "1452-1469"; the literal `"--detached",` dest string is at line 1453 and `@click.option(` opens at 1452. R3 §1 labels it "1452-1469" too. Both agree on the END (1469) and the guard line (1470), which is the load-bearing anchor. The 1452-vs-1453 difference is just whether you count the `@click.option(` opener. No action needed.

### 1d. param insertion (R1: tui before auto_inject_guard at :1485)

| File | Claim | Agrees? |
|---|---|---|
| R1 §2 | insert `tui: bool,` between `detached: bool,` (1484) and `auto_inject_guard: bool,` (1485) | — |
| R3 §1 | "param `tui: bool` BEFORE `auto_inject_guard` (`:1485`)"; "`detached: bool,` at commands.py:1484" | AGREE |

**SPOT-VERIFIED:** `sed -n '1483,1486p'` → 1483 `force_relens: bool,`, 1484 `detached: bool,`, 1485 `auto_inject_guard: bool,`, 1486 `) -> None:`. **CONSISTENT.**

### 1e. resume+detached reject mirror (R1: commands.py:1547-1553)

| File | Claim | Agrees? |
|---|---|---|
| R1 §3 | reject at 1547-1553; `EXIT_USAGE`; verbatim `if detached: click.echo("swarm run --resume: ... mutually exclusive with --detached (...)", err=True); raise click.exceptions.Exit(EXIT_USAGE)` | — |
| R3 §2 | identical block quoted verbatim at commands.py:1547-1553, same `EXIT_USAGE` shape | AGREE (verbatim match) |

**SPOT-VERIFIED:** `sed -n '1547,1553p'` matches the quoted block in BOTH R1 and R3 byte-for-byte. **CONSISTENT.**

### 1f. should_enable_tui signature + monkeypatch target (R2: tui.py:74; patch on superclaude.cli.swarm.tui)

| File | Claim | Agrees? |
|---|---|---|
| R2 §1 | `should_enable_tui(flag: bool, stream: Optional[IO] = None) -> bool` at tui.py:74; gate = `--tui` AND TTY | — |
| R5 §4 | monkeypatch `should_enable_tui` on the **source module** `superclaude.cli.swarm.tui` (deferred import seam); `_FakeTTY` makes `should_enable_tui(True, _FakeTTY())` True | AGREE — R2 gives signature/location, R5 gives the patch target on the same source module |
| R3 §3 | deferred import `from superclaude.cli.swarm.tui import TUI, should_enable_tui` inside `run_cmd` body | AGREE — makes R5's source-module patch correct |

**SPOT-VERIFIED:** tui.py:74 = `def should_enable_tui(flag: bool, stream: Optional[IO] = None) -> bool:` EXACTLY. **CONSISTENT.** R3's deferred-import finding, R2's location, and R5's source-module patch target form a coherent chain (deferred import ⇒ patch the source module, not a commands re-export).

### 1g. from_json location (R2: models.py:1820)

| File | Claim | Agrees? |
|---|---|---|
| R2 §5 / TL;DR | `from_json` at **models.py:1820**; spec's `logging_.py:46` is WRONG; import `from superclaude.cli.swarm.models import EventRecord, from_json` | — |
| R5 §5 note | "Parse each JSONL line with `from_json(EventRecord, line)` (models.py:1820, module-level function — NO `EventRecord.from_json` classmethod)" | AGREE (identical line) |

**SPOT-VERIFIED:** `grep -n "def from_json"` → `1820:def from_json(...)`; `to_json` at 1810. **CONSISTENT.** R2 and R5 agree on 1820 and on the module-level-function (not classmethod) detail.

---

## Checklist 2 — The two [CODE-CONTRADICTED] discrepancies resolved consistently?

### 2a. Filename: event-log.jsonl (stale) vs execution-log.jsonl (real)

- **R2 §7 / TL;DR #2:** `execution-log.jsonl` is the real write path (commands.py:1733); `event-log.jsonl` is docstring-only (logging_.py:7,44,92; models.py:1219). [CODE-CONTRADICTED] for event-log.jsonl.
- **R1 §8 / §7:** uses `execution-log.jsonl` (const `EXECUTION_LOG_JSONL_FILENAME` at :99; write literal at :1733). Never mentions event-log.jsonl. CONSISTENT.
- **R3 §5:** "the swarm log is `execution-log.jsonl` ... commands.py:1733". CONSISTENT.
- **R5 §5 / TL;DR / final summary:** sources FR-7 worker rows from `<output>/execution-log.jsonl`; the existing test asserts on `execution-log.jsonl`. CONSISTENT.

**VERDICT: RESOLVED CONSISTENTLY across all 4 files that touch the filename.** No file references `event-log.jsonl` as a live write path. SPOT-VERIFIED: line 1733 literal = `"execution-log.jsonl"`.

### 2b. from_json location: logging_.py:46 (stale spec) vs models.py:1820 (real)

- **R2:** models.py:1820; logging_.py:46 is prose in a docstring; logging_.py imports only `to_json` (logging_.py:59). [CODE-CONTRADICTED] for logging_.py:46.
- **R5:** models.py:1820, module-level function. CONSISTENT.
- R1, R3, R4 do not touch `from_json` (out of their scope) — no conflict.

**VERDICT: RESOLVED CONSISTENTLY.** SPOT-VERIFIED: `def from_json` is at models.py:1820; not in logging_.py. The two files that touch it (R2, R5) agree exactly.

---

## Checklist 3 — Stub-transport event-emission (R5) consistent with EventRecord/_project_workers contract (R2)?

- **R5 §5:** stub emits `worker_start` (dispatch.py:302-308) and `worker_done` (dispatch.py:311-330) per slot; payload carries `status`, `model_id`, `model_label`, `elapsed_ms`; stub returns `status="success"`, `model_label="stub-model-00"`. Feeds non-vacuous `_project_workers` rows.
- **R2 §3 (_project_workers) + §6 (EventRecord):** `_project_workers` folds ONLY `worker_start`/`worker_progress`/`worker_done` (tui.py:160-165); a non-vacuous row needs a `status` other than default `"pending"` plus a populated `model_label`/`elapsed`; `model_label` read from `payload["model_label"]` or `payload["model_id"]`; `worker_done` reads `payload["elapsed_ms"]`; `wave_transition`/`terminal` (worker_index=None) are skipped.

**CONSISTENT — and mutually reinforcing.** R5's emitted-payload fields (`status`, `model_label`, `model_id`, `elapsed_ms` on `worker_done`; `worker_index=index`) are EXACTLY the fields R2 says `_project_workers` consumes to build a non-vacuous row. R5's note that `wave_transition` events (worker_index=None) are "correctly skipped by `_project_workers`" matches R2 §3's drop rule (tui.py:157-159) verbatim. The stub's `status="success"`/`model_label="stub-model-00"` clears R2's non-vacuous bar (status ≠ "pending", model_label populated). **No contradiction; the two contracts dovetail.**

---

## Checklist 4 — Byte-offset tail idiom: R2 (_follow_log/_drain_appended) vs R3 (sprint/monitor.py:504-563)

Both cite a real, valid byte-offset tail pattern; they are **complementary templates, not contradictory.** Comparison:

| Aspect | R2's candidate (swarm `commands.py`) | R3's candidate (sprint/cleanup_audit `monitor.py`) |
|---|---|---|
| Location | `_follow_log` 2737 + `_drain_appended` 2834 (in `commands.py`, same file as the wiring) | `sprint/monitor.py:504-563` (twin at `cleanup_audit/monitor.py:134-156`) |
| Offset tracking | `last_pos` seeded `len(existing.encode())`; `seek`/`read`/`tell` | `_last_read_pos`; `stat().st_size` gate → `seek`+`read(size-last_pos)` |
| Partial-line handling | uses `errors="replace"` (lossy); R2 itself notes this is NOT ideal and recommends tracking offset to last `\n` | explicit `_line_buffer` carries the trailing partial across polls (the correct partial-tolerant idiom) |
| Output target | **prints to stdout** (CLI `logs --follow` surface) — R2 explicitly says it "cannot reuse it as-is" | parses NDJSON into structured events; no stdout coupling |

**R2 and R3 AGREE that:** the byte-offset/seek/tell/truncation-restart skeleton is the proven pattern to mirror; neither helper is reusable verbatim (R2's prints to stdout; R3's parses generic NDJSON, not EventRecord).

**Which is the better mirror?** R3's `monitor.py` pair is the better template for FR-2/FR-4 because it implements the **partial-trailing-line buffer** (`_line_buffer = lines[-1]`, parse `lines[:-1]`) that R5 §6 proves is REQUIRED (a fragment fed to `from_json` raises `json.JSONDecodeError`). R2's `_follow_log` uses lossy `errors="replace"` and R2 itself flags that as inadequate for the partial-line requirement. **R5 §6's truncation finding independently confirms R3's buffer approach is the correct one.** R2's value-add is that `_drain_appended` lives in the SAME file (`commands.py`) so it documents the in-file precedent; R3's value-add is the correct partial-line semantics. Recommendation for the builder: adopt R3's `monitor.py` `_read_new_chunk`/`_process_chunk` partial-line buffer shape, located in `commands.py` alongside the wiring (acknowledging R2's `_drain_appended` as the in-file sibling).

**No contradiction.** Both valid; R3's is the better structural mirror, corroborated by R5 §6.

> **MINOR symbol-name discrepancy (flag, low severity):** R2 §9 and its summary table name the function **`_follow_log_file`** at commands.py:2737. The ACTUAL function name is **`_follow_log`** (SPOT-VERIFIED: `grep -n "_follow_log"` → `2737:def _follow_log(`; there is no `_follow_log_file` symbol). The line number (2737) and `_drain_appended` (2834) are correct; only the symbol name has a spurious `_file` suffix. The builder must use `_follow_log`, not `_follow_log_file`, if referencing it. Does not affect R3's (better) recommendation.

---

## Checklist 5 — Any claim in one file refuted by another?

No outright refutations found. All overlaps are either agreement or complementary coverage. Cross-file relationships that strengthen (rather than conflict):

- **R3 (deferred import) ⟷ R5 (source-module monkeypatch target):** R3 establishes `run_cmd` uses a deferred function-local import; R5 relies on exactly that to justify patching `superclaude.cli.swarm.tui.should_enable_tui` (source module). R5 §4 even adds the correct caveat: IF the wiring lands as a module-top import, the target becomes `superclaude.cli.swarm.commands.should_enable_tui`. The two are coordinated, not conflicting.
- **R1 §10 (--tui --detached reject at :1581) ⟷ R3 §2 (reject idiom):** R1 recommends the reject at 1581 (after `_resolve_input_mode`, before `if detached:` at 1589); R3 supplies the verbatim idiom shape (EXIT_USAGE, err=True). SPOT-VERIFIED: `_resolve_input_mode` call at 1581, `if detached:` fresh branch at 1589 with `return` at 1607. CONSISTENT.
- **R5 §5 (stub emits to execution-log.jsonl via logger wired at 1727-1740, dispatch at 1807) ⟷ R1 §5/§7:** identical call-site and logger anchors.
- **R4 (template/MDTM):** orthogonal domain (task-file structure); no symbol/line overlap with R1/R2/R3/R5, so no cross-validation surface. Internally consistent; no conflicts with the code-anchor files.

---

## Cross-Validation Summary Table

| # | Anchor | Files | Result | Spot-verified |
|---|--------|-------|--------|---------------|
| 1a | dispatch_wave1 fresh @1807-1813 | R1,R3,R5 | AGREE | YES |
| 1b | Logger jsonl @1733 / manifest_dir==state_output_dir @1730-1731 | R1,R2,R3,R5 | AGREE | YES |
| 1c | --tui option after :1469, before guard :1470 | R1,R3 | AGREE | YES |
| 1d | tui param before auto_inject_guard :1485 | R1,R3 | AGREE | YES |
| 1e | resume+detached reject @1547-1553 (EXIT_USAGE) | R1,R3 | AGREE (verbatim) | YES |
| 1f | should_enable_tui @tui.py:74; patch source module | R2,R3,R5 | AGREE | YES |
| 1g | from_json @models.py:1820 | R2,R5 | AGREE | YES |
| 2a | filename: execution-log.jsonl (event-log stale) | R1,R2,R3,R5 | RESOLVED CONSISTENT | YES |
| 2b | from_json: models.py:1820 (logging_.py:46 stale) | R2,R5 | RESOLVED CONSISTENT | YES |
| 3 | stub emission ⟷ _project_workers contract | R2,R5 | CONSISTENT (dovetail) | partial (payload fields) |
| 4 | byte-offset tail: _follow_log vs monitor.py | R2,R3 | COMPLEMENTARY; R3 better mirror | YES |
| 5 | cross-file refutations | all | NONE | — |

**Contradictions found:** 0 (zero) that affect correctness.
**Minor discrepancies found:** 2 (both low-severity, documented below).

---

## Findings list (severity-rated)

### MINOR-1 — R2 symbol-name error: `_follow_log_file` should be `_follow_log`
- **Severity:** MINOR (does not change line numbers or the recommendation; R3's template is the one to adopt anyway).
- **Source:** R2 §9 + R2 summary table.
- **Evidence:** `grep -n "_follow_log"` → `2737:def _follow_log(`; no `_follow_log_file` symbol exists. Line 2737 and `_drain_appended`@2834 are correct.
- **Fix:** In the task file, if `_follow_log` is referenced as a precedent, use the correct name `_follow_log` (drop the `_file` suffix). Or simply prefer R3's `monitor.py` template, which sidesteps this entirely.

### MINOR-2 — R1 `--detached` block start framing (1452 vs 1453)
- **Severity:** MINOR (cosmetic; both R1 and R3 use "1452-1469" and agree on the END anchor 1469 + guard 1470, which is what the insertion depends on).
- **Source:** R1 §1, R3 §1.
- **Evidence:** `@click.option(` opens at 1452; the `"--detached",` dest literal is at 1453. The block END (1469) and `@auto_inject_guard_option` (1470) are exact.
- **Fix:** None required — the insertion point ("after 1469, before 1470") is unambiguous and correct.

### No CRITICAL or IMPORTANT cross-validation gaps.
The two stale-doc discrepancies the spec carried (`event-log.jsonl`, `from_json`@logging_.py:46) are resolved identically in every file that touches them, and the high-risk stub-emission claim (R5) is fully consistent with the reader contract (R2). The five files form a coherent, mutually-corroborating set with no conflicting line numbers or divergent symbol descriptions that would mislead the builder.

---

## VERDICT: PASS

All cross-checked anchors agree across files; both [CODE-CONTRADICTED] discrepancies are resolved consistently everywhere they appear; the stub-emission claim dovetails with the EventRecord/_project_workers contract; and the two byte-offset tail candidates are complementary (R3 is the better mirror, independently corroborated by R5 §6). Two MINOR discrepancies (a spurious `_follow_log_file` symbol name in R2, and a cosmetic 1452/1453 block-start framing) do not affect correctness and are documented above for the builder. No CRITICAL or IMPORTANT gaps. Research set is internally consistent and safe to proceed to task-build.

### Gap list (advisory only — does NOT block PASS)
1. (MINOR) R2: rename reference `_follow_log_file` → `_follow_log` (commands.py:2737). Or adopt R3's monitor.py template instead.
2. (MINOR) R1/R3: `--detached` block start is line 1453 (dest) / 1452 (`@click.option(`); end 1469 + guard 1470 are correct — no action needed.
