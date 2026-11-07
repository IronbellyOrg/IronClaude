1524eedc4cb5189cdcb3aba419460759f4142577
family simulated-rows-cite-no-test
defect form: a row marked simulated whose Evidence cell cites no test of tests/hooks/test_launch_job_identity.py with a line
command: grep -nE '\| simulated' .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/b-ctx-verdict.md
before-output:
18:| Background Bash to Git | simulated | E:10 (old governed background jobs refused in real-Git fixtures, sub
20:| Same-worktree human terminal | simulated | E:10 (concurrent same-clone human pushes to main and master se
22:| Detached or reparented job | simulated, with a stated limit | E:12 (deliberate setsid escape was unselect
24:| Process exit and PID reuse | simulated | D:563 (controlled subprocess tests exercise stale process data);
25:| Resume in a new process | simulated | E:10 (two new jobs for the same logical id were both recognized, "l
27:| Release while a job is alive | simulated | E:10 (after explicit release the old jobs reported ordinary/re
coupled sites: the count sentence 'Observed: 2 of 13 rows. Simulated: 6. Unobserved: 5.' (unchanged by the fix); the Evidence line T = tests/hooks/test_launch_job_identity.py at the head of the file
after:
  18:| Background Bash to Git | simulated | E:10 (old governed background jobs refused in real-Git fixtures, subprocess te
  20:| Same-worktree human terminal | simulated | E:10 (concurrent same-clone human pushes to main and master selected ord
  22:| Detached or reparented job | simulated, with a stated limit | E:12 (deliberate setsid escape was unselected and adv
  24:| Process exit and PID reuse | simulated | D:563 (controlled subprocess tests exercise stale process data); tests T:3
  25:| Resume in a new process | simulated | E:10 (two new jobs for the same logical id were both recognized, "labelled co
  27:| Release while a job is alive | simulated | E:10 (after explicit release the old jobs reported ordinary/released and
