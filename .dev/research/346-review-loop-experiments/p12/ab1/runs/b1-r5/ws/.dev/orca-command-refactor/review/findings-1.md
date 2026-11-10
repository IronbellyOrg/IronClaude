Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md F1)
### F1. CRITICAL-in-effect, blocking: AC-1.1 cannot pass for `load`, `brainstorm` and `init-lite` as the spec defines them
- Stated texts that contradict:
  - `spec:195` (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `spec:159` (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". `spec:196` (AC-1.2): "7.2 live check on each P1 command", whose step 4 requires `test -s <contract>` (`spec:183`).
  - `spec:112` (`load` row, section 3.2, phase P1): report "none (see note)", resume "n/a", "none: use it as a step inside another worker's brief, not as its own Task"; the decision row at `spec:265` repeats it: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - `spec:79`: for the 3.1 commands "The only command changes are the small fixes in the last column", and `spec:84` (`brainstorm`) and `spec:87` (`init-lite`) give "None" as the small fix. Neither is assigned to a phase in `spec:158-162`.
- Grading sentence: An implementer who follows the stated text as written adds a usage-line fix to `load`, no contract and no `## Unattended mode` section to `load`, `brainstorm` or `init-lite`, and AC-1.1 (which every phase check list requires to pass, `spec:167`) fails for those three commands, because AC-1.1 demands the section and the contract name on every 3.1-3.2 command. The acceptance criterion cannot pass on the spec's own per-command rows. For `load`, the AC-1.2 live check also cannot pass: the command writes no `return-contract.yaml`, so `test -s` fails.
- Why not Medium: no guess is needed. Two quoted rules ("every command ... has a section naming `return-contract.yaml`" and "`load`: report none, no file") exclude each other for `load`, and for `brainstorm`/`init-lite` the "None" cells and the 3.1 intro exclude the section AC-1.1 requires.

### M2

#### M2.a (round1-a.md F2)
### F2. CRITICAL-in-effect, blocking: the `/sc:adversarial` contract path in section 3.1 contradicts the WC-4 path the coordinator will read
- Stated texts that contradict:
  - `spec:62` (WC-4): the command writes `<output-dir>/return-contract.yaml`, "`<output-dir>` is the directory the coordinator passed", and the worker passes that path as `--report-path`. `spec:73` and `spec:182` / `spec:183` (7.2 steps 3-4): the report path is "the WC-4 contract path" and the check runs `test -s <contract>`.
  - `spec:83` (adversarial row): the brief passes `--output <dir>` and the P1 fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml`". `spec:198` (AC-1.4) accepts "adversarial names one fixed path" without saying which.
- Grading sentence: An implementer who follows the stated text as written fixes `/sc:adversarial` to write `<output>/adversarial/return-contract.yaml`; a coordinator that follows WC-4 and 7.2 reads `<output>/return-contract.yaml`, finds no file, and the live check at `spec:183` fails for adversarial, one of the three P0 smoke commands (`spec:158`, `spec:194`). Two stated paths for one file cannot both be the "WC-4 contract path". INV-A:60 confirms the on-disk drift this is meant to fix: contracts exist at two places, `.../P3-command-set/adversarial/return-contract.yaml` and a second one.

### M3

#### M3.a (round1-b.md F1)
### F1 - CRITICAL (blocking) - Wiegers, Adzic, Cockburn

### M4

#### M4.a (round1-b.md F2)
### F2 - MAJOR graded blocking - Fowler, Nygard, Whittaker
**AC-C5, the check that enforces "edits are additive" (SA-1, SA-4), cannot see a deleted bullet line.**

Text: AC-C5 (candidate line 176): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'`, pass condition "prints nothing: edits are additive". SA-4 (line 149) depends on it: "Command-file edits in Phases 1-3 are additive".

Attack (Whittaker, Sequence/Zero attack): the regex `^-[^-]` skips every removed line whose own text starts with `-`. A deleted markdown bullet `- foo` appears in a diff as `-- foo`, and a deleted frontmatter fence `---` appears as `----`. I ran `printf -- '-- removed bullet\n-removed plain\n--- a/file\n-|row\n' | grep -E '^-[^-]'` in the sandbox: it printed only `-removed plain` and `-|row`; the removed bullet and the file header were not printed. Command files are bullet-heavy lists (the command definition under review itself is, for example, the `- **Karl Wiegers**...` lists at its lines 53-66), so the common deletion goes unreported. AC-0.3 (line 193) uses the same regex but guards table rows that start with `|`, which are caught; only AC-C5 is affected.

Grading check: An implementer who follows the stated text as written builds a check that prints nothing for a diff that deletes `- ` lines from a command file, and passes the "additive" phase gate, and X is wrong because the gate is meant to prove standalone behaviour (SA-1) is untouched, and a deleted prompt or flag bullet is exactly a standalone change it must catch.

Origin: the document's own text. (UNVERIFIED that any specific command file would be edited this way; the check's blind spot is shown by the run above and needs no further assumption.)

### M5

#### M5.a (round1-c.md B1)
**B1. WC-4 puts the contract file in a directory the brief cannot name for several commands (CRITICAL, High)**
- Stated text 1, `spec:62` (WC-4): "One report file, known before dispatch ... the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`) ... It is written on success, failure, blocked and partial outcomes, including stops before any other output exists."
- Stated text 2, `spec:90` (tdd, section 3.1): "Brief must pass ... `--output <file>`"; `spec:87` (init-lite): "`--output <file>`"; `spec:200` (AC-2.2): "`/sc:tdd "auth" --unattended --output <file>` ... contract `status: blocked` with a non-empty `blocked_question`".
- Stated text 3, `spec:92` (workflow): report is `.dev/tasks/to-do/<id>/return-contract.yaml`, and the small fix is "Write the contract for pre-creation STOPs too"; `spec:85` (cleanup-audit): "output dir is fixed" with no contract path.
- Grading sentence: An implementer who follows WC-4 as written builds, for `/sc:tdd`, a contract at `<value of --output>/return-contract.yaml`, which is `docs/x/TDD.md/return-contract.yaml`; that cannot be created because the value is a file, so the blocked status in AC-2.2 cannot be written and the check cannot pass. For `/sc:workflow` the path contains a package id the command generates, so it is not "known before dispatch" (WC-4), and a pre-creation STOP has no package directory in which to write it. This follows from the stated texts with no further assumption.
- Wrong outcome: the one mechanism the coordinator relies on to detect a blocked or failed worker (`spec:62`, WC-5 at `spec:63`, step 4 at `spec:183`) has no resolvable location for tdd, init-lite, workflow pre-creation stops and cleanup-audit.

### M6

#### M6.a (round1-c.md B2)
**B2. AC-1.1 cannot pass for `/sc:load` as the spec itself specifies it (CRITICAL, High)**
- Stated text 1, `spec:195` (AC-1.1): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Stated text 2, `spec:112` (load row): report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task"; `spec:159` (P1): "load (usage line only)"; `spec:265`: "a report file would be an unrequested addition".
- Grading sentence: An implementer who follows P1 and the load row adds only the usage-line fix and no contract or `## Unattended mode` section, and then AC-1.1, which includes load in "every command in sections 3.1-3.2", fails; if the implementer instead adds the section to make AC-1.1 pass, it contradicts the load row and Decisions (`spec:265`). Both stated texts cannot hold together.

### M7

#### M7.a (round1-c.md B3)
**B3. P1 and AC-1.1 require unattended sections for the P4 commands, which depend on decisions P1 is said not to need (CRITICAL, High)**
- Stated text 1, `spec:154`: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
- Stated text 2, `spec:159` (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; `spec:195` (AC-1.1) as quoted above. Section 3.2 includes implement (`spec:109`), post-release (`spec:113`) and pr-submit (`spec:114`), all assigned to P4 (`spec:162`).
- Stated text 3, `spec:241`: D3 recommended option (a) "Coordinator or person only ... no pr-submit changes in Phase 4"; `spec:139`: "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
- Grading sentence: An implementer who follows P1/AC-1.1 writes a `## Unattended mode` section for pr-submit, implement and post-release before D2-D4 are answered, and the gate resolutions in those sections (implement's Ruling halt, post-release authorization, pr-submit as worker) are exactly what D2-D4 decide; with the recommended D3 (a) the pr-submit section the check demanded is the "pr-submit change" D3 (a) says does not happen. The stated texts contradict.
