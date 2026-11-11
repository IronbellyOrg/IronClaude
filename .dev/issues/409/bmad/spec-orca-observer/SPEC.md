---
id: SPEC-orca-observer
companions:
  - stack.md
  - release-gates.md
  - rendering-rules.md
  - adapter-contract.md
  - snapshot-export-schema.md
  - acceptance-tests.md
  - unverified-register.md
  - owner-decisions-and-risks.md
  - write-back-future-stage.md
  - ARCHITECTURE-SPINE.md
sources:
  - /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md
  - /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md
  - /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/write-back-stage.md
  - /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/architecture-options.md
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability only — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Orca Read-Only Terminal Observer (IronbellyOrg/IronClaude issue 409)

## Why

Pain to solve. One human supervising 5-10 Orca orchestrators and 50-100 sessions/worktrees loses human questions in recency-ordered chat, and "read" gets treated as "handled". Orca's non-consuming reads keep little history (`check --peek` returns unread messages only; `check --all` is capped at 100 rows), so an honest view must keep every observed question until explicit closure evidence appears, and must say plainly what it cannot see. The observer is a read-only terminal companion that separates verified outcomes from activity and discloses unknown, stale, unavailable and partial data instead of implying completeness. Orca and coordinator policies keep authority.

## Capabilities

- **CAP-1**
  - **intent:** A reviewer can replay synthetic fixtures (R0) to see the Signal Bridge, Attention Ledger and Decision Desk directions at 160, 116 and 80 columns, each with realistic degraded versions, before any live Orca call.
  - **success:** Every fixture variant renders at all three widths with the label "synthetic fixture, not live evidence"; the key-reader spike result is recorded (T50, T6, T16).
- **CAP-2**
  - **intent:** A supervisor can see one ledger row per worker dispatch from the verified `worker-list` source (R1), with lifecycle fields, outcome, `nextAction.kind`, liveness and evidence age shown raw.
  - **success:** Golden-sample replay through the fake runner shows every field verbatim or `unknown`, ordering and duplicates handled, and contract test T32 fails on any missing required field (T9, T20-T22, T32, T39).
- **CAP-3**
  - **intent:** A supervisor is told, above the ledger, that human questions are not observed in R1, so an empty screen is never read as "no questions".
  - **success:** The notice `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` renders in every live R1 state, with no number derived from any message source (T9, T33, T47).
- **CAP-4**
  - **intent:** A supervisor can tell how complete and how fresh every fact is: known, unknown, unavailable or stale; collected versus reported; scope; poll age versus evidence age.
  - **success:** PARTIAL, STALE, FAILED, mismatch and `n+? (k unknown)` forms render exactly as pinned; source counts are never summed (T4, T18, T35, T38, T40, T42).
- **CAP-5**
  - **intent:** A supervisor sees lifecycle, outcome, report status, acceptance, current tests and human approval as separate facts, and nothing is inferred from missing evidence.
  - **success:** Sourceless facts read `unavailable (no source)`; a released row is never "done"; cost reads `cost unavailable`; SETTLED and FROZEN read `unavailable (no source)` live (T13-T15, T31, T34).
- **CAP-6**
  - **intent:** A supervisor can select a row and inspect its full evidence, with selection anchored to identity rather than position.
  - **success:** The inspector shows every identifier untruncated or `unknown (absent in source)`; selection survives reordering and reports `selected <id> no longer in source window`; historical rows hide behind `h` with a visible count (T24, T25, T43).
- **CAP-7**
  - **intent:** A supervisor can see what changed since they last looked within a session.
  - **success:** The first observation is the baseline; `m` marks; rows changed in stage, `nextAction.kind` or `liveness.verdict` are starred and counted; unread pages read `not reobserved`; no mark lowers any open count (T8, T10, T41).
- **CAP-8**
  - **intent:** Untrusted source text cannot corrupt the terminal, and the view stays legible at 160, 116 and 80 columns, under NO_COLOR and in ASCII.
  - **success:** Injection fixtures render literally; CJK/emoji truncate on cell width; geometry and too-narrow/too-small diagnostics match; nothing blinks (T23, T26, T28-T30, T44, T49, manual CJK check).
- **CAP-9**
  - **intent:** A user on any platform can get a readable plain-text export of the same view the screen shows.
  - **success:** `e`/`--once` writes the record export from the same view model the screen renders: no ESC byte, full IDs, no truncation; an ID the screen truncates with `>` appears in full (T27, T48).
- **CAP-10**
  - **intent:** Each R1 cycle writes a versioned, additive-only JSON snapshot of the view so a later read-only Go screen inside TUIBBS can read it without depending on the Python code.
  - **success:** A schema test validates the snapshot against `snapshot-export-schema.md`, rejects an unknown major version, and finds no message bodies, prompts, file contents or credentials.
- **CAP-11**
  - **intent:** After QUESTION-OBSERVATION passes (R2), a supervisor sees every observed open human question retained until explicit closure evidence, with "seen is not resolved".
  - **success:** Marking never lowers the open count; source loss never closes a question; the panel is labelled "bounded best effort; coverage unknown" (T10-T12, T19, T46, T51).
- **CAP-12**
  - **intent:** After QUESTION-LINK passes (R3), a supervisor can see, for one selected question, the affected sessions with their worker-list evidence (Decision Desk).
  - **success:** Affected rows come only from an authoritative message-to-`dispatchId`/`worktreeId` mapping verified on this host; otherwise the desk reads "affected scope unknown".

## Constraints

- Read-only. No write path into Orca: no approve, retry, terminate, spawn, merge, rebase, delete-worktree, instruct or reply. R1 runs one allow-listed data argv (`worker-list`) plus the one-time binary discovery (at most one `skills list --json` probe per candidate, so at most two, via `_find_orca()`, before the first cycle); the forbidden verb set never shrinks (`adapter-contract.md`).
- Deterministic, bounded collection: no LLM in the loop, fixed 15 s cycle, at most 5 subprocesses per cycle and 8 MiB output per call.
- Every fact keeps its evidence label; anything unchecked is UNVERIFIED; no Orca API field is invented. The source-to-dashboard schema is PROPOSED, not an Orca contract (`unverified-register.md`).
- Unknown is never rendered as 0, false, `-` or blank. Source loss never closes a question, lowers an open count or turns a value into `failed`.
- Staged releases with data gates (`release-gates.md`). DIRECTION-SELECTED is not shown to have passed; owner to say (owner-decisions-20261108.md item 1). Until the owner confirms a production-integration reading the stricter one applies: offline R0 work only. Issue 409 does not authorize production code changes or deployment.
- Stack is Python + Rich as a `superclaude observe`-style subcommand in the IronClaude repo; the key-reader spike comes first; Textual replaces Rich only if the spike fails, never both (`stack.md`).
- No dependency on TUIBBS, no AGPL code copied, and the design prototype (`canvas.py`) is never imported.
- R1 output (screen, text export, snapshot) contains no message bodies, prompts, file contents or credentials; raw source output never goes into logs, fixtures or exports.

## Non-goals

- Any operational control or write-back in R1, including confirmations or corrections sent to agents; that is a future stage needing a boundary change (`write-back-future-stage.md`).
- A scheduler, session manager, or fork of another agent manager.
- Remote fleet rows (`--include-remote`) before R4; closure evidence, history beyond the 100-row window, admission, cost, durable replay and deep links before their own feeds exist.
- Parsing message rows (`check --peek/--all`, `inbox --json`) before QUESTION-OBSERVATION; the Decision Desk before QUESTION-LINK.
- Fleet SIGNALS bars, an `r` refresh key, persisted "last look" across runs, mouse, themes, animation, blinking, and Windows interactive keyboard input.
- The TUIBBS Go screen itself.

## Success signal

- In R1, replaying the redacted golden `worker-list` samples through the fake runner (and live once the owner clears the integration boundary), a supervisor sees on one screen collected/reported, freshness, scope, the worker ledger and the explicit "questions not observed" notice, the JSON snapshot passes its schema test, and the argv log shows only the allow-listed `worker-list` calls and at most one discovery probe per candidate (at most two).

## Assumptions

- The AC-1..AC-10 to test mapping comes from the seed brief via the merged requirements; it was re-checked against the issue's acceptance list (issue-409-body.md:77-87) and Proposed Solution (:19) on 2026-11-08, with the clause coverage in `acceptance-tests.md`.
- Orca timestamps (`liveness.observedAt`, `evidence.lastObservedAt`) are ISO-8601 on one clock; UNVERIFIED.
- Stack-table facts in `stack.md` were researched from primary sources but not run (UNVERIFIED).

## Open Questions

- Does the owner's staged choice satisfy DIRECTION-SELECTED, and where is the dated owner-written selection record?
- Which production-integration reading applies (1: registering the command or any live subprocess outside the fake runner; 2: wiring into the shipped product)?
- Final command name (recommended `superclaude observe`)?
- Fallback date for QUESTION-OBSERVATION?
- Sample capture and acquisition permission for live reads (open owner decision 6)?
- Message-content exposure (open owner decision 7)?
- What identifies a human question (open owner decision 8)?
- Multi-observer restriction (open owner decision 9)?
- Licence opinion before any Go screen reads the snapshot?
- Does TUIBBS become the staff platform?
- Is the write-back boundary change (issue 409 plus TUIBBS FR-X-13 amendment) approved?
- Which row order is authoritative for snapshot consumers: the snapshot's timestamp order or the ledger's source "newest first" order?
- Does `read k of N Runs since start` belong in the B view header only (merged-requirements rendering rule) or in every header (its adapter scope-honesty rule, T45 and the risks table)? CONTRADICTION in the source; see `rendering-rules.md`.
- What are the contents of A's width matrix, B's x/width coordinates beyond those copied, and C's 44-row height contract (drop order, minimum rows)? The sources name them but do not define them.
- Which `projection.stage.*` subfield drives change detection, and may `stage.detail`/`stage.activity` enter the snapshot (architecture-options.md lists them; merged requirements keep them inspector-only)?
