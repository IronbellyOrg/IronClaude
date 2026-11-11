# Revise 1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place). Blocking ids: L1, L5, L7, L13, L16 (`review/round1.md`, Reviser brief). Line numbers below are in the revised spec (S:N). I did not award a PASS.

## Byte accounting

Size before 57763 bytes, after 59727 bytes (net +1964). Added and deleted are the gross bytes of replaced text per id.

| id | bytes added | bytes deleted |
|---|---|---|
| L1 | 3141 | 1779 |
| L5 | 997 | 579 |
| L7 | 97 | 56 |
| L13 | 95 | 49 |
| L16 | 123 | 26 |
| total | 4453 | 2489 |

## Per finding id

| id | result | where (revised spec) |
|---|---|---|
| L1 | applied in part | see sub-claim table |
| L5 | applied | S:147 (SA-2 exemption), S:158 (P0 order), S:172 and S:178-183 (AC-C1 moved out of the table, pipes now plain ERE, exempt files named, `orca-ide` matched anywhere) |
| L7 | applied | S:190 (step 3 timeout 240000 ms, repeated with step 2 between waits; WC-10 4-minute rule and step 2's 5-minute rule now both hold) |
| L13 | applied | S:16 (section 1.1 now adds "plus the defect fixes section 3 names (SA-4)") |
| L16 | applied | S:91 (troubleshoot brief: no `--depth deep` with fewer than 10 words until P2; the STOP is at `sk/sc-troubleshoot-protocol/SKILL.md:57`, read through `INV-B:240`) |

### L1 sub-claims (L1 merges about 25 reviewer claims; each is listed once)

| sub-claim | result | where / reason |
|---|---|---|
| 37 commands vs 13 in P1 (AC-1.1, P1 scope; t1b F1, F17 part, t2 F2, t3-1 F2, t3-2 F2) | applied | S:76, S:79, S:159, S:203: the section and flag go in the phase named in each row; load and no-fix ready commands get neither; AC-1.1 covers the P1 row only |
| contract location for file-valued output (t1b F2, t2 F17) | applied | S:62: `<file>.return-contract.yaml` |
| adversarial path one directory too high (t1b F3) | applied | S:62: the section 3 row path overrides |
| unknown, empty or truncated status reported succeeded; FAIL verdict (t1b F4, t3-1 F5, t3-2 F8, t3-2 F11 part) | applied for status; FAIL-audit rule kept | S:63, S:62: only `succeeded` or `partial` give succeeded. The FAIL-audit rule is a stated design choice (Decisions table), not a contradiction |
| P0 step 3 and 4 demand a contract that does not exist yet (t1b F5, t3-2 F1) | applied | S:190, S:202 |
| retry in same directory (t1b F6, t3-2 F4) | applied | S:73 (fresh directory for a retry unless the resume flag is passed) |
| permitted `ask` path vs AC-2.2 (t1b F7) and `agentWait` in step 2 (t3-2 F15) | applied | S:208, S:189; "once" left undefined (rejected: wording, no wrong outcome) |
| authorising flag that does not exist (t1b F9) | applied | S:67 (action stays off where no flag exists); "paid external run" left undefined (rejected: missing definition, not a contradiction) |
| WC-11 vs fixed paths, one-at-a-time owed by the coordinator (t1b F11, t2 F7, t3-1 F13, t3-2 F5, F19) | applied | S:69, S:73 |
| worker's own tool-permission prompts (t1b F12) | rejected | A requirement the spec never states (missing-requirement), which the prompt grades as Medium; adding a rule no blocking finding's stated text calls for |
| existing statuses vs the four-value set (t1b F13, t2 F12, t3-2 F16 part) | applied in part | S:62 (unmapped word counts as failed). Contract version field not added (rejected: new mechanism) |
| P1 labelled "no gate" while listing refusals; README rule cited as reason (t1b F17 rest) | rejected | Label wording only; no wrong build follows |
| fixed contract directory shared (t2 F7) | applied | S:73 |
| ask then fresh-dir re-run, which contract is reported (t2 F8) | applied | S:61 |
| two code-editing workers breaking each other's builds without sharing a file (t2 F10) | rejected | Missing requirement (Medium) |
| SA-1 vs WC-1 launch prompt (t2 F11, t3-2 F9) | applied | S:146 ("of a command"), S:59 (WC-1 owner now names its check, 7.2 step 1) |
| WC-4 asserts what UNVERIFIED 3 lists (t2 F16, t3-1 F20) | applied | S:62 |
| "stall is invisible" (t2 F22) | applied | S:60 |
| report path not known before dispatch for workflow, research, init-lite (t3-1 F1) | applied | S:62 (generated paths reported in `--report-path`) |
| E3 cites skill-direct contract vs section 1.4 (t3-1 F6) | applied | S:23 (clause replaced by a statement that the run used the Agent-tool route) |
| ask resumption and stall have no bound (t3-1 F12) | rejected | Missing requirement (Medium) |
| WC-3, WC-6, WC-10, WC-11 have no acceptance check (t3-1 F14) | rejected beyond WC-1 | Missing requirement; only WC-1 was given a check (S:59) |
| AC-0.4 step 5 does not detect an Agent-tool wrapper (t3-2 F7) | applied | S:192 |
| step 6 fails when another writer is in the worktree (t3-2 F14) | applied | S:193 |
| two unresolved gates, which question is carried (t3-2 F20) | rejected | Missing requirement (Medium) |
| ready-today status for adversarial and workflow rests on unconfirmed path (t3-2 F18) | rejected | Covered by the S:62 path rule; the staging behaviour is unverifiable in the sandbox (UNVERIFIED) |

## Checks

- Positive control for the new AC-C1 pattern: `printf 'run orca orchestration check\nrun orca-ide status\nrun orca worktree list\nprose Orca is nice\nuse orca terminal send\n' | grep -nE -e '\borca[[:space:]]+(orchestration|worktree|terminal|agent|status|repo|skills)\b' -e '\borca-ide\b'` printed lines 1, 2, 3 and 5 and not the prose line 4. The verb list is not shown to be complete against Orca's command set (`inventory/orca-capabilities.md` lists `orca-ide skills` at line 12 only); UNVERIFIED beyond those verbs, with `orca-ide` matched anywhere as a backstop.
- Every replacement matched exactly once; no file other than the spec and this report was changed.

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "Narrowed or corrected the contradicting texts (phase scope of the flag and AC-1.1, contract path, status mapping, P0 steps 3-5, output-dir ownership, WC-9/WC-11, E3, UNVERIFIED-vs-fact claims); sub-claims that are missing requirements were rejected as listed."}
{"id": "L5", "action": "applied", "reason": "AC-C1 rewritten as a code block with plain ERE alternation and the two core files exempt, SA-2 states the exemption, and P0 now runs the smoke runs before writing the contract."}
{"id": "L7", "action": "applied", "reason": "Step 3 wait shortened to 240000 ms and repeated with step 2 between waits, so observations are at most 5 minutes apart."}
{"id": "L13", "action": "applied", "reason": "Section 1.1 now says commands also change by the defect fixes section 3 names, matching SA-4."}
{"id": "L16", "action": "applied", "reason": "The troubleshoot brief now excludes a --depth deep input under 10 words until P2 converts the STOP to blocked."}
```
