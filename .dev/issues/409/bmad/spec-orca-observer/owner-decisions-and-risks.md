# Owner decisions, risks and dissents

**Owner-list rule.** A decision belongs here if only a human can decide it, the issue assigns it to a human, or the recommendation departs from a preference the issue states. Each carries a recommendation; none is settled until the owner records it. Labels: "recorded owner decision N" refers to the first table (1-5); "open owner decision N" refers to the numbered open list (1-10).

## Recorded owner decisions (2026-11-08, binding)

| # | Decision | Status |
|---|---|---|
| 1 | Staged releases: R1 = A's worker ledger on `worker-list` plus B's "question source UNVERIFIED" notice; B after QUESTION-OBSERVATION; C behind QUESTION-LINK | Recorded in the dispatch brief. Whether it counts as the DIRECTION-SELECTED selection record is UNVERIFIED (`release-gates.md`) |
| 2 | Stack: Python + Rich, `superclaude observe`-style subcommand in IronClaude, plus versioned additive-only JSON snapshot with a schema test; key-reader spike first, Textual only if it fails, never both | CONFIRMED (owner-decisions-20261108.md item 5) |
| 3 | R1 is read-only. Write-back is a future stage needing an issue 409 boundary change and a TUIBBS FR-X-13 amendment | Recorded; `write-back-future-stage.md` |
| 4 | TUIBBS (private Go BBS, AGPL-3.0) is background only; no dependency, no copied code | Recorded. Licence opinion and "TUIBBS as staff platform" remain open |
| 5 | Every fact keeps its evidence label; no invented Orca field; schema PROPOSED; Orca and coordinator policies keep authority | Recorded |

## Open owner decisions

1. **Visual direction (DIRECTION-SELECTED).** A dated selection record written by the owner, never an agent: (a) default while no question rows exist, (b) default after QUESTION-OBSERVATION, (c) post-link choice or explicit deferral. Reviewed against R0 renders of A, B, C at 160/116/80 marked synthetic, each beside its degraded state, with the task "find the oldest question and inspect its evidence". Recommendation: A plus the COUNTS strip for R1; B after QUESTION-OBSERVATION with A one key away; C behind QUESTION-LINK. V3 dissents (C post-link). Not shown to have passed; owner to say (owner-decisions-20261108.md item 1).
2. **Stack.** Settled by recorded owner decision 2 above (the source listed it as open; it departed from the issue's Go Bubble Tea v2 preference).
3. **Command name and placement.** Recommend `superclaude observe`, registered in `cli/main.py` (deferred import, then `add_command`). Name is the owner's.
4. **Production-integration boundary.** Reading 1 (V1) or reading 2 (V3), both UNVERIFIED; stricter applies until confirmed (`release-gates.md`).
5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option.
6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, owner sets redaction rules. Unblocks B's headline panel.
7. **Message-content exposure.** What may be displayed and what exported; kept as separate permissions; no recommendation beyond that.
8. **Question-type choices.** What makes a message a "human question", which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference.
9. **Multi-observer restriction.** Caps are per process, no singleton. Recommend disclosure only.
10. **Still open from owner-decisions-20261108.md:** write-back stage (summary decision 3), TUIBBS licence opinion (decision 4), TUIBBS as staff platform (decision 5).

## Settled by engineering (not owner votes)

- Fixture replay before the live adapter (R0 has no Orca dependency).
- 100-row window for the question panel, with disclosure and observer-side retention, until durable history exists.
- `--include-remote` off until cross-host joins are verified (R4).
- No persisted "last look"; session memory only.
- Polling: 15 s cycle, at most 5 subprocesses per cycle, STALE after 45 s monotonic, per-call timeout measured at the first permitted live read, message calls per cycle by measurement.
- POSIX interactive mode plus `--once` text export on every platform.

## Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Message row contract never verifies | B's panel stays empty; product becomes relabelled A | Decisions 6 and 5; shared adapter and renderer, so a switch costs one layout |
| Worker ledger read as "questions" | False sense that human attention is covered | Ledger titled `worker-reported, not questions`, gap notice above it (T9) |
| `page.total` includes historical dispatches | Inflated denominators | `reported T`; `result.counts` shown separately (T18) |
| Bound scope shows one Run as the fleet | Missed orchestrators | `scope.source` in the header, `one Run only`, `read k of N Runs since start` |
| Hand-written key reader misbehaves | Terminal left in cbreak mode | cbreak with ISIG kept; restore in `finally` and on SIGINT, SIGTERM, SIGHUP and SIGTSTP, re-enter on SIGCONT (`stack.md`); `--once` needs no cbreak mode; R0 spike decides, Textual fallback |
| Sanitizer gaps | Escape-sequence injection from worker text | Own allow-printable sanitizer, literal rendering, `injection` fixture (T29, T44) |
| Retention grows in a long session | Memory, clutter | 1,000-record bound; `unknown (retention exceeded)`; eviction never lowers the open total (T46) |
| Fixture schema mistaken for an Orca API | Coupling to PROPOSED fields | Separate fixture loader; live model built only from verified fields (`unverified-register.md`) |
| `_find_orca()` lives in `install_user_setup.py` | Observer import pulls installer code | Import as is; moving it is a separate owner-approved refactor |
| Oldest rows not read at the paging cap (INV-007, accepted) | Long-running active workers missed | Strip disclosure; earlier rows kept as `not reobserved`; state filter UNVERIFIED |
| Message bodies acquired without permission (INV-017) | Sensitive content in the stdout buffer | Permission checked before the call; call skipped if a narrow read cannot honour it; raw output never logged, fixtured or exported |
| "Non-consuming" read consumes (INV-022) | Deliveries lost to real recipients | Quiet-scope before/after test in QUESTION-OBSERVATION (T51) |

## Dissents (2 of 3 positions merged)

- **`page.total` (C-008 / A-003):** V1 wants it required, rejecting responses without it. Merge keeps it optional (`reported unknown`) so returned workers are not hidden.
- **Post-link default (C-001):** V3 recommends C. Recorded owner decision 1.
- **A-008 label:** V1, V2 QUALIFY; V3 REJECT. QUALIFY applied: per-process caps, disclosed, no singleton.
- **Message calls per cycle (C-002 / X-007):** open, set by measurement; V3 default at most 1.
- **Production-integration boundary (S-007):** both readings UNVERIFIED; stricter applies.

## Notes on the debate record

- Invariant probe recorded 16 MEDIUM findings; Round 3 advocate texts refer to the 14 left after Round 2. Both counts are correct for what they describe.
- X-001: the design prototype does not match the seed brief's claim that Signal Bridge collapses at 116 columns; the prototype is visual reference only.
- DIRECTION-SELECTED is not shown to have passed; owner to say (owner-decisions-20261108.md item 1). The INV-019 design defect is resolved but no owner selection record exists in the source; until the owner says, the stricter reading applies.
