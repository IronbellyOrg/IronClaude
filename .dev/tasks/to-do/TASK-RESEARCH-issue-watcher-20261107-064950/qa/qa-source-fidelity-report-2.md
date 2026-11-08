# QA Report - Source-Document Fidelity (fidelity-agent-2)

**Status:** Complete
**Date:** 2026-11-07
**Phase:** source-fidelity
**Report under review:** `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md`
**Fix authorization:** false (report only)

---

## Progress log (appended incrementally)

### Part 1: codebase claims re-verified directly against source (report Section 2.3 vs file 02 vs code)

Method: read file 02 in full, read report Sections 1, 2.3 and research-notes ADDENDA, then re-ran greps/reads on the source files. All of these matched the report:

| Claim in report | Source check | Result |
|---|---|---|
| `.github/workflows/` holds exactly README.md, boundary-guard.yml, contract3-...yml, test.yml; triggers test.yml:3-8, boundary-guard.yml:25-33 (5 paths), contract3 22-29 | `ls`, `grep -n` on workflows | MATCH |
| No `schedule:`/`cron:`/`issues:`/`workflow_run`/`pull_request_target` anywhere in workflows | `grep -rnE` over `.github/workflows/` returned no match (rc=1) | MATCH |
| test.yml job skeleton lines (checkout@v4 l.17; setup-uv@v10.3.2 l.20-23; `uv pip install -e ".[dev]"` l.29/72/98; `make sync-dev` l.38; `permissions: contents: read` l.151-152; `persist-credentials: false` l.158; `test-summary` l.191-200, `needs` l.194) | `grep -n` on test.yml | MATCH |
| Makefile `test` 13, `lint` 48, `format` 53, `sync-dev` 109, `verify-sync` 166, `verify-deps` 356, `lint-architecture` 362; CI counterparts test.yml:46-47, 100-102, 104-106, 116-123, 127-135 | `grep -nE '^target:'` Makefile + test.yml | MATCH |
| `.github/workflows/README.md` "Adding a New Workflow" l.120; pin versions l.141; `workflow_dispatch` l.143 | grep -n | MATCH |
| Issue forms: bug_report `type: Bug`, `labels: bug`; feature_request `type: Feature`, `labels: enhancement`; other.yml none; config.yml `blank_issues_enabled: false` | read of heads of 4 files | MATCH |
| Live fork labels = the 9 GitHub defaults | `gh label list --repo IronbellyOrg/IronClaude --limit 100` re-run 2026-11-07: exactly bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix | MATCH |
| `gh issue list` JSON fields include `issueType`, `projectItems`; gh 2.103.3 | `gh issue list --help`, `gh --version` | MATCH |
| `ci.py` imports only `re`, `.classifier`, `.models` (l.10-15); docstring says pure; no subprocess anywhere in `src/superclaude/pr_submit`; 21 files in package | `sed`, `grep -rn subprocess` rc=1, `ls` | MATCH |
| `detection._fetch_payload` l.273-275 stub, comment l.267-270; `conftest.py:58` monkeypatch; `mock_gh` used in 3 test files, 6 occurrences | `sed`, grep counts (1+3+2) | MATCH |
| `conftest.py:3-4` stale docstring vs code l.38-59 (records `pr_num`, no `--repo` pin) | read | MATCH (STALE DOC correctly flagged) |
| 21 files in `src/superclaude` import `subprocess`; only `.py` hit for literal gh is `origin_repo.py:14` docstring; no `shutil.which("gh")` | grep -rl, grep -rn | MATCH (list of 21 identical) |
| `origin_repo.py` `_NUMBER` l.74, `check_claim` l.102-153, `read_origin` l.156-174, `ClaimError` l.77-83, `main` l.177-191, exit codes l.45-50 | read | MATCH |
| `main.py` 11 registrations l.519-561 with `# noqa: E402,I001` marker; `cli_portify_group` no `name=`; `version` l.513-516; `__main__` l.564 | read | MATCH |
| `pyproject.toml` console script l.70-71, packages l.78-79, testpaths l.107-116 (strict-markers l.114), ruff l.173-186, deps l.34-43, requires-python l.16 | `grep -n` | MATCH |
| `recommend/` 12 files 1,784 lines, `__getattr__` lazy export, `@click.group("recommend")` l.34-35, nested groups l.51/145/196; `tasklist/__init__.py` lazy export; `init_lite.py` 359 lines, `@click.command("init-lite")` l.285 | `wc -l`, read | MATCH |
| `cleanup_audit/__init__.py` eager import; `--dry-run` returns before side effects l.85-87 | read | MATCH |
| `tests/cli/test_cli_registration.py` EXPECTED_TOP_LEVEL_COMMANDS lacks `swarm` and `reflect` though both are registered; comment l.28-30 claims forced update; test at l.95-106 only runs `--help` | read | MATCH (CODE-CONTRADICTED correctly reported) |
| PATH-stub gh pattern in 5 files (test_conflict_e2e, test_conflict_scripts, test_codex_reviews, test_static_grep, test_cosmos_poll); `assert_no_retrigger_call` rejects write tokens; `ALLOWED_PROGRAMS` test_conflict_sync_protocol.py:40 | grep -rn "gh" tests, read | MATCH |
| `install_user_setup.py` `_ORCA_CLIS` l.35, `_find_orca` l.198-221 with `subprocess.run([path,"skills","list","--json"],...,timeout=10,stdin=DEVNULL)`, GNOME screen reader docstring, `install_orca_skills` from l.230 | read | MATCH (the function itself ends l.278; report's "l.230-263" covers the subprocess part, not blocking) |
| `doctor.py:61-77` ccsession-orca filesystem check | read | MATCH |
| `claim.md` l.13-16 Wave 0, l.26 field list, l.35-43 edge cases (l.41 other assignee STOP, l.42 own login idempotent), l.47 `--add-assignee @me`, l.85-87 PATCH; `labels.md` l.7, 9-13, 20, 22-42 | read with line numbers | MATCH |

Minor nits found so far (not blocking):
- MINOR M1: report Section 2.3 / file 02 cite `bug_report.yml:29,41-43` for `orca_version`; the `id: orca_version` is at line 28 (line 29 is `attributes:`). Off by one on a true claim.
- MINOR M2: report cites `install_orca_skills (l.230-263)`; the function ends at l.278. The subprocess-running part is within the cited range.

### Part 2: external sources re-fetched (Tavily not available in this agent's tool list; WebFetch used, auditable fallback)

Provider note: no `mcp__tavily__*` tool exists in this agent's runtime tool list, so every external check used WebFetch (reason: tavily-unavailable). WebFetch returns model-written summaries of the page, so the quoted wording below is the tool's rendering.

| # | URL re-fetched | Report claim compared | Result |
|---|---|---|---|
| 1 | https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows | 5-minute floor, delay and dropped queued jobs, default branch only, 60-day public-repo disable, the 20 `issues` activity types, `projects_v2_item` absent, "Not all webhook events trigger workflows" (Sections 5.1, 6.2) | MATCH on every item (activity list identical, 20 types) |
| 2 | https://raw.githubusercontent.com/coder/terraform-provider-coder/main/docs/resources/script.md (the registry.terraform.io page returned only "Terraform Registry", a JS shell; raw provider doc used instead) | `cron` six fields seconds first, `run_on_start` readiness, `timeout` default 0, example `0 */5 * * * *`, `coder_script_order` needs v2.39 (5.7, 6.1) | MATCH |
| 3 | https://code.claude.com/docs/en/headless | "User-invoked skills and custom commands work... `/skill-name`... expands"; `--bare` skips hooks/skills/custom commands and "will become the default for `-p`"; Manual mode default from v2.1.302; hooks in `.claude/settings.json` run in a never-trusted folder (5.9) | MATCH (quotes verbatim) |
| 4 | https://docs.github.com/en/rest/issues/assignees | "Users already assigned to an issue are not replaced", up to 10 assignees, silent disregard without push access, no conditional-request/compare-and-set mention (5.12) | MATCH |
| 5 | https://cli.github.com/manual/gh_project_item-list | flags `--owner`, `-L` default 30, `--query` "if supported by the API host", no scope mentioned (5.3) | MATCH on flags and defaults; **the page also shows status filters in `--query` examples (`assignee:octocat -status:Done`, `label:bug -status:Done`): see finding F1** |
| 6 | https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api | 5,000/h user, GITHUB_TOKEN 1,000/h per repo, App 5,000 base +50 beyond 20 cap 12,500, 100 concurrent, 900 points/min REST, 80/min and 500/h content creation, headers, 60-second wait/backoff (5.4) | MATCH |
| 7 | https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api | prefer webhooks, honor `x-poll-interval`, etag/`if-none-match` 304 consumes no primary allowance, sequential calls, one second between writes, retry-after/60 s/exponential backoff (5.4) | MATCH |
| 8 | https://coder.com/docs/reference/cli/ssh | runs a command, stopped workspace auto-starts unless `--disable-autostart` (5.8) | MATCH |
| 9 | https://github.com/coder/create-task-action | inputs, Coder 2.28+, `coder` label example, GitHub user id lookup via OAuth link, token needs org-wide user read and task launch for other users, no caller authorization described (5.10) | MATCH (page also lists 4 optional inputs; the report lists the required ones only, not a distortion) |
| 10 | https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ | version 08, 422 for same key different payload, 409 concurrent, consistent response after completion (5.12, 5.15) | MATCH (page date 22 October 2026, expiry 25 April 2027) |
| 11 | https://docs.github.com/en/rest/issues/events | mandatory `actor`, `label` {name,color}, per_page 30/100, no retention stated (5.6) | MATCH |
| 12 | https://coder.com/docs/user-guides/workspace-scheduling | activity bump 1 hour, qualifying activity list, excluded activity, no default TTL, Premium mandatory stop and dormancy (5.7) | MATCH |
| 13 | https://coder.com/docs/admin/networking | agents initiate HTTP(S) to `CODER_ACCESS_URL`, no fixed inbound port, STUN 3478, DERP, browser statement, E2E encryption (5.8) | MATCH |
| 14 | https://code.claude.com/docs/en/github-actions | write-access gate, `allowed_non_write_users`, `allowed_bots`, schedule default-branch and 60-day text, auth options, prompt accepts skill, App permission set, "GitHub doesn't let you accept a subset" (5.9) | MATCH (page adds that scheduled events skip the write-access check but not the human-actor check; consistent with the report's "dispatch and schedule events get no separate check" from W02) |
| 15 | https://docs.github.com/en/rest/search/search | 30 req/min, 10 for code/semantic, per_page 100, 1,000 results, `incomplete_results` on timeout (5.5) | MATCH |
| 16 | https://docs.github.com/en/organizations/.../repository-roles-for-an-organization | Triage lowest role for labels and assign; Read can open/comment/receive assignment; Write lowest role to create/edit/delete labels (5.6, 7.1) | MATCH (this also closes the "search-result summary, not separately fetched" caveat on label creation) |
| 17 | https://raw.githubusercontent.com/coder/terraform-provider-coder/main/docs/resources/app.md | `share` valid levels `owner` (default), `authenticated`, `public`; `subdomain` default false, wildcard needed (5.14) | MATCH |

Also re-run locally (read-only): `gh issue list --help` (flags/JSON fields), `gh project item-list --help` (example `--query "assignee:@me is:issue is:open"` supports the report's "form of the help example" remark), `orca agent launch --help` (retry note text verbatim as quoted in Q3; spec file `agent-launch.js` lines 9, 19, 27 present), `gh api repos/cli/cli/contents/pkg/cmd/project/shared/queries/queries.go?ref=v2.103.3` (`Issue.ExportData` at l.558-566 exports `body`, `title`, `number`, `repository`, `url`; `ProjectItem.ExportData` at l.673-678 exports `id`, `title`, `body`, `type`: matches the report's SC-5 / Phase 4 "`--jq` is mandatory" claim exactly), `gh api .../issues/331/events` (oldest first: first 2026-10-30T14:39:35Z, last 2026-11-07T06:48:14Z, as the plan states).

Re-fetched URLs: 17 (requirement was at least 6). One fetch (registry.terraform.io script page) returned no content and was replaced by the raw provider doc of the same text.

### Part 3: the F1/F2 edits (Section 8 Phase 3 step 3.4, Phase 5 step 5.1/5.2/algorithm step 3/4, the new test row, test plan row for `test_cli_once.py`)

The Gate-3 note at report line 1443 says these edits were not reviewed a fourth time. Checked directly:

- F2 (call-time `which` lookup). `resolve_orca(orca, *, which=None, names=...)` resolves `lookup = shutil.which if which is None else which` at call time (step 3.4); `launch_claim(..., which=None)` passes it to `resolve_orca`; `run_cycle(..., which=None)` is handed on at algorithm step 12 (`launch_claim(... which=which)`) and repeated in step 5.2; step 3.6 tests always pass a fake `which`; the `test_cli_once.py` row of the test plan says the patch takes effect "because `which` defaults to `None` and is resolved to `shutil.which` at call time"; Phase 6 step 6.2 restricts `PATH` to the stub directory and runs the verb with the default `which=None`. All five places agree. The stated Python reason (a default argument bound in the signature is fixed at import time, so a later patch has no effect) is correct. `which -a` host facts: the report says `which -a orca-ide` lists `/home/coder/.local/bin/orca-ide`; the live output also lists `/usr/bin/orca-ide` and `/bin/orca-ide` (see M3), which does not change the argument (the report's conclusion is "both names resolve on the real PATH").
- F1 (`considered` map). Step 5.1 defines `load_considered`/`record_considered` and the map; algorithm step 3 sorts "never examined first, then oldest `considered`, ties by ascending number" after the local-skip drop and before the cap; algorithm step 4 stamps every examined number; the test "Unhandled issues cannot monopolize the cap" works through its own arithmetic correctly: 15 unapproved issues + issue 99 = 16 results, cycle 1 examines 1-10 (all never-examined, ascending), cycle 2 sorts never-examined 11-15 and 99 first (6 issues) and fills the remaining 4 slots with the oldest-stamped of 1-10, so 99 is examined and launched in cycle 2; cycle 3 examines the oldest-stamped first. The text in step 3 ("window rotates... one slice per cycle") is consistent with that. No contradiction with the "Many already-handled candidates" test (that test relies on the local-skip drop before the cap, which the algorithm keeps).
- Internal references: Phase 1 step 1.7/1.9/1.10 still point to the right algorithm step numbers (step 8 pre-launch re-read, step 6 marker check), the Section 8 review-status note names the same two design points, and the options table of `once` matches 5.3.
- Nothing in the edited text is presented as a repo fact that the sources contradict.

### Part 4: addendum fidelity (checklist item 6)

- Recommendation wording: Section 6.1 heading "Decided by the owner (ADDENDUM 2)", Section 7.1 "Option A ... decided by the owner (ADDENDUM 2)", Section 1.1 table D1. `grep -in 'pending owner'` over the report returns nothing. PASS.
- Owner decision content (A poller every 5 minutes with own `gh` login via `orca agent launch`; no listener, inbound port, address registry; Q2 claim-only; Q3 integer-only; deliverable = design doc + tested poller with mock `gh` and mock `orca agent launch`, nothing live + label setup instructions; B/C and live deployment as follow-up): matches `research-notes.md` ADDENDUM 2 (lines 108-112) word for word in substance (report Sections 1.1, 7.1, 9.1 D1-D6, 8.1).
- Coder#477: Section 1.2, 7.7, 9.1 D5, G18 and the follow-up table state the repo boundary (listener, registration, transport live in the Coder repo, not IronClaude) and "option A makes #477 unnecessary unless B or C is revisited"; the prose of what #477 asks for and its candidate integration points matches ADDENDUM 2026-11-07T07:03Z point 2.
- B and C: description of B (Action + workspace listener) and C (central microservice + listener), sender authentication (HMAC + timestamp, GitHub OIDC, mTLS, Coder tokens: Section 5.13), `coder_app` sharing levels and exposure (5.14), minimal watcher-to-listener contract with request fields, `Idempotency-Key`, response codes 200/202/400/401/403/409/422/429 and audit fields (5.15), and nine revisit conditions (6, 5.15, 8) all trace to web-02 H, I, J and web-01 12, 14.5. The option-letter mapping problem in the web files (they call the Action design "C") is surfaced and resolved by description (Section 6.0 contradiction 1, 4.4, 9.3 C10) and the mapping is correct against web-01 line 25/line 183 and web-02 H2. PASS.

---

## Source-Document Fidelity Report

Report reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (2,176 lines, read in the parts listed under "Coverage and limits")
Source files checked: 35 codebase files, 11,249 lines (full reads or the cited ranges; list: `.github/workflows/{test,boundary-guard,contract3-generator-constraint-lint}.yml` and `README.md`, `.github/ISSUE_TEMPLATE/{bug_report,feature_request,other,config}.yml`, `src/superclaude/pr_submit/{ci,detection}.py`, `src/superclaude/cli/{main,install_user_setup,init_lite}.py`, `cli/recommend/{__init__,commands}.py`, `cli/cleanup_audit/commands.py`, `cli/tasklist/__init__.py`, `tests/pr_submit/{conftest,test_conflict_e2e,test_conflict_scripts,test_codex_reviews,test_static_grep,test_cosmos_poll}.py`, `tests/{cli,recommend,swarm}/test_cli_registration.py`, `docs/designs/*.md` (3), `Makefile`, `pyproject.toml`, `sc-issue-protocol/{scripts/origin_repo.py,refs/labels.md,refs/claim.md}`, `sc-pr-submit-protocol/scripts/poll-augment-review.sh`) plus 17 external URLs
Date: 2026-11-07

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|---|---|---|---|---|
| F1 | Distorted | `https://cli.github.com/manual/gh_project_item-list` (re-fetched) and `gh project item-list --help` (gh 2.103.3, run locally); also `research/01-claim-flow-and-session-launch.md:152` | Section 8, Phase 4 five-filter table, row 4 "Status Backlog" (report line 1612) | The row says "`status:Backlog` is documented for UI filtering only". The cited gh manual page and the local `--help` both show status filters used with `--query` of this very command: `--query "assignee:octocat -status:Done"` and the example `label:bug -status:Done`. File 01 recorded that example and the report dropped it. The open items stay correctly [UNVERIFIED] (the API host accepting `status:Backlog`, and the JSON schema), so the plan conclusion (fail closed, owner-run live call, Q8) does not change, but the "UI filtering only" statement is false against the cited page. (web-01 line 135 said the fetched manual text had no status example; the live page has two, so that research sentence is itself stale and was not carried, which is good.) Required fix: replace the clause with "`status:` filters appear in the `gh project item-list --query` examples (manual page and `--help`: `-status:Done`) and in the Projects filter documentation for views; acceptance of `status:Backlog` by the API host and the JSON schema are [UNVERIFIED]: Q8". Same softening is advisable in the R4/option A cell of the Requirement Scoring table (line 1265, "`status:Backlog` is documented for UI filtering"), which is not false but omits the CLI example. | IMPORTANT (blocking) |
| M1 | Inaccurate | `.github/ISSUE_TEMPLATE/bug_report.yml` | Section 2.3 (and R02 section 2) | `orca_version` is cited at `bug_report.yml:29,41-43`; `id: orca_version` is at l.28 (l.29 is `attributes:`); "Orca crashes when ..." is l.43. Off by one on a true claim. | MINOR |
| M2 | Inaccurate | `src/superclaude/cli/install_user_setup.py` | Section 2.3, Phase 2 preamble, G1/G3 ("`install_orca_skills` (l.230-263)", "`:198-263`") | `install_orca_skills` runs from l.230 to l.278; the cited range covers the subprocess part and `_find_orca`, so the claim holds, only the span label is short. | MINOR |
| M3 | Inaccurate | host `PATH` | Section 8 step 3.4 | "`which -a orca-ide` lists `/home/coder/.local/bin/orca-ide`": live output also lists `/usr/bin/orca-ide` and `/bin/orca-ide`. The argument built on it (both candidate names resolve on the real PATH, so a test using the real lookup could probe or launch a real binary) is unchanged and in fact stronger. | MINOR |
| M4 | Aspirational | `research/web-02...` A1, A4, A5 and Q5-type host facts | Section 7.7 and G18 ("the only follow-up A needs in the Coder repo is the `coder_script` cron entry ... and, if the template does not persist `$HOME`, a persisted path") | W02 says the template wiring is "a follow-up in the Coder repo" and that `$HOME` persistence is unknown; it does not say it is the only one. Section 9 Q5 lists further per-host facts (Orca runtime reachable by a scheduler-started process, `ccsession-orca`, picker IDs, ClickUp variables) that may also need template work. Suggested wording: "the only follow-up the research identified". | MINOR |
| M5 | Inaccurate (internal) | report Sections 6.1 step 6, 7.3 "Prompt (D3)", G12, SC-4 vs Phase 3 step 3.2 | prompt builder | Earlier sections give `"/sc:issue --claim " + str(int(number))`; step 3.2 deliberately hardens it to `type(number) is int` plus a regex and says so ("stricter than the `str(int(number))` of R01 §13"). Not a source distortion (R01 section 13 does say `str(int(number))`), only a not-updated earlier sentence. | MINOR |

Notes on source files (no report impact): file 02 section 3.3 counts "136 occurrences in 23 files" of `gh <subcommand>` in non-`.py` files under `src/superclaude`; my count with the same pattern lists at least 30 files. The report does not repeat that figure. File 02 also states `swarm/` 11,799 and `eval/` 11,367 lines (non-recursive); recursive counts are 16,055 and 11,426. Not carried into the report.

Adversarial result: the assignment said to assume at least 5 distortions. After re-checking 24 codebase claim groups, 17 external pages, the 5 live commands and every F1/F2-edited passage, one blocking distortion (F1) and five minor imprecisions were found. I did not find a phantom finding, an aspirational present-tense description of future code, or a distorted treatment of alternatives B and C or of the owner decision.

### Coverage and limits

Read in full or by cited range: report Sections 1, 2.3, 4 (all), 5 (all), 6.0 to 6.3 and Requirement Scoring, Options Comparison, Revisit table, 7 (all), 8 (all), 9 (all) and the parts of Section 3 that cite file 02 or the web files (via targeted scan). Not read line by line by me (they derive from files 01 and 03, which fidelity agent 1 owns, or are synthesis carry-forward lists): Sections 2.1, 2.2, 2.4, 2.5, the prose of Section 3, Section 6.4 (option D), Section 10 and Appendix A. Claims in those parts that rest on file 02 or the web files were caught by the search for file-02 and web citations; nothing in them contradicted a source.

### Summary

- Files checked: 35 codebase files (11,249 lines) and 17 external URLs (plus 5 live read-only commands)
- Claims verified: about 140 individual claims (24 codebase claim groups with line anchors, 17 external pages with 3 to 6 claims each, 5 live command outputs)
- Fidelity issues: 1 blocking (F1, IMPORTANT), 5 minor (M1 to M5)
- Required action before PASS: fix F1 (one sentence at report line 1612; optionally align line 1265). No other change is required.
- Confidence: Verified: 6/6 checklist areas (semantic coverage, detail preservation, phantom detection, code characterization including the `ci.py` point, no aspirational claims, addendum fidelity) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% for the assigned scope (see Coverage and limits for what was not read line by line)
- Tool engagement: Read: 17 | Grep: 7 | Glob: 1 | Bash: 14 (batched read-only inspections, including gh and orca help/read calls) | WebFetch: 19 calls (17 distinct successful URLs, 2 returned no content: tavily_search: 0, tavily_extract: 0, web_search_fallback: 0, web_fetch_fallback: 19; reason for every fallback: Tavily MCP tools are not present in this agent's tool list)

VERDICT: FAIL

## QA Complete
