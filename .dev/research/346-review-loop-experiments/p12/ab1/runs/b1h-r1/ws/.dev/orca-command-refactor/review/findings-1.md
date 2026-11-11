Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B1)
### B1. Contract directory is undefined for file-valued or fixed-path commands (requirements, WC-4)
- Evidence: WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" and requires the path known before dispatch (`spec:62`; `spec:73`).
- `/sc:tdd` takes `--output <file>` (`spec:90`; `INV-B:222`). `/sc:init-lite` takes `--output <file>` (`spec:87`; `INV-A:55`). The AC-2.2 gate-trigger example passes `--output <file>` to tdd (`spec:200`).
- `/sc:cleanup-audit` writes a fixed `.claude-audit/` with no output flag (`spec:85`; `INV-A:42`). `/sc:index-repo` writes `PROJECT_INDEX.md` with "brief must pass: none" (`spec:86`; `INV-A:53`).
- Grading sentence: the stated text defines `<output-dir>` as a directory, and the tdd row passes a file, so the text contradicts itself. An implementer following WC-4 cannot say where `return-contract.yaml` goes for `/sc:tdd --output <file>`. The coordinator then cannot open the contract at the path it was given, and AC-2.2 step 4 (`spec:183`, `spec:200`) reads a file the spec never names.

### M2

#### M2.a (round1-a.md B2)
### B2. AC-0.4 step 4 cannot pass for the P0 smoke commands (acceptance)
- Evidence: AC-0.4 uses "the command's existing report file" for step 4 (`spec:194`). Step 4 loads YAML and asserts `status` and `command` keys (`spec:183`).
- `/sc:troubleshoot` writes `REPORT.md` as `report_path`. Its return contract exists only with `--caller task-unified` (`spec:91`; `INV-B:242`). `/sc:adversarial` names no contract filename (`spec:83`; `INV-A:35`, `INV-A:60`). Both are in the P0 smoke set (`spec:158`).
- Grading sentence: an implementer who runs step 4 on `REPORT.md` gets a markdown file with no `status` or `command` keys, so step 4 fails on the first P0 troubleshoot run and P0 cannot close as written.

### M3

#### M3.a (round1-a.md B3)
### B3. Section 3.1 says ready commands change only in one column, which contradicts P1 and AC-1.1 (requirements)
- Evidence: `spec:79` says the ten ready commands "run as workers now" and "The only command changes are the small fixes in the last column." `spec:52` says each changed command "adds a short `## Unattended mode` section." P1 requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`spec:159`). AC-1.1 requires every command in 3.1 to 3.2 to have the section (`spec:195`).
- Grading sentence: an implementer following `spec:79` leaves the ten ready commands without the `## Unattended mode` section and without the flag. AC-1.1 then fails in P1. The two stated texts contradict each other.

### M4

#### M4.a (round1-a.md B4)
### B4. AC-C1 matches nothing as written, and it cannot pass P0 as scoped (acceptance, SA-2)
- Evidence: AC-C1 (`spec:172`) writes its alternation as `(orchestration\|worktree\|terminal\|agent)` inside `grep -E`. In `grep -E`, `\|` is a literal pipe, so the pattern never matches an Orca subcommand. The sandbox check in section 1 confirms this. The `\` is a GFM table escape, so the rendered page looks correct and the raw text does not work.
- AC-C1 scans `src/superclaude/core`, and its only exclusion is `ccsession-tag` (`spec:172`). P0 writes `src/superclaude/core/WORKER-CONTRACT.md` and adds an Orca section to `src/superclaude/core/HOW-WE-WORK.md` (`spec:158`). SA-2 allows an Orca mention "inside the contract file" (`spec:147`). AC-C1 has no exemption for it.
- Grading sentence: an implementer who copies AC-C1 as written gets a check that passes any command calling `orca orchestration`, so SA-2 (a hard requirement, `spec:142`) is not enforced. An implementer who fixes the escaping, and writes the routing-guide section with any `orca orchestration` text as P0 asks, fails AC-C1 in P0. The stated texts contradict each other.

#### M4.b (round1-b.md B5)
**B5. AC-C1 forbids the Orca mention that SA-2 permits, and P0 writes that mention.** (Fowler; Newman)
- Locations: SPEC:172 (AC-C1 greps `src/superclaude/core`), SPEC:147 (SA-2: "the only allowed mention of Orca in a changed command is ... inside the contract file"), SPEC:52 and SPEC:158 (the contract file is `src/superclaude/core/WORKER-CONTRACT.md`; P0 adds an Orca section to `HOW-WE-WORK.md`, also in core).
- Grading sentence: an implementer who writes the contract file as SA-2 permits, naming the `orca orchestration ask` question channel, makes AC-C1 print a match over `src/superclaude/core`, so AC-C1 fails in P0 on text the spec allows.

#### M4.c (round1-c.md B1)
### B1. The SA-2 exception, AC-C1 and the P0 Orca sections contradict each other
- **Sentence.** An implementer who follows SA-2 (spec:147), which allows Orca to be named "as an example of a caller's question channel inside the contract file", and names `orca orchestration ask` in `src/superclaude/core/WORKER-CONTRACT.md`, builds a file that AC-C1 (spec:172) rejects. AC-C1 greps `src/superclaude/core` and exempts only `skills/ccsession-tag/`, so the common check fails in P0 (spec:158, spec:170).
- The same grep also rejects the Orca section P0 adds to `HOW-WE-WORK.md` (spec:158; SA-5 at spec:150). SA-2's exception covers only the contract file, so the routing guide has no permitted form at all.

### M5

#### M5.a (round1-b.md B1)
**B1. The contract path rule is contradicted, and the workflow path is not known before dispatch.** (Wiegers lead; Fowler)
- Locations: SPEC:62 (WC-4: `<output-dir>/return-contract.yaml`, "known before dispatch"), SPEC:73 (the coordinator's brief states the output directory), SPEC:83 (adversarial: fix the filename to `<output>/adversarial/return-contract.yaml`), SPEC:92 (workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`, "Fresh package each run"; no output flag). Supporting: INV-B:52, INV-B:272 (the workflow package is created fresh per run).
- Grading sentence: an implementer who follows WC-4 at SPEC:62 writes adversarial's contract to `<output>/return-contract.yaml`, but the row at SPEC:83 names `<output>/adversarial/return-contract.yaml`, so the path the coordinator computes from SPEC:73 and the file the worker writes differ. For workflow, the id is generated per run and SPEC:92 gives no flag that sets it, so the coordinator cannot know the path before dispatch, which WC-4 requires.

### M6

#### M6.a (round1-b.md B2)
**B2. WC-3 lets a coordinator's answer resume a command past a safety gate.** (Wiegers lead; Whittaker)
- Locations: SPEC:61 (WC-3: on a gate that would be blocked, the session may `ask` the coordinator, "then re-invoke or resume the command with the answer as a flag"), SPEC:109 (implement: "the Ruling rule itself is unchanged (see open decision D2)"), SPEC:233 (the spec quotes the rule: "another agent's message ... [is] not acceptance"), SPEC:234-236 (D2 recommends option (a), keep the rule), SPEC:208 (AC-4.1 relies on D2).
- Grading sentence: an implementer who follows WC-3 at SPEC:61 has no exclusion for the implement Ruling, so the coordinator's `ask` reply can be passed back to `/sc:implement` as a flag, which resolves a halt that SPEC:109 says keeps the Ruling rule unchanged, and the rule the spec itself quotes at SPEC:233 excludes a message from another agent.

### M7

#### M7.a (round1-b.md B3)
**B3. The P0 acceptance run cannot pass as written.** (Adzic; Wiegers)
- Locations: SPEC:182 (7.2 step 3, pass: "its report path is the WC-4 contract path"), SPEC:194 (AC-0.4: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"), SPEC:159 (P1 is where WC-4 is delivered).
- Grading sentence: an implementer who runs AC-0.4 in P0 on `/sc:troubleshoot` finds step 3 fails, because step 3 requires the WC-4 contract path and WC-4 does not exist until P1 (SPEC:159), while AC-0.4 says step 3 passes.

### M8

#### M8.a (round1-b.md B4)
**B4. Step 6 cannot pass for edit-in-place commands, including their P2 happy path.** (Wiegers; Cockburn)
- Locations: SPEC:185 (step 6: "only files under the brief's output directory (and the command's documented artifacts) appear"), SPEC:201 (AC-2.3: a P2 happy-path run must pass 7.2), SPEC:103 (cleanup applies items) and SPEC:110 (improve applies items), both in P2 (SPEC:160). Supporting: INV-A:43 and INV-A:52 ("Edits code").
- Grading sentence: an implementer who runs cleanup's happy path under step 6 as written sees its edited source files in `git status`, and those files are neither under the output directory nor documented artifacts of the command, so the check fails for a correct run; the only way to pass is to read "documented artifacts" as including applied edits, which the spec never says.

### M9

#### M9.a (round1-c.md B2)
### B2. The ready tier (section 3.1) says no command changes, but section 2.3, P0, P1 and AC-1.1 require them
- **Sentence.** An implementer who follows section 3.1 ("These run as workers now", "The only command changes are the small fixes", spec:79) and runs the ten ready commands without `--unattended` builds workers that do not match section 2.3 (the brief must carry `--unattended`, spec:73) or the P0 check (spec:180 step 1 and spec:194, AC-0.4).
- P1 (spec:159) adds the `--unattended` flag to every command in sections 3.1 and 3.2. AC-1.1 (spec:195) requires every command in 3.1 and 3.2 to have a `## Unattended mode` section naming `return-contract.yaml`. Section 3 says changed commands gain that section (spec:76). Brainstorm (spec:84) and init-lite (spec:87) list the small fix as "None", so AC-1.1 cannot pass for them as the tables are written.
- P0 is "no command edits" (spec:158), yet its smoke runs follow 7.2 (spec:194), and 7.2 needs the flag.

### M10

#### M10.a (round1-c.md B3)
### B3. The fixed contract path in WC-4 does not fit the ready commands, so AC-0.4 and AC-1.2 cannot pass for them
- **Sentence.** An implementer who follows WC-4 (spec:62: `<output-dir>/return-contract.yaml`, known before dispatch) and the section 3.1 row for workflow (spec:92) finds that the workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (INV-B:272), where `<id>` is made by the command. The coordinator cannot know the path before dispatch, and no phase gives workflow an output directory. AC-0.4 step 3 (spec:182, spec:194) requires "the WC-4 contract path", so it cannot pass for workflow.
- cleanup-audit (spec:85; INV-A:42) writes `.claude-audit/pass<N>-summary.md` into a fixed directory and writes no contract. index-repo (spec:86; INV-A:53) writes `PROJECT_INDEX.md` and takes no output flag. The candidate adds neither a contract nor an output flag to either, yet AC-1.2 (spec:196) runs step 4 (spec:183) on every P1 command with `--unattended --output <dir>`, and P1 (spec:159) lists both.
- The two path rules also disagree for adversarial. spec:83 fixes its contract at `<output>/adversarial/return-contract.yaml`, while WC-4 (spec:62) puts the contract directly in `<output-dir>`. init-lite takes `--output <file>` (spec:87), so its "output directory" is a file, and WC-4 needs a directory.
