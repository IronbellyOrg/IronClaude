review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec

| Item | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review) |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `f8f6302199d147a422c4ace828ab0a5bd64e8d93cc92412e2478d4460e7d27ae` (59613 bytes) |
| Baseline | none given (neither `--re-review` nor `--baseline`), so this is a first review of the full document; no `baseline: missing` note applies |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full), under the command's Review Loop (`command.md:256-264`) |
| Panel (review order) | Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker (always active), Newman, Hohpe (architecture); Crispin only to validate the Guard Condition Boundary Table |
| Brief clauses overridden | none. The brief narrows nothing past the command and grades nothing itself. |
| Improve step (step 6) | not run. The brief says "do not edit anything else", and the command's Boundaries forbid modifying a specification without consent. Recommendations are in the findings only. |
| `--unattended` | not passed; no `return-contract.yaml` is written. |

Citation shorthand: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `PROMPTS:N` = `~/.claude/rules/prompts/document_review_loop_prompts.md`; `CMD:N` = `command.md`.

## Coverage

- **Read in full:** the candidate (285 lines), `README.md`, all three inventories, `command.md`, the review-loop prompts file.
- **Checked:** every `INV-A:N`, `INV-B:N`, `CAPS:N` and README citation the candidate makes was compared with the inventory line it names. I found no wrong line. I also checked the counts: 21 + 22 = 43 commands; 10 ready (`SPEC:83-92`), 27 needing change (`SPEC:99-125`), 6 coordinator-only (`SPEC:132-137`); 10 + 27 = 37; the phase counts in `SPEC:159-162` are 9 (P1) + 11 + 4 + 3 = 27 for the 27-row table, and all agree with the Phase column.
- **UNVERIFIED (cannot be checked in this sandbox):** every citation of `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/codegraph-migration/`, `.dev/evals/` and Orca's own files. Only the workspace's three inventories and README exist here. Where the candidate repeats such a line through an inventory, I checked only that the copy is faithful. Finding ids `F-01`, `F-02`, `F-03`, `N-01`, `N-02` in the candidate (`SPEC:62,64,73,79,147,158,194,195`) point at an earlier review and disposition (`README:25-26` lists `review/spec-panel.md`, `review/disposition.md`) that are not in the sandbox: UNVERIFIED.
- **Pipeline Dimensional Analysis (FR-17):** not triggered. The candidate is a rollout plan, not a data pipeline. The one count flow (43 commands, minus 6 coordinator-only, gives 37, spread over P1 to P4 as 9 + 11 + 4 + 3 with the 10 ready rows folded in) conserves counts, as checked above. No Quantity Flow Diagram is produced.
- **State Variable Registry:** not required, because `--focus correctness` is not active.
- **Not run:** nothing in the candidate was executed; every acceptance check is read, not run.

## Summary

The decision (Orca coordinates, commands stay units of work) is well argued, and the evidence is carefully hedged (`SPEC:41-45`). The defects are in the rollout and report-path mechanics: two stated texts contradict each other in each of the two blocking findings below. Nothing in the architecture decision is wrong.

Quality estimate (0-10, advisory): Clarity 7, Completeness 6, Testability 6, Consistency 5.

## === REQUIREMENTS ANALYSIS ===

### B-1 The contract path rule contradicts the rows it governs, so some acceptance checks cannot pass

- **Severity:** MAJOR (blocking)
- **Expert:** Wiegers (lead), Adzic
- **Priority:** High
- **Quality impact:** Testability +2, Consistency +2
- **Grading sentence:** An implementer who follows the stated text as written builds a contract file at `<output-dir>/return-contract.yaml` for every command (`SPEC:62`, `SPEC:76`), but for four ready rows the same document gives a different location or no directory at all, so the coordinator opens a path where no file exists, and acceptance checks that name the contract cannot pass.
- **Evidence (stated texts that contradict):**
  - `SPEC:76` defines "Contract" as the WC-4 file `<output-dir>/return-contract.yaml`, and `SPEC:62` says `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)", known before dispatch.
  - adversarial: `SPEC:83` fixes the contract at `<output>/adversarial/return-contract.yaml`. That is not `<output-dir>/return-contract.yaml`. AC-1.4 (`SPEC:198`) greps for "one fixed path" but 7.2 step 3 (`SPEC:182`) compares against "the WC-4 contract path".
  - workflow: `SPEC:92` puts the contract at `.dev/tasks/to-do/<id>/return-contract.yaml`, a package directory the command creates itself. The brief passes only `--handoff none` and no output directory. The same row asks the command to write the contract "for pre-creation STOPs too", but at a pre-creation STOP that package directory does not exist, and the row names no other place. AC-1.2 (`SPEC:196`) runs every P1 command, workflow included, with `--unattended --output <dir>` and then requires the WC-4 path.
  - tdd and init-lite: `SPEC:87` and `SPEC:90` give `--output <file>`, a file. WC-4 derives the contract from a directory. AC-2.2 (`SPEC:200`) runs `/sc:tdd "auth" --unattended --output <file>` and 7.2 step 4 (`SPEC:183`) then does `test -s <contract>`. No stated rule says where that file is.
  - `SPEC:64` (WC-6) also says "the command never chooses its own output directory", while cleanup-audit (`SPEC:85`, fixed directory), index-repo (`SPEC:86`) and workflow (`SPEC:92`) choose theirs.
- **Recommendation:** narrow, do not add. Make WC-4 say that the contract path is the one named for that command in section 3, and make each of the four rows above name it (and, for workflow, name where a pre-creation STOP writes it). Delete the "directory the coordinator passed" generalisation in `SPEC:62` and `SPEC:76` rather than adding a new mechanism. Rationale: one definition then holds for every row and every acceptance check.

### B-2 `--unattended` is made available to every command in P1, while the gate and outward-action rules it promises land in P2 to P4

- **Severity:** MAJOR (blocking; names a safety-boundary risk)
- **Expert:** Wiegers, Nygard
- **Priority:** High
- **Quality impact:** Consistency +2, safety of rollout
- **Grading sentence:** An implementer who follows the stated text as written ships P1 with `--unattended` accepted on all 37 commands (`SPEC:159`), each carrying an `## Unattended mode` section that names `return-contract.yaml` (`SPEC:195`), and the brief rule says to pass `--unattended` "from P1 on" (`SPEC:73`); but the rule that makes `--unattended` safe (WC-2: no prompt, WC-9: no outward default) is only built in P2 to P4 (`SPEC:100,109,113,114,121,160-162`). In that window `/sc:auggie-review <PR> --unattended` is accepted, still posts to GitHub with no confirmation (`SPEC:100`, `INV-A:38`), and then waits on a person, which is exactly what WC-2 and WC-9 say cannot happen under that flag.
- **Evidence:**
  - P1 scope (`SPEC:159`): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". It says nothing about a command that does have a gate.
  - AC-1.1 (`SPEC:195`) requires, in P1, a section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` on every 3.1 and 3.2 command except load. For P2 to P4 commands the contract and gate resolutions do not exist yet, so the P1 section would document behaviour not built.
  - Same pattern for implement (halt waits for a Ruling until P4, `SPEC:109`), post-release (confirmations until P4, `SPEC:113`), task (commit/push, `SPEC:121`), cli-eval (`SPEC:104`) and the ready rows whose gate fix is P2 (`SPEC:88-91`).
  - `SPEC:154` says phases are gated by checks, but no check stops a coordinator from using a command between phases; `SPEC:73` tells the coordinator to do so.
- **Recommendation:** narrow. In `SPEC:159`, `SPEC:195` and `SPEC:73`, limit P1 flag acceptance, the section and the "pass `--unattended`" instruction to the commands whose section-3 Phase column is P1 (and the P1 fixes of ready rows); each other command gains the flag and section in its own phase. If the flag must exist earlier, require a command whose gate conversion has not landed to refuse `--unattended` with a one-line message. Rationale: the flag then never claims a guarantee the command does not yet keep.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision itself (`SPEC:13-45`), the rejection of "commands call Orca" (`SPEC:28-39`), the coordinator-only set (`SPEC:127-139`) and the standalone guarantees (`SPEC:141-151`) are consistent with the inventories and with `CAPS:97-103`, `CAPS:145-150`. The architecture findings are the Medium items below (M-2, M-4, M-6, M-7, M-8, M-9), all under follow-up candidates.

### Whittaker adversarial analysis

Format: "I can break this specification by [attack]. The invariant at [location] fails when [condition]. Concrete attack: [scenario]."

- **A-1 (Sequence Attack).** I can break this specification by running a retry after a crash. The invariant at `SPEC:62` ("the coordinator reads the contract of the attempt it last dispatched") fails when the retry worker dies before it writes a contract and the directory still holds the first attempt's file. Concrete attack: attempt 1 writes `status: blocked`, the coordinator answers and retries on the same resume directory (`SPEC:64`); the retry crashes at minute 2; before: `return-contract.yaml` = blocked (attempt 1); after: unchanged, so a coordinator that opens "the" contract reads a stale blocked file. Nothing requires the command to overwrite or mark the contract at start. Severity: MAJOR but graded Medium (needs a crash plus a guess that the coordinator trusts the file). Listed as M-2.
- **A-2 (Zero/Empty Attack).** I can break this specification by passing `--unattended` with no output directory (or an unwritable one). The invariant at `SPEC:62` ("written on every outcome, including stops before any other output exists") fails when there is nowhere to write. Concrete attack: `/sc:tdd "x" --unattended`; before: no contract; after: the spec defines no behaviour, so one implementation writes to the current directory, another refuses silently. Graded Medium (a missing requirement, not a stated text that does harm). Listed as M-1.
- **A-3 (Sentinel Collision Attack).** I can break this specification by putting the flag in content. The invariant at `SPEC:51` ("when its caller passes `--unattended`") fails when the specification content or topic is itself the string `--unattended`. Concrete attack: `/sc:spec-panel "review the --unattended flag text" --focus requirements`; before: attended run; after: depending on the parser, a person's attended run loses its prompts, which breaks SA-1 (`SPEC:146`). The spec defines no token rule. Medium. Listed under GAP row GCB-3.
- **A-4 (Divergence Attack).** I can break this specification at the boundary between WC-2(c) and WC-3. The invariant at `SPEC:60-61` fails when a gate resolves as blocked and the worker "may instead ask": AC-2.2 (`SPEC:200`) requires `--outcome failed` and `status: blocked`, but a worker that uses `ask` (allowed by `SPEC:61`) never reaches that outcome on the same input. Concrete attack: tdd bare topic; worker A stops (blocked, failed); worker B asks, gets an answer, finishes succeeded; both obey the spec, yet AC-2.2 holds only for A. Medium: the AC could pin the flag-only path in its text. Listed under M-3.
- **A-5 (Accumulation Attack).** I can break this specification by running the AC-2.4 count check on a busy PR. The invariant at `SPEC:202` ("both counts unchanged") fails when the endpoint is paginated: `gh api .../reviews --jq length` returns at most one page (default 30), so a PR with 30 or more reviews or comments reports 30 before and after even if posting occurred. Medium. Listed as M-5.
- **A-6 (Sequence Attack).** I can break this specification by re-invoking after `ask`. The invariant at `SPEC:64` ("a re-run starts clean ... a new directory for each retry") fails for the in-session path of `SPEC:61`: the worker re-invokes the same command itself, with no new directory from the coordinator. Concrete attack: troubleshoot (fresh-dir row, `SPEC:91`) blocks at the `--depth deep` short-input STOP, the worker asks, and re-invokes into the same output directory; attempt 1's contract and any `REPORT.md` stub are overwritten or mixed. Medium. Listed as M-3.

## Guard Condition Boundary Table

Trigger: the candidate contains thresholds and conditional rules (`SPEC:60,61,63,64,68`, and the numeric rules at `SPEC:59,121`). Responsibility: Nygard builds, Crispin checks completeness, Whittaker attacks. One row per applicable input class; an omitted class has its one-line reason under the guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GCB-1 wait split ("blocks one call longer than 5 minutes, split into waits of at most 4 minutes") | SPEC:68 (WC-10) | Zero/Empty | wait of 0 s | false | nothing to split; no requirement needed | OK |
| GCB-1 | SPEC:68 | One/Minimal | wait of 1 s | false | no split | OK |
| GCB-1 | SPEC:68 | Typical | 3 min | false | no split needed; heartbeat cadence 5 min holds | OK |
| GCB-1 | SPEC:68 | Maximum/Overflow | 3600 s eval (cli-eval, `SPEC:104`) | true | split into waits of at most 4 min, heartbeat between | OK |
| GCB-1 | SPEC:68 | Sentinel Value Match | `--watch` (never ends, `SPEC:123`) | n/a | refused under `--unattended` | OK |
| GCB-1 | SPEC:68 | Legitimate Edge Case | single call of 4.5 min (above 4, not above 5) | false by the trigger, true by "waits of at most 4 minutes" | not decided; the pr-submit row (`SPEC:114`) uses 4 min as the limit, WC-10 uses 5 min as the trigger | GAP |
| GCB-2 outcome mapping (`failed`/`blocked`/no report gives `failed`, else `succeeded`) | SPEC:63 (WC-5) | Zero/Empty | contract file present but 0 bytes or unparseable | unspecified | not stated ("no report exists" covers only a missing file; AC step 4 `test -s` is a check, not a rule) | GAP |
| GCB-2 | SPEC:63 | One/Minimal | contract with `status` only (no `command`) | unspecified | WC-4 says "at least" those fields; WC-5 silent; AC step 4 (`SPEC:183`) would fail it | GAP |
| GCB-2 | SPEC:63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| GCB-2 | SPEC:63 | Sentinel Value Match | `status` outside the four values (an existing command's own value) | unspecified | not stated; WC-4 says existing contracts "keep their fields" (`SPEC:62`) | GAP |
| GCB-2 | SPEC:63 | Legitimate Edge Case | `partial`, or audit verdict FAIL | true | `succeeded`, status and verdict named in first sentence | OK |
| GCB-3 unattended mode (`--unattended` present) | SPEC:51, SPEC:60 | Zero/Empty | flag absent | false | today's behaviour (SA-1, `SPEC:146`) | OK |
| GCB-3 | SPEC:51 | One/Minimal | flag present, command has no gate | true | no-op plus contract | OK |
| GCB-3 | SPEC:51 | Typical | flag present, gate hit | true | per row of section 3 | OK |
| GCB-3 | SPEC:51, 62 | Maximum/Overflow | flag present, no output directory or unwritable | true | not stated | GAP |
| GCB-3 | SPEC:51 | Sentinel Value Match | the string `--unattended` inside quoted specification or topic text | ambiguous | no token rule | GAP |
| GCB-3 | SPEC:159, 100, 109 | Legitimate Edge Case | flag present, command's gate conversion not yet shipped (P1 to P4 gap) | true | contradicts WC-2/WC-9 (see B-2) | GAP |
| GCB-4 confidence gate (task, below 0.70 resolves blocked) | SPEC:121 | Zero/Empty | 0.0 | true | blocked | OK |
| GCB-4 | SPEC:121 | One/Minimal | 0.69 | true | blocked | OK |
| GCB-4 | SPEC:121 | Typical | 0.85 | false | continues | OK |
| GCB-4 | SPEC:121 | Sentinel Value Match | exactly 0.70 | false ("below") | continues | OK |
| GCB-4 | SPEC:121 | Legitimate Edge Case | confidence not computable | unspecified | not stated | GAP |
| GCB-5 retry directory (row resumes: same directory plus resume flag; else new directory) | SPEC:64 | Zero/Empty | first dispatch, no retry | n/a | no directory rule needed | OK |
| GCB-5 | SPEC:64 | Typical | troubleshoot retry | fresh dir | coordinator passes new directory | OK |
| GCB-5 | SPEC:64 | Maximum/Overflow | more than three failed starts for one Task | circuit breaker (`CAPS:116`) | the spec states no coordinator action | GAP |
| GCB-5 | SPEC:64 | Sentinel Value Match | `save` listed as a resuming row though its row gives no resume flag (`SPEC:119`) | true | coordinator "passes the same directory with the resume flag" for a flag that does not exist | GAP |
| GCB-5 | SPEC:61, 64 | Legitimate Edge Case | in-session re-invoke after `ask` on a fresh-dir row | unspecified | no directory stated | GAP |
| GCB-6 readiness (WC-1, "well inside" the 60 s limit) | SPEC:59 | Typical | 30 s fallback | within | passes (`CAPS:49`) | OK |
| GCB-6 | SPEC:59 | Legitimate Edge Case | fallback of 45 s | "well inside"? | fails per `CAPS:49`; "well inside" is not quantified | GAP |

Omitted classes, one line each: GCB-1 and GCB-6 One/Minimal and Zero (a zero-length startup prompt is not a state that can occur); GCB-4 Maximum (confidence cannot exceed 1.0, which is the Typical-high case); GCB-5 One/Minimal (identical to Typical); GCB-6 Zero, One, Maximum, Sentinel (the guard is an operator-owned time limit, not an input).

FR-8/FR-9 grading: no GAP row names a concrete wrong outcome an implementer would produce from stated text except GCB-3 (P1 to P4 gap), which is B-2. The other GAP rows are Medium and are carried to the follow-up list. FR-10: the table is complete for the guards identified.

## Follow-up candidates (Medium and minor; none fails the review or enters the Reviser brief)

Medium (warnings):

- **M-1** No behaviour for `--unattended` with a missing, empty or unwritable output directory (A-2, GCB-3). `SPEC:62`, `SPEC:73`.
- **M-2** A stale contract from an earlier attempt can be read as the current one; nothing requires the command to replace or mark it at start (A-1). `SPEC:62,64`, `SPEC:182-183`.
- **M-3** The in-session `ask` then re-invoke path (`SPEC:61`) has no directory rule and conflicts with AC-2.2's single expected outcome (A-4, A-6, GCB-5). `SPEC:61,64,91,200`.
- **M-4** WC-6 lists `save`, `index-repo` and `brainstorm` as rows where the coordinator passes "the same directory with the resume flag" (`SPEC:64`), but the section-3 rows give `save` no flag (`SPEC:119`, "it writes resume state"), index-repo `mode=update` (`SPEC:86`), brainstorm a flag that only skips the dialogue (`SPEC:84`). Align the list with the rows.
- **M-5** AC-2.4 (`SPEC:202`) counts with an unpaginated `gh api ... --jq length` (A-5). Use `--paginate` or compare ids.
- **M-6** WC-9 allows an outward action only "through the command's own explicit flag written in the brief" (`SPEC:67`), but task `commit`/`push` (`SPEC:121`) and post-release's VM, install, commit and PR (`SPEC:113`) have no such flag in the rows. The authorization mechanism for these is undefined (see D4, `SPEC:244-247`).
- **M-7** Several requirements have no acceptance check: WC-1 (`SPEC:59`), WC-3 (`SPEC:61`), WC-10 for any command other than pr-submit, including cli-eval (`SPEC:68`, `SPEC:104`), WC-11 for any command other than save (`SPEC:69`), WC-12 (`SPEC:70`). There is no WC-to-AC trace table.
- **M-8** WC-4 says commands with an existing contract "keep their fields" (`SPEC:62`) while WC-5 and 7.2 step 4 assume a fixed four-value `status` (`SPEC:63,183`, Decisions `SPEC:262`). Whether existing contracts already use those four values is not shown in the inventories (UNVERIFIED; GCB-2).
- **M-9** WC-11 (`SPEC:69`) requires timestamped or slugged default paths, but index-repo (`PROJECT_INDEX.md`) and cleanup-audit (`.claude-audit/`) keep fixed paths (`SPEC:85-86`), and `/sc:roadmap` writes memory through `sc:save` at every wave (`INV-B:154`) with no row covering that under WC-11.
- **M-10** The Unattended-mode sections point at `~/.claude/WORKER-CONTRACT.md` for the shared rules (`SPEC:52`); no behaviour is stated for a run where that file is absent (older install, or a checkout that has not been installed).
- **M-11** tasklist (`SPEC:122`) and reflect (`SPEC:88`) choose the headless auto-accept path for `--remediate` under `--unattended`, but the spec never says what an auto-accepted remediation does (which files, which hand-off). The headless rule itself is in `src/`, UNVERIFIED here (`INV-B:109`).
- **M-12** GCB-1 and GCB-6 boundary rows: 4 min versus 5 min in WC-10, and "well inside" in WC-1.
- **M-13** The finding ids `F-01`, `F-02`, `F-03`, `N-01`, `N-02` are used as authority in the text (`SPEC:62,64,73,79,147,158,194,195`) but are not defined in the document; a reader needs `review/disposition.md` (UNVERIFIED, not in the sandbox).

Minor notes:

- `SPEC:44` says Phase 0 "starts with live smoke runs", but `SPEC:158` writes the contract file and tests first, then runs the smoke tests.
- `SPEC:23` lists the PR #329 run as "It has worked before" while `SPEC:43` says it proves only the nested route; align the wording.
- `SPEC:16` says command changes are "limited to the worker contract"; section 3 and SA-4 (`SPEC:149`) add several defect fixes.
- `SPEC:252` (D5) calls R1 a "protection against runaway fan-out"; R1 (`SPEC:33`) is a limit on the rejected design, not a protection.
- load: the row says "P1 (usage line only)" (`SPEC:112`, `SPEC:159`) while AC-1.1 (`SPEC:195`) requires a section on load. Lines 76 and 79 resolve it, but the row reads as a contradiction.
- 7.2 step 5 (`SPEC:184`) greps the transcript for the string `AskUserQuestion`; loaded skill text can contain that string. The pass condition is stated as "no call", which a grep cannot separate.
- AC-1.3 (`SPEC:197`) uses a "scratch worktree" and `claude -p`; the repo's worktree rule (`CLAUDE.md`, UNVERIFIED here) requires Orca for project worktrees, and a `--print` run is the headless mode some commands treat differently (`SPEC:151`).
- `SPEC:172` and similar checks use `\|` inside code spans; copied raw from the file, `grep -E` reads `\|` as a literal pipe and the check could print nothing for the wrong reason.
- Question about opening an issue for the follow-up list: not asked. This run is a worker whose reply is fixed to `DONE <path>`; the coordinator that owns the loop asks the user once.

## Consensus and disagreements

- Consensus: the "Orca on top" decision and the coordinator-only set are sound; the evidence statement (`SPEC:41-45`) is honest about what is unproven.
- Disagreement: Wiegers and Whittaker would grade M-2 and M-3 as blocking; the grading check does not allow it, because each needs an assumption (a crash, a coordinator that trusts a stale file). They stay Medium.
- Disagreement: Fowler would prefer a single thin wrapper at the coordinator over `--unattended` in 37 commands. That is a design preference, not a defect, and the spec rejects the wrapper-in-commands route with reasons (`SPEC:28-39`).

## Reviser brief

Blocking finding ids: B-1, B-2.

Restated rules (the reviser reads this report, not the command): revise only text a blocking finding names. Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

- B-1: `SPEC:62`, `SPEC:76`, `SPEC:83`, `SPEC:87`, `SPEC:90`, `SPEC:92`, `SPEC:64`, with the checks at `SPEC:182-183`, `SPEC:196`, `SPEC:198`, `SPEC:200`. Make one definition of the contract path hold for every row.
- B-2: `SPEC:73`, `SPEC:159`, `SPEC:195`. Stop P1 from making `--unattended` and its section available on commands whose gate or outward-action rule ships in a later phase.

verdict: FAIL
