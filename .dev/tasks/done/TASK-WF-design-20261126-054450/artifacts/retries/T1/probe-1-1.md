31479e9baae6ae144456c44073a32251dd59d153
family: unrun-ac-command
defect form: an AC that asks for a test-run result has no evidence artifact in the review package
command: grep -n -E "passed|failed|error" .dev/tasks/to-do/TASK-WF-design-20261126-054450/artifacts/t1-test.log
before: 8:============================= 169 passed in 5.39s ==============================;
coupled sites: Task 8, 9, 10, 20 acceptance commands name pytest runs; each needs a ./artifacts/t<n>-test.log written before its review
after: 5:============================= 169 passed in 5.39s ==============================
