# Plan: narrow "contradiction" in the blocking rule to contradictions with real downstream consequence

Status: PLAN ONLY. No product file has been edited. Written 2026-11-14 after the owner's instruction: a contradiction in documentation, comments or other text with no downstream consequence must not be blocking; the reading must be narrowed to contradictions with real downstream consequence and a high probability of reaching the final deliverables. Goal behind it: more issues become follow-up notes so reviews finish faster (the owner's target: 35% less average severity).

Why a written plan and not a direct edit: the rule is copied into 11 pinned files (CLAUDE.md hard limit: more than 5 edits needs a written plan). The formal route (`/sc:workflow`) writes under `.dev/tasks/`, which this worker's standing constraint forbids, so the plan is here instead.

## 1. Baseline (699 valid-era reviewer reports, `20261111-a1`)

| Measure | Value |
|---|---|
| Findings | 2,753 (3.9 per report) |
| Blocking findings | 702 (25.5% of findings, 1.0 per report) |
| Blocking by category | unpassable-check 360 (51%), contradiction 307 (44%), other 16, safety 16, data-loss 3 |
| 35% target | remove about 246 blocking findings |

The contradiction clause is 44% of blocking findings. Demoting 246 of them would need about 80% of contradiction-blocking findings to fall under the new, narrower reading. That is likely more than the narrowing alone removes, so the plan measures first (section 5) and names a second lever (section 6) instead of promising 35%.

## 2. The change (exact wording)

Current grading check (`document_review_loop_prompts.md:31`, restated in `spec-panel.md:259` and, as the S-bullets, in `pragmatic.md:226-231`): blocking needs "two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass".

New wording for the contradiction clause only:

> "two stated texts that contradict each other and the contradiction would, with high probability, change what ships: it decides the behavior, output, test, interface or reader-facing instruction of a final deliverable. A contradiction confined to text that no deliverable reads or acts on (code comments, rationale or background prose, superseded or historical sections, examples, labels, internal notes) is Medium even when the two texts clearly disagree. To mark a contradiction blocking, name the deliverable it changes and say in one sentence why a reader or implementer would act on the wrong text. If you cannot name it, grade it Medium."

Unchanged: the data-loss, security and safety clause (a reviewer never suppresses it), the unpassable-acceptance-criterion clause, and the rule that Medium goes under follow-up candidates and never fails a review or triggers a fix.

Companion edit in `pragmatic.md`: "Blocking is a real defect: wrong behaviour, a false claim, ..." becomes "... a false claim that a reader or implementer of a deliverable would act on, ...". Without it the old bullet would still make any false claim blocking.

Not changed: documentation as a deliverable. When the deliverable is itself documentation (a user guide, a reference page), a contradiction in it is blocking because readers act on it. That keeps B6, B7 and B8 of the study packages blocking; it only removes contradictions in text that is not a deliverable.

## 3. Files to edit (all under `src/superclaude/`, then `make sync-dev`; nothing under `.claude/` is staged)

| # | File | Edit |
|---|---|---|
| 1 | `rules/prompts/document_review_loop_prompts.md` | grading check, line 31 |
| 2 | `commands/spec-panel.md` | grading line 259 |
| 3 | `output-styles/pragmatic.md` | blocking bullet and the spec-panel scale bullet (lines 226, 231) |
| 4-11 | the 8 other tracked copies of the S-bullet text: `rules/prompts/{documentation_expert,automated_qa_workflow,doc_code_analyst,recruiting_expert}_qa_prompt.md`, `agents/{rf-qa,rf-qa-qualitative}.md`, `templates/workflow/{01,02}_mdtm_template_*.md`, `templates/documents/{agent_template_qa,skill_template}.md` | companion edit to the "a false claim" wording, driven by the existing edit tables |
| 12 | `tests/skills/fixtures/review_severity_{cap,sweep}_edits.yaml` and the pins in `tests/skills/test_review_severity_rule.py`, `test_review_severity_mapping.py`, `test_review_prompt_overrides.py` | update the byte-copied tables and pinned strings to the new wording; add one test that the "name the deliverable" sentence exists in the brief |
| 13 | `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh` (line 17) and each collaboration design's pinned brief copy | eval harness only; do NOT change mid-experiment (section 7) |

The parser (`cli/review/findings.py`) needs no change: severity and the blocking flag are what the reviewer writes. No new category or field.

## 4. Safety checks

- Security, data-loss and safety findings stay blocking under the old rule, verbatim.
- A reviewer that cannot name the affected deliverable grades Medium; the finding is still reported under follow-up candidates, so nothing is dropped.
- Wrong direction to watch: reviewers may over-use "no deliverable" to demote real defects. The measurement below checks this against the ground truth.

## 5. Measure before editing (cheap, no reviewer reruns)

1. Take the 307 contradiction-blocking findings from the 699 reports (anchor, claim, candidate text).
2. One blind Opus judge pass classifies each with the new wording: blocking (names a deliverable and a high-probability change) or Medium. Also run it on the ground-truth contradiction items (B4, B6, B7, B8, I-class contradictions) as a control: those must stay blocking.
3. Report: how many of the 307 demote, the new blocking share, and which ground-truth items change. Predicted: demotes a minority of the 307, so the blocking share falls from 25.5% by well under 35%.

## 6. If the narrowing alone is not enough for 35%

The unpassable-check clause is 51% of blocking findings. The same test can apply there: an acceptance criterion that cannot pass is blocking only when the criterion gates a deliverable that ships. That is a second, separate owner decision; this plan does not include it.

## 7. Sequencing with the running experiment

The five collaboration designs and the judge pin the brief's grading text by sha256. Changing it now invalidates every run on the current brief. Options: finish the counted collaboration runs first, then apply this change and treat it as its own arm (the isolated panel with the new brief against the isolated panel with the old brief on the same hold-out), which is also the only clean way to measure the effect on review time.

## 8. Verification once approved

`uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_review_prompt_overrides.py tests/review -q`, `make verify-sync`, `grep` that no tracked file still carries the old wording, then an isolated-panel run with the new brief on the three study packages to compare blocking share and elapsed time against the baseline in section 1.
