9e83e1e98bec90d57fa2a925fa0bf92ecae216ee
## family verdict-new-table-parse (F3.1)
defect form: a review-3 row with a status word and no label is skipped even when its id is not a review-2 id
command: grep -n -e 'if any(c.lower() in STATUS_WORDS for c in cs\[1:\])' -e 'unlabelled_blocking(' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
914:def unlabelled_blocking(text: str) -> list[str]:
935:        if any(c.lower() in STATUS_WORDS for c in cs[1:]):
993:            [t for t, g in new.items() if g["blocking"]] + unlabelled_blocking(r3)
coupled sites: parse_report prior branch (T2, not changed: verdict-side fix); verdict tests
after: 914:def unlabelled_blocking(text: str, r2_ids: set[str] = frozenset()) -> list[str]:
after: 937:        if any(c.lower() in STATUS_WORDS for c in cs[1:]) and set(toks) <= r2_ids:
after: 996:            + unlabelled_blocking(r3, set(ids) | set(state.get("prior_only", [])))
