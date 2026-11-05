# Diagnosability tasklist (informational; verdict partial, trivial)
discriminator-required: no
## Emitter search
emitters-found: 2 (finish-merge.sh:232, :249) ; already-read-files: 1 ; usable-capture-routes: 1 (hermetic pytest run under tests/pr_submit/, same-shell)
## Pending rows
- P-1: regression test: conflict-marker-size=9 via .gitattributes, resolved file staged with markers left -> expect FINISH_FAIL markers (currently exit 0). Site: tests/pr_submit/test_conflict_scripts.py (invocation site, not product source).
- P-2: regression test: unrelated tracked script staged 100755 -> 100644 during the merge -> expect FINISH_FAIL staged_unexpected (currently exit 0). Site: tests/pr_submit/test_conflict_scripts.py.
