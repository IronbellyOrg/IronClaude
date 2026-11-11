7987ab62e0024258b9bd4ad4197ddcc89dbbee48
## family doc-claim-vs-code (F3.1)
defect form: the note says what a K1 failure implies about the spec; K1 fails on the spec sha256 or on the baseline sha256 (fix_audit.py:586-589)
command: grep -n -F -e 'K1' -- docs/designs/spec-panel-ponytail.md
before:
7:One fix audit per review loop, at the end of fix cycle 2: after the reviser applies the cycle-2 fixes and before review 3. It runs as its own step, `/sc:spec-panel-ponytail @<spec> --fix-audit --re-review <review-2 report> --baseline <copy review 2 saw>`, in a fresh session that is neither the rev
27:- `fix_audit.py apply` is the step that edits the specification. The auditor brief allows the auditor to write only `fix-audit/audit.md`, and check K1 fails the audit if the spec's sha256 changed since `prepare`. Invoking `--fix-audit` is the consent for that one scripted edit; the pre-audit copy
32:  - `check` does not write the specification. On a failure it writes `check.log`, records `audit: skipped(check failed)` and exits 1. (A K1 failure means the spec had already changed before the check ran.)
coupled sites: docs/designs/spec-panel-ponytail.md:27 (K1 fails if the spec's sha256 changed; true but not exclusive, kept); fix_audit.py:586-589 (not edited by T9)
after (doc-claim-vs-code F3.1):
after: 7:One fix audit per review loop, at the end of fix cycle 2: after the reviser applies the cycle-2 fixes and before review 3. It runs as its own step, `/sc:spec-panel-ponytail @<spec> --fix-audit --re-review <review-2 report> --baseline <copy review 2 saw>`, in a fresh session that is neither the rev
after: 27:- `fix_audit.py apply` is the step that edits the specification. The auditor brief allows the auditor to write only `fix-audit/audit.md`, and check K1 fails the audit if the spec's sha256 changed since `prepare`. Invoking `--fix-audit` is the consent for that one scripted edit; the pre-audit copy
after: 32:  - `check` does not write the specification. On a failure it writes `check.log`, records `audit: skipped(check failed)` and exits 1. (K1 fails when the spec's or the baseline's sha256 changed since `prepare`; a K1 failure on the spec means the spec had already changed before the check ran.)
