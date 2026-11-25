# Scoring pass 2 (reverse order: Variant B first, then Variant A), debate D07 position-bias check

Variant B = variant-2-original.md (Clay's line). Variant A = variant-1-original.md (the owner's line).
Sources opened read-only to check citations: Clay's DESIGN lines 136, 137, 264, 304, 341, 700, 702, 706, 708, 710, 714, 716, 866, 891, 893, 1159; PR-A `route.py` (603 lines, docstring lines 1-24, `O_EXCL | O_NOFOLLOW` at line 122, `fsync` line 126, `os.replace` line 129); the owner's `dispatch.py` (479 lines, `LOOP_CAP_S` line 52, `CHILD_TIMEOUT_S` line 53), `test_dispatch.py` (31 `def test_` functions), REQ lines 31, 37, 49 (R21 says "6 repos"), Q26 line 3, OWNER-ANSWERS line 23. All of these matched what the papers say. One small drift: A cites `CALL_CAP` at `github.py` line 46 (true on the master snapshot and in DESIGN); on the owner's branch it is line 49.

## Variant B (Clay's line), scored first

| Criterion | Verdict | Claim-Evidence-Verdict evidence |
|---|---|---|
| C1 all explicit requirements | 1 | Sections 1 to 6 hold claim, mechanism, 10 cited facts, cost, risk, gets-right; covers registry in separate repo, one per repo, three in flight, org search |
| C2 edge cases and failures | 1 | Fact 5 "a damaged file can only stop new routing"; fact 6 dead orchestrator restart; fact 3 "100 or more fails closed as truncated" |
| C3 dependencies and prerequisites | 1 | Section 4: second repo, "an absolute path in each host's poll config", "PR B does not exist" |
| C4 success or completion criteria | 0 | No statement of what done or winning looks like; only a list of planned tests (fact 5), not criteria |
| C5 out of scope | 0 | No out-of-scope statement for the paper or the design; "report session takes no issue" is a design fact, not a scope line |
| K1 no factual errors (3+ citations checked) | 1 | Checked DESIGN lines 700, 706, 710, 1159, 891, 893 and `route.py` lines 1-24, 122-129, 603 total: all match |
| K2 feasible within constraints | 1 | "About 8 calls per cycle against a budget of 35"; search limit 30 per minute stated |
| K3 terminology consistent | 1 | "orchestrator", "poll", "report session `coordinator`" kept distinct throughout |
| K4 no internal contradictions | 1 | Section 1 says another orchestrator starts "when the first is full", matching the mechanism; no self-conflict found |
| K5 claims supported | 1 | Every numbered fact carries a DESIGN line or PR-A file reference |
| S1 logical order | 1 | Claim, mechanism, facts, costs, risks, strengths |
| S2 consistent hierarchy | 1 | Six numbered H2 sections, flat lists below |
| S3 separation of concerns | 1 | Cost and risk kept in separate sections |
| S4 navigation aids | 1 | Abbreviation key (DESIGN, PR-A, REQ) and line references |
| S5 artifact-type conventions | 1 | Matches the required position-paper elements in the brief |
| L1 unambiguous language | 0 | Fact 1 "decided by the owner of record in the design" does not say who; diff X-001 shows the rulings belong to another person |
| L2 concrete | 1 | Exact search string, file names, counts (17 issues, 8+5+3+1) |
| L3 clear purpose per section | 1 | Each H2 has a single job |
| L4 terms defined on first use | 0 | "ADD3", "OD8", "E152", "U25", "DQ" used with no key entry; only three abbreviations defined |
| L5 actionable next steps or decisions | 0 | No decision point or next step; ends on "what it gets right" |
| R1 3+ risks with probability and impact | 0 | Section 5 lists 3 risks but gives no probability or impact |
| R2 mitigation per risk | 0 | No mitigation under any of the three risks |
| R3 failure modes and recovery | 1 | Fact 6 "starts ... again with the same tag ... `target.resume: true`"; `registry_invalid` exit 2 |
| R4 external dependencies and their failure | 1 | Section 4: org search limit 30 per minute, "short indexing delay", "fails closed at 100 results" |
| R5 monitoring or validation | 1 | Fact 8 `repos.yaml` validation refuses duplicate `<short>`; `registry_invalid` stops the cycle; test list in fact 5 |
| E1 collection boundaries | 1 | "A result of 100 or more fails closed"; "4-issues-one-repo routing test"; dead one "with nothing in flight is marked ended" |
| E2 state across boundaries | 1 | Entry "written `pending` with its target before anything is sent"; state file name "with no orchestrator id" |
| E3 guard gaps | 1 | Damaged state file counts as in flight; `wrong_target` refusal; tag pattern marked UNVERIFIED |
| E4 count divergence | 1 | 17 issues reconciled as 8+5+3+1; "below `max_in_flight`" and "100 or more" boundaries stated |
| E5 interaction effects | 1 | Section 5: day cap 6 makes many repos "queue up behind it"; two hosts rely on lease comment |

Subtotals (B): Completeness 3/5, Correctness 5/5, Structure 5/5, Clarity 2/5, Risk Coverage 3/5, Invariant and Edge Case 5/5. Total 23/30.

## Variant A (the owner's line), scored second

| Criterion | Verdict | Claim-Evidence-Verdict evidence |
|---|---|---|
| C1 all explicit requirements | 1 | Sections 1 to 6 present; 10 cited facts; covers project-local coordinators, one dispatcher, `orca repo list`, `issue-watch.d`, `COORD-<RepoName>` |
| C2 edge cases and failures | 1 | Section 5 "A bug in the dispatcher touches every project at once"; mitigations per-project lock, kill switch, first-run check leaves failing project `enabled: false` |
| C3 dependencies and prerequisites | 1 | Section 4 "It is not on origin"; fact 5 `orca repo list` verified under cron's empty environment |
| C4 success or completion criteria | 0 | No success or done criteria stated; only the claim that it is built |
| C5 out of scope | 0 | No out-of-scope statement; concessions in section 6 are not scope exclusions |
| K1 no factual errors (3+ citations checked) | 1 | Checked `dispatch.py` 479 lines and lines 52/53, 31 test functions, REQ R16 line 37, R21 "6 repos", Q26 line 3, DESIGN 700/706: all match; `CALL_CAP` line 46 is the master line (49 on the owner's branch), minor |
| K2 feasible within constraints | 1 | Fact 5 cron environment test; fact 9 per-repo budget of 35 per cycle |
| K3 terminology consistent | 0 | Mechanism 3 says "`Coordinator` branch", fact 1 says branch `coordinators`; paper admits "The names are not yet one" and uses both |
| K4 no internal contradictions | 0 | Claim names one session `COORD-<RepoName>` per project; fact 10 says "one coordinator per developer and scope, Q26 `<dev>--<N>`" |
| K5 claims supported | 1 | Each fact cites REQ rows, Q26 lines, `dispatch.py` lines or a command result |
| S1 logical order | 1 | Same required order as the brief |
| S2 consistent hierarchy | 1 | Six numbered H2 sections |
| S3 separation of concerns | 1 | Cost, risk and strengths separate |
| S4 navigation aids | 1 | Key defining REQ, DESIGN, Q26, OWNER-ANSWERS with paths; row references |
| S5 artifact-type conventions | 1 | All required position-paper elements present |
| L1 unambiguous language | 1 | Section 6 "The dispute is only where the session and the records live"; open naming questions are flagged as open, not blurred |
| L2 concrete | 1 | Constants, line numbers, `git ls-remote` hash, "223 entries", six repos named |
| L3 clear purpose per section | 1 | Each H2 has one purpose |
| L4 terms defined on first use | 0 | "ADD2", "ADD3", "dispatcher", "day cap", "kill switch" used without definition |
| L5 actionable next steps or decisions | 1 | Cost: "The spec must pick one" name; section 6 lists what to carry across ("can be carried into the per-project layout") |
| R1 3+ risks with probability and impact | 0 | Section 5 has two risks, no probability or impact |
| R2 mitigation per risk | 0 | Dispatcher risk has mitigations; standing-session cost risk has none (marked UNVERIFIED) |
| R3 failure modes and recovery | 1 | "restarted if stopped"; child killed after 255 s; failing project left `enabled: false` |
| R4 external dependencies and their failure | 1 | Cron minimal environment, Orca list, account rate-limit wait (mechanism 2, fact 5) |
| R5 monitoring or validation | 1 | "checked at boot and on every watcher run"; `run-all --dry-run`; origin check before every launch |
| E1 collection boundaries | 1 | `LOOP_CAP_S = 270.0` stops starting children; "A repository not reached"; one launch per sweep caps a burst |
| E2 state across boundaries | 1 | Origin check before every launch; claims folder one create-once file per item, each coordinator folder one writer |
| E3 guard gaps | 1 | Section 4 "no in-flight cap per coordinator and no idle end"; branch protection UNVERIFIED (Q26) |
| E4 count divergence | 1 | "31 test functions; the REQ ledger row ... counts 42 cases"; `coordinators` vs `Coordinator` |
| E5 interaction effects | 1 | "A bug in the dispatcher touches every project at once"; PR 686 "rewrites six of the same files" |

Subtotals (A): Completeness 3/5, Correctness 3/5, Structure 5/5, Clarity 4/5, Risk Coverage 3/5, Invariant and Edge Case 5/5. Total 23/30.

TOTALS: B=23/30 A=23/30
