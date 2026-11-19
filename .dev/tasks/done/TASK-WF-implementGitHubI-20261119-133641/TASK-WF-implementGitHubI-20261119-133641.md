---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-implementGitHubI-20261119-133641
version: "1"
priority: Medium
created_date: "2026-11-19"
---

# Merged pull request daily log: adapt Jay's generator into one opt-in script

Source: ./source.md
Goal: A single opt-in script, `scripts/merged_pr_log.py`, builds a per-day, per-person log of merged pull requests across the orgs IronbellyOrg and IronbellyGroup (a markdown digest and a web page), credits people under Clay's 2026-11-19 rule, rewrites one ClickUp Doc page in place, and ships with tests and an Orca automation definition that is written but not switched on.

## Constraints

- Scope is exactly three deliverables: `scripts/merged_pr_log.py`, tests under `tests/merged_pr_log/` (with `fixtures/`), and one definition file `scripts/merged_pr_log_orca_automation.md`. Add no skill, command, agent, hook or template. Do not edit `src/superclaude/cli/install_skills.py`, `src/superclaude/cli/main.py` or any `install_*.py` (install code only reads `src/superclaude/skills`, commands, agents, hooks and templates; the repo-root `scripts/` folder is never read by an install, which is what keeps this opt-in). Nothing is added to IronFlow.
- Independence: the script imports only the Python standard library, nothing from this repo. It does not read, import or name the daily work report or the orchestrator, and it does not run the `gh` command (no `subprocess`); it talks to GitHub and ClickUp through `urllib`.
- Adapt, do not rewrite. Start from Jay Wedgeworth's `scripts/build-fleet-daily-digest.py` (Apache-2.0, standard library only) at https://github.com/Simple-With-Us/AI-Fleet-Coordinator/blob/main/scripts/build-fleet-daily-digest.py ; fetch and read the original first (the function names and line numbers recorded during planning came from a summary of it and are unverified). Keep and adapt `token`, `env_int`, `gh_get`, `gh_list`, `parse_iso`, `to_local_day`, `fetch_merged_prs`, `bucket_all`, `build_markdown`, `build_html` and `main`. Drop `fetch_issue_churn`, `build_daily_ics`, `day_summary_title`, `day_description`, the public allowlist (`select_public_repos`, `PUBLIC_REPOS`, `DEFAULT_FLEET_OWNER`, `DEFAULT_REPOS`, `repo_legend_html`), the calendar imports, and all agent-from-title code (`extract_agents_and_clean`, `_normalize_agent_token`, `_split_agent_chain`, the `_AGENT_*` patterns, `AGENT_LOGO`, `agent_icons_html`, `agent_legend_html`, `agent_icons_md`, `_agent_label`, `logo_file`). Keep an Apache-2.0 notice in the module docstring naming Jay's file as the origin and stating the file was modified.
- Names every task and test relies on: script `scripts/merged_pr_log.py`; tests `tests/merged_pr_log/__init__.py` and `tests/merged_pr_log/test_merged_pr_log.py`; fixtures in `tests/merged_pr_log/fixtures/`; definition file `scripts/merged_pr_log_orca_automation.md`; functions `token`, `list_repos`, `fetch_merged_prs`, `credit_for_pr`, `bucket_all`, `build_markdown`, `build_html`, `publish_clickup`, `main`; constants `ORGS` (`IronbellyOrg`, `IronbellyGroup`) and `LOGIN_TO_PERSON`; command line `--out DIR` (required: the folder that receives `index.html` and `digest.md`) and `--dry-run`.
- Environment variables (names only, no values anywhere): `GH_TOKEN`, `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `CLICKUP_DOC_ID`, `CLICKUP_PAGE_ID`. The issue left the ClickUp names open and named a workspace id and a page id; the page rewrite call `PUT /v3/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}` also needs the Doc id, so there are three ClickUp ids. Non-secret settings, also from the environment: `DIGEST_TZ` (default `America/Chicago`) and `DIGEST_LOOKBACK_DAYS` (default 21).
- Testability: all network access goes through two injected callables, `get(path, params)` returning decoded JSON and `put(path, body)`; only `main` wires them to `urllib`. `main` has the signature `main(argv=None, env=None, get=None, put=None, now=None)` so a test can pass a fake environment, fake transport and a fixed clock. Tests never touch the network.
- Credit rule (Clay's ruling of 2026-11-19; it replaces any author-only rule): credit goes to the person who made the branch and submitted the PR, never to whoever merged it (the merger, `merged_by`, is never read). A PR opened by a human credits that login. A PR opened by a bot (login ending in `[bot]`, or user type `Bot`) credits the author of the branch's commits: the first commit, in order, whose author login is not a bot. A bot never gets credit for opening or merging. A PR made wholly by a bot with no person behind it (no commit with a non-bot author login) goes on a separate "no person" line and is credited to nobody. `LOGIN_TO_PERSON` maps `clayphi` to Clay, `ironbelly` to Ryan, `IBC-ChrisG` to Chris, `IB-Lea` to Leandro and `swill-ib` to William (login match ignores case). A login that is not in the table and is not a bot is shown as the login. No agent name or "Claude Code" is ever shown as a credit, a column, a legend or a label. PR titles are PR text and are shown as written.
- Secrets: never write a token value in any file, fixture, test or definition. Tests set environment values to obvious placeholders such as `placeholder-not-a-secret`, never a realistic token shape. The script never prints a token; error messages name the variable only.
- Recorded responses: fixtures are JSON files in the GitHub REST response shape, trimmed to the fields the script reads. Write them by hand unless an authorized capture already exists, and say which in the test module docstring.
- Run Python through `uv`: `uv run pytest tests/merged_pr_log -v` and `uv run ruff check scripts/merged_pr_log.py tests/merged_pr_log`.
- The work ends with `/sc:pr-submit --monitor 3`, run by the session owner after `/sc:implement` finishes. It is not a task here. No task creates the Orca automation in Orca or switches any schedule on.

## Phase 1: Build the digest script and its tests

## Task 1: Create the GitHub fetch layer in scripts/merged_pr_log.py

Create `scripts/merged_pr_log.py` and the test package `tests/merged_pr_log/` (`__init__.py`, `test_merged_pr_log.py`, `fixtures/`). The test module loads the script the way `tests/review/test_reflect_cluster_pairs.py` does (lines 14-16: `importlib.util.spec_from_file_location` on `ROOT / "scripts" / "merged_pr_log.py"`).

In the script, adapt Jay's `token` so it reads only `GH_TOKEN` from the environment mapping it is given and stops with a clear message that names `GH_TOKEN` when it is missing or blank (no fallback to `GITHUB_TOKEN`, `FLEET_GITHUB_TOKEN` or any stored login). Adapt `env_int`, `gh_get`, `gh_list`, `parse_iso` and `to_local_day`. Add `ORGS`. Write `list_repos(get, orgs)`: for each org, page through `GET /orgs/{org}/repos` with `type=all` and `per_page=100`, and return every repo whose `archived` flag is false, public and private, listed again on every call and stored nowhere. Adapt `fetch_merged_prs(get, org, repo, start_date, tz)` from Jay's version: `GET /repos/{org}/{repo}/pulls` with `state=closed`, `sort=updated`, `direction=desc`, keep only PRs with `merged_at` whose local date in `tz` is on or after `start_date`, and stop paging once a page is older than the window, as Jay's does. Read `DIGEST_TZ` and `DIGEST_LOOKBACK_DAYS` with the defaults in the Constraints, and compute the window start the way Jay's `main` does.

Acceptance criteria:
- With `GH_TOKEN` unset or blank, `token` exits non-zero with a message that contains `GH_TOKEN`, even when `GITHUB_TOKEN` is set, and the message contains no token value. A test in `tests/merged_pr_log/test_merged_pr_log.py` shows it.
- `list_repos` returns the non-archived repos of both `IronbellyOrg` and `IronbellyGroup`, private ones included, and returns no archived repo, using fixtures under `tests/merged_pr_log/fixtures/`.
- Repo added after the first run: a second `list_repos` call fed a second recorded org listing that contains one more repo returns that repo with no code or configuration change. A test shows it.
- A repo with no merged PRs in the window makes `fetch_merged_prs` return an empty list and raise nothing; a PR merged before the window start is left out and one inside it is kept. Tests show both.
- `scripts/merged_pr_log.py` imports only standard library modules and contains no `subprocess` use, and `uv run pytest tests/merged_pr_log -v` and `uv run ruff check scripts/merged_pr_log.py tests/merged_pr_log` pass.

## Task 2: Add the credit rule and per-day bucketing

Depends on: Task 1

In `scripts/merged_pr_log.py` add `LOGIN_TO_PERSON` and `credit_for_pr(get, org, repo, pr)` following the credit rule in the Constraints. For a bot-opened PR it reads `GET /repos/{org}/{repo}/pulls/{number}/commits` (`per_page=100`) and takes the first commit whose `author.login` is present and not a bot; a commit whose `author` is null is skipped. The function returns the person's name, the login for an unmapped non-bot login, or `None` for a PR with no person. It never reads `merged_by`. Adapt Jay's `bucket_all` so merged PRs are grouped by local date in the configured time zone, then by credited name, with the no-person PRs kept in their own list for that day; sort days newest first, names alphabetically, PRs by repo then number.

Add recorded fixtures for the PR and commit responses and tests in `tests/merged_pr_log/test_merged_pr_log.py`.

Acceptance criteria:
- A human-opened PR by `clayphi` is credited to `Clay`, and the same holds for `ironbelly` (Ryan), `IBC-ChrisG` (Chris), `IB-Lea` (Leandro) and `swill-ib` (William), including a login written in a different case. Tests show it.
- A PR opened by `github-actions[bot]` whose commits are authored by `IB-Lea` is credited to `Leandro`, and a PR opened by another account ending in `[bot]` behaves the same. A test shows it.
- A PR made wholly by a bot (every commit authored by a `[bot]` account, or no commit with an author login) is credited to nobody and appears in the day's no-person list. A test shows it.
- A PR opened by `clayphi` and merged by a different login (and one merged by a bot) is credited to `Clay`; the merger gets nothing. A test shows it.
- A human login that is not in the table is shown as the login. A test shows it.
- A merge timestamp near midnight UTC lands on the correct local day in `America/Chicago` and on a different day under another `DIGEST_TZ` value. A test shows it.

## Task 3: Render the markdown digest and the web page

Depends on: Task 2

Adapt Jay's `build_markdown` and `build_html` in `scripts/merged_pr_log.py`. Each lists, newest day first, the day heading in the configured zone, then each credited person with a count and their PRs, then a "No person" line for that day when it has any, with its count and PR links. Every PR entry shows `org/repo#number`, the title as written, and a link to its GitHub `html_url`. The header shows when the log was generated in the configured zone, the lookback window and the number of repos scanned. Remove everything tied to issues, the calendar feed, the public repo legend and agent icons or legends. HTML-escape all PR text in the page and escape markdown link characters in titles in the digest.

Add tests in `tests/merged_pr_log/test_merged_pr_log.py` that render from the Task 2 fixtures.

Acceptance criteria:
- The digest and the page both contain, for a fixture PR, its `html_url` and its `org/repo#number`, grouped under the right local day and the right person.
- A day with a no-person PR shows a "No person" line with its count, and that PR is listed under no person's name.
- A fixture PR title containing markup such as `<script>` appears escaped in the page and does not become a live tag.
- The text the script itself writes (headings, legends, column names) contains neither "claude" nor "agent" in any letter case; a test renders a fixture with plain titles and checks both outputs.
- Neither output contains an issue section, a calendar link or a repo allowlist legend.

## Task 4: Publish to ClickUp and wire main with --dry-run

Depends on: Task 3

In `scripts/merged_pr_log.py` add `publish_clickup(put, env, markdown)` and `main(argv=None, env=None, get=None, put=None, now=None)`. `publish_clickup` calls `PUT /v3/workspaces/{CLICKUP_WORKSPACE_ID}/docs/{CLICKUP_DOC_ID}/pages/{CLICKUP_PAGE_ID}` with the body `content` (the markdown digest), `content_format` `text/md` and `content_edit_mode` `replace`, and sends `CLICKUP_API_TOKEN` as the `Authorization` header value with no `Bearer` prefix (a personal token; see the ClickUp authentication notes in the hosting research quoted in `source.md`). `main` checks every required variable first, before any network call: `GH_TOKEN` always, and the four ClickUp variables unless `--dry-run` is given, and stops non-zero naming each missing variable. It then lists repos, fetches merged PRs for each, credits and buckets them, writes `index.html` and `digest.md` into the `--out` folder, and publishes the digest. Any GitHub or ClickUp error ends the run non-zero before anything is published, so the page already in ClickUp is never replaced by a partial log. `--dry-run` writes the two files and makes no ClickUp call, and prints the output of `GET /rate_limit` (the `core`, `graphql` and `search` remaining counts) once before and once after the GitHub reads, which settles the open question about the search limit from the research.

Add tests in `tests/merged_pr_log/test_merged_pr_log.py` using a fake `get`, a fake `put` and a fixed `now`.

Acceptance criteria:
- A full `main` run over fixtures writes `index.html` and `digest.md` under the `--out` folder and calls the fake `put` once, with path `/v3/workspaces/<id>/docs/<id>/pages/<id>`, `content_format` `text/md`, `content_edit_mode` `replace` and the digest as `content`. A test shows it.
- With any one of `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `CLICKUP_DOC_ID` or `CLICKUP_PAGE_ID` missing, `main` exits non-zero, names that variable, and makes no GitHub call and no `put`; with `--dry-run` only `GH_TOKEN` is required. Tests show both.
- A `--dry-run` run makes no `put` call and prints the rate limit counts twice (before and after). A test captures the output.
- When the fake `get` raises an error for one repo, `main` exits non-zero and the fake `put` is never called. A test shows it.
- No test or output prints a token value, and the test environments use only the placeholder value named in the Constraints.

## Phase 2: Opt-in boundary and the Orca definition

## Task 5: Write the Orca automation definition and the human steps

Depends on: Task 4

Create `scripts/merged_pr_log_orca_automation.md`, a definition only: nothing in it is created in Orca, enabled or triggered. The exact Orca automation file format is not confirmed in this repo (no automation definitions exist here), so the file lists the fields a person enters. Use these lines so a test can read them: a line `Name: merged-pr-log-refresh`, a line `Trigger (UTC): 5 0,6,12,18 * * *`, and a line `Status: written, not switched on`. Explain in one short paragraph that the name must not start with `coordinator-` because Orca run history under that prefix is copied into the daily work report, and that Orca triggers are UTC while day buckets use `DIGEST_TZ`. Give the precheck command shape that runs the script detached and exits non-zero so Orca starts no agent, loading the environment the way the workspace already does and running `uv run --no-project python scripts/merged_pr_log.py --out <out dir>`. List the environment variable names the run needs, names only. Then list the human steps in order, as plain bullets: create the ClickUp Doc and one page in the team's workspace, share it with the team only and leave public links off, and confirm the workspace plan allows the Docs API (not confirmed in the research); note the workspace id, Doc id and page id; create a token that can read pull requests in both orgs (the scheduler research found a fine-grained token targets one org, so confirm what covers both); deliver the five variables through the workspace environment without writing values in any file; run the script once by hand with `--dry-run` and read the rate limit counts; create the automation in Orca from this definition and leave it off; Clay switches it on.

Add a test in `tests/merged_pr_log/test_merged_pr_log.py` that reads this file.

Acceptance criteria:
- `scripts/merged_pr_log_orca_automation.md` exists, and a test finds the three lines above exactly, with the name not starting with `coordinator-` and the trigger equal to `5 0,6,12,18 * * *`.
- The file names the five environment variables and contains no token-shaped value (no `ghp_`, `github_pat_`, `pk_` followed by digits, or `Bearer ` followed by a value); a test checks it.
- The human steps include creating the ClickUp Doc and switching the Orca automation on, and the file states that nothing was created or enabled.
- Nothing in the file points at the daily work report configuration or the orchestrator as an input.

## Task 6: Add the opt-in and independence guard tests

Depends on: Task 5

In `tests/merged_pr_log/test_merged_pr_log.py` add tests that keep the log opt-in and independent, so a later change cannot break the hard rules silently. Use `ast` on `scripts/merged_pr_log.py` and file scans; read, never import, the install code.

Acceptance criteria:
- Every import in `scripts/merged_pr_log.py` is a standard library module (checked with `sys.stdlib_module_names`), and the source contains no `subprocess`, no `superclaude` and no reference to the work report or the orchestrator.
- No file under `src/superclaude/` mentions `merged_pr_log`, and no directory or file named `merged_pr_log*` exists under `src/superclaude/skills`, `commands`, `agents`, `hooks` or `templates`, so `superclaude install` output is unchanged.
- The three delivered files contain no token-shaped string and no occurrence of an agent name as a credit; the script reads credentials only through `os.environ` or the `env` mapping it is passed (no file read of a credential).
- The script file text contains no ClickUp or GitHub token variable value, and `uv run pytest tests/merged_pr_log -v` passes with all tests from Tasks 1 to 6.
