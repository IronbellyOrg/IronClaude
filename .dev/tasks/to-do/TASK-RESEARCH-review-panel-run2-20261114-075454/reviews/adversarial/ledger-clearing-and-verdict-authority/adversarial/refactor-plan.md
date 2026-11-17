# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (`variant-2-original.md`, proposal-b.md, "explicit per-row verification")
- Incorporating strengths from: Variant A (`variant-1-original.md`, proposal-a.md, "guarded one-pass silence-clear")
- Source of every rule below: the two advocates' Round 2 final positions in `debate-transcript.md` (the converged hybrid) and the scoring matrix there; no rule is added that the debate did not reach. Where the advocates still differ, the plan records both forms and marks the point open.
- Planned changes: 10 (changes 1-5 replace or modify base rules, changes 6-9 insert, change 10 records open conditions)
- Risk level: Medium overall (the clearing rule and the verdict surface change; three HIGH invariants from the probe stay open and are recorded, not resolved)
- Output of Step 5: `merged-ledger-clearing-and-verdict-authority.md` in the output folder; the merged text is a position paper on the converged design, with the same 7-section frame as the base.

## Planned Changes

### Change 1: Replace the quote-gated clearing rule with the quorum gate (from Variant A)
- **Source**: Variant A, Section 2 "Clearing rule" and "Requested reviewers" rows; debate outcome C-001, X-002, X-003 (Round 2 final positions of both advocates)
- **Target**: Base, Section 2.1 rule B1 (and B2), plus Section 1 paragraph (replace)
- **Rationale**: In the default flow the re-review is one reviewer (`panel.py:600`, 8 of 8 templates `apply_to: ["first"]`), so the quote adds only an occurrence check (B conceded "proves reading, not fixing"); a deletion fix leaves nothing to quote (`document_review_loop_prompts.md:53`). Debate C-001 85%, X-002 85%, X-003 80%.
- **Integration point**: A `resolved_check` row becomes `resolved` iff (a) distinct `block_ok`-true reviewers typing `prior <lid> resolved` >= need, (b) no `block_ok`-true reviewer typed `open` or `regressed` for it, (c) it is not re-found this round. Build the prior map before the clearing loop. `need = min(Q, requested)`, `requested` = reviewers in `--resolution`; C-03 owns Q and is asked to set Q(re-review) = 1. OPEN: when `--resolution` is absent, Variant A says requested = the reports passed, Variant B says need = Q (fail closed); the debate did not settle this (invariant probe INV-004, INV-001).
- **Risk**: Medium; changes the pinned silence-clear tests (`tests/review/test_review_ledger.py:193-217`, `:376-385`, `tests/review/test_review_cli.py:274-292`)

### Change 2: Make the `evidence` key record-only (from Variant A, key kept from Variant B)
- **Source**: Variant A Round 2 C-002 final position; Variant B Round 2 C-002 final position (converged)
- **Target**: Base, Section 2.1 rule B3 (replace "the ledger checks the quote" with "records the quote")
- **Rationale**: Debate C-002 88%; both advocates conceded the gate (span lossy at `findings.py:431` and `ledger.py:224-225`; no test separates a lazy yes from an examined yes).
- **Integration point**: Optional string `evidence` on a prior line, at most 200 characters after flatten, a bad value is ignored with no parser error (a parser error drops the line and invalidates the block, `findings.py:188-192`); the ledger writes it into the `prior_note` event with `quote_in_doc = bool(locate(doc_text, quote))`. Never gating. Promotion to a gate only on M1 evidence, with a deletion carve-out and a fix for the lossy replacement span.
- **Risk**: Low

### Change 3: Replace the blocking predicate with a typed authority plus a CRITICAL floor (from Variant A)
- **Source**: Variant A Section 2 `blocking` row; debate C-004, X-004, U-006 (both advocates' Round 2 final positions)
- **Target**: Base, Section 2.1 rule B6 (replace)
- **Rationale**: The category predicate misgrades `document_review_loop_prompts.md:31` ("needs a guess" is not category-expressible) and `findings-v1` has no `rule` or `wrong_outcome`; a parser-side floor would drop the line. Debate C-004 85%, X-004 85%.
- **Integration point**: In `merge_round`, at the point findings are annotated: `blocking = typed or severity == "CRITICAL"`; member records keep `blocking_typed`; each flip adds a warning. No category predicate and no blind grader in the core; the `verdict:` line stays parser-neutral; M3 stays an offline measurement. No conflict with `findings_v2.py:161-162` (the floor is a subset of that lens rule).
- **Risk**: Medium (residual: a reviewer typing MAJOR with `blocking: false` still passes, probe INV-016, UNADDRESSED)

### Change 4: Narrow the pinned prior-line rule and route dissent to `regressed` (Variant A rule, Variant B state)
- **Source**: Variant A Section 2 "Prior lines" row and Round 2 C-005; Variant B Round 2 C-005 (converged)
- **Target**: Base, Section 2.1 rule B1 text "A `prior` of `open` or `regressed` sets the row" and Section 2.2 spec module paragraph (modify)
- **Rationale**: Debate C-005 88%, X-001 85%. A prior line moves only a `resolved_check` row (clear or dissent); on any other status it is a `prior_note` plus a warning, so it cannot reopen a human-deferred row. A `block_ok`-true `open|regressed` moves a `resolved_check` row to `regressed` (history event `dissent`), which `apply_revision` accepts (`ledger.py:328` skips non-open rows).
- **Integration point**: Edit the docstring at `ledger.py:3-4`; rename `test_prior_lines_never_change_a_status` (`tests/review/test_review_ledger.py:318-338`; its assertions survive) and add `resolved_check` cases; same-round duplicate priors resolve to dissent.
- **Risk**: Medium (probe INV-002 HIGH UNADDRESSED: a valid `prior open` plus a same-round non-blocking re-find can drop the row out of every list; INV-009, INV-010 MEDIUM)

### Change 5: Add the derived-verdict output surface and the empty-brief handling (Variant A text, Variant B VM-6 form)
- **Source**: Variant A Section 2 "Verdict" row; Variant A and B Round 2 C-008 final positions
- **Target**: Base, Section 2.1 rule B5 (extend) and rule B4 last sentence (VM-6)
- **Rationale**: Debate C-008 85%. Both advocates found that when `brief_ids` is empty and `verify_ids` is not, the decision stays REVISE (exit 10), and that `render_merged_report` and the Escalation text list only `brief` ids (`ledger.py:438-466`, `:482`).
- **Integration point**: `ledger verdict` JSON gains `next` (`re-review` or `revise`); the Reviser-brief section prints "no revision needed; re-review the same candidate against the same baseline to answer: <ids>"; the report detail section and the Escalation paragraph list `brief_ids`, `verify_ids` and `held_ids`; `merge_round` refuses when `len(rounds) >= cap_reviews` or the derived decision before the merge is ESCALATE (VM-6, derived form).
- **Risk**: Medium (probe INV-003 HIGH UNADDRESSED: exit-code-only callers and `document_review_loop_prompts.md:70`; INV-006 MEDIUM: the derived check must not fail on an empty ledger)

### Change 6: Add `held` events, reason codes and `unverified_ids` to the merge output (from Variant A)
- **Source**: Variant A Section 2 Clearing-rule row, Section 3.4 item 8 and U-001
- **Target**: Base, Section 2.1 rule B5 and Section 5 test list (insert)
- **Rationale**: U-001 accepted by both advocates (YES); cheap, additive, explains each held row.
- **Integration point**: Merge JSON gains `unverified_ids` / `held_ids`; history events `held` (reason `no-examination-record` or `dissent`) and `refound_deferred`.
- **Risk**: Low

### Change 7: Keep terminal `defer`, drop expiry, add status guard tests (Variant B kept; Variant A tests added)
- **Source**: Variant B rule B7; Variant A Section 5 item 1 (D-11 A/B/C cases); debate C-006, C-007, U-002, U-003
- **Target**: Base, Section 2.1 rule B7 and Section 5 T3 (modify)
- **Rationale**: Debate C-006 88%, C-007 88%: expiry cannot fire (held-only gives ESCALATE and VM-6 refuses later rounds), re-find must not override a human park.
- **Integration point**: `defer` needs `--owner` and `--reason`, allowed on blocking rows in `open`, `regressed`, `resolved_check`, writes no round record, no expiry in the core; a re-found deferred row stays `deferred` and is listed as `refound_deferred` in the merge result and Escalation text. Tests: A's D-11 A/B/C reproductions, using a two-row fixture for the re-find case (probe INV-007).
- **Risk**: Low to Medium (probe INV-008 MEDIUM: no undefer command)

### Change 8: Make the file shape change drop the stored keys and add the text-hash guard (debate refinements of the base)
- **Source**: Variant B Round 2 C-009 and C-003 final positions; `synth-06-conflict-log.md:178` (VM-3 wording, read by the B advocate); Variant A Round 2 conditional form
- **Target**: Base, Section 4 INV-D paragraph and Section 2.1 rule B4 (modify)
- **Rationale**: Debate C-009 75%, C-003 90%. VM-3: "derived from rows on every read and is never stored"; Variant A's snapshot form is a stored verdict under another name.
- **Integration point**: New round records drop `verdict`, `decision`, `brief_ids`; `verdict()` derives from rows and ignores stored keys of old files; schema string `review-ledger/1` kept (whether `/2` is needed stays open, LG-2). `apply_revision` stores `pending_new_sha256`; `merge_round` refuses on a mismatch (ledger unchanged) and then clears it; `apply_revision` refuses while one is pending (revise is not idempotent, `ledger.py:343-347`).
- **Risk**: Medium (probe INV-005 and INV-018 MEDIUM: recovery path, older binaries failing at `last["verdict"]`; INV-014 MEDIUM: no hash if `revise` was skipped)

### Change 9: Merge the measurement plans (from Variant A and Variant B)
- **Source**: Variant A Section 5 items 3-4 (three-arm replay incl. the quote-verified arm, wrongness rule registered before the run); Variant B M2 and M3; debate C-010, U-004, U-008
- **Target**: Base, Section 5 (insert)
- **Rationale**: Debate C-010 80%; M2 is free (count prior-line compliance by ledger id in existing re-review reports).
- **Integration point**: Section 5 keeps T1-T5 (updated to the converged rules) and M1-M3, adds A's three-arm replay (current silence-clear, quorum gate, quote-verified per-row) and the compliance proxy `anchor_status`.
- **Risk**: Low

### Change 10: Record the open conditions the debate left unaddressed (from the invariant probe)
- **Source**: `invariant-probe.md` (INV-001 to INV-022); `return-contract.yaml` `unaddressed_invariants`
- **Target**: Base, Section 4 (insert a subsection "Open conditions left by the debate")
- **Rationale**: The invariant-probe gate blocks convergence while HIGH UNADDRESSED items exist (INV-001, INV-002, INV-003); depth `standard` has no Round 3. The merged document must state them as open, with the handling text only where the debate itself supplied it.
- **Integration point**: A table of the HIGH items and a list of the MEDIUM and LOW items by ID, no new rules.
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-006 | A's `expires_round` with reopen to `open` | Inert: held-only is ESCALATE and VM-6 refuses later rounds; both advocates dropped it |
| C-007 | A's re-find returns a deferred row to `open` | Overrides a human accepted-risk decision; both advocates dropped it |
| C-009 | A's primary form: keep a merge-time snapshot of `verdict`, `decision`, `brief_ids` | A stored verdict under another name; VM-3 wording; A's own conditional fires |
| C-001 | A's "dissent held at `resolved_check`" | `apply_revision` skips non-open rows (`ledger.py:328`); A conceded |
| C-002 | B's quote gate | Conceded by B (proves reading, not fixing; deletion fix; lossy span) |
| C-004 | B's lens category predicate and optional blind grader in the core | Misgrades the shipped grading check; B conceded |
| S-001, C-011 | A's table layout and "one clause at line 70" | Presentation; base layout kept; line 61 gains the optional `evidence` ask and line 70 is restated, as in the base |
| S-002 | Tag-discipline difference | Unresolved and low stakes; the merged text uses explicit tags and marks unverified items |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | A mis-set `need` re-opens silence-clear (INV-001) or deadlocks the one-reviewer re-review | Revert to base rule B1 text |
| 2 | Low | Bad optional key drops a block if error-raising | Remove the key from the grammar line |
| 3 | Medium | CRITICAL floor flips reviewer intent; MAJOR typed non-blocking still passes | Remove the floor, keep warning only |
| 4 | Medium | Dissent masked by a non-blocking re-find (INV-002) | Revert to base B1 status writes |
| 5 | Medium | Exit-code-only caller runs an empty reviser (INV-003) | Keep REVISE decision, drop `next` |
| 6 | Low | Additive fields only | Remove the fields |
| 7 | Low | Mistaken defer cannot be undone (INV-008) | Add an undefer command later |
| 8 | Medium | Old binaries fail on new files (INV-018); revise wedge (INV-005) | Keep storing the keys until all readers upgrade |
| 9 | Low | None (document content) | Remove the section |
| 10 | Low | None (record only) | n/a |

## Review Status
- [x] Auto-approved (default, non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14
