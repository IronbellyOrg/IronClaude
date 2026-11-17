# Control test for the stage 0c regrade: written before the grader ran

Time written: 2026-11-16 (before the control grader was spawned). Requested by the owner in chat after the old-rule injection confound was raised.

Question: when a grader is given a rule text that is deliberately very different from today's rule (while the same SubagentStart injection puts today's rule in its context), do its grades follow the rule it is given? If they do, the near-identical old and new grades in `../stage0c-regrade.md` are not explained by the injection alone.

Method: one fresh general-purpose agent, same brief as the three graders, grades the first 160 rows (lines 7 to 166) of `in/table-1.md` (a copy of `blind-table-1.md`) under rule C only (`in/rule-C.txt`: blocking only for data loss, exposure, a safety boundary or an act outside the declared scope; everything else not blocking). Output: `out/control-1.jsonl`. Reference: the three graders' grades of the same rows under the old text (A) and the new text (B).

Criterion fixed in advance (a proposal of the executor, not a spec number):
- Sensitive: 50 percent or fewer of the 160 rows graded blocking under C (the graders called 97 percent blocking under A and B). The injection does not stop a grader following the text it is given.
- Inconclusive: 51 to 85 percent.
- Insensitive: more than 85 percent. Then the instrument cannot tell texts apart (injection or a ceiling effect) and a re-run with the same instrument would show the same.

Not tested here: whether the new text B itself produces the movement the spec expects; this control only tests the instrument.
