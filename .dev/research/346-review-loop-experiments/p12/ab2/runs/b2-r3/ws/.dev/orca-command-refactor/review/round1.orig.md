review: 1 of 3

# Spec-panel review, round 1: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review; no `--re-review`, no `--baseline`, no `--unattended`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57763 bytes, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not applicable (first review)
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing)
- panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (always active, ordered after Nygard)
- citation keys: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = line N of `.dev/orca-command-refactor/README.md`. These four files were read in this sandbox and every `S:`/`INV-`/`CAPS:`/`README:` line cited below was checked. A citation into a file that is not in the sandbox (`cmd/*`, `sk/*`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml`, `install_core.py`, the codegraph-migration files, Orca guides) is UNVERIFIED here; where the spec carries such a citation only through an inventory line, I treat the inventory as the evidence.
- coverage: whole document (sections 1-9, Decisions, UNVERIFIED items) read; inventories and README read in full; the section 3 command counts, the phase lists and the section 7 checks were recomputed; the Improve step (6) was not run, because the brief assigns only this report and the Boundaries forbid modifying a specification without consent.
- Brief clauses overridden: none.
- Issue question (Review Loop bullet 3): this worker cannot ask the user, so it asks nothing and creates no issue; the follow-up candidates below are recorded for the coordinator to put to the user once.
- `--focus correctness` is not active, so no State Variable Registry is produced. Advisory auto-suggestion: the spec has numeric guard thresholds (60 s readiness, 5 min heartbeat, 4 min waits, 0.70 confidence, depth 1), so a later round may add `--focus correctness`.

## Findings table

| id | grade | expert | one line | location |
|---|---|---|---|---|
| B-1 | blocking | Wiegers | AC-1.1 requires an `## Unattended mode` section on `/sc:load`; the load row and Decisions say it gets no report file and only a usage-line fix | S:195, S:112, S:265, S:76, S:159 |
| B-2 | blocking | Fowler | WC-4 defines `<output-dir>` as the value of `--output`, but `--output` is a file for tdd and init-lite, so the contract path does not exist and AC-2.2 cannot read it | S:62, S:87, S:90, S:200, S:183 |
| M-1 | Medium | Whittaker | `--unattended` has no parse rule and no precedence against opposing flags or on a coordinator-only command | S:51, S:128, S:100, S:227-229 |
| M-2 | Medium | Nygard | No rule for `--unattended` with no output directory, though the contract is written "on every outcome" | S:62, S:73 |
| M-3 | Medium | Nygard | WC-3's `ask` route can supply a flag or Ruling that WC-9 and D2/D4 say must come from the brief or a person | S:61, S:67, S:233-236, S:245 |
| M-4 | Medium | Whittaker | A retry worker for a command that has a resume flag, run without it, rewrites the first attempt's directory | S:64, S:205 |
| M-5 | Medium | Whittaker | WC-4 keeps existing contract fields while WC-5 and Decisions assume a four-value `status` vocabulary | S:62, S:63, S:262 |
| M-6 | Medium | Cockburn | Section 2.3 and the P0 brief template put `--unattended` in the command line, but the flag does not exist until P1 | S:73, S:79, S:158, S:159, S:194 |
| M-7 | Medium | Fowler | Quantity flow: brainstorm and init-lite are in AC-1.1's count but in no phase Commands list (FR-19 label CRITICAL, graded Medium) | S:159, S:195, S:84, S:87 |
| M-8 | Medium | Crispin | `grep -E '^-[^-]'` in AC-C5 and AC-0.3 cannot see a deleted `- ` bullet or `---` line | S:176, S:193 |
| M-9 | Medium | Newman | WC-11 forbids shared default output paths, but two "ready today" commands write fixed ones | S:69, S:85, S:86 |
| M-10 | Medium | Fowler | SA-2 limits the no-Orca rule to commands/skills/agents; AC-C1 also greps `core/`, where P0 adds the contract and an Orca section | S:147, S:172, S:158 |
| M-11 | Medium | Nygard | WC-9 relies on "the command's own explicit flag", which pr-submit and post-release lack and `--post-pr` may not exist | S:67, S:100, S:113, S:114, INV-A:38 |
| M-12 | Medium | Wiegers | README:31 is a rule for this planning run, cited as product evidence for WC-9 and for `/sc:git` | S:67, S:133, README:31 |
| M-13 | Medium | Adzic | The live check in 7.2 has no reply step, so a worker that uses WC-3's `ask` never reaches `worker_done` | S:61, S:182 |
| M-14 | Medium | Wiegers | "43 commands in `cmd/`" and E5 rest on two enumerated scope lists and an unrepeatable grep; UNVERIFIED | S:25, S:76, INV-A:3, INV-B:3 |
| N-1 | minor | Crispin | Two thresholds are unquantified: "well inside" (WC-1) and the 4-5 minute band (WC-10) | S:59, S:68 |
| N-2 | minor | Crispin | AC-C1's raw text contains `\|` inside an ERE | S:172 |
| N-3 | minor | Crispin | AC-1.4's pass condition ("names one fixed path") is not decidable from a `grep -n` | S:198 |
| N-4 | minor | Wiegers | E3 cites `skill-direct` as support while 1.4 says the direct route is unproven | S:23, S:43 |
| N-5 | minor | Crispin | 7.2 step 5 asks for a transcript search for the string `AskUserQuestion` | S:184 |

## === REQUIREMENTS ANALYSIS ===

### B-1 (MAJOR, blocking, priority High, Wiegers)
Texts: AC-1.1 "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (S:195); section 3 intro "Every changed command also gains the `## Unattended mode` section" (S:76); load row, Report "none (see note)", Phase "P1 (usage line only)" (S:112); Decisions "a report file would be an unrequested addition. Only its usage-line defect is fixed" (S:265). `/sc:load` is in section 3.2, so it is inside AC-1.1's scope.
Grading sentence: An implementer who follows the stated text as written builds `/sc:load` with only its usage-line fix and no contract (S:112, S:265), and X is wrong because AC-1.1 (S:195) fails on it; if they instead add the section naming `return-contract.yaml`, they contradict the load row and the Decision. Two stated texts contradict, and the acceptance criterion cannot pass as written.
Recommendation: narrow AC-1.1 to name the exception (every 3.1-3.2 command except `load`), or change the load row and Decision. Prefer the narrowing, one clause.
Quality impact: Testability 6 to 8.

### M-6 (MAJOR label, Medium, priority Medium, Cockburn)
Section 2.3 says the brief carries "the exact command line including `--unattended`" (S:73). The flag is added in P1 (S:159). P0 writes a brief template "listing the section 3.1 flags" (S:158), those flags exclude `--unattended` (S:79-92), and AC-0.4 runs three commands in P0 (S:194).
Why Medium: the sentence "an implementer builds a P0 brief with `--unattended` and the P0 smoke run passes an unknown argument" needs a guess about how an unknown flag is handled, which the spec does not state.
Recommendation: state that the P0 brief omits `--unattended`.

### M-12 (MAJOR label, Medium, priority Low, Wiegers)
README:31 is "No git commits, pushes, PRs or GitHub comments." under "Rules for every worker" of this planning run. The spec cites it as evidence for WC-9 (S:67) and as a reason `/sc:git` is coordinator-only (S:133). It supports neither a product rule nor "unless the brief authorizes".
Recommendation: cite the command lines that perform the outward action; drop README:31 from those two rows.

### M-14 (MAJOR label, Medium, priority Medium, Wiegers) UNVERIFIED
S:76 says "The 43 commands in `cmd/`". The only support is two enumerated scope lists (INV-A:3, INV-B:3); no inventory line shows a directory listing. E5 (S:25) rests on a `grep` the spec says it ran; I cannot repeat it here. This reviewer session's own skill list also names commands in neither inventory (`sc:graph`, `sc:impact`, `sc:issue`) and describes `sc:issue` as creating an Orca worktree. That is outside the sandbox, so it is UNVERIFIED and is not used for grading. If it holds, E5 and the AC-C1 baseline (S:172) are wrong and the finding would become blocking.
Recommendation: re-run the `ls` and `grep` against the live tree before round 2 and record the output.

### Adzic scenarios (state traces)
1. Given `/sc:tdd "auth" --unattended --output docs/auth/TDD.md` (S:200). When the topic-only gate fires, the spec says contract `status: blocked`. Where the file goes is B-2.
2. Given `/sc:cli-eval run --unattended` with no `--suite`, AC-2.2 expects `worker_done --outcome failed`, contract `blocked`, no `agentWait`. Traceable (S:104, S:200). OK.
3. Given `/sc:load --unattended`, B-1 above.

### M-13 (MAJOR label, Medium, priority Medium, Adzic)
7.2 step 3 waits for `worker_done` with `--types "worker_done,escalation,question"` (S:182) and has no step that answers a `question`. WC-3 lets the worker ask (S:61). A worker that asks stays blocked until the coordinator replies; the check as written neither replies nor fails.
Why Medium: WC-3 says "may", so a worker that blocks without asking passes; the failure needs the guess that the worker asks.

## === ARCHITECTURE ANALYSIS ===

### B-2 (MAJOR, blocking, priority High, Fowler)
Texts: WC-4 "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (S:62); init-lite "Brief must pass `--output <file>`" (S:87); tdd "`--output <file>`" and "the TDD at `--output`" (S:90); AC-2.2 `/sc:tdd "auth" --unattended --output <file>` expecting "contract `status: blocked` with a non-empty `blocked_question`" (S:200); 7.2 step 4 reads `<contract>` (S:183); section 2.3 "the output directory, so the report path is known before dispatch" (S:73).
Grading sentence: An implementer who follows the stated text as written writes the tdd contract at `<--output value>/return-contract.yaml`, which is `docs/auth/TDD.md/return-contract.yaml`, and X is wrong because the `--output` value is the TDD file, so that path cannot be created and AC-2.2 step 4 cannot read a contract. WC-4 says `--output` is a directory; the tdd and init-lite rows say it is a file.
Recommendation: define the contract location for file-valued `--output` (for example the file's parent directory, or a separate `--report-dir`), and say which flag spec-panel's new `--output` (S:120) is.
Quality impact: Clarity and Consistency 6 to 8.

### M-2 (MAJOR label, Medium, priority Medium, Nygard)
WC-4 says the contract is written "including stops before any other output exists" (S:62), but the directory comes from the brief (S:73). If `--unattended` arrives with no directory, the spec gives no refusal, default or location. Commands with timestamped default directories (troubleshoot, S:91) have no stated rule either.
Why Medium: the requirement is missing, not contradicted.

### M-3 (MAJOR label, Medium, priority Medium, Nygard)
WC-3 lets the worker "ask the coordinator once ... then re-invoke or resume the command with the answer as a flag" (S:61). WC-9 turns outward actions on "only through the command's own explicit flag written in the brief" (S:67), D4(a) requires the user's own instruction quoted in the brief (S:245), and D2(a) says the worker ends `failed` on a Ruling halt (S:234; non-goal 6, S:218). A coordinator `ask` answer re-invoking with `--post-pr`, or relaying a Ruling, is allowed by WC-3 and excluded by the other three. Not blocking: WC-3 says "may", and the implement row says the Ruling rule is unchanged (S:109).
Recommendation: one sentence in WC-3 that an `ask` answer never turns on a WC-9 action or supplies a Ruling.

### M-4 (MAJOR label, Medium, priority Medium, Newman)
WC-6 says a command with a resume flag "resumes ... when given its resume flag" (S:64). A `--retry-of` worker whose brief omits the flag re-runs into the same directory. AC-3.2 requires exactly that for roadmap: existing `.session-memory.md`, no resume flag, "starts fresh" (S:205), so the first attempt's output in `<dir>` is overwritten or mixed.
Recommendation: say a re-run without the resume flag uses a fresh directory, or refuses when the directory is non-empty.

### M-9 (MAJOR label, Medium, priority Low, Newman)
WC-11: "Default output paths carry a timestamp or the slug the coordinator passes" (S:69). cleanup-audit writes the fixed `.claude-audit/` (S:85, "one audit per worktree at a time") and index-repo writes `PROJECT_INDEX.md` (S:86), yet both are "ready today" with no WC-11 fix. The cleanup-audit row discloses the limit, so no implementer is misled; the requirement and the verdict still disagree.
Recommendation: add "except where a row names a one-at-a-time limit" to WC-11.

### M-10 (MAJOR label, Medium, priority Low, Fowler)
SA-2 covers "command, skill or agent file" (S:147). AC-C1 also greps `src/superclaude/core` (S:172), and P0 adds `WORKER-CONTRACT.md` and "an Orca section" to `HOW-WE-WORK.md`, both in `core/` (S:158, S:52). SA-2 allows an Orca mention as a question-channel example in the contract file; if the example reads `orca orchestration ask`, AC-C1 flags it. The Orca section's content is not described.
Recommendation: align the two scopes and say whether command names may appear in those two core files.

### M-11 (MAJOR label, Medium, priority Medium, Nygard)
WC-9 requires "the command's own explicit flag" (S:67). pr-submit and post-release perform the outward action as their purpose and have no such flag (S:113-114, D3/D4 S:238-247). For auggie-review the row names `--post-pr` (S:100) while INV-A:38 shows only `--no-post-pr`, so the positive flag is UNVERIFIED; and `--unattended --post-pr` meets the implied `--no-post-pr` with no stated precedence.
Recommendation: name the authorizing flag per command or say it is added in the same phase.

## === ADVERSARIAL ANALYSIS (Whittaker) ===
Severity classes follow the panel (CRITICAL/MAJOR/MINOR); the grade column below is by consequence.

1. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:51 / S:227-229 (`--unattended` is the only switch, "cannot misfire on a person")** fails when **the token appears inside a quoted free-text prompt or on a command the spec says gets no mode**. Concrete attack: before: `/sc:troubleshoot "login fails after --unattended is passed"`, person at the keyboard, no flag intended. After: if the parser sees the token, the person's run gains blocked gates and off outward defaults, breaking SA-1 (S:146); if not, the mode silently stays off in a worker brief that quoted it. Same hole for `/sc:git --unattended` (S:128). Grade Medium (M-1): the spec states no parse rule, so the wrong outcome needs a guess.
2. I can break this specification by **Divergence Attack**. The invariant at **S:100 (auggie-review: `--unattended` implies `--no-post-pr`; posting returns only with `--post-pr`)** fails when **both apply**. Concrete attack: brief `--unattended --post-pr`; implied state `no_post_pr=true`, explicit `post_pr=true`; PR comments are posted or not depending on the implementer. Same for `--unattended --interactive` where only some rows say "refused" (S:103, S:110). Medium (M-1, M-11).
3. I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 (contract written on every outcome)** fails when **no output directory is given**. Concrete attack: `/sc:analyze src --unattended`; no directory, contract path undefined, the run stops before any output, `worker_done --report-path` has nothing real to carry (CAPS:73-74). Medium (M-2).
4. I can break this specification by **Sequence Attack**. The invariant at **S:64 (retry must not corrupt the first attempt)** fails when **the retry brief drops the resume flag**. Concrete attack: attempt 1 dies after roadmap wave 2 with files in `<dir>`; retry runs `/sc:roadmap <spec> --unattended --output <dir>` without `--resume`; AC-3.2 (S:205) then specifies "starts fresh" in the same `<dir>`. Medium (M-4).
5. I can break this specification by **Sentinel Collision Attack** (status values). The invariant at **S:62-63 / S:262** fails when **an existing contract's `status` uses another value**. Concrete attack: S:62 says commands that already write a contract "keep their fields"; workflow, reflect, brainstorm and adversarial write `status` (S:261). Their value sets are not in the inventories (UNVERIFIED). A value such as `halted` is not in WC-5's list (S:63), so the outcome mapping has no row for it. Medium (M-5).
6. I can break this specification by **Accumulation Attack**. The invariant at **S:68 (heartbeat every 5 minutes; split waits above 5 minutes into at most 4)** fails when **a single call lasts 4.5-5 minutes**. Concrete attack: heartbeat sent at t=0, one 290 s call, next heartbeat at t=290+; no rule requires a split. Minor (N-1), because the heartbeat's use in Orca's liveness verdict is itself UNVERIFIED (CAPS:130, CAPS:182).

## Guard Condition Boundary Table (Nygard builds, Crispin validates, Whittaker attacks)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| wait-split (WC-10) | S:68 | One/Minimal | 1 s poll | false | no split | OK |
| wait-split (WC-10) | S:68 | Typical | 120 s wait | false | no split, heartbeat between calls | OK |
| wait-split (WC-10) | S:68 | Maximum/Overflow | 3600 s eval | true | waits of at most 4 min (S:104) | OK |
| wait-split (WC-10) | S:68 | Legitimate Edge Case | 270 s and exactly 300 s call | false ("longer than 5 minutes") | none stated for the 4-5 min band | GAP (N-1) |
| `--unattended` switch | S:51, S:227 | Zero/Empty | flag absent | false | today's behaviour (SA-1, S:146) | OK |
| `--unattended` switch | S:51, S:159 | Typical | standalone token on a 3.1/3.2 command | true | mode on | OK |
| `--unattended` switch | S:51 | Sentinel Value Match | token inside a quoted prompt | unspecified | none stated | GAP (M-1) |
| `--unattended` switch | S:128 | Legitimate Edge Case | token passed to a section 4 command | unspecified | "get no mode", no refusal stated | GAP (M-1) |
| `--unattended` switch | S:100, S:103 | Legitimate Edge Case | with `--post-pr` or `--interactive` | both apply | stated only for rows that say "refused" | GAP (M-1) |
| output directory (WC-4) | S:62, S:73 | Zero/Empty | none passed | unspecified | none stated | GAP (M-2) |
| output directory (WC-4) | S:62 | Typical | directory passed | true | contract at `<dir>/return-contract.yaml` | OK |
| output directory (WC-4) | S:62, S:87, S:90 | Legitimate Edge Case | `--output` is a file | `<file>/...` | contract path not definable | GAP (B-2) |
| outcome map (WC-5) | S:63 | Typical | `succeeded`, `failed`, `partial`, `blocked` | mapped | succeeded, failed, succeeded, failed | OK |
| outcome map (WC-5) | S:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| outcome map (WC-5) | S:62, S:63 | Sentinel Value Match | existing contract with another `status` value | unspecified | none stated | GAP (M-5) |
| outward default off (WC-9) | S:67 | Typical | push/post default under `--unattended` | off | off | OK |
| outward default off (WC-9) | S:100 | Legitimate Edge Case | explicit flag plus implied-off flag | both apply | precedence not stated | GAP (M-11) |
| outward default off (WC-9) | S:113-114 | Legitimate Edge Case | command whose purpose is the action | no own flag | none stated | GAP (M-11) |
| confidence gate (task) | S:121 | Zero/Empty | 0.0 | true | blocked | OK |
| confidence gate (task) | S:121 | Typical | 0.5 | true | blocked | OK |
| confidence gate (task) | S:121 | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| retry (WC-6) | S:64, S:205 | Legitimate Edge Case | retry of a resumable command, flag omitted, same directory | fresh run into used directory | not stated | GAP (M-4) |
| additivity check | S:176, S:193 | Zero/Empty | empty diff | false | prints nothing, passes | OK |
| additivity check | S:176 | Sentinel Value Match | deleted `- ` bullet or `---` line | false (regex skips `--...`) | passes although a line was removed | GAP (M-8) |
| nesting depth (WC-8) | S:66, S:249-253 | Typical | depth 1 | true | worker cannot start workers | OK |
| nesting depth (WC-8) | S:249-253 | Maximum/Overflow | depth raised (D5 b) | false | WC-8 still forbids | OK |

Classes left out: wait-split Zero/Empty (a zero-length wait blocks nothing) and Sentinel (no sentinel); output directory One/Minimal and Maximum (no size limit applies); outcome map Maximum and One (the status set is closed and finite); outward default Zero/Empty and Maximum (the guard is boolean); confidence gate Sentinel (the value is a number) and Maximum (1.0 behaves as Typical above 0.70); retry Zero/Empty (no attempt, nothing to retry); additivity One/Minimal and Maximum (not input-sized); nesting depth Zero/Empty (a malformed setting falls back to 1, CAPS:100) and Sentinel (none).
FR-8/FR-9 grading: every GAP above names no concrete wrong outcome that follows with no further assumption except B-2 (GAP row, `--output` is a file); the others are Medium or minor. The table is complete (every guard enumerated, every class given a row or a reason), so FR-10 is met.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler leads, Whittaker attacks)
Trigger met: a multi-stage flow where counts differ (inventories to verdict split to phases to checks).

```text
[Source: 43 commands (INV-A 21 + INV-B 22; S:76)]
   --> [Stage 1: verdict split] --> 10 ready (S:81-92) + 27 change (S:97-125) + 6 coordinator-only (S:131-137) = 43   (conserved)
   --> [Stage 2: phase assignment]
         P1 commands list: 9 (analyze, build, business-panel, design, document, explain, index, test, load) + 4 fixes = 13   (S:159)
         P2 list: 15   (S:160)      P3 list: 4   (S:161)      P4 list: 3   (S:162)      listed total 35
         NOT LISTED in any phase: brainstorm, init-lite (3.1 "None", S:84, S:87)                      <-- 10 + 27 - 35 = 2
   --> [Consumer A: P1 scope sentence "every command in sections 3.1 and 3.2" (S:159)]   expects 37
   --> [Consumer B: AC-1.1 section on every 3.1-3.2 command (S:195)]                      expects 37, but load gets none (B-1)  <-- MISMATCH
   --> [Consumer C: section 4 exclusion (S:195)]                                          expects 0 of 6
```
Concrete scenario: an implementer who builds P1 from the Commands column produces 13 sections and none for brainstorm and init-lite, while AC-1.1 expects 37. FR-19 would label this CRITICAL; graded by consequence it is Medium (M-7), because the scope sentence in the same row resolves it with the reading that the column lists commands with extra work. Recommendation: say that brainstorm and init-lite get only the section, in P1. The 43 = 10 + 27 + 6 arithmetic and the P2 count of 15 both check out.

## Medium and minor items not detailed above

### M-1, M-5, M-7, M-8 (Medium)
Detailed in the adversarial section and the quantity flow diagram. M-8: `grep -E '^-[^-]'` (S:176, S:193) misses a deleted line whose text starts with `-`: a removed list item `- foo` appears in a diff as `-- foo`, a removed `---` as `----`. Table rows (`-| ...`) are caught, so AC-0.3 works for routing rows but AC-C5 does not for command files, which are mostly bullets. The check can print nothing while SA-4 (S:149) is broken. Fix: `grep -E '^-' | grep -vE '^---'`, or a count of deleted lines.

### Minor notes
- N-1: "well inside" the 60 s limit (S:59) and the 4-5 minute band (S:68) have no number.
- N-2: the raw `\|` in AC-C1 (S:172) is a markdown table escape; pasted into a shell, `\|` in ERE is a literal pipe and the check passes vacuously. Give the command outside a table.
- N-3: AC-1.4 (S:198) says "names one fixed path" but the check is a `grep -n`; state the expected output line.
- N-4: E3 (S:23) offers `invocation_method: "skill-direct"` as support, and 1.4 (S:43) says the direct route is unproven; the two are reconcilable but read as conflicting.
- N-5: step 5 (S:184) searches a transcript for the string `AskUserQuestion`, which also appears when a skill file is read; say "tool call named".

## Consensus and disagreements
- Consensus: the decision (S:13-25), the rejected alternative (S:28-39), the evidence-strength statement (S:41-45), the inventory totals and phase lists are internally sound; the section 3 counts reconcile. The Orca facts the spec leans on match CAPS:44-52, 58-61, 72-77, 97-103, 145-149.
- Disagreement kept: Wiegers would grade M-3 and M-11 blocking for safety; the grading rule keeps them Medium because WC-3 says "may" and the Ruling and posting defaults are off in the other rows (S:109, S:100).

## Follow-up candidates (Medium and minor; none triggers a revision)
M-1 to M-14 and N-1 to N-5 above. Open an issue for them only if the user says so; this run recorded the list and asked nothing.

## Reviser brief
Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

Blocking findings:
- B-1. Texts: AC-1.1 at S:195, "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"; the load row at S:112, Report "none (see note)", Phase "P1 (usage line only)"; the Decision at S:265, "a report file would be an unrequested addition. Only its usage-line defect is fixed." Wrong outcome: an implementer who follows the stated text as written builds `/sc:load` with only its usage-line fix and no contract, and AC-1.1 fails on it; if they instead add the section naming `return-contract.yaml`, they contradict the load row and the Decision. Two stated texts contradict, and the acceptance criterion cannot pass as written.
- B-2. Texts: WC-4 at S:62, "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; the tdd row at S:90, "`--output <file>`"; the init-lite row at S:87, "`--output <file>`"; AC-2.2 at S:200, "`/sc:tdd "auth" --unattended --output <file>`" expecting "contract `status: blocked` with a non-empty `blocked_question`". Wrong outcome: an implementer who follows the stated text as written writes the tdd contract at `<--output value>/return-contract.yaml`, a path under the TDD file that cannot be created, and AC-2.2 step 4 (S:183) cannot read a contract. WC-4 says `--output` is a directory; the tdd and init-lite rows say it is a file.

verdict: FAIL
