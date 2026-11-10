review: 2 of 3

# Spec panel report (critique mode, re-review): orca-worker-contract-spec.md

- Roles (fixed by the command line, never inferred): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `5214f80e3dc9557f5cf50e915b26edd24f7757a9ce7975ec766b78482cde7fd6`. BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`. PRIOR = `.dev/orca-command-refactor/review/round1.md`, sha256 `068d3df068f4163a3989d5a7002b1329a9e72de62236926f42f8d41b2cb7bca0`, header `review: 1 of 3` (`round1.md:1`), so this report is review 2 of 3.
- Command line reviewed: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`.
- Citation shorthand: `spec:N` = line N of CANDIDATE; `base:N` = line N of BASELINE; `R1:N` = line N of PRIOR; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.
- Evidence rule: the README, the three inventories, CANDIDATE, BASELINE and PRIOR are the only evidence this review could open. Every source line CANDIDATE cites under `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `~/.claude` or an Orca guide is UNVERIFIED here; where a finding leans on one it is reached through the inventory line that quotes it. The project `.claude/agents/rf-qa.md` and `~/.claude/agents/rf-qa.md` do not exist in this sandbox (`home/.claude` holds only `rules/prompts`), so the re-check of prior blocking findings follows the Review Loop bullet 5 rules, which stand alone.

## Step 1: Evidence block (before any finding)

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` (BASELINE first, CANDIDATE second). Output: `195,196c195,196`, two lines changed, nothing else (the whole diff is those two table rows; no other line differs apart from whitespace).

BEFORE (baseline), verbatim lines starting `<`:

```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
```

AFTER (candidate), verbatim lines starting `>`:

```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (F-01: it gets no contract, section 3.2 row) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
| P1 | AC-1.2 | 7.2 live check on each P1 command except `load` (F-01: no contract, so step 4 cannot apply) with `--unattended --output <dir>` | all steps pass |
```

The BEFORE lines are `base:195-196`; the AFTER lines are `spec:195-196`. The change is a pure narrowing: the exemption `except load` is added to AC-1.1 and AC-1.2, plus a parenthetical that names F-01. No section, flag or rule was added. This matches `review/revise1.md:21` (117 bytes added, 0 deleted; 57763 to 57880 bytes, which matches `wc -c` of the two files).

## Self-check (run before the verdict)

- Each AFTER line (without its `>`) was compared as an exact whole line: found in CANDIDATE at `spec:195` and `spec:196`, not found in BASELINE.
- Each BEFORE line (without its `<`) was compared as an exact whole line: found in BASELINE at `base:195` and `base:196`, not found in CANDIDATE.
- `grep -nF 'except \`load\`'` finds `spec:195` and `spec:196` only. Roles are not swapped. The sha256 of BASELINE equals the candidate sha256 recorded in PRIOR (`R1:5`), which confirms BASELINE is the text that round 1 reviewed.
- Dependency check of the AFTER text: every requirement that depends on AC-1.1/AC-1.2 was read (spec:76, spec:112, spec:139, spec:149, spec:159, spec:183, spec:198-200, spec:265). Result below; no dependent requirement contradicts the AFTER text.

## What this review covered

- Read in full: CANDIDATE (285 lines), BASELINE (diffed and spot-compared), PRIOR (223 lines), `review/revise1.md`, `README.md`, and the `/sc:load` blocks of `INV-B` (`INV-B:31`, `INV-B:57-65`).
- Checked: the diff; each prior blocking finding against the AFTER text only; every line of CANDIDATE that mentions `load` (`spec:11, 112, 139, 149, 159, 195, 196, 265, 268`); the P1 Commands column against AC-1.1/AC-1.2 (`spec:159`); step 4 of the live check (`spec:183`); WC-4 (`spec:62`); the section 3.2 `/sc:load` row (`spec:112`) and the Decisions row (`spec:265`).
- Experts, fixed order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Lead panels under `--focus requirements,architecture`: Wiegers/Adzic/Cockburn and Fowler/Newman/Hohpe/Nygard; Whittaker is active in every panel.
- Not covered: the source files and Orca guides behind the section 3 citations (not openable here); the live repository; `EVIDENCE.md`; git history; the Medium findings F-02 to F-13 and notes N-01 to N-11 of round 1 as such (none sits on a changed line; they are carried unchanged, `R1:204-207`). `--focus correctness` is not active, so no State Variable Registry is produced.

## Prior blocking findings

| Prior id | Prior label | Status | Reason (AFTER text only) |
|---|---|---|---|
| F-01 | CRITICAL | **resolved** | Defect (`R1:89`): AC-1.1 and AC-1.2 demanded a `## Unattended mode` section and a contract file for `/sc:load`, while the `/sc:load` row (`spec:112`: report "none", "use it as a step inside another worker's brief, not as its own Task") and the Decisions row (`spec:265`: "a report file would be an unrequested addition. Only its usage-line defect is fixed") give it neither. AFTER `spec:195` now tests "every command in sections 3.1-3.2 except `load`", and AFTER `spec:196` runs the live check "on each P1 command except `load` ... so step 4 cannot apply". Step 4 is the contract check at `spec:183`, which `load` cannot satisfy because it writes no contract; the exemption removes exactly that case. With `load` excluded, the P1 test and the P1 live check ask nothing of `load` that `spec:112` or `spec:265` withholds, so the two stated texts no longer contradict each other. No other AC or phase row demands a `load` section or contract (`grep -n 'load'` over CANDIDATE: `spec:112, 139, 149, 159, 265, 268` are all consistent with the exemption). Not regressed. |

Count: 1 prior blocking finding; 1 resolved, 0 open, 0 regressed.

## Mandatory artifact 1: Guard Condition Boundary Table (guards on changed lines only)

Triggered: the changed lines add a conditional exemption (`except load`) to a universally quantified test (AC-1.1, `spec:195`) and to a live check (AC-1.2, `spec:196`). In a re-review the table covers guards on changed lines only (Review Loop bullet 5); the guards of round 1 (GC-1 to GC-6, `R1:25-62`) sit on unchanged lines and are not rebuilt. Construction Nygard, completeness Crispin, attack Whittaker. The table is complete before synthesis (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-7 AC-1.1 exemption (`command == load`) | spec:195 | Zero/Empty | the parsed set of section 3.1-3.2 commands is empty (a test that reads zero table rows) | false for every element (none) | the universal assertion passes vacuously; no expected count (36 after the exemption) is stated | GAP (minor, N-14) |
| GC-7 AC-1.1 exemption | spec:195 | One/Minimal | the set is `{load}` only | true | exempt; nothing asserted (inferrable from the clause) | OK |
| GC-7 AC-1.1 exemption | spec:195 | Typical | `analyze` | false | must carry the `## Unattended mode` section naming both strings | OK |
| GC-7 AC-1.1 exemption | spec:195 | Maximum/Overflow | a command added to section 3.1 or 3.2 later | false | covered automatically by "every command in sections 3.1-3.2" | OK |
| GC-7 AC-1.1 exemption | spec:195 | Sentinel Value Match | the sentinel is the name `load`; no other command name in 3.1/3.2 contains it (`spec:81-125`) | exact match only | an exact-name match exempts one command; a substring match would also be harmless here (no collision) | OK |
| GC-7 AC-1.1 exemption | spec:195, spec:139, spec:240 | Legitimate Edge Case | `pr-submit` (a worker candidate only if D3 is accepted) is not exempt | false | must carry the section at P1 although D3 (a) keeps it off the worker list | GAP (inherited from base:195, F-14) |
| GC-8 AC-1.2 exemption (`command == load`) | spec:196 | Zero/Empty | P1 Commands column reduced to `load` only | true | nothing to run; the check passes vacuously | OK |
| GC-8 AC-1.2 exemption | spec:196, spec:159 | One/Minimal | `load` run with `--unattended --output <dir>` | true | exempt; the flag is accepted as a no-op (`spec:159`), no contract is checked | OK |
| GC-8 AC-1.2 exemption | spec:196, spec:183 | Typical | `analyze` | false | steps 1-7 including the contract check at step 4 | OK |
| GC-8 AC-1.2 exemption | spec:196, spec:159 | Maximum/Overflow | the 12 non-`load` P1 commands (13 listed minus `load`) | false | each gets the full 7.2 check | OK |
| GC-8 AC-1.2 exemption | spec:196, spec:159 | Sentinel Value Match | the four "fixes to adversarial, cleanup-audit, index-repo, workflow" entries are P1 commands that are not `load` | false | they carry a contract (WC-4), so step 4 applies | OK |
| GC-8 AC-1.2 exemption | spec:196, spec:112 | Legitimate Edge Case | `load` dispatched as its own Task anyway | true | the row says it should not be; no check is run on it | OK |

FR-8 labels the two GAP rows MAJOR minimum; under Review Loop bullet 2 a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce. GC-7 Zero/Empty names none (a test over zero rows needs an assumption that the implementer writes no row parser) and is graded minor (N-14). GC-7 Legitimate Edge Case is graded Medium (F-14, below). Neither is blocking, so the Status column does not block the verdict. No cell is blank (FR-9).

## Mandatory artifact 2: Quantity Flow Diagram (changed lines only)

Triggered: the changed lines alter a count at a stage of the partition 43 to 10/27/6 to phase sets (`spec:76`).

```text
[Source: 43 commands (INV-A:3 = 21, INV-B:3 = 22)]
   --> [verdict split, spec:76] --> 10 ready + 27 needs change + 6 coordinator-only = 43   (conserved)
   --> [worker-capable = 10 + 27 = 37, sections 3.1-3.2]
   --> [AC-1.1 after the change, spec:195: 37 - load = 36 commands asserted to carry `## Unattended mode`]
   --> [P1 Commands column, spec:159: 13 listed; AC-1.2 after the change, spec:196: 13 - load = 12 live-checked]
         Consumer A: AC-1.1 expects 36  <-- differs from the 12 edited by the P1 Commands column (unchanged divergence, softened by the P1 scope sentence at spec:159; F-14)
         Consumer B: AC-1.2 expects 12  == P1 commands that write a contract (conserved with the contract rule WC-4)
         Consumer C: the `load` row, spec:112 (no contract)  == the exemption in both checks (conserved; this is what F-01 asked for)
```

Divergence at Consumer A is the old 37-versus-13 divergence, now 36-versus-12 (`R1:68-81`). The change did not create it and did not widen it by more than the one removed element; Consumer C, which was the CRITICAL mismatch in round 1, is now conserved. The Consumer A divergence is recorded as F-14 (Medium), not CRITICAL: AC-1.1 asserts a static section and P1 (`spec:159`) states the flag is accepted by all of sections 3.1-3.2, so the two texts do not contradict each other, and the wrong outcome in F-14 depends on decision D3 (open).

## Synthesis (critique mode, findings on lines changed against the baseline)

### === REQUIREMENTS ANALYSIS ===

**F-14** MAJOR label (FR-8 area), graded **Medium**. origin=unchanged (it quotes the changed line `spec:195` but the changed words `except load` neither create nor worsen it). Expert: Wiegers (traceability), Cockburn (actor and goal), attack: Whittaker (Divergence).
- Issue: AFTER `spec:195` still asserts a `## Unattended mode` section on every non-`load` command of sections 3.1-3.2 at the end of P1, including commands whose rows are phased P2, P3 or P4 (for example `pr-submit`, `implement`, `post-release`, `roadmap`, `save`).
- Grading sentence: An implementer who follows AFTER `spec:195` builds, in P1, a `## Unattended mode` section in 36 commands including `pr-submit` (`spec:114`, phase P4), and that is wrong only if D3 option (a) is chosen, because `spec:139` and `spec:240` keep `pr-submit` a worker candidate only if D3 accepts it and recommend "no pr-submit changes"; the stated texts allow either reading, so the grade needs a guess about D3 and about what a section may say before its phase lands.
- Not graded blocking: no wrong outcome follows with no further assumption; round 1 judged the same divergence "Supporting, not needed for the grade" (`R1:90`). The exemption in the AFTER line does not make it worse.
- Recommendation (for a later cycle, not this one): name in AC-1.1 the command set per phase, or say that a P1 section for a P2-P4 command lists "pending, see section 3 row" only.
- Priority: Medium. Quality impact: Consistency +1.

### === ARCHITECTURE ANALYSIS ===

No new architecture finding on a changed line. The exemption does not touch an interface, a boundary or a failure mode: `load` stays a step inside another worker's brief (`spec:112`, `spec:139`), which is the same boundary as before the change.

### === MINOR NOTES (never fail the review)

- N-12 (origin=changed): `spec:76` says "Every changed command also gains the `## Unattended mode` section", and `load` is a changed command (usage line, P1, `spec:112`, `spec:159`). The exemption in AFTER `spec:195-196` therefore sits against `spec:76` for `load`. No wrong outcome: an implementer who adds the section to `load` passes every check (AC-1.1 asserts a section only on non-exempt commands and does not forbid one on `load`), and one who leaves it out matches `spec:112` and `spec:265`. A one-clause exemption in `spec:76` would remove the tension.
- N-13 (origin=changed): the parenthetical `(F-01: ...)` in AFTER `spec:195-196` points to a finding id that is defined only in `review/round1.md`; a reader of the spec alone cannot resolve it. It carries no requirement; the exemption stands without it.
- N-14 (origin=changed, from GC-7 Zero/Empty): AC-1.1 states no expected count of commands tested (36), so a test that parses zero rows passes vacuously. A per-section count assertion would close it.
- Round 1 notes N-01 to N-11 (`R1:178-189`) and Medium findings F-02 to F-13 (`R1:94-175`) remain on unchanged lines, are not re-graded here and carry forward unchanged as follow-up candidates.

## Adversarial analysis (Whittaker, FR-3 format)

1. I can break this specification by **Divergence Attack**. The invariant at **AC-1.1 / the `/sc:load` row (spec:195, spec:112)** was that every command checked has the section and a contract. It held only until `load`; after the change it fails when **`load` is the element tested**, and the exemption now excludes exactly that element. Concrete attack: before the change, 37 commands tested and `load` fails (no section, no contract); after the change, 36 tested, `load` skipped, 0 failures from `load`. Result: the attack no longer succeeds (F-01 resolved).
2. I can break this specification by **Sequence Attack**. The invariant at **P1 / AC-1.1 (spec:159, spec:195)** fails when **P1 is built from its own Commands column (13) and then the test asserts 36 sections**. Concrete attack: the 12 non-`load` listed commands are edited; the other 24 commands have only the accepted flag (`spec:159`); AC-1.1 asserts 36 sections and fails unless the implementer also adds sections to the other 24. Severity: MAJOR label, graded Medium (F-14): the P1 scope sentence plus spec:76 let the implementer add them, so no outcome is wrong with no further assumption. Origin: unchanged (`base:195`).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **the exemption token `load` (spec:195-196)** fails when **another command name contains `load`**. Concrete attack: scan `spec:81-125` for names containing `load`; none exists, so an exact or substring match gives the same 36. Result: no break.
4. I can break this specification by **Zero/Empty Attack**. The invariant at **AC-1.1 (spec:195)** fails when **the test parses zero commands**. Concrete attack: a section parser that matches no table row asserts nothing and passes; before the change 37 was equally unstated. Severity: MINOR (N-14).
5. Accumulation and Divergence attacks on the 36 / 12 counts: no finding beyond F-14.

## Quality metrics (0-10)

Clarity 7, Completeness 6, Testability 6, Consistency 6. Consistency rises from 5 (`R1:202`) because the only CRITICAL contradiction (a check that no stated row can satisfy) is gone. Panel consensus: the repair is minimal, local and correct, and it does not disturb any dependent requirement. Disagreement: none on F-01. Newman and Hohpe (as in round 1) would grade the carried F-10 higher; this review does not re-grade unchanged lines.

## Follow-up candidates (Medium and minor; none fails this review)

Medium: F-14 (new, origin=unchanged); F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13 (carried from round 1, unchanged lines).
Minor: N-12, N-13, N-14 (new); N-01 to N-11 (carried).

## Open blocking findings

None. F-01 is resolved; no new blocking finding was found on a changed line, and no severe defect was newly discovered on an older line.

## Reviser brief

No blocking finding is open, so there is nothing to revise. Binding terms if a later cycle is needed: apply to blocking finding ids only; revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; report the byte size of the specification before and after. Medium and minor findings are not to be fixed in a cycle that has no blocking finding. The reviser reads this report, not the command.

verdict: PASS
