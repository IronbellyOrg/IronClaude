# Merge Log

## Metadata

- **Base**: Variant B, `variant-2-sonnet-analyzer.md` (sonnet:analyzer)
- **Executor**: merge-executor (claude-opus-5-5)
- **Plan**: `refactor-plan.md`, 65 changes, applied in plan order
- **Changes applied**: 65 of 65 (0 failed, 0 skipped)
- **Status**: Complete, with 13 executor notes recorded below (clarifications needed to keep the merged text consistent; none overrides a plan decision) and 2 open items for the orchestrator
- **Output**: `/home/coder/workspaces/worktrees/IronClaude/bs346-ledger/.dev/brainstorms/346-ledger/nested/adversarial-1/merged-output.md` (521 lines, 13 headings, 76 Source tags)
- **Timestamp**: 2026-11-08T15:53:25Z (merge start; same value as the spec's Merge date header)

## Changes Applied

Method: a stub with the provenance header and all 12 section headings was written first, then each section was filled with one Edit, in section order, applying that section's plan changes in plan order. "s<n>" means section n.

### Change 1: State what the ledger is not claimed to change
- **Status**: Applied
- **Source**: INV-027 recommended resolution; Base s10
- **Target**: s1, bullet after "Claim of this spec"
- **Before**: s1 ended at the claim bullet.
- **After**: new bullet: the ledger is not claimed to change r; "ledger alone meets the bar" is falsified if measured B1 x r1 x r2 exceeds 3 in either replicate; forward pointer to s9.
- **Provenance tag**: `Invariant probe INV-027 recommended resolution and Base s10, merged per Change #1`
- **Validation**: s9 "Pre-registered quantities" exists and states the same condition.

### Change 2: Add the S1 brief alias
- **Status**: Applied
- **Source**: `invariant-probe.md` header (alias `BR`)
- **Target**: citation-alias paragraph
- **Before**: aliases ended at `HIST`.
- **After**: `BR` added. Executor note 1: two sentences added so every reference resolves or is marked external: citations merged from A, C and the debate keep their authors' readings; D5, D6, D9, D10, D11 always mean decisions in `DEC` (external). A third sentence marks the base's undefined `SPEC` alias and `C-R3-10` label as UNVERIFIED, external (added during post-merge validation).
- **Provenance tag**: `Base (original, modified): alias BR added per Change #2; ...`
- **Validation**: every `BR/...` citation (T05, T06, T09) uses the alias.

### Change 3: Kernel, contract and adapter split
- **Status**: Applied
- **Source**: Variant A s2 component table
- **Target**: s2, before "Names used below"
- **Before**: no component table.
- **After**: three-row table (kernel, contract, adapter); adapter row points to s7.
- **Provenance tag**: `Variant A s2 component table, merged per Change #3`
- **Validation**: s6 New files lists the same three files.

### Change 4: Replace the subcommand set and drop the role flag
- **Status**: Applied
- **Source**: Variant A s2 and s6 subcommands; C-R2 C-027 row
- **Target**: s2 step table "Script calls"; every `--as` mention in s2, s3, s6
- **Before**: `init --scale/--needs-outcome`, `add`, `show`, `answer`, `revise-check`, `open`, `mark`, `close`, `defer`, `verdict`, `render`; `--as reviewer|reviser|coordinator`.
- **After**: `init`, `find`, `answer`, `begin`, `verify`, `sweep --prepare|--input`, `close`, `status`, `revert-unclaimed`, `defer`, `verdict`; actor follows from the subcommand. Executor note 2: base "Checks the script owns" line (role gate, idempotent close exit 4) folded into the Tests subsection of Change 46, because both items no longer exist; s5 "`render` output" became "the `## Ledger` table that `close` appends".
- **Provenance tag**: `Base (original, modified): "Script calls" column restructured ... per Change #4`
- **Validation**: grep finds no `--as`, `add`, `open --`, `mark`, `render`, `show` subcommand outside Source comments; s6 command pins list the 11 names.

### Change 5: Derive the ledger path; fix the layout
- **Status**: Applied
- **Source**: Variant A s3 Location and Layout
- **Target**: s2 Names; s3 Location
- **Before**: `L = .dev/orca-command-refactor/review/ledger.jsonl`, `L.snap/`; reasons (a) to (e).
- **After**: `L = <doc dir>/<doc stem>.review-ledger/` (S1 path given), A's layout block. Executor note 3: layout also lists `diffs/` (Change 25) and `.lock` (Change 44) so the block matches later changes; base reason (e) "next to the reports" no longer holds and was rewritten as (f) "next to the document ... the analyst collects two folders instead of one" (the plan's own risk text); A's derivability reason added as (a).
- **Provenance tag**: `Variant A s3 Location, merged per Change #5; Base (original, modified): ...`
- **Validation**: no `ledger.jsonl` or `L.snap` left; s9 arm uses `<L>`.

### Change 6: Script-written verify plan
- **Status**: Applied
- **Source**: Variant A s2 Review 2 step 1, s3 layout
- **Target**: s2 item 4 (Verify)
- **Before**: `open` printed claimed text plus hunk per `fixed` row.
- **After**: `begin` writes `L/plan-r<k>.md` with the five listed contents.
- **Provenance tag**: s2 item 4 tag citing Change #6
- **Validation**: s6 `begin` row writes `plan-r<k>.md`; command bullet 3 reads it.

### Change 7: `begin` auto-claims overlapping hunks
- **Status**: Applied
- **Source**: orchestrator decision D1; INV-006 option 2; INV-008
- **Target**: new s2 item 3 "Admission at `begin`" (between Revise and Verify)
- **Before**: no admission step; unanswered hunks were unclaimed.
- **After**: reviser answers first, then auto-claim with `claimed_by=script-location`, paragraph widening, two-row claims, row moves to `fixed` (new T4); auto-claim count reported; known leak stated.
- **Provenance tag**: `Orchestrator decisions D1 and D2, invariant probe INV-006 (option 2), INV-007 and INV-030, merged per Change #7 and Change #8`
- **Validation**: T4 in s3; `minor_touched` split in s9; risk item 9 in s11.

### Change 8: Unclaimed hunks reported by default, reverted only with consent
- **Status**: Applied
- **Source**: D2; `SP:475`; INV-007, INV-030
- **Target**: s2 item 2 and item 3
- **Before**: `revise-check` exit 7, "repeat until exit 0"; `revert-unclaimed` restores hunks.
- **After**: report by default; `--revert-unclaimed` on the invocation line restores with preimage check and logged bytes; failed preimage gives `cannot-verify`; `begin` never stalls; reviser may still revert its own hunks.
- **Provenance tag**: s2 items 2 and 3 tags citing Change #8
- **Validation**: X term in s4 counts failed preimages; growth bullet in s9 reports discarded bytes.

### Change 9: Admission compares paragraphs
- **Status**: Applied
- **Source**: INV-019; D2
- **Target**: s2 item 4 hunk rule
- **Before**: line hunks only.
- **After**: one sentence: paragraph comparison for admission; raw line hunks kept for evidence and `HUNKS_LARGE`.
- **Provenance tag**: s2 item 4 tag citing Change #9
- **Validation**: s3 Diffs says normalized hunks drive admission paragraphs; test case "paragraph admission on a pure rewrap" in s6.

### Change 10: Verify answers every plan row with four results
- **Status**: Applied
- **Source**: D4; C-R2 C-021 row; Variant C s6 VERIFY schema; Base T7
- **Target**: s2 item 4
- **Before**: two questions per `fixed` row.
- **After**: one result per plan row (`resolved|open|regressed|cannot-verify`), evidence quote, `touched_ok`, child row on `touched_ok=no`, `E-INCOMPLETE`.
- **Provenance tag**: s2 item 4 tag citing Change #10
- **Validation**: T6, T7, T8, T10 cover the results; `cannot-verify` in X.

### Change 11: One new-defect check over both diff sides, no cap
- **Status**: Applied
- **Source**: D4; C-016 rows; Variant C s6
- **Target**: s2 item 5
- **Before**: "one, bounded" check on new-side hunks.
- **After**: both sides, tombstones, reviews 2 and 3, no row cap, `cannot-verify` on incomplete coverage, `HUNKS_LARGE` warns.
- **Provenance tag**: s2 item 5 tag citing Change #11
- **Validation**: s5 Per-fix check row updated consistently.

### Change 12: Allegations outside hunks become `scope=outside` rows
- **Status**: Applied
- **Source**: D4; INV-022 option 2
- **Target**: s2 item 5; s3 T1; s5 (via Change 39)
- **Before**: an anchor outside a hunk was refused.
- **After**: stored as `scope=outside`, `origin=outside`, never in `U`, counted in `O`. Executor note 4: the plan does not name the status of these rows; they are stored `deferred` (T2), which is the reading that makes "never block the loop" hold mechanically and keeps them out of the Reviser brief.
- **Provenance tag**: s2 item 5 tag citing Change #12
- **Validation**: U definition in s4 excludes `scope=outside`; O in s9.

### Change 13: Sweep in a fresh context on a copy of the accepted snapshot
- **Status**: Applied
- **Source**: D5; INV-002, INV-003; B-R2 New evidence 1; Variant C s4; Variant A s2
- **Target**: s2 item 6 and the Final sweep row of the step table
- **Before**: sweep session told not to read `L`, reads `DOC`, `late` rows.
- **After**: `sweep --prepare` copy in a fresh temp dir, `sweep --input` counts only, subagent route conditional on the smoke check, sixth dispatch fallback, `deferred` rows with `round_found=sweep`, `dup_of` proposals, ESCALATE on sweep blocker or challenge, `sweep_skipped=review1_pass`, live hash check. Executor note 5: `sweep --input` takes `--report R` so the sweep report receives the last line that Change 34 and the tail re-check of Change 35 require; the plan's CLI row names only `--prepare | --input`.
- **Provenance tag**: s2 item 6 and step-table tags citing Change #13
- **Validation**: s4 S term, s6 CLI rows, s9 arm (3), s11 sessions all describe the same single sweep.

### Change 14: Terminal phase refuses further loop work
- **Status**: Applied
- **Source**: D6; INV-004
- **Target**: new s2 item 8; s3 Forbidden paragraph
- **Before**: no terminal phase; phase `closed` refused all but T10.
- **After**: phase `terminal`; `begin`, `answer`, `find`, `verify` refuse `E-TERMINAL`; `status` reports post-terminal edits; coordinator runs `status` before each dispatch. Executor note 6: Change 29 calls `defer` "the one write allowed in the terminal phase", but the sweep also writes after a terminal decision; the text says "the only writes are the single sweep and `defer`", which keeps both changes true.
- **Provenance tag**: `Orchestrator decision D6 and invariant probe INV-004, merged per Change #14`
- **Validation**: no `closed` phase remains; all phase words are `find`, `revise`, `verify`, `terminal`.

### Change 15: Counters advance only on a committed `begin`
- **Status**: Applied
- **Source**: INV-018; INV-025 in part
- **Target**: s2 item 7 (Counting)
- **Before**: counter "incremented only by `open`".
- **After**: review counter on committed `begin`; fix-cycle counter only when a claimed hunk was admitted; zero-hunk round `complete-empty`, "no edits admitted"; no new refusal.
- **Provenance tag**: s2 item 7 tag citing Change #15
- **Validation**: s4 pseudo-code `n` uses the same rule; test case in s6.

### Change 16: One atomic JSON state object
- **Status**: Applied
- **Source**: Variant A s3 Format and example
- **Target**: s3 Format and example
- **Before**: JSON Lines header plus row lines.
- **After**: one object with the 13 plan keys; example rebuilt on F10, F22, N12 shapes with renamed fields (`caused_by` list, `grade`, `rule`, `claims`, `mappings`, `history`), half-open coordinates.
- **Provenance tag**: `Variant A s3 Format and Integrity, merged per Change #16 and Change #30; ...` and the example tag
- **Validation**: example rows obey T1, T2, T7 (L1 verified with child L3, `caused_by: ["L1"]`); decisions show U = 1 at rounds 1 and 2, consistent with the rows.

### Change 17: `blocking` computed by profile; `sev` removed
- **Status**: Applied
- **Source**: Variant A s3 Computed fields and s6 `PROFILES`
- **Target**: s2 item 1; new s3 Computed fields; every `sev`; `init --profile`
- **Before**: reviewer-supplied `sev`; FR-8/FR-9 blocking with no field (X-016).
- **After**: profile predicate copied from `SP:259`; `rule=FR-8, grade=MINOR` blocking; `PROFILES` maps vocabulary, predicate, cap, guards.
- **Provenance tag**: `Variant A s3 Computed fields and s6 PROFILES seam, merged per Change #17 (fixes X-016)`
- **Validation**: the only remaining `sev=` is implement's own `sev=`/`origin=` vocabulary in s7 (`QA:141`), which is correct.

### Change 18: Replace the frozen-field list
- **Status**: Applied
- **Source**: Variant A s3; Variant C s3; C-R2 C-008 row
- **Target**: s3 Frozen paragraph
- **Before**: `id`, `sev`, `grade`, `anchor`, `wrong_outcome`, `found`, `origin`, `parent`; exit 5 `FROZEN_FIELD`.
- **After**: plan's 12 fields plus original finding text; `E-FROZEN` exit 2; relocation records separate.
- **Provenance tag**: s3 Frozen tag citing Change #18
- **Validation**: exit 2 matches the s6 exit-code list.

### Change 19: Five statuses; `disputed` is a claim flag
- **Status**: Applied
- **Source**: B-R2 X-017 resolution; C-R2 X-017 row
- **Target**: s3 T4 and T8 (now T5 and T11); Forbidden paragraph
- **Before**: `disputed` used as status (T8 "From disputed") and as flag.
- **After**: statuses `open`, `deferred`, `fixed`, `verified`, `reopened`; `claim.action=disputed`; ruling `dispute=accepted|rejected`; unruled dispute at the cap counts as open.
- **Provenance tag**: transition-table tag citing Change #19
- **Validation**: `disputed` appears only as an answer action or claim flag (4 hits checked).

### Change 20: Rewrite the transition table
- **Status**: Applied
- **Source**: Base T1 to T11; Variant A error codes; Variant C history-derived reopen; B-R2 C-005, C-022
- **Target**: s3 Status transitions table
- **Before**: T1 to T11 with a "Who may" column.
- **After**: T1 to T12 with "Requested by (subcommand)", phase and refusal code per row; history decides `open` versus `reopened`; T9 reset; `E-NOT-CHANGED`; lexical cross-check warning. Executor note 7: the base's T7 refusal had no code (exit 6); `E-INCOMPLETE` is used because the missing child is a missing part of the answer set. Renumbering: auto-claim is T4, disputes T11, `defer` T12.
- **Provenance tag**: `Base s3 T1 to T11 restructured per Change #20, with Variant A error codes ...`
- **Validation**: every T-number used in the spec (T1 to T12) is a table row; 37 references checked.

### Change 21: Remove `late` as a row kind
- **Status**: Applied
- **Source**: `base-selection.md`; Variant A s2; D5
- **Target**: s2 item 6, s3, s4, s9
- **Before**: `late` rows, `origin == late`, `Lt`.
- **After**: `round_found=sweep`, status `deferred`, location classes kept; sweep blocking count `S`.
- **Provenance tag**: cited in the s2 item 6, s3 table and s4 tags
- **Validation**: no `late` or `Lt` outside Source comments; the one remaining "found late" is the base's cause name in s10 ("Pre-existing defects found late"), plain English, not a row kind.

### Change 22: Anchor quote rules
- **Status**: Applied
- **Source**: Variant A s3 Anchor rules
- **Target**: s2 item 1; new s3 Anchor rules
- **Before**: "byte-present once".
- **After**: whitespace-normalized, exactly once, `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `--at`, candidate lines in the error. Executor note 8: the plan says "at least 12 characters" and, in its rationale, that short quotes only warn (C-042); the text says a quote "should be at least 12 characters; a shorter or generic quote is accepted with a warning", which states both.
- **Provenance tag**: `Variant A s3 Anchor rules, merged per Change #22; Base s11 risk 1 ...`
- **Validation**: s11 item 1 lists only absence and ambiguity as anchor stall paths, consistent.

### Change 23: Anchor relocation with `anchor_state`
- **Status**: Applied
- **Source**: Variant C s3
- **Target**: new s3 Anchor relocation
- **Before**: none.
- **After**: mapping records per `begin`, unchanged-block mapping then unique quote, rewritten-quote rule, `anchor_state=missing|ambiguous` cannot be verified and enters X, tombstone rule.
- **Provenance tag**: `Variant C s3 "Anchor relocation and edit ownership", merged per Change #23`
- **Validation**: T6 refuses rows with a failed anchor state; X counts them.

### Change 24: Half-open line ranges
- **Status**: Applied
- **Source**: INV-014; Variant C s6
- **Target**: new s3 Coordinates; example spans
- **Before**: inclusive `"r2:220-220"` style.
- **After**: `[start, end)` on a named snapshot, deletion overlap rule, relocation before overlap; example uses `r2:[118,121)` form.
- **Provenance tag**: s3 Coordinates tag citing Change #24
- **Validation**: no inclusive span remains; T9 points to Coordinates.

### Change 25: Diffs with old and new ranges and tombstones
- **Status**: Applied
- **Source**: Variant C s6 diff paragraph
- **Target**: s2 item 4; new s3 Diffs
- **Before**: whitespace-collapsed new-side hunks only.
- **After**: `diffs/c1.json` (review 2) and `diffs/c2.json` (review 3) with raw ranges, boundaries, digests; raw drives ownership, normalized drives scope and admission; autojunk off; no git.
- **Provenance tag**: s3 Diffs tag citing Change #25
- **Validation**: s6 `begin` row writes `diffs/c<k-1>.json`, consistent with c1 at review 2.

### Change 26: Claim width limit; `caused_by` list
- **Status**: Applied
- **Source**: INV-008; D1; C-R2 C-023 row
- **Target**: s3 under T3; frozen fields; s10 row 2 (via Change 61)
- **Before**: no claim limit; single `parent`.
- **After**: `E-CLAIM-WIDE` beyond the paragraph unit; `caused_by` lists every claiming row; location attribution only, analyst adjudicates M3.
- **Provenance tag**: `Invariant probe INV-008 and orchestrator decision D1, merged per Change #26 ...`
- **Validation**: T3 check column carries the same rule.

### Change 27: `answer fixed` must name an edit
- **Status**: Applied
- **Source**: INV-009; Base T3; Variant A `deleted: true`
- **Target**: s3 T3 check and a short paragraph
- **Before**: `new_text` found in `DOC` and inside a changed hunk.
- **After**: names a hunk that changes or deletes text inside the mapped span, else `E-FIXED-NO-EDIT`; `not-fixed` or `disputed` otherwise; auto-claimed rows satisfy it.
- **Provenance tag**: `Invariant probe INV-009, merged per Change #27; ...`
- **Validation**: code is distinct from `E-NOT-CHANGED`, as the plan's rejection table requires.

### Change 28: Reviser gap entries as `scope=outside` rows
- **Status**: Applied
- **Source**: INV-010 adapted to D4
- **Target**: s3 after T3; s6 `answer` input; s9
- **Before**: gaps lived only in disposition prose.
- **After**: optional `gap` entries, listed in the plan, filed as `origin=reviser-gap`, `scope=outside`, counted in `O` and M3.
- **Provenance tag**: `Invariant probe INV-010, adapted to orchestrator decision D4, merged per Change #28`
- **Validation**: T2 covers `origin=reviser-gap`; O definition names reviser-gap rows.

### Change 29: `defer` is a record only
- **Status**: Applied
- **Source**: Base T10; C-R2 X-017 row; B-R2 C-007
- **Target**: s3 T10 (now T12)
- **Before**: blocking open row to `deferred` by the coordinator.
- **After**: `user_deferred` history record; status, `loop_decision`, `delivery_outcome` and headline counts unchanged. See executor note 6 for the terminal-phase wording.
- **Provenance tag**: transition-table tag
- **Validation**: s11 item 5 updated to match (cannot be demoted; `defer` records words only).

### Change 30: Body hash on the new object
- **Status**: Applied
- **Source**: Variant A s3 Integrity
- **Target**: s3 Format
- **Before**: `LEDGER_TAMPERED` exit 3 over following lines.
- **After**: `E-TAMPERED` exit 3 over canonical JSON without the hash key; not a security boundary.
- **Provenance tag**: s3 Format tag
- **Validation**: s11 item 6 renamed to `E-TAMPERED`; reseal question kept (s12 question 3).

### Change 31: `loop_decision` and `delivery_outcome`
- **Status**: Applied
- **Source**: Variant C s4; D5
- **Target**: s4 pseudo-code and result table
- **Before**: one Result column; `final` from `Lt`.
- **After**: U restricted to `scope=in`; three loop decisions; S; delivery outcome set only by `sweep --input` or the skipped-sweep review-1 `close`; worked example renamed. Executor note 9: two clarifying sentences added: `S` reads `pending` in the `ledger-verdict:` line until the sweep has run, and `S` counts by `blocking` while `W` (s9) counts the same rows by grade, so the two numbers are not two definitions of one count.
- **Provenance tag**: `Variant C s4 (loop_decision, delivery_outcome, S, X, I), merged per Change #31 and Change #32; ...`
- **Validation**: result table has both columns; worked example ends with delivery ESCALATE.

### Change 32: Integrity and structural escalation term
- **Status**: Applied
- **Source**: Variant C s4 (`X_r`, `I`)
- **Target**: s4 pseudo-code before the U test
- **Before**: none.
- **After**: `if not I or X > 0: ESCALATE`, X and I defined as planned.
- **Provenance tag**: same tag as Change 31
- **Validation**: X count reported per replicate (s9 Scope metrics).

### Change 33: `close` accepts the reviewer's verdict and appends the tail
- **Status**: Applied
- **Source**: D3; INV-021 option 2; Variant A s2 step 4
- **Target**: s4 footer lines; s2 item 7 last sentence
- **Before**: script footer plus `verdict:` last line; reviewer verdict implicitly forbidden.
- **After**: reviewer writes what the brief asks; `close` appends `## Ledger`, Reviser brief (CONTINUE), `ledger-verdict:` line, script last line; analyst records disagreements.
- **Provenance tag**: `Orchestrator decision D3 and invariant probe INV-021 (option 2), merged per Change #33; ...`
- **Validation**: validity check 5 in s9; risk item 10 in s11.

### Change 34: Last-line strings
- **Status**: Applied
- **Source**: D3; INV-024; Variant C s4
- **Target**: s4 strings paragraph and Next column
- **Before**: `verdict: PASS` if PASS else `verdict: FAIL` at every close.
- **After**: CONTINUE `verdict: FAIL`; pre-sweep terminal `loop: PASS|ESCALATE (sweep pending)`; sweep report `verdict: PASS|FAIL`; skipped-sweep review 1 `verdict: PASS`.
- **Provenance tag**: s4 strings tag citing Change #34
- **Validation**: result table "Last line" column uses exactly these strings.

### Change 35: Protect report tails at every later step
- **Status**: Applied
- **Source**: Variant A s4; D3; INV-011
- **Target**: s4 after the strings
- **Before**: none.
- **After**: tail digest; `begin` `E-REPORT-EDITED`; sweep (or skipped-sweep review-1 close) re-checks all prior tails; analyst `status`; idempotent regeneration.
- **Provenance tag**: `Variant A s4 (E-REPORT-EDITED), orchestrator decision D3 and invariant probe INV-011, merged per Change #35`
- **Validation**: s6 `close` row writes the digest; `sweep --input` row re-checks tails.

### Change 36: Cap with a tested constant
- **Status**: Applied
- **Source**: D7; Variant A s4; Variant C s4
- **Target**: s4 Cap paragraph
- **Before**: `close` never CONTINUE at 3; `open` exit 11.
- **After**: `CAP_REVIEWS = 3` tied to the text; refusals of fourth review, third cycle (`E-CAP`), second sweep (`E-SWEEP-DONE`), second `init` (`E-EXISTS`) or `find` (`E-PHASE`) even under a new op id; identical retry returns the committed result. Pinned strings verbatim. Executor note 10: the plan names no code for a second `find`; Variant A's `E-PHASE` is used.
- **Provenance tag**: s4 Cap tag citing Change #36
- **Validation**: both pinned strings present verbatim; s6 command pins check them.

### Change 37: Monotonicity is a profile guard
- **Status**: Applied
- **Source**: D7; Base s4; `RFQA:401`, `RFQA:407`
- **Target**: s4 last paragraph
- **Before**: "`close --monotonic`, default off".
- **After**: no halt in `spec-panel`; `PROFILES` ordered guards; rf-qa order regression, monotonicity, cap.
- **Provenance tag**: s4 "No second computed stop" tag
- **Validation**: s7 rf-qa row uses the same guard order; no `--monotonic` left.

### Change 38: Zero findings at review 1 is a valid PASS
- **Status**: Applied
- **Source**: INV-017
- **Target**: s4 result table; s6 `find` row
- **Before**: unstated.
- **After**: table row "zero findings" PASS, sweep skipped, `verdict: PASS`; `find` accepts an empty rows array; fixture in Tests.
- **Provenance tag**: s4 table tag citing Change #38
- **Validation**: test case "an empty `find`" present.

### Change 39: Update the s5 duty table
- **Status**: Applied
- **Source**: Base s5; Variant A s5; Changes 4, 7, 8, 12, 13, 33
- **Target**: s5 table
- **Before**: cells named `add`, `open`, `revise-check`, anchor-outside refusal, `close` exit 6; "Late findings" row.
- **After**: merged mechanism cells; "Sweep findings" row; new "Out-of-hunk findings" row. "What the ledger does NOT remove" kept unchanged.
- **Provenance tag**: s5 table tag citing Change #39
- **Validation**: no removed subcommand appears in the table.

### Change 40: Rewrite the command's loop bullets
- **Status**: Applied
- **Source**: D10; Base s6 outline; Variant A s6 Setup bullet
- **Target**: s6 outline Usage sentence and eight bullets
- **Before**: Mode, Phase, Find, Verify, Sweep, Cap, Reviser contract, Precedence with `--ledger` required, `add`, `open`.
- **After**: new Usage `[--ledger <dir>] [--revert-unclaimed] [--sweep]`, `--unattended` usage line dropped; bullets Setup, Find, Verify, Sweep, Report, Cap, Reviser contract, Precedence, one line each.
- **Provenance tag**: s6 outline tag citing Change #40
- **Validation**: eight numbered single-line bullets; the Cap bullet keeps both pinned strings by reference to the canonical sentence. Not checked: `BANNED_SEVERITY_PHRASES` (the list lives in the repo test file, which this merge did not open).

### Change 41: Refuse a standalone `--unattended`
- **Status**: Applied
- **Source**: D10; INV-026
- **Target**: s6 outline, one line before the bullets
- **Before**: `--unattended` silently ignored.
- **After**: "spec-panel-ledger has no unattended mode" printed and stop; not a heading.
- **Provenance tag**: s6 outline tag citing Change #41
- **Validation**: command pins assert the line exists.

### Change 42: Rewrite the CLI table and exit codes
- **Status**: Applied
- **Source**: D9; Variant A s6 CLI table; Variant C s6
- **Target**: s6 Script CLI
- **Before**: role column; `close` exits 0, 10, 11, 6, 4; `add` 4, 6; `revise-check` 7.
- **After**: 12 rows (11 subcommands, `sweep` in two forms); columns subcommand, caller (inferred), inputs, writes, output, checks, exit; committed exit 0; refusals 1, 2, 3, 4; only `verdict` 0, 10, 11; read fresh `status`. Executor note 11: the plan gives exit numbers but no codes for a stale binding (exit 2), a lock conflict and a stale sequence (exit 4); no new codes were invented.
- **Provenance tag**: s6 CLI tag citing Change #42
- **Validation**: all 16 error codes used in the spec appear in the s6 exit-code list; no `close` exit 10 or 11 remains (s11 item 8 now names `verdict` exit 11).

### Change 43: JSON stdout and input binding
- **Status**: Applied
- **Source**: Variant C s6
- **Target**: s6 under the CLI table
- **Before**: `{"ok":true,...}` or `{"error":...}`.
- **After**: success and error objects as planned; `round`, `document_sha256`, `ledger_seq` binding; stale refused.
- **Provenance tag**: `Variant C s6 stdout object and actor input envelope, merged per Change #43`
- **Validation**: s8 recommendation points to this subsection.

### Change 44: Transaction, crash and rerun
- **Status**: Applied
- **Source**: D8; Variant C s6 (reduced); INV-005
- **Target**: new s6 subsection; s7 concurrent-writer sentence removed
- **Before**: temp file plus `os.replace`; no lock in v1.
- **After**: nonblocking `fcntl.flock` on `L/.lock`, temp plus fsync plus `os.replace`, `--op`, `--expect-seq`, digest idempotency with `replayed: true`, no replay, hard links or directory sync, reviser crash handled at next `begin`. Executor note 12: `fcntl` added to the script's stdlib module list in the New files table.
- **Provenance tag**: s6 Transaction tag citing Change #44 and Change #45
- **Validation**: s7 opening paragraph says the lock handles concurrent writers; s12 closes base question 3 in part.

### Change 45: `init --archive-existing`
- **Status**: Applied
- **Source**: D8; INV-001
- **Target**: s6 `init` row and Transaction subsection
- **Before**: `init` exit 2 if the ledger exists.
- **After**: rename to `<stem>.review-ledger.aborted-<UTC timestamp>/`, recorded in the new state object; required by the protocol.
- **Provenance tag**: same tag as Change 44
- **Validation**: s9 arm (4) and failure (6) use it.

### Change 46: One Tests subsection
- **Status**: Applied
- **Source**: Variant A s6 Tests; Variant C fixtures; Base pins and drift test
- **Target**: s6 "Tests, beyond the script suite"
- **Before**: base pins plus a separate "Checks the script owns" line.
- **After**: Script cases (planned list), Command pins (planned list, subcommand and flag names spelled out), Drift test kept. Post-merge fix: the base's "(`DES` T9 style)" was reworded to say it means test T9 of the 427 design (external), not transition T9 of this spec.
- **Provenance tag**: s6 Tests tag citing Change #46
- **Validation**: every refusal code in the CLI list has a test case or is covered by "every refusal code".

### Change 47: Update the new-files table
- **Status**: Applied
- **Source**: D10; Variant C s6 fixtures; Base s6
- **Target**: s6 New files
- **Before**: six rows.
- **After**: fixtures row added; `SKILL.md` row lists layout, schemas, `PROFILES`, CLI, how to add a profile; Edited files paragraph and naming trap kept.
- **Provenance tag**: s6 New files tag citing Change #47
- **Validation**: skill name `sc-review-ledger` everywhere.

### Change 48: Experiment-install paragraph
- **Status**: Applied
- **Source**: D1; D5; Base s6
- **Target**: s6 Experiment install
- **Before**: "the briefs get the one-line name change and `--ledger <path>`".
- **After**: three review briefs only, `/sc:spec-panel-ledger --ledger <path> --revert-unclaimed`; reviser briefs verbatim; sweep route in s9.
- **Provenance tag**: s6 Experiment install tag citing Change #48
- **Validation**: matches s9 arm (1).

### Change 49: Adoption through `PROFILES`
- **Status**: Applied
- **Source**: Variant A s6, s7; C-R2 C-031, C-032, C-033
- **Target**: s7 title, opening paragraph, table
- **Before**: `--scale` vocabulary, concurrent-writer limit, `close --monotonic`, `mark`.
- **After**: heading names `/sc:reflect`, rf-qa, `/sc:implement` final review; one `PROFILES` row plus adapter section; reflect rows after the evidence-validator gate, "ledger PASS cannot authorize promotion"; rf-qa ordered guards and dedup identity (`RFQA:414`); implement not adopted, fresh full FINAL kept. Adoption order kept.
- **Provenance tag**: s7 tags citing Change #49
- **Validation**: heading is the required section 7 "Adoption" heading.

### Change 50: Resumed output must carry the current binding
- **Status**: Applied
- **Source**: C-R2 C-034; B-R2 C-034
- **Target**: s8 recommendation
- **Before**: recommendation without the binding rule.
- **After**: one sentence appended. Consequential edits in the same section: `hist` renamed `history`; the cost cell now reads "about 15 to 20 script calls per loop and up to one extra session" (Change 62); "severity" in the state list reads "grade" (Change 17).
- **Provenance tag**: s8 tags citing Change #50 and Change #62
- **Validation**: s8 cost cell agrees with s11.

### Change 51: Redefine the "led" arm
- **Status**: Applied
- **Source**: D1; D5; Base s9; B-R2 New evidence 1
- **Target**: s9 Arm paragraph
- **Before**: brief appends `--ledger .../ledger.jsonl`; one added sweep dispatch.
- **After**: five recorded changes as planned; smoke check; heartbeat citation `T09-R3-reviewer-L11-1c9a7ec8.md:31` as quoted in B-R2; sixth-dispatch brief line kept from the base, now reviewing only the `sweep --prepare` copy.
- **Provenance tag**: s9 arm tag citing Change #51
- **Validation**: s11 sessions bullet gives 5 or 6, consistent.

### Change 52: Replace P3 and P3s with the headline
- **Status**: Applied
- **Source**: D11; INV-015; X-011 rows; Variant C s9
- **Target**: s9 Metrics
- **Before**: P3 and P3s bullets.
- **After**: headline `|U3 union W union O|` with U3, W, O, blinded duplicate ruling with raw and auto-matched bounds, early-run carry rule; P3 kept as U3 (secondary); H kept, now over U3. One clarifying sentence added: the union counts a row once whichever sets it falls in (U3 includes deferred `scope=outside` rows, which are also in O).
- **Provenance tag**: s9 Metrics tag citing Change #52
- **Validation**: P3 and P3s appear only as "the base's P3/P3s" explanations.

### Change 53: Deferred floor and the control's comparable floor
- **Status**: Applied
- **Source**: INV-013; D11
- **Target**: s9 after the headline
- **After**: deferred CRITICAL or MAJOR count published, with/without decision pre-registered, control figure computed by the same rubric.
- **Before**: none.
- **Provenance tag**: s9 Metrics tag citing Change #53
- **Validation**: s12 question 9 lists the reading of the control reports among the blinded steps.

### Change 54: Pre-register B1, r1 and r2
- **Status**: Applied
- **Source**: INV-027; A-012 row
- **Target**: s9 paragraph before the Bar; s10 falsifying condition
- **Before**: none.
- **After**: "Pre-registered quantities" paragraph; s1 bullet (Change 1) and s9 failure (7) carry the falsifying condition. Executor note 13: the s10 convergence paragraph was kept unchanged (preserved base strength 5); the falsifying condition is stated in s1 and s9, which s10 already points to through its section 9 reference.
- **Provenance tag**: `Invariant probe INV-027 and the A-012 row, merged per Change #54`
- **Validation**: numbers 13, 0.46, 0.17, 2.7, 39 match the probe text.

### Change 55: Baseline sweeps first, with the decision rule
- **Status**: Applied
- **Source**: INV-028; D11; Base s9
- **Target**: s9 Baseline sweep paragraph
- **Before**: baseline sweeps, no ordering, no rule.
- **After**: run before any replicate with the same procedure; mean 3 or more triggers the advance declaration; comparison kept via failure (2).
- **Provenance tag**: s9 Baseline tag citing Change #55
- **Validation**: s11 counts the six baseline sessions.

### Change 56: Arm B as the second comparator
- **Status**: Applied
- **Source**: D11; INV-029; Base s9 Bar
- **Target**: s9 Bar
- **Before**: one bar against control plus a trailing Arm B sentence.
- **After**: claim (a) against control, claim (b) against Arm B, isolation reason stated.
- **Provenance tag**: s9 Bar tag citing Change #56
- **Validation**: failure (1) uses both comparators.

### Change 57: Mandatory validity checks
- **Status**: Applied
- **Source**: D11; Variant A s9 V1-ledger; INV-023, INV-006, INV-002, INV-011
- **Target**: s9 before Metrics
- **Before**: none.
- **After**: seven numbered checks as planned.
- **Provenance tag**: s9 Validity tag citing Change #57
- **Validation**: each check points to the section that produces its data.

### Change 58: Discarded and deferred bytes beside growth
- **Status**: Applied
- **Source**: INV-030; A-008 row; Base s9
- **Target**: s9 Growth and Scope metrics bullets
- **Before**: growth of `DOC` after revise 2; `revise-check` exit-7 count.
- **After**: growth on the accepted snapshot after revise 2, three byte figures beside it, "not attributable" rule; scope metrics split by admission path, plus revert, `E-CLAIM-WIDE`, `scope=outside` and X counts.
- **Provenance tag**: s9 Metrics tag citing Change #58
- **Validation**: failure (5) says "after the discarded bytes are shown".

### Change 59: Re-base the predictions
- **Status**: Applied
- **Source**: Base s9 Predictions; A-012; D1
- **Target**: s9 Predictions
- **Before**: P3 column; flg-r2 row "F22 stays deferred ... N5 and N12 never exist".
- **After**: planning-aid label; recompute from measured B1; flg-r2 row conditioned on the AC-0.4 paragraph check on `HIST/spec-v2-after-round1.md`; P3s 5.5 is a lower estimate for the headline. The withdrawn forecasts (A's 2.5, C's 1.5) are named in a short paragraph, as the task requires, from the plan's "Changes NOT Being Made" rows.
- **Provenance tag**: s9 Predictions tag citing Change #59, and a separate tag for the withdrawn-forecast paragraph
- **Validation**: the three trace rows and four forecast bullets are present.

### Change 60: Rewrite the failure criteria
- **Status**: Applied
- **Source**: Base s9 failure list; D11; Changes 52 to 58
- **Target**: s9 failure list
- **Before**: five items on P3 and exit-7 gating.
- **After**: seven items as planned; "not significant" sentence kept with D6 meaning the decision in `DEC`.
- **Provenance tag**: s9 failure tag citing Change #60
- **Validation**: item (6) says the replicate "is then not treatment, not a failure of the idea", which is the plan's wording inside a failure list; carried as planned, not a new contradiction.

### Change 61: Update the causes table and the hiding argument
- **Status**: Applied
- **Source**: Base s10; D1; D2; D4; INV-008
- **Target**: s10 rows 2 and 6, items 1 and 5
- **Before**: "hunks no blocking row claims are listed and revertible"; item 5 had no counter.
- **After**: rows and items as planned. Consequential renames in the same section: row 4 freezes `grade`, `rule`, `blocking` (no `sev`); row 5 names `E-CAP` and `E-TERMINAL`; item 2 says the N15-type finding becomes a non-blocking `scope=outside` row; "mark resolved=yes" became "a `resolved` result"; P3 read as U3.
- **Provenance tag**: s10 tags citing Change #61
- **Validation**: the B1 x r x r paragraph kept verbatim except "visible `bytes_added`", now "visible bytes per claim".

### Change 62: Recount sessions, heartbeats and script calls
- **Status**: Applied
- **Source**: D5; B-R2 New evidence 1; Base s11
- **Target**: s11 Costs sessions and script-call bullets
- **Before**: 6 sessions; 20 to 31 calls.
- **After**: 5 or 6 sessions plus smoke check and baseline sweeps; heartbeat cost; per-step counts as planned. The per-step counts sum to 13 to 17, while the plan states "about 15 to 20"; the text gives both: "13 to 17 per loop from the steps alone and about 15 to 20 with retries and the coordinator's `status` checks". Wall-time and token bullets kept with `render` and JSONL renamed.
- **Provenance tag**: s11 Costs tag citing Change #62
- **Validation**: s8 cost cell matches.

### Change 63: Update the "ways the ledger could make the loop worse" list
- **Status**: Applied
- **Source**: Base s11 items 1 to 8; D1; D2; D6; INV-007; INV-019
- **Target**: s11 numbered list
- **Before**: 8 items naming `revise-check`, `open` exit 11, T10, `LEDGER_TAMPERED`.
- **After**: items 1, 7, 8 modified as planned; items 9 and 10 appended; items 5 and 6 renamed (T12, `E-TAMPERED`, open question 3).
- **Provenance tag**: s11 list tag citing Change #63
- **Validation**: item 6 points to s12 question 3, which is `reseal --reason`.

### Change 64: Rewrite the MECHANICAL and PROSE table
- **Status**: Applied
- **Source**: Base s11 table; S-012 rows
- **Target**: s11 table
- **Before**: 17 rows naming `--as`, `revise-check`, `mark`, `late`.
- **After**: 23 rows; changed classifications as planned (identity PROSE; sweep independence split; verdict line split; auto-claim and revert MECHANICAL with residual); new rows for auto-claim, `--revert-unclaimed`, `scope=outside`, terminal phase, report tail, request-digest idempotency.
- **Provenance tag**: s11 table tag citing Change #64
- **Validation**: T-range in the table reads T1 to T12.

### Change 65: Close, add and narrow open questions
- **Status**: Applied
- **Source**: Base s12; D1; D2; D5; D8; probe brief readings
- **Target**: s12
- **Before**: 10 items.
- **After**: 10 open items (kept base 1, 3 narrowed to several files, 4, 5, 7, 8 with the paragraph calibration; added smoke check, `E-CLAIM-WIDE` and auto-claim frequency, blinded-ruling staffing; narrowed UNVERIFIED list) plus a "Closed by this merge" paragraph for base 2, 3 in part, 6, 9. Base question 1 reworded from "PASS at review 1 or 2" to "PASS with fix cycles left", because a review-1 PASS on an unchanged document now skips the sweep.
- **Provenance tag**: s12 tags citing Change #65
- **Validation**: s11 item 6 and s12 cross-references resolve.

## Post-Merge Validation

### Structural Integrity
- **Heading hierarchy**: PASS. One H1 (title) and 12 H2 sections; no H3 or deeper; no level gaps. Subsections use bold run-in labels, as the base does.
- **Section ordering**: PASS. Sections 1 to 12 appear in the base order with the required titles (section 7 title now names `/sc:reflect`, rf-qa and the `/sc:implement` final review, per Change 49).
- **Flow**: PASS. Each section reads in the order mechanism, rules, exceptions; forward references (s1 to s9, s2 to s3/s4/s9) point to text that exists. No stub text remains (grep `STUB-` = 0). No em dashes or en dashes (grep = 0).
- **Provenance**: 76 `<!-- Source: ... -->` tags; every section and significant block is tagged; the header states that Change numbers, INV ids and orchestrator decision ids in tags are external.

### Internal References
- **Total checked**: about 222: section and subsection references (80, including 10 "section 2, item N"), transition numbers T1 to T12 (37), error codes (93 occurrences of 16 codes), open-question numbers (2), DEC decision numbers outside comments (9), and brief-file citations (12, T05, T06, T09).
- **Resolved**: all section, subsection, item and question references resolve to existing text; all 16 error codes are defined in the s6 exit-code list; every T-number is a row of the s3 table; D5, D6, D9, D10, D11 are marked external (decisions in `DEC`) in the alias paragraph; INV ids appear only inside Source comments, which the header marks external.
- **Broken**: 0 unmarked. Two references carried from the base have no definition anywhere in the sources: the alias `SPEC` (s10, `SPEC:245`, `SPEC:207,210`, `SPEC:224,238`) and the label `C-R3-10` (s3 Location). They are now explicitly marked "UNVERIFIED, external" in the alias paragraph; no definition was invented. One ambiguous reference fixed: "(`DES` T9 style)" in the s6 pins now says it means test T9 of the 427 design, not transition T9.

### Contradiction Re-Scan
- **New contradictions introduced**: 0.
- **Checks run**:
  - Exit-code rules: one rule only (s6): committed 0; 1, 2, 3, 4 for refusals; `verdict` alone 0, 10, 11. Mentions in s3 (`E-TAMPERED` exit 3, `E-FROZEN` exit 2) and s11 item 8 (`verdict` exit 11) agree. No `close` exit 10 or 11 survives.
  - Sweep sessions: one sweep per loop everywhere (s2 item 6, s2 table, s4 cap paragraph "one extra fresh context", s6 `E-SWEEP-DONE`, s9 arm (3), s11 "5 if the smoke check passes, else 6").
  - R3 count definitions: `U` (s4, loop, blocking, `scope=in`), `U3` (s9, by grade, after review 3), headline `|U3 union W union O|`, `S` (s4, sweep, by blocking) and `W` (s9, sweep, by grade). The s4 text states that S and W count the same rows by different keys; no two definitions share a name.
  - Statuses: every status used (`open`, `deferred`, `fixed`, `verified`, `reopened`) is a table status; `disputed` is used only as an answer action or claim flag; verify results (`resolved`, `open`, `regressed`, `cannot-verify`) and `complete-empty` are results, not statuses. Phases used: `find`, `revise`, `verify`, `terminal` only; the base's `closed` phase is gone.
  - Terminal writes: "the only writes are the single sweep and `defer`" (s2 item 8) reconciles Change 14 with Change 29.
- **Underspecified, flagged for the orchestrator (not contradictions)**:
  1. `verdict` maps PASS, CONTINUE, ESCALATE to 0, 10, 11, and its JSON carries both `loop_decision` and `delivery_outcome`, but the plan does not say which decision the exit code reflects before the sweep. If it reflects `loop_decision`, a pre-sweep loop PASS exits 0, which is the hollow-PASS risk Change 34 guards against in the report text.
  2. Change 60 item (6) sits in the failure list but says the replicate is "not a failure of the idea". Carried as planned.
- **Not checked**: that the eight command bullets avoid `BANNED_SEVERITY_PHRASES` (`tests/skills/test_review_severity_rule.py:112-117` was not opened); the invariant probe was not re-run on the merged spec, which `refactor-plan.md` "Review Status" asks for before the run is treated as complete.

## Summary

- **Planned**: 65
- **Applied**: 65
- **Failed**: 0
- **Skipped**: 0
- **Executor notes**: 13 (listed in the change entries: notes 1 to 13), each a clarification that keeps two planned changes consistent or fills a value the plan left unnamed (sweep `--report`, `scope=outside` rows stored `deferred`, `E-INCOMPLETE` for T7, `E-PHASE` for a second `find`, the 12-character warning wording, the 13 to 17 versus 15 to 20 call count, `S=pending`); none reverses a plan decision.
- **Post-merge validation**: PASS (structure PASS; references PASS with 2 base-inherited undefined aliases marked external; 0 new contradictions; 2 underspecified items flagged above; invariant-probe re-run still pending).
