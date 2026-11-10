16998e097f99aaab2e978d33f5106defc8eb7713
## family revert-replay
defect form: a mutation whose result depends on the live document builds its request digest without the document's state, so a later call after a new edit is replayed
command: grep -n -e canonical( src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py
before:
98:def canonical(obj) -> bytes:
106:        canonical({k: v for k, v in state.items() if k != "body_sha256"})
437:    return data, canonical(data)
1104:        return canonical({"hunk": args.hunk})
1264:        return canonical(
1620:        return canonical({"report": str(report)})
coupled sites: :1104 revert-unclaimed (the finding); answer (cmd_answer at :1075 uses read_input's digest at :437, input only, while its provisional hunks come from the live document: same defect form, sibling in scope); :1264 begin already carries the document sha256; :1620 close depends on the report, not the document (Task 3 owns the report-tail rules); :437 for find is bound to snapshot r1, which never changes

after:
98:def canonical(obj) -> bytes:
106:        canonical({k: v for k, v in state.items() if k != "body_sha256"})
437:    return data, canonical(data)
655:            doc_unchanged = op.get("doc_after") in (
657:                live_binding(args)["doc_sha256"],
1080:def live_binding(args) -> dict:
1096:        return read_only_input() + b"\0" + canonical(live_binding(args))
1115:        doc_after = sha256_bytes(ledger.doc_path(state).read_bytes())
1119:            "_op": {"claims": claims, "gaps": gaps, "doc_after": doc_after},
1129:        return canonical({"hunk": args.hunk, **live_binding(args)})
1182:            "_op": {"x_items": x_items, "doc_after": sha256_text(after_text)},
1290:        return canonical(
1646:        return canonical({"report": str(report)})
