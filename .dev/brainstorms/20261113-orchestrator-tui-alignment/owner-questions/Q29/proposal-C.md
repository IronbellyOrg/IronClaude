# Proposal C: decide later; record the sweep duty as not runnable and hold the join test

## Answer

Do not pick a delivery route now: the coordinator's `/sc:sweep` duty is recorded as "not runnable", XC-04 (the real-id join comparison) stays held, and the question is asked again when XC-04 is next, with the then-current state of the Coder pin and of this host's installs.

## What happens next if the owner picks it

1. The ledger records "SWEEP-RUNNABLE: not met; WC-16 `/sc:sweep` duty not runnable (Q29 default, date)".
2. The coordinator does not run `/sc:sweep`; any status it needs comes from Orca read verbs.
3. When the Coder monitor's pin bump lands on its own and the workspace is updated, the coordinator re-checks `superclaude sweep --help`; if it exits 0, the gate holds without a decision.
4. If it does not, Q29 is asked again before XC-04.

## What it unlocks

- Nothing new; it avoids an exception to the owner's update rule and any host change before it is needed.
- The template may deliver the sweep without anyone acting, because the monitor runs daily.

## What it costs or risks

- The coordinator runs without the sweep it was designed around (WC-16), and XC-04 and everything after it wait.
- On this host the gate may never pass on its own: the user-level install at `~/.local/bin` shadows the image install (observed 2026-11-14), so a template update alone may change nothing.
- The question returns later with the same options.

## What stays unresolved

- Everything Q29 asks.
