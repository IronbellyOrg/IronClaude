### M2
| M2 | open | Row `candidate:86` now asks for a per-run directory, which WC-6 needs, but no phase schedules it: the P1 command list at `candidate:160` omits init-lite. The same row also changes the standalone `--output` type (see N2). Open until N1 and N2 are fixed. |
(text of this finding in the prior report)
### M2
#### M2.a, from round1-a.md B2: *B2. init-lite re-run overwrites its report, which WC-6 forbids.** Expert: Nygard (lead), Fowler. Severity: MAJOR, blocking.
- Stated texts: section 3.1 gives init-lite "Re-run overwrites its marked report" (spec:87). WC-6 says a command either resumes from its on-disk state or "writes each run into a fresh output directory so a re-run starts clean", and that a retry "must not corrupt the first attempt's output" (spec:64). The inventory agrees on the overwrite (INV-A:55).
- Grading sentence: An implementer who follows section 3.1 leaves init-lite as it is, so a `worker-start --retry-of` re-run replaces the first attempt's `context-audit.md`; WC-6 says the retry must not corrupt that output, and the spec names no third option.

### N1
### N1 (blocking, origin=changed): the init-lite fix is in no phase, and the row still treats init-lite as ready today
- Location: `candidate:86` (row), `candidate:79` (3.1 header), `candidate:92` (end of 3.1), `candidate:159` (P0), `candidate:160` (P1 scope).
- Stated texts: `candidate:86` says the brief must pass `--output <dir>` "after P1" and gives the fix as "Per-run output directory (P1)". `candidate:160` lists the P1 commands as "analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow". init-lite is not in that list, and P2-P4 (`candidate:161-163`) do not name it either. `candidate:79` says the 3.1 commands "run as workers now if the brief uses the stated flags", and `candidate:159` says P0 "uses only the 9 ready commands (section 3.1)", which includes init-lite.
- Grading sentence: an implementer who follows the P1 scope at `candidate:160` does not change init-lite, so a `worker-start --retry-of` re-run writes over the first attempt's `context-audit.md`, which WC-6 (`candidate:64`) forbids. An implementer who follows `candidate:79` and `candidate:86` dispatches init-lite today with `--output <dir>`, a value the flag does not accept today (`.dev/orca-command-refactor/specs/history/spec-v1.md:87` says `--output <file>`). Two stated texts contradict each other on the phase and the readiness of this command.

### N2
### N2 (blocking, origin=changed): the init-lite row changes the standalone `--output` type
- Location: `candidate:86`. Conflicting texts: `candidate:147` (SA-1) and `candidate:143` (the section-5 hard requirement on every phase). Baseline for comparison: `.dev/orca-command-refactor/specs/history/spec-v1.md:87` (`--output <file>`).
- Stated texts: `candidate:86` makes `--output` "directory-valued" ("the flag becomes directory-valued") with no `--unattended` qualifier. SA-1 (`candidate:147`) says that without `--unattended` "every ... output path ... stays as it is today".
- Grading sentence: an implementer who follows `candidate:86` makes `--output` directory-valued for every run, so a person who runs `/sc:init-lite --output report.md` in a plain session gets a directory where today they get a file. SA-1 forbids that, and the two texts contradict each other.
