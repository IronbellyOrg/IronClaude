# Q30: Which coordinator Run may OB-04 read, and do you accept in writing that its questions may be consumed?

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q30 (line 557).

> Which coordinator Run may OB-04 read, and do you accept in writing that its questions may be consumed? (new, R25-INV-008)

## The spec's recommended answer (verbatim)

> A disposable representative Run you open for the test (a live `--wait` listener and an ack cycle), never the program's own

## Default if unanswered (verbatim)

> OB-04 held; OB-06 not opened

## What it gates (in words)

- OB-04: one recorded live attempt of the observer's coordinator-questions panel in the real coordinator layout, run in the terminal that holds the chosen Run (`merged-requirements.md:252`). The observer is `superclaude observe`, the read-only terminal dashboard of Orca workers (issue #409).
- Through OB-04, OB-06: the guard-flip PR that switches the observer's questions read on (`QUESTION_GATE_PASSED = True`); it needs OB-04's record (`merged-requirements.md:254`, (c)).
- Wave: W1 (the second wave); asked when the item is next (`merged-requirements.md:523`, `:557`).

## Facts the question depends on

1. Orca terms (ADJ glossary, `alignment-findings-adjudicated.md:76`): a Run is one coordinated piece of work, a Dispatch one task handed to a worker, a Worker an agent session on a Dispatch.
2. Gate test Q-1 failed on 2026-11-11: a terminal that does not hold a Run cannot read another terminal's Run, so only the terminal holding the Run can read its questions (ADJ `:87`; INV-024 at ADJ `:465`).
3. `run-use` on a live coordinator (gate test Q-2) has never been tested and is forbidden for the observer (ADJ `:87`; `merged-requirements.md:252` (3)).
4. Open question X-016 (61 percent, unproven both ways): whether the observer's read `check --all --types question` consumes messages on a live coordinator Run. Orca's own `check --help` on this build says `--all` "does not mark read" and that `--peek` and `--all` "do not drain a mailbox on their own" (ADJ `:144`, E-18; `:333`). Plain `check` reads and removes a message (ADJ `:97`).
5. OB-03, the seeded consumption test on a throwaway Run created with `run-create`, runs before OB-04; it is necessary but not sufficient, because a throwaway Run has no `--wait` listener or acknowledge cycle ("A bound Run replays the same Delivery until --ack") and a pass says nothing about usability (INV-041, ADJ `:470`; `merged-requirements.md:251`, `:1156`).
6. The program's own coordinator (XC-09) re-arms its `--wait` continuously; if the read consumed there, the program would lose its own workers' questions and their acknowledgement timeline (probe R25-INV-008, `adversarial/adversarial/invariant-probe.md:16`).
7. 28 of 53 Runs on record have no `coordinator_handle`; whether a person can use the panel in a terminal that already holds a Claude coordinator session is UNVERIFIED (INV-024; ADJ `:146`, `:497`).
8. The owner's existing pass record covers one old Run, `run_93bfa00cae2b` ("Claim issue 375"); the scope of the pass is question Q6 (ADJ `:458`, `:776`).
9. Authority limits: Q30 does not authorize `run-use` or any Run other than the named one (`merged-requirements.md:578`); OB-04 needs its own `GRANT(OB-04,live-read)` ledger row (`:252`).
10. Every live lane needs the Orca app to answer (ORCA-AVAILABLE); it did not answer on 2026-11-13 (`merged-requirements.md:604`; current state not re-checked here).
