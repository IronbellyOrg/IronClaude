# ADJUDICATION-RESULT: C-02 ledger-clearing-and-verdict-authority

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge` flag). Date 2026-11-14. Return contract status: `partial`. Convergence score: 0.955 (21 of 22 diff points; threshold 0.80), but the debate's own status is BLOCKED_BY_INVARIANTS (3 HIGH invariants left unaddressed).

## Winner

A named hybrid that the debate itself produced, built on Variant B as the selected base: **Variant B as base, with Variant A's quorum gate, record-only evidence key and CRITICAL floor.** It is neither proposal unmodified; the merged statement of it is `merged-ledger-clearing-and-verdict-authority.md`.

Base selection (quoted from `adversarial/base-selection.md`): "Selected Base: Variant B (explicit per-row verification; `proposal-b.md`)". Scores:

| | quant_score | qual_score | Final score | Correctness criteria MET |
|---|---|---|---|---|
| Variant A | 1.000 | 24/30 = 0.800 | 0.9000 | 2 of 5 |
| Variant B | 0.996 | 25/30 = 0.833 | 0.9148 | 3 of 5 |

Margin 1.48 percentage points, below the 5% threshold, so the tiebreaker applied: Level 1 (debate points won) tied at 5 each; Level 2 (correctness criteria count) selected B (3 of 5 against 2 of 5). The raw combined score also ranks B first. Position-bias passes: pass 1 A 23/30, B 24/30; pass 2 B 25/30, A 24/30; two disagreements re-evaluated (A Correctness 4, B Clarity 1), both final MET.

## Rationale

From `base-selection.md` and the Round 2 final positions in `debate-transcript.md`: the only dimension where the variants differ is Correctness. A carried a terminology and factual error ("recorded completion state is `complete`", `--resolution` already carrying requested ids) and two feasibility defects (a dissent held at `resolved_check` is skipped by `apply_revision`, `ledger.py:328`; a quorum above the one-reviewer re-review deadlocks). B carried a B1/B7 contradiction and two feasibility defects (quote gate cannot clear a deletion fix; category predicate misgrades `document_review_loop_prompts.md:31`). Both advocates converged in Round 2, and the converged design is:

- Clearing (C-001, X-003): quorum gate over distinct `block_ok`-true reviewers typing `prior <lid> resolved`, `need = min(Q, requested)`, any valid `open|regressed` prior vetoes and routes the row to `regressed`, a same-round re-find wins, silence never clears (from A, with B's dissent state).
- Evidence quote (C-002, X-002): optional bounded `evidence` key, recorded only with `quote_in_doc`, never gating.
- Text binding (C-003): `pending_new_sha256`; `merge_round` refuses on mismatch; `revise` refuses while one is pending (from B).
- Blocking authority (C-004, X-004): typed `blocking` stays the authority, plus a CRITICAL floor applied in `merge_round`, `blocking_typed` kept, a warning per flip; no category predicate and no grader in the core.
- Prior-line rule (C-005, X-001): a prior moves only a `resolved_check` row; the pinned test is renamed and the `ledger.py:3-4` docstring edited.
- `defer` (C-006, C-007): owner and reason required, terminal and counted open, no expiry in the core, a re-found deferred row stays `deferred` and is listed as `refound_deferred`.
- Verdict surface (C-008, C-009): `brief_ids`, `verify_ids`, `held_ids` derived on read, `next` field, VM-6 derived refusal, stored `verdict`/`decision`/`brief_ids` dropped from new round records (VM-3 wording at `synth-06-conflict-log.md:178`, read by the B advocate).
- Measurement (C-010): A's three-arm replay plus B's M2 and M3.

Debate tally (scoring matrix): A wins 5, B wins 5, hybrid 6, tie 1, qualified or independent 4, unresolved 1 (S-002).

## Conditions under which the winner holds

Taken from the debate, not added:
- C-03 sets `Q(re-review) = 1`, or the `min(Q, requested)` rule is used, so a one-reviewer re-review (`panel.py:600`, all 8 packaged templates `apply_to: ["first"]`) can clear rows (A-005, X-003).
- The `--resolution`-absent fallback is still OPEN: Variant A says requested = the reports passed, Variant B says `need = Q` (fail closed); the debate did not settle it.
- Reviewers type one `prior` line per prior blocking row at an acceptable rate. This is unmeasured; if compliance is low, unanswered rows hold until the cap (3 reviews) and the loop ends in ESCALATE (both papers' Section 4/5). M2 (count compliance by ledger id in existing re-review reports) is the free check.
- The false-affirmation residue is accepted: a `prior resolved` is a self-report, the quote is recorded and does not gate. The debate names A's replay (three arms, wrongness rule registered before the run) and B's M1 as the measurements that would show the guard has the wrong strength.
- "No effect on reflect" holds for this slot only (A-004, QUALIFY); it reopens if the unified panel makes reflect a consumer of the review ledger.
- Round-1 partial panel (D-2, one valid block of N) stays with slot C-03.
- The pins asserting the old behaviour are rewritten together with the change (`tests/review/test_review_ledger.py:193-217`, `:376-385`, `:396-405`; `tests/review/test_review_cli.py:274-292`, `:298-313`).

## Invariants the debate left unaddressed (from `adversarial/invariant-probe.md` and the return contract)

Probe totals: 22 findings; 6 ADDRESSED; 16 UNADDRESSED (HIGH 3, MEDIUM 12, LOW 1). The HIGH items block convergence under the protocol's invariant gate; depth `standard` has no Round 3, so they are carried as open conditions. They are listed in the return contract `unaddressed_invariants`.

| ID | Severity | Category | Open condition |
|---|---|---|---|
| INV-001 | HIGH | collection_boundaries | `need = min(Q, requested)` can be 0 if `--resolution` carries an empty reviewers list (`merge_cmd.py:73-83` accepts it), which re-opens the silence clear; no floor such as `max(1, ...)` is specified |
| INV-002 | HIGH | interaction_effects | a valid `prior open` plus a same-round non-blocking re-find leaves a `regressed` non-blocking row in none of `brief_ids`, `verify_ids`, `held_ids` (`ledger.py:213-218`, `:235-238`); the round can pass over the dissent |
| INV-003 | HIGH | sufficiency_challenge | empty `brief_ids` with non-empty `verify_ids` stays REVISE (exit 10); exit-code-only callers run an empty reviser and an empty-diff re-review regresses fixed rows (`document_review_loop_prompts.md:44`, `spec-panel.md:262`); `next` is only in `ledger verdict` JSON and line 70 does not tell coordinators to read it |

MEDIUM, UNADDRESSED: INV-004 (`--resolution` absent: either fallback fails, one bypasses Q, one deadlocks), INV-005 (`pending_new_sha256` can wedge the loop; no force path), INV-006 (derived VM-6 pre-check must not fail on an empty ledger and does not block after a PASS), INV-007 (`refound_deferred` is unreachable in the one-row D-11 A shape because held-only is ESCALATE then VM-6 refuses the round), INV-008 (no undefer command; `--owner ""` satisfies "required"), INV-009 (an invalid-block reviewer's `prior open` is collected but ignored; an "incomplete" reviewer with a valid block counts toward `need`), INV-010 (dissent does not re-anchor the row; `apply_revision` still needs a hunk touching its span), INV-011 (prior ids are ledger ids `L<n>`, reviewers see `F<n>`; whether PRIOR is the merged report is unverified), INV-013 (an unexamined `prior resolved` clears; the quote is recorded, not gating), INV-014 (the hash exists only if `revise` ran), INV-016 (the CRITICAL floor keys on reviewer-typed severity; a re-classification to MAJOR non-blocking still drops the row), INV-018 (older binaries read `last["verdict"]` and fail; stored per-round verdicts cannot be reconstructed).

LOW, UNADDRESSED: INV-020 (a non-blocking `resolved_check` row is outside `verify_ids` and stays `resolved_check`; harmless to the verdict).

Unresolved diff point: S-002 (tag-discipline split, Low). Residual disagreement inside converged points: the `--resolution`-absent fallback (C-001) and the C-009 form (A did not re-read synth-06 after B verified the VM-3 wording).

## Adversarial artifacts

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/ledger-clearing-and-verdict-authority/`

- Merged output: `merged-ledger-clearing-and-verdict-authority.md`
- Under `adversarial/`: `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`
- Supporting files under `adversarial/`: `round1-A.md`, `round1-B.md`, `round2-A.md`, `round2-B.md` (advocate statements, assembled verbatim into the transcript), `scorer-pass1.md`, `scorer-pass2.md` (position-bias passes with per-criterion CEV)
