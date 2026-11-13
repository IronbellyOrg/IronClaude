# Tier 1 reflection card — pre-TASK-WF-implementTheDesi-20261031-182028-shadow11 (UC-1)

mode: pre | spec: source.md (delegates to design doc) | tasklist: 15 tasks, 5 phases
rubric_inputs: S_scope=15 (tasklist items) | S_domains=4 (core code, tests, skill/refs markdown, user docs) | S_dev_density_union=0.20 (4/20)

## Coverage verdict

Parsed coverage 1.00 (12/12 design sections the task vocabulary names are mapped).
Union coverage 0.80: four requirement rows from design section 18 (coordinator-approved
amendments A0-A6, dated 2026-10-31, which "override any earlier text they contradict") are
not satisfied by the plan as written.

## Findings (Tier 1)

T1-F1 [MAJOR, contradiction] Task 7 pins superseded completion semantics.
Task 7 body says `codex_review_state` has "completion time = `updated_at`" and its AC makes
"two summary comments" classify `polling`. Amendment A1 (design s18) redefines completion as
the LATER of the marker `updated_at` and the newest completing review's `submitted_at`;
amendment A3 makes multiple valid markers resolve to the latest `updated_at` (only same-time
ties poll). An executor following Task 7 verbatim implements both rules wrong and writes
tests asserting the wrong behavior.
citations: plan:91,95 -> spec(design):439-443,452-454

T1-F2 [MAJOR, contradiction] Task 2's second AC asserts A0 reversed.
Plan AC: "A local override YAML without Codex fields still loads (Codex identities empty, so
Codex is disabled for that override)". A0: absent keys FALL BACK to shipped values; only an
explicit empty/null disables. The executor would write a test pinning the wrong semantics.
Ground truth: progress.md records the coordinator overturning exactly this mid-run ("T2:
Ruling: accept T2 F1.1 ... yes-fallback"), and shipped detection.py:157-158 implements A0 —
evidence the contradiction was live, not theoretical.
citations: plan:44 -> spec(design):434-437, progress.md T2 Ruling

T1-F3 [MAJOR, missing requirement] Amendment A6 (root-selection later-of rule) is in no task.
A6 overrides design s7's "created no later than completion" wording after a live PR 337
incident (root stamped 1s after review submission polled to terminal_timeout, 622 s). Task 7
passes "the marker time" to `_thread_findings` — the pre-A6 rule. No task, AC or test item
carries A6. (Shipped classifier.py:321 implements A6; again corrected outside the plan.)
citations: spec(design):467-479 -> plan:91 (absent)

T1-F4 [MINOR, partial] A2's augment-absent-continue rule lacks an AC.
When Augment alone hits TERMINAL_AUGMENT_NO_RESPONSE with Codex present, the run must record
reviewer_absent{augment} and CONTINUE with Codex. Task 12 says only "Wave 1 records
reviewer_absent / reviewer_incomplete"; no AC pins the continue rule or A2's absent-set
input to the wait outcomes (Task 8 signature has no absent-set parameter).
citations: spec(design):445-449 -> plan:102,147

T1-F5 [MINOR, weak AC] Task 15's grep AC cannot enforce its rule.
"`grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` returns no pr-submit
sentence that omits Codex" — grep returns the matching lines; deciding none is a pr-submit
sentence that omits Codex is judgment, not the grep's exit state. Recurring repo pattern:
grep-count ACs do not gate exact rule text (deviation-patterns, shadow04/shadow06).
citations: plan:182

T1-F6 [MINOR, partial] A5 report/dedup specifics only partially in Task 12.
"flagged by: augment, codex" report line, fix_applied per member fix_key, and "S5 wait covers
only re-triggered reviewers" appear in the design amendment but not in Task 12's bullet list.
citations: spec(design):459-466 -> plan:147

## Best-practice grade

4/5. Phase structure, per-task ACs with named evidence paths, dependency graph, and the
constraint block are all strong. Deduction: ACs that assert superseded semantics (T1-F1/F2)
are worse than missing ACs because they pin wrong behavior as "done".

## Self-assessed confidence: 0.88

Strongest on contradictions (verbatim plan text vs verbatim amendment text, plus the
coordinator ruling as execution-time ground truth). Weakest on whether A2/A5 partials
mattered in practice (progress.md suggests the SKILL landed them, but no AC pinned it).
