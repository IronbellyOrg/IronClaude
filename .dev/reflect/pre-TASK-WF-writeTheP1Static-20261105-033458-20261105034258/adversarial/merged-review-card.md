# Merged Review Card

verdict: PARTIAL
base: V3 (reviewer 3 card, refactorer, opus)
merge_method: adversarial
counts: total 20; blocking 8 (MF-01..MF-08); minor 12 (MF-09..MF-20)
reviewer_verdicts: V1 FAIL, V2 PARTIAL, V3 PARTIAL
plan_under_review: .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md (cited as `plan:N`)
spec cited as `spec:N`.
Severity scale: blocking = wrong behaviour or a missing required deliverable (every debate "should-fix"); minor = every debate "minor".
Inputs: reviewer-cards/reviewer-{1,2,3}-card.yaml, adversarial/debate-transcript.md (Round 2.5 probe INV-1..INV-6), adversarial/base-selection.md, adversarial/refactor-plan.md.

## Findings

### MF-01
- severity: blocking
- title: graph and impact skills cannot take the new flags or write the worker contract for `--report-dir`
- claim: Both skills have closed flag tables and write the contract only via `--output-dir`; Tasks 4 and 5 edit only the contract-field rows and the Will Not write line. The `--report-dir`-only path is unfulfillable, and nothing says where `impact.md` lands. V1's impact sub-claim (bad flags end blocked) is dropped: `--output-dir` has a default and step 10 always writes.
- evidence: graph `SKILL.md:23-28`, `:64`, `:85`; impact `SKILL.md:19-30`, `:49`, `:182`; `graph.md:42`; `impact.md:45`; `spec:72`; `spec:144-145`; `plan:109`, `plan:111`, `plan:124`, `plan:126`
- sources: R1-01 + R3-03
- plan edit: Task 4 and Task 5. Add `--unattended` and `--report-dir` rows to each skill's flag table; edit graph G-O, the "(only with `--output-dir`)" heading (`SKILL.md:85`) and the Will Not write line (`SKILL.md:158`); edit impact step 10 and the write-scope sentence (`SKILL.md:182`). State where `impact.md` lands under `--report-dir` and that the worker contract at `<report-dir>` lists the command's own contract in `artifacts`. Copy brainstorm's two-case wording. Add a test that each flag table names both flags. No "bad flags blocked" wording.
- provenance: V3 base (R3-03) merged with V1 (R1-01); V1 blocking label dropped

### MF-02
- severity: blocking
- title: graph `init` refusal must be a skill STOP row, not a step after Init
- claim: `graph.md` runs the skill first and the Init steps run only after the skill's preflight returned `init.form`, so a refusal placed after Init fires too late. Only the skill writes the contract, and `refused_reason` has no unattended value.
- evidence: `graph.md:39-53`; `graph.md:40`; `graph.md:46`; `graph.md:48`; graph `SKILL.md:108`; `spec:57`; `spec:72`; `plan:109`
- sources: R1-13
- plan edit: Task 4. Add a STOP row to the graph skill's flag table: positional `init` with `--unattended` gives `status: blocked`, mapped to `worker_status: failed`, reason "init runs only when the user types it". A STOP yields no `init.form`, so the Init steps never run; no change to the command's Init text and no new enum value.
- provenance: added-from-V1 (R1-13); wording per V3 Round 2

### MF-03
- severity: blocking
- title: init-lite shells out to a strict CLI; the plan does not keep the new flags off it or say who writes the contract, including on `--dry-run`
- claim: The skill's preferred path runs `superclaude init-lite` with the resolved flags; the CLI has six click options and `src/superclaude/cli/` is not editable. Task 8 adds the flags to the Inputs table but not to the command's Activation pass-through, and `init-lite.md:94` ("Write anything when `--dry-run` is set") contradicts the contract being written on `--dry-run`.
- evidence: init-lite `SKILL.md:57`; `SKILL.md:25`; `init-lite.md:52`; `init-lite.md:54-58`; `init-lite.md:94`; `cli/init_lite.py:284-317`; `plan:44`; `plan:171`
- sources: R3-02 + R1-02 + R3-09 + probe INV-3
- plan edit: Task 8. Add Activation bullets (added lines only) for `--unattended` and `--report-dir`; state in the skill that both flags are consumed and never forwarded to the CLI and that the skill writes `<report-dir>/return-contract.yaml` after the CLI returns on every outcome including `--dry-run`; add an "except under `--unattended`, the worker contract" line next to `init-lite.md:94`; add a grep acceptance check and an `UNATTENDED_EXPECT` phrase for each.
- provenance: V3 base (R3-02, R3-09) merged with V1 (R1-02) and probe INV-3

### MF-04
- severity: blocking
- title: Task 15's path-list equality fails on files changed before the plan
- claim: The worktree already holds a modified `APPROVED.md` and an untracked `.dev/reflect` folder; neither is under `.dev/tasks/` or `.claude/`, so a correct run fails the equality or lists paths it did not change. `git status --short` also collapses untracked folders and carries status-letter prefixes.
- evidence: `plan:289`; `plan:284`
- sources: R3-01 + R1-05
- plan edit: Task 15. Scope the check to `git status --short --untracked-files=all -- src tests plugins`, comparing paths only, and state the expected groups; or save `git status --short` as a baseline in Task 1 and compare against paths new since it.
- provenance: V3 base (R3-01) merged with V1 (R1-05)

### MF-05
- severity: blocking
- title: Task 14's nested-propagation test has no rule for what "names a nested invocation" means
- claim: Task 14 asserts every command whose section names a nested invocation writes `nested/<command>-<n>/`. Task 9's workflow section names its reflect step, which runs without the flag, so a literal check fails for workflow or the executor invents a rule.
- evidence: `plan:261`; `plan:184`; workflow `SKILL.md:58`; `spec:62`; brainstorm `SKILL.md:273-280`
- sources: R3-04 + R1-03
- plan edit: Task 14 (data field also in Task 1's `UNATTENDED_EXPECT`). Add `UNATTENDED_EXPECT[cmd]["nested"]` listing the nested commands that receive the flag (brainstorm `[analyze, adversarial]`, workflow empty) and assert `nested/<c>-` only for those; workflow's section names reflect as gate-free without `--remediate` and not passed the flag.
- provenance: V3 base (R3-04) merged with V1 (R1-03)

### MF-06
- severity: blocking
- title: brainstorm may write its contract to a suffixed dir, and early STOPs write no contract
- claim: brainstorm creates its output dir with a `-N` suffix when the dir exists and is not empty, so the worker contract can land in a dir the coordinator did not pass. The early STOPs (steps 1-7) end before the contract is written.
- evidence: brainstorm `SKILL.md:105-108`; `SKILL.md:108`; `SKILL.md:95-107`; `SKILL.md:335`; `plan:94`; `plan:96`; transcript probe INV-1
- sources: probe INV-1
- plan edit: Task 3. Under `--unattended` use the passed dir exactly (never suffixed); refuse a dir that already holds a `return-contract.yaml`; every STOP writes a `failed` worker contract.
- provenance: added-from-probe (INV-1, HIGH)

### MF-07
- severity: blocking
- title: `--report-dir` has none of the path rules the commands' own dir flags have
- claim: graph blocks `.git`/`.codegraph` dirs and adversarial has forbidden prefixes, but `--report-dir` has no such rules; the contract location for a rejected or unwritable report dir is undefined (a report dir under `.claude/skills/` would also break `make verify-sync`).
- evidence: graph `SKILL.md:27`; adversarial `SKILL.md:396-398`; `WORKER-CONTRACT.md:14`; `plan:24`; `plan:109`; `plan:124`; transcript probe INV-2
- sources: probe INV-2
- plan edit: Skeleton (`plan:24`) and Tasks 2, 4, 5. `--report-dir` gets the same path rules as the command's own dir flag; a rejected or unwritable report dir counts as "no report dir known", refusal printed in chat only.
- provenance: added-from-probe (INV-2, HIGH)

### MF-08
- severity: blocking
- title: Consent steps left open in commands called "no gate"
- claim: `/sc:test` (via `--fix`), `/sc:analyze` and `/sc:design` keep consent steps that a worker cannot answer, so an unattended run can stall or proceed without consent.
- evidence: `test.md:22`; `test.md:106`; `analyze.md:100`; `design.md:99`; `plan:201`; `plan:214`; transcript probe INV-5
- sources: probe INV-5
- plan edit: Add decision D-P1-12 to the decision list (`plan:43`): consent is never given under `--unattended` (or `--fix` counts as the caller-supplied consent per WC-2 (b)). Task 10 (analyze, design) and Task 11 (test) each state the result in their section.
- provenance: added-from-probe (INV-5, MEDIUM; raised to blocking by the refactor plan)

### MF-09
- severity: minor
- title: brainstorm Wave 0 step 7 stops before the skip rule, its handoff ref still forwards interactive flags, and `-i` and `=` spellings are not refused
- claim: Wave 0 step 7 STOPs when the handoff skill is missing, before the plan's skip rule (Wave 4) runs, and `SKILL.md:385` says "User must choose". `handoff-routing.md` still passes `--output <output>/adversarial/` and forwards `--interactive`; Task 3 does not list it.
- evidence: brainstorm `SKILL.md:105-107`; `SKILL.md:385`; `handoff-routing.md:87-101`; `brainstorm.md:59`; `plan:92`; `plan:96`; transcript probe INV-4 and INV-6
- sources: probe INV-4 + INV-6
- plan edit: Task 3. Skip Wave 0 step 7 under `--unattended` and record the skip; add `handoff-routing.md` to Task 3's Files with an `--unattended` block; refuse `-i` and the `=` spellings.
- provenance: added-from-probe (INV-4, INV-6; probe MEDIUM, edit is small, applied with MF-06)

### MF-10
- severity: minor
- title: The helper reuses Check SCAN's POSIX regex, which Python reads differently
- claim: The regex uses `[[:space:]]` and grep's `-i` flag; Python `re` reads `[[:space:]]` as an ordinary character set, so the Orca check in the Task 1 helper never matches and passes vacuously.
- evidence: `plan:29`; `plan:60`; `pyproject.toml:107-116` (no `filterwarnings = error`, from the transcript)
- sources: R3-10 + R1-04
- plan edit: Task 1. Give the Python form `re.compile(r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I)` and add a negative case that a section containing "orca worktree" makes the helper fail.
- provenance: V3 base (R3-10) merged with V1 (R1-04); V1 should-fix settled at minor

### MF-11
- severity: minor
- title: "Final boundaries heading" disagrees with the tasks for files with two boundaries headings
- claim: `brainstorm.md`, `workflow.md` and `cleanup-audit.md` have `## Boundaries` and a later `## CRITICAL BOUNDARIES`; the skeleton says "final boundaries heading" while Tasks 3, 6 and 9 say "before `## Boundaries`". Both pass the grep criteria, so the guess is silent.
- evidence: `brainstorm.md:145`, `:177`; `workflow.md:63`, `:78`; `cleanup-audit.md:87`, `:101`; `plan:24`; `plan:94`
- sources: R3-08 + R2-03
- plan edit: Skeleton (`plan:24`). Replace "final boundaries heading" with "the first `## Boundaries` heading" (business-panel: `## CRITICAL BOUNDARIES`; index-repo: after `## Output Format`), and make Tasks 3, 6 and 9 agree.
- provenance: V3 base (R3-08) merged with V2 (R2-03); both settled at minor

### MF-12
- severity: minor
- title: Task 6 runs a test that checks the Python pipeline, and the pre-existing file count is off
- claim: `tests/test_cleanup_audit_structure.py` checks `src/superclaude/cli/cleanup_audit`, not the edited Markdown, and is in neither baseline run. Task 15 says the wider run shows all sixteen pre-existing files, but six of them (not seven) are under `tests/skills/`, which the wider run does not include.
- evidence: `tests/test_cleanup_audit_structure.py:17`, `:39`; `plan:147`; `plan:52-53`; `plan:42`; `plan:276`
- sources: R3-06 + R2-04
- plan edit: Task 6. Delete `tests/test_cleanup_audit_structure.py` from the pytest line (`plan:147`). Task 15: read the sixteen files from the combined AC-C3 and wider results, with the count stated as six.
- provenance: V3 base (R3-06, count corrected) merged with V2 (R2-04); V2's weaker fix not used

### MF-13
- severity: minor
- title: D-P1-1 redefines the worker `command` field for graph and impact
- claim: WC-4 says `command` is the exact command line, while existing graph and impact contracts carry the short name; the plan keeps the existing key and lists it in the Task 15 report. The 7.2 step 4 check only requires a non-empty command.
- evidence: `spec:72`; graph `SKILL.md:90`, `:116`; impact `SKILL.md:74`; `plan:43`; `plan:284`
- sources: R1-07 + R2-05
- plan edit: Task 15 and `plan:43`. Reword D-P1-1's lead-in (two readings of WC-4, the plan keeps the existing key); the coordinator ratifies in the Task 15 report. See open owner question D-P1-1.
- provenance: V1 (R1-07) merged with V2 (R2-05); V2 should-fix settled at minor

### MF-14
- severity: minor
- title: The lint comparison does not say whether a new size warning counts
- claim: `make lint` warns (exit 0) for a command file over 200 lines; `adversarial.md` grows in Task 2 and `brainstorm.md` is already over 200. "No new violation" could judge a correct run FAIL.
- evidence: `Makefile:406`; `Makefile:403`; `plan:281`
- sources: R3-05 + R1-12
- plan edit: Task 15 (and wherever the lint comparison is stated, `plan:281`). Define pass as exit 0, no new ERROR and no ruff finding; record new `WARN [Check 3]` lines without failing.
- provenance: V3 base (R3-05) merged with V1 (R1-12)

### MF-15
- severity: minor
- title: adversarial's person-mode refusal names only `--interactive`; the command also has `-i` (and `-o`)
- claim: The Options table lists `--interactive | -i` and `--output | -o`. The flag parse rule counts standalone tokens, so `-i` is a person-mode flag that could slip through, and `-o` could slip past the one-report-directory rule.
- evidence: `adversarial.md:68`; `adversarial.md:69`; `plan:79`
- sources: R1-10
- plan edit: Task 2. Name `-i` and `-o` in the adversarial section and add `-i` to its `UNATTENDED_EXPECT` flags.
- provenance: added-from-V1 (R1-10)

### MF-16
- severity: minor
- title: The `--output` retirement rule also covers the refs Task 9 edits
- claim: `test_output_flag_is_retired_everywhere` checks every line of the workflow command, skill and all five refs, and the parse ref must not contain `E-MISSING-DIR`. Task 9 states the retired/Never rule only for the `workflow.md` section although it adds a Worker flags section to `input-parse.md` and a missing-directory error.
- evidence: `tests/commands/test_workflow_command.py:124`; `tests/commands/test_workflow_command.py:127`
- sources: R3-07
- plan edit: Task 9. Apply the `--output` retired/Never rule to the `SKILL.md` and refs edits too, and forbid naming the new error `E-MISSING-DIR`.
- provenance: kept-from-base (V3 R3-07)

### MF-17
- severity: minor
- title: init-lite's invariant-2 extension is a spec delta decided inside a task body
- claim: The spec's small fix names Safety Invariant 3 only; Task 8 amends Invariants 2 and 3 because the contract is required on `--dry-run`. The extension is necessary but is not in the D-P1 decision list.
- evidence: `spec:147`; init-lite `SKILL.md:62-63`; `plan:169`
- sources: R2-06
- plan edit: Add decision D-P1-11 to the decision list (`plan:43`): the init-lite contract is also written on `--dry-run`, so Safety Invariants 2 and 3 both admit it. Cross-reference from Task 8.
- provenance: added-from-V2 (R2-06)

### MF-18
- severity: minor
- title: Plugin command copies of the converted commands (other than workflow) go stale by design
- claim: No test pins those copies and the plan documents the policy, but the stale set should be visible to the coordinator before the plugin is next built.
- evidence: `plan:23`; `src/superclaude/commands/README.md:9`; `tests/commands/test_routing_plugin_parity.py:43`
- sources: R2-07
- plan edit: Task 15. Add one inventory line to the static report naming the plugin command copies left stale by P1.
- provenance: added-from-V2 (R2-07)

### MF-19
- severity: minor
- title: Task 11's "at most 4 deleted lines" bound breaks if frontmatter trailing spaces are stripped
- claim: The bound is arithmetically right, but `business-panel.md:6` ends in two spaces; stripping them makes a fifth deleted line. The reviewer's "no fix needed" conclusion is rejected.
- evidence: `plan:223`; `business-panel.md:1-11`; `business-panel.md:6` (trailing spaces, per transcript Round 2 V2 advocate)
- sources: R2-01 + calibrator
- plan edit: Task 11 (`plan:223`). Change the criterion to "frontmatter keys and values byte-for-byte unchanged, including trailing spaces on `business-panel.md:6`", keeping the at-most-4-deleted-lines bound.
- provenance: added-from-V2 (R2-01 bound) with the debate/calibrator correction

### MF-20
- severity: minor
- title: `WORKER-CONTRACT.md` brief-flag table stays P0-era after P1
- claim: The table still lists `/sc:index-repo` as "none" and `/sc:init-lite` as `--output <file>`, and `WORKER-CONTRACT.md:184` still says "At P0 no command accepts it". A coordinator following it would omit `--report-dir` and the worker would refuse. The file is outside this plan's files; this is a spec observation, not a plan defect.
- evidence: `WORKER-CONTRACT.md:196`; `WORKER-CONTRACT.md:197`; `WORKER-CONTRACT.md:184`; `plan:22`
- sources: R1-11
- plan edit: None to any task's files (note only). Optionally add one line to the Task 15 spec observations; fix the table in a later phase.
- provenance: note-only (V1 R1-11)

## Rejected or not merged

- R1-06: the downgrade of brainstorm nesting; `spec:142` says "from P2" but the plan discloses D-P1-4. Left as an owner question (below).
- R1-09: unconfirmed (the coverage matrix was not read).
- R1-01's impact sub-claim: wrong, `--output-dir` has a default at impact `SKILL.md:29` and step 10 always writes.
- R2-01's "no fix needed" conclusion.
- R3-06's "seven" count (the count is six).
- R3-08 as should-fix (stays minor).
- The "bad flags blocked" wording in the graph and impact tables (no STOP column lists an unknown-flag stop).

## Open owner questions

- D-P1-1, command-key collision for graph and impact: WC-4 says `command` is the exact command line (`spec:72`), while the existing graph and impact contracts carry the short name (graph `SKILL.md:90`, impact `SKILL.md:74`). The plan keeps the short name (`plan:43`). Owner or coordinator to ratify (see MF-13).
- D-P1-4, brainstorm nested scope: `spec:142` says brainstorm passes `--unattended` and a nested report directory "from P2"; the plan passes the flag to nested analyze and adversarial in P1 (brainstorm `SKILL.md:273-280`). Disclosed as D-P1-4 and in the Task 15 report; owner to confirm (R1-06 was not merged).
