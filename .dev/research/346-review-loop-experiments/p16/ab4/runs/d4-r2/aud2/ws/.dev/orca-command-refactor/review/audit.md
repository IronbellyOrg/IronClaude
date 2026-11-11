review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (/sc:spec-panel, critique mode)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (format: standard; one review whatever `--iterations` says)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `520642eef4a21c603b07d310309b173eed3bbf84e2a66e5c9d61cdc65c86fe24`
- baseline: none given, none needed (first review of the whole document); prior report: none
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full), with the grading check applied to every finding
- brief clauses overridden: none
- coverage: whole document, all 9 sections plus Decisions and UNVERIFIED; every `INV-A:N`, `INV-B:N` and `CAPS:N` citation I spot-checked against `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (about 60 of them, all section 3 and 4 rows, E1-E6, R1-R5, WC-1 to WC-12). Counts re-derived (see Quantity check). Citations to `cmd/`, `sk/`, `src/superclaude/cli/install_core.py`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, `Makefile`, `.dev/codegraph-migration/...`, `.dev/evals/...` and Orca's installed files are UNVERIFIED: none of those files exist inside the workspace (`.dev/orca-command-refactor/README.md:11-17` lists them as evidence a worker may read, but the sandbox holds only the README, the three inventories and the spec).

## Quality assessment (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 7 | WC-1..WC-12 and the per-command tables are precise; several path and scope rules are stated in two places that differ (F-01, F-02). |
| Completeness | 7 | Every one of 43 commands is placed; refusal outcome, contract location without an output flag and some acceptance checks are missing (F-02, F-03, F-07). |
| Testability | 7 | Section 7 gives runnable checks for most requirements; WC-3, WC-6, WC-12 and the cli-eval part of WC-10 have none (F-07); AC-C1 conflicts with SA-2 (F-06). |
| Consistency | 6 | Internal count and citation consistency is good; scope-of-section and authorization rules diverge between sections (F-01, F-05, F-08). |

## === REQUIREMENTS ANALYSIS ===

Experts in panel order: Wiegers (lead), Adzic, Cockburn. Whittaker attacks follow in the Adversarial section. Nothing below is blocking: each item either needs a guess between two readings the text allows, or is a requirement the document never states (grading check, `document_review_loop_prompts.md:31`).

**F-01 [MAJOR label, graded Medium] Which commands gain `## Unattended mode` and a contract is stated three different ways. Expert: Wiegers. Priority: Medium.**
- `spec:76` says only commands whose row "names an unattended-mode change" gain the section, and lists brainstorm, init-lite, load and the P4 commands as exceptions. `spec:159` and `spec:195` (AC-1.1) use a wider set: every command whose row names "a P1 change", which includes the small fixes to adversarial, cleanup-audit and index-repo (`spec:83,85,86`). Those three rows name a filename fix, a report-name fix and an output-location statement, not an unattended-mode change.
- WC-4 (`spec:62`) writes a contract "in unattended mode" for cleanup-audit (`.claude-audit/return-contract.yaml`) and index-repo (`PROJECT_INDEX.return-contract.yaml`), which needs `--unattended` and so the section. WC-4 also names init-lite as a command whose `--output` file gets `<output-file>.return-contract.yaml`, while `spec:76` and `spec:87` say init-lite gains no section and changes nothing.
- Outcome: an implementer who follows `spec:76` does not give adversarial, cleanup-audit or index-repo the section; AC-1.1 (`spec:195`) then fails for them. An implementer who follows WC-4 adds a contract to init-lite that `spec:76` forbids. Both depend on picking a reading, so Medium.
- Recommendation: state one rule (suggested: every command with a row in sections 3.1-3.2 that is dispatched with `--unattended` has the section; init-lite and brainstorm are the named exceptions) and drop init-lite from WC-4's file-output example.
- Quality-impact estimate: removes the one place where AC-1.1 can fail on a reading dispute.

**F-02 [MAJOR label, graded Medium] "Report file known before dispatch" (WC-4) is not achievable for many P1-P3 commands as written. Expert: Wiegers, Adzic. Priority: Medium.**
- WC-4 (`spec:62`) derives the contract path from a directory the coordinator passes (`--output` / `--output-dir`) and lists exceptions only for tdd, init-lite, cleanup-audit, index-repo, adversarial and workflow. Section 3.2 rows for research (`spec:116`: "contract naming the generated `claudedocs/research_*.md` path"), recommend (`spec:115`), review-translation (`spec:117`), task (`spec:121`), save (`spec:119`), cli-eval (`spec:104`), cli-portify (`spec:105`: "file location unnamed"), implement (`spec:109`: "beside the ledger") and the P1 rows that say only "add an output path" (`spec:99,101,102,106-108,111,123`) never say whether the new flag is a directory or a file or where the contract goes. Several defaults carry a timestamp or generated id (`INV-B:92,127-135` via `spec:116`; pr-submit's default dir, `INV-B:92`).
- The check that depends on it: AC 7.2 step 3 (`spec:182`) passes only if the `worker_done` report path "is the WC-4 contract path". For research or review-translation no WC-4 path exists to compare against.
- Also unstated: what the command does when `--unattended` is passed but no directory is supplied or the directory cannot be written (empty or unwritable input). The `/sc:spec-panel` command definition in this sandbox refuses before any work in that case and prints the refusal in chat only (`command.md:460`); the spec has no equivalent rule.
- Recommendation: add one rule to WC-4: every command with no output directory flag gets one in its row (directory form), the contract is `<dir>/return-contract.yaml`, and `--unattended` without a writable directory is refused before work, status line printed in chat.

**F-03 [MAJOR label, graded Medium] The outcome of a refused flag is undefined. Expert: Adzic. Priority: Medium.**
- Section 3 says `--interactive` is refused under `--unattended` for cleanup and improve (`spec:103,110`), roadmap (`spec:118`), `--watch` for test (`spec:123`), `--monitor 1` for pr-submit (`spec:114`), `--mode socratic` for business-panel (`spec:102`) and `--format interactive` for explain (`spec:108`). WC-2 (`spec:60`) defines only three resolutions for a gate: default, caller flag, blocked. "Refused" is none of them, and WC-4/WC-5 (`spec:62-63`) define `status` and `--outcome` but not which value a refusal takes (`failed` or `blocked`, and whether `blocked_question` is filled).
- AC-2.2 (`spec:200`) lists cleanup and improve among the six commands that "never write `blocked`", so a refusal there would have to be `failed`; for pr-submit (blocked HALTs) the same table is silent. The reader must guess.
- Recommendation: add to WC-2 "a refused flag combination is `status: failed` with the reason in the report; the contract is still written".

**F-07 [MINOR/Medium] Requirements without an acceptance check. Expert: Wiegers (traceability), Crispin-style check. Priority: Medium.**
- WC-3 (ask / resume by message ID), WC-6 (retry with `--retry-of` must not corrupt the first attempt), WC-12 (`consumer_fenced`) and the cli-eval half of WC-10 (4-minute wait split) appear in no AC in section 7 (`spec:167-210`). AC-4.3 (`spec:210`) tests WC-10 for pr-submit only. WC-6 in particular is a data-integrity rule (fresh directory or resume) and nothing exercises a retry.
- Recommendation: add one retry run to 7.2 (kill a worker mid-run, `worker-start --retry-of`, assert the first attempt's files are unchanged) and one AC per remaining requirement, or mark them as not machine-checked.

**F-05 [MAJOR label, graded Medium] Authorization of outward actions: WC-9 already assumes D4 option (a), and D4 (a) uses a weaker trust rule than D2. Expert: Cockburn (stakeholder / actor), Wiegers. Priority: Medium.**
- WC-9 (`spec:67`) says a default that pushes, posts, installs or opens a PR "turns on only through the command's own explicit flag written in the brief". That is D4 option (a) (`spec:245`) before the user has decided D4 (`spec:244-247`). If the user picks D4 (b) ("Never", `spec:246`) WC-9 and the P2 rows for auggie-review `--post-pr` (`spec:100`) and task `commit`/`push` (`spec:121`) contradict the decision. Yet `spec:154` and `spec:225` say Phases 1-3 need no user decision, although D4 lists auggie-review and task, both Phase P2 (`spec:160`), among the commands it affects (`spec:244`).
- Two commands in WC-9's scope have no such flag: task's EXEMPT `commit`/`push` are keyword-triggered (`INV-B:204`), and post-release authorizes through "pre-authorized this session" wording (`INV-B:79,84`; `spec:113` says only "unless the brief authorizes them"). "The command's own explicit flag" does not exist for them.
- Trust model: D2 (`spec:233-236`) keeps the Ruling rule because another agent's message is not acceptance (`INV-A:66`); D4 (a) lets an agent's brief (the coordinator's) carry the authorization for pushes, PRs and posted comments. The text does not say why the coordinator's quote is acceptable for D4 but not for D2.
- Recommendation: make WC-9 say "off unless the user decision D4 allows it", name the flag mechanism task and post-release will gain, and either move auggie-review and task's outward switch to P4 or state that D4 does not gate their default-off change.

**F-08 [MAJOR label, graded Medium] WC-11 is absolute but three ready commands use fixed shared paths. Expert: Wiegers, Nygard. Priority: Medium.**
- WC-11 (`spec:69`): two workers in one worktree "must never write the same file". WC-4 fixes cleanup-audit's contract at `.claude-audit/return-contract.yaml` and index-repo's at `PROJECT_INDEX.return-contract.yaml` (`spec:62`); init-lite re-run "overwrites its marked report" (`spec:87`). Only cleanup-audit's row carries the exception ("one audit per worktree at a time (WC-11)", `spec:85`); index-repo and init-lite do not, and 2.3 (`spec:73`) tells the coordinator to state worktree placement but not to serialize these three.
- Recommendation: put "at most one worker per worktree for cleanup-audit, index-repo, init-lite" into the 2.3 brief template or into WC-11 as a named exception.

**F-09 [MINOR/Medium] tasklist row depends on an unspecified order inside P2 and drops an inventory recommendation without recording it. Expert: Fowler, Wiegers. Priority: Medium.**
- `spec:122` has tasklist pass `--unattended` to each reflect so reflect's headless auto-accept rule applies; reflect gains that mode in the same phase (`spec:88`, `spec:160`). P2 is "one written plan" (`spec:164`) but the order inside it is not given, so a tasklist change landing first passes a flag reflect rejects.
- `INV-B:215` recommended running the reflect fan-out at the worker's top level, not in subagents, and `INV-B:210,314` mark nested spawning UNVERIFIED. The spec instead asserts the fan-out is "inside Claude Code's nesting limit" via `INV-A:14` and lists no UNVERIFIED item for a reflect running inside a tasklist subagent and spawning its own agents (`spec:271-285`).
- Under headless auto-accept the remediation offer is accepted for auto-fixable registers (`INV-B:109`), so an unattended tasklist run now hands off to workflow/task-builder without a person; this is local, so WC-9 is not violated, but it is a behaviour change the row does not mention.
- Recommendation: order reflect before tasklist in the P2 plan; add the nested-reflect question to the UNVERIFIED list; say that remediation auto-accepts in an unattended tasklist run.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard.

**Strengths (no finding).** The decision (Orca on top, commands unchanged units, `spec:16`) is backed by rejected-alternative reasons R1-R5 that each point at an inventory line (`spec:33-37`, checked against `CAPS:97-103,145-150`, `INV-A:90`, `INV-B:285-286`). The message pattern is clean: one `worker_done` from the top-level session (`spec:63,65`), pull-based follow-ups (`spec:70`), `ask` for questions (`spec:61`), a file as the data hand-off (Hohpe: file drop plus completion event, with the file opened by the coordinator because Orca does not check it, `spec:62`, `CAPS:79`). Interface segregation (Fowler): all shared rules in one installed contract file, each command adds only its gate list (`spec:52`).

**F-04 [MINOR] The mechanism by which a worker session runs a `/sc:` command is never stated. Expert: Fowler, Newman. Priority: Low.**
- A worker's first message is Orca's preamble plus the brief (`CAPS:47`: Claude receives the task on the command line); `spec:16,65` say the worker "runs the command" directly, and the repo rule in the project instructions requires the Skill tool for `/sc:` commands. Whether the worker types, or the Skill tool starts, the command, and how that differs from "wrapping it in an Agent-tool subagent" (WC-7), is not written. The spec itself records that no direct run exists (`spec:43`, `spec:272`) and AC-0.4 (`spec:194`) tests it, so this is a note, not a defect: the evidence gap is acknowledged and gated before any command edit.

**F-10 [MINOR] E3 and section 1.4 characterize the PR #329 evidence differently. Expert: Fowler. Priority: Low.**
- `spec:23` (E3) cites `invocation_method: "skill-direct"` as evidence it "has worked before"; `INV-A:13,35` calls this a direct Orca-worker skill call. `spec:43` then says the same run proves "the nested route, not the direct route" because its brief told workers to use an Agent-tool subagent (`CAPS:156`). The two statements are compatible only if `skill-direct` means the skill inside the subagent. The spec should say so in one line. Not blocking: `spec:43` already states the weaker conclusion and Phase 0 tests it.

**F-11 [MINOR] Non-goal 8 conflicts with two included defect fixes. Expert: Fowler. Priority: Low.**
- `spec:220` limits scope to defects "that stop a command working as a worker" and excludes `/sc:agent`'s missing frontmatter line (`INV-A:36`). `spec:112` (load usage line, `INV-B:63`) and `spec:102` (business-panel frontmatter, effect on loading UNVERIFIED, `INV-A:120`, `spec:278`) are included and listed in SA-4 (`spec:149`), yet neither is shown to stop a worker. A one-line reason, or moving them to the excluded list, removes the inconsistency.

**F-12 [MINOR] AC-C1 versus SA-2 and the P0 deliverables. Expert: Nygard, Crispin-style check. Priority: Medium (carried as follow-up).**
- AC-C1 (`spec:172`) requires the grep over `src/superclaude/core` (among others) to print nothing, with an exemption only for `skills/ccsession-tag/`. SA-2 (`spec:147`) allows Orca to be mentioned "as an example of a caller's question channel inside the contract file", and P0 (`spec:158`) creates `src/superclaude/core/WORKER-CONTRACT.md` and a new Orca section in `core/HOW-WE-WORK.md`. A mention written as `orca orchestration ask` matches the regex and fails AC-C1, and a phase passes only when every common check passes (`spec:167`). Whether the contract text uses that form is not fixed, so I grade this Medium, not blocking.
- Also: the command in the table is written with `\|` escapes (`spec:172`); copied from the raw file into a shell it does not run as intended.
- Recommendation: exempt `core/WORKER-CONTRACT.md` and the Orca section of `HOW-WE-WORK.md` in AC-C1, or forbid command-form mentions in SA-2.

## Adversarial analysis (Whittaker; Review Order 6, after Fowler and Nygard)

Scope: five attack methodologies against the spec's invariants. Concrete findings only; all graded by consequence.

1. I can break this specification by **Divergence Attack**. The invariant at **WC-4 vs SA-3 (`spec:62` vs `spec:148`)** fails when **a caller passes the new output flag without `--unattended`**. Concrete attack: `/sc:analyze x --output out/` (no `--unattended`). Before: no contract. After per SA-3: contract written ("or when the caller passes the new output flag"); after per WC-4: no contract ("in unattended mode"). AC-1.3 (`spec:197`) only tests the no-flag case. Severity: MAJOR label, graded Medium (F-13 below): output is a harmless extra file; no wrong build follows from either reading.
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (`spec:63`)** fails when **the contract file exists but `status` is missing, empty or not one of the four values**. Concrete attack: the command crashes after writing `status:` with no value; the worker's rule is "`--outcome failed` ... or no report exists; `--outcome succeeded` otherwise" (`spec:63`): the file exists, the status is not `failed`/`blocked`, so the worker reports `succeeded`. Step 4 of 7.2 (`spec:183`) would catch it in tests only. Severity: MAJOR label, graded Medium (F-14 below).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 status vocabulary (`spec:63`, `spec:262`)** fails when **a command's own existing status words collide with the fixed four**. Concrete attack: workflow's own contract already carries `status` (`INV-B:272`) and reflect/brainstorm contracts exist (`spec:261`); "commands that already write a contract keep their fields" (`spec:62`) means a workflow `status: ok`-style value of that older vocabulary is kept. The spec does not say that the four values apply to existing contracts or that they are mapped. UNVERIFIED which values those contracts use (`sk/sc-workflow-protocol/refs/return-contract.md` not in the workspace). Severity: MINOR (inferrable from "keep their fields and add the missing ones", but the collision is unaddressed).
4. I can break this specification by **Sequence Attack**. The invariant at **Phase gating (`spec:154`, `spec:158`, AC-0.4 `spec:194`)** fails when **P0's smoke runs are done before the contract file exists as a loaded document**. Concrete attack: P0 writes `WORKER-CONTRACT.md`, then runs three workers "without `--unattended`". The workers do not read the contract at all (no command references it until P1), so AC-0.4 proves the ready commands, not the contract. The spec states this (`spec:194`: "step 4 is `test -s` ... since the contract ... arrive[s] in P1"), so this is a note.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-6 plus the circuit breaker (`spec:64`, `spec:263`, `CAPS:80`, `CAPS:116`)** fails when **a blocked command is retried repeatedly**. Concrete attack: a gate resolves `blocked`, worker sends `--outcome failed`, the coordinator retries with `--retry-of` three times without supplying the missing flag. `CAPS:80` says a worker's own `failed` report does not count toward the three-failure breaker, so retries are unbounded by Orca; the spec does not tell the coordinator to stop and ask the person after a `blocked` outcome (2.3, `spec:72-73`, covers only reading the report). Severity: MAJOR label, graded Medium (follow-up F-15): a coordinator rule, not a command defect.

## Guard Condition Boundary Table (Nygard builds, Crispin validates completeness, Whittaker attacked entries above)

Guards identified: G1 readiness limit, G2 wait/heartbeat window, G3 confidence threshold, G4 nesting depth, G5 WC-5 outcome mapping, G6 flag refusal under `--unattended`, G7 contract location, G8 SA-3 new-file rule, G9 AC-C1 grep. Classes left out: G1 Maximum/Overflow and Sentinel (the upper bound of `--timeout-ms` is UNVERIFIED in `CAPS:54`, outside the spec's own text; no sentinel value exists); G2 Zero/Empty (a zero-length wait cannot be configured, WC-10 states only an upper bound); G3 Sentinel and Maximum (0.70 is the only threshold and confidence is capped at 1.0 by the scale, `INV-A:36`); G4 Zero/Empty and Maximum (depth is a fixed setting of 1, `CAPS:100`, malformed values fall back to the default); G9 Sentinel (a grep has none).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 readiness limit | WC-1 `spec:59` | Zero/Empty | `--timeout-ms` 0 or absent | default 60 s used | `CAPS:44-45`: only a positive number overrides; spec says "default 60 s" | OK |
| G1 readiness limit | WC-1 `spec:59` | One/Minimal | prompt with 30 s fallback | true (passes, 34 s) | passes (`spec:59`, `CAPS:49`) | OK |
| G1 readiness limit | WC-1 `spec:59` | Typical | no prompt | true | `state: ready` (AC 7.2 step 1, `spec:180`) | OK |
| G1 readiness limit | WC-1 `spec:59` | Legitimate Edge Case | fallback just above ~45 s | false | "above about 45 s it fails again" (`spec:59`) | OK |
| G2 wait window | WC-10 `spec:68` | One/Minimal | one 4-minute wait | true | heartbeat between waits | OK |
| G2 wait window | WC-10 `spec:68` | Typical | cli-eval eval of up to 3600 s | true | split into waits of at most 4 min (`spec:104`) | OK |
| G2 wait window | WC-10 `spec:68` | Maximum/Overflow | single tool call >5 min that cannot be split (poll script runtime) | unknown | pr-submit poll runtime "UNVERIFIED" (`spec:114,283`); no fallback if one iteration exceeds 4 min | GAP |
| G2 wait window | WC-10 `spec:68` | Legitimate Edge Case | wait exactly 5 min | boundary | "longer than 5 minutes" must be split; exactly 5 not specified, 4-min rule makes it moot | OK |
| G3 confidence | task row `spec:121` | Zero/Empty | confidence 0.0 | true (< 0.70) | blocked | OK |
| G3 confidence | task row `spec:121` | Legitimate Edge Case | confidence exactly 0.70 | false | proceeds ("below 0.70 resolves as blocked") | OK |
| G4 nesting | R1, WC-8 `spec:33,66` | One/Minimal | worker calls `worker-start` at depth 1 | true (refused) | `nested_worker_depth_exceeded`; commands never call it | OK |
| G4 nesting | R1, WC-8 `spec:33,66` | Sentinel Value Match | user raises the depth (D5) | n/a | WC-8 still forbids Orca calls in commands (`spec:66`, D5 `spec:249-253`) | OK |
| G5 outcome mapping | WC-5 `spec:63` | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G5 outcome mapping | WC-5 `spec:63` | Zero/Empty | report with missing/unknown `status` | undefined | "`failed` ... or no report exists; `succeeded` otherwise" gives `succeeded` | GAP |
| G5 outcome mapping | WC-5 `spec:63` | Sentinel Value Match | audit `verdict: FAIL`; `status: partial` | n/a | both `succeeded`, body states status and verdict | OK |
| G6 flag refusal | `spec:102,103,108,110,114,118,123` | Legitimate Edge Case | `--interactive`, `--watch`, `--monitor 1`, socratic, interactive format | true | "refused"; status and outcome of the refusal not specified | GAP |
| G7 contract location | WC-4 `spec:62` | Zero/Empty | no output dir supplied or not writable | undefined | not specified (compare `command.md:460`) | GAP |
| G7 contract location | WC-4 `spec:62` | Typical | `--output <dir>` | n/a | `<dir>/return-contract.yaml` | OK |
| G7 contract location | WC-4 `spec:62` | Legitimate Edge Case | command with no output flag (research, recommend, review-translation, task, save) | undefined | path not given | GAP |
| G8 new-file rule | SA-3 vs WC-4 `spec:148`, `spec:62` | Legitimate Edge Case | new output flag, no `--unattended` | conflicting | SA-3: contract written; WC-4: only unattended | GAP |
| G9 AC-C1 | `spec:172` | Legitimate Edge Case | allowed mention of Orca in `WORKER-CONTRACT.md` in command form | true (match) | check fails; SA-2 allows the mention (`spec:147`) | GAP |

Completion gate (FR-10): every guard enumerated, every input class either given a row or left out with its reason above; synthesis therefore proceeded. FR-8/FR-9: the seven GAP rows each become a finding; none names a concrete wrong outcome without a guess about the implementer's reading, so each is Medium: G2 poll runtime (already UNVERIFIED in the spec; carried in F-16), G5 (F-14), G6 (F-03), G7 (F-02), G7 no-flag (F-02), G8 (F-13), G9 (F-12).

Propagation: GAP rows are the priority candidates for `sc:adversarial` AD-1 (invariant probe) if the user runs it.

## Quantity check (Pipeline Dimensional Analysis)

Not triggered as a data pipeline: the spec describes a dispatch flow, not a multi-stage transformation whose output count may differ from its input count. The counts it does state were re-derived, so no Quantity Flow Diagram is produced:

- 43 = 21 (`INV-A:3`) + 22 (`INV-B:3`). Verdict sums: 5+5 ready = 10, 13+14 needs-change = 27, 3+3 coordinator-only = 6 (`INV-A:73`, `INV-B:278`); the spec's 10 / 27 / 6 matches (`spec:76`).
- Section 3.1 lists 10 rows, section 3.2 lists 27 rows, section 4 lists 6 rows (`spec:81-92`, `97-125`, `130-137`): 43.
- Phase membership: needs-change 27 = P1 9 (analyze, build, business-panel, design, document, explain, index, load, test) + P2 11 + P3 4 (roadmap, save, validate-roadmap, validate-tests) + P4 3 (implement, post-release, pr-submit). P2 total 15 = those 11 plus reflect, release-split, tdd, troubleshoot from section 3.1 (`spec:160`). Ready 10 = 3 P1 fixes (adversarial, cleanup-audit, index-repo) + 4 P2 + 3 with no change (brainstorm, init-lite, workflow). AC-2.2's 9 "blocked" commands plus its 6 "never blocked" = 15 (`spec:200`). All conserved.

## Expert consensus

- Wiegers, Adzic, Cockburn: the requirements are specific and mostly testable; the gaps are definitional (which commands, which path, what a refusal means) and fixable by deleting a second statement of a rule or adding one sentence (F-01, F-02, F-03).
- Fowler, Newman, Hohpe: the architecture decision is well supported and the rejected alternative is argued from Orca's constraints; the contract file as one shared document is the right place for shared rules. The unproven direct-run route is stated honestly and tested first (`spec:43`, AC-0.4).
- Nygard, Whittaker: failure paths are covered for gates and blocked workers; the unbounded retry of a `blocked` run and an unreadable or half-written contract are the unstated edges (F-14, F-15).
- Disagreement: none recorded. Hightower, Crispin, Gregory not in the requested focus areas; Crispin's check appears only as the traceability item F-07.

## Findings by severity

Blocking (CRITICAL, or a MAJOR/FR-8/FR-9 finding naming a concrete wrong outcome without a guess): none. Every MAJOR-labelled item above fails the grading check on the sentence "an implementer who follows the stated text as written builds X, and X is wrong because Y": each needs the implementer to choose between readings the text allows, or is a requirement the document never states.

| id | label | graded | one line |
|---|---|---|---|
| F-01 | MAJOR | Medium | which commands get the section and contract: `spec:76` vs `spec:159,195`, `spec:62` |
| F-02 | MAJOR | Medium | contract path undefined without an output directory flag (`spec:62`, `spec:182`) |
| F-03 | MAJOR | Medium | outcome of a refused flag undefined (`spec:60`, `spec:63`) |
| F-05 | MAJOR | Medium | WC-9 presupposes D4 (a); trust model differs from D2 (`spec:67`, `spec:236`, `spec:245`) |
| F-08 | MAJOR | Medium | WC-11 absolute vs fixed paths (`spec:69`, `spec:62`, `spec:85`) |
| F-14 | MAJOR | Medium | missing or unknown `status` maps to `succeeded` (`spec:63`) |
| F-15 | MAJOR | Medium | no coordinator rule after a `blocked` outcome; retries unbounded (`spec:72-73`, `CAPS:80`) |
| F-07 | MINOR | Medium | WC-3, WC-6, WC-12, cli-eval wait split have no acceptance check |
| F-09 | MINOR | Medium | tasklist/reflect order within P2; nested reflect not listed UNVERIFIED |
| F-12 | MINOR | Medium | AC-C1 fails on a mention SA-2 allows |
| F-13 | MINOR | Medium | SA-3 and WC-4 disagree on contract with output flag only |
| F-16 | MINOR | Medium | pr-submit poll runtime UNVERIFIED with no fallback (`spec:114,283`) |
| F-04, F-10, F-11 | MINOR | minor | worker command invocation mechanism; skill-direct wording; non-goal 8 vs two fixes |
| F-17 | MINOR | minor | leftover revision labels M1, M2, M5, M6, M7 (`spec:62,73,76`) refer to a disposition the reader of this spec does not have; `INV`/`CAPS` defined only in the citation block (`spec:8`); AC 7.2 step 5 (`spec:184`) searches the transcript for the string `AskUserQuestion`, which also appears in loaded command and skill text, so the check needs "tool call", not "string" |
| F-18 | MINOR | minor (observation outside the spec's evidence set) | the `/sc:spec-panel` definition in this sandbox already has `## Unattended mode` with `--report-dir`, a contract at `<report-dir>/return-contract.yaml`, `--output` as a file option, and points at `~/.claude/WORKER-CONTRACT.md` (`command.md:22-24,455-465`), while the spec's spec-panel row says no `--output` exists and asks for one (`spec:120`, `INV-B:43,182`). The convention (`--report-dir`) also differs from WC-4's `--output`/`--output-dir` wording (`spec:62`). The command file is not an input listed by `spec:5`; its version relative to the inventories is UNVERIFIED. If it is current, the spec-panel row and WC-4 need reconciling with it. |

## Improvement roadmap

- Immediate (text edits, no new mechanism): F-01 one scope rule; F-02 one directory rule plus the refuse-before-work rule; F-03 one sentence in WC-2; F-14 "a contract with a missing or unknown status is `failed`"; F-12 and F-13 wording.
- Short term (before P1 starts): F-05 decide whether WC-9 waits for D4; F-07 add the retry check and mark non-checked requirements; F-08 serialization wording in 2.3; F-09 order inside P2.
- Long term: F-15 add to 2.3 "after a `blocked` outcome the coordinator relays the question to the person and does not retry unchanged"; F-16 measure the poll runtime in P4; F-18 reconcile with the current `/sc:spec-panel` unattended section.

## follow-up candidates

Medium and minor findings, none blocking, none triggers a revision: F-01, F-02, F-03, F-05, F-07, F-08, F-09, F-12, F-13, F-14, F-15, F-16 (Medium); F-04, F-10, F-11, F-17, F-18 (minor). Per the command (Review Loop, bullet 3) the session that ran the review asks the user once per loop whether to open an issue for them and creates none without an answer. This run is a worker in a sandbox with no way to ask and no authority to file anything: it created no issue, and the coordinator should put the one question to the user.

## Reviser brief

None: no blocking finding is open, so nothing is to be revised. If a later loop does produce blocking ids, the reviser contract is: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report byte size before and after with bytes added and deleted per finding id; leave minor and Medium findings alone; do not award yourself a PASS.

verdict: PASS
