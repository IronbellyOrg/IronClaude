16998e097f99aaab2e978d33f5106defc8eb7713
## family revert-preimage
defect form: a revert whose preimage is compared with the same text it was computed from, or a hunk reference not tied to what the caller saw
command: grep -n -e revert_hunks( -e reread_doc( src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py
before:
299:def revert_hunks(lines: list[str], hunks: list[dict], old: list[str]):
1128:        lines, reverted, failed = revert_hunks(
1314:                reread_doc(doc) != live_text
1318:                final, reverted, failed = revert_hunks(live, unclaimed, old)
coupled sites: begin's revert (:1314-1318) already re-reads the document; status's provisional hunk list (the caller's view) needs the key
after:
299:def revert_hunks(lines: list[str], hunks: list[dict], old: list[str]):
1133:        current = reread_doc(ledger.doc_path(state))
1137:            lines, reverted, failed = revert_hunks(
1324:                reread_doc(doc) != live_text
1328:                final, reverted, failed = revert_hunks(live, unclaimed, old)
(revert-unclaimed now re-reads at :1133; --hunk takes the key status prints; status lists "key")

## family phase-code
defect form: a subcommand whose brief names E-PHASE returns E-TERMINAL through require_phase in a terminal phase
command: grep -n -e 'require_phase(state, "revise")' src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py
before:
1079:        require_phase(state, "revise")
1107:        require_phase(state, "revise")
1273:        require_phase(state, "revise")
coupled sites: :1079 is answer and :1273 is begin, whose briefs name E-TERMINAL (correct there)
after:
1079:        require_phase(state, "revise")
1283:        require_phase(state, "revise")
(revert-unclaimed uses its own check at :1107 that refuses E-PHASE in every phase but revise)
