review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Kind: labelled whole-document audit, a first review of the full document (no `--re-review`, no `--baseline`; `baseline: missing` not applicable, none was requested).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `06730fb96147b55377f384ee4605e4ba1f6a74c60f4f348ab9d5de3b86c1559f`
- Baseline sha256: none given.
- Reviewer model used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (grading check at `:31`, brief at `:32`).
- Run mode: not `--unattended`; the Improve step was not run and the candidate was not edited.
- Evidence rule: the only checkable evidence is inside the workspace. Citations into `src/`, `CLAUDE.md`, `pyproject.toml`, `EVIDENCE.md`, `.dev/codegraph-migration/` and the `.claude` skills are UNVERIFIED (not in workspace). Citations to `INV-A`, `INV-B`, `CAPS` and the README were checked.

## Coverage (what was covered)

- Read in full: command definition, README (`README.md:1-38`), review-loop prompts, the candidate (285 lines).
- Cross-checked against inventories: command counts and the 10/27/6 split (`commands-a.md:3,76-83`, `commands-b.md:3,289`, candidate `:76-125`); phase assignment conservation (below); the Orca facts the requirements lean on (`orca-capabilities.md:44-47,52,58,64,66-67,72-80,86,92,97-103,107-116,129-130,145-161,176-188`); the inventory remarks the candidate leans on (`commands-a.md:62,95-98,106,113,118,120`, `commands-b.md:210,272,285-286,292,311,314,320,323`).
- Spot-check of about 60 `INV-A:`/`INV-B:`/`CAPS:` citations: every one checked says what the candidate claims, except the points under S-4 and S-8. Citations to non-workspace files were not checked.
- Not covered: the focus areas `testing`, `compliance`, `correctness` (not requested); the state variable registry (only produced under `--focus correctness`). Guard Condition Boundary Table and count-flow check below were produced because the spec contains thresholds and a multi-stage phase flow.

## Panel (review order per command definition)

Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard (architecture); Whittaker (adversarial, active in every review); Newman, Hohpe (architecture lens). Crispin, Gregory and Hightower have no lead role under the requested focus and are not attributed.

=== REQUIREMENTS ANALYSIS ===

### Blocking findings

**B-1. MAJOR and blocking. Acceptance check AC-0.4 cannot pass for its first listed command. (Wiegers, Adzic)**
- Grading sentence: an implementer who follows the stated text as written builds a P0 smoke test whose step 4 runs `yaml.safe_load` and asserts `d['status']` and `d['command']` on "the command's existing report file" (candidate `:194`, step 4 text at `:183`), and for `/sc:troubleshoot` that file is `REPORT.md` (candidate `:91`), a markdown report with no `status` or `command` key; the check raises (string or parse error, then `d['status']` fails), so AC-0.4 cannot pass, and the P0 gate ("a failure here reopens section 1", `:194`) fires on a check defect, not on a decision defect.
- Same text breaks the other half: step 3 requires `--outcome` to "match the contract's `status` under WC-5" (`:182`), and a markdown `REPORT.md` has no such status, so there is nothing to match against.
- The adversarial smoke run is also unsound: the spec says its contract file name is not fixed and its fields are only "promised" (candidate `:83`, `commands-a.md:97`), so `status`/`command` keys in the existing contract are not established (UNVERIFIED); only the workflow contract is documented with a `status` field (`:92`).
- Recommendation: for P0 only, state a different step 4 for pre-P1 commands (file exists and is non-empty, plus the worker's body states the outcome) and keep the YAML assertion for P1 onward. Priority High.
- Quality impact: P0 is the gate that "tests the decision before anything is built on it" (`:158`); as written it cannot go green.

**B-2. MAJOR and blocking. The additive-edit check AC-C5 (and AC-0.3) passes when existing bullet lines are deleted. (Wiegers, Nygard)**
- Grading sentence: an implementer who follows the stated text as written runs `git diff -U0 master...HEAD -- <file> | grep -E '^-[^-]'` (candidate `:176`, same pattern at `:193`) and gets no output when an existing line such as `- Foo` is deleted, because the diff shows it as `-- Foo`, which the `[^-]` excludes (reproduced: `printf -- '-- bullet deleted\n' | grep -E '^-[^-]'` prints nothing; `-plain deleted` does match); so the check reports "edits are additive" for edits that remove standalone behaviour, and SA-4 and SA-1 (`:146,149`), declared a hard requirement on every phase (`:142`), are not actually enforced.
- Commands and skills in this repo are mostly bullet-heavy markdown, so the escaped class is common, and blank-line deletions (`-` alone) also pass.
- Recommendation: replace the pattern with a deleted-line count that excludes only the `---` header, for example `grep -E '^-' | grep -vE '^---( |$)'`. Priority High.
- Quality impact: restores the check's meaning at one line of change.

### Medium (follow-up candidates; not blocking)

**M-1. Which ready commands get `--unattended`, `--report-dir` and the `## Unattended mode` section is not stated consistently.**
- Section 2.3 says every brief carries `--unattended` and `--report-dir` (`:73`); WC-4 says "every unattended command accepts" `--report-dir` (`:62`); the 3.1 table says the ten ready commands run "if the brief uses the stated flags" with no `--unattended` (`:79-81`) and gives brainstorm and init-lite "None" as the fix (`:84,87`); section 6 P1 names adversarial, cleanup-audit, index-repo and workflow only as "fixes" (`:159`), and AC-1.1/AC-1.2 apply to "every command named in the P1 row" (`:195-196`).
- Two readings are allowed (the four fix-only commands get the section and flags, or they do not); brainstorm and init-lite never get a phase at all, so an unattended worker brief for them either passes an unknown flag or has no contract. Needs a guess about the implementer's reading, so Medium. (Cockburn)
- Recommendation: add one column "gets `--unattended` in phase" to 3.1, or one sentence in section 6.

**M-2. WC-4 versus the fixed adversarial path.** WC-4 puts the contract at `<report-dir>/return-contract.yaml` (`:62`); 3.1 fixes adversarial at `<output>/adversarial/return-contract.yaml` (`:83`); AC-1.4 only asks that "one fixed path" be named (`:198`). The coordinator cannot know the path before dispatch (WC-4's own goal) unless the two are reconciled. (Adzic)

**M-3. Stale contract on retry or reuse (Whittaker, Sequence Attack).** I can break this specification by **Sequence Attack**. The invariant at **WC-4/WC-5/WC-6 (`:62,63,64`)** fails when a retry worker (`--retry-of`) is given the same `--report-dir` the coordinator fixed before dispatch (`:73`). Concrete attack: attempt 1 writes `status: succeeded`; the coordinator retries (for example after the pane died before `worker_done`); attempt 2 crashes before writing; the contract on disk still says `succeeded`, and WC-5 ("no report exists" means `failed`) never triggers. The spec says "fresh output directory" for commands without a resume flag (`:64`) but 2.3 fixes one directory per Task. Missing requirement: remove or overwrite the contract first, or one directory per Dispatch.

**M-4. WC-3 re-invocation versus the fixed report path (Whittaker, Divergence Attack).** After a blocked gate the worker may `ask` and then "re-invoke or resume" the command (`:61`). For the 17 or so commands whose resume is "fresh dir" (`:99-125`), re-invocation starts a new run; the report location the coordinator expects from the brief may not be the new run's. Also AC-2.2 requires `worker_done --outcome failed` on a gate-trigger run (`:200`), which the `ask` branch of WC-3 would not produce. Make the `ask` branch explicitly optional in the brief or tell the worker to skip it.

**M-5. `--unattended` without `--report-dir`.** WC-4 requires the flag and 3.1/3.2 assume it (`:62,73`) but no text defines what a command does when it is missing (zero/empty case); the sibling `/sc:spec-panel` definition refuses before any work (`command.md:460`), the candidate leaves it open (and itself notes the spec-panel definition as UNVERIFIED, `:62`).

**M-6. Tasklist row asserts more than the inventories support.** The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" (`:122`). `INV-B:210` describes Stage 10.5 as subagent to agent nesting (reflect itself spawns two agents) and marks whether nested spawning works UNVERIFIED; `INV-A:14` is about the limit generally. That is two layers below the worker and unproven. AC-2.3 would catch a failure, so Medium. (Fowler)

**M-7. Scope mismatch between SA-2 and AC-C1.** SA-2 covers "command, skill or agent" files (`:147`) and allows an Orca mention only inside the contract file; AC-C1 greps `src/superclaude/core` too (`:172`), and P0 adds an Orca section to `HOW-WE-WORK.md` (`:150,158`) and a brief template to `WORKER-CONTRACT.md`, both in `core/`. If either names `orca-ide orchestration ...` (the 7.2 steps do), AC-C1 fails on the spec's own deliverable. The pattern also misses `orca open`, `orca status`, `orca-ide skills`. Also, in a rendered table `\|` shows as `|`, but copied from raw source the escaped pipes make the alternation literal. (Nygard)

**M-8. Worker-session rules have no vehicle for P0.** WC-3, WC-5, WC-7, WC-10, WC-12 are owned by "worker session" (`:61,63,65,68,70`), but the worker reads `WORKER-CONTRACT.md` only through a command's `## Unattended mode` section (`:52`), which does not exist for any command in P0; section 2.3 does not list these rules as brief content (`:73`). The P0 smoke runs therefore rely on the Orca preamble alone. (Newman)

**M-9. Undefined labels M1 to M6.** The candidate cites `M1`, `M2`, `M3`, `M4`, `M5`, `M6` (`:62,76,105,195,194,201`) with no definition in the spec or in the workspace files listed in the README; they appear to come from the not-yet-visible disposition (`README.md:27`). A reader cannot resolve them.

**M-10. Heartbeat gap for blocked-but-waiting.** WC-10 requires a 5-minute heartbeat (`:68`) while WC-3 sends none during `ask` (`:61`); `CAPS:64` supports this, but `ask` has no bounded timeout in the spec (`CAPS:68` UNVERIFIED, `:281`), so a long `ask` has no liveness bound beyond what Orca does. Acceptable because it is stated UNVERIFIED; recorded for the Reviser's awareness only.

### Minor notes

- 1.4(2) reframes the README's 60-second claim (`README.md:13`) as narrower; the reframing rests on `EVIDENCE.md:39,45`, which are UNVERIFIED here. If wrong, WC-1 and 1.4(2) are the places to change.
- `sk/sc-pr-submit-protocol/SKILL.md:37-39` (candidate `:11,65`) versus `:47-49` in the installed skill copy (`CAPS:161`): different files, so not a conflict, but unchecked here (UNVERIFIED).
- AC-1.3 and 7.2 mention a "scratch worktree"; the repo rule is that worktrees are created through Orca with an agent (CLAUDE.md, not in workspace; UNVERIFIED), worth wording as "a checkout the coordinator created".
- `/sc:git` is called mutating in "most operations" (`:133`) while `INV-A:91` says "every operation"; harmless.
- The 3.2 header counts `load` among 27 "needs a change" yet its row changes only a usage line (`:112`); the numbers still conserve (below).

=== ARCHITECTURE ANALYSIS ===

No additional blocking architecture finding beyond B-1 and B-2. The central decision (Orca on top, commands as units of work) is consistent with the evidence in the inventories: nested depth 1 (`CAPS:97-101`), `worker_done` bound to the dispatched pane (`CAPS:76,150`), Orca keeps Task records only for coordinator-started workers (`CAPS:158`), and no command calls Orca today (E5, UNVERIFIED grep; matches the README's premise, `README.md:6`). Fowler: the boundary is clean (contract file, report file, unattended mode); Newman: the contract version is not stated (the `return-contract.yaml` schema has no `version` field in WC-4, `:62`), which makes later field additions unversioned (Medium-level, folded into follow-up below). Nygard: failure modes covered in WC-2(c), WC-5 and WC-6 are good; gaps are M-3 and M-4.

### Guard Condition Boundary Table (guards in the spec)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-2 gate resolution | `:60` | Zero/Empty | gate with no default and no flag | blocked | contract `status: blocked` plus question | OK |
| WC-2 gate resolution | `:60` | Legitimate Edge Case | flag supplied but empty value | unspecified | not stated | GAP (Medium; M-5 family) |
| WC-4 `--report-dir` | `:62` | Zero/Empty | flag missing under `--unattended` | unspecified | not stated | GAP (M-5) |
| WC-4 `--report-dir` | `:62,64` | Typical (reuse) | same dir on `--retry-of` | unspecified | stale contract possible | GAP (M-3) |
| WC-5 outcome | `:63` | Zero/Empty | no report exists | failed | `--outcome failed` | OK |
| WC-5 outcome | `:63` | Sentinel Value Match | `status: partial` | true | `--outcome succeeded`, body states partial | OK |
| WC-5 outcome | `:63` | Legitimate Edge Case | audit verdict FAIL | true | `succeeded` | OK |
| WC-10 wait split | `:68` | Maximum/Overflow | single call over 5 min | split into at most 4 min | stated | OK |
| WC-10 wait split | `:68` | Legitimate Edge Case | pr-submit iteration over 4 min | UNVERIFIED | confirm per iteration (`:114`, UNVERIFIED #12) | GAP (stated as open) |
| Readiness limit | `:59` | Maximum/Overflow | prompt fallback above about 45 s | fails | stated (`EVIDENCE.md:56`, UNVERIFIED) | OK |
| Circuit breaker (Orca) | `CAPS:80,116` | Typical | three failed `worker-start` attempts | trips | worker `failed` reports do not count | OK |
| Nesting depth | `:33` | Maximum/Overflow | worker calls `worker-start` | refused | stated (R1) | OK |
| Confidence gate (task) | `:121` | Sentinel Value Match | confidence exactly 0.70 | UNVERIFIED | row says "below 0.70" blocks; at 0.70 not stated | OK (inherits the command's own rule) |

Left out classes: "One/Minimal" for the thresholds (no distinct behaviour from Typical); Maximum for WC-2 (not a numeric guard).
FR-8/FR-9 grading: the GAP rows name no concrete wrong outcome beyond M-3 and M-5 (already Medium), so none is blocking.

### Count-flow check (the spec's multi-stage flow)

[43 commands: 21 (`INV-A:3`) + 22 (`INV-B:3`)] --> [10 ready + 27 needs-change + 6 coordinator-only = 43] --> [phases: P1 9, P2 11 from section 3.2 plus 4 ready commands that gain gates (reflect, release-split, tdd, troubleshoot) = 15, P3 4, P4 3; 9 + 11 + 4 + 3 = 27 needs-change, conserved]. The 3.1 ready commands that get no `--unattended` phase (brainstorm, init-lite) are the M-1 divergence point. Per-inventory splits (A: 5 ready, 13 needs-change, 3 coordinator-only; B: 5, 14, 3) sum to 10, 27, 6 (`commands-a.md:62-66,86-94`, `commands-b.md:289`, `:285-287`). No count mismatch, so no CRITICAL pipeline finding.

## Follow-up candidates (Medium and minor; never trigger a revision)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10; the minor notes above; WC-4 `return-contract.yaml` carries no schema `version` field. The session that ran this audit has no interactive channel to the user in this sandbox, so the question "open an issue for these?" is not asked and no issue was created; this list is recorded only.

## Cap and loop state

Review 1 of 3. Fix cycles used: 0 of 2. Blocking findings open: B-1, B-2.

## Reviser brief

Blocking finding ids: B-1, B-2.

Rules (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. No brief clause overrode a rule of the command in this run.

verdict: FAIL
