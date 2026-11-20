4bf8f84e56b01a644fcb81014084a87af9447026

# Family probe probe-1-1.md (failing review r1-1)

## family: first-stop-gate
defect form: a shared launch helper applies one fixed wait for the agent's first turn to end, so a subcommand whose plan text gives a longer or different wait (session d: up to 90 minutes; session e: the cycle wait) ends early with PENDING; and a self-test whose stub gives every log a Stop on any send, so the early end cannot be seen.
search command: grep -n -e 'wait_first_stop' -e 'launch_real' -e 'OB_INITIAL_WAIT_S' .dev/issues/442/scripts/session-gov.sh .dev/issues/442/scripts/session-gov-selftest.sh
before-output (touched files):
  session-gov.sh:96: wait_first_stop definition
  session-gov.sh:134: launch_real definition (no wait parameter)
  session-gov.sh:154: wait_first_stop "$label" "${OB_INITIAL_WAIT_S:-900}" || pending no-first-stop (applies to all four sessions)
  session-gov.sh:233, 269, 299, 348: launch_real calls for b, c, d, e
  session-gov-selftest.sh:123: OB_INITIAL_WAIT_S=2 in every run
coupled sites: session-gov.sh:299-305 (d's own 90-minute loop) and 349-362 (e's cycle loop) own the waits for d and e; session-gov-selftest.sh stub orca appends a Stop to every log on any send.
after: launch_real takes a fourth argument (seconds to wait for the first Stop, absent or 0 means do not wait); b and c pass OB_INITIAL_WAIT_S (default 900); d and e pass nothing. The stub gets STUB_STOP_ONLY=<label> to give a Stop only to that log, and new cases show d and e reaching their own waits (no `no-first-stop`) and c still stopping with `no-first-stop`.

## family: o10-target
defect form: a write whose target is chosen by scanning a log of everything the agent read (the first pull request URL found), with no check that the target is the disposable item.
search command: grep -n -e 'find_pr_url' -e 'fire_o10' -e 'gh_fork api' -e 'gh_fork pr' .dev/issues/442/scripts/session-gov.sh .dev/issues/442/scripts/session-gov-selftest.sh
before-output (touched files):
  session-gov.sh:313: find_pr_url (first match in the whole log)
  session-gov.sh:327-341: fire_o10 (reads the pull request head branch, then PUTs to it)
  session-gov.sh:329: gh_fork pr view (read)
  session-gov.sh:331: gh_fork api ... ?ref= (read)
  session-gov.sh:334: gh_fork api ... PUT (the write)
  session-gov.sh:352, 358: callers
  (no other gh_fork write in the touched files)
coupled sites: session-gov-selftest.sh e scenarios assume the PUT happens (the T4 test worktree must sit on the pull request's branch); the stub gh answers `pr view` with a fixed branch.
after: fire_o10 compares the pull request head branch with the T4 worktree's current branch (`git -C $WT4 rev-parse --abbrev-ref HEAD`) and writes only when they are equal; otherwise it records `e-o10 FAIL` and no PUT. The test worktree T4 is created on branch ob-442-t4-branch; the stub gh takes STUB_PR_BRANCH; a new case shows a different head branch giving no PUT.
