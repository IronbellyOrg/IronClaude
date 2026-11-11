# Spec-panel-ledger: a durable finding contract

Design proposal, variant 3. Nothing in this document is implemented.
All interfaces, paths and flags described as proposed below are new, not existing commands.

## 1. Problem and evidence

- Whole-document loops did not converge: control R3 critical+major mean 6.0; 427 mean 5.5; growth means 63.5% and 29.7% (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md:19-30`).
- In treatment, 89% of R2 and 100% of R3 new findings were on changed lines, not proof that every such finding was caused by the fix (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md:30`).
- Adding baseline flags gave R3 mean 3.5 and growth 30.0%, still not proven; proxy and blocking counts differ (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md:20-37`).
- Current enforcement is prose plus text-presence tests, not executable loop control (`docs/designs/spec-panel-review-loop.md:143`).
- Proposal: a single-writer, versioned ledger owns state; reviewers supply evidence, never the verdict. A lower ledger count alone is not evidence of a better document.

## 2. Mechanism

All steps below are proposed. MECHANICAL means the script refuses a violation; PROSE means a model must obey it.
Classification applies throughout: unmarked schema, storage, CLI, count and transition rules are MECHANICAL requirements; unmarked reviewer, reviser and coordinator instructions are PROSE.
Residual PROSE risks are semantic misjudgment, ignored scope, wrong dispatch and incorrect experiment recording; section 11 names them individually. No rule is claimed implemented.
Let `D` be the existing working specification; `L` an explicit absolute ledger path; `P` the selected skill directory.
Write `ledger <args>` below for `uv run --no-project python "$P/scripts/review_ledger.py" <args>`.
The coordinator alone runs ledger mutations; reviewer and reviser responses are untrusted JSON request files.
Each mutation supplies `--ledger L --op <stable-step-id> --expect-seq <last-seq>`; these are abbreviated below.
The coordinator passes the same `L` on every invocation. No missing-ledger fallback to a new FIND is allowed.

1. **Review 1, FIND.** Coordinator calls `ledger init --document D`, pinning `snapshots/r0.txt` and its digest.
   Reviewer reads that snapshot and the existing panel criteria, then writes `inputs/find-r1.json`, one finding per object.
   Coordinator calls `ledger find --input inputs/find-r1.json`; the script validates anchors, assigns F001 upward, freezes grading and commits review 1.
   It writes `reports/review-1.md` from ledger state and calls no reviser itself. `init` also emits `packets/find-1.json`; `ledger verdict` returns the next action.
2. **Revise 1.** Only on CONTINUE, coordinator calls `ledger packet --kind revise`, producing `packets/revise-1.json` with open blocking ids and the pinned preimage.
   Reviser reads it and edits `D` with prior user authorization; writes `inputs/revise-1.json` with one disposition per supplied row and explicit old/new line spans.
   Coordinator calls `ledger revise --cycle 1 --document D --input inputs/revise-1.json`.
   Script saves `snapshots/r1.txt`, computes `diffs/c1.json`, checks edit ownership, records byte/line sizes and sets only supported rows to fixed.
3. **Review 2, VERIFY.** Coordinator calls `ledger packet --kind verify`; reviewer reads `packets/verify-2.json`, named row histories and exact before/after sentence contexts, not the whole document.
   Reviewer writes `inputs/verify-2.json`: per-row resolved/open/regressed or cannot-verify, evidence quotes and touched-sentence assessment.
   This packet also authorizes the sole changed-line discovery check for the entire loop: all non-whitespace changed lines, maximum 200, with two context lines per hunk.
   That check may add at most one new finding C001, with the same grading rules and severity frozen on creation; two candidates or more than 200 changed lines yields ESCALATE, never silent truncation.
   Coordinator calls `ledger verify --review 2 --input inputs/verify-2.json`, then `ledger verdict`. Discovery budget is spent even when it finds nothing.
4. **Revise 2.** Only on CONTINUE, use `ledger packet --kind revise`, the new `packets/revise-2.json`, and the same reviser contract.
   Reviser edits `D` and writes `inputs/revise-2.json`; coordinator calls `ledger revise --cycle 2 --document D --input inputs/revise-2.json`.
   Script commits `snapshots/r2.txt` and `diffs/c2.json`. A crash never earns an extra cycle.
5. **Review 3, VERIFY.** `ledger packet --kind verify` produces `packets/verify-3.json`; reviewer writes `inputs/verify-3.json` checking remaining blockers and previously verified rows touched again.
   No discovery check remains. A different defect in a touched sentence is recorded as a regression observation and escalates, not relabeled as resolution of the original issue.
   Coordinator calls `ledger verify --review 3 --input inputs/verify-3.json`; `ledger verdict` returns PASS or ESCALATE, never CONTINUE.
6. **Final sweep.** At the first terminal loop decision, even early PASS or escalation, coordinator calls `ledger packet --kind sweep`.
   A fresh reviewer reads the entire last accepted snapshot once and writes `inputs/sweep.json`, including duplicates by existing id and genuinely new findings.
   Coordinator calls `ledger sweep --input inputs/sweep.json`; script stores new S001-style rows as deferred, preserves their blocking flags, and writes `reports/final.md`.
   There is no fix, re-VERIFY or second sweep. New blockers make the delivery outcome ESCALATE; zero blockers preserve the loop result.

MECHANICAL: packets bind response schema, round, document hash and ledger sequence; no response can advance the wrong phase.
PROSE: reviewers avoid reading extra document text and revisers avoid unrelated ideas. Residual risk: both can ignore scope despite a narrow packet.
MECHANICAL: snapshots, ledger and generated reports are script-owned. `D` remains reviser-owned; the reviewer never edits it.

## 3. Ledger file

### Storage and schema

MECHANICAL: use UTF-8 JSON, no comments, duplicate keys, NaN, unknown fields or implicit type coercion; `schema_version` is integer 1.
Proposed default `L` is `<document-parent>/.review-ledger/<document-stem>/<run-id>/ledger.json`; an explicit `--ledger` overrides it.
This is next to the reviewed source, works for untracked documents, avoids installed directories, and is directly script-readable.
Each run directory also holds `inputs/`, `snapshots/`, `diffs/`, `packets/`, `reports/` and `.lock`.
`run-id` is an opaque random identifier, not a timestamp; opening an existing `L` always resumes that run.
The only authoritative state is `ledger.json`. Reports and packets are disposable projections; snapshots are immutable dependencies.
Top-level exact keys are `schema_version`, `run_id`, `events`. Every event has `seq`, `op`, `actor`, `kind`, `request_sha256`, `body`.
`seq` is consecutive from 1; `op` is unique in the run; actor is `script|reviewer|reviser`, naming the evidence producer, not file permissions.
Event kinds are `init|find|revision|verification|sweep|halt`. Each kind has its own closed body schema.
`init` stores absolute document path, initial snapshot path/hash, byte/line sizes and frozen profile `spec-panel-v1`.
`find` stores rows; `revision` stores pre/post hashes, snapshot, diff and dispositions; `verification` stores row answers, relocations, observations and optional C001.
`sweep` stores duplicate references, challenges to existing verifications, and new deferred S rows. `halt` stores a structural stop reason, never a resolution.
MECHANICAL: a sweep challenge does not restart transitions; it remains a terminal observation whose blocking flag enters the delivery decision.
A row's current status is obtained by replaying events. `ledger show` returns the complete row projection as JSON; no second writable status store exists.

Example: a FIND event creates exactly three rows below. `H0` and `H1` stand for actual 64-lowercase-hex SHA-256 values in a real file; this is illustrative, not a runnable fixture.

```json
{
  "schema_version": 1,
  "run_id": "run-a831",
  "events": [
    {"seq": 1, "op": "init", "actor": "script", "kind": "init", "request_sha256": "H0",
     "body": {"document": "/workspace/spec.md", "snapshot": "snapshots/r0.txt",
              "sha256": "H1", "bytes": 180, "lines": 8, "profile": "spec-panel-v1"}},
    {"seq": 2, "op": "find-r1", "actor": "reviewer", "kind": "find", "request_sha256": "H0",
     "body": {"review": 1, "document_sha256": "H1", "rows": [
       {"id": "F001", "introduced_review": 1, "origin": "initial", "severity": "CRITICAL",
        "criterion": "correctness", "blocking": true, "initial_status": "open",
        "anchor": {"quote": "Retry creates a second payment.", "line": 2, "before": "Retries", "after": "Timeouts"},
        "issue": "A retry duplicates the debit.", "wrong_outcome": "The same request debits twice."},
       {"id": "F002", "introduced_review": 1, "origin": "initial", "severity": "MAJOR",
        "criterion": "correctness", "blocking": true, "initial_status": "open",
        "anchor": {"quote": "The cursor is shared by all users.", "line": 5, "before": "Pagination", "after": "Errors"},
        "issue": "One user's cursor skips another user's records.", "wrong_outcome": "A client loses records during pagination."},
       {"id": "F003", "introduced_review": 1, "origin": "initial", "severity": "MINOR",
        "criterion": "clarity", "blocking": false, "initial_status": "deferred",
        "anchor": {"quote": "An example may be included.", "line": 8, "before": "Examples", "after": ""},
        "issue": "An optional example would improve readability.", "wrong_outcome": ""}
     ]}}
  ]
}
```

MECHANICAL: row strings are bounded to 4 KiB each; quote is nonempty and exact; line is a positive 1-based integer; 200 initial rows and 10 MiB per document are explicit refusal limits.
MECHANICAL: id, original anchor, issue, wrong_outcome, origin, criterion, introduced_review, severity and blocking freeze at creation, including C/S rows.
MECHANICAL: CRITICAL or criterion FR-8/FR-9 is blocking; otherwise MAJOR is blocking iff wrong_outcome is nonempty; other rows are notes.
PROSE: deciding whether wrong_outcome is concrete or the grade is justified remains a reviewer judgment. A syntactically nonempty false claim can still block.
MECHANICAL: no severity promotion or demotion, even on reopening; discovered higher harm becomes a separately reported escalation observation, not an upgraded old row.
No automatic blocking deferral or user-waiver API in version 1. Disputed blockers escalate honestly; notes are initially deferred.

### Row transitions

Only the script writes states. WHO below means who can request the evidence-bearing transition through the coordinator.

| From | To | WHO and required evidence |
|---|---|---|
| absent | open | Reviewer in FIND, or sole authorized changed-line check; script derives blocking=true. |
| absent | deferred | Script for nonblocking FIND/check rows; all final-sweep rows, even blockers, are deferred. |
| open/reopened | fixed | Reviser supplies applied disposition, before/after spans and explanation of the fix. |
| open/reopened | same | Reviser supplies no-change/disputed reason; reviewer confirms unresolved. |
| fixed | verified | Reviewer quotes the replacement or proves deletion, judges original harm absent and touched sentence sound. |
| fixed | open | Reviewer proves original finding remains and no earlier verification exists. |
| fixed | reopened | Reviewer proves failure after an earlier verified state; history, not last status, controls this. |
| verified | fixed | Reviser changes its mapped sentence again while fixing another blocker; script invalidates old verification. |
| verified | reopened | Reviewer shows regression in a rechecked row. |
| verified | verified | Script carries it only when its mapped text and supporting context are unchanged. |
| deferred | deferred | Script preserves note or sweep observation; no revision authority follows. |

MECHANICAL: every unlisted edge, missing row, duplicate response, unauthorized phase or absent evidence is `E_TRANSITION`; append nothing.
A missing/ambiguous anchor cannot become verified; it stays unresolved with `anchor_state=missing|ambiguous` and yields ESCALATE if no supported mapping is supplied.

### Anchor relocation and edit ownership

MECHANICAL: retain the frozen initial quote and line forever; each revision appends a separate mapping with snapshot hash, current quote, start/end line and method.
Use unchanged-block line mapping first; then unique exact quote with exact before/after context. Line numbers are hints, never proof.
If the old quote was rewritten, use the reviser's replacement span only when its old span contains the previously mapped quote and its new span belongs to the computed replacement hunk.
Repeated quotes need unique context; never pick the nearest match silently. An empty replacement is a tombstone, not proof of resolution.
PROSE: verifier must decide whether deletion removed the requirement improperly. Residual risk: a deleted obligation can look like a successful fix.
MECHANICAL: each changed old/new line belongs to at least one submitted blocking-row span; uncovered edits fail revision admission.
A disposition names the original issue, exact spans and change summary. Shared hunks list every affected row; note-only rows cannot sponsor edits.
PROSE: this detects unclaimed edits, not unrelated mechanisms hidden inside a claimed span. The verifier checks that semantic boundary.

## 4. Termination rule

Retain verbatim: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`.
That literal is pinned in `tests/skills/test_review_severity_rule.py:215-219` and present in `src/superclaude/commands/spec-panel.md:261`.
MECHANICAL: the loop has one FIND and at most two VERIFY commits; initialization, packet generation and crash retries are not reviews.
Let `r` be the highest committed review number, and `B_r = count(row.blocking AND row.status != verified)` after that review.
Let `X_r` count unresolved regression observations, anchor failures, coverage overflow and cannot-verify answers; notes never enter X.
Let `I` mean valid replay, intact snapshots, complete row responses and no out-of-band document change.

```text
if not I or X_r > 0:                  ESCALATE
else if B_r == 0:                     PASS
else if r < 3:                       CONTINUE
else:                                ESCALATE
```

MECHANICAL: at `r=0` only FIND is legal; during a revision/response wait, return `pending`, never evaluate an incomplete review as PASS.
A fixed row still counts in B until verified. A deferred blocking sweep row also counts; deferral never launders a blocker.
MECHANICAL: final sweep is OUTSIDE the three-review remediation cap, with its own `phase: sweep`, no review-4 label and no authority to reopen the loop.
It is a deliberate extra full-document assessment, not a disguised fourth fix cycle. Do not claim the total number of assessments is three.
Let `S` count new sweep blockers, blocking challenges to previously verified rows, and unresolved sweep uncertainty; delivery outcome is ESCALATE iff loop outcome is ESCALATE or S > 0, else PASS.
Before sweep completion, PASS is explicitly `loop_decision`, never `delivery_outcome`; no final PASS artifact is emitted early.
MECHANICAL: CONTINUE renders `verdict: FAIL` with only current blockers in the Reviser brief; ESCALATE omits revision instructions and renders `verdict: FAIL`.
PASS renders `verdict: PASS`; headers remain `review: N of 3`. The script, not the reviewer, appends the verdict line.
MECHANICAL: a second sweep, a fourth review, a third fix or FIND on an existing run is refused, even with a new operation id.
No monotonicity halt is added to spec-panel. Counts and the cap suffice; other adopters can require stricter guards explicitly.
If integrity cannot be established, stop without a sweep and report an incomplete run, not a completed review loop.

## 5. Difference from PR 427

427 already accepts prior findings and a saved copy; it checks prior blockers, permits changed-line findings and relies on the coordinator's count (`src/superclaude/commands/spec-panel.md:258-264`).
This proposal removes three things, not just a flag omission:
- MECHANICAL: VERIFY has no arbitrary findings array. It accepts existing row answers and, only in review 2, the one bounded discovery result.
- MECHANICAL: existing findings cannot be reworded, renumbered, regraded, silently dropped or marked resolved by the reviser.
- MECHANICAL: the script derives diff ownership, remaining blockers, report verdict and legal next phase; a report header cannot reset the count.
PROSE: the verifier is asked to assess only the finding and the touched sentence, not search the changed document for every possible defect.
Residual risk: a model can disguise a new objection as a failed verification. Evidence and immutable issue text expose that for audit, not automatic truth detection.
The final sweep deliberately restores full-document visibility once, but its findings cannot spawn another automatic fix/review chain.
This is narrower than 427, and may hide real defects until escalation. That trade must be tested, not described as guaranteed convergence.

## 6. Exact changes, file by file

All additions in this section are proposed implementation work, not changes made by this design task.

| File | Exact responsibility |
|---|---|
| `src/superclaude/commands/spec-panel-ledger.md` | New additive command, installed as `~/.claude/commands/sc/spec-panel-ledger.md`; invocation `/sc:spec-panel-ledger`. |
| `src/superclaude/skills/review-ledger/SKILL.md` | New owning skill: actor packets, orchestration, precedence, complete CLI and response schema. |
| `src/superclaude/skills/review-ledger/scripts/review_ledger.py` | New standard-library-only state machine, validator, diff engine and report renderer. |
| `src/superclaude/skills/review-ledger/refs/schema-v1.json` | Closed JSON Schema for ledger events and actor inputs; script implements equivalent explicit validation without a new dependency. |
| `tests/skills/test_review_ledger.py` | Behavioral reducer, CLI, crash, lock, anchor, scope, verdict and schema parity tests. |
| `tests/skills/test_spec_panel_ledger_contract.py` | Command/skill lookup, cap literal, critique-only semantics and unchanged original-command contract. |
| `tests/skills/fixtures/review-ledger/` | New tiny documents and actor JSON covering ambiguous anchors, deletions, shared hunks and invalid requests. |
| `docs/designs/spec-panel-ledger.md` | Maintainer contract, recovery guide, S1 protocol and explicit nonclaims. |
| `docs/user-guide/spec-panel-ledger.md` | New usage, ledger path, pending versus final results and resume examples. |

A script must ship in the skill payload: installation copies the whole skill directory (`src/superclaude/cli/install_skill.py:35-53`).
Use the loaded skill base, as the existing helper invocation does (`src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:54,64`).
The new command must load `review-ledger` before any review; lookup skill globally at `~/.claude/skills/review-ledger/SKILL.md`, then project `.claude/skills/review-ledger/SKILL.md`.
Never put source-tree paths in installed command instructions. This table names source files for maintainers only.
Plugin packaging parity/discovery for a NEW command and skill has not been inspected: UNVERIFIED; resolve before implementation, do not promise a plugin install.
Leave `src/superclaude/commands/spec-panel.md`, its plugin copy, severity pins and routing defaults unchanged. No automatic migration or replacement of old reports.

### New command text outline

1. Metadata/name; explicitly experimental, critique-only, preserves panel methods for FIND and final sweep.
2. Proposed usage: `/sc:spec-panel-ledger @file --ledger <absolute-path> [--mode critique] [--experts "names"] [--focus areas] [--format standard|structured|detailed] [--iterations N]`.
3. Accept existing critique selectors as presentation options; `--iterations` never creates another review. Existing selectors are documented in `src/superclaude/commands/spec-panel.md:22-26`.
4. Load owning skill, validate L and phase, call script, supply only the emitted packet; no inline fallback if helper is missing.
5. Treat any caller phrase making minor findings fail as overridden; deliver script-generated report and next action, not a model verdict.
6. User authorization to revise remains separate; command itself reviews only. Resume infers the phase from L, never from the latest report filename.

### Proposed script CLI and checks

Every subcommand requires `--ledger`; mutators additionally require `--op` and `--expect-seq` (init expects 0).
`init --document <path>` creates the run; `find --input <json>` admits review 1.
`packet --kind revise|verify|sweep` emits a deterministic packet path plus its hash; no history event.
`revise --cycle 1|2 --document <path> --input <json>` snapshots the candidate and admits one disposition batch atomically.
`verify --review 2|3 --input <json>` checks exact row coverage and evidence, commits the review, computes its decision.
`sweep --input <json>` commits the one terminal sweep. `validate`, `show` and `verdict` are read-only projections.
Success stdout is one JSON object: `{schema_version,run_id,seq,phase,review,counts,loop_decision,delivery_outcome,next_action,artifact_paths}`; unset decisions are null.
Errors return `{error,run_id,seq,detail,next_action}`; diagnostics go to stderr, never mixed into JSON stdout.
Exit codes: 0 successful operation/query; `verdict` alone uses 2 for CONTINUE, 3 for ESCALATE; 4 invalid data/transition, 5 lock/sequence/idempotency conflict, 6 I/O failure, 7 unsupported schema or CLI usage.
An operation may successfully commit an ESCALATE decision and exit 0; callers inspect JSON, never infer PASS from process success.

MECHANICAL: every actor-input object has exactly `packet_sha256`, `document_sha256`, `data`; phase-specific data has these closed fields:
- FIND: `findings`, an array of `{anchor,severity,criterion,issue,wrong_outcome}`; the script supplies ids, origin, status and blocking.
- REVISE: `candidate_sha256,dispositions`; each disposition is `{id,action,reason,spans}`; action is `applied|no-change|disputed`.
- A span is `{old_start,old_end,new_start,new_end}` using 1-based half-open line ranges; zero-width ranges denote insertion/deletion boundaries.
- VERIFY: `answers,discovery,observations`; each answer is `{id,result,evidence,reason,sentence_sound}` with result `resolved|open|regressed|cannot-verify` and sentence_sound boolean.
- Evidence is an array of `{snapshot_sha256,start,end,quote}`; quote must exactly match that snapshot range. A deletion cites the old range and its new tombstone boundary.
- Discovery is null in review 3; in review 2 it is `{complete,findings}`, with at most one FIND-shaped object plus a diff-hunk reference, or an explicit overflow observation.
- SWEEP: `new_findings,duplicates,challenges,complete`; duplicates name existing ids; challenges use VERIFY-shaped answers; incomplete sweep yields ESCALATE.
MECHANICAL: packets enumerate the exact required answer/disposition ids; the script carries untouched verified rows and notes itself, never asks the reviser to certify them.
MECHANICAL: candidate_sha256 must match bytes captured from D; expected preimage is the packet's document_sha256. Reject a candidate changed during capture or readback.
MECHANICAL: discovery quotes must intersect computed changed old/new ranges; its overflow signal is accepted as a halt observation, not a second finding row.
All admitted input fields are retained in the corresponding event body, alongside script-derived ids, mappings, digests and counts, so replay does not depend on mutable inputs/ files.

MECHANICAL: diff raw saved bytes as UTF-8 line arrays using deterministic sequence matching with heuristic autojunk disabled; never compare git refs or current repository HEAD.
Save zero-context old/new hunk ranges, insertion/deletion boundaries and content digests in `diffs/cN.json`. Compute both raw and whitespace-normalized changed sets.
Raw hunks drive ownership and document hashes; whitespace-only hunks are excluded only from discovery. Deletions retain old spans and a new insertion boundary, so empty new spans do not disappear.
No diff means no new fixed states; unresolved blockers remain open and the subsequent VERIFY still consumes its review slot.
MECHANICAL: reject stale document/packet hashes, incomplete dispositions, reused row ids, malformed evidence, uncovered hunks, symlinked run members and path traversal outside the explicit run directory.

### Transaction, crash and rerun contract

MECHANICAL: acquire a nonblocking OS advisory lock on `.lock`; no stale-lock timeout stealing. Single-host local filesystem only in version 1.
Under lock: validate/replay L, look up op, check expected sequence and hashes, validate the entire proposed event, then save snapshots/diffs before publishing L.
Write each immutable artifact to a same-directory temporary file, sync it, then publish with an atomic no-replace hard link; unlink the temporary name and sync the directory before committing references.
If the final artifact name exists, require byte-identical content; partially written temporary files are never referenced. Refuse filesystems without these local publication guarantees.
Create a temporary ledger in the same directory, preserving the complete old event prefix and appending exactly one event; sync it, atomically replace L, sync the directory.
This is logically append-only history, NOT physical append-only file bytes. There is no second status file requiring a distributed transaction.
An identical op and request digest returns its original prefix-derived result without appending, even with an old expect-seq; same op with different content is `E_IDEMPOTENCY`.
Request digest covers canonical input JSON and document content hash, excludes transport fields op/expect-seq; the coordinator retains the submitted candidate hash for retries.
Crash before ledger publication leaves the previous valid state and possibly unreferenced artifacts; crash after publication resumes from the committed event and regenerates missing reports.
A reviser crash can leave D partly edited: it is uncommitted input, not accepted state. Resume from the saved preimage or finish the same candidate; never manufacture a passing event.
MECHANICAL: no auto-repair of malformed L or missing referenced snapshots; fail closed. A different live D before VERIFY requires investigation, not silent re-baselining.
Tests inject failure before/after every sync/replace boundary, kill a lock holder, replay identical/different ops, race two writers and verify that only a whole old or whole new event is visible.
Also test every status edge, all verdict branches, CRITICAL/FR grading, note non-revision, sweep blockers, both cap refusals, raw/normalized diff coverage and unknown schema refusal.
Schema/examples must round-trip through actual validation; the illustrative H0/H1 values above are replaced with fixture digests.

## 7. Adoption by other review tools

Adoption is later work, not bundled into the first experiment. Reuse storage and transitions, not spec-panel grading everywhere.

| Adopter | Proposed adapter | What must remain different |
|---|---|---|
| `/sc:reflect` | Seal FIND after the existing synthesis/evidence gate; assign canonical ids after merged findings, never once per reviewer. Caller carries L through remediation; VERIFY consumes row packets. | Keep mode-specific grounding, reviewer diversity, calibration, evidence validation and separate promotion permission. Ledger PASS cannot authorize promotion. |
| rf-qa agents | Translate IMPORTANT to a profile-specific blocking severity, submit Fix Cycle row answers, replace model-written counts with script counts. | Keep regression-before-monotonicity-before-cap, synthetic-finding dedup keys and existing halt messages. Do not weaken those guards to match spec-panel. |
| `/sc:implement` final review | Add a sidecar finding ledger for repeated final-review failures, separate from the task progress ledger; bind it to the entire delivery-state digest. | Every archive attempt still needs a fresh independent full FINAL; a prior ledger PASS cannot replace it or change per-task verdict grammar. |

Reflect's grounding, heterogeneous fan-out and evidence gate are explicit in `src/superclaude/skills/sc-reflect-protocol/SKILL.md:148-167`.
rf-qa already verifies prior blockers and ignores minors, but writes its verdict and enforces stricter stop guards in prose (`src/superclaude/agents/rf-qa.md:386-416`).
Implement currently permits new blockers anywhere in task-owned text on every review (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:184-196`).
Its FINAL explicitly requires fresh full-plan/full-delivery inspection per archive attempt (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:309-311`).
Therefore wholesale VERIFY-only adoption by FINAL would be incompatible: use ledger-backed repair tracking between mandatory FINALs, or seek a separately approved contract change.
MECHANICAL, future: each adapter pins its own grading/stop profile at init; unsupported profiles fail, rather than falling through to spec-panel defaults.
PROSE, future: semantic adapters must preserve each tool's meaning of evidence. Residual risk: mapping different severities by name silently changes release gates.
No reach claim for these adopters until their own experiments pass.

## 8. Stateful reviewer session versus file ledger

| Choice | Benefit | Failure mode |
|---|---|---|
| One persistent reviewer conversation | Less repeated context and potentially fewer starts; remembers why a fix was requested. | Memory is neither a durable transaction nor a reproducible count; compaction, crash and self-consistency bias can erase or defend prior judgments. |
| File ledger with fresh verification sessions | Explicit state, replayable counts, crash recovery and independent judgment with bounded inputs. | More files and calls; narrow packets omit context, and independently restarted reviewers can still disagree semantically. |

Recommendation: file ledger is authoritative; fresh VERIFY reviewers consume it, and the final sweep uses a fresh session.
Keep original rationale as immutable row text, not hidden conversation memory. A resumed reviewer may cache context but gains no write authority.
MECHANICAL: any cache/session output must carry the current packet digest; old-session answers cannot mutate newer state.
PROSE: use an independent final reviewer. Residual risk: a coordinator can reuse the same model/session despite this instruction; actor labels alone do not prove independence.
Skip a durable reviewer-session manager, database server and model-specific identity service in version 1. Files and a local lock are enough for this bounded experiment.

## 9. Measurement plan on S1

Use the same S1 starting bytes, base, overlay, model and briefs as the controlled experiment, not today's changed contract document (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md:49-55`).
Only authored brief change: substitute `/sc:spec-panel` with `/sc:spec-panel-ledger --ledger <absolute-run-path>` on its invocation line. Keep existing requested output filenames.
The variant's generated report supplies the reviser contract/JSON response request; do not rewrite the surrounding brief to make it cooperative.
PROSE: the coordinator copies the helper's report verbatim to the original explicitly requested output path; the helper itself writes only within its run directory. Residual risk: a manually edited copy can misstate the computed result.
D9 showed personal command precedence, so a distinct installed name is necessary; loading only a project copy is not activation evidence (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md:45-46`).
Future experiment setup must record variant command, skill and script hashes and actual loaded paths. This design task installs or edits nothing globally.
Use two independent treatment replicates and the same controls; label reused historical controls and their time separation, rather than claiming concurrent randomization.
Preserve D5 M1 rounds, M2 blocking findings, M3 fix-induced share, M4 bytes/lines/growth and M5 calls/tokens (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md:22-23`).

MECHANICAL: record raw ledger `B_3` and severity proxy separately. A MAJOR note still belongs to the critical+major proxy, not the blocking count.
Define `U3 = {F/C rows with severity CRITICAL or MAJOR and status != verified after review 3}`.
Define `W = {new CRITICAL/MAJOR S rows from the final sweep}`; deduplicate references to existing ids, never count a resolved-history mention as open.
The headline comparable end-state proxy is `|U3 union W|`, not merely B3. Publish `|U3|`, `|W|` and their union separately so reduced search cannot manufacture success.
A sweep allegation that a verified row still fails invalidates that verification for measurement and delivery escalation; record it as an observation referencing that id, without mutating its frozen issue/severity.
Include such challenged ids in U3 for the end-state proxy and show the pre-sweep raw count separately. Never erase a sweep finding because discovery budget was spent.
PROSE: duplicate recognition and fix-caused attribution need independent analyst judgment. Residual risk: subjective merging understates the union or overstates causality.
For early terminal runs, carry the terminal document/count to the R3 horizon without inventing another review; report the actual number of reviews and no further growth.
If integrity/overflow prevents a final sweep, the replicate is incomplete, not a zero-finding success; report the failure and costs.

Forecast, not measured: headline proxy 1 and 2, mean 1.5, versus control mean 6.0; growth 20% and 25%, mean 22.5%, versus control mean 63.5%.
Expected raw unresolved ledger blockers at R3: 0 to 1. Expect the final sweep to supply much of the remaining proxy, rather than claiming none exist.
Apply the fixed bars <=3 and <=44.4%, effect larger than the larger within-arm spread, and every treatment replicate better than every control replicate (`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md:64`).
The forecast proxy effect is 4.5 versus control spread 4; forecast growth effect is 41 points versus control spread 11.6 (controls in `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md:13-19`).
Fail the idea for S1 if either bar, spread test or per-replicate ordering fails; also fail it if ledger PASS routinely becomes sweep escalation without a lower combined proxy.
A low raw B3 with a combined proxy above 3 is suppression, not convergence. A pass proves only a large-effect screen on S1, not the other tools.
MECHANICAL: measure both live D and the accepted snapshot; any mismatch is surfaced. Growth uses accepted raw byte sizes after each fix; sweep calls/time enter M5, never document growth.
Record review/verify/sweep wall time and calls separately; early escalation is not a clean early PASS, and counting a fourth assessment has a real cost.

## 10. Causes removed and causes left

Evidence distinguishes observed association from demonstrated causation. Changed-line origin is observed; grading drift is a reported risk, not a quantified causal effect.

| Cause or symptom | Proposed effect | Limit |
|---|---|---|
| Fresh finding batches on changed lines | MECHANICAL: removes unlimited later discovery; only C001 and final sweep can introduce new rows. | Does not remove actual fix-induced defects; row verification and sweep can still expose them. |
| Severity drift | MECHANICAL: existing-row severity and blocking freeze at creation; counts cannot rise by relabeling. | PROSE: initial grading can be wrong; a new allegation can still create escalation pressure. |
| Reviser additions, including minor fixes | MECHANICAL: only blocking-row spans sponsor edits; notes never enter the revise packet. | PROSE: new mechanisms can hide inside an authorized hunk; lexical ownership is not semantic necessity. |
| No mechanical stop | MECHANICAL: history-derived phases and cap refuse extra cycles and repeated FIND. | PROSE: a caller can abandon L and start a new run; version 1 has no cross-run approval registry. |

The changed-line shares are measured in `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md:30`.
The enrichment reports a fix-created N12, all minor rows applied, and related extra fixes (`.dev/brainstorms/346-ledger/enrichment/codebase-context.md:22-24`); these are secondary observations, not independently re-read original session logs here.
MAJOR variability and the unenforced count are acknowledged by the existing design (`docs/designs/spec-panel-review-loop.md:162-164`).
Net claim: fewer opportunities to move the goalposts, not proof that the original specification is correct or that all wrong fixes are prevented.

## 11. Risks and costs

Planning estimates below are UNVERIFIED forecasts, not timings from the experiment.
A full three-review loop uses 15 dedicated helper invocations in section 2, plus optional validation/show calls and actor response writes.
It uses four reviewer sessions including the sweep and two reviser sessions, versus the specified three reviews and two revisions without a sweep.
Budget 0.1 to 2 seconds per local helper start, and 5 to 15 minutes for the extra full sweep; verification context savings may or may not offset that session.
Net extra tool calls and total wall time are UNVERIFIED until M5 and session durations are recorded. Report both medians and per-run totals, including failed/retried calls.
Storage is roughly three complete document copies plus JSON/history/reports. There is no background service, network dependency or external database.

| Rule or cost | Enforcement | How it could make the loop worse or remain unsafe |
|---|---|---|
| Narrow VERIFY packets | MECHANICAL for packet shape; PROSE for actual reading scope | Missing distant contradictions causes false PASS; models can read the full file anyway. |
| Frozen severity | MECHANICAL | Locks in bad first-pass grading; legitimate discoveries escalate instead of improving the frozen judgment. |
| One new-row budget, 200 changed lines | MECHANICAL | Large legitimate fixes escalate immediately; an overflow may dominate S1 rather than test convergence. |
| Row-scoped reviser behavior | PROSE, with MECHANICAL hunk ownership | A reviser can attach a legitimate id to unrelated additions in the same span; false ownership creates false confidence. |
| Concrete wrong outcome and correct fix | PROSE | Fluent but false evidence passes structural validation. A script cannot decide specification truth. |
| Sentence boundary/context choice | PROSE, script validates quoted spans | Reviewer may omit the dependent sentence that proves a regression; context hashes alone do not prove semantic coverage. |
| No note-driven fixes | MECHANICAL request filtering; PROSE semantics | A minor improvement can be smuggled into a blocker fix; a mislabeled serious note remains unfixed. |
| Final sweep is independent and exhaustive | PROSE for reviewer behavior; MECHANICAL once-only admission | Correlated blindness remains, and the sweep can expose expensive late surprises that cannot be fixed automatically. |
| No fourth remediation review | MECHANICAL within one L | Early halt can leave more user work than a longer loop. Starting another run bypasses the cap unless the caller obeys PROSE run continuity. |
| Correct phase dispatch and command/skill loading | PROSE, with MECHANICAL response rejection | Wrong tool text or a caller ignoring helper errors can bypass the design entirely; logs must show actual calls. |
| Local atomic replacement and file sync | MECHANICAL, local-filesystem assumption | Unsupported filesystems or host/storage failure may violate durability; no NFS/distributed writers supported. |
| Actor separation | PROSE for identity; MECHANICAL allowed-field checks | All agents may share one OS account. Actor strings are not authentication and cannot stop deliberate impersonation. |
| Append-only event history | MECHANICAL through helper API | A direct editor can rewrite history and recompute hashes; this is crash safety, not tamper-proof audit storage. |
| Quoted source and snapshots | MECHANICAL size/path checks; PROSE confidentiality | Ledgers duplicate potentially sensitive content. Do not upload them automatically; local permissions do not decide what is safe to share. |
| Retry operation reuse | MECHANICAL | Wrong op reuse is refused, but missing request files or changed D may require manual recovery rather than convenient continuation. |
| Exact anchors and raw diff | MECHANICAL | Reflow, duplicated quotes or huge replacement hunks can cause false ambiguity, overly broad ownership or escalation of harmless edits. |
| Consistent grading over adopters | PROSE until adapters are tested | Reusing spec-panel's severity mapping in rf-qa/FINAL can weaken an existing release gate. |

MECHANICAL: emit operation result with seq, input/document hashes, row counts, phase and next action; never log full request bodies to stderr.
PROSE: operators retain run directories until experiment recording finishes, then apply their project's retention policy. Residual risk: uncontrolled deletion breaks replay and duplicates can retain secrets indefinitely.
MECHANICAL: future unsupported schema versions stop without migration. Upgrade/recovery work cannot silently rewrite old events.
Recommend the smallest scope: one local ledger script and one additive command; skip cross-run dedup services, signatures, auto-waivers and a generalized workflow engine.
PROSE residual risk of this scope choice: independent callers can create competing ledgers for the same document; each is individually consistent but they do not share a cap.

## 12. Open questions

1. Is one loop-wide changed-line discovery check acceptable? This proposal chooses review 2 only; widening it after seeing results invalidates the comparison.
2. Is the 200-line refusal limit practical for S1? Preflight on saved copies before preregistering a run; do not silently sample lines or tune it after a failed replicate.
3. Can the existing output-format selectors carry a script-generated report without surprising callers? The variant keeps requested report destinations but must document reduced formatting freedom.
4. Does the final-sweep proxy union need blinded analyst duplicate adjudication in both arms? Recommended yes; raw counts must remain available.
5. What additional evidence makes deleted requirements safe to verify? Version 1 requires a reviewer explanation and an exact tombstone, not mere disappearance.
6. How should a genuinely wrong initial blocker be disputed without freezing a false failure forever? Version 1 escalates; a future operator-ruling event needs a separately approved authority model.
7. Which plugin packaging surfaces discover the new skill and command? UNVERIFIED here; installation coverage is a required implementation acceptance test.
8. Should later adapters retain this final-sweep policy or their stronger independent full reviews? Keep stronger gates until separately measured, especially archive FINAL.
9. Are local advisory locks and directory sync supported on every intended host? Version 1 claims only a single Linux host with a local filesystem; other platforms need explicit tests.
10. What cost ceiling makes the extra sweep unjustified? Set a wall-time/tool-call budget before S1, alongside the existing quality and growth bars.

Design is complete; implementation, installation, tests and live S1 runs were intentionally not performed. The main unresolved risk is apparent convergence caused by reduced discovery rather than fewer real defects.
