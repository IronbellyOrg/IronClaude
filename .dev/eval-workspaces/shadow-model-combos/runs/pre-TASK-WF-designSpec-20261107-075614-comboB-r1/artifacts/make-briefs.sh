#!/usr/bin/env bash
# Materialize the three reviewer briefs (SKILL 3B.0). Generation only; reads the inputs, writes <out>/reviewer-briefs/.
set -u
ROOT=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
ID=TASK-WF-designSpec-20261107-075614
OUT=$ROOT/.dev/eval-workspaces/shadow-model-combos/runs/pre-$ID-comboB-r1
REL=.dev/eval-workspaces/shadow-model-combos/input/$ID
SPEC=$ROOT/$REL/source.md
PLAN=$ROOT/$REL/$ID.md
SPECR=$REL/source.md
PLANR=$REL/$ID.md
CG="codegraph run state: index_state=fresh checked_at=2026-11-13T03:05:00Z worktree_root=$ROOT projectPath=$ROOT"

FMT='End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Write the heading as exactly `## Findings block` and open the fence as exactly ```findings-v2 (not ```json, not `## Findings`). Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.'

hunk() { # file-abs file-rel from to lang
  printf '### %s:%s-%s\n\n```%s\n' "$2" "$3" "$4" "$5"; sed -n "${3},${4}p" "$1"; printf '```\n\n'; }

common_head() { # N persona
  cat <<EOF
# Reviewer brief $1 (persona: $2) - UC-1 pre-execution review

You are a read-only reviewer. Audit the PLAN (tasklist) against the SPEC. Do not run commands, do not edit files, do not write files; return your card as text only.
Use these repo-relative paths in citations: spec = \`$SPECR\`, plan = \`$PLANR\`. Cite role \`spec\` for the spec and role \`plan\` for the plan; line numbers are 1-based lines of those files.
The working tree is HEAD, which already contains the merged feature. The spec's facts were true at base commit e8db2fe6. Judge the plan against the spec and against base-commit facts; do not treat code that exists only at HEAD as evidence about what the plan should have said. Say so when a finding depends on HEAD-only code.
Report only defects you can ground in a quote. A finding must name what a builder following the plan would get wrong. Zero findings is a valid answer if you state which rows you checked.

EOF
}

mkdir -p "$OUT/reviewer-briefs"
FB() { printf '%s\n\n' "$FMT"; }

# ---- reviewer 1 analyzer
{
  common_head 1 analyzer
  echo '## T1 card excerpt'; echo
  sed -n '/^## Grounding at the spec base commit/,/^## Confidence and gaps/p' "$OUT/t1-card.md" | sed '$d' | sed -E "s/^## (.*)$/**\1**/"
  FB
  echo '## Grounding hunks'; echo
  echo "$CG"; echo
  hunk "$SPEC" "$SPECR" 75 127 text
  hunk "$SPEC" "$SPECR" 129 210 text
  hunk "$PLAN" "$PLANR" 52 91 markdown
  echo '## Coverage slice'; echo
  echo '| Requirement / Task | Card ID | Status | Grounding |'; echo '|---|---|---|---|'
  jq -r '.rows[]|select((.id|ltrimstr("INF-")|tonumber)>=19 and (.id|ltrimstr("INF-")|tonumber)<=42)|"| \(.id) \(.quote[0:90]|gsub("\\|";"/")) | \(.matched_task_ids[0] // "none") | \(if .matched_task_ids==[] then "unmapped" else "mapped" end) | \(.citation) |"' "$OUT/artifacts/coverage-matrix.json"
} > "$OUT/reviewer-briefs/reviewer-1.md"

# ---- reviewer 2 qa (spec body as grounding hunks)
{
  common_head 2 qa
  echo 'Persona line: Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.'; echo
  echo '## T1 card excerpt'; echo
  sed -n '/^## Coverage (mechanical/,/^## Grounding at the spec base commit/p' "$OUT/t1-card.md" | sed '$d' | sed -E "s/^## (.*)$/**\1**/"
  FB
  echo '## Grounding hunks'; echo
  echo "$CG"; echo
  hunk "$SPEC" "$SPECR" 1 378 markdown
  echo '## Coverage slice'; echo
  echo '| Requirement / Task | Card ID | Status | Grounding |'; echo '|---|---|---|---|'
  jq -r '.rows[]|select((.id|ltrimstr("INF-")|tonumber)<=18 or (.id|ltrimstr("INF-")|tonumber)>=43)|"| \(.id) \(.quote[0:90]|gsub("\\|";"/")) | \(.matched_task_ids[0] // "none") | \(if .matched_task_ids==[] then "unmapped" else "mapped" end) | \(.citation) |"' "$OUT/artifacts/coverage-matrix.json"
} > "$OUT/reviewer-briefs/reviewer-2.md"

# ---- reviewer 3 refactorer (plan structure)
{
  common_head 3 refactorer
  echo '## T1 card excerpt'; echo
  sed -n '/^## Candidate findings/,/^## Confidence and gaps/p' "$OUT/t1-card.md" | sed '$d' | sed -E "s/^## (.*)$/**\1**/"
  sed -n '/^## Recommendations/,$p' "$OUT/t1-card.md" | sed -E "s/^## (.*)$/**\1**/"
  FB
  echo '## Grounding hunks'; echo
  echo "$CG"; echo
  hunk "$PLAN" "$PLANR" 1 30 markdown
  hunk "$PLAN" "$PLANR" 104 200 markdown
  hunk "$SPEC" "$SPECR" 283 301 markdown
  hunk "$SPEC" "$SPECR" 358 378 markdown
  echo '## Coverage slice'; echo
  echo '| Requirement / Task | Card ID | Status | Grounding |'; echo '|---|---|---|---|'
  jq -r '.rows[]|select((.id|ltrimstr("INF-")|tonumber)>=43)|"| \(.id) \(.quote[0:90]|gsub("\\|";"/")) | \(.matched_task_ids[0] // "none") | \(if .matched_task_ids==[] then "unmapped" else "mapped" end) | \(.citation) |"' "$OUT/artifacts/coverage-matrix.json"
} > "$OUT/reviewer-briefs/reviewer-3.md"
wc -c "$OUT"/reviewer-briefs/*.md
