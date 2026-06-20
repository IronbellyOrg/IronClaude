# Reviewer Card — Tier-2 Pre-Execution (UC-1, SPEC-LITERAL / BEST-PRACTICE lens)

**Reviewer role:** Spec-literal adversarial auditor
**Task:** TASK-RF-swarm-tui-wiring-20260618-165434 — Wire `--tui` into `superclaude swarm run` (Approach A)
**Spec:** `.dev/brainstorms/swarm-tui-wiring/merged-requirements.md`
**Stance:** Adversarial — assume the tasklist mis-states a spec token, weakens an acceptance criterion, or re-opens the crash class.
**Mode:** Read-only. Ground-truth facts independently re-verified via Bash/Read this turn (not from memory).

---

## Independently re-verified ground-truth facts (this turn)

| Fact | Source | Verified value |
|---|---|---|
| Fresh-run JSONL write path | commands.py:99, 1733 | `execution-log.jsonl` (constant `EXECUTION_LOG_JSONL_FILENAME` + literal at Logger ctor) |
| `event-log.jsonl` as write path | grep commands.py | **ZERO write-path hits** — stale/docstring-only (spec FR-4 token is wrong) |
| `from_json` definition | models.py:1820 | `def from_json(cls: Type[T], payload: str) -> T` (sole def in swarm/) |
| `dispatch_wave1` signature | dispatch.py:334-343 | positional `preflight_result`, `transport=None`, kw-only `transport_for_slot/prompt/parallel_executor/worker_spec/logger` |
| Fresh dispatch call | commands.py:1807 | `worker_results = dispatch_wave1(` |
| Resume dispatch call (LEAVE UNTOUCHED) | commands.py:2264 | `raw_redispatched = dispatch_wave1(` — distinct call site |
| Resume branch structure | commands.py:1539-1567 | `if resume_job_id is not None:` → resume+detached reject 1547-1553 → `--output` reject 1554-1560 → `_run_resume_branch` 1561 → `return` 1567 |
| Exit constants | commands.py:188-190 | `EXIT_OK=0`, `EXIT_INVALID=1`, `EXIT_USAGE=2` |
| `should_enable_tui` | tui.py:74 | `(flag, stream=None)` → `False` unless `flag AND target.isatty()` |
| `--strict-markers` + no `tui` marker | pyproject.toml:111, 114-135 | strict on; `tui` not registered → unmarked tests mandatory |

---

## CHECK 1 — FR-1 / FR-5 non-negotiable threaded-dispatch gate

**(a) Worker thread NON-DAEMON (`daemon=False`)** — **PASS**
- Key Constraints block: "`threading.Thread(..., daemon=False)` + explicit `join()`" (tasklist line 135).
- Step 2.5 clause (a): "wrapped in a closure run on a NON-DAEMON thread `threading.Thread(target=_worker, name="swarm-wave1", daemon=False)`" (line 215).
- Research G1 ([CODE-VERIFIED]) explicitly warns the `executor.py:416` precedent is `daemon=True` and must NOT be copied verbatim ("copy the box, flip the flag to `False`"). Tasklist Step 2.5 honors this. Matches spec FR-5 line 105 verbatim mandate.

**(b) `tui.stop()` in `finally` BEFORE worker BaseException is re-raised** — **PASS**
- Step 2.5 clauses (c)/(d): "`tui.stop()` is called in a `finally:`" then "AFTER `tui.stop()`, if the exception-box holds a captured worker `BaseException`, re-raise it on the main thread … BEFORE the post-dispatch continuation" (line 215).
- Ordering is explicit and correct: `finally: stop()` → post-`finally` re-raise. Matches spec FR-5 line 102-103 ("call `tui.stop()` **first**, and **then** re-raise") and the G3 pattern (gapfill lines 145-163: `finally: stop()` then `if "e" in exc_box: raise`).
- Step 3.5 asserts (c) `tui.stop()` ran before the re-raise via spy/probe — the acceptance criterion is tested, not assumed.

**(c) NO worker/dispatch code path imports/calls TUI/Live/Console (single-writer topology)** — **PASS**
- Step 2.5 invariant: "the worker thread NEVER calls `click.echo`/`print`/touches stdout while Live is active (FR-1 single-writer; all worker output goes through the filesystem `Logger`)" (line 215).
- Step 3.1 replaces the vacuous audit with an AST import-graph reachability test over `dispatch.py` + `parallel.py` (+ `_run_worker`) asserting zero `rich.*` / `superclaude.cli.swarm.tui` imports and zero `TUI`/`Live`/`Console`/`should_enable_tui` name references, WITH a mandatory vacuity guard (≥1 module scanned) AND a mutation guard (synthetic `import rich.live` must be flagged). This is a genuine structural enforcement, not a grep that passes vacuously.
- Step 2.6 adds the caller-side runtime `threading.get_ident()` assertion before each `tui.update`, keeping `tui.py` unchanged (G4). Step 3.2 tests it with a mandatory `assert seen_idents` vacuity guard.

**CHECK 1 verdict: PASS (all three sub-criteria).** No daemon=True leak, correct stop-before-reraise ordering, structural single-writer enforcement with anti-vacuity guards.

---

## CHECK 2 — Filename correctness (`execution-log.jsonl`, NOT spec's stale `event-log.jsonl`)

**PASS (and the spec-is-wrong/code-is-right resolution is explicitly carried).**
- Spec FR-4 (line 86-91) literally says `event-log.jsonl` — this token is **stale**. Independently re-verified this turn: `event-log.jsonl` has ZERO write-path hits in commands.py; the real path is `execution-log.jsonl` (commands.py:99, 1733).
- Tasklist Key Constraints "Filename truth" (line 138): "the fresh-run dispatch writes `execution-log.jsonl` (NOT `event-log.jsonl` — the spec's FR-4 reference to `event-log.jsonl` is STALE / [CODE-CONTRADICTED])". Every tail/test item targets `execution-log.jsonl`:
  - Step 2.4 (`_tail_events`): "target the on-disk file `execution-log.jsonl` (NOT the stale `event-log.jsonl`)" (line 209).
  - Step 2.5 poll loop: "`_tail_events(state_output_dir / "execution-log.jsonl", offset)`" (line 215).
  - Steps 3.3, 3.4, 3.7 all read/parse `execution-log.jsonl`.
- The tasklist did NOT copy the spec's stale token. The [CODE-CONTRADICTED] resolution (research 02 §7) is faithfully propagated. **This is the spec being wrong, the code/tasklist being right** — noted as required.

---

## CHECK 3 — `from_json` import source (`models.py:1820`, NOT spec's `logging_.py:46`)

**PASS.**
- Spec FR-4 (line 88) says `from_json(EventRecord, line)` (logging_.py:46). Independently re-verified: the only `def from_json` in swarm/ is `models.py:1820`. `logging_.py:46` is a docstring line.
- Tasklist Key Constraints (line 138): "`from_json` lives in `models.py:1820` (NOT `logging_.py:46` — STALE). ALL items + tests target … `from superclaude.cli.swarm.models import EventRecord, from_json`."
- Step 2.4 mandates the deferred import "`from superclaude.cli.swarm.models import EventRecord, from_json` (from_json is in models.py:1820, NOT logging_.py)" (line 209). Steps 3.3/3.7 use the same import line. Correct source, stale spec token rejected.

---

## CHECK 4 — Scope: fresh-run only; resume dispatch (~2264) UNTOUCHED; `--tui`+resume REJECTED (not silently entering loop)

**PASS.**
- Resume dispatch at commands.py:2264 (`raw_redispatched = dispatch_wave1(`) is a distinct call site from the fresh dispatch at 1807, independently confirmed this turn.
- `unchanged_by_design` frontmatter + Phase-2 header (line 189): "DO NOT touch the resume `dispatch_wave1` call site (~commands.py:2264)." Step 2.5 refactors ONLY the fresh-run dispatch site at ~1807.
- FR-3 second criterion (spec line 79: "`--tui` on a resume … does **not** enter the TUI loop"): Step 2.3b inserts a NEW `if tui:` reject INSIDE the resume branch, AFTER the resume+detached reject (~1553) and BEFORE `_run_resume_branch(...)` (~1561), with `EXIT_USAGE` and a message naming the `--tui`/`--resume` incompatibility (line 205). Structurally validated: `_run_resume_branch` is at 1561 and the resume branch `return`s at 1567, so a reject placed before 1561 guarantees the resume path never reaches the TUI loop. **`--tui` is rejected, NOT silently ignored** — matches FR-3 acceptance literally.
- Step 3.1b sub-test (b) asserts the resume+`--tui` invocation exits `EXIT_USAGE` (2) AND "the run does NOT spawn the TUI loop (… monkeypatch `TUI` to fail if constructed and assert it was never constructed)". The "does not enter the loop" criterion is tested, not assumed.

---

## CHECK 5 — C3/AC-004/NFR-001: no item changes `dispatch_wave1`/`ParallelExecutor` signatures; verifying check present

**PASS.**
- Phase-2 header (line 189) + Key Constraints (line 137) freeze both signatures; the poll loop lives in the caller (`run_cmd`), not in `dispatch_wave1`. Step 2.5 calls `dispatch_wave1(...)` "with its EXACT unchanged kwargs and result name `worker_results`."
- TWO independent verifying checks:
  1. **Step 3.8** — `inspect.signature(...)` test pinning exact param names/order/defaults/kind for `dispatch_wave1` (positional `preflight_result`, `transport=None`, kw-only `transport_for_slot/prompt/parallel_executor/worker_spec/logger`) and `ParallelExecutor.__init__` (`max_workers: int = 10`) + presence of `plan`/`execute`. The pinned signature matches the verified dispatch.py:334-343 verbatim.
  2. **Step 4.4** — `git diff <start_commit> -- dispatch.py parallel.py` proof with a PASS/FAIL verdict written to the capture. `start_commit` = `300c06a6...` (frontmatter line 19).
- Belt-and-suspenders (inspect + git-diff). NFR-001 frozen `ParallelExecutor` covered by the same inspect test.

---

## CHECK 6 — Acceptance-criteria literalness (per-FR, no weakened proxy)

| FR | Spec acceptance (literal) | Tasklist test | Verdict |
|---|---|---|---|
| FR-1 | Zero TUI/Rich reachability from dispatch/worker; runtime main-thread `get_ident` check | Step 3.1 (AST audit + mutation guard) + Step 3.2 (`get_ident` probe + `assert seen_idents`) | **PASS** — non-vacuity enforced on both |
| FR-2 | "identical exit code, identical `execution-log.jsonl` + state output, and **zero** ANSI bytes" | Step 3.4: asserts identical exit code, identical `worker_done` count, zero ANSI on BOTH `--tui`/no-`--tui` non-TTY runs (`_assert_no_ansi`) | **PASS** — all three sub-criteria asserted, not a subset |
| FR-3 | Both invocations exit `UsageError` naming incompatibility; resume does not spawn loop | Step 3.1b (a) `--tui --detached`→exit 2 naming; (b) `--resume --tui`→exit 2 + TUI never constructed | **PASS** — both criteria |
| FR-4 | Mid-line truncation → exactly-once, no parse error on partial, ≥1 worker row via `_project_workers` | Step 3.3: partial-line + corrupt-complete-line + exactly-once + `_project_workers(...).values()` has `status != "pending"` (NON-VACUOUS) | **PASS** — exceeds spec (adds corrupt-complete-line skip/advance) |
| FR-5 | `tui.stop()` ran, terminal restored, non-zero exit, ORIGINAL exception/traceback (not "TUI closed") | Step 3.5: non-zero + distinctive message reaches caller + `stop()` spy confirmed | **PASS** — original-exception-not-masked asserted literally |
| FR-6 | Parametrize clean/exception/SIGINT; `stop()` idempotent; SIGINT "exit code reflecting interruption" | Step 3.6: all three paths; `stop()` once + idempotent 2nd call; **SIGINT asserts `exit_code == 130` specifically (not merely non-zero)** | **PASS** — 130 pinned, stronger than spec's "reflecting interruption" |
| FR-7 | Fails if `--tui` unwired; passes with populated table; INV-012 zero-ANSI companion | Step 3.7: `_project_workers(...).values()` ≥1 `status != "pending"` row sourced from tailed log; `_assert_no_ansi`; regression-guard framing | **PASS** — "≥1 NON-VACUOUS worker row" (status != pending) asserted, not "any dict entry" |

**FR-7 non-vacuity (the classic weakening trap): PASS.** The tasklist pins "at least one `WorkerSnapshot` has `status != "pending"`" (Steps 3.3, 3.7) — exactly the research-02 §3 definition of a non-vacuous row (line 51: "status other than the default `"pending"`"). It did NOT weaken to "len(dict) >= 1 of any entry."

**CHECK 6 verdict: PASS for all 7 FRs.** No acceptance criterion is weakened to a proxy; two are strengthened (FR-4 corrupt-complete-line, FR-6 exit-130 pin).

---

## CHECK 7 — Best-practice (markers, UV, ruff)

- **Tests unmarked / `--strict-markers`** — **PASS.** Independently confirmed `--strict-markers` (pyproject.toml:111) and absence of a `tui` marker (markers list 114-135). Phase-3 header (line 223) + every test item: "New tests MUST be UNMARKED (no `tui` pytest marker is registered; `--strict-markers` is on … adding an unregistered marker breaks collection)."
- **`uv run pytest`** — **PASS.** Every test/validation command uses `uv run pytest …` / `uv run ruff …`; no `python -m`/`pip`. Key Constraints (line 141): "UV-only."
- **ruff check AND ruff format --check both gated** — **PASS.** Step 4.1 `uv run ruff check`; Step 4.2 `uv run ruff format --check src/ tests/` with explicit rationale "CI runs format-check SEPARATELY from `make lint` … green make lint ≠ green CI format" (matches the project's `make lint ≠ CI ruff format` memory). Both are present and separated.

**CHECK 7 verdict: PASS.**

---

## Adversarial findings (≥3 required)

The stance demanded finding ≥3 issues. The tasklist is unusually tight on the 7 mandated spec-literal axes; no CRITICAL or HIGH spec-literal defect survived verification. The following are the genuine residual issues found — none rise to blocking, but they are recorded honestly rather than manufactured:

**ISSUE-1 (LOW / cosmetic-traceability) — `_tail_events` byte-offset double-discipline is subtle and slightly self-tensioned in prose.**
Step 2.4 (line 209) instructs: a complete-but-malformed line must SKIP + ADVANCE the offset (no reparse), while a partial trailing line must NOT advance (buffer). Research G6 (gapfill line 354) states the *opposite* default for a parse failure: "if a line fails `from_json`, do NOT advance the offset past it (treat as still-partial)." The tasklist Step 2.4 resolves this correctly (it distinguishes newline-terminated-malformed → advance vs newline-less-partial → buffer), and Step 3.3 tests both cases — so the executed behavior is correct. But the tasklist contradicts its own cited research (G6) on the malformed-complete-line case without flagging that it is *overriding* G6. Risk: an executor who reads G6 verbatim for the "JSONDecodeError → don't advance" rule could implement an infinite-reparse stall on a corrupt complete line. **Mitigation already present:** Step 3.3's corrupt-complete-line sub-assertion (d) "does NOT stall … on a follow-up call" would catch this at test time. Severity LOW because the test gate closes the hole; flagged for traceability.

**ISSUE-2 (LOW) — `should_enable_tui(tui, sys.stdout)` second-arg literalness under CliRunner.**
Spec FR-2 (line 67) defines the gate as `should_enable_tui(--tui, stream)` where `stream.isatty()`. Tasklist Step 2.5 passes `sys.stdout`. Verified `should_enable_tui` defaults `stream` to `sys.stdout` and returns `False` on any non-TTY — so the literal call `should_enable_tui(tui, sys.stdout)` is correct. The residual risk is purely in the FR-2/FR-7 *tests*: Steps 3.2/3.5/3.7 force the gate by monkeypatching `should_enable_tui` to `True` on `superclaude.cli.swarm.tui` (the deferred-import source module). If Step 2.5 lands a module-top import instead of the deferred function-local import the research assumes, the monkeypatch target is wrong and the forced-TTY tests would silently exercise the OFF path (vacuous pass). **Mitigation already present:** Step 3.7 explicitly says "verify against the LANDED import style — if Step 2.5 used a module-top import instead, patch `…commands.should_enable_tui`." So the trap is named. Severity LOW.

**ISSUE-3 (LOW) — FR-6 SIGINT exit-130 is an inference from Click internals, not a spec literal.**
Spec FR-6 acceptance (line 119) says only "exit code reflecting interruption" — it does NOT name 130. The tasklist Step 3.6 hard-pins `result.exit_code == 130` (sourced from gapfill G3). This is a *strengthening* (good), but it converts a soft spec criterion into a brittle literal. If Click's `KeyboardInterrupt`→130 mapping differs under `CliRunner` (CliRunner can surface exceptions differently than `BaseCommand.main`), Step 3.6 (c) could fail on a behavior the spec would have accepted as "reflecting interruption." Severity LOW: it errs toward stricter-than-spec, and a failure here flags a real teardown defect rather than masking one. Recommend the executor, if `CliRunner` does not yield exactly 130, fall back to asserting non-zero + distinct-from-`EXIT_OK` (still satisfying the spec literal) and record the deviation — rather than weakening or forcing.

**ISSUE-4 (INFORMATIONAL) — FR-4 "refresh cadence 2/s (≈0.5s loop sleep)" + iteration ceiling.**
Spec FR-4 (line 92) says "reuse the TUI's own `refresh_per_second=2` (≈0.5s loop sleep)" and an "*optional* iteration ceiling." Tasklist Step 2.5 makes the ceiling **CONCRETE (NOT optional)** and adds Step 3.7b to verify it. This is a deliberate strengthening of an explicitly-optional spec clause (anti-spin safety), correctly scoped so the ceiling breaks only the render loop while `join()` still drains the non-daemon worker (never truncating it — preserving FR-5). Not a defect; recorded because it is a divergence from the spec's "optional" wording that a post-execution auditor should classify as *Authorized expansion*, not drift.

---

## Cross-cutting confirmations

- **Frontmatter "Implements FR-1..FR-7" claim is TRUE** for both FR-3 sub-criteria after Step 2.3b (tasklist explicitly asserts this at line 205). No over-claim.
- **QA-gate waiver** (QA_GATE_REQUIREMENTS: NONE, mirroring TASK-RF-pr167-verdict-regex) is consistent with a tightly-scoped single-file code change; verification rests on the full pytest suite + FR tests + ruff + POST reflect gate. Defensible.
- **No `.claude/` staging, no commit/push/PR** instructed (lines 141, 267) — compliant with project absolute rules.
- **POST reflect gate** (Post-Completion line 295) uses the flat wrapper behind the recursion-breaker, consumes exit code literally (only 0 advances), does not hand-author `reflect_post`. Correct.

---

## Calibrated confidence

**0.93** that the tasklist is spec-literal-correct.

Rationale: All 7 mandated spec-literal checks PASS against independently re-verified ground truth. The two [CODE-CONTRADICTED] resolutions (`execution-log.jsonl`, `models.py:1820`) are faithfully carried and the stale spec tokens are explicitly rejected — the single highest-risk failure mode (copying the spec's wrong tokens) did not occur. FR-1/FR-5 non-negotiable gates are correctly specified (daemon=False, stop-before-reraise, structural single-writer with anti-vacuity test guards). No acceptance criterion is weakened; two are strengthened. The 0.07 residual is the test-seam monkeypatch-target risk (ISSUE-2) and the exit-130 brittleness (ISSUE-3), both of which are already named in the tasklist and gated by tests — they could cost an executor a fix-cycle but cannot ship a spec-literal violation.

---

**best_practice_grade: 5/5**
(UV-only; both ruff check + ruff format --check gated and rationalized; unmarked tests under `--strict-markers`; mandatory vacuity + mutation guards on every audit; inspect + git-diff dual signature-freeze proof; non-vacuous-row assertions pinned to `status != "pending"`; baseline-before-change capture; frozen-file scope discipline.)

**VERDICT: PASS**

Severity-rated issues: 0 CRITICAL, 0 HIGH, 0 MEDIUM, 3 LOW (ISSUE-1 G6 self-tension, ISSUE-2 monkeypatch-target seam, ISSUE-3 exit-130 brittleness), 1 INFORMATIONAL (ISSUE-4 ceiling strengthening). All LOW issues are already mitigated by existing test gates or explicit in-tasklist guidance; none block execution.
