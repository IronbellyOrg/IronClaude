review: 1 of 3

# Spec-panel critique, round 1: Orca worker contract spec

- Mode: `--mode critique --focus requirements,architecture`; first review (no `--re-review`, no `--baseline`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Reviewer model actually used: claude-sonnet-5-5.
- Prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). One reviewer in this sandbox, so the three-review MERGE rule is not applied here; the coordinator merges if it runs three.
- Citation shorthand: `SPEC:N` = line N of the candidate. `CAPS:N`, `INV-A:N`, `INV-B:N` = lines of `.dev/orca-command-refactor/inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md`. `CMD:N` = line N of `command.md` (the /sc:spec-panel definition in the sandbox).
- Coverage: read the whole candidate, the README, and the three inventories (CAPS 40-188 sampled by cited line; INV-A 1-120 in full; INV-B at every cited line). Checked section 3 verdict counts (10/27/6 = 43, matching INV-A:73 and INV-B:289), the phase lists against the section 3 phase column (P1 9+4 fixes, P2 15, P3 4, P4 3), and the acceptance checks against the requirements. Every citation into `src/`, `sk/`, `cmd/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `Makefile`, `pyproject.toml` and the Orca install is UNVERIFIED (those files are not in the workspace); this includes SPEC:11 (11 re-read locations) and SPEC:285 (the "340 citations" check). Sampled INV/CAPS citations matched (for example CAPS:97-103, 72-77, 129-130, 145-151, INV-A:90-98, INV-B:289-301).

=== REQUIREMENTS ANALYSIS ===

### B1 (CRITICAL, blocking): `/sc:load` is both given no report and required to have one
Experts: Wiegers (traceability), Adzic (testability). Priority High. Quality impact: Testability 3 to 8 once fixed.

Grading sentence: an implementer who follows the stated text as written builds a `/sc:load` that satisfies the section 3.2 row (no report, "usage line only") and then fails AC-1.1; or builds the `## Unattended mode` section naming `return-contract.yaml` that AC-1.1 demands and breaks the row and the Decision. Either way the P1 acceptance check cannot pass without breaking another stated text.

Conflicting texts:
- SPEC:112: load row, Report (WC-4) = "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)".
- SPEC:265: Decision "`/sc:load` handling": "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- SPEC:76 and SPEC:159: every command in 3.2 gets the `## Unattended mode` section and accepts `--unattended` in P1.
- SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Supporting inventory: INV-B:65 (load writes no file; if dispatched it would need a context-summary file).

Recommendation (narrow, no new mechanism): in AC-1.1 and SPEC:76/159, exclude `/sc:load` explicitly (the same way section-4 commands are excluded), or move `/sc:load` into a list of "brief-step only" commands. Delete rather than add.

### B2 (CRITICAL, blocking): the single report path rule cannot be met by commands whose `--output` is a file or that have no output directory
Experts: Wiegers, Adzic, Cockburn (actor/coordinator needs a known path). Priority High. Quality impact: Completeness and Testability.

Grading sentence: an implementer who follows WC-4 as written puts the contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is the value of `--output`; for `/sc:tdd` and `/sc:init-lite` the brief passes `--output <file>`, so the implementer builds a path under a file (or must guess a directory), and the acceptance check `test -s <contract>` has no defined path to test.

Conflicting texts:
- SPEC:62 (WC-4): contract is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", "known before dispatch".
- SPEC:87: init-lite "Brief must pass `--output <file>`". SPEC:90: tdd "`--output <file>`", report "the TDD at `--output`". SPEC:200 (AC-2.2): `/sc:tdd "auth" --unattended --output <file>` must produce a contract with `status: blocked`.
- SPEC:183 (7.2 step 4): `test -s <contract>` and parse it; SPEC:182: report path "is the WC-4 contract path".
- SPEC:83: adversarial contract is fixed at `<output>/adversarial/return-contract.yaml` (a sub-directory), unlike the `<output>/return-contract.yaml` of brainstorm and reflect (SPEC:84, 88). SPEC:85 and SPEC:86: cleanup-audit and index-repo have a fixed or implied output location and no directory flag.
- SPEC:120: spec-panel gets "add `--output`" with no statement whether it is a file or a directory.
- Evidence the question is real: `CMD:460` (the spec-panel definition in the sandbox) resolves the same problem with a separate `--report-dir` because "`--output` is file-valued".

Recommendation: state one rule for where the contract goes when `--output` is a file (for example a separate directory flag, or the file's parent), and make SPEC:83 agree with WC-4 or state adversarial as the exception. Narrowing, not a new mechanism.

### B3 (CRITICAL, blocking): P1 makes `--unattended` accepted by every command, including those whose unattended gate behaviour arrives only in P2 or P4
Experts: Wiegers (consistency), Nygard (what happens before the safety changes land). Priority High. Quality impact: Consistency.

Grading sentence: an implementer who follows SPEC:159 builds `--unattended` (and the `## Unattended mode` section) on `auggie-review`, `task`, `post-release`, `pr-submit` and `implement` in P1 with no gate resolution, so `/sc:auggie-review <PR> --unattended` still posts to the PR and `/sc:post-release --unattended` still installs or provisions; that contradicts WC-9 and WC-2, which define `--unattended` as "outward defaults off" and "no person-blocking step".

Conflicting texts:
- SPEC:159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
- SPEC:67 (WC-9) and SPEC:60 (WC-2): under `--unattended` outward defaults are off and no gate blocks on a person.
- SPEC:100, 121 (auggie-review, task: P2), SPEC:113, 114, 109 (post-release, pr-submit, implement: P4), SPEC:162, 154 (P4 waits for D2-D4), SPEC:195 (AC-1.1 requires the section on all of them in P1).
- SPEC:138-139 and 114/241 and 240: under D3 option (a), pr-submit is not a worker, yet P1 and AC-1.1 add the flag and section to it.
- Evidence of the outward default: SPEC:67 cites `cmd/auggie-review.md:51-54` (UNVERIFIED here); INV-A:78 states it.

Recommendation: restrict the P1 flag and AC-1.1 to the P1 commands (SPEC:159 list), and add the flag to each P2/P3/P4 command in the phase that converts its gates (this deletes scope from P1 rather than adding a rule).

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The core decision (commands stay units of work, Orca coordinates) is stated consistently across SPEC:16, 28-39, 141-151, 213 and supported by the sampled inventory lines (CAPS:97-103 depth 1, CAPS:148 and CAPS:150 worker_done only from the dispatched pane, INV-A:90, INV-B:285-286). Architecture notes are under follow-up candidates (M5, M7, M8). Experts: Fowler (boundary between command and contract file is clean), Newman (the `--unattended` flag is an additive interface, SA-4), Hohpe (report-file hand-off is a pull model, WC-12), Nygard (pr-submit heartbeat splitting is sound but its timing is unverified, SPEC:283).

=== ADVERSARIAL ANALYSIS (Whittaker) ===
Each finding below is graded under FIRST-REVIEW grading rules; only those listed above as B1-B3 are blocking.

- I can break this specification by **Divergence Attack**. The invariant at **SPEC:62/200** ("contract at `<output-dir>/return-contract.yaml`") fails when **`--output` is a file**. Concrete attack: brief `/sc:tdd "auth" --unattended --output .dev/x/auth-tdd.md` gives `<output-dir>` = `.dev/x/auth-tdd.md`; before: no contract; after: coordinator runs `test -s .dev/x/auth-tdd.md/return-contract.yaml` and gets an error regardless of command behaviour. (= B2.)
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:159 vs SPEC:162** (gates convert in P2/P4) fails when **a coordinator runs `/sc:post-release v1.4 --unattended` after P1 merges**. Concrete attack: P1 state = flag accepted, section present, gate behaviour absent; the command runs its VM and install steps with no person to confirm. (= B3.)
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:113 vs SPEC:62** ("require an explicit `--output` ... else blocked", contract "written on every outcome") fails when **`--output` is empty**. Concrete attack: `/sc:post-release v1.4 --unattended` with no `--output`; the command must write a blocked contract into a directory it was never given. Medium (M3), because the text leaves the fallback undefined rather than stating a wrong one.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62** (`status` in `succeeded|partial|failed|blocked`) fails when **a command's own report already uses `status` with other values**. Concrete attack: workflow's existing contract (SPEC:92, `INV-B:272`) carries its own `status` values; SPEC:62 says commands "keep their fields and add the missing ones", so the same field can hold two vocabularies. UNVERIFIED (the contract ref is not in the workspace); noted as minor.
- Accumulation and other attacks: none found that name a concrete wrong outcome.

=== GUARD CONDITION BOUNDARY TABLE ===
Guards identified: G1 WC-10 wait split (poll wait versus 5-minute heartbeat), G2 WC-4 output-directory presence, G3 WC-5 outcome mapping from contract status, G4 WC-1 readiness fallback (60 s limit). Classes left out: One/Minimal and Maximum/Overflow for G2, G3, G4 cannot occur as distinct cases (the guard is a presence or enum test); Sentinel for G1, G4 has no sentinel value.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 single wait > 4 min | SPEC:68 | Zero/Empty | wait of 0 s | false | not stated; no split needed | OK |
| G1 | SPEC:68 | Typical | 600 s budget made of poll-then-sleep iterations | true (split) | iterate, heartbeat between; confirm each iteration < 4 min (SPEC:114, 283) | OK |
| G1 | SPEC:68, 210 | Maximum | eval timeout 3600 s (SPEC:68) | true | split into waits of at most 4 min | OK |
| G1 | SPEC:68 | Legitimate Edge Case | exactly 5 min, 4 min 30 s | boundary between 4 and 5 min | "at most 4 minutes" for wait, heartbeat "every 5 minutes"; exact gap unstated for one non-splittable call | GAP (Medium, M6: a non-splittable tool call of 4 to 5 min is not addressed) |
| G2 output dir present | SPEC:62, 113 | Zero/Empty | no `--output` | false | post-release: "else blocked"; where the blocked contract is written: unspecified | GAP (Medium, M3) |
| G2 | SPEC:62, 87, 90, 200 | Legitimate Edge Case | `--output <file>` | ambiguous | unspecified | GAP (blocking, B2) |
| G2 | SPEC:62 | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| G3 status to outcome | SPEC:63 | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| G3 | SPEC:63 | Typical | `succeeded`, `failed`, `blocked`, `partial` | mapped | failed for failed/blocked, succeeded otherwise | OK |
| G3 | SPEC:63 | Sentinel Value Match | status value outside the four (existing command vocabulary, SPEC:62) | undefined | unspecified; "no report exists" does not cover an unreadable status | GAP (Medium, M4) |
| G4 launch prompt fallback | SPEC:59 | Typical | fallback 30 s | true | passes | OK |
| G4 | SPEC:59 | Legitimate Edge Case | fallback between 45 s and 60 s | boundary | "well inside" the limit; evidence says above about 45 s fails (`EVIDENCE.md:56`, UNVERIFIED here); no number is required of the launch setup | GAP (Medium, M5) |

Table complete: every guard is enumerated, every cell populated, omitted classes carry their reason (FR-10 satisfied). GAP rows B2 (blocking, FR-8) and the Medium ones are reported as findings. Pipeline Dimensional Analysis: not triggered (no multi-stage data flow whose counts diverge; the phase table is sequencing, not a data pipeline). `--focus correctness` is not active, so no State Variable Registry; auto-suggestion not triggered (no 3+ mutable state variables).

=== FOLLOW-UP CANDIDATES (Medium and minor; never trigger a revision) ===
Medium (warnings):
- **M1** Brief versus P0 (SPEC:73 vs SPEC:79, 194): section 2.3 says the brief carries the command line "including `--unattended`", but the 10 ready commands in 3.1 and the P0 smoke runs have no `--unattended` until P1/P2. Needs a guess at which reading the implementer takes.
- **M2** Decisions needed before P1-P3 (SPEC:154, 225 vs SPEC:100, 121, 244): "Phases 1-3 need no user decision" while D4 (outward authorization) governs auggie-review `--post-pr` and task commit/push, both P2 rows, and D1 governs every phase. SPEC:225 says phases proceed on recommendations, so the two statements can be read as compatible.
- **M3** No place for the blocked contract when `--output` is missing (see Zero/Empty attack above; SPEC:113 vs SPEC:62).
- **M4** Status vocabulary clash with commands' existing `status` fields (SPEC:62, 261, `INV-B:272`).
- **M5** WC-1 has an owner ("Launch setup, not commands", SPEC:59) but no phase deliverable and no acceptance check in section 6 or 7 beyond the generic `state: ready` check (SPEC:180).
- **M6** One non-splittable tool call between 4 and 5 minutes (G1 edge row).
- **M7** SA-2 versus AC-C1 (SPEC:147 vs SPEC:172): SA-2 allows Orca mentions inside the contract file, but AC-C1 greps `src/superclaude/core` (where the contract lives) for `orca orchestration`; if the contract file spells that command the check fails. Needs a guess about the contract's wording.
- **M8** SA-3 versus WC-4 (SPEC:148 vs SPEC:62): SA-3 lets the contract be written "when the caller passes the new output flag" without `--unattended`; WC-4 and AC-1.3 (SPEC:197) tie it to unattended mode.
- **M9** Stale premise for `/sc:spec-panel`: SPEC:120 and SPEC:195 assume the command has no unattended mode and needs `--output`. The command definition supplied for this review already has `--unattended`, `--report-dir`, `--output <file>`, a `<report-dir>/return-contract.yaml` and a reference to `~/.claude/WORKER-CONTRACT.md` (`CMD:23`, `CMD:457-465`). Either the spec was written against an older `cmd/spec-panel.md` (UNVERIFIED, file absent from the workspace) or it ignores existing work; its row and its D1 flag-naming are then partly done and use `--report-dir`, not `--output-dir`.
- **M10** The pr-submit counting (SPEC:76, 139, 114, 162, 240): under D3(a) it is a coordinator-side command, but it is counted among the 27 changed commands and in P4.
- **M11** Citation reliability: SPEC:11 and SPEC:285 claim independent re-checks (11 locations; about 340 citations); UNVERIFIED here, and the 9 defects fixed in place cannot be seen. Over 90 percent of the spec's evidence points at `src/`, `sk/`, `cmd/`, `CLAUDE.md` and the Orca install, none of which is in the workspace.
Minor notes:
- SPEC:252 (D5 (b)) calls R1 a "protection against runaway fan-out"; R1 (SPEC:33) states a refusal, not a protection.
- The Decisions table (SPEC:255-269) is placed after section 9 and before UNVERIFIED items, while README rule order puts `## Decisions` anywhere; no effect.
- AC-C1 (SPEC:172) shows `\|` inside a table cell; copied into a shell it must be unescaped.

Open question for the person running this loop (the command asks once per loop whether to open an issue for the Medium and minor list; this reviewer cannot ask and creates none): open an issue for M1-M11? Not asked in this sandbox, none created.

Reviser brief (applies to review 1; blocking ids only; the reviser reads this report, not the command):
- Blocking finding ids: B1, B2, B3.
- Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing over adding. Report the byte size of the spec before and after, with bytes added and deleted per finding id. Leave Medium and minor findings (M1-M11 and the notes) alone, and do not award yourself a PASS.
- B1: texts SPEC:112, 265, 76, 159, 195; stated wrong outcome: AC-1.1 cannot pass for `/sc:load` without breaking its row.
- B2: texts SPEC:62, 83, 87, 90, 120, 182, 183, 200; stated wrong outcome: the contract path is undefined when `--output` is a file, so AC-2.2 and 7.2 step 4 have no path to test.
- B3: texts SPEC:159, 195, 100, 109, 113, 114, 121, 162 against SPEC:60, 67; stated wrong outcome: after P1 a command accepts `--unattended` while its outward defaults and person-blocking gates are still on.

verdict: FAIL
