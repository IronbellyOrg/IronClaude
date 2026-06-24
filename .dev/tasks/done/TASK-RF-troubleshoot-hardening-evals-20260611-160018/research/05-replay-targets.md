# Research 05 — Replay-Target Verification (per-escape OLD=MISS vs NEW=CATCH differential)

**Status: Complete**

**Topic:** For each escape E1–E5, establish the concrete differential the harness asserts:
OLD-protocol=MISS at the pre-fix parent vs NEW-H0–H5-gate=CATCH. Maps 1:1 to RELEASE-SPEC §8.3.

**Repo root:** `/config/workspace/IronClaude/` (full git history).

**Scope:** git history only — the 5 fix commits + their pre-fix parents. I document, per escape:
(a) file(s)/function(s) the fix changed; (b) the BUGGY pre-fix behavior; (c) the concrete OLD=MISS
observable (what input slips past, what old code returns); (d) the NEW=CATCH target (what the H{1,2,3,4}
gate must assert); (e) confirmation against §8.3.

---

## Source-of-truth confirmation (re-verified with `git show --stat`)

| Escape | Fix SHA | Pre-fix parent SHA | Wave | §8.3 row | Files changed by fix (non-`.dev/`) |
|--------|---------|--------------------|------|----------|-----------------------------------|
| E1 | `7601ad25` | `94d5baa0` | H1 | "E1 backtest" | `cli/prd/process.py`, `cli/prd/prompts.py`, `tests/cli/prd/test_spec_flag.py` |
| E2 | `e97aa4fd` | `10723863` | H3 | "E2 backtest" | `cli/prd/gates.py`, `tests/cli/prd/test_gates.py`, `skills/sc-auggie-review-protocol/SKILL.md`† |
| E3 | `eb9a2633` | `e97aa4fd` | H3 | "E3 backtest" | `cli/pipeline/gates.py`, `cli/pipeline/models.py`, `cli/prd/gates.py`, `tests/pipeline/test_gates.py`, `tests/cli/prd/test_gates.py` |
| E4 | `b97c9960` (UNMERGED) | `1b0264f1` | H2 | "E4 backtest" | `cli/prd/executor.py`, `tests/cli/prd/test_executor.py` |
| E5 | `10723863` | `d878bc6d` | H4 | "E5 backtest" | `skills/task-builder/SKILL.md` |

† E2's `sc-auggie-review-protocol/SKILL.md` change is an out-of-scope bundled doc edit (the
`--wait-for-indexing` mandate); it is NOT part of the E2 escape differential. The E2 escape lives
entirely in `cli/prd/gates.py::_check_parallel_instructions`.

**Wave-numbering note (RELEASE-SPEC Appendix A crosswalk):** §8.3 + this task both use the draft's
H0–H5 numbering. The task assignment's E→wave mapping (E1→H1, E2→H3, E3→H3, E4→H2, E5→H4) matches
§8.3 exactly. Note E2 and E3 share wave H3 (the parallel-instructions classifier), and E3+E4 form the
**dual-evaluator pair** — §8.3's E4 row explicitly requires "both `gate_passed` AND `_evaluate_gate`
consumers classified," which is why E3 (=`gate_passed`) and E4 (=`_evaluate_gate`) are separate escapes.

**Cross-check sources (independent of the commits):**
- `.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` — `BASE_COMMIT: 94d5baa0…`; uses
  alt escape-ids (PRD-E04=#151, PRD-E05=#154, PRD-E06=#155, REFLECT-E01=#153) that map to the same SHAs.
- `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` §8.3.

---

## E1 — PRD cloud-only `--file` flag (fix `7601ad25`, parent `94d5baa0`, wave H1)

### (a) What the fix changed
- **`src/superclaude/cli/prd/process.py`** — DELETED the entire `_build_file_args` static method and its
  `extra_args=file_args` wiring in `PrdClaudeProcess.__init__`. Removed three now-dead module constants:
  `_PHASE_ALLOWED_REFS` (the phase→refs map), `_FILE_SIZE_THRESHOLD = 50_000`, and
  `_SPEC_FILE_STEPS = frozenset({"scope-discovery", "investigation"})`. De-`--file`'d the module/class
  docstrings (GAP-003 reworded "Phase-aware `--file` arg scoping" → "inline prompt-based spec/ref delivery").
- **`src/superclaude/cli/prd/prompts.py`** — Upgraded `_authoritative_specs_block(spec_paths)` from a
  paths-only block to **inline-with-cap**: each existing spec is embedded verbatim via `_read_file(Path(p))`
  (50 KB cap + `_TRUNCATION_MARKER`) under a `--- SPEC: <path> ---` header, behind a mandatory
  `Path(p).is_file()` guard (missing/stale paths fall back to a path-only `- <p>` line; never raises
  `FileNotFoundError`).
- **`tests/cli/prd/test_spec_flag.py`** — Inverted: tests now assert `--file` ABSENCE + inline/truncation/
  missing-path/empty-input coverage.

### (b) Buggy pre-fix behavior (at `94d5baa0`)
`PrdClaudeProcess._build_file_args` emitted two kinds of `--file` argv into the `claude` subprocess:
1. refs >50 KB: `file_args.extend(["--file", str(ref_path)])`;
2. for `scope-discovery`/`investigation` steps (`_SPEC_FILE_STEPS`), every `config.spec_files` entry:
   `file_args.extend(["--file", spec_path])` — i.e. **local filesystem paths passed to a cloud-download
   flag**. The pipeline base appends these verbatim (`cli/pipeline/process.py`: `cmd.extend(self.extra_args)`).
`claude --file` expects `file_id:relative_path` and requires `CLAUDE_CODE_SESSION_ACCESS_TOKEN`. PRD was
the ONLY pipeline emitting `--file`; roadmap/tasklist/validate executors explicitly forbid it
(FR-003/FR-023: "`--file` is a cloud download mechanism and does not inject local file content").

### (c) OLD=MISS observable
A **headless** `superclaude prd run --spec <local-spec>` (no session token) reaches `scope-discovery`,
emits `--file <local_path>`, and the `claude` subprocess exits 1 in ~0.27 s with
`Error: Session token required for file downloads. CLAUDE_CODE_SESSION_ACCESS_TOKEN must be set.` →
3× crashloop. **The escape:** the pre-fix test suite inspected *command construction* (the argv list)
WITHOUT running the headless path, so the malformed-`--file` argv was accepted as "clean" — a passing
review over a non-executing test. OLD code path: `--file <local_path>` is present in argv and no gate
flags it.

### (d) NEW=CATCH target (H1)
H1 (runtime-entrypoint / boundary verification) must replay the real headless `--spec` path against the
production entrypoint with the fix reverted and **FAIL** (negative witness: crashloop / `--file` present),
then PASS post-fix. Concrete oracle: `grep -rn '"--file"' src/superclaude/cli/prd/` → **0** post-fix; the
sibling-pipeline contract sweep proves no local path is delivered via `claude --file` in any pipeline.
§8.3 expected outcome: "H1 FAIL pre-fix (negative witness), PASS post-fix."

### (e) §8.3 confirmation — MATCH
§8.3 "E1 backtest": *"Replay headless PRD `--spec` with local-path `--file` against H1 → H1 FAIL pre-fix
(negative witness), PASS post-fix."* The commit (`7601ad25`) removes exactly the local-path `--file`
emission that the negative witness asserts. Confirmed.

---

## E2 — Final-phase false-positive in `_check_parallel_instructions` (fix `e97aa4fd`, parent `10723863`, wave H3)

### (a) What the fix changed
- **`src/superclaude/cli/prd/gates.py::_check_parallel_instructions`** — Added a **final-phase exemption**:
  computes `max_phase = max(int(m.group(1)) for m in phase_sections)`; for the phase whose number ==
  `max_phase`, reads the full heading line and `continue`s (skips the parallel-keyword check) when the
  heading matches a completion signal. `completion_signals = [present, complete, finaliz, sign-off,
  sign off, wrap-up, wrap up]`, matched with **word-boundary anchoring**
  `re.search(r"\b" + re.escape(sig), heading_line)` (second commit in the squash fixed a bare-substring
  bug where "complete" matched "incomplete" and "present" matched "representation"). Docstring corrected
  from "phases 2-5" → "work phases (>=2) … final completion phase exempt."

### (b) Buggy pre-fix behavior (at `10723863`)
The OLD body (confirmed via `git show 10723863:src/superclaude/cli/prd/gates.py`) enforced the
parallel-keyword requirement on **every** `later_phases` entry (all phases with number ≥2), returning a
hard failure string for the first phase lacking a keyword — **despite** the docstring claiming "phases 2-5."
No final-phase exemption existed.

### (c) OLD=MISS observable
A live heavyweight PRD task-file whose **final** phase is a legitimately *sequential* completion phase
(e.g. `### Phase 7 - Present & Complete`, no parallel keywords because parallelism is N/A to a
presentation bookend) → OLD `_check_parallel_instructions` returns the failure string
`"Phase 7 missing parallel execution instructions (expected one of: parallel, concurrent, simultaneously,
batch)"`, **HALTing** a ~25-min heavyweight PRD run at `build-task-file`. The escape: the gate
false-positives on a correct artifact (the sequential bookend is intentional per anti-orphaning
convention). This was a real live halt.

### (d) NEW=CATCH target (H3)
H3 (parallel-instructions classifier) must replay a full generated artifact and distinguish:
(i) an **intended executable violation** (a real work phase with no parallelism) → still HALTs;
(ii) the **near-miss sibling negative** (a completion-titled final phase, or an "incomplete"-titled
phase that must NOT be exempted) → does NOT hard-fail / is correctly classified. The word-boundary rule
is the load-bearing guard (FR-8 / spec gap G-4): "complete" must not exempt "incomplete."

### (e) §8.3 confirmation — MATCH
§8.3 "E2 backtest": *"Replay full generated artifact containing `complete` and near-miss `incomplete`
phase text against H3 classifier → Intended executable violation still HALTs; near-miss sibling negative
does not hard-fail."* The commit's word-boundary completion-signal match (`\b` + `re.escape`) is exactly
the `complete`-vs-`incomplete` discrimination §8.3 names. Confirmed.

---

## E3 — Hard parallel-instructions gate → advisory in `pipeline.gates.gate_passed` (fix `eb9a2633`, parent `e97aa4fd`, wave H3)

### (a) What the fix changed
- **`src/superclaude/cli/pipeline/models.py`** — `SemanticCheck` dataclass gains `advisory: bool = False`.
- **`src/superclaude/cli/pipeline/gates.py::gate_passed`** — Added a `logging` import + module logger; in
  the STRICT semantic-check loop, when a check fails AND `getattr(check, "advisory", False)` is true, it
  `_log.warning(...)` (including `output_file` for traceability) and `continue`s instead of
  `return (False, f"Semantic check '{check.name}' failed: {detail}")`.
- **`src/superclaude/cli/prd/gates.py`** — `_make_semantic_check` gains an `advisory` param; only
  `build-task-file`'s `parallel_instructions` check is wired `advisory=True`; `task_phases_present` and
  `b2_self_contained` stay STRICT/halting.
- **`tests/pipeline/test_gates.py` (+) / `tests/cli/prd/test_gates.py` (+)** — advisory non-fatal + WARNING
  logged; non-advisory still halts; mixed advisory+strict still halts; default `False`; build-task-file
  wiring lock.

### (b) Buggy pre-fix behavior (at `e97aa4fd`)
Even after E2's final-phase exemption, `_check_parallel_instructions` is a brittle heuristic (loose
`Phase \d` heading regex + literal-keyword detection). At the parent, the gate framework had **no advisory
severity** — every `SemanticCheck` failure was fatal in `gate_passed`. So a *second* class of false
positive survived: the loose `(?:^|\n)\s*#{1,4}\s+.*Phase\s+(\d+)` regex matched **Task-Log placeholder
headings** like `### Phase 2 - Codebase Research Findings`, whose (empty placeholder) section had no
parallel keyword → hard HALT again.

### (c) OLD=MISS observable
A well-formed generated MDTM task file containing a Task-Log section (`### Phase N - … Findings`
placeholders outside the executable phase plan) → OLD `gate_passed` runs `parallel_instructions`, gets a
failure string, and (no advisory branch) returns `(False, "Semantic check 'parallel_instructions'
failed: …")`, HALTing the run. The escape: a hard gate whose **false-positive cost** (halting a long run)
exceeds the **risk it guards** (a task that merely runs agents serially — slower, not wrong); the
asymmetry was unaccounted for, so the pipeline accepted a halt-on-correct-artifact as legitimate.

### (d) NEW=CATCH target (H3)
H3 (unmask/sweep card) must replay the Task-Log/Findings sibling-heading artifact and assert:
(i) the sweep proves `K_swept == K_true` (the parser was swept over ALL generated sections, not just the
observed final-phase case); (ii) non-executable headings **WARN/CONTINUE** rather than HALT. The advisory
mechanism (`SemanticCheck.advisory` + the `continue` branch in `gate_passed`) is the CATCH surface.

### (e) §8.3 confirmation — MATCH
§8.3 "E3 backtest": *"Replay Task-Log/Findings sibling-heading artifact against H3 unmask/sweep card →
H3 FAILs until `K_swept == K_true` and non-executable headings WARN/CONTINUE rather than HALT."* The
commit's advisory `continue` (warn-don't-halt) is precisely the "WARN/CONTINUE rather than HALT" behavior.
Confirmed. (defect-escape-table PRD-E06 corroborates: #155 = "did not unmask-and-sweep the parser over all
generated task sections … preserved a hard gate whose false-positive cost exceeded the risk.")

---

## E4 — Dual-evaluator gap: advisory ignored in `PrdExecutor._evaluate_gate` (fix `b97c9960` UNMERGED, parent `1b0264f1`, wave H2)

### (a) What the fix changed
- **`src/superclaude/cli/prd/executor.py::PrdExecutor._evaluate_gate`** — Added `logging` import + module
  logger `_log`. In the semantic-check loop, when a check fails AND `getattr(check, "advisory", False)`:
  `_log.warning("Advisory gate check '%s' did not pass (non-fatal) for step '%s': %s", …)`, appends to
  `advisory_notes`, and `continue`s instead of `return False`. After the loop, if `advisory_notes`,
  surfaces them on the passing `gate_result` (`log_gate_result(step_id, True, "All checks passed
  (advisory: …)")` then `return True`). `task_phases_present` / `b2_self_contained` stay STRICT.
- **`tests/cli/prd/test_executor.py` (+)** — advisory non-fatal + WARNING; non-advisory still halts;
  advisory+strict still halts (via the actual `_evaluate_gate` path).

### (b) Buggy pre-fix behavior (at `1b0264f1`)
**The two-evaluator discovery.** PR #155 (E3) added advisory handling to `pipeline.gates.gate_passed` — but
the **live PRD path never calls `gate_passed`.** `PrdExecutor` uses its own evaluator,
`_evaluate_gate` (executor.py ~:850), which RE-IMPLEMENTS the semantic-check loop. At the parent `1b0264f1`
(confirmed via `git show 1b0264f1:src/superclaude/cli/prd/executor.py`), that loop halts on the first
non-True check **regardless of the advisory flag** (`if result is not True: … return False`). So E3 did
NOT actually relax the *runtime* PRD gate — `build-task-file` kept halting on the advisory-marked
`parallel_instructions` check on the live path.

### (c) OLD=MISS observable
Run a known-advisory-failing check through the **live** PRD path: `_evaluate_gate("build-task-file", …)`
on the live-repro task. OLD code returns **`False`** (halts) — even though E3 marked `parallel_instructions`
advisory — because `_evaluate_gate` never reads `check.advisory`. The escape: E3's fix was verified against
`gate_passed` (the wrong consumer), so a test/review that exercised only `gate_passed` saw GREEN while the
production executor still halted. A review that classified only ONE evaluator missed the second consumer.

### (d) NEW=CATCH target (H2)
H2 (boundary/consumer ledger) must enumerate **both** advisory-check consumers — `gate_passed` AND
`_evaluate_gate` — and FAIL until both are classified/hardened. The oracle: the actual path
`_evaluate_gate("build-task-file", …)` on the live-repro task now returns **`True`** with the advisory
warning logged (and the advisory note surfaced on the passing `gate_result`).

### (e) §8.3 confirmation — MATCH
§8.3 "E4 backtest": *"Run advisory check through PRD `_evaluate_gate` with H2 ledger → H2 FAIL until both
`gate_passed` and `_evaluate_gate` consumers classified."* The commit message states verbatim: "PR #155
added advisory-check handling to `pipeline.gates.gate_passed`, but the PRD executor never calls
`gate_passed` — it uses … `PrdExecutor._evaluate_gate` … which … halted on the first non-True check
regardless of the advisory flag." Confirmed — E4 is the second-consumer of the E3 advisory mechanism.

---

## E5 — POST-reflect `--diff` base: `start_commit..HEAD` → merge-base working-tree (fix `10723863`, parent `d878bc6d`, wave H4)

### (a) What the fix changed
- **`src/superclaude/skills/task-builder/SKILL.md`** — The generated `N.{X-1}` POST-reflect gate item.
  OLD action (confirmed at `d878bc6d:…/SKILL.md` line 2195): `/sc:reflect --mode post --remediate
  --diff <BASE>..HEAD …` where `<BASE>` = `start_commit` (HEAD at task start). NEW action:
  `--diff <BASE>` as a **SINGLE ref** (NOT `<BASE>..HEAD`), where `<BASE> = git merge-base HEAD
  <integration-branch>`; `<integration-branch>` resolved dynamically via
  `git symbolic-ref --short refs/remotes/origin/HEAD` (fallback to whichever of `origin/master`/
  `origin/main` exists). Passing a single ref makes reflect diff `<BASE>` against the **working tree**
  (capturing committed + staged + unstaged edits to tracked files). Added the `git add -A` caveat
  (untracked files are NOT captured by `git diff <BASE>`) and the explicit "Do NOT use
  `start_commit..HEAD`" prohibition. `start_commit` retained in frontmatter for provenance only.

### (b) Buggy pre-fix behavior (at `d878bc6d`)
The generated POST-reflect item emitted `--diff <start_commit>..HEAD`, a **two-dot commit range** anchored
on `start_commit = git rev-parse HEAD` captured at task start.

### (c) OLD=MISS observable
Two real failure modes (both hit live while auditing PR #151):
1. **Uncommitted work (the usual `/task` outcome):** `/task` edits the working tree but does NOT commit, so
   `start_commit..HEAD` (commit range) audits **none** of the task's changes — the working tree diff is
   invisible to a `..HEAD` range. Reflect runs over an empty/foreign diff and returns a vacuous PASS.
2. **Foreign-commit interleave:** an unrelated commit lands on the branch after task start, so
   `start_commit..HEAD` spans **foreign** work — reflect audits unrelated changes.
The escape: the diff *selector* (`start_commit..HEAD`) names the wrong **effective input**; an off-path
review existed but pointed off-path, so reflect "passed" without ever inspecting the actual task changes.

### (d) NEW=CATCH target (H4)
H4 (effective-input / selector-correctness gate) must **FAIL closed** (treat the wrong surface as a failure)
until the diff selector is proven correct — i.e. the effective diff contains the task's files and excludes
foreign commits. The oracle (per defect-escape-table): a dogfood POST-reflect e2e that edits the working
tree **without committing** + lands a foreign commit in range, then verifies the effective diff *contains*
the task files and *excludes* the foreign commit. The single-ref-against-working-tree base
(`merge-base HEAD <integration>`) is the correct selector.

### (e) §8.3 confirmation — MATCH
§8.3 "E5 backtest": *"POST-reflect with dirty `/task` work + a foreign commit in range → H4 FAIL closed
(wrong surface) until selector proven correct."* The two §8.3 conditions ("dirty `/task` work" +
"foreign commit in range") are exactly the two failure modes the commit message enumerates. The "FAIL
closed (wrong surface)" matches H4 treating the `start_commit..HEAD` selector as a failing surface.
Confirmed. (defect-escape-table REFLECT-E01 = #153 corroborates: "when task work was uncommitted, reflect
audited none of the actual changes; when foreign commits landed, it audited unrelated work.")

---

## Harness assertion table (the per-escape differential the eval harness must encode)

| Escape | Pre-fix parent (checkout target) | OLD=MISS (replay through prod entrypoint, fix reverted) | NEW=CATCH (H-wave gate behavior) | Wave |
|--------|-------------------------------|--------------------------------------------------------|----------------------------------|------|
| E1 | `94d5baa0` | Headless `--spec` argv contains `--file <local_path>`; `claude` exits 1 (session-token) / crashloop; pre-fix tests inspect argv without running → accepted clean | H1 negative-witness FAILs pre-fix, PASSes post-fix; `grep '"--file"'` → 0; sibling-pipeline contract sweep clean | H1 |
| E2 | `10723863` | `_check_parallel_instructions` returns `"Phase 7 missing parallel execution instructions …"` on a sequential completion final phase → HALT on a correct artifact | H3 classifier: real work-phase violation still HALTs; completion-titled near-miss (and `incomplete`-titled) correctly classified via `\b`-anchored word-boundary match | H3 |
| E3 | `e97aa4fd` | `gate_passed` has no advisory severity; Task-Log `### Phase N - … Findings` placeholder → fatal `(False, "Semantic check 'parallel_instructions' failed …")` → HALT | H3 unmask/sweep: `K_swept == K_true`; non-executable headings WARN/CONTINUE (advisory `continue`) not HALT | H3 |
| E4 | `1b0264f1` | `_evaluate_gate("build-task-file", …)` returns `False` (halts) despite advisory flag — `gate_passed` was fixed (E3) but the live executor's separate loop ignores `check.advisory` | H2 ledger enumerates BOTH consumers; `_evaluate_gate` returns `True` w/ advisory WARNING; FAIL until both classified | H2 |
| E5 | `d878bc6d` | `--diff start_commit..HEAD` range audits none of uncommitted `/task` work (and/or spans a foreign commit) → reflect vacuous-PASS over wrong surface | H4 FAIL-closed until selector proven: single-ref `merge-base HEAD <integration>` vs working tree; effective diff contains task files, excludes foreign commit | H4 |

---

## Summary

All five escapes are characterized 1:1 against their RELEASE-SPEC §8.3 backtest rows, with the fix SHA and
pre-fix parent SHA re-confirmed via `git show --stat` and the OLD bodies re-read at each parent
(`git show <parent>:<file>`):

- **E1 (`7601ad25` ⟂ `94d5baa0`, H1)** — removed local-path `--file` emission (`prd/process.py`
  `_build_file_args` + 3 dead consts) + inlined specs in `prd/prompts.py::_authoritative_specs_block`.
  OLD=MISS: crashloop on headless `--spec`, accepted by argv-only tests. NEW=CATCH: H1 negative witness.
- **E2 (`e97aa4fd` ⟂ `10723863`, H3)** — final-phase completion exemption + word-boundary signal match in
  `prd/gates.py::_check_parallel_instructions`. OLD=MISS: HALT on sequential final phase. NEW=CATCH: H3
  classifier discriminates `complete` vs `incomplete`.
- **E3 (`eb9a2633` ⟂ `e97aa4fd`, H3)** — added `SemanticCheck.advisory` + warn-don't-halt branch in
  `pipeline/gates.py::gate_passed`; marked `parallel_instructions` advisory. OLD=MISS: hard HALT on
  Task-Log placeholder headings. NEW=CATCH: H3 WARN/CONTINUE + `K_swept==K_true`.
- **E4 (`b97c9960` UNMERGED ⟂ `1b0264f1`, H2)** — mirrored the advisory branch into the live executor's
  `prd/executor.py::_evaluate_gate` (the second consumer `gate_passed` fix missed). OLD=MISS:
  `_evaluate_gate` returns `False` despite advisory. NEW=CATCH: H2 ledger requires BOTH consumers.
- **E5 (`10723863` ⟂ `d878bc6d`, H4)** — `task-builder/SKILL.md` POST-reflect base changed from
  `start_commit..HEAD` range to single-ref `merge-base HEAD <integration>` vs working tree. OLD=MISS:
  audits none of uncommitted work / spans foreign commit. NEW=CATCH: H4 FAIL-closed until selector proven.

**Key structural fact for the harness:** E3 and E4 are NOT independent — they are the **dual-evaluator
pair** for the *same* advisory mechanism. `gate_passed` (E3) and `_evaluate_gate` (E4) are two separate
consumers; the E4 escape exists *because* E3's fix was verified against the wrong consumer. The harness
must assert both, exactly as §8.3's E4 row states ("until both `gate_passed` and `_evaluate_gate`
consumers classified").

**Evidence:** all SHAs + file paths cited inline from `git show <sha>` and `git show <parent>:<file>`
diffs; cross-validated against `.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` and
RELEASE-SPEC §8.3.
