review: 1 of 3

# Spec-panel review: orca-worker-contract-spec.md

```yaml
specification_review:
  mode: critique
  focus_areas: [requirements, architecture]
  candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  candidate_sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
  baseline: not given (first review of the full document)
  reviewer_model: claude-sonnet-5-5 (Sonnet 5.5)
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker]
```

## Header record

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (from `sha256sum`, 57763 bytes, 285 lines)
- baseline: none (first review; no `--re-review`, no `--baseline`)
- reviewer model actually used: `claude-sonnet-5-5` (Sonnet 5.5)
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing)
- brief clauses overridden: none

## Evidence rules for this review

- Checkable evidence is only the three files under `.dev/orca-command-refactor/inventory/` plus the spec and README. Citation forms: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.
- Any citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, Orca internals or `EVIDENCE.md` that is not quoted by an inventory file is UNVERIFIED here (no such file exists inside the sandbox).
- I spot-checked every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in spec sections 1, 2, 3, 4 and 8 against the inventory files. Each pointed at the line it names (examples: `INV-A:106`, `INV-B:320`, `INV-A:97`, `INV-B:272`, `CAPS:92`, `CAPS:155`, `CAPS:187`). No wrong inventory line number found.
- Outside the permitted evidence: the definition of `/sc:spec-panel` that I am executing (`command.md:460`) says "`--report-dir <dir>` only (`--output` is file-valued)". That is not evidence about the repo's current commands. I use it only as a pointer that the file-versus-directory question in F-01 is real, and mark it UNVERIFIED for the repo.

## Verdict summary

4 blocking findings (F-01 to F-04), 14 Medium follow-up candidates (M-01 to M-14), 4 minor notes (m-01 to m-04). Last line of this file is `verdict: FAIL`.

| id | severity (graded by consequence) | one line |
|---|---|---|
| F-01 | CRITICAL, blocking | WC-4 report path rule is undefined or impossible for file-valued `--output`, fixed-directory and generated-directory commands |
| F-02 | CRITICAL, blocking | Phase 1 puts `--unattended` on all 37 commands before the gates of the 19 gated ones exist; that breaks WC-2 and WC-9 and "each phase leaves a safe state" |
| F-03 | MAJOR, blocking | The additive-edit check `grep -E '^-[^-]'` (AC-C5, AC-0.3) cannot see a deleted markdown bullet or a deleted `---` line |
| F-04 | MAJOR, blocking | `/sc:load` is both "no report, usage line only" and a P1 command that AC-1.1 requires to carry an Unattended section naming `return-contract.yaml` |

---

=== REQUIREMENTS ANALYSIS ===

### F-01 (blocking) WC-4 path rule does not hold for commands whose output is a file, fixed, or generated

- Experts: Karl Wiegers (lead), Gojko Adzic, Gregor Hohpe.
- Location: `SPEC:62` (WC-4), `SPEC:73` (section 2.3), `SPEC:83-92` (section 3.1 rows), `SPEC:200` (AC-2.2), `SPEC:182` (7.2 step 3).
- Stated text: WC-4 puts the report at `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and section 2.3 says the coordinator knows the path before dispatch (`SPEC:62`, `SPEC:73`).
- Grading sentence: An implementer who follows the stated text as written builds a `tdd` that, given `--output docs/x/TDD.md`, writes `docs/x/TDD.md/return-contract.yaml`, and a coordinator that follows 2.3 looks for the report there; that path cannot exist because `TDD.md` is a file. The text is wrong for at least these commands, each shown in the spec's own rows:
  - `tdd` and `init-lite` take `--output <file>` (`SPEC:87`, `SPEC:90`).
  - `cleanup-audit` has a fixed `.claude-audit/` directory and no output flag (`SPEC:85`; INV-A:42).
  - `index-repo` has no flag and an implied repo-root location (`SPEC:86`; INV-A:53).
  - `workflow` writes into `.dev/tasks/to-do/<id>/`, where `<id>` is generated at run time, so the path is not known before dispatch (`SPEC:92`; INV-B:272). The row's fix, "write the contract for pre-creation STOPs too", has no directory to write to, because the package does not exist yet at a pre-creation STOP (INV-B:272 says "Not written for pre-creation STOPs").
  - `adversarial` puts its contract at `<output>/adversarial/return-contract.yaml` (`SPEC:83`), which is not `<output-dir>/return-contract.yaml` for the `--output <dir>` the brief passes.
- Acceptance consequence: AC-2.2 itself uses `/sc:tdd "auth" --unattended --output <file>` and expects a `blocked` contract (`SPEC:200`); the stated text gives no path at which to look for it, so the criterion cannot be run as written.
- Adzic example. Given the brief `/sc:tdd "auth" --unattended --output .dev/out/TDD.md`; When the bare-topic gate fires; Then WC-4 says write `status: blocked` to `<output-dir>/return-contract.yaml`. The before state has `.dev/out/` empty. The after state is undefined: `.dev/out/TDD.md/` is not creatable if `TDD.md` was already written, and `.dev/out/return-contract.yaml` is the unstated guess. Degenerate variant: `--output` omitted: the text names no location at all.
- Recommendation: state one rule that covers all cases, for example "the contract is written to the caller-supplied `--report-dir <dir>` (a directory flag distinct from the file-valued `--output`), else the directory part of `--output`, else a path the row names" and name the path for each 3.1 row that has a fixed or generated directory. Delete the "`--output` / `--output-dir`" alternative that conflates file and directory.
- Priority: High. Quality impact: Completeness 4 to 7, Testability 5 to 8.

### F-04 (blocking) `/sc:load` is excluded from reporting and also required to report

- Experts: Karl Wiegers, Gojko Adzic.
- Location: `SPEC:112` (3.2 `load` row), `SPEC:265` (Decisions), `SPEC:159` (P1 scope), `SPEC:195` (AC-1.1), `SPEC:76` (section 3 intro).
- Stated texts that contradict each other:
  - `SPEC:112`: report "none (see note)", resume "n/a", change "none: use it as a step inside another worker's brief, not as its own Task"; phase "P1 (usage line only)".
  - `SPEC:265`: "a report file would be an unrequested addition".
  - `SPEC:76`: "Every changed command also gains the `## Unattended mode` section".
  - `SPEC:159`: P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - `SPEC:195`: AC-1.1 asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Grading sentence: An implementer who follows the text as written makes `load` pass AC-1.1 by adding an Unattended section that names `return-contract.yaml`, which tells a reader that `load` writes the WC-4 contract; the Decision at `SPEC:265` and the row at `SPEC:112` say it writes no report. Or the implementer follows the row, and the P1 gate (7.1: "a phase passes only when every check in its block ... passes") cannot be passed. Either reading violates a stated text.
- Recommendation: remove `load` from the AC-1.1 and P1 "every command" sets, or state in one sentence what `load`'s Unattended section says (for example "writes no contract; use inside a brief"), and make AC-1.1 test for that sentence.
- Priority: High. Quality impact: Consistency 5 to 7.

---

=== ARCHITECTURE ANALYSIS ===

### F-02 (blocking) Phase 1 ships `--unattended` on 37 commands while 19 of them still have an unconverted gate

- Experts: Martin Fowler (lead), Michael Nygard, Sam Newman.
- Location: `SPEC:154` ("Each phase is independently useful and leaves standalone behaviour unchanged"), `SPEC:159` (P1), `SPEC:160-162` (P2-P4), `SPEC:60` (WC-2), `SPEC:67` (WC-9), `SPEC:195` (AC-1.1).
- Stated text: P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". The gates of the gated commands are converted in P2 (15 commands), P3 (4) and P4 (3) (`SPEC:160-162`).
- Pipeline Dimensional Analysis (FR-17 to FR-19; see the Quantity Flow Diagram below). P1 input is 37 commands that accept the flag (10 in 3.1 plus 27 in 3.2). Of these, 18 have no gate to convert, so a no-op is correct: the 9 P1 commands of 3.2, the 6 ready commands with no `--unattended` gate (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow), and save, validate-roadmap and validate-tests (drift fixes only). The other 19 accept the flag while their gate conversion lands later: 15 in P2 (11 from 3.2 plus reflect, release-split, tdd, troubleshoot), 1 in P3 (roadmap's resume prompt) and 3 in P4 (implement, post-release, pr-submit). Under FR-19 that 37-versus-18 mismatch is CRITICAL.
- Grading sentence: An implementer who follows P1 as written, and then stops because "each phase is independently useful", ships `/sc:auggie-review --unattended` that is accepted but still posts to GitHub and then waits on a chat offer (the P2 row at `SPEC:100`; INV-A:38 shows both are default-on), and `/sc:post-release --unattended` that is accepted but still asks the pre-tag and outward-action questions (P4, `SPEC:113`). WC-2 says no person-blocking step under `--unattended`, and WC-9 says outward defaults are off under it; both are violated, and the first is an outward write to a third party. The parenthetical "(a no-op where a command has no gate)" does not say what the flag does where a command does have one, so a reader cannot tell whether those 19 are no-ops, refusals or full implementations.
- Whittaker attack (FR-2.4 Sequence Attack): see W-2.
- Recommendation: narrow P1 to the 18 commands without a gate, and make the flag land on each of the other 19 in the phase that converts its gate; or state that in P1 a gated command refuses `--unattended` with a clear message until its phase. Align AC-1.1 and the section 3 intro (`SPEC:76`) with the narrowed set.
- Priority: High. Quality impact: Consistency 5 to 8, Safety posture 5 to 8.

### Quantity Flow Diagram (FR-21)

```text
[inventories: 21 (INV-A:3) + 22 (INV-B:3) = 43 commands]
   --> [classification, SPEC:76]  10 ready (3.1) + 27 needs change (3.2) + 6 coordinator-only (section 4) = 43   (conserved)
   --> [phase assignment of the 27, SPEC:97-125]  P1 9 + P2 11 + P3 4 + P4 3 = 27   (conserved)
   --> [phase assignment of the 10 ready, SPEC:81-92]  P1 fixes 4 + P2 fixes 4 + no phase 2 (brainstorm, init-lite) = 10   (conserved)
   --> [P1 deliverable "flag accepted by every command in 3.1 and 3.2", SPEC:159]  37 commands accept --unattended
          |-- 18 have no gate to convert (9 P1 + 6 ready no-gate + save, validate-roadmap, validate-tests)   (no-op is correct)
          |-- 19 accept the flag while their gate conversion lands later: P2 15, P3 1 (roadmap), P4 3   <-- MISMATCH 37 vs 18 (F-02)
   --> [AC-1.1 test population, SPEC:195]  37 commands must carry a section naming return-contract.yaml   <-- includes load (F-04)
```

No other count mismatch found: 10 + 27 + 6 = 43 and 9 + 11 + 4 + 3 = 27 both reconcile with the rows.

### Guard Condition Boundary Table

The spec contains conditional logic and thresholds (readiness limit, heartbeat and wait sizes, outcome mapping, flag recognition, confidence threshold, diff filters), so the table is produced. Experts: Nygard (construction), Crispin's checklist applied by Nygard (completeness), Whittaker (attack). One row per applicable input class; classes left out are listed in the line below the table with the reason. Every cell is filled and every guard is enumerated (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 WC-1 prompt fallback "well inside" the readiness limit | SPEC:59 | Typical | fallback 30 s | passes (EVIDENCE via CAPS:49: start returned after 34 s) | worker reaches `input_accepted` | OK |
| G1 | SPEC:59 | Maximum/Overflow | fallback 46 to 60 s | not decidable: "well inside" has no number; CAPS:49 quotes "above about 45 seconds ... fail again" while the limit is 60 s | none | GAP (M-05) |
| G2 WC-10 wait split | SPEC:68 | Typical | single call 10 min | split into waits of at most 4 min | stated | OK |
| G2 | SPEC:68 | Legitimate Edge Case | single call 4 min 30 s | not "longer than 5 minutes", so unsplit; AC-4.3 (`SPEC:210`) demands "no single tool call exceeds 240 s" | WC-10 and AC-4.3 disagree between 240 s and 300 s | GAP (M-04) |
| G2 | SPEC:68 | One/Minimal | single call of exactly 5 min 00 s | "longer than 5 minutes" is false | none | GAP (M-04) |
| G3 WC-5 outcome from report `status` | SPEC:63 | Typical | `succeeded`, `partial`, `failed`, `blocked` | mapped to succeeded, succeeded, failed, failed | stated | OK |
| G3 | SPEC:63 | Zero/Empty | contract file empty, unparsable or `status` key missing | only "no report exists" is mapped | none | GAP (M-11) |
| G3 | SPEC:63 | Sentinel Value Match | `status` from an existing contract, outside the four values (WC-4 says existing commands "keep their fields") | none | none | GAP (M-11) |
| G4 WC-4 report location | SPEC:62 | Typical | `--output <dir>` | `<dir>/return-contract.yaml` | stated | OK |
| G4 | SPEC:62 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | `<file>/return-contract.yaml` | impossible path | GAP (F-01) |
| G4 | SPEC:62 | Zero/Empty | no output flag: fixed directory (cleanup-audit, index-repo) or generated directory (workflow, pre-creation STOP) | no `<output-dir>` exists | none | GAP (F-01) |
| G5 `--unattended` recognized | SPEC:51, SPEC:228 | Typical | standalone token `--unattended` | mode on | stated by D1(a) | OK |
| G5 | SPEC:51, SPEC:228 | Sentinel Value Match | `--unattended` appearing inside the quoted free-text prompt of tdd, troubleshoot, task, research | no token rule is given | none | GAP (M-07) |
| G6 contract written only when "unattended mode or when the caller passes the new output flag" | SPEC:148 (SA-3) vs SPEC:62 (WC-4) | Legitimate Edge Case | `--output` given, `--unattended` absent | WC-4 says unattended only; SA-3 says either | two readings | GAP (M-01) |
| G7 /sc:task confidence below 0.70 resolves as blocked | SPEC:121 | Zero/Empty | confidence 0.0 | blocked | stated | OK |
| G7 | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | guard is "below 0.70" (INV-B:199 "< 0.70"), so it proceeds | stated by the inventory threshold | OK |
| G8 AC-C5 / AC-0.3 additive-edit filter `grep -E '^-[^-]'` | SPEC:176, SPEC:193 | Typical | modified prose line | caught | stated | OK |
| G8 | SPEC:176, SPEC:193 | Sentinel Value Match | deleted markdown bullet `- Will Not: push` (appears as `-- Will Not: push`) and deleted `---` frontmatter line (appears as `----`) | not caught; reproduced in this run | none | GAP (F-03) |
| G9 AC-1.1 population "every command in 3.1-3.2" | SPEC:195 | Legitimate Edge Case | `load` (no report, usage line only) | contradiction | none | GAP (F-04) |
| G10 P1 "flag accepted by every command" | SPEC:159 | Maximum/Overflow | all 37 including gated and outward-capable ones | flag behavior for the 19 gated ones is not stated | none | GAP (F-02) |
| G11 contract freshness on resume or retry | SPEC:64 (WC-6), SPEC:62 | Legitimate Edge Case | `--resume` or `--retry-of` into a directory that holds a contract from the previous attempt | no rule that the command invalidates or overwrites it first | none | GAP (M-02) |
| G12 WC-9 outward default off | SPEC:67 | Typical | auggie-review PR posting | off (row `SPEC:100`) | stated | OK |
| G12 | SPEC:67 | Legitimate Edge Case | "calls a paid external run"; reflect default UC-2 folder move and tracked-file write (INV-B:114); web search by research and review-translation | not in or out of the list | none | GAP (M-13) |
| G13 WC-12 `check` before `worker_done` | SPEC:70 | Zero/Empty | `check` returns nothing | CAPS:67: an empty check never means replaced; continue | stated by CAPS:67 | OK |

Classes left out, with reason: G1 Zero/Empty (a 0 s fallback means the prompt never waits, which is the goal); G1 One/Minimal and Typical-over (covered by the 30 s row); G2 Zero/Empty (a 0 s wait needs no split); G3 One/Minimal (no counter involved); G4 One/Minimal (same as Typical); G5 Zero/Empty (no token means flag off, which is standalone behavior, SA-1); G5 Maximum (no count involved); G7 Maximum (confidence 1.0 behaves like Typical proceed); G8 Zero/Empty (an empty diff prints nothing and passes, which is correct); G13 Maximum/Sentinel (no numeric or sentinel input).

FR-8 and FR-9 grading: the GAP rows G4 (two rows), G8, G9 and G10 name a concrete wrong outcome or a safety-boundary risk, so they are the blocking findings F-01, F-03, F-04, F-02. The other GAP rows are Medium and are listed under follow-up candidates.

### Quality assessment

| dimension | score 0-10 | note |
|---|---|---|
| Clarity | 7 | rows are dense but each requirement has an owner and evidence column |
| Completeness | 6 | report-path rule (F-01) and phase scoping (F-02) leave holes |
| Testability | 6 | most acceptance checks are runnable; AC-C5 filter and AC-1.1 population are defective (F-03, F-04) |
| Consistency | 6 | four internal contradictions (F-01, F-02, F-04, M-04) |

---

=== ADVERSARIAL ANALYSIS (James Whittaker) ===

Whittaker's attacks apply the five methodologies against the spec's invariants. Each finding uses the FR-3 template and carries the id of the finding it supports.

- **W-1.** I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`SPEC:62`)**, "the report is at `<output-dir>/return-contract.yaml`", fails when **`--output` is a file path (tdd, init-lite) or absent (cleanup-audit, index-repo, workflow)**. Concrete attack: before: `.dev/out/` exists and is empty. Brief: `/sc:tdd "auth" --unattended --output .dev/out/TDD.md`. Step 1: the command resolves `<output-dir>` = `.dev/out/TDD.md`. Step 2: it writes the TDD to that path. Step 3: it must write `.dev/out/TDD.md/return-contract.yaml`, which fails because `TDD.md` is a file (or fails earlier when the gate fires first and `TDD.md` does not yet exist and gets created as a directory). After: no contract at any path the coordinator can compute; `test -s <contract>` in 7.2 step 4 cannot be formed. Supports F-01.
- **W-2.** I can break this specification by **Sequence Attack**. The invariant at **P1 versus P2 to P4 (`SPEC:159-162`) and WC-9 (`SPEC:67`)**, "under `--unattended` outward defaults are off", fails when **a phase is shipped and used before its successor**. Concrete attack: after P1 merges, the coordinator briefs `/sc:auggie-review 123 --unattended --output .dev/r/` as the contract in 2.3 says. Before: the PR has 0 reviews. The P1 command accepts the flag, which P1 treats as a no-op for a gated command; P2 (where "`--unattended` implies `--no-post-pr`", `SPEC:100`) has not landed. The run posts a review with `gh pr review --comment` and inline comments without a prompt (INV-A:38). After: 1 review and N inline comments exist on the PR, and the contract shows `succeeded`. Supports F-02.
- **W-3.** I can break this specification by **Divergence Attack**. The invariant at **WC-4 versus SA-3 (`SPEC:62` versus `SPEC:148`)**, "no new file appears unless asked", fails when **the caller passes the new output flag without `--unattended`**. Concrete attack: a person runs `/sc:analyze src/x.py --output out/`. WC-4 says the contract is an unattended-mode artifact; SA-3 says it is also written "when the caller passes the new output flag". Both branches apply to the same input and give different file sets (0 or 1 `return-contract.yaml`), and AC-1.3 (`SPEC:197`) tests only the case with neither. Supports M-01.
- **W-4.** I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) (`SPEC:228`)**, "[`--unattended`] cannot misfire on a person", fails when **the free-text prompt of a command contains the string `--unattended`**. Concrete attack: a person (or a coordinator) briefs `/sc:workflow "add --unattended to analyze and build" --handoff none`. The text names no token rule, so a parser that scans the whole argument string sees the flag. Before: gates active. After: gates resolve as blocked, outward defaults off, and a contract is written, none of which the person asked for. This is the exact subject of this refactor, so the collision is likely in this project's own prompts. The command definition under review runs here (`command.md:459`) restricts the switch to "a standalone argument token outside any quoted argument"; the spec has no such sentence. Supports M-07.
- **W-5.** I can break this specification by **Sequence Attack**. The invariant at **WC-4 and WC-5 (`SPEC:62-63`)**, "the report is written on every outcome, and no report means failed", fails when **a resumed or retried run dies before it rewrites the contract**. Concrete attack: attempt 1 of `/sc:brainstorm --unattended --output D` ends `status: succeeded`, then the coordinator retries it with `worker-start --retry-of` (for example because the worker was fenced) and the same brief. Attempt 2 reads state from `D`, hits an error before its first write, and the context ends. State trace: `D/return-contract.yaml` still holds attempt 1 with `status: succeeded`; "no report exists" is false; WC-5 maps `succeeded` to `--outcome succeeded`. Nothing in the contract (`SPEC:62`) identifies the run, such as a dispatch id or start time, so 7.2 step 4 (`SPEC:183`) also passes. Supports M-02.
- **W-6.** I can break this specification by **Accumulation Attack**. The invariant at **SPEC:85 (cleanup-audit)**, "one audit per worktree at a time", fails when **two audits run one after the other in the same worktree**. Concrete attack: audit 1 completes and leaves `.claude-audit/progress.json` (INV-A:42: "enables resume-from-checkpoint"). Audit 2 for a different `--pass` or a changed tree starts, finds the checkpoint, and resumes it as if interrupted. The spec says "fresh dir" is not available (output dir is fixed) and gives no rule for clearing a completed checkpoint. Whether a completed checkpoint is resumed is UNVERIFIED (INV-A:42 does not say). Supports M-02 (graded Medium because the resume behavior is unverified).

---

## Cockburn, Newman, Nygard and Hohpe notes (no separate blocking items)

- Cockburn (actor and goal): the primary actor is the coordinator and the goal "dispatch a command and read one trustworthy report" is clear (`SPEC:16`, `SPEC:73`); the main success scenario exists as 7.2 steps 1 to 7. The extension scenarios (worker asks and is answered, worker retried, worker fenced) have no matching acceptance scenario. See M-06.
- Newman (evolution): no version on the contract or on `WORKER-CONTRACT.md`, and WC-4 says existing contracts "keep their fields" while fixing `status` to four values, so a v1.1 contract such as the workflow one (INV-B:272) and the new schema collide. See M-11.
- Nygard (failure): the stale-contract path (W-5), the fixed-directory accumulation path (W-6) and the "no heartbeat while blocked in ask" rule (`SPEC:61`, CAPS:64) are the failure edges; only the last is covered by the text.
- Hohpe (exchange pattern): WC-3 delivers a coordinator answer by "re-invoke or resume the command with the answer as a flag" (`SPEC:61`). For gates the spec resolves only as "blocked" with no answer flag (cli-portify approvals `SPEC:105`, review-translation Phase 1 `SPEC:117`, implement Ruling `SPEC:109`), there is no flag to carry the answer. See M-12.

---

## follow-up candidates

Medium and minor findings. None triggers a revision, none fails this review, and none appears in the Reviser brief. Issue offer: not made (no interactive user in this run); nothing was created.

### Medium (warnings)

- **M-01** (Wiegers) SA-3 (`SPEC:148`) lets the contract be written "when the caller passes the new output flag", WC-4 (`SPEC:62`) says only "in unattended mode". Pick one trigger and add the other case to AC-1.3. Source of the attack: W-3.
- **M-02** (Nygard, Whittaker) Stale or reused state. No requirement that a command delete or overwrite its contract at start, no freshness field (dispatch id, start time) in WC-4, and WC-6 (`SPEC:64`) says "fresh output directory" without saying who creates it (the coordinator's brief fixes `<output-dir>` before dispatch, SPEC:62, SPEC:73, so a retry with the same brief reuses it). Supports W-5, W-6. Needs the reader to guess which reading of "fresh" applies, hence Medium.
- **M-03** (Fowler) AC-C1 (`SPEC:172`) greps `src/superclaude/core` and must print nothing in every phase, yet P0 adds an Orca section to `HOW-WE-WORK.md` and writes `WORKER-CONTRACT.md` (`SPEC:158`), and SA-2 allows "Orca as an example of a caller's question channel inside the contract file" (`SPEC:147`). Whether the section text contains `orca orchestration` is not stated; if it does, AC-C1 fails in P0. SA-2 also says "contract file" for `WORKER-CONTRACT.md` while section 3 says "Contract" for `return-contract.yaml` (`SPEC:52`, `SPEC:76`).
- **M-04** (Nygard, Crispin) WC-10 (`SPEC:68`) splits calls "longer than 5 minutes" into at most 4 minutes; the rows (`SPEC:104`, `SPEC:114`), Decisions (`SPEC:266`) and AC-4.3 (`SPEC:210`) use 4 minutes or 240 s. A 4 min 30 s call complies with WC-10 and fails AC-4.3, and it leaves too little room under the 5-minute heartbeat cadence (CAPS:130). Table G2.
- **M-05** (Wiegers) WC-1 (`SPEC:59`) says "well inside" the 60 s limit with no number, although the evidence it cites (CAPS:49) gives 30 s passing and "above about 45 s" failing. The owner is "Launch setup, not commands" and no phase delivers it or checks it (7.2 step 1 only checks `state: ready`). Table G1.
- **M-06** (Wiegers, Cockburn) Traceability. Of WC-1 to WC-12, no acceptance check exists for WC-3 (ask path), WC-6 (a retry does not corrupt attempt 1), WC-11 outside `save`, WC-12 or the cli-eval wait split (WC-10 is tested only for pr-submit, AC-4.3); WC-7 is checked only in P0 (AC-0.4).
- **M-07** (Whittaker) No token-recognition rule for `--unattended`; see W-4. Table G5.
- **M-08** (Nygard) `partial` maps to `--outcome succeeded` (`SPEC:63`, `SPEC:263`), and a succeeded Task makes its dependents ready (CAPS:89-90, CAPS:86), so a DAG successor starts on a partial deliverable unless the coordinator opens the report first. The contract word `blocked` also collides with the Orca Task status `blocked` (CAPS:89), which means a dependency state, not a gate. The spec's own 1.3 example chains troubleshoot reports into an adversarial worker (`SPEC:39`).
- **M-09** (Cockburn) Evidence strength is stated inconsistently. Section 3.1 says the 10 commands "run as workers now" (`SPEC:79`) and the Decisions say verdicts are kept (`SPEC:268`), while section 1.4 says no command was run end to end as an Orca worker and PR #329 proves only the nested route (`SPEC:43`; INV-B:323); INV-A:35 calls adversarial "proven" and `SPEC:23` cites `skill-direct` as evidence of success. Also section 1.4 says "Phase 0 therefore starts with live smoke runs" (`SPEC:43`) while P0 writes the contract, the installer change and the routing section first and runs the smoke tests "Then" (`SPEC:158`), so the decision is tested after work is built on it.
- **M-10** (Fowler, Nygard) The tasklist row (`SPEC:122`) makes Stage 10.5 pass `--unattended` to reflect so "the headless rule applies". INV-B:215 and INV-B:205 recommended the opposite for tasklist (drop `--remediate`), and the headless rule keys on `claude --print` (INV-B:109, INV-B:310; the spec's own UNVERIFIED 9 says an Orca worker is assumed not headless, `SPEC:280`). The remediation auto-accept would then start a corrective `sc:workflow` run inside tasklist generation. INV-B:209 also leaves unresolved who answers a `needs_human_decision` HALT inside a subagent (UNVERIFIED), which WC-2 requires to resolve as (a), (b) or (c). The row's nesting claim (`INV-A:14`) conflicts with INV-B:210 and INV-B:314, which mark nested spawning UNVERIFIED.
- **M-11** (Newman, Hohpe) Contract schema gaps: no `contract_version`; "keep their fields" versus a fixed `status` set (`SPEC:62`, `SPEC:262`) with no mapping for existing values; report paths not defined as relative to repo root or worktree; unknown, missing or unparsable `status` has no mapping in WC-5 (Table G3).
- **M-12** (Hohpe) WC-3 delivers the answer "as a flag" (`SPEC:61`) but the 3.2 rows for cli-portify, review-translation and implement define no answer flag; the sequencing of D4 also matters: P2 builds WC-9 authorization behavior (`SPEC:100`, `SPEC:121`) while D4 (`SPEC:244`) names auggie-review and task as affected and Phase 4 is where the answer is applied (`SPEC:154`, `SPEC:162`). A "never" answer to D4 would force P2 rework.
- **M-13** (Wiegers) WC-9's list (`SPEC:67`) does not define "paid external run". Reflect's default UC-2 folder move and tracked-file write (INV-B:114) stay on under `--unattended` unless the brief passes `--no-promote` (`SPEC:88`), and web search in research and review-translation (INV-B:134, INV-B:144) is neither in nor out. Table G12.
- **M-14** (Fowler) AC-C5 (`SPEC:176`) says edits must be additive, but adding a flag to a command normally changes its Usage line; a changed line shows as a removed line in `git diff -U0` and AC-C5 would print it. The `load` row itself fixes a Usage line (`SPEC:112`). Decide whether Usage-line edits are allowed and say so in SA-4.

### Minor (notes)

- **m-01** `SPEC:11` lists 11 re-read locations; none of them, and none of the `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml` or Orca-internal lines cited in sections 1, 2 and 7, can be checked inside this sandbox. They stand as UNVERIFIED here: for example the E5 grep result (`SPEC:25`), `src/superclaude/cli/install_core.py:13-24` (`SPEC:52`), `CLAUDE.md:74,83,334,408` and `pyproject.toml:38`.
- **m-02** The same top-level rule is cited at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`SPEC:11`, `SPEC:65`; INV-B:90) and at `:47-49` (CAPS:40, CAPS:161, which cites the installed copy). Two copies with different line numbers; harmless but worth one clarifying clause.
- **m-03** `SPEC:114` says the pr-submit 600 s default is a cumulative budget (citing `SKILL.md:46-64`, unreadable here), while INV-B:95 and INV-B:299 describe "600 s per wait". The spec marks the poll runtime UNVERIFIED (item 12), so only the reading differs.
- **m-04** `SPEC:120` (spec-panel row) says to "add `--output`". The definition of the command I am running already has `--output <file>`, `--report-dir <dir>` and an `--unattended` section (`command.md:22-23,455-465`). That is outside the permitted evidence (UNVERIFIED for the repo's `cmd/spec-panel.md`), but if the repo copy matches it, the row and `SPEC:62` need to follow it.

---

## Coverage statement

- Covered: the whole candidate (all 285 lines): sections 1 to 9, the Decisions table and all 14 UNVERIFIED items; every acceptance check in 7.1 to 7.3; every 3.1, 3.2 and section 4 row against the inventory row it cites; the three inventory files for cross-checking counts, verdicts and line numbers; the Quantity Flow of counts (43, 10/27/6, phase sums); `grep -E '^-[^-]'` behavior, reproduced with `diff -U0` on test text in this run (a deleted `---`, a deleted `- Will Not: push` bullet and a modified usage line gave one hit, the usage line).
- Not covered: any `src/`, `CLAUDE.md`, `Makefile`, Orca-internal or `EVIDENCE.md` line (not present in the sandbox; UNVERIFIED); live Orca behavior; whether the claims in the spec's UNVERIFIED list hold; the 340-citation validator pass the spec reports at `SPEC:285`, which I could not repeat.
- Not done by design: no edit to the candidate, no second review, no revision of any finding.

## Reviser brief

Findings to repair: F-01, F-02, F-03, F-04.

Rules restated from the command (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that a listed finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

- F-01: the WC-4 `<output-dir>` rule and the 3.1 rows for tdd, init-lite, cleanup-audit, index-repo, workflow and adversarial (`SPEC:62`, `SPEC:73`, `SPEC:83-92`), plus AC-2.2 (`SPEC:200`).
- F-02: the P1 scope sentence and the matching AC-1.1 population and section 3 intro (`SPEC:159`, `SPEC:195`, `SPEC:76`).
- F-03: the check command in AC-C5 and AC-0.3 (`SPEC:176`, `SPEC:193`).
- F-04: the `load` entries in P1 scope, AC-1.1 and the section 3 intro (`SPEC:112`, `SPEC:159`, `SPEC:195`, `SPEC:76`).

verdict: FAIL
