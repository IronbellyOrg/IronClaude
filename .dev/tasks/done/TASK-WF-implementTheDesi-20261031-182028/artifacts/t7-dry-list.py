"""Read-only dry check: list review threads of a live poll snapshot read from stdin."""
import json, sys
from superclaude.pr_submit import DetectionContract
from superclaude.pr_submit.reviewers import classify_codex, list_review_threads, reviewer_activity
snap = json.load(sys.stdin); c = DetectionContract.load()
print(f"PR {snap['pr']} head={snap['head_sha'][:8]} flags={snap['reviews_ok']},{snap['comments_ok']},{snap['threads_ok']} activity={reviewer_activity(snap, c)} codex_state_at_head={classify_codex(snap, c)}")
for row in list_review_threads(snap, c):
    print(f"  {row['reviewer']:7} {row['path']}:{row['line']}/{row['original_line']} resolved={row['is_resolved']} priority={row['priority']} severity={row['severity']} comment={row['comment_id']}")
