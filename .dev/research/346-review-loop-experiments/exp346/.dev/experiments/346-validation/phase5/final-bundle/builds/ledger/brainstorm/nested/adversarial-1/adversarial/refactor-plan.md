# Refactoring Plan: Merge into Base (Variant B)

## Overview

- **Base**: Variant B, `variant-2-sonnet-analyzer.md` (sonnet:analyzer), selected in `base-selection.md` (combined score 0.899 against A 0.882 and C 0.819; margin under 5%, decided by the debate tiebreaker, B 22 points won outright).
- **Incorporated variants**: Variant A, `variant-1-opus-architect.md` (kernel, contract and adapter split; `PROFILES` table and profile-computed `blocking`; one JSON state object with per-row history; derivable ledger path; `plan-r<k>.md`; `E-REPORT-EDITED`, `E-NOT-CHANGED`; V1-ledger; `dup_of` proposals; actor inferred from the subcommand). Variant C, `variant-3-haiku-backend.md` (`loop_decision` and `delivery_outcome`; `cannot-verify`; inputs bound to round, document hash and ledger sequence; nonblocking lock with `--op`, request digest and `--expect-seq`; old-side ranges and deletion tombstones; anchor relocation with `anchor_state=missing|ambiguous`; integrity term).
- **Binding inputs**: orchestrator decisions D1 to D11 (cited as Dk), the 22 split-point resolutions in the `## Proposed resolution of split points` tables of `round2-rebuttal-{A,B,C}.md`, the scoring matrix in `debate-transcript.md`, and all 27 UNADDRESSED items of `invariant-probe.md` (9 HIGH: INV-004, INV-006, INV-007, INV-008, INV-013, INV-021, INV-022, INV-027, INV-028). Every UNADDRESSED item is applied below; the ones applied only in part, because they conflict with a D decision, are listed at the end of the rejection section with the reason.
- **Base strengths preserved unchanged** (from `base-selection.md`): the root-cause trace (F22, N5, N12) and trace-grounded predictions (s1, s9, s10); minor rows mechanically unanswerable (s2, s3); the fresh sweep, its location classes and the hidden-defect share H, and the six baseline sweeps (s4, s9); the install naming trap and the copy-plus-drift test with `## Unattended mode` omitted (s6); the honest causes table (s10); no second computed stop for spec-panel, with data (s4).
- **Base fixes planned**: X-016 (FR-8 and FR-9 blocking with no field; fixed by the profile, Change 17), X-017 (`disputed` used as status and as flag; Change 19), and the `late` sweep-row terminology (Change 21).
- **Planned change count**: 65 (s1: 2, s2: 13, s3: 15, s4: 8, s5: 1, s6: 9, s7: 1, s8: 1, s9: 10, s10: 1, s11: 3, s12: 1).
- **Overall risk**: Medium. Three changes are High: Change 7 (`begin` auto-claim can admit a minor edit that shares a paragraph with a blocking row, which weakens the base's main lever), Change 13 (the subagent sweep route is UNVERIFIED for an Orca worker) and Change 52 (the headline union depends on a blinded human ruling that does not exist yet). Most other changes rename or tighten rules the three advocates already agreed in Round 2.

## Planned Changes

Changes are grouped by the base section they edit. "s<n>" means base section n of `variant-2-sonnet-analyzer.md`. Confidence figures are from the `## Scoring Matrix` of `debate-transcript.md`.

**Base section 1: Problem and evidence**

### Change 1: State what the ledger is not claimed to change (from invariant probe)
- **Source**: INV-027 recommended resolution; B s10 ("Why two fix cycles cannot be promised to converge").
- **Target**: s1, append one bullet after "Claim of this spec".
- **Rationale**: INV-027 (HIGH) shows the review-3 bar can fail on B1 x r1 x r2 alone, and B s10 already rates fix-induced defects LEFT. The claim must say the ledger is not claimed to change r, and that "ledger alone meets the bar" is falsified if the measured B1 x r1 x r2 exceeds 3 in either replicate. D11 pre-registers the same quantities.
- **Integration point**: the existing last bullet of s1; forward reference to s9 (Change 54).
- **Risk**: Low. Narrows a claim; no mechanism changes.

### Change 2: Add the S1 brief alias to the citation list (from invariant probe)
- **Source**: `invariant-probe.md` header (alias `BR` for `W/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/task-text/`).
- **Target**: the citation-alias paragraph above s1, append `BR`.
- **Rationale**: Changes 7, 12, 33 and 51 cite the S1 brief texts (`BR/T05-...`, `BR/T06-...`, `BR/T09-...`) that INV-006, INV-021 and INV-022 opened. The base marks unopened files UNVERIFIED (S-002, Variant B, 90%), so the new citations need an alias in the same list.
- **Integration point**: the alias paragraph; s12 item 10 (the base's UNVERIFIED note that "the other briefs were not opened" is narrowed in Change 65).
- **Risk**: Low. Citation hygiene only.

**Base section 2: Mechanism**

### Change 3: Split the design into kernel, contract and adapter (from Variant A)
- **Source**: A s2 component table (kernel `scripts/review_ledger.py`, contract `sc-review-ledger/SKILL.md`, adapter `/sc:spec-panel-ledger` with profile `spec-panel`).
- **Target**: s2, insert the three-row component table before "Names used below".
- **Rationale**: S-004 (Variant A, 90%): the explicit split is the reuse seam adopters need; B-R2 "Updated assessment" adopts A's frame. `base-selection.md` "Strengths to Incorporate" item 1. D8 names the split as binding.
- **Integration point**: s6 file table (same three files), s7 adoption (Change 49), the `PROFILES` table (Change 17).
- **Risk**: Low. Names an existing layout; no behavior change.

### Change 4: Replace the subcommand set and drop the role flag (orchestrator decision D8)
- **Source**: A s2 and s6 subcommands (`init`, `find`, `answer`, `begin`, `verify`, `sweep`, `close`, `status`) plus `revert-unclaimed` and read-only `verdict` (C-R2 C-027 row); D8 ("Actor follows from the subcommand; no `--as` flag").
- **Target**: s2 step table, restructure the "Script calls" column; remove every `--as` mention in s2, s3 and s6.
- **Rationale**: C-027 (Variant A + C, 90%) and C-004 (Variant A, 90%); X-006 (Variant A, 90%). B-R2 concedes `--as` "proves nothing" (base-selection weakness list). Base subcommands map as: `add` in find to `find`, `add` in verify plus `mark` to `verify`, `open` to `begin`, `revise-check` folded into `answer` output, `show` and `render` folded into `status` and `close`, `defer` kept (Change 29).
- **Integration point**: the s2 step table, the s3 transition table (Change 20), the s6 CLI table (Change 42), the command bullets (Change 40).
- **Risk**: Medium. Every downstream table is renamed; a missed rename leaves a dangling subcommand. Mitigation: the Change 46 text pin lists the subcommand names.

### Change 5: Derive the ledger path from the document and fix the folder layout (orchestrator decision D8)
- **Source**: A s3 "Location" and "Layout"; D8 (`<doc dir>/<doc stem>.review-ledger/`, overridable by `--ledger`).
- **Target**: s2 "Names used below", replace `L = .dev/orca-command-refactor/review/ledger.jsonl` and `L.snap/` with the A layout (`ledger.json`, `snapshots/r1.md r2.md r3.md`, `inputs/`, `plan-r2.md plan-r3.md`); s3 "Location" paragraph, replace. In S1, `L = .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/`.
- **Rationale**: C-002 (Variant A, 90%), X-008 (Variant A, 90%), X-019 (Variant A, 90%): a derivable path survives a lost flag, which is the 427 failure "without them the run is a first review" (B-R2 New evidence 5). Base reasons (a) to (e) for a plain worktree file outside `DOC` and outside `.claude/` still hold and are kept.
- **Integration point**: s3 Location, s6 command Setup bullet, s9 arm definition (Change 51); `init --archive-existing` (Change 45).
- **Risk**: Low. The reports stay in `review/`; only the ledger moves next to the document. The analyst collects two folders instead of one.

### Change 6: The script writes a verify plan per review (from Variant A)
- **Source**: A s2 "Review 2" step 1 and s3 layout (`plan-r<k>.md`).
- **Target**: s2 item 3 (Verify), replace "prints, per `fixed` row, the claimed text plus its hunk with 3 lines of context" with: `begin` writes `L/plan-r<k>.md` listing every blocking row in `open`, `fixed` or `reopened` with frozen grade, wrong outcome, old anchor and its hunks (old and new text, 3 lines of context); every `verified` row whose span a hunk touched; every unclaimed hunk with bytes; every reviser `gap` entry (Change 28); the auto-claim list (Change 7).
- **Rationale**: `base-selection.md` "Strengths to Incorporate" item 1 names `plan-r<k>.md`; D4 requires the verifier to answer "every plan row", which needs a plan file that the script, not the model, writes.
- **Integration point**: Change 10 (verify answers are keyed to plan rows), Change 7, Change 8.
- **Risk**: Low. Replaces printed output with a file; same content.

### Change 7: `begin` auto-claims hunks that overlap a blocking row's paragraph (orchestrator decision D1)
- **Source**: D1; INV-006 recommended resolution (second option); INV-008 (claim limit).
- **Target**: s2, insert a new item between item 2 (Revise) and item 3 (Verify), titled "Admission at `begin`".
- **Rationale**: INV-006 (HIGH): the S1 reviser briefs never run `answer` (`BR/T06-R1-reviser-L10-3bb70411.txt`, "apply confirmed findings"), so under base rules every hunk is unclaimed and each cycle makes no progress. D1 keeps the reviser briefs verbatim and makes `begin` claim, with `claimed_by=script-location`, every hunk that overlaps the mapped span of an `open` or `reopened` blocking row, widened to its enclosing paragraph; a hunk overlapping two rows is claimed by both; a row with a claimed hunk moves to `fixed`. Reviser answers, when present, are applied first and auto-claim fills only the remaining hunks. The auto-claim count is reported as a compliance metric (INV-006; Change 57).
- **Integration point**: s3 T3 (Change 27 for answered claims), `caused_by` as a list (Change 26), the plan (Change 6), s10 minor-row cause (Change 61).
- **Risk**: High. A minor fix written in the same paragraph as a blocking row is admitted as part of that row's fix; the flg-r2 F22 edit to AC-0.4 would be admitted if AC-0.4 also held a blocking row's span. That leak is measured by `minor_touched` (Change 58) and stated in the predictions (Change 59).

### Change 8: Unclaimed hunks are reported by default and reverted only with consent (orchestrator decision D2)
- **Source**: D2; `src/superclaude/commands/spec-panel.md:475` ("Modify specifications without explicit user consent and validation", under "Will Not"); INV-007 and INV-030 recommended resolutions.
- **Target**: s2 item 2, replace the `revise-check` exit 7 loop ("repeat until exit 0") and the `revert-unclaimed` sentence.
- **Rationale**: INV-007 (HIGH): the debate never chose who may revert. D2 decides: by default `begin` reports unclaimed hunks (no blocking row overlaps them), counts their bytes and lists them in the plan, and never reverts. Only when the invocation line carries `--revert-unclaimed` does `begin` restore the snapshot text for those hunks, preimage-checked, each revert logged with bytes discarded. If a preimage check fails, that hunk is not reverted and the round records `cannot-verify` for it instead of stalling (INV-007). `begin` never stalls on unclaimed hunks. Reverted bytes feed the growth report (INV-030, Change 58). A reviser may still run `revert-unclaimed` on its own hunks.
- **Integration point**: Change 7 (claimed set), Change 9 (paragraph comparison), s6 command Usage (Change 40), s12 open question 2 (closed by Change 65).
- **Risk**: Medium. Without the flag, minor edits outside blocking paragraphs survive and the F22 chain can recur; S1 passes the flag (D1), so the experiment is protected, but a default user run is not.

### Change 9: Admission compares paragraphs, not raw lines (from invariant probe)
- **Source**: INV-019 recommended resolution; D2 ("a pure rewrap is not unclaimed").
- **Target**: s2 item 3, add one sentence to the hunk rule: for admission only, the script compares paragraphs (runs of non-blank lines joined with single spaces); raw line hunks are kept for evidence and for `HUNKS_LARGE`.
- **Rationale**: INV-019 (MEDIUM): a rewrapped paragraph changes every line under line-based `difflib` and would become an unclaimed hunk. C-R2 holds that structural whitespace is not harmless; paragraph comparison keeps every non-whitespace change and drops only reflow.
- **Integration point**: Change 7 (claim widening uses the same paragraph unit), Change 25 (raw and normalized changed sets).
- **Risk**: Low. A one-word change inside a long paragraph makes the whole paragraph the admission unit, which is already the D1 claim unit.

### Change 10: Verify answers every plan row with four results (orchestrator decision D4)
- **Source**: D4; C-R2 C-021 row; C s6 VERIFY schema (`resolved|open|regressed|cannot-verify`, `sentence_sound`); B s3 T7 (child row).
- **Target**: s2 item 3, replace "answers exactly two questions per `fixed` row".
- **Rationale**: C-021 (Variant B + C, 90%). Every plan row, not only `fixed` ones, gets exactly one result with an evidence quote present in the new snapshot (a deletion cites the old span and the new boundary, C-R2) and `touched_ok`; `touched_ok=no` requires a child row in the same batch (base T7, X-015 Variant B, 90%). A missing answer is refused `E-INCOMPLETE` (A). `cannot-verify` feeds the escalation term (Change 32). INV-012 (ADDRESSED) is kept as written.
- **Integration point**: s3 transitions (Change 20), s4 `X` term (Change 32), s6 `verify` row (Change 42).
- **Risk**: Low. All three advocates accepted this rule in Round 2.

### Change 11: One new-defect check over both diff sides, with no row cap (orchestrator decision D4)
- **Source**: D4; C-R2 and B-R2 C-016 rows; C s6 (old and new ranges, deletion boundaries).
- **Target**: s2 item 4, replace.
- **Rationale**: C-016 (Variant A + B, 90%), X-004 (Variant A + B, 90%). Reviews 2 and 3 both check this round's hunks on old and new sides, including deletion tombstones, with the base's `depends_on` exception; no row-count cap; a verifier that cannot cover every hunk answers `cannot-verify`, which escalates; oversize hunks only warn (`HUNKS_LARGE`). B-R2 New evidence 2: both flg-r2 fix-induced defects (N1, N12) arrived as new rows in changed text.
- **Integration point**: Change 12 (allegations outside the hunks), Change 25 (diff storage).
- **Risk**: Low. Base already had the check; this widens it to the old side.

### Change 12: Allegations outside the hunks become `scope=outside` rows (orchestrator decision D4)
- **Source**: D4; INV-022 recommended resolution (second option).
- **Target**: s2 item 4, insert after the anchor rule; s3 T1 check text; s5 `origin=` row (Change 39).
- **Rationale**: INV-022 (HIGH): the unchanged review-3 brief (`BR/T09-R3-reviewer-L11-1c9a7ec8.txt`) says "assume defects remain and look for them", so a verifier will find defects outside the hunks; base and A refused them (`E-OUT-OF-SCOPE`), leaving them in uncounted prose. D4: `verify` stores them as rows with `scope=outside` that never count toward `U` and never block the loop, but are counted in the headline with the sweep rows (`O` in D11, Change 52). The base's failure item 5 ("a model that cannot add a row anywhere may add it nowhere") is mitigated by the same rule.
- **Integration point**: s4 `U` definition excludes `scope=outside` (Change 31); s9 headline (Change 52).
- **Risk**: Medium. Out-of-scope rows could swell if a verifier runs a whole-document panel anyway; the count is then visible rather than hidden, which is the purpose.

### Change 13: Sweep in a fresh context on a copy of the accepted snapshot (orchestrator decision D5)
- **Source**: D5; INV-002 and INV-003 recommended resolutions; B-R2 New evidence 1 (subagent route UNVERIFIED, heartbeat cost); C s4 (sweep challenges); A s2 (`dup_of`).
- **Target**: s2 item 5 and the "Final sweep" row of the step table, replace.
- **Rationale**: C-012 (Variant B + C, 70%), C-039 (none, 90%), X-002 (Variant B + C, 90%). The sweep is one whole-document critique by a context that has not read the ledger, run on a copy of the accepted snapshot placed in a fresh temporary directory with no ledger; the prompt names only that copy (INV-002, INV-003). `sweep --prepare` makes the copy and prints only its path; `sweep --input` ingests rows and prints counts only. Preferred route: a subagent spawned by the terminal review session, used only if a pre-run smoke check shows a dispatched Orca worker can spawn one and the session sends a heartbeat before and after it; otherwise a sixth dispatch, declared as a deviation. Sweep rows are `deferred` with `round_found=sweep`; the script proposes `dup_of` candidates; a sweep blocker or a sweep challenge to a `verified` row makes `delivery_outcome = ESCALATE`, never a new cycle (A-011, Variant C, 70%). After a review-1 PASS with no revision and an unchanged document hash the sweep is skipped and recorded `sweep_skipped=review1_pass` (C-030, X-013, Variant A, 90%). `sweep` records live `D` against the snapshot hash and reports a mismatch as post-terminal edits, not as a loop integrity failure (INV-003).
- **Integration point**: s4 delivery rule (Change 31), s9 arm and cost (Changes 51, 62), Change 21 (terminology), Change 57 (sweep report citing a ledger row id fails V1-ledger).
- **Risk**: High. The subagent route is unproven and a long Agent call can miss the 5-minute heartbeat (`T09` wrapper line 31, cited in B-R2); the fallback adds a session and is a declared deviation.

### Change 14: Add a terminal phase that refuses further loop work (orchestrator decision D6)
- **Source**: D6; INV-004 recommended resolution.
- **Target**: s2, insert after item 6; s3 "Forbidden and refused" paragraph, extend.
- **Rationale**: INV-004 (HIGH): the S1 dispatch list is fixed, so a review-3 `begin` after a review-2 PASS could open a new round over post-terminal edits and change a recorded outcome. After any terminal loop decision, `begin`, `answer`, `find` and `verify` refuse `E-TERMINAL` with a JSON body naming the decision and "do nothing further"; `status` reports post-terminal edits by document hash. The coordinator runs `status` before each dispatch (prose; in S1 the experiment coordinator does it). A-008 (none, 70%).
- **Integration point**: s4 cap and phases (Change 36), s6 exit codes (Change 42), s11 risk 8 (Change 63).
- **Risk**: Low. A refusal in a terminal state cannot lose work; the coordinator still has to read it.

### Change 15: Counters advance only on a committed `begin` (from invariant probe)
- **Source**: INV-018 and INV-025 recommended resolutions (INV-025 in part, see the rejection list).
- **Target**: s2 item 6 (Counting), replace "incremented only by `open`".
- **Rationale**: INV-018 (MEDIUM) and INV-025 (MEDIUM): it was unstated when the fix-cycle counter moves. Rule: the review counter advances only on a committed `begin` (or `init`); the fix-cycle counter advances only on a committed `begin` that admitted at least one claimed hunk (answered or auto-claimed); a zero-hunk round still counts as a review, its new-defect check is recorded `complete-empty` (never `cannot-verify`), and the round result lists "no edits admitted". A crashed reviser's edits are handled by the D1 auto-claim at the next `begin`; no refusal is added (D2).
- **Integration point**: s4 `n` definition (Change 31), cap refusals (Change 36), Change 38 (zero findings).
- **Risk**: Low. Makes an implicit counter explicit; fixtures cover the zero-hunk round (Change 46).

**Base section 3: Ledger file**

### Change 16: One atomic JSON state object replaces JSON Lines (orchestrator decision D8)
- **Source**: A s3 "Format" and example; D8 ("one atomic JSON state object (rows with history, sequence, saved operation results)").
- **Target**: s3 "Format" paragraph and the JSONL example, replace with one pretty-printed object (`schema: 1`, `profile`, `doc`, `cap_reviews`, `round`, `fix_cycles`, `phase`, `seq`, `snapshots`, `decisions`, `ops` (saved results by request digest), `rows`, `body_sha256`), rebuilt on the base's real-shape rows (F10, F22, N12) with renamed fields.
- **Rationale**: C-001 (Variant A, 90%), S-005 (Variant A, 90%). One object with per-row `history` gives the audit trail of C's events without a reducer (B-R2 "Updated assessment", C-R2 transaction table "Event replay ... Drop"). The base's stdlib-only reason (`json`, no PyYAML) still holds.
- **Integration point**: every s3 table, s6 transaction subsection (Change 44), Change 30 (body hash).
- **Risk**: Medium. The example must be rewritten consistently with Changes 17 to 29; an inconsistent example is the kind of intra-variant contradiction that cost B a terminology criterion.

### Change 17: `blocking` is computed by a profile; `sev` is removed (base fix X-016)
- **Source**: A s3 "Computed fields" and s6 `PROFILES` seam; B-R2 "Resolution of X-016"; D8 ("profile computes `blocking`, fixing X-016").
- **Target**: s2 item 1, replace "refuses `sev=blocking` with grade MAJOR unless ..."; s3, insert a "Computed fields" paragraph; drop `sev` from every row and from `init --scale/--needs-outcome` (replaced by `init --profile spec-panel`).
- **Rationale**: X-016 (Variant A + C, 90%), C-009 (Variant A + C, 70%), X-014 (Variant A + C, 90%). The base command bullet says "CRITICAL and FR-8/FR-9 are blocking" but no field carries FR-8/FR-9. The reviewer now supplies `grade`, `rule` and `wrong_outcome`; profile `spec-panel` computes `blocking = grade == CRITICAL or rule in {FR-8, FR-9} or (grade == MAJOR and wrong_outcome non-empty)`, copying `spec-panel.md:259` (B-R2 New evidence 5); non-blocking rows are `deferred` by the script. `PROFILES` maps a profile to vocabulary, predicate, cap and optional guards (Change 37). Test from B-R2: `rule=FR-8, grade=MINOR` is blocking, not deferred.
- **Integration point**: s3 frozen fields (Change 18), s4 `U` (Change 31), s7 (Change 49), s9 P3 by grade.
- **Risk**: Low. All three advocates accepted it; it removes a reviewer-supplied hole.

### Change 18: Replace the frozen-field list (from Variant A)
- **Source**: A s3 frozen list; C s3 (frozen original issue text); B-R2 C-008 row.
- **Target**: s3 "Frozen after `add`" paragraph, replace.
- **Rationale**: C-008 (Variant A + C, 90%). Freeze `id`, `label`, `round_found`, `origin`, `scope`, `caused_by`, `grade`, `rule`, `wrong_outcome`, `blocking`, `anchor`, `at` and the original finding text; any later input carrying one for an existing id is refused `E-FROZEN`. Relocation mappings and later evidence are separate records (C-R2 C-008 row). The base's argument (no upward drift) is kept.
- **Integration point**: Change 17 (`grade`, `rule`), Change 23 (relocation records), Change 26 (`caused_by` list).
- **Risk**: Low.

### Change 19: Five statuses; `disputed` is a claim flag (base fix X-017)
- **Source**: B-R2 "Resolution of X-017"; C-R2 X-017 row.
- **Target**: s3 T4 and T8, replace; "Forbidden and refused" paragraph, adjust.
- **Rationale**: X-017 (Variant B, 90%); `base-selection.md` marks B NOT MET on consistent terminology partly for `disputed` used as both status and flag. Statuses are `open`, `deferred`, `fixed`, `verified`, `reopened`. A dispute is `claim.action=disputed` on an `open` or `reopened` row; the verifier must rule `dispute=accepted|rejected` with evidence about the original harm; an unruled, rejected or uncertain dispute at the cap counts as an open blocker (C-006, Variant B, 70%).
- **Integration point**: Change 20 (transition table), Change 10 (verify answers).
- **Risk**: Low.

### Change 20: Rewrite the transition table (from Variant B with Variant A and C rules)
- **Source**: B s3 T1 to T11; A s3 error codes (`E-ILLEGAL`, `E-FROZEN`, `E-NOT-CHANGED`, `E-INCOMPLETE`, `E-ANCHOR`); C s3 (history-derived reopen); B-R2 C-005 and C-022 rows.
- **Target**: s3 "Status transitions" table, restructure: keep numbered rows with a phase column; replace the "Who may" column with "Requested by (subcommand)"; add A's named error code per row.
- **Rationale**: C-005 (Variant B + C, 90%), S-006 (Variant A + B, 90%), C-022 (Variant A + B, 90%), X-021 (Variant B + C, 90%). Rules: `fixed` to `verified` only from `fixed` or a ruled dispute; `fixed` to `open` when no earlier verification exists, else `reopened` (history, not last status, decides, C); script resets `verified` to `fixed` when a hunk overlaps the row's mapped span (base T9); `regressed` on an untouched `verified` row is refused `E-NOT-CHANGED`; a lexical cross-check (an identifier named in a verified claim appears in a hunk) is a warning line in the plan, not a status change (B-R2 C-022 row).
- **Integration point**: Changes 7, 10, 19, 21, 27, 29.
- **Risk**: Medium. The table is the core contract; a missing edge stalls a run. Each edge gets a named test (Change 46).

### Change 21: Remove `late` as a row kind (base fix, sweep terminology)
- **Source**: `base-selection.md` (B NOT MET on consistent terminology: "`late` rows with status `open`"); A s2 (`round_found=sweep`, status `deferred`); D5 ("Sweep rows are `deferred`").
- **Target**: s2 item 5, s3 T11 and example, s4 pseudo-code, s9 metrics: replace every `late`, `origin == late` and `Lt`.
- **Rationale**: Base T11 says a sweep row goes to "open, immutable" while s2 calls it `late`, and `origin` is also used for `find|changed|depends`. New terms: sweep rows have `round_found=sweep`, status `deferred`, and a `location` class (`in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks`, kept from base s2 item 5); the sweep blocking count is named `S` (C s4), defined in Change 31.
- **Integration point**: Changes 13, 31, 52.
- **Risk**: Low. Rename only; the location classes, which are a preserved base strength, stay.

### Change 22: Anchor quote rules (from Variant A)
- **Source**: A s3 "Anchor rules"; B s2 item 1 (`--at`).
- **Target**: s2 item 1 and s3, replace "byte-present once" with: the quote is whitespace-normalized, at least 12 characters, must occur exactly once in the named snapshot (`E-ANCHOR` if absent, `E-ANCHOR-AMBIGUOUS` if repeated, `--at <line>` disambiguates); the error text lists candidate lines (base s11 risk 1).
- **Rationale**: C-018 (Variant A + B, 70%), C-042 (Variant A + B, 70%: minimum length plus a warning, not refusals that stall runs). Absence and ambiguity stay refusals because a row without a location cannot be verified; short or generic quotes below the warning threshold only warn.
- **Integration point**: Change 23 (relocation starts from the frozen quote).
- **Risk**: Low.

### Change 23: Relocate anchors across revisions with `anchor_state` (from Variant C)
- **Source**: C s3 "Anchor relocation and edit ownership"; D8.
- **Target**: s3, insert a subsection "Anchor relocation" after the anchor rules.
- **Rationale**: A-009 (Variant C, 90%), C-019 (Variant C, 90%: the only relocation algorithm that handles unrelated edits and deletions). Keep the frozen quote and line forever; each `begin` appends a mapping (snapshot hash, current span, method): unchanged-block line mapping first, then unique exact quote with context; a rewritten quote maps to the replacement span only when the old span contains it and the new span is in the computed hunk. A row that cannot be mapped gets `anchor_state=missing|ambiguous`, cannot become `verified`, and enters the escalation term (Change 32). An empty replacement is a tombstone, not proof of resolution.
- **Integration point**: Change 24 (coordinates), Change 25 (hunks), Change 20 (T9 retouch uses the mapped span).
- **Risk**: Medium. The algorithm is new code with several branches; fixtures for deletion, repeat and rewrite are required (Change 46).

### Change 24: Half-open line ranges on named snapshots (from invariant probe)
- **Source**: INV-014 recommended resolution; D8; C s6 (`1-based half-open line ranges`).
- **Target**: s3, insert one paragraph "Coordinates"; replace inclusive forms such as `"r2:220-220"` in the example.
- **Rationale**: INV-014 (MEDIUM): an off-by-one silently skips or wrongly fires the `verified` to `fixed` reset. All spans and hunk ranges are half-open `[start, end)` lines on a named snapshot (`r2:[220,221)`); a zero-width deletion at position p overlaps `[s, e)` when `s <= p <= e`; a span is relocated into the old-side snapshot of a diff before any overlap test; one fixture per edge.
- **Integration point**: Changes 7, 20, 23, 25, 26.
- **Risk**: Low. A convention, enforced by fixtures.

### Change 25: Store diffs with old and new ranges and deletion tombstones (from Variant C)
- **Source**: C s6 (diff paragraph: raw and whitespace-normalized changed sets, zero-context old and new ranges, insertion and deletion boundaries); A s3 snapshots; B-R2 C-003 resolution.
- **Target**: s2 item 3 hunk sentence and s3, insert "Diffs": `begin` saves `L/diffs/c<k>.json` with raw old and new ranges, deletion boundaries and content digests; raw hunks drive ownership and hashes; normalized hunks drive the new-defect scope and the admission paragraphs (Change 9).
- **Rationale**: C-003 (Variant A + C, 70%), C-020 (Variant C, 70%), X-020 (Variant C, 70%), A-010 (Variant C, 90%): new-side-only ranges lose deletions, and A's coordinates mixed snapshots. `difflib` with autojunk disabled; no git call (base reason kept).
- **Integration point**: Changes 9, 11, 24, 26; s12 open question 8 (hunk parity, kept).
- **Risk**: Low.

### Change 26: Limit claim width; make `caused_by` a list (orchestrator decision D1)
- **Source**: INV-008 recommended resolution; D1 ("wider claims refused `E-CLAIM-WIDE`; `caused_by` is a list"); C-R2 C-023 row.
- **Target**: s3, insert under T3; s3 frozen fields (`caused_by` list, Change 18); s10 row 2 ("A reviser can still widen a blocking fix under the same row id").
- **Rationale**: INV-008 (HIGH): a reviser-supplied claim had no size limit, so one row could sponsor edits across a section, and a hunk claimed by two rows had no way to name both parents. Claim limit: a claim span may not exceed the row's mapped span widened to its enclosing paragraph (the D1 auto-claim unit); wider claims are refused `E-CLAIM-WIDE`. A child row's `caused_by` lists every row that claimed its hunk. C-023 (Variant A + C, 70%): the script records location attribution only; the analyst adjudicates causation for M3.
- **Integration point**: Changes 7, 27; s9 M3 (Change 57).
- **Risk**: Medium. A paragraph can be long in a spec with dense bullets; `E-CLAIM-WIDE` frequency is an open question (Change 65).

### Change 27: `answer fixed` must name an edit inside the row's span (from invariant probe)
- **Source**: INV-009 recommended resolution; B s3 T3 ("`new_text` ... inside a changed hunk"); A s3 (`deleted: true`).
- **Target**: s3 T3 check, replace.
- **Rationale**: INV-009 (MEDIUM): the merged C-005 rule dropped the base's "inside a changed hunk" requirement, so a `fixed` claim with no edit reached the verifier. `answer` with `fixed` must name at least one hunk that changes or deletes text inside the row's mapped span, else it is refused `E-FIXED-NO-EDIT` (renamed from the probe's `E-NO-CHANGE`, see the rejection list); a reviser who changed nothing answers `not-fixed` or `disputed`. Auto-claimed rows (Change 7) satisfy this by construction.
- **Integration point**: Changes 7, 19, 26.
- **Risk**: Low.

### Change 28: Reviser gap entries are recorded as `scope=outside` rows (from invariant probe, adapted to D4)
- **Source**: INV-010 recommended resolution; D4.
- **Target**: s3, insert after T3; s6 `answer` input schema (Change 42); base s9 scope metrics.
- **Rationale**: INV-010 (MEDIUM): a legitimate gap fix outside every row is reverted (with `--revert-unclaimed`) or left unclaimed, and the gap survived only in the disposition prose. A reviser that runs `answer` may add `gap` entries (anchor on unchanged text, reason); the next plan lists them; the verifier may file each as a row with `origin=reviser-gap`, which D4 stores as `scope=outside`, never blocking, counted in `O` of the headline and separately in M3. The probe's blocking form is not taken (rejection list).
- **Integration point**: Changes 6, 12, 52.
- **Risk**: Low. Only active when the reviser runs `answer`, which the S1 reviser briefs do not ask for.

### Change 29: `defer` is a record of the user's words and changes no recorded outcome (from Variant B)
- **Source**: B s3 T10; C-R2 X-017 row ("a quote claiming user permission cannot clear a real blocker or change a recorded escalation"); B-R2 closing paragraph (C-007 kept).
- **Target**: s3 T10, replace "blocking, any open state to deferred" with: after a terminal decision, `defer --id --quote "<user words>"` appends a `user_deferred` record to the row's history; the row's status, the recorded `loop_decision`, `delivery_outcome` and every headline count are unchanged; the analyst reports the records.
- **Rationale**: C-007 (Variant B, 70%) keeps user-only demotion; C-R2 and B-R2 both add that it cannot change the recorded verdict. `defer` is the one write allowed in the terminal phase (Change 14).
- **Integration point**: Change 14, Change 52.
- **Risk**: Low.

### Change 30: Keep the body hash on the new state object (from Variant A)
- **Source**: A s3 "Integrity"; B s3 `body_sha256`; C-024 row.
- **Target**: s3 Format paragraph, replace `LEDGER_TAMPERED` exit 3 with `E-TAMPERED` (A's name) over the canonical JSON without the hash key.
- **Rationale**: C-024 (Variant A, 70%: body hash plus report-tail check catches both edit paths). The tail check is Change 35. Detects hand edits; not a security boundary (A s3). Base s12 open question 4 (`reseal`) is kept.
- **Integration point**: Changes 16, 35.
- **Risk**: Low.

**Base section 4: Termination rule**

### Change 31: Separate `loop_decision` from `delivery_outcome` (from Variant C)
- **Source**: C s4 (`loop_decision`, `delivery_outcome`, `S`); D5; C-R2 transaction table.
- **Target**: s4 pseudo-code, replace; result table, replace the "Result" column with `loop_decision` and add a `delivery_outcome` column.
- **Rationale**: C-013 (Variant C, 90%: no early final PASS), X-001 (Variant B + C, 90%). `U = count(blocking rows with scope=in and status in {open, fixed, reopened})`; `loop_decision = PASS | CONTINUE | ESCALATE` as base, never CONTINUE at review 3; `S = sweep blocking rows + blocking sweep challenges to verified rows + incomplete sweep`; `delivery_outcome = ESCALATE if loop_decision == ESCALATE or S > 0, else PASS`, set only by `sweep` (or by the review-1 `close` when the sweep is skipped). Base worked example on flg-r2 counts (S-007, Variant B, 70%) is kept with the new names.
- **Integration point**: Changes 13, 21, 32, 34; s9 headline.
- **Risk**: Low. All three advocates accepted the split.

### Change 32: Add the integrity and structural escalation term (from Variant C)
- **Source**: C s4 (`X_r`, `I`); B-R2 C-010 row.
- **Target**: s4 pseudo-code, insert before the `U == 0` test: `if not I or X > 0: ESCALATE`, where `X` counts `cannot-verify` answers, `anchor_state=missing|ambiguous` rows, failed revert preimages (Change 8) and coverage overflow; `I` is a valid state object, intact snapshots and complete row answers.
- **Rationale**: C-010 (Variant B + C, 70%: B's count without a no-progress halt plus C's integrity and structural escalation). Without it, `cannot-verify` has no effect on the decision.
- **Integration point**: Changes 8, 10, 11, 23.
- **Risk**: Medium. One `cannot-verify` ends the loop; a verifier that overuses it ends runs early. The count is reported per replicate.

### Change 33: `close` accepts the reviewer's own verdict and appends the script tail (orchestrator decision D3)
- **Source**: D3; INV-021 recommended resolution (second option); A s2 step 4.
- **Target**: s4 "report footer" and "report last line" lines, replace; s2 item 6, replace the last sentence.
- **Rationale**: INV-021 (HIGH): the review-1 brief requires "a numbered findings list ... and a PASS or FAIL verdict" (`BR/T05-R1-reviewer-L11-699ae853.txt`) and the review-3 brief says "any finding of any severity is FAIL" (`BR/T09-R3-reviewer-L11-1c9a7ec8.txt`), so a `close` that refuses a reviewer table or verdict fails every session. D3: the reviewer writes what the brief asks; `close` never refuses it and appends `## Ledger` (rendered rows), the Reviser brief (CONTINUE only), `ledger-verdict: <loop_decision> U=<U> S=<S> review: <n> of 3` and, as the very last line, the script verdict. The analyst records every reviewer-versus-script verdict disagreement (Change 57). This overrides the Round 2 C-029 consensus ("`close` refuses a report that does"), which D3 replaces.
- **Integration point**: Changes 34, 35, 57; s6 command Verdict bullet (Change 40).
- **Risk**: Medium. Two verdicts sit in one report; analysts must read the last line. The tail protection (Change 35) and the string rules (Change 34) make the last line unambiguous.

### Change 34: Fix the last-line strings before and after the sweep (orchestrator decision D3)
- **Source**: D3; INV-024 recommended resolution; C s4 (CONTINUE renders `verdict: FAIL`).
- **Target**: s4 pseudo-code tail and the result table "Next" column, replace.
- **Rationale**: INV-024 (MEDIUM): a review-2 report ending `verdict: PASS` followed by a sweep with two blockers reproduces A's hollow PASS. Strings: CONTINUE ends `verdict: FAIL`; a loop-terminal report written before the sweep ends `loop: PASS (sweep pending)` or `loop: ESCALATE (sweep pending)`, with no `verdict:` line from the script; the sweep report ends `verdict: PASS` or `verdict: FAIL` from `delivery_outcome` (ESCALATE maps to FAIL); a review-1 report with the sweep skipped ends `verdict: PASS`.
- **Integration point**: Changes 31, 33, 38.
- **Risk**: Low.

### Change 35: Protect report tails at every later step (from Variant A)
- **Source**: A s4 (`E-REPORT-EDITED` at the next `begin`); D3 ("`begin` refuses an edited script tail"); INV-011 recommended resolution.
- **Target**: s4, insert after the strings paragraph.
- **Rationale**: INV-011 (MEDIUM): the last loop report and the sweep report have no next `begin`. Rules: `begin` refuses `E-REPORT-EDITED` when the prior report's script tail differs from the recorded tail digest; `sweep` (or, when the sweep is skipped, the review-1 `close`) re-checks the tail of every prior report against the recorded decisions; the V1-ledger analyst step runs `status` once after the last dispatch and records the result (Change 57). The tail is regenerated idempotently after a crash (C-R2 C-029 row).
- **Integration point**: Changes 30, 33, 57.
- **Risk**: Low.

### Change 36: Enforce the cap with a tested constant (orchestrator decision D7)
- **Source**: D7; A s4 (`CAP_REVIEWS = 3`); C s4 (refusals under a new op id); B-R2 C-043 row.
- **Target**: s4 "Cap text and the sweep" paragraph, replace the enforcement sentences; keep both pinned strings verbatim (`CANONICAL_CAP_TEXT` at `tests/skills/test_review_severity_rule.py:215` and the at-cap clause).
- **Rationale**: C-043 (Variant A + C, 90%). `CAP_REVIEWS = 3` with a test tying the constant to the text; the script refuses a fourth review (`E-CAP`), a third fix cycle, a second sweep (`E-SWEEP-DONE`) and a second `init` or `find` on an existing ledger, even under a new op id; an identical retry returns the committed result instead of using a slot (Change 44). Base reason "the sweep is outside the 3-review cap" is kept (INV-016 ADDRESSED).
- **Integration point**: Changes 14, 15, 44, 46.
- **Risk**: Low.

### Change 37: Monotonicity is an rf-qa profile guard, not a `close` flag (orchestrator decision D7)
- **Source**: D7; B s4 "No second computed stop"; A-R2 and B-R2 New evidence on `rf-qa.md:401,407`.
- **Target**: s4 last paragraph, replace "`close --monotonic`, default off" with: no monotonicity halt in profile `spec-panel`; `PROFILES` may list ordered guards, and a later `rf-qa` profile would carry regression, then monotonicity, then cap with its existing halt messages.
- **Rationale**: C-014 (Variant B, 70%), X-003 (Variant B + C, 70%): blocking fell in all six S1 runs, so the guard never fires; rf-qa's own order is regression first (`rf-qa.md:407`, verified by A-R2 and B-R2). A guard set by profile, not by flag, cannot be switched on by a brief.
- **Integration point**: Change 17 (`PROFILES`), Change 49 (rf-qa adoption).
- **Risk**: Low. Preserved base strength 6; only the switch moves.

### Change 38: A review 1 with zero findings is a valid PASS (from invariant probe)
- **Source**: INV-017 recommended resolution.
- **Target**: s4 result table, append a row; s6 `find` row, add "accepts an empty rows array".
- **Rationale**: INV-017 (LOW): a strict schema could refuse an empty `find`. `find` accepts `[]`; `close` prints the zero-row table and ends `verdict: PASS`; the sweep is skipped (`sweep_skipped=review1_pass`, Change 13); one fixture.
- **Integration point**: Changes 13, 34, 46.
- **Risk**: Low.

**Base section 5: Difference from PR 427**

### Change 39: Update the duty table to the merged mechanism (consequential, from D1 to D4)
- **Source**: B s5 table; A s5 table; Changes 4, 7, 8, 12, 13, 33.
- **Target**: s5 table, replace the "Ledger variant" and "What is removed" cells for `origin=`, minor rows, review count and verdict, per-fix check, late findings; add a row "Out-of-hunk findings" (427: `origin=unchanged` minor notes; ledger: `scope=outside` rows, counted, never blocking).
- **Rationale**: The base table names `add`, `open`, `revise-check` and "`add` rejects an anchor outside a hunk", all changed by D4 and D8. The base's "What the ledger does NOT remove" paragraph and its two-trace check are kept unchanged (preserved strength 1).
- **Integration point**: Changes 4, 12, 13, 33.
- **Risk**: Low.

**Base section 6: Exact changes, file by file**

### Change 40: Rewrite the command's loop bullets (orchestrator decision D10)
- **Source**: D10; B s6 outline (eight one-line bullets); A s6 Setup bullet; D1 to D6.
- **Target**: s6 "`spec-panel-ledger.md` outline", replace the Usage sentence and the eight bullets of `## Review Ledger Loop`.
- **Rationale**: The base bullets name `--as`, `add`, `open`, a ledger that is required as a flag, and a sweep that reads `DOC`. New Usage: `SP:22` minus `--re-review ... --baseline ...` plus `[--ledger <dir>] [--revert-unclaimed] [--sweep]`; the `--unattended` usage line is dropped. Bullets, one line each: (1) Setup: critique only; invoke `Skill sc-review-ledger` (dual lookup, `~/.claude/skills/` first); ledger is `--ledger` or `<doc dir>/<doc stem>.review-ledger/`; `init` if absent, else `begin`; a refusal stops the run and never falls back to a first review. (2) Find: full panel; findings as rows with `grade`, `rule`, `wrong_outcome`, anchor; the script decides blocking. (3) Verify: answer every row in `plan-r<k>.md`; one new-defect check on this round's hunks; anything else is filed `scope=outside`. (4) Sweep: only on the copy `sweep --prepare` prints; never open the ledger folder. (5) Report: write what the brief asks; never edit the lines `close` appends. (6) Cap: the canonical sentence verbatim and the at-cap clause; `review: N of 3` comes from the script. (7) Reviser contract: revise only text a listed blocking row names; minor rows are not answerable; unclaimed edits are reported and, with `--revert-unclaimed`, restored. (8) Precedence: a brief may narrow scope, not widen it, and cannot change a grade or a script verdict.
- **Integration point**: Change 41, Change 46 (text pins count eight bullets and the names).
- **Risk**: Medium. Each bullet must stay one line for line matchers (B s6) and must avoid `BANNED_SEVERITY_PHRASES`; `test_review_severity_rule.py` runs first, as the base already says.

### Change 41: The command refuses a standalone `--unattended` (orchestrator decision D10)
- **Source**: D10; INV-026 recommended resolution.
- **Target**: s6 outline, insert one line before the loop bullets: "spec-panel-ledger has no unattended mode" printed and stop, when `--unattended` appears as a standalone token.
- **Rationale**: INV-026 (LOW): omitting `## Unattended mode` keeps `test_worker_contract.py:831-839` green (X-009, Variant B, 90%) but a later brief passing `--unattended` would be silently ignored and an ESCALATE could wait on a person. A one-line refusal is explicit and is not a `## Unattended mode` heading, so the set-equality test stays green.
- **Integration point**: Change 46 (the drift test asserts the line exists).
- **Risk**: Low.

### Change 42: Rewrite the CLI table and exit codes (orchestrator decision D9)
- **Source**: D9; A s6 CLI table; C s6 (JSON stdout, `verdict` only decision-coded); B-R2 C-027 row.
- **Target**: s6 "Script CLI" paragraph and table, replace.
- **Rationale**: X-007 (Variant C, 90%), C-027 (Variant A + C, 90%), S-008 (Variant A + C, 90%). Columns: subcommand, caller (inferred), inputs, writes, output, checks, exit. Rows: `init [--archive-existing]`, `find`, `answer`, `begin [--revert-unclaimed]`, `verify`, `sweep --prepare | --input`, `close`, `status`, `revert-unclaimed`, `defer`, `verdict`. Every committed operation exits 0 whatever the decision; refusals use distinct non-zero codes (1 usage, 2 input refused, 3 state refused including `E-TERMINAL`, `E-CAP`, `E-REPORT-EDITED`, 4 lock or sequence conflict); only `verdict` maps PASS, CONTINUE, ESCALATE to 0, 10, 11. A retry may return an older result, so callers read fresh `status` before acting (C-R2).
- **Integration point**: Changes 4, 14, 36, 43, 44.
- **Risk**: Medium. Base `close` exit 10 and 11 are referenced in s2, s4 and s11 risk 8; every mention must move to `verdict`.

### Change 43: JSON stdout and inputs bound to round, document hash and sequence (from Variant C)
- **Source**: C s6 (stdout object, actor input envelope `packet_sha256`, `document_sha256`, `data`); C-R2 C-034 row.
- **Target**: s6, insert under the CLI table.
- **Rationale**: C-004 (Variant A, 90%, "C's packet binding added"), C-034 (Variant C, 70%). Success stdout: `{ok, seq, phase, review, fix_cycles, counts, loop_decision, delivery_outcome, next_action, artifact_paths}`; errors `{error, detail, next_action}`; diagnostics on stderr. Every input file carries `round`, `document_sha256` and `ledger_seq`; a stale binding is refused, so resumed or cached output from an older round cannot be ingested.
- **Integration point**: Changes 44, 50.
- **Risk**: Low.

### Change 44: Add a "Transaction, crash and rerun" subsection (orchestrator decision D8)
- **Source**: D8; C s6 "Transaction, crash and rerun contract" (reduced per C-R2 machinery table); INV-005 recommended resolution.
- **Target**: s6, insert a subsection after Change 43; s7 paragraph on concurrent writers, replace (now in the kernel).
- **Rationale**: C-025 (Variant B + C, 90%). Under a nonblocking `fcntl.flock` on a stable lock file: validate, write snapshots and diffs by temp file plus fsync plus `os.replace`, then replace the state object the same way. Every mutation takes `--op` and `--expect-seq`. INV-005 (MEDIUM): idempotency is by request digest within the same phase and round, independent of op id: a new op id carrying a payload already committed returns the original result with `replayed: true`; only a different payload under a stale `--expect-seq` is refused. No event replay, no hard-link publish, no directory sync (D8). A reviser crash leaves `D` edited and uncommitted; the next `begin` treats it as input (Change 15).
- **Integration point**: Changes 15, 36, 42.
- **Risk**: Medium. Lock and digest code is easy to get subtly wrong; C-R2 keeps small failure tests for duplicate and different-op retries, stale sequence and two writers (Change 46).

### Change 45: `init --archive-existing` for reruns (orchestrator decision D8)
- **Source**: D8; INV-001 recommended resolution.
- **Target**: s6 CLI `init` row and the transaction subsection, insert.
- **Rationale**: INV-001 (MEDIUM): with a derivable path, an aborted replicate leaves a ledger that blocks `init` (`E-EXISTS`), pushing the operator to delete it by hand. `init --archive-existing` renames the old folder to `<stem>.review-ledger.aborted-<UTC timestamp>/` and records the rename in the new header; the experiment protocol requires it, never a manual delete (Change 51).
- **Integration point**: Changes 5, 36.
- **Risk**: Low.

### Change 46: One Tests subsection with named cases, fixtures and pins (from Variant A)
- **Source**: A s6 Tests; C s6 fixtures folder; B s6 text pins and drift test; D7; D10.
- **Target**: s6 "Tests, beyond the script suite", restructure into one "Tests" subsection.
- **Rationale**: S-009 (Variant A + C, 90%). Script cases: every transition edge and refusal code; profile blocking for CRITICAL, FR-8 with MINOR, MAJOR with and without outcome, MINOR; auto-claim (one row, two rows, no row); `E-CLAIM-WIDE`; `E-FIXED-NO-EDIT`; paragraph admission on a pure rewrap; unclaimed reported without the flag and reverted with it; failed preimage; `scope=outside`; `E-TERMINAL`; zero-hunk round `complete-empty`; empty `find`; half-open overlap and deletion edges; relocation with `missing` and `ambiguous`; identical payload under a new op id; stale sequence; two writers; `E-TAMPERED`; `E-REPORT-EDITED`; `CAP_REVIEWS == 3` tied to `CANONICAL_CAP_TEXT`. Command pins: both cap strings, eight one-line bullets, subcommand names, the `--unattended` refusal line, dual lookup order, no `## Unattended mode`, no banned phrase, no cap above 2. Drift test kept as in the base. Fixtures in `tests/skills/fixtures/review-ledger/`.
- **Integration point**: every mechanism change.
- **Risk**: Low.

### Change 47: Update the new-files table (orchestrator decision D10)
- **Source**: D10; C s6 file table (fixtures folder); B s6 (naming trap, no `test_cli_install.py` edit).
- **Target**: s6 "New files" table, append `tests/skills/fixtures/review-ledger/`; the `SKILL.md` row adds "contract: layout, input schemas, `PROFILES`, CLI, how to add a profile"; the "Edited files: none" paragraph is kept.
- **Rationale**: Skill name `sc-review-ledger`, not `sc-spec-panel-ledger` (preserved base strength 4; A-R2 New evidence 5 confirms the trap is conditional on `install_skills.py:57`). X-010 (Variant B, 90%): `test_cli_install.py` is presence-only, no edit. S-013 (Variant A + B, 90%): one design doc, no user guide.
- **Integration point**: Change 3, Change 46.
- **Risk**: Low.

### Change 48: Align the experiment-install paragraph with D1 and D5 (orchestrator decision D1)
- **Source**: D1; D5; B s6 "Experiment install".
- **Target**: s6 "Experiment install (not a repo change)", replace the brief sentence.
- **Rationale**: Base text says "the briefs get the one-line name change and `--ledger <path>`". D1 fixes it: only the three review briefs change, by one line, `/sc:spec-panel` becomes `/sc:spec-panel-ledger --ledger <path> --revert-unclaimed`; reviser briefs stay verbatim. The sweep route follows D5 and is described in s9 (Change 51). Hand install, `make sync-dev`, `make verify-sync`, and never staging `.claude/` are kept.
- **Integration point**: Change 51.
- **Risk**: Low.

**Base section 7: Adoption**

### Change 49: Adoption goes through the `PROFILES` seam (from Variant A)
- **Source**: A s6 extension seam and s7 table; C-R2 C-031, C-032, C-033 rows; B-R2 matching rows; A-R2 New evidence 4; C-R2 New evidence 4.
- **Target**: s7, restructure: title names the real commands (`/sc:reflect`, rf-qa, the `/sc:implement` final review, S-001 Variant A, 70%); opening paragraph replaces "the script knows no spec-panel words" plus `--scale` with "an adopter adds one `PROFILES` row and an adapter section; a new guard needs kernel work and tests" (A-R2 narrowing); the concurrent-writer limit is removed (now in the kernel, Change 44); table cells updated.
- **Rationale**: C-031 (Variant B + C, 90%): reflect is future work, rows only after the evidence-validator gate, multi-file `--doc`, caller-owned loop, "ledger PASS cannot authorize promotion". C-032 (Variant B + C, 90%): rf-qa profile with ordered guards regression, monotonicity, cap and the existing halt messages, keeping its dedup identity (`rf-qa.md:414`, C-R2). C-033 (Variant B + C, 90%): implement not adopted; every archive attempt keeps a fresh full FINAL. Base order of adoption (spec-panel, rf-qa, reflect, implement last or never) is kept.
- **Integration point**: Changes 3, 17, 37.
- **Risk**: Low. Future work only; nothing in this change edits an adopter.

**Base section 8: Stateful reviewer session versus file ledger**

### Change 50: Resumed output must carry the current binding (from Variant C)
- **Source**: C-R2 C-034 row; B-R2 C-034 row.
- **Target**: s8, append one sentence to the recommendation.
- **Rationale**: C-034 (Variant C, 70%). The file ledger is authoritative; output from a resumed or cached session must carry the current round, document hash and sequence (Change 43) or is refused; a stateful-session arm stays a cheap later experiment, as the base says, outside this change.
- **Integration point**: Change 43.
- **Risk**: Low.

**Base section 9: Measurement plan on S1**

### Change 51: Redefine the "led" arm (orchestrator decision D1)
- **Source**: D1; D5; B s9 arm paragraph; B-R2 New evidence 1 (smoke check).
- **Target**: s9 "Arm led" paragraph, replace changes (1) and (3).
- **Rationale**: X-018 (Variant A + B, 90%: one-line brief change holds when sessions call the script). (1) In the three review briefs only, `/sc:spec-panel` becomes `/sc:spec-panel-ledger --ledger <L> --revert-unclaimed` (the flag is the consent D2 requires, given by whoever wrote the invocation line); reviser briefs verbatim. (2) Hand install as before. (3) Before replicate 1, one throwaway dispatched worker with the T09 wrapper spawns one subagent that reads a file and prints its hash; yes means the sweep is a subagent of the terminal review session, with a heartbeat before and after; no means a sixth dispatch on the copy that `sweep --prepare` prints, declared as a deviation. (4) Reruns use `init --archive-existing` (Change 45). (5) The coordinator runs `status` before each dispatch (Change 14).
- **Integration point**: Changes 13, 48, 62.
- **Risk**: Medium. The arm differs from Arm B in three recorded ways (name, flag, sweep route); all are disclosed.

### Change 52: Replace P3 and P3s with the D11 headline (orchestrator decision D11)
- **Source**: D11; INV-015 recommended resolution; B-R2, A-R2, C-R2 X-011 rows; A s9 (`dup_of`).
- **Target**: s9 Metrics, replace the P3 and P3s bullets; keep P3 (renamed `U3`) and H as secondary numbers.
- **Rationale**: X-011 (Variant C, 90%: the Arm B proxy counted MAJOR by grade, `ARMB:37`). Headline = |U3 union W union O|: `U3` = rows of grade CRITICAL or MAJOR not `verified` after review 3, deferred included; `W` = deduplicated sweep CRITICAL or MAJOR rows plus sweep challenges to verified rows; `O` = `scope=outside` CRITICAL or MAJOR rows (Changes 12, 28). INV-015 (MEDIUM): the script only proposes `dup_of` candidates; a blinded analyst rules duplicate, child or challenge (C-R2 New evidence 3: N5 and N12 overlap in AC-0.4 but are distinct harms); the headline uses the ruled count and publishes the raw count and the auto-matched count as bounds. A run that ends early is counted at its terminal review and carried to the R3 horizon without inventing a review (C-R2 X-011 row).
- **Integration point**: Changes 53, 54, 56, 60; s4 `S` (Change 31).
- **Risk**: High. The ruled count needs a blinded analyst step that is not built yet; until it runs, only the two bounds exist.

### Change 53: Publish the deferred floor and the control's comparable floor (from invariant probe)
- **Source**: INV-013 recommended resolution; D11.
- **Target**: s9 Metrics, insert after the headline.
- **Rationale**: INV-013 (HIGH): a deferred MAJOR row (no `wrong_outcome`) can never become `verified`, so it is a permanent floor on `U3`; with four such rows the bar is unreachable whatever the loop does. Publish the deferred CRITICAL or MAJOR count as its own number; pre-register whether the bar is applied with or without it; compute the control's comparable number (control MAJOR findings with no concrete wrong outcome) so both arms are measured on the same population.
- **Integration point**: Changes 52, 56, 57 (the `wrong_outcome` audit uses the same ruling).
- **Risk**: Medium. Computing the control floor needs a reading of the control reports by the same rubric; it is analyst work, not script output.

### Change 54: Pre-register B1, r1 and r2 per replicate (from invariant probe)
- **Source**: INV-027 recommended resolution; D11; A-012 row (none, 70%: recompute forecasts from each replicate's measured review-1 blocking count).
- **Target**: s9, insert a "Pre-registered quantities" paragraph before the Bar; s10 "Why two fix cycles" paragraph, add the falsifying condition.
- **Rationale**: INV-027 (HIGH): with B1 = 13 and r = 0.46 twice the bound is 2.7 before any sweep or deferred row; B1 of 39 at those ratios exceeds 3. B1, r1 and r2 are measured per replicate, U3 is reported against B1 x r1 x r2, and the claim "ledger alone meets the bar" is falsified if the measured product exceeds 3 in either replicate (Change 1).
- **Integration point**: Changes 1, 59.
- **Risk**: Low.

### Change 55: Run the baseline sweeps first and declare the consequence in advance (from invariant probe)
- **Source**: INV-028 recommended resolution; D11 ("baseline sweeps on the six existing finals first"); B s9 baseline paragraph; C-R2 C-040 row.
- **Target**: s9 "Baseline sweep" paragraph, replace the ordering and add the decision rule.
- **Rationale**: INV-028 (HIGH): pre-existing defects review 1 missed are "RELABELLED, not prevented" (B s10); if the baseline sweep finds 3 or more CRITICAL or MAJOR per document, the combined headline exceeds 3 even with U3 = 0. The six sweeps run before any ledger replicate, with the same sweep procedure as Change 13 (copy in a temp folder); if their mean CRITICAL or MAJOR count is 3 or more, the spec declares before replicate 1 that the combined bar cannot be met by the ledger alone, and U3 and the sweep are reported separately as the primary result. The base comparison (ledger sweep at least 2 above baseline means hiding) is kept.
- **Integration point**: Changes 52, 60.
- **Risk**: Low. Adds six sessions the base already counted.

### Change 56: Add Arm B as the second comparator (orchestrator decision D11)
- **Source**: D11; INV-029 recommended resolution; B s9 Bar last sentence.
- **Target**: s9 Bar, restructure: (a) the control comparison applies to the combined ledger-plus-427 claim; (b) Arm B is the comparator for the ledger's own effect: headline mean below 3.5 and growth at most 30.0% (`ARMB:20`).
- **Rationale**: INV-029 (MEDIUM): the ledger arm carries 427 grading through the profile, so a win against control credits both. D11 names Arm B as a second comparator; INV-029 calls it the primary one for the ledger's effect; this plan states both claims and which comparator each uses, following D11's wording.
- **Integration point**: Changes 52, 60.
- **Risk**: Low.

### Change 57: Mandatory validity checks (orchestrator decision D11)
- **Source**: D11; A s9 V1-ledger; INV-023, INV-006, INV-002, INV-011 recommended resolutions; D3; C-R2 C-040 row (recorded hashes); A-007 row.
- **Target**: s9, insert a "Validity checks" paragraph before Metrics.
- **Rationale**: C-040 (Variant A + B, 90%) and A-R2 New evidence 3 (`DEC:64` already applies the same rule to Arm B). Checks: (1) V1-ledger: the ledger shows rounds 1 to 3 or an earlier terminal decision, the snapshots, a sweep record or `sweep_skipped`, no `E-TAMPERED`; a replicate whose sessions never ran the script is "ledger not honoured"; a sweep report that cites any ledger row id fails V1-ledger (INV-002). (2) Blinded `wrong_outcome` audit, mandatory (INV-023): more than 30% of MAJOR-blocking rows judged filler marks the replicate "grading not honoured"; the cut-off is pre-registered; review-1 grade distribution is recorded (A-007, none, 90%). (3) Recorded command, skill and script hashes and live-versus-snapshot mismatch (C). (4) Auto-claim count per cycle (INV-006). (5) Every reviewer-versus-script verdict disagreement (D3). (6) One `status` after the last dispatch (INV-011). (7) M3 causation adjudicated by the analyst from the script's location attribution (C-023).
- **Integration point**: Changes 7, 13, 33, 35, 52, 53.
- **Risk**: Medium. Two checks need blinded human rulings; the cut-off value is a judgment and is fixed before data.

### Change 58: Report discarded and deferred bytes beside growth (from invariant probe)
- **Source**: INV-030 recommended resolution; A-008 row (growth from the accepted snapshot); B s9 Growth and Scope metrics.
- **Target**: s9 Growth bullet and Scope metrics bullet, replace.
- **Rationale**: INV-030 (MEDIUM): `--revert-unclaimed` and minor deferral cut bytes mechanically, so growth at or under 44.4% can be met by discarding content. Growth is measured on the accepted snapshot after revise 2 (A-008), with beside it: bytes discarded by reverts, bytes of unclaimed hunks left in place, bytes inside deferred-row spans; a growth gain explained mostly by discarded bytes is reported "not attributable to better fixes". Scope metrics: `minor_touched` split into hunks admitted by an answer and hunks admitted by paragraph auto-claim (Change 7), unclaimed bytes, revert count, `E-CLAIM-WIDE` count, `scope=outside` count.
- **Integration point**: Changes 7, 8, 60.
- **Risk**: Low.

### Change 59: Re-base the predictions on measured inputs and state the auto-claim caveat (from Variant B, with orchestrator decision D1)
- **Source**: B s9 Predictions table and bullets; A-012 row; D1.
- **Target**: s9 Predictions, modify: keep the three trace rows; relabel the numeric forecasts "planning aids, not calibrated" (the consensus wording quoted in INV-027); replace the flg-r2 row's mechanism text.
- **Rationale**: C-036 (Variant B, 90%) and X-012 (Variant B, 90%): B's forecast is the most grounded and honest that the conservative bar may fail; it stays. Under D1 the flg-r2 row holds only if the F22 hunk falls outside every blocking row's enclosing paragraph in AC-0.4; if a blocking row shares that paragraph, auto-claim admits the F22 edit and the N5 and N12 chain can recur. That condition is checked on `HIST/spec-v2-after-round1.md` before the run and printed in the predictions. The forecasts are recomputed from each replicate's measured B1 (Change 54). Headline forecasts add the deferred floor (Change 53) and `O`, so the base's P3s figure of about 5.5 is a lower estimate for the headline.
- **Integration point**: Changes 7, 53, 54.
- **Risk**: Medium. The pre-run paragraph check is one replicate's history; a different reviser can place the minor edit elsewhere.

### Change 60: Rewrite the failure criteria for the new metrics (orchestrator decision D11)
- **Source**: B s9 "What result would mean the idea failed"; D11; Changes 52 to 58.
- **Target**: s9 failure list, replace.
- **Rationale**: Items: (1) headline mean 4 or more, or not below Arm B's 3.5 for the ledger's own effect; (2) ledger sweep at least 2 CRITICAL or MAJOR above the baseline sweep mean (kept); (3) `minor_touched` above 0 in either replicate with `--revert-unclaimed` on, reported by admission path; (4) a stall caused by the script (a refused call with no recovery path); (5) growth above 30.0% after discarded bytes are shown; (6) V1-ledger or the `wrong_outcome` audit failing in either replicate (the replicate is then not treatment, not a failure of the idea, and is rerun with `init --archive-existing`); (7) measured B1 x r1 x r2 above 3 falsifies "ledger alone meets the bar" (Change 54). A result inside the spread of both arms stays "not significant" (the experiment's own decision D6 in `DEC`, not orchestrator D6; kept).
- **Integration point**: Changes 52 to 58.
- **Risk**: Low.

**Base section 10: Which measured causes the mechanism removes and which it leaves**

### Change 61: Update the causes table and the hiding argument to the merged rules (from Variant B, with orchestrator decisions D1, D2, D4)
- **Source**: B s10; D1; D2; D4; INV-008.
- **Target**: s10 table rows 2 and 6 and the "strongest argument" items 1 and 5, modify; keep every other row and the B1 x r x r paragraph (preserved strength 5).
- **Rationale**: Row 2 ("Reviser applies minor rows"): mechanism becomes "`answer` refuses deferred rows; `begin` auto-claims only hunks inside a blocking row's paragraph; unclaimed hunks are reported, and reverted with `--revert-unclaimed`"; the remaining leak is a minor edit in a blocking paragraph and a claim no wider than `E-CLAIM-WIDE` allows (INV-008). Row 6 ("Pre-existing defects found late"): add "verify-time allegations outside hunks are now counted as `scope=outside`". Item 1: P3 can still fall by construction, but `O` and `W` enter the headline. Item 5: `verify` no longer refuses out-of-scope allegations, so the incentive to file nothing is reduced, and the `scope=outside` count is the new early-warning number next to `outside_hunks`.
- **Integration point**: Changes 7, 8, 12, 52.
- **Risk**: Low.

**Base section 11: Risks and costs**

### Change 62: Recount sessions, heartbeats and script calls (orchestrator decision D5)
- **Source**: D5; B-R2 New evidence 1; B s11 costs; C-041 row (Variant B, 70%).
- **Target**: s11 "Costs per loop", replace the sessions and script-call bullets; keep wall time and tokens.
- **Rationale**: Sessions: 5 if the smoke check passes (the sweep is a subagent of the terminal review session), else 6; plus the smoke-check worker and the six baseline sweeps for the experiment. The subagent route costs a heartbeat before and after the Agent call (T09 wrapper, B-R2). Script calls per loop with the new set: about 3 in review 1 (`init`, `find`, `close`), 0 to 2 per revise (the S1 reviser runs none), 4 per verify (`status`, `begin`, `verify`, `close`), 2 in the sweep (`sweep --prepare`, `sweep --input`), about 15 to 20, below the base's 20 to 31.
- **Integration point**: Changes 13, 51.
- **Risk**: Low. Estimates, marked UNVERIFIED as in the base.

### Change 63: Update the "ways the ledger could make the loop worse" list (from Variant B, with orchestrator decisions D1, D2, D6)
- **Source**: B s11 items 1 to 8; D1; D2; D6; INV-007; INV-019.
- **Target**: s11 numbered list, modify items 1, 7 and 8; append two items.
- **Rationale**: Item 1 (refusal stalls): unclaimed hunks no longer refuse (D2) and a failed preimage becomes `cannot-verify` (INV-007); the residual stall paths are anchor absence and `E-CLAIM-WIDE`. Item 7 (confounds): the sweep route and the `--revert-unclaimed` flag are added; reading `L` anyway is now detectable by a cited row id (Change 57). Item 8 (coordinator retries at the cap): `E-TERMINAL` and `verdict` exit 11 replace `close` exit 11. New item: auto-claim admits a minor edit in a blocking paragraph (Change 7). New item: two verdicts in one report can mislead a reader who stops before the last line (Change 33).
- **Integration point**: Changes 7, 8, 14, 33.
- **Risk**: Low.

### Change 64: Rewrite the MECHANICAL and PROSE table (from Variant B)
- **Source**: B s11 rule table; S-012 row; C-R2 S-012 row (separate schema validity, evidence presence and semantic truth).
- **Target**: s11 table, replace rows for `--as`, unclaimed hunks, claims in hunks, sweep independence, verdict; add rows for auto-claim, `--revert-unclaimed`, `scope=outside`, terminal phase, report tail, request-digest idempotency.
- **Rationale**: S-012 (Variant B, 90%): one end table with residual risk. Changed classifications: role identity stays PROSE (the actor follows from the subcommand, but any session can run any subcommand); sweep independence moves from PROSE to "MECHANICAL for the copy and the row-id check, PROSE for not opening the ledger folder"; the verdict line is MECHANICAL for the last line and PROSE for the reviewer's own verdict above it; auto-claim and revert are MECHANICAL with residual "a minor edit in a blocking paragraph".
- **Integration point**: every mechanism change.
- **Risk**: Low.

**Base section 12: Open questions**

### Change 65: Close answered questions, add new ones, narrow the UNVERIFIED list (orchestrator decisions D1, D2, D5, D8)
- **Source**: B s12; D1; D2; D5; D8; `invariant-probe.md` brief readings.
- **Target**: s12, restructure.
- **Rationale**: Closed: Q2 unclaimed hunks (D2), Q3 parallel writers (lock in v1, D8; multi-file stays open), Q6 sweep independence (D5), Q9 the coordinator brief (kept verbatim; D1 auto-claim answers it). Kept: Q1, Q4 (`reseal`), Q5, Q7, Q8 (hunk parity; also calibrate the paragraph unit on the three S1 history pairs). Added: the smoke-check result (D5); `E-CLAIM-WIDE` and auto-claim frequency on real documents; whether the blinded rulings (Changes 52, 53, 57) can be staffed before replicate 1. UNVERIFIED list: the probe opened `BR/T05`, `BR/T06` and `BR/T09` (no `--unattended` token in T05; the T09 whole-document instruction), so the base's "the other briefs were not opened" is narrowed to the briefs still unopened.
- **Integration point**: Changes 2, 8, 13, 44.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| S-005, C-001 | C: event replay as the only authoritative store (`events` array, status derived by replay) | D8 forbids event replay. One state object with per-row `history` gives the same audit trail without a second reducer every reader must trust (B-R2 "Updated assessment"; C-R2 machinery table "Drop from version 1"). The base's single-writer rule is kept; its JSON Lines format is replaced by A's object (Change 16), not by events. |
| C-025 | C: no-replace hard-link publish of artifacts and directory sync | D8 forbids hard-link publish and directory sync. C-R1 concession 7 asks for measured cost first; temp file plus fsync plus `os.replace` under a lock covers interrupted processes on one host (C-R2 machinery table). |
| X-006, X-018 | C: coordinator-only mutation (only the coordinator calls the script) | Cannot run under the one-line brief rule (C-R1 concession 1, cited in A-R2 and B-R2); X-006 goes to Variant A (90%): each session calls its own subcommand. C-R2 itself drops it. |
| C-016 | C: 200-line discovery limit | No discovery cap (D4; C-016 Variant A + B, 90%). C-R2 drops it: "never truncate evidence". |
| C-016, X-004 | C: one-row discovery budget, and discovery only in review 2 | Both flg-r2 fix-induced defects arrived as new rows in different rounds (N1 at review 2, N12 at review 3; B-R2 New evidence 2); C-R2 drops the quota. Reviews 2 and 3 both check hunks (D4). |
| C-039, X-002 | A: sweep inside the review-3 verifier's own context, after it has just verified the rows | The sweep would be anchored on the rows it just read (base s4 reason (b)); D5 requires a fresh context that has not read the ledger; X-002 (Variant B + C, 90%). A's later "fresh subagent" proposal is the D5 preferred route, conditional on the smoke check (Change 13). |
| C-014, X-003 | A: no-progress ESCALATE at review 2 when `B(2) >= B(1)` | Blocking fell in all six S1 runs (base s4: 11 to 9, 12 to 7, 9 to 5, 9 to 7, 16 to 5, 17 to 6), so it never fires; D7 keeps it only as a profile guard for rf-qa (Change 37). C-014 Variant B (70%). |
| C-036, X-012 | C: forecast of 1.5 for the R3 count | No basis; C-R1 conceded it was unsupported, and `base-selection.md` marks C NOT MET on "claims supported by evidence" for it. B's trace-grounded forecast is kept (C-036 Variant B, 90%). |
| C-036 | A: forecast of 2.5 (range 1 to 4) for the R3 count | Withdrawn by A (A-R2 "Updated assessment": "A's measurement forecast is withdrawn"). Its basis used the wrong row: R1 blocking in flg-r2 was 13, not 5 to 6 (A-R2 New evidence 2, `ARMB:13`, `F2D1:39`). |
| C-022, A-011 | A-R2: record supporting passages at verification time and re-queue a verified row when one changes; C: dependency-passage tracking for verified rows | Not in version 1: 0 of 19 prior blockers regressed across flg-r2 reviews 2 and 3 (B-R2 New evidence 2), which C-R2 accepts as limited evidence; a lexical cross-check warning (Change 20) and fresh-sweep challenges (Change 13) cover the case. |
| X-021 | A: `open` to `verified` transition (a verifier may verify a row nobody answered) | Only `fixed` rows, or ruled disputes, become `verified` (X-021 Variant B + C, 90%). Under D1, an untouched row stays `open`, and its plan answer is `open`. |
| X-009, C-028 | A: copy keeps `## Unattended mode` | `tests/skills/test_worker_contract.py:831-839` set equality would fail (X-009 Variant B, 90%; A-R2 New evidence 6 confirms). Base omission is kept and Change 41 adds the refusal line. |
| X-010 | A: edit `tests/unit/test_cli_install.py` baselines | Presence-only check at `:501`, no edit needed (X-010 Variant B, 90%; A-R2 New evidence 7). |
| X-019, C-002 | C: `<document-parent>/.review-ledger/<stem>/<run-id>/` with a random run id | A random id is not derivable by a fresh session; D8 adopts A's derivable path (X-019 Variant A, 90%). Reruns use `init --archive-existing` instead (Change 45). |
| X-007, C-027 | C: `verdict` exit codes 2 for CONTINUE and 3 for ESCALATE; B: `close` exits 10 and 11 | D9: committed operations exit 0; only `verdict` maps PASS, CONTINUE, ESCALATE to 0, 10, 11. B's `close` codes are dropped (B-R2 concession) and C's numbers are not used because 2 and 3 are refusal codes in the merged CLI. |
| C-029 | C: the script writes the whole report | B-R2 rejects it; the reviewer keeps the panel prose and the script appends the tail (D3, Change 33). |
| C-004 (packets) | C: separate `packet --kind` subcommand emitting packet files | A's `plan-r<k>.md` written by `begin` carries the same content (Change 6); binding by round, document hash and sequence is kept (Change 43). |
| S-013, C file table | C: `docs/user-guide/spec-panel-ledger.md` and `refs/schema-v1.json` | S-013 (Variant A + B, 90%): one design doc suffices for an experimental variant; C-R2 drops "extra version-1 documentation/schema machinery". Schemas are documented in `SKILL.md` (A). |
| C-042 | C: refusal limits of 200 initial rows and 10 MiB per document | C-042 (Variant A + B, 70%): warnings, not refusals that stall runs. `HUNKS_LARGE` stays a warning. |
| C-007 | C: no user-waiver API in version 1 | C-007 goes to Variant B (70%): `defer` is kept, but as a record that cannot change a recorded outcome (Change 29), which meets C-R2's own condition. |

**Invariant-probe resolutions applied only in part or in a changed form** (every other UNADDRESSED item is applied as recommended):

| Item | Recommended resolution | What this plan does instead, and why |
|---|---|---|
| INV-006 | Option 1: a one-sentence reviser-brief change, disclosed | Not taken. D1 keeps reviser briefs verbatim; option 2 (auto-claim at `begin`) is applied (Change 7). |
| INV-007 | Verify session may revert hunks overlapping no blocking row, after a preimage check | Applied in D2's form: the revert happens inside `begin`, only with `--revert-unclaimed` on the invocation line, because `spec-panel.md:475` forbids modifying a specification without consent. The preimage-failure fallback (`cannot-verify` instead of a stall) is applied as recommended (Change 8). |
| INV-009 | Refusal code `E-NO-CHANGE` | Applied with the code renamed `E-FIXED-NO-EDIT`, because A's `E-NOT-CHANGED` (regressed on an untouched row) is kept and two near-identical codes with different meanings repeat the terminology fault that `base-selection.md` charged against B (Change 27). |
| INV-010 | Verifier may file reviser gaps as rows with `origin=reviser-gap`, implicitly able to block | Applied without the blocking part: D4 says allegations outside the hunks never block the loop, so gap rows are `scope=outside`, counted in `O` and in M3 (Change 28). |
| INV-021 | Option 1: change the PASS/FAIL acceptance items of the three review briefs | Not taken. D1 allows only the one-line invocation change; option 2 (`close` accepts the reviewer verdict and appends the script verdict as the last line, analyst records disagreements) is applied (Changes 33, 57). |
| INV-022 | Option 1: replace "look for new defects" in the review-2 and review-3 briefs | Not taken, for the same reason as INV-021; option 2 (`scope=outside` rows) is applied (Change 12). |
| INV-025 | `begin` refuses `E-NO-ANSWERS` without consuming the round when edits exist with no answers and no auto-claim | The counter rule is applied (Change 15). The refusal is not added: D2 says `begin` never stalls on unclaimed hunks, and under D1 edits overlapping a blocking row are auto-claimed, so the only edits left are unclaimed ones, which are reported (or reverted with consent) and the round proceeds. A refusal here would stall the fixed S1 dispatch list, which base failure criterion 4 counts as a failure of the idea. |
| INV-029 | Arm B as the primary comparison for the ledger's own effect | Applied with D11's wording, "Arm B as a second comparator": the plan names which claim each comparator tests (control for ledger plus 427, Arm B for the ledger alone), which gives the same isolation (Change 56). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | Claim overstated in s1 | Drop the added bullet |
| 2 | Low | New brief citations unresolvable | Drop the alias; cite full paths |
| 3 | Low | Adopters lack a named seam | Remove the component table |
| 4 | Medium | Dangling base subcommand names in tables or bullets | Restore base names in the affected table; Change 46 pins catch misses |
| 5 | Low | Sessions look for the ledger in two places | Restore `review/ledger.jsonl` with `--ledger` required |
| 6 | Low | Verifier works from printed output, not a file | Restore base `open` printout |
| 7 | High | Minor edits in a blocking paragraph are admitted; the F22 chain can recur | Narrow the auto-claim unit to the mapped span (no paragraph widening); the leak is visible in `minor_touched` either way |
| 8 | Medium | Unclaimed minor edits survive in non-consent runs | Make `--revert-unclaimed` the default for experiment invocations only; S1 already passes it |
| 9 | Low | Rewraps reported as unclaimed | Fall back to line hunks for admission |
| 10 | Low | Rows skipped by the verifier | Restore base two answers per `fixed` row |
| 11 | Low | Deletion defects missed | Restore base new-side-only check |
| 12 | Medium | Verifier files many `scope=outside` rows, swelling `O` | Keep the rows but report `O` separately from the headline |
| 13 | High | Sweep anchored on the ledger, or missed heartbeats in the subagent route | Use the sixth-dispatch route only (base design) |
| 14 | Low | Post-terminal `begin` changes a recorded outcome | Remove `E-TERMINAL`; rely on coordinator `status` (prose) |
| 15 | Low | Cap counted on the wrong event | Restore base counter on `open` |
| 16 | Medium | Example and tables inconsistent with the new object | Restore JSON Lines with the renamed fields |
| 17 | Low | FR-8 or FR-9 rows deferred | Restore reviewer-supplied `sev` (reintroduces X-016) |
| 18 | Low | A field drifts between rounds | Restore base frozen list plus `rule` |
| 19 | Low | Disputes skipped | None needed; X-017 fix has no alternative that keeps one meaning |
| 20 | Medium | Missing edge stalls a run | Add the edge; each edge has a test |
| 21 | Low | Old `late` term left in a section | Search and replace; no behavior effect |
| 22 | Low | Short anchors match the wrong line | Raise the minimum length |
| 23 | Medium | Wrong relocation marks a fix verified on the wrong text | Set every unmappable row `anchor_state=missing` and escalate |
| 24 | Low | Off-by-one in retouch detection | Fixtures fail first; correct the comparator |
| 25 | Low | Deletion hunks lost | Keep new-side ranges plus tombstones only |
| 26 | Medium | `E-CLAIM-WIDE` refuses legitimate long-paragraph fixes | Raise the margin to a fixed line count (INV-008 alternative: 10 lines) |
| 27 | Low | `fixed` claims with no edit reach the verifier | Drop the check; the verifier answers `open` |
| 28 | Low | Gaps lost to prose | Drop gap entries; gaps go to the disposition note as in the base |
| 29 | Low | A user quote changes a recorded outcome | Remove `defer` entirely |
| 30 | Low | Hand edits undetected | Keep `LEDGER_TAMPERED` naming; behavior is the same |
| 31 | Low | Early loop PASS read as delivery PASS | Restore base single `final` with `Lt` |
| 32 | Medium | One `cannot-verify` ends runs early | Count `X` but escalate only at review 3 |
| 33 | Medium | Two verdicts confuse readers | Restore the C-029 consensus refusal and disclose a brief change (INV-021 option 1) |
| 34 | Low | Pre-sweep PASS mistaken for final | Restore base footer strings |
| 35 | Low | Edited final tail undetected | Keep `begin` check only |
| 36 | Low | Fourth review or third cycle slips through | Restore base `open` exit 11 |
| 37 | Low | A brief turns on a stop the data do not support | Restore `close --monotonic` default off |
| 38 | Low | Empty review 1 refused | Require at least one row and print a zero-row note |
| 39 | Low | s5 describes removed subcommands | Restore base table text |
| 40 | Medium | Bullet text trips a line matcher or a banned phrase | Revert to base bullets with renamed subcommands only |
| 41 | Low | `--unattended` silently ignored | Drop the refusal line |
| 42 | Medium | A caller treats CONTINUE as a crash, or ignores ESCALATE | Restore base exit codes on `close` |
| 43 | Low | Stale input ingested | Drop the binding; rely on `--expect-seq` |
| 44 | Medium | Double-applied or refused retries | Fall back to op-id-only idempotency (INV-005 risk returns) |
| 45 | Low | Manual deletes of old ledgers | Document a manual rename |
| 46 | Low | Untested edges | Add tests as defects appear |
| 47 | Low | Fixtures not packaged | List fixtures under `tests/` only |
| 48 | Low | Install text contradicts s9 | Point to s9 only |
| 49 | Low | Adopters read an outdated seam | Restore base s7 table |
| 50 | Low | Cached output from an old round ingested | Drop the sentence; Change 43 still refuses stale bindings |
| 51 | Medium | Arm differs from Arm B in an undisclosed way | Disclose each difference in the run log; fall back to the sixth dispatch |
| 52 | High | Headline unavailable without the blinded ruling | Publish the raw and auto-matched bounds as the result until the ruling exists |
| 53 | Medium | Arms compared on different populations | Publish the floor only, without the control figure, and mark the comparison incomplete |
| 54 | Low | Forecast not tied to measured inputs | Keep base fixed B1 = 13 forecast |
| 55 | Low | Hiding not measurable | Run baseline sweeps after the arm (base order) |
| 56 | Low | Ledger effect not isolated from 427 | Keep base single control bar |
| 57 | Medium | Non-compliant replicate counted as treatment | Keep V1-ledger only; mark audit results advisory |
| 58 | Low | Growth gain credited to discarding text | Report growth alone, as the base does |
| 59 | Medium | F22 prediction wrong because of paragraph auto-claim | Keep base prediction text with the caveat appended |
| 60 | Low | Failure criteria mismatch the metrics | Restore base list with renamed metrics |
| 61 | Low | s10 overstates what is removed | Restore base rows with a pointer to Change 7 |
| 62 | Low | Cost misstated | Restore base cost bullets |
| 63 | Low | Risk list misses the auto-claim leak | Append the two new items to the base list unchanged |
| 64 | Low | Table misclassifies a rule | Restore base table and append new rows |
| 65 | Low | Answered questions left open | Restore base s12 |

## Review Status

- **Status**: Auto-approved (default). No user review gate was requested for this step.
- **Timestamp**: 2026-11-08 (UTC date from the session environment; time of day not recorded).
- **Carried forward**: the 9 HIGH UNADDRESSED invariants that blocked the convergence gate (INV-004, INV-006, INV-007, INV-008, INV-013, INV-021, INV-022, INV-027, INV-028) are each closed by at least one planned change (Changes 14, 7, 8, 26, 53, 33, 12, 54, 55 respectively). The merge executor should re-run the invariant probe on the merged spec before treating the run status as complete.
