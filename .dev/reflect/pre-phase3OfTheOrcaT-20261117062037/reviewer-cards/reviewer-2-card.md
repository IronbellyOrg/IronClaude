persona: qa
model_class: haiku
verdict: FAIL
confidence: 0.97

findings:
- F1 | task 6 | BLOCKING | Regression | plan line 103
  plan_says: the snapshot JSON contains neither the ask string nor any dispatch id of a question
  reality: export.py:26 has dispatchId in _TEXT_FIELDS and line 195 exports all worker rows; a linked question necessarily shares its dispatch id with one of those rows; Task 6 also forbids changing snapshot_dict and requires preserving the snapshot.
  wrong_outcome: a realistic linked fixture cannot pass this check; the executor removes worker identifiers (weakening the snapshot contract) or leaves the matching worker out of the test.
  fix: restrict the dispatch-id exclusion to the snapshot's `questions` group; keep the whole-snapshot exclusion for the ask string; require a fixture with the matching worker and preserve rows[].dispatchId; keep link-on/link-off byte equality.
- F2 | task 3 | BLOCKING | Gap | plan line 62
  plan_says: pass `link=` to Collector at the call at line 355
  reality: commands.py:218 constructs another Collector in run_once without the argument; lines 224-230 choose between a width-bound screen and record_text. The plan's command-level check verifies the constant's source text; its collector checks supply link=True themselves.
  wrong_outcome: --once uses the default link=False; width-bound one-shot screens keep the generic subject and records omit dispatch and link information, while the specified tests pass.
  fix: pass link=_link_on(options) at both sites; add command-level tests with a distinctive synthetic payload: the width-bound screen shows sanitized question text, the record has dispatch and link information but not that text, closing the gate restores existing behaviour.
- F3 | task 4 | BLOCKING | Regression | plan line 75; view.py:914
  plan_says: update QUESTIONS_KEYS_LINE to list n/p question; constraint line 24: link off behaves exactly as before
  reality: view.py:914 selects QUESTIONS_KEYS_LINE whenever a question panel exists, independent of the link switch.
  wrong_outcome: with questions on and link off the footer changes, advertises unavailable keys, and its length can alter wrapping and the height budget.
  fix: keep the existing line and select a separate link-enabled line only when linking is on; add a byte-for-byte link-off screen comparison with questions enabled at all three widths (the R1 surface alone does not exercise this).
- F4 | task 4 | MEDIUM | Gap | plan line 78
  plan_says: a linked question gives session_fields with exactly the nine labels and the worktree note
  reality: no missing-value assertions for the desk and none for its stale or as-of note, though line 23 requires unknown never to become zero, false or blank and Task 4 line 75 requires a STALE or as-of note.
  wrong_outcome: the checks pass with a desk that shows a missing worktree as blank or shows retained worker evidence without its freshness qualification.
  fix: add a selected linked-question test with missing worker fields and resource.worktreeId asserting exact unknown wording, and failed or stale worker-read cases asserting the freshness qualification.

uncovered_requirements:
- INF-001: partially (no check proves payload text reaches the one-shot screen through command wiring; F2).
- INF-007: partially (link-off question-screen behaviour unchanged is not checked; F3).
- INF-008: partially (command-level link-gate propagation not checked; F2).
- INF-010: the privacy check exists but the whole-snapshot dispatch-id exclusion makes its criterion contradictory for a linked worker (F1).
- INF-013: constraint only; no delivery check.

checked: read plan, source, coverage matrix, grounding evidence, the five spec files and release gates, and the command, collector, parser, retention, view, renderer, export and test code. INF-002 has explicit malformed and missing payload checks in Task 2; INF-003 to INF-006 have join, unlinked, worktree-evidence and shared-worktree checks in Task 4 (plus F4). INF-009 is not untested: fake runners reject non-allow-listed argv, adapter tests pin forbidden verbs, key tests prevent adapter or collector access, Task 7 requires the full suite; a link-enabled argv assertion would strengthen it. INF-011 covered by Tasks 1 and 7; INF-012 by tasks 2 to 6. Named test files and functions exist; the new question_message builder is created before its dependents; declared dependencies have no ordering defect. No commands run.
