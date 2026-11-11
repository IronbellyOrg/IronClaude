review: 1 of 3

# /sc:spec-panel critique: Orca worker contract spec (whole-document audit)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Run type: first review of the whole document (no `--re-review`, no `--baseline`; `baseline: n/a`). Labelled whole-document audit of the final spec. Prompt used: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (296 lines)
- Candidate sha256: `90517bb8b39156a6ae96df698dafb7e24324de3cb8682a343273a1cbd2cce875`
- Reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5)
- Review date: 2026-11-10
- Mode: unattended-style, single report; the candidate was not edited.
- Shorthand: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

- Read in full: the command definition, the FIRST-REVIEW prompt, `README.md`, the candidate (all 296 lines), and all three inventories (tables, per-command notes, summaries, UNVERIFIED lists, with the full `CAPS` text read for every line the candidate cites).
- Checked against the inventories (the only checkable evidence): every `CAPS:N` reference in the candidate (about 55 distinct line refs), every `INV-A:N` and `INV-B:N` reference at row or note level (about 60), `README:6,11-17,12,30,31,35`. Counts were re-derived: 21 + 22 = 43 commands; 10 ready (5 + 5), 27 needs-change (13 + 14), 6 coordinator-only (3 + 3); phase lists P1 12 + P2 15 + P3 4 + P4 3 = 34 changed, plus 3 untouched ready commands (brainstorm, init-lite, workflow) = 37 = 10 + 27.
- Result of the citation check: no wrong or shifted line found among the checkable `CAPS`/`INV`/`README` references, except the notes N-01 and N-02 below.
- UNVERIFIED (cannot be checked in this sandbox, carried second-hand from the inventories): every citation into `src/superclaude/...` (`cmd/`, `sk/`, `ag/`), `CLAUDE.md`, `Makefile`, `pyproject.toml`, `src/superclaude/cli/install_core.py`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `/opt/Orca/...`, and the claims at S:11 and S:295 that 11 and about 340 citations were re-read. Findings that rest on them are marked.
- Not covered: any behaviour of the real commands, skills or Orca; the spec was reviewed against what it states and against the inventories, not against the repository.
- Panel (focus `requirements`, `architecture`, plus Whittaker who is active in every review, and Crispin for the Guard Condition Boundary Table): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Nygard, Whittaker, Newman, Hohpe, Crispin. `--focus correctness` was not requested, so the State Variable Registry is not produced.

## Mandatory artifacts

### Guard Condition Boundary Table (Nygard builds, Crispin validates completeness, Whittaker attacks)
The spec contains conditional logic and thresholds, so the table is required. One row per applicable input class; omitted classes are named in the line under each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `outcome_map` | S:63 (WC-5) | Zero/Empty | report file exists but is 0 bytes or has no `status` key | "report says failed or blocked" false; "no report exists" false | "`--outcome succeeded` otherwise" applies, so an empty report is reported as succeeded | GAP (M-01) |
| `outcome_map` | S:63 | Zero/Empty (absent) | no report file | "no report exists" true | `--outcome failed` | OK |
| `outcome_map` | S:63 | One/Minimal | `status: partial` | false | `--outcome succeeded`, body first sentence says partial | OK |
| `outcome_map` | S:63 | Typical | `status: blocked` | true | `--outcome failed` | OK |
| `outcome_map` | S:63 | Sentinel Value Match | audit with `verdict: FAIL` and `status: succeeded` | false | `--outcome succeeded` (stated) | OK |
| `outcome_map` | S:62-63 | Legitimate Edge Case | `status` outside the four values (existing contracts "keep their fields", S:62), or a stale report from an earlier attempt in the same directory | false | undefined; falls to "otherwise", so succeeded | GAP (M-01, M-03) |
| `split_wait` | S:68 (WC-10) vs S:220 (AC-4.3) | Zero/Empty | no blocking call | not over 5 min | no split | OK |
| `split_wait` | S:68 | One/Minimal | 1 s call | false | no split | OK |
| `split_wait` | S:68 | Typical | 120 s poll | false | no split | OK |
| `split_wait` | S:68 | Maximum/Overflow | 301 s call | true | split into waits of at most 4 min | OK |
| `split_wait` | S:68, S:220 | Legitimate Edge Case | 270 s call | false (not "longer than 5 minutes") | WC-10 leaves it unsplit; AC-4.3 fails any call over 240 s | GAP (M-05) |
| `split_wait` | S:68 | Sentinel Value Match | pr-submit default 600 s | not a single call; a cumulative budget over iterations | stated as such | OK |
| `readiness_fallback` | S:59 (WC-1) | Zero/Empty | no startup prompt | n/a | nothing to bound | OK |
| `readiness_fallback` | S:59, CAPS:49 | Typical | 30 s auto-fallback | inside the limit | start passes (34 s) | OK |
| `readiness_fallback` | S:59, CAPS:49 | Maximum/Overflow | fallback above about 45 s | at or beyond a 45 s `--timeout-ms` | WC-1 says only "well inside" the 60 s default; no number | GAP (M-13) |
| `ask_resume` | S:61 (WC-3) | Zero/Empty | coordinator never answers | `ask` times out | resume the same message ID; no cap on resumes, no fallback to blocked | GAP (M-13) |
| `ask_resume` | S:61 | One/Minimal | answered at first wait | n/a | re-invoke or resume with the answer as a flag | OK |
| `ask_resume` | S:61 | Typical | one timeout then an answer | n/a | resume same ID, no duplicate | OK |
| `depth_fence` | S:33, S:66 (R1, WC-8) | Zero/Empty | setting absent or malformed | falls back to 1 (CAPS:100) | worker cannot start workers | OK |
| `depth_fence` | S:33, S:66 | One/Minimal | setting 1 | worker refused | commands never call `worker-start` | OK |
| `depth_fence` | S:66, S:262 | Maximum/Overflow | setting raised (D5 b) | fence relaxed | WC-8 still forbids the call | OK |
| `outward_default_off` | S:67 (WC-9), S:255 (D4) | Zero/Empty | no authorizing flag in the brief | off | no push, PR, post, install | OK |
| `outward_default_off` | S:67, S:255 | Legitimate Edge Case | the flag is in the brief, but the user's instruction is not quoted | WC-9: on (flag only); D4(a): off (flag plus quoted instruction) | two rules disagree | GAP (M-09) |
| `outward_default_off` | S:100 | Sentinel Value Match | `--unattended` implies `--no-post-pr`; explicit `--post-pr` also present | posting returns | stated: only an explicit `--post-pr` turns it on | OK |

Omitted classes, one line each: `outcome_map` Maximum/Overflow (no size or count dimension); `ask_resume` Maximum/Overflow is covered by the Zero/Empty row (the same unbounded wait); `ask_resume` Sentinel (no sentinel value); `readiness_fallback` Sentinel (no sentinel; `--timeout-ms` is a caller knob, CAPS:45); `depth_fence` Typical and Sentinel (depth is an integer with one default); `outward_default_off` Maximum/Overflow and Typical (boolean).
FR-8 and FR-9 were applied: each GAP is graded by consequence below; none has a blank Specified Behavior. FR-10: the table is complete for the guards listed.

### Quantity Flow Diagram (Fowler annotates, Whittaker attacks; Pipeline Dimensional Analysis triggers: the spec is a multi-stage classify, assign, verify flow with count changes)

```text
[Source: 43 command files in cmd/ (S:76; INV-A:3 + INV-B:3 = 21 + 22)]
   --> [Stage 1: verdict split (S:78, S:94, S:127)] --> 10 ready + 27 needs-change + 6 coordinator-only = 43  (conserved)
   --> [Stage 2: phase assignment (S:156-162)]
         P1 = 12 named (9 no-gate + 3 small fixes)   P2 = 15   P3 = 4   P4 = 3   -> 34 changed
         + 3 ready commands in no phase list (brainstorm S:84, init-lite S:87, workflow S:92) = 37 = 10 + 27  (conserved)
   --> [Stage 3: P1 acceptance]
         S:159 "flag accepted by every command in sections 3.1 and 3.2" = 37
         S:205 AC-1.1 "every command in sections 3.1-3.2 has a ## Unattended mode section" = 37
         Phase list for P1 = 12  <-- MISMATCH (37 expected in P1, 12 delivered; 22 belong to P2-P4, 3 to no phase)
```
The mismatch is finding B-01. No other stage divides counts inconsistently.

## === REQUIREMENTS ANALYSIS ===

### B-01 (blocking) AC-1.1 and the P1 scope sentence ask for 37 sections in P1; the same document defers 25 of those commands
- Expert: Wiegers (traceability), Adzic. Priority: High. Label: CRITICAL (dimensional mismatch, FR-19).
- Location: S:159 (P1 scope), S:205 (AC-1.1), against S:250 (D3 a), S:112 and S:275 (load), S:160-162 (P2-P4 scope), S:60 (WC-2).
- Grading sentence: An implementer who follows the stated text as written builds a Phase 1 that adds a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` to all 37 commands of sections 3.1-3.2 and a passing `test_worker_contract.py` that asserts it, and that is wrong because (a) it includes `pr-submit`, which D3(a) says gets "no pr-submit changes in Phase 4" (S:250) and which the section 3.2 row still lists as changed (S:114); (b) it includes `load`, whose own row says "Report: none" and whose Decisions entry says a report file "would be an unrequested addition" (S:112, S:275); (c) it includes `implement`, `post-release`, `roadmap`, `cli-eval` and the other P2-P4 commands, so their sections describe gate resolutions that WC-2 says the command performs ("never calls `AskUserQuestion`") while the gate conversion is scheduled for a later phase (S:160-162), and a coordinator that reads those sections after P1 dispatches a worker that still stalls on the prompt; and (d) the test cannot pass for pr-submit under D3(a) without making the change D3(a) rules out.
- Recommendation (narrow, do not add): limit the S:159 flag sentence and AC-1.1 to the commands named in the P1 row of S:159 (12), and let AC-2.1, a P3 check and a P4 check assert the sections for their own commands; state that `load` and the three untouched ready commands get no section, or name the phase that gives it.
- Quality impact: Testability and Consistency.

## === ARCHITECTURE ANALYSIS ===
No blocking architecture finding. The central decision (Orca on top, commands unchanged as units of work, S:13-45), the rejected alternative (S:28-39), the standalone guarantees (S:141-151) and the coordinator-only split (S:127-139) are consistent with the inventories I could check (CAPS:97-103, 147-161; INV-A:90-98; INV-B:285-287).

## Medium findings (warnings, listed under follow-up candidates; none blocks)

- M-01 (Whittaker, Wiegers) WC-5 maps every report that exists and does not say failed or blocked to `succeeded` (S:63).
  I can break this specification by the Zero/Empty attack. The invariant at WC-5 fails when the report file exists but is empty, unparseable, has no `status`, has a value outside the four, or is a stale file from an earlier attempt in a reused directory (resume-capable commands reuse theirs, S:64). Concrete attack: attempt 1 ends `partial`; the retry worker crashes before rewriting `return-contract.yaml`; the old file is read, "no report exists" is false, `--outcome succeeded` is sent, and the Task's dependents are released on an incomplete run. Graded Medium: it needs the implementer to read "report exists" as "any file", where "a valid report" is the other reading the text allows. Recommendation: say the worker sends `succeeded` only for a readable report with a status in the four values written during this run, and `failed` otherwise.
- M-02 (Cockburn, Wiegers) `<output-dir>` is undefined for commands whose `--output` is a file (S:62, S:73).
  tdd, init-lite and spec-panel take `--output <file>` (S:87, S:90, S:120), adversarial, brainstorm and reflect take a directory (S:83-84, S:88). WC-4 writes `<output-dir>/return-contract.yaml` "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". For a file-valued flag the text allows two readings (the file's parent directory, or a second flag); with the first, two TDD workers writing into one parent directory overwrite each other's contract (WC-11, S:69). AC-2.2 runs `/sc:tdd ... --unattended --output <file>` and expects a contract (S:210), so the check cannot name the contract path. Recommendation: one sentence fixing the contract path for file-valued `--output`.
- M-03 (Wiegers) The status vocabulary of the contracts that already exist is not checked (S:62, S:204, S:272).
  WC-4 says existing contracts "keep their fields", and also that `status` is one of four values. The inventories list the `status` key for workflow (INV-B:272) without its values, and give no values for brainstorm, reflect or adversarial. AC-0.4 compares the worker outcome with workflow's own `status` (S:204). If those values differ from the four, WC-5 has no mapping for them. Recommendation: record the existing values or say the mapping table is extended per command.
- M-04 (Crispin, Adzic) Several requirements have no acceptance check, and the live check cannot detect the stall it is meant to catch.
  No check covers WC-6 (retry, `--retry-of`; S:64), WC-3 (the `ask` path; S:61), WC-12 (`check` and `consumer_fenced`; S:70) or WC-1 (S:59) beyond the incidental `state: ready` in step 1; WC-10 is checked only for pr-submit (S:220), not for the cli-eval wait split promised in S:104 and S:160. In 7.2, step 3 waits "until `worker_done` arrives" with no failure bound (S:192), although the spec's own failure mode is a silent stall with no `worker_done` (S:44); step 5 searches only for `AskUserQuestion` (S:194), while the stalling form for auggie-review is a plain chat offer (INV-A:62), which also leaves `agentWait` null. Recommendation: add a stall bound to step 3 and one pass condition each for WC-3, WC-6 and WC-12.
- M-05 (Whittaker, Nygard) WC-10 and AC-4.3 disagree on the boundary (S:68, S:114, S:220, S:276). WC-10 splits only calls "longer than 5 minutes"; every row and AC-4.3 use 4 minutes (240 s) and the Decisions entry chooses 4 minutes for margin. A 270 s step passes WC-10 and fails AC-4.3. Divergence attack: heartbeat gap = work since the last heartbeat plus the next call, so a 270 s call started 60 s after a heartbeat leaves a 330 s gap. Recommendation: make the WC-10 trigger match its target.
- M-06 (Crispin) The additivity checks do not see deleted bullet lines (S:186, S:203). `git diff -U0 ... | grep -E '^-[^-]'` skips any removed line whose content starts with `-`, and a removed markdown bullet `- text` appears as `-- text`. SA-1 (S:146) therefore has an undetected failure path for command files, which are bullet-heavy. Recommendation: `grep '^-' | grep -v '^---'`.
- M-07 (Newman, Fowler) The directory-flag name and the spec-panel row may disagree with the command as it exists. Evidence is outside the inventories and is the definition file used to run this audit, not a repository path: `command.md:23` lists `--output <file>`, `--unattended` and `--report-dir <dir>`; `command.md:457-463` already has an `## Unattended mode` section that points at `~/.claude/WORKER-CONTRACT.md`, requires `--report-dir`, writes `<report-dir>/return-contract.yaml`, and uses three statuses (succeeded, blocked, failed; `command.md:461`), with `--output` file-valued (`command.md:460`). The spec names the directory flag `--output` / `--output-dir` (S:62), proposes creating `WORKER-CONTRACT.md` (S:52, S:158) and adds `partial` (S:62). The spec already hedges the row (S:120, S:296 item 15), so this is a warning: if the file exists in the repo, P0 collides with it and WC-4's flag names and status set need one reconciliation. UNVERIFIED against the repository.
- M-08 (Fowler, Nygard) The tasklist row picks the more consequential reflect default and asserts a nesting claim the inventory leaves open (S:122). It has Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies"; that rule auto-accepts remediation for auto-fixable registers (INV-B:109), where INV-B:215 recommends calling reflect without `--remediate`. The spec does not say that unattended tasklist now runs N remediations, and S:88 keeps reflect's own ready brief at "no `--remediate`". It also states the reflect fan-out is "inside Claude Code's nesting limit" with "none" as the other change, while INV-B:215 says the fan-out should run at the worker's top level and INV-B:314 marks subagent nesting UNVERIFIED. Recommendation: state the consequence or pick the conservative decline default (a WC-2 option (a)).
- M-09 (Wiegers) WC-9 turns an outward action on with "the command's own explicit flag written in the brief" (S:67); D4(a) requires the flag plus the user's quoted instruction (S:255). Also S:154 says Phases 1-3 need no user decision, while D4 governs auggie-review `--post-pr` and task `commit`/`push` (S:254), both in P2. Recommendation: one gating rule, stated once.
- M-10 (Hohpe, Wiegers) Section 2.3 requires every brief to include `--unattended` (S:73) and 7.2 step 1 builds the brief per 2.3 (S:190), while section 3.1 says the ten ready commands "run as workers now" with the stated flags (S:79) and AC-0.4 lists P0 commands without it (S:204). Before P1 the flag does not exist, so a 2.3 brief for a ready command carries an unknown flag. Recommendation: say 2.3's `--unattended` applies from P1.
- M-11 (Cockburn) `/sc:git` is made coordinator-only partly because workers "make no commits or pushes" and git operations "need the user's authorization in this repo" (S:133), citing `README:31`. That line is the rule for workers of this planning run (`README:30-31`), not repository policy; INV-A:91 says so ("this run forbids"). The verdict may still hold on the confirmation gates (`cmd/git.md:90`, UNVERIFIED), but the stated reason is run-local. Recommendation: cite the lasting reason only.
- M-12 (Newman) Possible unlisted commands. This session's installed skill list shows `/sc:graph`, `/sc:impact` and `/sc:issue`, which neither inventory covers, and describes `sc-issue-protocol` as creating an Orca worktree and launching an agent. If they are in `cmd/`, the count of 43 (S:76) and E5 ("no command... calls Orca today", S:25) are wrong and AC-C1's "prints nothing" baseline (S:172-180) fails before any change. UNVERIFIED: the source is the session's skill listing, not a file in the sandbox.
- M-13 (Nygard, Whittaker) Two unbounded values (from the Guard Condition Boundary Table). WC-1 says a startup fallback must be "well inside" the 60 s default (S:59) with no number, while CAPS:49 shows failures above about 45 s under a 45 s limit. WC-3 resumes the same `ask` message "never creates a duplicate" (S:61) with no cap on resumes and no fall-through to `blocked`, so an unanswered question parks a healthy-looking worker indefinitely (CAPS:52). Accumulation attack: a coordinator that has ended its turn never replies; the worker resumes forever. Recommendation: one number each, or a stated escalation after N resumes.

## Minor notes (never fail the review)

- N-01 S:296 (item 15) says `INV-B:43` states no output flag exists; INV-B:43 is the table row ("no path"), the `--output` statement is in the note at INV-B:177-186. The same item refers to "a sandbox copy of the command file, outside this workspace", wording that does not belong in a spec.
- N-02 The pr-submit top-level rule is cited at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (S:65, S:11, INV-B:90) but at `:47-49` in the installed copy (CAPS:161). Different files, so possibly both right; the spec does not say which copy.
- N-03 S:172-183: the [B2] prose and code block sit inside the AC-C1..AC-C5 table, so rows AC-C2 to AC-C5 render outside the table.
- N-04 S:43 says Phase 0 "starts with live smoke runs"; S:158 puts writing the contract file first.
- N-05 S:23 (E3) lists `invocation_method: "skill-direct"` as evidence; S:43 says that run proves only the nested route. Both are stated, but E3 does not carry the caveat.
- N-06 S:193 relies on PyYAML as a declared dependency (`pyproject.toml:38`, UNVERIFIED); the project instructions list only pytest, click and rich.
- N-07 AC-C1 (S:177) checks four Orca subcommands while SA-2 bans any `orca` or `orca-ide` command (S:147), and the `plugins/superclaude/` mirror is outside its path list (S:289, item 8).

## Expert consensus and disagreements

- Consensus (Wiegers, Fowler, Nygard, Newman): the design decision and the standalone guarantees are well evidenced, the citation quality is high, and the unknowns are labelled UNVERIFIED (S:281-296).
- Single blocking point: the P1 acceptance and scope sentence (B-01).
- Disagreement: Whittaker would grade M-01 blocking (the stated "otherwise" does harm); Wiegers and Nygard read "no report exists" as "no valid report" and keep it Medium. The grading rule gives Medium, because it needs a guess about which reading the implementer picks.

## Follow-up candidates (Medium and minor, for the user to triage; none was filed)

M-01 to M-13 and N-01 to N-07 above. This run records the list; the session that coordinates the loop asks the user once whether to open an issue for them, and none was created.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing beyond the command's scope.

## Reviser brief

Blocking finding ids: B-01.
Rules for the reviser (restated from the command, Review Loop bullet 6): revise only the text finding B-01 names (S:159, S:205 and, if needed to keep them consistent, the one sentence in S:76 or S:112 that B-01 cites); add no rule, mechanism or section that B-01 does not call for; cite the finding id on every added paragraph or table row; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
