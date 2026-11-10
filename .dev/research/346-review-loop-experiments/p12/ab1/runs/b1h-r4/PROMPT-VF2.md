You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

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

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
