# Proposal B: live side: keep today's observer behaviour and make it the rule

## Answer

`reclaimable` counts on the live side of the line, not historical: a reclaimable worker still has something for a person to do (Orca's next action is `release`), so it stays in the observer's default view as it does today. The mapping table records this as the decided meaning; no code changes.

## What happens next if the owner picks it

1. The contract note draft (XC-05) writes the mapping row: "reclaimable = not historical; shown in the default view with Orca's word `reclaimable`, because it still awaits release".
2. No change to the observer: `HISTORICAL_STATES` stays `("released", "retained")` (`view.py:35`), so reclaimable rows stay visible by default, exactly as built and merged (PRs #503, #514).
3. No change to the sweep: its "safe to close" already says "could not determine" for a reclaimable worker whose next action is `release` (`classify.py:479-481`), which matches "still needs attention".
4. OB-06 prerequisite (e) is met by the row.

## What it unlocks

- Zero code change and zero new test; the decision ratifies the observer as built.
- A reclaimable worker stays in front of a person until it is released, which is the cleanup cue Orca's next action points at.
- The guard-flip PR (OB-06) can proceed with a final row.

## What it costs or risks

- The default observer view can be dominated by finished workers: at the probe Orca reported 27 reclaimable and 0 active (INV-023). A person scanning for working agents sees a list of finished ones.
- "Live" may mislead: a reclaimable worker is not running. The row must say "awaiting release", not "running".
- Orca's exact meaning of `reclaimable` is UNVERIFIED; if it means "already finished and safe to forget", this choice keeps noise on screen.

## What stays unresolved

- Orca's own definition of `reclaimable`.
- Whether a later observer release should add a separate "awaiting release" group.
