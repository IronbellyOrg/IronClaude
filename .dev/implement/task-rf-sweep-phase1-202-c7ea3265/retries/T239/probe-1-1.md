b837c1e3edfed97a2e605ca0cdc26f9b42a006ab
Family: phase10-findings-claims (covers F1.1 and F1.2 of review r1-1)
- Defect form: a claim in the two `### Phase 10 Findings` bullets of the plan file is not true or not proven on disk: (F1.1) the second bullet names `test-readonly.txt` and `test-cli-registration.txt` as result maps that still show pre-fix counts, but the stale files are `phase10-validation.md` (559) and `test-cli-registration.txt` (469); (F1.2) the first bullet says no code fix was made in Phase 10 without saying that the file times of three source modules moved because implementer agents mutated them in place and restored them.
- Probe command: grep -n -o -e "still show pre-fix counts" -e "no code fix was made in Phase 10" -e "No Phase 10 test item exposed a bug" .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
- Before-output: three hits on the two Phase 10 Findings bullets (lines 2984 and 2985).
- Coupled sites: the second bullet's disclosures sentence, which gets the in-place mutation disclosure too.
- after: (grep -n -o -e 'still show pre-fix counts' -e 'no code fix was made in Phase 10' -e 'No Phase 10 test item exposed a bug' on the plan file)
  - 2984:No Phase 10 test item exposed a bug
  - 2984:no code fix was made in Phase 10
  - 2985:still show pre-fix counts
