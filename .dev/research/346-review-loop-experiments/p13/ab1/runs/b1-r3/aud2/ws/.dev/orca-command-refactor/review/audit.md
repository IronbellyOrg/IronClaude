review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

| Header field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `9cef9de023524eef0ec002f54d934b470019f03f17a77205bff3ed6600c2b9c7` |
| Baseline | not given (neither `--re-review` nor `--baseline`); this is a first review of the full document |
| Reviewer model actually used | claude-sonnet-5-5 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` |
| Brief clauses overridden | none |
| Label | whole-document audit of the final spec |

Citation keys: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. Anything outside those five files (`src/...`, `EVIDENCE.md`, `CLAUDE.md`, Orca guides, `install_core.py`, grep outputs the spec quotes) cannot be opened in this sandbox and is UNVERIFIED here, as the brief requires. Panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active).

## What was covered
- All 293 lines of the candidate, read in full, plus README and all three inventories in full.
- Every `INV-*`/`CAPS:*` citation in sections 1-4 was spot-checked against the inventory lines and matched. All 43 command rows in section 3 were matched to the A/B inventory verdicts. The 10/27/6 split reconciles with A (5/13/3) and B (5/14/3) (`INV-A:73`, `INV-B:278`, `spec:76`). Phase placement is consistent: every section-3 row maps to exactly one phase in `spec:159-162`, and 35 + 2 + 6 = 43 once the two no-fix ready commands (brainstorm, init-lite) are added.
- Not covered or not checkable: every `src/...`, `CLAUDE.md`, `EVIDENCE.md`, `install_core.py`, and `grep` citation, and the spec's own claims of an independent citation check (`spec:11`, `spec:293`). These are UNVERIFIED here.
- Deviation to disclose: to confirm the AC-C5 regex defect (B1) I ran a throwaway `git init` demo in a temp directory under `/tmp`, outside the stated sandbox directory, and deleted it. It read nothing from, and wrote nothing to, the repo, the workspace or git history.

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**B1. AC-C5 and AC-0.3 cannot detect a deleted bullet line, so the "additive edits" rule is not checkable** (CRITICAL as an acceptance defect; priority High; quality impact: Testability -3)
- Expert: Crispin/Wiegers (testability), Whittaker (zero/empty attack on the check).
- Stated text: SA-4 requires command-file edits to be additive (`spec:149`). AC-C5 checks it with `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-[^-]'` and passes on empty output (`spec:176`). AC-0.3 does the same for `HOW-WE-WORK.md` (`spec:201`).
- An implementer who follows the stated text as written deletes a markdown bullet (`- text`) from a command file, runs AC-C5, sees empty output and records a pass, and that result is wrong because a deleted `- text` line appears in the diff as `-- text`, whose second character is `-`, which `[^-]` rejects. Reproduced: a file with `- keep` and `- drop me`, after removing `- drop me`, gave `-- drop me` in the diff and no output from the AC-C5 regex (exit 1). Command and routing files are largely bullet lists (the lines the inventory cites, for example `INV-B:31-65`, are bullet-heavy), so the most common deletion is the one the check misses. The same applies to a deleted YAML `---` line (diff line `----`).
- Recommendation: replace the pattern with one that excludes only the file header, for example `grep -E '^-' | grep -vE '^--- '`, and apply the same fix at `spec:201`. Priority High.

**B2. AC-2.3 cannot pass for `/sc:cli-portify`: its three approval gates always resolve as blocked and no input can pass them** (MAJOR, blocking; priority High; quality impact: Consistency -2)
- Expert: Adzic (example/scenario), Wiegers.
- Stated text: the cli-portify row says "each of the three approval gates resolves as blocked with the artifact to review named in the contract" and adds only a `--resume <contract>` flag (`spec:105`). WC-2 allows a gate to resolve by default, by a caller-supplied flag, or as blocked (`spec:60`). The row picks "blocked" for all three and names no flag that supplies approval. AC-2.3 requires, for every P2 command, "a happy-path run with every required flag in the brief" that ends `--outcome succeeded` (`spec:209`). cli-portify is a P2 command (`spec:105`, `spec:160`).
- An implementer who follows the stated text as written builds a cli-portify that stops `blocked` at the Phase 2 review (`INV-A:45`, S:152) and, after `--resume`, stops `blocked` again at the final-spec approval (`INV-A:45`, S:393), so every run ends `failed` under WC-5 (`spec:63`). That is wrong because AC-2.3 can never see `succeeded` for this command, and the coordinator has no way to carry a person's approval into the worker.
- Recommendation: either give each gate an approval input (WC-2 (b)) or a documented default (WC-2 (a)), or exempt cli-portify from AC-2.3 and say that its success outcome is "spec delivered, approval pending". Priority High.

**B3. WC-5's outcome rule contradicts section 3.1's "ready today" commands whose report is not a status file** (MAJOR, blocking; priority High; quality impact: Consistency -2)
- Expert: Wiegers/Fowler.
- Stated text: WC-5 allows `--outcome succeeded` "only when the report parses and its `status` is `succeeded` or `partial`" and sends "a missing, empty, unparseable or unknown-status report" to `failed` (`spec:63`). Section 3.1 lists ten commands that "run as workers now", and `init-lite` writes only a markdown audit (`.dev/superclaude/context-audit.md`), with fix "None" (`spec:87`; `INV-A:55`). Commands with fix "None" "get neither" the flag nor the section (`spec:76`), and WC-4 writes the contract only "in unattended mode" (`spec:62`). So init-lite never gets a status file, and the same holds for md-only ready commands in the interval before their phase (index-repo `PROJECT_INDEX.md`, cleanup-audit `pass<N>-summary.md`, tdd, troubleshoot `REPORT.md`, release-split) (`spec:82-92`).
- An implementer who follows the stated text as written builds a worker that sends `--outcome failed` after a clean init-lite run, and that is wrong because the command succeeded and the coordinator would mark the Task failed and retry. The text 3.1 gives for the interim, "the worker reports the named file until Phase 1 adds the contract" (`spec:79`), says what path to report, not which outcome to send, and Phase 1 never adds a contract for init-lite. AC-0.4 carves out the YAML check for P0 only (`spec:202`).
- Recommendation: add one WC-5 clause for commands with no status contract (outcome `succeeded` iff the named report file exists and is non-empty and the command ended without an error stop), or give init-lite and the ready commands without a contract the `--unattended` section and contract in P1. Priority High.

## === ARCHITECTURE ANALYSIS ===

The architecture decision (Orca on top, commands as units) is sound and the rejected alternative is well argued: R1-R5 are tied to inventory lines (`spec:33-37`, `CAPS:97-103`, `CAPS:145-150`), the evidence gaps are stated honestly (`spec:41-45`), and Phase 0 tests the decision before building on it (`spec:158`). Two architectural points are Medium and listed below (M4, M6). No architecture finding is blocking.

### Quantity Flow (Pipeline Dimensional Analysis)
Triggered by the inventory-to-phase pipeline, which has a count-changing stage.

```text
[Inventory A: 21 + B: 22 = 43] --> [verdict split] --> [10 ready] [27 change] [6 coordinator-only]   (10+27+6 = 43, OK)
[27 change] --> P1: 9 (analyze, build, business-panel, design, document, explain, index, test, load)
            --> P2: 11 (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research,
                        review-translation, spec-panel, task, tasklist)
            --> P3: 4 (roadmap, save, validate-roadmap, validate-tests)
            --> P4: 3 (implement, post-release, pr-submit)                     (9+11+4+3 = 27, OK)
[10 ready] --> P1 fixes: 4 (adversarial, cleanup-audit, index-repo, workflow)
           --> P2 fixes: 4 (reflect, release-split, tdd, troubleshoot)
           --> no fix: 2 (brainstorm, init-lite)                                (4+4+2 = 10, OK)
```
No count mismatch found. The 2 no-fix ready commands are the source of B3.

## Guard Condition Boundary Table (Nygard builds, Crispin validates completeness, Whittaker attacks)

One row per applicable input class; classes left out are named with a reason below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome map | spec:63 | Zero/Empty | empty or missing report | failed | `--outcome failed` | OK |
| WC-5 outcome map | spec:63 | Typical | report `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome map | spec:63 | Sentinel Value Match | existing contract uses another status word | not in the four | counts as `failed` (spec:62), vocab of brainstorm, adversarial, reflect not checked | GAP (M7) |
| WC-5 outcome map | spec:63 | Legitimate Edge Case | md-only report, no `status` (init-lite) | unparseable | `failed` under WC-5; 3.1 says ready | GAP (B3) |
| WC-4 contract path | spec:62 | Zero/Empty | no output flag passed | n/a | brief must pass one (spec:73); troubleshoot/reflect/workflow rows list no output flag (spec:88,91,92) | GAP (M6) |
| WC-4 contract path | spec:62 | Typical | `--output <dir>` | dir | `<dir>/return-contract.yaml` | OK |
| WC-4 contract path | spec:62 | Legitimate Edge Case | `--output <file>` | file | `<file>.return-contract.yaml` | OK |
| WC-2 gate resolution | spec:60 | Typical | gate with a default | (a) | documented default | OK |
| WC-2 gate resolution | spec:60 | Legitimate Edge Case | gate with no input able to pass it (cli-portify) | (c) always | blocked every run; AC-2.3 happy path unreachable | GAP (B2) |
| WC-9 outward default | spec:67 | Typical | command has an explicit flag (auggie-review `--post-pr`) | off unless flag | OK | OK |
| WC-9 outward default | spec:67 | Legitimate Edge Case | action has no flag (task `commit`/`push`) | stays off | D4 lists it as authorizable (spec:252) | GAP (M2) |
| WC-6 resume or fresh dir | spec:64 | Typical | command has resume flag | resume | OK | OK |
| WC-6 resume or fresh dir | spec:64 | Legitimate Edge Case | retry of a command whose report path was brief-fixed | fresh dir | path changes; reported in `--report-path` | OK |
| WC-10 wait size | spec:68 | Maximum/Overflow | single call between 4 and 5 min | "longer than 5" not met, "at most 4" exceeded | thresholds differ (5 at spec:68, 4 at spec:114, 240 s at spec:218) | GAP (minor, N1) |
| WC-10 wait size | spec:68 | Zero/Empty | no wait | n/a | no action | OK |
| AC-C5 / AC-0.3 regex | spec:176,201 | Legitimate Edge Case | deleted `- bullet` | `-- text` | not matched, check passes | GAP (B1) |
| AC-C5 / AC-0.3 regex | spec:176,201 | Typical | edited table row | `-\|...` | matched, check fails | OK |
| 7.2 step 2 agentWait | spec:189 | Zero/Empty | field absent (Orca never looked, CAPS:129) | "never non-null" true | counts as pass | GAP (minor, N2) |
| 7.2 step 2 agentWait | spec:189 | Typical | null | pass | OK | OK |

Classes left out: One/Minimal for WC-4 and WC-5 (a one-element report is the Typical row); Maximum/Overflow for WC-5, WC-4, WC-2 and WC-9 (no capacity is involved); Sentinel Value Match for WC-4 (the contract path carries no control value other than the adversarial exception, which spec:62 already names); Zero/Empty for WC-9 (an empty brief equals "no authorization", the default off row).

## Whittaker adversarial analysis

- I can break this specification by **Sequence Attack**. The invariant at **spec:154** ("later phases do not start until the earlier phase's checks pass") fails when **P0 writes `WORKER-CONTRACT.md` only if AC-0.4 passes (spec:158) while AC-0.1 to AC-0.3 (spec:199-201) are P0 checks that need that file**. Concrete attack: AC-0.4 fails, so the file is not written (state: file absent), AC-0.1 then fails by construction (`'WORKER-CONTRACT.md' in KNOWN_CORE_FILES` false), and the phase can never pass, even though "a failure here reopens section 1" (spec:202) is the intended outcome. Severity MINOR: the inferable reading is "phase fails, reopen section 1".
- I can break this specification by **Divergence Attack**. The invariant at **spec:100** (`--unattended` implies `--no-post-pr`; posting only with explicit `--post-pr`) fails when **both `--no-post-pr` and `--post-pr` appear in a brief**. Concrete attack: brief has `--unattended --no-post-pr --post-pr`; before: no comments on the PR; after: undefined, the spec gives no precedence. MINOR (a coordinator controls the brief; N3).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **spec:62** (four status words) fails when **a command's own contract already uses a status value that is neither of the four** (unchecked for brainstorm, adversarial, reflect; `INV-B:272` shows only that workflow has `failed`). Concrete attack: reflect writes `status: complete`; WC-4 says it "counts as `failed`"; the coordinator marks a good review failed. Graded Medium (M7): needs a guess that a command's vocabulary differs.
- Accumulation Attack on WC-5 `blocked` to `failed` against the circuit breaker: three blocked runs for one Task. `CAPS:80` says a worker's own `failed` report does not count toward the breaker, so this holds. No finding.
- Zero/Empty Attack on section 2.3: a brief that omits the output directory for a fixed-path command. WC-11 covers it (`spec:69`, `spec:73`). No finding.

## Findings that are not blocking (follow-up candidates)

Medium (warnings; each needs a guess or concerns a requirement the document does not state):

- **M1. Section 6 says "Phases 1-3 need no user decision" (`spec:154`), but D4 (`spec:252-255`) governs the P2 rows for auggie-review `--post-pr` (`spec:100`) and task `commit`/`push` (`spec:121`).** If the user picks D4(b) "never", the P2 text that re-enables posting with `--post-pr` is wrong. Needs a guess about the user's answer. Recommend moving those two outward re-enables to P4 or stating that P2 only turns the actions off. Priority Medium.
- **M2. D4 lists task `commit`/`push` as authorizable (`spec:252`), but WC-9 says an action without an explicit flag "stays off" (`spec:67`), and task's EXEMPT `commit`/`push` run from keywords with no flag (`INV-B:204`).** Under WC-9 the authorization can never be used. Conservative failure only. Priority Low-Medium.
- **M3. Gate conversions live in skill files, but SA-4, AC-C5 and AC-2.1 speak only of command files (`spec:149`, `spec:176`, `spec:207`).** Many gates are skill text (review-translation `SKILL.md:44,76`, tdd `SKILL.md:52-61`, roadmap `SKILL.md:433-438`, reflect `refs/remediation-handoff.md:228`, per `spec:88-118`). The spec does not say whether an override section in the command beats a skill's own "STOP AND WAIT" or whether the skill is edited, nor whether that edit is additive. Priority Medium.
- **M4. tasklist row: `--unattended` passes `--unattended` to each reflect while Stage 10.5 still passes `--remediate` (`spec:122`; `INV-B:46,209`).** Per `INV-B:109`, the headless rule then auto-accepts auto-fixable registers and runs the remediation handoff, a behavior the inventory did not recommend (`INV-B:215` says drop `--remediate`). The row's claim that the fan-out sits "inside Claude Code's nesting limit" (`INV-A:14`) counts one layer and does not count reflect, remediation and workflow layers beneath each reflect subagent. Priority Medium.
- **M5. 7.2 step 5 passes only if the transcript never contains the string `AskUserQuestion` (`spec:192`).** Skill and command text loaded into the transcript can contain that word (`INV-A:44`, `INV-B:47` cite skills that mention it), so the literal search can fail a correct run. Reading it as "no such tool call" is available but not stated. Priority Medium.
- **M6. Section 2.3 requires the report path to be known before dispatch (`spec:73`, `spec:62`), but the exception clause names only generated paths "section 3 names" and the 3.1 rows for troubleshoot, reflect and workflow list no output flag and give timestamped or id-based defaults (`spec:88`, `spec:91`, `spec:92`; `INV-B:112`, `INV-B:242`, `INV-B:272`).** Only research is named as generated (`spec:116`). Priority Medium.
- **M7. WC-4's fixed four-value status rule is asserted without checking the vocabulary of the commands that already write a contract** (brainstorm, adversarial, reflect, workflow) (`spec:62`, `spec:269-270`). Priority Medium.
- **M8. SA-3 allows the new contract "when the caller passes the new output flag" (`spec:148`), while WC-4 writes it "in unattended mode" (`spec:62`).** A person passing the new `--output` to analyze may or may not get a contract. Priority Low-Medium.
- **M9. WC-11 names only `save` as a single-owner-file writer (`spec:69`, AC-3.4 `spec:215`).** The inventories show other shared-path writers: roadmap saves at every wave through `sc:save` (`INV-B:154`), validate-roadmap writes fail-open memory under `.superclaude/memory/validate-roadmap/` (`INV-B:253`). Priority Low-Medium.
- **M10. The section 3 spec-panel row says add `--output` (`spec:120`, `INV-B:43,182`), but the `/sc:spec-panel` definition supplied to this audit already lists `[--output <file>]` and `--report-dir` (`command.md:23-24,460`).** That file is not the spec's evidence base and may be a later version; flagging the drift only. Priority Low (UNVERIFIED which is current).

Minor notes (never fail a review):

- N1. WC-10 uses three different thresholds: "longer than 5 minutes" / "at most 4" (`spec:68`), "under 4 minutes" (`spec:114`), "exceeds 240 s" (`spec:218`).
- N2. 7.2 step 2 passes when `agentWait` is absent, though `CAPS:129` says absent means Orca never looked.
- N3. No precedence rule when a brief contains both `--no-post-pr` and `--post-pr`.
- N4. SA-2 permits Orca text only "for a coordinator" (`spec:147`), but WC-3, WC-5 and WC-12 make `WORKER-CONTRACT.md` instruct the worker session to run Orca commands (`spec:61`, `spec:63`, `spec:70`).
- N5. Section 9 says Phases 0-3 "can proceed on the recommendations" (`spec:233`) while section 6 says Phases 1-3 "need no user decision" (`spec:154`); D1 is a decision both rely on.
- N6. AC-2.4's `gh api ... --jq length` counts only the first page of reviews/comments (`spec:210`).
- N7. `INV-A:13` records earlier Orca workers running `/sc:adversarial` with `invocation_method: "skill-direct"`, which the spec cites as re-read (`spec:11`) but does not reconcile with its claim that the PR #329 run proves only the nested route (`spec:43`). The spec's reading matches `CAPS:156`; reconciling the two would remove a reader's doubt.
- N8. UNVERIFIED from this sandbox (not defects): the quoted `grep` runs (`spec:25`), `install_core.py:13-24` and `:4,33` (`spec:52`), `CLAUDE.md` line cites, `src/superclaude/core/CLAUDE.md:65` and `HOW-WE-WORK.md:22` (`spec:164`), `EVIDENCE.md:39,45,56`, and the spec's two claimed independent citation checks (`spec:11`, `spec:293`).

## Consensus and disagreements
- Consensus: the decision, the six-command coordinator-only list, the phase order (no-gate first, safety rules last) and the honest evidence-gap section are well supported by `INV-A`, `INV-B` and `CAPS`.
- Wiegers vs Fowler: Wiegers wants the WC-5 mapping tightened (B3); Fowler would rather keep WC-5 simple and give the no-contract commands a contract in P1. Both fixes satisfy B3.
- Crispin: the acceptance regexes are the weakest part of section 7 (B1, M5); the rest of section 7 is concrete and runnable.

## follow-up candidates
M1, M2, M3, M4, M5, M6, M7, M8, M9, M10 (Medium) and N1 to N8 (minor), as above. No issue was opened and the user was not asked: this audit ran as a sandbox worker whose final reply is limited to the output path, so the once-per-loop question to the user is left to the coordinator.

## Reviser brief
Blocking finding ids: **B1, B2, B3**. Rules for the reviser (restated from the command, bullet 6; the reviser reads this report, not the command):
- Revise only the text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium findings M1 to M10 and minor notes N1 to N8 alone; do not apply them, including by "apply all findings".
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
