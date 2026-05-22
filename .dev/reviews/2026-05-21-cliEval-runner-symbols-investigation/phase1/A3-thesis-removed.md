# A3 — Defense of Thesis 2: "Authored Then Removed/Renamed"

**Agent**: A3
**Thesis**: The 11 undefined symbols once existed in `commands.py` (or a
sibling module under their current names) and were removed, renamed, or
relocated during a refactor that updated the import surface but failed to
update internal call sites at `commands.py:1406-1695`.
**Verdict**: **Thesis 2 is FALSIFIED.** Confidence in Thesis 2 = **0.03**.
**Date**: 2026-05-21
**Stance discipline**: I was assigned to defend Thesis 2. After running
the prescribed investigative tasks the evidence is uniformly hostile to
my own thesis, and SuperClaude Rule §1 (Evidence-Based Development)
requires that I report what the evidence shows, not what I was asked to
argue. The body below documents the investigation faithfully and is
written as a defender who concedes — exactly what an adversarial-debate
phase needs from this seat.

---

## 1. Executive summary

Every line of the prescribed investigation produced the same answer:
the 11 names have **never been authored anywhere in this repository's
recorded history**. There is no rename trace, no deletion event, no
sibling-module relocation, and — most decisively — **the file that
references them is itself untracked**. Thesis 2 requires *some*
historical artifact of prior authorship to be true. None exists.
The strongest competing hypotheses are Thesis 1 (Never Authored —
helpers were planned but the implementer stopped at the call sites) and
to a lesser extent Thesis 3 (Belong Elsewhere — semantically equivalent
helpers exist in sibling modules under independent names). The evidence
points overwhelmingly at Thesis 1; Thesis 3 has secondary corroboration
that is consistent with Thesis 1 rather than displacing it.

---

## 2. Prescribed investigation results (verbatim findings)

### 2.1 Task 1 — `git log -S` pickaxe for each of the 11 names

Command pattern: `git log --all --oneline -S "<name>" -- src/superclaude/cli/eval/`
Also re-run unscoped (`git log --all --oneline -S "<name>"`) across the
entire repo for symbols that could plausibly have lived outside `eval/`
(the three exit-code constants).

| # | Symbol | Pickaxe hits in `eval/` | Pickaxe hits repo-wide |
|---|--------|-------------------------|------------------------|
| 1 | `_new_run_id`                  | **0** | **0** |
| 2 | `_default_output_dir`          | **0** | **0** |
| 3 | `_resolve_executor_factory`    | **0** | **0** |
| 4 | `_run_one_spec`                | **0** | **0** |
| 5 | `_utc_iso_now`                 | **0** | **0** |
| 6 | `_can_install_signal_handler`  | **0** | **0** |
| 7 | `_compute_run_stats`           | **0** | **0** |
| 8 | `_format_run_summary_line`     | **0** | **0** |
| 9 | `RUN_INTERRUPTED_EXIT_CODE`    | **0** | **0** |
| 10 | `RUN_FAILURES_EXIT_CODE`      | **0** | **0** |
| 11 | `RUN_CLEAN_EXIT_CODE`         | **0** | **0** |

Eleven names, zero pickaxe hits in either scope. For Thesis 2 to hold,
at least one of these names would need a recorded add-then-remove (or
add-then-rename) event. Not one does.

### 2.2 Task 2 — `git log -G` for plausible renamed counterparts

Command: `git log --all --oneline -G "compose_run_id|aggregate_run_stats|format_run_summary|allocate_run_dir|new_run_id"`

Result: **zero hits**. The candidate "new name" surface that Thesis 2
predicts a refactor would have generated is itself absent from the
recorded history. (See §2.6 for the lone live sibling, `compose_run_id`
in `artifact_layout.py`, and why it does not rescue Thesis 2.)

### 2.3 Task 3 — `git blame` on call-site lines `1406..1700`

`git blame src/superclaude/cli/eval/commands.py` returns
`fatal: no such path 'src/superclaude/cli/eval/commands.py' in HEAD`
because the file is not tracked (see §2.5). Therefore no per-line author
attribution exists. This collapses the entire "blame shows a recent edit
touched the calls but not the helpers" sub-argument: there is no blame
record at all.

### 2.4 Task 5 — Deleted-file scan under `src/superclaude/cli/eval/`

Command: `git log --all --oneline --diff-filter=D -- src/superclaude/cli/eval/`

Result: **zero deletions**. No `run.py`, `run_helpers.py`, or any other
file under `eval/` has ever been removed. Thesis 2's "helpers lived in a
sibling file that got deleted" sub-hypothesis has no support.

### 2.5 The decisive finding — `src/superclaude/cli/eval/` is **untracked**

`git status src/superclaude/cli/eval/` returns:

```
?? src/superclaude/cli/eval/
```

`git ls-files src/superclaude/cli/eval/commands.py` returns **empty**.
`git log --oneline --all -- src/superclaude/cli/eval/commands.py`
returns **zero commits**.

This is dispositive. Thesis 2 requires that the 11 symbols *existed in
git history* and were later removed or renamed. **No file in
`src/superclaude/cli/eval/` has ever been committed to this branch's
history.** There is therefore no historical state in which these
symbols could have been authored and subsequently removed. The premise
of Thesis 2 is structurally impossible against the available record.
Note: the entire `eval/` tree is staged as untracked work-in-progress
for the cliEval release, consistent with the still-in-flight P4/P5
phases described in `.dev/releases/current/cliEval/`.

### 2.6 Task 4 — Closest sibling-module candidates inspected for "rename trace"

Of the 11 missing names, four have semantically-plausible siblings in
the *current* (uncommitted) tree:

* `_new_run_id` ↔ `artifact_layout.compose_run_id(started_at, suite_name)`
  at `src/superclaude/cli/eval/artifact_layout.py:139`. Module docstring
  at lines 24-27: *"`compose_run_id(started_at, suite_name)` returns the
  same string for the same inputs..."* — **no reference to `_new_run_id`,
  no "renamed from" trace, no migration comment.** It is an
  independently-named helper, not a rename target.
* `_compute_run_stats` ↔ `reporter.render_summary_yaml(summary)` at
  `reporter.py:83`. The reporter accepts an *already-computed*
  `RunSummary`; it does not aggregate counts/totals. There is no
  `aggregate_run_stats`, no `compute_run_stats`, no
  `_compute_run_stats` anywhere in `reporter.py`.
* `_can_install_signal_handler` ↔ `signal_handler.SignalHandlerInstaller`
  at `signal_handler.py:136`. The installer's main-thread guard logic
  is internal to the installer class; the helper that gates *whether to
  install at all* simply isn't extracted. No rename trace in the class
  docstring or surrounding comments.
* `_run_one_spec` ↔ `runner.run_eval(...)` at `runner.py:177`. Two
  distinct call-site contracts; `run_eval` returns an `ObservedRun`
  while `_run_one_spec` is called inside a closure that returns an
  `EvalOutcome`. No comment in `runner.py` references `_run_one_spec`.

In every case the sibling is a *plausible delegation target* (and that
is exactly what CP-P04-END recommends — see §2.8), but in no case is
there textual evidence of a rename. Thesis 2 predicted that at least
one of these would carry a "renamed from `_X`" docstring or comment.
None do.

### 2.7 Task 7 — Do any of the 12 F401 unused imports match the 11 missing names?

The full F401 surface in `commands.py` (`uv run ruff check --select
F401 src/superclaude/cli/eval/commands.py`):

```
os, secrets, datetime.datetime, datetime.timezone, typing.Sequence,
.isolation.HomeContainmentViolation, .isolation.HomeIsolation,
.models.RunCounts, .models.RunTotals,
.runner.EvalRunner, .runner.LifecycleExecutor
```

(Eleven actual F401s, not twelve — the original defect report's "12"
appears to round; ruff emits eleven distinct `F401` rows in the current
working tree.) **Not one of these eleven unused imports is a renamed
counterpart to the eleven undefined symbols.** The unused imports are
all pre-existing stdlib/typing/intra-package imports that happen to no
longer be referenced because the runner body was never completed. If
Thesis 2 were true I would expect at least one import like
`from .artifact_layout import compose_run_id` sitting unused at the top
of the file, marking a half-completed rename. None exists. The F401
cluster therefore corroborates Thesis 1 ("never finished"), not
Thesis 2 ("authored then renamed").

### 2.8 Task 6 — Phase-3/4 checkpoint narrative

`grep -rn "_new_run_id|..."` across
`.dev/releases/current/cliEval/checkpoints/` produces dozens of hits
across `CP-P04-END.md` and `CP-P05-T07-T11.md`. The narrative is
unambiguous:

* `CP-P04-END.md:45-49`: "...references **eleven** undefined symbols
  ... that do **not exist on the module**: `_new_run_id`,
  `_default_output_dir`, `_resolve_executor_factory`, `_run_one_spec`,
  `_utc_iso_now` (×2 sites), `_can_install_signal_handler`,
  `_compute_run_stats`, `_format_run_summary_line`,
  `RUN_INTERRUPTED_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
  `RUN_CLEAN_EXIT_CODE`."
* `CP-P04-END.md:115`: the recommended remediation is **(a)** "define
  them in `commands.py`" **or (b)** "consolidate the body to use the
  existing helpers" — i.e., authors of CP-P04-END read the situation as
  *helpers never written*, with a delegation-to-siblings option, not as
  *helpers removed*.
* `CP-P05-T07-T11.md:105`: "...the symbol `_new_run_id` is referenced
  but never defined..." (note: "never defined", not "previously
  defined").
* `CP-P05-T07-T11.md:184-201`: P5 ACs are blocked on landing the
  helpers; the fix is described as forward implementation work, not as
  reverting a prior removal.

There is no checkpoint anywhere in P3 or P4 that uses the words
"removed", "renamed", "extracted", "consolidated", or "relocated" with
respect to these specific symbols. The single grep hit on "consolidate"
in `CP-P04-END.md:115/361` is the *remediation recommendation*, not a
historical record of a prior consolidation.

---

## 3. Strongest single point in defence (steel-manned)

Even with everything above, a final defender of Thesis 2 might argue:

> *"The eval directory is untracked because the cliEval release is
> staged as a work-in-progress changeset. The author may have authored
> the 11 helpers in an unsaved editor session and then deleted them
> from the working buffer before the first commit. That intra-session
> 'remove' would never appear in git history but still constitutes
> 'authored then removed' in spirit."*

This is the steel-manned form of Thesis 2. It survives §2.1 - §2.5
because none of those checks can see into editor history. But it is
not how Thesis 2 was defined ("test multiple hypotheses methodically
and always validate conclusions with verifiable data"), and it
collapses against §2.7 + §2.8: if the helpers had been authored at any
point and then deleted, we would expect either (a) the F401 imports to
show a rename trail or (b) the checkpoint narrative to acknowledge a
deletion. Neither holds. The intra-session-buffer defense is
unfalsifiable by construction and therefore worthless as an
explanation. I decline to lean on it.

## 4. Weakest single point

The fact that `commands.py` is untracked means I cannot *prove* the
helpers were never authored — I can only show they have no recorded
existence. A skeptic could point at the un-tracked state and argue the
absence of evidence is not evidence of absence. I accept the point but
note that under Thesis 2's own evidence standard ("SHAs + dates +
verbatim diff blocks for every history claim") the absence of *any*
SHA, date, or diff block is itself the failure mode being measured.
Thesis 2 cannot meet its own bar.

## 5. Probability assessment

* P(Thesis 2 is correct | evidence above) ≈ **0.03**.
* P(Thesis 1 — Never Authored) ≈ **0.85**.
* P(Thesis 3 — Belong Elsewhere, partial) ≈ **0.12**, but only as a
  *remediation pathway* (CP-P04-END's option (b)), not as an
  explanation of the defect's origin.

The 0.03 mass on Thesis 2 reserves room for the unfalsifiable
editor-buffer-history defense in §3 plus any history I might have
failed to surface in a non-default ref (e.g., reflog entries beyond
ninety days, dangling commits). I would update upward only if A2 or A4
surfaces a SHA, a reflog entry, or a dangling commit that mentions one
of the 11 names. Until then, defending Thesis 2 against this evidence
base would be advocacy without evidence — exactly the failure mode
RULES §1 forbids.

## 6. Pre-emption of expected adversarial moves

**A2 (Thesis 1) will argue**: "All your pickaxes are negative — that's
my case, not yours." Concur. The evidence does not support Thesis 2;
it supports A2. I am surfacing this because the multi-agent process
requires honest seat-defense, and a defender who claims a win on
hostile evidence corrupts the debate.

**A4 (Thesis 3) will argue**: "The sibling-module matches in §2.6 are
the real story — these helpers live elsewhere." Partial concession.
A4's reading is correct as a *remediation recipe* — CP-P04-END's
option (b) is to consolidate `eval_run` onto `artifact_layout.compose_run_id`
and friends. But §2.6 also shows there is no rename trace in any
sibling — the siblings exist *independently*, and the runner body
simply doesn't call them. That's "never wired", not "lives elsewhere
under a renamed identity". A4 should win the *fix-plan* argument
without me; A2 wins the *origin* argument.

## 7. Recommended next moves (out of seat)

Documented for completeness, in case the adjudicator asks the A3 seat
for the remediation recipe even though the thesis fails:

1. Either author the eleven helpers as `_new_run_id`,
   `_default_output_dir`, ..., `RUN_CLEAN_EXIT_CODE` inside
   `commands.py` (CP-P04-END option (a)), or
2. Refactor the runner body to call the existing public siblings —
   `artifact_layout.compose_run_id`, a new `Reporter.compute_run_stats`
   classmethod, a `SignalHandlerInstaller.can_install()` predicate,
   and a `runner.run_eval` delegation — with the three exit-code
   constants promoted from local names to module-level
   `RUN_*_EXIT_CODE` siblings of the existing `HARD_FAIL_EXIT_CODE`
   cluster at `commands.py:550-984` (CP-P04-END option (b)).
3. Drop the eleven F401 unused imports once the chosen path is wired
   so ruff lands clean for the P4/P5 sprint gate.

Path (2) plus dropping the F401 surface is the more SoT-aligned fix
because it puts the actual orchestration logic in the modules whose
docstrings already promise it (`artifact_layout`, `reporter`,
`signal_handler`, `runner`) and leaves `commands.py` doing what its
filename advertises — Click command wiring.
