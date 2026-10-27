# D-0025 — Implementation notes

## Execution context

- T02.03 was executed before T02.01 (vendored ptytest sources) physically
  landed under `src/superclaude/cli/eval/pty/`. The directory was created by
  this task in order to host `PROVENANCE.md` and `CHECKLIST.md`. T02.01 will
  populate the rest of the directory (sources + `LICENSE` + `__init__.py`)
  and confirm/update the SHA row in `PROVENANCE.md` §2 in the same commit.
- This out-of-order execution is safe because T02.03 is EXEMPT-tier
  documentation that *describes* the pin and the policy — it does not depend
  on running code. The dependency relationship in phase-2-tasklist.md is
  reversed here only because the documentation surface (`PROVENANCE.md` +
  `CHECKLIST.md`) is what the SHA pin and cadence live in, and that surface
  must exist before T02.01 can write the SHA into it.

## SHA selection rationale

- The SHA `61a46870e38710c7cfc95f00cefbf0499111aa5f` is the upstream `master`
  HEAD on 2026-05-20 as returned by the GitHub commits API.
- This is the same SHA that T02.01 would naturally pin against if it ran
  today. If upstream advances between now and T02.01 landing, T02.01 has
  authority to pick the newer SHA and update the row.
- We chose to record a concrete SHA (rather than a TBD placeholder) so that
  the AC10 acceptance criterion ("records fork SHA") is unambiguously met
  by the artifact T02.03 produces, independent of T02.01 timing.

## Cadence anchor selection rationale

- The first review is due 2026-08-20 (90 days from authoring). This is a
  deliberate choice over alternatives:
  - "First review on M2 exit" → couples the cadence to an internal milestone
    that may slip; the calendar-based anchor is more durable.
  - "First review one year out" → too lax for a security-sensitive PTY layer.
  - "First review at next quarterly board" → no such board exists for this
    project.
- 90 days matches the cadence specified in `decisions.md` D-1
  ("Quarterly review of upstream `pexpect` releases; resync if
  security-relevant.") so the policy is internally consistent.

## Why CHECKLIST.md and not a CI automation

- T02.03 is intentionally a *procedure* artifact. Automating the quarterly
  trigger is deferred to R5-mit (T02.26 per `phase-2-tasklist.md` Notes) so
  that the policy lands first and the automation can be designed against the
  established procedure rather than guessed at.
- The 5-step shape was chosen so each step has a single decision point and
  a single output, making the procedure easy to follow in 15 minutes by
  someone other than the original author.

## Open caveats

1. **SHA reconciliation gap.** Between T02.03 landing and T02.01 landing,
   the PROVENANCE.md SHA row points at the *intended* vendoring target, not
   at on-disk content. T02.01 closes this gap. Until then, the `Vendoring
   date` and `Vendoring commit` rows remain `TBD`.
2. **No upstream LICENSE byte hash captured.** `CHECKLIST.md` Step 4
   instructs the reviewer to diff the upstream LICENSE against the vendored
   copy, but does not record a current SHA256 of the LICENSE text. This is a
   deliberate omission — capturing the hash here would create a second pin
   that has to be maintained in lockstep with the source pin. The diff is
   cheaper and self-documenting.
3. **Out-of-band trigger list is curated, not exhaustive.** The three triggers
   in §3 of PROVENANCE.md cover the realistic high-signal cases. A
   conservative reviewer may add more without amending this file.
