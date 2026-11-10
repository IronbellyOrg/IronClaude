You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p16/ab4/runs/d4h-r2/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md F1)
### F1. Phase 0 acceptance check cannot pass as written. BLOCKING. CRITICAL.
- Issue: AC-0.4 says "steps 1-3 and 5-7 pass" in P0 (`spec:194`). Step 3 passes only if the worker_done "report path is the WC-4 contract path" (`spec:182`). The WC-4 contract does not exist for these commands until P1 (`spec:159`), and `spec:194` says so itself ("the contract arrives in P1").
- Grading check: An implementer who runs AC-0.4 as written in P0 finds that step 3 cannot pass, because the WC-4 contract path is not produced until P1 (`spec:159`), and that is wrong because `spec:194` says steps 1-3 pass.

### M2

#### M2.a (round1-a.md F2)
### F2. Two commands needing a change are assigned to no phase, so AC-1.1 cannot pass. BLOCKING. CRITICAL.
- Issue: `brainstorm` (`spec:84`) and `init-lite` (`spec:87`) are in section 3.1 and need the `## Unattended mode` section. The phase rows (`spec:159-162`) list P1 13 commands, P2 15, P3 4, P4 3, for 35 in total. The 3.1 and 3.2 rows add up to 37 (10 + 27). Neither brainstorm nor init-lite appears in any phase row. P1 says the flag is accepted "by every command in sections 3.1 and 3.2" (`spec:159`), and AC-1.1 asserts the section for every such command (`spec:195`).
- Grading check: An implementer who follows the phase table builds 35 of the 37 changes and leaves brainstorm and init-lite without `--unattended`, and that is wrong because `spec:195` requires the section for every command in 3.1-3.2.

### M3

#### M3.a (round1-a.md F3)
### F3. /sc:load contradicts itself on whether it names the contract. BLOCKING. MAJOR.
- Issue: The `load` row gives "Report (WC-4): none (see note)" (`spec:112`). The Decisions table says `/sc:load` gets no report file: "a report file would be an unrequested addition" (`spec:265`). AC-1.1 requires every command in 3.1-3.2 to have a section "naming `return-contract.yaml`" (`spec:195`), and `load` is in P1 (`spec:159`).
- Grading check: An implementer who follows the load row adds no contract and fails AC-1.1; an implementer who satisfies AC-1.1 writes a report file that the Decision rejects.

### M4

#### M4.a (round1-a.md F4)
### F4. The init-lite row breaks WC-6. BLOCKING. MAJOR.
- Issue: WC-6 allows exactly two behaviours: resume "when given its resume flag", or "writes each run into a fresh output directory", and a retry "must not corrupt the first attempt's output" (`spec:64`). The `init-lite` row says "Re-run overwrites its marked report" (`spec:87`; source `INV-A:55`, which says the marked report is overwritten on re-run). Overwriting is neither allowed behaviour.
- Grading check: An implementer who follows the init-lite row builds a re-run that replaces the first attempt's report, and that is wrong because WC-6 (`spec:64`) forbids corrupting the first attempt's output and allows only resume or a fresh directory.

### M5

#### M5.a (round1-a.md F5)
### F5. Ready-today commands can write one file from two workers. BLOCKING. CRITICAL.
- Issue: WC-11 says "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes" (`spec:69`). Section 2.3 sends workers to the current worktree by default (`spec:73`, citing `CAPS:115`: "workers share the current worktree by default"). `index-repo` is listed as ready today with brief flags "none" and writes a fixed `PROJECT_INDEX.md` whose location is only "implied" (`spec:86`, `INV-A:53`). It gets an output flag only in P1. `cleanup-audit` writes a fixed `.claude-audit/` path and the row relies on "one audit per worktree at a time (WC-11)" (`spec:85`). Section 2.3 does not state that serialization rule (`spec:73`). Ready waves run tasks in parallel (`CAPS:86`).
- Grading check: An implementer who dispatches two `index-repo` tasks in one ready wave (`CAPS:86`, placement `spec:73`) gets two writers to `PROJECT_INDEX.md`, and WC-11 (`spec:69`) says that must never happen.
---

### M6

#### M6.a (round1-a.md F6)
### F6. WC-3 lets a coordinator's answer become the implement Ruling. BLOCKING. CRITICAL (safety boundary).
- Issue: WC-3 says that when a gate "would resolve as blocked", the session "may instead ask the coordinator once ... wait, then re-invoke or resume the command with the answer as a flag" (`spec:61`). The `implement` halt at `E-HALT-QA` or `E-NO-RULING` is a blocked gate (`spec:109`). D2 option (a) keeps the rule that the person rules, and says the worker ends `failed` (`spec:234-236`). Option (b), a relayed Ruling, is described as one that "weakens a deliberate safety rule" (`spec:235`). The rule that "another agent's message ... [is] not acceptance" is quoted at `INV-A:66`, and `INV-A:66` says an Orca coordinator is "another agent".
- Grading check: An implementer who follows WC-3 as written lets the coordinator's answer to the worker's `ask` be passed back to `/sc:implement` as its Ruling, and that is wrong because `INV-A:66` quotes the rule that another agent's message is not acceptance. WC-3 thereby adopts D2(b) before the user decides it.

### M7

#### M7.a (round1-b.md B1)
**B1. [BLOCKING, High] Live-check steps 2 and 3 cannot both hold, and step 2 passes with no observation.**
- Cites: `S:181`, `S:182`; `CAPS:63` (the `check --wait ... --timeout-ms 900000` example); `CAPS:129` (absent vs null `agentWait`).
- Text: step 2 says `worker-show` "at least once per 5 minutes"; step 3 runs `check --wait --timeout-ms 900000` "until worker_done arrives".
- Wrong outcome: "An implementer who runs step 2 and then step 3 as ordered makes one `worker-show` call and then waits 15 minutes, so the 5-minute cadence is missed." The step-2 pass ("`agentWait` is never non-null") also holds when the field is absent, and `CAPS:129` says an absent field "means it never looked", so a run with zero observations passes.

### M8

#### M8.a (round1-b.md B2)
**B2. [BLOCKING, High] Step 3 has no branch for a worker `question` or `escalation`.**
- Cites: `S:61` (WC-3: a worker may ask the coordinator); `S:182` (types include `question`, loop "until worker_done arrives"); `CAPS:62` (`reply --id`); `CAPS:63`.
- Wrong outcome: "An implementer who follows step 3 as written, receives a `question`, and loops again never sends `reply`, so the worker stays parked in `ask` and no `worker_done` arrives."

### M9

#### M9.a (round1-b.md B3)
**B3. [BLOCKING, High] AC-0.4 cannot pass for the three P0 commands.**
- Cites: `S:182` (step 3 path must be "the WC-4 contract path"); `S:183` (step 4 parses YAML with `status` and `command`); `S:194` (AC-0.4 says step 4 "uses the command's existing report file"); `S:62` (WC-4 path `<output-dir>/return-contract.yaml`); `INV-B:242` (troubleshoot writes `REPORT.md`); `INV-B:272` (workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`); `INV-A:35`, `INV-A:60` (adversarial writes under `<output>/adversarial/`).
- Wrong outcome: "An implementer who runs AC-0.4 on `/sc:troubleshoot` gets `REPORT.md`, which is neither the WC-4 path nor YAML, so step 3 and step 4 fail; the same holds for the workflow and adversarial paths." The contract arrives in P1 (`S:194`), so the P0 gate cannot pass.

### M10

#### M10.a (round1-b.md B4)
**B4. [BLOCKING, High] P0 briefs must carry `--unattended`, which the spec adds only in P1.**
- Cites: `S:73` (2.3: each brief carries "the exact command line including `--unattended`"); `S:79` (3.1: ready commands run "if the brief uses the stated flags", and no stated flag is `--unattended`); `S:159` (P1 adds the flag "accepted by every command"); `S:180` (step 1 uses the 2.3 brief); `S:194` (AC-0.4 runs the commands "as real Orca workers").
- Wrong outcome: "An implementer who builds the P0 brief from 2.3 passes `--unattended` to `/sc:troubleshoot`, which has no such flag in P0, so the smoke run tests an undefined argument path, not the ready-today path the gate is meant to test."

### M11

#### M11.a (round1-b.md B5)
**B5. [BLOCKING, High] AC-0.4 claims the direct-run condition is checked in step 5, but step 5 checks only AskUserQuestion.**
- Cites: `S:184` (step 5 pass: "no AskUserQuestion call"); `S:194` ("no Agent-tool wrapper, verified in the step-5 transcript"); `S:43` (gap 1: no direct-route end-to-end run exists).
- Wrong outcome: "A P0 run in which the worker wraps the command in an Agent-tool subagent passes step 5 and AC-0.4." The direct route, which section 1.4 names as the main unproven point, is therefore never tested.

### M12

#### M12.a (round1-b.md B6)
**B6. [BLOCKING, High] The WC-4 fixed-path rule conflicts with the per-command rows, and pre-creation output has no location.**
- Cites: `S:62` (WC-4: `<output-dir>/return-contract.yaml`, "known before dispatch", includes "stops before any other output exists"); `S:83` (adversarial: `<output>/adversarial/return-contract.yaml`); `S:92` (workflow: pre-creation STOP contract, no output flag); `S:198` (AC-1.4 requires workflow to "state the contract is written for pre-creation STOPs"); `INV-B:272` (workflow writes no contract for pre-creation STOPs today); `INV-B:52`.
- Wrong outcome: "An implementer who follows WC-4 for workflow has no `--output` directory to write into, and the pre-creation contract's path depends on an id that does not exist before creation, so the coordinator cannot know the path before dispatch, which WC-4 requires."

### M13

#### M13.a (round1-b.md B7)
**B7. [BLOCKING, High] AC-2.2 requires a `blocked` outcome for every P2 gate, but WC-2 allows a documented default.**
- Cites: `S:200` (AC-2.2: "contract `status: blocked` with a non-empty `blocked_question`"); `S:60` (WC-2 (a) default, (b) flag, (c) blocked); `S:116` (research pins `--strategy planning`, no block); `S:103` (cleanup lists approval items, no block); `S:110` (improve, same).
- Wrong outcome: "An implementer runs AC-2.2 on `/sc:research --unattended`. The planning strategy is pinned (`S:116`), no blocked outcome occurs, and the AC requires one, so a correct implementation fails."

### M14

#### M14.a (round1-b.md B8)
**B8. [BLOCKING, High] AC-1.1 and AC-1.2 cannot pass at P1, and `load` cannot produce a contract.**
- Cites: `S:195` (AC-1.1: every command in 3.1-3.2 has the section); `S:159` (P1 scope lists 13 commands); `S:160-161` (P2-P3 scope); `S:112` (load: report "none", phase "P1 (usage line only)"); `S:265` (load is used inside a brief, not as a Task; no report file); `S:76-77` (every changed command gains the section); `S:196` (7.2 on each P1 command).
- Wrong outcome: "An implementer who finishes P1 as listed cannot pass AC-1.1, because auggie-review (P2, `S:160`) has no section. An implementer who adds the section to `load` writes a contract the spec says the command never writes (`S:112`)."

### M15

#### M15.a (round1-b.md B9)
**B9. [BLOCKING, High, outward action] P1 accepts `--unattended` on commands whose outward default is still on.**
- Cites: `S:159` (P1: the flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"); `S:100` (the auggie-review `--unattended` implication is in P2); `INV-A:38` (auggie-review posts to GitHub by default, "No confirmation prompt"); `S:67` (WC-9: outward defaults are off under `--unattended`); `S:114` (pr-submit pushes and replies by default; its fix is in P4).
- Wrong outcome: "An operator who follows the P1 brief runs `/sc:auggie-review <PR> --unattended`. The flag is a no-op at P1, the command posts review comments to GitHub, and WC-9 forbids that under `--unattended`."

### M16

#### M16.a (round1-b.md B10)
**B10. [BLOCKING, High, outward action] AC-4.2 claims to check for no install or VM, and checks only commit and PR.**
- Cites: `S:209` (AC-4.2: "no install, VM, commit or PR"; checks `git log -1` and `gh pr list`); `S:67` (WC-9: installs and provisions are off by default); `S:113` (post-release fix: installs and VM "off unless the brief authorizes them"); `INV-B:33` (post-release runs real installs and VMs).
- Wrong outcome: "An implementer whose post-release provisions a VM or runs a real-target install without authorization passes AC-4.2, because the check looks only at `git log` and the PR list."

### M17

#### M17.a (round1-b.md B11)
**B11. [BLOCKING, High] AC-C1 fails the contract text that SA-2 permits.** Experts: Fowler (boundaries), Whittaker (contradiction probe).
- Cites: `S:147` (SA-2: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file"); `S:172` (AC-C1 greps `src/superclaude/core` and excludes only `ccsession-tag`); `S:158` (P0 writes `src/superclaude/core/WORKER-CONTRACT.md`); `S:52` (the contract file is a core file).
- Wrong outcome: "An implementer who writes SA-2's permitted example, `orca orchestration ask`, into WORKER-CONTRACT.md fails AC-C1, which runs in every phase, so the implementer must choose between the two texts."

### M18

#### M18.a (round1-b.md B12)
**B12. [BLOCKING, High] The 7.2 commands omit the identity that the spec's own ORCA definition requires outside an Orca terminal.** Experts: Hohpe (messaging), Hightower (operations).
- Cites: `S:167` (ORCA means `orca-ide` outside an Orca terminal); `S:180`, `S:182` (no `--from` or `--terminal` in any `ORCA` command); `CAPS:149` (outside an Orca terminal the caller must pass `--from`/`--terminal`; without identity lifecycle commands are refused with `no_active_sender_terminal`); `CAPS:148`.
- Wrong outcome: "An implementer who runs step 1 from outside an Orca terminal, which `S:167` allows, gets `no_active_sender_terminal`, so step 1 cannot pass."

### M19

#### M19.a (round1-b.md B13)
**B13. [BLOCKING, High] WC-5 maps a present but unparseable or empty contract to `succeeded`.**
- Cites: `S:63` (WC-5: `--outcome failed` only when "the report says failed or blocked, or no report exists"; otherwise `succeeded`); `CAPS:73` (outcome mandatory); `S:183` (step 4 parses the file, but WC-5 does not use step 4's result).
- Wrong outcome: "An implementer who follows WC-5 for a worker that writes a 0-byte contract after a failed run sends `--outcome succeeded`, because the file exists and is not `failed` or `blocked`." The coordinator reads `succeeded`.

### M20

#### M20.a (round1-b.md B14)
**B14. [BLOCKING, High] WC-11 forbids a shared default file, but three ready-today or P1 rows keep one.**
- Cites: `S:69` (WC-11: "must never write the same file"; default paths carry a timestamp or the coordinator's slug); `S:85` (cleanup-audit: fixed output dir, "one audit per worktree at a time (WC-11)"); `S:86` (index-repo: `PROJECT_INDEX.md`, brief passes none); `S:87` (init-lite: default `.dev/superclaude/context-audit.md`); `CAPS:115` (workers share the current worktree by default).
- Wrong outcome: "Two index-repo workers dispatched with the brief in `S:86` (no flags) in one worktree both write `PROJECT_INDEX.md`, which WC-11 forbids." The "one audit at a time" note in `S:85` is not in WC-11 and is not in the 2.3 coordinator duties.

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
