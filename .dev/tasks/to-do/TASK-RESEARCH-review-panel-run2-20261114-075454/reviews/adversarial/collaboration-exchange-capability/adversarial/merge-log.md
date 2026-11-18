# Merge Execution Log

## Metadata
- Base: Variant A (Proposal A, `variant-1-original.md`)
- Executor: merge-executor agent (slot C-12, `collaboration-exchange-capability`)
- Plan: `refactor-plan.md` (10 changes plus Change 9b from the "Amendments from the analytical review", amendments 1 to 11 applied; amendments override the change text where they differ)
- Output: `../merged-collaboration-exchange-capability.md`
- Changes applied: 11 of 11 planned (Changes 1 to 10 and 9b)
- Status: success
- Timestamp: 2026-11-14
- Forbidden run-1 paths (the two paths barred by the run instructions): not read, listed or cited (grep of the merged file for both names: 0 matches)

## Changes Applied

### Change 1: Restate the position as a staged resolution
- **Status**: Applied
- **Source**: `rounds/r2-advocate-A.md` section 5(c); `rounds/r2-advocate-B.md` sections 3 and 4.2
- **Target**: Base section 1 (tail of sentence group three replaced; amendment 4: sentence "Unconditional ..." kept verbatim), plus title, Position line and lead paragraph (lead facts from `base-selection.md` and the `debate-transcript.md` convergence assessment)
- **Before**: "...nothing of the hook transport, the board, the seal or the message-kind registry is built into the core until an exchange arm beats the static kit on a package with real ground truth." Title "Proposal A for slot C-12"; Position "A (... not built until an exchange arm beats the kit)".
- **After**: "...nothing of the transport (...) is built now", then the build trigger (three conditions: C-07 launcher with persistence and a per-session activation channel named by capability; X-14 metric and decision rule plus C-08 served-model record; named owner and expiry with the state "unmeasured, not rejected") and a separate enable trigger. Title "Merged position for slot C-12 (slug `collaboration-exchange-capability`)"; lead paragraph names the base, 0.9198 vs 0.8747, tiebreaker level 1 (12 vs 5 debate points), convergence 24 of 25 = 96%, BLOCKED_BY_INVARIANTS by INV-005 and INV-009, the staged hybrid, kit default off.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Change 1 ... -->` (section 1) and `<!-- Source: Base (original, modified) - Change 1, Change 10 ... -->` (title block)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: Correct three base statements the debate showed stale or overstated (four places, amendment 3)
- **Status**: Applied
- **Source**: `rounds/r1-advocate-A.md` concessions 1 and 2; `rounds/r2-advocate-A.md` B-W3 and section 3 rows X-002, X-004; `rounds/r2-advocate-B.md` section 4.1 rows X-002, X-004
- **Target**: Base 4.4 (`--resume` clause), 8 answer (2) (hook-cost sentence and the `--resume` item in the same list), 4.2 last sentence of the "Reading, and its limits" bullet, section 0 legend
- **Before**: 4.4 "its `--resume` dependency on gateway ids is not evidenced [UNVERIFIED]"; 8(2) "hook cost of tens to about 150 ms against a 0.1 s planning budget" listed as unverified; 4.2 "no exchange arm has a matching control row"; legend without a note on later commits.
- **After**: 4.4 records S2 `--resume` PASS for four gateway ids in two packages at the pinned tip (`BP r5 spikes/NOTES.md:23-30`, `r2 spikes/RESULTS.md`), plumbing on the E2 launcher, not benefit and not a product launcher (X-002, B 82%); 8(2) states 57 to 85 ms (r5) and 73 and 81 ms (r2) fit 0.1 s but are maxima over 4 to 10 calls, r4's 143 and 90 ms stay [UNVERIFIED]; 4.2 reads "no exchange arm has a row matched against the A2 kit arm at a size that separates from noise"; legend adds "Later E2 commits up to `e2f2ac268` were not read by either advocate". The added 8(2) retrofit qualifier of amendment 3 ("argued, not measured", orphan script, `install_hooks.py:35-41`) is in answer (2).
- **Provenance tag**: `<!-- Source: Base (original, modified) - Change 2 ... -->` on sections 0, 4.2 and 4.4; section 8 tag cites Change 2
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: Replace the measurement gate (6.1) with a two-sided enable rule and the build trigger; new 6.0 (amendments 1, 2, 9)
- **Status**: Applied
- **Source**: `rounds/r2-advocate-B.md` section 3 (Build 1-3, Enable 1-2); `rounds/r2-advocate-A.md` section 5(c) and section 3 (Accept)
- **Target**: New 6.0 "When the transport is built and when exchange is enabled"; base 6.1 (wrong-if/right-if sentences only)
- **Before**: 6.1 "This proposal is wrong if an exchange arm beats A2 ... It is right, for now, if none does, and this is the same experiment slot B would need ..., so it costs nothing extra under either position."
- **After**: 6.0 states the build trigger (three conditions, capability not flag, conditions 1 and 2 as cross-slot dependencies, owner is the lead's decision, the C-08 served-model and act-rate record satisfiable now) and the enable trigger (arm against A2 on module-matched ground truth, hold-out of at least 4 unseen defects as a floor, power calculation, pre-registered two-sided rule with the three outcomes, tasklist review only, preconditions of 3.2.1, plus S0/S2 on the product launcher per gateway-class model, hook p95 over at least 30 calls, fault injection, installed-file-set diff). 6.1 keeps its matching-control comparison and the note that the same experiment serves either position; "costs nothing extra" now reads "for running the arms on the E2 launcher; the result binds a product decision only after a repeat on a product launcher with the served model recorded (C-08)", with C-008 (B 57%, partly overtaken at `c44c98a77`, [POST-BASELINE] secondary only, paired with E3).
- **Provenance tag**: `<!-- Source: Debate Round 2, r2-advocate-B.md section 3 ... - merged per Change 3 and amendments 1, 2 and 9 -->` (6.0); `<!-- Source: Base (original, modified) - Change 3 and amendment 1 ... -->` (6.1)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Derived edit (flag for the orchestrator)**: the base's section 7 last bullet ("an exchange arm winning measurement 1 ... Then the build is a new capability behind `exchange`") contradicted the new build/enable split. Wording only was adjusted so that an arm win is the enable trigger and the build trigger is 6.0. No plan line names this bullet; it is a consequence of Changes 1 and 3.
- **Structure note**: the base's numbered list 1 to 7 in section 6 became headings 6.1 to 6.7 with the same numbers (so the plan's "6.1", "6.4" resolve to headings), and a sentence says "measurement N" means 6.N.

### Change 4: Add the binding design note of preconditions (new 3.2.1; amendments 2 and 11)
- **Status**: Applied
- **Source**: Variant B sections 2.1, 2.2 (as corrected), 2.5, 3.A, 5, 6 (tests 4 and 6); `rounds/r2-advocate-A.md` section 4 (six-item minimum); `rounds/r2-advocate-B.md` sections 3 and 4.3
- **Target**: Base 3.2, new subsection 3.2.1 after the 3.2 text
- **Before**: Section did not exist.
- **After**: Six items: (1) `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only; (2) harness-written sidecar keyed by reviewer id and finding id, key not `origin`, quorum over own-origin lines only; (3) untrusted-anchor rules with the adversarial-anchor test, board files never in the review-telemetry export; (4) fault injection (seal fails closed, review fails open); (5) single-copy requirements (`agent_id` skip, timed lock, seal before first delivery, parallel-call replay); (6) installer footprint (script in `src/superclaude/hooks/scripts/`, name in `_FRESHNESS_SCRIPTS`, NO `hooks.json` entry, `install_hooks.py:94-96`, per-session channel, no `src/superclaude/` path in installed text, package `exchange/` because `.gitignore:13` is `lib/`). States that the note binds the lift of `exchange: off`, none of it is built now, and its tracked-file home is not decided in this slot. Adds the enable-side launcher tests of amendment 2.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Sections 2.1, 2.2 (as corrected), 2.5, 3.A, 5 and 6 (tests 4 and 6); Debate Round 2 ... - merged per Change 4 and amendments 2 and 11 -->`
- **Validation**: Structural integrity ✅ (H4 under H3 3.2) | References ✅ | Contradictions ✅

### Change 5: Replace the off-state test (6.4 and the 3.1 item 6 test sentence; amendments 6 and 7)
- **Status**: Applied
- **Source**: `rounds/r1-advocate-A.md` A-002; `rounds/r1-advocate-B.md` A-002; `rounds/r2-advocate-B.md` W2
- **Target**: Base 6.4 (rewritten) and the test sentence of 3.1 item 6
- **Before**: 6.4 "launch argv and brief bytes with `exchange: off` equal those of a profile without the key; with `kit: off` equal those of today's brief." 3.1 item 6 "A test pins that the launch argv and the brief bytes ... equal those without the key".
- **After**: 6.4 lists five checks (argv and brief bytes equal the baseline; no new file under `~/.claude/hooks/`; no `hooks.json` or merged-settings diff; no new run-record key attributable to exchange; a named installed-file-set diff). The baseline sentence "today's brief plus the H1 lines" is tagged "[merge-author correction of the base 3.1/6.4 contradiction; not debate-concluded]" with INV-004 left open. "By construction" appears only with the qualifier "for hooks, `hooks.json` and `~/.claude/hooks/`; if the key is code, the key itself is not covered by that argument [OPEN: INV-003]". 3.1 item 6 now points to 6.4, states why byte equality alone is not inertness, and carries the Open note (INV-003: `panel.py:37-46,160-176`; B R2 push-back 3; not decided in this slot). 6.5 and 6.6 kept unchanged.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Change 5 and amendments 6 and 7 ... -->` (6.4); `<!-- Source: Base (original, modified) - Change 5 (test sentence replaced) and amendment 6 ... -->` (3.1 item 6)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: Make the kit default off for every module until measurement (amendment 8)
- **Status**: Applied
- **Source**: `rounds/r2-advocate-A.md` B-W2; base 3.4
- **Target**: Base 3.4 last sentence of the first paragraph; base 6.2 (added by amendment 8)
- **Before**: "The spec-review and tasklist modules ... are the first candidates for `on`, subject to the cost measurement in section 6." 6.2 turned `kit: on` on the cost ratio alone.
- **After**: Spec-review and tasklist modules also start `kit: off` and turn `on` only after 6.2 (cost) and 6.7 (hold-out of at least 4 unseen defects) pass; the kit evidence (n = 2 against 4, one judge) is stated; the cost-gate dimension (elapsed or tokens, panel size) is an open item [OPEN: INV-006]. 6.2 adds the measurement-7 condition.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Change 6 ... -->` (3.4) and `<!-- Source: Base (original, modified) - Change 6 and amendment 8 ... -->` (6.2)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: Add the fallback and the F1 constraint to the objection answer and 4.4
- **Status**: Applied
- **Source**: Variant B section 8 concession; `rounds/r2-advocate-B.md` V5 and V6
- **Target**: Base 4.4 (one sentence appended: V6) and base 8 (answer (6) appended after answer (5): fallback and the V5 scope correction)
- **Before**: Neither text existed.
- **After**: 4.4: no existing path passes a session id to `claude`; the swarm transport is stateless (`openai_compat.py:384-388`); F1 on swarm needs a new round-two dispatch step and the second prompt must carry the reviewer's own phase-1 report; no F1 run exists on swarm [UNVERIFIED]. 8(6): if C-07 yields no launcher with persistence and a per-session activation channel, the hook half is dropped and the F1 second prompt on swarm stays a design question for the swarm slot, still off; `--settings` is absent from `src/superclaude/**/*.py` but present in the ccsession shell launcher (`skills/ccsession-tag/ccsession:1150,1259`), which is not a headless panel launcher.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Change 2 ... and Change 7 ... -->` (4.4); `<!-- Source: Base (original, modified) - Change 2 ... and Change 7 (answer 6 appended ...) -->` (section 8)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: Add the served-model and act-rate probe record as a "now" item (amendment 10)
- **Status**: Applied
- **Source**: `rounds/r2-advocate-B.md` section 3 (Build 2) and 4.3; base 6.3
- **Target**: Base 3.2 ("What the core keeps open", sentences added) and 6.3 (one sentence)
- **Before**: 3.2 listed the run-record persistence field only; 6.3 described the probe only.
- **After**: The probe record (served model; act rate per model and instruction form) is a now item accepted by both advocates as cheap with consumers today; its home is not decided; B R2 4.3 names only "slot C-08 if that slot owns it"; no schema specified. [OPEN: INV-002]
- **Provenance tag**: `<!-- Source: Base (original) - first paragraph; second paragraph modified by Change 8 ... -->` (3.2); `<!-- Source: Base (original, modified) - Change 8: one sentence added -->` (6.3)
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Add a "Residual open items carried from the debate" section
- **Status**: Applied
- **Source**: `invariant-probe.md` (all 16 findings); the team lead's new-evidence note on `e2f2ac268`; amendment 11
- **Target**: New section 9 at the end, before the final Status line
- **Before**: Section did not exist.
- **After**: Gate status BLOCKED_BY_INVARIANTS; INV-005 and INV-009 (HIGH) quoted as the plan says; a 16-row table (id, status, severity, one-line assumption): 2 ADDRESSED (INV-001 with its residual "a note has no mechanical consumer, so an expiry triggers nothing"; INV-012), 14 UNADDRESSED (2 HIGH, 12 MEDIUM: INV-002, 003, 004, 006, 007, 008, 010, 011, 013, 014, 015, 016); the `e2f2ac268` open item as the plan words it ([POST-BASELINE], the central premise must be re-checked when the unification folds the tasklist branch in, the debate was not rerun). No item claimed resolved.
- **Provenance tag**: `<!-- Source: Debate Round 2.5, invariant-probe.md ... - merged per Change 9 and amendment 11 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9b: Tag-only [OPEN] markers on three base sentences (amendment 5)
- **Status**: Applied
- **Source**: Amendments 5 and 6 of the plan; `invariant-probe.md` INV-005, INV-009, INV-013
- **Target**: Base 3.3 tasklist/reflect row; 3.1 item 2; section 5 INV-G row
- **Before**: Untagged sentences ("no call-site change"; the H2 step; "no reviewer sees another's text").
- **After**: "[OPEN: see section 9, INV-005]"; "[OPEN: INV-009, see section 9]"; "[OPEN: INV-013]". No resolution added.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Change 9b: tag only, no resolution -->` (3.1 item 2); same wording in the 3.3 and section 5 block tags
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Beyond the three sentences (flag for the orchestrator)**: one more tag-only marker, "[OPEN: see section 9, INV-005]", on the section 5 INV-A row ("No change to `src/superclaude/cli/reflect` and no contract key"), because INV-005 states that naming the driving spec needs an edit in `cli/reflect`; without it the row stated the opposite of 3.3 untagged. Tag only, no resolution.

### Change 10: Provenance and the merged-file header
- **Status**: Applied
- **Source**: protocol Section 6 provenance format
- **Target**: Whole file
- **Before**: No provenance annotations; header "Proposal A for slot C-12".
- **After**: File header carries `<!-- Provenance: This document was produced by /sc:adversarial -->`, `<!-- Base: Variant A (Proposal A) -->`, `<!-- Merge date: 2026-11-14 -->`; 30 `<!-- Source: ... -->` tags cover every section and significant block (original blocks "Base (original)", changed blocks "Base (original, modified) - Change N", inserted blocks with source variant or debate file and change number). "Status: Complete" kept at the top and the end; the section 0 legend kept, with added lines on `[OPEN: ...]`, merge-added facts and the merge-author correction tag.
- **Provenance tag**: `<!-- Provenance: ... -->`, `<!-- Base: Variant A (Proposal A) -->`, `<!-- Merge date: 2026-11-14 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ H1 title; H2 sections 0 to 9; H3 under 3 (3.1 to 3.4), 4 (4.1 to 4.4) and 6 (6.0 to 6.7); H4 3.2.1 under H3 3.2. No level gaps (checked with a grep of all heading lines).
- Section ordering: ✅ base numbering 0 to 8 kept; new 3.2.1 follows the 3.2 text and precedes 3.3; new 6.0 precedes 6.1; new section 9 is last, before the closing Status line.
- Document flow: ✅ Section 1 names the two triggers, 6.0 defines them, 3.2.1 holds the preconditions the enable trigger needs, 8(6) holds the fallback 6.0 refers to, 9 lists the open items the tags point to.

### Internal References
- Total references: 61 section or subsection references (for example "see 3.4", "6.0", "3.2.1", "section 9", "measurement 7 (6.7)", "E2 in 4.1") plus 12 `[OPEN: ...]` tags that point to finding ids in section 9 and a few claim-row pointers (E2, E3, E8, E10) into 4.1
- Resolved: 61 of 61; 12 of 12 finding-id tags resolve to a row of the section 9 table (INV-002, 003, 005, 006, 008, 009, 011, 013, 014); claim rows exist in 4.1
- Broken: 0
- Note: references written "Variant B 6.4", "Variant B 3.A and 6.6" and "r09 section N", "B R2 section N" point to the source documents, not to this file, and are not counted.

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: checked pairs: (a) reserved key as code vs as a note: 3.1 item 6, 6.4 and section 9 INV-003 all carry [OPEN: INV-003]; no unmarked statement says either; (b) "no change to `cli/reflect`" vs H1 into reflect: 3.3 row and the section 5 INV-A row carry [OPEN: INV-005]; the section 2 C-01 row quotes the slot outcome as that slot stated it; (c) 6.4 baseline vs H1 shipping unconditionally: resolved by the tagged merge-author correction, INV-004 left open; (d) 4.2 "no matching control row" vs 4.3 counted rows: corrected; (e) section 1 and the base section 7 last bullet vs the build/enable split: section 1 replaced, section 7 bullet adjusted (see Change 3); (f) "first candidates for `on`" removed; no other statement says a module starts with the kit on. Two wording tensions that existed in the base and are only mitigated, not removed: section 1 sentence two and the 3.3 spec-review row speak of the kit being rendered into briefs while 3.4 now starts every module at `kit: off`; the "Unconditional" sentence and 3.4 cover it. The kit/exchange evidence tags were kept; no fact that exists only at `c44c98a77` or later is the sole evidence for a decisive point (6.1 C-008 is paired with E3).

## Summary
- Total changes planned: 11 (Changes 1 to 10 plus 9b)
- Successfully applied: 11
- Failed: 0
- Skipped: 0
- Items flagged for the orchestrator (outside the literal plan text, wording or tag only, no content decided): (1) section 7 last bullet adjusted to the build/enable split; (2) the INV-A row tag in section 5; (3) the base's numbered measurement list turned into headings 6.1 to 6.7; (4) the lead paragraph and a one-sentence reading note; (5) a legend bullet defining `[OPEN: ...]` and the merge-added tags. Nothing was added that the plan or the debate files do not contain.
- Post-merge validation: PASS
