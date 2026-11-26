## Verdict
**still-relevant.** Keep [#604](https://github.com/IronbellyOrg/IronClaude/issues/604) open as deferred remote-fleet work, not as active implementation and not as permanently rejected work. Live issue read on 2026-11-24: OPEN, no comments; its stated 2026-11-17 owner decision is to backlog R4, not cancel it.

Evidence from the current checkout:
- Remote reads remain excluded: `src/superclaude/cli/observe/adapter.py:153-183` accepts only run/cursor options after the local worker-list template. `tests/observe/test_adapter.py:242-269` includes explicit remote-flag rejection. No remote flag appears anywhere in the observer package (Grep `include.remote`, zero matches).
- Host facts are partly supported, not R4: `src/superclaude/cli/observe/parse.py:75-76` reads host id/kind; `src/superclaude/cli/observe/export.py:25-35` maps both into snapshots. The inspector shows host id at `src/superclaude/cli/observe/view.py:504`; the issue's wording that the inspector shows both id and kind is broader than the current inspector fields.
- The live namespace is still the resolved executable path (`src/superclaude/cli/observe/adapter.py:378-381`); the collector passes that same namespace for all pages (`src/superclaude/cli/observe/collector.py:277-284`), and row identity is namespace plus dispatch id (`src/superclaude/cli/observe/parse.py:333-355`). Host is not part of that key. If different hosts reuse a dispatch id, admitting their rows without changing identity could merge them.
- The Decision Desk finds the first worker with the question's dispatch id, without a host comparison (`src/superclaude/cli/observe/view.py:912-926`). This is an R4 prerequisite, not a demonstrated present local-mode failure. The view uses source order for visible rows (`src/superclaude/cli/observe/view.py:1064-1072`), not host groups.
- `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:14` still says the cross-host ownership gate is not established; its link evidence remains one Run on one host (`:60-65`). `docs/user-guide/observer.md:154`, shipped in merged PR #708 (`52d371e2c20a32a4c17613108daa7f0a295baa36`), explicitly calls #604 not built.

Existing releases R1-R3 are merged (#503, #514, #577, #592, #598), but none fulfills R4. Bounded PR searches for `604` and `observe remote` found no R4 implementation; unrelated text-search hits were discarded. Exhaustive PR/timeline completeness and real remote ownership behavior remain UNVERIFIED. The architecture analysis is saved at `.dev/issuecleanup/g4/604/analyze/analyze-report.md`.

## Complexity and size
**complexity complex; size L.** This is a gated multi-layer extension across remote acquisition, host-qualified row/question identity, unavailable-host reporting, rendering, exports and tests; host metadata already exists, but a flag-only change cannot safely deliver it. This is an engineering estimate, not an implementation authorization.

## Priority
**P3.** Explicitly deferred optional remote visibility, with no verified current local-observer outage or dependency blocking local delivery; its cross-host proof gate remains closed. Do not confuse the future wrong-session risk of enabling remote rows prematurely with an active production incident.

## Concrete next steps
No active R4 implementation was verified. Existing host metadata and releases R1-R3 are prerequisites already present, not partial proof of the remote feature. When the owner chooses to resume it:
1. Save redacted real-remote-host ownership/link evidence and obtain the owner's explicit chat confirmation of the R4 gate. Preserve success, missing, stale and contradictory cases (`.dev/issues/409/bmad/spec-orca-observer/release-gates.md:5,14`). No live probes are authorized by this review.
2. Extend the existing literal read-only adapter template and its tests; add no write verb. Make namespace/identity and the question-to-worker lookup host-qualified before admitting remote rows; missing host or ownership evidence must remain unknown or unlinked, never guessed from a worktree name.
3. Group rows by host and show unreadable hosts as unavailable, not as an empty fleet. Cover 160/116/80 columns, NO_COLOR and ASCII, repeated dispatch ids on different hosts, stale/missing host data and partial reads. Reuse `tests/observe/test_parse.py:254-261` for distinct-namespace behavior, but add the real same-source/different-host case.
4. Preserve snapshot schema compatibility, explicit UNKNOWN values and screen-only question text; update the existing release/spec/unverified/acceptance documents with actual built behavior and remaining limits. Do not route anything through the Coder listener.
5. Run the focused observer tests only in a later implementation task with test execution authorized. This review ran no tests, installations or application commands.

## Dependencies
- **Needs:** verified cross-host ownership/link evidence plus the owner's confirmation, as required by #604 and the R4 release gate. This is a data/approval prerequisite, not a verified dependency on another unfinished issue.
- **Already available:** #409's releases R1-R3 via merged PRs #503/#514/#577/#592/#598. #409 itself remains OPEN; completion of its entire remaining scope is not established as necessary for #604.
- **Does not block the separate local backlog:** #706 explicitly separates remote fleet into #604; #409's 2026-11-20 and 2026-11-23 comments also keep it separate from local follow-up work.
- **PrivateRepoF#477:** referenced integration context only; no hard completion dependency established. Observer traffic must not use its prompt-routing write channel.
- No issue was verified to require #604 as a hard predecessor. Structured GitHub dependency edges and the full event timeline were not read with this brief's allowed commands: UNVERIFIED, not asserted empty.

## Related issues
- [#409](https://github.com/IronbellyOrg/IronClaude/issues/409), OPEN: parent observer dashboard. Its latest read comments retain #604 as a separate deferred release.
- [#706](https://github.com/IronbellyOrg/IronClaude/issues/706), OPEN: remaining local dashboard summaries, links, named steps, navigation/source decisions and scale coverage; its body explicitly keeps remote fleet separate.
- [PrivateRepoF#477](https://github.com/IronbellyOrg/PrivateRepoF/issues/477), workspace listener and prompt routing: mentioned by #604, not an observer permission grant. A read-only lookup was mistakenly made outside this brief's allowed repository; no mutation occurred and no implementation decision relies on its state. No further cross-repository lookups were made.

Scope and limits: only report files under `.dev/issuecleanup/g4/604/` were authored. No source edits, commit, staging, installation, tests, issue/PR edits, comments, labels or closures. Real remote behavior and exhaustive related-item completeness remain UNVERIFIED.

## Related PRs
All rows were read live with `gh pr view --repo IronbellyOrg/IronClaude`; GitHub reports MERGED. These are shipped prerequisites/documentation, not an R4 closing implementation.

| PR | Contribution | Merge commit |
|---|---|---|
| #503 | R1 worker ledger | `9e2608b03857c78ab89fc9439c85256d3bd5d989` |
| #514 | R2 one-Run questions, initially live-off | `cd873619957b3fd4235c54f00363664fca28a193` |
| #577 | Enabled questions and recorded direction selection | `44ff04aeff5ce4bc51cc423a4bf4ffcb59d001cc` |
| #592 | R3 dispatch-level Decision Desk link | `3206bdb9cb6b0fe3c81e6cdbeadcc1455aeeffda` |
| #598 | Owner decision: question text stays on screen only | `10f6ec670bf55f0fe768be8e0ef2067d5c5d879e` |
| #708 | User guides explicitly mark remote fleet not built | `52d371e2c20a32a4c17613108daa7f0a295baa36` |

No R4 implementation found in the bounded text searches; search completeness remains UNVERIFIED.
