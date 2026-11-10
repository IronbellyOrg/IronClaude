7987ab62e0024258b9bd4ad4197ddcc89dbbee48
## family doc-claim-vs-code (F1.1)
defect form: the note states which ids the script logs as DOWNGRADE more widely than fix_audit.py:653 does
command: grep -n -F -e 'DOWNGRADE' -- docs/designs/spec-panel-ponytail.md
before:
30:- A finding review 2 graded blocking, or protected (CRITICAL, FR-8, FR-9), is never closed by the audit. A validated-minor grade on such an id is logged `DOWNGRADE <id>` only.
39:Owner decision: findings that the script defers (reverted, listed in `closed-minor.txt`) or demotes (logged `DOWNGRADE`) stay open in the success measure. `final-verdict.md` prints `held open (deferred or demoted): ...`, `review-3 new critical+major: <n>` and `review-3 critical+major (owner count, held findings included): <n>`, which adds every held id that review 2 labelled CRITICAL or MAJOR. 
coupled sites: docs/designs/spec-panel-ponytail.md:39 (owner count: held = deferred plus DOWNGRADE ids); source.md 2.6 last bullet
after (doc-claim-vs-code):
after: 30:- A finding review 2 graded blocking, or protected (CRITICAL, FR-8, FR-9), is never closed by the audit. A validated-minor grade on an id review 2 graded blocking is logged `DOWNGRADE <id>` only; a protected id that review 2 did not grade blocking gets no `DOWNGRADE` line.
after: 39:Owner decision: findings that the script defers (reverted, listed in `closed-minor.txt`) or demotes (logged `DOWNGRADE`) stay open in the success measure. `final-verdict.md` prints `held open (deferred or demoted): ...`, `review-3 new critical+major: <n>` and `review-3 critical+major (owner count, held findings included): <n>`, which adds every held id that review 2 labelled CRITICAL or MAJOR. 
