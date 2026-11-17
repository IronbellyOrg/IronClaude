# Adjudication result: slot C-10 (pr-review-wire-format-and-slot)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, both advocates (Round 1 and Round 2), the fault-finder, three scorers, a plan reviewer and the merge-executor were separate agents. Everything below is taken from the debate's own artifacts (paths at the end); nothing here was added after the debate.

## Winner

**A hybrid on Variant A (Proposal A) as the base: the resolution the debate named C10-R, "separate pre-step, pure panel-to-Finding converter, sibling `panel` field".** The debate's own base selection (`base-selection.md`): "Selected Base: Variant A (Proposal A, `variant-1-original.md`; default model, default persona)", chosen by tiebreaker level 1 (debate performance), not by the weighted layers. The merged resolution is `merged-output.md`. Neither proposal won as written: both advocates, after Round 2, named the same superior approach on all 49 diff points by label (Variant A 9, Variant B 6, Hybrid 16, Neither 18; Round 1 label agreement was 33 of 49).

What C10-R is, as the debate produced it (A-R2 section 5, overall confidence 70%): the panel runs as a main-session pre-step before the snapshot gate; a new pure module on the `pr_submit` side takes `cluster_v2` output, the same reviewer records joined on `(reviewer_id, id)`, the PR's changed-line ranges, the PR-profile severity table, the requested reviewer ids and the head SHA, and returns `Finding`s through the unchanged `finding_from_comment`, `remap_severity` and `route`, plus a `dropped` list and the panel standing; the standing is a new sibling Output Contract field `panel`, never inside `reviewers`. `Finding`, `Severity`, the FSM, `REVIEWERS`, `merge_wait`, `reviewer_activity`, `reviewers.py` and the single python gate block are not edited. Variant B's slot axis (third name in `REVIEWERS`, third key in `reviewers`) and its four model-emitted line keys were conceded or withdrawn in B's own Round 1 and Round 2.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer (re-evaluation scorer, one counting rule per metric applied to both variants): A 0.9237, B 0.9359 (requirement coverage A 0.9412, B 0.8824; internal consistency A 0.9322, B 0.9552; specificity 1.0000 each; dependency completeness A 0.8333, B 0.8824; section coverage A 0.8889, B 1.0000). Pass 1 had A 0.9509 and B 0.9846; Pass 2 had A 0.9193 and B 0.9437; they used different units and standards, which is why a single re-computation was made.
- Qualitative layer (30 criteria, two position-bias passes, 7 of 60 pairs re-evaluated): A 23/30 = 0.7667, B 24/30 = 0.8000. Dimensions: Completeness A 4/5, B 4/5; Correctness A 2/5, B 2/5; Structure 5/5 each; Clarity A 4/5, B 5/5; Risk Coverage 3/5 each; Invariant and Edge Case 5/5 each.
- Combined: A 0.8452, B 0.8679. "Margin: 2.27% (0.0227; below the 5% threshold)". "Tiebreaker applied: Yes, level 1 (debate performance). Variant A won 9 points against 6 for Variant B" (the gap of 3 points is 6.1 percentage points of 49, above the 5% band; level 2 would have tied on Correctness criteria met, A 2 and B 2).
- Both layers are reported: the weighted layers favour B inside the 5% tie band (the lead comes from Clarity 4, where A fails on the unglossed "S1-S5", and from IC, DC and SC; A is ahead on RC only, R-14); the debate favours A.
- The debate's stated reasons: B conceded the slot axis (S-002 to S-004, C-004, C-005) and withdrew its model-emitted line keys, its `finding_from_v2` placement in `severity_router.py` and harness injection; A's verified defects (X-001: the cluster record holds no severity or category; X-002 and X-003: the pin claim and "50 files" (47 `test_*.py`); A-004: downstream also reads `in_diff`, `verification_status`, `fix_key` and comment ids) are corrected from the debate's own Round 2 content.
- Convergence: label agreement 49 of 49 (100%), content-adjusted 44 of 49 (0.90) against an 80% threshold; taxonomy coverage passed (L1 = 4, L2 = 30, L3 = 15 points). Status BLOCKED_BY_INVARIANTS (5 HIGH UNADDRESSED probe findings; see below). Standard depth has no Round 3, so none was debated.

## Conditions under which the winner holds (A-R2 section 5, all stated in `merged-output.md`)

1. First release is report-only: panel findings are converted, remapped, routed and listed in the summary and the `panel` field, but are not appended to `decision["used"]` and drive no push until the owner decides A-005, C-008 and INV-J.
2. The converter is pure (dict in and out), imports nothing from `cli/review`, `cli/reflect` or `cli/swarm`, uses no `gh` or `git` tokens, and converts per cluster, each in its own `try`; a malformed primary citation, join miss or empty claim is counted in `dropped`, never silent and never a batch drop.
3. Field rules: `body` is the representative's `claim` verbatim; `reviewer = "panel"` set by code; `confidence` and `original_line` unset; `in_diff` computed from `changed_ranges` (new code, since `pr_submit` has no hunk parser; A's premise that the pre-step holds the diff is [UNVERIFIED]).
4. Standing: `present` when every requested reviewer is `complete` (requested ids minus `complete_reviewers`); the field carries the reviewed head SHA, valid only for that SHA, once per head SHA, no automatic re-run after a fix push; the run summary never says "clean" while the panel is not `present`; models named in a PR report say "requested", not "served", until C-08.
5. Prerequisites owned elsewhere: FX-5 category parameters on `check_finding` (the core's 6 categories share no value with the router's 18, and one out-of-set category invalidates a reviewer's whole block); `snapshot_file_list` is the PR head file list; the PR template says the first citation is the defect location (C-07); the repair policy for over-limit lines (C-06).
6. Prose and test constraints: no new python fence in `SKILL.md` (pinned in four test files), no `src/superclaude/` path in installed prose (INV-F), new tests are new files.
7. On promotion, thread-less panel findings get one PR conversation follow-up and the skill-supplied reply and resolve callbacks skip findings with no integer `comment_id` (INV-K, prose-level and unpinned until a test exists).
8. Per-round panel cost is unmeasured (GQ-177, OQ-18); M1 is needed by both positions before the panel runs per round.

Contested and not answered by Variant A (recorded as contested in `merged-output.md` section 7, not as part of C10-R): B's AM-1 (one Finding per cluster and category), AM-2 (reviewer-severity side record; "never lowers a CRITICAL" struck), AM-3 (missing ranges degrade, never drop), AM-4 (zero-cluster standing, `blocking_clusters`, "not clean" wording), AM-5 (append the module to `CORE_PURE_FILES` versus a new test file), AM-6 (FX-5 minimum is the category set; PR head tree), D6 (converter invocation path). Content-unresolved diff points: C-001, C-002, C-006, S-004, S-008. Owner items open in both advocates' files: C-008, A-005, A-006.

What would change the resolution (A-R2 and B-R2): the converter's PR keys move toward the line format ("adapter now, extensible v2 later") if M3 is nonzero, a second consumer needs the same per-finding key, or M2 shows reviewer-stated `in_diff` is more accurate than the hunk computation; B: M4 near zero would simplify AM-1 to a fixture-only guard, and a decision that the first release has no summary would shrink D2 and D5 to wording.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 20 findings, 6 ADDRESSED (probe INV-004, 005, 013, 016, 017, 020), 14 UNADDRESSED. Convergence was blocked by the five HIGH items; standard depth has no Round 3, so none was resolved. The probe's ids (written "probe INV-0xx" in `merged-output.md`) collide with two prior-slot invariants, INV-003 (R-C01) and INV-007 (R-C03); they are different things.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-002 | HIGH | state_variables | Panel standing, reviewed SHA and dropped list have no durable home across `--resume`: the run log's 45-member EventType is pinned in three test lines, so a new panel event edits `models.py` and tests (contradicting "no existing module, no existing test edited"); reusing existing event types carries neither SHA nor dropped list. |
| INV-007 | HIGH | count_divergence | "Requested" is defined as the dispatched count, so a slot that fails to launch makes a 2-of-3 panel read present; `cluster_v2` sees only reviewers that produced a record. (Restates R-C03 INV-007.) |
| INV-008 | HIGH | count_divergence | A reviewer with an empty findings block is invalid, not complete, unless a non-empty Coverage slice was assigned (`findings_v2.py:291-298`, pinned by tests); a PR has no Coverage rows, so a clean panel can never read present and the AM-4 zero-cluster case is unreachable. |
| INV-011 | HIGH | collection_boundaries | The rule "present when every requested reviewer is complete" is vacuously true for an empty requested set (same defect class as D3, on reviewers instead of clusters). |
| INV-012 | HIGH | collection_boundaries | AM-1 splits by category only; a same-category cluster still pairs the maximum severity with the representative's unrelated claim and line, and the uncalibrated representative is the lowest-ordinal member. |
| INV-001 | MEDIUM | state_variables | The standing enum has no stale value, so after a fix push the report is absent (false) or present for an old SHA nothing makes the reader compare. |
| INV-003 | MEDIUM | state_variables | The checkout the reviewers see is not shown to equal the PR head tree used for `snapshot_file_list` and `changed_ranges` (dirty or untracked files). |
| INV-006 | MEDIUM | guard_conditions | Missing `changed_ranges` degrading to `in_diff` unset (True) is permissive for editing; nothing says the rule is report-only-only or that promotion must re-require ranges. |
| INV-009 | MEDIUM | count_divergence | The unit of "dropped" (cluster, category group, chain member) differs from the unit of "cluster", so a CRITICAL can be lost while standing stays present. |
| INV-010 | MEDIUM | count_divergence | `blocking_clusters` counts the reviewer-typed boolean, so a run can say clean beside a CRITICAL non-blocking cluster. |
| INV-014 | MEDIUM | interaction_effects | No rule excludes panel Findings from `dedup_groups` input, so a panel Finding could raise a bot group's route and breach "drive no push". |
| INV-015 | MEDIUM | interaction_effects | The "not clean" wording rule covers the run summary only, not the posted thread or the literal `terminal_clean` status (set at eight sites in `fsm.py`, panel-blind); the thread-less follow-up has no idempotency key. |
| INV-018 | MEDIUM | sufficiency_challenge | The converter's inputs (parsed blocks with the PR category set plus cluster output) cannot be produced by existing machinery: `review cluster` writes no parsed records and `parse_block` carries no category set; the invocation path (D6) is unspecified. |
| INV-019 | MEDIUM | sufficiency_challenge | `finding_from_comment` needs a positive int `comment_id`; a natural key map that passes the v2 finding id or cluster id raises for every cluster, and T1 would not catch it unless built from the converter. |

LOW UNADDRESSED: none. Return contract `unaddressed_invariants` (HIGH only): INV-002, INV-007, INV-008, INV-011, INV-012.

Also left open by both Round 2 advocate files (`merged-output.md` section 5): INV-G HIGH (mutually blind, mechanically read-only reviewers; launch path is C-07); INV-I HIGH (held as reporting only; nobody traced how `terminal_clean` is reached); INV-007 (R-C03) HIGH; INV-003 (R-C01) HIGH (repair step versus pins); INV-J MEDIUM (which tier is blocking); INV-K MEDIUM; INV-F MEDIUM (open until the prose exists); B only: INV-L (HIGH before promotion, MEDIUM in the report-only release) and INV-M (MEDIUM), both closed only by the contested AM-1 and AM-2.

## Return contract

Status `partial`; convergence score 0.90 (44 of 49 by content = 0.898; 49 of 49 by label); base variant `variant-1 (Proposal A; default model, default persona)`; unresolved conflicts 5 (C-001, C-002, C-006, S-004, S-008); fallback mode false; failure stage null; invocation method `task-agent`.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/pr-review-wire-format-and-slot/`

- Merged file: `.../pr-review-wire-format-and-slot/merged-output.md`
- Adversarial artifacts, all under `.../pr-review-wire-format-and-slot/adversarial/`: `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`, `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, `debate-transcript.md`, `invariant-probe.md`, `scoring-pass1.md`, `scoring-pass2.md`, `scoring-reeval.md`, `base-selection.md`, `refactor-plan.md`, `plan-review.md`, `merge-log.md`, `return-contract.yaml`
- This file: `.../pr-review-wire-format-and-slot/ADJUDICATION-RESULT.md`
