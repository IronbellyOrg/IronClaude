# QA Report: master-contract fidelity lens (Phase 12 edits)

**Date:** 2026-11-12
**Reviewer:** qa-master-contract (rf-qa), fix_authorization: false
**Scope:** `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`, guide line in `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, compared with master `5dc29d23` (`git diff HEAD`).

## Findings

No BLOCKING or MAJOR finding. I found no master test or rule that the Phase 12 edits break. Two MINOR notes follow; MINOR findings never fail the gate.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `src/superclaude/core/WORKER-CONTRACT.md:110` ("After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep") against `:277` ("On every coordinator wake, at most once every 5 minutes, ... runs `/sc:sweep`") | Master's sweep runs after a wake or a timeout; WC-16 ties `/sc:sweep` to a "wake" only and, in the preceding sentence, says an expired wait is re-armed. A reader can take it that `/sc:sweep` is skipped on a timeout while "The sweep." still runs. The text is byte-identical to DESIGN section 8 (`docs/designs/orchestrator-mode.md:677-679`) as the owner approved it (OQ-3), and WC-16 says the same pass runs "The sweep." unchanged, so no master pin or rule is broken. | None for this gate. If the owner wants it closed, change "On every coordinator wake" to "After every wake or timeout" in a later design revision (this would change a pinned phrase, `RULE_PHRASES["WC-16"]` at `tests/skills/test_worker_contract.py:173`). |
| F2 | MINOR | `WORKER-CONTRACT.md:277` ("Its own reads are not L1 probes and do not count against the L1 cap") against `:110` ("Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep") and `:151` ("at most 2 costly probes per triggered worker per sweep") | WC-16 declares an exception: `/sc:sweep` reads transcripts and sessions outside the L1 cap. Lines 110 and 151 are untouched and their pins pass, so the master text is not reworded, but the combined contract now has a carve-out the master lines do not mention. It is stated in WC-16's own words, was added by design fix R4, and is covered by the owner's OQ-3 approval. | None needed; recorded so the reader knows the carve-out is deliberate. |

Evidence quality note (not a defect in the product): `phase-outputs/test-results/step-1.17-checks.md` Check 2 counts `^### WC-14`, which matches nothing on master either (WC-14 is a bullet at `:63`), so it proves nothing by itself. My own checks C7 and C8 below cover the real concern.

## Checks

All evidence below was read or run on disk in this session (contract read in chunks of at most 150 lines; `git show HEAD:...` compared with `diff`/`cmp`; mutations ran in memory against the text of the contract, with working copies under /tmp deleted afterwards).

| id | check and evidence | result |
|---|---|---|
| C1 | `_check_rule` (`tests/skills/test_worker_contract.py:765-772`): `RULE_PHRASES` has 58 keys with no duplicate key (AST scan), so the new `"WC-16"` key (:173) does not override `"WC-14"` or `"WC-15"`. `_check_rule` passes for WC-14, WC-15 and WC-16 on the real contract. The heading line 275 carries both ident and first phrase. Mutation: removing the heading is caught. | PASS |
| C2 | `_check_repo_setup_gated` (:823-838): the WC-16 paragraph (contract :277) has no `--setup`/`--run-hooks` flag and no launcher code span (only `/sc:sweep` and `worktree ps --agent-wait`, neither in the launcher list). Test passes in the 742-test run. Mutation: inserting a `uv run ...` span in WC-16 is caught, so the check still bites. | PASS |
| C3 | `_check_never_as_worker` (:775-781): one term line (contract :23); every `NEVER_AS_WORKER` entry, now 9 including `/sc:sweep` (:400), appears in backticks. The renamed test `test_never_as_worker_list_names_every_listed_command` runs the same check. Mutation removing `/sc:sweep` from line 23 is caught. `RULE_PHRASES["never-as-worker"]` (:86) matches line 23 word for word (test passes). | PASS |
| C4 | `_check_no_unattended_sections` (:841-849): `src/superclaude/commands/sweep.md` has 0 `## Unattended mode` headings (`grep -c`), and `COMMANDS_DIR` is `src/superclaude/commands`. The new assertion `"sweep" not in UNATTENDED_COMMANDS` (:1333) holds. | PASS |
| C5 | `_check_p2_set` / `UNATTENDED_EXPECT`: `len(UNATTENDED_EXPECT) == 31` now and 31 on master (`git show HEAD:tests/...`); no duplicate key; `sweep` is not a key; the diff does not touch the dict. | PASS |
| C6 | Write-verb audit: `AUDIT_ROOTS` (:1951-1955) is skills, commands and agents only, so the contract is not scanned. `WRITE_VERB_CLASSIFICATION` (:2027) is not in the diff, and `test_every_write_verb_hit_is_classified` and `test_classification_table_has_no_stale_entries` pass (547-test selected run and 742-test full run). No classification row was added or needed. | PASS |
| C7 | Liveness pins: contract lines 110 and 151 are byte-identical to master (`cmp`); the line 110 pin phrase "at most once every 5 minutes, the coordinator runs one sweep" (test :221) and the line 151 pin phrase "Every sweep; at most 2 costly probes per triggered worker per sweep" (test :240) pass. Mutations rewording either line are caught. Whole-file compare: master lines 1-273 except 23, and master 275 to end against now 279 to end, are identical, so the only contract changes are line 23 and the 4 inserted lines 275-278. | PASS |
| C8 | WC-14 references not renamed: lines 63 (rule), 124 (S6 "the WC-14 exception") and 213 (Chain) are byte-identical to master; the template Chain line is master :289, now :293, identical. `grep -n "WC-14"` on the contract shows exactly lines 63, 124, 213 and 293. No heading `### WC-14. Coordinator loop` exists. | PASS |
| C9 | No WC-9 lock-retry text (IronbellyOrg/IronClaude#446): WC-9 (:41-45) is untouched by the diff; the added lines contain no lock, retry-lock or 446 text (the only `lock` substring in added lines is "blocked"). | PASS |
| C10 | WC-16 text equals DESIGN section 8 final text: `sed -n 275,277p` of the contract and `sed -n 677,679p` of `docs/designs/orchestrator-mode.md` are `cmp`-identical. The heading is `### WC-16`, the next free id after master's WC-14 and WC-15 (master has 0 WC-16 hits). Placement is after the fan-in paragraph and before the worked example, as DESIGN section 8 specifies. The OQ-3 record is `status: RESOLVED` with the owner's direct decision (`OQ-3-GQ-11-rule-id-decision.md:36-39`). | PASS |
| C11 | Line 23 matches DESIGN section 8 "Never-as-worker addition" (`orchestrator-mode.md:705`) word for word, including the unchanged D3 sentence. OQ-1 (`worktree ps --agent-wait` allowed) is consistent: WC-16 says `/sc:sweep` does not run that listing, and line 110 is not edited, as the OQ-1 record's "Applied by" requires. | PASS |
| C12 | R7 guide edit: `git diff` shows one line changed (guide :991), adding `/sc:sweep` between `/sc:spawn` and `/sc:swarm-wizard`; the order equals contract line 23. The guide bullet at :993 still tells maintainers to edit `NEVER_AS_WORKER`, which now holds the entry. A repo-wide grep for the old list wording found no other stale copy outside `.dev`, `.claude`, `docs/designs` and the installed `.venv` copy. | PASS |
| C13 | Test-file diff scope: only the five design pins (never-as-worker phrase, `"WC-16"` entry, `NEVER_AS_WORKER` entry, test rename, `"sweep" not in UNATTENDED_COMMANDS`). No pin was loosened or removed; no other test body changed. | PASS |
| C14 | Runs: `uv run pytest tests/skills/test_worker_contract.py` gives 742 passed; `uv run pytest tests/skills tests/core` gives 2008 passed (matches `phase12-validation.md` Check 3 and `step-1.19-pytest.txt`); `uv run ruff check` and `uv run ruff format --check` on the test file pass. | PASS |
| C15 | Semantic fit of WC-16 with master rules (WC-6, WC-10, "Never on silence", contract :244, :246, :250, :273): the escalation list matches those lines; "missing heartbeat is absence, never death" matches WC-10; WC-16 authorizes no action on silence. Two ambiguities are recorded as MINOR F1 and F2; neither breaks a master test or rule text. | PASS (with notes) |

Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 9 | Grep: 1 (plus grep inside Bash) | Glob: 0 | Bash: 7 (diff/cmp against `git show HEAD`, pytest, ruff, in-memory mutations)
Files written: this report only. The /tmp working copies were deleted.

Verdict: PASS

Blocking count: 0
