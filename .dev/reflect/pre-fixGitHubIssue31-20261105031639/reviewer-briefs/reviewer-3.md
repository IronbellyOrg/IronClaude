# Reviewer 3 brief (persona: refactorer; model class: opus)

You are a read-only Tier-2 reviewer for a UC-1 (pre-execution) reflection. Audit the structure and scope of the proposed tasklist. You may Read, Grep and Glob; you may not run commands or edit files. RETURN your card as the final message (YAML, format at the end); do not write files. Tag every claim Grounded (with a `file:line` you actually Read) or `[INFERRED]`. Drop claims you can tag neither way. Start from an adversarial position: assume the plan expands scope, hides decisions, or has bad task boundaries, and look for that.

Driving spec: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/source.md (one long line)
Tasklist: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md
Persona lens: structure and scope discipline. Which plan decisions go beyond the source text (the Constraints section lists some), are they safe and reversible, and are task boundaries and dependencies sound (each task reviewable alone, no hidden coupling, no duplicated logic between ccsession and ccsession-orca)?

## T1 card excerpt

- R3. Task 3 and Task 4 auto-name every non-interactive launch that carries a task (prompt-bearing, no terminal). Orchestrators that start many sessions will add many saved names; no cleanup or cap is planned.
- R4. Task 3 classifies `--session-id` as task-carrying and auto-names it. Passing both ccsession `--name` and Claude `--session-id` may conflict with the label/resume logic in ccsession (a saved label resumes by id).
- R5. Task 3 lifts a Claude `--name`/`-n` out of Orca's arguments into ccsession's `--name`; this changes today's behaviour (the value currently reaches Claude as-is and the question is still asked) and is not in the source text. It is listed in Constraints as a plan-author decision.
- R6. Print mode (`-p`/`--print`) and `CCSESSION_AUTOSTART=0` stay untagged by plan-author decision, also not in the source text.
- R7. Task 7 depends only on Task 5 and Task 8 only on Task 5; Task 6 depends on Task 5 while it tests behaviour added in Tasks 1 and 2. Ordering is valid but Task 6 and Task 7 are large single tasks.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-05T03:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-315-ccsession-name-prompt projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-315-ccsession-name-prompt (the index holds python and yaml only; ccsession and ccsession-orca are bash, so use Read and Grep for them)

### src/superclaude/skills/ccsession-tag/ccsession-orca:71-95
```bash
if [ "$ask" = 1 ] && [ -n "${ORCA_PANE_KEY:-}" ]; then
  plain=1
  for _arg in "$@"; do
    case "$_arg" in
      --prefill | --prefill=* | -p | --print | --name | --name=* | -n | \
        --session-id | --session-id=* | --fork-session | --from-pr | --from-pr=*) plain=0 ;;
      -*) : ;;
      *) plain=0 ;;
    esac
  done
  reopen=""
  if [ "$plain" = 1 ]; then
    reopen=$("$CCSESSION" --orca-tab-reopen 2>/dev/null) || reopen=""
  fi
  ...
```
The reopen block reads `ask` (computed from terminal, CCSESSION_AUTOSTART and resume-like options). Plan Task 3 says the reopen keeps "the same conditions as before" while `ask` itself changes meaning (it will also be 0 for a launch with a task or name).

### src/superclaude/skills/ccsession-tag/ccsession:1649-1654 and 1681-1692
```bash
if [ "$NAME_GIVEN" = 1 ]; then
  TOPIC=$(validate_label "$NAME_ARG") || exit 2
else
  TOPIC=$(validate_label "$1") || exit 2
  shift
fi
...
if [ -f "$TOPIC_FILE" ]; then
  SESSION_ID=$(head -n 1 "$TOPIC_FILE")
  if ! session_saved "$SESSION_ID"; then ... rm -f "$TOPIC_FILE"; fi
fi
if [ -f "$TOPIC_FILE" ]; then
  echo "[ccsession] Resuming '$TOPIC' (session ${SESSION_ID:0:8})"
  ... exec "$CLAUDE_BIN" ... --name "$TOPIC" --resume "$SESSION_ID" "$@"
```
A name that equals a saved label resumes that session; Read the plan Constraints and Tasks 1, 3, 4, 6, 7, 8 and the "Decisions taken by the plan author" bullet.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| Plan Constraints: master only, no clayphi branch, Coder untouched | INF-015, INF-016 | covered in Constraints only | plan Constraints |
| Plan-author decisions: print mode, AUTOSTART=0, resume-like, --name lift | none in source | added by plan author | plan Constraints |

## Card format to return

```yaml
reviewer: 3
persona: refactorer
findings:
  - id: F1
    claim: <one sentence>
    tag: grounded | inferred
    evidence: <file:line you Read, or null when inferred>
    severity: blocking | minor      # blocking = a plan decision contradicts the source or existing behaviour that must be kept, or task boundaries make a task impossible to review or order
    deviation_class: authorized | necessary | drift | regression | none
    recommendation: <file + change + how to verify>
scope_additions: [<plan decisions beyond the source, with a keep/ask-owner/remove opinion>]
verdict: ready | ready-with-notes | not-ready
self_confidence: <0.0-1.0>
```
