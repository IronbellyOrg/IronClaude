review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `79f7d923a8aec892c0aa73658332d8e091d8ce46bc45e64a342ab24dea176c15` (286 lines, 58669 bytes). Cited below as `SPEC:N`.
- Baseline / prior report: none given. This is a labelled whole-document audit, a first review of the full document. No baseline is claimed.
- Reviewer model actually used: claude-sonnet-5-5.
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`. Brief clauses overridden: none.
- Coverage: the whole document (sections 1-9, Decisions, UNVERIFIED items). I checked every `INV-A:N`, `INV-B:N`, `CAPS:N` and `README.md:N` reference I could resolve against `.dev/orca-command-refactor/inventory/*.md` and `.dev/orca-command-refactor/README.md`. All resolved to the stated content. I did not re-run the source-file greps or `orca-ide` output.
- Panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, active every review); Crispin (guard-table completeness). Hightower, Gregory not engaged by the focus areas.
- Citations I cannot check in the sandbox are UNVERIFIED: `CLAUDE.md:*`, `src/superclaude/**` line cites quoted only through the inventories, `EVIDENCE.md:*` (seen only as quoted at `CAPS:49`), `.dev/codegraph-migration/**`, `pyproject.toml:38`, `Makefile:68-74`, the grep results at `SPEC:25`, and the self-attested citation checks at `SPEC:11` and `SPEC:285`.
- Medium/minor findings are listed under `follow-up candidates`. The session was not asked whether to open an issue and none was created (sandbox, no user channel).

## Summary

The decision (Orca on top, commands stay units of work) is well supported by the inventories. The counts reconcile: 10 ready (`SPEC:81-92`), 27 needing change (`SPEC:97-125`), 6 coordinator-only (`SPEC:130-137`), matching `INV-A:73` and `INV-B:278`. The phase lists at `SPEC:159-162` match the Phase column of section 3.2 and the 3.1 small fixes. One blocking finding: the report-file location rule cannot be satisfied for the commands whose output flag is a file.

=== REQUIREMENTS ANALYSIS ===

### B1 [MAJOR, blocking] WC-4 puts the contract in an output directory, but the spec's own tdd brief and acceptance check pass a file
- Expert: Wiegers (lead), Adzic.
- Grading sentence: an implementer who follows the stated text builds `/sc:tdd ... --unattended --output <file>` so that it writes `<file>/return-contract.yaml`, because WC-4 says the contract goes in `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)" (`SPEC:62`). That is wrong because `<file>` is a file, so the path cannot exist. No contract is written, WC-5 then maps "no report exists" to `--outcome failed` (`SPEC:63`), and AC-2.2 cannot pass.
- Contradicting texts:
  - 3.1 tdd row: brief passes `--output <file>`, report "the TDD at `--output`" (`SPEC:90`, from `INV-B:47,222`).
  - AC-2.2 literally runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked` with a non-empty `blocked_question`" (`SPEC:200`).
  - 7.2 step 4 does `test -s <contract>` (`SPEC:183`), with no definition of `<contract>` for a file-valued flag.
  - Section 2.3 tells the coordinator to state "the output directory" in the brief (`SPEC:73`).
  - Several P1/P2 rows say only "add `--output`" or "add a report path" without saying file or directory (`SPEC:99,101,106,108,120`). `spec-panel` is the same case.
- Concrete attack (Whittaker, divergence): at the boundary between a file-valued and a directory-valued output flag, the rule has no branch. State trace: before, brief = `--output out/TDD.md`; after, contract path = `out/TDD.md/return-contract.yaml`, ENOENT/ENOTDIR, report absent, outcome `failed`. The same applies to any P1/P2 command whose new flag is given as a file.
- Recommendation: state in WC-4 where the contract goes when the output flag names a file (for example beside it, or in a separate `--report-dir`), and make the "add `--output`" rows say which kind. Narrow, do not add a mechanism. Priority High.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. Fowler/Newman: the boundary (coordinator plans, command executes, contract file is the only interface) is clean, and R1-R5 (`SPEC:31-37`) are consistent with `CAPS:97-103,145-150`. Hohpe/Nygard concerns are Medium (below).

## Guard Condition Boundary Table
Classes left out: "One/Minimal" for every guard (no guard in this spec has a distinct minimal-value rule); "Maximum/Overflow" where no numeric bound applies.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | SPEC:16,51 | Zero/Empty | flag absent | off | today's behaviour (SA-1, SPEC:146) | OK |
| `--unattended` switch | SPEC:128,154 | Legitimate Edge Case | flag passed to a section-4 command, or to brainstorm/init-lite/load which "gain neither" | undefined | not specified (no refusal, no ignore rule) | GAP (F-M1) |
| WC-4 output location | SPEC:62 | Typical | directory-valued flag | contract in dir | specified | OK |
| WC-4 output location | SPEC:62,90,200 | Legitimate Edge Case | file-valued flag (tdd) | undefined | contradicts AC-2.2 | GAP (B1) |
| Contract written | SPEC:62,148 | Zero/Empty | `--output` given, no `--unattended` | WC-4 says no, SA-3 says yes | two readings | GAP (F-M2) |
| WC-10 wait split | SPEC:68,114 | Maximum/Overflow | `--poll-interval` > 240 s | sleep > 4 min | not capped | GAP (F-M10) |
| WC-10 wait split | SPEC:68 | Typical | single call ≤ 4 min | heartbeat fits | specified | OK |
| Readiness limit | SPEC:59 | Typical | fallback 30 s of 60 s | ok | specified | OK |
| Confidence gate (task) | SPEC:121 | Sentinel Value Match | exactly 0.70 | "below 0.70" | blocked only below 0.70 | OK |
| Worker end state | SPEC:63,183 | Zero/Empty | worker dies, no `worker_done`, no contract | undefined | no coordinator rule | GAP (F-M4) |
| Nesting depth | SPEC:66 | Typical | depth 1 | WC-8 forbids | specified | OK |

FR-8/FR-9 grading: each GAP above is a requirement the document never states (not a stated text doing harm), so Medium, except B1.

## Quantity Flow Diagram
```text
[43 commands] --> [inventory split] --> [10 ready + 27 needs-change + 6 coordinator-only = 43]   (reconciles, SPEC:76)
[N Tasks started] --> [N worker sessions] --> [<= N worker_done] --> [<= N contract files]
                                                  |                      |
                                                  v                      v
                                  coordinator reads M contracts (M <= N) <-- MISMATCH when a worker dies (F-M4)
[P1 asserted: every command of phases <= P1 has the section] --> AC-1.1 (SPEC:195)  consistent with SPEC:154,159
```
Only the contract-flow divergence matters; graded Medium because the failure needs a worker crash the document never discusses.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

- B1 above (divergence attack, file vs directory).
- Sentinel collision: none found; the four `status` values are closed (`SPEC:62`).
- Sequence attack: WC-3 says ask once, wait, then "re-invoke or resume the command with the answer as a flag" (`SPEC:61`); see F-M3 for gates with no such flag.
- Accumulation attack: circuit breaker of 3 failures (`CAPS:80`) is not affected by `blocked` reports; fine.

## follow-up candidates (Medium and minor; none triggers a revision)

Medium (each needs a reading choice or is a requirement the document never states):
- F-M1 (Nygard/Whittaker): behaviour of `--unattended` on a section-4 command, or on brainstorm/init-lite/load, is unstated (`SPEC:128,154`).
- F-M2 (Wiegers): WC-4 says the contract is written "in unattended mode" (`SPEC:62`); SA-3 says "only in unattended mode or when the caller passes the new output flag" (`SPEC:148`); AC-1.3 only tests neither flag (`SPEC:197`). Whether `--output` alone writes the contract is unstated.
- F-M3 (Cockburn): WC-3 resumes "with the answer as a flag" (`SPEC:61`), but cli-portify's three approval gates resolve as blocked with only a `--resume` flag (`SPEC:105`) and release-split's `--r1-scope custom` and tasklist-input blocks (`SPEC:89`) name no input that carries the answer. A resumed run could hit the same gate and block again.
- F-M4 (Nygard/Hohpe): no rule for a worker that never sends `worker_done` or writes no contract; WC-5 covers only a worker that reports (`SPEC:63`); 7.2 step 2 only polls (`SPEC:181`). `CAPS:111,126` say not to release or stop on silence, so the coordinator needs a stated path.
- F-M5 (Newman): WC-11 forbids two workers writing the same file (`SPEC:69`) but several ready/changed commands write fixed shared paths: index-repo `PROJECT_INDEX.md` (`SPEC:86`), cleanup-audit `.claude-audit/` (`SPEC:85` admits one audit per worktree), and editing commands (cleanup, improve, document, test `--fix`) default to a shared worktree (`CAPS:115`). No requirement keeps edit workers apart.
- F-M6 (Crispin): AC-C1 greps `src/superclaude/core` for `orca ... orchestration|worktree|terminal|agent` with only `ccsession-tag` excluded (`SPEC:172`), while SA-2 allows an Orca mention in the contract file (`SPEC:147`) and P0 adds an Orca section to `HOW-WE-WORK.md` (`SPEC:158`, SA-5 `SPEC:150`). A natural mention fails P0.
- F-M7 (Wiegers): the index row says "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)" (`SPEC:111`) while UNVERIFIED item 6 says section 3 "refuses or pins" it regardless (`SPEC:277`). The row does neither; if the mode does wait, WC-2 fails silently.
- F-M8 (Hohpe): tasklist Stage 10.5 under `--unattended` passes the flag to reflect (`SPEC:122`), but `needs_human_decision` HALTs (`INV-B:209`) are not mapped to blocked. The "inside Claude Code's nesting limit" claim rests on `INV-A:14` while `INV-B:210,314` mark nested spawning UNVERIFIED.
- F-M9 (Adzic): AC-0.4 compares the outcome to "the status in the command's existing report" and uses "that file" as the report path (`SPEC:194`). For adversarial the 3.1 row says the filename is not fixed (`SPEC:83`, `INV-A:60`), and nothing shows troubleshoot's REPORT.md has a status field (`INV-B:242`). The P0 smoke runs for those two cannot be judged pass or fail as written.
- F-M10 (Nygard): WC-10 caps single waits at 4 minutes (`SPEC:68`) but pr-submit's sleep is "at least `--poll-interval`" (`SPEC:68`); a larger interval breaks the cap. The command change is hedged on UNVERIFIED poll runtime (`SPEC:114,283`).
- F-M11 (Wiegers): WC-9 turns off "a paid external run" (`SPEC:67`); research and review-translation use Tavily web search by default (`INV-B:134,144`) and their rows do not say whether that is off (`SPEC:116-117`).
- F-M12 (Fowler): auggie-review "posting returns only with an explicit `--post-pr`" (`SPEC:100`); the inventory shows only `--no-post-pr` (`INV-A:38`), so the flag may be new, not listed as an added flag. D4, which governs it, is a P4 decision (`SPEC:244`) while the change is P2 and P2 "adds no outward capability" (`SPEC:160`).
- F-M13 (Crispin): AC-C5 requires zero deleted lines for edits without a named defect fix (`SPEC:176`); documenting new flags in a one-line Usage line deletes that line. SA-4 (`SPEC:149`) does not say where flags are documented.

Minor notes:
- n1: "F-1", "F-2", "F-3" are used as rule references (`SPEC:73,154,176,194`) and "ladder rung 2" at `SPEC:261`, with no definition in the document.
- n2: `SPEC:154` says Phases 1-3 need no user decision, while D1 (flag versus detection) is a user decision they depend on; `SPEC:225` resolves this by proceeding on recommendations.
- n3: E2 says the worker "answered" citing `EVIDENCE.md:45` (`SPEC:22`); `CAPS:49` quotes only `state: ready, stage: input_accepted`.
- n4: section 1.3 R1 is stated as certain while `CAPS:103` marks the enforcing call sites UNVERIFIED; the text does say so.
- n5: "fresh dir" in many 3.2 rows (`SPEC:99-125`) does not say what a command that writes a single file at a fixed path does on re-run.

## Verified and not-verified claims
- Verified against files in the workspace: counts at `SPEC:76`; all `INV-A`/`INV-B` row references in 3.1, 3.2, 4; `CAPS` references in section 1.2-1.4, WC-1 to WC-12, section 8, D1/D5; `README.md:6,11-17,30,31`; phase membership at `SPEC:159-162`.
- UNVERIFIED (outside the sandbox): see Coverage list above.

## Reviser brief
Blocking finding ids: B1.
Rules for the reviser (restating the command's Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.

verdict: FAIL
