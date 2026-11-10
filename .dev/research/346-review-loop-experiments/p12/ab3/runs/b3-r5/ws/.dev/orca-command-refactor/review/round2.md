review: 2 of 3

# /sc:spec-panel re-review: orca-worker-contract-spec.md

## Header

| Item | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| Prompt followed | RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full): roles, Step 1, review number, self-check |
| CANDIDATE (revised text under review) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, 57939 bytes, sha256 `a836576df87b59b039072268c20705696ba11a57c7fd7ec19d1e677d12268487` |
| BASELINE (text before the revision) | `.dev/orca-command-refactor/specs/history/spec-v1.md`, 285 lines, 57763 bytes, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| PRIOR (previous review report) | `.dev/orca-command-refactor/review/round1.md`, 200 lines, sha256 `be1daedd60ab891f4402652703eee50c821f4d9bd26507a6a142dd3d6ce5f7bd`; its header is `review: 1 of 3`, so N = 2 |
| Baseline check | The baseline hash equals the "Candidate sha256" recorded in the prior report (`round1.md:12`), so the baseline is the exact text round 1 reviewed |
| Reviewer model | claude-sonnet-5-5 (Sonnet 5.5) |
| Mode | critique, one review. `--iterations` ignored, Improve step skipped, no revised specification written (CMD:261) |
| Brief clauses overridden | none |
| Citation keys | `S:N` = line N of the CANDIDATE; `B:N` = line N of the BASELINE (both files have 285 lines and the diff changes no line number); `INV-A:N`, `INV-B:N`, `CAPS:N` = the inventory files under `.dev/orca-command-refactor/inventory/`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = `command.md`. A citation to a file outside the workspace (`src/superclaude/...`, `CLAUDE.md`, `EVIDENCE.md`) is UNVERIFIED unless a workspace line quotes it. |
| rf-qa.md | `.claude/agents/rf-qa.md` (project) and `~/.claude/agents/rf-qa.md` are not present in the sandbox, so the re-check follows the rules of CMD:262 alone, which stand alone when that file is unread |

## Step 1: evidence block (before any finding)

Command run: `diff -w BASELINE CANDIDATE`. Two hunks (`159c159`, `195c195`), no other change; whitespace-only differences are ignored. Lines copied verbatim.

### Hunk 1, line 159 (section 6, row P1)

BEFORE (baseline):

```text
< | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

AFTER (candidate):

```text
> | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command named in this row's Commands column (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. Each later phase adds the flag and the section for its own commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

### Hunk 2, line 195 (AC-1.1)

BEFORE (baseline):

```text
< | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
```

AFTER (candidate):

```text
> | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command named in the P1 row of section 6, except load (it writes no report), has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one; commands of Phases 2-4 are not asserted here | passes |
```

Self-check (run): each AFTER line, with its `> ` removed, was found whole in the CANDIDATE at lines 159 and 195 (`grep -nFxf`); each BEFORE line, with its `< ` removed, was found whole in the BASELINE at lines 159 and 195; neither AFTER line occurs in the BASELINE (count 0). Roles are correct.

Size change (measured, `wc -c`): 57763 to 57939 bytes, +176 net. The reviser's own per-finding byte report was not read; it is not an input of this brief.

## What was covered

- Read in full: the CANDIDATE (S:1-285), the BASELINE, the PRIOR report (round1.md:1-200), the README, the loop prompts file and CMD.
- Re-checked the one prior blocking finding against the AFTER text only.
- Checked the changed lines against: the Phase column of section 3.1 (S:83-92) and 3.2 (S:99-125); section 4 (S:130-137); S:73, S:76, S:79, S:154, S:162, S:196-210; the counts in the Quantity Flow Diagram below. Inventory citations on the changed lines: none are added, so there is nothing new to verify there.
- Dependencies of the changed lines: AC-1.2 (S:196), AC-2.1 (S:199), S:79, S:112.
- Not covered: whole-document assurance. Lines the diff did not touch were not re-reviewed (CMD:262: a scoped PASS is not whole-document assurance). Every `src/superclaude/...` line number remains UNVERIFIED here, as in round 1.
- Mandatory artifacts for a re-review (CMD:262): Guard Condition Boundary Table limited to guards on changed lines; Quantity Flow Diagram for the changed count. The State Variable Registry is not produced (`--focus correctness` not requested).

Panel, in review order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower (CMD:103-113). Focus experts: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture (CMD:133,144).

## Prior blocking findings

| Id | Prior status | Re-review status | Basis |
|---|---|---|---|
| F1 | blocking (round1.md:34-44) | **resolved** | See below |

### F1 re-check against the AFTER text

The defect: the P1 flag sentence and AC-1.1 consumed 37 commands (all of sections 3.1 and 3.2) while the Phase column assigns 13 to Phase 1 (9 from 3.2 and 4 ready-command fixes), so AC-1.1 could not pass and, with S:154 ("Later phases do not start until the earlier phase's checks in section 7 pass"), Phases 2-4 would never start (round1.md:41).

- AFTER S:159 limits the flag to "every command named in this row's Commands column". That column is unchanged: analyze, build, business-panel, design, document, explain, index, test, load, adversarial, cleanup-audit, index-repo, workflow = 13. It matches the Phase column exactly: the nine P1 rows of 3.2 (S:99, 101, 102, 106, 107, 108, 111, 112, 123) plus the four 3.1 fixes marked P1 (S:83, 85, 86, 92).
- AFTER S:195 asserts a section for the same set except load (12 commands), and says Phase 2-4 commands are not asserted. The load carve-out agrees with S:112 ("none (see note)" for the report).
- The text no longer asks Phase 1 to touch pr-submit (S:114), implement (S:109) or post-release (S:113), so the conflict with S:154, S:162 and the D3(a) recommendation (S:240) is gone. The AFTER text is consistent with S:76 ("Every changed command also gains the `## Unattended mode` section").
- The new sentence "Each later phase adds the flag and the section for its own commands" is the addition the recommendation asked for (round1.md:43). It is one sentence, and the edit narrowed more than it added.

Status: resolved. Wrong outcome removed: an implementer who follows AFTER S:159 and S:195 builds 12 sections in Phase 1, the test passes, and Phase 2 can start.

## Findings on lines changed against the baseline

Total: 0 blocking, 2 Medium, 2 minor. All four findings are new ids (R2-n); none cites a prior finding.

### === REQUIREMENTS ANALYSIS ===

#### R2-1 Medium, origin=changed: two ready commands have no phase that adds the flag, section or contract

- Experts: Wiegers (traceability), Fowler (count annotation). Priority: Medium.
- Stated texts: AFTER S:159 limits the flag to the Commands column and says "Each later phase adds the flag and the section for its own commands". The Phase columns put brainstorm (S:84, "None") and init-lite (S:87, "None") in no phase, and no row of section 6 names either (S:158-162). S:79 says "the worker reports the named file until Phase 1 adds the contract". The BEFORE text covered both through "every command in sections 3.1 and 3.2", so the narrowing removed their only owner.
- Why Medium: both commands still run as workers today with the S:84 and S:87 brief flags, and brainstorm already writes `<output>/return-contract.yaml` (S:84). The harm needs a guess that the coordinator must put `--unattended` in their brief (S:73) or that init-lite must write a WC-4 contract. S:79 says Phase 1 adds the contract for ready commands; for init-lite nothing does.
- Recommendation: state in S:84 and S:87 that no phase changes them and that they report the named file, or name the phase that adds their section. Delete rather than add where possible.
- Quality impact: Completeness 6/10 for the rollout table.

#### R2-2 Medium, origin=unchanged (older defect, found now): AC-1.2 applies the live check to load, which AC-1.1 says writes no report

- Experts: Adzic, Crispin. Priority: Medium. Where it came from: present in the BASELINE (B:196, identical to S:196); round 1 did not report it. It depends on the changed line S:195, which now states that load "writes no report".
- Stated texts: S:196 (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass". Load is a P1 command (S:112, S:159). Section 7.2 steps 3 and 4 require the WC-4 contract (S:182-183), and S:112 says load is "not its own Task".
- Why Medium, not blocking: S:112 itself says load is not dispatched as its own Task, so an implementer has a stated text that excludes it from 7.2, which creates one Task per command (S:180). The reading that includes load needs a guess that the implementer ignores S:112.
- Recommendation: add "except load" to S:196, the same carve-out S:195 now has.

### === ARCHITECTURE ANALYSIS ===

No architecture finding on the changed lines. Fowler and Newman checked that the new S:159 sentence adds no mechanism and no Orca reference (SA-2 and AC-C1 are unaffected: the diff adds no `orca` command string).

### Minor notes (never fail the review)

- R2-3 minor, origin=changed (Wiegers): S:159 says the flag is accepted by "every command named in this row's Commands column", which includes load ("usage line only"). A flag on load conflicts with S:112 ("none") but is harmless: S:159 itself says "a no-op where a command has no gate", and S:195 and S:112 exclude load from the section and the report.
- R2-4 minor, origin=changed (Gregory): the new sentence "Each later phase adds the flag and the section for its own commands" has no matching acceptance check for Phases 2-4 (AC-2.1 asserts per gate, S:199; AC-3.1 and AC-4.x assert other things). S:195 says only that Phases 2-4 "are not asserted here". The requirement is stated without a test.

Older Medium and minor items of the round 1 report sit on lines the diff did not touch. They are neither re-graded nor re-opened. One touches the changed text indirectly: the round 1 note that section 2.3 (S:73) tells the coordinator to pass `--unattended` before a command accepts it is unchanged; the new S:159 sentence ("Each later phase adds the flag ...") is consistent with the recommended wording but does not remove it. Origin=unchanged, minor note.

## Guard Condition Boundary Table (guards on changed lines only, CMD:262)

Guards: GA = the assertion set "every command named in the P1 row of section 6, except load" (S:195); GB = the flag set "every command named in this row's Commands column" (S:159).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GA assertion set | S:195 | Typical | analyze (P1, section 3.2) | true | section required, asserted | OK |
| GA assertion set | S:195 | Legitimate Edge Case | adversarial (named only under "fixes to") | true | section required; consistent with S:76 and the 3.1 phase tag (S:83) | OK |
| GA assertion set | S:195 | Sentinel Value Match | load (the named exception) | false | excluded, reason given; S:196 (AC-1.2) does not carry the exception | GAP (R2-2) |
| GA assertion set | S:195 | Legitimate Edge Case | pr-submit, implement, post-release (Phase 4) | false | "Phases 2-4 are not asserted here" | OK |
| GA assertion set | S:195 | Legitimate Edge Case | brainstorm, init-lite (ready, no phase) | false | named in no row; no phase adds a section | GAP (R2-1) |
| GB flag set | S:159 | Typical | build | true | flag accepted | OK |
| GB flag set | S:159 | Legitimate Edge Case | load ("usage line only") | true | flag accepted as a no-op; S:112 says "none" | GAP (R2-3, minor) |
| GB flag set | S:159 | Legitimate Edge Case | tdd (3.1, tagged P2) | false | flag added by Phase 2 under the new sentence; no check asserts it | GAP (R2-4, minor) |

Omitted classes: Zero/Empty and Maximum cannot occur (the set is a fixed list of named commands, not a count or input); One/Minimal is the Typical case. All cells are populated. GAP entries R2-1 and R2-2 are graded Medium (no concrete wrong outcome without a guess); R2-3 and R2-4 are minor.

## Quantity Flow Diagram (changed count)

```text
[Source: 43 commands (INV-A 21 + INV-B 22)]
   --> ready 10 | needs-change 27 | coordinator-only 6 (S:76)
   --> [Flag + section + contract owner, after the revision]
        P1  13 named (9 from S:3.2 + 4 ready fixes)  --> AC-1.1 asserts 12 (load excluded)      [match]
        P2  15 named (11 from S:3.2 + reflect, release-split, tdd, troubleshoot)  --> no AC-1.1 assertion (stated)
        P3   4 named (roadmap, save, validate-roadmap, validate-tests)
        P4   3 named (implement, post-release, pr-submit)
        none 2 ready commands (brainstorm, init-lite)                                           <-- R2-1
        13 + 15 + 4 + 3 + 2 = 37 (10 ready + 27 needs-change), conserved; 6 coordinator-only get nothing (S:128)
   --> [AC-1.1 consumer] expects 12 of 13 P1 names; before the revision it expected 37        <-- F1 mismatch closed
```

## Adversarial analysis (Whittaker)

- Divergence Attack on S:159 and S:195: the invariant "the assertion set equals the P1 work set" now holds (12 of 13, load excluded and the exclusion stated). It fails only for the AC-1.2 consumer (R2-2): load is in the P1 work set, so AC-1.2 asks for a contract load never writes. Concrete attack: before = 9 section-3.2 P1 rows; AC-1.1 counts 12; AC-1.2 counts 13 and load fails step 4 if S:112 is ignored.
- Sequence Attack on S:154 with the new S:159 sentence: Phase 2 starts after Phase 1 passes; the sentence tells Phase 2 to add its own sections, so the order is stated and no step can be skipped. No finding.
- Zero/Empty Attack on the Phase column: two ready commands map to no phase (R2-1). Sentinel Collision, Accumulation: no attack on the changed lines.

## Follow-up candidates (Medium and minor; none triggers a revision)

R2-1, R2-2, R2-3, R2-4, plus the unchanged older Medium and minor items of the round 1 report (kept on its follow-up list, not re-opened here). The session that ran the review asks the user once per loop whether to open an issue for them (CMD:260); this worker cannot ask, so none was created.

## Coverage

scoped PASS: changed lines + prior blockers

This is not whole-document assurance. A whole-document check needs a separate first review, the gate review (CMD:262; loop prompts file, GATE prompt).

## Reviser brief

Blocking finding ids: none. No revision is requested; Medium and minor findings never enter the Reviser brief (CMD:259,263).

Rules for any reviser, restated from CMD:263 (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on every addition; prefer deleting or narrowing to adding; report byte size before and after, and bytes added and deleted per finding id.

verdict: PASS
