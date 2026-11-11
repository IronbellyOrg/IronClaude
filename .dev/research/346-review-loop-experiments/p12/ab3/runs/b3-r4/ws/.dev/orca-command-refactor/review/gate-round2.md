review: 2 of 3

# Gate-loop re-review: orca-worker-contract-spec.md (`/sc:spec-panel --mode critique --focus requirements,architecture --re-review`)

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `79f7d923a8aec892c0aa73658332d8e091d8ce46bc45e64a342ab24dea176c15` (58669 bytes)
- baseline: `.dev/orca-command-refactor/specs/history/spec-g.md`, sha256 `fd9020aeb88b0fd3aa673b34de70465e3d6d2d18a0ec0245de39c5d2383e536b` (58573 bytes). This hash equals the candidate hash recorded in the prior report (`gate.md:7`), so the baseline is the text the gate review judged.
- prior report: `.dev/orca-command-refactor/review/gate.md`, sha256 `4b8c07f2f7967739d2a603694e033f070830fbc43c4d2403afc626310ce58ad6`, header `review: 1 of 3` (`gate.md:1`), final line `verdict: FAIL` (`gate.md:140`). N = 1 + 1 = 2.
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- mode / focus: critique; requirements, architecture. `--iterations` ignored and the Improve step skipped (re-review). No revised specification written.
- prompt followed: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Roles fixed by the table there: CANDIDATE = the `@file`, BASELINE = `--baseline`, PRIOR = `--re-review`. This is the re-review of the gate loop (gate.md was a GATE review; one REVISE pass, `revise-gate.md`, then this re-review). It is the last review of the gate loop; no further review follows it.
- brief clauses overridden: none.
- Citation shorthand: `SPEC:N` = line N of the candidate; `BASE:N` = line N of the baseline; `GATE:N` = `review/gate.md`; `REV:N` = `review/revise-gate.md`; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.
- Evidence limit: only the README, the three inventories, the candidate, the baseline and the review files are checkable here. Every `src/`, `CLAUDE.md`, `tests/`, `.dev/codegraph-migration/` and Orca-file citation is UNVERIFIED by me; where an inventory quotes it, I checked the quote only.

## Prior blocking findings
| id | prior state | now | reason (AFTER text only) |
|---|---|---|---|
| BLK-1 | blocking (CRITICAL): `/sc:load` required both to gain and not to gain an Unattended mode; AC-1.1 could not pass for load | resolved | Four changed lines make load an explicit exception. SPEC:76 "Every changed command except load (section 6) also gains the `## Unattended mode` section"; SPEC:154 "brainstorm, init-lite and load (usage-line fix only) gain neither"; SPEC:195 positive set "except load" and negative set "load, no command of a later phase and no section-4 command has one"; SPEC:196 "each P1 command except load". These now agree with SPEC:112 (load: report "none (see note)", resume "n/a", P1 usage line only) and with the Decisions row SPEC:265 ("a report file would be an unrequested addition"). The P1 gate can pass without a contract for load, which writes no file (INV-B:62-65, as cited at GATE:33). |
| BLK-2 | blocking (CRITICAL): WC-4 and the adversarial row named two contract paths for one flag value | resolved | SPEC:83 now reads "Fix the contract path to `<output>/return-contract.yaml`, the WC-4 path (P1)"; WC-4 (SPEC:62) says `<output-dir>/return-contract.yaml` with `<output-dir>` the directory passed as `--output`; the brief template (SPEC:73) promises the output directory before dispatch. The two texts name the same file. AC-1.4 (SPEC:198) now requires "`<output>/return-contract.yaml` and no other path", so AC-1.2 steps 3 and 4 (SPEC:182-183) check one path for adversarial. The skill's artifacts stay under `<output>/adversarial/` (INV-A:35); only the contract file sits one level up, which does not conflict with any stated text. |

Count: 2 prior blocking findings, 2 resolved, 0 open, 0 regressed.

## Step 1: evidence block
Roles as above. Command run: `diff -w BASELINE CANDIDATE` (spec-g.md against orca-worker-contract-spec.md). Whitespace-only changes ignored. Five hunks, all quoted verbatim below.

BEFORE (baseline) lines (`<`):
- BASE:76 `... Every changed command also gains the `## Unattended mode` section (section 2.1), in the phase its row names and not earlier (F-1). Phase numbers refer to section 6.`
- BASE:83 `| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1) | ... |`
- BASE:154 `... brainstorm and init-lite have no small fix and gain neither; a P4 command that D2-D4 leave unchanged (pr-submit under D3 (a)) gains neither.`
- BASE:195 `... every command of the phases up to the one under test (P1 here) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no command of a later phase and no section-4 command has one (F-1) | passes |`
- BASE:196 `| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |`
- BASE:198 `... | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |`

AFTER (candidate) lines (`>`):
- SPEC:76 `... Every changed command except load (section 6) also gains the `## Unattended mode` section (section 2.1) ...`
- SPEC:83 `... | Fix the contract path to `<output>/return-contract.yaml`, the WC-4 path (P1) | ... |`
- SPEC:154 `... brainstorm, init-lite and load (usage-line fix only) gain neither; a P4 command that D2-D4 leave unchanged (pr-submit under D3 (a)) gains neither.`
- SPEC:195 `... every command of the phases up to the one under test (P1 here), except load, has a `## Unattended mode` section ... and that load, no command of a later phase and no section-4 command has one (F-1) | passes |`
- SPEC:196 `| P1 | AC-1.2 | 7.2 live check on each P1 command except load with `--unattended --output <dir>` | all steps pass |`
- SPEC:198 `... | adversarial names `<output>/return-contract.yaml` and no other path; workflow states the contract is written for pre-creation STOPs |`

(Lines abbreviated with `...` where the diff line is a long table row; the changed phrase is complete in each quote. The full lines are at the cited line numbers.)

Self-check run: each AFTER line (without `>`) found by `grep -cF` in the candidate: 6 of 6 found. Each BEFORE line (without `<`) found in the baseline: 6 of 6 found, and 0 of 6 found in the candidate. No role swap.

Size: 58573 to 58669 bytes, net +96, matching REV:7. Six lines changed, no section or table added. The reviser's accounting of bytes per finding id is in REV:10-14; I confirmed the total only.

## Coverage
Covered: all six changed lines; the dependencies of each (load in SPEC:112, SPEC:139, SPEC:159, SPEC:265, SPEC:268; adversarial in SPEC:62, SPEC:73, SPEC:83, SPEC:182-183, SPEC:198, and the P0 smoke check AC-0.4); each prior blocking finding against the AFTER text only. Not covered: unchanged text that no changed line or prior blocking finding depends on (the Medium findings of the gate review MED-1 to MED-9 sit there and are left alone by design). Citations to `src/` and Orca files stay UNVERIFIED. Per the Review Loop, FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only.

coverage: scoped PASS: changed lines + prior blockers

=== REQUIREMENTS ANALYSIS ===

No new blocking finding. Notes on changed lines, each graded by the grading sentence.

### MIN-5 (MINOR, origin=changed; Wiegers) - SPEC:159 still lists load in the P1 command column next to a flag rule that SPEC:154 now excepts
- SPEC:159 says P1 adds "the `--unattended` flag, on the P1 commands in the next column only (F-1)"; the next column lists "load (usage line only)". SPEC:154 (changed) says load gains neither the flag nor the section. The two lines can be read together because SPEC:159 writes "(usage line only)" beside load and SPEC:154 names the exception outright, so no implementer builds a wrong outcome from the text as written. Optional wording fix: "on the P1 commands in the next column except load".
- Quoted changed line this depends on: SPEC:154.

### MIN-6 (MINOR, origin=changed; Wiegers) - the adversarial row's contract column still says "filename not fixed"
- SPEC:83 column (c) reads "contract, but filename not fixed" while the fix column now fixes the path. Column (c) describes the state today and the fix column the change, so the row reads correctly; the cell could say "path not fixed today". Note only.
- Quoted changed line this depends on: SPEC:83.

### Recheck of two edge cases the fixes could have opened
- load under 7.2 and AC-1.3: AC-1.2 now excludes load; AC-1.3 (SPEC:197) runs "two P1 commands" and does not name load, so an implementer may pick any two; both outcomes pass. No finding.
- adversarial under WC-4 "known before dispatch" (SPEC:62, SPEC:73): the contract path is now `<output>/return-contract.yaml`, derivable from the brief's `--output`; the promise holds for adversarial. No finding.

=== ARCHITECTURE ANALYSIS ===

No new blocking finding. The fixes narrow the text (a test obligation deleted for load, one path aligned to the shared rule); they add no rule, mechanism or section. This matches the REVISE prompt (`document_review_loop_prompts.md`: add nothing a listed finding does not call for) and the Reviser brief (GATE:132-138). The one shared interface (the contract file at `<output-dir>/return-contract.yaml`) is now uniform for the P1 commands that write one (WC-4, SPEC:84 brainstorm, SPEC:88 reflect, SPEC:83 adversarial).

## Adversarial analysis (Whittaker, on changed lines)
- Sequence attack on the by-phase gate: finish all P1 edits as section 3 says; run AC-1.1 and AC-1.2. State trace: P1 done; load has no section and no contract; AC-1.1 negative set contains load, so it passes; AC-1.2 skips load; P2 may start. The prior dead end (GATE:85) is gone. Attack failed.
- Divergence attack, one flag two paths: `--output D` for adversarial. WC-4 gives `D/return-contract.yaml`; SPEC:83 gives `D/return-contract.yaml`. One path. Attack failed.
- Sentinel collision: "load" in AC-1.1 is now a named exception; a future command also named with load as a substring is not affected because the test names the command. Not a finding.
- Newly discovered severe defect older than the revision: none found in the dependencies I read.

## Guard Condition Boundary Table
Changed lines contain no guard condition, threshold or sentinel comparison. The only conditional is the AC-1.1 membership test (command is load or not), which is a finite enumeration. No guard conditions identified on changed lines; synthesis is not blocked. The Medium GAP rows of the prior table (readiness upper bound, 4.5-minute call, `--monitor 0|2`) sit on unchanged text and are not re-judged here.

Pipeline Dimensional Analysis: not triggered.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium, carried unchanged from GATE (origin=unchanged; none quotes a changed line, so none is regraded and none blocks): MED-1, MED-2, MED-3, MED-4, MED-5, MED-6, MED-7, MED-8, MED-9. Same text, same grading as GATE:48-82.
Minor notes:
- MIN-1 to MIN-4 from GATE:123-126, unchanged.
- MIN-5, MIN-6 above (origin=changed).
- Question for the user (once per loop): whether to open an issue for the follow-up candidates. Not asked here: no user channel in this sandbox and no `--unattended` flag was given, so the coordinator asks. No issue was created.

## Loop status
Gate loop: gate review (`review: 1 of 3`, FAIL), one REVISE pass, this re-review (`review: 2 of 3`, PASS). The gate loop ends here with no further review. Document total so far: the gate loop's reviews are counted within the ceiling of 5 reviews and 3 fix cycles (`document_review_loop_prompts.md`, GATE prompt, Ceiling); this adds no review beyond them.

verdict: PASS
