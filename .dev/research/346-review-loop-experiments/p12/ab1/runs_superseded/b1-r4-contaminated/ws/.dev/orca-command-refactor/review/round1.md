review: 1 of 3

# Merged first review (coordinator; MERGE rule over three independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 3254a1be810c50abdfc50715615147f4ef0a63496dffb9f2773ba03c6eaddd37
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 d770a778057aa434434aab1dbb9d9f774f1f3e52d51260ac27a521c9c5e3073a
- .dev/orca-command-refactor/review/round1-c.md verdict FAIL sha256 5561a04cd50cd9a658af3789852cc46be36e6c534d725e72e73658d248072c52

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M2, M3, M5. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M1 (verifier: A section that names the contract can say load writes none, so AC-1.1 does not force a report file and 265 is not violated; the two texts do not contradict without the assumption that the section means a report. (M1.a, M1.b checked)); M4 (verifier: The claimed outcome (auggie-review or post-release still posts or installs after P1) is a phase-interim state of a phased plan, not a stated result; the text never says P1 ships the flag as live behavior, and the pr-submit/D3 part is the same issue as M5. (M4.a checked)). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M2

#### M2.a, from round1-a.md F2: F2 (blocking, Adzic / Wiegers): AC-0.4 step 3 cannot pass in P0 for the commands it names
- Texts: AC-0.4 (SPEC:194) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 of the live check (SPEC:182) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Facts the spec itself states: in P0 no command has the WC-4 contract or `--unattended` (the contract is added in P1, SPEC:159; SPEC:79 says the worker "reports the named file until Phase 1 adds the contract"). The `/sc:troubleshoot` row names `REPORT.md` as its report (SPEC:91). The inventory confirms troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:242`), so it has no contract `status` to match.
- Grading sentence: An implementer who runs AC-0.4 as written on `/sc:troubleshoot "<symptom>"` finds no contract file, so "the contract's `status`" and "the WC-4 contract path" in step 3 do not exist, and the check cannot pass. The same holds for `/sc:adversarial`, whose contract filename is not fixed until P1 (SPEC:83; `INV-A:60`). AC-0.4 exempts only step 4, not step 3.
- Why blocking: an acceptance criterion cannot pass as written. The fix is narrow (step 3 in P0 compares the outcome with the command's existing report, as step 4 already does).

#### M2.b, from round1-c.md F2: F2 (blocking) - Adzic, Crispin - AC-0.4 cannot pass as written
Grading sentence: an implementer who runs AC-0.4 as written on `/sc:troubleshoot` and `/sc:adversarial` builds a P0 whose step 3 can never pass, because step 3 requires the report path to be "the WC-4 contract path" and the spec says that contract does not exist until P1.

Quoted texts:
1. Spec:182 (7.2 step 3): "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
2. Spec:194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
3. Spec:62 (WC-4): the contract is `<output-dir>/return-contract.yaml`; spec:91: troubleshoot's report today is `REPORT.md`; spec:83: adversarial's contract filename "not fixed" and the fix is P1 (spec:159, spec:198).

Attack (state trace): P0 smoke run of troubleshoot. Before: no `return-contract.yaml`. Worker sends `worker_done --report-path REPORT.md`. Step 3 pass condition: "report path is the WC-4 contract path" -> false; "outcome matches the contract's status" -> there is no contract to match. AC-0.4 declares steps 1-3 must pass. The text relaxes only step 4. The gate that decides whether section 1 stands (spec:194, "a failure here reopens section 1") therefore fails or is applied by guess.

Recommendation: state in AC-0.4 that step 3 also uses the existing report file for P0 (the same relaxation already given for step 4). Priority High.

### M3

#### M3.a, from round1-b.md B2: B2 (CRITICAL, blocking): the single report path rule cannot be met by commands whose `--output` is a file or that have no output directory
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

### M5

#### M5.a, from round1-c.md F1: F1 (blocking) - Wiegers, Cockburn - AC-1.1 contradicts D3(a), the P4 deferral and "Phases 1-3 need no user decision"
Grading sentence: an implementer who follows the stated text as written builds a P1 that adds an `## Unattended mode` section, a `--unattended` flag and a passing test for `pr-submit`, `implement` and `post-release`, and that is wrong because the same document says those three commands' unattended behaviour waits for user decisions D2-D4 in P4, and under the recommended D3(a) pr-submit gets no change at all.

Quoted texts:
1. Spec:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
2. Spec:195 (AC-1.1, a P1 check): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
3. Spec:154 and spec:225: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
4. Spec:240 (D3(a), the recommendation): "no pr-submit changes in Phase 4"; spec:139: "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
5. Spec:109, spec:113, spec:114, spec:162: implement, post-release and pr-submit are rows of section 3.2 with phase P4 and gates that D2 to D4 decide.

Attack (Whittaker, sequence attack): run the phases in the spec's order. After P1, AC-1.1 passes only if pr-submit, implement and post-release each carry the section. pr-submit has real gates (`--monitor 1` y/n, operator HALTs, `INV-B:34`, `INV-B:89`), so a "no-op" flag is not available for it (the text at 159 allows a no-op only "where a command has no gate"). Under D3(a) the section must not exist, so AC-1.1 fails by construction for the recommended path. Under D3(b) it is P4 work done in P1 before the user decided. Two stated texts contradict (AC-1.1 against D3(a) and against 154/225), and an acceptance criterion cannot pass on the recommended path.

Evidence check: inventory confirms pr-submit has default-off gates only at `--monitor 1` and halts handed to "the operator" (`INV-B:89`), and implement's halt cannot be unblocked by another agent (`INV-A:66`; the Ruling rule at `refs/qa.md:238` is quoted in `commands-a.md` notes and is UNVERIFIED against the source here).

Recommendation (narrow, no new rule): scope AC-1.1 and the P1 flag scope to the commands whose phase is P1-P3, and list pr-submit, implement and post-release as P4 only. Priority High.

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M1 (verifier: A section that names the contract can say load writes none, so AC-1.1 does not force a report file and 265 is not violated; the two texts do not contradict without the assumption that the section means a report. (M1.a, M1.b checked))

#### M1.a, from round1-a.md F1: F1 (blocking, Wiegers / Adzic): AC-1.1 requires a contract-naming `## Unattended mode` section on `/sc:load`, which the spec says gets no report
- Texts that conflict:
  - AC-1.1 (SPEC:195): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `/sc:load` is in section 3.2 and its Report cell is "none (see note)", Resume "n/a", and "use it as a step inside another worker's brief, not as its own Task" (SPEC:112).
  - Decisions (SPEC:265): "a report file would be an unrequested addition".
  - WC-4 (SPEC:62) makes the contract the thing an unattended command writes; P1 scope for load is "usage line only" (SPEC:159).
- Grading sentence: An implementer who follows SPEC:112 and SPEC:265 gives `/sc:load` only a usage-line fix and no contract section, and that implementation fails AC-1.1 at SPEC:195. Following AC-1.1 instead makes the implementer add a contract-naming section to a command the spec says writes no report, which contradicts SPEC:265. Both builds are wrong because the spec says both are right.
- Why blocking: two stated texts contradict, and an acceptance criterion cannot pass under the other text.

#### M1.b, from round1-b.md B1: B1 (CRITICAL, blocking): `/sc:load` is both given no report and required to have one
Experts: Wiegers (traceability), Adzic (testability). Priority High. Quality impact: Testability 3 to 8 once fixed.

Grading sentence: an implementer who follows the stated text as written builds a `/sc:load` that satisfies the section 3.2 row (no report, "usage line only") and then fails AC-1.1; or builds the `## Unattended mode` section naming `return-contract.yaml` that AC-1.1 demands and breaks the row and the Decision. Either way the P1 acceptance check cannot pass without breaking another stated text.

Conflicting texts:
- SPEC:112: load row, Report (WC-4) = "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)".
- SPEC:265: Decision "`/sc:load` handling": "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- SPEC:76 and SPEC:159: every command in 3.2 gets the `## Unattended mode` section and accepts `--unattended` in P1.
- SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Supporting inventory: INV-B:65 (load writes no file; if dispatched it would need a context-summary file).

Recommendation (narrow, no new mechanism): in AC-1.1 and SPEC:76/159, exclude `/sc:load` explicitly (the same way section-4 commands are excluded), or move `/sc:load` into a list of "brief-step only" commands. Delete rather than add.

### M4 (verifier: The claimed outcome (auggie-review or post-release still posts or installs after P1) is a phase-interim state of a phased plan, not a stated result; the text never says P1 ships the flag as live behavior, and the pr-submit/D3 part is the same issue as M5. (M4.a checked))

#### M4.a, from round1-b.md B3: B3 (CRITICAL, blocking): P1 makes `--unattended` accepted by every command, including those whose unattended gate behaviour arrives only in P2 or P4
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

## Follow-up candidates

Listed in the three source reports above; not merged.

## Reviser brief

Blocking finding ids: M2, M3, M5.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
