82b89d847c64a3eb5f7cf540b3acf9d9b2a2be3b
family gate-evidence: the gate record says reviewer rows passed but no reviewer scorecard is in the gate folder.
search: grep -n -F -e RB-29 .dev/issues/409/visual-parity/scores/p2/scores.json
before: scores.json and notes.md only; the gate folders hold checks.json and the renders
coupled sites: iter-1 and iter-2 gate folders
after: iter-2/reviewer-outputs/width-160, width-116 and width-80 scorecards, and iter-1/reviewer-outputs/summary.md
