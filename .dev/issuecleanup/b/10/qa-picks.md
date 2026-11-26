# QA picks (written before opening any findings file)

## #815 (W7 narrower token scope)
1. #722 - shared GitHub login / who-approved identity; a separate agent account or App is the identity decision that a narrower poll token depends on.
2. #818 (W10) - permissions of launched sessions; the other credential/permission-scope FU item.
3. #723 - master/integration protection rules; other GitHub-permission hardening work.

## #816 (W8 alert after three bad cycles)
1. #814 (W6) - shadow-run check also reads exit codes from audit log/status per cycle.
2. #820 (W12) - the other item that needs a reader over the audit log / status numbers.
3. #761 - gaps list for watcher and coordinator.

## #817 (W9 conditional reads)
1. #812 (W4) - GitHub throttling backoff; same call-budget/rate-limit area.
2. #811 (W3) - poll interval, the other lever on call volume.
3. #761 - gaps list for watcher and coordinator.
