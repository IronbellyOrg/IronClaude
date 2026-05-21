# A2 — Thesis 1: Never Authored

**Investigator:** Agent A2 (defender of Thesis 1)
**Date:** 2026-05-21
**Scope:** The 11 undefined symbols in `src/superclaude/cli/eval/commands.py::eval_run` (lines 1406-1695).

---

## 1. Thesis Statement

The 11 symbols (`_new_run_id`, `_default_output_dir`,
`_resolve_executor_factory`, `_run_one_spec`, `_utc_iso_now`,
`_can_install_signal_handler`, `_compute_run_stats`,
`_format_run_summary_line`, `RUN_INTERRUPTED_EXIT_CODE`,
`RUN_FAILURES_EXIT_CODE`, `RUN_CLEAN_EXIT_CODE`) **were never
implemented as concrete definitions inside the `cli/eval` module at
any point in repository history.** The `eval_run` body was authored
forward-referencing a planned helper layer that the project's own
roadmap explicitly scheduled to land **inside task T04.10** of Phase
4. T04.10 closed at status FAIL with the helper-authorship subtask
never executed. The defect is therefore **not** a regression
(nothing was removed), **not** a misnamed sibling (no sibling has
the same signature *and* call site), and **not** an "owns elsewhere"
import gap (no other module exports any of these eleven names under
any name). They are abstract obligations that the author of the
`eval_run` body discharged forward-of-knowledge — Click renders
`--help` from the decorator stack without ever touching the body, so
the gap was masked by a green smoke-help test and only manifests on
the first real invocation.

A precise restatement: **eleven obligations were written into the
call site; zero of the eleven were ever discharged into a `def`
or constant binding under `src/superclaude/cli/eval/`.**

---

## 2. Supporting Evidence

### 2.1 Git-pickaxe (-S) returns empty for 10 of 11 names across ALL branches and history

Running `git log --all --oneline -S "<name>"` against the eleven names produced **zero hits** for ten of them and three unrelated hits (all in roadmap / sprint / sc-pm modules) for `_default_output_dir`. The unrelated hits do not name the `cli/eval` directory:

```
=== _new_run_id ===                          (empty)
=== _default_output_dir ===
7097608 feat(sprint): land C1-C4 deterministic runner fixes …
478a5e0 docs(hook-sync): release artifacts + NFR-CONV-2 …
6aa76aa chore(tasks): archive 5 CI-rot RF tracks to done/ …
38a44d3 update
c0599e3 feat(sc:roadmap): add Wave 4-5 implementation details …
=== _resolve_executor_factory ===            (empty)
=== _run_one_spec ===                        (empty)
=== _utc_iso_now ===                         (empty)
=== _can_install_signal_handler ===          (empty)
=== _compute_run_stats ===                   (empty)
=== _format_run_summary_line ===             (empty)
=== RUN_INTERRUPTED_EXIT_CODE ===            (empty)
=== RUN_FAILURES_EXIT_CODE ===               (empty)
=== RUN_CLEAN_EXIT_CODE ===                  (empty)
```

To rule out the false positive, the same pickaxe was rescoped to the
eval module:

```
$ git log --all --oneline -S "_default_output_dir" -- src/superclaude/cli/eval/
(no output)
```

And the combined -G pattern over **all eleven** names, scoped to the
module:

```
$ git log --all --oneline -G "(_new_run_id|_default_output_dir|…|RUN_CLEAN_EXIT_CODE)" \
    -- src/superclaude/cli/eval/
(no output)
```

**Conclusion:** No commit in any branch has ever added or removed a
definition for any of these eleven names inside `cli/eval`. The only
appearance of these strings inside `cli/eval` in the current tree is
on the reference sites at lines 1467, 1469, 1577, 1598, 1612, 1624,
1636, 1642, 1671, 1677, 1694, 1695 — the very call sites that fail.

### 2.2 The checkpoint that closed T04.10 enumerates all eleven as still-missing

`.dev/releases/current/cliEval/checkpoints/CP-P04-END.md:43-47`
explicitly lists the cluster:

> "the body at `commands.py:1418..1646` references **eleven**
> undefined symbols (`_new_run_id`, `_default_output_dir`,
> `_resolve_executor_factory`, `_run_one_spec`, `_utc_iso_now` ×2,
> `_can_install_signal_handler`, `_compute_run_stats`,
> `_format_run_summary_line`, `RUN_INTERRUPTED_EXIT_CODE`,
> `RUN_FAILURES_EXIT_CODE`, `RUN_CLEAN_EXIT_CODE`); ruff reports the
> cluster as `F821`."

Same file at lines 108-116 names the remediation:

> "Either (a) **author the eleven missing helper symbols**
> (`_new_run_id`, `_default_output_dir`, `_resolve_executor_factory`,
> `_run_one_spec`, `_utc_iso_now`, `_can_install_signal_handler`,
> `_compute_run_stats`, `_format_run_summary_line`, …) or (b)
> rewrite the body to use already-landed helpers."

The phrasing is dispositive: **option (a) is "author them"**, not
"restore them" / "re-add them" / "merge them back from branch X" —
which is the diction the project consistently uses for regressions
(cf. CP-P04-T07-T11.md:11 "functionally landed in production code"
versus the eleven where the diction is "not on the tree" and
"missing").

### 2.3 D-0081/notes.md schedules the eleven *inside* T04.10 as "adds"

`.dev/releases/current/cliEval/artifacts/D-0081/notes.md:105-110`:

> "## T04.10 hand-off
>
> T04.10 is the run-loop closure that **adds** `_new_run_id`,
> `_run_one_spec`, `_compute_run_stats`, and the three terminal
> exit-code constants. **Once T04.10 lands:** Tests 5 and 6 un-skip
> automatically … the OPS-003 advice path becomes reachable in
> normal end-to-end runs …"

The verb "adds" and the forward-conditional clause "Once T04.10
lands" cannot describe a removed symbol; they describe authorship
work that the design declared the *responsibility* of T04.10 to
discharge — and that T04.10 then failed to complete.

### 2.4 Tests reference the eleven as "T04.10-wired", not "imported", and skip pending the helpers

`tests/cli/eval/test_no_mcp_skip.py:32-33` (and parallel docstrings in
`test_no_pty_exclusion.py`, `test_exit_codes.py`):

> "T04.10 wires the run helpers (`_run_one_spec`, `_new_run_id`,
> `_compute_run_stats`, `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`)
> plus the `--no-mcp` runtime …"

`tests/cli/eval/test_exit_codes.py:205, 359` repeatedly defers
end-to-end exit-code assertions:

> "T04.10's `_run_one_spec` — we skip until that helper lands"
> "raises NameError on `_new_run_id` before reaching the wait"

`tests/cli/eval/test_validation_commands.py:167-172`:

> "B1 (_new_run_id) and B2 (ptytest) are explicitly recorded …
> B1 must name **the missing helper** (`_new_run_id`) so the
> follow-up …"

The validation surface (`PatchChecklist.md` / `ValidationReport.md`)
records the missing helper as known-blocker **B1**. The diction
"missing helper" and "follow-up" again refuses the "regression"
framing.

### 2.5 The Phase-5 capture shows the live NameError + names the responsible task

`.dev/releases/current/cliEval/checkpoints/CP-P05-END.md` (live
capture during the M5 gate):

> ```
> File "…/eval/commands.py", line 1418, in eval_run
>     run_id = _new_run_id()
>              ^^^^^^^^^^^
> NameError: name '_new_run_id' is not defined
> ```
>
> "The Phase-4 follow-up task track
> `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/`
> still **owns this remediation** and has not landed."

A live follow-up task ticket (`TASK-RF-20260518-cliEval-P4-wire-and-ship`)
sits in `.dev/tasks/to-do/` waiting to be picked up. There is no
companion ticket in `.dev/tasks/done/` for the helper authorship —
which would exist if the helpers had ever been authored and removed.

### 2.6 The runtime evidence is consistent across 9+ independent invocations

The same NameError stack is captured verbatim in (at least):
`evidence/T04.22/ruff-check.log` (lines 132, 137, 146); `T05.04`,
`T05.08`, `T05.09`, `T05.10`, `T05.11`, `T05.19`, `T05.21`, `T05.25`,
`T05.28`, `T06.11` README/log files. The cardinality on disk is 9
distinct evidence directories that all converge on the same line
and the same first-blame symbol. This is incompatible with the
"belong elsewhere / import gap" story (which would surface
`ImportError` not `NameError`) and incompatible with the "removed"
story (which would have a git-rm in history).

### 2.7 The design-spec mentions run-id / output-dir abstractly only

`design-spec.md` references "`run_id`" in the abstract data shape
(line 21: ".dev/eval-runs/<ISO>/<run-id>/"; line 194 as a
`--output-dir` token; line 381 as `hash(eval_id + run_id)[:16]`; line
535 as a JSON field). It does **not** specify a home module, a
function signature, a callable name, or constant identifiers for any
of the eleven symbols. The eleven names are local design choices the
T04.10 author made — and never made concrete. **Concretely:** the
design said "you need a way to allocate a run id"; the `eval_run`
body said "I'll call `_new_run_id()`"; no file said "here's the
implementation". This is the textbook "never authored" signature.

---

## 3. Falsifying Evidence (self-honesty)

I will not dodge the items that weaken my thesis. There are two.

### 3.1 `compose_run_id` exists in `artifact_layout.py:139` — a functional sibling for ONE of the eleven

`CP-P05-END.md` notes:

> "the already-landed replacement `artifact_layout.compose_run_id`
> (`artifact_layout.py:139`) has not been wired into the call site"

This is a real near-equivalent for `_new_run_id`. The signature
differs (`compose_run_id(started_at: str, suite_name: str = "")`
versus the bare `_new_run_id()` call at line 1467, which receives
no arguments), so the call site cannot be a literal "you forgot
to write the underscore-prefix wrapper" — the T04.10 author either
(a) was unaware of `compose_run_id` and meant to author a separate
helper, or (b) intended a thin wrapper that fixes a started-at
default and never wrote it. **Either way, the bare `_new_run_id`
itself was never authored**, but A4 can plausibly argue that 1-of-11
"belongs elsewhere".

`run_eval` at `runner.py:177` is a similar near-equivalent for
`_run_one_spec` — the runner module owns the per-eval lifecycle, so
A4 will argue `_run_one_spec` was an intended thin closure that
wraps `run_eval`. Same self-honest concession: **A wrapper that
never landed is still "never authored", but A4 can plausibly argue
that the symbol's true home is the existing `runner.py` and the
fix is wiring, not authoring.**

For the remaining **9 of 11** symbols (`_default_output_dir`,
`_resolve_executor_factory`, `_utc_iso_now`,
`_can_install_signal_handler`, `_compute_run_stats`,
`_format_run_summary_line`, and the three `RUN_*_EXIT_CODE`
constants), I have not found any sibling with a near-identical
signature. A4 will need to argue much harder for those.

### 3.2 The unrelated `_default_output_dir` git hits

The five commits returned by `git log -S "_default_output_dir"` are
all in `sprint`, `sc:roadmap`, and `hook-sync` modules — unrelated
identifiers that happen to share the same string token in
docstrings or argument names. `git log -S "_default_output_dir" --
src/superclaude/cli/eval/` returns empty, confirming the hits do
not implicate `cli/eval`. A3 may try to argue that "a removal could
have escaped pickaxe under a refactor that renamed *and* deleted
the symbol in the same commit, which `-S` *does* see but `-G`
doesn't". I rebut this in §5: the combined `-G` over all eleven
names scoped to `cli/eval/` also returns empty, and `-G` *does*
catch rename-and-delete because it matches added or removed lines
containing the regex. Both pickaxe modes converging on zero is
strong evidence — though A3 can still raise *outside-`cli/eval/`*
relocations, which I address in §5.

---

## 4. Strongest Point

**The narrative diction in the project's own checkpoint trail is
"author" / "missing helper" / "adds … once T04.10 lands", not
"restore" / "regression" / "merge back".** A project that had once
authored these eleven symbols and lost them would describe the
remediation as a restoration. A project that knows it never wrote
them describes the remediation as authoring. CP-P04-END.md:109,
D-0081/notes.md:106, and ValidationReport.md's B1 entry all use
the authoring diction, and the human-authored test docstrings
(test_no_mcp_skip.py:32, test_exit_codes.py:35) use the
forward-tense "T04.10 wires …" — a future-tense schedule against
helpers that don't yet exist. That diction is consistent with no
prior authorship; it is inconsistent with deletion. Combined with
zero hits across both `-S` and `-G` pickaxe modes (any
deletion would have left at least one removal-line hit), the
authorship-never-occurred conclusion is over-determined.

---

## 5. Weakest Point

**The pickaxe is module-scoped, and a relocator could in principle
have moved the symbols out of `cli/eval/` entirely before any of
the current branches were created.** If, hypothetically, the
eleven helpers once lived in `src/superclaude/cli/_eval_helpers.py`
(or any other file) and were then deleted in a force-pushed
history-rewritten commit, the current `git log --all` would not
necessarily see them. I have NOT (within the time budget of this
investigation) run the pickaxe over the entire repository tree
(only `src/superclaude/cli/eval/`). A3 could plausibly point at a
deleted file under, say, `src/superclaude/cli/eval/_helpers.py` or
even `src/superclaude/helpers/run.py` that once held the eleven
names. If A3 produces *any* hit anywhere in repo history for the
strings `_new_run_id`, `_resolve_executor_factory`,
`_compute_run_stats`, or the three `RUN_*_EXIT_CODE` constants —
in any path — that materially weakens my thesis.

(I would still argue that the diction in CP-P04-END.md / D-0081
overrides the pickaxe hit — the human authors of the checkpoint
trail describe the work as "authoring", which is much harder to
square with "we deleted them and now have to put them back". But
the probability would shift.)

---

## 6. Probability Estimate

**P(Thesis 1 correct) = 0.82, range 0.74–0.90.**

The high end (0.90) reflects: (a) two independent pickaxe modes
returning zero inside the eval module, (b) the dispositive
narrative diction in CP-P04-END.md and D-0081, (c) nine separate
runtime captures of the NameError on the unchanged call site, (d)
the live follow-up ticket in `.dev/tasks/to-do/` rather than a
"done" record, (e) test docstrings using future-tense scheduling
diction, and (f) the design-spec referencing the underlying *needs*
(run id, output dir, exit codes) abstractly without binding them to
named symbols.

The low end (0.74) reflects: (i) I did not pickaxe outside
`cli/eval/`, leaving room for a relocated-and-deleted alternate
home; (ii) two of the eleven (`_new_run_id`, `_run_one_spec`) have
plausible sibling near-equivalents, which Thesis 3 (A4) can lean
on; (iii) it is conceivable that an intermediate dev branch (now
abandoned and never merged) once held the helpers and was deleted
without leaving a trace, although this would not be visible from
`git log --all` only if the branch was force-deleted and garbage-
collected from the reflog of every clone — unlikely on a shared
repo but not impossible.

The point estimate of 0.82 reflects my honest read that the
narrative + pickaxe evidence is jointly very strong for "never
authored", with residual uncertainty concentrated in the
sibling-relocation argument that A4 will push.

---

## 7. Open Questions

1. **Cross-tree pickaxe.** Did any branch, at any point, contain a
   `def _new_run_id` / `def _compute_run_stats` / `def _run_one_spec`
   *anywhere* in the repo (not just under `cli/eval/`)? If A3 can
   produce a single such hit on **any path**, my §5 caveat becomes
   active and Thesis 2 deserves serious consideration.

2. **`compose_run_id` vs `_new_run_id`.** Is the project's intent
   "wire `compose_run_id` directly into line 1467" or "author a
   `_new_run_id()` wrapper that calls `compose_run_id(_utc_iso_now())`
   for ergonomics"? The design-spec is silent; D-0081/notes.md is
   silent; this is genuinely ambiguous. If A4 can show the project
   *intended* a direct wiring of existing siblings, then Thesis 3
   ("belong elsewhere — just wire them") gains weight for at least
   `_new_run_id` and `_run_one_spec`.

3. **Three `RUN_*_EXIT_CODE` constants.** Design-spec §4 specifies
   the *values* (0, 1, 2, 3) but does not name the constants. The
   project already exports `HARD_FAIL_EXIT_CODE = 2` at
   `commands.py:550` and similar exit-code constants from
   `loader.py` (`SUITE_LOADER_ERROR_EXIT_CODE`,
   `SUITE_NOT_FOUND_EXIT_CODE`) and the runner. So three more
   constants would be *trivial* to author (3 lines of code). The
   fact that even these one-line constants never landed strengthens
   the "never authored" reading — if the project had ever authored
   the harder helpers and deleted them, the three trivial constants
   would almost certainly survive somewhere. Their absence is
   probative.

4. **Why was T04.10 abandoned mid-task?** No checkpoint narrates the
   *reason* T04.10 stopped before authoring the helpers. Was it a
   time-box exhaustion, a deferred design decision, or did the
   author lose the work? This is forensic curiosity rather than
   load-bearing for the thesis, but worth flagging for downstream
   remediation planning.

5. **Whether the integration branch `master` or any feature branch
   has a divergent copy.** `git log --all` was used, but a branch
   that was pruned (`git remote prune` + `git gc`) before the
   current investigation could have held the helpers. The
   probability is low for a project this active, but non-zero.
