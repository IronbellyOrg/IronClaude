# QA Report — Research Depth (research-depth lens)

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery
**Date:** 2026-06-15
**Phase:** research-depth (qualitative; adversarial stance)
**Fix cycle:** N/A
**Driving spec:** .dev/brainstorms/sprint-429-recovery-spec.md
**Research dir:** .dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/research/

---

## Lens

Evaluate whether the research is DEEP ENOUGH to produce a high-quality,
per-file-granular MDTM task file WITHOUT the builder needing to re-read source.
Adversarial stance: assume superficial until proven otherwise.

Depth checklist:
1. detector→policy→status→persistence→resume chain HOW, not just WHAT
2. Concurrency model (spawn unlocked / reconcile locked / latch both call sites / storm bound ≤cap+(K−1)) — High-risk P3/P4
3. Detector-ordering rule + _task_completed_before_overrun reuse — exact branch insertion
4. Diagnostic-bundle hazard (executor.py:2103) at behavioral level
5. 6 fixtures with JSON detail + subprocess_factory seam worked example
6. Per-file/per-test checklist items derivable from research alone

---

## Files Reviewed (all 6 .md in research dir)

| File | Lines | Focus | Depth verdict |
|---|---|---|---|
| 01-file-inventory.md | 221 | per-symbol edit map (monitor/models/recovery_policy/aienv) | DEEP |
| 02-patterns-conventions.md | 220 | 6 reusable idioms w/ verbatim code + file:line | DEEP |
| 03-integration-points.md | 538 | IP-1..IP-10 exact wrap points + spec corrections | DEEP |
| 04-data-flow-tracer.md | 222 | runtime 429 chain + 4-way table + 10 edges + F-1 | DEEP |
| 05-test-verification.md | 494 | fixtures JSON + factory seam + per-test items | DEEP |
| 06-template-examples.md | 191 | MDTM template skeleton + POST-reflect emission | DEEP |

---

## Independent Source Verification (adversarial — claims re-checked against actual code)

I did NOT take the research at face value. I re-verified the most load-bearing
claims against `src/superclaude/cli/sprint/` source:

| Claim under test | Source checked | Result |
|---|---|---|
| `_run_one_task` sig + UNLOCKED-spawn docstring + status ladder + `:1003` gate + `nullcontext` guard | executor.py:963-1017 | CONFIRMED verbatim (signature, docstring, `:999-1015` ladder, `:1003` `detect_error_max_turns AND _task_completed_before_overrun`, `:1017` guard idiom) |
| **F-1 diagnostic-bundle hazard** — `:2103 if status.is_failure:` runs DiagnosticCollector + FailureClassifier + writes `phase-N-diagnostic.md` (spec said "only halts") | executor.py:2103-2132 | CONFIRMED — spec is WRONG; research correctly caught it |
| `TaskResult.from_dict` hard-keyed for result-level fields, `.get()` only on nested task | models.py:218-240 | CONFIRMED — back-compat hazard real; `.get()` requirement correct |
| No `DriftNominator` — only 3 Nominator classes | recovery.py grep | CONFIRMED — `Nominator`/`ManualNominator`/`ReflectReportNominator` only |
| `count_turns_from_stream_json` in process.py NOT monitor.py; monitor has `count_turns_from_output` | grep both files | CONFIRMED — name/location correction valid |
| `_is_transient_failure` returns True on `api_retry` (429 collision) | executor.py:2278 | CONFIRMED — ordering-is-the-fix reasoning sound |
| `_classify_transcript` reads `subtype`+`is_error`, NOT `api_error_status` (429 invisible today) | rerun_tasks.py:579-582 | CONFIRMED — subtype-trap + offline-misclassification real |

**Verdict on accuracy:** every spot-checked claim held. The research not only
matches source — it independently CORRECTS the driving spec in three places
(F-1 diagnostic bundle; no DriftNominator; cmd/env in pipeline/process.py not
sprint/process.py) and corrects upstream research-notes (count_turns name;
PhaseStatus 3-property; monitor missing imports). This is the opposite of the
"lists file names without understanding behavior" shallow pattern the
adversarial stance screens for.

---

## Depth Checklist Evaluation

### 1. detector→policy→status→persistence→resume chain HOW (not just WHAT) — PASS

File 04 §0 gives the full one-line end-to-end map for BOTH paths, then §1-§6
trace each hop with mechanism: detector keys on LAST `{"type":"result"}` event
via `api_error_status` (file 02 Pattern B gives the verbatim parse loop from
rerun_tasks.py:555-574); policy `decide` truth table (file 01 FILE 3, file 04
§1); status routing through `is_failure`→resume (file 03 IP-8 proves the planner
is ZERO-EDIT because `TaskStatus(value)` auto-resolves + `not is_success`
auto-reruns); persistence via `_write_phase_result_json` payload append (file 03
IP-5 exact keys); resume auto-routing (file 03 IP-8 + file 05 §10 end-to-end
test). The chain is explained at the mechanism level, with each link's exact
insertion site. Builder can write each hop without re-reading source.

### 2. Concurrency model (spawn unlocked / reconcile locked / latch both call sites / storm bound ≤cap+(K−1)) — PASS [HIGH-RISK PHASE — scrutinized hardest]

This is the highest-risk surface and the research is correspondingly deepest:
- **Spawn unlocked / reconcile locked:** file 02 Pattern E quotes the verbatim
  lock-contract docstring (executor.py:976-985) + the `guard = lock if lock is
  not None else contextlib.nullcontext()` idiom at `:1017` (I re-verified both).
- **Latch threading at BOTH call sites:** file 02 Pattern E §3 + file 03 IP-1
  give the EXACT two call sites — K>1 `:1134-1145` (`lock=lock`) and K=1
  `:1337-1348` (`lock=None`) — and explicitly warn that missing either site =
  `None` policy = no recovery on that K mode. File 03 also flags
  `_execute_phase_tasks_parallel` (`:1048-1062`) needs the param plumbed through.
- **Storm bound:** file 02 (`:158`), file 03 IP-1, and file 04 §3 ALL state the
  load-bearing arithmetic `≤ cap + (K−1)` and `< K × cap`, **explicitly NOT
  `≤ cap`**, and file 04 §3 + file 05 scenario 5 name the over-strict-assertion
  trap (`assert spawns <= cap` is WRONG for K>1). File 05 §6.2 gives the
  thread-safe-counter test harness and points at existing concurrency tests
  (test_handoff_concurrency.py) for the idiom.
- **Check-under-lock / spawn-unlocked / trip-under-lock** sequence is spelled out
  step-by-step (file 04 §3 pseudocode). Implementable safely from research alone.

### 3. Detector-ordering rule + `_task_completed_before_overrun` reuse — exact branch insertion — PASS

File 03 IP-1 gives the line-exact ladder (`:999-1015`) and the precise insert
point: "BELOW the `:1003` completion gate, ABOVE `:1012` `_is_transient_failure`",
with the ordering `success-envelope → error_max_turns (PASS_RECOVERED) →
provider-failure → transient → terminal`. File 04 §2 explains the TWO sub-cases
(overrun-then-429 handled by ordering alone; clean-success-then-trailing-429
where the new branch must ITSELF call `_task_completed_before_overrun`), and
crucially analyzes the guard's `lines[:-1]` mechanics (executor.py:2367-2387) to
PROVE the reuse stays sound when the terminal line is a 429 instead of
error_max_turns. That is genuine behavioral understanding, not flagging. I
verified `:1003`/`:1012` against source. Builder can write the exact branch.

### 4. Diagnostic-bundle hazard (executor.py:2103) at behavioral level — PASS [verified strongest]

This is the standout. File 04 FINDING F-1 and file 03 IP-3 independently
establish — and I re-confirmed against executor.py:2103-2132 — that the spec's
claim ("`is_failure` only halts the phase, no auto-remediation consumer") is
TRUE for the per-task `TaskStatus.is_failure` path (which `continue`s at `:1781`
before ever reaching `:2103`) but FALSE for the single-session
`PhaseStatus.is_failure` path (which auto-runs DiagnosticCollector +
FailureClassifier + writes `phase-N-diagnostic.md`). The research explains WHICH
path triggers it (single-session phase), WHY (`PhaseStatus.is_failure` gate at
`:2103`), and HOW to resolve it (option B1: add to `is_terminal` not
`is_failure`, OR guard the `:2103` block with `and status is not
PROVIDER_EXHAUSTED`), with a required test asserting no diagnostic bundle is
written. This is exactly the is_terminal-not-is_failure resolution the checklist
asks for, at full behavioral depth. The per-task-vs-single-session divergence is
the single most important insight in the whole research set and it was NOT in the
spec — the research found it.

### 5. 6 fixtures with JSON detail + subprocess_factory seam worked example — PASS

File 05 §3 gives all 6 fixtures as complete, authorable NDJSON (single_account,
all_account_cooldown w/ resolved-model capture, operation_timeout,
api_retry_maxed, task_failure_real, clean_pass) — each with the exact
`is_error`/`api_error_status`/`result`-body fields and the discriminator note.
File 05 §2 gives the subprocess_factory seam worked example: the verified
contract (`factory(task,config,phase) → (exit,turns,bytes)` AND writes
`config.task_output_file`), the `_make_scripted_factory` per-attempt call-counter
implementation, and a full PASS-scenario test. §6.2 enumerates all 6 executor
loop scenarios as a table mapping scripted attempts → assertions, including the
K>1 latch bound. Back-compat (§7), UX golden-string (§8.1), aienv (§8.2),
doc⇆CLI parity two layers (§9), resume-safety (§10) all have real code. Fixtures
and seam are immediately authorable.

### 6. Per-file/per-test checklist items derivable from research alone — PASS

File 01 SUMMARY gives a per-symbol edit count per file (e.g. monitor.py P1 = 6
new symbols + 2 import-adds at insertion zone L250-L253). File 03 closing table
maps every integration point to Edit?/Phase/exact-site. File 05 §5 gives a
per-test-item checklist at A3 granularity. File 06 supplies the exact template
path (correcting the skill default), the PART-2 section skeleton with line
anchors, the B2 6-element item shape, M3/I19 QA-agent floors, and the
POST-reflect emission contract w/ `start_commit`/`executor_model_class`
frontmatter. A builder has everything needed to emit per-file/per-test items
without re-reading source.

---

## Quality Signals Beyond the Checklist

- **Honest Unverified markers throughout** — files 02/03/05 explicitly tag what
  was NOT re-read this pass (`build_resume_output` line range, the `run` Click
  subcommand symbol, sprint-guide heading structure, the `decide` `<` vs `<=`
  boundary) and assign them to a phase/owner. This is the mark of disciplined
  research, not hand-waving.
- **needs_human_decision discipline** — file 01 (aienv os.environ-vs-file-parse)
  and file 03 IP-7 (G nominator exclusion) correctly flag design choices to
  ENCODE-with-default + document, never silently pick — aligned with
  `feedback_human_decision_items_must_halt`.
- **SoT / toolchain gates captured** — file 02 Pattern F + file 05 §11 encode the
  UV-only, `ruff format --check` CI gap, fork-PR `--repo`, and verify-sync
  discipline as VALIDATION items.

---

## Self-Audit (mandatory)

1. **Factual claims independently verified against source:** 7 distinct
   load-bearing claims (see Independent Source Verification table) across 4 source
   files — including the single most-disputed one (F-1 diagnostic bundle).
2. **Files read to verify:** `executor.py` (963-1017, 2103-2132), `models.py`
   (218-240), `rerun_tasks.py` (538-590 via grep), `recovery.py` (grep),
   `monitor.py` + `process.py` (grep for count_turns). Plus all 6 research files
   end-to-end and the driving spec end-to-end.
3. **Why trust I checked:** I did NOT find 0 issues by assumption — I re-ran the
   spec's own most aggressive claim ("no auto-remediation consumer") against
   executor.py:2103 and found the research had ALREADY caught the spec being
   wrong; I confirmed the absence of `DriftNominator` by grep; I confirmed the
   hard-keyed `from_dict` by reading the method. Each PASS rests on a tool result,
   not a vibe.
4. **Web research:** none performed (this is a local-source-bound depth review);
   Tavily-first N/A.

**Tool engagement:** Read: 9 | Grep/Bash: 2 | Glob: 0 (Bash ls used instead) —
exceeds the 6 depth-checklist items.

---

## VERDICT: PASS

The research is DEEP ENOUGH to produce a high-quality, per-file/per-test-granular
MDTM task file WITHOUT the builder needing to re-read source. All 6 depth
checklist items pass, including the two High-risk concurrency items (P3/P4) which
were scrutinized hardest and independently source-verified. The research exceeds
the bar: it understands behavior (not just file names), corrects the driving spec
in three material places (most importantly the F-1 diagnostic-bundle hazard, which
I confirmed against executor.py:2103), corrects upstream research-notes, supplies
verbatim code idioms with file:line exemplars, authorable fixture JSON, a worked
subprocess_factory seam, and honest Unverified/needs_human_decision markers.

No issues of any severity. No remediation required before task-building.

### Note for the builder (carry-forward, NOT a research defect)
The research itself flags these as builder-close items (already documented in the
files, so they are NOT depth gaps): confirm the `decide` `<`-vs-`<=` cap boundary;
confirm the `run` Click subcommand symbol name in commands.py; Read the sprint
guide heading structure before writing the doc⇆CLI parity slicer; confirm the
real `~/.aienv` export format and the `suggest_alternate_model(aienv_path=...)`
signature; finalize the `reset_policy`/latch param name. All are correctly
scoped to implementation phases, not research, and each carries an Unverified tag
in the source research.
