# Research: Spec / CG-4

Status: Complete
Date: 2026-06-03

**Scope:** SPEC DOCS ONLY — `design.md` (27.8 KB) + `merged-requirements.md` (13.2 KB) in
`.dev/brainstorms/20260602-sprint-auto-resume-default/`. Owns CG-4 (spec self-contradiction),
the F-2 design-amendment surface, and the F-4 spec basis. Researchers 01–04 own the code
internals; I read cited code lines ONLY to tag doc claims [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED].

**Tag legend:**
- `[CODE-VERIFIED]` — the spec passage describes behavior that the implementation actually exhibits.
- `[CODE-CONTRADICTED]` — the spec passage describes behavior the implementation does NOT exhibit
  (the implementation diverges from this specific spec line).
- `[UNVERIFIED]` — pure spec text, no implementation claim to check.

---

## 1. CG-4 — The spec self-contradiction (VERBATIM)

CG-4 is a **requirements-level** contradiction: two passages in the same spec corpus disagree on
whether a bare `sprint run --yes` may proceed past *reported-but-not-quarantined* partial work.
The implementation could not satisfy both; it resolved toward §7.

### 1a. design §7 — happy-path `passed=True` with half-written outputs merely *reported*

`design.md:292-296` (VERBATIM):

```
     ├─ BoundaryIntegrityGate.run → validate T03.3 (last PASS, artifacts ok) ✓;
     │     report half-written T03.4 outputs (copy→.resume-quarantine-<ts>/ if opted in); passed=True
     ├─ print_plan(...)  "Resuming phase 3 · phases 1-2 complete · re-running T03.4 · drift 1.0"
     ├─ prompt (skipped: --yes / interactive assent)
     └─ dispatch → run_rerun_tasks(phase=3, tasks=[T03.4]) → merge_back refreshes result.json
```

Key clause (`design.md:293`): *"report half-written T03.4 outputs (copy→.resume-quarantine-<ts>/
**if opted in**); **passed=True**"*. Under §7, partial work is **reported**, quarantine is
**opt-in only** (default report-only), and the gate **passes** — the resume plan simply re-runs
that task. Quarantine is NOT a precondition of `passed`.

`[CODE-VERIFIED]` — `integrity.py:314` `return accept_suspect or report.validated_last`. The
verdict is a pure function of `validated_last` (+ the `accept_suspect` override); detected partial
work is surfaced (`integrity.py:64-65`) but never enters `passed`. The docstring at
`integrity.py:310-312` states this explicitly: *"The hard gate is last-completed integrity.
Boundary partial work is surfaced (FR-2.2) but does NOT flip the verdict — the resume plan re-runs
that task (§7)."* The implementation faithfully follows §7.

### 1b. design §4(c) — the HARD-gate formula that §7 omits

`design.md:184-187` (VERBATIM):

```
  # (c) gate verdict (FR-2.4 — hard gate). PURE function of deterministic signals; Haiku
  # coherence_warnings are surfaced in print_plan for the operator but are NOT in `passed` (NFR-3).
  passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)
  if not passed: blocking_reasons explain exactly what must be resolved → caller STOPs
```

The operative formula (`design.md:186`):
`passed = validated_last AND (no unresolved suspects) AND (partial work quarantined or accepted)`.

This formula has a **third conjunct** — `(partial work quarantined or accepted)` — that §7's
`passed=True` line silently drops. Under §4(c), `passed` cannot be True while partial work exists
unless that work is **quarantined** OR **accepted**.

`[CODE-CONTRADICTED]` — `integrity.py:314` implements only the FIRST conjunct
(`validated_last`, with `accept_suspect` as the override knob). The `(no unresolved suspects)` and
`(partial work quarantined or accepted)` conjuncts from `design.md:186` are **absent** from
`_verdict`. The implementation chose the §7 reading (`integrity.py:73` comment: *"Boundary partial
work does NOT flip the verdict (§7)."*) over the §4(c) reading. This is the exact code-level
fingerprint of the CG-4 contradiction: **§4(c):186 and the implementation disagree.**

### 1c. merged-requirements FR-2.4 — the HARD gate (full text)

`merged-requirements.md:85-87` (VERBATIM):

```
- FR-2.4 **Gate condition (hard):** resume MUST NOT proceed until (a) boundary half-finished
  work is cleaned or explicitly assessed-and-accepted, AND (b) the last completed task is
  doubly validated. Failure ⇒ STOP with a report and require operator decision.
```

FR-2.4 condition (a): *"boundary half-finished work is **cleaned OR explicitly
assessed-and-accepted**"* — this is the requirements-level source of §4(c)'s third conjunct.
Note FR-2.4 makes BOTH (a) and (b) preconditions of "MUST NOT proceed"; §4(c) encodes (a) as
`(partial work quarantined or accepted)` and (b) as `validated_last`.

`[CODE-CONTRADICTED]` (condition (a) only) — the implementation enforces (b) `validated_last`
(`integrity.py:314`) but NOT (a) on the `--yes`/CI path: partial work is neither cleaned
(quarantine is opt-in, default report-only — `integrity.py:66-67`) nor genuinely
"assessed-and-accepted" (the prompt is skipped under `--yes`, AND per F-2 the partial **paths**
are not even printed on the report-only path — see §3). So on `--yes`, FR-2.4(a)'s
"assessed-and-accepted" is not actually satisfied — it is *bypassed*, not *met*.

### 1d. FR-2.1 — treat a pass status as a claim to be re-checked

`merged-requirements.md:76-79` (VERBATIM):

```
- FR-2.1 **Last completed task — deep suspicion validation.** Re-verify the last
  confirmed-completed task's declared deliverables/checkpoints actually exist and are
  coherent (checkpoint file existence per `checkpoints.py`, deliverable paths, and a
  targeted coherence read). Treat a "pass" status as a claim to be re-checked, not trusted.
```

FR-2.1 is the (b) leg of FR-2.4 — *"Treat a 'pass' status as a claim to be re-checked, not
trusted."* This is the conjunct the implementation DOES honor.

`[CODE-VERIFIED]` — `integrity.py:90-101` (`_validate_last_completed`): *"A PASS claim is
RE-CHECKED, never trusted (R1)."* Signal A (persisted) is reconciled against Signal B (derived
from transcript) + artifacts existence. This leg is implemented; the gap is purely the (a) leg
(partial-work) on the `--yes` path.

### 1e. The precise contradiction (stated)

> Under **design §7** (`design.md:293`), a bare `sprint run --yes` whose boundary has merely
> *reported* (not quarantined) partial work **passes the gate and proceeds** — quarantine is
> opt-in, `passed=True`.
>
> Under **design §4(c)** (`design.md:186`) and **FR-2.4** (`merged-requirements.md:85-87`), the
> same run **MUST NOT proceed**: `passed` requires `(partial work quarantined OR accepted)`, and
> on `--yes` the partial work is neither quarantined (default report-only) nor genuinely
> assessed-and-accepted (prompt skipped + paths not shown).

Both passages cite **the same requirement (FR-2.4)** as their authority — §4(c):184 says
"(FR-2.4 — hard gate)" while §7:293 enacts the soft "report + passed=True" reading. The spec
contradicts itself about what FR-2.4 *means* on the non-interactive path. This cannot be resolved
in code alone (the implementation already had to pick one — it picked §7); it needs an
**authoritative operator ruling.**

---

## 2. The EXACT decision CG-4 needs (binary, operator-facing)

> **DECISION CG-4:** Does bare `sprint run --yes` proceeding past **REPORTED-but-not-quarantined**
> partial work satisfy FR-2.4(a) *"cleaned OR explicitly assessed-and-accepted"*?

This is a binary ruling. The two options are mutually exclusive on the `--yes`/CI path; the
interactive path is unaffected (an operator who sees the prompt and assents IS "assessed-and-accepted").

### Option YES — §7 governs; F-1 is as-designed
- **Reading:** On `--yes`/CI, "printing the plan + the operator pre-authorizing via `--yes`" IS a
  form of acceptance. The resume engine re-runs the boundary task, so the half-written outputs are
  about to be overwritten anyway — quarantine is a courtesy, not a safety precondition.
- **Consequence for F-1:** F-1 downgrades to *as-designed* (the report's current lean is
  "Necessary deviation + residual safety gap" — see REPORT.md:35-39). No gate tightening.
- **Required companion fix:** the F-2 path-surfacing **MUST** land, so that "reported" is
  *meaningful* — today `--yes` proceeds without even printing the partial paths (§3), so the
  operator's `--yes` is uninformed consent. YES is only defensible if the paths are shown.
- **Spec edits:** amend §4(c):186 to MATCH the implementation — drop the
  `(partial work quarantined or accepted)` conjunct OR re-word it to
  `(partial work reported AND (quarantined OR operator-assented-or---yes))`. Amend FR-2.4(a) to
  state that on the non-interactive path, "`--yes` + a printed partial-paths report" constitutes
  "explicitly assessed-and-accepted." §7 stays as-is.

### Option NO — §4(c)/FR-2.4 governs; tighten the gate
- **Reading:** "Assessed-and-accepted" requires a *positive* disposition of the partial work —
  either it is quarantined (cleaned) or a human/flag explicitly accepts THAT SPECIFIC partial
  work. A blanket `--yes` (which exists for the *drift* prompt, NFR-4/FR-3.4) is NOT consent to
  proceed over un-cleaned partial work. Silent proceed defeats the "non-idempotent seam is
  suspect" thesis (`merged-requirements.md:30-33`).
- **Consequence for F-1:** F-1 is a genuine **safety gap** — the gate must change. On `--yes`/CI,
  partial work present ⇒ either auto-quarantine (clean) OR hard-STOP with `blocking_reasons` until
  the operator passes an explicit accept flag (e.g. `--accept-partial`).
- **Spec edits:** §7:293 must be amended to remove the unconditional `passed=True` when partial
  work exists — replace with `passed=True only if (partial quarantined OR --accept-partial)`. §4(c)
  and FR-2.4 stay as-is (they already say this). `integrity.py:314` `_verdict` must add the third
  conjunct.

### Recommended default ruling: **YES (with the F-2 fix as a hard prerequisite)**

**Rationale:**
1. **The implementation already shipped §7**, was reviewed through 9 in-band gates, and the
   re-run-overwrites-the-boundary-task design means the half-written outputs are transient by
   construction (the dispatched `run_rerun_tasks` re-runs that exact task — `design.md:296`). The
   safety value of *quarantining* output that is about to be regenerated is low.
2. **The report itself leans YES-ish:** F-1 is adjudicated *"Necessary deviation + residual safety
   gap"* (REPORT.md:35), NOT a clean regression — *"The implementation resolved toward §7 and
   logged it → Necessary"* (REPORT.md:39). The residual gap the report names is precisely that
   *"paths not shown (see F-2)"* — i.e. the fix is F-2, not a gate-tightening.
3. **The honest blocker is informedness, not quarantine.** Today `--yes` proceeds without printing
   the partial paths (§3, `[CODE-VERIFIED]`), so the operator's standing `--yes` is *uninformed*.
   Land F-2 (print the paths on the report-only path) and `--yes` becomes informed pre-consent —
   which is a reasonable reading of "assessed-and-accepted" for an unattended pipeline.
4. **Caveat / NO-leaning counter-evidence to record:** on the pure-CI path nobody reads the
   printed paths in real time, so "informed consent" is weaker than interactive. If the team
   weights non-idempotent-seam safety above CI-ergonomics, NO (add `--accept-partial`, default
   STOP-on-partial under `--yes`) is the conservative choice. The decision record below carries
   both so the operator rules explicitly.

---

## 3. F-2 — design-amendment surface (Option A vs §4(b) "always")

### 3a. design §2 field-exactness (the constraint that blocked the F-2 field)

`design.md:84-93` — the `BoundaryReport` dataclass definition (VERBATIM):

```python
@dataclass
class BoundaryReport:
    validated_last: bool
    suspects: list[BoundaryTask]
    quarantined: dict[Path, Path]               # canonical → quarantine copy
    passed: bool                                # gate verdict (FR-2.4) — deterministic only
    blocking_reasons: list[str]
    coherence_warnings: list[tuple[BoundaryTask, str]]  # advisory Haiku flags; NOT part of `passed` (NFR-3)
```

This is the §2 "field-exactness" surface the report cites (REPORT.md:45): `BoundaryReport` has
**six** fields, and **none** carries report-only partial-work *paths*. `quarantined` only holds
paths *after* a quarantine COPY ran; `suspects` holds `BoundaryTask` objects (task identity), not
file paths. The implementer declined to add a 7th field, *"citing design §2 field-exactness, which
Phase-1 QA verified"* (REPORT.md:45).

`[CODE-VERIFIED]` — `models.py:84-101` matches this dataclass exactly (six fields:
`validated_last`, `suspects`, `quarantined`, `passed`, `blocking_reasons`, `coherence_warnings`).
No partial-paths field exists.

### 3b. design §4(b) — "report suspect paths in BoundaryReport (always)"

`design.md:172-180` (VERBATIM):

```
  if partial:
      report suspect paths in BoundaryReport (always)                     # FR-2.2 surface
      if cleanup_opted_in:                                                # default: report-only
          acquire .recovery-locks/phase-{phase}.lock                      # recovery.py:275
          qdir = results_dir/(".resume-quarantine-" + ts)
          copy suspect paths → qdir preserving structure; write qdir/manifest.json
                                                                          # same shape as rerun_tasks.py:961
          append recovery-audit.log {event:"resume_quarantine", task, manifest: qdir/manifest.json}
          quarantined[canonical] = qdir-copy                              # reversible via restore_from_bundle
```

The load-bearing line is `design.md:173`: *"**report suspect paths in BoundaryReport (always)**
# FR-2.2 surface"*. The word **"always"** is unconditional — it precedes the `if cleanup_opted_in`
branch, so §4(b) requires the **paths** to be in the `BoundaryReport` on **every** path including
report-only (default). The quarantine block at `:175-180` is the *opt-in* extra. So §4(b)
separates two surfaces: (1) **always** report the paths in the report; (2) **optionally** copy them
to quarantine.

`[CODE-CONTRADICTED]` — the implementation conflates the two. `integrity.py:63-67`: paths are
detected (`_detect_partial` → `partial_paths`), but the only "always" surface is
`_surface_partial` (`integrity.py:65,198-208`), which appends a **`BoundaryTask`** (task identity)
to `report.suspects` — NOT the paths. The paths reach `report.quarantined` ONLY inside the
`if cleanup_opted_in` branch (`integrity.py:66-67` → `_quarantine`). On the default report-only
path, `partial_paths` is **discarded** after detection — never stored on the report, never printed
(`_print_resume_decision` prints `quarantined` only — `commands.py:533-534`). **§4(b)'s "always"
is not honored.**

### 3c. Is F-2 Option A (add a `BoundaryReport` partial-paths field) MORE faithful to §4(b)?

**Yes — decisively.** §4(b):173 literally says *"report suspect paths **in BoundaryReport**
(always)"*. The current implementation reports the suspect **task** in `BoundaryReport.suspects`
and the **paths** only in `BoundaryReport.quarantined` (opt-in). Adding a dedicated report-only
field — e.g. `partial_paths: list[Path]` populated unconditionally whenever `partial_paths` is
non-empty — is the **literal** realization of "suspect paths in BoundaryReport (always)." It is
strictly more faithful to §4(b) than the status quo, which under-delivers the "(always)" clause
(this is exactly the F-2 "Drift" adjudication, REPORT.md:41-45).

The report's alternative (print the `_detect_partial()` paths in `_print_resume_decision()` —
REPORT.md:110-112) satisfies the *operator-visibility* intent of §4(b) without a new field, but it
does NOT satisfy the literal *"in BoundaryReport"* clause — the paths would live only in the print
side-effect, not in the data structure. **Option A (the field) is the §4(b)-faithful choice;
print-only is a weaker compromise that preserves §2 field-exactness at the cost of the §4(b)
"in BoundaryReport" wording.**

### 3d. Minimal §2 amendment text to authorize the new field

To keep §2 field-exactness intact while allowing Option A, amend the `design.md:84-93`
`BoundaryReport` dataclass to add ONE field:

```python
    partial_paths: list[Path] = field(default_factory=list)  # report-only suspect paths (FR-2.2 / §4(b) "always"); populated regardless of cleanup_opted_in
```

and add a one-line note to §4(b):173 making the field the named home of the "always" surface:
*"report suspect paths in `BoundaryReport.partial_paths` (always, regardless of
`cleanup_opted_in`); `quarantined` additionally holds the copy mapping when cleanup is opted-in."*
This is the smallest amendment that reconciles §2 (exact field list) with §4(b) ("in
BoundaryReport, always") — it adds exactly one field with a documented, backward-compatible default.

---

## 4. F-4 — spec basis (merged-req :141-143 vs design §4(a))

### 4a. merged-requirements.md:141-143 — AC-3 prior-tail double-validation (VERBATIM)

`merged-requirements.md:141-143` (VERBATIM):

```
- AC-3 Hard crash mid-phase 3 (no `phase-3-result.json`): auto-resume assesses/cleans
  half-finished phase-3 artifacts, then re-runs phase 3; last completed task (phase 2 tail)
  is double-validated first.
```

The load-bearing clause: *"last completed task (**phase 2 tail**) is **double-validated first**."*
On a hard crash mid-**phase 3** with no `phase-3-result.json`, the last *completed* task lives in
**phase 2** (the prior phase). AC-3 requires that phase-2 tail to be double-validated **before**
re-running phase 3. (FR-2.3, `merged-requirements.md:83-84`, corroborates: *"Crash with no per-task
data. Phase re-run is permitted, but FR-2.2-style half-finished-work assessment/cleanup still runs
first for the whole boundary phase."* — and FR-2.4(b) requires last-completed double-validation
unconditionally.)

`[UNVERIFIED]` (spec text). The implementation-side contradiction is tagged in §4c.

### 4b. design §4(a) — interrupted-phase-scoped validation (VERBATIM)

`design.md:148-154` (VERBATIM):

```
  # (a) doubly-validate last completed task (DD-2, FR-2.1)
  lc = plan.boundary_tasks.role==last_completed
  signalA = lc.persisted_status
  signalB = _classify_transcript(read(task_output_file(phase, lc.id)))   # rerun_tasks.py:550
  artifacts_ok = all declared checkpoint/deliverable paths for lc exist  # checkpoints.py + executor.py:1844 logic
  validated_last = (signalA==PASS and signalB==PASS and artifacts_ok)
  if not validated_last: suspects += [lc]   # over-claim caught (R1)
```

Design §4(a) scopes `lc` (last_completed) to `plan.boundary_tasks` — and per the planner
(`design.md:122-132`, §3 step 2), `boundary_tasks` is built **only for `interrupted_phase`**. The
DD-2 definition reinforces this: *"Vacuously True when there is no last-completed task (PHASE
granularity / hard crash)"* (`design.md:24` DD-2 prose + `integrity.py:94-95` docstring). So §4(a)
validates the last-completed task *within the interrupted phase only*; on a true hard crash with
no per-task transcripts, `boundary_tasks` is empty, there is no `last_completed`, and validation is
**vacuously True** — it never reaches back into phase 2.

### 4c. How the implementation followed §4(a) but under-delivers :141-143

`[CODE-VERIFIED]` (followed §4(a)): `planner.py:158-169` — on the hard-crash/PHASE branch,
`boundary` is populated only from `discover_failed_tasks_from_transcripts(results_dir, interrupted)`
(the *interrupted* phase). A true hard crash with no transcripts ⇒ `derived == []` ⇒
`granularity = PHASE`, `boundary == []`, `rerun_task_ids == []`. Then `integrity.py:97-101`
(`_validate_last_completed`): `lc = next((bt ... role=="last_completed"), None)` ⇒ `lc is None` ⇒
`return True, [], None` — **vacuously validated.** The prior phase (phase 2) is never read.

`[CODE-CONTRADICTED]` (vs :141-143): merged-req AC-3 requires the **phase-2 tail** (prior
completed phase's last task) to be double-validated first on the phase-3 hard crash. The
implementation only ever considers the *interrupted* phase's boundary; because that phase has no
per-task data on hard crash, the requirement's "phase 2 tail" double-validation **never runs**.

**Precise statement:** The implementation is **faithful to design §4(a)** (interrupted-phase-scoped
last-completed validation) but **under-delivers merged-requirements.md:141-143** (which demands the
*prior completed phase's* tail be double-validated when the interrupted phase yields no
last-completed). This is the F-4 adjudication (REPORT.md:53-57): *"Faithful to §4(a),
under-delivers merged-req :141-143 + item 5.3's phrasing. Narrow but real."* The root cause is a
spec-internal scope mismatch: §4(a) scoped validation to the interrupted phase; AC-3 :141-143
scoped it to "last completed task" globally (which on a phase-boundary hard crash is in the prior
phase). **§4(a) silently narrowed AC-3's intent** — a second, smaller CG-4-class spec gap.

**Fix surface (spec side):** amend design §4(a) so that when `granularity==PHASE` (no
last-completed in the interrupted phase), the gate reaches into the **highest completed phase** and
double-validates ITS tail task before permitting the phase re-run — explicitly realizing AC-3's
"phase 2 tail" clause. (Code-side fix is researchers 01–04's scope; this records the spec basis.)

---

## 5. Decision Record skeleton (for the task to fill)

A ready-to-fill decision record. The task owner fills `RULING` after the operator decides; the
"spec edits" and "downstream effect" columns are pre-derived from §§1–4 above.

```
### DECISION RECORD — CG-4 (sprint auto-resume partial-work gate)

QUESTION:
  Does bare `sprint run --yes` proceeding past REPORTED-but-not-quarantined partial work
  satisfy FR-2.4(a) "boundary half-finished work cleaned OR explicitly assessed-and-accepted"?

AUTHORITY IN CONFLICT:
  - design §7 (design.md:293)         → passed=True, quarantine opt-in        [implemented]
  - design §4(c) (design.md:186)      → passed needs (partial quarantined OR accepted)
  - FR-2.4 (merged-requirements.md:85-87) → MUST NOT proceed until cleaned OR assessed-and-accepted
  Both §7 and §4(c) cite FR-2.4 as their authority → genuine self-contradiction.

OPTIONS:
  [ ] YES — §7 governs. F-1 = as-designed (Necessary deviation, REPORT.md:35).
            HARD PREREQUISITE: land F-2 path-surfacing so `--yes` consent is informed.
      Spec edits:
        - design.md:186 — drop/re-word the `(partial work quarantined or accepted)` conjunct
          to `(partial reported AND (quarantined OR --yes/assented))`.
        - merged-requirements.md:85-87 — clarify that on the non-interactive path,
          "`--yes` + printed partial-paths report" == "explicitly assessed-and-accepted".
        - design.md:293 (§7) — unchanged.
        - integrity.py:314 _verdict — unchanged (already §7).
      Downstream:
        - F-1 → closed as-designed (no gate change).
        - F-2 → MANDATORY (the informedness fix; promote to blocking for this option).

  [ ] NO — §4(c)/FR-2.4 govern. F-1 = real safety gap; tighten the gate.
            On `--yes`/CI with partial work: auto-quarantine OR hard-STOP until `--accept-partial`.
      Spec edits:
        - design.md:293 (§7) — replace unconditional `passed=True` with
          `passed=True only if (partial quarantined OR --accept-partial)`.
        - design.md:186 (§4(c)) — unchanged (already correct).
        - merged-requirements.md:85-87 (FR-2.4) — unchanged (already correct).
        - integrity.py:314 _verdict — ADD third conjunct (partial quarantined-or-accepted);
          add `--accept-partial` flag (code = researchers 01–04 scope).
      Downstream:
        - F-1 → fixed via gate tightening.
        - F-2 → still wanted (visibility), but no longer the sole safety mechanism.

RECOMMENDED DEFAULT: YES + F-2-as-prerequisite (rationale §2; report leans Necessary not Regression).
RULING: __________ (operator)  DATE: __________  BY: __________

SECONDARY (F-4 sub-decision, smaller-scope, same family):
  design §4(a) (design.md:148-154) narrowed AC-3 :141-143 ("phase 2 tail double-validated first").
  Ruling needed: on PHASE-granularity hard crash, MUST the gate reach into the prior completed
  phase and double-validate its tail? (Report adjudicates F-4 as Necessary deviation / coverage
  gap — REPORT.md:53-57; recommended: YES, amend §4(a) + add CG-3 test.)
```

---

## Summary

**CG-4 is a genuine, requirements-level self-contradiction, confirmed at the code level.**

- **The contradiction (§1):** design §7 (`design.md:293`) enacts `passed=True` with partial work
  merely *reported* (quarantine opt-in); design §4(c) (`design.md:186`) and FR-2.4
  (`merged-requirements.md:85-87`) require `passed` to include `(partial work quarantined OR
  accepted)`. **Both cite FR-2.4 as authority** — the spec disagrees with itself about FR-2.4's
  meaning on the `--yes`/CI path. The implementation (`integrity.py:314`
  `return accept_suspect or report.validated_last`) followed §7 and **omits** the §4(c) third
  conjunct → `[CODE-CONTRADICTED]` against §4(c):186, `[CODE-VERIFIED]` against §7:293.
- **The decision (§2):** binary — does `--yes` past *reported* partial work satisfy
  "assessed-and-accepted"? **Recommended ruling: YES, conditional on landing F-2** (the report
  adjudicates F-1 as *Necessary deviation + residual safety gap*, not a regression — REPORT.md:35-39;
  the residual gap is informedness, fixed by F-2, not by gate-tightening). NO (tighten gate, add
  `--accept-partial`) is the conservative alternative, carried in the decision record.
- **F-2 surface (§3):** §4(b) (`design.md:173`) says *"report suspect paths in BoundaryReport
  (**always**)"* — unconditional, before the opt-in quarantine branch. The implementation surfaces
  the suspect **task** (`integrity.py:65,198-208`) but the **paths** only inside the opt-in
  quarantine branch (`integrity.py:66-67`); on report-only they are discarded and never printed
  (`commands.py:533-534` prints `quarantined` only) → `[CODE-CONTRADICTED]` against §4(b)'s
  "(always)". **Option A (add `BoundaryReport.partial_paths`) is decisively MORE faithful to §4(b)**
  than print-only; minimal §2 amendment = one new field with a `field(default_factory=list)` default.
- **F-4 spec basis (§4):** merged-req `:141-143` (AC-3) requires the **phase-2 tail** (prior
  completed phase) to be double-validated first on a phase-3 hard crash. design §4(a)
  (`design.md:148-154`) scoped last-completed validation to the **interrupted phase only**; on a
  no-per-task hard crash `boundary_tasks==[]` ⇒ validation is vacuously True (`planner.py:158-169` +
  `integrity.py:97-101`, both `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]`). **The implementation is
  faithful to §4(a) but under-delivers :141-143** — §4(a) silently narrowed AC-3's "last completed
  task" to the interrupted phase. A second, smaller CG-4-class spec gap.
- **Decision-record skeleton (§5):** drop-in, with both options' exact spec-edit line targets
  (§7:293, §4(c):186, FR-2.4:85-87) and the downstream F-1/F-2 effects pre-derived; includes the
  F-4 §4(a)/AC-3 secondary sub-decision.

**Net:** two spec-level gaps in the same family — (1) §7 vs §4(c)/FR-2.4 on partial-work gating
(CG-4, needs the operator ruling), and (2) §4(a) vs AC-3:141-143 on prior-phase-tail validation
(F-4 basis). Both are "spec narrowed a broader requirement, implementation faithfully followed the
narrower spec." Code-side fixes belong to researchers 01–04; this file supplies the verbatim spec
quotes, the binary decision framing, the recommended ruling, and the fill-in decision record.
