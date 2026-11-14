# Proposal A: no live attempt for now; hold OB-04 and keep the guard off

## Answer

Name no Run and accept no consumption risk: OB-04 is held, the guard-flip PR (OB-06) is not opened, and the observer's questions panel stays off until a later decision.

## What happens next if the owner picks it

1. The ledger records "OB-04 held (Q30 default, date); OB-06 not opened".
2. OB-03, the seeded consumption test on a throwaway Run, may still run if its own approval exists; its record is kept.
3. The observer keeps working without the questions panel (the guard is `False` on master).
4. Q30 is asked again only if the owner wants the questions panel, with OB-03's result in hand.

## What it unlocks

- Nothing new; it guarantees no live coordinator Run is read by the observer and no question can be lost.
- It costs no setup: no extra coordinator session, Run or worker.

## What it costs or risks

- The questions panel (the observer's release-2 feature) never ships while held; the guard-flip PR waits indefinitely.
- OB-03's result, however good, cannot be turned into a flip.
- The open question of whether the panel is usable in a real coordinator terminal stays open.

## What stays unresolved

- Everything about usability in the real layout (INV-024).
