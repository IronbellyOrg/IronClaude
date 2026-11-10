review: 2 of 3

# Spec panel report, round 2 (re-review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md`
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `0686b734a23ad02747840178fa995a98e02d1dad4e7ef5e12322d1cb7ce8879d` (taken with `sha256sum`; equals the hash on `lint-2.md:1`, so the lint ran on this exact file)
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v1.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in `round1.md:7`, so it is the text round 1 reviewed)
- PRIOR: `.dev/orca-command-refactor/review/round1.md`, sha256 `c0cf7ea05947e9d800a2d90f27934360d0c0871a6a594d83987511371562ea47`, header `review: 1 of 3` (`round1.md:1`), so N = 2
- lint: `.dev/orca-command-refactor/review/lint-2.md`, sha256 `b9cb56771d9fe53a713fb203fd0e326d8c7beb8046fe73af54518f28b26b9853`
- reviewer model used: claude-sonnet-5-5
- panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial pass)
- prompt followed: RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:35-49`, read in full; roles per the table at `:40-44`.
- citation convention: `SPEC:N` = line N of the CANDIDATE. `INV`/`CAPS` citations point into `.dev/orca-command-refactor/inventory/`. Anything under `cmd/`, `sk/`, `src/`, `EVIDENCE.md` is outside the workspace: UNVERIFIED.
- baseline: given (no `baseline: missing` note).
- Reviser byte accounting was checked: `wc -c` gives 57763 (baseline) and 58091 (candidate), net +328, which matches `revise1.md:10`.

## Step 1. Evidence block (`diff -w BASELINE CANDIDATE`)

Five changed lines: 76, 154, 159, 195, 196. No other line differs.

BEFORE (baseline), verbatim fragments of the `<` lines:
- 76: `... "Contract" means the WC-4 file ... Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.`
- 154: `... Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4.`
- 159: `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; ...`
- 195: `... the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one`
- 196: `| P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |`

AFTER (candidate), verbatim fragments of the `>` lines:
- 76 (SPEC:76): `A command gains the `## Unattended mode` section (section 2.1) in the phase that resolves its gates, `/sc:load` never (F-1, F-2).`
- 154 (SPEC:154): `... Phase 4 waits for answers to D2-D4. A command gets `--unattended` and its section only in the phase that resolves its gates, and under D3(a) pr-submit gets neither (F-2).`
- 159 (SPEC:159): `the `--unattended` flag and `## Unattended mode` section only for the commands listed here that have no unconverted gate, not for load (F-1) and not for any command a later phase converts (F-2); output flags for commands that lack one; ...`
- 195 (SPEC:195): `the test asserts that every command in the P1 row except load (F-1, F-2) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one`
- 196 (SPEC:196): `7.2 live check on each P1 command except load, which writes no contract (F-1), with `--unattended --output <dir>``

Self-check (commands were run): each of the 5 AFTER lines was found as a whole line in the CANDIDATE (`grep -cxF` = 1 each) and each of the 5 BEFORE lines in the BASELINE (= 1 each). No roles are swapped.

## Prior blocking findings (round1.md:204 lists F-1 and F-2)

| id | status | basis |
|---|---|---|
| F-1 | resolved | The defect was that `/sc:load` writes no report (SPEC:112, SPEC:265) yet AC-1.1 and AC-1.2 required it to have a contract-naming section and a contract. AFTER text: AC-1.1 asserts the section for "every command in the P1 row except load" (SPEC:195); AC-1.2 skips load "which writes no contract" (SPEC:196); SPEC:76 and SPEC:159 name load as the exception. The load row (SPEC:112) and Decision (SPEC:265) are unchanged and now agree with both checks. No stated text requires a contract or section for load. |
| F-2 | resolved | The defect was a P1 flag on commands whose gates convert in P2-P4. AFTER text: SPEC:159 limits the flag and section to P1 commands "that have no unconverted gate ... not for any command a later phase converts"; SPEC:154 states the rule for all phases and says pr-submit gets neither under D3(a). The P1-row commands carry only no-gate cases or P1-resolved refusals (business-panel `--mode socratic`, explain `--format interactive`, test `--watch`, index: SPEC:102, 108, 111, 123). implement, post-release, pr-submit (P4, SPEC:162) and roadmap (P3, SPEC:161) are no longer given the flag early, so the stall described at `round1.md:92` cannot arise from P1. SPEC:240 (D3(a): "no pr-submit changes in Phase 4") now agrees with SPEC:154. |

No prior blocking finding is open or regressed.

## Lint evidence (`lint-2.md`)

- LINT-REF-1 and LINT-REF-2 (`lint-2.md:5-18`): "F-1 / F-2 are referenced but never defined" at SPEC:76. Confirmed as a fact: the ids appear at SPEC:76, 154, 159, 195, 196 and no section of the spec defines them; the spec does not point to `review/round1.md` (`grep -c round1` = 0). Grade check: an implementer who follows the text as written builds exactly the same rules, because every sentence carrying an id is complete without it; the only cost is a reader who cannot look the id up. No concrete wrong outcome, so this is a minor note (N-7), not blocking. The Review Loop (bullet 6) requires the reviser to cite the finding id, so the ids themselves are compliant; the missing pointer is the only gap.

## === REQUIREMENTS ANALYSIS === (changed lines only)

### G-1 [MAJOR, Medium, origin=changed] Ready commands that no phase converts never receive `--unattended`, while SPEC:2.3 requires it in every brief
Expert: Wiegers (lead), Cockburn, Whittaker (Divergence Attack)
Priority: Medium.

Needs a guess about which text wins, so Medium (follow-up candidate), not blocking.

- Before the revision, P1 gave the flag to every command in 3.1 and 3.2 (baseline line 159). After it, SPEC:154 and SPEC:159 give the flag and section only "in the phase that resolves its gates". `brainstorm` and `init-lite` have "None" as their change (SPEC:84, SPEC:87), appear in no phase row (SPEC:158-162), and so never gain the flag or section. `load` is excepted by name (SPEC:76).
- SPEC:73 (2.3, unchanged) says the brief states "the exact command line including `--unattended`" for each Task. SPEC:79 (unchanged) says 3.1 commands run as workers "if the brief uses the stated flags", and the Brief-must-pass column (SPEC:83-91) lists no `--unattended`. SPEC:194 (AC-0.4) likewise runs the P0 smoke commands without it. So two readings exist for a 3.1 or pre-conversion command: pass the flag or omit it. The spec does not say what a command that has not yet gained the flag does with it.
- Grading: the implementer picks between two readings the text allows; no stated text forces the worse one. Medium.

Recommendation: one sentence in SPEC:73 or SPEC:79 that the `--unattended` token is passed only to commands that already document it (and that brainstorm, init-lite and load are dispatched without it). Not for the reviser to apply in this loop.

## === ARCHITECTURE ANALYSIS ===

No architecture finding on the changed lines. The phase ordering still holds: P1 (no-gate) before P2 gates, P3 drift, P4 safety (SPEC:159-162); the rule at SPEC:154 makes the order explicit and removes the Sequence Attack of round 1.

## Origin check on older text that depends on the changed lines

- SPEC:52 ("Each changed command adds a short `## Unattended mode` section") is inherited and now reads against SPEC:76 (load is changed in P1 but exempt). SPEC:76 states the exception, so the reader is not misled. Minor note N-8, origin=unchanged, quotes the changed line SPEC:76.
- SPEC:79 ("The only command changes are the small fixes in the last column") is the round-1 note N-4, still true of the ten ready commands only; origin=unchanged, minor, carried.
- Guard Condition Boundary Table: guards on the changed lines are (1) the P1 flag scope and (2) the load exemption.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| P1 flag scope "no unconverted gate" | SPEC:159 | Typical | analyze (no gate) | true | flag and section added in P1 | OK |
| P1 flag scope | SPEC:159, 195 | Legitimate Edge Case | explain, test, business-panel (refusal resolved in P1, SPEC:102, 108, 123) | true | gets flag in P1; AC-1.1 asserts the section | OK |
| P1 flag scope | SPEC:154, 159 | Zero/Empty | brainstorm / init-lite (no gate, no change, in no phase row) | n/a | not specified; SPEC:73 still says pass `--unattended` | GAP (G-1, Medium) |
| load exemption | SPEC:76, 195, 196 | Sentinel Value Match | load named in P1 row | true | excluded from AC-1.1 and AC-1.2; consistent with SPEC:112 | OK |
| pr-submit under D3(a) | SPEC:154, 240 | Divergence | D3(a) chosen | true | no flag, no section, no P4 edit; consistent | OK |
| pr-submit under D3(b) | SPEC:154, 162 | Divergence | D3(b) chosen | false for "neither" | gets flag and section in P4; AC-4.3 (SPEC:210) applies | OK |

Classes left out: Maximum/Overflow (no capacity exists for a phase membership test).

## Count conservation

Section counts are untouched by the diff: 3.1 has 10 rows (SPEC:83-92), 3.2 has 27 (SPEC:99-125), section 4 has 6 (SPEC:132-137); 10 + 27 + 6 = 43 (SPEC:76). No mismatch.

## What was covered

- Step 1 diff and both self-check greps; hashes; all five changed lines; the phase table SPEC:156-162; section 7 checks that depend on them (SPEC:195-210); the load row (SPEC:112), the load Decision (SPEC:265), D3 (SPEC:238-242), WC-2 (SPEC:60), 2.3 (SPEC:73), 3.1 intro (SPEC:79).
- Not covered: whole-document assurance (this is a scoped review) and every `cmd/` and `sk/` citation (outside the workspace, UNVERIFIED). Round-1 Medium and minor findings F-3 to F-8, N-1 to N-6 sit on unchanged lines and were not re-judged; they remain open follow-ups.
- Newly discovered severe defects older than the diff: none.
- Process note on the reviser (not a finding): `revise1.md:10-20` reports net bytes per id, not bytes added and deleted separately as `round1.md:208` asked, and counts the shared SPEC:76 edit under F-2. The sum matches `wc -c`, so no verdict effect.

coverage: scoped PASS: changed lines + prior blockers

## follow-up candidates

Medium (warnings; none changes the verdict):
- G-1 `--unattended` never reaches brainstorm / init-lite while SPEC:73 requires it (SPEC:73, 79, 154, 159)
- Carried from round 1, unchanged lines: F-3 (SPEC:172, 147, 158), F-4 (SPEC:62, 83, 92), F-5 (SPEC:176, 149), F-6 (SPEC:114, 241), F-7 (SPEC:68, 114, 210), F-8 (SPEC:62, 87, 90)

Minor notes:
- N-7 F-1 / F-2 are cited at SPEC:76, 154, 159, 195, 196 but not defined or linked in the spec (LINT-REF-1, LINT-REF-2)
- N-8 SPEC:52 "each changed command adds the section" vs the load exemption at SPEC:76
- Carried: N-1 to N-6 from round 1 (N-4 still applies to SPEC:79)

The session that ran this review asks the user once per loop whether to open an issue for these follow-up candidates and creates none without an answer. (No answer was available in this run, so no issue is created.)

## Reviser brief

None needed: no blocking finding is open (the brief lists only blocking ids, and there are none).

verdict: PASS
