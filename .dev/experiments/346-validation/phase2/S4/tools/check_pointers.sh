#!/usr/bin/env bash
# Check that the evidence pointers cited in ANALYSIS.md / REPLAY.md / baseline-metrics.json exist and say what is claimed.
# Read-only. Usage: tools/check_pointers.sh   (from anywhere). Exit 0 and "POINTERS_OK n=<count>" when all pass.
set -u -o pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BM=/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global/189f8649-3921-4435-bc6b-a15182a20399.jsonl
SA=${BM%.jsonl}/subagents
QA="$here/evidence/baseline-qa-outputs"
TF="$here/inputs/task-file/TASK-RESEARCH-bmad-first-use-20261107-075901.md.v2-at-2026-11-07T15-38-37Z"
P1=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase1/REPORT.md
n=0; bad=0
ok()   { n=$((n+1)); }
fail() { bad=$((bad+1)); echo "FAIL: $*"; }
# bm LINE REGEX : line LINE of the main log matches REGEX
bm()  { local t; t=$(sed -n "${1}p" "$BM"); if printf '%s' "$t" | rg -q -- "$2"; then ok; else fail "BM L$1 !~ $2"; fi; }
sa()  { local t; t=$(sed -n "${2}p" "$SA/agent-$1.jsonl" 2>/dev/null); if printf '%s' "$t" | rg -q -- "$3"; then ok; else fail "SA $1 L$2 !~ $3"; fi; }
fl()  { local t; t=$(sed -n "${2}p" "$1" 2>/dev/null); if printf '%s' "$t" | rg -q -- "$3"; then ok; else fail "$(basename "$1") L$2 !~ $3"; fi; }
ex()  { if [ -e "$1" ]; then ok; else fail "missing $1"; fi; }

# main log
bm 13 'Please carry out this task from my Orca coordinator'
bm 23 'f1ac0c93 Merge pull request #476'
bm 138 '"name":"Skill"'; bm 142 'Base directory for this skill: /home/coder/.claude/skills/tech-research'
bm 156 '"name":"Skill"'; bm 158 'Base directory for this skill: /home/coder/.claude/skills/task'
bm 868 'the exact commit of this worktree'
bm 1093 '6 new blocking issues'
bm 1173 'GATE1_FINAL: FAIL - HALT'; bm 1247 'orchestration ask'; bm 1476 'GATE1_FINAL: PASS'
bm 2308 'GATE2_FINAL: FAIL - HALT'; bm 2377 'orchestration ask'; bm 2742 'GATE2_FINAL: PASS'
bm 2758 'rf-assembler'; bm 2844 '1785'
bm 3395 'GATE3_FINAL: FAIL - HALT'; bm 3462 'orchestration ask'; bm 3702 'GATE3_FINAL: PASS'
bm 3936 'GATE4_FINAL: PASS'
bm 4382 'GATE5_FINAL: FAIL - HALT'; bm 4513 'msg_8c3d61e635e2'; bm 4601 'GATE5_FINAL: PASS'
bm 4631 'Final validation'; bm 5109 'sc-workflow-protocol'; bm 5306 'sc-reflect-protocol'
for l in 19 29 4771 4785 4818; do bm $l 'spec-panel'; done
# every Agent wrapper line in briefs/INDEX.md is an Agent tool_use for that agent type
while IFS='|' read -r _ f ln _ st _ aid _; do
  f=$(echo "$f" | tr -d ' '); ln=$(echo "$ln" | tr -d ' '); st=$(echo "$st" | tr -d ' '); aid=$(echo "$aid" | tr -d ' ')
  case "$f" in G*|W*|Z*) ;; *) continue;; esac
  bm "$ln" "\"subagent_type\":\"$st\""; ex "$SA/agent-$aid.jsonl"; ex "$here/briefs/$f"
done < <(rg '^\| [GWZ][^|]*\.md \|' "$here/briefs/INDEX.md")
# agent logs cited
sa a9c6678fe08ab2dda 44 '"name":"Write"'; sa a9c6678fe08ab2dda 124 'Quality Gates and User-Accepted Exceptions'
ex "$SA/agent-a2db640f53a99c857.jsonl"; ex "$SA/agent-a06234f4b582724ab.jsonl"
# gate decision / consolidated files
fl "$QA/qa-gate1-decision.md" 13 'analyst-completeness-report'; fl "$QA/qa-gate1-decision.md" 19 'introduced X-1'
fl "$QA/qa-gate1-decision.md" 40 'New-1'; fl "$QA/qa-gate1-decision.md" 42 'GATE1_FINAL: FAIL - HALT'; fl "$QA/qa-gate1-decision.md" 46 'msg_acc5015c9601'; fl "$QA/qa-gate1-decision.md" 48 'GATE1_FINAL: PASS'
fl "$QA/qa-gate2-decision.md" 13 'analyst-synthesis-accuracy'; fl "$QA/qa-gate2-decision.md" 39 'V-1'; fl "$QA/qa-gate2-decision.md" 40 'V-2'; fl "$QA/qa-gate2-decision.md" 42 'GATE2_FINAL: FAIL - HALT'; fl "$QA/qa-gate2-decision.md" 48 'GATE2_FINAL: PASS'
fl "$QA/qa-gate3-decision.md" 5 'SEVERITY_DOWNGRADES: 5'; fl "$QA/qa-gate3-decision.md" 21 'template-conformance'; fl "$QA/qa-gate3-decision.md" 53 'N-1'; fl "$QA/qa-gate3-decision.md" 54 'N-2'; fl "$QA/qa-gate3-decision.md" 56 'GATE3_FINAL: FAIL - HALT'; fl "$QA/qa-gate3-decision.md" 62 'GATE3_FINAL: PASS'
fl "$QA/qa-gate4-decision.md" 13 'qa-source-fidelity-report-1'; fl "$QA/qa-gate4-decision.md" 23 'GATE4_FINAL: PASS'
fl "$QA/qa-gate5-decision.md" 5 'SEVERITY_DOWNGRADES: 2'; fl "$QA/qa-gate5-decision.md" 15 'slice1'; fl "$QA/qa-gate5-decision.md" 41 'N-1'; fl "$QA/qa-gate5-decision.md" 43 'GATE5_FINAL: FAIL - HALT'; fl "$QA/qa-gate5-decision.md" 49 'GATE5_FINAL: PASS'
for f in "qa-consolidated-findings-phase3.md 9" "qa-consolidated-findings-phase3-cycle2.md 6" "qa-consolidated-findings-phase5.md 8" "qa-consolidated-findings-phase5-cycle2.md 3" "qa-consolidated-findings-phase6.md 18" "qa-consolidated-findings-phase6-cycle2.md 5" "qa-fidelity-consolidated-findings.md 1" "qa-anti-omission-consolidated-findings.md 4" "qa-anti-omission-consolidated-findings-cycle2.md 3"; do set -- $f; fl "$QA/$1" 1 "^BLOCKING_COUNT: $2\$"; done
fl "$QA/qa-verification-phase3-cycle2-content.md" 34 'PARTLY RESOLVED'; fl "$QA/qa-verification-phase3-cycle2-content.md" 55 'New-1'
fl "$QA/qa-verification-phase5-cycle1-content.md" 21 'PARTLY RESOLVED'; fl "$QA/qa-verification-phase5-cycle1-content.md" 33 'N-3'
fl "$QA/qa-verification-phase5-cycle2-content.md" 21 'redefining'; fl "$QA/qa-verification-phase5-cycle2-content.md" 29 'V-1'; fl "$QA/qa-verification-phase5-cycle2-content.md" 32 'redefining'; fl "$QA/qa-verification-phase5-cycle2-content.md" 36 'V-2'
fl "$QA/qa-fix-verification-qualitative-phase6-cycle1.md" 14 'caused or exposed'; fl "$QA/qa-fix-verification-qualitative-phase6-cycle1.md" 39 'B-1'; fl "$QA/qa-fix-verification-qualitative-phase6-cycle1.md" 47 'B-2'
fl "$QA/qa-fix-verification-phase6-cycle1.md" 60 'F-1'
fl "$QA/qa-fix-verification-qualitative-phase6-cycle2.md" 17 'PARTLY RESOLVED'; fl "$QA/qa-fix-verification-qualitative-phase6-cycle2.md" 19 'PARTLY RESOLVED'
fl "$QA/analyst-completeness-report.md" 180 '365 lines'
# task file lines (state v2)
fl "$TF" 130 'Maximum 2 fix cycles \(3 reviews\)'; fl "$TF" 214 'at most 2 fix cycles'; fl "$TF" 361 'at most 2 fix cycles'
for l in 218 222 226 234 238 242 254 258 262 308 312 316 324 328 332 344 348 352 371 373 375 379 381 383 387 393 397 399 405 407 409 417 419 421 425 427 429 447 449 451 455 457 459 465 467 469; do fl "$TF" $l 'BEGIN AGENT PROMPT'; done
for l in 230 320 391 423 453 475; do fl "$TF" $l 'Read '; done
fl "$TF" 246 'SEVERITY_DOWNGRADES'; fl "$TF" 535 'Pre-start user exception'
# phase 1 report lines cited
fl "$P1" 196 'I4 BMAD first-use research report'; fl "$P1" 235 'Tools/skills'; fl "$P1" 239 'Cost to find'
# files named in the package
for f in ANALYSIS.md REPLAY.md baseline-metrics.json inputs/MANIFEST.sha256 inputs/SOURCES.md briefs/INDEX.md briefs/S-user-resume-brief_L13.md briefs/S-skill-tech-research_L138.json briefs/S-skill-task_L156.json briefs/taskfile-L222_embedded-prompt.md evidence/m4-sizes.tsv evidence/agent-costs.tsv tools/make_gate_entry.sh tools/reconstruct.py tools/reverse_notes.py inputs/gate3-start/RESEARCH-REPORT-bmad-first-use.md inputs/gate1-start/research/research-notes.md; do ex "$here/$f"; done
# file-history backups cited
for h in 32d05845d5285d52@v1 32d05845d5285d52@v2 ae5475a180c7c83a@v1 b1f12dba87654e26@v1 3e4a4f8f424a5b4d@v1 4bee01eff428f97f@v1 7c3e47725f1b55c6@v1 ca7857aee503d1e6@v1; do ex "/home/coder/.claude/file-history/189f8649-3921-4435-bc6b-a15182a20399/$h"; done
if [ "$bad" -eq 0 ]; then echo "POINTERS_OK n=$n"; else echo "POINTERS_FAIL bad=$bad of n=$((n+bad))"; exit 1; fi
