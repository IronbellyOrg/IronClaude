review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

## Header

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `de92cfbd1e91f7c9b127746790c558a078c2ca7c0cfa873d862dfcbd0dab1bb9` |
| Baseline | not given (no `--re-review`/`--baseline`); this is a labelled whole-document first review (audit), not a scoped re-review |
| Prior report | none |
| Reviewer model | claude-sonnet-5-5 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full) |
| Shared context read first | `.dev/orca-command-refactor/README.md` (read in full) |

Citation key: `SPEC:N` = the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

Citation checking: the workspace holds only `.dev/orca-command-refactor/`. I resolved every `INV-A`, `INV-B`, `CAPS` and `README` line cite in the candidate against the files (the per-row cites in `SPEC:83-125`, `SPEC:132-137`, the `CAPS:` cites in sections 1 and 2, `README:6,11-17,30,31,35`); each lands on the row or paragraph claimed. Every cite to `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `~/.claude/...`, `/opt/Orca/...`, `.dev/evals/...` and `.dev/codegraph-migration/...` is UNVERIFIED here (no such file in the sandbox); the spec reaches them only through the inventories, which state they were checked once in fresh context (`INV-A:106`, `INV-B:320`).

## Panel and method

Active focus panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, every review). Mandatory artifacts produced below: Guard Condition Boundary Table (guards present), Pipeline Dimensional Analysis plus Quantity Flow Diagram (multi-stage count-changing flow present). `--focus correctness` is not active, so no State Variable Registry is required.

## What the spec claims and what I checked it against

The spec decides "Orca coordinates, commands stay units of work" (`SPEC:16`), defines worker rules WC-1..WC-12 (`SPEC:57-70`), assigns 10 ready, 27 needing change and 6 coordinator-only commands (`SPEC:76`), phases P0-P4 (`SPEC:156-162`), acceptance checks (`SPEC:167-210`) and five open decisions (`SPEC:224-253`).

Internal-consistency checks that passed:
- Counts: 10 rows in 3.1 (`SPEC:83-92`), 27 rows in 3.2 (`SPEC:99-125`), 6 rows in section 4 (`SPEC:132-137`); 21+22 commands (`INV-A:3`, `INV-B:3`); inventory totals 5+5 ready, 13+14 needs-change, 3+3 coordinator-only (`INV-A:73`, `INV-B:278`) sum to 10/27/6.
- P2 list (`SPEC:160`, 15 commands) equals the commands marked P2 in sections 3.1 and 3.2; P3 and P4 lists match their rows.
- Verdicts agree with the inventories row by row for the 43 commands (for example `SPEC:132` vs `INV-A:36,90`; `SPEC:135` vs `INV-B:32,285`).
- Decision D2 matches the safety rule quoted at `INV-A:66` and `INV-A:51`.
- Fork-safe `gh` forms in AC-2.4 and AC-4.2 (`SPEC:202,209`) use `IronbellyOrg/IronClaude`, as the repo rule in README-referenced policy requires.
- Evidence gaps are stated, not hidden (`SPEC:41-45`, `SPEC:271-285`).

## === REQUIREMENTS ANALYSIS ===

No blocking finding. Findings are Medium (warnings, listed under follow-up candidates) or minor. Each Medium finding carries the grading sentence required by the FIRST-REVIEW prompt.

### M-1 (Medium, MAJOR label) No rule for nested `/sc:` commands under `--unattended`. Wiegers, Cockburn. Priority High. Quality impact: completeness -1.

WC-2 is written for "the command" (`SPEC:60`). Only one nested case is resolved, tasklist to reflect (`SPEC:122`). Other nested invocations carry gates the spec never routes: tasklist Stage 9 runs `sc:task --compliance strict` (`INV-B:211`) and `sc:task` has the confidence gate and TFEP "FULL STOP" (`SPEC:121`, `INV-B:199`); roadmap writes memory through `sc:save` at every wave (`INV-B:154`); release-split calls brainstorm and adversarial (`INV-B:119`, `INV-B:121`); cli-eval `create` runs spec-panel and adversarial (`INV-A:44`). Grading sentence: an implementer who follows the stated text builds per-command sections that resolve each command's own gates and leave a nested command's gate unresolved, and that is wrong if the nested gate fires, but only if the nested command is not already given `--unattended`; the text does not say either way, so this needs a guess. Medium.
Recommendation: one sentence in WC-2: a command passes `--unattended` to every `/sc:` command it invokes, and lists in its own section any nested command that has a gate.

### M-2 (Medium) WC-11 conflicts with roadmap's `sc:save` calls. Wiegers, Nygard. Priority Medium.

WC-11 says single-owner shared files "are not written in unattended mode" (`SPEC:69`). The roadmap row does not mention memory (`SPEC:118`), yet the skill saves through `sc:save` at every wave (`INV-B:154`), and `sc:save`'s single-owner keys are overwritten whole (`INV-B:165`). `validate-roadmap` also writes fail-open memory under `.superclaude/memory/validate-roadmap/` (`INV-B:253`); the row is silent (`SPEC:124`). Two parallel roadmap workers in one worktree follow their row text and still clobber `pm_context`/`last_session`/`next_actions`. Needs the guess that roadmap's saves use the save row's per-session keys (`SPEC:119`). Medium.

### M-3 (Medium) P1 end state and the acceptance test over-reach the phase table. Wiegers, Fowler. Priority Medium.

`SPEC:159` makes P1 accept `--unattended` in every command in 3.1 and 3.2. AC-1.1 asserts a `## Unattended mode` section naming `return-contract.yaml` for all of them (`SPEC:195`). Consequences:
- Commands the phase table never names in P1 (brainstorm, init-lite, and the P2-P4 commands) get the section by prose only (`SPEC:159` command column lists 9 commands plus 4 fixes).
- init-lite's 3.1 row says small fix "None" (`SPEC:87`) while WC-4 requires a `return-contract.yaml` in unattended mode (`SPEC:62`); the row contradicts the requirement unless P1 adds one.
- After P1, about 15 gated commands accept the flag while still prompting (their gate conversion is P2 and P4, `SPEC:160,162`), which breaks WC-2 until then. The P0 brief template tells coordinators to pass `--unattended` (`SPEC:158`, `SPEC:73`).
- pr-submit, implement and post-release get their section in P1 before D2/D3/D4 are decided (`SPEC:154,162`), and under D3(a) pr-submit is coordinator-or-person only (`SPEC:240`, `SPEC:139`).
Grading: the implementer must pick which reading wins; the harm (a stall in a window the live checks do not cover) needs the guess that a coordinator dispatches a P2 command before P2 lands. Medium.

### M-4 (Medium) WC-4 path rules do not cover several rows; dangling ids. Wiegers, Cockburn. Priority Medium.

- workflow: the contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` with a generated id (`SPEC:92`, `INV-B:272`), and the spec asks it be written for pre-creation STOPs (`SPEC:92`). At that point no package directory exists (`INV-B:272` note on `:39`), WC-4 demands a path "known before dispatch" (`SPEC:62`), and no workflow output flag is added. No location is stated for the pre-creation contract.
- research: contract "naming the generated `claudedocs/research_*.md` path" (`SPEC:116`); no output directory or flag is specified, so WC-4's `<output-dir>` is undefined (`INV-B:132`).
- cli-portify: the row says the contract "file location unnamed" (`SPEC:105`); the command's default output directory is the generated CLI package under `src/superclaude/cli/<name>/` (`INV-A:45`), so a default would put a runtime file in product source.
- `B-1` and `B-2` are cited as authority in `SPEC:62,76,195,200` and are defined nowhere in the spec or README (searched all of `.dev/orca-command-refactor/`).
Medium: each is a requirement the document never states, not a text that does harm.

### M-5 (Medium) WC-6 "fresh output directory" vs WC-4 "directory known before dispatch". Wiegers, Fowler. Priority Medium.

About 20 rows resolve resume as "fresh dir" (for example `SPEC:99,101,106,107,110`). WC-4 puts the contract at the coordinator-passed directory (`SPEC:62`); WC-6 says a retry must not corrupt the first attempt, by writing "into a fresh output directory" (`SPEC:64`). The spec never says whether the command creates a fresh subdirectory (then the contract is not at `<output-dir>/return-contract.yaml`) or the coordinator passes a new directory per retry (`CAPS:116` retry keeps the Task spec). Needs the guess that the coordinator re-briefs. Also the WC-3 re-invocation after `ask` (`SPEC:61`) hits the same ambiguity. Medium.

### M-6 (Medium) Status vocabulary of existing contracts is not checked. Wiegers, Adzic. Priority Medium.

WC-4 requires `status` in {succeeded, partial, failed, blocked} and says commands with a contract "keep their fields and add the missing ones" (`SPEC:62`); AC step 4 asserts the four-value set (`SPEC:183`). The existing contracts of workflow, brainstorm, reflect and adversarial (`SPEC:261`) are cited for their existence only; their `status` values are not recorded in either inventory (`INV-B:272`, `INV-A:97`). If an existing value differs, "keep their fields" and the four-value assertion cannot both hold. Also AC-0.4 runs three commands before any contract exists but still applies the WC-5 mapping "contract's status" (`SPEC:182`, `SPEC:194`); troubleshoot's `REPORT.md` has no stated status field (`INV-B:242`). UNVERIFIED which values exist. Medium.

### M-7 (Medium) WC-9's "explicit flag" does not exist for the commands that need it. Wiegers, Nygard. Priority High.

WC-9: outward defaults turn on "only through the command's own explicit flag written in the brief" (`SPEC:67`). The rows that need it are post-release (`SPEC:113`), task `commit`/`push` (`SPEC:121`), pr-submit under D3(b) (`SPEC:241`, `SPEC:114`) and D4 (`SPEC:244-247`). The inventories record confirmation prompts and "pre-authorized this session" (`INV-B:79,85`), and pr-submit's push is its default at `--monitor 3` (`INV-B:89,94`), not flag-gated. So no flag named in the spec carries the authorization; each phase would invent one. P4's acceptance checks only the no-authorization path (`SPEC:209`), not the authorized path. Also "paid external run" is undefined: research and review-translation run web search by design (`INV-B:134,144`), and the spec does not say whether `--unattended` turns that off. Medium.

### M-8 (Medium) roadmap resume rule leaves the key choice open. Wiegers, Cockburn. Priority Medium.

The row replaces the `[Y/n]` prompt with "the explicit resume flag" and says to reconcile `.roadmap-state.json` with `.session-memory.md` (`SPEC:118`; mechanisms conflict at `INV-B:153`). It does not say which file the flag reads. AC-3.2 only tests the no-flag case (`SPEC:205`); no check covers the flagged resume. validate-roadmap and validate-tests are similarly "reconcile" rows (`SPEC:124-125`): AC-3.1 checks one filename match (`SPEC:204`), and AC-3.3 `test -d` on the default target (`SPEC:206`) passes if someone creates an empty directory, because the row never says what the default target becomes. Medium.

### M-9 (Medium) Requirements with no acceptance check. Adzic, Crispin-style testability lens (Wiegers). Priority Medium.

Not exercised by any AC in section 7: WC-6 resume or safe re-run (including cli-portify's new `--resume`, `SPEC:105`); WC-10 splitting for cli-eval (`SPEC:104`, AC-4.3 covers pr-submit only); WC-12 `consumer_fenced`; WC-3's `ask` path (AC-2.2 asserts the blocked path only, `SPEC:200`); WC-1 (no number for "well inside" the 60 s limit although the cited evidence shows 30 s passes and about 45 s fails, `SPEC:59`, `CAPS:49`). Medium: untested requirements, not harm.

### M-10 (Medium) AC-C5 additive-edit check vs new flags on existing lines. Adzic, Fowler. Priority Low.

AC-C5 fails any removed line in a command file outside named defect fixes (`SPEC:176`). New flags (`--unattended`, `--output`, `--resume`) are normally documented on the Usage line, which is an existing line, so the diff removes and re-adds it. SA-4 lists permitted defect fixes (`SPEC:149`) and does not include Usage-line additions. Needs the guess that flags go on that line. Medium.

### M-11 (Medium) AC-C1 grep covers `core/`, where P0 adds Orca-mentioning text. Fowler. Priority Low.

AC-C1 forbids `orca orchestration|worktree|terminal|agent` text under `src/superclaude/core` (`SPEC:172`), and SA-2 allows an Orca mention "inside the contract file" (`SPEC:147`). P0 adds `WORKER-CONTRACT.md` with a brief template and an Orca section in `HOW-WE-WORK.md` (`SPEC:158`), both in `core/`. If either names a command in the checked form, AC-C1 fails on the spec's own deliverable. Not forced by the text. Medium.

### M-12 (Medium) tasklist Stage 10.5 now auto-accepts remediation, against the inventory's advice. Wiegers, Fowler. Priority Medium.

Inventory B recommends dropping `--remediate` in Stage 10.5 or running headless (`INV-B:215`) and records that who answers the offer is UNVERIFIED (`INV-B:209`, `INV-B:322`). The spec instead keeps `--remediate` and passes `--unattended` so the headless auto-accept rule applies (`SPEC:122`, `SA-6` `SPEC:151`). Consequence: N unattended remediation handoffs per tasklist run, and the `needs_human_decision` HALT (`INV-B:209`) has no stated resolution. The spec's own UNVERIFIED list (`SPEC:271-285`) omits both the HALT question and the divergence from the inventory. Medium.

### M-13 (Medium, from Guard table G3) WC-10 trigger vs cap vs AC-4.3.

WC-10 splits calls "longer than 5 minutes" into waits of "at most 4 minutes" (`SPEC:68`); the pr-submit row and cli-eval row use 4 minutes (`SPEC:104,114`); AC-4.3 fails any single call over 240 s (`SPEC:210`). A call of 4.5 minutes needs no split under WC-10 and fails AC-4.3. The implementer must choose the stricter reading. Medium.

### Minor notes (never fail the review)

- N-1 `SPEC:11` says every other section-3 line is "carried from the inventories without a second read"; `SPEC:285` says a fresh agent re-read about 340 citations. Both can be true but the provenance statement is confusing.
- N-2 pr-submit is counted among the 27 changed commands (`SPEC:76`, `SPEC:114`) while the recommended D3(a) removes it from worker scope (`SPEC:139`, `SPEC:240`); the headline count only holds if D3(b) is chosen.
- N-3 The tasklist row says its reflect fan-out runs "one layer below the worker" (`SPEC:122`); the reflect subagents are one layer down, and their reviewers (`INV-B:111`) are a second layer. The conclusion (inside the three-layer limit, `INV-A:14`) still holds.
- N-4 `SPEC:148` (SA-3) lets a new `--output` flag alone trigger the contract; WC-4 says unattended mode only (`SPEC:62`).
- N-5 WC-7 cites `INV-A:95` for "nesting loses tools"; that finding is itself marked UNVERIFIED for Monitor and AskUserQuestion (`INV-A:112`). The rule is safe either way.

## === ARCHITECTURE ANALYSIS ===

Fowler (lead), Newman, Hohpe, Nygard.

Strengths: the decision is clearly separated from its rejected alternative with five evidenced reasons (`SPEC:29-37`); layering is clean (coordinator, worker session, command, subagent) with lifecycle messages confined to the top-level session (`SPEC:65`); the contract file is one shared document referenced by installed path, consistent with the repo's installed-path rule (`SPEC:52`, `SPEC:264`); phases are ordered by risk (`SPEC:267`); standalone behaviour is a hard constraint with its own checks (`SPEC:141-151`, AC-1.3, AC-2.5).

Findings:
- A-1 (Medium; Newman, API evolution) The contract schema has no version field. WC-4 lists required keys (`SPEC:62`) while existing contracts carry their own versions (workflow "contract 1.1", `INV-B:272`). Two schemas will coexist across P1-P3 and a coordinator reader has nothing to branch on. Recommendation: add `contract_version`. Medium (a missing requirement).
- A-2 (Medium; Hohpe, message exchange) `worker_done` is the only completion signal and Orca does not read the report (`SPEC:62`, `CAPS:79`); if the worker dies between writing the contract and sending, the coordinator relies on `worker-show`/`agentWait` (`SPEC:44`, `SPEC:181`). The spec states this but gives no coordinator rule for "contract present, no `worker_done`". Medium.
- A-3 (Nygard) Failure modes are covered unusually well: silent stall (`SPEC:44`), consumer fencing (`SPEC:70`), circuit breaker (`SPEC:263`), ask timeout resume (`SPEC:61`). The remaining gap is M-5 (retry output).
- A-4 (Fowler, bounded contexts) Putting the shared rules in `~/.claude/WORKER-CONTRACT.md` and a per-command section is the right seam; M-1 shows the seam is missing one clause (nested commands).

Open decisions D1-D5 each give options, a recommendation and a reason (`SPEC:227-253`). D1 option (b) correctly identifies the risk to SA-1 (`SPEC:229`). No architecture finding is blocking.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Each attack names the methodology, the invariant location and a trace. Grading follows the consequence test.

1. **Sequence Attack** on WC-3/WC-4/WC-5. Invariant at `SPEC:61-63`: one contract, one `worker_done`. Trace: command blocks, writes `status: blocked` contract; worker `ask`s, receives an answer, re-invokes the command with the answer flag; for a "fresh dir" command (`SPEC:64`) the second run writes to a different directory. State before: contract at `D/return-contract.yaml` (blocked). After: contract at `D2/...` (succeeded); the path the coordinator knew (`D`) still says `blocked`. If the worker sends `--report-path D/...`, the coordinator reads blocked and the outcome contradicts the work. Needs the guess that the worker picks the stale path. Medium (M-5).
2. **Divergence Attack** on WC-10. Invariant at `SPEC:68`: boundary between "longer than 5 minutes" and "at most 4 minutes". Trace: a 4.5-minute poll call: no split required, AC-4.3 fails it (`SPEC:210`). Medium (M-13).
3. **Sentinel Collision Attack** on the status enum. Invariant at `SPEC:62-63`: `blocked` and `failed` both map to `--outcome failed`. A real failure and a gate stop become the same Orca outcome, so the coordinator must open the file to tell them apart (the spec says the coordinator opens it, `SPEC:62`). No collision of user data with a control signal found. OK.
4. **Zero/Empty Attack** on WC-4. Invariant at `SPEC:62`: contract "written on every outcome, including stops before any other output exists". Trace: workflow bad input before package creation: no directory, no flag, no path (M-4). Medium. Also `blocked_question` empty: AC-2.2 requires non-empty (`SPEC:200`), WC-4 does not. Minor.
5. **Accumulation Attack** on WC-11. Invariant at `SPEC:69`: no two workers write one file. Trace: cleanup-audit has a fixed `.claude-audit/` directory (`SPEC:85`, `INV-A:42`); three single-pass workers run one after another all write `.claude-audit/return-contract.yaml` (WC-4 puts the contract in the output directory). Sequential runs overwrite; a coordinator reading late sees the last pass only. The spec states "one audit per worktree at a time" for concurrency but not the contract name per pass. Minor (the `report_path` inside the contract identifies the pass).

## Pipeline Dimensional Analysis (Fowler leads, Whittaker attacks)

Trigger: multi-stage flow with count changes (command set to worker-capable set to phases to tests). Steps 1-4 (FR-18):

1. Detection: inventory (43) to verdict split (10/27/6) to phase assignment to acceptance checks.
2. Quantity annotation and 3. downstream tracing and 4. consistency check: see the diagram.

```text
[Commands in cmd/: 43 (INV-A:3 + INV-B:3)]
   --> [Verdict split]
        --> [coordinator-only: 6 (SPEC:132-137)]     (no phase, no --unattended; AC-1.1 asserts none has a section)
        --> [worker-capable: 37 = 10 ready + 27 change]
              --> [Phase table SPEC:158-162: P1 9 + 4 fixes, P2 15, P3 4, P4 3 = 35 named]
                    --> [AC-1.1 consumer: expects ALL 36 in 3.1-3.2 except load (SPEC:195)]  <-- expects 36, phases name 35
                    brainstorm, init-lite: not in any phase row (covered only by SPEC:159 prose)
```

Result: worker-capable 37 minus `load` (no section) is 36; the phase table names 35 (brainstorm and init-lite absent), while AC-1.1 asserts a section for all 36 at the end of P1. FR-19 labels a dimensional mismatch CRITICAL; under the Review Loop grading rule I grade by consequence: the mismatch is covered by the prose at `SPEC:159` ("every command in sections 3.1 and 3.2"), so an implementer who reads the whole spec adds the two sections, and the harm needs a guess that the table alone is followed. Recorded as part of M-3, Medium, not blocking. Counts that do reconcile: 10+27+6=43; P2 15 = 11 (3.2) + 4 (3.1); P3 4 and P4 3 match.

## Guard Condition Boundary Table

Guards in the specification: gate resolution (WC-2), outcome mapping (WC-5), the 4/5-minute wait rules (WC-10), the default-off outward rule (WC-9), the readiness limit (WC-1), the depth-1 rule (WC-8), the task confidence gate (`SPEC:121`). Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack). The table is complete: every guard is enumerated, every cell populated; classes that cannot occur are listed under the table with a one-line reason (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 gate resolution | SPEC:60 (WC-2) | Zero/Empty | no caller flag, no default | blocked branch (c) | write `status: blocked` + question, stop | OK |
| G1 gate resolution | SPEC:60 | Typical | caller flag supplied | branch (b) | use the flag | OK |
| G1 gate resolution | SPEC:60, SPEC:122 | Legitimate Edge Case | gate inside a nested `/sc:` command | unresolved | only tasklist to reflect stated; others unspecified | GAP (M-1) |
| G2 outcome mapping | SPEC:63 (WC-5) | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| G2 outcome mapping | SPEC:63 | Typical | status `succeeded` | succeeded | `--outcome succeeded` | OK |
| G2 outcome mapping | SPEC:63, SPEC:263 | Legitimate Edge Case | status `partial`; audit verdict FAIL | succeeded | `--outcome succeeded`, body states status | OK |
| G2 outcome mapping | SPEC:63, SPEC:194 | Legitimate Edge Case | report exists but has no `status` (P0 commands) | undefined | not stated | GAP (M-6) |
| G3 wait split | SPEC:68 (WC-10) | Typical | call of 2 minutes | no split | none required | OK |
| G3 wait split | SPEC:68, SPEC:210 | Maximum/Overflow | single call of 4.5 minutes | WC-10 not triggered; AC-4.3 fails | WC-10 silent between 4 and 5 minutes | GAP (M-13) |
| G3 wait split | SPEC:68 | Maximum/Overflow | single call of 6 minutes | split | waits of at most 4 minutes | OK |
| G4 outward default off | SPEC:67 (WC-9) | Typical | auggie-review under `--unattended` | off | `--no-post-pr`, posting only via explicit `--post-pr` | OK |
| G4 outward default off | SPEC:67, SPEC:113-114 | Legitimate Edge Case | command whose purpose is the outward action (pr-submit, post-release) | no enabling flag named | "the command's own explicit flag" (none exists) | GAP (M-7) |
| G5 readiness limit | SPEC:59 (WC-1) | Typical | prompt falls back at 30 s | within limit | passes (`CAPS:49`) | OK |
| G5 readiness limit | SPEC:59 | Maximum/Overflow | fallback at 50 s | exceeds evidence threshold (~45 s) | "well inside" 60 s, no number | GAP (minor; launch setup is out of command scope) |
| G6 nesting depth | SPEC:66 (WC-8) | Typical | worker calls `worker-start` | refused (depth 1) | forbidden; split by coordinator | OK |
| G6 nesting depth | SPEC:66 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | forbidden either way (`CAPS:103`) | OK |
| G7 task confidence | SPEC:121 | Sentinel Value Match | confidence exactly 0.70 | not below threshold | only `< 0.70` is a gate (`INV-B:199`) | OK |
| G7 task confidence | SPEC:121 | Typical | confidence 0.5 | blocked | `blocked` with the question | OK |

Left out, with reasons: One/Minimal for G1-G7 (no minimal-size input distinct from Typical); Sentinel Value Match for G1-G6 (no reserved value is compared, apart from the status enum, tested under attack 3); Maximum/Overflow for G1, G2, G4, G6, G7 (no capacity or upper bound defined; depth is a fixed 1).

GAP grading (FR-8, FR-9): G1-edge, G2-edge, G3, G4-edge are Medium (see M-1, M-6, M-13, M-7): none names a stated text that yields a wrong outcome without a further guess. The minor G5 row is a note. FR-9 (blank Specified Behavior): the G2 and G4 GAP rows and the G1 nested row are the only blank behaviours; graded the same.

## Synthesis

The spec is coherent, its evidence is unusually well sourced and its uncertainty is declared. Its weaknesses are about completeness at the seams between the contract and the existing commands (nested commands, report locations, retry output, enabling flags for outward actions) and about acceptance checks that do not exercise every requirement. None of them is a stated text that, followed as written, yields a wrong outcome without an additional guess.

Quality scores (0-10): Clarity 8, Completeness 7, Testability 7, Consistency 8.

## Coverage

Covered: the whole candidate (all nine sections and the Decisions and UNVERIFIED lists), cross-read against the three inventories and the README. Not covered: any file outside `.dev/orca-command-refactor/` (see citation checking), live Orca behaviour (no Orca in the sandbox), and the commands' source text, so the inventory rows themselves were taken as given.

## Follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, A-1, A-2.
Minor: N-1 to N-5, Whittaker attack 5, G5 row.
Issue offer: the session that ran this review is to ask the user once whether to open an issue for these; this run had no user and created none.

## Brief clauses overridden

None. The brief asked for a whole-document first review; the report is labelled as such and contains no scoped-PASS wording.

Reviser brief: none; no blocking finding is open, so no revision is requested.

verdict: PASS
