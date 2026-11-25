d95444990fe6b04affa92eecd996c95a4447b49d
Review one task for spec compliance.

Task brief: ## Task 9: Prepare the controlled create-run kit and the empty 30-row matrix

Depends on: Task 8

Static text checks cannot prove agent behavior, so the spec asks for controlled create runs. They cannot run in this session: its guard refuses `superclaude install`, a child agent session, a Skill call to the issue protocol and Bash text that names the GitHub CLI with `issue` or `api`. This task therefore only prepares the kit and the matrix; it runs no create flow, starts no child session and runs no installer. Write every file below with the Write tool, never with a Bash heredoc, under `./artifacts/create-run-kit/` in this package:

- `README-run.md`: the steps a person runs in their own terminal. Run `make sync-dev` first (or confirm no project mirror exists), because agents are read from the project mirror before the home copy. Create a temporary home and install the changed skill, agents and command into it with the per-component installers that take a target path (`install_all_skills(target_path=..., force=True)` in `src/superclaude/cli/install_skills.py`, `install_agents(target_path=...)` in `src/superclaude/cli/install_agents.py`, `install_commands(target_path=...)` in `src/superclaude/cli/install_commands.py`), never `superclaude install` (it also runs the hooks, ccsession, user-setup and codegraph phases, `src/superclaude/cli/main.py:211-255`). Put the shim first on `PATH`. For each row use a fresh scratch working directory, because the create flow renames its draft folder to `.dev/issues/<N>/` and writes files there. The gateway model pins come from the person's own environment; the kit never copies a key or token into the temporary home or into this package (NFR12).
- `gh-shim.sh`: the stand-in for the GitHub CLI. It never runs the real `gh`. It answers only these calls, each logged to the row's own log file `./artifacts/create-run-kit/rows/<row-id>/gh-calls.log`: auth status; the label, issue-type and issue-field lookups from the fixtures; the duplicate search; a fake `issue create` that prints a fake URL whose number is the row's fake number; the issue view for the issue type; `issue comment` (log only, keep a copy of the body); the issue-field POST (log only); and the issue-field read-back. Every other call is logged as `REFUSED` and exits non-zero. Row `n` of 30 uses fake issue number 900000+n, which is above any real issue number of this repository.
- `fixtures/`: the label, issue-type, issue-field (Complexity) and duplicate-search answers the shim returns.
- `matrix.md`: 30 rows, one for each of ten scenarios at each of the three depths quick, standard and deep, with columns row id, scenario, depth, drafting worker, expected questions, observed questions, answer given, posts observed, additions kept, pushback comment posted, fake issue number, result. Every row starts with the result `not run: owner run required`. The ten scenarios: S01 empty notes (both lists hold only `- None`), 0 questions; S02 additions only including an `Assumption:` line, 0; S03 reversed choice, 1; S04 dropped requirement, 1; S05 changed flag, 1; S06 user-stated fact contradicted by verified code, 1; S07 two contradictions at once, 1 naming both; S08 additions plus one contradiction, 1 and the additions stay in the body; S09 a worker disagrees with a user-supplied flag and the issue is filed with the user's flag, 0 questions, and the pushback comment is posted at standard and deep depth only; S10 an addition that is the only evidence of a contradiction, 1 question, and the answer "keep my wording" removes only that content while every other addition stays. In every row that asks, the answer given is "keep my wording" unless the row says otherwise.

Acceptance criteria:
- [T9.AC1] `./artifacts/create-run-kit/` holds `README-run.md`, `gh-shim.sh`, a `fixtures/` folder and `matrix.md`, all written with the Write tool; no installer, child session or create flow ran in this session.
- [T9.AC2] `grep -c "not run: owner run required" ./artifacts/create-run-kit/matrix.md` prints 30, and `grep -c "^| S" ./artifacts/create-run-kit/matrix.md` prints 30.
- [T9.AC3] Reading `gh-shim.sh` shows a final default branch that logs `REFUSED` and exits non-zero, and `grep -nE "exec .*gh|command gh|/usr/bin/gh" ./artifacts/create-run-kit/gh-shim.sh` prints nothing (the shim never reaches the real tool).
- [T9.AC4] `README-run.md` names the per-component installers, the words "never `superclaude install`", the fake-number rule (900000+n), the per-row scratch directory and per-row log file, and says the plan stays partial until the matrix is filled.
- [T9.AC5] The executor's final report states that Task 9 delivered the kit and left the 30 rows to the owner's run, so the plan is reported partial, not fully verified.
Global constraints: ## Constraints

- Base branch is `integration` (the issue text says `master`; that is stale). Edit only canonical sources under `src/superclaude/`, `docs/` and `tests/`. The generated project mirrors are refreshed only by `make sync-dev`, never edited by hand.
- Keep `AskUserQuestion` in the `allowed-tools` line of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (pinned by `ALLOWED_TOOLS` in `tests/skills/test_issue_protocol.py:40`).
- Keep the full issue body never shown for approval (default B1), the post-create flag pushback comment (create Wave 5, `templates/create-review-comment.md`), the three required plan sections and their one shared rule sentence (`PLAN_SECTIONS_RULE`, `tests/skills/test_issue_worker_agents.py:34-39`), claim assignment, ClickUp, Orca, watcher and launch safeguards, the stage-claim recommendation skip from pull request 833, and the launched `worktree` agent's plan-approval boundary. None of these text blocks may change in meaning. Task 9 and Task 10 each carry a check that the launch-level safeguards stay untouched.
- Lines of `src/superclaude/skills/sc-issue-protocol/refs/create.md` that `tests/skills/test_worker_contract.py` pins verbatim (the GitHub-write rule paragraph near line 9, the lookup paragraph near line 20 and step 6 of Wave 5 near line 95) must stay byte-identical. SKILL.md step 6 of create mode (line 103) is also pinned there; Task 4 updates that pinned copy together with the line.
- Do not add a new return-contract field, flag, script, agent or dependency to the product. The classification is instruction text plus tests, as the current rule is. The kit of Task 9 is evidence tooling under this package's `./artifacts/`, not product code.
- A contradiction counts only with all three parts: its category, the user's own words (a quote from `description.md` or a flag passed on the command line), and the conflicting evidence (draft text, or a verified `path:line` of code the worker read). A line missing any part is New material. `None` is the empty marker, never an item, and a notes file with `- None` under both headings is the same state as empty notes.
- The changed-flag category means the drafted issue itself would not honor a flag the user passed (for example it would be filed with another mode or type). A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag; it stays a pushback comment.
- When an addition is also the only evidence for a contradiction, it is listed under Contradictions, and "keep my wording" removes only that content; every other New material item stays.
- The session that carries out this plan is a launched session whose guard refuses the installer for the whole tool, a child agent session, a Skill call to the issue protocol and any Bash text that names the GitHub CLI together with `issue` or `api`. No task here runs a create flow, starts a child session or runs `superclaude install`. Task 9 therefore prepares a kit and leaves the controlled runs to a person, and the final report calls the plan partial until that run fills the matrix.
Start sha: d95444990fe6b04affa92eecd996c95a4447b49d
Diff against the start snapshot: 
--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/README-run.md (full contents) ---
# Controlled create runs for issue 834: how to run them

This kit was prepared by the session that implemented the plan, and nothing in it has been run. That session is a launched session: its guard refuses the whole-tool installer, a child agent session, a Skill call to the issue protocol and any Bash text that names the GitHub tool with `issue` or `api`. It started no child session, ran no installer and ran no create flow. The plan therefore stays **partial** until a person has run the 30 rows of `matrix.md` and filled them in. The static tests in `tests/` prove the instruction text only; they do not prove agent behavior.

Run everything below in your own terminal, in your own session. Give the agent your gateway credentials through your own environment, as you always do. Never copy a key or token into the temporary home, into this kit, or into any file of this package (NFR12).

## 1. Make the project mirrors fresh

Agents are read from the project mirror before the home copy. From the repository root of this branch run `make sync-dev` (or confirm no project mirror exists), so that the mirror holds the changed agents and skill.

## 2. Make a temporary home and install into it

Use the per-component installers below, which take a target path, and never `superclaude install`: that command also runs the hooks, ccsession, user-setup and codegraph phases (`src/superclaude/cli/main.py:211-255`).

- `install_all_skills(target_path=<KIT_HOME>/.claude/skills, force=True)` in `src/superclaude/cli/install_skills.py`
- `install_agents(target_path=<KIT_HOME>/.claude/agents, force=True)` in `src/superclaude/cli/install_agents.py`
- `install_commands(target_path=<KIT_HOME>/.claude/commands/sc, force=True)` in `src/superclaude/cli/install_commands.py`

`<KIT_HOME>` is a new folder from `mktemp -d`. Call each function from `uv run python` in the repository root, and read the returned message; each one prints the folder it wrote.

## 3. Put the shim first on PATH

The create flow calls a program named `gh`. Make a folder `<KIT_HOME>/bin`, link or copy `gh-shim.sh` into it under the name `gh`, make it executable, and put `<KIT_HOME>/bin` first on `PATH`. Before every row run `command -v gh` and `gh --version`: the first must print the shim path and the second must print `gh-shim (not the real GitHub CLI)`. If it does not, stop; the real tool would be reached.

The shim never runs the real tool and never opens a connection. It needs these variables, set again for every row:

- `SHIM_ROW_ID`: the row id, for example `S03-standard`
- `SHIM_ROW_NUMBER`: the row number n from `matrix.md` (1 to 30); the fake issue number is 900000+n, above any real issue number of this repository
- `SHIM_LOG_DIR`: the absolute path of `rows/<row id>` inside this kit (the shim creates it); the row's log file is `rows/<row id>/gh-calls.log`
- `SHIM_FIXTURES`: the absolute path of the `fixtures` folder of this kit
- `SHIM_REPO`: the `owner/repo` that the scratch directory's origin names (use `IronbellyOrg/IronClaude`)

The shim answers only the calls the create flow makes and logs each as one line: `OK-AUTH`, `LOOKUP-LABELS`, `LOOKUP-TYPES`, `LOOKUP-FIELDS`, `LOOKUP-DUPES`, `CREATE`, `VIEW-TYPE`, `COMMENT`, `FIELD-POST`, `FIELD-READ`. Everything else, and any call about an issue number other than this row's fake number, is logged as `REFUSED` and exits non-zero. The fixtures follow the shape the skill text describes; if a lookup worker reports it cannot read one, adjust that fixture to the real API answer and say so in the row.

## 4. Use a fresh scratch directory for every row

The create flow reads `<R>` from the working directory's `origin` remote and stops with `E-NO-ORIGIN` without one. It also renames its draft folder to `.dev/issues/<N>/` and writes files there. So for each row make a new per-row scratch directory outside this repository checkout, run `git init` in it, and add a local `origin` that names the fork (`git remote add origin https://github.com/IronbellyOrg/IronClaude.git`; nothing is ever fetched or pushed). Never run a row inside a real checkout, and never reuse a scratch directory.

## 5. Start the agent on the temporary home and run the row

Start your own Claude Code session in the scratch directory with `CLAUDE_CONFIG_DIR=<KIT_HOME>/.claude`, the shim first on `PATH` and the five `SHIM_` variables set. The executor of the plan starts no child session; you do. Type `/sc:issue --create "<description>" --depth <depth>` plus the flags of the scenario recipe below. When the one question appears, give the answer the matrix row names (`keep my wording`). Ask nothing else and answer nothing else.

## 6. Scenario recipes (suggestions)

A recipe is a description meant to provoke the scenario. A row counts only when the drafter's own `draft-notes.md` (saved as `.dev/issues/<N>/draft-notes.md` in the scratch directory; copy it into the row folder) holds the list content the scenario expects. If it does not, mark the row `scenario-not-reproduced`, not pass, and retry with a stronger description up to three times.

- S01: `"Fix the typo 'recieve' to 'receive' in README.md line 3."` with `--mode bug --type docs`.
- S02: `"Add a --verbose flag to the sample CLI. Assume the entry point is src/cli.py and keep output on stderr."` with `--mode feature --type cli`; expect `Assumption:` lines under New material.
- S03: `"Keep the existing JSON cache in src/superclaude/cli/ and do not introduce SQLite. Add a cache-expiry option."` with `--mode feature --type cli`; the contradiction is the draft choosing SQLite.
- S04: `"Add a retry option to the sample CLI. It must log every retry to stderr."`; the contradiction is the draft dropping the logging requirement.
- S05: a description that reads as a crash report, passed with `--mode feature`; the contradiction is the drafted issue being filed as a bug.
- S06: `"parse_ledger_line in src/superclaude/cli/ledger_utils.py already validates tabs; extend it to spaces."` (no such function exists); the contradiction is the user's stated fact being false.
- S07: S03 and S06 together in one description.
- S08: S02 and S06 together in one description.
- S09: all flags given, with a mode and type the worker will dispute (for example `--mode bug --type docs` on a feature request); at quick depth the flags are taken at face value, so no comment is expected there.
- S10: `"The cache never expires; add a refresh flag."`; the draft adds a code fact that the cache has a time limit (an addition that is the only evidence of the contradiction).

Run each scenario at all three depths with the same description.

## 7. Reading a row

After the run, read `rows/<row id>/gh-calls.log`. A row passes only when all of these hold:

- the log has zero `REFUSED` lines;
- it has exactly one `CREATE` line and exactly one `FIELD-POST` line;
- the number of `COMMENT` lines equals the "Calls expected" column (a comment only for S09 at standard and deep depth);
- the number of questions you saw equals the "Expected questions" column, and the answer you gave is the one the row names;
- every addition listed in the copied `draft-notes.md` is present in `rows/<row id>/issue-body.posted.md`, and the final output has one `kept without approval: <item>` line for each;
- the agent never offered the full issue body for approval.

Fill the observed columns of `matrix.md` from these facts and replace the Result with `pass`, `fail: <reason>` or `scenario-not-reproduced`. At deep depth the first worker may fall back to the tier 2 worker; write the worker that really drafted the body (the fallback line is in `draft-notes.md`).

## 8. Report

When all 30 rows are filled, the plan is fully verified. Until then the plan is reported partial, and the pull request body lists the unfilled rows as a follow-up.

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/gh-shim.sh (full contents) ---
#!/usr/bin/env bash
# gh-shim.sh: a stand-in for the GitHub command line tool, for the controlled
# /sc:issue --create runs of issue 834. It never reaches the real tool and never
# opens a network connection. Link it as an executable named `gh` in the first
# folder of PATH (see README-run.md).
#
# It answers only the calls the create flow makes, each logged to the row's own
# log file ($SHIM_LOG_DIR/gh-calls.log). Every other call, and every call about
# an issue number other than this row's fake number, is logged as REFUSED and
# exits non-zero.
#
# Required environment (set per row, see README-run.md):
#   SHIM_ROW_ID      row id, for example S03-standard
#   SHIM_ROW_NUMBER  row number 1..30; the fake issue number is 900000 + this
#   SHIM_LOG_DIR     absolute path of rows/<row id> inside this kit
#   SHIM_FIXTURES    absolute path of the fixtures folder of this kit
#   SHIM_REPO        owner/repo that the scratch directory's origin names
# Optional: SHIM_ISSUE_TYPE (default Feature) answers the issue-type read-back.
set -u

: "${SHIM_ROW_ID:?set SHIM_ROW_ID}"
: "${SHIM_ROW_NUMBER:?set SHIM_ROW_NUMBER}"
: "${SHIM_LOG_DIR:?set SHIM_LOG_DIR}"
: "${SHIM_FIXTURES:?set SHIM_FIXTURES}"
: "${SHIM_REPO:?set SHIM_REPO}"

mkdir -p "$SHIM_LOG_DIR"
LOG="$SHIM_LOG_DIR/gh-calls.log"
FAKE_N=$((900000 + SHIM_ROW_NUMBER))
OWNER="${SHIM_REPO%%/*}"
ARGS="$*"

log() {
  printf '%s %s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" "${2:-}" >> "$LOG"
}

# value of a long option, for example: opt_value --body-file "$@"
opt_value() {
  local want="$1"
  shift
  while [ "$#" -gt 0 ]; do
    if [ "$1" = "$want" ] && [ "$#" -gt 1 ]; then
      printf '%s' "$2"
      return 0
    fi
    shift
  done
  return 1
}

refuse() {
  log REFUSED "$ARGS"
  echo "gh-shim: refused: $ARGS" >&2
  exit 1
}

case "${1:-}" in
  --version)
    echo "gh-shim (not the real GitHub CLI)"
    exit 0
    ;;
  auth)
    if [ "${2:-}" = "status" ]; then
      log OK-AUTH "$ARGS"
      echo "Logged in to github.com (gh-shim)"
      exit 0
    fi
    refuse
    ;;
  label)
    if [ "${2:-}" = "list" ]; then
      log LOOKUP-LABELS "$ARGS"
      cat "$SHIM_FIXTURES/labels.json"
      exit 0
    fi
    refuse
    ;;
  issue)
    case "${2:-}" in
      list)
        log LOOKUP-DUPES "$ARGS"
        cat "$SHIM_FIXTURES/duplicates.json"
        exit 0
        ;;
      create)
        log CREATE "$ARGS"
        body="$(opt_value --body-file "$@" || true)"
        if [ -n "$body" ] && [ -f "$body" ]; then
          cp "$body" "$SHIM_LOG_DIR/issue-body.posted.md"
        fi
        echo "https://github.com/$SHIM_REPO/issues/$FAKE_N"
        exit 0
        ;;
      view)
        [ "${3:-}" = "$FAKE_N" ] || refuse
        log VIEW-TYPE "$ARGS"
        echo "${SHIM_ISSUE_TYPE:-Feature}"
        exit 0
        ;;
      comment)
        [ "${3:-}" = "$FAKE_N" ] || refuse
        log COMMENT "$ARGS"
        body="$(opt_value --body-file "$@" || true)"
        if [ -n "$body" ] && [ -f "$body" ]; then
          cp "$body" "$SHIM_LOG_DIR/comment.posted.md"
        fi
        echo "https://github.com/$SHIM_REPO/issues/$FAKE_N#issuecomment-1"
        exit 0
        ;;
    esac
    refuse
    ;;
  api)
    if [ "${2:-}" = "-X" ] && [ "${3:-}" = "POST" ]; then
      if [ "${4:-}" = "repos/$SHIM_REPO/issues/$FAKE_N/issue-field-values" ]; then
        log FIELD-POST "$ARGS"
        input="$(opt_value --input "$@" || true)"
        if [ -n "$input" ] && [ -f "$input" ]; then
          cp "$input" "$SHIM_LOG_DIR/field-values.posted.json"
        fi
        echo '{}'
        exit 0
      fi
      refuse
    fi
    case "${2:-}" in
      "repos/$SHIM_REPO/issue-types")
        log LOOKUP-TYPES "$ARGS"
        cat "$SHIM_FIXTURES/issue-types.json"
        exit 0
        ;;
      "orgs/$OWNER/issue-fields")
        log LOOKUP-FIELDS "$ARGS"
        cat "$SHIM_FIXTURES/issue-fields.json"
        exit 0
        ;;
      "repos/$SHIM_REPO/issues/$FAKE_N/issue-field-values")
        log FIELD-READ "$ARGS"
        if [ -f "$SHIM_LOG_DIR/field-values.posted.json" ]; then
          cat "$SHIM_LOG_DIR/field-values.posted.json"
        else
          echo '[]'
        fi
        exit 0
        ;;
    esac
    refuse
    ;;
esac

# Default branch: any call not listed above is refused and logged.
refuse

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/matrix.md (full contents) ---
# Controlled create-run matrix (issue 834): 10 scenarios x 3 depths = 30 rows

Status: prepared, not filled. Every row below starts with the Result marker that says an owner run is required. A row is filled only by a person who ran it as README-run.md says, from the row's own `rows/<row id>/gh-calls.log` and the session transcript.

Scenarios:

- S01 empty notes (both lists hold only `- None`): 0 questions.
- S02 additions only, including an `Assumption:` line: 0 questions.
- S03 reversed choice: 1 question.
- S04 dropped requirement: 1 question.
- S05 changed flag: 1 question.
- S06 user-stated fact contradicted by verified code: 1 question.
- S07 two contradictions at once: 1 question naming both.
- S08 additions plus one contradiction: 1 question, and the additions stay in the body.
- S09 a worker disagrees with a user-supplied flag and the issue is filed with the user's flag: 0 questions; the pushback comment is posted at standard and deep depth only.
- S10 an addition that is the only evidence of a contradiction: 1 question; the answer "keep my wording" removes only that content, every other addition stays.

Row pass rule (README-run.md, section "Reading a row"): zero REFUSED lines in the row's log, exactly one CREATE line, exactly one FIELD-POST line, the number of COMMENT lines in "Calls expected", the observed question count equal to the expected one, every addition present in the posted body, and no offer to approve the full body.

| Row | Scenario | Depth | Drafting worker | Expected questions | Observed questions | Answer given | Calls expected | Calls observed (from the log) | Additions kept in the posted body | Pushback comment (expected / observed) | Fake issue number | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01-quick | empty notes | quick | issue-worker-t3 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900001 | not run: owner run required |
| S01-standard | empty notes | standard | issue-worker-t2 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900002 | not run: owner run required |
| S01-deep | empty notes | deep | issue-worker-t1 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900003 | not run: owner run required |
| S02-quick | additions only | quick | issue-worker-t3 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900004 | not run: owner run required |
| S02-standard | additions only | standard | issue-worker-t2 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900005 | not run: owner run required |
| S02-deep | additions only | deep | issue-worker-t1 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900006 | not run: owner run required |
| S03-quick | reversed choice | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900007 | not run: owner run required |
| S03-standard | reversed choice | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900008 | not run: owner run required |
| S03-deep | reversed choice | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900009 | not run: owner run required |
| S04-quick | dropped requirement | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900010 | not run: owner run required |
| S04-standard | dropped requirement | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900011 | not run: owner run required |
| S04-deep | dropped requirement | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900012 | not run: owner run required |
| S05-quick | changed flag | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900013 | not run: owner run required |
| S05-standard | changed flag | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900014 | not run: owner run required |
| S05-deep | changed flag | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900015 | not run: owner run required |
| S06-quick | user-stated fact contradicted by verified code | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900016 | not run: owner run required |
| S06-standard | user-stated fact contradicted by verified code | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900017 | not run: owner run required |
| S06-deep | user-stated fact contradicted by verified code | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900018 | not run: owner run required |
| S07-quick | two contradictions at once | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900019 | not run: owner run required |
| S07-standard | two contradictions at once | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900020 | not run: owner run required |
| S07-deep | two contradictions at once | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900021 | not run: owner run required |
| S08-quick | additions plus one contradiction | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900022 | not run: owner run required |
| S08-standard | additions plus one contradiction | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900023 | not run: owner run required |
| S08-deep | additions plus one contradiction | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900024 | not run: owner run required |
| S09-quick | worker disagrees with a user-supplied flag | quick | issue-worker-t3 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900025 | not run: owner run required |
| S09-standard | worker disagrees with a user-supplied flag | standard | issue-worker-t2 | 0 | to fill | n/a | 1 create, 1 field POST, 1 comment | to fill | to fill | yes / to fill | 900026 | not run: owner run required |
| S09-deep | worker disagrees with a user-supplied flag | deep | issue-worker-t1 | 0 | to fill | n/a | 1 create, 1 field POST, 1 comment | to fill | to fill | yes / to fill | 900027 | not run: owner run required |
| S10-quick | addition that is the only evidence of a contradiction | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900028 | not run: owner run required |
| S10-standard | addition that is the only evidence of a contradiction | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900029 | not run: owner run required |
| S10-deep | addition that is the only evidence of a contradiction | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900030 | not run: owner run required |

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/fixtures/labels.json (full contents) ---
[{"name": "enhancement"}, {"name": "bug"}, {"name": "documentation"}]

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/fixtures/issue-types.json (full contents) ---
[{"id": 1, "name": "Feature"}, {"id": 2, "name": "Bug"}, {"id": 3, "name": "Test"}]

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/fixtures/issue-fields.json (full contents) ---
[{"id": 1, "name": "Complexity", "data_type": "single_select", "options": [{"id": 1, "name": "Simple"}, {"id": 2, "name": "Medium"}, {"id": 3, "name": "Complex"}]}]

--- new untracked file .dev/tasks/to-do/TASK-WF-issueSummary-20261125-190451/artifacts/create-run-kit/fixtures/duplicates.json (full contents) ---
[]


Codegraph context:
index_state=stale checked_at=2026-11-25T19:23:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-834 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-834
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor; dependents of the changed text that are not in this task's touched set are edited by later tasks of the plan.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
