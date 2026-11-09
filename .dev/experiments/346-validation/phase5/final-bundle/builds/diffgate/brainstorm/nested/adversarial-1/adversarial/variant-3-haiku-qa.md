# Diffgate proposal: checked review surfaces

## 1. Problem and evidence

**Decision.** Ship an additive critique-mode command, `/sc:spec-panel-diffgate`, that accepts findings only through a checked, round-specific surface. Also check the reviser's edits against blocking finding footprints. Do not change the existing command, increase the review cap, suppress genuine changed-line blockers, or claim a scoped PASS certifies the whole document.

Evidence read for this proposal includes the seed brief and enrichment, both experiment reports in `exp346-p1-logs`, all three `spec-panel*.md` reports and both dispositions in `exp346-ab-flg-r2`, the current command's Review Loop and Unattended sections, its design document, and the implement QA rubric. The experimental reports describe a single scenario with two replicates per arm, not a general causal estimate.

| Measured problem | Evidence | What this variant removes or leaves |
|---|---|---|
| Fix-induced defects on changed lines | A/B treatment reports label 89% of new R2 findings and 100% of new R3 findings `origin=changed`. Best Arm B run resolves every prior blocker in R2 and R3 but creates N12 while fixing N5. | Leaves these defects in scope. Reduces their creation by rejecting unrelated and minor-driven edits. Cannot eliminate faulty fixes. |
| Severity drift | Best-run N5 and N12 have explicit disagreements over whether false or incomplete test evidence is blocking. | Freezes the grade of a continuing finding and prevents reopening an unchanged resolved finding. New changed-line severity still needs judgment. |
| Revisers fixing notes and adding mechanisms | First disposition applies 21 of 22 findings, including eight non-blocking ones. Second applies all 15 rows, including five minors and four citation notes. | An edit must map to exactly one open blocking id and its approved footprint. A minor id cannot authorize edits. Semantic misuse of a valid id remains possible. |
| No mechanical loop stop or scope check | Current design calls its rules prose only. Arm B reviewers calculate their own diff and assign their own origin tags. | Script owns snapshots, round transitions, anchor membership, edit authorization and final verdict arithmetic. A coordinator can still bypass the tool entirely, which invalidates the experiment rather than producing an accepted run. |

Controls have R3 critical+major proxy mean 6.0 and growth mean 63.5%. Plain 427 reduces growth to 29.7% but leaves R3 proxy 5.5. Arm B with flags has proxy 3.5 and growth 30.0%; neither arm passes its pre-registered convergence bar. The best run's N12 is a real changed-line test-surface defect, not evidence that stricter scope alone would have passed that run.

**Non-goals.** No automatic repair, new reviewer ensemble, generic workflow engine, new dependency, implementation of the target specification, or adoption by other review commands in this change. This document specifies new interfaces; names explicitly marked PROPOSED below do not exist yet. Existing names are grounded in the inspected files. No implementation or live experiment was run while authoring it.

## 2. Mechanism and loop ownership

Let `D` be the absolute path of the specification and `G` be a new caller-chosen state directory. All filenames under `G` in this proposal are PROPOSED runtime artifacts. Reviewers never edit `D`, snapshots, surfaces, accepted reports or the ledger. The reviser may edit only `D` after explicit authorization. The coordinator owns transitions and runs the helper. The reviewer command must refuse to review without a prepared surface.

| Order | Owner and action | Reads | Writes |
|---|---|---|---|
| 1. Before review 1 | Coordinator runs `init`, then `surface`. The helper saves exact input bytes and pins the document path and run id. | `D` | `G/ledger.json`, `G/r1/baseline.md`, `G/r1/surface.json`, `G/r1/surface.md` |
| 2. Review 1 | Reviewer command runs the copied panel over the full saved document. Full review is allowed only here. It proposes findings, grades, wrong outcomes and exact repair footprints. | R1 surface, saved document, read-only source context | `G/r1/draft-1.json` |
| 3. Accept review 1 | Coordinator Reads finding quotes and repair footprints back, records confirmations, and runs `check`. Helper checks anchors, derives grades and verdict, and accepts once. On PASS go to end. | Snapshot, surface, draft, `G/r1/confirmation-1.json` | `G/r1/check-1.json`, `G/r1/accepted.json`, `G/r1/report.md`, updated ledger |
| 4. Fix cycle 1 | Coordinator gives only accepted blocking ids and footprints to reviser. Reviser makes the smallest correction after consent and declares every changed edit-group's owner. Coordinator runs `check-fix`. | R1 report, baseline, authorized footprints, `D`, `G/fix1/map.json` | Reviser writes `D` and map; helper writes `G/fix1/check.json`, then on success `G/r2/baseline.md` and ledger |
| 5. Review 2 | Coordinator runs `surface` against R1's saved document and R2's snapshot. Reviewer sees that computed delta and prior blocker records, with full documents available only as read-only context. Command writes a draft; coordinator confirms and runs `check` as at R1. | `G/r2/surface.json`, `surface.md`, R1 blocker records, read-only context | `G/r2/draft-1.json`, `confirmation-1.json`, `check-1.json`, `accepted.json`, `report.md`, ledger |
| 6. Fix cycle 2 | If R2 FAIL, coordinator authorizes only R2's open blockers. Reviser edits and maps edits. Helper checks against R2's snapshot and footprints. On PASS skip this cycle. | R2 report and authorizations, `D`, `G/fix2/map.json` | `D`, map, `G/fix2/check.json`, then `G/r3/baseline.md` and ledger |
| 7. Review 3 | Helper computes only the R2-to-R3 delta. Reviewer proposes statuses and changed-line findings. Coordinator confirms; helper accepts and derives verdict. | R3 surface, prior blockers, read-only context | R3 draft, confirmation, check, accepted report, ledger |
| 8. End | Coordinator runs `finish`. Helper renders final summary with open blockers and one deferred appendix. No R3 Reviser brief and no third fix cycle. | Ledger, accepted records, rejection diagnostics, snapshots | `G/summary.md`, `G/deferred.md`, terminal ledger state |

Retain the literal cap: **at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings**. At R3 FAIL: **HALT and escalate to the user with the open blocking findings**. An earlier PASS ends the chain. Broken inputs or twice-invalid reviewer output end as `invalid`, never PASS. A bad fix map ends as `fix-rejected` without consuming another review; do not keep retrying edits automatically.

Every snapshot is the document actually reviewed in that round, despite the historical `--baseline` flag naming the previous reviewed copy. Thus R2 compares saved R1 against saved R2, never R1 against R3. The helper verifies `D` still hashes to the pending snapshot before accepting a review and before completing a fix. A concurrent edit invalidates the step. An empty effective delta still consumes R2 or R3; prior open blockers stay open, even if a reviewer claims they were resolved.

The command may invoke the checker itself for early feedback, but the coordinator must independently run it before accepting a report or dispatching a fix. A tool invocation and matching accepted-record hashes, not the reviewer's self-audit, are the evidence of enforcement. This is an acceptance gate, not a filesystem sandbox.

## 3. Script interface and file contracts

**PROPOSED implementation.** One Python standard-library script, `diffgate.py`, hosted by a new skill, `sc-spec-panel-diffgate-protocol`. Resolve the complete skill directory from `~/.claude/skills/sc-spec-panel-diffgate-protocol/` first, else `.claude/skills/sc-spec-panel-diffgate-protocol/`. Require both its `SKILL.md` and script; do not mix an installed skill with a project script. Expand `~` before invoking the interpreter. Run it with `uv run --no-project python "<resolved skill base>/scripts/diffgate.py" ...`. This is an existing invocation pattern; all subcommands and flags in the following table are new, PROPOSED interfaces.

| Subcommand and inputs | Output and transition |
|---|---|
| `init --state G --document D` | Exclusive new state directory; UTF-8, nonempty document required. Save R1 bytes; ledger state `ready`, next round 1. Never infer state from a markdown header alone. |
| `surface --state G` | From pinned snapshots and accepted ledger records, generate round-specific JSON authority and readable Markdown. Return their absolute paths and SHA-256 digests in stdout JSON. No round increment. Exact repeat returns the same bytes. |
| `check --state G --draft P --confirmation C [--baseline B --re-review R]` | Validate current pending round, draft and coordinator confirmations. Forward any predecessor flags from the command unchanged; if either is supplied require both and verify them against ledger-pinned predecessor files. Write numbered diagnostics. If valid, save accepted JSON and render report, then atomically advance ledger to PASS, fix-eligible FAIL, or capped FAIL. Idempotent for identical accepted inputs only. |
| `check-fix --state G --map M` | Compare last accepted snapshot with `D`; validate complete ownership of actual edits. On success save the next reviewed snapshot, map digest and byte sizes, then advance to ready for the next round. No automatic edit or revert. |
| `finish --state G` | Require PASS, capped FAIL or explicit invalid/fix-rejected stop. Render summary and deferred appendix; mark terminal. Repeated calls return the existing summary, without re-notifying the user. |

Exit codes: `0` operation accepted, including a valid review verdict FAIL; `2` invalid arguments, encoding, schema or unreadable input; `3` rejected report or fix authorization; `4` stale hashes, wrong state transition, exhausted report retry, or attempt beyond the cap; `5` I/O or persistence failure. Stdout is one JSON object with `schema_version`, `operation`, `status`, `round`, `paths` and diagnostic code; stderr is explanatory text. Verdict and execution success are separate fields. Never interpret exit 0 alone as review PASS.

### Surface definition

Use `difflib.SequenceMatcher(autojunk=False)` over lines to derive edit opcodes and a unified diff with three context lines. The JSON contains raw baseline/current SHA-256, run id, round, document path, diff policy version, prior accepted-record digest, unified diff, hunk records, and prior blocking finding records. The readable surface carries the same ids, changed lines, deletion records and prior table. JSON is authoritative; the checker recomputes it from saved bytes rather than trusting editable JSON.

Each hunk id is `r<round>-<ordinal>-<digest>`, where digest is SHA-256 over the round, both document hashes, opcode coordinates and exact old/new text. Use the full digest in JSON, a shortened display only in Markdown. A later round never accepts an earlier hunk id, even when text is identical. A hunk records its old and new ranges, additions, removals, unchanged context and exact line text. Only added/replaced current lines and deleted old lines are eligible anchors. Context lines do not become eligible merely by sharing a hunk.

Keep physical line numbering, final-newline state and raw bytes. For the effective eligibility mask, ignore an aligned replacement pair when its line text differs only in ASCII spaces/tabs, retaining all non-whitespace characters in order. Do not remove newline boundaries or normalize Unicode. Raw whitespace edits remain in the diff and fix map, but do not open new blocking scope. This intentionally preserves 427's whitespace-only exclusion, with its semantic risk recorded in section 10. A reflow or move across physical lines is a real delta; no heuristic move detection or paragraph parser in version 1.

A deletion-only hunk has zero eligible current lines and explicit eligible old lines. Its anchor is `{side:"old", line:N, hunk:H, quote:"exact removed line"}`. It may support a finding that removal lost a required rule. It cannot assert that the removed text is still in the current document. Insertions at start/end have explicit boundary coordinates, including an empty old range.

### Reviewer draft and confirmation

`draft-<attempt>.json` is strict JSON, not YAML embedded in Markdown. Reject duplicate JSON keys and unknown control fields. It has `schema_version`, `run_id`, `round`, `surface_sha256`, `statuses`, `findings`, `deferred` and `analysis`. `analysis` holds the copied panel's scores, consensus and boundary tables, referencing finding ids rather than declaring a second verdict. All defects, including citation notes, must appear once in the findings or deferred array.

A new finding has an id `F<round>.<ordinal>`, `severity` from `CRITICAL|MAJOR|MINOR`, `rule` from `ordinary|FR-8|FR-9`, `wrong_outcome` (string or null), exact anchor objects, issue text, recommendation, optional `parent_id`, and a repair footprint. Footprints are saved-current line ranges or insertion boundaries, each with exact text or neighboring-line hashes. A deletion finding's repair footprint is a current insertion boundary, not a nonexistent current line. Coupled sites outside the primary line must be listed explicitly and confirmed before revision.

Prior findings get one status each: `{id, status:"resolved|open|regressed", evidence:[...], reason}`. No reissued finding id and no replacement wording for an old outcome. The surface includes all historically blocking ids with their last status; resolved ids are eligible for `regressed` only if a present delta intersects their saved footprint. Otherwise their status remains resolved. Continuing open findings may cite their prior id without a current hunk.

The coordinator writes `confirmation-<attempt>.json`, pinned to draft and surface digests, listing each finding's anchor Read-back result, confirmation of the claimed wrong outcome, and approval or rejection of each repair footprint. It cannot add findings, authorize a minor, or widen the surface. Presence of a confirmation is checkable; truth of its semantic judgment is not.

### Ledger and fix map

`ledger.json` is a versioned object with run id, canonical document path, state, round, snapshots and hashes, accepted report hashes, immutable finding identities/outcomes/grades, status history, repair footprints, fix-map hashes, byte counts, rejection attempts and deferred fingerprints. Use a short exclusive-create lock during each operation, compare ledger generation, write temp files under `G`, then atomic replacement. Refuse symlink state paths and output collisions. A crash before ledger replacement leaves only unreferenced artifacts; resume verifies every referenced digest and either completes the identical pending operation or stops, never silently resets.

`map.json` lists actual zero-context edit groups, each with old/new coordinates and exact content digests plus exactly one `finding_id`. The helper recomputes groups from the last reviewed snapshot and current bytes. Every group, including whitespace edits, must be covered once, owned by an open blocker, and fit its approved footprint. Adjacent edits merged into one group need one common authorized owner; mixed-owner groups are rejected rather than guessed. New insertion lines inherit the authorized insertion boundary. Notes, deferred ids, stale ids and unspecified coupled sites cannot own edits. The map also states byte size before and after; the script calculates and checks these values.

## 4. Checker and rejected reports

The checker proves that every accepted finding has a permitted, live, exact anchor. It does not prove the reviewer never thought about unchanged text or that its claim follows logically from its anchor. That distinction is a release constraint, not a footnote.

Validation order is closed and fail-closed:

1. Verify ledger generation, expected round, nonterminal state, document hashes, script schema version and recomputed surface digest. Check the optional `--baseline` and `--re-review` inputs against the actual pinned predecessor snapshot and accepted report, never against caller descriptions.
2. Parse strict draft JSON. Check required arrays, enum values, unique ids across the chain, and expected new-id prefix. A present but empty findings array is valid. A missing findings field, truncated JSON, duplicate key or hidden Markdown-only report is not.
3. Require exactly one status for every prior blocking id, including previously resolved ids. Reject extras, duplicates or omissions. Freeze each existing id's outcome and grade. For a resolved id to regress, require both an eligible current delta anchor and a coordinator confirmation that the original wrong outcome returned. A different defect is a new changed-line finding, not a recycled id.
4. For each new finding, require at least one eligible changed-line/deletion anchor; for continuation of a prior blocker, require its id and unchanged recorded outcome. Validate round-specific hunk membership, side, range and exact quote. A reference to unchanged context or to a hunk without a specific eligible line is insufficient. Validate every claimed surface anchor, not just the first good one.
5. Any new claim with neither eligible changed anchor nor permitted prior id must be placed in `deferred` as `deferred: pre-existing`, with `blocking:false`. If it appears in findings instead, record it in rejection diagnostics as a deferred candidate and reject the report. A stale hunk, wrong quote or nonexistent prior id is an integrity error, not proof of a pre-existing defect.
6. Check coordinator confirmations match this exact draft. Derive blocking from 427's rule: confirmed CRITICAL and FR-8/FR-9 are blocking; MINOR is never blocking; ordinary MAJOR requires a confirmed concrete wrong implementer outcome. A nonempty outcome string is necessary but not sufficient. Reject unconfirmed claims or footprints rather than silently accepting fabricated evidence.
7. Derive origin from validated anchors, not a reviewer tag. R1 is `first`; new eligible R2/R3 findings are `changed`; continued open ids retain their first origin; deferred findings are `unchanged`. For a new changed finding, derive its parent from the accepted fix-map group containing its primary anchor. A supplied contradictory parent id is rejected.
8. Generate the accepted JSON and Markdown report. Report first the prior-blocker status table, then new findings, notes, computed byte sizes and scope digest. Include `review: N of 3`; final line is exactly `verdict: PASS` or `verdict: FAIL`. FAIL means a confirmed blocker is open. Only these generated reports are authoritative. The reviewer writes no authoritative verdict.

A resolved claim requires exact current evidence in the prior finding's authorized footprint, with saved-to-current coordinate mapping from diff opcodes; deleted text may be supported by a checked absence record and the replacement/insertion boundary. Parent Read-back still checks whether that evidence actually fixes the stated outcome. No effective diff forces every previously open blocker to remain open, preserving the current command's empty-diff rule.

**One report repair, not another review.** On rejection, helper writes `check-1.json` and leaves the accepted finding set, round and document untouched. Coordinator asks the same reviewer once to repair only schema, anchor or deferred placement errors, using identical surface bytes; save `draft-2.json` and a matching confirmation. Do not invite new substantive findings during this repair. A second reject marks the run invalid and escalates with diagnostics and any accepted open blockers. No automatic third attempt, no fresh whole-document fallback, no silent dropping of a blocking claim, and no new fix cycle. Diagnostics and deferred candidates survive invalid termination.

The one-repair ceiling is script-enforced from ledger attempt count and draft digests. A coordinator inventing a new state directory would evade that history, so the experiment recorder must reject a run whose state root or run id changes mid-chain. This is the same trust boundary as a parent that can skip a test altogether.

## 5. Convergence and fix-induced defects

**Use a one-round delta lease plus checked edit ownership.** A substantive line written by fix cycle k is eligible for new findings in review k+1 only. If the next fix leaves it unchanged, it has no eligible anchor in the following review. If a later authorized fix changes it again, it receives a new lease. This follows from adjacent snapshot diffs, not an expanding cumulative diff against the original draft.

Open prior blockers remain reviewable by id until resolved or escalated. That exception permits checking the same original defect, not a fresh audit of all text cited in its rationale. An unchanged resolved finding cannot reopen. A reviewer cannot promote an unchanged minor to blocking by assigning it a fresh id; it has no eligible anchor. A continuing open MAJOR cannot acquire a stronger grade through renaming or a status row.

Every fix edit-group has one blocking owner and stays inside the already approved repair footprint. This closes the measured reviser escape that applied minor and citation notes because the brief said to apply confirmed findings. A minor-only correction outside a blocker footprint is rejected. A change inside a blocker's footprint still needs semantic Read-back: the helper cannot tell whether a large rewrite genuinely addresses that blocker. The coordinator must reject an inflated footprint before any edits, not justify it afterward.

New defects introduced by an authorized fix are **not capped to minor**. For example, the best run's F10 to N1 transition and N5 to N12 transition must both be accepted as new blockers when the changed-line evidence and wrong outcome are confirmed. Script-derived parent ids preserve those chains. An R2 child may authorize the second fix. Any R3 child stays open in capped FAIL. No third generation is repaired within this loop, and a new invocation cannot reset the round in the same ledger.

This guarantees finite execution and prevents unchanged text and note-driven edits from replenishing the surface. It does **not** guarantee a falling blocker count or a PASS by R3. The hard cap guarantees termination, not correctness or convergence. There is no severity ceiling, no arbitrary quota that hides an N12-class defect, and no monotonicity halt that could make a failed experiment look like an early success. The falsifiable claim is that narrower, blocking-only repairs produce fewer real defects, not that fewer defects are permitted to be reported.

## 6. Deferred pre-existing defects

A missed R1 defect on unchanged text goes into the deferred array, never into the re-review blocker set. Store its first-seen round, proposed severity, text, unchanged location and quote when available, and exclusion reason. The checker sets effective blocking to false regardless of claimed severity or FR rule. An unlocated observation is also non-blocking, with `location_unverified:true`; do not invent a source location.

Deduplicate exact repeats by document identity, quoted text and normalized issue text. Preserve all distinct claims and all first-seen records; semantic deduplication is not claimed. A previously deferred line that is later substantively changed by an authorized fix may support a new changed-line finding under a new id; link it to the deferred entry, but do not retroactively change the earlier verdict.

`finish` prints the deferred list once, at PASS, capped FAIL or invalid termination, with the heading `Deferred: pre-existing, not reviewed for acceptance in this loop`. Intermediate reports give only its count and path, not a new reviser assignment. The final summary explicitly states that PASS is scoped and deferred severity is the reviewer's unvalidated claim. No automatic remediation, ticket, new review or conversion into an Open Question follows.

A severe deferred defect remains visible to the user at the end. This design knowingly trades whole-document assurance for finite scoped re-review. It must not be adopted for a safety-critical acceptance gate that requires every discovered defect to block release. A user may separately authorize a new full review after the experiment, but that is a new decision and cannot be counted as convergence of this chain.

## 7. Comparison with PR 427

| 427 and flags | Diffgate addition |
|---|---|
| Coordinator passes saved copy and prior report; reviewer computes changed lines itself. | Helper saves byte-pinned copies and computes adjacent-round diff and eligible line mask before dispatch. |
| Reviewer self-reports `origin=changed|unchanged`; unchanged can block by quoting a dependency. | Checker derives origin. A dependency must anchor the actual changed line; quoting unchanged text alone cannot block. |
| Status table and report header are prose, potentially covering minor findings too. | Exact prior-blocker roster, unique immutable ids and closed status transitions are checked. Notes do not authorize repairs. |
| Report carries its own verdict and cap header. | Script derives verdict and count; ledger rejects stale state and additional reviews. |
| Reviser is asked to edit only text a blocking finding names. | Every actual edit-group must map to an approved open blocking footprint, including coupled sites. |
| Missing one re-review input can start a first review. | Variant critique requires its state root. Once initialized, missing or mismatched predecessor inputs stop the chain, never reset it. |

Keep 427's grade vocabulary, wrong-outcome test, minor-note policy, `resolved|open|regressed`, `review: N of 3`, `Reviser brief`, byte-size reporting, no Improve on re-review and the canonical cap. Preserve the rf-qa lookup order for its steps 1-5: project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; do not import its separate monotonicity wrapper.

Still prose or semantic judgment: whether an anchor proves the claimed wrong outcome; whether FR-8/FR-9 applies; whether a prior finding is truly resolved; whether an approved coupled-site change is necessary; whether prose discussion conceals an unregistered defect; and whether the coordinator actually invokes the helper. A parent Read-back reduces anchor laundering but cannot make these mathematical facts. The script proves membership, history and arithmetic only. A real regression caused by a changed rule can be anchored on that changed rule even when its consequence occurs in unchanged text; the reviewer must explain that dependency and the parent must confirm it.

The implement QA prior art separates reviewer claims from parent-derived grades, Reads anchors back and uses diff hunk headers to cap inherited text. It also permits late genuine blockers on task-owned text and performs a full audit on later reviews. Diffgate borrows parent ownership and structured evidence, not that broader late-blocker policy. The protocols are not equivalent and must not be silently substituted for each other.

## 8. Exact changes and installation

All additions in this table are **PROPOSED**, not existing paths. Source paths here are maintainer edit locations, not paths to embed in installed instructions. Existing inspected files are explicitly labeled existing.

| File | Exact change |
|---|---|
| `src/superclaude/commands/spec-panel-diffgate.md` (new) | Copy the current source `spec-panel.md`, not the historically drifting plugin copy. Change frontmatter name, title, examples and self-references to the variant name. Add PROPOSED `--diffgate-dir <dir>` to Usage, mandatory in critique mode. Add Activation invoking `Skill sc-spec-panel-diffgate-protocol` before critique analysis. Preserve existing expert methods and focus areas. Replace Review Loop authority as described below. |
| `src/superclaude/skills/sc-spec-panel-diffgate-protocol/SKILL.md` (new) | Skill metadata, dual-surface helper lookup, exact subcommands, state machine, strict draft schema, confirmation contract and coordinator/reviser instructions from sections 2-6. Include valid zero-finding and deletion-finding examples. No more files or abstractions in this initial skill. |
| `src/superclaude/skills/sc-spec-panel-diffgate-protocol/scripts/diffgate.py` (new) | Standard-library snapshot, diff, schema validation, edit-map checker, ledger transitions, report renderer and CLI. No imports from the package, no shell subprocess, network, Git mutation or target-document write. |
| `tests/skills/test_spec_panel_diffgate.py` (new) | Unit, negative, state-machine, subprocess, static command and isolated install tests in section 13. Fixtures are generated under pytest temporary directories; no external-worktree dependency. |
| `docs/designs/spec-panel-review-loop.md` (existing) | Append a clearly labeled additive variant annex, leaving the historical 427 design distinguishable. Document installed paths, experiment brief substitution, surface limits, terminal failures and deferred disclosure. Do not rewrite historical conclusions as implementation evidence. |
| `plugins/superclaude/commands/spec-panel-diffgate.md` (new) | Exact copy of the new variant source command. Leave the existing plugin `spec-panel.md` and its unrelated one-word drift untouched. |
| `plugins/superclaude/skills/sc-spec-panel-diffgate-protocol/SKILL.md` and `scripts/diffgate.py` (new) | Byte-identical mirrors of the new skill files. New tests pin parity and execute both script copies. |

Do not edit the existing `src/superclaude/commands/spec-panel.md`, its plugin mirror, user-level `spec-panel.md`, implement QA rubric, rf-qa agent, worker contract, severity rule, routing table or installer. The installer already discovers command Markdown files and installs protocol skills without stripping their `-protocol` suffix. Verify isolated installation of the new names in tests rather than changing shared installation code.

### Command text to add or replace

Add a critique-only mechanical precedence paragraph before the existing Review Loop. Its required new text is:

> Critique mode requires `--diffgate-dir <dir>` and a prepared, current surface from the diffgate helper. Review 1 may audit the full saved document. Later reviews may propose new findings only on eligible changed or deleted lines in that surface, plus status checks of its prior blocking ids. Context is read-only and cannot widen eligibility. Write the strict draft JSON, not an authoritative verdict. Only the helper-generated accepted report may authorize revision. An invalid or missing state stops this run; never fall back to a first review.

Adapt the seven bullets in place in the new copy:

1. Mode retains critique-only re-review. Require state and verify any supplied `--re-review` and `--baseline` paths against the ledger; replace the first-review fallback with refusal for partial/mismatched inputs in an existing chain.
2. Grading retains 427 literals, with coordinator confirmation and script-derived blocking.
3. Verdict names the generated report as owner, never the reviewer's draft.
4. Cap retains the canonical sentence and at-cap halt clause verbatim, one review per accepted round and no automatic reset. Re-review ignores `--iterations`, skips Improve and writes no revised specification.
5. Re-review output retains prior status table, `origin=changed|unchanged` as compatibility vocabulary, rf-qa lookup order, guard-table scoping and empty-diff behavior. Replace self-tagging with computed fields and mandatory eligible-line anchors. In ledger R1 origin is `first`; emitted R1 report needs no compatibility origin tag.
6. Reviser contract retains `Reviser brief`, blocking ids only and byte-size reporting. Add exact approved footprints and edit-map acceptance. Omit the brief at R3.
7. Precedence retains that a brief may narrow scope, never widen it or make minor findings blocking. State that an instruction to apply all confirmed findings cannot authorize minor edits.

In Behavioral Flow and Mandatory Output Artifacts, add the same critique-only precedence: R2/R3 tables and registries cover changed guards and prior blocker footprints, not an invitation to enumerate the whole document again. Full context may explain a changed guard but does not authorize unrelated findings. In `## Tool Coordination`, remove the copied repository-only example-template read: installed primitives must not tell a worker to read a package source file that does not ship to its project. Do not replace it with an invented installed example path. Other modes retain the original behavior and are outside the diffgate acceptance claim; re-review remains critique-only.

In the new Unattended section, keep standalone-token parsing, `--report-dir <dir>`, `--output` as a file, prohibited report directories, TDD gate, no outward writes and no target-spec modification. Add checker/state failures as execution failures and never publish an unchecked draft as `report_path`. On accepted review, `report_path` is the generated report copied to the requested `--output`, or the existing default `<report-dir>/spec-panel-report.md`. Those copies must hash-match. Artifact paths list actual non-ignored surface, accepted JSON and ledger outputs. A valid audit FAIL still means report execution succeeded; no accepted report means failed execution with diagnostics, not a fake verdict. If a report directory is known, preserve writing `return-contract.yaml` on every outcome.

### Script outline

Use `argparse`, `pathlib`, `hashlib`, `json`, `difflib`, `os` and `tempfile`. Dispatch the five subcommands to small operations. Common boundary validation reads immutable snapshots and ledger once, rejects invalid encodings, symlinks and stale generations, then constructs candidate outputs. Recompute opcodes once per operation and use the same coordinates for rendering and checking. A single derivation path computes grades and verdict. Render Markdown only from accepted structured records. Persist immutable per-round artifacts before atomically replacing the ledger; check hashes on resume. Unit-test pure diff and schema routines separately from file-state tests. No generic plugin system, persistent service, database or configuration layer.

### Install and experiment note

For a development implementation, run the repository's existing `make sync-dev` and `make verify-sync`; do not stage generated `.claude/` mirrors. For the experiment, install **only** the new command at `~/.claude/commands/sc/spec-panel-diffgate.md` and its complete new skill directory at `~/.claude/skills/sc-spec-panel-diffgate-protocol/`. Preserve the original user-level command byte-for-byte. Do not run a broad force reinstall during parallel experiments. Record hashes of both new installed primitives and the unchanged original before dispatch, and check them at every step. The project `.claude/` copies are fallback lookup surfaces, not proof that a worker loaded this variant.

The one-line brief substitution is:

```text
Replace /sc:spec-panel with /sc:spec-panel-diffgate and append --diffgate-dir <absolute state directory for this replicate>; keep every other original argument unchanged.
```

Record three additional coordinator step lines in each experimental brief: prepare the helper surface before review; accept only after coordinator confirmation plus `check`; accept a revision only after `check-fix`. These are the treatment, not uncontrolled brief improvements. A worker must invoke the variant command through the Skill tool so its command text and then its protocol skill are loaded; reading their files alone is not invocation. Verify that call order in the transcript. Restart/discover the newly installed name before starting measured runs; failure to resolve it is a setup failure, never permission to use the old command.

## 9. Measurement plan for S1

Pre-register two independent treatment replicates on the same S1 source, base, model, original briefs and 3-review/2-fix schedule used by the recorded comparison. Use only the command-name/state substitution and the three mechanical step lines specified above. Do not replace the original briefs with improved QA prose, change the model, expose the finished master answer, or apply notes to help the treatment. Record any unavoidable deviation. Existing controls are historical comparators; do not describe them as concurrent randomized controls.

| Metric | Historical control mean | Required bar | Point forecast for two replicates |
|---|---:|---:|---|
| Open CRITICAL+MAJOR proxy at R3 | 6.0 | Each replicate <=3, or scoped PASS earlier | 1 and 2, mean 1.5 |
| Spec byte growth after two fix cycles | 63.5% | Each replicate <=44.4% | 24% and 30%, mean 27% |

These are hypotheses, not calibrated estimates. The optimistic forecast depends on **reviser enforcement**, not on denying changed-line findings. In the best run the F22 non-blocking edit creates the more specific WC-1 evidence claim, later N5, then N12. A blocking-only map would refuse F22 as an edit owner. That removes one observed defect-generation route without suppressing N12 if an authorized fix really introduces it. Rejecting nine non-blocking R2 edit requests also narrows the second repair. It does not predict that the F10-to-N1 blocking chain disappears. Between-run spread is large, and a hunk-only gate without edit ownership would probably resemble Arm B rather than meet this forecast.

Compute growth from raw UTF-8 bytes: `100 * (final_bytes - initial_bytes) / initial_bytes`. Use the untouched 57,763-byte S1 draft if it matches the original brief's actual input. If a run passes early, carry its unchanged terminal document forward to the scheduled endpoint for the growth comparison; do not add an unnecessary fix. Record early PASS explicitly rather than pretending a third review occurred.

For comparability, the independent recorder retains the original severity proxy counting rule, not just script-derived blocking. At each round record total distinct findings, open critical+major proxy, effective blocking count, prior resolved/open/regressed counts, new changed-line findings, deferred counts by proposed severity, spec byte sizes, accepted edit groups, rejected reports/maps, state hashes, loaded-command hashes, tool calls, session count and elapsed time. Count each finding once, not once per expert or table. Keep raw drafts and rejected claims so a lower accepted count cannot conceal a reporting failure. Do not compare Arm B's proxy to treatment's narrower effective-blocking number.

A deferred CRITICAL/MAJOR is excluded from the scoped blocker metric but must appear in a second all-discovered critical+major count. Report both side by side. A gain caused only by moving unchanged findings into deferred does not support the claim of fewer fix-induced defects. Inspect the changed-line ancestry and rejected edit map to identify the actual route removed.

**Failure and validity rules fixed before running:**

- Either replicate has R3 proxy >3 without earlier PASS, or growth >44.4%: primary idea fails this S1 screen.
- Both thresholds pass but the reduction is entirely deferred relabeling, a genuine changed-line blocker is rejected, or an N12-class regression becomes invisible: quality claim fails.
- Missing checker invocation, wrong installed variant, changed run id, lost snapshot, answer exposure, unchecked accepted edits, or invalid termination: not a successful replicate. Report it as invalid with its cost; do not discard it and quietly replace it.
- Retain the original spread check as a separate strength-of-evidence test. Proxy reduction must exceed the larger within-arm spread, not merely equal it. Forecast reduction 4.5 exceeds the historical control spread 4 and forecast treatment spread 1. Growth reduction 36.5 percentage points exceeds the larger recorded control growth spread, 11.6 points, and forecast treatment spread 6. The older broader comparison reports a 13.2-point maximum across its arms, also below 36.5. If the observed effect does not exceed observed spread, report not proven even if the two primary bars pass.

Two replicates on one document screen only for a large effect. No adoption recommendation beyond an experimental variant follows from a pass. A broader safety review and other scenarios would be a separate decision.

## 10. Costs and risks

### Cost envelope

An uninterrupted three-review chain adds ten helper invocations: init, three surface computations, three report checks, two fix checks and finish. It keeps the original three reviewer sessions and two reviser sessions; coordinator confirmation is not a new model session. Add three confirmation-file writes, two edit-map writes and roughly one parent Read per distinct anchor, batched by file where possible. For 20 findings with multiple anchors, parent Read-back can cost more than the helper itself. Do not call this free or count only Python runtime.

Budget, UNVERIFIED until measured: under one second per helper invocation on S1-sized inputs, 1-3 minutes of coordinator validation per round, and 1-2 minutes to map each fix. That is about 5-13 added minutes per full loop, excluding review work saved by smaller surfaces. One rejected report can add one extra reviewer response and one extra check/confirmation per round, potentially 2-10 more minutes each; it need not add a session but can require resuming one. No automatic fix-map repair session. Storage includes three full document snapshots plus JSON, reports and diffs, expected below a few megabytes on S1; measure actual bytes.

### Failure modes and mitigations

| Risk | Guard and remaining cost |
|---|---|
| Missed cross-document regression | Read-only full context remains available; a finding must anchor the changed rule causing the effect. A reviewer can still miss the connection. Scoped PASS is not whole-document certification. |
| Real old critical defect is deferred | Required by the experiment, disclosed once at end with claimed severity. Unsuitable for release gates that cannot tolerate this exclusion. |
| Anchor laundering | Exact quote and membership checks reject fake anchors. Parent checks the causal link. A nearby legitimate quote can still be used to argue an unrelated defect if parent judgment is poor. |
| Broad repair footprint becomes a loophole | Footprints are approved before editing and retained with the finding. Mechanical containment is not minimality; parent must reject whole-document footprints without justification. |
| Arbitrary fix split or merged adjacent hunks | Zero-context edit groups and single-owner rule are deterministic. Adjacent legitimate fixes may fail the map and force manual replanning; do not silently assign multiple owners. |
| Paragraph move or hard reflow opens a large surface | No move detector. Treat moved/reflowed lines as changed, show eligible-line counts and footprint sizes. Discourage unrelated reflow; it is rejected if outside authorization. A justified structural repair can still expand review cost. |
| Whitespace carries meaning | Ignoring spaces/tabs can hide indentation defects, changed shell arguments or Markdown structure. Raw diff remains visible, but new whitespace-only defects cannot block under this policy. This is an explicit compatibility risk, and a quality veto if exercised on S1. A whitespace-sensitive policy is a separate experimental arm, not a post-hoc tuning change. |
| False resolution by disappearance | A removed rule is not necessarily fixed. Require replacement/absence evidence and parent outcome confirmation; a deletion anchor stays eligible for lost-requirement findings. |
| Previous blocker id used for a different complaint | Freeze outcome and grade; only status can change. Parent must distinguish a new defect from an old one. Exact duplicates can be caught; semantic duplicates remain a judgment risk. |
| Deferred flooding or repeated severe notes | Exact deduplication and single final disclosure prevent looping, not semantic repetition. Counts remain visible; a flood can overwhelm the user and invalidate usefulness even with a low blocker count. |
| Checker skipped or global install changes | Recorder demands tool evidence, matching hashes and one state root. No harness permission boundary forces a cooperative coordinator to obey. Wrong installation or reset means invalid experiment, not PASS. |
| Concurrent writes, partial output or stale baseline | Digest checks, generation lock and atomic ledger replacement stop acceptance. Lock contention or crashes can leave a stuck run; stop for explicit recovery rather than deleting a lock automatically. External mutation of all artifacts by a malicious owner is outside the trust model. |
| Path alias, symlink or output overwrites | Resolve absolute document identity; refuse symlink state paths, state under `.git/`, `.codegraph/` or distributable `.claude/` folders, and any output aliasing `D` or snapshots. The helper never changes `D`. Existing files require matching idempotent content, otherwise fail. |
| JSON/parser/tool complexity creates fresh failures | Strict schema, duplicate-key rejection, plain JSON authority and boundary tests. A malformed draft stops useful work; one repair balances recovery and loop cost. |
| Diff resource exhaustion | Version 1 accepts at most 2 MiB per document, 100,000 physical lines and 1,000 finding/status entries per draft; reject before diff with exit 2 and a named limit. Stdlib matching can still be slow on repetitive text. Test a bounded repetitive fixture; limits are not a formal CPU bound. |
| Report format breaks downstream users | This is a new command only. Render familiar tables and final verdict, but consumers expecting the old expert prose or YAML structure need explicit migration. Do not route existing callers automatically. |
| Lower counts without better specifications | Preserve raw proxy, effective blocking and deferred-severity counts separately. Never advertise a scoped PASS alone as convergence evidence. |

No new session transport, automatic rollback, speculative remediation ladder or severity quota is added. A rejected fix leaves the revised document on disk, clearly unaccepted, with its baseline intact. The coordinator must stop and ask for a decision; silently reverting user edits would destroy data and hide experiment cost.

## 11. Later adopters

- **`/sc:reflect`: possible opt-in repair re-review, not initial coverage/deviation audit.** It could consume the same snapshot and surface format after a corrective edit, provided its own severity and evidence-validation rules remain authoritative. A driving-spec clause is read-only context, not permission to reopen the whole result. Do not replace the first full audit with a delta check.
- **rf-qa agents: closest structural fit.** Existing Fix Cycle steps 1-5 already check prior blockers and fix-induced defects and leave minors as notes. A helper could enforce anchor membership there. Its regression and monotonicity guards remain stronger stop rules; adopting diffgate must not weaken or silently duplicate them. Need a separate contract for non-document artifacts and synthetic findings.
- **`/sc:implement` final review: do not replace it with this scoped gate.** The inspected rubric allows genuine late blockers on task-owned text and the managed FINAL reads all delivery files and plan acceptance criteria. That is deliberately broader than diffgate. A later adopter could use checked delta surfaces for a narrowly authorized repair after FINAL, while retaining a fresh full FINAL for archive acceptance. That integration needs its own tests and explicit product decision.

The new helper starts document-only. Generalizing to multi-file code diffs, Git trees, cross-file dependencies or multiple severity systems is deferred. Those extensions would add scope without helping the S1 experiment.

## 12. Open questions

These questions do not leave the initial interface undefined. Defaults above govern the first experiment; changing them creates a recorded new treatment.

1. **Is the parent confirmation worth its cost?** Default: required, in the coordinator's existing session. Measure Read-back time and disagreements. A future fully automated coordinator would need a trusted semantic confirmation policy; the checker alone cannot supply one.
2. **Should whitespace-sensitive specs use a different policy?** Default: preserve the stated whitespace-only exclusion and disclose its risk. Evidence of an indentation or token-separation regression vetoes general adoption and motivates a separate arm, not silent scope expansion.
3. **Are line footprints too restrictive for valid root-cause repairs?** Default: allow predeclared coupled ranges, no whole-document catch-all. Count legitimate maps rejected for fragmentation and stop rather than widening after the fact.
4. **Does a newly accepted changed finding duplicate a resolved old outcome?** Default: coordinator confirms identity; exact id reuse is forbidden except status transitions. A semantic fingerprint algorithm is UNVERIFIED and is not part of version 1.
5. **How much of S1's improvement would come from fix gating rather than review gating?** Default: this proposal tests the combined mechanism. A later ablation could remove the fix-map check, but the combined result cannot identify either component's isolated effect.
6. **Is an early scoped PASS useful when severe deferred claims remain?** Default: disclose both; do not equate PASS with approval to implement or ship. A product owner must decide whether to authorize a separate full review.
7. **How should plugin-only installation expose this command name?** Default: ship mirrored files and test installation/discovery in an isolated environment. Actual plugin runtime discovery is UNVERIFIED here. A plugin-only failure must not be concealed by successful source installation.

## 13. Test plan

Tests must check behavior, not just the presence of rule sentences. Use temporary directories and tiny byte-exact fixtures; no network, installed-user mutation, Git writes or dependence on the evidence worktrees. The new test module must execute the script as a subprocess as well as exercise its pure validation routines. All Python test execution uses UV.

### P0: eligibility and checker unit cases

| Case and concrete fixture | Required oracle |
|---|---|
| Empty diff: saved and current are `A\nB\n` | Zero eligible lines. A new blocker on B is rejected/deferred. Existing open F1.1 stays open even if proposed resolved. Round still advances once after a valid report. |
| Whitespace-only: `limit = 2\n` to `limit  =  2\n` | Raw diff present, effective changed mask empty. Raw edit still needs an open blocking owner in the fix map. New changed-line blocker cannot pass. |
| Mixed whitespace and real edit | Only non-whitespace replacement lines become eligible. Whitespace context cannot be used as a shortcut anchor. |
| Moved paragraph: `A\nB\nC\n` to `B\nA\nC\n` | Deterministic add/delete representation; eligible old/new sides follow computed opcodes. Do not assert a particular heuristic move identity. An unchanged C anchor is rejected. |
| Hard reflow: one paragraph split into two lines | Changed physical lines remain visible and eligible. No silent flattening to empty diff. Record the noise rather than pretending semantic equivalence. |
| Delete-only: `A\nrequired rule\nB\n` to `A\nB\n` | Hunk has eligible old line 2, no added line. A loss-of-rule finding with old-side quote and current insertion-boundary repair footprint passes membership checks. |
| Finding cites a deleted line as current | Reject, even if the same line number now holds B. Correct old-side anchor passes. Out-of-range line and wrong quote both reject. |
| Finding cites a context line within a valid hunk | Reject as an in-scope finding; hunk membership alone is not eligibility. Move to deferred only when it is actually unchanged context. |
| Stale hunk id from R2 reused in R3 | Exit 3 or stale-state exit 4 as appropriate, no accepted output or verdict change. Identical text in another round does not rescue it. |
| Duplicate finding ids in one draft or reused across rounds | Reject before grade derivation. Duplicate JSON object keys also reject, including duplicate `severity` or `surface_sha256`. |
| No findings: R1 `findings:[]`, `statuses:[]`, valid metadata | Accepted PASS, not parser failure. R2 with zero new findings and one open status is FAIL. R2 with a genuine effective fix and every blocker confirmed resolved is PASS. |
| New MAJOR with empty wrong outcome | Derive minor, not blocking. A nonempty unconfirmed outcome cannot pass. CRITICAL and confirmed FR-8/FR-9 follow their retained rules; MINOR cannot block. |
| Resolved prior id on unchanged text reported regressed | Reject reopening. Same original outcome on a newly changed footprint may regress with confirmed evidence. A different outcome needs a new id and current anchor. |
| Prior id alone laundering a new defect | Reject new-id records with only an unrelated prior id. A legitimate open continuation must use its exact existing id, outcome and grade. Semantic identity still has a manual test. |
| One good and one stale anchor in a finding | Reject the entire draft, not accept on the first good anchor. |
| Empty file, invalid UTF-8, BOM, CRLF and no final newline | Empty/invalid UTF-8 rejected; define BOM as an ordinary first codepoint and preserve it. Preserve CRLF and final-newline bytes in hashes. Eligibility numbering remains physical and one-based. |
| Repeated equal lines and large repetitive input | Stable opcodes and ids on repeated calls with `autojunk=False`; no anchor at the wrong occurrence. Reject size/line limits before diff; bounded stress test records runtime without a machine-specific flaky threshold. |

### P0: reviser authorization and lineage tests

- One legitimate replacement owned by an open blocker and contained in its footprint passes; computed byte sizes match raw files.
- An additional spelling fix owned by a minor fails even if useful. Unmapped edits, duplicate map entries, stale snapshot hashes and invented blocking ids fail with no new-round snapshot accepted.
- An insertion before line 1 and at EOF can be authorized by explicit boundary hashes. A deletion-only repair maps old lines correctly. An approved coupled site outside the primary anchor passes; an undeclared sibling edit fails.
- Two adjacent fixes that merge into one actual edit-group and name two owners fail. One owner covering the complete group passes only if its footprint authorizes all of it.
- A changed-line finding gets the actual owner of its edit group as parent. Supplied unrelated parent id fails; a line unchanged since the immediately previous review has no new-finding eligibility even if it was first added two rounds ago.
- A parent refuses an excessive footprint; the script cannot accept a fix using it. Test both the refusal record and exact coordinate containment, not an assertion that all broad rewrites are automatically detectable.

### P0: state-machine and failure tests

Exercise a complete stubbed chain: R1 FAIL, authorized fix, R2 resolves old blocker and finds a real changed-line child, second authorized fix, R3 finds a child defect, capped FAIL. Assert three accepted reviews, two fix checks and an open R3 child. A fourth review, third fix, reinitialized existing state or changed run id is refused. This proves finite execution without suppressing a fix-induced blocker.

Also exercise early PASS; valid empty diff with open blockers; missing/partial re-review arguments in an existing chain; wrong prior report digest; missing baseline; invalid status enum; missing prior status; duplicate status; wrong-side deletion quote; corrupted ledger; document changed during review; mismatched confirmation digest; unknown schema version; concurrent operation lock; unwritable state; forbidden or symlink paths; output aliasing the document; and failure injected before/after snapshot write and ledger replacement. None may yield PASS or reset the counter.

Report repair test: submit an unanchored blocking claim, check rejection, repair it into deferred using the same surface, accept once, then verify final summary shows it once with `blocking:false`. Submit two invalid drafts and assert terminal invalid with diagnostic history. Identical replay of an accepted operation is idempotent; changed accepted content is refused. Failure while writing the report leaves no accepted ledger event. Resume must recreate identical missing derived output or stop, never accept a different one.

### P1: command, installation and regression surface

- Static tests inspect both new command copies for Activation, state requirement, computed-anchor contract, seven adapted bullets, retained cap literals, no Improve on re-review, and unattended return-contract behavior. Run existing text pins against the untouched original, not against a relaxed matcher.
- Assert source/plugin parity for all new files. Scan the new installed primitives for prohibited package-source lookup paths; require both installed and project skill lookup surfaces. Keep the existing agent lookup order where retained.
- In an isolated temporary HOME, install/discover the new command and skill using the existing installer path; assert the new script is present and its CLI help works outside the repository. Place a sentinel old `spec-panel.md` there and assert its bytes stay unchanged. Never run this test against the real user HOME.
- Run `uv run pytest tests/skills/test_spec_panel_diffgate.py` after implementation. Also run the existing `tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_review_severity_rule.py`, `tests/skills/test_worker_contract.py`, `tests/skills/test_primitive_dual_surface_lookup.py` and `tests/unit/test_cli_install.py` with `uv run pytest`. Run repository lint and sync verification separately; text pins do not prove reviewer behavior.

### Live acceptance and manual semantic checks

The S1 experiment is a separate two-replicate validation, not a unit-test pass. Inspect each transcript for variant and protocol Skill calls, surfaces delivered before review, and parent checker invocation before every accepted edit. Check at least one rejected unanchored claim using a controlled nonmeasured fixture before starting S1.

Use a small manual case with a changed rule contradicting unchanged context: a valid current anchor and actual harmful consequence must remain blocking. Use a second case that quotes the same changed line but complains about an unrelated untouched section: parent must reject the causal claim. Replay the F22/N5/N12 pattern as a semantic example: a minor F22 edit is unauthorized, but an equivalent defect introduced by a legitimate blocking fix remains reportable at R3. These are semantic acceptance observations, not claims the script understands natural language.

## 14. Acceptance criteria

Implementation acceptance is separate from experimental success. An implementer can check the following without interpreting an optimistic forecast as evidence.

1. **Additive delivery.** All new command, skill, script, tests and mirrors in section 8 exist. The original source, plugin and installed `spec-panel.md` bytes remain unchanged. No real user installation is modified by tests.
2. **Portable invocation.** The installed helper runs through the stated UV pattern from a temporary non-repository working directory using only the standard library. Lookup follows installed-skill-first, project-skill-second order and refuses mixed or incomplete skill directories.
3. **Deterministic surface.** Repeated preparation of identical state produces byte-identical JSON and Markdown. A source change, round change or predecessor change invalidates its digest and hunk identities. Saved copies, not Git refs or file modification times, determine eligibility.
4. **Strict scope.** A finding with no eligible changed/deleted-line anchor and no permitted continuing blocker id cannot enter an accepted blocking set. A valid hunk id with an unchanged context line is insufficient. Deferred claims cannot authorize a fix or change the verdict.
5. **Deletion correctness.** A loss-of-rule finding can anchor a removed old line with its exact quote and authorize a current insertion boundary. A deleted line falsely cited as current is rejected.
6. **Report integrity.** Duplicate ids or keys, stale surfaces, missing statuses, false quotes, unknown ids and bad confirmations produce nonzero rejection with diagnostics. No generated report is authoritative before successful `check`. Zero findings is a supported valid report.
7. **Parent ownership.** Grade derivation and verdict use coordinator-confirmed evidence and script rules, not a reviewer-supplied verdict. The generated report has the prior status table first, compatibility origin fields where applicable, the exact round header and final verdict line. Notes alone never fail it.
8. **Fix ownership.** Every raw edit-group, whitespace included, maps exactly once to an open blocking id and an approved footprint. Unmapped, minor-owned, stale or out-of-footprint edits fail `check-fix`; the document is not silently reverted or accepted.
9. **Lease and lineage.** A substantive changed line is newly reviewable only in the immediate next review unless changed again. Untouched resolved findings cannot reopen. An actual new fix-induced blocker on eligible lines is accepted with its computed parent, including at R3.
10. **Bounded execution.** A valid chain accepts no more than three reviews and two fixes. One report repair is permitted per round on identical surface; a second reject stops invalid. Missing state or one missing predecessor flag never restarts a chain. Repeated terminal operations are idempotent, not fresh rounds.
11. **Safe state.** Digest, output collision, encoding, symlink, lock, resource-limit and crash-recovery tests pass. The helper never writes the target document. Any unresolved stale-state or persistence failure is a surfaced failure, never PASS.
12. **Deferred disclosure.** All deferred records and rejected unanchored candidates survive to one final appendix with their proposed severity and exclusion reason. Early PASS, capped FAIL and invalid termination all disclose them. The summary states PASS is scoped and is not permission to implement or ship.
13. **Unattended compatibility.** Directory refusals, TDD gating and return-contract outcomes are covered. Accepted audit FAIL is distinguishable from helper execution failure; `report_path` never names an unchecked draft. Requested report copies hash-match accepted reports.
14. **Regression evidence.** The new behavioral test module, listed existing regression modules, lint, source/plugin parity and sync verification pass after implementation. The source-path lookup scan has no new prohibited references. No static assertion is described as proof of live compliance.
15. **S1 screen.** Both replicates satisfy the pre-registered proxy and growth bars, with no integrity deviation or hidden changed-line defect; report the spread check, raw/deferred counts and runtime cost even when unfavorable. If this fails, retain or remove the additive variant by explicit decision, but do not promote it to the original command.

This proposal is complete as a specification. Its implementation, tests, installation behavior, cost estimates and S1 predictions remain unexecuted and therefore unproven.
