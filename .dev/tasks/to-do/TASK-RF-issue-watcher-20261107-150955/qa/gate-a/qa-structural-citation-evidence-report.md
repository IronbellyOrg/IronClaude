# QA Report - Gate A, citation-evidence lens

**Topic:** issue-watch implementation (Phases 2 and 3)
**Date:** 2026-11-07
**Phase:** task-integrity / citation evidence (fix_authorization: false, report only)
**Fix cycle:** N/A

## Overall Verdict: FAIL

Three blocking findings (B-1, B-2, B-3) and ten minor notes. Only the blocking findings drive the verdict. Every other citation I opened resolves and says what it claims.

Scope read: `gate-a-change-set.md`, the 4 source files (`runner.py`, `predicates.py`, `audit.py`, `github.py`), the 4 test files plus `conftest.py`, all 11 `_assumed_shape` fixtures, design lines 212-272, 490-730 and 815-860, spec-final lines 80-115, 118-221 (FR/NFR rows) and 326-361, and research 06 rows DF-01 to DF-60 and Table 1.5.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Design line anchors cited in code and tests (554, 556, 575, 590, 718, sections 8.1 to 8.5) | PASS | Opened design 541-602 and 718: line 554 is the `--method GET` rule, 556 the body-access rule, 575 the GraphQL completeness rule, 590 the UNVERIFIED stderr table, 718 the never-keys list; `FORBIDDEN_KEYS` (test_audit.py:163) matches 718. |
| 2 | DF-nn citations resolve to a row that says what the citation claims | PASS | Read DF-01, 02, 03, 14, 16, 18, 19, 21, 22, 28, 31, 32, 35, 37, 55, 57 in research 06 (lines 24-37, 143-164, 189-191). All cited uses match, except the minor DF-32 wording (M-4). |
| 3 | Spec FR/NFR citations (FR-002 to FR-011, FR-023, FR-028, FR-029, NFR-002 to NFR-009) | PASS with notes | Opened the rows (spec lines 118-221). Wrong ids only at test_predicates.py:376-377 (M-1) and test_github.py:140 (M-2). |
| 4 | AC-nn citations (AC-2, 3, 13, 14, 17) | PASS | design lines 874-898 map AC-2 to FR-003/004, AC-3 to FR-005/006, AC-13 to FR-019, AC-14 to FR-020/NFR-006, AC-17 to FR-026/021. |
| 5 | Spec reason table range "330-358" and the 57-name count | PASS | Counted spec lines 332-358: 52 names; plus the five DF proposals (`marker_unreadable`, `edits_unreadable`, `operator_reset`, `dry_run_shadow_reset`, `reset_refused`) = 57; `audit.REASON_TABLE` has the same names, kinds and exits (audit.py:19-89). |
| 6 | Every fixture has `_assumed_shape` true and a non-empty `source` | PASS | Printed all 11 files; test_github.py:491-498 also asserts it. |
| 7 | Fixture `source` anchors name the right design row and line | PASS with notes | Lines 834, 835, 836, 837, 838, 545, 546, 585, 586 all exist and say what is cited, except M-3 and M-9. |
| 8 | No UNVERIFIED reply shape stated as fact outside an `_assumed_shape` fixture (design 829-847) | FAIL | B-2 (src comment) and B-3 (tests). |
| 9 | The `_assumed_shape` fixtures actually pin the shapes (design 560, 636, 847; research 05 section 3 table, column "Consumed by") | FAIL | B-1: 5 of 11 fixtures are never read by any test. |
| 10 | No model-alias string and no `SuperClaude-Org` outside a negative needle | PASS | Case-insensitive Grep over `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` for `SuperClaude-Org`, `claude-(opus\|sonnet\|haiku\|fable)`, the bare model names, `gpt-`, `gemini`: one hit, test_github.py:271 (`assert "SuperClaude-Org" not in element`, a negative needle). |
| 11 | jq and GraphQL constants equal the design and research 06 Table 1.5 | PASS | `EVENTS_JQ`, `MARKER_JQ`, `REREAD_JQ` equal design 545, 546, 549; `EDITS_QUERY`, `PROJECT_ITEMS_QUERY` equal research 06 lines 92-124. |
| 12 | Change set inventory, line counts and decision-row list | PASS with note | `wc -l` and `find` match every row of gate-a-change-set.md (22 files, 4666 lines in total). M-7: the decision list omits rows the files cite or apply. |
| 13 | `OQ-37` and `OQ-38` cited in predicates.py resolve | PASS with note | Defined only in the task file (lines 952-953), and they say what the code does; see M-5. |

## Summary
- Checks passed: 11 / 13 (3 of them with minor notes)
- Checks failed: 2 (items 8 and 9)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 3
- Minor notes: 10
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found

### Blocking findings

| id | severity | file | evidence | expected versus actual |
|----|----------|------|----------|------------------------|
| B-1 | IMPORTANT (blocking: a missing required deliverable) | `tests/issue_watch/fixtures/_assumed_shape/gh_issue_list.json`, `graphql_edits.json`, `graphql_project_items.json`, `rest_comments_marker.json`, `rest_events_page.json`; `tests/issue_watch/test_github.py` | Grep for the five file names across `tests/` and `src/` returns no match. `load()` (test_github.py:46-48) is called only for `gh_api_user_include`, `gh_stderr_auth_401`, `gh_stderr_rate_403`, `gh_stderr_rate_429`, `gh_graphql_insufficient_scopes` and `gh_graphql_rate_limited` (lines 309, 325, 339, 353-357, 464, 472, 478, 1040). The only test that touches the five is `test_every_assumed_shape_fixture_parses_and_is_labelled` (line 491), which checks marker and source, not content. The G2, G3, G4, G5 and G6 reads are tested only against inline helpers: `discovered` (1130-1137), `event_item` (520-532), `marker_item` (535-545), `gql`, `comment_node`, `item_node`, `edits_page`, `project_page` (840-878). | Expected: design 560 says the G5/G6 reply shapes "are pinned by `_assumed_shape` fixtures"; design 636 says the same for the Orca id path; design 847 says each UNVERIFIED answer is recorded in the matching `_assumed_shape` fixture; research 05 section 3 lists these files as "Consumed by `test_github`, `test_predicates`"; FU-1 (design 853) replaces "every `_assumed_shape` fixture". Actual: a real capture dropped into any of the five files changes no test result, so the replace-and-recheck step in FU-1 cannot detect a wrong assumption for discovery, events, comments, edits or Project items. Fix: have the tests build their replies from these fixtures (for example `ok(load("rest_events_page.json")["payload"])`), or delete the files and record where the assumed shape now lives. |
| B-2 | IMPORTANT (blocking: an UNVERIFIED reply shape stated as fact; the lens criterion for design 829-847) | `src/superclaude/cli/issue_watch/github.py:713` | `status = d.get("fieldValueByName")  # null when Status is unset or not single-select`. Design line 837 marks `fieldValueByName` UNVERIFIED ("none in repo ... run `PROJECT_ITEMS_QUERY` once"); design 560 marks the whole G6 reply shape UNVERIFIED. The query (github.py:93-95) uses an inline fragment `... on ProjectV2ItemFieldSingleSelectValue { name }`; for a field value of another type a GraphQL inline fragment normally returns an empty object, not null, so the comment is both unverified and probably wrong. Nothing in the repo records either behaviour. | Expected: any statement of what GitHub returns for an UNVERIFIED shape is either inside an `_assumed_shape` fixture or tagged `[UNVERIFIED]` like github.py:69-70 and 224-225. Actual: stated as fact. The code itself is safe (`_opt_text(_obj(status).get("name"))` returns None for both `null` and `{}`), so the fix is the comment: tag it `[UNVERIFIED]` or say "None when absent or empty". |
| B-3 | IMPORTANT (blocking: same lens criterion as B-2, in the tests) | `tests/issue_watch/test_github.py:58-62, 331, 342, 355, 368, 374, 378, 840-867, 1018, 1029` | Inline literals that stand in for gh and GraphQL replies the design marks UNVERIFIED (design 835 layout, 838 stderr text, 837 GraphQL shape) with no `_assumed_shape` marker: `g1_result` docstring "A G1 result: status line, `headers`, a blank line, then a JSON body" and the literal `HTTP/2.0 429 Too Many Requests` with headers `Retry-After` and `x-ratelimit-reset` (the entire `rate_limit_wait` and `retry_after` test matrix at lines 403-457 runs on it, and no fixture holds a G1 reply with `Retry-After`); stderr strings `To get started with GitHub CLI, run: gh auth login` (331), `gh: your token has not been granted the required scopes: read:project` (342), `gh: HTTP 403: Secondary RATE LIMIT hit` (355), `gh: HTTP 403: Resource not accessible` (368), `gh: HTTP 502: Bad Gateway` (374), `gh: HTTP 404: Not Found` (378); the `gql`, `comment_node`, `item_node` helpers and the inline `errors` bodies (1018, 1029). No fixture exists for a 5xx reply or for a G1 reply with `Retry-After`. | Expected: design 847 "The implementer records each UNVERIFIED answer in the matching `_assumed_shape` fixture"; the lens rule allows these shapes only inside an `_assumed_shape` fixture. Actual: the shapes that drive `classify`, `retry_after`, `rate_limit_wait` and `_graphql_read` tests are written inline and unlabelled, so FU-1 will not find them. Fix: move each literal into a fixture (add `gh_stderr_5xx.json` and a G1 `Retry-After` fixture) or add a one-line `# [UNVERIFIED, assumed shape]` comment tied to the design row at each helper. This shares a remedy with B-1. |

### Minor findings (notes only, not rechecked)

| id | severity | file | evidence | expected versus actual |
|----|----------|------|----------|------------------------|
| M-1 | MINOR (citation id) | `tests/issue_watch/test_predicates.py:376-377` | Test name `test_fr003_intended_owner_is_exactly_own_login` and docstring "FR-003: only the set {own login} is the intended owner." FR-008 (spec line 139) is the intended-owner rule; design AC-4 (line 877) maps owner tables to FR-007, FR-008. FR-003 (spec line 121) is the discovery argv. | Expected FR-008. Actual FR-003. |
| M-2 | MINOR (citation id) | `tests/issue_watch/test_github.py:140` | `test_g5_argv_first_page_has_no_cursor__fr003`. G5 is the edit-timestamp read (design 547, "Section 3 Unchanged"), part of FR-005; FR-003 is discovery. | Expected FR-005. Actual FR-003. |
| M-3 | MINOR | `fixtures/_assumed_shape/rest_comments_marker.json` `source` | Cites the section 15 row "REST events fields" (line 836), which covers events only. Section 15 has no row for comment fields; the G4 anchor (line 546) in the same string is right. | Name G4 (design 546) and say no section 15 row covers comment fields. |
| M-4 | MINOR | `test_github.py:5, 488`; `github.py` has none | "the `_assumed_shape` fixtures (DF-32)". DF-32 (research 06 line 159) only requires that fixtures parse with `json.loads` and carry placeholder ids; their names and shapes come from DF-49 (line 183). | Cite DF-49 for the fixtures, DF-32 for the parse test. |
| M-5 | MINOR | `predicates.py:204, 227` | Cites `OQ-38` and `OQ-37`. Both are defined only in the task file (TASK-RF-issue-watcher-20261107-150955.md lines 952-953) and say what the code does, but the id means nothing in the design or the spec. | Add the one-line rule next to the id, or cite the task file path. |
| M-6 | MINOR | `fixtures/_assumed_shape/gh_stderr_auth_401.json` | Records `"exit": 1`, while DF-37 (research 06 line 164) records that gh exits 4 when authentication is needed. Inside an assumed fixture and `classify` ignores exit codes, so no behaviour changes, but the two assumed facts disagree. | Align the fixture with DF-37 or note the disagreement in `note`. |
| M-7 | MINOR | `phase-outputs/reports/gate-a-change-set.md:45` | "Decision rows applied" omits DF-24 (`FakeClock(now, mono)`, `FakeLauncher` names, conftest.py:40-60), DF-31 (test_audit.py:6), DF-32 (test_github.py:5), DF-49 (fixture names) and DF-56 (conftest split by phase). | Add the rows so the change set matches the files. |
| M-8 | MINOR (wording) | `github.py:354`; `audit.py:1-7` | `retry_after` docstring says None "when absent"; the code also returns None for an unparseable or negative value (the tests at 407-411 cover that). The audit module docstring says "no issue text can reach a line", but `_TYPES` (audit.py:165-184) checks only the type of `state`, `host`, `login`, `ts`, `cycle_id` and `approved_at`, while design 712 makes `state` an enum. | Reword both. |
| M-9 | MINOR | `fixtures/_assumed_shape/graphql_edits.json` `source` | Cites design section 15 line 837, a row about `userContentEdits`; `EDITS_QUERY` (github.py:72-83) and the fixture use `createdAt` and `lastEditedAt`, and never request `userContentEdits`. The design itself is inconsistent (row 837 versus G5 at line 547). | Note in `source` that the row names `userContentEdits` while the query follows design 547. |
| M-10 | MINOR | `predicates.py:279-292`; `test_predicates.py:519-523` | `eligibility_order` and its test cite FR-023 for "several new issues sort by number" and "ties sort by number". FR-023 (spec line 166) says "oldest first, never-examined first" and gives no tie rule. | Mark the number tie-break as a local choice. |

---

## Actions Taken
None. fix_authorization was false; the only file written is this report. I read the source, tests, fixtures, design, spec and research files and did not modify them.

## Recommendations
- Resolve B-1, B-2 and B-3 together: wire the five unused fixtures into `test_github.py` (and `test_predicates.py` where research 05 expects it), add the missing 5xx and G1-`Retry-After` fixtures, and tag or reword the github.py:713 comment. Then re-run G-1 (`uv run pytest tests/issue_watch/ -v`) and the ruff gate on the changed files.
- Fix M-1 and M-2 in passing, since both are one-token edits in files that B-1 and B-3 touch.

## Confidence and tool engagement
- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 26 | Grep: 17 | Glob: 1 | Bash: 5 (Read + Grep + Glob = 44 calls against 13 checklist items)
- Not verified: the live behaviour of gh and GitHub GraphQL (no network call was made; B-2's "probably wrong" is a reading of GraphQL inline-fragment semantics, not an observed reply). Tests and gates were not re-run; that belongs to the gate-command lens.

## QA Complete
