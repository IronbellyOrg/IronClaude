<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (opus:architect) -->
<!-- Merge date: 2026-10-24T06:56:32Z -->
<!-- Plan: refactor-plan.md (35 changes); log: merge-log.md -->

# Severity and convergence for /sc:implement (merged spec)

<!-- Source: Base (original, modified): retitled from "Variant 1 (architect)" for the merged document -->
Path prefixes: `P=src/superclaude/skills/sc-implement-protocol/` (this checkout); `E=/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/implement/03-memory-docs-f5865990/` (evidence run). Seed: `../seed-brief.md`.

## 1. Problem, scope and terms

<!-- Source: Base (original, modified): revert count corrected per base defect X-018 (Change #1) -->
**Problem.** In run `E` a docs-only task (T1, 4 AC, 2 files) used five attempts, 3 `step=revert` records (`E/progress.md:5,9,13`; the evidence file's fourth revert is UNVERIFIED) and about 1.17 million subagent tokens, then halted `ladder-end` (`E/progress.md:16`), although the last two reviews found only evidence-paperwork gaps (`E/retries/T1/review-4.md:3`, `review-5.md:3-11`). Current behaviour that causes it:

- The verdict has no severity: any unmet AC gives `missing`, any extra scope gives `extra` (`P/refs/qa.md:37-50`).
- Any non-compliant verdict after the one fix pass enters the ladder (`P/SKILL.md:129`, `P/refs/retry.md:7-14`).
- Each ladder step reverts to Q0 (`P/refs/retry.md:11-13`, `:148-178`) and brings in advisers (`:72-87`).
- Every review is a fresh whole-diff audit with no memory of earlier reviews (`P/refs/qa.md:5-11`, `:88-90`).
- The only exit from a halt is a user Ruling (`P/refs/qa.md:61-68`, `P/refs/retry.md:449`).
- Nothing stops the orchestrator adding review criteria (`P/refs/qa.md:88` lists inputs but forbids nothing).

<!-- Source: Variant 2 (sonnet:refactorer), Section 3 opening (V2:87); base-selection Clarity criterion 4: merged per Change #1 -->
**Terms.** Each term is defined once here and used with this meaning throughout.

- **AC**: an acceptance criterion of a task, cited as `Ti.ACk`.
- **Q0 to Q8**: the per-task steps of `P/SKILL.md` (Q0 snapshot, Q1 execute, Q2 diff, Q3 review, Q4 verdict, Q5 fix pass, Q6 extras, Q7 gate, Q8 next).
- **`$start`**: the tree recorded by the task's `start sha=` line, the Q0 snapshot.
- **A1 to A5**: the attempts, the rows of the attempt ladder (`P/refs/retry.md:7-14`). A1 is Q1, A2 is the Q5 fix pass, A3 to A5 are the adviser-brief attempts.
- **Ladder**: the escalation procedure of `P/refs/retry.md` that runs A3 to A5.
- **Review k**: the review that closes attempt k; `review-<k>.md` is its file.
- **Repair re-review**: the fresh review after a repair (Section 6.1). It sits inside the attempt it repairs and does not start a new attempt.
- **Legacy FINAL**: the advisory whole-list review of a legacy source (`P/SKILL.md:155`).
- **Managed FINAL**: the mandatory archive-gate review of a managed package (`P/refs/managed-workspace.md:49`).
- **Ruling**: the user-confirmed acceptance record of `P/refs/qa.md:54-72`.
- **Blocking family**: the set of blocking findings that share one `family=` value (FR-008).
- **Origin**: where the flagged text came from: `inherited`, `late`, `fix-induced`, `new` or `unknown` (Section 3.2).

<!-- Source: Variant 2 (sonnet:refactorer), Section 1 (V2:9-19); seed-brief Addenda 1 to 3 (SB:79-103); IR rule 34: merged per Change #2 -->
**Scope.** Requirements for changes to `src/superclaude/commands/implement.md`, `P/SKILL.md`, `P/refs/{qa,retry,ledger,managed-workspace}.md`, their plugin mirror, their tests, and one line of `src/superclaude/output-styles/pragmatic.md`. The archive helper `P/scripts/archive_workspace.py` is not changed. This document is a spec only. It covers the seven requested items (severity model; attempt-based convergence; the role of `/ponytail-review`; caps and the accepted-minor path; fix in place with advisers only for blockers; the closed reviewer contract; the output-style decision) plus the three user Addenda:

- Addendum 1: per-finding first-seen attempt, and distinct handling of late discovery, fix-induced regression and inherited text (Section 3.2).
- Addendum 2: fix the pattern, not only the named instances (Section 6.2); fix-induced regression detection and a severity-weighted convergence measure (Section 3.4); reviewer-standard drift control (Section 7); the PVE2 replay (Section 10.3).
- Addendum 3: a per-attempt statement of which severities may interrupt automation or prompt the user (Section 5.2), and the full list of remaining interrupts (Section 5.3).

**Out of scope.** The adviser citation-stability rule (`P/refs/retry.md:80`, evidence mechanism 9). It is a real cost, but it is not one of the seven requested items. The `/task-builder` A.10 finding quota and its all-severity monotonicity rule: a listed follow-up, not this release. Revert safety, sweep refs and the archive helper's move rules stay unchanged.

**Design stance.** Add one concept, a per-finding severity derived from factual answers, and one exit, a repair in place; route everything else through records and files that already exist. No new verdict value, no new ledger record kind, no new halt reason, no new flag, no helper change. The only scaffolding added is what a requirement below needs: a finding-line format in review files, a per-task notes file, repair and probe files, and reviewed-tree refs.

**Rollout.** Two phases; each ships and reverts alone.

| Phase | Content |
|---|---|
| P1 | Severity derivation (Section 2), notes file and accepted-minor path (Section 5.4), closed reviewer contract (Section 7), origin fields (Section 3.2), interruption table (Section 5.2) |
| P2 | Repair round at A2 and A3 to A5 (Section 6.1), family probe (Section 6.2), convergence measure (Section 3.4) |

## 2. Severity model

<!-- Source: Base (original, modified): FR-001 to FR-003 and FR-005 restructured per Change #3 (IR rules 1, 2, 4 and 33; INV-010, INV-012, INV-020, INV-041); B1 to B4 glossary names kept (S-003, C-002) -->
**FR-001 Three severities.** Every finding has exactly one severity, derived by the parent from the finding's checklist answers (FR-002 to FR-004), never read from the reviewer's wording:

| Severity | Definition |
|---|---|
| `blocking` | At least one checklist answer of FR-002 is `yes` and its anchor passed the parent's Read-back (FR-003), and the inherited cap of FR-011 does not apply. |
| `minor` | All four answers are `no`, and the finding is a real defect in what this task delivered: ambiguous wording, a missing or mismatched evidence entry for a claim the reviewer verified true. |
| `note` | All four answers are `no`, and the finding is cosmetic, a "consider changing" suggestion, or has origin `inherited` or `late` (Section 3.2); also any finding whose only `yes` failed its Read-back. |

**FR-002 Four checklist answers; the blocking triggers.** Every finding carries four factual answers, each `yes` or `no`. Each answer is the confirmation of one blocking trigger, so the trigger names stay as a glossary:

| Answer | Trigger | `yes` when |
|---|---|---|
| `ac-outcome-missing` | B1 unmet AC | Output an AC requires is absent, or contradicts the AC text, or an evidence claim the reviewer could not verify has no evidence row (FR-005). |
| `false-claim` | B2 wrong statement | A claim in delivered text or code is false against live source, a recipe or instruction followed as written does not do what the text says it does, or a span an earlier review accepted is later shown false. |
| `harmful-effect` | B3 harmful effect | Code or a recipe added or changed by this task writes, appends, chmods or deletes tracked or production data, mutates state outside the task's declared outputs, or exposes a secret. |
| `quoted-constraint-breach` | B4 constraint breach | The diff violates a parent `## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable` item or an explicit task instruction (`P/refs/qa.md:13-17`), including editing text the plan reserves for another task, and the reviewer can quote that text. |

"Cannot verify" (formerly B5) is not a per-finding severity. It stays the existing `cannot-verify` step of the verdict order (`P/refs/qa.md:41-52`); an evidence claim the reviewer could not verify is `ac-outcome-missing=yes` anchored on the AC words (FR-005).

**FR-003 Who assigns severity.** The reviewer answers the four questions and cites one anchor per `yes`. The reviewer is a fresh subagent whenever a task could complete with findings (FR-030). The parent orchestrator then derives the severity mechanically and Reads each anchor back once:

- `ac-outcome-missing`: the quoted AC words are byte-present in the AC.
- `false-claim`: the cited live-source `path:line` holds the contradicting text.
- `harmful-effect`: the cited diff line is the write.
- `quoted-constraint-breach`: the quoted text is byte-present in the plan Constraints or a task instruction.

A finding whose only `yes` fails its Read-back is a note. The reviewer's prose label (low, IMPORTANT, MINOR or any other) is never read. There is no second model pass: `P/refs/qa.md:11` allows one reviewer per review, and the Read-back is a file check, not a judgment.

**FR-004 Derivation and vocabulary mapping.** Any confirmed `yes` gives `blocking`, except that a finding on inherited text is capped at note by the mechanical rule of FR-011. All `no` gives `minor`, or `note` when the finding is cosmetic or its origin is `inherited` or `late` (Section 3.2). Mapping of the words a reviewer might use: high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`. Example: the A2 reviewer labelled the data write "low" (`E/retries/T1/review-2.md:3`); its `harmful-effect=yes` is anchored on the diff line, so it is `blocking` (R-A2, Section 10.1).

<!-- Source: Variant 2 (sonnet:refactorer), FR-003 (V2:50): merged per Change #4, replacing base FR-004; base sentence on not widening the AC kept -->
**FR-005 Evidence-type AC.** For an AC that asks for evidence (for example T1.AC4, "claim matrix cites live source", `E/retries/T1/review-5.md:5`), the AC is unmet only when:

- the evidence artifact is absent (`ac-outcome-missing=yes`);
- a cited evidence row is false (`false-claim=yes`); or
- a claim the reviewer could not verify has no evidence row (`ac-outcome-missing=yes`, anchored on the AC words).

A claim the reviewer verified true but that lacks a row, and a saved script/output pair that does not match when the reviewer reproduced the claim itself, are all-`no` findings: `minor`. The reviewer may not widen the AC (for example from "each corrected behavior" to "every sentence asserting a fact", evidence mechanism 7). This keeps real evidence requirements and removes the paperwork trap.

<!-- Source: Base (original, modified): FR-006 kept; the B5 bullet reworded so it agrees with FR-002 (Change #6) -->
**FR-006 Mapping onto the closed verdict enum (unchanged).** The enum stays `compliant | missing | extra | misunderstood | cannot-verify` (`P/refs/qa.md:37`). Only the inputs to the order at `P/refs/qa.md:41-48` change:

- An AC is unmet only when a B1 or B2 finding is attached to it.
- `misunderstood` requires a B1 finding of the "contradicts" kind.
- `extra_scope` is non-empty only for B3 or B4 findings.
- An AC claim the reviewer cannot verify (formerly B5) gives `cannot-verify` through the existing order.
- `minor` and `note` findings never change the verdict. A review whose findings are all `minor` or `note` yields `compliant`, provided every met AC has a citation (unchanged rule, `P/refs/qa.md:48`).

<!-- Source: Base (original), FR-006, with appended sentences from SM C-005/X-024 and IR rule 28 (INV-029): merged per Change #6 -->
The reviewer produces the verdict by running today's order over blocking findings only. The orchestrator never rewrites a verdict. An empty diff whose AC are all met by a cited live-source `path:line` is `compliant`; an empty diff without such a citation stays `cannot-verify`.

<!-- Source: invariant-resolution.md IR rule 3 (INV-031): merged per Change #5 -->
**FR-007 Drive-by files.** A drive-by file not implied by the AC is blocking only when a confirmed `quoted-constraint-breach` or `harmful-effect` applies; otherwise it is a minor, stays in `files=` and goes to notes. This replaces the rule "Drive-by files not implied by the AC are `extra`" at `P/SKILL.md:118-119` (change surface, Section 9).

<!-- Source: Base (original, modified): FR-007 format block replaced per Change #7 (PV-FR-002 family=; PVE2 K-8; IR rules 1, 5, 22) -->
**FR-008 Review file format.** `review-<k>.md` (now also written for k = 1, FR-029) starts with one header line holding the task's `start` sha and the 40-hex of the reviewed tree (FR-012), then one finding per line:

```
F<k>.<j> sev=<blocking|minor|note> trigger=<B1|B2|B3|B4|none> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> first=<start|A<m>> origin=<inherited|late|fix-induced|new|unknown>: <text>
```

- The reviewer writes `ac=`, `at=`, `anchor=`, `chk=`, `family=` (short, reviewer-chosen, reused for findings of the same defect form), `fix=` and the text.
- The parent writes `sev=` and `trigger=` from `chk=` and the anchor Read-back (FR-003), and writes `first=` and `origin=` (FR-010). The reviewer never writes these four keys.
- The base `fix=local|nonlocal` key is dropped: locality is decided by the parent (FR-024).

It also holds one status line per prior blocking finding: `F<m>.<j> resolved|open|regressed`. This file is not in the ledger, so no regex parses it and the new keys are grammar-safe.

<!-- Source: Base (original, modified): FR-008 renumbered FR-009; example line replaced per Change #8 -->
**FR-009 Ledger lines (no regex change).** A task that completes with open `minor`/`note` findings writes the existing verdict line with `complete verdict=compliant`, plus one evidence token that points at its notes file:

```
T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3,T1.AC4 evidence=T1.AC1@<path:line>,T1.AC2@<path:line>,T1.AC3@<path:line>,T1.AC4@<path:line>,notes@.dev/implement/03-memory-docs-f5865990/retries/T1/notes.md:1-<m> extras=lint:skip,typecheck:skip,test:skip files=docs/user-guide/memory-system.md,docs/memory/README.md
```

<!-- Source: Variant 3 (haiku:qa), FR-018 and Section 9 (V3:159-161): example corrected per Change #8 (base defect X-017); typed token convention of the base kept (C-008) -->
The example cites all four AC, as FR-006 requires. There is one token convention: the typed `notes@<path>:<a>-<b>` token inside `evidence=`, never an AC citation. No field may follow `files=` (negative test, Section 9).

Checked against the verdict regex (`P/refs/ledger.md:56`, `P/scripts/archive_workspace.py:49-53`): `ac=([^ ]+)` takes the comma list with no spaces; `evidence=(.+)` runs to ` extras=lint:`, so the `notes@` token is inside it; `files=(.+)$` stays last and unchanged, so the greedy `files=` problem does not arise. The helper reads only `files=` from verdict lines (`archive_workspace.py:388-400`) and accepts a `compliant` complete line with no Ruling (`:373-374`). Managed packages write `notes@./artifacts/retries/T<id>/notes.md:<a>-<b>` (package-relative, `P/refs/ledger.md:223`). A `notes@` token is never an AC citation, so it never satisfies `P/refs/qa.md:27-33`.

## 3. Attempt-based convergence rules

<!-- Source: Variant 2 (sonnet:refactorer), Section 3 opening (V2:87): merged per Change #1, replacing the base opening paragraph -->
### 3.1 Attempts

An attempt is a ladder row, A1 to A5 (`P/refs/retry.md:7-14`), numbered as the k rule numbers them (`P/refs/retry.md:30`), so `review=3` means A3. It is not "the third review": a repair re-review sits inside the attempt it repairs. "By the 3rd attempt" therefore means no later than the review that closes A3. This design gives a stronger guarantee: a `minor` or `note` finding never fails any attempt (FR-006), and the T1 replay completes inside A2 (Section 10.2).

<!-- Source: seed-brief Addendum 1 (SB:79-95); IR rules 5 and 8 (INV-001, INV-003); PV-FR-008, PV-FR-011; Variant 2 FR-011 covers= escape (V2:105); base FR-010 inherited cap (V1:76) moved here: merged per Change #9 -->
### 3.2 Finding origin and first-seen attempt

In run `E` most later findings were late discoveries, a minority were fix-induced, and two were inherited (SB:85-95). The three origins are handled differently, so each finding records where its text came from.

**FR-010 `first=` and `origin=`.** For every finding the parent, never the reviewer, writes two fields into the review file, from exact line text:

- `first=<start|A<m>>`: the earliest pinned reviewed tree of this `start` (FR-012) that holds the flagged text, or `start` when `$start` holds it.
- `origin=`:
  - `inherited`: the text is present in `$start`.
  - `late`: the text is present in an earlier reviewed tree of the current chain and was not flagged there. `late` takes precedence over `fix-induced`.
  - `fix-induced`: the text first appears in a tree written by an in-place fix (the A2 fix pass or a repair) after a review.
  - `new`: the first review of the chain, or text of a tree rebuilt from Q0 by an adviser brief, which starts a new chain.
  - `unknown`: `$start` is not a tree (HEAD fallback or `nogit`, `P/SKILL.md:115`), or a recorded tree is missing.

**FR-011 Handling by origin.**

| Origin | Defined by (parent, exact line text) | Blocking finding | Non-blocking finding |
|---|---|---|---|
| `inherited` | text present in `$start` | capped at note, mechanically from the `git diff "$start"` hunk headers, unless a quoted AC clause or constraint covers it or a task-added sentence depends on it (`covers=`) | note |
| `late` | present in an earlier reviewed tree of the current chain and not flagged there | blocks at every attempt; never capped; never a regression (FR-014) | note |
| `fix-induced` | first present in a tree written by an in-place fix after a review | blocks, and is a regression only on an in-place-fix tree; sends the next step to the adviser route (FR-027) | minor, recorded; not edited from A3 (FR-025) |
| `new` | first review of the chain, or text of a Q0-rebuilt tree | blocks | minor or note per FR-004 |
| `unknown` | `$start` not a tree, or a recorded tree missing | no origin rule applies; severity stands as derived | as derived |

A `fix-induced` blocker counts as a regression only on a tree produced by an in-place fix; text of a Q0-rebuilt tree is `new` and is never a regression. With no usable baseline (`unknown`) there is no inherited cap. Example of the inherited cap: the `chmod 644` recipe at `docs/memory/README.md:208` is "in HEAD unchanged" (`E/retries/T1/review-5.md:9`); the tar recipe at `:119` is inherited by the Addendum 1 grep of the saved diffs (SB:92). The fixture expectation for the seven Addendum 1 findings is in Section 11.

<!-- Source: IR rule 6 (INV-002) and IR rule 9 (INV-005); PV-FR-007 as amended by INV-002; PVE2 K-11: merged per Change #10 -->
**FR-012 Pinned reviewed trees and the `start` header.** Origin needs every reviewed tree, including A1's and each repair's, and a repair writes no `step=open` checkpoint (FR-024).

- Each reviewed tree is pinned as `refs/superclaude/implement/<slug>/retry/T<rid>/r<k>-<j>`, and its 40-hex is written on the header line of that review file (FR-008).
- On any resume the ref is re-pinned from the recorded sha.
- At `complete`, after `first=` and `origin=` are written, these refs are deleted with the checkpoint refs.
- Every file the new rules read (`review-*.md`, `repair-*.md`, `probe-*.md`, the notes file) holds the task's `start` sha on its first line; a file holding any other value counts as absent.

<!-- Source: Base (original, modified): FR-011 and FR-012 replaced per Change #11 (SM C-012, C-013; IR rule 10; PV-FR-006, PV-FR-015; Addendum 2 reviewer-standard drift) -->
### 3.3 What each review may raise

**FR-013 What each review may raise.** Every review at every attempt may raise a new blocker (any confirmed checklist `yes`) anywhere in task-owned text, meaning text the task added or changed; text present in `$start` follows the inherited rule of FR-011. A blocker on task-owned text is never capped, whatever its origin or attempt. Only new minors, notes and "cannot verify" findings with no confirmed `yes` on text unchanged since the last pinned reviewed tree (FR-012) are capped at note, so later reviews cannot re-open accepted text with a lower-severity finding. Minors and notes never fail an attempt (FR-006).

| Review of | Scope of audit | Prior-finding re-check | Fails the attempt |
|---|---|---|---|
| A1 | Full audit of the diff | none | a confirmed blocker only |
| A2 and each repair re-review | Full audit, plus the delta diff from the previous pinned reviewed tree as context (PV-FR-015) | each prior blocking finding marked `resolved`, `open` or `regressed` (FR-029); the saved-probe re-check list (FR-026) | a confirmed blocker only |
| A3 | as A2 | as A2 | a confirmed blocker only |
| A4 | as A2 | as A2 | a confirmed blocker only |
| A5 | as A2 | as A2 | a confirmed blocker only |

A non-blocking `late` finding is a note (FR-011). A finding whose flagged text is absent from the current tree is `resolved` in the re-check, is not carried to notes, and keeps its recorded `first=` and `origin=`.

<!-- Source: seed-brief Addendum 2 (SB:97-99); IR rules 7 and 34 (INV-033, INV-043); PV-FR-009, PV-FR-010 as amended by INV-033; PVE2 K-12: merged per Change #12 -->
### 3.4 Convergence measure

**FR-014 Progress is counted in open blocking families.** Progress is measured by the distinct open blocking families (`family=`, FR-008). Minor, note and total finding counts are never read by any route, halt or prompt decision.

- An in-place fix (the A2 fix pass or a repair) has failed when any family it targeted is still `open` or `regressed`, or the next review has a `fix-induced` blocker.
- After a failed in-place fix the next step is the existing adviser route (FR-027); no further repair runs in that attempt, and no halt reason is added.
- `late` and `new` blockers are not regressions.
- Regressions are listed first, verbatim, in the next fixer or adviser input.

The rf-qa `[HALT-MONOTONICITY]` count halt is not imported: a count halt would add the user interrupts that Addendum 3 forbids.

## 4. Role of /ponytail-review

<!-- Source: Base (original), Section 4 opening paragraphs, kept per Change #13 -->
**Why it cannot assign severity.** `ponytail-review` covers over-engineering only and says "Correctness bugs, security holes, and performance are explicitly out of scope" (`/config/.claude/plugins/marketplaces/ponytail/skills/ponytail-review/SKILL.md:52-53`). Concrete failure: run over the A2 diff, it sees a short, plain snippet and returns `Lean already. Ship.` (`:48`). It cannot know that `docs/memory/solutions_learned.jsonl` is tracked production data (`E/retries/T1/review-2.md:12`). Used as the severity filter, it would pass the B3 blocker that R-A2 requires to block.

**What it is good for: fix cost against value.** Its tags `delete:`, `yagni:` and `shrink:` (`SKILL.md:23-27`) answer a different question: is the proposed fix worth its lines?

<!-- Source: Variant 2 (sonnet:refactorer), FR-014 and FR-015 (V2:123-125); Variant 3 (haiku:qa), Section 4 "Failure that must not happen" (V3:92); PVE2 K-3: merged per Change #13, replacing base FR-014 and FR-015 -->
**FR-015 The lens is embedded in `refs/qa.md`; no runtime call.** The fix-cost question ("is the fix worth its lines") is embedded in `refs/qa.md` as part of the `fix=` field of every finding (FR-008). Over-engineering observations are notes. The protocol never invokes the `ponytail-review` plugin, so its absence changes nothing; a plugin in a marketplace cannot be relied on in another project.

**FR-016 Guards.** A ponytail-style judgment:

- never changes a checklist answer, so it never changes a severity or a verdict;
- never deletes or shrinks text an AC requires (for example, a `delete` on the claim matrix would drop T1.AC4's evidence artifact);
- never reduces the set of sites a family probe listed (FR-026); it may pick the smaller fix per listed site.

**What must change elsewhere.** Nothing in the ponytail plugin. Cost: zero spawns.

## 5. Caps, interruption policy and the accepted-minor path

<!-- Source: Base (original, modified): FR-016 caps table replaced per Change #14 (Variant 3 FR-011, V3:100-105; Variant 2 FR-018, V2:133-143; IR rule 16, INV-026); NFR-001 kept -->
### 5.1 Caps

**FR-017 Hard caps per task.**

| Cap | Value | Justification |
|---|---|---|
| Attempts | 5 (A1-A5, unchanged) | Keeps `review=[2-5]` and the k rule (`P/refs/ledger.md:98`, `P/refs/retry.md:30`). Severity, not more attempts, fixes the loop. |
| Repairs | at most 1 per attempt, except the second A2 repair of FR-024; at most 2 per task; counted as `repair-<k>-<j>.md` files | A repair that fails shows the defect is not local, so the adviser route takes over (FR-027). Counting files makes a resume give the same answer. |
| Reverts | at most 3, and only on the adviser route | A repair never reverts. Run `E` wrote 3 `step=revert` records (`E/progress.md:5,9,13`); the evidence file's fourth revert is UNVERIFIED. |
| Adviser spawns | at most 6 (unchanged, `P/refs/retry.md:144`) | Advisers are reached only for blockers (FR-027). |
| Tasks entering the ladder per run | `RETRY_BUDGET = 8` (unchanged, `P/refs/retry.md:53`) | A repair writes no `step=open` record, so it does not spend a budget slot. The test-pinned sentence (`tests/skills/test_task_workspace_lifecycle.py:532-536`) stays byte-identical. |

Sentence for `Cost and caps` in `P/refs/retry.md`: the review ceiling per task is 5 ladder reviews plus at most 2 repair re-reviews, one respawn per review, one Row V re-review per crash and one operator review per resume after a halt, counted, not measured.

**NFR-001 No token cap.** Token use is not written to the ledger or any retry file. A token gate could not be recomputed on resume, and resume must dispatch from the ledger alone (`P/refs/ledger.md:136`). Run `E` cost about 160,000 tokens per review (evidence section 2), so the attempt and spawn caps above already bound the worst case. Without severity, minors forced extra reviews. With it, they no longer can. UNVERIFIED: that the delta-diff context (FR-013) makes later reviews cheaper; every review is still a full audit.

<!-- Source: seed-brief Addendum 3 (SB:101-103); IR rules 4, 19 and 35 (INV-020); PV-FR-001, PV-FR-017, PV-FR-018; PVE2 Section 4 pick M9.1: merged per Change #15 -->
### 5.2 Interruption table per attempt

**FR-018 Which severities may interrupt.** The user asked that after the 2nd or 3rd round nothing below high priority prompts the user, and that no automation is interrupted for low or low-medium issues (SB:103). This spec applies that gate from A1, which is stronger; the user confirmed on 2026-10-24 that the gate starts at attempt 1:

| Attempt | May fail the attempt | May halt | May prompt the user | Minors may be edited |
|---|---|---|---|---|
| A1 | `blocking` only | `blocking` only (in practice never: an A1 failure goes to the A2 fix pass) | `blocking` only (in practice never) | only inside lines already changed for a blocker |
| A2 with repairs 1 and 2 | `blocking` only | `blocking` only | `blocking` only | only inside lines already changed for a blocker |
| A3 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |
| A4 | `blocking` only | `blocking` only | `blocking` only | no, recorded only |
| A5 | `blocking` only | `blocking` only (`ladder-end`) | `blocking` only | no, recorded only |
| legacy FINAL | `blocking` only, advisory (never reopens a task) | never | never (summary only) | no |
| managed FINAL | `blocking` only (`issues`) | `blocking` only (`E-ARCHIVE-BLOCKED`) | `blocking` only | no |

Mapping (FR-004): high = any confirmed checklist `yes` = `blocking`; medium, IMPORTANT without a `yes`, low-medium, low and cosmetic = `minor` or `note`. Every minor and note is recorded in the notes file and cleared: no halt, no Ruling, no user prompt, at every row. "Cleared" means recorded and closed, not necessarily edited. The FINAL still runs. The only non-finding interrupts are the STOP rows of `P/SKILL.md:26-42` (Section 5.3).

<!-- Source: IR rules 29 and 36 (INV-021, INV-042); PV-FR-018; live STOP table P/SKILL.md:26-42; live halt reason table P/refs/retry.md:394-408: merged per Change #16 -->
### 5.3 Remaining paths that can stop or prompt

**FR-019 Closed list of interrupts.** Each line names the path, when it fires and why it stays.

1. `E-HALT-QA` after a ladder halt (`ladder-end`, `advice-rejected`, `no-runner-up`, `brief-invalid`, `budget`, `batch`, `no-snapshot`, `head-moved`, `no-evidence`): reachable only after an attempt failed on a confirmed blocker that a repair could not close. Kept because a real failure must block (SB:55) and the revert guards protect data. The halt message and any Ruling request list blocking findings only.
2. `dispute` halt: only when the adviser disputes a blocking finding or the AC itself (FR-027). Kept because a disputed AC is a user decision.
3. `E-NO-RULING`: reachable only when someone tries to continue past a non-compliant verdict, which now exists only with a blocker. Kept as the user-acceptance safety gate.
4. `operator-review`: user-initiated after a halt, never started by automation.
5. `E-RESUME-NEEDED` (`reviewer-down` after a second paperwork-only or unparseable review, `ref-failed` including a notes file that cannot be written, incomplete revert, adviser agent missing): infrastructure, never about a finding; it asks the user to re-run, not to fix anything. Kept because continuing would record an unverified completion or risk data loss.
6. Input and integrity STOPs (`E-NO-SOURCE`, `E-SOURCE-MISSING`, `E-NO-TASKS`, `E-NO-AC`, `E-LEGACY`, `E-LEDGER-CORRUPT`, `E-LEDGER-PATH`, `E-MANAGED-INVALID`, `E-MANAGED-CONFLICT`, `E-PLAN-CHANGED`, `E-ARCHIVE-MARKER`): occur before or outside per-task QA. Kept unchanged.
7. `E-ARCHIVE-BLOCKED` (managed): FINAL `issues` naming a blocking defect at the end state (FR-023), `--skip-final-review` on a managed package, or a helper refusal. Kept because FINAL is never waived (SB:56).

No other path may stop automation or prompt the user. A minors-only replay writes no `halt` and no `Ruling:` line (static check, Section 11).

<!-- Source: Base (original, modified): FR-009 moved from Section 2 and "append-only" replaced per Change #17 (IR rule 13, INV-006, INV-018; Variant 3 FR-012, V3:107) -->
### 5.4 Notes file and accepted-minor path

**FR-020 Notes file.** The file is `<retries>/T<id>/notes.md`. Line 1 holds the task's `start` sha (FR-012); then one line per recorded finding: `A<k> F<k>.<j> <minor|note> <path:line> <checklist answers> <text>`.

- It is rewritten, not appended, at `complete`, from the minors and notes of the review that produced `compliant` plus any capped finding of that same tree. Findings of reverted or superseded trees stay only in their review files.
- The folder already exists for every tree-snapshot task, because Q0 writes `q0-head` there (`P/SKILL.md:114`). The revert domain excludes `<retries>` (`P/refs/retry.md:155`), so notes survive any revert. A task whose start is `nogit` or a HEAD fallback has no `q0-head`; it creates the folder when it first writes the file.
- Fail closed: if the file cannot be written, STOP `E-RESUME-NEEDED reason=ref-failed`, with no ledger line and no `blocked` line.
- A review with no minors and no notes writes no notes file and no `notes@` token.

<!-- Source: Base (original, modified): FR-017 renumbered FR-021 and its references updated; appended paragraph per Change #18 -->
**FR-021 Automatic accepted-minor path.** When a review has no `blocking` finding, the orchestrator does three things and asks the user nothing:

1. Write the notes file (FR-020).
2. Run Q6 extras.
3. Append the `complete verdict=compliant … notes@…` line (FR-009).

How it differs from the Ruling:

| | Accepted-minor | Ruling (`P/refs/qa.md:62-72`) |
|---|---|---|
| Who decides | Severity derived by the parent from the reviewer's checklist answers and anchors (FR-003), plus the mechanical origin caps (FR-011) | The user, in the current conversation |
| Covers | `minor` and `note` only | Any explained gap, blockers included |
| Ledger | `compliant` verdict plus a `notes@` token | A `Ruling:` line, then `complete` with the unchanged non-compliant verdict |
| Writes a `Ruling:` line | Never | Always |

The Ruling path is unchanged and remains the only exit from a halt.

<!-- Source: IR rule 14 (INV-011); IR rule 21 (INV-009); Variant 3 (haiku:qa), Section 6 last paragraph (V3:130): merged per Change #18 -->
Conditions on the accepted-minor path:

- A task completes with recorded minors only after a fresh subagent review (FR-030).
- When no FINAL that can block will run (legacy N=1, legacy `--skip-final-review`, or any legacy run, whose FINAL is advisory), the run's final summary prints every recorded minor with its checklist answers. The summary is informational and never asks the user anything.
- A batch task whose A2 has only minor or note findings completes on this path instead of halting `batch`. A batch A2 with a confirmed blocker still halts `batch`.

<!-- Source: Base (original, modified): FR-018 kept and renumbered FR-022; FR-019 replaced by FR-023 per Change #19 (IR rule 15, INV-013; PV-FR-022; SM A-002) -->
### 5.5 FINAL is never waived

**FR-022 Proof that FINAL is never waived.**

1. The legacy FINAL trigger is "after the last task is `complete`, when N>1 and not `--skip-final-review`" (`P/SKILL.md:155`; `P/refs/ledger.md:129`). It depends on task status, not on the verdict value. The accepted-minor path writes an ordinary `complete` line, so the trigger is unchanged. For N=1 there is no legacy FINAL today; that is existing behaviour, not a waiver.
2. The managed archive gate runs "every attempt (N=1, resume, retry; an earlier FINAL never counts)" (`P/refs/managed-workspace.md:49`). The helper refuses to archive unless the latest FINAL is `pass` and bound to the current state digest (`P/scripts/archive_workspace.py:66`, `:427`). The accepted-minor path writes no `FINAL:` or `ARCHIVE:` line.
3. Both FINALs already read every file in `<retries>/T<id>/` (`P/SKILL.md:155`, `P/refs/qa.md:82`), so they read the notes file, and they read the probe and review files too.

**FR-023 FINAL applies the same derived test.** The managed FINAL reads the notes, probe and review files, applies the FR-002 to FR-004 test with the FR-003 anchor Read-back to the end state, and returns `issues` only for a blocking defect. A notes entry whose answers are all `no` is cited `noted` and is not an unmet AC; a notes entry with a confirmed `yes` is `issues` even if it is listed as minor. Minors never make a FINAL `issues`. The legacy FINAL applies the same test and stays advisory.

Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `--skip-final-review` runs get no FINAL re-check of the notes. The primary gate against a misgraded finding is the mechanical derivation and the anchor Read-back (FR-003); for those runs the final summary prints every recorded minor (FR-021).

## 6. Fix in place; advisers only for blockers

<!-- Source: Variant 2 (sonnet:refactorer), FR-024 and FR-025 (V2:173-180) mechanism at Variant 3 (haiku:qa), FR-013 and FR-014 (V3:122-128) timing; Variant 2 FR-010 locality (V2:103); IR rules 11, 12, 20 and 25 (INV-025, INV-040, INV-036, INV-007): merged per Change #20, replacing base FR-020, FR-021, FR-023 and FR-024 -->
### 6.1 Repair round

**FR-024 Repair round.** The text lives in an H3 "Repair round" under the existing "## Escalation procedure" heading of `P/refs/retry.md`, so the eight pinned H2 headings stay (`tests/skills/test_task_workspace_lifecycle.py:518-527`).

1. **Locality predicate**, decided by the parent before the fixer runs. The open blocking set is local when it has at most 5 blocking families (`family=`) and at most 2 files named by finding lines. Probe-listed hits inside touched or AC-named files are in scope and are not counted again; a hit outside that scope is listed with a one-line reason and not edited. A family whose probe is missing or incomplete is non-local (FR-026). A missing required outcome (`ac-outcome-missing=yes`) is non-local.
2. **Repair.** After a failed review of attempt k, if the set is local and the caps allow (FR-017), the parent writes `repair-<k>-<j>.md` (line 1 the `start` sha; then the blocking findings it applies, verbatim from `review-<k>.md`; then its tree pin). The fixer applies the blocker fixes plus probe-listed sibling and coupled lines only. A fresh subagent re-reviews. No ledger line, no checkpoint, no revert, no adviser.
3. **A2 timing.** An A2 repair runs after the A2 review and before procedure step 0, with no `blocked` line first, so Resume row P stays unreachable. A second A2 repair is allowed when the first did not fail (FR-014), every new blocker is `late`, the set passes the predicate, and the 2-per-task cap is not spent.
4. **File naming.** `review-<k>.md` is the last review of attempt k; no `review-<k>-pre.md` is written. Adviser citations, the adviser pick and the brief-5 lessons check read `review-<k>.md` only.
5. **Resume.** Row S of `P/refs/ledger.md:158` becomes: "Start line only: if a `repair-2-<j>.md` for the current `start` exists, re-run only the re-review of the highest j (fresh subagent); else A1, as today." A repair is spent once its file exists; there is no `state=` field. A3 to A5 repairs resume through Row V, whose last record is still `retry n=<n> step=review`.
6. **Advisers and revert** run only when a blocker is still open after A2 and the set is non-local, or its repair failed (FR-027).

<!-- Source: IR rule 19 (INV-020); Variant 2 FR-023 (V2:171); PV-FR-017 narrowed; PVE2 K-4: merged per Change #21 -->
**FR-025 Minors are never the reason for a fix.** At A1 and A2 a fixer may edit a minor only inside lines it is already changing for a blocker; from A3 minors are recorded only. Minors are never the reason for a fix pass, a repair or a review. Reason: fix edits made 31% of PVE2's later findings (PVE2 K-4), and from A3 no review is spent on minors to catch such edits.

<!-- Source: seed-brief Addendum 2 (SB:99); IR rules 17 and 18 (INV-032, INV-034); PV-FR-003 to PV-FR-006, PV-FR-019; PVE2 K-1, K-2: merged per Change #22 -->
### 6.2 Family probe

**FR-026 Fix the pattern, not only the named instances.** Before any fix of a blocker (A2 fix pass, repair, brief run) the fixer writes `probe-<k>.md` (line 1 the `start` sha). Per blocking family it holds:

- the defect form;
- one read-only search command;
- its before-output and after-output over the touched files plus the files the AC names;
- the coupled sites: other lines in that scope that state or depend on the rule being fixed.

Rules:

- Edits to probe-listed sibling and coupled lines are in scope; any other edit is extra scope.
- A missing or incomplete probe never stops the run: it makes that family non-local (FR-024) and becomes a reviewer re-check item.
- A probe command is one `grep -nE`, `rg -n` or `git grep -n` with literal arguments over the probe scope, checked by the parent before it runs.
- The orchestrator re-runs every saved probe before each later review and passes only hit locations to the reviewer as a re-check list, never as evidence that an AC is met.
- A fix that inserts the same block of 3 or more lines in 3 or more places adds a byte-equality probe naming one source copy.

<!-- Source: IR rules 7, 26 and 27 (INV-033, INV-014, INV-015, INV-016); PV-FR-009, PV-FR-016; Variant 3 FR-014 (V3:128): merged per Change #23, replacing the escalation-number rule of base FR-022 -->
### 6.3 Failed fix and the adviser route

**FR-027 Adviser route.** When an in-place fix has failed (FR-014) or the open blocking set is non-local (FR-024), today's escalation procedure runs unchanged, with these amendments:

- Advisers and fixers receive the finding lines verbatim, never a paraphrase, with regressions first.
- A `dispute` halts only when it names a blocking finding of `review-<k>.md` or the AC itself. A dispute of a minor or note is recorded in the notes file, and the answer is treated as `ready` for the parent check.
- In escalation 3, "failure finding" means a blocking finding of `review-4.md`; minors and notes need no `lessons from A4:` line.
- The escalation-2 pick counts distinct blocking findings of `review-<k>.md` only.

Every halt value used is already in the table at `P/refs/retry.md:394-408`, so the 22-line `halt-examples` block is unchanged. The pinned pick lines stay byte-identical, except the single-adviser form that FR-036 retires.

<!-- Source: seed-brief Addendum 4 (user requirement, 2026-10-24): added after the merge -->
### 6.4 Escalation 1: two parallel advisers from different model families

**FR-034 Two advisers at escalation 1.** The first adviser escalation (after A2 fails with a blocker the repair round could not close; it writes brief 3, `P/refs/retry.md:11`) always spawns two advisers in one message, never one. This replaces today's "1 adviser one rung up" for every executor tier.

- `advice-3-a.md`: the executor's own model family, one rung up the active ladder (today's rule). It uses the top rung when the executor is already on the top rung or its tier is unknown.
- `advice-3-b.md`: the other model family. The family is read from the model id with any trailing `[...]` stripped: a `claude-` prefix is Claude, a `gpt-` prefix is GPT.
  - Executor is Claude: adviser B is a GPT model on T1, meaning the id of `T1_Model01`, else `T1_Model02`, that starts with `gpt-`.
  - Executor is GPT: adviser B is the Claude top rung (`opus` when it resolves to a `claude-` id).
  - Executor is neither family or unknown: adviser A uses the top rung, and adviser B uses whichever of the Claude top rung and the GPT T1 model is not adviser A's family.
- Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model (`T1_Model01` when the executor is not already on it, else `T1_Model02`, else the same T1 model).
- The two advisers share no state and neither has Write, as today (`P/refs/retry.md:72`).
- The pick uses the existing two-answer rule and pick line: the answer citing more distinct blocking findings of `review-2.md` wins, and a tie goes to `-a` (`P/refs/retry.md:85`, FR-027). One passing answer and the critique round keep their existing forms; the critique adviser uses adviser A's model.

**FR-035 Resolving and spawning the cross-family model.** Before spawning, the parent resolves adviser B's model id and writes it on the first line of `advice-3-b.md`: `model: <id> family: <claude|gpt> rung: <T1|top>`.

- The Agent `model` parameter in this harness takes aliases (`opus`, `sonnet`, `haiku`, `fable`). Whether it also accepts a full model id is UNVERIFIED. The implementation must first verify one spawn path for a GPT T1 id and pin it with a test: either an alias that `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` maps to that id, or a full-id `model` value.
- Fallback when no model of the other family can be reached: spawn adviser B on the strongest reachable model, write `family-fallback: <reason>` on its header line, and list the fallback in the run's final summary. Never STOP and never prompt the user for this (FR-018, FR-019): a missing model is configuration, not a finding.
- Facts on this host, 2026-10-24: no `T*_Model*` variable is set, so the fallback ladder is active. The aliases resolve `opus` to `claude-opus-5-5`, `sonnet` to `claude-sonnet-5-5` and `haiku` to `grok-4.7`, and `ANTHROPIC_MODEL=gpt-6.1-sol`. No alias reaches a GPT model, so FR-034 would take the fallback here until a GPT T1 model is configured.

**FR-036 What stays and what moves.**

- Unchanged: escalation 2 (two advisers on the top rung), escalation 3, the `tier=` record, `RETRY_BUDGET = 8` and the 6-spawn adviser cap. Escalation 1 now always spawns 2, plus at most 1 critique.
- The `Cost and caps` sentence (`P/refs/retry.md:144`) changes from "escalation 1 adds 1 adviser spawn (2 when the executor is known to be on the top rung)" to "escalation 1 adds 2 adviser spawns, one from each model family".
- The Model ladder escalation rule and its worked example (`P/refs/retry.md:131-138`) gain an adviser-B column. Deliberate pin moves: `tests/skills/test_task_workspace_lifecycle.py:587-590` (worked-example rows) and `:572` (the `single adviser` pick line, retired because escalation 1 no longer spawns one adviser).
- Not extended: cross-family advisers at escalation 2 were not requested.

## 7. Reviewer contract is closed

<!-- Source: Base (original, modified): Section 7 reordered by Changes #24 to #26 -->
<!-- Source: Base (original, modified): FR-025 renumbered FR-028; slot list amended to seven and quota ban added per Change #25 (IR rules 22 and 24; PV-FR-012, PV-FR-013, PV-FR-015; PVE2 K-7) -->
**FR-028 Closed prompt.** `P/refs/qa.md` holds the reviewer prompt as one fenced template with exactly seven named slots and no others: `{task_brief}`, `{global_constraints}`, `{diff}`, `{start_sha}`, `{prior_findings}`, `{delta_diff}`, `{recheck_list}`. The four checklist questions (FR-002), the anchor rule (FR-003) and the finding-line format (FR-008) are fixed text inside the template. The orchestrator fills only those slots from the sources the protocol names. It may not add, remove or reword any criterion, whether it comes from an output style, the session, or its own judgment. The template contains no finding quota ("find at least N issues" or similar). Run `E`'s "zero defects of any severity" and "every sentence asserting a fact needs a matrix row" (evidence mechanism 7) are exactly what this forbids. Inline reviews (`P/SKILL.md:101`) use the same template text.

Reviewer-standard drift (Addendum 2) is controlled by four rules together: this closed template with no quota; the same derived test at every attempt and at FINAL (FR-004, FR-023); the cap on lower-severity findings on accepted text (FR-013); and `late` non-blocking findings as notes (FR-011).

<!-- Source: Base (original, modified): FR-013 moved from Section 3, renumbered FR-029, limited to blocking findings per Change #25 (IR rules 22 and 24; INV-008, INV-004) -->
**FR-029 Prior findings without breaking isolation.** Reviewers still never read retry folders (`P/refs/qa.md:90`).

- **A1 failure record.** When A1 fails, the orchestrator writes `<retries>/T<id>/review-1.md` with its `start=` and tree header (FR-008), pins the `r1-1` tree (FR-012) and keeps the A1 notes. It writes no ledger line, because the ladder writes none after A1 (`P/refs/retry.md:30`). Today the A1 review is lost (evidence section 2). This record is specified in `refs/qa.md`, which is loaded at Q3, not in `refs/retry.md`.
- **`{prior_findings}`** holds, byte for byte, the earlier blocking findings of this `start` only, never minors or notes. The reviewer marks each `resolved`, `open` or `regressed` from the diff before listing new findings, and never cites the slot or its source file. `P/refs/qa.md:90` exempts the slot from the forbidden-read rule and keeps the citation ban.
- **`{delta_diff}`** holds `git diff <previous pinned reviewed tree> -- <touched files>` from A2 on, as context beside the full diff.
- **`{recheck_list}`** holds the hit locations of the re-run saved probes (FR-026).

These are reviewer outputs and parent-run searches, not implementer claims or adviser text, so the rule "Do not trust the implementer's report" (`P/refs/qa.md:7`) is not weakened. Paraphrase is forbidden.

<!-- Source: IR rule 21 (INV-009): merged per Change #24 -->
**FR-030 Inline reviews may not complete a task with findings.** `P/SKILL.md:101` lets the first in-flow review of A1 or A2 run inline in the executor's session. An inline review may return only `compliant` with zero findings, or a non-compliant verdict. An inline review that would complete a task with any minor or note is discarded and re-run once as a fresh Task subagent with the closed template and a saved `prompt-<k>.md`. Every repair re-review is a fresh subagent. Reason: an inline reviewer that passes its own session's minors would be the producing context grading itself.

<!-- Source: Base (original, modified): FR-026 renumbered FR-031; layer 1 kept; layer 2 (reviewer self-report) replaced per Change #26 (IR rule 23, INV-017; SM C-026) -->
**FR-031 Detection and paperwork-only reviews.**

1. The orchestrator saves the exact prompt it sent as `<retries>/T<id>/prompt-<k>.md`. The managed FINAL (`P/refs/qa.md:82`) and the legacy FINAL already read that folder. They compare the prompt with the template and return `issues` (managed) or record it in `FINAL:` evidence (legacy) when the two differ outside the slots.
2. A review whose only failure is reviewer paperwork (a missing, bare or malformed citation for an AC it marked met, or a missing or unparseable checklist answer) is unparseable: respawn once with the same input; a second such review is `E-RESUME-NEEDED reason=reviewer-down` (`P/refs/retry.md:447`). It never fails the attempt and never starts the ladder. An anchorless `yes` is handled by FR-003: a failed anchor Read-back makes the finding a note. The base's reviewer self-report layer (`contract-breach:` lines) is dropped; the saved prompt stays as the audit trail.

**NFR-002** No executable check can prove what a prompt contained. The saved-prompt comparison is protocol-level, so the enforcement map (`P/refs/managed-workspace.md:81-86`) gains one "protocol" row and makes no executable claim.

<!-- Source: Base (original, modified): Section 8 kept; line citations qualified per base defect X-027 and IR rule 29 appended per Change #27; PVE2 K-13 -->
## 8. Output-style conflict decision

The conflicting rule is in the `pragmatic` output style (`pragmatic.md`): "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict; a 'minor issues still pass' allowance is PROHIBITED." It is at line 212 of the installed copy `/config/.claude/output-styles/pragmatic.md` and line 225 of the source copy `src/superclaude/output-styles/pragmatic.md` (the copies are offset by 13 lines).

**Decision: inside `/sc:implement`, the protocol's severity model wins, for per-task QA and for both FINALs. Everywhere else, `pragmatic.md` wins unchanged.**

| Gate | Rule that applies | Which wins | Effect |
|---|---|---|---|
| Per-task QA (A1 to A5 and every repair re-review) | FR-006: only `blocking` fails | protocol | Minors pass as notes |
| Legacy FINAL and managed archive FINAL | Binary `pass`/`issues` (already binary, so it matches the style's "binary verdict" rule, installed `pragmatic.md:211`, source `:224`); `issues` only for a blocking defect at the end state, including a misgraded note (FR-023) | protocol | A recorded minor is not `issues` |
| Every other review, including work outside a protocol that defines its own gate | The `pragmatic.md` any-severity rule, unchanged | `pragmatic.md` | Unchanged |

**Reasoning.**

1. The protocol's gate is specific; an output style is general session behaviour. The specific rule governs its own gate.
2. The user explicitly requires minors to pass with notes (evidence section 5), and that requirement is more recent and more specific than the style.
3. Applying the style at FINAL would re-create the loop one level up: a managed package would archive-block on paperwork.
4. The parts of the style that improve review quality stay in force: adversarial stance, Self-Audit on zero findings, and a fresh context (installed `pragmatic.md:206-209`, source `:219-222`). Nothing is passed silently, because every minor is written to the notes file and the ledger points at it.

**FR-032 Precedence stated in the protocol.** `P/refs/qa.md` states this precedence in the reviewer template (FR-028). Every halt message and Ruling request lists blocking findings only, and at every attempt only blocking findings may fail an attempt, halt or prompt the user (FR-018).

**FR-033 Carve-out clause in the style.** In the source copy `src/superclaude/output-styles/pragmatic.md:225`, add the clause "except inside a protocol that defines its own severity model, such as `/sc:implement` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`)". The clause names the installed path, never `src/`. The installed copy follows through `superclaude install`. This single clause stops the orchestrating session from re-injecting the rule (FR-028 forbids it either way). No `--strict` flag is added: strictness belongs in a task's AC.

## 9. Grammar, compatibility and change surface

<!-- Source: Base (original, modified): Section 9 restructured for the no-helper-change design per Change #28 (Variant 2 Section 9, V2:228-253; Variant 3 FR-018 and NFR-004, V3:159-168; IR rules 30 and 31, INV-039, INV-038) -->
**Grammar diff (`P/refs/ledger.md`).**

- **Regex lines:** no change. This covers the header, start, verdict, Ruling, retry, halt, FINAL, PLAN and ARCHIVE regexes (`P/refs/ledger.md:24-111`, `:217-219`).
- **Verdict evidence tokens (`:50`):** add the bullet for `notes@<path>:<start>-<end>`, a pointer to the task's notes file that is never an AC citation (FR-009).
- **Complete rule (`:59`):** add "`compliant` may carry open minor/note findings recorded in the notes file (`refs/qa.md`)".
- **Resume Row S (`:158`):** amended as in FR-024. No other resume row changes.
- **Halt reasons and the reason-to-`review=` table:** unchanged.
- No new ledger record kind, no new halt reason, and no field after `files=`. All new state lives in files under `<retries>/T<id>/` and in the `r<k>-<j>` refs (FR-012).

**Compatibility.**

- **NFR-003** Every existing ledger parses under the new protocol and the unchanged helper. No regex changed and no helper code changed.
- **NFR-004** Ledgers written before the change resume through the existing rows. Findings with no recorded tree get `origin=unknown`, and absent repair files for the current `start` mean both repairs are unspent.

**Change surface.**

| File | Change |
|---|---|
| `P/refs/qa.md` | Severity derivation, checklist and anchor rule, verdict inputs (FR-001 to FR-007); A1 failure record (FR-029); closed seven-slot template (FR-028 to FR-031); FINAL test (FR-023); precedence (FR-032) |
| `P/refs/retry.md` | "Repair round" H3 under "## Escalation procedure" (FR-024); `Cost and caps` sentence (FR-017, FR-036); adviser-route wording (FR-027); escalation-1 two-family advisers and the Model ladder table (FR-034 to FR-036) |
| `P/refs/ledger.md` | Token bullet, corrected example line (FR-009), complete rule, Row S (FR-024) |
| `P/SKILL.md` | `:101` inline rule (FR-030); `:118-119` drive-by rule (FR-007); `:129` Q5 (only `blocking` fails); `:161` Done (complete with notes) |
| `P/refs/managed-workspace.md` | FINAL wording (FR-023); enforcement-map protocol row (NFR-002) |
| `src/superclaude/commands/implement.md` | `:146` Completion mentions completion with notes; edit the committed plugin copy identically (equality pinned by `tests/skills/test_task_workspace_smoke.py`) |
| `src/superclaude/output-styles/pragmatic.md` | `:225` clause (FR-033) |
| `plugins/superclaude/skills/sc-implement-protocol/` | Byte mirror of every `P/` change. `diff -rq` shows the trees identical today. |

`P/scripts/archive_workspace.py` is not in the change surface.

**Tests.**

- Pins that stay green without edits: the eight H2 headings and `RETRY_BUDGET = 8` (`tests/skills/test_task_workspace_lifecycle.py:516-537`), the 22-line `halt-examples` block (`:677`, `tests/skills/test_workflow_archive.py:1024`), the revert bash block (`tests/skills/test_implement_retry_revert.py`). The parallel-rules pin moves deliberately with ponytail item 2 (final section).
- The negative regex cases at `test_workflow_archive.py:817-820` stay.
- New negative test: a verdict line ending `files=src/a.py notes=x` stores `files` as `src/a.py notes=x` (greedy `files=(.+)$`), so no field may follow `files=`.
- A `compliant` complete line with a `notes@` token passes `--print-state` with an unchanged `files` list.

**NFR-005 Installed-path rule.** No new or edited primitive text names `src/superclaude/...`. The check `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` gains no hit (project CLAUDE.md). **NFR-006 No new flag.** Every new behaviour is the default; `--skip-final-review` keeps its meaning.

## 10. Replay cases

<!-- Source: Base (original, modified): Section 10 table re-derived from checklist answers and Addendum 1 origins per Change #29 (IR rule 33, INV-041; SB:85-93; SM C-037, A-006, X-019; Variant 3 R-A5 rows, V3:204-205) -->
### 10.1 Replay cases R-A1 to R-A5

Severity is derived under FR-001 to FR-004 from the checklist answers each finding supports as the reviews state it, and origin is taken from the Addendum 1 grep of the saved per-attempt diffs (SB:85-93). The A1 review was never saved (evidence section 2), so R-A1 uses the evidence summary and is UNVERIFIED against a review file.

| Case | Input | Finding | Checklist answers, origin | Severity | Outcome |
|---|---|---|---|---|---|
| R-A1 | evidence table, row A1 | D1 guard behaviour overstated | `false-claim=yes`, `new` | blocking | **Blocks A1.** A2 fix pass with probes. |
| | | D2 "not implemented" rows contradict pm-agent restore | `false-claim=yes`, `new` | blocking | |
| | | README summary lines for Task 4 rewritten | `quoted-constraint-breach=yes` only if the anchor Read-back finds quotable plan text; UNVERIFIED (no A1 review on disk) | blocking if the anchor holds, else minor | |
| | | D3 unescaped pipe in matrix row | all `no`, cosmetic | note | recorded |
| | | D4 "bad lines are harmless" too broad | all `no` | minor | recorded |
| R-A2 | `review-2.md:10-14` | Snippet appends to tracked `solutions_learned.jsonl`. The reviewer labelled it "low"; the plan forbids seeding production data. | `harmful-effect=yes`, anchored on the diff line of the write; `late` (text present since A1, SB:87) | blocking | **Blocks.** Repaired inside A2 (FR-024); T1 does not complete at A2 without that repair. The "low" label is never read (FR-003). |
| R-A3 | `review-3.md:14-17` | D1 sample-file sentence: README:35 calls old-layout rows lookup-ready | `false-claim=yes`, `late` (A1) | blocking (late blockers are never capped) | **Blocks** on D1 and D2: 2 families, 1 file, so the set is local and is repaired, with no revert and no adviser. |
| | | D2 `jq -c .` "to find invalid lines" misses rows that raise | `false-claim=yes` (the recipe followed as written does not do what the text says), `late` (A2) | blocking | |
| | | D3 Task 4 bullets reworded (reviewer: "low") | `quoted-constraint-breach` anchor Read-back fails: the plan has no Task 4 reservation to quote (`PLAN:15-19`, `:68-82`) | note | recorded |
| | | D4 "except the pytest recorder" ambiguous | all `no`, `late` (A1) | note | recorded |
| R-A4 | `review-4.md:15-18` | Serena-restore claim without a matrix row | all `no` (verified true, FR-005), `fix-induced` (A2) | minor | **Passes with notes.** `complete verdict=compliant`, no Ruling, no prompt. |
| | | Second verified-true claim without a matrix row | all `no` (FR-005) | minor | |
| | | "manual" vs "agent-written" wording | all `no`, a "consider" suggestion | note | |
| R-A5 | `review-5.md:8-11` | (1) tar writes to the current directory, README:119 | `inherited` (Addendum 1 grep of saved diffs) | note (FR-011 inherited cap) | **Passes with notes**, no escalation. |
| | | (2) `chmod 644`, README:208 | `inherited` (`review-5.md:9`: "in HEAD unchanged") | note (FR-011 inherited cap) | |
| | | (3) matrix lacks rows for verified-true facts | all `no` (FR-005) | minor | |
| | | (4) snippet `.py` and `.out` mismatch | all `no`: the reviewer reproduced the claim itself (`review-5.md:5`, FR-005); `fix-induced` (A5 evidence) | minor | recorded, not fixed (FR-025) |

R-A3, decided per finding. D1 and D2 block because each is a false statement a reader would act on, and lateness is not evidence of low severity: a `late` blocker blocks at every attempt (FR-011). D3 does not block: the base graded it as a plan-constraint breach, but under FR-003 the `quoted-constraint-breach` answer needs text byte-present in the plan Constraints or a task instruction, and the plan holds no Task 4 reservation, so the Read-back fails and the finding is a note. D4 is true but unclear; no reader gets a wrong result, so it is a note. Only the chmod finding says "in HEAD unchanged" (`review-5.md:9`); the tar origin comes from the Addendum 1 grep.

<!-- Source: IR rule 32 (INV-040), superseding SM C-040; Variant 3 FR-019 ledger block; SM X-004, A-004: merged per Change #30, replacing the base "Full T1 replay" -->
### 10.2 T1 end state

Expected end state: T1 completes inside A2, after four reviews, with no human. The clean final re-review is UNVERIFIED, because no such tree was ever reviewed in run `E`.

```
T1: start sha=05644ca4028cd263cc9e59aedbe8f21596e35d7d
T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3,T1.AC4 evidence=T1.AC1@<path:line>,T1.AC2@<path:line>,T1.AC3@<path:line>,T1.AC4@<path:line>,notes@.dev/implement/03-memory-docs-f5865990/retries/T1/notes.md:1-<m> extras=lint:skip,typecheck:skip,test:skip files=docs/user-guide/memory-system.md,docs/memory/README.md
```

Step by step:

1. A1 review fails (R-A1). The parent writes `review-1.md` and pins `r1-1` (FR-029, FR-012). No ledger line.
2. A2 is the fix pass, with probes (FR-026). The A2 review fails (R-A2, the data write).
3. Repair 1 (the data write) runs inside A2, before procedure step 0, with no `blocked` line (FR-024).
4. Its re-review raises D1 and D2, both `late`; the first repair did not fail (FR-014), so repair 2 (D1, D2) runs.
5. The second re-review is clean (UNVERIFIED). The notes file holds D3, D4 and the other minors and notes.
6. `complete` at A2 after 4 reviews, 0 reverts, 0 advisers, `RETRY_BUDGET` unspent, and 2 ledger lines: `start`, then `complete verdict=compliant … notes@…` citing all four AC.
7. T2 to T4 run. Because N = 4 > 1, the legacy FINAL runs (`P/SKILL.md:155`) and reads `retries/T1/` (FR-023).

Conditional branch: if the second re-review fails, the repair cap is spent, so the same rules give procedure step 0, a revert and escalation-1 advisers at A3 (FR-027); R-A4 and R-A5 type findings still pass there with notes, with no human.

Every line in the replay block matches its regex: start `P/refs/ledger.md:38`, verdict `:56`.

<!-- Source: enrichment/pve2-failure-analysis.md Section 5 "Replay case PV-R1" (PVE2:196-205); PV-FR-020; IR rule 34 (INV-043): merged per Change #31 -->
### 10.3 PV-R1 replay from the PVE2 RCA

The second failure case (Addendum 2) is a different review/fix loop whose finding totals rose 6, 12, 14. Mapping: R0 = review of A1, R1 = review of A2, R2 = review of A3. Inputs are UNVERIFIED: the RCA gives severity totals only, so the replay assumes its IMPORTANT findings have a confirmed checklist `yes` and its MINOR findings do not.

| Round | Actual | Under these rules |
|---|---|---|
| R0 / A1 | 6 findings, 6 IMPORTANT | 6 blocking families. The A2 fix pass writes probes (FR-026); the path, STEP 0 and boundary probes would list most later scriptable findings before the fix (UNVERIFIED how many, because the probes were never run). |
| R1 / A2 | 12 findings: 6 IMPORTANT, 6 MINOR | The 6 minors go to notes and change nothing. Blocking families 6 to 6, and B2-N2 is a `fix-induced` blocker: a regression, so the fix failed (FR-014). A3 takes the adviser route. No halt, no prompt. |
| R2 / A3 | 14 findings: 4 IMPORTANT, 10 MINOR | The 10 minors go to notes. Blocking families 6 to 4: progress; the ladder continues to A4 with the four families verbatim, regressions first. S-N3r3 is `late`: it blocks only if it has a confirmed `yes`, and is never a regression. |
| End | a third pass was predicted to give another 10 to 15 findings | Either the four blocking families are fixed by A4 or A5 and the task completes `compliant` with its minors in notes and the FINAL still runs, or the ladder ends and the user is shown at most those four blocking families. |

The 6, 12, 14 total series is never consulted by any decision. The `/task-builder` A.10 quota that drove the original loop is out of scope (Section 1).

## 11. Acceptance criteria for the implementation

<!-- Source: Base (original, modified): Section 11 restructured per Change #32 (Variant 2 AC-002 oracle, V2:302; IR rules 35 and 36; PV-FR-008, PV-FR-021; Variant 3 Section 9 negative test); base AC-05 (helper brief chain) deleted -->
- **AC-01** (FR-001 to FR-004) `P/refs/qa.md` states the four checklist answers, the anchor Read-back, the derivation and the vocabulary mapping. Static test.
- **AC-02** (FR-028) The reviewer template in `P/refs/qa.md` is one fenced block whose slot names are exactly the seven of FR-028 and that contains no finding quota. Static test.
- **AC-03** (FR-006) The verdict order in `P/refs/qa.md` says that only `blocking` findings feed steps 3-5. A review with only minor/note findings yields `compliant`. Static wording test.
- **AC-04** (NFR-003) No ledger regex string changes. A test compares the regex blocks of `P/refs/ledger.md:56,97-98` and `archive_workspace.py:44-67` with their current text.
- **AC-05** (FR-009) `aw._VERDICT` matches the FR-009 example line with all four AC cited, and `files=` is captured as exactly the two guide paths.
- **AC-06** (FR-009) The greedy `files=` negative test of Section 9 passes.
- **AC-07** (NFR-003, NFR-004) Every existing fixture ledger in `tests/skills/` still parses and passes the helper unchanged.
- **AC-08** (FR-001 to FR-014, FR-024) Replay oracle `tests/skills/test_implement_severity_replay.py`: a short reference of the pure-function rules fed transcribed finding lines (checklist answers, family, origin) for R-A1 to R-A5 and PV-R1. It asserts the Section 10 outcomes, and that flipping the convergence rule (FR-014) to count all severities makes it fail.
- **AC-09** (FR-010) Origin fixture built from Addendum 1: the seven T1 findings get `late`, `late`, `late`, `late`, `fix-induced`, `inherited`, `fix-induced`.
- **AC-10** (FR-018) The per-attempt table is present in the protocol, and every other section is consistent with it. Static test.
- **AC-11** (FR-019) Static check: every site that writes `halt`, STOPs `E-HALT-QA` or `E-ARCHIVE-BLOCKED`, or asks for a Ruling is reachable only while a blocking finding with a confirmed anchor is open, or is a non-finding STOP row of `P/SKILL.md:26-42`; a minors-only replay writes no `halt` and no `Ruling:` line.
- **AC-12** (FR-017, FR-027) The pins of Section 9 pass with no edit: the eight headings, `RETRY_BUDGET = 8`, the 22-line `halt-examples` block, the revert block. The only moved pin is the parallel-rules pin of ponytail item 2.
- **AC-13** (FR-024, FR-029) A replay fixture of Section 10.2 (a temp repo with a legacy ledger) ends with T1 `complete verdict=compliant` at A2, zero `step=revert` records and a notes file. This is a protocol walkthrough test, so it is UNVERIFIED that the current test harness can drive it without a model. If it cannot, AC-13 is a manual check recorded in the PR.
- **AC-14** (FR-023) `P/refs/qa.md` FINAL text includes the derived-test re-check. `P/refs/managed-workspace.md:49` ("every attempt") is unchanged.
- **AC-15** (NFR-005) `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit, and `pragmatic.md` names only `~/.claude/...`.
- **AC-16** (Section 9, mirror row) `diff -rq src/superclaude/skills/sc-implement-protocol plugins/superclaude/skills/sc-implement-protocol` is empty, and `make verify-sync` passes.
- **AC-17** (NFR-006) `src/superclaude/commands/implement.md` front-matter `argument-hint` is unchanged (no new flag).
- **AC-18** (FR-034) A pure-function test of the adviser choice: for executor ids `claude-sonnet-5-5`, `claude-opus-5-5`, a GPT T1 id, `grok-4.7` and unknown, escalation 1 returns two advisers from different families, and every GPT adviser returned is a T1 model.
- **AC-19** (FR-035) A test pins the verified spawn path for a GPT T1 id, and a test with no reachable GPT model asserts the `family-fallback:` header line and no STOP.

## 12. Risks

<!-- Source: Base (original, modified): table reshaped with probability and impact per Change #33 (Variant 2 Risks 1 and 3, V2:319-321; SM A-001 to A-003; base-selection Risk-1); base risks 1 to 6 kept and rewritten for the merged mechanisms -->
Probability and impact are the authors' judgment, not measured.

| # | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| 1 | A reviewer answers a checklist question wrong, so a real defect is derived `minor` (the "low" label on R-A2 is the example, `review-2.md:3`). Labelling reliability is UNVERIFIED. | Medium | High | Severity comes from factual answers, never the adjective (FR-003); the parent Reads every anchor back; the managed FINAL re-applies the test to the notes (FR-023). |
| 2 | The `{prior_findings}` slot anchors the reviewer, which then hunts only old findings and misses a new blocker. | Medium | Medium | The full audit is mandatory at every attempt (FR-013). The slot holds verbatim blocking findings only and no implementer claims (FR-029). |
| 3 | The accepted-content cap hides a real defect an earlier review missed. | Low | High | Blockers are never capped at any attempt; only new minors, notes and unverifiable claims on unchanged text are capped (FR-013). |
| 4 | The inherited-text cap passes a harmful inherited recipe, such as `chmod` on data files. With no usable baseline there is no inherited cap (origin `unknown`). | Low | Medium | The `covers=` escape (FR-011); recorded as a note, printed in the run summary, read by FINAL. Fixing pre-existing text is outside the task's AC by definition, and the user can open a task for it. |
| 5 | Repairs loop on one stubborn finding. | Low | Medium | At most 1 repair per attempt and 2 per task, then the adviser route (FR-017, FR-027). The attempt cap of 5 is unchanged. |
| 6 | "compliant with notes" weakens the meaning of `compliant` for later readers of old ledgers. | Low | Low | `compliant` still requires every AC met with a citation. The `notes@` token makes notes visible on the line. Old ledgers have no token and mean what they meant. |
| 7 | Origin is miscomputed, so a fix is misrouted or a real inherited defect is capped. | Low | Medium | Origin is computed by the parent from exact line text against pinned trees (FR-010, FR-012); a missing tree gives `unknown`, which applies no origin rule. |
| 8 | Probe cost per fix grows on large tasks. | Medium | Low | One read-only search per family, with literal arguments (FR-026). |
| 9 | `late` blockers keep a task looping. | Medium | Medium | Bounded by the 5-attempt ladder; they are never regressions, so they do not by themselves change the route (FR-014). |
| 10 | The inline-review re-run adds a spawn on the minors path. | Medium | Low | Bounded to one re-run per review (FR-030). |
| 11 | A misgraded minor in a run with no blocking FINAL (legacy N=1, `--skip-final-review`). | Low | Medium | Residual stated in FR-023; the final summary prints every recorded minor (FR-021). |

## Ponytail simplifications (3)

<!-- Source: refactor-plan.md "## Ponytail simplifications (3)": item 1 from Variant 2 ponytail item 1 (V2:335; SM C-044) replaces base item 1; items 2 and 3 are base items (V1:326-335; SM C-045, C-046, X-009) amended with pin handling: merged per Change #34 -->
None of the three removes a safety control, a gate or a requirement of this spec.

1. **Shrink `src/superclaude/commands/implement.md` (146 lines) to about 105 lines.**
   - **Delete:** the Examples section `implement.md:85-113`; the Boundaries "Will" list `implement.md:117-125` (repeated by `P/SKILL.md` and `P/refs/qa.md`; it also holds the Ruling repeat at `:124`); Related Commands `implement.md:136-142`.
   - **Shrink:** the Managed workflow packages body `implement.md:65` to one sentence: "Managed packages: the ledger is the sibling `progress.md`, a fresh FINAL is mandatory, and only the archive helper moves the package; details in `refs/managed-workspace.md` of the protocol skill."
   - **Replace with** one line before Completion: "Examples, boundaries and related commands: see the protocol skill (`~/.claude/skills/sc-implement-protocol/SKILL.md`)."
   - **Keep:** the heading `## Managed workflow packages` (pinned, `tests/skills/test_task_workspace_lifecycle.py:333`), the Options rows `:58-59` (pinned strings "Managed packages always use the sibling `progress.md`" and "blocks archiving"), the whole "Will Not" list `:126-134` (pinned "Move a package by any means other than the archive helper"; no-auto-commit safety), and Completion `:144-146`. Edit the committed plugin copy identically (`tests/skills/test_task_workspace_smoke.py` asserts equality).

2. **State the parallel-batch rules in one file.** Rules (a), (b) and (c) appear word for word in `P/SKILL.md:97` and again in `P/refs/retry.md:47-49` ("Parallel rules (one text, two files)"), so every edit has to be made twice.
   - **Delete:** `P/refs/retry.md:47-49` (the "Parallel rules (one text, two files)" sentence and the quoted rules (a) to (c)).
   - **Replace with** one line: "Parallel batches: rules (a) to (c) in `SKILL.md` Parallel. A batch task gets no retry ladder (check 2)." Keep `P/refs/retry.md:51` (the pre-upgrade batch rule, ladder-specific) and check 2 itself, so no revert guard moves.
   - **Pins:** move the two `"> " + _PARALLEL_RULES` assertions at `tests/skills/test_task_workspace_lifecycle.py:530` and `:794` to assert the one-line pointer; `:786` already pins the canonical text in `P/SKILL.md` and stays. This is a deliberate, named pin move.

3. **State the Ruling confirmation rules once, in `P/refs/qa.md:54-72`.** The same "clear user confirmation, executor records it, never invent approval" text is repeated in `implement.md`, `P/SKILL.md`, `P/refs/ledger.md` and `P/refs/managed-workspace.md`.
   - **Delete or shrink the repeats:** `P/SKILL.md:131` (Q7) keeps "Apply the Halt table in refs/qa.md and the ladder in refs/retry.md. Write ledger line(s). Flush before the next task." and loses the confirmation sentences; `P/refs/ledger.md:67` shrinks to "Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`."; `P/refs/managed-workspace.md:67-69` keeps only the sentences "Do not ask the user for duplicate archive approval or make them hand-write records.", "Acceptance never waives FINAL or evidence of current outcomes, nor authorizes commit, PR, merge or release.", the helper-limits sentence containing "conversation truth", and the FINAL-staleness sentence, and drops the rest. The `implement.md:124` repeat goes with item 1.
   - **Replace each removed passage with** the pointer "User acceptance (Ruling): `refs/qa.md` Halt table."
   - **Keep:** the record form and regex `P/refs/ledger.md:63-65`, `:69-71`; the post-ruling complete rule `:73-81`; the eligibility rule `P/refs/retry.md:449-451`; the `E-NO-RULING` STOP row; the helper's Ruling check. Pinned strings stay present: "MUST automatically append" in `refs/qa.md` and `refs/ledger.md`, "Do not ask the user for duplicate archive approval" and "conversation truth" in `refs/managed-workspace.md` (`tests/skills/test_task_workspace_lifecycle.py:347-351`).
