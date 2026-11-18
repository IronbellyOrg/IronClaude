# Refactoring Plan: Merge into Base (Variant A = Proposal A)

## Overview
- Base: Variant A (Proposal A, `variant-1-original.md`), selected per `base-selection.md` (combined 0.9198 vs 0.8747, margin 4.51%, tiebreaker level 1: 12 vs 5 debate points)
- Incorporating strengths from: Variant B (Proposal B, `variant-2-original.md`) and the staged-hybrid resolution that both advocates reached in Round 2
- Planned changes: 10
- Risk level: Low to Medium overall (all changes are additive or wording corrections; no code is specified)
- Output file: `merged-collaboration-exchange-capability.md` in the `--output` folder (one level above `adversarial/`)
- Hard rule for the merge: add nothing the debate did not conclude. Every change cites a diff point, a round statement or a verified fact. The merged file must keep the base's evidence tags ([CODE-VERIFIED], [UNVERIFIED], [POST-BASELINE]) and must not use any post-baseline fact as the only evidence for a decisive point. Do not cite or read the forbidden run-1 paths.

## Planned Changes

### Change 1: Restate the position as a staged resolution (from the debate, both advocates' Round 2)
- **Source**: `rounds/r2-advocate-A.md` section 5(c); `rounds/r2-advocate-B.md` sections 3 and 4.2 (these two agree)
- **Target**: Base section 1 ("The position in one paragraph") (replace)
- **Rationale**: Diff points X-001, C-001, C-002 (agreed resolution); C-002 stayed unresolved only on its label (A 52 vs "Merge 62"), both advocates endorse the same trigger form. Base text "not built until an exchange arm beats the kit" is ownerless and conflates instrument with capability (Advocate A Round 2, B-W1).
- **Integration point**: Keep the base's first-sentence list of what ships now (H1, H2, H4 principle, H3 rule, catalogue/kit, reserved key). Replace the last two sentences with: nothing of the transport is built now; a build trigger (all three: C-07 adjudicated to a launcher with persistence and a per-session activation channel named by capability; X-14 metric of record and decision rule committed and C-08 served-model record landed; a named owner and expiry with the recorded state "unmeasured, not rejected") and a separate enable trigger (see Change 3).
- **Risk**: Low. Wording only; matches both Round 2 files.

### Change 2: Correct three base statements the debate showed stale or overstated (from X-002, X-004, W3)
- **Source**: `rounds/r1-advocate-A.md` Concessions 1 and 2; `rounds/r2-advocate-A.md` B-W3; `rounds/r2-advocate-B.md` V3
- **Target**: Base 4.4 (`--resume` sentence), 8 answer (2) (hook-cost sentence) and 4.2 first sentence of the matching-control claim, plus the evidence legend line in 0 (replace)
- **Rationale**: X-002 (B 82%): S2 `--resume` PASS recorded for four gateway ids in two packages at the pinned tip (`BP r5 spikes/NOTES.md:23-30`, `r2 spikes/RESULTS.md`), plumbing on the E2 launcher, not benefit and not a product launcher. X-004 (B 62%): recorded 57 to 85 ms (r5), 73 and 81 ms (r2) fit 0.1 s but are maxima over 4 to 10 calls, not a 30-call p95; r4's 143 and 90 ms stay [UNVERIFIED]. "No exchange arm has a matching control row" becomes "no exchange arm has a row matched against the A2 kit arm at a size that separates from noise".
- **Integration point**: In-place sentence replacements; keep the base's tags and add the pinned-tip citations above.
- **Risk**: Low.

### Change 3: Replace the measurement gate (6.1) with a two-sided pre-registered enable rule and the build trigger (from C-002, C-007, Enable 1)
- **Source**: `rounds/r2-advocate-B.md` section 3 (Build 1-3, Enable 1-2 with amendments, accepted by Advocate A's hybrid); `rounds/r2-advocate-A.md` section 5(c)
- **Target**: Base 6.1 (replace) and a new subsection 6.0 "When the transport is built and when exchange is enabled" before 6.1
- **Rationale**: Diff points C-002, C-007, C-008, A-001. Enable rule: an exchange arm against A2 on module-matched ground truth, hold-out of at least 4 unseen defects (a floor, not a power guarantee), power calculation, a pre-registered rule on gain and cost, outcomes "clears minimum gain with an interval that excludes zero", "no effect detected at n", "underpowered, unmeasured"; tasklist review only (A-001), PR review and rf-qa stay off. Build trigger names the capability (persistence on, a per-session activation channel, a headless main-thread lane), not the `--settings` flag.
- **Integration point**: 6.0 states both triggers and states that the three build conditions are cross-slot dependencies (C-07, C-08, X-14), not C-12 deliverables. 6.1 keeps the base's matching-control comparison and A's note that the same experiment serves either position.
- **Risk**: Medium. New structure, but each element is stated in both Round 2 files.

### Change 4: Add the binding design note of preconditions (from Variant B 2.1, 2.5, 5, 6 and 3.A; C-010, C-006, X-005, X-006)
- **Source**: Variant B sections 2.1, 2.5, 5, 6 tests 4 and 6, 3.A, 2.2 (as corrected); `rounds/r2-advocate-A.md` section 4 (six-item minimum contents); `rounds/r2-advocate-B.md` section 4.3
- **Target**: Base 3.2 (append a new 3.2.1 "Design note: preconditions for lifting `exchange: off`") (insert)
- **Rationale**: C-010 (B 79%), C-006 (merge 63%), X-005 (B 58%): record, as preconditions and not as code, (1) `panel-msg/1` per-kind keys, forbidden keys `claim verdict blocking severity category note`, 600-byte cap, located-anchor rule, harness-authored kinds only; (2) harness-written sidecar keyed by reviewer id and finding id, key not named `origin`, quorum counts over own-origin lines only; (3) untrusted-anchor rules with an adversarial-anchor test (injection text, 600-byte boundary, forbidden key in a located-anchor field) and "board files never enter the review-telemetry export"; (4) fault injection (seal fails closed, review fails open); (5) single hook copy requirements (`agent_id` skip, timed lock, seal before first delivery, parallel-call replay); (6) installer footprint as a test item: script in `src/superclaude/hooks/scripts/`, name in `_FRESHNESS_SCRIPTS`, NO `hooks.json` entry (the `launch-level-pre-push.sh` pattern, `install_hooks.py:94-96`), activation only through a per-session channel baked by the adapter, no `src/superclaude/` path in installed text, package named `exchange/` because `.gitignore:13` is `lib/`.
- **Integration point**: New 3.2.1 after the base's list of what stays unbuilt. State that the note binds the lift of `exchange: off` and that none of it is built now.
- **Risk**: Low. Additive documentation.

### Change 5: Replace the off-state test (6.4) with the stricter test (from A-002, C-011)
- **Source**: `rounds/r1-advocate-A.md` A-002; `rounds/r1-advocate-B.md` A-002; `rounds/r2-advocate-B.md` W2
- **Target**: Base 6.4 and 3.1 item 6 test sentence (replace)
- **Rationale**: A-002 (both QUALIFY): byte equality of argv and brief proves the launched session unchanged, not inertness. Add: no new file under `~/.claude/hooks/`, no `hooks.json` or merged-settings diff, no new run-record key when off, a named installed-file-set diff. Note the baseline problem the probe found (INV-004): with H1 shipping unconditionally, the "brief equals today's" baseline must be stated as "today's brief plus the H1 lines".
- **Integration point**: Rewrite 6.4 as the stricter test; add the baseline sentence; keep 6.5 (brief lint) and 6.6 unchanged.
- **Risk**: Low.

### Change 6: Make the kit default `off` for every module until measurement (from B-W2 concession and C-003)
- **Source**: `rounds/r2-advocate-A.md` B-W2; Variant A 3.4
- **Target**: Base 3.4, last sentence of the first paragraph ("first candidates for `on`") (replace)
- **Rationale**: C-003 (A 73%): kit key and per-module cost gate stay; Advocate A withdrew "first candidates for `on`" without the hold-out (measurement 7); kit evidence is n = 2 against 4, one judge.
- **Integration point**: Spec-review and tasklist modules become `kit: off` until measurements 2 and 7 pass; the cost-gate dimension (elapsed or tokens, panel size) is stated as an open item (INV-006).
- **Risk**: Low.

### Change 7: Add the fallback and the F1 constraint to the objection answer and 4.4 (from U-013, C-005)
- **Source**: Variant B section 8 concession; `rounds/r2-advocate-B.md` V5, V6
- **Target**: Base 8 (append after answer (5)) and 4.4 (append one sentence) (insert)
- **Rationale**: If C-07 yields no launcher with persistence and a per-session activation channel, the hook half is dropped and the F1 second-prompt on swarm remains a design question for the swarm slot, still off. V6: no existing path passes a session id to `claude`; the swarm transport is stateless (`openai_compat.py:384-388`), so F1 on swarm needs a new round-two dispatch step and the second prompt must carry the reviewer's own phase-1 report; no F1 run exists on swarm [UNVERIFIED]. V5 (corrected scope): `--settings` is absent from `src/superclaude/**/*.py` but present in the ccsession shell launcher (`skills/ccsession-tag/ccsession:1150,1259`).
- **Integration point**: Sentences appended, with tags.
- **Risk**: Low.

### Change 8: Add the served-model and act-rate probe record as a "now" item (from Build 2 amendment, A's measurement 3)
- **Source**: `rounds/r2-advocate-B.md` section 3 (Build 2) and 4.3; Variant A 6.3
- **Target**: Base 3.2 (last sentence, "What the core keeps open") and 6.3 (amend)
- **Rationale**: Both advocates accept the probe record as cheap and having consumers today. The debate did not decide its home (probe INV-002); the merge states it as an open item and must not invent a schema.
- **Integration point**: One sentence in 3.2 naming the probe record as a now item with the home unresolved; 6.3 unchanged otherwise.
- **Risk**: Low.

### Change 9: Add a "Residual open items carried from the debate" section (from the invariant probe and the lead's evidence note)
- **Source**: `invariant-probe.md` (all 16 findings; INV-005 and INV-009 HIGH); the team lead's new-evidence note
- **Target**: New section 9 at the end of the base, before the final Status line (insert)
- **Rationale**: Protocol: unaddressed invariants must be reported with severity. List the two HIGH items verbatim (INV-005: H1 into reflect needs an edit in `cli/reflect/ensemble.py` while "no change to cli/reflect" is adjudicated; INV-009: H2 re-ask inside C-01's `parse_block` placement while C-01 INV-003 is open and C-06 is open), the 12 MEDIUM items by id and one-line assumption, and the [POST-BASELINE] open item: the tasklist-study branch gained commits up to `e2f2ac268` (2026-11-14 19:19, "counted results, replicates and write-up for the five collaboration designs") which neither advocate read; the central premise (no exchange arm measured against the static kit) may be answered there and must be re-checked when the unification folds the tasklist branch in; the debate was not rerun on it.
- **Integration point**: New section 9 with a table (ID, severity, one-line assumption). Do not claim any of them resolved.
- **Risk**: Low.

### Change 10: Provenance and the merged-file header
- **Source**: protocol Section 6 provenance format
- **Target**: Whole file (header and per-block tags)
- **Rationale**: Every block carries `<!-- Source: ... -->`. Header: `<!-- Provenance: This document was produced by /sc:adversarial -->`, `<!-- Base: Variant A (Proposal A) -->`, merge date.
- **Integration point**: Tag base blocks "Base (original)", changed blocks "Base (original, modified) - Change N", inserted blocks with the source and change number. Keep the base's "Status: Complete" convention and its evidence-tag legend (section 0).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-003, C-001, X-001 | Build the engine-local exchange package, hook script, board, seal, validator and `collab` record now (Variant B 2.1-2.4) | Debate conclusion X-001 (A 63%): no launcher at HEAD (`review-tiers.default.json:25-29` `"launch": {}`, no `--settings` in `src/superclaude/**/*.py`), no family with a clean measured success, no exerciser; Advocate B conceded build-now in Round 2 |
| C-004 | New raw-id launch adapter with persistence and per-session `--settings` built outside `ClaudeProcess` (Variant B 2.3) | Depends on open slot C-07; `process.py:149-152` keeps `--no-session-persistence`; an adapter written first would be shaped by fixtures (B Round 2 W1) |
| X-006 | Hook "registered as `~/.claude/hooks/...` in `hooks.json`" (Variant B 2.2) | Defect conceded by B: a `hooks.json` entry fires in every session; the unregistered-script pattern is used instead (Change 4 item 6) |
| C-011 | Argv-diff test of the new adapter against the adapter without the package as the off-state guarantee (Variant B 2.4, 6.1) | Compares new code with new code and cannot see installer, hooks.json or telemetry effects; replaced by the stricter test (Change 5) |
| C-005 | F1 between-phase as "the portable family" (Variant B 2.8) | No session-id path exists, swarm needs a new orchestration step, no F1 run exists on swarm; kept as a design question only (Change 7) |
| C-010, C-006 | Validator as pure functions, sidecar schema as code, `collab` record built now | No caller exists without an exchange arm or a launcher; a second dormant surface (agreed by both advocates in Round 2); recorded as design-note preconditions (Change 4) |
| X-007 | "Waiting is not free" (Variant B 8) | Waiting is free for the packages (they stay on the branch); not free for repeatability, which the build trigger addresses (X-007 A 57%) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Position paragraph inconsistent with sections 6.0/8 | Restore base section 1 |
| 2 | Low | A stale fact remains | Revert the sentence |
| 3 | Medium | Triggers misstated against the Round 2 files | Restore base 6.1; remove 6.0 |
| 4 | Low | Over-specifies a design | Remove 3.2.1 |
| 5 | Low | Test text inconsistent with INV-004 note | Restore base 6.4 |
| 6 | Low | Kit default reads stronger than evidence | Restore base sentence |
| 7 | Low | Tagged sentences overstate | Remove appended sentences |
| 8 | Low | Probe record home is read as decided | Remove the sentence |
| 9 | Low | Open items read as resolved | Remove section 9 |
| 10 | Low | Missing tag | Re-tag |

## Review Status
- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (--interactive)
- Approved by: auto (pending the analytical review of this plan recorded in `merge-log.md`)
- Approval timestamp: 2026-11-14 (orchestrator run)

## Amendments from the analytical review (`refactor-plan-review.md`, verdict APPROVE-WITH-AMENDMENTS; all applied; they override the change text above where they differ)

1. **Change 3 (C-008)**: the base 6.1 sentence "costs nothing extra under either position" becomes "costs nothing extra for running the arms on the E2 launcher; the result binds a product decision only after a repeat on a product launcher with the served model recorded (C-08)". Add C-008 (B 57%, partly overtaken at `c44c98a77`, [POST-BASELINE] secondary evidence only) to the rationale. Only the wrong-if/right-if sentence of 6.1 is replaced; its matching-control comparison stays.
2. **Change 3 and Change 4 (Enable 2)**: the enable trigger also requires S0 and S2 on the product launcher for every gateway-class model in the panel, hook p95 over at least 30 calls per model, fault injection, and the installed-file-set diff (B R2 Enable 2; A R2 section 3 Accept). State it in 6.0 and in 3.2.1.
3. **Change 2 sources**: replace "V3" by "B R2 section 4.1 rows X-002 and X-004; A R2 section 3 rows X-002 and X-004". Change 2 edits four places (4.4, 8 answer (2), 4.2 last sentence of the "Reading, and its limits" bullet, the section 0 legend). The legend gets: "later E2 commits up to `e2f2ac268` were not read by either advocate". Add to base 8 answer (2): "'retrofit is bounded' is argued, not measured (A-003, both QUALIFY); removing a shipped dormant script leaves an inert orphan in installed `~/.claude/hooks/` (`install_hooks.py:35-41`)".
4. **Change 1 target**: replace only the tail of base section 1 sentence 3 (from "and nothing of the hook transport ...") with the staged text; keep sentence 4 (the definition of "Unconditional") verbatim.
5. **New Change 9b**: append tags only (no resolution) to three base sentences: 3.3 tasklist/reflect row "no call-site change" gets "[OPEN: see section 9, INV-005]"; 3.1 item 2 (H2 / re-ask) gets "[OPEN: INV-009]"; section 5 INV-G row "no reviewer sees another's text" gets "[OPEN: INV-013]".
6. **Reserved `exchange` key**: 3.1 item 6 gets "Open (INV-003): the key is code (`panel.py:37-46,160-176` rejects unknown panel keys) or a design-note entry (B R2 push-back 3); not decided in this slot". The 6.4 test is scoped to "no run-record key attributable to exchange". Do not write "passes by construction" without the qualifier "for hooks, `hooks.json` and `~/.claude/hooks/`; the key itself is code".
7. **Change 5**: the baseline sentence "today's brief plus the H1 lines" is tagged "[merge-author correction of the base 3.1/6.4 contradiction; not debate-concluded]"; INV-004 stays open in section 9.
8. **Change 6**: add 6.2 to the target ("... and measurement 7 (hold-out of at least 4) passes", A R2 B-W2); retitle "spec-review and tasklist default off" (reflect is already off).
9. **Change 3 wording**: the three build conditions are C-07 (launcher), C-08/X-14 (metric, decision rule, served-model record) and the owner with expiry; the first two are cross-slot dependencies, the owner is "the lead's decision, not C-12's". State that the C-08 served-model and act-rate record is satisfiable now and does not wait on the transport.
10. **Change 8**: cite B R2 4.3 ("slot C-08 if that slot owns it") as the only named candidate home; the home stays undecided.
11. **Change 4 and 9**: 3.2.1 is the content of the design note; its tracked-file home is not decided in this slot. Section 9 lists all 16 findings (2 ADDRESSED: INV-001 with its residual "a note has no mechanical consumer, so an expiry triggers nothing", INV-012; 14 UNADDRESSED).
