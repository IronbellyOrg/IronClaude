# Which Orca program the observer may run (owner question 13)

## Question in one sentence
May the observer dashboard fall back to a program simply named `orca` on the system path, when the sweep's rule is to never do that?

## Why you are being asked
The two programs find the Orca command line differently, and the planned contract note between them (a design file recording how they relate) must say whether that difference is accepted. Accepting it is a small written acceptance of risk, so it is yours.

## Background you need
- Orca is the local agent-orchestration app; both programs call its command line. On this host it is reachable as `orca-ide` and as `orca`.
- On Linux, a program named `orca` outside Orca's own terminals is usually the GNOME screen reader, not Orca.
- The observer (`superclaude observe`, merged) tries `orca-ide`, then `orca`, and uses one only if it answers an Orca-only question (`skills list --json` must list `orca-cli`). The issue watcher does the same.
- The sweep (`/sc:sweep`, PR #539) uses the variable `ORCA_CLI_COMMAND` if set, else `orca-ide`, and never `orca`. It asks no question first.
- So the two differ only if `ORCA_CLI_COMMAND` is set, or `orca-ide` is missing or fails. Today the variable is unset and both use `orca-ide`.

## Your options
1. **Yes, and write down the limit** (recommended)
   - If you pick this: the contract note records both rules, says the check proves "this is Orca" but not "the same Orca the sweep reads", records the Orca build next to each capture, and you are asked again if builds differ or `ORCA_CLI_COMMAND` is used. Two small gaps are logged for later, not fixed now.
   - Upside: no code change; keeps working where only `orca` exists; future programs get a stated rule.
   - Downside: two rules stay; a silent fallback to `orca` can happen if `orca-ide` is slow or broken.
2. **No: make the observer use the sweep's rule**
   - If you pick this: a small observer PR makes it use `ORCA_CLI_COMMAND`, else `orca-ide`, keeping the Orca check.
   - Upside: both read-only programs always read the same Orca, which helps a planned comparison of their records.
   - Downside: changes working code for a problem never seen; hosts with only `orca` stop working until the variable is set.
3. **No ruling: record both rules as facts**
   - If you pick this: the note lists both rules with no verdict; you are asked only if a difference is ever seen.
   - Upside: spends no decision on an unseen problem.
   - Downside: the next program that calls Orca has no rule to copy.

## What the debate found
- Two of three advocates picked option 1 when unassigned; one picked option 2 narrowly.
- All three agreed the Orca check proves identity, not sameness.
- On a normal host both programs already read `orca-ide`; the fallback matters only where `orca-ide` is missing.

## Recommendation and confidence
Option 1, 72 percent.

## If you do not answer
The note records both rules without a verdict (the same as option 3).

## What this answer does not authorize
No code change to the observer, the watcher or the sweep, no edit to PR #539, and no fix of the two logged gaps.

## How to answer
Type: "Q13: option 1" (or "Q13: option 2" or "Q13: option 3").
