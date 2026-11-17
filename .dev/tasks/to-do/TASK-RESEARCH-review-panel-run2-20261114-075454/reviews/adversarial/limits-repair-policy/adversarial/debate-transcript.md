# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements; Round 2 sequential rebuttals, A then B) plus Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 85.7%
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2
- Generated: 2026-11-14T16:40:36Z
- Advocate agents: Variant 1 = Proposal A (default model, default persona); Variant 2 = Proposal B (default model, default persona). Each Round 1 statement and Round 2 rebuttal below is the advocate's own file, reproduced unedited (end markers removed); the same files are kept beside this transcript as `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`.
- Debate-point set: diff-analysis.md (S 6, C 14, X 4, U 11, A 6; convergence denominator S+C+X+A with A restricted to the promoted or flagged assumptions A-001, A-003, A-005, A-006 = 28)

## Round 1: Advocate Statements

### Variant 1 Advocate (Proposal A)

# Round 1 advocate statement: Variant 1 (Proposal A), slot C-06 limits-repair-policy

Advocate: advocate for Variant 1 (normalise before the parser). Focus: correctness, risk, test-coverage.
Code state: HEAD 50d4d2b9d, branch `ironbelly/shadow-runs`. Every `file:line` below was read in this session before it was cited. "A" = Variant 1, "B" = Variant 2. Doc-sourced figures (audit-D, E1 tables) are quoted from the two variants and the diff analysis and are marked as such; I did not re-run any replay.

## Position summary

Over-limit lines should be shortened by one deterministic, recorded step inside the shared parsers, before the unchanged validator, because that is the only option that recovers 88 of the 92 measured drops (and 48 of 49 blocking ones) without a model call, without a transport, and on every dispatch path. B is right about three things that A should take: the itemised drop record with a blocking state, a refusal when a PASS rests on a lost blocking line, and a first-parse state kept apart from the repaired state. My position is A's order with those three additions (a hybrid on the residual, not on the main path).

## Steelman of Variant 2

B's strongest version is not "never touch text". It is a provenance and fail-closed argument with two real measurements behind it.

1. **The reviewer's own words stay the only source.** B's section 4.5 shows that normalisation in E2 created a second form of every line that every later check had to know about (design-review finding 2: seal writes raw `p1.md` while the combiner compares normalised lines), and that the ledger stores `report_sha256` of the reviewer's text (`ledger.py:146`, read) while a truncated finding is no longer a byte copy of a line in that hashed report.
2. **The drop becomes visible and the dangerous case is closed.** Today `merge_round` refuses only when no reviewer has a valid block (`ledger.py:150-157`, read) and the only trace of a dropped line is one string with the error count and the first message (`ledger.py:130-134`, read). B's `dropped` record (line, id, rule, field, actual, limit, `blocking_state` true/false/unknown) plus a conservation property (non-blank lines = kept + priors + dropped) plus a `dropped-blocking` refusal with an owner-and-reason acknowledgement exit is a precise, small rule. By B's own reading of `flags.tsv` it would have fired on exactly the 3 merges where a wrong PASS was stored and on none of the 261 others.
3. **B brought the better evidence.** A replay of 5,270 lines from 1,215 committed reports: of 94 over-limit anchor and anchor2 fields, 89 occur verbatim and for all 89 the 200-character prefix occurs once with the same first span; `refs_norm` changes on 0 of 125 lines; plus the E1 re-ask table (5 re-asks, 5 blocks recorded valid afterwards). These narrow the arguments against truncation, and B says so honestly.
4. **A separable incidence lever.** The constants module makes raising the limits a one-line change; 300/450 admits 120 of the 124 length-failing lines unedited.

What B genuinely gets right: the claim field is where the finding's reasoning lives (`document_review_loop_prompts.md:60`), A has measured nothing about meaning, A never names where first-parse state is carried, and A is silent on a lost blocking line.

## Strengths claimed (Variant 1)

1. **Recovery that depends on no unmeasured thing.** The three length reasons are 88 of 92 dropped lines and 48 of 49 blocking (A section 3.1, derived from audit-D reasons 56+18+14 and 24+14+10, arithmetic confirmed by the diff analyst). A pure function has no recovery rate to measure: it either yields a line the real validator accepts or it does not. B's own text concedes the re-ask recovery on gateway models is an unrun measurement (B section 8 point 5, M2) and rests B-core on "5 of 5 in E1, Agent path, n small".
2. **It works on every dispatch path.** A's repair needs no session, no `--resume`, no second prompt. B's re-ask needs a `continue(reviewer, message)` capability per transport and B itself says a transport without it gets "itemise-only plus the fail-closed rule" (B section 3.2). The swarm transport sends one user message and keeps no session (A cites `openai_compat.py:384-388`, B cites the same line), the Tier-1 child runs `--no-session-persistence`, and B excludes headless `--resume` until isolation exists (INV-G, B section 5). On those paths B's recovery is zero.
3. **In the spec loop B's re-ask has no place to run.** `merge_cmd.py:99-116` (read) reads the reports, calls `led.merge_round` once, and saves the ledger; `ledger.py:128` is the only v1 parse (grep `parse_block\(` over `src` returns exactly five hits: `ledger.py:128`, `cluster_cmd.py:151`, `verify_cmd.py:133` and the two definitions). There is no pre-merge validator command, so B's "re-ask before the merge" for 44 reviewer runs needs a new CLI surface, and a re-ask after a partial merge is impossible because `merge_round` demands `n == len(rounds)+1` (`ledger.py:114-118`). A's residual is at most 4 lines (1 blocking), so A can ship with itemisation and refusal for them and a re-ask as an optional later step. B cannot.
4. **It fixes the loss unit in the engine reflect uses.** In v2 one bad line sets `state = invalid` (`findings_v2.py:299-303`, read), and `cluster._members` skips every record whose block is not valid (`cluster.py:256-257`, read). So one over-limit claim costs a reviewer all of its findings. B's own answer for v2 is the re-ask; if it fails or cannot run, the whole reviewer is still skipped, itemised only (B section 3.4). A's test "one over-limit line and one valid line: block `complete`, both findings reach `cluster`" is the direct fix.
5. **The central empirical worry has now been answered in A's favour, by B's own replay.** GQ-017 (does a cut anchor still locate?) was A's biggest open exposure. B's section 4.3 replay gives 89 of 89 verbatim over-limit anchors locating once with the same span, and 0 of 125 `refs_norm` changes. That is stronger than A's synthetic run. It is single-line tasklist rows, so A's 75 percent kill line on code-like corpora stays as the falsifier.
6. **Parser-drift and second-form hazards are avoided by placement.** B cites E2 note D10 (normaliser imports `parse_block` from the worktree and drifts) and then concedes the repair inside the parser removes the drift (B section 4.5). The repair is `repair_line(obj) -> (obj', repairs)`, a pure function called between `json.loads` and the check (`findings.py:164-188`, `findings_v2.py:268-284`, read), so no later check sees a second form: it sees the repaired object, and the stored record keeps the original and kept lengths.
7. **Pins stay literally true.** `parse_block(text, *, repair=False)` with the three production callers passing `repair=True` keeps `test_review_findings.py:113,117` and `test_review_findings_v2.py:200,241` unmodified. I re-ran the grep for over-limit literals (`"x" * 2xx|3xx`) over `tests/review`: the only over-limit pins are those four plus the card_convert claim test at `test_review_card_convert.py:490-501`. This answers C-01 INV-003, which C-01 left HIGH and UNADDRESSED (`core-shape-and-finding-contract/ADJUDICATION-RESULT.md`). B's route to the same answer needs B-raise, which rewrites the pins.
8. **It is the only position with a measurement that can show harm.** A's M2 re-merges the 264 merges with repair on and off and counts merges that turn from PASS to FAIL because a repaired line added a blocking row. B's M1 to M3 test conservation, fire-set and recovery; none counts false-blocker cost.
9. **Limit-agnostic.** The repair works for whatever the constants are. B-raise (300/450) still leaves about 4 of 124 lines failing (B section 3.5) and any fixed limit has a tail; raising the limits relocates the cutoff, it is not a policy for lines beyond it.

## Weaknesses identified in Variant 2

1. **Internal inconsistency in who counts as `complete`.** B says a reviewer with an unresolved dropped line is not `complete` and does not count for clearing (B sections 2, 3.3), and that dropped `blocking: false` lines are "itemised and not re-asked" in the spec loop (B section 3.2). Both are true of the same reviewer: it stays `block_ok` False (`ledger.py:129` sets `block_ok[...] = parsed["ok"]`) with no recovery path, so its `prior resolved` votes and its quorum seat are lost over a length error on a non-blocking line. B counts 44 re-asked runs against audit-D's 80 `block ok false` runs and does not say what happens to the other 36 (diff analysis C-002).
2. **The fail-closed rule is derived, not executed.** B's "fires on 3 of 264 and none of the other 261" comes from the wording of `flags.tsv` (B section 4.2 says so: "derived ... not re-executed"). The `unknown` class (non-boolean `blocking`, bad JSON) is not in `flags.tsv`, so the fire-set is unknown for that class. B's own M1 is the test that would show it, and has not been run.
3. **B-raise is a grammar widening that B itself marks an owner decision, with an undercounted pin cost.** It touches INV-C (HIGH). B counts four boundary pins; if `card_convert.py` imports the shared constants as B section 3.1 requires, `test_review_card_convert.py:500` (`len(f["claim"]) == 300`, read) fails as well, so five (diff analysis C-011 is right). Reviewer behaviour under raised limits is untested (B section 4.6 concedes research/08 point 9). Longer anchors also flow into ledger rows and the merged report.
4. **The E1 recovery evidence is weaker than "5 of 5".** B's own E3 row says reviewer 2 "still had two bad citations" and "3 of 3 (to be confirmed by `review cluster`)", so it is four confirmed and one unconfirmed. Four of the five re-asks were for non-length causes (B's table: `coverage_rows` outside the slice, citation line numbers counted inside the brief), so it is not evidence that a re-ask recovers over-limit lines on long-anchor models (luna 27 of 30 drops were anchors, ember 24 of 33, per B section 4.2).
5. **B's re-ask depends on a record the manifest may refuse.** B section 3.2 reports that in E1 run A2 the re-ask "could not be recorded in the manifest (stage 'collected' already committed; OutOfOrder refused)" and defers the record shape to C-08. That refusal is real code: `manifest.py:371-372` raises `OutOfOrder` when the stage is committed, and `:378-381` raises `Conflict` when the earlier attempt was `complete`. B needs the second attempt on 44 runs; A needs it on at most 4 lines.
6. **The textual argument (X-001) weakens itself.** B's last bullet in 4.5 concedes a code normaliser is deterministic and "bears on where a repair may live, not on a repair written in code". The line B relies on, `SKILL.md:343`, reads: "The orchestrator never edits, remaps or normalizes a reviewer's findings itself: a block that still fails after the one re-ask stays invalid." It is a step of the reflect orchestrator's agent procedure; its last clause is consistent with A (residual lines stay invalid).
7. **B cannot reach the third copy of the limits.** `card_convert.py` truncates claims (`MAX_CLAIM = 300` at `:86`, `text[: MAX_CLAIM - 3] + "..."` at `:200-201`, read) in production-tree code and B keeps it ("a measurement converter") while forbidding truncation elsewhere. That is a split policy inside one package.

## Concessions

1. **`refs` is touched.** A section 1 says the step "touches no field the limits do not name"; section 5 then copies tail-only reference tokens into `refs`. The sentence is wrong as written. Corrected: the step touches `anchor`, `anchor2`, `quote`, `claim`, and `refs` only to preserve tokens a cut would remove. B's 0 of 125 `refs_norm` changes says that rule rarely fires on tasklists; it stays as a cheap guard for other corpora.
2. **"Exact prefix" is true of anchors, anchor2 and quote, not of claim.** The claim is 297 characters plus `...`, matching `card_convert.py:200-201`. The anchor cut has no marker (a marker would break `locate`, `findings.py:276-304`).
3. **The claim cut is the weakest part.** A has not measured whether a cut changes a finding's meaning; B's replay shows 34 claims lose 3 to 135 characters (median 37.5, 9 lose more than 60) and the tails are consequence clauses. A's M1 to M4 do not judge meaning. I add a falsifier: a blind judge over B's 34 claims (10 blocking). If the judge finds that more than a pre-set share of blocking claims change meaning, claims fall back to re-ask first and anchors, anchor2 and quote stay cut.
4. **The first-parse state is not carried (C-013).** `cluster_cmd.py:159` writes `"state": "complete" if block["state"] == "complete" else "invalid"` from the single `parse_block` call at `:151`, so with `repair=True` a repaired card reads `complete`. A's claim that `findings_block_compliance_rate` stays honest was stated for a `repair=False` parse but A named no carrier. Fix: `parse_block` returns `first_pass_ok` and `first_pass_errors` computed before repair, and the card listing emits `block_state` from the first pass plus a `repaired` count. `scripts/reflect_shadow_exit.py:247` then reads first-pass data.
5. **The manifest claim over-generalised (A-006).** A section 2 item 5 says the re-ask "is therefore recorded as attempt 2". That holds only inside an open stage for a reviewer whose earlier attempt was not `complete` (`manifest.py:371-381`), and the manifest is used by `manifest.py`, `manifest_cmd.py` and `__init__.py` only; the v1 `merge` path has no manifest. For v1 the re-ask output is simply the report file passed to `merge`.
6. **A is silent on a lost blocking line (C-004).** A's residual (3 bad severity, 1 bad refs, bad JSON, under-length anchor) can still lose a blocking line, and nothing makes that visible beyond the itemised list. B's refusal is the right net for the residual.
7. **A's "4 of 92" is a v1 audit-D figure** and does not size the v2 residual (X-003). B's E1 table shows non-length causes (coverage rows, citation line numbers) that truncation never touches.
8. **A's re-ask recovery is unmeasured** (GQ-018, Spike 5 not run); B's E1 table is the first recorded evidence in the repository and "unmeasured" in research/02 gap 5 was too strong. It is still n = 5, Agent path, mixed causes.
9. **A's `repair` keyword has a failure mode**: a new caller that omits `repair=True` silently gets today's behaviour. That direction is fail-safe (less repair), but I add a test that every production call site passes the keyword explicitly.

## Per-point positions

| ID | Proposed winner | Reason |
|---|---|---|
| S-001 | Hybrid | A's order (cut, parse, one re-ask, record) on the main path; B's itemised record, blocking state and PASS-by-loss refusal on the residual. |
| S-002 | Hybrid | A's `repair` keyword (keeps four pins literally true) plus B's additive `dropped` classifier record and conservation test; both add keys, neither removes any. |
| S-003 | Variant 2 | B's replay and E1 table are the broader evidence; its results support A's truncation of anchors. |
| S-004 | Hybrid | A's numeric kill line (75 percent of 48 blocking located and unambiguous) plus B's rule-files-before-run discipline and T-B1..T-B5; "close to the other policies" in B has no margin. |
| S-005 | Variant 2 | B's fourteen-row table covers more invariants (INV-F, INV-K, INV-N); A's five rows are a subset. |
| S-006 | Neither | Presentation only. B's "open facts not settled" section is a good practice A should copy. |
| C-001 | Variant 1 | Cut-then-parse recovers 88 of 92 with no model call; a dropped blocking line is itself an edit (A section 7 point 2). Claim carve-out: keep cut, with the M1b meaning judge as falsifier (concession 3). |
| C-002 | Variant 1 | A length-only fault must not make a reviewer non-`complete`; `ledger.py:129`, `cluster.py:221`. B leaves 36 `block ok false` runs with no recovery path (weakness 1). Depends on C-02 and C-03 counting repaired blocks. |
| C-003 | Variant 1 | `cluster.py:256-257` skips the whole reviewer; B's fallback after a failed re-ask is the same skip. |
| C-004 | Hybrid | Adopt B's `dropped-blocking` refusal and acknowledgement exit for residual lines (at most 4 in the study, 1 blocking); A is silent, not opposed. |
| C-005 | Hybrid | A's trigger (only what repair leaves) with B's `blocking_state` gating: re-ask lines that said `true` or `unknown`, itemise `false`. |
| C-006 | Hybrid | A's stateless prompt (no `--resume`, no session surface, avoids E2 finding 7 if the prompt holds only the reviewer's own block); B's requirement that the record exist and that the re-ask runs before the stage commit. Record shape is C-08's. |
| C-007 | Hybrid | B's replay replaces A's synthetic run as the evidence for verbatim single-line anchors; A's kill line stays for multi-line and code anchors where B says its numbers do not transfer. |
| C-008 | Hybrid | Keep A's copy-to-`refs` guard (cheap, tested by `refs_norm(original) == refs_norm(repaired)`); B's 0 of 125 says it rarely fires. Fix A's "touches no other field" sentence. |
| C-009 | Hybrid | Neither has judged meaning. Cut with marker and record, plus the blind-judge falsifier on B's 34 claims; fall back to re-ask for claims if it fails. |
| C-010 | Variant 1 | `repairs` carries field, original and kept lengths; markers on anchors would break `locate`. |
| C-011 | Variant 1 | Raising limits relocates the cutoff (about 4 of 124 still fail at 300/450), widens INV-C (HIGH), is an owner decision, untested on reviewer behaviour, and costs five pins, not four. A works under any constants, so B-raise stays an orthogonal optional lever. |
| C-012 | Hybrid | B is right that the stored finding is not a byte copy; add `original_sha256` of the flattened original field to each `repairs` item (a hash, not text, so INV-H holds) so provenance can be checked against `report_sha256`. |
| C-013 | Variant 2 | A did not name a carrier for first-parse state. Fix is small (`first_pass_ok` in the parse result, first-pass `block_state` in the card listing). |
| C-014 | Hybrid | A's quote prefix works with `verify_cmd.py:68-72` substring test (read); B is right that code lines are not whitespace-flat and neither corpus covers PR code. Per-profile limits are a parameter to the step. |
| X-001 | Variant 1 | The sentence addresses the orchestrator agent; B concedes the code case. It remains a reading, so I state the dependency: if the owner reads it as covering code, one sentence in the Normalize step is amended or the policy moves toward B. |
| X-002 | Hybrid | B is right that E1 holds recorded re-asks; its E3 row shows one unconfirmed and one partly fixed, so no rate exists for gateway models. A's "unmeasured" stands for the path that matters. |
| X-003 | Hybrid | B is right that A's "4 of 92" does not size the v2 residual; A is right that the E1 length-cause re-asks (claims over 300, A1 and the memory note) are exactly what the cut removes. Residual in v2 is non-length causes, for both policies. |
| X-004 | Hybrid | Both hold only if first-parse state is carried; see C-013. |
| U-001 | Variant 1 | The `repair` keyword is the only mechanism found that keeps T1 true and answers C-01 INV-003. |
| U-002 | Variant 1 | Cheap guard, low expected firing rate. |
| U-003 | Variant 1 | Only measurement that can show the policy harmful (false-blocker cost against the cap of 3 reviews). |
| U-004 | Variant 1 | `repaired_lines_rate` exposes briefs that hide the limits; B's brief lever needs the same telemetry to be tested. |
| U-005 | Hybrid | True only inside an open stage and for a non-`complete` earlier attempt (`manifest.py:371-381`); reflect only. |
| U-006 | Variant 2 | Adopt as M1's base population and admission curve. |
| U-007 | Variant 2 | Adopt; also confirms the brief must state the 300 and 200 caps (memory note). |
| U-008 | Variant 2 | Adopt for residual lines; cheap and it closes the PASS-by-loss case. |
| U-009 | Variant 2 | Adopt `blocking_state` and the conservation property (also covers bad `prior` lines). |
| U-010 | Variant 2 | The counter-evidence is real. A's stateless re-ask avoids finding 7 only while the prompt is limited to the reviewer's own block; make that a test (B's T-B5). |
| U-011 | Variant 2 | A separable owner-decision lever, kept out of the default policy. |

## Shared-assumption responses

- **A-001 (audit-D figures are the right base for sizing every policy): QUALIFY.** Both variants use 92/49/44/80, and the diff analysis found audit-D excludes stale and contaminated rows, lacks `merge-stdout.txt` for 45 merges, and mixes lines, runs, triples and merges as units. The base is adequate for ordering the policies (the three length reasons dominate under every count: B's own replay gets 124 length failures against 30 non-length) and not adequate for stating a recovery percentage. A's "88 of 92" is therefore a derived upper bound on lines parsed, which M1 replaces with measured located-and-unambiguous counts.
- **A-002 (a cut anchor still locates, and first occurrence is the right one): ACCEPT, qualified by corpus.** Stated by both; B's replay gives 89 of 89 verbatim anchors with a unique prefix on tasklist rows. It holds for verbatim single-line anchors only; audit-D X2 finds 46 kept rows with null span today, so unlocated anchors exist under any policy, and `annotate` keeps them visibly (`findings.py:346-360`, `anchor_status: missing`).
- **A-003 (reviewer behaviour is stationary): QUALIFY.** It is unstated by both and matters: the decided brief change (CO-8) should shrink the baseline, B-raise would shift it, and research/08 point 9 says raised limits are untested. A's design is the least exposed because the repair is limit-agnostic and any new tail is handled the same way; the exposure that remains is a rising repair rate hiding brief failure, which `repaired_lines_rate` (M4) is there to show. Any sizing of the residual from E2 data should be treated as a baseline, not a forecast.
- **A-004 (`block_ok` semantics from C-02 and C-03 apply): ACCEPT.** Code agrees: `ledger.py:129,150`, `cluster.py:221`. C-002 and C-003 change with those slots, which is why A's position depends on a repaired block counting as `complete` for clearing and quorum.
- **A-005 (shadow mode: no verdict reads the v2 parse result): QUALIFY.** True today. When reflect leaves shadow, `cluster_cmd.py:159-160` card state feeds `clusters_kept`, and `scripts/reflect_shadow_exit.py:247` reads the compliance telemetry. With `repair=True` a repaired card would read `complete` and lift the figure the exit script reads, unless first-pass state is carried (concession 4). The assumption holds only after that fix.
- **A-006 (a second attempt can be recorded and consumed where the block is parsed): REJECT as written.** Code contradicts the unconditional form: `manifest.py:371-372` raises `OutOfOrder` once the stage is committed, `:378-381` raises `Conflict` when the earlier attempt is `complete`, and B's E1 run A2 hit the first refusal. The true form is narrower: the second attempt is recordable before the stage commit and for a non-`complete` first attempt, in the reflect manifest only. For v1 there is no manifest. Under A the exposure is small, because a repaired block is `complete` on the first attempt and only the residual needs a second one; under B it applies to every re-asked block.

### Variant 2 Advocate (Proposal B)

# Round 1 advocate statement: Variant 2 (Proposal B), slot C-06 limits-repair-policy

Advocate: B (never edit reviewer text; itemise every dropped line; one bounded re-ask by the reviewer; refuse a PASS that rests on dropped blocking-or-unknown lines, with a human acknowledgement exit; optionally raise the limits). Focus: correctness, risk, test-coverage.
Code state: HEAD 50d4d2b9d, branch `ironbelly/shadow-runs`, read-only. Tags: [VERIFIED] means I read the file or ran the search in this session; [DOC] means I took it from a variant or research text and did not re-open the source; [UNVERIFIED] means neither.

Code facts I re-read for this statement (so the cites below are mine, not the variants'):

- `src/superclaude/cli/review/ledger.py:127-157`: `merge_round` parses each reviewer with `fnd.parse_block`, sets `block_ok[...] = parsed["ok"]` (`:129`), keeps every parsable finding even from an invalid block (`:135-138`), stores `report_sha256` of the whole report text (`:146`), and refuses only when no reviewer has a valid block (`:150-157`). The only visibility of a drop is one warning string with the error count and the first message (`:130-134`).
- `src/superclaude/cli/review/findings.py:188-195`: an invalid finding line sets `ok` False, appends `{line, msg}` and `continue`s. No repair step exists. `findings.py:175-186` does the same for a bad `prior` line.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md:343`: "Record `findings_block_compliance_rate` here: the cards whose block is valid on this first parse ... before any re-ask. An invalid block gets one bounded re-ask for the block only ... The orchestrator never edits, remaps or normalizes a reviewer's findings itself: a block that still fails after the one re-ask stays invalid."
- `src/superclaude/cli/review/manifest.py:52` (`COMPLETIONS = ("complete", "truncated", "invalid", "failed", "timed_out")`), `:371-372` (`OutOfOrder` when the stage is already committed), `:378-383` (`Conflict` only when the latest attempt is `complete`; otherwise the earlier attempt is marked `superseded_by`).
- `src/superclaude/cli/review/cluster_cmd.py:151-161` and `verify_cmd.py:137`: both read `block["state"]` from one `parse_block` call; the card listing carries a single `block_state`.
- `src/superclaude/rules/prompts/document_review_loop_prompts.md:60`: the only limit the v1 brief states is "12 to 200" for the anchor (grep for `300`, `at most 200`, `12 to 200` in that file returns only that match).
- `grep` for `findings_v2|review\.findings|cli\.review` under `src/superclaude/cli/reflect`: no match. `findings_block_compliance_rate` has no Python computation in `src`; `scripts/reflect_shadow_exit.py:247` only reads it from telemetry, so the first-parse figure is carried by the skill and the orchestrator.
- Pins: `tests/review/test_review_findings.py:113,117`; `tests/review/test_review_findings_v2.py:199-200,241`; `card_convert.py:85-86,199-201`; `tests/review/test_review_card_convert.py:490-501` (`len(f["claim"]) == 300`, endswith `...`).
- `manifest.py` is referenced only by `manifest_cmd.py` and `__init__.py` among the review modules (`grep -l manifest` over `src/superclaude/cli/review/*.py`); `ledger.py`, `findings.py`, `cluster.py` and `cluster_cmd.py` never mention it. The v1 spec loop therefore has no manifest to record a second attempt in.
- E1 notes read: `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboA-r1/panel/notes.md:2` (claims F6/F10 over 300, 3/3 valid after one re-ask), `...comboA-r2/panel/notes.md:4-14` (deterministic parser found the defect the orchestrator's ad-hoc parse missed; re-ask could not be recorded, OutOfOrder), `...comboE-r3/panel/notes.md:2-3` ("3 of 3 (to be confirmed by `review cluster`)").

## 1. Position summary

The shared step must be a classifier plus a per-line record, not a text rewrite: the parser keeps rejecting an over-limit line exactly as today, but every drop is itemised, a reviewer who still has a dropped blocking-or-unknown line is not a `complete` reviewer, and a round whose only blocking evidence was dropped is refused instead of stored as PASS. Truncation can remain at most an optional, separately decided lever; the fail-closed rule is needed under either policy, because truncation cannot reach bad severity, bad refs or bad JSON, and because only B states what happens when a blocking line is lost. I concede that B-core leaves the reflect (v2) loss unit unfixed unless the re-ask or the raise lever works, and that my own E1 recovery evidence is weaker than my variant states.

## 2. Steelman of Variant 1 (Proposal A)

The strongest version of A is not "truncate and hope". It is this: the loss today is real (92 dropped lines, 49 blocking, 3 stored wrong PASSes in audit-D), the dominant cause is length (88 of 92 by reason), and a deterministic, no-model-call step that cuts a field to an exact prefix recovers almost all of it without depending on an unmeasured re-ask. Three parts of A are genuinely strong:

1. The anchor argument. `locate` flattens and searches the flattened document (`findings.py:276-304`, [DOC] re-read by both variants), so an exact prefix of a verbatim anchor locates at the same span. B's own replay confirms it: of 94 over-limit anchor and anchor2 fields, 89 are verbatim and for all 89 the 200-character prefix occurs once at the same first span (B section 4.3). A predicted this and B measured it. That removes the location objection for tasklist-row anchors.
2. The loss-unit argument. In v2 one bad line makes the whole reviewer `invalid` (`cluster.py:221,256-257`, [DOC]; the `if not r["valid"]: continue` at `cluster.py:256-257` is the code I saw adjacent to my read). Repair turns a reviewer-sized loss into a nothing-lost outcome, and the E1 memory note says 4 claims over 300 characters needed re-asks in the shadow runs. A does the cheap thing first and leaves the expensive, unmeasured thing (the re-ask) a residual of about 4 lines.
3. Engineering hygiene. A's `parse_block(text, *, repair=False)` keyword keeps every direct parser pin literally unmodified while production call sites opt in (`ledger.py:128`, `cluster_cmd.py:151`, `verify_cmd.py:133`), which is a real answer to the open C-01 INV-003; A's stateless re-ask (original brief, the reviewer's own block, the parser's per-line errors) needs no `--resume`; A also designs the cost-side measurement (M2: a repaired line may add a blocking row and flip a PASS to FAIL against a cap of 3 reviews), the only measurement in either proposal that can show the policy is harmful.

A is also honest about what it does not know: it labels the 88-of-92 figure a derived upper bound, states the 75 percent kill line before any run, and says in its section 7 point 1 that its reading of `SKILL.md:343` is a reading, not a fact.

## 3. Strengths claimed for Variant 2 (Proposal B)

1. **It is the only variant that answers "what if the blocking line is lost?"** `ledger.py:150-157` refuses only when no reviewer produced a valid block. A merge in which every reviewer's surviving rows are non-blocking, but one reviewer's dropped line said `blocking: true`, goes through as PASS. audit-D shows four such rows in three merges (g3-sonnet-luna-ember-r3, g5-ember2-luna-r2, n5-sonnet-ember; [DOC] re-read by the diff analyst from `flags.tsv`). A says the rule is "compatible with A ... not part of A" (A section 4.1). But it is needed under A too: A's residual (3 bad severity, 1 refs-bad, plus bad JSON and under-length anchors, none reachable by truncation) is exactly the set of lines that fail silently today. A rule that fires only when no blocking row survives after the union, and only when a blocking-or-unknown line was lost, has a small fire set (3 of 264 merges per B section 4.2, derived from `flags.tsv` wording, not executed) and a human exit (acknowledgement with owner and reason, same shape as C-02's `defer`).
2. **It keeps the `SKILL.md:343` contract true for both parsers.** The sentence ends "a block that still fails after the one re-ask stays invalid." Under A a block that fails only on length becomes `ok: True` / `state: complete` with a `repairs` list, which contradicts the last clause for the one class of failure that is most common (audit-D: 88 of 92 by reason). A concedes the sentence "needs one sentence changed" (A section 2 item 7). B needs no amendment to an owner-authored installed rule.
3. **The compliance metric is honest by construction.** `findings_block_compliance_rate` is "valid on this first parse ... before any re-ask" (`SKILL.md:343,988`). Its only machine-side carrier of state is `block["state"]` from one `parse_block` call (`cluster_cmd.py:151,159-160`; `verify_cmd.py:137`). A's `repair=True` at those three call sites makes that state `complete` for a repaired block, and A does not name a second carrier; it says the metric "is computed from a `repair=False` parse" but there is no Python that computes it, only `scripts/reflect_shadow_exit.py:247` reading telemetry. Under B the parse result and the `errors` shape are identical to today, so the first-parse state cannot drift.
4. **No reviewer output is altered, so the stored finding stays a copy of a line in the hashed report.** `ledger.py:146` hashes the whole report text and members come from that text. Under a claim cut with `...`, the stored claim is no longer a substring of any line in the hashed report; for anchors the stored prefix still is. This is a provenance consequence, not a verdict consequence, and I label it a design inference.
5. **It reaches the rules truncation cannot.** B's classifier covers bad severity, bad refs, non-boolean `blocking` (state `unknown`), bad JSON and bad `prior` lines (`findings.py:175-186`), plus a conservation property (non-blank lines of the last block = kept + priors + dropped, T-B1) that is a real test A lacks. A's `dropped` list also exists, but A reads `blocking` from the raw object only "when it is a dict" and has no `unknown` class.
6. **It brings new evidence.** The replay of 5,270 lines from 1,215 committed reports (first failing rule: anchor 64, anchor2 29, claim 31, category 26, severity 3, refs 1) and the E1 re-ask table are real additions; the claim-cut measurement (34 claims lose 3 to 135 characters, median 37.5, 9 lose more than 60) is the only measurement of what the cut removes. I did not re-run the replay; it is [DOC].
7. **The brief is the source of the claim failures.** The v1 loop brief states only "12 to 200" for the anchor and gives the claim as "one sentence naming the wrong outcome" with no limit (`document_review_loop_prompts.md:60`, grep re-run). Generating the limits sentence from the constants (CO-8, decided) removes the cause of the claim drops (14 of 92 by reason in audit-D, 34 of 124 length failures in B's replay) before any policy runs. This benefits both proposals; it also means any rate measured on E2 reviewers overstates the steady state (A-003 below).
8. **B-raise is a lever A does not have, and it is separable.** With anchor and anchor2 at 300 and claim at 450, B's replay admits 120 of the 124 length-failing lines unedited (69 blocking). It is a widening of findings-v1 (owner decision, INV-C) and costs pin rewrites (I count five, see Concessions).

## 4. Weaknesses identified in Variant 1

1. **A's central claim ("88 of 92 recovered; at most 4 residual") is a v1 tasklist derivation, not a measurement, and does not size the reflect residual.** In E1 four of the five re-asks were for non-length causes (coverage rows outside the slice in A2, citation line numbers counted inside the brief in E2 and E3; per B section 4.4, and I re-read A2 and E3 notes). Truncation touches none of them. A's re-ask half is therefore load-bearing in reflect, not a 4-line afterthought, and that half is as unmeasured as B's (A section 3.3: "Recovery is unmeasured").
2. **A's "exact prefix" is not what it ships for claims.** A section 1 says "exact prefix"; A section 2 item 7 and section 7 point 3 say the claim keeps 297 characters plus `...` (same rule as `card_convert.py:199-201`). The stored claim is then not a substring of the report and not a pure prefix. Anchors, anchor2 and quote are cut unmarked, so nothing in the ledger row or the merged report tells a reviser that the anchor it sees is a cut, except the separate `repairs` record that A says is added to the reviewer entry.
3. **`repair=True` at the three production call sites changes what `block_ok` means.** `ledger.py:129` sets `block_ok = parsed["ok"]`; with repair, `ok` is True for a block that violated the grammar. Under C-02 (quorum of distinct `block_ok`-true reviewers typing `prior ... resolved`) and C-03 (completion counts for quorum), a reviewer whose block was never valid now votes to clear and counts toward the floor. A recommends this ("A recommends counting the block", A section 4 INV-I row) and notes the alternative, but the diff analyst's point stands: A raises clearing and quorum power from blocks that broke the contract.
4. **A leaves two sources of truth for first-parse state.** `cluster_cmd.py:151` makes one `parse_block` call and the listing at `:155-162` carries one `state`/`block_state`; `verify_cmd.py:137` also carries one `block_state`. A's "computed from a `repair=False` parse" needs a second parse or a second field at each site; A does not name which.
5. **A's own copy-to-`refs` rule contradicts its own sentence "It touches no field the limits do not name".** A section 5 adds a step that writes tail-only reference tokens into `refs` (cap 8) and records `refs_lost` otherwise. B's replay found 0 of 125 lines changed by truncation on this corpus, so the rule may be dead code here; but it is a field edit, and it means a repaired finding has a different `fp` input than the reviewer wrote.
6. **A stays silent on the fail-closed case.** A section 4.1 says a rule for a residual dropped blocking line is "compatible with A ... not part of A". Without it, 4 residual lines (1 blocking) and every bad-JSON or non-boolean-`blocking` line pass silently, the exact failure the audit-D data shows.
7. **A's re-ask record claim does not apply to the loop where the drops occurred.** A section 2 item 5 says the re-ask "is recorded as attempt 2 and adds no vote" via `manifest.py:378-383`. I confirmed that is correct for the manifest as far as it goes (an `invalid` completion is allowed to be superseded), but (a) `OutOfOrder` fires once the stage is committed (`:371-372`) and E1 run A2 hit exactly that, and (b) `ledger.py` never references the manifest, so the v1 spec loop, the source of every audit-D drop, has no manifest record at all. The record that exists in v1 is the new report file and its `report_sha256` in the ledger entry.
8. **A's kill line (75 percent of 48 blocking length lines located and unambiguous) is a figure A proposed and the owner may change, and the cost-side M2 is run only on the E2 population.** I accept the design; the weakness is that it is not run, so nothing is shown yet, which is symmetric with B.

## 5. Concessions

1. **B-core does not fix the v2 loss unit** (diff point C-003). In the reflect engine one over-limit line still invalidates the whole reviewer (`cluster.py:256-257`) unless the one re-ask succeeds. B's only mitigations there are the re-ask, the brief change (CO-8) and B-raise. This is a real cost and A's "both findings reach `cluster`" test shows A is better on this axis. It is mitigated, not removed, by shadow mode (INV-L: no verdict reads the parse result; I verified `cli/reflect` imports no findings parser).
2. **"5 of 5 re-asked blocks recorded valid" overstates** (X-002). The E3 note says "3 of 3 (to be confirmed by `review cluster`)", and the A2 note shows the orchestrator's ad-hoc parse said 3/3 while the deterministic parser found the defect. At most four of five are tool-confirmed, the evidence is orchestrator-reported on the Agent path, n is 5, and only one of the five was a length failure. It supports "a re-ask can work", not a rate.
3. **B's three-in-264 fire set is derived from `flags.tsv` wording, not executed** (C-004). The `unknown` class (non-boolean `blocking`, bad JSON) is not in that file at all, so B does not know its fire rate. M1 exists to run it. B's audit-D claim "fires on none of the other 261" is therefore a prediction.
4. **B under-handles the up to 36 `block_ok` False runs it does not re-ask** (C-002). audit-D has 80 `block ok false` runs; B re-asks 44 under the spec-loop trigger. A run whose only drops said `blocking: false`, or whose block is invalid for another reason, stays `block_ok` False with no recovery path, so under C-02 its `prior ... resolved` lines do not count. I propose an amendment in the table below (re-ask also when an invalid block carries a `prior` line).
5. **Five pins, not four, if the shared constants are raised** (C-011). If `card_convert.py` imports the shared claim limit (B section 3.1) and the limit becomes 450, `tests/review/test_review_card_convert.py:500` (`len(f["claim"]) == 300`) fails along with the four boundary assertions. The way out is to leave `card_convert.py`'s marked truncation at 300 as a legacy measurement converter, or to rewrite the pin.
6. **B's replay population is not the audit-D population** (A-001): it includes stale and superseded folders, and its single-line table-row anchors do not transfer to multi-line anchors or code hunks. The 89 of 89 prefix-locate result is real for these tasklists and closes GQ-017 only for them. It narrows B's own location arguments, and I withdraw "a cut anchor may bind to a different occurrence" as an argument for B on tasklist documents.
7. **"Meaning of the claim cut" is [UNVERIFIED].** The sampled tails are consequence clauses, but no judge ran. B cannot show a cut changes meaning, and A cannot show it does not (A's M1 to M4 do not judge meaning).
8. **A is better on three design contributions**: the `repair=False` keyword for pin stability (U-001), the cost-side verdict replay M2 (U-003), and the stateless re-ask form (C-005). B should adopt the stateless form as one of its transports and a counterpart of M2 (false-refusal rate and stall count).
9. **A-006 is a hole in B too**: B defers the record shape to C-08 and says only that one must exist. I define the constraint below.
10. **The `SKILL.md:343` textual argument (X-001) is weaker than B states.** The sentence names "the orchestrator", an agent session, and B's own section 4.5 last bullet concedes a deterministic code step differs. B's case against truncation rests on provenance, the first-parse metric and unmeasured claim meaning, not on the sentence alone.

## 6. Per-point positions

Proposed winner is one of Variant 1, Variant 2, Hybrid, Neither. "Hybrid" means a named combination in the reason.

| ID | Proposed winner | Reason |
|---|---|---|
| S-001 | Hybrid | Shared fixed order: classify and itemise, one bounded re-ask, fail closed on a lost blocking-or-unknown line (B); any truncation is an optional lever behind an owner decision, not the default. The itemise and fail-closed pieces are needed under A as well. |
| S-002 | Hybrid | Take B's classifier inside both `parse_block` functions with the additive `dropped` key and the `unknown` blocking state; take A's `repair=False` keyword only if an owner-approved repair exists. Without a repair, no keyword is needed. |
| S-003 | Variant 2 | B adds two bodies of evidence (the 5,270-line replay and the E1 re-ask table) to the audit-D base; both carry population caveats I list in Concessions 6. |
| S-004 | Hybrid | A's pre-stated numeric kill line is better than B's "close to the other policies" with no margin; B's conservation and merge-matrix tests (T-B1 to T-B5) are better than A's list. Adopt both and fix margins before any run. |
| S-005 | Variant 2 | B's 14-row invariant table separated into core and raise columns is more complete; A's `partly endangered` for INV-C is the more candid label for repair. Low severity. |
| S-006 | Neither | Presentation. |
| C-001 | Variant 2 | The fate-of-line question is governed by `SKILL.md:343` and by `ok`/`block_ok` semantics (`ledger.py:129`); B keeps both literally true. If the owner amends the sentence, A becomes viable for anchors only (see C-007) and not for claims (C-009). |
| C-002 | Hybrid | B plus an amendment: in the spec loop, also re-ask any reviewer whose block is invalid and who typed a `prior` line, so no clearing vote is lost silently. A's `block_ok` True after repair raises clearing and quorum power from broken blocks (Weakness 3); I concede B's trigger leaves the other ~36 runs with no path. |
| C-003 | Variant 1 | Repair is better on the v2 loss unit and B-core does not fix it; B-raise and the CO-8 brief change reduce it without editing text. Shadow mode lowers the cost for now. |
| C-004 | Variant 2 | A is silent and needs the rule for its own residual (bad severity, bad refs, bad JSON, non-boolean `blocking`). B's fire set (3 of 264) is derived, not run, and its `unknown` class is unmeasured (M1). |
| C-005 | Hybrid | B's trigger scoping (re-ask on blocking-or-unknown drops, or any invalid block with a `prior` line) with A's stateless prompt as the default transport (own brief, own block, parser errors), `--resume` an optimisation only. |
| C-006 | Hybrid | A-006 is contradicted for both; see the shared-assumption response. A is right that the manifest can hold attempt 2 (`invalid` is a `COMPLETIONS` value, `:52`); B is right that the stage must still be open (`:371-372`). In the v1 loop there is no manifest (`ledger.py` never references it), so the record is the new report and its `report_sha256`. |
| C-007 | Hybrid | Both reach "a prefix locates" for single-line anchors (A by code and a synthetic run, B by replay, 89 of 89). B's evidence is stronger and I withdraw the location argument for tasklist anchors; it does not transfer to code hunks or multi-line anchors, and it supports B-raise (admitting the line unedited) as much as it supports a cut. |
| C-008 | Variant 2 | 0 of 125 changed on this corpus makes A's copy-to-`refs` rule unneeded here; A's sentence "touches no field the limits do not name" is contradicted by the rule it adds. The 124 versus 125 gap is unexplained in B; one plausible reason is a line whose first failing rule is not a length rule but which also has an over-limit field [UNVERIFIED]. |
| C-009 | Variant 2 | The claim carries "X is wrong because Y" (brief, `:60`) and is the field cut with a marker; neither variant measured meaning. B's risk argument stands only as a risk, labelled [UNVERIFIED]. A's "exact prefix" is wrong for claims (297 + `...`). |
| C-010 | Variant 2 | Under B nothing is changed and nothing needs a marker; A marks claims only and leaves cut anchors, anchor2 and quote unmarked. Low severity. |
| C-011 | Hybrid | CO-8 brief generation is common ground. B-raise is an owner decision on a widening of findings-v1; it admits 120 of 124 lines in B's replay and reviewer reaction is untested. Keep it separate, run M3, and adopt the five-pin count. |
| C-012 | Variant 2 | The ledger hashes whole reports (`ledger.py:146`); a cut claim with `...` is not a line of the hashed text. This is an inference; A's answer (derived copy plus `repairs` record) is acceptable for anchors. |
| C-013 | Variant 2 | B leaves `parse_block`'s result and `errors` shape identical, so the first-parse state is unchanged; A needs a second carrier at `cluster_cmd.py:151,159-160` and `verify_cmd.py:137`, and does not name it. |
| C-014 | Hybrid | Both keep `verify-citations` workable: A by a quote prefix (substring test at `verify_cmd.py:68-72`, [DOC], not re-read by me), B by re-ask or a higher quote limit. B's limit applies where code lines exceed 200 characters; neither is measured on PR code. The PR path is the in-session main session, so the stateless re-ask is the usable transport. |
| X-001 | Variant 2 | On the text as written the last clause ("stays invalid") fits B and requires amendment under A; the "agent versus code" reading is A's reasonable reading and B concedes a code step differs. This is an owner call; whichever way it goes, record it before the policy is built. |
| X-002 | Neither | Both are unmeasured. B overstated "5 of 5" (four tool-confirmed at most, orchestrator-reported) and A is right that no rate exists. The two policies are equally dependent on M2/M3. |
| X-003 | Variant 2 | A's "4 of 92" is a v1 tasklist derived figure; E1 non-length causes (4 of 5 re-asks) show the re-ask is load-bearing in reflect no matter how truncation performs. |
| X-004 | Hybrid | Both claims hold only if first-parse state is carried separately. B yields it by construction; A must add it. Require the separate state under either policy. |
| U-001 | Variant 1 | The keyword reconciles INV-003 for any repair. Cost: a caller that omits `repair=True` silently gets today's behaviour. Not needed under B-core. |
| U-002 | Variant 1 | Real finding about `refs_norm`; B's replay says it does not bite on tasklist rows. |
| U-003 | Variant 1 | The cost-side measurement is the best measurement design in either proposal. B needs a counterpart (false-refusal rate and stall count of the `dropped-blocking` refusal). |
| U-004 | Variant 1 | A repaired-lines rate is useful; B should report a `dropped_lines_rate` per model for the same reason (a rising rate means the brief fails to state limits). |
| U-005 | Variant 1 | Verified: attempt 2 is allowed only while the stage is open and the earlier attempt was not `complete` (`manifest.py:371-383`); `invalid` is an allowed completion (`:52`). |
| U-006 | Variant 2 | Largest new evidence; population caveat stands. |
| U-007 | Variant 2 | First recorded re-ask evidence in the repository; I restate it as "four confirmed, one unconfirmed, orchestrator-reported". |
| U-008 | Variant 2 | The `dropped-blocking` refusal with an acknowledgement exit is the only proposed rule for PASS by loss; its fire set is derived, not run. |
| U-009 | Variant 2 | `unknown` blocking state and the conservation property cover the `prior`-line case and non-boolean `blocking`. |
| U-010 | Variant 2 | E2 design-review findings 2, 4, 7 and the A2 transcription corruptions are evidence about agent-run normalisers and session surfaces ([DOC]); A's stateless prompt avoids finding 7 only if it stays limited to the reviewer's own block. |
| U-011 | Variant 2 | B-raise as a separable lever with its pin cost stated; see C-011 for the five-pin correction. |
| A-001 | see below | QUALIFY |
| A-002 | see below | QUALIFY |
| A-003 | see below | REJECT |
| A-004 | see below | ACCEPT |
| A-005 | see below | QUALIFY |
| A-006 | see below | QUALIFY |

## 7. Shared-assumption responses

**A-001 (the audit-D figures are the right base for sizing every policy): QUALIFY.** The 56/18/14/3/1 split and the 49 blocking rows are as both state, and I checked neither against the files myself (I rely on the diff analyst's re-read of `summary.md` and `flags.tsv` at `6c0984326`). But the base excludes batch-10, contaminated, superseded and quarantine rows, includes stale reports (16 merges flagged EXCLUDE), has 45 merges without `merge-stdout.txt`, and mixes units (lines, runs, triples, merges). B's own replay is on a different population (154 invalid, 124 length-failing). Use the audit-D numbers as an order of magnitude and re-derive the fire set in M1 on one frozen population before any rule is chosen on them. This applies to my "3 of 264" and to A's "4 of 92" equally.

**A-002 (a cut anchor still locates and the first occurrence is the right one; optional response): QUALIFY.** True for verbatim single-line anchors in these tasklist documents (B's 89 of 89), unmeasured for multi-line anchors and code. `anchor_ambiguous` is read by nothing (A concedes DR-006), so a wrong first occurrence is silent. Under B-raise the question is the same for lines admitted unedited, with no cut involved.

**A-003 (reviewer behaviour is stationary: E2 drop rates carry to production after the brief states the limits, after any raise, or after a re-ask): REJECT.** The v1 brief states no claim limit today (grep of `document_review_loop_prompts.md` finds only "12 to 200"), the E1 memory note says briefs should state the 300 and 200 caps, and CO-8 (decided) will generate the limits sentence from the constants. The drop rate will move, and a raise or a re-ask moves it again; research/08 point 9 says raising limits has not been tested. Every figure in both proposals (A's 4 residual, B's 44 runs and 120 of 124) is a baseline, not a forecast. Consequence for design: prefer the policy whose cost goes to zero when the rate does. B-core's itemise-and-refuse costs nothing when nothing is dropped; A's repair becomes dead code. If the rate stays high, A's net matters. The policy decision should be written to be robust in both directions and the choice between B-raise and the cut should wait for the M3 measurement of first-pass compliance after the brief change.

**A-004 (C-02 and C-03 `block_ok` semantics apply: an invalid block is skipped for clearing and quorum): ACCEPT, with a caveat.** Code agrees (`ledger.py:129,150`; `cluster.py:256-257`). Both variants depend on it and both change its meaning: A makes `block_ok` True for length-only faults; B leaves it False and adds a re-ask and the `dropped-blocking` refusal. If C-02 or C-03 later change how an invalid block counts, C-002 and C-003 change with them; the C-03 INV-006 (merge unions findings of invalid-block reviewers, `ledger.py:127-138`) is still unaddressed by both.

**A-005 (shadow mode: no verdict reads the v2 parse result, so the policy cannot break INV-A, INV-B or INV-L): QUALIFY.** True today: I confirmed `src/superclaude/cli/reflect` references none of `findings_v2`, `review.findings`, `cli.review`, and `findings_block_compliance_rate` is only read by `scripts/reflect_shadow_exit.py:247`. It stops being true when reflect leaves shadow and cards feed `clusters_kept` (`SKILL.md:347`) and then a verdict. At that point `block_state` and the first-parse state matter to the exit script. A record that preserves the first-parse state (B by construction, A by a second field) is a precondition of leaving shadow, and the shadow exit should be re-checked against whichever policy is chosen.

**A-006 (a second attempt for a reviewer can be recorded and consumed at the point where the block is parsed): QUALIFY (the diff analyst's CONTRADICTED is right for the case it names, wrong as a blanket).** Facts from code: `manifest.py:371-372` raises `OutOfOrder` when the stage is already committed, so a re-ask after the `collected` stage commits cannot be recorded (E1 run A2); `:378-383` raises `Conflict` only when the earlier attempt is `complete`, and `COMPLETIONS` includes `invalid` (`:52`), so a first attempt recorded `invalid` can be superseded by attempt 2 while the stage is open. Two requirements follow, for either policy: (1) parse before the stage commit, record attempt 1 as `invalid`, re-ask, record attempt 2 as `complete`, then commit; (2) the v1 spec loop has no manifest at all (`ledger.py` never references it), so there the record is the second report file and its `report_sha256` in the reviewer entry. B must state requirement 1 in its text; A must state requirement 2.

## Round 2: Rebuttals

### Variant 1 Rebuttal (Proposal A; went first)

# Round 2 rebuttal: Variant 1 (Proposal A), slot C-06 limits-repair-policy

Advocate: A (normalise before the parser). Focus: correctness, risk, test-coverage. Goes first in Round 2.
Code state: HEAD 50d4d2b9d, branch `ironbelly/shadow-runs`, read-only. E2 data read only through `git show` at `6c0984326`.
Tags: [READ] = I read the file or lines in this session before citing; [RAN] = I executed a read-only command this session; [DOC] = taken from a variant, a Round 1 file or an adjudicated merged text that I read but whose source I did not re-open; [UNVERIFIED] = neither.
"A" = Variant 1, "B" = Variant 2. Round 1 files are `round1-advocate-A.md` (mine) and `round1-advocate-B.md`.

## 0. What I moved on, in one paragraph

I keep the core of A (cut first, in code, inside the parsers, recorded) and I now take four things from B as part of the policy, not as additions: the itemised drop record with a three-valued `blocking_state`, the refusal of a PASS that rests on a lost blocking-or-unknown line (with an owner-and-reason acknowledgement), a first-pass state carried next to the repaired state, and B's measurement discipline (rules written before the run, a line-conservation test). I withdraw three statements of mine: "at most 4 residual lines" (it is a floor, section 3 N3), "C-02 INV-009 is unchanged by A" (A actually removes it for length-only faults, N4) and "the SKILL.md:343 sentence needs one sentence changed" (an additive sentence is enough and a test pins the old text, N7). I demote the copy-to-`refs` rule to a recorded flag. New code reading shows that B's re-ask cannot run in the v1 spec loop without a new pre-merge command, and that every one of the 4 audit-D rows where a lost blocking line produced a PASS was an anchor over 200, so cut-first leaves B's refusal almost nothing to fire on in the study data.

## 1. Response to criticisms

Each item states the criticism in its strongest form first, then the answer.

### 1.1 Variant 2's weaknesses 1-8 of Variant 1

**W1. "A's 88 of 92 recovered, at most 4 residual, is a v1 tasklist derivation and does not size the reflect residual; A's re-ask half is as unmeasured as B's."**
Strongest form: `_check_finding` returns the first fault only, so a by-reason count cannot bound second faults; B's replay finds 30 non-length first faults in 154 invalid lines (19.5 percent, 26 of them category), not 4 in 92; and in E1 four of the five re-asks were for causes truncation never touches (coverage rows outside the slice, citation line numbers counted inside the brief).
Answer: conceded in part, and I corrected the claim by reading the order of checks. [READ] `findings.py:96-118`: id, duplicate, severity, blocking, MINOR-with-blocking, category (`:102`), anchor (`:104`), anchor2 (`:107`), refs (`:111-117`), claim (`:118`). A line whose first fault is anchor or anchor2 can hide behind it only a later `refs` fault (the only non-length rule ordered after the length rules; claim is length and is cut in the same pass). So the residual is "4 plus the length-first lines that also carry a refs fault", which is rare (audit-D has one refs-first line in 92) but not measured. The category failures B's replay finds are checked before the anchor, so they were first faults there; they are absent from audit-D's reasons, and why is [UNVERIFIED] (the replay includes stale and superseded folders). Corrected statement: the residual is at least 4 of 92 on the audit-D population and at least 30 of 154 on B's population. What survives: (i) for the length-first lines the cut recovers without a model call, so the re-ask no longer carries all of them; (ii) in the v1 spec loop, which is where all 92 drops happened, the re-ask is needed for roughly the residual instead of 44 reviewer runs (X-003); (iii) in reflect the residual is mostly non-length and the re-ask is load-bearing for both policies equally. I do not claim a recovery rate for the re-ask; Spike 5 is not run.

**W2. "A's 'exact prefix' is 297 characters plus `...` for claims, and cut anchors, anchor2 and quote carry no marker, so a reviser cannot tell."**
Strongest form: the stored claim is no longer a substring of any line of the hashed report, and the only visible trace of a cut anchor is a `repairs` record that nothing renders.
Answer: conceded on both. [READ] `card_convert.py:199-201` cuts to `MAX_CLAIM - 3` plus `...`, so "exact prefix" holds for anchor, anchor2 and quote and not for claim. The fix is in the render slot C-01 already agreed: the per-row `### Lx` block of `## Blocking findings` prints the anchor status (C-01 merged text, section 2.3 [DOC]); it also prints one line "shortened: anchor 335 to 200, claim 412 to 300" from the `repairs` record. No new table column, so the header pins stay (`test_review_ledger.py:451` per C-03 merged text [DOC]).

**W3. "`repair=True` changes what `block_ok` means: a block that broke the contract now votes to clear and counts toward quorum."**
Strongest form: `ledger.py:129` sets `block_ok = parsed["ok"]`; C-02 B2 makes `block_ok` the only reviewer-quality test on the clearing path and C-03 counts `complete` for the floor; A raises both from blocks that were not valid.
Answer: the objection assumes a length fault means the review did not happen. INV-I is about "a review that did not happen" and its refusal (`ledger.py:150-157`, [READ]) is untouched; after the cut `ok` is still the real parser's verdict on the repaired lines, and any residual fault leaves it False. The cost of the literal semantics is concrete, and I did not state it in Round 1 (N4): it deletes dissent (C-02 INV-009), wastes a review of the cap in a one-reviewer re-review (C-02 B5), and lowers C-03 quorum (at least 7 of 264 audit-D merges sit below a 2-of-3 floor today). The legitimate part of the objection is that the quorum analysis must be able to tell a clean block from a repaired one: the round entry records `repaired` beside `block_ok`, and C-03 may choose to count only `repaired == 0` blocks for its floor (a parameter, default off).

**W4. "Two sources of truth for first-parse state; A names no carrier."**
Strongest form: `findings_block_compliance_rate` has no Python in `src`, the only per-card machine state is `block["state"]` in the two card listings, and with `repair=True` that state reads `complete`.
Answer: conceded in Round 1 and now specified from code (N6): the carrier is two additive keys in the listings, derived exactly without a second parse.

**W5. "The copy-to-`refs` rule contradicts 'touches no field the limits do not name'; it may be dead code."**
Answer: conceded and changed. [READ] `refs_norm` reads `anchor`, `anchor2`, `claim` and `refs` (`findings.py:321-337`), so a token that appears only in a cut tail is a real exposure in principle; B's replay changes `refs_norm` on 0 of 125 lines. Under the ladder (no speculative code) the step now only records `refs_changed: true` in the `repairs` item when `refs_norm(original) != refs_norm(repaired)`. The copy rule is added only if M1 shows a nonzero count. The sentence "touches no field the limits do not name" is then true again.

**W6. "A is silent on a lost blocking line."**
Answer: conceded, and adopted (C-004): B's refusal is part of the merged policy for the residual. The new fact is that under cut-first its fire set in the study data is empty (N2), so it is cheap insurance, not a measured necessity.

**W7. "A's re-ask record claim does not apply to the v1 loop: no manifest."**
Answer: conceded (Round 1 concession 5). For v1 the record is the replacement report passed to the re-run `merge` and its `report_sha256` in that round's reviewer entry; a refused merge records nothing by construction (`merge_cmd.py:109-116` [READ]; the in-memory pin at `test_review_ledger.py:373` [READ]).

**W8. "A's 75 percent kill line is its own, and M2 is not run."**
Answer: accepted as stated; symmetric with B's M2 having no margin. Section 6 pre-registers numeric lines for every measurement; the owner may change them before the first run.

### 1.2 B's concessions that bind B, and what I take from them

| B concession (round1-advocate-B.md section 5) | Consequence for the final policy |
|---|---|
| 1. B-core does not fix the v2 loss unit | C-003 goes to A: `cluster.py:255-257` [READ] skips the whole reviewer when its block is not valid; the cut removes that for length faults. |
| 2. "5 of 5" overstated (four confirmed, one unconfirmed, orchestrator-reported) | X-002 is Neither: no recovery rate exists for any policy on gateway models. |
| 3. "3 of 264" derived, `unknown` class unmeasured | I add: its derivation is the `flags.tsv` text, and that text says the cause of all 4 rows was anchor over 200 (N2). |
| 4. About 36 `block ok false` runs have no path in B | B's amendment (re-ask also when an invalid block carries a prior) is adopted for the reflect trigger; in v1 the cut removes most of the cause at the source (W3). |
| 5. "five pins, not four" | The count is more precise than five (N8); the point that B-raise costs pin rewrites and A costs none stands. |
| 6. B's replay population is not audit-D's | M1 runs on both frozen populations; A-001 is Neither. |
| 7. Meaning of the claim cut is [UNVERIFIED] for B | Equally unverified for A: I add a two-judge falsifier (K2). |
| 8. A better on U-001, U-003 and the stateless form | Adopted into the merged policy as written. |
| 9. A-006 is a hole in B too | A-006: narrow form accepted by both. |
| 10. The X-001 textual argument is weaker than B states | X-001: see N7; the sentence is reflect-only and pinned, and an additive sentence is enough. |

### 1.3 B's per-point positions where I still disagree, with the strongest form first

**S-001 and C-001 (B: itemise first, truncation an optional lever behind an owner decision).** Strongest form: any cut is an edit; `SKILL.md:343` forbids normalising; the owner should decide before code does. Answer: the cut is a recorded pure function in the parser path, applied where no text rule forbids it (N7), it recovers the dominant failure class with no model call, no transport and no new command, and it is the only option that works in the v1 loop where no pre-merge step exists (N1). Dropping a line is also an edit, and a larger one: it removed 49 blocking lines and flipped 3 verdicts to PASS in audit-D (R02:100-101 [DOC]). I agree that itemising and the refusal are required under A as well; they are now in the policy.

**C-002 (B: Hybrid, add a re-ask when an invalid block carries a prior).** Strongest form: A's `block_ok` True after repair raises clearing power from broken blocks. Answer: W3 and N4. B's amendment is sound for residual faults and I adopt it as a reflect-path trigger; in the v1 loop an invalid-block reviewer's lost `prior resolved` costs one review of the cap (rows stay `resolved_check`, C-02 B5 [DOC]), not a wrong PASS, so it is a re-ask trigger and not a refusal.

**C-009 and C-012 (B: B wins; claim meaning and byte provenance).** Strongest form: the claim carries "X is wrong because Y" (`document_review_loop_prompts.md:60` per both variants [DOC]), the cut tails in B's sample are consequence clauses, and the stored member is no longer a byte copy of a hashed line. Answer: both stand as risks and neither is measured. I keep the cut for claims only with three safeguards: the visible `...` marker, the "shortened from N" line in the row, and a blind two-judge test on B's 34 claims (22 blocking, corrected from the "10 blocking" I wrote in Round 1: 10 is audit-D's claim-blocking count, 22 is B's replay count); if the judges mark more than 20 percent of the blocking claims as having lost a decision-relevant clause, claims move to re-ask-first and anchors, anchor2 and quote stay cut. For provenance each `repairs` item carries `original_sha256` of the flattened original field, so a cut field can be checked against `report_sha256`; the stored member is a recorded derived value, not a byte copy, and I say so.

**X-001 (B: Variant 2).** Answered in N7: the sentence is in the reflect skill only, is pinned by a test, and an additive sentence keeps both true. The remaining question is an owner call, which I state as a dependency and give a mechanical fallback for.

**X-003 (B: Variant 2, the re-ask is load-bearing in reflect).** Conceded for reflect; contested for v1: see N3 and N1.

## 2. Updated assessment of Variant 2

What B has shown that I did not have: the replay (5,270 lines, prefix locates 89 of 89 verbatim over-limit fields, `refs_norm` unchanged on 0 of 125), the E1 re-ask table, the PASS-by-loss refusal with an acknowledgement exit, the `blocking_state` class, the conservation property, the pre-registration discipline and the E2 design-review counter-evidence about agent-run normalisers and session surfaces. B is right that the compliance metric is honest by construction under B-core, and that the claim cut is the weakest part of A.

What B's defence leaves standing against B-core as a default:
1. **No place to run in v1.** The re-ask for the 44 reviewer runs needs a check that runs before the merge records the round, and none exists (N1). Either a new subcommand or a scratch merge is required, and B names neither.
2. **Deletion of votes.** Under literal `block_ok`, a length fault silently drops that reviewer's `prior open` dissent, wastes a review in a one-reviewer re-review and lowers quorum (N4). B's own amendment (re-ask also for invalid blocks that carry a prior) is the admission.
3. **The v2 loss unit** stays a whole reviewer per bad line unless the re-ask works (B conceded).
4. **B-raise** is untested on reviewer behaviour and an owner decision; it composes with A rather than replacing it, because any fixed limit has a tail.

My overall view: B's policy and A's policy differ on one thing, whether the first response to a length fault is a code cut or a model call. The code cut wins on dispatch independence, on the v1 mechanics and on the effects on C-02 and C-03. B's contributions fix the places where A was silent or unsafe. The merged policy below is A's order with B's record, refusal and carrier.

## 3. New evidence (code checks run now)

**N1. There is no pre-merge check or re-ask step for the v1 loop [READ, plus grep].**
- `merge_cmd.py:99-118` reads the reports, calls `led.merge_round` once (`:109`), renders (`:110`), writes `--out` (`:113-115`) and saves the ledger last (`:116`). A raised `LedgerError` is converted to a `ClickException` (`:111-112`), so a refused merge writes nothing.
- `merge_round` demands `n == len(rounds)+1` (`ledger.py:114-118`), so after a successful merge the same round cannot be merged again.
- The registered commands in `src/superclaude/cli/review` are `merge`, the ledger group (`revise`, `defer`, `verdict`, `capture`), `manifest` (`init`, `advance`, `validate`), `panel` (`resolve`, `validate`), `telemetry`, `cluster` and `verify-citations` (grep of command registrations): none parses a v1 block without merging.
- Consequence: B's re-ask for dropped blocking lines in merges that succeed (45 of 49 blocking drops in audit-D end with a surviving blocking row) needs a new parse-only command or a scratch merge. A re-ask driven by a refusal needs nothing new: the refusal leaves the file unchanged (`merge_cmd.py:109-116`), the docstring already says so for the zero-valid case (`ledger.py:111`), and the re-run passes the replacement report. That is the v1 transport in the merged policy.

**N2. All 4 PASS-by-loss rows in audit-D are anchors over 200 [RAN].**
`git show 6c0984326:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/flags.tsv`, filtered on "NO blocking row": g3-sonnet-luna-ember-r3 (F1), g5-ember2-luna-r2 (F1), n5-sonnet-ember (F1 and F2), each "blocking finding dropped by merge (anchor>200)". So the 3 merges B's refusal would catch are all inside the cut's reach. Under cut-first, B's refusal fires on 0 of 264 merges in this population, provided the repaired lines carry no hidden second fault (the hidden faults can only be `refs`, N3). Derived from the file's reason text, not re-executed against ledgers. The refusal therefore guards the residual (bad JSON, non-boolean `blocking`, bad severity, refs) and keeps `INV-I` closed for them; it is not justified by a measured fire rate.

**N3. The residual is a floor and depends on the population [READ, DOC].** See W1. Audit-D: at least 4 of 92 (3 severity, 1 refs). B's replay: at least 30 of 154 (category 26, severity 3, refs 1). Both from first-fault counts. M1 reports the post-cut residual by rule on both populations.

**N4. What `block_ok` True after repair changes for C-02 and C-03 [READ, RAN, DOC].**
- C-02 INV-009 (merged C-02 text, probe table): the `block_ok` filter drops an invalid reviewer's `prior resolved` and also its `prior open` (collected at `findings.py:186-187` [READ], passed on at `ledger.py:139-140` [READ] with no `block_ok` test), so a valid `resolved` can clear over that dissent. With the cut, a length-faulted reviewer's dissent counts. My Round 1 line "INV-009 is unchanged by this position" was wrong for length-only faults.
- C-02 B5 and E2: the standard re-review is one reviewer (all 8 packaged templates carry `apply_to: ["first"]`, C-02 E2 [DOC]), so a length fault on a new finding by that reviewer leaves every `resolved_check` row unanswered, the decision REVISE with `next = re-review`, and one of the 3 reviews spent. Under B-core only a pre-merge re-ask prevents that, and N1 says none exists.
- C-03 floor (`complete >= min(2, requested)`, merged-output.md:36 [READ]): audit-D has 80 `2-blockok` rows [RAN: awk over `flags.tsv`], in 73 distinct (row, package) merges; 7 merges have two block-ok-false reviewers and none has three. With three reviewers and a floor of 2, at least those 7 of 264 merges (2.7 percent) are below the floor under today's `block_ok`; two-reviewer rows (for example `n5-sonnet-ember`) would be refused on a single fault, and I did not count them. Not all 80 are length faults (a missing block or a truncated block is also False), so repair lowers this number by an unknown amount and cannot raise it.
- The refusal at `ledger.py:150-157` is unchanged, and the one `block_ok` pin I checked (`test_review_ledger.py:376-385`) uses `_broken`, whose text has no findings block at all (`:341-342`), so a length repair does not flip it.

**N5. The dropped-blocking refusal and the C-03 refusal object [READ, DOC].**
- C-03 decided a `LedgerError` subtype, exit 12, and a printed object `{"refusal": "quorum_shortfall", requested, complete, invalid}` with no `decision` key (merged-output.md:36 and :77 [READ]).
- A dropped-blocking check needs the post-union result (is the derived verdict PASS), so it runs at the end of `merge_round`, after the quorum check. It still precedes `led.save` (`merge_cmd.py:116`), so the file on disk is unchanged. But `merge_round` mutates the ledger as it goes, and the existing refusal pin asserts the in-memory ledger is untouched (`test_review_ledger.py:373`: `led["rounds"] == [] and led["rows"] == []`). So the check must run on a deep copy that is swapped in on success, or the pin pattern breaks.
- It reuses the object: `{"refusal": "dropped_blocking", reviewers, dropped: [{reviewer_id, line, finding_id, blocking_state, rule}]}`, same exit 12, so the coordinator has one "re-run the review" signal. The acknowledgement option on `merge` takes owner and reason, mirrors C-02's `defer`, is stored in the round entry and listed in the merged report. C-03's open INV-001 applies unchanged: a refusal leaves no stored trace, so its rate is not measurable from the ledger.
- C-03's open INV-006 (merge unions findings of invalid-block reviewers) shrinks under A because fewer blocks are invalid; it is not closed.

**N6. First-pass state can be carried exactly, without a second parse [READ].**
- The only per-card state carriers in `src` are `cluster_cmd.py:155-163` (`state`, `block_state`, `errors`) and `verify_cmd.py:136-138` (`block_state`); `block_state` appears nowhere else (grep), and `findings_block_compliance_rate` has no Python in `src` (grep over `*.py`: no match); `scripts/reflect_shadow_exit.py:247` only reads it from telemetry.
- With `repair=True`, `errors` in the cluster listing would be empty for a repaired block and the length violations would vanish from the shadow artifact. So the listing must carry `repairs`.
- Exactness: the cut fires only on a field the unrepaired parse would reject, so the first-pass state is `state` if `state != "complete"`, else `invalid` if `repairs` is non-empty, else `complete`. Two additive keys, `first_pass_state` and `repairs`, in both listings; existing consumers read `state` and `errors` (`test_review_cluster_cmd.py:89,99,167` [grep]) and keep working.
- The same fact settles B's weakness 4: no second parse is needed; a differential test against a `repair=False` parse checks it.

**N7. The `SKILL.md:343` sentence is reflect-only and pinned [READ, RAN].**
- The sentence ("The orchestrator never edits, remaps or normalizes a reviewer's findings itself: a block that still fails after the one re-ask stays invalid") is step 4 of the reflect shadow procedure. `document_review_loop_prompts.md` and `spec-panel.md` have zero matches for "never edits", "remaps" and "normaliz" (grep counts: 0 and 0), so no text rule binds the v1 `merge`, where all 92 audit-D drops happened.
- `tests/cli/reflect/test_shadow_skill_contract.py:229-232` asserts three substrings of it ("valid on this first parse", "before any re-ask", "never edits, remaps or normalizes a reviewer's findings itself") and `first parse (before any re-ask)` in the skill text. Changing that sentence means editing a pin; adding one sentence after it does not. So my Round 1 line "needs one sentence changed" is withdrawn in favour of an additive sentence.
- It stays an owner reading whether package code counts as "the orchestrator"; the mechanical fallback is to leave the v2 call sites at `repair=False` (itemise only) and keep the repair in v1 `merge`.

**N8. Pin counts [READ, grep over `tests/`].**
- Over-limit literals in `tests/review`: `test_review_findings.py:113` (anchor 201) and `:117` (claim 301); `test_review_findings_v2.py:200` (quote 201; `:199` is the passing 200) and `:241` (claim 300 / 301); `test_review_card_convert.py:500` (`len == 300`). `parse_block` appears in only three test files (`test_review_findings.py`, `test_review_findings_v2.py` and one hit in `tests/cli/reflect/test_shadow_skill_contract.py:215`). `test_review_card_convert.py:697` uses `cc.MAX_REF_TEXT` and follows a changed constant.
- Under A: `repair=True` at the three production call sites rewrites 0 pins (no ledger or CLI test feeds an over-limit line); the direct-parser pins stay with the default `repair=False`.
- Under B-raise as stated (anchor, anchor2 and claim only): 3 assertion sites (`:113`, `:117`, v2 `:241`), 4 if `card_convert` imports the shared claim constant (`:500`). The quote pin (v2 `:200`) changes only if the quote limit is also raised. B's "four" listed the quote pin B-raise does not touch and omitted `card_convert`; the "five" in the diff analysis and both Round 1 files holds only if the quote limit is raised as well.

**N9. A repaired line that does not locate is still kept [READ].** `annotate` keeps a finding whose anchor is not found with `anchor_status: missing` (C-01 merged text, section 2.3 [DOC]; `findings.py:346-360` as cited in Round 1). B's own replay says 5 of 94 over-limit fields are not verbatim and are missing under any policy; under A the difference is a visible row where today there is none.

What I did not check this session: panel sizes per audit-D row (so the 2-reviewer quorum effect is uncounted), whether the audit-D non-blocking drops hide a second fault, whether any E2 launcher depends on dropped lines, and any PR-code corpus.

## 4. FINAL per-point table

Where I moved from Round 1 the reason column says "moved".

| ID | Final winner | Conf. | One-line reason |
|---|---|---|---|
| S-001 | Hybrid | 76 | A's cut-then-parse, with B's itemised record, PASS-by-loss refusal, and one stateless re-ask driven by the refusal (v1) or the invalid block (reflect); raise lever deferred. |
| S-002 | Hybrid | 80 | A's `repair` keyword (0 pins rewritten) plus B's additive `dropped` record with `blocking_state` and a derived `first_pass_state`. |
| S-003 | Variant 2 | 78 | B's 5,270-line replay and E1 table are the larger evidence base; my `flags.tsv` read adds that all 4 PASS-by-loss rows are anchor over 200. |
| S-004 | Hybrid | 82 | A's numeric kill lines and cost-side replay plus B's pre-registration, conservation test and T-B5; margins fixed before any run. |
| S-005 | Variant 2 | 70 | B's INV-A..N table is wider; keep A's candid "partly endangered" label for INV-C inside it. |
| S-006 | Neither | 60 | Presentation only; adopt B's open-facts section. |
| C-001 | Variant 1 | 72 | Cut anchor, anchor2, quote in code; claim cut visible in the row with a judge falsifier; no text rule binds v1; a drop is itself a larger edit (moved: anchors now visible too). |
| C-002 | Variant 1 | 80 | A length-only fault must not void a block: it deletes dissent (C-02 INV-009), wastes a review (C-02 B5) and lowers C-03 quorum (at least 7 of 264); residual faults stay `ok` False. |
| C-003 | Variant 1 | 76 | `cluster.py:255-257` skips a whole reviewer for one bad line; B conceded; shadow-only today. |
| C-004 | Variant 2 | 78 | Adopt B's refusal and acknowledgement for residual lines; it fires on 0 of 264 audit-D merges once the cut exists (insurance; moved from Hybrid). |
| C-005 | Hybrid | 74 | A's residual-only stateless re-ask with B's `blocking_state` gating; in v1 the trigger is the refusal, in reflect the E1 rule plus B's invalid-block-with-prior amendment. |
| C-006 | Hybrid | 72 | Stateless prompt, no `--resume`; reflect: attempt 2 before the `collected` commit (`manifest.py:371-383`); v1: replacement report plus its sha in the re-run merge; record shape belongs to C-08. |
| C-007 | Hybrid | 80 | B's replay (89 of 89, unique prefix) is the tasklist evidence; A's kill line stays for multi-line and code anchors. |
| C-008 | Hybrid | 70 | Record `refs_changed` only; copy-to-`refs` only if M1 shows firing (B: 0 of 125); fixes A's "touches no other field" sentence (moved). |
| C-009 | Hybrid | 62 | Cut claim with marker and a "shortened from N" row line, two-judge falsifier K2, fall back to re-ask-first for claims if it fails. |
| C-010 | Hybrid | 72 | `repairs` item per cut plus a rendered "shortened" line in the row's `### Lx` block; `...` marker on claims only (moved from Variant 1: unmarked anchors were a real gap). |
| C-011 | Hybrid | 70 | Repair is the default and works at any limit; raising limits is a separate owner decision after the CO-8 measurement; its pin cost is 3 (4 with `card_convert`), not 5. |
| C-012 | Hybrid | 70 | Derived copy plus `original_sha256` of the flattened field and the existing `report_sha256`; accept that the member is not a byte copy. |
| C-013 | Hybrid | 76 | A's repair plus a derived `first_pass_state` and `repairs` in both listings (exact, no second parse) and a differential test; B's by-construction safety replaced by a test (moved from Variant 2). |
| C-014 | Hybrid | 64 | Quote prefix passes the substring test (`verify_cmd.py:68-72`); per-profile limits as a parameter; in-session stateless re-ask; a code corpus is required before a PR module relies on it. |
| X-001 | Variant 1 | 66 | Sentence is reflect step 4 only (0 hits in v1 prompt and spec-panel) and pinned; additive sentence keeps the pin; owner must confirm code is not "the orchestrator"; fallback is v2 `repair=False`. |
| X-002 | Neither | 62 | No recovery rate exists for gateway models; E1 is four confirmed of five, Agent path, one length cause. |
| X-003 | Hybrid | 72 | A's 4 is a floor (hidden refs faults) and 19.5 percent on B's population; B's 44 reviewer runs fall to roughly the residual in v1; reflect's residual is non-length for both. |
| X-004 | Hybrid | 82 | Both hold only if first-pass state is carried: `first_pass_state` plus `repaired_lines_rate` and `dropped_lines_rate`. |
| U-001 | Variant 1 | 80 | The keyword keeps the five over-limit pins literal and answers C-01 INV-003; add a test that all three call sites pass it. |
| U-002 | Hybrid | 68 | The `refs_norm` exposure is real (`findings.py:321-337`) but measured at 0 of 125: record, do not copy (moved). |
| U-003 | Variant 1 | 85 | The cost-side re-merge is the only measurement that can show the policy harmful. |
| U-004 | Variant 1 | 80 | `repaired_lines_rate` per model, with B's `dropped_lines_rate` as the counterpart. |
| U-005 | Hybrid | 72 | Valid only in an open reflect stage for a non-`complete` earlier attempt; v1 has no manifest. |
| U-006 | Variant 2 | 85 | Adopt as the M1 population and the admission curve, with the population caveat. |
| U-007 | Variant 2 | 80 | Adopt, restated as four confirmed, one unconfirmed, Agent path. |
| U-008 | Variant 2 | 80 | Adopt the refusal with the acknowledgement exit; acknowledgement mirrors C-02 `defer`. |
| U-009 | Variant 2 | 80 | Adopt `blocking_state` and the conservation property (covers bad `prior` lines). |
| U-010 | Variant 2 | 70 | Adopt T-B5: the re-ask holds only the reviewer's own block and rejected lines and grants no tool. |
| U-011 | Variant 2 | 68 | B-raise as a documented, separable owner-decision lever; not in the default policy. |
| A-001 | Neither | 75 | QUALIFY: the audit-D base orders the policies but cannot state a recovery percentage; M1 uses two frozen populations. |
| A-002 | Neither | 78 | ACCEPT for verbatim single-line anchors (89 of 89); open for multi-line and code; missing-anchor rows exist today under any policy. |
| A-003 | Neither | 72 | REJECT stationarity (moved from QUALIFY): CO-8 changes the claim rate; both policies are written to hold either way, A's repair costs about nothing when the rate falls. |
| A-004 | Hybrid | 80 | ACCEPT, now quantified: C-02 INV-009, C-02 B5 and the C-03 floor (at least 7 of 264). |
| A-005 | Hybrid | 76 | QUALIFY: true only while shadow lasts; leaving shadow requires `first_pass_state` to be carried. |
| A-006 | Hybrid | 78 | REJECT the unconditional form, accept the narrow form (reflect manifest, open stage, non-`complete` earlier attempt); v1 record is the replacement report. |

## 5. Where I moved from Round 1, and why

1. "At most 4 residual lines" to "at least 4, population-dependent": code order of checks (`findings.py:96-118`) and B's replay.
2. "INV-009 unchanged by A" to "A removes it for length-only faults": `findings.py:186-187` and `ledger.py:139-140` collect priors from invalid blocks.
3. "SKILL.md:343 needs one sentence changed" to "add one sentence": a test pins the old substrings (`test_shadow_skill_contract.py:229-232`).
4. C-004: Hybrid to Variant 2 (adopt B's refusal), because INV-I covers the residual and the rule is cheap; its fire rate is 0 in the study data once the cut exists.
5. C-010 from Variant 1 to Hybrid and C-013 from Variant 2 to Hybrid: cut anchors need a rendered note; the first-pass carrier is exact and cheap, so A can own it.
6. Copy-to-`refs` demoted to a recorded flag (C-008, U-002): B's 0 of 125 and the ladder.
7. The v1 re-ask is refusal-driven (no new command): N1.
8. "10 blocking claims" corrected to 22 in B's replay population (10 is audit-D's).
9. A-003: QUALIFY to REJECT stationarity.
10. Pin count: "five" replaced by the per-site count (N8).

## 6. Proposed resolution text (12 bullets)

1. **Cut first, in the parsers (a).** Both `parse_block` functions take `repair=False`; the production call sites `ledger.py:128`, `cluster_cmd.py:151` and `verify_cmd.py:133` pass `repair=True` (a test checks every production call site passes it). One pure `repair_line(obj)` in the shared limits module cuts `anchor`, `anchor2` and a citation `quote` to the first 200 characters of their flattened form and `claim` to 297 plus `...`, before `_check_finding` and `check_finding`, and touches no other field and no `prior` line. Direct-parser pins stay unmodified.
2. **Itemise everything that is still dropped (a).** Each residual drop and each cut is recorded as `{line, finding_id, blocking_state (true, false, unknown), rule, field, original_chars, kept_chars, original_sha256}`, never reviewer text; the report file is never edited; a conservation test holds per block (non-blank lines = kept + priors + dropped); the merged report's `### Lx` block prints "shortened from N" next to the anchor status.
3. **Re-ask trigger (b).** Only for what remains invalid after the cut. In the v1 spec loop the trigger is the dropped-blocking refusal (item 8); lines that said `blocking: false` are itemised and not re-asked. In reflect the E1 rule stands (an invalid block after repair gets one bounded re-ask) plus B's amendment (an invalid block that carries a prior line is re-asked too).
4. **Re-ask transport (b).** Stateless: the original brief, the reviewer's own block and the parser's per-line errors, whole block returned; no other reviewer's content, no new tool grant, no `--resume` dependency (an optimisation only where a transport proves it). A transport that cannot re-ask degrades to itemise plus the refusal.
5. **Re-ask record (b).** Reflect: attempt 2 recorded before the `collected` commit, only while the earlier attempt is not `complete` (`manifest.py:371-383`). v1: the replacement report goes to the re-run `merge` and its `report_sha256` is in that round's entry. The record shape is C-08's.
6. **`block_ok` (c).** `block_ok` is the real parser verdict on the repaired lines: a length-only block is True (v1) or `complete` (v2); any residual fault is False. Reviewer entries add `repaired` and `dropped`; C-02 counts `block_ok`; C-03 counts `complete`, and may count only `repaired == 0` blocks for its floor as a recorded parameter (default off).
7. **First-pass carrier (d).** The parse result gains `repairs` and `first_pass_state` (`state` unless complete, else `invalid` when `repairs` is non-empty); `cluster_cmd.py:155-163` and `verify_cmd.py:136-138` emit both beside the unchanged `state`; `findings_block_compliance_rate` is the share of cards whose `first_pass_state` is complete; a differential test against a `repair=False` parse must show zero mismatches; `repaired_lines_rate` and `dropped_lines_rate` per model sit beside it.
8. **Dropped-blocking refusal (e).** At the end of `merge_round`, after the quorum check and on a deep copy swapped in on success (`test_review_ledger.py:373`), if the derived verdict would be PASS and an unacknowledged residual dropped line has `blocking_state` true or unknown, raise the C-03 refusal subtype: exit 12, `{"refusal": "dropped_blocking", reviewers, dropped}`, ledger file unchanged. An owner-and-reason acknowledgement option on `merge` lifts it, is recorded and listed in the report. No refusal when a blocking row survives; the dropped ids are printed.
9. **Raise lever (f).** Not part of the policy. Briefs state the limits from the constants (CO-8). After that change, measure first-pass compliance and `repaired_lines_rate`; any raise of the constants is a separate owner decision that rewrites 3 assertion sites (4 with `card_convert`, 5 only if the quote limit is raised) and reruns M1 and M2.
10. **Measurements (g).** M1 offline replay of the cut on two frozen populations (audit-D, 264 merges and 92 lines; B's 154 invalid lines), reporting passes-parser, locates-uniquely, `refs_changed` and residual by rule. M2 re-merge of the 264 merges with repair on and off, counting added blocking rows judged false and PASS-to-FAIL flips. M3 two-judge claim-meaning test. M4 stateless re-ask on the residual lines, per transport. M5 unit tests: no-op on every valid fixture line, boundaries 200/201 and 300/301 with and without repair, idempotence, no invented anchor, conservation, differential first-pass. M6 live `repaired_lines_rate` per model.
11. **Kill lines (g), written to a file before the first run; the owner may change the numbers.** K1: fewer than 90 percent of over-limit anchor, anchor2 and quote fields pass the parser and locate uniquely on audit-D (75 percent on a code or multi-line corpus once one exists) demotes that field class to itemise plus re-ask. K2: more than 20 percent of blocking claims judged to lose a decision-relevant clause (both judges) moves claims to re-ask-first. K3: repair is wrong if the blocking rows it adds are judged false more than 10 percentage points above the base rate of kept blocking rows, or if any merge flips PASS to FAIL through a false repaired row the cap of 3 reviews cannot clear. K4: the re-ask half is wrong if recovery is under 60 percent over at least 20 residual lines or if any re-ask changes a line it was not asked about. K5: the refusal is wrong if it fires on more than 5 of 264 merges after the cut or if any refusal has no re-ask or acknowledgement exit.
12. **`SKILL.md:343` (h).** Leave the existing Normalize sentences byte-identical (they are pinned at `tests/cli/reflect/test_shadow_skill_contract.py:229-232`); add one sentence after them: the package's parser step shortens over-limit fields in code, records every shortening, and the orchestrator still never edits a finding; the first-parse compliance rate reads `first_pass_state`. The owner confirms that package code is not "the orchestrator"; if not, the v2 call sites stay at `repair=False` (itemise and re-ask only) and the v1 `merge` keeps the repair, because no text rule binds it.

### Variant 2 Rebuttal (Proposal B; went second, saw the Variant 1 rebuttal)

# Round 2 rebuttal: Variant 2 (Proposal B), slot C-06 limits-repair-policy

Advocate: B (never edit reviewer text; itemise; one bounded re-ask; refuse a PASS that rests on dropped blocking-or-unknown lines; optional raise of limits). Focus: correctness, risk, test-coverage. Goes second in Round 2 and answers `round2-advocate-A.md`.
Code state: HEAD 50d4d2b9d, branch `ironbelly/shadow-runs`, read-only. E2 data read only through `git cat-file` / `git show` at `6c0984326`; no file written other than this one.
Tags: [READ] I read the file or lines this session before citing; [RAN] I executed a read-only replay this session (method in section 3); [DOC] taken from a variant, a Round 1 file or an adjudicated merged text whose source I did not re-open; [UNVERIFIED] none of these.
"A" = Variant 1, "B" = Variant 2. "P273" = the population of my replays (section 3).

## 0. Position in one paragraph, and what I moved on

I moved a long way. Round 1 held "no edit by default; truncation only as an owner-decided lever". After A's Round 2 and my own replays I now hold a split by field. The three location fields (`anchor`, `anchor2`, citation `quote`) are cut to a 200-character flattened prefix in code, recorded, behind A's `repair=False` keyword: on P273 all 70 over-limit fields whose full anchor locates keep the same first span under the prefix (34 of 37 blocking fields; the other 3 do not locate under any policy), the cut flips only the 3 merges that were wrong PASSes, and B-core's no-edit rule would put 10 of 273 merges below the C-03 floor in a way I had not counted. The claim and every other field stay unedited: a claim cut changes no verdict on P273, the cut-free alternatives (a claim limit of 450, the already-decided brief change, a refusal-driven re-ask) reproduce the cut-all outcome or cost 2 merges, and the claim is the one field whose meaning nobody has measured. I keep B's itemised record with `blocking_state`, the PASS-by-loss refusal with an acknowledgement exit, and the pre-registered measurements; I adopt A's keyword, A's derived first-pass carrier, A's refusal-driven v1 transport and A's cost-side re-merge. Where I still disagree with A: the default for claims, and A's claim that the dropped-blocking rule is only insurance (it is, after the cut, but it is the only thing that keeps INV-I closed for lines the cut cannot reach).

## 1. Response to criticisms

Each item states the criticism in its strongest form, then the answer or concession.

### 1.1 A's Round 1 weaknesses of Variant 2

**W1. "B calls a reviewer with an unresolved dropped line non-`complete` yet re-asks only `blocking: true|unknown` drops, leaving about 36 `block ok false` runs with no recovery path."**
Strongest form: under C-02 B2 an invalid-block reviewer's `prior` lines do not count and under C-03 it leaves the floor, so a length fault on a non-blocking line silently costs clearing power and quorum.
Answer: conceded, and the damage is larger than either Round 1 counted. [RAN] On P273, 79 of 855 reviewer-runs have `ok` False: 75 are length-only (40 with at least one dropped `blocking: true|unknown` line, 35 with only `blocking: false` drops), 2 carry a non-length line fault, 2 are block-level faults (missing, unclosed or multiple block). Under the floor C-03 adopted (`complete >= min(2, requested)`, `merge-verdict-policy-and-quorum/merged-output.md:36` [READ via grep]), with today's `ok` as the completeness test, 10 of 273 merges fall below the floor (panel sizes 3: 144, 2: 51, 4: 45, 5: 27, 1: 6). A's "at least 7 of 264" counted only three-reviewer panels. My Round 1 answer 1 ("stall exposure is small") is withdrawn. Fix: eligibility for clearing and quorum must not be the bare parser bit (section 6 bullet 5); with that rule 5 of the 10 remain (the other reviewer's blocking line was the lost one) and with a perfect re-ask or the cut none do.

**W2. "The fail-closed rule is derived from `flags.tsv` wording, not executed; the `unknown` class is unmeasured."**
Strongest form: B says "3 of 264, none of the other 261" from file text.
Answer: now executed. [RAN] Re-merging P273 with HEAD `ledger.merge_round`: the baseline re-merge reproduces the stored verdict in 273 of 273; the stored PASS with a dropped `blocking: true|unknown` line occurs in exactly 3 merges (g3-sonnet-luna-ember-r3 and g5-ember2-luna-r2 on makeTheAlias, n5-sonnet-ember on design). The `unknown` class (bad JSON, non-boolean `blocking`) has 0 members in P273, so its fire rate is 0 here and remains unmeasured elsewhere. A is right that after the cut the refusal fires on 0 of 273 (section 3, E4), so it is insurance for lines the cut cannot reach; see section 1.3 for why I keep it.

**W3. "B-raise is a grammar widening, an owner decision, with an undercounted pin cost."**
Answer: conceded on the count, and narrowed. A's N8 count holds [READ]: over-limit literals are `tests/review/test_review_findings.py:113` (anchor 201) and `:117` (claim 301), `tests/review/test_review_findings_v2.py:200` (quote 201) and `:241` (claim 300 / 301), `tests/review/test_review_card_convert.py:500` (`len(f["claim"]) == 300`). My "four" listed the quote pin that an anchor-and-claim raise does not touch. I no longer propose raising anchors at all (the cut covers them). The only lever I keep is a claim-only raise: 2 assertion sites (`:117`, v2 `:241`), 3 if `card_convert` imports the shared claim constant. It stays an owner decision (INV-C).

**W4. "The E1 recovery evidence is weaker than '5 of 5'."**
Answer: conceded in Round 1 (four confirmed, one unconfirmed, Agent path, one length cause). X-002 is Neither.

**W5. "B's re-ask depends on a record the manifest may refuse; v1 has no manifest."**
Answer: conceded and verified. [READ] `manifest.py:371-372` raises `OutOfOrder` when the stage is committed or not next; `:378-381` raises `Conflict` when the latest earlier attempt is `complete`; otherwise `:382-383` sets `superseded_by`. [READ] The registered review commands are `merge`, `ledger` (`revise`, `defer`, `verdict`, `capture`), `manifest`, `panel`, `telemetry`, `cluster`, `verify-citations`; `ledger.py` never imports the manifest. So the second attempt is recordable only in reflect, before the `collected` commit, for a non-`complete` first attempt; in v1 the record is the replacement report and its `report_sha256`.

**W6. "B's textual argument from `SKILL.md:343` weakens itself."**
Answer: conceded, with one more verified fact. [READ] `SKILL.md:343` is step 4 ("Normalize") of the reflect shadow procedure and is addressed to "the orchestrator"; the same file's step 6 (`SKILL.md:345` region, read as line 345) says the cluster and verify commands "drop nothing". [READ] A grep of the v1 review package, the spec-panel and review skills, the loop prompts and the reflect skill finds "remaps" only at `SKILL.md:343`. [READ] `tests/cli/reflect/test_shadow_skill_contract.py:230-232` pins three substrings of that step, so an additive sentence is safe and an edit to the sentence is not. I withdraw X-001 as a B win for v1.

**W7. "B keeps `card_convert.py`'s marked truncation while forbidding truncation elsewhere: a split policy in one package."**
Strongest form: `card_convert.py` cuts claims to 297 plus `...` in production-tree code (A cites `:86` and `:199-201`; [READ] the pin `test_review_card_convert.py:494-501` confirms the 300-character result with a trailing `...`).
Answer: partly conceded. The converter turns foreign legacy cards into findings for measurement; it is not a gate on reviewer output. But with a no-cut claim default the package would carry one marked claim cut and no other. The merged text should say so in one sentence (resolution bullet 12) rather than leave a silent exception. This is a documentation fix, not a reason to cut claims in the parsers.

### 1.2 A's Round 2 arguments against B-core

**N1 ("no pre-merge check or re-ask place in the v1 loop"). Strongest form:** the re-ask for 44 reviewer runs needs a parse-only step; `merge_round` demands `n == len(rounds)+1` (`ledger.py:114-118`), so a re-ask after a successful merge cannot be re-merged; the registered commands include none that parses a v1 block without merging.
Answer: confirmed [READ: `merge_cmd.py:99-118` saves only after success at `:116`; the command list above]. B's Round 1 trigger ("re-ask whenever a dropped line is `true` or `unknown`") had no v1 vehicle. I adopt A's vehicle: in v1 the re-ask is driven by a refusal (`dropped-blocking`, or the C-03 quorum refusal), which records nothing, so the coordinator re-asks the named reviewer and re-runs `merge` with the replacement report. Cost: v1 never recovers a lost blocking line in a merge that succeeds with another blocking row standing (36 of 39 merges that carry a dropped blocking line in P273); the line is itemised and printed only. That is the real price of "never edit", and it is what the anchor cut removes.

**N2 ("all 4 PASS-by-loss rows are anchor over 200, so cut-first leaves B's refusal nothing to fire on").** Confirmed [RAN]: the four lines (F1 x3, F2) have anchors of 215, 218, 240, 240 characters, claims of 79 to 166, no second fault. A cut recovers them; a limit of 250 would too. B's claim that the refusal "fires on 3 of 264" is correct for no-cut and 0 for cut.

**N3 ("the residual is a floor, not 4 lines").** Conceded. [READ] `_check_finding` order (`findings.py:96-118`): id, duplicate, severity, `blocking`, MINOR-blocking, category (`:102`), anchor (`:104`), anchor2 (`:107`), refs (`:111`), claim (`:118`); it returns the first fault, so a by-reason count cannot bound second faults. [RAN] with all faults collected on P273: 4 of 90 dropped lines carry a non-length fault (3 severity, 1 refs); every other dropped line has only length faults, so on this population the first-fault floor is also the all-fault count. The replay population of B's Round 1 (category 26 first faults) is not reproduced on P273: no category fault occurs here, which supports A's "[UNVERIFIED] why".

**N4 ("literal `block_ok` deletes dissent, wastes a review, lowers the floor").** Verified in part, corrected in part. [READ] `ledger.py:150` and `:295` are the only reads of `block_ok` in `src/superclaude/cli/review` (grep); the clearing loop at `:254-258` does not read it, and `ledger.py:139-140` collects priors with no `block_ok` test, as `findings.py:175-187` appends a valid prior before `ok` goes False. So today a length fault costs a reviewer nothing at clearing. The cost A describes is a consequence of the adjudicated C-02 B1/B2 (quorum gate over `block_ok`-true reviewers, `ledger-clearing-and-verdict-authority/merged-ledger-clearing-and-verdict-authority.md`, B1 and B2 [READ via grep]) and of C-03's floor, which together make `ok` load-bearing. I accept the consequence: under those rules a bare `ok` False is expensive, and section 6 bullet 5 stops using the bare bit.

**N5 ("the refusal must run on a working copy").** Confirmed [READ]: `merge_round` appends rows at `ledger.py:204` and the round at `:276`, so a check that needs the derived verdict runs after mutation; the pins are `tests/review/test_review_ledger.py:352-361` (ledger JSON byte-identical after a zero-valid refusal) and `:373` (`led["rounds"] == [] and led["rows"] == []`). It applies equally to A's and B's refusal. Agreed.

**N6 ("first-pass state can be carried exactly").** Conceded: B's Round 1 point that A named no carrier is answered. [READ] `cluster_cmd.py:151-163` makes one `parse_block` call and lists `state`, `block_state`, `errors` from it; `findings_block_compliance_rate` has no Python in `src` (A's grep, and my Round 1). A's derivation (`first_pass_state` is `state` unless complete, else `invalid` when `repairs` is non-empty) is exact because the cut fires only on a field the unrepaired parse rejects. I add one requirement: the skill's step 4 must read `first_pass_state`, which is the additive sentence of bullet 11, and a differential test must show zero mismatches against a `repair=False` parse.

**N7 (`SKILL.md:343` is reflect-only and pinned).** Confirmed (W6).

**N8 (pin counts).** Confirmed (W3).

**N9 (a cut line that does not locate is still kept, `anchor_status: missing`).** Agreed [DOC: `findings.py:346-360` as cited by both]. It is a visible row where today there is none.

### 1.3 Positions where I still disagree with A

**Claims are not cut by default (C-001 claim part, C-009).** Strongest form of A: the claim is the reviser's reading aid, the verdict reads `blocking`, the cut is marked (`...`), recorded, and falsified by a two-judge test.
Answer, with data [RAN, P273]: (i) 12 dropped lines have a claim over 300 (8 blocking), lengths 303 to 401, median 339, one also with an anchor2 over 200. (ii) Cutting anchors only leaves 2 merges below the C-03 floor and 15 merges with a bad block (4 with the claim cut); the extra 3 blocking rows come from the claim cut; the verdicts of anchors-only and cut-all are identical on all 273 merges. (iii) Cutting anchors and admitting claims at 450 without any claim cut produces the same verdicts, blocking-row counts and bad-block count as cut-all (3 PASS to FAIL, 16 extra blocking rows, 4 merges with a bad block). So no verdict or quorum outcome on P273 needs a claim cut; a claim limit change gives it for free, and the decided brief change (CO-8; [DOC] the v1 loop brief states no claim limit, `document_review_loop_prompts.md:60` per both variants) attacks the cause. The meaning of a cut claim is unmeasured by anyone, the field carries "X is wrong because Y" ([DOC] same line), and an irreversible edit of that field buys 2 merges of quorum. I would accept A's claim cut only if A's K2 passes first (both judges), which A's own fallback already prefers.

**The refusal is more than insurance (C-004).** After the cut it fires on 0 of 273, but the cut cannot reach bad severity, bad refs, bad JSON or non-boolean `blocking` (4 of 90 lines here), and it is the only INV-I closure for a claim-only blocking drop when claims stay uncut. On P273 the anchors-only cut also fires 0 times (no verdict differs from cut-all), so the cost of keeping it is near zero and its guarantee does not depend on the corpus.

**Raise lever (C-011, U-011).** A is right that a raise relocates the cutoff and needs a measured admission curve. I keep it only for claims, as an owner decision, with the 12-line curve above as the evidence: a claim limit of 400 admits 11 of 12 (401 is the exception), 450 admits all 12.

## 2. Updated assessment of Variant 1

What A's defence settled for me: the cut of location fields is safe on the measured corpora (B's 89 of 89, my 70 of 70 verbatim over-limit fields with unique same-span prefixes), it is the only option that needs no transport (the v1 spec loop has none), it is the only position that was designed with a cost-side measurement, its `repair=False` keyword keeps every direct-parser pin literal, and its first-pass carrier is exact. A has also withdrawn "at most 4 residual lines", "INV-009 unchanged" and the copy-to-`refs` rule, which removes three of my Round 1 attack points.

What stays open on A: (1) the claim cut (above); (2) A's K1 is stated as "at least 90 percent of over-limit fields located and unambiguous": on P273 blocking fields are 34 of 37 (91.9 percent), and the 3 misses are fields that do not occur verbatim in the document at all, so the line as written tests reviewer fidelity, not the cut; it should be computed over fields whose full anchor locates (70 of 70 here); (3) the C-03 parameter "count only `repaired == 0` blocks for the floor, default off" leaves a policy knob that nobody can calibrate and would reopen the 10-merge problem if turned on; I would drop it and keep `repaired` as a recorded count only; (4) A's two adjudication-dependent claims (C-02 B2 and C-03 floor) rest on rules that those slots already settled, so A's design is only as safe as `ok` staying a parser verdict on the cut lines; that is acceptable but must be stated.

## 3. New evidence (code checks run now)

Method for all runs [RAN]: `git ls-tree -r` and `git cat-file --batch` at `6c0984326` under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`; `combos/<row>/<package>/ledger.json` for the three packages `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649`, `TASK-WF-design-20261108-041415`; rows filtered with audit-D's own exclusion pattern (`contaminated|superseded|quarantine|^i1-|^i2-`); reports taken from the last round's `report` paths; 279 merges found, 6 skipped because a report blob is absent from the commit, 273 analysed (855 reviewer-runs); HEAD `findings.parse_block`, `findings.locate`, `findings._check_finding` and `ledger.merge_round` imported read-only; every dropped line gets ALL its faults (audit-D's `check` returns the first only). Differences from audit-D (264 merges; 92 lines; 49 blocking; 80 ok-False runs): P273 has 90 lines (57 anchor first-fault, 18 anchor2, 11 claim, 3 severity, 1 refs), 46 blocking, 79 ok-False runs. I did not reconcile the 15-merge difference (audit-D's `exclude-list.txt` has 54 reviewer-level entries and I did not apply it) or the 3 claim and 1 anchor lines; the order of magnitude and every ranking below do not depend on it. Round-1-only ledgers: all P273 ledgers have one round (audit-D summary says so).

**E1. Recovery by policy (lines and blocking lines recovered of 90 and 46).** Cut all three fields 86 and 45; cut anchors only 74 and 37; cut anchors plus claim limit 450 86 and 45; claim limit 450 alone 11 and 8; raise anchors and anchor2 to 300 and claim to 450 82 and 44; raise to 250 and 350 70 and 38. Four lines are unreachable by any length policy (3 bad severity, 1 refs). Claim-dependent lines: 12 (8 blocking). Over-limit anchor and anchor2 lengths: median about 218, 72 of 76 at most 300, 4 above (301, 355, 467, 680) [RAN, first-pass listing, 76 fields in a slightly larger population].

**E2. Prefix location on P273.** 75 over-limit anchor and anchor2 fields: 70 occur verbatim after flattening, and for all 70 the 200-character prefix occurs exactly once with the same first span as the full anchor (blocking 34 of 37, non-blocking 36 of 38); 5 are not verbatim (3 blocking) and are missing under any policy. This reproduces B's 89 of 89 on a second population (audit-D's rather than the 1,215-report one) and is A's M1 on its own population. Limits: single-line tasklist rows only; code hunks and multi-line anchors untested.

**E3. Verdict simulation with HEAD `merge_round` (A's M2, first version).** Baseline re-merge equals the stored verdict in 273 of 273. Cut all: 3 verdicts change PASS to FAIL (exactly the three wrong PASSes), 16 merges gain 16 blocking rows and 21 rows in total, 13 of the 16 were already FAIL, no FAIL becomes PASS, 4 merges still have a bad block. Cut anchors only (claims at 300): the same 3 flips, 15 merges with a bad block, verdicts identical to cut-all in all 273 merges. Cut anchors with the claim limit at 450: identical to cut-all. Not measured: whether the 16 added blocking rows are true or false blockers (needs the judge in K3).

**E4. Floor and eligibility (C-03 floor `min(2, n)`, panel sizes above).** Merges below the floor: today's `ok` 10; with eligibility that tolerates dropped `blocking: false` lines 5; with a perfect re-ask on every length-only run 0; with the cut 0; with the anchors-only cut 2. Stored PASS with a dropped `blocking: true|unknown` line: 3. Merges carrying at least one dropped blocking line: 39 (so a re-ask on every such merge, B's Round 1 trigger, is 39 merges and 40 runs, 14 percent of merges). `blocking_state` `unknown` lines: 0.

**E5. Code facts.** `block_ok` is read only at `ledger.py:150` (and returned at `:295`) [READ, grep]; the clearing loop `:254-258` does not read it. `parse_block` v2 sets `state = invalid` on any dropped line (`findings_v2.py:298-304` [READ]) and `cluster._members` skips every record with `valid` False (`cluster.py:254-258` [READ]); `valid` is `block.get("state") == "complete"` at `cluster.py:219-221` [READ]. `cluster_cmd.py:151-163` [READ] carries one `block_state`. No parse-only v1 command exists (grep of registrations).

What I did not check: PR-code corpora; panel sizes of the 6 skipped merges; whether any E2 launcher depends on dropped lines; the true/false status of the 16 added blocking rows; reviewer behaviour under a changed brief or limit.

## 4. FINAL per-point table

"Moved" in the reason column marks a position that changed from Round 1.

| ID | Final winner | Conf. | One-line reason |
|---|---|---|---|
| S-001 | Hybrid | 78 | A's order (cut, parse, itemise, refusal-driven re-ask) for the three location fields; B's no-edit rule for claim and every other field; B's itemise-plus-refusal net (moved from B-led). |
| S-002 | Hybrid | 78 | A's `repair=False` keyword and one `repair_line` for anchor, anchor2, quote; B's additive `dropped` record with `blocking_state` and conservation test; A's derived `first_pass_state`. |
| S-003 | Variant 2 | 78 | B's replay and E1 table are the larger base; E2 above reproduces B's prefix result on audit-D's population (70 of 70). |
| S-004 | Hybrid | 82 | A's numeric kill lines and cost-side re-merge; B's pre-registration, conservation test and T-B5; K1 computed over verbatim fields. |
| S-005 | Variant 2 | 68 | B's invariant table is wider; keep A's "partly endangered" label for INV-C inside it. |
| S-006 | Neither | 60 | Presentation only; keep an open-facts section. |
| C-001 | Hybrid | 76 | By field: cut anchor, anchor2, quote (Variant 1); leave claim unedited (Variant 2). Moved. |
| C-002 | Hybrid | 74 | `ok` stays the parser's verdict on the cut lines (Variant 1); clearing and quorum use a derived eligibility that tolerates dropped `blocking: false` lines and fails on block-level faults or unresolved `true`/`unknown` drops (Variant 2 refinement). Moved. |
| C-003 | Variant 1 | 72 | `cluster.py:254-258` skips a whole reviewer; the cut removes that for anchor-class faults; claim faults stay a loss unit in v2 until the brief change, a limit or the re-ask works. |
| C-004 | Variant 2 | 80 | Refusal with acknowledgement adopted by both; fires 3 of 273 uncut, 0 after the anchor cut; kept for what the cut cannot reach. |
| C-005 | Hybrid | 76 | Re-ask only what remains; v1 trigger is the refusal (no pre-merge command exists), reflect keeps E1's rule plus invalid-block-with-prior; `blocking_state` gates. Moved. |
| C-006 | Hybrid | 74 | Stateless default prompt (Variant 1); reflect attempt 2 recorded before the `collected` commit, not after (`manifest.py:371-383`); v1 replacement report plus its sha; record shape is C-08's. |
| C-007 | Hybrid | 80 | A's mechanism, B's and E2's evidence (70 of 70, 89 of 89 verbatim fields keep their first span); A's 75 percent line for multi-line and code anchors. |
| C-008 | Hybrid | 70 | Record `refs_changed` only (A moved); copy rule only if M1 shows firing (B: 0 of 125). |
| C-009 | Variant 2 | 76 | No claim cut by default: no verdict or floor outcome needs it on P273, a claim limit reproduces it exactly, meaning is unmeasured. |
| C-010 | Hybrid | 70 | `repairs` item plus a rendered "shortened" note per cut anchor (Variant 1); nothing to mark for claims (Variant 2). |
| C-011 | Hybrid | 72 | CO-8 brief is common ground; no limit change by default; a claim-only raise to 450 is a separate owner lever (Variant 2, narrowed); pin cost 2 sites, 3 with `card_convert`. |
| C-012 | Variant 1 | 68 | The cut anchor is a flattened-form substring of the reported line, so `original_sha256` plus `report_sha256` keep provenance; the byte-copy objection applied to the claim cut, which is dropped. Moved. |
| C-013 | Hybrid | 76 | A's derived `first_pass_state` and `repairs` in both listings, checked by a differential test; B's by-construction safety holds for every uncut field. Moved. |
| C-014 | Hybrid | 62 | Quote prefix passes the substring test (`verify_cmd.py:68-72` [DOC]); quote limit a per-profile parameter; K1 at 75 percent for code until a code corpus exists; neither measured PR code. |
| X-001 | Variant 1 | 68 | The sentence is reflect step 4 only (`SKILL.md:343`), pinned (`test_shadow_skill_contract.py:230-232`), and a CLI parser step is not "the orchestrator"; additive sentence; owner confirms; fallback is v2 at `repair=False`. Moved. |
| X-002 | Neither | 65 | No recovery rate exists for gateway models; E1 is four confirmed of five, Agent path, one length cause. |
| X-003 | Hybrid | 72 | A's 4 is a floor and v1-only; reflect's residual is non-length for both policies; B's 44 re-ask runs are 40 runs and 39 merges on P273 and fall to the refusal-driven few in v1. |
| X-004 | Hybrid | 82 | Both hold only if first-pass state is carried: `first_pass_state` plus `repaired_lines_rate` and `dropped_lines_rate`. |
| U-001 | Variant 1 | 76 | The keyword keeps four direct-parser pins literal and answers C-01 INV-003; add a test that every production call site passes it. |
| U-002 | Hybrid | 66 | `refs_norm` exposure is real in principle, 0 of 125 measured: record, do not copy. |
| U-003 | Variant 1 | 85 | Cost-side re-merge is the only measurement that can show harm; first run above: 3 flips, 16 extra blocking rows, judge still needed. |
| U-004 | Variant 1 | 76 | `repaired_lines_rate` per model; add B's `dropped_lines_rate`. |
| U-005 | Hybrid | 72 | Valid only in an open reflect stage for a non-`complete` earlier attempt; v1 has no manifest. |
| U-006 | Variant 2 | 82 | Adopt the replay and the admission curve as base data; E2 corroborates on a second population. |
| U-007 | Variant 2 | 70 | Adopt, restated as four confirmed, one unconfirmed, Agent path. |
| U-008 | Variant 2 | 80 | Refusal with acknowledgement; now executed: 3 of 273 uncut, 0 cut. |
| U-009 | Variant 2 | 78 | `blocking_state` and the conservation property; `unknown` has 0 members on P273. |
| U-010 | Variant 2 | 68 | E2 design-review findings and T-B5: the re-ask holds only the reviewer's own block and grants no tool. |
| U-011 | Variant 2 | 62 | A separable owner lever, narrowed to claims; E1 gives its admission curve (12 of 12 at 450). |
| A-001 | Neither | 75 | QUALIFY: audit-D and P273 order the policies but differ in count (90 versus 92, 46 versus 49 blocking, 79 versus 80 runs); freeze one population before any percentage. |
| A-002 | Neither | 80 | ACCEPT for verbatim single-line anchors (70 of 70, 89 of 89); open for multi-line and code; unlocated rows exist under any policy. |
| A-003 | Neither | 70 | REJECT stationarity: CO-8 changes the claim rate and any lever changes more; write the policy to hold in both directions. |
| A-004 | Hybrid | 80 | ACCEPT, quantified: today's code never reads `block_ok` in clearing; C-02 B2 and C-03 make it load-bearing and put 10 of 273 merges below the floor under a bare `ok`. |
| A-005 | Hybrid | 76 | QUALIFY: true only while shadow lasts; leaving shadow needs `first_pass_state` carried and the exit script re-checked. |
| A-006 | Hybrid | 78 | REJECT the unconditional form; accept reflect-only, open stage, non-`complete` earlier attempt; v1 record is the replacement report. |

## 5. Where I moved from Round 1, and why

1. S-001, C-001: from "no edit by default" to "cut the three location fields". Reason: E2 and B's own replay (prefix keeps the first span), no verdict cost beyond the three recoveries (E3), no v1 transport for a re-ask (N1), and 10 of 273 merges below the floor under no-edit (E4).
2. C-002: from "B plus a re-ask amendment" to Hybrid with a derived eligibility. Reason: 35 of the 79 ok-False runs have only `blocking: false` length drops and no re-ask path.
3. C-012, X-001: from Variant 2 to Variant 1. Reason: the stored anchor stays a flattened-form substring; the sentence is reflect-only and pinned.
4. C-013: from Variant 2 to Hybrid. Reason: A's carrier is exact and testable.
5. C-005, C-006: v1 re-ask is refusal-driven; reflect re-ask is recorded before the stage commit. Reason: N1, W5.
6. C-011, U-011: raise lever narrowed from anchors-and-claims to claims. Reason: the cut covers anchors; pin count corrected.
7. Withdrawn: "stall exposure is small" (Round 1 section 8, answer 1) and my four-pin count.
8. Unchanged: C-004, U-008, U-009 (refusal and `blocking_state`), C-009 (no claim cut), S-003, A-003.

## 6. Proposed resolution text (12 bullets)

1. **(a) Cut location fields, in code, behind a keyword.** Both `parse_block` functions take `repair=False`; `ledger.py:128`, `cluster_cmd.py:151` and `verify_cmd.py:133` pass `repair=True` (a test checks every production call site). One pure `repair_line(obj)` in the limits module cuts `anchor`, `anchor2` and a citation `quote` to the first 200 characters of the flattened form, before `_check_finding` and `check_finding`. It touches no other field and no `prior` line. Direct-parser pins stay unmodified.
2. **(a) No other field is ever cut; everything dropped is itemised.** `claim`, `refs`, `severity`, `blocking` and `category` are never edited. Each cut and each residual drop becomes `{line, finding_id, blocking_state (true, false, unknown), rule, field, original_chars, kept_chars, original_sha256}`, never reviewer text; the report is never edited; a conservation test holds per block (non-blank lines = kept + priors + dropped); the merged report's `### Lx` block prints "shortened from N" beside the anchor status.
3. **(b) Re-ask trigger.** Only for what remains invalid after the cut. v1: the trigger is a refusal (bullet 7 or the C-03 quorum refusal), because no parse-only command exists and a merged round cannot be merged again (`ledger.py:114-118`, `merge_cmd.py:99-118`). Reflect: E1's rule (an invalid block gets one bounded re-ask) plus an invalid block that carries a `prior` line. Dropped `blocking: false` lines are itemised, never re-asked.
4. **(b) Transport and record.** Stateless prompt by default: the original brief, the reviewer's own block and the parser's per-line errors, whole block returned; no other reviewer's content, no new tool grant, no `--resume` dependency. Reflect records attempt 2 before the `collected` commit and only while the earlier attempt is not `complete` (`manifest.py:371-383`); v1 records the replacement report and its `report_sha256` in that round's entry. Record shape belongs to C-08. A transport that cannot re-ask degrades to itemise plus the refusal.
5. **(c) `block_ok` and eligibility.** `ok` (v1) and `state` (v2) stay the parser's verdict on the cut lines: a block whose only faults were length faults on location fields is `ok` and `complete`. For clearing (C-02 B2) and the floor (C-03) a reviewer counts iff it has no block-level fault, no non-length drop on a `true` or `unknown` line, and no unresolved dropped line with `blocking_state` `true` or `unknown`; dropped `blocking: false` lines do not disqualify. `repaired` and `dropped` counts are recorded beside `block_ok`; no policy knob for counting only `repaired == 0` blocks.
6. **(d) First-pass carrier.** The parse result gains `repairs`, `dropped` and `first_pass_state` (`state` unless complete, else `invalid` when `repairs` is non-empty); `cluster_cmd.py:155-163` and `verify_cmd.py:136-138` emit them beside the unchanged `state`; `findings_block_compliance_rate` is the share of cards whose `first_pass_state` is complete; a differential test against a `repair=False` parse shows zero mismatches; `repaired_lines_rate` and `dropped_lines_rate` per model are reported next to it.
7. **(e) Dropped-blocking refusal.** At the end of `merge_round`, after the quorum check and on a working copy swapped in on success (pins `test_review_ledger.py:352-361,373`), if the derived verdict is PASS and an unacknowledged dropped line has `blocking_state` `true` or `unknown`, raise C-03's refusal subtype with exit 12 and `{"refusal": "dropped_blocking", reviewers, dropped}`; the ledger file is unchanged. An owner-and-reason acknowledgement option on `merge` lifts it, is recorded and listed in the report. No refusal when a blocking row survives; the dropped ids are printed.
8. **(f) Raise lever.** Not part of the default policy. The briefs state the limits from the constants (CO-8, decided). A claim-only raise to 450 is a separate owner decision, admitted by the measured curve (12 of 12 claim lines at 450, 11 of 12 at 400), costing 2 assertion sites (`test_review_findings.py:117`, `test_review_findings_v2.py:241`) and 3 with `card_convert.py` (`test_review_card_convert.py:500`); anchors are never raised.
9. **(g) Measurements, rules written to a file before the first run.** M1 offline replay of the cut on two frozen populations (audit-D, and the 1,215-report corpus), reporting lines passing the parser, fields locating uniquely over fields whose full anchor locates, `refs_changed`, and the residual by rule. M2 re-merge with repair on and off, counting added blocking rows judged false by a blind judge and PASS-to-FAIL flips (first run: 3 flips, 16 extra blocking rows). M3 stateless re-ask on the residual lines per transport. M4 unit tests: no-op on every valid fixture line, boundaries 200/201 with and without repair, idempotence, no invented anchor, conservation, differential first-pass, merge matrix (one reviewer all dropped; one dropped blocking plus one empty block; surviving blocking row; only `blocking: false` drops; acknowledged drops; below-floor panels of sizes 1 to 5).
10. **(g) Kill lines (owner may change the numbers before the first run).** K1: fewer than 90 percent of over-limit location fields that occur verbatim in the document keep a unique same-span prefix (75 percent on a code or multi-line corpus) demotes that field class to itemise plus re-ask. K2: a claim cut is allowed only if both judges mark at most 20 percent of blocking claims as losing a decision-relevant clause. K3: the cut is wrong if the added blocking rows are judged false more than 10 points above the base rate of kept blocking rows, or any merge flips PASS to FAIL through a false repaired row the cap of 3 reviews cannot clear. K4: the re-ask half is wrong if recovery is under 60 percent over at least 20 residual lines or any re-ask changes an unlisted line. K5: the refusal is wrong if it fires on more than 5 of 273 merges after the cut or any refusal lacks a re-ask or an acknowledgement exit.
11. **(h) `SKILL.md:343`.** Leave the Normalize sentences byte-identical (pinned at `tests/cli/reflect/test_shadow_skill_contract.py:230-232`); add one sentence after them: the package's parser step shortens location fields in code and records every shortening, the orchestrator still never edits a finding, and the first-parse compliance rate reads `first_pass_state`. The owner confirms that package code is not "the orchestrator"; if not, the v2 call sites stay at `repair=False` (itemise and re-ask only) and the v1 `merge` keeps the cut, because no text rule binds it.
12. **Pins and the third copy of the constants.** `card_convert.py` imports the shared constants and keeps its marked claim cut as a legacy conversion measure; the merged text names it as the one explicit exception to "no claim cut" so the package carries no silent split. The three production call sites passing `repair=True` rewrite no pin; a test asserts the default stays `False`.

## Round 2.5: Invariant Probe

See `invariant-probe.md` (summary) and `round2.5-fault-finder-raw.md` (full). 26 findings; HIGH + UNADDRESSED: INV-001, INV-017, INV-018, INV-023.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L2 | Hybrid | 77% | Both: A's order (cut, parse, itemise, refusal-driven re-ask) with B's itemised record and PASS-by-loss refusal. |
| S-002 | L2 | Hybrid | 79% | Both: A's `repair=False` keyword + one `repair_line`, B's additive `dropped` record with `blocking_state`, A's derived `first_pass_state`. |
| S-003 | L2 | Variant 2 | 78% | Both: B's 5,270-line replay and E1 table are the larger base; B's second-population run reproduced 70 of 70. |
| S-004 | L2 | Hybrid | 82% | Both: A's numeric kill lines and cost-side re-merge plus B's pre-registration and conservation tests. |
| S-005 | L2 | Variant 2 | 69% | Both: B's invariant table is wider; keep A's "partly endangered" INV-C label. |
| S-006 | L1 | Neither | 60% | Presentation only; both would keep an open-facts section. |
| C-001 | L3 | Split (no majority) | 55% | A: Variant 1 (72), B: Hybrid by field (76). Both cut anchor, anchor2, quote; they differ on cutting the claim. |
| C-002 | L3 | Split (no majority) | 55% | A: Variant 1 (80): `ok`/`complete` of the repaired parse. B: Hybrid (74): derived eligibility that tolerates dropped `blocking: false` lines. |
| C-003 | L3 | Variant 1 | 74% | Both: `cluster.py:255-257` skips a whole reviewer; the cut removes that only for the length share. |
| C-004 | L3 | Variant 2 | 79% | Both: adopt B's `dropped-blocking` refusal with acknowledgement; fires 0 of 264/273 after the cut (insurance). |
| C-005 | L3 | Hybrid | 75% | Both: re-ask only what remains; v1 trigger is the refusal, reflect keeps the E1 rule plus invalid-block-with-prior. |
| C-006 | L3 | Hybrid | 73% | Both: stateless prompt; attempt 2 before the `collected` commit; v1 record is the replacement report and its sha. |
| C-007 | L3 | Hybrid | 80% | Both: B's replay (89 of 89; 70 of 70) as evidence, A's 75 percent kill line for multi-line and code anchors. |
| C-008 | L3 | Hybrid | 70% | Both: record `refs_changed` only; copy rule only if M1 shows firing. |
| C-009 | L3 | Split (no majority) | 55% | A: Hybrid (62) cut claim with marker and judge falsifier. B: Variant 2 (76) no claim cut by default. |
| C-010 | L1 | Hybrid | 71% | Both: `repairs` item plus a rendered "shortened" note per cut. |
| C-011 | L3 | Hybrid | 71% | Both: CO-8 briefs common ground; raise is a separate owner lever (B narrowed to claims). |
| C-012 | L3 | Split (no majority) | 55% | A: Hybrid (70) original_sha256 plus report_sha256. B: Variant 1 (68), same mechanism once the claim cut is dropped. |
| C-013 | L3 | Hybrid | 76% | Both: derived `first_pass_state` and `repairs` in both listings, differential test. |
| C-014 | L2 | Hybrid | 63% | Both: quote prefix passes the substring test; per-profile limits; no PR-code corpus yet. |
| X-001 | L2 | Variant 1 | 67% | Both: `SKILL.md:343` is reflect step 4 only and pinned; additive sentence; owner confirms; fallback v2 `repair=False`. |
| X-002 | L3 | Neither | 64% | Both: no recovery rate exists for gateway models; E1 is four confirmed of five. |
| X-003 | L3 | Hybrid | 72% | Both: A's "4 of 92" is a floor and v1-only; reflect's residual is non-length for both policies. |
| X-004 | L3 | Hybrid | 82% | Both: honest only if first-pass state is carried. |
| A-001 | L2 | Neither (QUALIFY / QUALIFY) | 75% | Both: audit-D and P273 order the policies but cannot give a recovery percentage. |
| A-003 | L3 | Neither (REJECT / REJECT) | 71% | Both reject reviewer-behaviour stationarity (CO-8 changes the claim rate). |
| A-005 | L3 | Hybrid (QUALIFY / QUALIFY) | 76% | Both: holds only while shadow lasts; leaving shadow needs `first_pass_state`. |
| A-006 | L3 | Hybrid (REJECT unconditional / narrow form accepted) | 78% | Both: reflect-only, open stage, non-`complete` earlier attempt; v1 has no manifest. |

Unique-contribution rows U-001..U-011 are not counted in the convergence denominator (protocol: S, C, X, A only). Both advocates' final tables agree on every U row in substance: U-001, U-003, U-004 to Variant 1; U-006..U-009, U-011 to Variant 2; U-002, U-005 Hybrid; U-010 Variant 2.

Shared-assumption responses (every required A-NNN addressed by both advocates; omissions: none): A-001 QUALIFY/QUALIFY; A-003 QUALIFY->REJECT (A moved in Round 2) / REJECT; A-005 QUALIFY/QUALIFY; A-006 REJECT as written / QUALIFY then narrow form accepted by both. Optional A-002 and A-004 also answered by both.

Per-point tally of clean winners: Variant 1: 2 (C-003, X-001); Variant 2: 3 (S-003, S-005, C-004); Hybrid: 15; Neither: 4; Split: 4.

## Convergence Assessment
- Points resolved: 24 of 28
- Alignment: 85.7%
- Threshold: 80%
- Taxonomy coverage: L1 = 2 points (S-006, C-010), L2 = 8 (S-001..S-005, C-014, X-001, A-001), L3 = 18; all three levels covered, no forced round needed
- Invariant probe gate: 26 findings, 20 UNADDRESSED; HIGH + UNADDRESSED = 4 (INV-001, INV-017, INV-018, INV-023); MEDIUM + UNADDRESSED = 12 (warnings)
- Status: BLOCKED_BY_INVARIANTS (agreement 85.7% >= 80% and taxonomy covered, but 4 HIGH-severity UNADDRESSED invariants exist; --depth standard has no Round 3, so none was resolved in debate)
- Unresolved points: C-001, C-002, C-009, C-012 (all four turn on the same two questions: whether the claim field is cut, and whether clearing and quorum eligibility is the bare parser bit or a derived rule)
- Oscillation: none detected; both advocates moved toward the same hybrid between Round 1 and Round 2 (A: withdrew "at most 4 residual", "INV-009 unchanged", copy-to-refs; B: withdrew "no edit by default" for the three location fields, the four-pin count and "stall exposure is small")
