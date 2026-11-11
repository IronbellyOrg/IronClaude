review: 1 of 3

# Spec-panel critique: Orca worker-contract spec (labelled whole-document audit, first review)

## Header

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 346 lines |
| Candidate sha256 | `7492365d5c2762de22b8891da8bbf57aa26adebbb515942890f731fdffd2f096` (taken before and after reading; identical) |
| Baseline / prior | none given; `--re-review` and `--baseline` absent, so this is a first review of the full document, `review: 1 of 3` |
| Reviewer model actually used | `claude-sonnet-5-5` (Sonnet 5.5) |
| Prompt followed | FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (lines 1-55) before any finding |
| Unattended mode | not engaged: no standalone `--unattended` token in the arguments, so no `return-contract.yaml` is written (`command.md:459`) |
| Improve step | skipped: the brief says edit nothing but this file and the FIRST-REVIEW prompt says do not edit the candidate |
| Brief clauses overridden | none |
| Output format | critique-mode grouping (`command.md:123`) with the `--format standard` keys condensed into one YAML block (section 9) |

Citation shorthand: `spec:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `command.md:N` = the `/sc:spec-panel` definition given with the brief.

## 1. Coverage

- Read in full: the candidate (all 346 lines), `README`, `INV-A`, `INV-B`, `CAPS`, `command.md`, and the review-loop prompts file.
- Compared with the inventory text: every `INV-A`, `INV-B` and `CAPS` line reference in sections 1.2-1.4, 2.2, 3.1-3.3, 4 and the UNVERIFIED list. No mismatch found. The counts reconcile (section 8).
- Not checkable here (no file in the workspace): every `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `HOW-WE-WORK.md`, `install_core.py`, `.dev/codegraph-migration/...` and `EVIDENCE.md` line the spec cites directly rather than through an inventory line. These are UNVERIFIED in this review. The spec marks its own unwitnessed statements UNVERIFIED (`spec:13`, `spec:337`), which is consistent.
- This is the separate, labelled whole-document review that `command.md:262` allows. Had it found a blocker, the blocker would be escalated and no fourth review started.

## 2. Result in one paragraph

No blocking finding. The spec's decision (Orca coordinates, commands stay units of work) is supported by the inventories, the requirements WC-1 to WC-12 are consistent with each other on the points that decide behaviour, and the 43 / 10 / 27 / 6 and phase counts reconcile exactly. Fourteen Medium findings (listed under `follow-up candidates`, F-01 to F-14) are gaps a careful implementer would have to resolve by guess; none is a stated text that, followed as written, builds the wrong thing. Eleven minor notes follow (N-1 to N-11).

## 3. Grading check (FIRST-REVIEW prompt)

For each strongest candidate the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" was written, and the finding was blocking only if it held with no further assumption.

| Id | Sentence | Needs a guess? | Grade |
|---|---|---|---|
| F-01 | An implementer builds `command` as the argument string the Skill tool passes, and `spec:222` compares it with the Task's line, which differs by the `/sc:<name>` prefix and quoting. | Yes: that the brief's "exact command line" includes the slash prefix and that the command sees it. | Medium |
| F-02 | An implementer builds WC-5.2 as written, a command that dies silently leaves an old non-empty report, and the worker sends `succeeded`. | Yes: that the command exits without a STOP line. | Medium |
| F-04 | An implementer builds resume flags, and no route the spec allows lets a coordinator pass one. | Yes: that a coordinator wants to resume rather than re-run. | Medium |
| F-08 | An implementer builds WC-4.4 as written and it deletes any file at the contract path. | Yes: that the brief reused a location (a coordinator error under `spec:78`). | Medium |
| F-13 | An implementer builds tasklist's unattended Stage 10.5 and a `needs_human_decision` item has no stated resolution. | Yes: that the headless rule leaves that item as a HALT. | Medium |
| F-14 | An implementer builds the adversarial smoke run (AC-0.4), the command prints no path, and the run is recorded `failed`. | Yes: that adversarial prints nothing. | Medium |

## 4. Expert sequence (fixed order, `command.md:103-113`)

1. **Wiegers** (requirements lead): requirements are mostly measurable and carry ids and evidence. Gaps are in the ready-command contract fields (F-03) and the canonical form of `command` (F-01).
2. **Adzic**: examples are concrete (research `--strategy intent`, tdd bare topic). One example contradicts a rule (F-10) and one acceptance run depends on an unproven print (F-14).
3. **Cockburn**: primary actor is the coordinator, goal is dispatching a command without a person. The coordinator's failure goal (a worker that never reports) is not a stated requirement (F-05).
4. **Fowler** (architecture lead): the decision and its rejected alternative are sound. The shared contract file mixes two audiences (F-06) and the "section lives in the command" assumption breaks for skill-direct callees (F-11).
5. **Nygard**: failure modes mostly addressed (stale file, blocked, refusal, circuit breaker). Residual: unconditional deletion (F-08), silent-stall handling (F-05), unproven background polling with no fallback (F-09).
6. **Whittaker**: attack results in section 7.
7. **Newman**: contract schema has no version or compatibility rule although existing consumers exist (F-07).
8. **Hohpe**: delivery semantics are sound (exactly one `worker_done`, `ask` resumed by message id, `spec:63,65`). Correlation relies on command-line equality and mtime (F-01).
9. **Crispin**: acceptance checks are executable; the scan in code block 1 has blind spots (F-12).
10. **Gregory**: quality expectations are defined per phase (section 7.3). Three-amigos style gap: the person's view (standalone) is protected by SA-1 to SA-6.
11. **Hightower**: operational notes are in minor findings (remote host checks, N-2).

## === REQUIREMENTS ANALYSIS ===

### F-01 `command` field equality has no canonical form
- Severity label MAJOR, graded **Medium**. Expert: Wiegers, Adzic (Hohpe on correlation).
- Location: WC-4.3 (`spec:64`), 7.2 step 4 (`spec:222`), brief duty (`spec:75`, `spec:79`).
- Issue: WC-4.3 requires `command` "(the exact command line)". Step 4 asserts `str(d['command']).strip() == <this Task's exact command line>`. The command never sees the Task text; it sees the Skill-tool `args` (`spec:79`). Whether the stored string carries the `/sc:<name>` prefix, the original quoting and the `--unattended` token is not defined, so a correct command can fail the check, or an implementer pads the field to pass. The same field is the only Task correlation (the contract carries no Task or Dispatch id because the command never sees them, R3 at `spec:37`).
- Recommendation: define `command` as `/sc:<name> ` plus the `args` string exactly as the brief passes it, or compare a normalised token list; say which. Rationale: removes a guess from every phase's step 4.
- Priority: High. Quality impact: testability +0.5.

### F-02 WC-5.2 has no freshness test; the worker settles before the coordinator can catch it
- Severity MAJOR, graded **Medium**. Expert: Nygard, Whittaker.
- Location: WC-5.2 (`spec:65`), fixed-location rows (`spec:93`, `spec:94`), step 4 mtime test (`spec:222`).
- Issue: for a command with no contract yet, `--outcome succeeded` is sent when the "Report today" file "exists, is non-empty" and the final output has no halt or STOP line. Index-repo's `PROJECT_INDEX.md` (`mode=update`, INV-A:53) and cleanup-audit's `.claude-audit/` files (INV-A:42) pre-exist on a re-run. The mtime test lives only in the coordinator's step 4, which runs after `worker_done` has settled the Task and unblocked its dependents (CAPS:77, CAPS:90).
- Recommendation: add "and was modified after the command started" to WC-5.2. Rationale: one clause, no new mechanism.
- Priority: High. Quality impact: consistency +0.3.

### F-03 Ready commands that already write a contract: fields and status vocabulary are not checked before the acceptance run
- Severity MINOR-to-MAJOR, graded **Medium**. Expert: Wiegers.
- Location: WC-4.3 and WC-5.2 (`spec:64-65`); rows `spec:92` (brainstorm), `spec:96` (reflect), `spec:100` (workflow), `spec:236` (AC-1.2).
- Issue: WC-4.3 says existing contracts "keep their fields and add the missing ones", yet the rows read "None (section and flag only)". The status words of brainstorm and reflect contracts are recorded nowhere (the inventories name workflow's fields, INV-B:272, but not brainstorm's or reflect's status words, INV-A:39, INV-B:112). AC-1.2 step 4 asserts a four-value `status` and a `command` key on each P1 command, brainstorm included.
- Recommendation: add to the brainstorm and reflect rows "map status to the four values; add `command`", or record their vocabularies in the P0 step 0 report as WC-5.2 already does for workflow.
- Priority: Medium. Quality impact: completeness +0.3.

### F-04 Resume flags are unreachable through the two retry routes the spec allows
- Severity MAJOR, graded **Medium**. Expert: Cockburn, Whittaker (Sequence).
- Location: WC-6 (`spec:66`), "One output location per Task" (`spec:78`), item 18 (`spec:341`), rows `spec:91`, `spec:92`, `spec:97`, `spec:98`, `spec:113`, `spec:122`.
- Issue: a retry reuses its Task text (WC-6), and whether the text can change is UNVERIFIED, so a `--retry-of` run cannot add a resume flag. A new Task is the other route, but `spec:78` says a location is "never shared with a concurrent or sibling Task". "Sibling" is not defined, so whether a new Task may resume from a settled Task's location is neither allowed nor refused. Six rows promise a resume flag that no allowed route can pass.
- Recommendation: state that a new Task may reuse a settled Task's location when it passes the command's resume flag and no other Task is running there. Rationale: matches the fixed-location rule already given for cleanup-audit.
- Priority: Medium. Quality impact: consistency +0.4.

### F-05 No coordinator-side requirement for a worker that never reports
- Severity MAJOR, graded **Medium** (a requirement the document never states). Expert: Cockburn, Nygard.
- Location: 1.4 item 2 (`spec:46`), 2.3 (`spec:75-81`), step 2 (`spec:220`), item 11 (`spec:334`).
- Issue: `spec:46` says "Section 2 covers both cases" (the `agentWait` stall and the missing report). Section 2 prevents the stall at the command (WC-2) and defines what happens after `worker_done` (`spec:75`). It never says what a coordinator does when `agentWait` is non-null or no `worker_done` arrives. Step 2 only fails an acceptance run. Orca's own proof-of-stall rule (CAPS:126) and "never release on silence" (CAPS:111) are not adopted. Item 11 (no run-time bound) makes this a live gap.
- Recommendation: add one coordinator duty: on non-null `agentWait` read the transcript, and either `reply` to the question, or stop and retry only on the positive-proof conditions of CAPS:126. Rationale: closes the overstated sentence at `spec:46`.
- Priority: High. Quality impact: completeness +0.5.

### F-10 AC-2.2's cli-eval example cannot observe a blocked contract under WC-4.2
- Severity MINOR-to-MAJOR, graded **Medium**. Expert: Adzic, Whittaker (Zero/Empty).
- Location: AC-2.2 (`spec:240`), WC-4.2 (`spec:64`), cli-eval row (`spec:112`).
- Issue: the example `/sc:cli-eval run --unattended` with no `--suite` passes no `--report-dir`. WC-4.2 stops such a run before any work with no file written, so the pass condition "contract `status: blocked`" cannot be seen. Which stop wins when both a missing location and a missing gate input apply is not stated.
- Recommendation: add `--report-dir <dir>` to the example and say the refusal comes first when both apply.
- Priority: Low. Quality impact: testability +0.2.

### F-12 The AC-C1 scan has blind spots against SA-2 and WC-8
- Severity MINOR-to-MAJOR, graded **Medium**. Expert: Crispin.
- Location: code block 1 (`spec:204-209`), notation `ORCA` (`spec:192`), SA-2 (`spec:172`), WC-8 (`spec:68`).
- Issue: the pattern is `grep -rnE` without `-i` and matches only `orca` or `orca-ide` followed by `orchestration|worktree|terminal|agent`. The spec's own notation and Orca's guide examples are upper case (`ORCA orchestration task-create`, CAPS:86; `ORCA orchestration worker-start`, CAPS:116). A command that copies the contract's brief template with `ORCA orchestration worker-start` passes AC-C1 while violating WC-8. `orca-ide status`, `orca open` and `orca send` are also not matched.
- Recommendation: use `-i` and widen the verb group to any word after `orca(-ide)?`. Rationale: the check then matches the requirement it guards.
- Priority: Medium. Quality impact: testability +0.3.

### F-13 Unattended remediation inside tasklist and reflect leaves one gate without a resolution
- Severity MAJOR, graded **Medium**. Expert: Wiegers.
- Location: tasklist row (`spec:130`), reflect row (`spec:96`), WC-2.2 (`spec:62`).
- Issue: WC-2.2 requires every gate to resolve by default, flag or blocked. The reflect row converts the `[yes / no]` offer to the headless auto-accept rule. The tasklist row passes `--unattended` to each reflect "so the headless rule applies". Stage 10.5 also halts on `needs_human_decision` items (INV-B:209), and the headless rule is documented only for auto-fixable registers (INV-B:109). The resolution for those items is not stated. The tasklist row also makes an automatic remediation hand-off run per phase, where INV-B:215 recommended dropping `--remediate`; the effect is not discussed.
- Recommendation: state in the tasklist row that a `needs_human_decision` item resolves as blocked, and that unattended remediation only writes files under the output directory.
- Priority: Medium. Quality impact: completeness +0.3.

### F-14 AC-0.4 assumes adversarial prints its contract path
- Severity MINOR-to-MAJOR, graded **Medium**. Expert: Adzic.
- Location: AC-0.4 (`spec:233`), adversarial row (`spec:91`), WC-5.2 (`spec:65`).
- Issue: the pass rule for adversarial is "the contract file the command printed". No inventory line says adversarial prints a path; the contract lands at one of two layouts (INV-A:35, INV-A:60). If nothing is printed, WC-5.2 has no file to judge and a healthy run is recorded `failed`, and the AC says that result "reopens section 1".
- Recommendation: add a fallback: look for `return-contract.yaml` under `<output>/adversarial/` and `<output>/adversarial/adversarial/`.
- Priority: Medium. Quality impact: testability +0.3.

## === ARCHITECTURE ANALYSIS ===

### F-06 One contract file serves two audiences
- Severity MAJOR, graded **Medium**. Expert: Fowler.
- Location: `spec:18` (commands contain no Orca calls), `spec:54` (every command's section points to `WORKER-CONTRACT.md`), SA-2 exemption (`spec:172`), WC-7 (`spec:67`).
- Issue: `WORKER-CONTRACT.md` is to hold command-side rules (gate resolution, report, resume) and worker-session rules (`heartbeat`, `ask`, `worker_done`, `check`). Every command's section tells the model to read it, so a command run, and any subagent it spawns, reads Orca verbs that WC-7 reserves for the top-level session. AC-C1 exempts the file by name, which hides the boundary instead of keeping it.
- Recommendation: two files or two clearly marked parts; the command sections point only to the command-side part. Rationale: keeps `spec:18` true in the text the commands actually load.
- Priority: Medium. Quality impact: consistency +0.3.

### F-07 The contract schema has no version or compatibility rule
- Severity MINOR-to-MAJOR, graded **Medium**. Expert: Newman.
- Location: WC-4.3 (`spec:64`).
- Issue: existing contracts gain fields (`command`, a four-value `status`) with no version rule. Consumers exist: workflow's contract is versioned 1.1 (INV-B:272) and troubleshoot's contract is read by the `task-unified` caller (INV-B:242). A changed status vocabulary can break such a reader.
- Recommendation: add `contract_version` to the required fields and say existing versions are kept or bumped explicitly.
- Priority: Medium. Quality impact: consistency +0.2.

### F-08 WC-4.4 deletes whatever file sits at the contract path
- Severity MAJOR, graded **Medium**. Expert: Nygard, Whittaker (Sequence).
- Location: WC-4.4 (`spec:64`), `spec:78`, R3 (`spec:37`).
- Issue: the command removes "a contract an earlier attempt of its own Task left". The command has no Task id (R3), so it cannot tell its own Task's file from another run's file; it removes whatever is there. Safety rests only on the coordinator's one-location rule (`spec:78`).
- Recommendation: rename the old file to `return-contract.yaml.prev` instead of deleting. Rationale: same staleness effect, no loss.
- Priority: Medium. Quality impact: robustness +0.3.

### F-09 Background polling for build and test has no fallback
- Severity MINOR-to-MAJOR, graded **Medium**. Expert: Nygard.
- Location: WC-10 (`spec:70`), rows `spec:109`, `spec:131`, AC-1.2 (`spec:236`), item 22 (`spec:345`).
- Issue: P1 requires build and test to run as background jobs polled in waits of at most 240 s, and AC-1.2 requires the transcript to show it. Feasibility is UNVERIFIED (item 22). If a project command cannot be backgrounded, P1 cannot pass and no alternative (foreground with a bounded timeout and a `partial` report) is given. P1 is also described as "mechanical" (`spec:184`).
- Recommendation: state the fallback, or move these two commands to the phase after item 22 is settled.
- Priority: Medium. Quality impact: completeness +0.2.

### F-11 The unattended section is defined for command files, but nested calls go to skills
- Severity MAJOR, graded **Medium**. Expert: Fowler, Whittaker (Divergence).
- Location: `spec:54`, `spec:62` (WC-2.6), `spec:80`, `spec:235` (AC-1.1), nested table `spec:138-150`, E3 (`spec:25`).
- Issue: the section is added to command files and the support check reads the command file. The proven route is skill-direct (E3), and the nested table lists skill callees such as `sc:adversarial-protocol` and `sc:troubleshoot-protocol`. A skill never reads its command's section. WC-2.6 speaks of a skill "that has its own `## Unattended mode` section", but nothing places one there or says how a skill protocol learns the mode. Several gate conversions (reflect's `--remediate` rule is in a skill ref, `spec:96`) must live in skills.
- Recommendation: say where the text lives for skill-backed commands (a pointer in the skill, or the command passes the resolved gate values as arguments).
- Priority: High. Quality impact: consistency +0.4.

## 5. Guard Condition Boundary Table (FR-8, FR-9, FR-10)

Trigger: the spec contains thresholds, boolean guards and sentinel comparisons. Constructed by Nygard, completeness checked by Crispin, attacked by Whittaker. A GAP row is graded by consequence (FR-8) and a blank behaviour is graded the same way (FR-9). No GAP below names a concrete wrong outcome that needs no further assumption, so each is Medium and appears in section 10.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5.1 usable-report test | `spec:65` | Zero/Empty | file missing, empty or not YAML | not usable | `--outcome failed` | OK |
| WC-5.1 usable-report test | `spec:65` | One/Minimal | `status: succeeded` only, no `command` | usable | `succeeded`; WC-4.3 and `spec:222` then require `command` (F-03, F-01) | GAP |
| WC-5.1 usable-report test | `spec:65` | Typical | full contract, status `partial` | usable | `succeeded`, body says `partial` | OK |
| WC-5.1 usable-report test | `spec:65` | Sentinel Value Match | `status: blocked`, `blocked_question: "   "` | not usable | `failed` (empty question; `spec:222` strips) | OK |
| WC-5.1 usable-report test | `spec:65` | Legitimate Edge Case | legacy status word or `running` | not usable | `failed`, or WC-5.2 when no phase contract yet | OK |
| WC-5.2 no-contract rule | `spec:65` | Zero/Empty | report file missing or empty | false | `failed` | OK |
| WC-5.2 no-contract rule | `spec:65` | Typical | file non-empty, no STOP line | true | `succeeded` | OK |
| WC-5.2 no-contract rule | `spec:65` | Legitimate Edge Case | pre-existing non-empty file, command died silently | true | Unspecified (no mtime test; F-02) | GAP |
| WC-5.2 no-contract rule | `spec:65` | Sentinel Value Match | "path the command printed" and nothing printed | cannot evaluate | Unspecified (F-14) | GAP |
| WC-10 wait cap 240 s | `spec:70` | Typical | one wait of 90 s | within cap | proceeds | OK |
| WC-10 wait cap 240 s | `spec:70` | Maximum/Overflow | pr-submit 600 s default wait | over cap | P4 measures and splits (`spec:122`) | OK |
| WC-10 wait cap 240 s | `spec:70` | Maximum/Overflow | cli-eval up to 3600 s | over cap | split into waits of at most 240 s (`spec:112`) | OK |
| WC-10 wait cap 240 s | `spec:70` | Legitimate Edge Case | parallel Agent batch over 240 s | exempt | silence is not a stall | OK |
| WC-10 wait cap 240 s | `spec:70` | Legitimate Edge Case | build or test cannot run in background | cannot meet cap | Unspecified (F-09) | GAP |
| `--unattended` switch | `spec:53` | Zero/Empty | flag absent | false | attended, unchanged (SA-1) | OK |
| `--unattended` switch | `spec:53` | Typical | standalone unquoted token | true | mode on | OK |
| `--unattended` switch | `spec:53` | Sentinel Value Match | token inside a quoted topic | false | not switched | OK |
| `--unattended` switch | `spec:53` | Legitimate Edge Case | token inside an unquoted multi-word topic, or `--unattended=false` | ambiguous | Unspecified (N-1) | GAP |
| WC-4.1/4.2 placement | `spec:64` | Zero/Empty | no location given, command needs one | none | refusal in chat, no file, worker `failed` | OK |
| WC-4.1/4.2 placement | `spec:64` | Typical | existing directory given | dir | `<dir>/return-contract.yaml` | OK |
| WC-4.1/4.2 placement | `spec:64` | Legitimate Edge Case | location inside `.git/` or a distributable `.claude` folder | forbidden | refusal (SA-5) | OK |
| WC-4.1/4.2 placement | `spec:64` | Legitimate Edge Case | missing location and missing gate input together | both | Unspecified which wins (F-10) | GAP |
| Support check | `spec:80` | Zero/Empty | no section or no `WORKER-CONTRACT.md` | false | flag not passed, not dispatched unattended | OK |
| Support check | `spec:80` | Typical | section and file present | true | dispatch with the flag | OK |
| Support check | `spec:80` | Legitimate Edge Case | worker started with `--on <environment>` | host-dependent | check on that host or do not dispatch | OK |
| Step 4 contract test | `spec:222` | Zero/Empty | contract empty | `test -s` fails | fail | OK |
| Step 4 contract test | `spec:222` | Typical | matching `command`, valid status, newer mtime | pass | pass | OK |
| Step 4 contract test | `spec:222` | Sentinel Value Match | `command` differs only in prefix or quoting | assertion fails | Unspecified canonical form (F-01) | GAP |
| WC-2.5 gate-opening flag | `spec:62` | Typical | `--strategy intent` | refused | `failed` with reason (`spec:124`) | OK |
| WC-2.5 gate-opening flag | `spec:62` | Legitimate Edge Case | another run-time-question flag not named | rule is general | refused like the research flag | OK |
| task confidence guard | `spec:129` | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| task confidence guard | `spec:129` | Sentinel Value Match | confidence exactly 0.70 | not below | proceeds (row says "below 0.70") | OK |
| task confidence guard | `spec:129` | Legitimate Edge Case | caller passes `--compliance` override (INV-B:199) | WC-2.2 precedence says flag wins | row says blocked (N-9) | GAP |
| AC-C5 removed-lines listing | `spec:201`, `spec:214` | Zero/Empty | no removed lines | prints nothing | pass | OK |
| AC-C5 removed-lines listing | `spec:201`, `spec:214` | Legitimate Edge Case | local `master` behind `origin/master` | false positives | Unspecified (N-4) | GAP |

Classes left out with the reason: Maximum/Overflow for WC-5.1 and for the step 4 test (a small YAML file has no capacity bound); Zero/Empty for WC-10 (a zero-length wait is not a step); One/Minimal for the switch, placement, support check and WC-2.5 (no distinct one-element case exists); Maximum/Overflow for the switch, placement, WC-2.5 and AC-C5 (no numeric limit is stated); Typical and Maximum for the support check edge (covered by its rows); Maximum/Overflow for the confidence guard (confidence is capped at 1.0 and the guard is a lower bound).

FR-10 check: every guard listed above has its rows or a stated omission, and every cell is populated, so the table is complete and synthesis was not blocked. FR-9: seven entries read "Unspecified" and each is covered by a finding (F-02, F-14, F-09, N-1, F-10, F-01, N-4). Nygard, Crispin and Whittaker all took part.

## 6. Pipeline Dimensional Analysis and Quantity Flow Diagram (FR-17 to FR-21)

Trigger: the classification stage splits 43 commands into groups and the phase stage assigns them (output count differs from input count at each stage). Fowler annotated counts; Whittaker attacked each divergence point. Result: every count reconciles; no dimensional mismatch, so nothing is CRITICAL.

```text
[Source: 43 commands = 21 (INV-A:3) + 22 (INV-B:3)] --> [Stage 1: classify per INV-A:73, INV-B:278]
        ready 5+5 = 10 ; needs-change 13+14 = 27 ; coordinator-only 3+3 = 6         (10+27+6 = 43, spec:84)
                                                    |
                                                    v
                         [Stage 2: remove coordinator-only (spec:153-162)] --> 37 worker-capable (10+27)
                                                    |
                                                    v
                         [Stage 3: phase assignment (spec:183-187)]
        P0: 0 edited (3 smoke runs)   P1: 8 needs-change + 6 ready = 14   P2: 11 needs-change + 4 ready = 15
        P3: 4   P4: 3   load: usage-line only (P1)            14+15+4+3 = 36 ; 36 + load = 37
                                                    |
                                                    v
        [Consumer AC-1.1 (spec:235): asserts 14 sections in P1, none for load and the 6 coordinator-only]   count matches
        [Consumer 3.1 table (spec:91-100): 10 rows]  [Consumer 3.2 table (spec:107-133): 27 rows]          counts match
```

Consumers use N = 14, 10 and 27 where the producer yields 14, 10 and 27; no consumer assumes the pre-filter count of 43.

## 7. Adversarial analysis (Whittaker)

Attack coverage (five methodologies): Zero/Empty (empty report, empty blocked question, empty location: handled by WC-4.2, WC-5.1; one finding F-10), Divergence (F-11), Sentinel Collision (F-01, N-1), Sequence (F-02, F-04, F-08), Accumulation (retry circuit breaker is acknowledged at `spec:66`, `CAPS:116`, `CAPS:80`: no break; the count flow in section 6: no break).

- I can break this specification by **Sequence Attack**. The invariant at **WC-5.2 (`spec:65`)** fails when **a fixed-location report pre-exists and the command exits early without a STOP line**. Concrete attack: before, `PROJECT_INDEX.md` exists (mtime T0) and Task B depends on Task A; Task A starts at T1; the command aborts at T1+5 s with a tool error; after, the worker finds the file non-empty and no STOP line and sends `--outcome succeeded` with `--report-path PROJECT_INDEX.md`; Orca settles Task A and Task B becomes startable on a stale index. Severity MAJOR, graded Medium (F-02).
- I can break this specification by **Sequence Attack**. The invariant at **WC-6 with `spec:78` (`spec:66`)** fails when **a coordinator wants to resume a failed run**. Concrete attack: Task A (`/sc:adversarial ... --output out`) fails at phase 2; `--retry-of` reuses the Task text without `--pipeline-resume`, so it re-runs in place and overwrites the manifest; a new Task with `--pipeline-resume` and the same `--output` is a "sibling" sharing a location, which `spec:78` forbids; the resume capability is never used. Severity MAJOR, graded Medium (F-04).
- I can break this specification by **Sequence Attack**. The invariant at **WC-4.4 (`spec:64`)** fails when **a Task is started at a location another Task used**. Concrete attack: Task A completed with `out/return-contract.yaml`; Task B is briefed with `--output out` by mistake; B removes A's contract first and then stops at a refusal; the coordinator now holds a completed Task A with no contract on disk. Severity MAJOR, graded Medium (F-08).
- I can break this specification by **Divergence Attack**. The invariant at **WC-2.6 and AC-1.1 (`spec:62`, `spec:235`)** fails when **the callee is a skill, not a command**. Concrete attack: brainstorm (P1) calls `sc:adversarial-protocol` through the Skill tool; the section exists only in adversarial's command file; the skill protocol never sees the mode and an `--interactive` default or a future gate fires unconverted, while AC-1.1 passes because the command file has its section. Severity MAJOR, graded Medium (F-11).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **the token rule (`spec:53`)** fails when **`--unattended` appears unquoted inside a multi-word topic**. Concrete attack: `/sc:tdd explain the --unattended flag handling` has the token outside quotes, the command switches mode, and a topic-only run resolves as blocked instead of asking a person. Severity MINOR (N-1).

## 8. Citation check results

- Counts: ready 10, needs-change 27, coordinator-only 6, total 43, match `INV-A:73` and `INV-B:278`; P1 14, P2 15, P3 4, P4 3 plus load match the rows.
- Inventory line references checked in sections 1-4 and the UNVERIFIED list: no wrong line found.
- UNVERIFIED in this review (no file in the workspace): `spec:25` return-contract line, `spec:27` grep result, `spec:36` and `spec:54` `CLAUDE.md` and `install_core.py` lines, `spec:171` `HOW-WE-WORK.md:171,249,254`, `spec:176` `sc-reflect-protocol/SKILL.md:320-322` (no inventory line witnesses it), `spec:189` `core/CLAUDE.md:65`, `spec:274` `qa.md:232` "valid existing operator Ruling" (INV-A:51 and INV-A:66 witness only `:231,233,238`), `spec:222` `pyproject.toml:38`, `spec:331` `Makefile:68-74`.
- Self-description: `spec:337` and `spec:13` say the statements about the earlier citation check have no witness here. Agreed.

## 9. Quality assessment (standard keys, condensed)

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin, gregory, hightower]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.9
  clarity: 8
  completeness: 7.5
  testability: 7.5
  consistency: 8.5
critical_issues: []   # no blocking finding
expert_consensus:
  - decision and rejected alternative are well evidenced
  - counts and phase assignment reconcile
  - acceptance checks are executable; a few depend on unproven prints or formats
improvement_roadmap:
  immediate: [F-01, F-02, F-05, F-11]
  short_term: [F-03, F-04, F-06, F-07, F-08, F-12, F-13, F-14]
  long_term: [F-09, F-10]
adversarial_analysis:
  - {attack: sequence, severity: MAJOR-graded-Medium, location: "spec:65", finding: F-02}
  - {attack: sequence, severity: MAJOR-graded-Medium, location: "spec:66", finding: F-04}
  - {attack: sequence, severity: MAJOR-graded-Medium, location: "spec:64", finding: F-08}
  - {attack: divergence, severity: MAJOR-graded-Medium, location: "spec:62", finding: F-11}
  - {attack: sentinel-collision, severity: MINOR, location: "spec:53", finding: N-1}
```

Advisory (not forced): the spec has numeric thresholds (60 s, 240 s, 300 s, 0.70) and a status state machine; a later review may add `--focus correctness`.

## 10. Follow-up candidates

Medium (warnings, none blocks, none enters the Reviser brief): F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14.

Minor notes:
- N-1 `--unattended` token inside an unquoted multi-word topic, or `--unattended=false`, is ambiguous (`spec:53`).
- N-2 Step 4 and step 6 run locally; for `--on <environment>` workers the mtime and `test -s` checks need the remote host, and clock skew is not addressed (`spec:80`, `spec:222`, non-goal 9 at `spec:262`).
- N-3 Reference collision: "round-1 note 22" (`spec:65`, `spec:233`) reads like item 22 (`spec:345`), which is a different matter; AC-2.6 sits before AC-2.4 (`spec:242-243`).
- N-4 Code block 2 uses local `master` as the merge base (`spec:214`); a stale local `master` lists other people's removals. The fork rule in the project instructions says fork `master` can be ahead (UNVERIFIED here).
- N-5 Section 6 says phases 1-3 need no user decision (`spec:179`) while D4 affects auggie-review and task in P2 (`spec:285`, `spec:185`); a "never" answer would undo the P2 `--post-pr` flag.
- N-6 WC-9 requires one flag per outward class, so pr-submit under D3 (b) needs at least four (PR, commit, push, GitHub post); row `spec:122` names none and defers to D3.
- N-7 spec-panel's installed copy already carries a section that differs from WC-2.4 and WC-4.3 (`spec:128`, `command.md:460-462`); the support check also needs `~/.claude/WORKER-CONTRACT.md`, which `command.md:457` depends on and which P0 creates (`spec:183`). Reconciliation is deferred to P2 by design.
- N-8 Section 3 says "every changed command also gains" the section (`spec:84`), while load is changed and gains none (`spec:184`); the row resolves it.
- N-9 task: a caller `--compliance` override and the "blocked" resolution (`spec:129`, INV-B:199) are not ordered against WC-2.2's flag-first precedence.
- N-10 Plugin command mirrors are covered by neither AC-C1 nor AC-C2 (item 8, `spec:331`).
- N-11 AC-0.4's workflow smoke run creates a package under `.dev/tasks/to-do/<id>/` and no cleanup or disposition is stated (`spec:233`, INV-B:274).

The session that ran this review could not ask the user whether to open an issue for these; this was a worker run with no user turn, so the question is recorded for the coordinator and no issue was created.

## Decisions

| Decision | Options | Rationale |
|---|---|---|
| Grade of every gap that needs a guess | blocking; Medium | Medium, per the FIRST-REVIEW prompt: each needs an assumed implementer choice or a coordinator error, or is a requirement the document never states. |
| Output shape | pure YAML; markdown with a condensed YAML block | Markdown, because the brief wants a cited report; the standard keys are kept in section 9. |
| Quantity Flow Diagram | skip; produce | Produce: classification and phase assignment change counts, which triggers FR-17. |
| Improve step | run; skip | Skip: the brief and the first-review prompt both forbid editing the candidate. |

## Reviser brief

No blocking finding ids. Nothing is to be revised. (Rules for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on every addition; prefer deleting or narrowing to adding; report byte size before and after and bytes added and deleted per finding id; leave Medium and minor findings alone.)

verdict: PASS
