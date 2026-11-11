You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2/runs/b2h-r3/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

### F-01
### F-01 | MAJOR | BLOCKING | Expert: Newman (interface evolution, phased rollout)
- Location: `SPEC:73`, `SPEC:79`, `SPEC:158`, `SPEC:159`, `SPEC:194`.
- Issue: `SPEC:73` requires every brief to state "the exact command line including `--unattended`". `SPEC:79` says the ten ready-today commands run as workers "if the brief uses the stated flags", and the table at `SPEC:83-92` lists no `--unattended` flag. `SPEC:159` introduces the flag only in P1. P0 (`SPEC:158`) and its check AC-0.4 (`SPEC:194`) run the ready commands with briefs built per `SPEC:73`.
- Grading sentence: An implementer who follows `SPEC:73` for the P0 smoke runs writes `--unattended` into briefs for commands that do not yet define it, so their gates take the interactive path and the worker stalls, which is the failure WC-2 forbids (`SPEC:60`). Two stated texts conflict.

### F-02
### F-02 | MAJOR | BLOCKING | Expert: Fowler (interface design)
- Location: `SPEC:62` (WC-4), `SPEC:73`, `SPEC:87`, `SPEC:90`, `SPEC:92`; `INV-B:47`, `INV-B:52`, `INV-B:273`; `INV-A:55`.
- Issue: WC-4 requires `<output-dir>/return-contract.yaml`, where `<output-dir>` is what the coordinator passes, and says the path is "known before dispatch" (`SPEC:62`, repeated in `SPEC:73`). Two rows break this:
  - `/sc:workflow` writes `.dev/tasks/to-do/<id>/return-contract.yaml` and "Fresh package each run" (`SPEC:92`). `INV-B:52` and `INV-B:273` describe the `<id>` and "never overwrites or reuses"; nothing in the spec says who sets `<id>` or when it is known.
  - `/sc:tdd` and `/sc:init-lite` take `--output <file>` (`SPEC:90`, `SPEC:87`; `INV-B:47`, `INV-A:55`). A file has no directory to hold `return-contract.yaml`. WC-4 never says how a file-valued output maps to `<output-dir>`.
- Grading sentence: An implementer who follows WC-4 for `tdd --output docs/x.md` writes the contract to `docs/x.md/return-contract.yaml`, and one who follows it for `workflow` cannot name the path before dispatch, so the coordinator opens a missing file and the worker's outcome becomes `failed` under WC-5 (`SPEC:63`). Two stated texts cannot both hold.

### F-03
### F-03 | MAJOR | BLOCKING | Expert: Nygard (retry safety, failure modes)
- Location: `SPEC:64` (WC-6), `SPEC:69` (WC-11), `SPEC:85`, `SPEC:86`, `SPEC:87`; `INV-A:53`, `INV-A:55`, `INV-A:107`.
- Issue: WC-6 says "a retry worker must not corrupt the first attempt's output" (`SPEC:64`). WC-11 says "default output paths carry a timestamp or the slug the coordinator passes" (`SPEC:69`). The section 3.1 rows use fixed defaults:
  - `index-repo` writes a fixed `PROJECT_INDEX.md` (`SPEC:86`; `INV-A:53`).
  - `init-lite` writes a fixed `.dev/superclaude/context-audit.md` and its resume column reads "Re-run overwrites its marked report" (`SPEC:87`).
  - `cleanup-audit` writes a fixed `.claude-audit/` directory (`SPEC:85`; `INV-A:107`).
  The spec's "What changes" column adds only "State the output location" for index-repo (`SPEC:86`), not a per-run path.
- Grading sentence: An implementer who follows the section 3.1 rows builds a retry of `init-lite` that overwrites the first attempt's report, and two `index-repo` workers in one worktree that write the same `PROJECT_INDEX.md`, so the earlier output is lost. The spec's own WC-6 and WC-11 forbid both. Two stated texts conflict, and data is lost.

### F-04
### F-04 | MAJOR | BLOCKING | Expert: Wiegers (testability)
- Location: `SPEC:195` (AC-1.1), `SPEC:112` (`load`), `SPEC:87` (`init-lite`), `SPEC:265` (`/sc:load` decision), `SPEC:159`.
- Issue: AC-1.1 requires that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`" and that the test passes at P1. Two commands cannot meet this as the spec defines them:
  - `load` is in section 3.2 but writes no file: "None" report and "use it as a step inside another worker's brief, not as its own Task" (`SPEC:112`). The decision at `SPEC:265` says "a report file would be an unrequested addition".
  - `init-lite` reports to `.dev/superclaude/context-audit.md` or `--output` (`SPEC:87`), not `return-contract.yaml`, and no phase (`SPEC:158-162`) adds a contract to it. P1's command list (`SPEC:159`) does not name it.
- Grading sentence: A test written from AC-1.1 fails for `load` and for `init-lite`, so the P1 exit check cannot pass as written. Blocking because the acceptance criterion cannot be met.

### F-05
### F-05 | MAJOR | BLOCKING | Expert: Whittaker (zero/empty attack, FR-2.1); see Adversarial Analysis A-1
- Location: `SPEC:63` (WC-5), `SPEC:183` (7.2 step 4).
- Issue: WC-5 sends `--outcome failed` "when the report says failed or blocked, or no report exists", and `succeeded` "otherwise" (`SPEC:63`). A contract that exists but is zero bytes, truncated, or has no `status` key matches none of the failed cases, so it falls to "otherwise". The validity check is in step 4 (`SPEC:183`), which runs after the coordinator has already settled the Task.
- Grading sentence: An implementer who follows WC-5 literally sends `--outcome succeeded` for an empty or unparseable contract, and the Task settles as succeeded with no deliverable. Blocking because the stated rule produces a concrete wrong outcome.

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
