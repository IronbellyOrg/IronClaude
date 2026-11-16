# Inferred requirements (Pass 2) for source.md

Pass 1 found zero labeled ids (no R-n, REQ-n, SPEC-n or T-n token in `source.md`); `parsed_count = 0`, `inferred_count = 22`. Every quote below was verified as a substring of the cited line by `artifacts/inferred_rows.py` (22 of 22 quotes match). Matching items: the Constraints section and the eight task sections of the plan; containment threshold 0.6.

| INF id | Citation | Verbatim quote (shortened here; full quote in `inferred_rows.py`) | Best item | Ratio | Match |
|---|---|---|---|---|---|
| INF-001 | source.md:11 | the sweep only records (`promote` off), the classifier has no authority | Constraints | 1.000 | containment |
| INF-002 | source.md:12 | the two `rf-qa.md` cap sites are not touched here (stage 3) | Constraints | 0.857 | containment |
| INF-003 | source.md:13 | Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus ... and the limits. | Task 7 | 1.000 | containment |
| INF-004 | source.md:14 | Write `./artifacts/shadow_summary.py` ... prints the stage 2 exit numbers the spec defines | Task 8 | 1.000 | containment |
| INF-005 | source.md:14 | Then write `./artifacts/stage2-summary-for-owner.md` ... not by this file. | Task 8 | 1.000 | containment |
| INF-006 | source.md:15 | Acceptance lines inside this package that a later task of the same package makes false get an end point. | Constraints | 0.818 | containment |
| INF-007 | source.md:19 | No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking. | Constraints | 1.000 | containment |
| INF-008 | source.md:19 | Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account. | Constraints | 0.714 | containment |
| INF-009 | source.md:27 | Every task that edited `src/superclaude/skills/task/SKILL.md` is dropped ... | Constraints | 0.429 | none (matcher limit; by hand: covered by the "Retired carriers are not edited" Constraint) |
| INF-010 | source.md:28 | Record and print only: one read-only call, no `--promote`, no `--write`, no question. | Task 3 | 0.875 | containment |
| INF-011 | source.md:29 | tech-research keeps its ledger-writing edit (Task 4); no sweep, no offer ... | Constraints | 0.688 | containment |
| INF-012 | source.md:30 | No new plugin surface. | Constraints | 1.000 | containment |
| INF-013 | source.md:31 | `follow-ups.md` stays a separate file; no mapping to `review-ledger/1`; `ledger.py` is not edited. | Constraints | 0.875 | containment |
| INF-014 | source.md:69 | Task 8's `--confirmed-misses` file now holds `<run_id>:<row id>` entries ... | Task 8 | 1.000 | containment |
| INF-015 | source.md:70 | Task 7 now runs the supplier first ... (Step C). | Task 7 | 0.871 | containment |
| INF-016 | source.md:71 | `follow-ups safety` now prints a last line `worker_status_signal: partial` ... | Task 5 | 0.781 | containment |
| INF-017 | source.md:72 | Task 4 now edits four active templates ... the two legacy templates are not edited. | Task 4 | 0.867 | containment |
| INF-018 | source.md:76 | Task 2 `safety` saves the tag through the stage 1 writer ... after a second `write`. | Task 2 | 0.941 | containment |
| INF-019 | source.md:78 | Task 3 prints "No follow-up ledger was written in this run." for 0 ... | Task 3 | 1.000 | containment |
| INF-020 | source.md:87 | The file needs a `reviewed: <date> by <name>` line; without it ... "not computable". | Constraints | 1.000 | containment |
| INF-021 | source.md:88 | New Constraints bullet; Task 7 adds `classifier_eval.py` and its test; ... | Constraints | 0.750 | containment |
| INF-022 | source.md:89 | `incomplete` is sticky in a ledger; tested in Task 2. | Task 2 | 0.500 | none (matcher limit; by hand: covered by Task 2's `incomplete` test line) |

Note on supersession: source.md lines 11 and 12 are the original request text; Revision 2 (source.md:27-29) replaces the task-skill carrier and the halt-offer sentences. The plan follows the revisions. A reviewer must not report the original lines 11 and 12 as unmet.
