# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3

Task 5 (independent review). Command run: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`. Planning only. The spec was not edited, and the Improve step (step 6) was not run because the brief forbids editing the spec.

## Citation keys and review limits
- `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.
- `SPCMD:N` = line N of the `/sc:spec-panel` definition supplied with this run (`command.md` in the sandbox root, outside the workspace). It is used for the Review Loop rules and as one piece of evidence about command text.
- The sandbox holds only the spec, the README and the three inventories. Citations to `src/`, `~/.claude`, `CLAUDE.md`, `.dev/evals/...`, `.dev/codegraph-migration/...` and Orca output are UNVERIFIED by this review unless the inventories quote them. The inventories were read in full.
- Unattended mode (`SPCMD:451-461`) does not apply: no `--unattended` argument was passed, so no `return-contract.yaml` is written. `--re-review` and `--baseline` were not passed, so this is a first review of the full document. `~/.claude/WORKER-CONTRACT.md` does not exist in the sandbox home.
- Citation spot check: about 70 `INV-A`, `INV-B` and `CAPS` citations in the spec were compared with the inventory lines they point to, including the per-command evidence cells for all 43 commands, the section 4 rows and the UNVERIFIED cross-references. No wrong line was found. The 10 / 27 / 6 split adds to 43, and the 3.1 and 3.2 rows plus the section 3 phase tags add to 37 worker-capable commands.

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  mode: critique
  focus_areas: [requirements, architecture]
  expert_panel: [Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker, Newman, Hohpe, Crispin (guard-table completeness)]
  review: 1 of 3
quality_assessment:
  overall_score: 5.5
  clarity: 6
  completeness: 6
  testability: 5
  consistency: 5
critical_issues:
  # one line per blocking finding; detail in the buckets below, canonical list in "Numbered findings list"
  - {id: F-01, severity: MAJOR, expert: Wiegers, issue: "WC-4 output location has three spellings and mixed file/dir semantics", recommendation: "fix one directory flag, distinct from file-valued --output"}
  - {id: F-02, severity: MAJOR, expert: Nygard, issue: "No behavior for missing/unusable report location; WC-4 'known before dispatch' conflicts with WC-6 'fresh dir'", recommendation: "coordinator supplies a new dir per attempt; define the no-dir refusal"}
  - {id: F-03, severity: CRITICAL, expert: Fowler, issue: "P1 flag and AC-1.1 cover 37 commands; only 15 are converted in P1", recommendation: "accept --unattended per command only in its own phase"}
  - {id: F-04, severity: MAJOR, expert: Crispin, issue: "AC-C1 contradicts P0 deliverables and is vacuous as written", recommendation: "rescope and fix the grep"}
  - {id: F-05, severity: MAJOR, expert: Newman, issue: "Fixed status vocabulary never checked against existing contracts; empty report undefined", recommendation: "inventory existing statuses; add validity rule"}
  - {id: F-06, severity: MAJOR, expert: Nygard, issue: "WC-3 ask protocol: 'once' undefined, no answer channel, no silence/decline rule", recommendation: "per-gate rule, answer flags, max wait"}
  - {id: F-07, severity: MAJOR, expert: Nygard, issue: "WC-10 leaves a 4-5 minute hole and does not cover Monitor-driven waits", recommendation: "cap every call at 4 minutes; define Monitor heartbeat"}
  - {id: F-08, severity: MAJOR, expert: Whittaker, issue: "WC-9 authorization has no mechanism for task commit/push or flag conflicts", recommendation: "name the flag or drop the claim"}
expert_consensus:
  - "The decision (Orca on top, commands as units of work) is well evidenced and the evidence gaps are stated honestly (SPEC:41-45)."
  - "Counts and cross-references are accurate: 43 = 10 + 27 + 6, and every worker-capable command is tagged to one phase."
  - "The contract is not yet implementable uniformly: output location, status vocabulary, retry directory and the phase/flag scope are inconsistent between sections."
  - "Several requirements have no acceptance check (F-09), and one check cannot pass (F-04)."
improvement_roadmap:
  immediate: [F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08]
  short_term: [F-09, F-10, F-11, F-12, F-13]
  long_term: [F-14, F-15, F-16, F-17, F-18, F-19, F-20, F-21, F-22]
adversarial_analysis: "see === ADVERSARIAL ANALYSIS (Whittaker) ==="
```

## Panel and method
Review order followed `SPCMD:101-113` for the experts active under `--focus requirements,architecture` (`SPCMD:131-148`) plus Whittaker (active in every panel, `SPCMD:84`) and Crispin for guard-table completeness (`SPCMD:311`). Wiegers, Adzic and Cockburn took the requirements pass, Fowler, Nygard, Newman and Hohpe the architecture pass. Whittaker attacked the guards and the phase pipeline. Severity grading follows the Review Loop (`SPCMD:259`): CRITICAL and FR-8/FR-9 findings are blocking, MINOR is minor, and a MAJOR is blocking only when it names a concrete wrong outcome an implementer would produce. Severity labels are kept as the experts assigned them; the `Blocking` column in the numbered list gives the graded result. `--focus correctness` is not active, so no State Variable Registry is produced. The Guard Condition Boundary Table and Quantity Flow Diagram are produced because the spec contains threshold guards and a multi-stage count-changing flow.

## Mandatory output artifacts
These were completed before the synthesis sections below (hard gate FR-10, `SPCMD:330`).

### Guard Condition Boundary Table
Triggered: the spec contains threshold guards, flag-state guards and a status mapping (`SPCMD:309`). Construction: Nygard; completeness check: Crispin; attack on entries: Whittaker. Guards covered are the ones in section 2 whose value or flag state decides behavior: G1 `WC-10` wait size, G2 `WC-4/WC-5` report validity and outcome mapping, G3 `WC-3` ask gate, G4 `WC-4` report location, G5 `WC-9` outward-action default, G6 `WC-1` startup fallback. The section 6 phase gate is treated in the Quantity Flow Diagram and F-03. Guard G3 has a seventh row because the typical case splits in two. Every cell is populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 single-call wait > 5 min must split to <= 4 min | SPEC:68 | Zero/Empty | wait = 0 s (no blocking step) | false | No splitting needed; no requirement applies | OK |
| G1 | SPEC:68 | One/Minimal | wait = 1 s | false | No splitting needed | OK |
| G1 | SPEC:68 | Typical | single call of 3 min | false | Allowed; worker heartbeat cadence of 5 min applies (CAPS:130) | OK |
| G1 | SPEC:68, SPEC:104 | Maximum/Overflow | one eval of 3600 s (INV-A:65) | true | Split into waits of at most 4 min | OK |
| G1 | SPEC:68 | Sentinel Value Match | single call of 4 min 30 s (above the 4 min cap, below the 5 min trigger) | neither clause applies | Not specified. A call that starts 2 min after a heartbeat leaves 6.5 min between heartbeats | GAP |
| G1 | SPEC:68, SPEC:104 | Legitimate Edge Case | wait is a background Bash job watched by Monitor, so there is no single blocking call (INV-A:44) | not evaluable | Not specified how an idle, Monitor-driven turn sends heartbeats | GAP |
| G2 report validity and outcome mapping | SPEC:62-63, SPEC:183 | Zero/Empty | report file present with 0 bytes | n/a | WC-5 covers "no report exists" only; empty or unparseable file not specified | GAP |
| G2 | SPEC:62-63 | One/Minimal | report with only `status: failed` and `command` | valid | `--outcome failed` | OK |
| G2 | SPEC:63 | Typical | `status: succeeded` | valid | `--outcome succeeded` | OK |
| G2 | SPEC:63, SPEC:263 | Maximum/Overflow | `status: partial` | valid | `--outcome succeeded`; first sentence names `partial` | OK |
| G2 | SPEC:62, SPEC:262 | Sentinel Value Match | `status` is outside the four values (a legacy value in an existing contract) or absent | not in set | Not specified; step 4 assertion fails and WC-5 is silent | GAP |
| G2 | SPEC:63 | Legitimate Edge Case | audit report with `status: succeeded` and verdict FAIL | valid | `--outcome succeeded`; verdict stated in the first sentence | OK |
| G3 ask once, then resume with the answer as a flag | SPEC:61 | Zero/Empty | no preamble (a person passes `--unattended` in a plain session) | false | Gate resolves as blocked; no ask (SPEC:50, SPEC:60 (c)) | OK |
| G3 | SPEC:61 | One/Minimal | one gate hit, preamble present | true | Ask once, wait, resume with the answer | OK |
| G3 | SPEC:61, SPEC:120 | Typical | coordinator answers; the command has a flag for the answer (`target_release`, `--suite`) | true | Re-invoke with the answer as a flag | OK |
| G3 | SPEC:61, SPEC:90, SPEC:115, SPEC:117 | Typical (no answer flag) | gate with no named flag: tdd topic clarification, recommend question, review-translation Phase 1 | true | Not specified how the answer reaches the command | GAP |
| G3 | SPEC:61, SPEC:104-105 | Maximum/Overflow | three gates in one run (cli-portify) or several (cli-eval) | "once" is ambiguous | Not specified whether "once" is per gate or per run | GAP |
| G3 | SPEC:61, CAPS:60 | Sentinel Value Match | `ask` times out, question still pending | true | Resume the same message ID; no duplicate | OK |
| G3 | SPEC:61, CAPS:68 | Legitimate Edge Case | coordinator never replies, or replies "no" | unknown | Not specified: no maximum wait, no decline path, no exit rule | GAP |
| G4 report location known before dispatch | SPEC:62, SPEC:73 | Zero/Empty | `--unattended` with no report location | false | Not specified. WC-4 says the contract is written on every outcome, including stops before output exists, which is impossible with no location. The supplied command definition refuses before any work, in chat only (SPCMD:456) | GAP |
| G4 | SPEC:62 | One/Minimal | existing empty directory | true | Write the contract there | OK |
| G4 | SPEC:62 | Typical | directory given, creatable | true | Write the contract there | OK |
| G4 | SPEC:62 | Maximum/Overflow | directory unwritable, inside `.git/` or `.codegraph/`, or a git-ignored path (SPCMD:456-457) | true | Not specified | GAP |
| G4 | SPEC:62, SPEC:87, SPEC:90 | Sentinel Value Match | `--output` is file-valued (tdd, init-lite) but WC-4 reads it as `<output-dir>` | collision | Not specified which path receives `return-contract.yaml` | GAP |
| G4 | SPEC:62, SPEC:64, CAPS:116 | Legitimate Edge Case | retry worker (`--retry-of`) given the same directory, which holds the first attempt's contract | true | Not specified: WC-6 wants a fresh directory, WC-4 fixes the path before dispatch | GAP |
| G5 outward actions off unless explicitly authorized | SPEC:67 | Zero/Empty | no authorization flags | false | Every outward default off | OK |
| G5 | SPEC:67, SPEC:100 | One/Minimal | one explicit flag (`--post-pr`) | true | That action only | OK |
| G5 | SPEC:245 | Typical | brief quotes the user's instruction and passes the flag | true | Action allowed (D4 (a)) | OK |
| G5 | SPEC:113, SPEC:245 | Maximum/Overflow | several actions in one brief (post-release VM, install, commit, PR) | true | Deferred to D4 and P4; decision recorded | OK |
| G5 | SPEC:100, INV-A:38 | Sentinel Value Match | brief carries both `--post-pr` and the existing `--no-post-pr` | conflict | Not specified which wins | GAP |
| G5 | SPEC:67, SPEC:121, INV-B:204 | Legitimate Edge Case | outward action with no flag today: `/sc:task` EXEMPT `commit` and `push` | true | WC-9 needs "the command's own explicit flag"; none exists and none is named | GAP |
| G6 startup fallback inside the readiness limit | SPEC:59 | Zero/Empty | no prompt before the input box | false | Nothing to do | OK |
| G6 | SPEC:59 | One/Minimal | fallback after 1 s | true | Passes | OK |
| G6 | SPEC:59, CAPS:49 | Typical | fallback after 30 s | true | Passes (EVIDENCE.md:45 as quoted at CAPS:49) | OK |
| G6 | SPEC:59, CAPS:49 | Maximum/Overflow | fallback after 45 s or more | true | "Well inside" the limit; evidence says about 45 s fails (EVIDENCE.md:56 as quoted at CAPS:49). Unquantified, see F-19 | OK |
| G6 | SPEC:59 | Sentinel Value Match | fallback exactly equal to the 60 s limit | true | Excluded by "well inside" | OK |
| G6 | SPEC:59, CAPS:45 | Legitimate Edge Case | coordinator raises `--timeout-ms` for one start | true | Limit moves; the rule is stated against the default 60 s | OK |

GAP entries (priority invariant candidates for AD-1): G1 rows 5-6, G2 rows 1 and 5, G3 typical (no answer flag), maximum and edge, G4 rows 1, 4, 5 and 6, G5 sentinel and edge. By FR-8 each GAP row is at least MAJOR; they are folded into F-07, F-05, F-06, F-02/F-01 and F-08 respectively.

### Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)
Triggered: the spec describes a multi-stage flow whose count changes (classification, phase assignment, acceptance). Fowler annotated the counts; Whittaker attacked the divergence point. Counts come from `SPEC:76-78`, the 3.1 and 3.2 tables, and the phase table at `SPEC:158-162`.

```text
[Source: 43 commands in cmd/ (SPEC:76)]
   --> [Stage 1: classify (SPEC:76-139)]
        --> [6 coordinator-only (SPEC:128)]                         excluded from every phase and from AC-1.1's section check
        --> [37 worker-capable = 10 ready (3.1) + 27 change (3.2)]
              |
              v
        [Stage 2: phase assignment (SPEC:158-162)]
              P1 names 13  (9 no-gate commands + 4 fixes: adversarial, cleanup-audit, index-repo, workflow)
              P2 names 15  (11 from 3.2 + reflect, release-split, tdd, troubleshoot)
              P3 names  4  (roadmap, validate-roadmap, validate-tests, save)
              P4 names  3  (implement, post-release, pr-submit)
              named total 35; brainstorm and init-lite appear only in the blanket P1 sentence (SPEC:159)
              fully converted when P1 ends: 13 + 2 = 15 ; flag accepted but gates still open: 37 - 15 = 22
              |
              +--> [Consumer A: P1 scope "flag accepted by every command in 3.1 and 3.2": expects 37]      <-- MISMATCH (15 converted)
              +--> [Consumer B: AC-1.1 asserts a "## Unattended mode" section in all 37 (SPEC:195)]         <-- MISMATCH (15 converted; load has no contract; 3 commands wait for D2-D4)
              +--> [Consumer C: AC-1.2 live check "each P1 command" (SPEC:196): expects 15]                  OK
              +--> [Consumer D: P4 gate "waits for D2-D4" (SPEC:154): expects 3 of the 37 held back]         <-- MISMATCH with Consumers A and B
```

Divergence at Stage 2 (37 in, 15 converted out). Concrete scenario: after P1 passes, 22 commands accept `--unattended` but still hold their gates (for example `/sc:tdd "auth" --unattended` still asks the user to clarify a bare topic until P2). A coordinator that builds its brief from the P0 template and passes `--unattended` to every worker-capable command stalls those 22 workers silently, which is the failure WC-2 exists to prevent. Under FR-19 this mismatch is CRITICAL (F-03).

## Findings by analysis bucket
Each finding gives: issue, severity, expert, recommendation with rationale, priority, quality-impact. Evidence paths are repeated in the numbered findings list.

=== REQUIREMENTS ANALYSIS ===

**F-01 (MAJOR, blocking). Karl Wiegers: the report location has three spellings and mixed file/directory meaning.**
- Issue: WC-4 defines `<output-dir>` as the directory the coordinator passed, "`--output` / `--output-dir`" (SPEC:62), and puts `return-contract.yaml` in it. But `--output` is file-valued for tdd and init-lite (SPEC:87, SPEC:90), is given no value type in the spec-panel row ("add `--output`", SPEC:120), and is directory-valued for adversarial and brainstorm (SPEC:83-84). AC-1.2 passes `--output <dir>` to every P1 command (SPEC:196) and AC-0.4 passes it to adversarial (SPEC:194). The supplied `/sc:spec-panel` definition uses a third form: `--output <file>` plus `--report-dir <dir>`, with the contract at `<report-dir>/return-contract.yaml` (SPCMD:22-23, SPCMD:456-457). It also cites "(WC-4)" for a rule that git-ignored paths are left out of `artifacts` (SPCMD:457), and that rule is not in SPEC:62. Whether the repo's commands already carry that text is UNVERIFIED, since `src/` is not in the sandbox.
- Wrong outcome an implementer would produce: applying WC-4 to `/sc:tdd` puts the contract at `<TDD file>/return-contract.yaml`, or invents a new flag; 37 commands each pick their own spelling, so the P0 brief template (SPEC:158) cannot be uniform, and AC-1.2 hands a directory to a file-valued flag.
- Recommendation: fix one directory flag name for the contract location, distinct from file-valued `--output`, state it in WC-4, in section 2.3 and in every AC, and list it per command in section 3. Rationale: the coordinator needs one predictable brief shape (Wiegers: unambiguous, consistent requirement).
- Priority: High. Quality impact: Consistency +2, Testability +1.

**F-04 (MAJOR, blocking). Lisa Crispin / Karl Wiegers: AC-C1 cannot pass as designed and is vacuous as written.**
- Issue: AC-C1 greps `src/superclaude/core` and excludes only `ccsession-tag` (SPEC:172) and requires no output. P0 adds `src/superclaude/core/WORKER-CONTRACT.md` and an Orca section in `src/superclaude/core/HOW-WE-WORK.md` (SPEC:158, SPEC:150), and SA-2 itself allows an Orca mention in the contract file (SPEC:147). Any `orca orchestration ...` text in either file fails the "prints nothing" condition. Separately, the command as written in the file uses `\|` inside `grep -E`, which is a literal pipe in an ERE. I ran it in the sandbox: on lines `orca-ide orchestration worker-start` and `orca worktree create` it printed nothing (exit 1) as written, and matched both when unescaped. Neither form matches the spec's own placeholder `ORCA orchestration ...` (SPEC:167), and the verbs list omits `status`, `open` and `skills`, and does not name the `worker-start`, `dispatch` and `task-create` calls WC-8 forbids (SPEC:66).
- Wrong outcome: P0 cannot pass, or the implementer leaves the Orca section out of the routing guide to satisfy the check, or the check is run vacuously and SA-2/WC-8 are never tested.
- Recommendation: scope AC-C1 to `commands/`, `skills/` and `agents/` (with the `ccsession-tag` exclusion), allow-list the two core documents explicitly, write the pattern unescaped, case-insensitive and keyed on the WC-8 verbs.
- Priority: High. Quality impact: Testability +2.

**F-09 (MAJOR, not blocking). Wiegers: eight requirements have no acceptance check, or only a weak one.**
- Traceability matrix against SPEC:172-210: WC-1 (only the implicit `state: ready` in step 1), WC-3 (none; the ask/resume path is never exercised), WC-6 (none; no retry run), WC-8 (AC-C1 only, see F-04), WC-10 (AC-4.3 covers pr-submit only; cli-eval's wait splitting in P2, SPEC:104, has none), WC-11 (AC-3.4 covers save only), WC-12 (none), WC-7 (AC-0.4, three commands in P0 only).
- Recommendation: add one check per row of that list, or state that the requirement is verified by inspection. Priority: Medium. Quality impact: Testability +1.

**F-12 (MAJOR, not blocking). Wiegers: `partial` is undefined and a FAIL-verdict run settles as success.**
- Issue: WC-5 maps `partial` and an audit with verdict FAIL to `--outcome succeeded` (SPEC:63, SPEC:263). Orca then completes the Task, and a Task with `--deps` on it appears in `task-list --ready` (CAPS:84-92). No command is said to emit `partial`, and no rule says when. A coordinator DAG therefore cannot express "implement only if the review passed". Section 2.3 has the coordinator open the report after `worker_done` (SPEC:73) but does not require checking `status` and the verdict before starting dependents.
- Recommendation: list which commands may emit `partial` and what makes a deliverable usable, and add to section 2.3 that the coordinator reads `status` and the verdict before starting any dependent Task. Priority: Medium.

**F-14 (MINOR). Alistair Cockburn: the invocation step is missing from the actor-goal flow.**
- Issue: the brief carries "the exact command line" (SPEC:73) and the worker runs it "directly" (SPEC:65), but nothing says how a worker session runs a `/sc:` command. A worker's first message is the Orca preamble plus the brief (CAPS:47: the task is passed as an argument), not a typed slash command. The project instructions require the Skill tool to be invoked for `/sc:` commands (project `CLAUDE.md`, not in the sandbox; UNVERIFIED line) and the earlier run used `skill-direct` (SPEC:23). AC-0.4 would catch a wrong choice, but only for three commands.
- Recommendation: add one sentence and one example to the brief template: invoke through the Skill tool `sc:<name>` with the arguments. Priority: Medium.

**F-17 (MINOR). Wiegers: a rule for this planning run is cited as product rationale.**
- Issue: SPEC:67 (WC-9) and SPEC:133 (`/sc:git` coordinator-only) cite `README:31`, which reads "No git commits, pushes, PRs or GitHub comments" and belongs to the worker rules of this planning run (README:29-38). INV-A:49 and INV-A:91 make the same move. It is not evidence about how a product worker should behave.
- Recommendation: rest both on the command text (`cmd/git.md:14-17,90`, `cmd/auggie-review.md:51-54` as cited at SPEC:67, SPEC:133) and drop `README:31`. Priority: Low.

**F-19 (MINOR). Wiegers: "well inside the readiness limit" is not measurable.**
- Issue: WC-1 (SPEC:59) says a startup prompt must fall back "well inside" the 60 s limit, while its own evidence gives numbers: a 30 s fallback passed and about 45 s failed (EVIDENCE.md:45,56 as quoted at CAPS:49).
- Recommendation: state the number, for example "at most 30 s". Priority: Low.

**F-20 (MINOR). Cockburn: effort is scheduled for two commands the spec says not to dispatch.**
- Issue: section 4 says `/sc:load` and `/sc:recommend` are better used on the coordinator side (SPEC:139), yet both sit in the 27 "needs a change" commands (SPEC:112, SPEC:115), get phase work (load P1 usage line, recommend P2 gate and file output), and count in AC-1.1's 37. `/sc:load` has "Report: none" (SPEC:112), so AC-1.1's requirement that its section names `return-contract.yaml` (SPEC:195) cannot hold.
- Recommendation: move both to a "coordinator-side helper" list outside the 37, or drop the contract requirement for them. Priority: Low.

**F-21 (MINOR). Wiegers: "Phases 1-3 need no user decision" contradicts D1.**
- Issue: SPEC:154 says phases 1-3 need no user decision, and SPEC:225 says phases 0-3 proceed on the recommendations, but D1 (flag versus Orca detection, SPEC:227-230) decides the mechanism P1 builds. The spec does say it is written for the recommended flag (SPEC:51).
- Recommendation: say that P1 assumes D1 (a) and is rework if the user picks (b). Priority: Low.

**F-22 (MINOR). Gojko Adzic: no worked example of the contract or the brief.**
- Issue: WC-4 lists the contract fields in prose (SPEC:62) and 2.3 lists the brief contents (SPEC:73), but there is no example `return-contract.yaml` and no example brief. Only D1 has an example command line (SPEC:228). The 37 command changes are therefore not anchored by a concrete Given/When/Then.
- Recommendation: add one blocked and one succeeded example contract and one complete brief for a P0 smoke command. Priority: Medium.

=== ARCHITECTURE ANALYSIS ===

**F-03 (CRITICAL, blocking; FR-19 dimensional mismatch). Martin Fowler: P1 asks for the flag and the section on 37 commands, but only 15 are converted in P1.**
- Issue: the P1 row says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (SPEC:159). AC-1.1 asserts a `## Unattended mode` section in every command of sections 3.1-3.2 (SPEC:195). That is 37 commands. The phase table names gate conversion for 22 of them in P2 (15), P3 (4) and P4 (3) (SPEC:160-162), and P4 explicitly "waits for D2-D4" (SPEC:154). See the Quantity Flow Diagram above: 37 enter, 15 are converted.
- Concrete scenario: P1 passes. `/sc:tdd "auth" --unattended` is accepted, and the topic-only clarification (SPEC:90) is still live because the gate resolution is a P2 change. The worker waits for a person, which is the silent stall WC-2 forbids and 7.2 step 2 is meant to catch. The same holds for `/sc:implement`, `/sc:post-release` and `/sc:pr-submit`, whose design waits on user decisions D2-D4 (SPEC:225), so AC-1.1 cannot pass in P1 without implementing undecided P4 designs.
- Recommendation: a command accepts `--unattended` only in the phase that converts its gates; AC-1.1 checks the P1 list only, and each later phase checks its own list; the P0 brief template states which commands may take `--unattended` before which phase. Rationale: keeps "each phase independently useful" (SPEC:154) true.
- Priority: High. Quality impact: Consistency +2, Testability +1.

**F-02 (MAJOR, blocking; FR-8 from guard G4). Michael Nygard: no behavior when the report location is missing or unusable, and WC-4 conflicts with WC-6.**
- Issue: WC-4 says the contract "is written on success, failure, blocked and partial outcomes, including stops before any other output exists" and that the path is "known before dispatch" (SPEC:62). It does not say what happens under `--unattended` with no location, or with an unwritable or git-controlled one (the supplied command definition refuses before any work and prints the refusal in chat only, SPCMD:456). WC-6 says a command without a resume flag "writes each run into a fresh output directory" (SPEC:64), and 19 rows say "fresh dir" (3 in section 3.1 and 16 in section 3.2, for example SPEC:99-101, SPEC:103-104, SPEC:106-108, SPEC:110-111, SPEC:120-123). A fixed pre-dispatch path and a fresh directory per run cannot both hold unless the coordinator supplies a new directory per attempt, and section 2.3 (SPEC:73) does not say so.
- Concrete scenario: attempt 1 writes `<D>/return-contract.yaml` with `status: failed`. The coordinator retries with `worker-start --retry-of` and the same brief (CAPS:116), so `<D>` is unchanged. The command either overwrites the first attempt (violating WC-6) or creates `<D>/<fresh>/` (then the path is not the one the coordinator knew before dispatch, violating WC-4).
- Recommendation: add to 2.3 that the coordinator passes a new directory for every attempt including retries; state the no-location refusal and the unusable-location rule in WC-4. Priority: High.

**F-05 (MAJOR, blocking; FR-8 from guard G2). Sam Newman: the fixed status vocabulary was never checked against the contracts that already exist.**
- Issue: WC-4 fixes `status` to `succeeded|partial|failed|blocked` and says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62); the Decisions row chooses the fixed set over each command's own statuses (SPEC:262). The existing writers are workflow (contract 1.1, INV-B:272), reflect (INV-B:112), brainstorm (INV-A:39), adversarial (INV-A:35, INV-A:60) and, for `--caller task-unified`, troubleshoot (INV-B:242). Their `status` values are not listed anywhere in the spec or the inventories; the spec re-read only their locations (SPEC:11). Step 4 of 7.2 asserts the four values for every command (SPEC:183).
- Concrete scenario: if workflow or adversarial emits a different value, the live check fails; renaming it breaks the commands that consume those contracts (adversarial's contract is "returned when invoked by another command", INV-A:60), contrary to SA-1 and SA-4 (SPEC:146, SPEC:149). Which vocabularies exist is UNVERIFIED (sources not in the sandbox). Also unspecified: a report file that exists but is empty or does not parse (guard G2 row 1); WC-5 covers only "no report exists" (SPEC:63).
- Recommendation: add a short inventory of existing `status` vocabularies and either map them or add a separate `worker_status` field; add a rule for empty or unparseable reports (treated as no report, outcome failed). Priority: High.

**F-06 (MAJOR, blocking; FR-8 from guard G3). Nygard: the WC-3 ask protocol is not complete.**
- Issue: WC-3 lets the worker "ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (SPEC:61). Three holes: (1) "once" is undefined for commands with several gates (cli-portify has three, cli-eval several, SPEC:104-105); (2) the answer-as-flag exists for few gates: `target_release` (SPEC:120) and `--suite` (SPEC:104), but the tdd topic clarification (SPEC:90), the recommend question (SPEC:115) and review-translation Phase 1 (SPEC:117) name no flag or input, so the re-invocation has nothing to carry the answer; (3) no maximum wait, no decline path and no exit rule if the coordinator never answers or says no (the `ask` timeout leaves the question pending and is resumed by ID, CAPS:60; the default timeout is UNVERIFIED, CAPS:68).
- Recommendation: define the rule per gate, add an `--answer`-style input for gates without a flag, and set a limit after which the worker resolves as blocked. Priority: High.

**F-07 (MAJOR, blocking; FR-8 from guard G1). Nygard: WC-10 leaves a hole between 4 and 5 minutes and does not cover Monitor-driven waits.**
- Issue: the rule splits a call "longer than 5 minutes" into waits "of at most 4 minutes" (SPEC:68). A single call of 4 min 30 s triggers neither the split nor a heartbeat, and the liveness requirement is cumulative since the last heartbeat, not per call. The cli-eval run waits through a background Bash job and Monitor (INV-A:44, INV-A:65), so there is no single blocking call to split, and the spec only says "split the eval wait into waits of at most 4 minutes" (SPEC:104).
- Concrete scenario: heartbeat at t=0, two minutes of work, then a 4.5 minute call: 6.5 minutes since the last heartbeat with the rule satisfied.
- Recommendation: "No single tool call may last longer than 4 minutes" (applies to every call), and one sentence on how a Monitor-driven wait heartbeats. Priority: High.

**F-10 (MAJOR, not blocking). Fowler / Gregor Hohpe: no general rule for nested invocations or for contract file collisions.**
- Issue: the only propagation rule is tasklist to reflect (SPEC:122). Other nests exist: brainstorm to adversarial (INV-A:39), release-split to brainstorm to adversarial (INV-B:119), tdd to task (INV-B:219), task to troubleshoot (INV-B:201), pr-submit to troubleshoot (INV-B:91), workflow to reflect (INV-B:271). The supplied command definition has a per-command "Nested invocations" line (SPCMD:460), which suggests the contract should ask every command to state this. Several of these children write `<output>/return-contract.yaml` themselves (reflect INV-B:112, brainstorm INV-A:39), so a child that inherits the parent's `<output-dir>` overwrites the parent's contract. This is UNVERIFIED because the skill sources are not in the sandbox.
- Recommendation: a WC row: a command passes `--unattended` to every nested command it invokes and gives each child its own subdirectory. Priority: Medium.

**F-11 (MAJOR, not blocking). Nygard: the coordinator side of failure handling is missing.**
- Issue: the spec says a stalled command prompt is invisible to the coordinator (SPEC:60) and that the coordinator sees it only through `worker-show`'s `agentWait` or a missing report (SPEC:44). Section 2.3 (SPEC:73) and 7.2 (SPEC:180-186) give a test procedure but no production rule: how often to poll, what to do when `agentWait` is non-null, how long to wait for a missing report, or what to do on a silent worker. Orca's own guidance allows leaving the wait only on positive proof (CAPS:126, CAPS:125), and whether Orca bounds total Dispatch time is UNVERIFIED (SPEC:282).
- Recommendation: add a short coordinator procedure to 2.3 that points to Orca's recovery guide and states the maximum wait the brief gives a worker. Priority: Medium.

**F-13 (MAJOR, not blocking). Fowler: WC-11 conflicts with fixed output paths, and the worktree choice is left implicit.**
- Issue: WC-11 says default output paths carry a timestamp or slug (SPEC:69), but the 3.1 "ready" commands keep fixed outputs: index-repo `PROJECT_INDEX.md` with only "state the output location" as the fix (SPEC:86), cleanup-audit `.claude-audit/` (SPEC:85, acknowledged as one audit per worktree). The need for WC-11 comes from workers sharing a worktree by default (SPEC:69, CAPS:115), while the project instructions say parallel sessions each use their own Orca worktree (project `CLAUDE.md`, section on parallel worktrees; not in the sandbox, UNVERIFIED line). Section 2.3 lists "the worktree placement" without a rule (SPEC:73).
- Recommendation: state in 2.3 when the brief must request a separate worktree, and give index-repo an output parameter or add it to the single-owner list. Priority: Medium.

**F-15 (MINOR). Hohpe: worker-written files are consumed without a trust statement.**
- Issue: the coordinator reads `blocked_question`, the report and the summary body, all produced by a worker that has read PR text, web pages and repo files (auggie-review, research, review-translation; SPEC:100, SPEC:116-117). The spec does not say that this content is data, not instructions, and that a relayed question goes to the person unchanged.
- Recommendation: one sentence in 2.3. Priority: Medium.

**F-16 (MINOR). Newman / Hohpe: contract versioning, write ordering and a name collision.**
- Issue: WC-4 has no `contract_version` field although workflow's contract is already versioned (1.1, INV-B:272); mixed installs of commands and `WORKER-CONTRACT.md` are possible (the contract file is installed separately, SPEC:52). It does not require that the file is written completely (temporary file then rename) before `worker_done` carries its path. The contract `status: blocked` also reuses a word Orca uses for a Task status (`blocked`, CAPS:89), which invites confusion in coordinator logic.
- Recommendation: add `contract_version`, an atomic-write rule and an ordering rule. Priority: Low.

**F-18 (MINOR). Fowler / Newman: three statements are stronger than their evidence.**
- (a) The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122, citing INV-A:14, a docs fetch), while INV-B:210 and INV-B:314 mark nested spawning of agents UNVERIFIED.
- (b) Section 1.4 (2) states that a command prompt "does not fail `worker-start`" (SPEC:44), but the task reaches Claude as a launch argument (CAPS:47) and the only evidence is a plain launch (EVIDENCE.md:45 as quoted at CAPS:49), so whether readiness completes while a turn is already running is UNVERIFIED.
- (c) E3 cites `invocation_method: "skill-direct"` as evidence the approach worked (SPEC:23), and section 1.4 (1) says that run proved only the Agent-tool route (SPEC:43). The two readings of one record are not reconciled; P0 resolves it.
- Recommendation: mark (a) and (b) UNVERIFIED in place and reconcile (c) in one sentence. Priority: Low.

=== ADVERSARIAL ANALYSIS (James Whittaker) ===
Severity classes: CRITICAL (provably wrong), MAJOR (ambiguous or incomplete under attack), MINOR (inferrable). Each attack is tied to a finding.

**A-1 (F-08, MAJOR, blocking). I can break this specification by Zero/Empty and Sentinel Collision attacks on WC-9.** The invariant at **WC-9 (SPEC:67) and the task row (SPEC:121)** fails when **an outward action has no flag to authorize it, or two flags conflict**. Concrete attack: **before: the brief for a task worker says `/sc:task "commit the fix" --unattended`; `commit` is an EXEMPT keyword that runs at once with no skill (INV-B:204, cmd/task.md:80,99 as cited there). WC-9 says outward actions turn on "only through the command's own explicit flag", but `/sc:task` has no such flag and the spec names none. After: the P2 implementer must either invent a flag (undefined name, not checked by any AC in SPEC:199-203) or refuse every commit/push forever, so D4's "authorized" path (SPEC:244-247) is unreachable for task. Second state: an auggie-review brief carries `--unattended --post-pr --no-post-pr`; `--no-post-pr` exists today (INV-A:38) and the spec adds `--post-pr` (SPEC:100) without stating precedence.** Recommendation: name the authorization flag per command in section 3, and state "explicit grant beats implied-off, conflicting flags are a usage error". Priority: High.

**A-2 (F-03, CRITICAL). I can break this specification by a Sequence attack on the phase order.** The invariant at **SPEC:154 ("each phase independently useful") and SPEC:159** fails when **a command accepts the flag before its gates are converted**. Concrete attack: **after P1: tdd, task, implement, pr-submit, post-release and 17 others accept `--unattended` (22 in total, see the diagram); the coordinator passes it to a task worker; the worker reaches the confidence prompt at confidence below 0.70 (cmd/task.md:93 via INV-B:199), ends its turn on a chat question, and never sends `worker_done`; 7.2 step 2 would show `agentWait`, but only in a test run.** Recommendation: see F-03.

**A-3 (F-02, MAJOR, blocking). I can break this specification by a Zero/Empty and a Sequence attack on WC-4/WC-6.** The invariant at **SPEC:62 and SPEC:64** fails when **the report directory is absent, or the same directory is reused by a retry**. Concrete attack: **state 0: `<D>` empty. Attempt 1 writes `<D>/return-contract.yaml` (`status: failed`). State 1: retry worker started with `--retry-of`, same brief, same `<D>`. State 2a: the command overwrites the file, so the first attempt's evidence is gone (WC-6 violated). State 2b: the command writes `<D>/run-2/`, so the coordinator's pre-dispatch path points at the stale `failed` file and the retry is read as failed (WC-4 violated). Variant: `--unattended` with no `<D>`: nothing can be written, yet WC-4 requires a file on every outcome.** Recommendation: see F-02.

**A-4 (F-05, MAJOR, blocking). I can break this specification by a Sentinel Collision attack on the `status` field.** The invariant at **WC-4/WC-5 (SPEC:62-63) and 7.2 step 4 (SPEC:183)** fails when **an existing contract uses a `status` word outside the four, or the file is empty**. Concrete attack: **before: workflow writes contract 1.1 (INV-B:272) with its own status words (UNVERIFIED which). The live check asserts `status in {succeeded, partial, failed, blocked}`. After: either the check fails on a healthy run, or the implementer renames the word and a downstream reader of that contract breaks. Second attack: a 0-byte `return-contract.yaml` left by a crashed run: `test -s` fails in the check, but WC-5 has no rule, so the worker's outcome for "file exists but empty" is whatever the model improvises.** Recommendation: see F-05.

**A-5 (F-07, MAJOR, blocking). I can break this specification by a Divergence attack at the 4 to 5 minute boundary of WC-10.** The invariant at **SPEC:68** fails when **a single call lasts between 4 and 5 minutes**. Concrete attack: **t=0 heartbeat; t=0 to 2 min: tool calls; t=2 to 6.5 min: one 4.5 min call. The condition "longer than 5 minutes" is false, so no split is required; the next heartbeat is due at 5 min and goes out at 6.5 min.** The cli-eval Monitor-driven wait (INV-A:44) has no single call at all, so the rule never evaluates. Recommendation: see F-07.

**A-6 (F-06, MAJOR, blocking). I can break this specification by an Accumulation attack on WC-3.** The invariant at **SPEC:61** fails when **a command has more than one gate, or the coordinator never answers**. Concrete attack: **cli-portify has three approval gates (SPEC:105). Gate 1: worker asks, coordinator replies "approve", worker re-invokes with the answer; gate 2: "ask once" is already spent if it means once per run, so the worker either resolves blocked after a successful gate 1 or asks again against the rule. Separate trace: the coordinator is itself waiting on the person; the worker's `ask` times out, resumes the same message ID, times out again; nothing in WC-3 ends the loop, and heartbeats are suspended while blocked in `ask` (CAPS:64).** Recommendation: see F-06.

**A-7 (F-12, MAJOR, not blocking). I can break this specification by a Divergence attack on the outcome mapping.** The invariant at **WC-5 (SPEC:63)** fails when **a gate-type command ends with verdict FAIL**. Concrete attack: **a `/sc:reflect` or `/sc:spec-panel` worker ends with verdict FAIL and `status: succeeded`; `worker_done --outcome succeeded` completes the Task; the dependent implement Task shows in `task-list --ready` (CAPS:84-92); a coordinator that starts ready Tasks without opening the report runs the implementation on a failed review. Section 2.3 asks the coordinator to open the report only after `worker_done` (SPEC:73), not before starting dependents.** Recommendation: see F-12.

**A-8 (F-10, MAJOR, not blocking). I can break this specification by a Sentinel Collision attack on the contract file name.** The invariant at **SPEC:62 (one fixed name, `return-contract.yaml`)** fails when **a nested command writes the same name into the same directory**. Concrete attack: **release-split runs with `<D>`, calls brainstorm, which calls adversarial; reflect and brainstorm already write `<output>/return-contract.yaml` (INV-B:112, INV-A:39). If the child receives `<D>` as its output, the child's contract overwrites the parent's file in `<D>`; the worker then reports a contract with the child's `command` field. UNVERIFIED: whether the children inherit the parent's output directory today.** Recommendation: see F-10.

## Synthesis
Consensus points
- The decision in section 1 is sound and well argued: commands stay the units of work, the coordinator owns Orca calls, and the rejected alternative is rejected with line-level reasons (SPEC:28-39). The honesty of section 1.4 and the 14-item UNVERIFIED list (SPEC:271-285) is a strength.
- Bookkeeping is accurate: the 43 = 10 + 27 + 6 split holds, each worker-capable command is tagged to one phase, and the sampled INV/CAPS citations are correct.
- The contract is not yet implementable uniformly. The five points where it breaks (location, retry directory, status vocabulary, phase and flag scope, ask protocol) are all in section 2 and 6-7, not in the decision.

Disagreements
- Fowler and Hohpe grade F-10 (nested invocations and file collisions) MAJOR but not blocking, because the child skills' behavior is UNVERIFIED here; Whittaker would block it on the collision trace in A-8. The Review Loop rule applies: no concrete wrong outcome is established, so it stays non-blocking.
- Wiegers and Whittaker differ on F-12: Wiegers wants the `partial` and FAIL semantics defined in WC-5, Whittaker wants the coordinator rule in 2.3. Both are listed in the recommendation.
- Cockburn would drop load and recommend from the worker list entirely (F-20); Fowler would keep them with a smaller scope. Left to the author.

Priority-ranked improvements: F-01, F-02, F-03, F-05, F-04, F-06, F-07, F-08 (blocking, in this order because F-01 and F-02 fix the contract shape that F-05 and F-03 depend on), then F-09, F-10, F-11, F-12, F-13, then the minor items.

## Numbered findings list
22 findings: 1 CRITICAL, 12 MAJOR, 9 MINOR in the experts' labels; 8 blocking (F-01 to F-08) and 14 not blocking under the Review Loop. `Blocking` is the graded result: CRITICAL and FR-8/FR-9 findings block, a MAJOR blocks only with a concrete wrong outcome, MINOR never blocks. Evidence paths are relative to the workspace root (`.dev/orca-command-refactor/...`); `CLAUDE.md` is the project instruction file and is not in the sandbox (UNVERIFIED line).

| # | Finding | Severity | Blocking | Spec section | Evidence (path:line) |
|---|---------|----------|----------|--------------|----------------------|
| F-01 | The report location has three spellings (`--output`, `--output-dir`, `--report-dir`) and mixed file/directory meaning; WC-4, the 3.1 and 3.2 rows and the ACs disagree | MAJOR | yes | 2.2 WC-4; 3.1; 3.2; 7.3 AC-0.4, AC-1.2 | SPEC:62, SPEC:83-84, SPEC:87, SPEC:90, SPEC:120, SPEC:194, SPEC:196; SPCMD:22-23, SPCMD:456-457 |
| F-02 | No behavior when the report location is missing or unusable (FR-8, guard G4); the fixed pre-dispatch path (WC-4) conflicts with the fresh directory per run (WC-6) | MAJOR | yes | 2.2 WC-4, WC-6; 2.3 | SPEC:62, SPEC:64, SPEC:73, SPEC:99-123; CAPS:116; SPCMD:456 |
| F-03 | P1 and AC-1.1 cover 37 commands but only 15 are converted in P1; 22 accept `--unattended` with their gates still open; AC-1.1 cannot pass without undecided P4 designs (FR-19) | CRITICAL | yes | 6 (P1, P2-P4); 7.3 AC-1.1; 9 | SPEC:154, SPEC:159-162, SPEC:195, SPEC:225; Quantity Flow Diagram above |
| F-04 | AC-C1 fails by construction (P0 adds Orca text to `core/`) and as written matches nothing (`\|` in ERE, uppercase placeholder, wrong verbs) | MAJOR | yes | 7.1 AC-C1; 5 SA-2; 6 P0 | SPEC:147, SPEC:150, SPEC:158, SPEC:166-167, SPEC:172, SPEC:66; sandbox `grep -E` test in F-04 |
| F-05 | The fixed status vocabulary was never checked against existing contracts (workflow, reflect, brainstorm, adversarial, troubleshoot); an empty or unparseable report has no rule (FR-8, guard G2) | MAJOR | yes | 2.2 WC-4, WC-5; Decisions; 7.2 step 4 | SPEC:62-63, SPEC:183, SPEC:262; INV-B:272, INV-B:112, INV-B:242; INV-A:35, INV-A:39, INV-A:60 |
| F-06 | WC-3 ask protocol is incomplete: "once" per gate or per run, no answer channel for gates without a flag, no maximum wait or decline path (FR-8, guard G3) | MAJOR | yes | 2.2 WC-3; 3.2 | SPEC:61, SPEC:90, SPEC:104-105, SPEC:115, SPEC:117, SPEC:120; CAPS:60, CAPS:64, CAPS:68 |
| F-07 | WC-10 has a 4 to 5 minute hole and does not cover Monitor-driven waits (FR-8, guard G1) | MAJOR | yes | 2.2 WC-10; 3.2 cli-eval | SPEC:68, SPEC:104; INV-A:44, INV-A:65; CAPS:130 |
| F-08 | WC-9 names no authorization mechanism for `/sc:task` commit and push, and no precedence between `--post-pr` and `--no-post-pr` (FR-8, guard G5) | MAJOR | yes | 2.2 WC-9; 3.2 task, auggie-review; 9 D4 | SPEC:67, SPEC:100, SPEC:121, SPEC:244-247; INV-A:38; INV-B:204 |
| F-09 | Eight requirements have no acceptance check or a weak one (WC-1, 3, 6, 7, 8, 10 in P2, 11, 12) | MAJOR | no | 7.1-7.3 | SPEC:172-210 |
| F-10 | No general rule for passing `--unattended` and output directories to nested commands; same-named contract files can collide | MAJOR | no | 2.2 WC-2, WC-4; 3.2 tasklist | SPEC:122; INV-A:39; INV-B:91, INV-B:112, INV-B:119, INV-B:201, INV-B:219, INV-B:271; SPCMD:460 |
| F-11 | No coordinator-side procedure for silent stalls, `agentWait`, or a maximum wait | MAJOR | no | 2.3; 7.2 | SPEC:44, SPEC:60, SPEC:73, SPEC:180-186, SPEC:282; CAPS:125-126, CAPS:129 |
| F-12 | `partial` is undefined; a FAIL-verdict run settles as success and unblocks dependents; 2.3 does not require reading status before starting dependents | MAJOR | no | 2.2 WC-5; 2.3; Decisions | SPEC:63, SPEC:73, SPEC:263; CAPS:84-92 |
| F-13 | WC-11 conflicts with fixed output paths (index-repo, cleanup-audit); the worktree-per-session rule is not reconciled | MAJOR | no | 2.2 WC-11; 3.1; 2.3 | SPEC:69, SPEC:73, SPEC:85-86; CAPS:115; `CLAUDE.md` parallel-worktree section (UNVERIFIED) |
| F-14 | The way a worker runs a `/sc:` command (Skill tool versus typed slash) is not stated | MINOR | no | 2.2 WC-7; 2.3 | SPEC:23, SPEC:65, SPEC:73; CAPS:47; `CLAUDE.md` slash-command rule (UNVERIFIED) |
| F-15 | Worker-written reports and `blocked_question` are consumed without saying they are data, not instructions | MINOR | no | 2.2 WC-4; 2.3 | SPEC:62, SPEC:73, SPEC:100, SPEC:116-117 |
| F-16 | No `contract_version`, no atomic-write or write-before-`worker_done` rule; `blocked` collides with Orca's Task status | MINOR | no | 2.2 WC-4 | SPEC:52, SPEC:62; INV-B:272; CAPS:89 |
| F-17 | A rule for this planning run (`README:31`) is cited as product rationale for WC-9 and for `/sc:git` | MINOR | no | 2.2 WC-9; 4 | SPEC:67, SPEC:133; README:29-38; INV-A:49, INV-A:91 |
| F-18 | Three statements are stronger than their evidence (tasklist nesting, "does not fail worker-start", E3 versus 1.4 (1)) | MINOR | no | 1.2 E3; 1.4; 3.2 tasklist | SPEC:23, SPEC:43-44, SPEC:122; INV-A:14; INV-B:210, INV-B:314; CAPS:47, CAPS:49 |
| F-19 | "Well inside" the readiness limit is unmeasurable although numbers (30 s ok, about 45 s fails) are in the evidence | MINOR | no | 2.2 WC-1 | SPEC:59; CAPS:49 |
| F-20 | `/sc:load` and `/sc:recommend` get phase work while section 4 says to use them coordinator-side; `load` has no contract, so AC-1.1 cannot hold for it | MINOR | no | 3.2; 4; 7.3 AC-1.1 | SPEC:112, SPEC:115, SPEC:139, SPEC:195 |
| F-21 | "Phases 1-3 need no user decision" contradicts D1, which decides the flag P1 builds | MINOR | no | 6; 9 D1 | SPEC:51, SPEC:154, SPEC:225, SPEC:227-230 |
| F-22 | No worked example of a contract or a brief | MINOR | no | 2.2 WC-4; 2.3 | SPEC:62, SPEC:73, SPEC:228 |

Open blocking findings: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08.

## Decisions
| Decision | Options | Rationale |
|---|---|---|
| Output format | `--format standard` YAML only; critique-mode buckets only; both | Both. The default format is YAML (`SPCMD:270`), critique mode groups findings by bucket (`SPCMD:123`) and the brief asks for a numbered list. The YAML block carries metadata and the blocking findings; detail sits in the buckets; the list is canonical. |
| Guard table scope | every numeric or flag condition in the spec; the six guards that decide section 2 behavior | Six guards plus the Quantity Flow Diagram for the phase gate. Listing every acceptance-check condition would add rows without new findings. |
| Grading of FR-8 rows | one finding per GAP row; one finding per guard | One finding per guard, each naming its GAP rows, so the reviser has eight items to close instead of fourteen. |
| Evidence outside the sandbox | read it anyway; mark UNVERIFIED | The prompt forbids reading outside the sandbox directory, so those citations are marked UNVERIFIED. |
| Supplied command definition used as evidence | ignore; cite for the command's own text only | Cited only where it shows how a command's text already treats the same question (F-01, F-02, F-10), and always with the note that the repo's baseline is UNVERIFIED. |

## UNVERIFIED in this review
1. Whether the repo's commands match the spec's 3.2 baseline; the supplied `/sc:spec-panel` definition already carries `--output <file>`, `--report-dir`, `--unattended` and an `## Unattended mode` section (`SPCMD:22-23`, `SPCMD:451-461`), which the spec lists as work to do (`SPEC:120`).
2. The `status` vocabularies of the existing contracts (F-05).
3. Whether nested commands inherit the parent's output directory (F-10).
4. All `CLAUDE.md` line references (F-13, F-14); the file is not in the sandbox.
5. Every citation to `src/`, `~/.claude`, `.dev/evals/` and `.dev/codegraph-migration/` that the inventories do not quote.
6. Whether a worker's argv-launched `/sc:` text is expanded as a slash command (F-14).

## Reviser brief
Blocking finding ids only: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08.
Rules for the reviser (the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Report the byte size of the spec before and after.

verdict: FAIL
