# Merge Execution Log

## Metadata
- Base: Variant 1 (option a: keep the Ruling rule; the person gives the Ruling in their own session)
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (13 changes, auto-approved after an independent review, 2026-11-02T18:30Z)
- Output: `merged-output.md` (this directory)
- Changes applied: 13 of 13
- Status: success
- Timestamp: 2026-11-02T18:19:52Z (merge started 2026-11-02T18:14:25Z, the date in the paper's provenance header)
- Citation key used below: as in `merged-output.md` (`SPEC`, `QA`, `LEDGER`, `RETRY`, `SKILL`, `IMPL`, `CAPS`, `CR-01`). `V<n> L<k>` = line k of variant n.

## Changes Applied

Applied in plan order. "This plan's, not debated" labels from the plan are kept visible in the paper as "(added in the merge; not debated)".

### Change 1: Restate the position as (a)+(c)
- **Status**: Applied
- **Source**: Round 2 recommendations of all three advocates (`debate-transcript.md:390,469,552`)
- **Target**: Base, title and Position paragraph (V1 L1, L3)
- **Before**: Title "D2 option (a): keep the Ruling rule; the person gives the Ruling in their own session"; Position = (a) only, "the spec's current recommendation".
- **After**: Title "D2 merged position: keep the Ruling rule; (a) by default, (c) as the way back into Orca; reject (b)". Position keeps V1's halt-behaviour sentence (`SPEC:335`, `SPEC:67`) and lists (a) as default and the only route for `dispute` (`SPEC:337`), (c) as the way back into Orca, (b) rejected (`SPEC:336`); cites the unanimous Round 2 result.
- **Provenance tag**: `<!-- Source: Base (original, modified) — title and Position restated as (a)+(c) per Change #1 (unanimous Round 2 result; resolves X-002 and S-005) -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:335,336,337`; `debate-transcript.md:390,469,552` re-read) | Contradictions ✅

### Change 2: Citation key, anchor drift note and PR #343 note
- **Status**: Applied, with one accuracy adjustment (below)
- **Source**: V1 L5-L7; `diff-analysis.md` citation key; K3; plan "Citation corrections" table
- **Target**: Base, citation key and drift paragraph (V1 L5-L7)
- **Before**: Key with `SPEC`, `QA`, `LEDGER`, `RETRY` only (`SPEC` = "spec line"); drift note naming only `SPEC:334`.
- **After**: Key gives full paths for `SPEC`, `QA`, `LEDGER`, `RETRY`, `MW`, `SKILL`, `IMPL`, `CAPS`, `CR-01`, and says bare `debate-transcript.md:N` and `invariant-probe.md` are files in the debate directory. Drift note lists every stale spec anchor from the plan (`SPEC:334`, `SPEC:67`, `SPEC:185`, `SPEC:319`, `SPEC:132`, `SPEC:14`) and the correct targets (`QA:254`, `QA:247-249`, `QA:247-256`). New paragraph on the installed copy lagging PR #343.
- **Adjustment**: the plan says "every line D2 cites is byte-identical in both copies". A numbered diff run in this merge shows the installed copy differs at `QA:267`, `LEDGER:143` and `RETRY:141-142,147-149,189,193`, and the paper cites `QA:267` and `RETRY:142` (K3) precisely to show the change. The sentence therefore reads "Apart from `QA:267` and `RETRY:142` ... every line cited here is byte-identical". Line numbers align in all four files (no insertions or deletions). `MW` is defined in the key as the plan's Change 2 lists it, but no section cites it.
- **Provenance tag**: `<!-- Source: Base (original, modified) — citation key extended and drift note widened per Change #2 (S-003 kept; K3 installed-copy note added) -->`
- **Validation**: Structural integrity ✅ | References ✅ (`SPEC:14,67,132,185,319,334` re-read; each cites the old `qa.md` anchor) | Contradictions ✅

### Change 3: Add route (c), corrected
- **Status**: Applied
- **Source**: Variant 3, Position (L3) and "Why this works with no protocol change" (L7-L10)
- **Target**: Base, new section "Route (c): hand-written Ruling, then a resume Task", directly after Safety
- **Before**: Section did not exist.
- **After**: Six bullets: line format (`LEDGER:65,71`); current grammar admits it (`LEDGER:110`) but the spec needs one sentence (SC-2 correction); both eligibility clauses (`RETRY:498`); row R before P and H, no review (`LEDGER:149-156`), implicit `--resume` (`IMPL:57`); malformed last line stops at `E-LEDGER-CORRUPT` (`LEDGER:123`, `SKILL:36`; SC-4 correction); ineligible line ignored (`RETRY:500`) and falls to row H (`LEDGER:141,156`), against `QA:283`, so (c) needs the following three sections.
- **Provenance tag**: `<!-- Source: Variant 3, Position (L3) and "Why this works with no protocol change" (L7-L10) — merged per Change #3, corrected for spot-checks SC-2 (OVERSTATED) and SC-4 (WRONG) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (V3's "ignored" claim is not carried over)

### Change 4: Coordinator rules after an `/sc:implement` stop
- **Status**: Applied
- **Source**: Round 2 recommendations (V1 new evidence 1, V2 contract fields, V3 response 9); `invariant-probe.md` INV-002, INV-005, INV-023
- **Target**: Base, new section "What the coordinator does after the halt"
- **Before**: Section did not exist.
- **After**: Three "why" bullets (`SPEC:84`, `IMPL:57`, `LEDGER:155-156`, `QA:283`; `SPEC:68`, `RETRY:494`, `SKILL:42`; memory-only freeze) and rules (i)-(v) as written in the plan. Labels kept: (i)'s STOP-code field, (ii), (iv), (v) "(added in the merge; not debated)"; (iii) and (i)'s ledger path and worktree marked debated. Cross-references "Change 5" and "Change 8" were rewritten as the section names "The check before a resume Task" and "How a person works day to day", because the paper has no change numbers.
- **Provenance tag**: `<!-- Source: Variant 1, Variant 2 and Variant 3 Round 2 recommendations (show-and-freeze; contract carries ledger path and worktree) plus invariant-probe.md fix shapes for INV-002, INV-005, INV-023 — merged per Change #4 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: The read-only pre-dispatch check for route (c)
- **Status**: Applied
- **Source**: V3 R2 recommendation item 3; V1 R2 new evidence 2; V2 R2 ("test both clauses"); `invariant-probe.md` fix shapes
- **Target**: Base, new section "The check before a resume Task", after the coordinator section
- **Before**: Section did not exist.
- **After**: Scope sentence (route (c) only; (a) has its own hand-back check), three "load-bearing" bullets from the plan's rationale (`LEDGER:141,156`, `QA:283`; `LEDGER:71,154`; `LEDGER:82,154`, `RETRY:229,492`, `LEDGER:93`, `RETRY:44,456`), conditions (1)-(7) and the failure rule. Debated scope stated once; each undebated part labelled per condition ((2)'s anchor, count and newline rules; (3); (5)'s three extra reasons; (6); (7)).
- **Provenance tag**: `<!-- Source: Variant 3 Round 2 recommendation item 3, Variant 1 Round 2 new evidence 2, Variant 2 Round 2 ("test both clauses") plus invariant-probe.md fix shapes for INV-006, INV-007, INV-011, INV-012, INV-014, INV-022 — merged per Change #5; replaces Variant 3's Round 2 porcelain guard (INV-020) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: Placement and the frozen worktree
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-001, INV-018, INV-019, INV-020; V3 R2 new evidence 1; `CR-01:16-23,41`
- **Target**: Base, new section "Where the resume runs"
- **Before**: Section did not exist.
- **After**: Four "why" bullets (`LEDGER:3`; `RETRY:500`, `LEDGER:154`; porcelain guard dropped, `LEDGER:3`; CR-01 T2, `CR-01:18`) and rules (i)-(vi) as written in the plan, labelled "(added in the merge; not debated, except the idea of a drift check, which is Variant 3's)".
- **Provenance tag**: `<!-- Source: invariant-probe.md fix shapes for INV-001, INV-018, INV-019, INV-020, Variant 3 Round 2 new evidence 1 (the drift-check idea only) and CR-01 (K1, K4) — merged per Change #6 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: Implement worker briefs use a file or managed source
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-017
- **Target**: Base, section "Where the resume runs" (appended rule)
- **Before**: Rule did not exist.
- **After**: One bullet "Implement worker briefs (added in the merge; not debated)" with its reason (`SKILL:61`, `SKILL:52`, `SKILL:50`, `SPEC:274`, `SPEC:70`, `SKILL:64`) and four sub-bullets: Wave 0 options in P4 (`SPEC:132`), options before the source, file or managed source only, AC-4.1 same-ledger-path assertion.
- **Provenance tag**: `<!-- Source: invariant-probe.md fix shape for INV-017 — merged per Change #7 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ after the Change 13 consistency fix (see Post-Merge Validation)

### Change 8: Hand-back after route (a) and single writer in both directions
- **Status**: Applied
- **Source**: `invariant-probe.md` INV-003, INV-004; V1 R2 responses 2 and 6; V3 L14
- **Target**: Base, section "How a person works day to day" (appended)
- **Before**: The section ended with "the remaining tasks of that plan leave Orca".
- **After**: Block "Single writer and the hand-back after (a)" with the no-lock fact (`LEDGER:145`) and rules (i)-(iv): (i) marked debated; (ii)-(iv) "(added in the merge; not debated)" (`SPEC:70`, `QA:248`, `QA:256`, `LEDGER:123`, `LEDGER:153`).
- **Provenance tag**: `<!-- Source: invariant-probe.md INV-003, INV-004; Variant 1 Round 2 responses 2 and 6; Variant 3 Safety (L14) — appended per Change #8 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Day-to-day text covers both routes and (c)'s weakness
- **Status**: Applied
- **Source**: V3 L19-L21; V3 R2 response 1 and new evidence 2
- **Target**: Base, section "How a person works day to day" (V1 L17-L19 replaced)
- **Before**: Two bullets: the person opens the ledger and resumes in their own session; "the remaining tasks of that plan leave Orca".
- **After**: Five bullets: the coordinator shows the full halt text (`RETRY:490`, `QA:247`); (a) gives the executor's scoped explanation (`QA:254-256`); (c) is typed by the person, format only, never pre-filled words; (c)'s weakness stated plainly (`QA:254`, `LEDGER:65`), (a) one choice away; cost per halt, with the plan staying in Orca under (c) and under (a) unless handed back.
- **Provenance tag**: `<!-- Source: Variant 3, "How a person works day to day" (L19-L21) and Variant 3 Round 2 response 1 and new evidence 2 — replaces Base L17-L19 per Change #9 (C-003 kept: only (a) gives the executor's explanation) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (base "leave Orca" sentence removed by the replacement)

### Change 10: Safety additions
- **Status**: Applied
- **Source**: V3 L13-L14; diff point A-010
- **Target**: Base, section Safety (V1 L9-L11, appended)
- **Before**: Two base bullets.
- **After**: Base bullets unchanged, plus two bullets: a coordinator- or worker-written or drafted line is "executor-invented approval" (`QA:249`); eligibility is positional only (`RETRY:498`), so who typed the line is policy, an accepted residual risk as for operator-written lines today (`LEDGER:195`). The plan's integration point names these two bullets; the no-lock precondition it mentions in its rationale is placed by Change 8.
- **Provenance tag**: `<!-- Source: Variant 3, Safety (L13) and diff point A-010 — merged per Change #10 -->` (base bullets keep `<!-- Source: Base (original) -->`)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Reliability adds V3's AC-4.1 extension
- **Status**: Applied
- **Source**: V3 L17
- **Target**: Base, section Reliability (appended)
- **Before**: AC-4.1 checked only the halt.
- **After**: Bullet with the five-step return path (`QA:248`, `LEDGER:82`) and the Orca-created worktree (K1, `CR-01:41`, superseding `SPEC:235`), with the resume Task run in that same worktree before removal.
- **Provenance tag**: `<!-- Source: Variant 3, Reliability (L17) — merged per Change #11, adjusted for K1 and INV-018 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: Record (b) as rejected
- **Status**: Applied
- **Source**: V2 L13-L14; V2 R2 recommendation and new evidence 1, 2, 4
- **Target**: Base, new section "Why not (b)", placed directly before Implementation cost
- **Before**: Section did not exist.
- **After**: Six bullets: relayed reply is the coordinator's message (`CAPS:62`, `QA:254`, `QA:249`); weaker scope check; one ask per Task cannot clarify (`QA:254`, `SPEC:67`); late answer collapses into (c) (`SPEC:67`); dispute needs the advice file (`RETRY:107`, `QA:281`); V2 withdrew (`debate-transcript.md:469`) and (b) is only a later explicit opt-in, never for `reason=dispute`.
- **Provenance tag**: `<!-- Source: Variant 2, Safety (L13-L14) and Variant 2 Round 2 recommendation and new evidence 1, 2, 4 — merged per Change #12 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 13: Implementation cost and frequency, updated for K3
- **Status**: Applied, with two consistency adjustments (below)
- **Source**: V1 L15, L21-L22; V3 L23-L24; V3 R2 response 13; K3
- **Target**: Base, Reliability bullet 2 (V1 L15) and Implementation cost (V1 L21-L22), both replaced
- **Before**: "Halts are rare by design" (no K3); "Zero change to `sc-implement-protocol`".
- **After**: Reliability bullet 2 adds K3 (`QA:274`, `QA:288`, `QA:280`, `RETRY:142`) and the UNVERIFIED frequency note. Implementation cost: zero edits to `qa.md`, `ledger.md`, `retry.md`; spec-text list; V3's "(a) stays available unchanged"; base reversibility sentence kept.
- **Adjustments**: (1) the cost list also names the one `SKILL.md` Wave 0 change that Change 7 makes a required P4 change, so "zero edits" is scoped to the three refs files and does not contradict Change 7; (2) the plan's "one new AC step" is worded "one AC-4.1 extension", because Changes 7 and 11 add a five-step return path and a same-ledger-path assertion.
- **Provenance tag**: Reliability bullet: `<!-- Source: Base (original, modified) — bullet 2 rewritten per Change #13 to cover K3 -->`; cost section: `<!-- Source: Base (original, modified) — replaced per Change #13 (Base L21-L22 and Variant 3 L23-L24, updated for K3); the SKILL.md Wave 0 line is carried from Change #7 and "one new AC step" is worded as one AC-4.1 extension to match Changes #7 and #11, so this section does not contradict them (post-merge consistency fixes) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ after the adjustments

### Additions required by the merge brief (not numbered changes)
- **Fixed constraints K1-K4**: new section "Fixed constraints" after the citation block, text from the plan's Overview, labelled "not debated; applied as given" (`CR-01:41,45,3,18,23`; `SPEC:235`; `QA:267`; `RETRY:142`). Tag: `<!-- Source: refactor-plan.md, Overview, fixed constraints K1-K4 ... -->`.
- **Residual risks R1 and R2**: new last section "Accepted residual risks", text from the plan's "Invariant coverage". Tag: `<!-- Source: refactor-plan.md, "Invariant coverage" residual risks R1 and R2 ... -->`.

## Post-Merge Validation

All checks below were run in this merge on the final `merged-output.md` (148 lines), with `grep`/`sed` over the file and the cited sources.

### Structural Integrity
- Heading hierarchy: ✅ One H1 (line 5), 11 H2, zero H3 or deeper, so no level gaps and no orphan H3. Zero `TODO` placeholders left.
- Section ordering: ✅ Position, citation key and drift note, Fixed constraints, Safety, Route (c), What the coordinator does after the halt, The check before a resume Task, Where the resume runs, Reliability, How a person works day to day, Why not (b), Implementation cost, Accepted residual risks. The route-(c) mechanism (line 39) comes before the check that guards it (line 62); Route (c) sits directly after Safety (Change 3); the check follows the coordinator section (Change 5); "Why not (b)" sits directly before Implementation cost (Change 12).
- Document flow: ✅ Every section carries a `<!-- Source: ... -->` tag (18 tags). Forward references (the check's condition 6 and the coordinator rule v pointing to later sections) are by section name and resolve.

### Internal References
- Citation prefixes used in prose: `SPEC`, `QA`, `LEDGER`, `RETRY`, `SKILL`, `IMPL`, `CAPS`, `CR-01`. All are defined in the paper's citation key; no unknown prefix found. `MW` is defined but unused (harmless; the plan's Change 2 lists it). Bare `debate-transcript.md:N` (2 tokens) and `invariant-probe.md` are defined in the key.
- Total references: 128 citation tokens (74 distinct) plus 2 debate-transcript tokens; 9 quoted section-name cross-references, 3 "rule i-vi" cross-references, 4 K-constraint references, and 2 named-section references ("Fixed constraints, K3", "Reliability").
- Resolved: all. No "Change N" text remains in the prose (the plan's "Change 5"/"Change 8" cross-references were rewritten as section names).
- Broken: 0.
- Cited source lines re-opened in this merge (25; the first 15 by a phrase-match script, all 15 OK; the rest re-read with Read or `sed -n` in this run):
  1. `SPEC:68` has "`reason` when failed" (Change 4 i).
  2. `RETRY:494` has "Re-run the same command; do not write a Ruling." (Change 4).
  3. `SKILL:42` is the `E-ARCHIVE-BLOCKED` row (Change 4).
  4. `LEDGER:155` row P appends "halt review=2 reason=operator-review" (Change 4 ii).
  5. `QA:283` "never started by automation" (Changes 3, 4, 5).
  6. `RETRY:229` `no-evidence` is terminal and the operator path is "Resume row H" (Change 5).
  7. `RETRY:44` writes `no-snapshot`/`head-moved` "on a resume through row O" (Change 5).
  8. `RETRY:456` "`no-evidence` | revert guard for n = 3, 4, 5" (Change 5).
  9. `SKILL:50` "`--force` as an option token → STOP `E-NO-RULING`"; known options exclude `--unattended` and `--report-dir` (Changes 5, 7).
  10. `SKILL:114` writes `<retries>/T<id>/q0-head` only for a tree snapshot (Change 6 ii).
  11. `RETRY:41` "HEAD has not moved ... equals the 40-hex in `<retries>/T<id>/q0-head`" (Change 6 ii).
  12. `QA:202` a `nogit` or HEAD-fallback start "has no `q0-head`" (Change 6 ii).
  13. `RETRY:433` `r<k>-<j>` refs "also deleted at `complete`", so kept until then (Change 6 ii).
  14. `SKILL:61` inline prompt slug uses "SHA-256 of the **full** prompt" (Change 7).
  15. `LEDGER:153` row 1 "Latest verdict is `complete` | Skip" (Change 8 iii).
  16. `QA:178-179` reviewed trees pinned as `r<k>-<j>` and re-pinned on resume (Change 6 ii).
  17. `SKILL:52` tokens after the first non-option token are source or prompt text (Change 7).
  18. `SKILL:64` file slug hashes the absolute path; managed ledger is `<package>/progress.md` (Changes 6 iv, 7).
  19. `SPEC:132` implement row says "none on the happy path" and cites `qa.md:231-238` (Changes 2, 7).
  20. `SPEC:274` AC-4.1 command puts `--unattended --report-dir` after `<plan>` (Change 7).
  21. `SPEC:70` "No retry while the earlier attempt is not settled"; each retry gets its own report directory (Changes 3, 5, 7, 8).
  22. `LEDGER:3` legacy ledger never `git add`ed; managed ledger under `.dev/tasks/`, always staged (Change 6).
  23. `RETRY:492` the two resume-time exceptions for revert-guard halts (Change 5).
  24. `LEDGER:123-129` resume pseudo-code with the `E-LEDGER-CORRUPT` last-line test (Changes 3, 4 iv).
  25. `CR-01:18` trigger T2; `CR-01:41` location resolved to Orca defaults; `CR-01:45` upstream never touched; `CR-01:3` "Status: PROPOSED"; `CR-01:23` merge-back by the git owner (K1-K4, Change 6).
- Installed-copy check (Change 2): numbered `diff` of source against `~/.claude/skills/sc-implement-protocol/` for `qa.md`, `ledger.md`, `retry.md`, `SKILL.md`: differences only at `qa.md:267`, `ledger.md:143`, `retry.md:141-142,147-149,189,193`; `SKILL.md` identical; no line shifts. Two of those lines are cited (K3), which the paper now states.

### Contradiction Re-Scan
- Method: read the whole merged paper against itself; grep for the known risk phrases ("leave Orca", "zero protocol", "no protocol change", "zero change", "No new mechanism"); compare against X-001 to X-004 in `diff-analysis.md`.
- New contradictions introduced: 0 remaining. Three were found during the merge and fixed mechanically within the plan:
  1. Base Reliability bullet 1 said "No new mechanism", while Changes 4-8 add coordinator rules. Fixed: "No new ledger mechanism for either route ... What the merge adds are coordinator rules". Tag records the fix.
  2. Change 13's "zero edits" cost list against Change 7's required `SKILL.md` Wave 0 option addition. Fixed: zero edits scoped to `qa.md`, `ledger.md`, `retry.md`, plus one named Wave 0 change "which P4 needs anyway".
  3. Change 13's "one new AC step" against the five-step return path (Change 11) and the same-ledger-path assertion (Change 7). Fixed: "one AC-4.1 extension".
- Base "the remaining tasks of that plan leave Orca" (the X-002 conflict) is gone: Change 9 replaced it, and the paper now says the plan stays in Orca under (c) and under (a) unless handed back, consistent with Change 8 (ii). The phrase "no protocol change" survives only inside the HTML provenance comment that names Variant 3's section title.
- X-001 (relay vs `QA:254`): consistent; the paper rejects the relay ("Why not (b)", Safety). X-002: resolved by (a)+(c). X-003 (WC-3 ask route): consistent; Position says the worker never asks, and "Why not (b)" uses WC-3's one-ask limit. X-004 (V2 internal): only the "cannot detect" side is carried.
- Not a contradiction, noted for the reader: Safety bullet 1 calls the rule "the one human checkpoint", and Safety bullet 4 says that under (c) who typed the line is policy, not mechanism. Both come from the plan (base text and Change 10) and the paper states the second as an accepted residual risk.

## Summary
- Total changes planned: 13
- Successfully applied: 13 (Changes 2 and 13 with the accuracy and consistency adjustments recorded above)
- Failed: 0
- Skipped: 0
- Additions required by the merge brief: Fixed constraints K1-K4 and Accepted residual risks R1-R2, both included and tagged.
- Post-merge validation: PASS (structure ✅; references 0 broken, 25 cited lines re-opened and confirmed; 0 new contradictions remaining after 3 mechanical fixes)
- Open item for the next step: the plan was not re-reviewed after its revision (`refactor-plan.md` Review Status); this validation and the final citation check of `RECOMMENDATION.md` are the remaining independent checks.
