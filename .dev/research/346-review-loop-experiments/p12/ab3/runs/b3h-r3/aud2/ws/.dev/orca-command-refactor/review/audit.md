review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (spec-panel, critique mode)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `92a25ab664b0803fb12bd23716793e4aba1f0dc0171d60f876c747679cfcf973`
- baseline: n/a (first review, no `--re-review`, no `--baseline`); `--iterations` ignored (one review)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- focus: requirements (Wiegers lead, Adzic, Cockburn), architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker active; Crispin on the boundary table
- citation convention: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. I checked every INV/CAPS citation I use against those files. Anything that points to `src/`, `~/.claude/` (other than the review-loop prompt), `CLAUDE.md`, `.dev/evals/`, `.dev/codegraph-migration/` or Orca sources is outside the workspace and is **UNVERIFIED** here; I rely on the inventory's quotation of it and say so.
- brief clauses overridden: none.

## Coverage statement
Covered: all of S:1-285. I read README.md, the three inventory files (targeted reads: INV-A:1-120 table rows and cross-cutting sections, INV-B rows for reflect, task, pr-submit, research, tasklist, workflow and the Needs-change and Decisions sections, CAPS:40-188) and checked the spec's counts (43 = 21 + 22; 10 + 27 + 6 = 43; 3.2 rows per phase 9/11/4/3 = 27; 3.1 rows plus 3.2 rows per phase = P1 14 behaviour-complete, P2 15, P3 4, P4 3) and cross-references (WC, SA, AC, D, F ids).
Not covered / not checkable: the 11 source locations the spec says it re-read (S:11), `EVIDENCE.md`, `CLAUDE.md`, the commands and skills themselves (not in the workspace). The F-/GR- finding ids the spec cites (F-01 to F-05, GR-B1, GR-B2) refer to a prior panel report that is not in the workspace (`review/spec-panel.md` and `disposition.md` do not exist here); I could not check them (UNVERIFIED).

## Grading
Each blocking finding carries the required sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." (prompt line 31). Findings that need a guess between two allowed readings, or that are a requirement the document never states, are Medium and sit under `follow-up candidates`.

=== REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking) Wiegers / Cockburn: `--unattended` is made accepted by 36 commands in P1, while the behaviour it promises arrives for 22 of them in P2-P4
Priority: High. Quality impact: safety and stall risk in P1-P3.
Texts that collide:
- S:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` (a no-op where a command has no gate)". That is 10 + 26 = 36 commands.
- S:73 (section 2.3): the brief carries "`--unattended` only for a command that already accepts it in the phase being run".
- S:60 (WC-2): under `--unattended` the command "never calls `AskUserQuestion`, never ends its turn on a chat question", and WC-9 (S:67) turns every push, PR, post, install, provision and paid call off.
- S:109-113, S:114, S:162 and S:154: the gate resolutions for implement, post-release and pr-submit are P4 and "wait for answers to D2-D4"; the 15 P2 commands convert in P2 (S:160); roadmap, save, validate-roadmap, validate-tests in P3 (S:161).
Quantity flow (FR-19, count divergence): 36 commands accept the flag after P1; 14 are behaviourally complete (8 no-gate P1 rows other than `load`, plus adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow). 22 accept it with the gate or outward default still as today (15 until P2, 4 until P3, 3 until P4).
Sentence: An implementer who follows the stated text as written adds `--unattended` to `/sc:post-release`, `/sc:pr-submit`, `/sc:task`, `/sc:cleanup` and `/sc:tdd` in P1, and a coordinator who follows section 2.3 passes it to them in P1-P3 because they "accept it"; that is wrong because WC-2 and WC-9 promise no prompt and no outward action under that flag, yet post-release still confirms and performs install, VM, commit and PR steps and the others still stop on a prompt the coordinator cannot see (a silent stall, S:60, CAPS:129), until P2-P4.
Why the acceptance checks do not catch it: AC-1.1 (S:195) tests only that a `## Unattended mode` section exists and names two strings; AC-1.2 (S:196) live-checks P1 commands only.
Recommendation (narrow, no new mechanism): in S:159 and S:73 state that a command accepts `--unattended` only in the phase that converts its own gates (the section 3 "Phase" column), or that before that phase the command refuses the flag with `status: blocked`. Delete "a no-op where a command has no gate" if it is not needed.

### B-2 (CRITICAL, blocking) Wiegers / Adzic: AC-0.4 cannot pass as written, and P0 gates the whole rollout
Priority: High. Quality impact: the acceptance criterion for the phase that tests the core decision is unsatisfiable.
Texts that collide:
- S:182 (7.2 step 3) passes only if "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (`<output-dir>/return-contract.yaml`, S:62).
- S:194 (AC-0.4) requires "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". It exempts only step 4.
- S:158 and S:73: P0 briefs omit `--unattended`, and the P0 commands do not write the WC-4 file: troubleshoot reports `REPORT.md` (S:91), workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92), and adversarial's contract is under `adversarial/` until the P1 fix (S:83; INV-A:60).
- S:154 and S:158: later phases do not start until the earlier phase's checks pass; a failure "reopens section 1" (S:194).
Sentence: An implementer who follows the stated text as written runs AC-0.4 on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial`, and step 3 can never pass for any of them, because step 3 demands a `status` and a path (`<output-dir>/return-contract.yaml`) that these commands do not produce before P1; an acceptance criterion cannot pass, so either P0 never closes or the implementer waives it and the evidence-gap closure (S:43) is unproven.
Recommendation: in AC-0.4, exempt the contract half of step 3 as well (match `--outcome` against the command's existing report, and take the report path from the file the command writes today), as S:194 already does for step 4.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The core decision (Orca on top, commands unchanged units; S:16-45) is internally consistent, its alternatives are rejected on evidence I could check (R1 `CAPS:97-103`; R2 `CAPS:147-149`; R3 `CAPS:76,150`; R4 `CAPS:145`; R5 `INV-A:90`, `INV-B:285-286`), and its own evidence gaps are stated (S:41-45, S:271-285). The Medium items below are listed under follow-up candidates.

### Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks; FR-8 to FR-10)
Table is complete: every guard in the spec with a threshold, flag test or sentinel is listed; a class that cannot occur is omitted with a one-line reason under the table. Status GAP rows are graded under FR-8/FR-9: none names a wrong outcome beyond B-1/B-2, so they are Medium (follow-up candidates).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit (60 s) | S:59 (WC-1), CAPS:44 | Typical | prompt falls back in 30 s | pass | worker-start succeeds (EVIDENCE.md:56 via S:59, UNVERIFIED) | OK |
| readiness limit (60 s) | S:59 | Maximum/Overflow | fallback at 45 s or more | fail | worker-start fails at `agent_readiness` (S:59) | OK |
| readiness limit (60 s) | S:59 | Legitimate Edge Case | `--timeout-ms` non-positive | falls back to 60 s | CAPS:44 only; the spec does not say what the brief may set | GAP (M-9) |
| gate resolution | S:60 (WC-2) | Zero/Empty | required flag supplied as `""` | not stated | not specified: default, supplied value or blocked? | GAP (M-9) |
| gate resolution | S:60 | Typical | gate hit, no flag | blocked | contract `status: blocked`, `blocked_question`, stop | OK |
| gate resolution | S:60 | Legitimate Edge Case | gate hit, then `ask` answered (WC-3) | re-invoke with the answer as a flag | S:61; what happens if the re-invoked run blocks again is not stated ("ask ... once") | GAP (M-9) |
| outcome mapping | S:63 (WC-5) | Zero/Empty | no report | `failed` | S:63 | OK |
| outcome mapping | S:63 | Typical | `partial` | `succeeded` | S:63, S:263 | OK |
| outcome mapping | S:63 | Legitimate Edge Case | report exists but is unparseable or has a `status` outside the four values | not stated | not specified (7.2 step 4 checks it only after the fact, S:183) | GAP (M-9) |
| wait split | S:68 (WC-10) | Typical | single call over 5 min | split | at most 4 min each | OK |
| wait split | S:68 | Legitimate Edge Case | single call of 4 to 5 min | neither | not stated; heartbeat cadence itself is UNVERIFIED (CAPS:130) | GAP (M-3) |
| wait split | S:68 | Sentinel Value Match | foreground Agent-tool fan-out call over 5 min | not stated | the rule says "a single tool call" but section 3 applies it only to cli-eval and pr-submit | GAP (M-3) |
| overwrite guard | S:64, S:87 (WC-6, GR-B1) | Typical | existing marked report, `--unattended` | true | contract `blocked`, no overwrite | OK |
| overwrite guard | S:64 | Legitimate Edge Case | existing file at `--output` that is not marked | not stated | not specified | GAP (M-9) |
| nesting depth (1) | S:66 (WC-8), CAPS:97-98 | Maximum/Overflow | worker calls `worker-start` | refused | `nested_worker_depth_exceeded`; WC-8 forbids the call | OK |
| circuit breaker (3) | S:263, CAPS:80 | Maximum/Overflow | three failed `worker-start` attempts | breaker trips | worker's own `failed` report does not count | OK |
| task confidence 0.70 | S:121 | Typical | below 0.70 | blocked | S:121 | OK |
| task confidence 0.70 | S:121 | One/Minimal | 0.70 to 0.89 band | not stated | the inventory ties the prompt to "< 0.70" only (INV-B:199); the band is unspecified | GAP (M-9) |
| `--unattended` acceptance | S:159, S:73 | Divergence (phase boundary) | command with a later-phase gate in P1 | accepts flag | gate still as today | GAP, blocking: see B-1 |
| additive-edit check (AC-C5) | S:176 | Typical | line removed by a named defect fix | exempt | SA-4 list S:149 | OK |

Omitted classes: "Zero/Empty" and "Sentinel Value Match" for the nesting depth and circuit breaker (they are counters set by Orca, cannot be empty or collide with a sentinel; `CAPS:100` covers the malformed setting); "One/Minimal" for the readiness limit (a one-millisecond limit is Orca's own setting, not a spec choice).

### Quantity Flow Diagram (FR-21, Fowler leads, Whittaker attacks)
```text
[Source: 43 commands in cmd/ (INV-A:3 21 + INV-B:3 22)]
   --> [Classify: S:76] --> [10 ready] [27 needing change] [6 coordinator-only]   (10+27+6 = 43, OK)
[27 needing change + 10 ready = 37] --> [P1 flag acceptance: 36 (all but load)]
   --> [Behaviourally complete after P1: 14]                 <-- MISMATCH (36 vs 14), finding B-1
   --> [P2 gate conversion: 15] --> [P3: 4] --> [P4: 3]      (14 + 15 + 4 + 3 = 36, OK)
[Consumer: coordinator brief S:73 passes --unattended to "any command that accepts it": uses 36]
[Consumer: WC-2/WC-9 promises: hold for 14 in P1]
```

### Adversarial analysis (Whittaker)
- Sequence attack on S:154-162 and S:73: I can break this specification by **Sequence Attack**. The invariant at **S:154 ("each phase independently useful, standalone unchanged") with S:60** fails when **P1 ships and P2-P4 have not**. Concrete attack: before: post-release has no unattended mode; after P1: it accepts `--unattended` (S:159) with WC-9 off until P4 (S:162); a coordinator pass of `--unattended` (S:73) leaves VM, install, commit and PR defaults on. Same finding as B-1.
- Sequence attack on P0: I can break this specification by **Sequence Attack**. The invariant at **S:154 ("later phases do not start until the earlier phase's checks pass")** fails when **AC-0.4 cannot pass**. Concrete attack: state before: P0 files written; the live run of `/sc:troubleshoot` yields `REPORT.md` and no `return-contract.yaml`; step 3 fails; P1 never starts. Same finding as B-2.
- Sentinel collision on the "blocked" outcome: `status: blocked` maps to `--outcome failed` (S:63), the same value as a real failure. A coordinator reading only Orca's outcome cannot tell a gate stop from a crash, and a `--retry-of` replacement worker (S:64) with the same brief hits the same gate. The spec says the coordinator opens the contract (S:62), so the information is recoverable; this is a note, not a finding.

## Follow-up candidates (Medium and minor; none blocks, none enters the Reviser brief)

Medium (warnings):
- **M-1 (MAJOR label, graded Medium) Wiegers: contract location is undefined for commands whose output flag is a file or absent.** WC-4 (S:62) puts the contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)". tdd (S:90, brief passes `--output <file>`), spec-panel (S:120 "add `--output`"), troubleshoot (S:91) and release-split (S:89) name no directory flag, yet AC-2.2 (S:200) expects a contract for `/sc:tdd ... --output <file>`. The real command definition used for this audit also differs: it already carries `--report-dir <dir>` for the contract and says `--output` "is file-valued" (command.md:460-461 in the audit sandbox; the repo copy cited at S:120 could not be compared, UNVERIFIED). Grade: needs a guess about which reading (dirname of the file, a new flag, `--report-dir`) the implementer picks. Suggest one directory-flag name per command in the section 3 tables.
- **M-2 Fowler: fresh directory versus a path fixed before dispatch.** WC-6 (S:64) says a command without a resume flag "writes each run into a fresh output directory"; WC-4 (S:62) and section 2.3 (S:73) fix the directory in the brief; WC-3 (S:61) re-invokes the same command after an `ask`. If the brief's directory is reused, a retry (`--retry-of`) overwrites the first attempt; if the command creates a subdirectory, the contract path is not known before dispatch. Say who creates the fresh directory (the coordinator, one per attempt).
- **M-3 Nygard: WC-10 covers polls and evals only.** The rule (S:68) is general ("a single tool call" over 5 minutes), but section 3 applies it to cli-eval (S:104) and pr-submit (S:114). Foreground Agent-tool fan-out in cleanup-audit, tdd, tasklist, roadmap, reflect can block a single call as long (INV-A:42, INV-B:46). The 5-minute heartbeat cadence is from this worker's own preamble, and whether Orca uses heartbeat age is UNVERIFIED (CAPS:130, CAPS:182), so no concrete wrong outcome is named.
- **M-4 Newman / Hohpe: tasklist `--unattended` departs from the inventory and adds a nested chain.** INV-B:46 and INV-B:215 say drop `--remediate` in Stage 10.5; S:122 keeps it and passes `--unattended` to each reflect, which under S:88 then follows the headless auto-accept rule for `--remediate` (INV-B:109). That auto-runs a workflow or task-builder remediation below tasklist and reflect, deeper than "one layer below the worker" (S:122). Nesting limit is three layers (INV-A:14); Agent loses its tool at the limit. Also inconsistent with the 3.1 reflect brief, which says no `--remediate` (S:88). Decide whether unattended tasklist should pass `--no-remediate` instead.
- **M-5 Cockburn: scope creep against non-goal 8.** Non-goal 8 (S:220) limits fixes to defects that stop a command working as a worker. `/sc:load`'s missing `--checkpoint` in its Usage line (S:112, S:265) and business-panel's frontmatter (S:102, effect UNVERIFIED, S:278) do not meet that test, while `/sc:agent`'s frontmatter is excluded on the same grounds. Also the P1 command list (S:159) omits init-lite, whose fix S:87 labels P1.
- **M-6 Crispin: the SA-2 check is weaker than the claim.** SA-2 (S:147) says no primitive runs an `orca` or `orca-ide` command; AC-C1 (S:172) greps only `orca(-ide)? (orchestration|worktree|terminal|agent)` in lowercase, so `orca status`, `orca open`, `orca-ide skills get` and `ORCA orchestration` pass. Widen the pattern or narrow SA-2.
- **M-7 Nygard: pr-submit as a worker is unreconciled with its own "Will Not: run headless".** INV-B:90 quotes `cmd/pr-submit.md:85` and `SKILL.md:225` ("Will Not: run headless / imply a daemon"). D3(b) (S:241) and the row at S:114 do not mention it. The spec also reads the 600 s as a cumulative budget (S:68, S:114) where INV-B:299 and INV-B:94 read "600 s per wait"; the spec's reading rests on `SKILL.md:46-64`, which I could not check (UNVERIFIED), and the spec itself flags the poll runtime UNVERIFIED (S:283).
- **M-8 Hightower / Crispin: verification steps that conflict with repo rules or miss counts.** AC-1.3 (S:197) and AC-4.3 (S:210) use a "scratch worktree" and "scratch fork PR"; the repo's CLAUDE.md says worktrees come from Orca with an agent and are never created for one's own use (UNVERIFIED here, not in the workspace). AC-2.4 (S:202) compares `--jq length`, which counts only the first page (default 30) of reviews and comments, so a posted comment on a long thread can leave the count unchanged.
- **M-9 Wiegers: the GAP rows of the boundary table above** (empty flag values, unparseable or out-of-vocabulary `status`, repeated block after an `ask`, unmarked existing file at `--output`, the 0.70 to 0.89 task band, `--timeout-ms` non-positive). Each is a requirement the document never states; none names a wrong outcome an implementer would produce on its own text.

Minor (notes):
- D5(b) (S:252) says raising depth would "break R1's protection against runaway fan-out"; R1 (S:33) is a refusal reason, not a protection. Wording only.
- S:11 says "11 of the load-bearing locations" re-read; the list contains 11 items, fine. The sources it names are outside the workspace (UNVERIFIED).
- E2 (S:22) and E3 (S:23) cite `EVIDENCE.md:45`, the PR #329 README and a `return-contract.yaml:10`; I confirmed only how the inventories quote them (`CAPS:49`, `CAPS:156`, `INV-A:35`).
- WC-3 (S:61) wording "ask the coordinator once" then "wait, then re-invoke" does not say whether the `worker_done` of WC-5 comes before or after the `ask`; the order is inferable (after).
- `S:285` item 14 (fresh evidence-validator found 9 defects) cannot be checked; the 9 = 5 + 3 + 1 arithmetic is consistent.

Issue creation: the session that ran this review did not ask the user whether to open an issue for the follow-up candidates, because the brief allows no interaction and this run only records the list; no issue was created.

## Reviser brief
Blocking finding ids: B-1, B-2. (Only these ids.)
Rules for the reviser (restated from the command's Review Loop bullet 6; the reviser reads this report, not the command):
- Revise only the text a blocking finding names: B-1 names S:73 and S:159 (and, if needed, the P4 rows S:109-114 and S:162); B-2 names S:182 and S:194.
- Add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table row cites its finding id.
- Prefer deleting or narrowing text to adding.
- Leave Medium and minor findings (M-1 to M-9 and the notes) alone, even under an "apply all findings" instruction.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Return the candidate once; do not award yourself a PASS. A re-review (`--re-review <this file> --baseline <saved copy>`) is the next step; the cap is 2 fix cycles (3 reviews).

verdict: FAIL
