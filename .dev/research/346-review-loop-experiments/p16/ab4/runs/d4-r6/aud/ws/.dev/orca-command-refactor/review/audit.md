review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review; no `--re-review`, no `--baseline`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines
- candidate sha256: `969ea3c660a240d980e47aa21c5b87e0ebbb7ea61cb15bc2f7483d1290dc6ad5`
- baseline: none given (first review of the full document)
- reviewer model: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 27-32)
- mode flags: not `--unattended`, so no `return-contract.yaml` is written. `--improve` not passed, so no improved spec is written. The candidate was not edited. Written file: this one only.
- brief clauses overridden: none. The brief asks for path:line citations and UNVERIFIED marking; both are applied. Its "Write only your output file" is obeyed.

## Coverage (what was and was not checked)
- Read in full: the spec (lines 1-285), `README.md` (1-38), `inventory/commands-a.md` (1-121), `inventory/commands-b.md` (1-324), `inventory/orca-capabilities.md` (1-189).
- Checkable evidence is only the three inventories plus the README. Every spec citation of the form `INV-A:N`, `INV-B:N`, `CAPS:N` was matched against the inventory line. About 120 matched with no mismatch: spec section 1.2 and 1.3 rows, WC-1 to WC-12, all 43 rows of section 3, section 4, UNVERIFIED items 1-13. Citation of `.dev/orca-command-refactor/README.md:12` and `:31` also matches.
- NOT checkable in this sandbox, so UNVERIFIED here: every direct citation of `src/superclaude/...` (`cmd/`, `sk/`), `CLAUDE.md:N`, `Makefile`, `pyproject.toml`, `install_core.py`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `HOW-WE-WORK.md:N`, and the E5 grep results (`spec:25`). The spec's own claims of a prior citation check (`spec:11`, `spec:285`) are also UNVERIFIED. Where an inventory line quotes the cited source (for example `EVIDENCE.md:39,45,56` via `CAPS:49`), that quote was accepted as secondary evidence.
- Not covered: the actual behavior of any command, Orca itself, or whether the PR #329 run worked.

## Grading check
For each finding that could be blocking, the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" was tried. None holds without a further assumption (a guess that the implementer picks the worse of two readings, or a requirement the text never states). So no finding is blocking. Every finding below is Medium (a warning) or a minor note.

---

## === REQUIREMENTS ANALYSIS ===

### Wiegers (lead): traceability of WC-1..WC-12 to acceptance checks
| Requirement | Acceptance check that exercises it | Evidence |
|---|---|---|
| WC-1 no prompt before ready | only implied by 7.2 step 1 (`state: ready`) | spec:180 |
| WC-2 no person-blocking step | 7.2 step 5, AC-2.2 | spec:184, :200 |
| WC-3 ask to coordinator | none | no AC mentions `ask`/`reply` (spec:166-210) |
| WC-4 report file | 7.2 step 4 | spec:183 |
| WC-5 outcome mapping | 7.2 step 3 | spec:182 |
| WC-6 resume or safe re-run | none (no `--retry-of` step anywhere) | spec:166-210 |
| WC-7 top level | AC-0.4 + step 5 | spec:194 |
| WC-8 no Orca fan-out | AC-C1 | spec:172 |
| WC-9 no outward action | AC-2.4, AC-4.2 | spec:202, :209 |
| WC-10 wait size | AC-4.3 only (pr-submit); cli-eval, also changed for WC-10 in P2, has none | spec:104, :210 |
| WC-11 parallel-safe | AC-3.4 (save only); cleanup-audit "one audit per worktree" has none | spec:85, :207 |
| WC-12 pull follow-ups | none | spec:70 |

### F-01 (Medium, MAJOR label): four requirements have no acceptance check (WC-3, WC-6, WC-12, WC-1 beyond readiness)
- Expert: Wiegers, Crispin. Priority Medium.
- Grading: the text states the requirements and states no check for them. This is "a requirement the document never states" (a missing check), not a stated text that does harm, so it is Medium.
- Recommendation: add one live check per missing row (a retry with `--retry-of` that leaves attempt 1's output unchanged; a gate-trigger run where the worker uses `ask` and the coordinator `reply`s).

### F-02 (Medium): behavior when `--unattended` is given without an output path is not stated
- Expert: Wiegers (empty-input shift), Whittaker (Zero/Empty attack). Priority Medium.
- Location: WC-4 (spec:62), 2.3 (spec:73), section 3.2 "add `--output`" rows (spec:99-125).
- Attack: coordinator passes `--unattended` and omits `--output` for `analyze`. WC-4 says the contract goes "in the directory the coordinator passed". No text says to refuse, to default, or to resolve as blocked. The three WC-2 resolutions (default, flag, blocked) are defined for gates, not for a missing output flag. Before-state: no dir; after-state: contract path unknown, so `worker_done --report-path` has no real value (`CAPS:72-74`).
- Grading: the spec leaves the state undefined; an implementer may pick any of three behaviors. Medium.

### F-03 (Medium): `--output` kind (directory or file) is unstated for the 9 P1 commands and the contract location depends on it
- Expert: Wiegers, Adzic. Priority Medium.
- Location: WC-4 names the file case only for `tdd` and `init-lite` (spec:62). Section 3.2 says "add an output path" for build, design, document, test, index, business-panel (spec:101-111); `explain` says "write the explanation to a file" (spec:108). Only AC-1.2 (spec:196) shows `--output <dir>`.
- Consequence: the sidecar name rule (`<file-stem>.return-contract.yaml`) vs the dir rule (`return-contract.yaml`) cannot be chosen from the text for these commands.
- Grading: readable from AC-1.2; the guess is small. Minor-to-Medium; listed Medium.

### F-04 (Medium): the contract rule for `init-lite` contradicts itself within WC-4, and the same row puts the sidecar in a tracked docs path for `tdd`
- Location: spec:62 says "(tdd, init-lite) writes `<file-stem>.return-contract.yaml` beside that file", then in the same row "A ready command with no phase for a contract (init-lite) reports its section 3.1 file". Section 3.1 gives init-lite "Small fix: None" (spec:87) and section 3 says the other 3.1 commands get no Unattended section (spec:76).
- No phase builds the init-lite sidecar, so the two sentences cannot both be implemented.
- Grading: harm is low (init-lite is read-mostly and the fallback is named). Medium.

### F-05 (Medium): section 2.3 says every brief carries `--unattended`, but 16 of the 43 commands never get that flag
- Location: spec:73 ("the exact command line including `--unattended`") vs section 3.1 "Brief must pass" columns (spec:83-92: no `--unattended` for adversarial, brainstorm, cleanup-audit, index-repo, init-lite) and the P0 smoke commands (spec:194: no `--unattended`). Commands with no Unattended section: 5 of the ready 10 (brainstorm, adversarial, cleanup-audit, index-repo, init-lite), `load`, and 6 coordinator-only.
- Attack (Sequence): P0 coordinator follows 2.3 literally and appends `--unattended` to `/sc:brainstorm`. The flag does not exist there; what the command does with an unknown flag is not stated (UNVERIFIED).
- Grading: two stated texts disagree, but the implementer is told the P0 commands in AC-0.4, so a reasonable reading exists. Medium.

### F-06 (Medium): WC-9 relies on "the command's own explicit flag" for outward actions, and that flag does not exist for several commands
- Location: spec:67, section 3.2 `task` (spec:121: "EXEMPT `commit`/`push` refused unless authorized"), `post-release` (spec:113), D4 (spec:244-247).
- `INV-B:204` says `task`'s EXEMPT commit/push run "immediately with no skill" and names no flag. The spec defines a new `--post-pr` only for auggie-review (spec:100). So for `task` there is no flag the brief can pass to authorize; D4(a) ("passes the command's explicit flag") cannot be carried out.
- Grading: P4 and D4 are explicitly pending; for `task` (P2) the unauthorized default is the safe one. Medium.

### F-07 (Medium): `reflect` is listed "ready today" but its default-on side effects are only conditionally switched off
- Location: spec:88 ("`--no-promote` when the coordinator owns folder moves"), `INV-B:114` (default-on Wave 7 moves the validated work-unit folder; writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md`).
- WC-9 (spec:67) lists pushes, PRs, posts, installs, provisioning, paid runs; it does not list local moves of other work units' folders or writes to tracked docs. WC-11 (spec:69) covers shared files only by example.
- Attack (Accumulation): two parallel reflect workers in one worktree both promote and both append to the tracked memory file.
- Grading: harm needs a guess about coordinator behavior. Medium.

### F-08 (Medium): "ready today" verdicts do not trace gates through nested commands
- Location: spec:81-92 against `INV-A:39` (brainstorm Wave 4 optional `sc-tasklist-protocol`/`task-builder`) and `INV-B:209` (tasklist Stage 10.5 runs reflect with `--remediate`, which can prompt).
- brainstorm is "ready" with "None" fix (spec:84), and release-split nests brainstorm (`INV-B:119`). Whether brainstorm's optional handoff can reach tasklist's reflect prompt is not traced. UNVERIFIED.
- Grading: unknown, not shown wrong. Medium.

---

## === ARCHITECTURE ANALYSIS ===

### Fowler (lead): decision soundness
- The decision (Orca on top, commands unchanged units, one shared `WORKER-CONTRACT.md`) is supported by `CAPS:97-103` (depth 1), `CAPS:147-150` (standalone, `worker_done` bound to the dispatched pane) and `INV-A:90`/`INV-B:285-286` (orchestrators are coordinator-only). Rejected alternative R1-R5 checks out against those lines.
- Interface note: one name (`return-contract.yaml`) for 30 commands plus fixed vocabulary `succeeded/partial/failed/blocked` (spec:62, :262) is a clean interface for the coordinator.

### F-09 (Medium): the new fixed status vocabulary is imposed on contracts that already exist without checking their current values
- Expert: Fowler, Newman (compatibility). Priority Medium.
- Location: WC-4 "Commands that already write a contract keep their fields and add the missing ones" (spec:62) vs Decisions "Fixed set `succeeded / partial / failed / blocked`" rather than "copy each command's own statuses" (spec:262).
- The inventories show only that workflow's contract carries `status`, `plan_path`, `reflect_report_path` (`INV-B:272`) and name no value sets for workflow, brainstorm, reflect, adversarial. If an existing `status` takes other values, "keep their fields" and "one of four" cannot both hold, and SA-4 (additive edits) blocks a rename.
- Also: no `schema_version`/contract-version field is required in WC-4, though workflow's is already "contract 1.1" (`INV-B:272`). The shared file cannot evolve safely. Newman: "How does this handle backward compatibility?"
- Grading: depends on unread data. Medium.

### F-10 (Medium): nested `--unattended` forwarding and contract placement are not specified
- Expert: Hohpe (data flow), Fowler.
- Location: tasklist row (spec:122: "passes `--unattended` to each reflect"), plus tdd to task, workflow to reflect, release-split to brainstorm/adversarial, task to troubleshoot (`INV-B:201`).
- WC-4 says a contract goes in "the directory the coordinator passed". For a nested call the spec does not say which `--output` the parent hands the child, so child `return-contract.yaml` files can land in the parent's directory under the same name. Adversarial avoids this only by its own fixed subdirectory (spec:83).
- Sequence: tasklist (P2) forwards the flag to reflect (also P2); the order inside P2 is unstated, and until reflect gains the flag it receives an unknown option.
- Grading: collision needs an assumption about what the parent passes. Medium.

### F-11 (Medium): tasklist row asserts nesting is safe, against its own inventory
- Location: spec:122 ("runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`").
- `INV-B:215` recommends the per-phase reflect fan-out run "at the worker's top level, not inside subagents"; `INV-B:210` marks nested spawning UNVERIFIED. The spec drops that recommendation and states the limit as met. Counting layers: worker (0), Stage 10.5 reflect subagent (1), reflect's Tier 2 reviewers (2), and their own adversarial advocates (2-3) reach the "three layers" cap in `INV-A:14`, where the Agent tool is withheld.
- The spec's rationale for the change from the inventory (pass `--unattended` instead of drop `--remediate`) is not recorded in its Decisions table (spec:258-269).
- Grading: unverified, not shown wrong. Medium.

### F-12 (Medium): how the worker session actually runs a `/sc:` command is not stated
- Location: spec:16, WC-7 (spec:65), AC-0.4 (spec:194). `CAPS:47`: Orca passes the task to Claude on the command line (argv) with a preamble.
- A slash command is expanded only when it starts the message (UNVERIFIED for this setup); the preamble comes first. The spec never says whether the worker uses the Skill tool or a slash command. UNVERIFIED item 1 covers "does a direct run complete" but not this mechanism. P0 will expose it, but the contract text (2.3) should name it.
- Also, `spec:1.2 E3` cites `invocation_method: "skill-direct"` (`INV-A:13`) as proof, while 1.4(1) says that run proves only the nested route. The tension is not reconciled.
- Grading: Medium.

### Nygard: failure modes
### F-13 (Medium): no rule for "report written but no `worker_done`" and none for the coordinator's handling of `blocked`
- Location: 2.3 (spec:72-73), WC-5 (spec:63).
- WC-4 makes the contract exist on every outcome, so a worker that dies or runs out of context after writing it leaves a readable file and no `worker_done`. The coordinator procedure (spec:73) opens the report only "after `worker_done`". `CAPS:125-126` says only `exited` liveness is positive proof of a stall; the spec does not connect the two.
- For `blocked`: WC-5 maps it to `--outcome failed`, which keeps dependents blocked until a `--retry-of` replacement completes (`CAPS:90`). The coordinator-side sequence (read `blocked_question`, answer, start `--retry-of` with the answer as a flag, pass a new output dir for "fresh dir" commands) is never written. WC-6 says a "fresh output directory" without saying who creates it; WC-4 pre-fixes the path (spec:62, :64), so the two cannot both place it.
- The circuit breaker is not a problem: `CAPS:80` says a worker's own `failed` report does not count (the spec cites this at spec:263).
- Grading: unstated requirement. Medium.

### Hohpe: delivery
- Exactly-once `worker_done` (WC-5) and pull-only follow-ups (WC-12) match `CAPS:73,66-67`. No finding.

### Newman, Hightower, Gregory, Cockburn
- Cockburn: primary actors (coordinator, person, worker) and goals are clear in 1.1 and section 5. No finding.
- Hightower: no cloud-native deployment content applies to a planning spec. No finding.
- Gregory: acceptance checks and their live cost are stated per phase; no finding beyond F-01.
- Newman: see F-09.

---

## === ADVERSARIAL ANALYSIS (Whittaker, review order 6) ===

### F-14 (Medium): AC-C5 and AC-0.3 cannot detect deleted bullet lines
I can break this specification by **Divergence Attack**. The invariant at **AC-C5 (spec:176) and AC-0.3 (spec:193)** ("`grep -E '^-[^-]'` prints nothing: edits are additive") fails when **a removed line is a markdown bullet or any line starting with `-`**. Concrete attack: command file has `- Will Not: modify files`; the phase deletes it. The diff shows `-- Will Not: modify files`. Pattern `^-[^-]` needs a non-dash second character, so it does not match. Test run in this sandbox: input `-- removed bullet` printed nothing; `-removed plain` and `-| removed row |` printed. Before: check passes; after: a bullet removed and still passes. Command files and the "Will Not" lists are mostly bullets, so the additivity guarantee (SA-4) is largely unenforced.
Also, adding a new flag to a Usage line (SA-4 "new flags") rewrites an existing line, which `-U0` shows as a removed line and so would fail AC-C5 for any such edit that is not a separate new line. The spec does not say new flags go on a new line.
Grading: the check is weak, not the stated text wrong. Medium.

### F-15 (Medium): AC-C1 misses the spec's own spelling of the Orca command and is wrong when copied raw
I can break this specification by **Sentinel Collision Attack**. The invariant at **AC-C1 (spec:172) / WC-8 / SA-2** fails when **a changed file writes `ORCA orchestration worker-start`**, which is the exact placeholder spelling the spec uses in section 7 (spec:167, :180-186). The pattern is lowercase `\borca` with no `-i`, so it does not match. Concrete attack: a command gains the line `ORCA orchestration worker-start --task ...`; AC-C1 prints nothing; SA-2 is broken. Second defect: the raw text has `(orchestration\|worktree\|terminal\|agent)` and `\| grep -v`. In ERE `\|` is a literal pipe (verified here: `printf 'b\n' | grep -E 'a\|b'` returned 1), so the raw command matches nothing and passes vacuously; the same `\|` before `grep` breaks the shell pipeline. It is correct only after table rendering. Same for AC-C4, AC-C5 and AC-0.3.
Also P0's own deliverables live in `src/superclaude/core` (the contract file and the HOW-WE-WORK Orca section, spec:158), which AC-C1 scans, while SA-2 (spec:147) allows an Orca mention in the contract file. Whether the P0 text trips AC-C1 depends on its spelling.
Grading: Medium.

### F-16 (Medium): undefined count and file totals not covered by evidence: the "43 commands" claim and E5
I can break this specification by **Accumulation Attack** on the total. The invariant at **section 3 intro (spec:76) and E5 (spec:25)** ("The 43 commands in `cmd/`"; "no command, skill, agent or core file calls Orca today") fails when **`cmd/` holds more files than the two inventories scope**. Both inventories list their scope as names (`INV-A:3`, `INV-B:3`); neither shows a directory listing, so 43 is a sum of scopes, not a count of the directory. UNVERIFIED here. A pointer from outside the evidence: the host's installed skill list also contains `sc:graph`, `sc:impact` and `sc:issue` (the last described there as creating an Orca worktree and launching an agent). These are absent from both inventories and from the spec. This is not checkable in the sandbox and may be absent from the spec's worktree; it is recorded so the coordinator confirms with `ls src/superclaude/commands | wc -l` and `grep -rli orca src/superclaude/commands`. If a command does call Orca, E5, SA-2 and AC-C1 are wrong as written.
Grading: depends on data not in evidence. Medium.

### F-17 (minor): the sequence of conditions in section 6 and 9
- Spec:154 says "Phases 1-3 need no user decision" while D1 (flag versus detection) changes every P1-P3 edit (spec:227-230). Spec:225 and D1 say the phases proceed on the recommendation; the two statements are consistent only on that reading.
- `pr-submit` is counted in "27 needing a change" (spec:76) although under the recommended D3(a) it gets no change (spec:240). Minor count inconsistency.
- Non-goal 8 (spec:220) limits scope to worker-blocking defects, but `load`'s missing `--checkpoint` in Usage and business-panel's frontmatter (effect UNVERIFIED, spec:278) are in scope (spec:102, :112).
- SA-1 (spec:146: every default flag value stays) vs the validate-tests default-target fix (spec:125) are reconciled only by SA-4 (spec:149).
- Revision tags `(M1)`..`(M7)` (spec:62, :76, :79, :89, :183, :194-196, :200) refer to a disposition list not named in the spec's citation conventions (spec:7-11).

---

## Guard Condition Boundary Table
Trigger: the spec contains thresholds and guards (60 s readiness, 5-minute heartbeat and 4-minute wait, depth 1, confidence 0.70, status mapping). Input classes that cannot occur for a guard are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit | WC-1 spec:59 | Zero/Empty | no launch-path prompt | pass | worker reaches `input_accepted` | OK |
| readiness limit | WC-1 spec:59 | Maximum/Overflow | fallback above about 45 s | fail | "fails again" (`EVIDENCE.md:56` via `CAPS:49`); spec says fall back "well inside" the limit, no number | OK |
| heartbeat cadence | WC-10 spec:68 | Typical | wait of 3 minutes | within | heartbeat between waits | OK |
| heartbeat cadence | WC-10 spec:68 | Legitimate Edge Case | single tool call of exactly 4-5 minutes | boundary | "longer than 5" must split into "at most 4"; 4:01-5:00 is covered by neither rule | GAP |
| heartbeat cadence | WC-10 spec:68 | Zero/Empty | blocked in `ask` or `check --wait` | skip | no heartbeat while blocked (WC-3, `CAPS:64`) | OK |
| status mapping | WC-5 spec:63 | Zero/Empty | no report file exists | true | `--outcome failed` | OK |
| status mapping | WC-5 spec:63 | Sentinel Value Match | `partial` | true | maps to `succeeded`; stated in first sentence | OK |
| status mapping | WC-5 spec:63 | Legitimate Edge Case | report says `succeeded` but no `worker_done` sent | n/a | not specified | GAP |
| output path | WC-4 spec:62 | Zero/Empty | `--unattended` with no `--output` | n/a | not specified | GAP |
| output path | WC-4 spec:62 | One/Minimal | `--output` names an existing file or non-writable dir | n/a | "including stops before any other output exists" but no location (see F-02, F-13) | GAP |
| nesting depth | WC-8 spec:66 | Maximum/Overflow | command calls `worker-start` | refused | `nested_worker_depth_exceeded` (`CAPS:99`); WC-8 forbids it | OK |
| confidence gate (task) | spec:121 | Typical | 0.69 | true | blocked | OK |
| confidence gate (task) | spec:121 | Legitimate Edge Case | exactly 0.70 | false | proceeds ("below 0.70" blocks); inventory says 0.70-0.89 present alternatives (`INV-B:199`) | OK |
| outward-action default | WC-9 spec:67 | Legitimate Edge Case | `task` EXEMPT `commit`/`push` | refused | no authorizing flag exists (F-06) | GAP |
| resume | WC-6 spec:64 | One/Minimal | retry worker, command has no resume flag | fresh dir | who creates the dir is unstated (F-13) | GAP |

Grading (FR-8, FR-9): each GAP is Medium. None names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk; they are undefined states. The 4:01-5:00 minute gap in WC-10 is Medium: the stated ranges overlap-free but leave a window where the 5-minute heartbeat can be missed by one wait.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)
Trigger: classification and phasing are two or more stages whose counts differ. Counts were summed from the spec and the inventories.

```text
[Source: 43 commands = INV-A 21 + INV-B 22]
   --> [Stage 1: verdict (INV-A 5/13/3 + INV-B 5/14/3)] --> [10 ready + 27 needs-change + 6 coordinator-only = 43]   N = M
   --> [Stage 2: phase assignment]
         P0: 0 edits | P1: 9 needs + 4 ready fixes = 13 | P2: 11 needs + 4 ready = 15 | P3: 4 | P4: 3 | untouched: brainstorm, init-lite
         13 + 15 + 4 + 3 + 2 untouched = 37 = 10 ready + 27 needs   (6 coordinator-only never edited)   N = M
   --> [Consumer: Unattended-section recipients = 8 (P1) + 11 + 4 (P2) + 4 (P3) + 3 (P4) = 30]   subset of 37, by design (spec:76)
```

Recount, stated plainly: 10 ready = 4 (P1 small fixes: adversarial, cleanup-audit, index-repo, workflow) + 4 (P2: reflect, release-split, tdd, troubleshoot) + 2 untouched (brainstorm, init-lite). 27 needs-change = 9 (P1, incl. `load`) + 11 (P2) + 4 (P3) + 3 (P4). 6 coordinator-only. 4+4+2+9+11+4+3+6 = 43. Counts are conserved at every stage; no consumer assumes a larger count. Unattended section recipients = 8 + 11 + 4 + 4 + 3 = 30 (workflow, adversarial, cleanup-audit, index-repo get fixes only, not the section). No dimensional mismatch (no FR-19 finding). The only unverified input to the diagram is the 43 itself (F-16).

## Adzic: example scenarios with a degenerate variant
- Scenario A (blocked gate). Given `/sc:tdd "auth" --unattended --output docs/TDD_AUTH.md` (bare topic). When the worker runs it. Then `docs/TDD_AUTH.return-contract.yaml` has `status: blocked` and a non-empty `blocked_question`; the worker sends `worker_done --outcome failed --report-path` that file (spec:62, :63, :90). Degenerate variant: the same call without `--output` has no defined outcome (F-02).
- Scenario B (partial). Given a roadmap run that finishes with `status: partial`. Then `--outcome succeeded`, first body sentence says `partial` (spec:63, :263). Degenerate variant: contract absent, so `failed`. Consistent.
- Scenario C (retry). Given a `blocked` worker. When the coordinator starts `--retry-of` with the answer as a flag. Then a "fresh dir" command writes where? Not stated (F-13).

## Crispin: boundary tests the spec should add
Below minimum (no `--output`), at minimum (empty dir), typical, above maximum (two workers, one dir), degenerate (unwritable dir). Only the typical case has a check today (F-01, F-02).

---

## follow-up candidates (Medium and minor; none blocks)
| id | severity | summary |
|---|---|---|
| F-01 | Medium | WC-3, WC-6, WC-12, WC-1 have no acceptance check |
| F-02 | Medium | `--unattended` without an output path is undefined |
| F-03 | Medium | `--output` kind (dir or file) unstated for the 9 P1 commands |
| F-04 | Medium | init-lite contract rule contradicts itself in WC-4 |
| F-05 | Medium | 2.3 says every brief has `--unattended`; 16 commands never get it |
| F-06 | Medium | WC-9 needs an explicit flag that does not exist for `task`/`post-release` |
| F-07 | Medium | reflect's default promote and tracked-file write only conditionally off |
| F-08 | Medium | nested gates for "ready" commands not traced (brainstorm, release-split) |
| F-09 | Medium | fixed status vocabulary and no contract version, existing contracts unchecked |
| F-10 | Medium | nested `--unattended` forwarding and contract placement unspecified |
| F-11 | Medium | tasklist nesting claim contradicts its inventory; reason not in Decisions |
| F-12 | Medium | how a worker runs a `/sc:` command is not stated; "skill-direct" vs nested tension |
| F-13 | Medium | no rule for report-without-`worker_done`; `blocked` handling and fresh-dir owner unstated |
| F-14 | Medium | AC-C5/AC-0.3 miss deleted bullet lines and flag-line edits |
| F-15 | Medium | AC-C1 misses `ORCA`, and the raw `\|` is wrong when copied |
| F-16 | Medium | "43 commands" and E5 rest on scoped names, not a directory listing (UNVERIFIED) |
| F-17 | minor | count and scope inconsistencies, undefined `(M1)`..`(M7)` tags |

Issue question: this is a worker run in a sandbox without a user channel, so the "open an issue for these?" question was not asked and nothing was created. A coordinator or user should decide.

## UNVERIFIED in this audit
`src/superclaude/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/evals`, `.dev/codegraph-migration` citations (no copy in the sandbox); whether `cmd/` holds only the 43 scoped commands; the E5 grep results; the spec's claims of 11 re-read locations and 340 re-checked citations; unknown-flag handling in commands; whether the preamble affects slash-command expansion.

## Reviser brief
none: there are no open blocking findings, so there is nothing to revise. (Rules for any later brief: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing; report byte size before and after with bytes added and deleted per finding id.)

verdict: PASS
