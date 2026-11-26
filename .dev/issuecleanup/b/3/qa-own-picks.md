# QA own picks (written before opening any "Closest overlap" section)

#788 (C7 worker start): 1) #819 W11, one retry of an unknown launch outcome via Orca operation id; shares the unknown-outcome / no-double-start rule (FR-21), about 1 of 3 done-when bullets. 2) #786 C5, Run lifecycle and rebind after restart (shares the restart bullet, needs a bound Run for worker-start). 3) #799 C18, reused worktree and one-live-agent check.

#789 (C8 body hash and re-read): 1) #791 C10, hourly status pass (its S02-F32 includes "issue re-read"; C8 third bullet is the re-read on each status pass; about 1 of 3 bullets plus the shared pass). 2) #775, comment or edit after approval voids approval (shares body-changed detection, unchanged_since). 3) #795 C14, report entry line (C8 second bullet).

#790 (C9 handoff template): 1) #792 C11, worker_done validation (S02-F27 asks worker to report the regression gate result in worker_done; listed as related); about 1 of 9 rows. 2) #799 C18, hand-back round n (round block of S04-F24). 3) #771, closeout wiring and already_closed (S14-F27).
