# Reviewer 1 brief (persona: analyzer; model class: sonnet)

You are a read-only Tier-2 reviewer for a UC-1 (pre-execution) reflection. Audit whether the proposed tasklist can be implemented correctly against the driving spec and the real code. You may Read, Grep and Glob; you may not run commands or edit files. RETURN your card as the final message (YAML, format at the end); do not write files. Tag every claim Grounded (with a `file:line` you actually Read) or `[INFERRED]`. Drop claims you can tag neither way. Start from an adversarial position: assume the plan has defects and look for them.

Driving spec: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/source.md (one long line)
Tasklist: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md
Persona lens: root-cause and design correctness. Will the planned bash mechanics (exit statuses, `trap`, `read -t`, command substitution, `exec`, the python `select` probe, `stty`) actually deliver what each task claims? Which edge cases break them?

## T1 card excerpt

Candidate risks from the Tier-1 card (verbatim, unverified; confirm or reject each with evidence):
- R1. Task 2 plans exit status 3 with the pasted text on stdout. ccsession-orca reads it with command substitution, which strips trailing newlines and cannot tell a message from a name by content; the plan keys on the exit status, which looks right, but multi-line text and NUL/escape bytes through `$(...)` and `read -r` need checking.
- R2. Task 2 detects a multi-line paste by "more bytes already waiting after the line", reusing the python `select` probe that needs line mode switched off; the existing probe is run once before the question. A second probe after `read` has a timing race (a paste may not have fully arrived).
- R4. Task 3 classifies `--session-id` as task-carrying and auto-names it. Passing both ccsession `--name` and Claude `--session-id` may conflict with the label/resume logic in ccsession (a saved label resumes by id).
- R5. Task 3 lifts a Claude `--name`/`-n` out of Orca's arguments into ccsession's `--name`; this changes today's behaviour and is not in the source text.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T03:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-315-ccsession-name-prompt projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-315-ccsession-name-prompt (the index holds python and yaml only; ccsession and ccsession-orca are bash, so use Read and Grep for them)

### src/superclaude/skills/ccsession-tag/ccsession-orca:48-63
```bash
ask=1
[ -t 0 ] && [ -t 1 ] || ask=0
[ "${CCSESSION_AUTOSTART:-1}" = 0 ] && ask=0
_skip=0
for _arg in "$@"; do
  if [ "$_skip" = 1 ]; then
    _skip=0
    continue
  fi
  case "$_arg" in
    --prefill) _skip=1 ;;
    --resume|--resume=*|-r|--continue|-c) ask=0 ;;
  esac
done
```

### src/superclaude/skills/ccsession-tag/ccsession-orca:97-117
```bash
name=""
if [ "$ask" = 1 ]; then
  ask_timeout="${CCSESSION_ASK_TIMEOUT:-30}"
  ...
  trap ':' INT
  name=$(CCSESSION_ASK_TIMEOUT="$ask_timeout" "$CCSESSION" --ask "$hint") || name=""
  trap - INT
fi
if [ -n "$name" ]; then
  exec "$CCSESSION" --name "$name" --shim --claude-args "$@"
fi
exec "$CCSESSION" --shim --claude-args "$@"
```

### src/superclaude/skills/ccsession-tag/ccsession:1417-1437 and 1469-1492
```bash
ask_session_name() {
  local hint="${1:-Enter = untagged, Ctrl+C = plain shell}"
  [ -t 0 ] && [ -t 2 ] || return 1
  local tty_mode="" waiting=1
  trap 'if [ -n "$tty_mode" ]; then stty "$tty_mode" 2>/dev/null || :; fi; echo >&2; exit 130' INT
  tty_mode=$(stty -g 2>/dev/null) && stty -icanon min 0 time 0 2>/dev/null
  python3 -c 'import select, sys; sys.exit(0 if select.select([0], [], [], 0)[0] else 1)' 2>/dev/null && waiting=0
  [ -n "$tty_mode" ] && stty "$tty_mode" 2>/dev/null
  if [ "$waiting" = 0 ]; then trap - INT; return 1; fi
  ...
  local read_opts=() limit="${CCSESSION_ASK_TIMEOUT:-0}"
  case "$limit" in '' | *[!0-9]* | 0) : ;; *) read_opts=(-t "$limit") ;; esac
  trap 'echo >&2; exit 130' INT
  while :; do
    read -r ${read_opts[@]+"${read_opts[@]}"} -p "Session name ($hint): " name || { echo >&2; return 1; }
    [ -z "$name" ] && break
    if [ "$name" = "*" ]; then show_saved "" "..."; continue; fi
    validate_label "$name" >/dev/null && break
  done
  trap - INT
  printf '%s\n' "$name"
}
```
Also Read ccsession:275-302 (`validate_label`), ccsession:1543-1546 (`--ask` dispatch), ccsession:1635-1714 (launch paths) and the plan Tasks 1 to 4.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-003 30-second timer inside ask_session_name | Task 2 | covered | plan Task 2 |
| INF-004 Ctrl+C exits 130, orca stops trapping INT | Task 4 | covered | plan Task 4 |
| INF-007 typed line that cannot be a name goes to Claude | Task 2, Task 4 | covered by reading (matcher 0.59) | plan Tasks 2, 4 |
| INF-010 Enter gets an auto-name | Task 2, Task 4 | covered | plan Task 2 |

## Card format to return

```yaml
reviewer: 1
persona: analyzer
findings:
  - id: F1
    claim: <one sentence>
    tag: grounded | inferred
    evidence: <file:line you Read, or null when inferred>
    severity: blocking | minor      # blocking = would make a task fail its own acceptance criteria or break existing behaviour
    deviation_class: authorized | necessary | drift | regression | none
    recommendation: <file + change + how to verify>
risks_rejected: [<R-ids you checked and found fine, with one-line evidence>]
verdict: ready | ready-with-notes | not-ready
self_confidence: <0.0-1.0>
```
