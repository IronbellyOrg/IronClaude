# Revise 1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Blocking ids from `review/round1.md:330-333` (Reviser brief): L1, L2, L4, L5. Minor and Medium findings (L3, L6-L16) left alone. No PASS is claimed.

## Byte accounting
Spec before: 57763 bytes. After: 60019 bytes. Net +2256.
Counts are the exact replaced text (bytes added = new text, bytes deleted = old text); an edit that rewords a clause counts both.

| id | bytes added | bytes deleted | net |
|---|---|---|---|
| L1 | 3600 | 1957 | +1643 |
| L2 | 400 | 313 | +87 |
| L4 | 757 | 361 | +396 |
| L5 | 285 | 155 | +130 |
| total | 5042 | 2786 | +2256 |

## Per finding
| id | result | where (spec, after edit) |
|---|---|---|
| L1 | applied (parts), the rest rejected below | |
| L1 WC-3 (t2-1 F1, t3-1 F1, t1b-1 M2, t3-2 M1) | applied | WC-3: `ask` only after the blocked contract is written, only for a flag section 3 lists, never a `/sc:implement` Ruling (D2), `failed` if no answer. Rationale: `sk/sc-implement-protocol/refs/qa.md:238` quoted at spec D2. |
| L1 WC-4 paths (t1b-1 F1, M3, M4; t2-1 F2; t3-1 F7; t3-2 M2) | applied | WC-4: directory = `--output-dir` or parent of `--output <file>`; fixed path per section 3 row (adversarial); no output means stop before work; workflow path learned from `--report-path`. |
| L1 versioning/status map (t1b-1 M6) | applied narrowly | WC-4 adds `contract_version` and the mapping of existing statuses; the install-missing fallback (t3-2 M11) is rejected: it is a new mechanism. |
| L1 completeness (t3-2 N1) | applied | WC-4 "complete before `worker_done`". |
| L1 missing or unknown status (t2-1 F8, t3-1 F15) | applied | WC-5 maps it to `failed`. |
| L1 partial as completed (t2-1 F6, t3-1 F8, t3-2 N3) | applied | 2.3: coordinator opens the report before starting any dependent Task. |
| L1 retry path (t2-1 F7, t3-2 M3, t3-1 F6) | applied | WC-6 retry brief names the fresh directory; init-lite row changed to a fresh `--output` file per attempt. |
| L1 WC-10 boundary (t1b-1 M1, t2-1 F12, t3-2 N2) | applied | WC-10 threshold 4 minutes, matching AC-4.3 (240 s). The Agent-tool fan-out call (t3-1 F9) is rejected: a subagent call cannot be split, and WC-10 targets command waits. |
| L1 WC-12 (t3-1 F19) | applied | `consumer_fenced` excludes an empty result. |
| L1 permission prompt (t3-1 F3, t3-2 M13) | applied | 2.3 sentence; 7.2 step 2 already detects the parked state. |
| L1 blocked retry loop (t3-1 F16) | applied | 2.3 last sentence. |
| L1 readiness fallback (t3-2 M16) | applied | WC-1 now 30 s (`EVIDENCE.md:45,56` as cited in WC-1). |
| L1 flag before gates convert, AC-1.1 scope, load, brainstorm/init-lite in no phase (t1b-1 F2, F3; t2-1 F4; t3-1 F5, F18; t3-2 N6) | applied | Section 6 P1 row lists exactly the commands that get the section and flag in P1 (adds brainstorm, init-lite; load excluded); gate commands get the flag in their own phase; AC-1.1 uses the P1 list and later phases extend it. F18 beyond that is rejected: P2 AC-2.1 already asserts each gate. |
| L1 AC-0.4 (t3-2 F1, t2-1 F10) | applied | 7.2 step 3 allows the existing report file in P0; step 5 also searches for an Agent-tool call running the command. |
| L1 hardcoded template path (t2-1 F13) | applied | cli-portify cell now a brief rule, no edit. |
| L1 required-flags column (t3-2 M6) | applied | 2.3 names the columns that carry required flags. |
| L1 stale contract of a fenced attempt (t3-1 F13) | rejected | Needs a new locking mechanism; WC-12 stops a fenced worker and the retry uses a fresh directory (WC-6). |
| L1 brief restatement of worker-session rules (t3-2 M12) | rejected | Would add a new template section; no blocking sentence rests on it. |
| L2 | applied | AC-C5 and AC-0.3 now `grep -E '^-' \| grep -v '^--- a/'`, so a deleted `- b` line (diff `-- b`) is caught. |
| L4 | applied | AC-C1 moved to a fenced block with plain-`|` alternation, verbs `status|open|skills` added, and the contract file and routing guide excluded (SA-2 allows Orca text in the contract). |
| L5 | applied | Section 3.1 intro no longer promises a P1 contract; the P2 row adds the WC-4 contract for release-split, tdd and troubleshoot, so AC-2.3 step 4 can pass. |

## Evidence caveats
Citations in the added text point to spec lines and to `qa.md:238` and `EVIDENCE.md:45,56` already cited by the spec; none was re-read from the repo (not in this sandbox), so they are UNVERIFIED here. I did not run the new AC-C1 or AC-C5 commands.

## Fix map
```fixmap-v1
{"id": "L1", "action": "applied", "reason": "WC-3, WC-4, WC-5, WC-6, WC-10, 2.3, the P1 list and AC-1.1 and AC-0.4 steps now agree; WC-12 fence and brief restatement sub-points rejected as new mechanisms."}
{"id": "L2", "action": "applied", "reason": "AC-C5 and AC-0.3 use grep -E '^-' then drop the '--- a/' header so deleted dash-lines are caught."}
{"id": "L4", "action": "applied", "reason": "AC-C1 rewritten with plain-pipe alternation in a code block, wider verbs, and the contract and routing files excluded."}
{"id": "L5", "action": "applied", "reason": "P2 row adds the WC-4 contract for release-split, tdd and troubleshoot and 3.1 no longer defers it to P1."}
```
