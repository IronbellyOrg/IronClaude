review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `3cd5458f8a2ac3b837384ffb0c2d1ee1a68493aec2a3e3b821f7c0d4938d6464`
- Baseline: none given; no `--re-review`. This is a first review of the full document.
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`. No brief clause was overridden.
- Panel (focus order): Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active).
- Coverage: every section of the candidate (1-9, Decisions, UNVERIFIED), read in full. Each `INV-A:N`, `INV-B:N` and `CAPS:N` citation was checked against the three inventory files. Spot checks matched the cited content; I found no wrong line. `sk/`, `cmd/`, `CLAUDE.md`, `install_core.py`, `pyproject.toml`, `Makefile`, `EVIDENCE.md` and `.dev/codegraph-migration/*` citations cannot be opened in this sandbox. They are UNVERIFIED except where an inventory quotes the same line, and the spec's own re-read claim (spec:11) was not re-checked. The only difference between copies is `sc-pr-submit-protocol/SKILL.md` top-level rule at `:37-39` (spec:65, INV-B:90) versus `:47-49` (CAPS:40,161). They are likely different copies, repo `src/` versus installed `~/.claude/`. UNVERIFIED which is current.

## Grading note

One finding is blocking (B-1). Every other finding is Medium or minor and goes under `follow-up candidates`, per `command.md:259` and `document_review_loop_prompts.md:31`.

=== REQUIREMENTS ANALYSIS ===

### B-1 [MAJOR, blocking] AC-0.4 requires a WC-4 contract path that no P0 smoke command can produce
- Expert: Wiegers (testability), Adzic (example), Crispin-style acceptance check.
- Grading sentence: an implementer who follows AC-0.4 as written (spec:194) builds a P0 gate that cannot pass, and it is wrong because the text relaxes only step 4 while step 3 still demands "its report path is the WC-4 contract path" (spec:182). The P0 smoke commands are `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial`.
- Evidence:
  - `/sc:troubleshoot` reports `REPORT.md`. It writes `return-contract.yaml` only with `--caller task-unified` (spec:91, INV-B:242).
  - `/sc:adversarial` writes its contract at `<output>/adversarial/return-contract.yaml` in real runs, and the path fix is scheduled for P1 (spec:83 "P1; M2", INV-A:35,60).
  - P0 is "no command edits" (spec:158).
  - AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (spec:194).
  - Step 3 also says the `--outcome` must "match the contract's `status` under WC-5". No contract exists at P0.
  - AC-0.4 ends "a failure here reopens section 1" (spec:194), so a literal, unavoidable failure reopens the central decision.
- Recommendation: narrow AC-0.4. Say that for P0 steps 3 and 4 use the command's existing report file and `worker_done` outcome, and that the WC-4 path and `status` match are checked from P1. Delete rather than add a mechanism.
- Priority: High. Quality impact: Testability -2.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision itself (Orca coordinates, commands stay units of work, section 1) is internally consistent and its evidence lines check against `CAPS`. The shipped-contract-file design is a reasonable single-owner split. Architecture issues are in the follow-up list (M-4, M-6, M-9, M-12, M-16).

## Guard Condition Boundary Table (Nygard builds, Crispin completes, Whittaker attacks)

The spec contains guards and thresholds, so the table is required. Input classes that cannot occur are left out with a one-line reason. Rows are the guards that decide an outcome.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | spec:68 | Zero/Empty | 0 s wait | no split | none needed (no wait) | OK |
| WC-10 wait split | spec:68 | Typical | 3 min Bash wait | no split | heartbeat each 5 min | OK |
| WC-10 wait split | spec:68 | Maximum/Overflow | one Agent-tool call of more than 5 min (cleanup-audit waves, INV-A:42; tdd, INV-B:221) | rule says "single tool call" but the example and fix cover only Bash polls | not stated; cannot be split | GAP (M-9) |
| WC-10 wait split | spec:68, AC-4.3 spec:210 | Legitimate Edge Case | 4 min 30 s wait | rule triggers only above 5 min; requirement says "at most 4 min"; AC-4.3 uses 240 s | contradictory band (4, 5] min | GAP (M-9) |
| WC-5 outcome map | spec:63 | Typical | `status: partial` | succeeded | stated | OK |
| WC-5 outcome map | spec:63 | Sentinel Value Match | `status` outside the four values (existing contract vocabularies; "keep their fields", spec:62) | not defined | not stated | GAP (M-10) |
| WC-5 outcome map | spec:63 | Zero/Empty | contract file empty or unparsable | not defined (only "no report exists" is stated) | not stated | GAP, minor |
| WC-1 readiness | spec:59 | Typical | 30 s fallback | passes | `EVIDENCE.md:45` via spec | OK |
| WC-1 readiness | spec:59 | Legitimate Edge Case | 45-60 s fallback | "well inside" is not a number; spec cites failure above about 45 s | not stated | GAP (M-15) |
| Task confidence | spec:121 | Legitimate Edge Case | exactly 0.70 | "below 0.70" resolves blocked, 0.70 proceeds | stated by the row | OK |
| Nesting depth | spec:33, CAPS:97 | Typical | depth 1 | worker-start refused | stated (call sites UNVERIFIED, CAPS:103) | OK |
| WC-4 contract directory | spec:62 | Zero/Empty | no `--output`, empty or unwritable directory | blocked contract has no valid path | not stated; spec:113 itself makes `--output` a blocked-if-missing input | GAP (M-2) |
| WC-4 contract directory | spec:62 | One/Minimal | two workers whose `--output` files share a directory (tdd default `docs/<domain>/`, INV-B:222) | both write the same `return-contract.yaml` | WC-11 (spec:69) forbids it; WC-4 causes it | GAP (M-1) |
| SA-3 contract write | spec:148 vs spec:62 | Legitimate Edge Case | new output flag passed, no `--unattended` | SA-3 says allowed, WC-4 says unattended only | two readings | GAP (M-11) |

Classes left out: Maximum/Overflow and Sentinel for WC-1 (a timeout has no collision class); Zero/One for the 0.70 and depth guards (a count of workers or a score of 0 maps to the same typical rule).

## Quantity Flow Diagram (Fowler counts, Whittaker attacks)

```text
[43 commands: INV-A:3 (21) + INV-B:3 (22)] --> [verdict split]
   --> [10 ready (spec:78-92)] --> P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow)
                                 P2 fixes 4 (reflect, release-split, tdd, troubleshoot)
                                 unphased 2 (brainstorm, init-lite)             = 10  conserved
   --> [27 need change (spec:94-125)] --> P1 9 + P2 11 + P3 4 + P4 3           = 27  conserved
   --> [6 coordinator-only (spec:127-137)]                                      = 6   conserved
   Consumers: AC-1.1 (spec:195) asserts the P1-P3 set only; implement, post-release, pr-submit (P4) and
   the two unphased ready commands have no section-presence check. Not a count mismatch; listed as M-5.
```

No dimensional mismatch found. Counts conserve (10 + 27 + 6 = 43), and the phase lists match the section 3 phase column.

## Follow-up candidates (Medium and minor; none fails the review)

Each Medium finding is a requirement the document does not state, or a case that needs a guess between two readings the text allows.

Medium:
- M-1 [MAJOR-label, Medium; Wiegers, Whittaker]. WC-4 (spec:62) derives the contract directory from the file for file-valued flags (tdd, init-lite). TDD defaults to `docs/<domain>/TDD_<COMPONENT>.md` (INV-B:222), so two workers writing different components in one domain write the same `return-contract.yaml`, which WC-11 (spec:69) forbids. It becomes wrong only if the coordinator picks one shared directory. Recommend: require a unique contract directory per Task, or name the contract after the Task.
- M-2 [Medium; Whittaker]. WC-4 says "written on every outcome ... including stops before any other output exists" (spec:62), but spec:113 makes `--output` an input whose absence resolves "blocked", and no rule says where a blocked contract goes with no valid directory. WC-5 would then report `failed` with the question lost (spec:63). `command.md:460` shows a shipped answer (refusal printed in chat, contract path unknown). That file is outside the inventory and not an evidence line. Recommend: state the no-directory case.
- M-3 [Medium; Wiegers]. WC-4 requires each fixed or generated-directory row to name the contract path (spec:62). Rows for index-repo (spec:86), recommend (spec:115), research (spec:116), save (spec:119) and task (spec:121) name none.
- M-4 [Medium; Fowler, Nygard]. P1 adds `--unattended` acceptance for every phased command, with the gate conversion in P2 (spec:159-160, "a no-op where a command has no gate"). In the interim an `--unattended` flag on a gated command is accepted without WC-2/WC-9 behaviour, for example `/sc:auggie-review` keeps PR posting until P2 (spec:100). Section 6 says phases are independently useful (spec:154). The text reads two ways: flag only, or flag plus gate. Recommend: state that P1 adds the flag only where the command has no gate, or that a gated command refuses `--unattended` until its P2 row lands.
- M-5 [Medium; Adzic]. Section 2.3 says the brief carries "the exact command line including `--unattended`" for every Task (spec:73). `/sc:brainstorm` and `/sc:init-lite` (unphased, spec:195 "M1") and `/sc:load` (spec:76) never gain the flag. Also, spec:81 says ready commands "report the named file until Phase 1 adds the contract", but those two never reach P1. AC-1.1 (spec:195) and no other check cover P4 commands.
- M-6 [Medium; Newman]. AC-C1 passes only if no `orca orchestration|worktree|terminal|agent` text appears under `src/superclaude/{commands,skills,agents,core}` outside `ccsession-tag` (spec:172). SA-2 allows an Orca mention as an example in the contract file (spec:147), and P0 adds an Orca section to `HOW-WE-WORK.md` (spec:158) and a coordinator brief template. Any literal `orca orchestration ask` or `worker-start` text fails AC-C1. Recommend: narrow AC-C1 to `commands/`, `skills/` and `agents/`, or exclude the two core files.
- M-7 [Medium; Crispin]. AC-C5 (spec:176) fails on any deleted line, but SA-4 permits "new flags" (spec:149). Adding `--unattended` to an existing Usage line produces a `-` line. Recommend: say new flags go on a new line, or exempt the Usage line.
- M-8 [Medium; Crispin]. AC-1.2 runs each P1 command with `--unattended --output <dir>` (spec:196), but cleanup-audit (fixed `.claude-audit/`, spec:85), index-repo (spec:86) and workflow (generated package, spec:92) take no `--output`.
- M-9 [Medium; Nygard, Whittaker]. WC-10 only handles Bash waits (spec:68). A top-level session blocked on one long Agent-tool fan-out cannot heartbeat at all. The effect of a missed heartbeat on liveness is UNVERIFIED (CAPS:130,182). Also see the (4, 5] min band in the guard table.
- M-10 [Medium; Newman, Hohpe]. WC-4 fixes `status` to four values but says existing contracts "keep their fields" (spec:62). Existing vocabularies are UNVERIFIED (INV-A:35, INV-B:112,272). Also WC-5 maps `partial` and a FAIL audit to `succeeded` (spec:63, Decisions spec:263), and a completed Task unblocks dependents (CAPS:90), so a coordinator that relies on Task status without opening the report starts dependents on a partial result. Section 2.3 does say the coordinator opens the report (spec:73). Recommend: add a mapping line for non-vocabulary values, and a `partial` note for dependents.
- M-11 [Medium; Wiegers]. SA-3 allows contract files "when the caller passes the new output flag" (spec:148), WC-4 writes them "in unattended mode" (spec:62), and AC-1.3 tests only the no-flag case (spec:197). A person running `/sc:analyze --output x` in a plain session gets an unspecified result.
- M-12 [Medium; Nygard, Whittaker]. WC-6 "fresh output directory" (spec:64) versus WC-4 "directory the coordinator passed" leaves open who creates the fresh directory. Examples: a `tdd` retry without `--resume` overwrites the `--output` TDD file (spec:90), and AC-3.2 enshrines `/sc:roadmap` starting fresh in an existing `<dir>` (spec:205), overwriting a prior session if the brief omits the resume flag. Recommend: state that the coordinator supplies a new directory per Dispatch.
- M-13 [Medium; Whittaker, sentinel collision]. D1(a) selects a standalone flag (spec:228) but never says it counts only as an argument token outside quoted content. A topic such as `"why does --unattended fail"` would trigger the mode. `command.md:459` states that rule for spec-panel; it is not a spec requirement.
- M-14 [Medium; Fowler]. The tasklist row passes `--unattended` to each reflect so the headless rule applies (spec:122), and the reflect row makes `--remediate` follow the auto-accept rule (spec:88). INV-B:215 recommended dropping `--remediate` in Stage 10.5. The consequence of auto-accepted remediation inside a tasklist worker is unstated. Also "one layer below the worker" (spec:122) understates INV-B:210, where each reflect subagent fans out further (nesting works, UNVERIFIED, INV-A:112).
- M-15 [Medium; Wiegers]. WC-1 says "well inside" the 60 s limit (spec:59), which is not measurable, and it has no owner phase in section 6 (spec:156-162).
- M-16 [Medium; Nygard]. Section 1.4(2) admits a silent stall is visible only through `worker-show` or a missing report (spec:44). Section 2.3 gives the coordinator no polling duty; only the test checks it (spec:181). WC-12's "natural checkpoints" is undefined (spec:70).
- M-17 [Medium; Cockburn]. D4(a) requires the user's own instruction to name the action (spec:245), but WC-9 allows it by flag in the brief (spec:67). P2 proceeds "on the recommendations" (spec:225), yet auggie `--post-pr` and task `commit`/`push` (spec:100,121) depend on D4.
- M-18 [Medium; Cockburn]. The `/sc:git` rationale ("need the user's authorization in this repo", spec:133) and WC-9 (spec:67) cite `README.md:31`, which is the planning-run worker rule, not a repo-wide policy. The repo-wide basis is UNVERIFIED here.
- M-19 [Medium; Newman]. The plugin mirror update rule is unresolved (UNVERIFIED #8, spec:279); no acceptance check covers `plugins/superclaude/commands/`. AC-C2 (`make verify-sync`) covers `.claude/` only (spec:173).
- M-20 [Medium; Crispin]. AC-0.4 says the "no Agent-tool wrapper" fact is verified in the step-5 transcript (spec:194), but step 5 only searches for `AskUserQuestion` (spec:184).

Minor (notes):
- Unresolved tags `(M1)`, `(M2)`, `(M4)`, `(M5)`, `(M6)` appear throughout (spec:11,52,62,76,83,176,195) and are explained nowhere in the document; they appear to come from a disposition file not in this audit.
- E3 (spec:23) cites `invocation_method: "skill-direct"` as a precedent, while section 1.4(1) says the PR #329 run proved only the nested route (spec:43); the evidence text is not consistent between the two.
- Contract has no schema version field (spec:62), though workflow's contract carries one (INV-B:272).
- AC-2.4 `gh api ... --jq length` counts one page only (spec:202); use `--paginate`.
- cli-eval `run` is gated only by `--suite` and safety flags, but WC-9 also lists a paid external run (spec:67,104).
- UNVERIFIED item 14 (spec:285) is a statement, not an unverified item.
- Section 1.1 says command changes are "limited to" three contract items (spec:16), while section 3 also lists defect fixes (spec:118,124,125,108,102); SA-4 acknowledges them (spec:149).

## Issue offer
The review session is a non-interactive worker run. Whether to open an issue for the follow-up candidates is left to the coordinator, who should ask the user once for this loop. This report creates no issue.

## Reviser brief
Blocking finding ids: B-1

Reviser contract (restated from `command.md:263`; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that a blocking finding does not call for; cite the finding id on each added paragraph or table; prefer deleting or narrowing text to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
