# Extract of originals for the BMAD PRD, Orca observer (issue 409)

Extraction worker output, 2026-11-08. Quotes are verbatim; evidence labels are kept as written. Source keys:
- **H** = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/handoff-step1.md`
- **M** = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md`
- **O** = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md`
- **T** = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/summary.md`
- **I** = issue-409 body (`gh issue view 409 --repo IronbellyOrg/IronClaude`, read 2026-11-08; line numbers are of `--json body --jq .body` output, numbered with `cat -n`)
- **R3** = `/tmp/orca-observer-pass3.json` (review 3 minors, the file H:11 points to)
- **S/** = spec folder `/home/coder/workspaces/worktrees/Coder/dashboard-bmad/_bmad-output/specs/spec-orca-observer/`

## 1. Issue acceptance criteria (I, heading "Acceptance Criteria", I:77-87)

The issue writes them as unnumbered checkboxes; numbers below are their order.

1. "A human selects the visual direction before production integration." (I:77)
2. "The observer identifies human attention items and explains why they matter, shows affected scope and meaningful changes since last look, and provides inspection of underlying evidence." (I:78)
3. "The view distinguishes verified outcomes from activity, displays evidence freshness and completeness, and makes missing, stale and partial information explicit." (I:79)
4. "Lifecycle, report status, acceptance, current tests and human approval remain separate; the display does not infer conflict, failure or admission from insufficient evidence." (I:80)
5. "The selected design supports 160, 116 and 80 column views, stable keyboard selection, NO_COLOR, readable ASCII/text exports and full identifiers in selected detail; no blinking or compulsory motion." (I:81)
6. "Test the 8-orchestrator/80-session base and 5/8/10-orchestrator, 50/80/100-session scenarios, including uneven ownership, shared/unmapped worktrees, historical records, duplicates/out-of-order events, stale sources and missing fields. One-to-one session/worktree mapping is not assumed." (I:82)
7. "Sanitize untrusted ANSI/OSC/control sequences; use display-cell width for safe truncation and keep filtered versus global counts explicit." (I:83)
8. "Tokens are not progress; elapsed time is not completion percentage; missing cost is not zero; a partial subtotal is not total spend; policy-frozen work remains for explicit human handling." (I:84)
9. "Keep collection deterministic and bounded, without a default LLM polling loop or operational controls." (I:85)
10. "Integration uses confirmed source contracts and clearly identifies unsupported or incomplete coverage instead of presenting synthetic fixture fields as established Orca API fields." (I:86)
11. "The twenty primary design images and complete package are provided with the issue, subject to attachment support and an accessible package delivery method." (I:87)

Out of Scope (I:91): "Approving, retrying, terminating, spawning, merging, rebasing, deleting worktrees or instructing workers; a new scheduler or session manager; forks of other agent managers. This issue request does not authorize production code changes or deployment."

## 2. Users, scale, jobs and pains

- Who and scale, I "Problem Statement" (I:11): "One human supervising 5-10 orchestrators and 50-100 sessions/worktrees can miss important decisions, meaningful updates, and evidence in noisy chats. They need to distinguish verified outcomes from activity and understand what needs attention and why."
- User story, I "User Story" (I:15): "As a human supervising orchestrators, I want a read-only view of attention, affected work, changes, and evidence, so that I can find decisions and inspect their supporting facts without confusing activity with outcomes."
- Product identity, I "Feature Summary" (I:7): "Create a human-observation terminal companion for Stably.ai Orca in the existing IronClaude/Coder environment. It is not github.com/orca-cli/orca, a scheduler, or a session manager."
- Test scale, I AC 6 (I:82): "the 8-orchestrator/80-session base and 5/8/10-orchestrator, 50/80/100-session scenarios".
- Pain, root cause, M:12: "Root cause of #409: a human question gets lost because chat is ordered by recency and because reading a message is treated as handling it."
- Pain at scale, M:201: "With 5-10 orchestrators, many questions are open at once, so the single-panel slot repeats the recency bias #409 complains about."
- Pain, false resolution, M:25: "A panel built on `--peek` would therefore resolve questions when they are read. That is exactly the defect #409 describes."
- Job, decide one question, M:203: "C answers \"who is affected, and what is the evidence?\" for one request".
- Job, walkthrough task, M:220: "C's walkthrough task \"find the oldest question and inspect its evidence\"."
- Job, fleet at a glance, M:200: "A also answers \"is the fleet alive?\" at a glance."
- Proposed-solution distinctions, I "Proposed Solution" (I:19): "Keep lifecycle, report status, acceptance, current tests, and human approval distinct. A dirty worktree is not automatically dangerous, stale is not failed, shared paths do not establish a conflict, and inspectable evidence is not admission."
- Future user job (not R1), O:13: "Users must be able to send confirmations or corrections from the BBS to their agents."
- Wider user group (background), O:15: "the owner is also exploring TUIBBS as an internal communication tool and platform for all human staff who manage agent teams; the observer may become a TUIBBS module."
- Counter-evidence on teams, T:10 (Refuted): "TUIBBS as a team platform (no teams; group resolver empty, `internal/auth/provider.go:244-257`)".

## 3. Owner decisions (O, 2026-11-08)

O:3: "Recorded by an Orca worker (run run_93bfa00cae2b, task task_bfe724db1dac) from the coordinator's relay of the owner's order."

1. **Staged direction chosen ("Stage it")** (O:5-9). "Release 1: Signal Bridge's worker ledger, built on the verified worker-list source, carrying Attention Ledger's \"question source UNVERIFIED\" notice." / "Attention Ledger comes after the QUESTION-OBSERVATION gate." / "Decision Desk comes behind the QUESTION-LINK gate." / "Whether this fully satisfies the DIRECTION-SELECTED gate is for the owner to say. What is recorded here: the owner chose the staged direction; the technology stack was NOT yet confirmed."
2. **Stack not confirmed; TUIBBS review first** (O:11). "Python + Rich remains only a recommendation. The owner asked for a review of the TUIBBS codebase (IronbellyOrg/TUIBBS-scp) before the stack is confirmed." Superseded by item 5.
3. **New requirement: write-back from the BBS** (O:13). "This departs from issue 409, which lists approving, retrying, terminating, spawning, merging and instructing workers as out of scope and requires a read-only observer. It is recorded as a FUTURE stage that needs an explicit boundary change to issue 409. Release 1 does not do it."
4. **Background, not deciding for release 1** (O:15). TUIBBS as internal communication tool and staff platform; "the observer may become a TUIBBS module."
5. **Stack and release-1 scope CONFIRMED** (O:17). "The owner chose \"Python + Rich with snapshot export\" ... release 1 is the standalone Python + Rich observer (Signal Bridge worker ledger), and its `export(view)` writes a versioned, additive-only JSON snapshot with a schema test, in release-1 scope, so a read-only Go screen inside TUIBBS can read it later. This supersedes item 2 (stack no longer open). The key-reader spike stays the first task. Still open and NOT decided: write-back boundary change (summary.md decision 3), the licence opinion (decision 4), TUIBBS as the staff platform (decision 5)."

Still-open owner decisions from M section 11 (M:417-425), not settled by O: 1 visual direction (dated selection record; "This is the DIRECTION-SELECTED gate (section 7), which has NOT passed."), 3 command name, 4 production-integration boundary, 5 fallback deadline, 6 sample capture and acquisition permission, 7 message-content exposure, 8 question-type choices, 9 multi-observer restriction. (Decision 2, stack, is settled by O item 5.)

## 4. TUIBBS review facts (T)

- Snapshot inspected, T:3: "TUIBBS-scp at a6d7e7f (2026-10-20), cloned read-only to `/tmp/tuibbs-review`."
- Licence status, T:6: "If TUIBBS is chosen later, it gets a compiled-in, read-only Go screen (AGPL, in the TUIBBS repo) that reads the snapshot". T:9 (Validated): "no copying keeps MIT safe". T:10 (Refuted): "a non-AGPL Go screen inside TUIBBS". T:11 (Unverified): "whether JSON-only exchange keeps MIT and AGPL separate (legal)". T:18 owner decision 4: "Get a licence opinion before a Go screen reads the MIT observer's output." Status: licence opinion open (O:17).
- Rule FR-X-13, T:9 (Validated): "the read-only boundary holds on both sides (`internal/serve/menu.go:637-640`, \"FR-X-13: no write-back\")". T:17: "Write-back: approve the boundary change for issue 409 and, separately, ask the TUIBBS owner to amend FR-X-13, before any build. Smallest first stage: answer your own agent's pending question with one of its fixed options, relayed through the coordinator, with 9 gates (write-back-stage.md)."
- Why a Go screen regardless, T:6: "TUIBBS screens are all compiled-in Go and its plugins cannot draw (`proto/v1/plugin.proto:61-68`), so a Go screen is needed whatever R1 is written in; a stable data contract is the one thing R1 can usefully give it. Write-back stays out of R1 and out of the snapshot."
- What R1 must not depend on or copy: M:301 "TUIBBS-scp is AGPL, so no code is copied from it, whatever the stack. The sanitizer is written in the observer package. The design package's prototype `canvas.py` is never imported by production code"; I:27 "informed by TUIBBS-scp styling and components without extracting AGPL code absent license assessment"; I:38 "Use original compositions or properly licensed upstream library APIs, not an unreviewed transplant of third-party application code/assets."; H:5 "no TUIBBS dependency or copied code."
- Not a stable base, T:10 (Refuted): "a separately shipped module (plugin host unwired, `internal/module/README.md:4-5`)"; "TUIBBS as a stable base (hobby, dogfood-only, `docs/scope.md:17-18`; no successful release)".
- Field-path correction, T:12: "the evidence timestamp is `projection.evidence.lastObservedAt` (merged-requirements.md:328 omits `projection.`)."
- Risks, T:22-25: "TUIBBS docs claim more than its code wires ... trust the code."; "Who Orca accepts a `reply` from is unproven; `--from` is a caller-supplied claim. Write-back must relay through the coordinator until that is settled."; audit key beside database ("audit chain is forgeable by anyone with host access"); "The PTY door (zero-rewrite path) is a v1 non-goal and unbuilt".

## 5. Step-1 handoff (H)

- **Locked**, H:5: "read-only observer; R1 data argv is only `worker-list` plus a one-time `skills list --json` discovery probe (outside the 5-per-cycle cap); 15 s cycle, 5 subprocesses, 8 MiB per call; Python + Rich `superclaude observe`-style subcommand, key-reader spike first, Textual only on failure; versioned additive-only JSON snapshot with a schema test (schema PROPOSED); staged releases R0 to R4 behind data gates; unknown never shown as 0/blank; no message bodies, prompts, files or credentials in any output; write-back is a future stage only; no TUIBBS dependency or copied code."
- **Capabilities**, H:7: "CAP-1 fixture replay (R0); CAP-2 worker ledger; CAP-3 \"questions not observed\" notice; CAP-4 completeness and freshness; CAP-5 separate facts, no inference; CAP-6 ID-anchored inspector; CAP-7 changes since last look; CAP-8 safe, legible rendering; CAP-9 lossless text export; CAP-10 JSON snapshot; CAP-11 question retention (R2); CAP-12 Decision Desk links (R3)."
- **Open questions (15)**, H:9: "DIRECTION-SELECTED record; production-integration reading; command name; QUESTION-OBSERVATION fallback date; open owner decisions 6-9 (sample/acquisition permission, message exposure, what is a human question, multi-observer); licence opinion; TUIBBS as staff platform; write-back boundary change; snapshot row order; `read k of N Runs since start` placement (CONTRADICTION); undefined width matrix / x-width coordinates / 44-row contract; which `stage.*` subfield drives change detection and whether `stage.detail`/`.activity` enter the snapshot (CONTRADICTION)."
- **Validation**, H:11: "Review 3 of 3 (fresh-context adversarial, coherence plus preservation, at the coordinator's request): **PASS**, 14/14 FIXED, 0 new blocking, 14 minor. All minors recorded in the review JSONs (`/tmp/orca-observer-pass{1,2,3}.json`, not copied), not fixed. Review 3 did not re-read the design package."
- **Open minors: 14, confirmed** (R3 `minor[0..13]`, verbatim, trimmed with "..."):
  0. "owner-decisions-and-risks.md:41 'Decisions 6 and 5' lacks the 'open owner decision' qualifier defined at line 3."
  1. "release-gates.md:45 'decision 8 ... and decision 6' lacks the 'open owner decision' qualifier"
  2. "owner-decisions-and-risks.md:66 references INV-019 with no definition anywhere in the spec."
  3. "SPEC.md CAP-6 cites T24, T25, T43 for `h`/selection-lost; the `h` test is T21 and no test pins selection-lost."
  4. "SPEC.md CAP-10 success signal names the snapshot schema test but it has no test ID"
  5. "SPEC.md CAP-12 cites no test ID (R3, gated; acceptable but untraced)."
  6. "SPEC.md CAP-2 'contract test T32 fails on any missing required field' overstates T32: missing scope/page.total/projection.* render unknown, not failure."
  7. "SPEC.md:73 'Issue 409 does not authorize production code changes or deployment' is phrased more strongly than the sources" (see contradiction X8)
  8. "snapshot-export-schema.md:25 source.status vocabulary OK/STALE/ERROR/UNKNOWN differs from screen words FAILED/NOT POLLED; mapping unstated."
  9. "snapshot-export-schema.md:26 glosses source.observedAt as 'Time of the last successful read'; the source does not define it."
  10. "rendering-rules.md:32 'with `stage` moved into the inspector' copies source wording that implies a prior stage column."
  11. "unverified-register.md:27 'until three proofs are recorded' omits the non-consumption test and question identity that release-gates.md also requires."
  12. ".memlog.md:29 'R1 uses one allow-listed argv' is superseded by line 51 (allow-list plus discovery probe); historical log line."
  13. "stack.md drops the source qualifier 'best of the four' for the chosen option."
- **UNVERIFIED, flagged for the PRD**, H:13: "stack-table facts (nothing run); AC-1..AC-10 mapping (from seed brief, not the issue); Orca timestamp clock/format; all message-row fields and the `check --all` candidate; `nextAction.kind` and `stage.*` value sets; `page.total` meaning; whether the owner's staging counts as DIRECTION-SELECTED; Orca `reply` sender rule (future stage)."
- **Contradictions recorded, not resolved**, H:15: "`read k of N` placement; `stage.detail`/`.activity` in the snapshot (withheld, stricter reading). Notice wording unified to Change 28 (source T9 used a variant)."
- **Dropped / not done**, H:17: "design package not fully absorbed (binary exports never opened); project-context.md absent, skipped; issue's Go preference overridden by owner decision 2."
- Flag for the PRD (this extract): the spec's AC table maps AC-1..AC-10 from the seed brief (S/acceptance-tests.md:3, "UNVERIFIED against #409"); the issue has 11 criteria (section 1). The PRD should map to the issue's 11 directly.

## 6. Coverage gaps and contradictions

Method: case-insensitive fixed-string `grep -rciF` over S/ (all 10 files plus `.memlog.md`), about 140 terms in three batches. "0 hits" means no line in S/ contains the term.

### Coverage gaps (10)

| # | Requirement (source) | Grep terms tried, result |
|---|---|---|
| G1 | "elapsed time is not completion percentage" (I:84, AC 8) | `elapsed`, `percentage`, `completion percent`: 0 hits |
| G2 | "a partial subtotal is not total spend" (I:84, AC 8) | `subtotal`, `spend`, `total spend`: 0 hits. Only "missing cost is not zero" is covered (`cost unavailable`, 5 hits) |
| G3 | "policy-frozen work remains for explicit human handling" (I:84, AC 8) | `FROZEN`: 5 hits (marker only, T34); `explicit human handling`, `human handling`: 0 hits. Partial |
| G4 | "The twenty primary design images and complete package are provided with the issue" (I:87, AC 11) | `twenty`, `images`, `PREVIEWS`: 0 hits; `design package`: 2 hits (rendering-rules.md, .memlog.md), not as a requirement. No test or reviewer check |
| G5 | "A dirty worktree is not automatically dangerous" (I:19) | `dirty`, `dangerous`: 0 hits |
| G6 | "shared paths do not establish a conflict" (I:19) | `shared path`: 0 hits; `conflict`: 3 hits, all timestamp conflicts (adapter-contract.md:44, acceptance-tests.md AC-8, .memlog.md:15). Shared worktree rows are covered (`unmapped`, `one-to-one` in acceptance-tests.md) |
| G7 | "inspectable evidence is not admission" (I:19) | `inspectable`: 0 hits; `admission`: 4 hits, only as an unestablished feed |
| G8 | "Stably.ai Orca ... It is not github.com/orca-cli/orca" (I:7) | `Stably`, `orca-cli`: 0 hits (`scheduler`, `session manager` covered at S/SPEC.md:81) |
| G9 | "Wish, Huh and Harmonica are optional, not first-version requirements" (I:27) | `Wish`, `Harmonica`: 0 hits. Low relevance after the stack override |
| G10 | Retention rationale: "`--peek` returns \"only unread messages\" ... A panel built on `--peek` would therefore resolve questions when they are read" (M:25) | `only unread`: 0 hits; `peek` appears only as forbidden or candidate (adapter-contract.md:17, unverified-register.md:21,27). The rule is kept, the reason is not |

Checked and covered (not gaps): AC 6 scenario matrix (`27 renders`, `10 orchestrators` in acceptance-tests.md); "stale is not failed" (``into `failed` `` in SPEC.md:72, rendering-rules.md); 5-10 / 50-100 scale (SPEC.md:26); every M rendering string tried (`read k of N`, `SEEN IS NOT RESOLVED`, `RETAIN CONTEXT`, `terminal too narrow`, `retention exceeded`, `cycle overran`, `2 KiB`, `GNOME`, `one Run only`, `x/y shown`, `+N more`, `n+?`, `U+202E`, `44-row`, `width - 43`, both prototype invariant lines, AC-S, T51, INV-022, four-kinds gate samples).

### Contradictions (9; X1, X2 already recorded in S/ as CONTRADICTION)

- **X1 `read k of N` placement (originals-internal).** M:45 "In the B view the header adds `read k of N Runs since start`" vs M:355 "The header also shows `read k of N Runs since start`." Recorded open at S/SPEC.md:111.
- **X2 `stage.detail`/`.activity` in the snapshot.** M:138 "The MVP shows these only in the inspector" vs architecture-options.md (cited at S/snapshot-export-schema.md:43, "CONTRADICTION: architecture-options.md lists them"). Spec withholds them; open at S/SPEC.md:113.
- **X3 Row order.** M:64 "One row per worker from `worker-list`, in source order" vs S/snapshot-export-schema.md:51 "By `liveness.observedAt`, else `evidence.lastObservedAt`, newest first; ties by `dispatchId`." S/.memlog.md:16 calls it a "Tension recorded, not a defect"; H:9 lists "snapshot row order" as open.
- **X4 Field path.** T:12 "the evidence timestamp is `projection.evidence.lastObservedAt`" vs bare `evidence.lastObservedAt` at S/SPEC.md:94, S/unverified-register.md:43, S/snapshot-export-schema.md:51 (S/adapter-contract.md:44 uses the full path).
- **X5 Post-link default.** S/owner-decisions-and-risks.md:57 "Post-link default (C-001): V3 recommends C. Recorded owner decision 1." vs the same file :17 (open decision 1, "(c) post-link choice or explicit deferral ... NOT passed"), M:463 "The owner decides (section 11, decision 1)" and M:224 "Optional owner re-confirm of the post-link default (B or C)". O:8 says only "Decision Desk comes behind the QUESTION-LINK gate."
- **X6 Recorded owner decision 5 has no source in O.** S/owner-decisions-and-risks.md:13 "Every fact keeps its evidence label; no invented Orca field; schema PROPOSED; Orca and coordinator policies keep authority | Recorded". O item 5 (O:17) is the stack and scope confirmation; nothing in O matches. Closest original: I:21 "Orca and coordinator policies retain authority." S/owner-decisions-and-risks.md:9 attributes decision 1 to "the dispatch brief", not O.
- **X7 Decision numbering.** S/.memlog.md:15 "superseded by owner decision 2 (Python + Rich)" and H:17 "overridden by owner decision 2" vs O:11 (item 2: "Python + Rich remains only a recommendation") and O:17 (item 5 confirms). S/owner-decisions-and-risks.md:10 uses its own table number 2 and cites "owner-decisions-20261108.md item 5", so the meaning is right but "owner decision 2" is ambiguous against O.
- **X8 Review minor 7 vs the issue.** R3 minor 7 says S/SPEC.md:73 "Issue 409 does not authorize production code changes or deployment" is "phrased more strongly than the sources", but I:91 says "This issue request does not authorize production code changes or deployment." SPEC.md:73 matches the issue; the minor is wrong.
- **X9 Gap-notice wording (originals-internal, resolved in S/).** M:66 and M:168 `source UNVERIFIED, 0 rows interpreted, not "no questions"` vs M:370 (T9) and M:172 `0 rows interpreted (contract UNVERIFIED)`. S/rendering-rules.md:61 and S/.memlog.md:52 unify on the first.

Overridden by the owner, not a contradiction: I:27 "Preferred direction is Bubble Tea v2, Lip Gloss v2 and Bubbles v2" vs S/stack.md:3 Python + Rich, per O:17.

### Not read

Design package binaries (none opened, per instructions); architecture-options.md and write-back-stage.md of the TUIBBS review (not in the input list; cited only through T and S/).

