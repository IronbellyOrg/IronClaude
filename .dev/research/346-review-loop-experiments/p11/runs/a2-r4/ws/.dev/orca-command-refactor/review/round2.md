review: 2 of 3

# /sc:spec-panel critique, round 2 (re-review): orca-worker-contract-spec.md

| Field | Value |
|---|---|
| CANDIDATE | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 57927 bytes), sha256 `7d31f7c49bc684b022504fe6730429f5c5b09ff3a76841344026b64dde9565a6` |
| BASELINE | `.dev/orca-command-refactor/specs/history/spec-v1.md` (285 lines, 57763 bytes), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| PRIOR | `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, `round1.md:1`), sha256 `b5201de5670e62364413a32a09d3ddbfb51f24d5018bc38a87264613b06c1d4c` |
| Mode / focus | critique / requirements, architecture; `--re-review` with `--baseline` |
| Input status | complete. README, command definition, PRIOR, BASELINE, CANDIDATE, `review/revise1.md` and the inventories were readable. The baseline sha256 equals the one PRIOR recorded as its candidate (`round1.md:8`), so BASELINE is the text PRIOR reviewed. |
| Candidate edited | no. No revised specification written (re-review skips the Improve step). |

Citation shorthand: `SPEC:N` is CANDIDATE, `BASE:N` is BASELINE, `R1:N` is PRIOR, `INV-B:N` is `inventory/commands-b.md`, `README:N` is `.dev/orca-command-refactor/README.md`. Citations to files outside the README, the inventories and the review/spec files are UNVERIFIED.

## Step 1. Evidence block

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` (BASELINE then CANDIDATE). Result: 4 changed hunks (lines 112, 159, 195, 196; same line numbers on both sides). The diff is not empty.

### BEFORE (baseline)

```text
< | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
< | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

### AFTER (candidate)

```text
> | load | no gate | none | n/a | none: use it as a step inside another worker's brief, not as its own Task; it gets no `## Unattended mode` section, no `--unattended` flag and no contract, so AC-1.1 and AC-1.2 skip it (B-1); separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (B-1) (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (B-1) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
> | P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (B-1) with `--unattended --output <dir>` | all steps pass |
```

### Self-check (commands run)

Each AFTER line (without `>`) was searched with `grep -nF` in CANDIDATE: found at `SPEC:112`, `SPEC:159`, `SPEC:195`, `SPEC:196`, and none of them is also present in BASELINE. Each BEFORE line (without `<`) was searched with `grep -nF` in BASELINE: found at `BASE:112`, `BASE:159`, `BASE:195`, `BASE:196`, and none of them is also present in CANDIDATE. No quote was missing, so the roles are not swapped. Size check: `wc -c` gives 57763 (BASELINE) and 57927 (CANDIDATE), net +164, matching `review/revise1.md:7-18`.

## What I covered

- The four changed hunks above, in full, with the table columns each sits in (`SPEC:112,159,195,196`).
- Every line that depends on them. I grepped CANDIDATE for `load`, `Unattended mode`, `every command`, `every changed`, and the counts 36, 37 and 27. Dependent lines read in full: `SPEC:52` (section 2.1 contract file), `SPEC:76` (section 3 intro), `SPEC:79` (section 3.1 intro), `SPEC:139` (coordinator-side helpers), `SPEC:149` (SA-4), `SPEC:158-159` (P0, P1), `SPEC:176` (AC-C5), `SPEC:178-185` (7.2 live check), `SPEC:190-200` (7.3 per-phase checks), `SPEC:265` (load decision), `SPEC:268` (inventory verdicts).
- The `load` evidence: `INV-B:31,57-65` (no gate, no file written, context only in chat).
- Not covered: all text unrelated to the four hunks. Prior non-blocking findings F-1 to F-9 and N-1 to N-9 were not re-reviewed, because they are Medium or minor and not blocking (`R1:189-202`); the revision touched none of them (`revise1.md:33`). The `.claude/agents/rf-qa.md` file named by Review Loop bullet 5 is absent in this sandbox (`ws/.claude/agents/rf-qa.md` and `home/.claude/agents/rf-qa.md` do not exist), so its steps 1-5 were not read and the rules of Review Loop bullet 5 were applied from the command text alone, which the command says stands alone.

## Re-check of prior blocking findings

PRIOR has one blocking finding, B-1 (`R1:87-93`, `R1:185-187`). Its defect: AC-1.1 and AC-1.2 required a `## Unattended mode` section and a contract for every command in 3.1-3.2, while the `load` row gave `load` no contract. Result: P1 could not pass. The comparison below uses the AFTER text only.

| Prior blocking id | Prior grade | Status | Evidence (AFTER text only) |
|---|---|---|---|
| B-1 | CRITICAL | resolved | `SPEC:195` now asserts the section for "every command in sections 3.1-3.2 except `load` (B-1)", and `SPEC:196` runs the 7.2 live check on "each P1 command except `load` (B-1)". Step 4 of 7.2 (`test -s <contract>`, `SPEC:183`) is therefore never applied to `load`. `SPEC:112` says `load` gets "no `## Unattended mode` section, no `--unattended` flag and no contract, so AC-1.1 and AC-1.2 skip it". `SPEC:159` drops the flag for `load`. `SPEC:265` already said "a report file would be an unrequested addition" and agrees. The four AFTER lines and `SPEC:265` now agree on one outcome for `load`: no section, no flag, no contract, usage-line fix only. An implementer who follows the stated checks builds a P1 that passes. |

Regressed: none. Open: none.

## Findings on changed lines (ignoring whitespace-only changes)

### Guard Condition Boundary Table (changed-line guards only, per Review Loop bullet 5)

The changed lines introduce two guards: GA, the "except `load`" exclusion in AC-1.1 and AC-1.2 (`SPEC:195-196`), and GB, the "except load" flag scope in P1 (`SPEC:159`, `SPEC:112`). Six rows each; no blank cell.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GA AC-1.1/1.2 exclusion | `SPEC:195-196` | Zero/Empty | the excluded set is empty (no command named `load` in 3.1-3.2) | not reachable | `load` is a 3.2 row (`SPEC:112`), so the set has exactly one member | OK |
| GA | `SPEC:195-196` | One/Minimal | exactly `load` | excluded | AC-1.1 asserts no section for it, AC-1.2 runs no live check | OK |
| GA | `SPEC:195-196` | Typical | any other 3.1-3.2 command, for example `analyze` | not excluded | must have the section (AC-1.1) and pass 7.2 (AC-1.2) | OK |
| GA | `SPEC:195-196`; `SPEC:183` | Maximum/Overflow | all 36 non-`load` commands | not excluded | each checked; 7.2 step 4 applies to 36, not 37 | OK |
| GA | `SPEC:195` | Sentinel Value Match | a name that matches `load` as a substring or prefix (`/sc:load` versus a skill whose name contains "load") | exact name `load` | the exclusion is by command name; no other 3.1-3.2 command name contains "load" (the section-3.2 row names at `SPEC:99-124` carry none) | OK |
| GA | `SPEC:195`, `SPEC:112` | Legitimate Edge Case | a later edit gives `load` a `## Unattended mode` section anyway | AC-1.1 still passes | AC-1.1 asserts presence for the other 36 and absence only for section-4 commands; a section in `load` is neither required nor forbidden | OK (see C-1) |
| GB flag scope | `SPEC:159`, `SPEC:112` | Zero/Empty | `/sc:load` with no flags | flag not involved | standalone behavior, unchanged | OK |
| GB | `SPEC:159`, `SPEC:112` | One/Minimal | `/sc:load --unattended` | flag not accepted | what `load` does with a flag it does not define is not stated; the coordinator brief template could still list it | GAP (C-2) |
| GB | `SPEC:159` | Typical | `/sc:analyze x --unattended --output <dir>` | flag accepted | contract written | OK |
| GB | `SPEC:159`, `SPEC:112` | Maximum/Overflow | a coordinator brief template that lists `--unattended` for all 37 worker-capable commands | flag passed to `load` | same gap as the One/Minimal row | GAP (C-2) |
| GB | `SPEC:112` | Sentinel Value Match | `--checkpoint` (the flag this P1 row does add to the Usage line) | accepted | usage-line fix only; the flag is `load`'s own, unrelated to `--unattended` | OK |
| GB | `SPEC:112`, `SPEC:139` | Legitimate Edge Case | `load` dispatched as its own Task (not as a brief step) | worker runs it | `SPEC:112` says "not as its own Task"; no contract is written, so WC-5 maps the run to `--outcome failed` (no report exists); the spec gives that as the expected result for a misuse | OK (note C-2) |

GAP rows carry FR-8 MAJOR minimum; both link to C-2, graded below by the concrete-outcome test.

### Quantity Flow Diagram (changed counts only)

```text
[43 commands]  SPEC:76
   --> [Triage] --> 6 coordinator-only (section 4)           : N=43, M=37
   --> 37 worker-capable = 10 ready (3.1) + 27 needs change (3.2)
        --> [Consumer: AC-1.1, SPEC:195] expects section in 37 - 1 (load) = 36
        --> [Consumer: AC-1.2, SPEC:196] live-checks the P1 commands except load
   --> [Producer: SPEC:112 load row] no section for load      : 36 sections
   --> [Producer: SPEC:52, SPEC:76 "each/every changed command"] read literally:
       load is a changed command (usage-line fix, SPEC:112, SPEC:159) => 37 sections
```

Expected by the consumer: 36. Produced by the specific row: 36. Produced by the general lines read literally: 37. AC-1.1 asserts presence for 36 and absence only for section 4, so both 36 and 37 pass it (C-1).

### Findings

#### C-1. Medium (MAJOR label, not blocking), origin=unchanged, quotes the changed line `SPEC:112`. The general lines say every changed command gains the section; the changed `load` row says `load` does not.

- Experts: Wiegers (traceability), Fowler (count divergence), Crispin.
- Locations: `SPEC:52` ("Each changed command adds a short `## Unattended mode` section"); `SPEC:76` ("Every changed command also gains the `## Unattended mode` section (section 2.1)"); changed line `SPEC:112` ("it gets no `## Unattended mode` section"). `load` is a changed command by its usage-line fix (`SPEC:112`, `SPEC:159`, `SPEC:149`).
- What depends on what: `SPEC:76` and `SPEC:52` depend on the changed `SPEC:112` for their exception. The revision did not add "except load" to them (`revise1.md:37` records this as residual risk).
- Grading check: the sentence "an implementer builds X, and X is wrong" fails without a guess. Under the literal reading of `SPEC:76`, an implementer adds a section to `load.md`. AC-1.1 and AC-1.2 skip `load`, so P1 still passes; the extra section breaks no check, and `SPEC:265` forbids only a report file, not a section. Under the specific-row reading (the row names `load` and gives the reason), no section is added. Both readings end in a passing P1; one leaves a section that the `load` row says should not exist. FR-19 classes a count mismatch CRITICAL, but the mismatch here (36 versus 37) lands on the safe side of the only consumer, which asserts a lower bound, so I do not treat it as a wrong outcome. The coordinator should know this is a judgment call: a literal FR-19 reading would grade it CRITICAL and make this review FAIL.
- Recommendation (follow-up, not part of this revision): add "except `load` (B-1)" to `SPEC:52` and `SPEC:76`. Rationale: removes the 36 versus 37 reading and keeps the general statements true.
- Priority: Medium. Quality impact: Consistency +1.

#### C-2. Medium (MAJOR label, not blocking), origin=changed. `--unattended` passed to `load` has no stated outcome.

- Experts: Whittaker (Zero/Empty, Divergence), Cockburn.
- Locations: changed lines `SPEC:112` ("no `--unattended` flag"), `SPEC:159` ("except load"); the section-4 commands have the same undefined case from the first review (F-1, `R1:57`, `R1:95-101`).
- Concrete attack: before, a coordinator brief template (P0 lists the 3.1 flags, `SPEC:158`) is applied to every worker-capable command and adds `--unattended`. After, `/sc:load <key> --unattended` runs a command that does not define the flag. What the command does with it (ignore, warn, fail) is not stated. Because `SPEC:112` says `load` is used as a step inside another worker's brief, the stated way to use `load` does not pass the flag, so the outcome needs a guess about a coordinator that ignores that advice.
- Grading check: needs that guess, so it is not blocking.
- Recommendation: one sentence in the `load` row saying the flag is ignored or refused. Same sentence class as F-1.
- Priority: Low. Quality impact: Completeness +1.

#### Other changed-line checks, no finding

- `SPEC:112` "Report: none" (was "none (see note)"): the removed note pointed at nothing in BASELINE (`BASE:112`); the new text is consistent with `INV-B:57-65` (no file written).
- `SPEC:159` P1 command list still names `load (usage line only)` while the flag text excludes it: consistent, because the usage-line fix is not the flag.
- AC-1.2 "each P1 command except `load`": the P1 list at `SPEC:159` names `adversarial, cleanup-audit, index-repo, workflow` as ready commands with fixes; they stay in AC-1.2 and AC-1.1 as before. No change for them.
- AC-1.3 and AC-1.4 (`SPEC:197-198`) do not mention `load` and are unaffected.
- `SPEC:149` (SA-4) lists the `load` usage line as a permitted defect fix; unaffected by the revision.

## Expert review (changed behavior and its dependencies)

=== REQUIREMENTS ANALYSIS ===

- Wiegers: B-1 is closed by an exclusion that appears at all four places that mention it (`SPEC:112,159,195,196`), each tagged B-1. Traceability from the finding to the fix is complete. The two general lines (`SPEC:52`, `SPEC:76`) are the only untagged statements of the old rule (C-1).
- Adzic: example check. `load` row + AC-1.1: `/sc:load` has no section and AC-1.1 passes; `/sc:analyze` has the section and AC-1.1 passes; removing the section from `analyze` fails AC-1.1. The test discriminates as intended.
- Cockburn: the actor (coordinator) and goal (a passing P1) are served; `load` is used as a brief step per `SPEC:112` and `SPEC:139`.

=== ARCHITECTURE ANALYSIS ===

- Fowler: interface consistency between the contract-file rule (`SPEC:52`), the per-command table (`SPEC:112`) and the acceptance tests (`SPEC:195-196`) now holds for the tests and the table. The remaining gap is the prose in `SPEC:52` and `SPEC:76` (C-1). Count divergence is 43 to 37 to 36, each step explained.
- Newman: no new versioning impact; the change adds no field or interface.
- Hohpe: no message-flow change. WC-5's "no report exists maps to failed" still covers the misuse of dispatching `load` as its own Task (GB last row).
- Nygard: no new failure mode. The exclusion lowers the number of live checks, not the safety checks.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

1. I can break this specification by **Divergence Attack**. The invariant at **AC-1.1 versus `SPEC:76`** fails when **an implementer reads "every changed command" literally for `load`**. Concrete attack: before, `load.md` has no section (per `SPEC:112`); after the implementer adds one per `SPEC:76`, the count is 37 sections against 36 expected; AC-1.1 still passes because it asserts presence for 36 and absence only for section 4. Severity: MAJOR label, Medium (C-1).
2. I can break this specification by **Zero/Empty Attack**. The invariant at **`SPEC:159` (flag scope except load)** fails when **`--unattended` is passed to `load`**. Concrete attack: the brief template adds the flag to every worker-capable command; `load` has no such flag and no stated reaction; the outcome is undefined. Severity: MAJOR label, Medium (C-2).
3. Sequence, Sentinel Collision and Accumulation attacks on the changed lines: no attack found. The exclusion is by exact command name, applies to one command, and the count it changes (37 to 36) is the same in the table, the tests and the diagram.

## Quality assessment (0 to 10, changed scope)

Clarity 8, Completeness 7, Testability 8, Consistency 7. Testability and Consistency rose against round 1 (6 and 6) because AC-1.1 and AC-1.2 now agree with the `load` row. The remaining deduction is C-1.

## Follow-up candidates (Medium and minor; none fails this review)

Medium: C-1 (`SPEC:52` and `SPEC:76` need "except load"); C-2 (`--unattended` passed to `load`). Carried over unchanged from round 1 and not re-graded here: F-1 to F-9 (`R1:191`). Minor notes N-1 to N-9 (`R1:193-202`) remain as written in PRIOR; the revision touched none of those lines.

## Consensus and disagreements

- Consensus: B-1 is resolved by the exclusion; no prior blocking finding is open or regressed.
- Disagreement flagged for the coordinator: C-1 is graded Medium because the only consumer of the count (AC-1.1) tolerates 37; a reader who applies FR-19 literally (any count mismatch is CRITICAL) would grade it blocking and fail this review. I followed the concrete-outcome test of Review Loop bullet 2.

## Blocking findings (open)

None.

## Reviser brief

Blocking finding ids: none. No revision is needed for this review.
- Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- The reviser reports the byte size before and after.
- C-1, C-2, F-1 to F-9 and N-1 to N-9 are follow-up candidates and are not part of any revision unless the coordinator chooses to fix them outside this loop.

verdict: PASS
