You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r3/vf2. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r3/vf2/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r3/vf2/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2-r3/vf2/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### M-15
### M-15 (MAJOR label, Medium, priority Low, Adzic), origin=unchanged, quotes the changed line
Texts: the changed AC-1.1 at S:195, "every command in sections 3.1-3.2 except `load` (B-1)", sets that load has no section and no contract (S:112 "none (see note)"). The neighbouring AC-1.2 at S:196 reads "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass", and P1 at S:159 lists "load (usage line only)" in its Commands column. Step 4 of 7.2 (S:183) runs `test -s <contract>`, and step 3 (S:182) needs "its report path is the WC-4 contract path". For load there is no contract.
Why Medium and not blocking: the sentence "an implementer builds AC-1.2 against load and step 4 fails" needs the guess that "each P1 command" includes a command whose own row says "use it as a step inside another worker's brief, not as its own Task" (S:112); both readings are allowed. It surfaces only because the changed line made load's missing contract explicit. Same family: WC-4 (S:62) says "In unattended mode the command writes" the contract, and S:159 has load accept `--unattended`.

### N-6
| N-6 | minor | changed | Wiegers | the review id `(B-1)` sits inside two normative sentences, so a test author meets an id the spec never defines | S:76, S:195 |

### N-7
| N-7 | minor | unchanged | Wiegers | S:52 "Each changed command adds a short `## Unattended mode` section" has no `load` exception; S:76 carries it | S:52, S:76 |

### B-2
### B-2 (open, blocking, priority High, Fowler)
Texts as in the prior-findings table above. Grading sentence (FIRST-REVIEW form, re-applied to the AFTER text): An implementer who follows the stated text as written takes `<output-dir>` to be the value of `--output`, which for tdd is the TDD file (S:90), so the contract path is `<TDD file>/return-contract.yaml`, a path beneath a regular file that cannot be created, and X is wrong because AC-2.2 (S:200) and step 4 of 7.2 (S:183) then cannot read the contract that WC-4 says is written on every outcome, including blocked. WC-4 (S:62) says the `--output` value is a directory; S:87 and S:90 say it is a file. Two stated texts contradict, and an acceptance criterion cannot pass as written. The grade holds; no further assumption is needed.
Narrowest repair: in WC-4, say where the contract goes when `--output` is a file (a named sibling directory or a separate report-directory flag), one sentence, and make the init-lite and tdd rows and AC-2.2 agree with it.

Write your full reply to .dev/orca-command-refactor/review/verify-2.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
