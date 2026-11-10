b675805775e8472e8b3a8576b9f83a1347a648e9
family audit-hunk-real-dropped
form: an audit record with a hunk key and real:true has no effect on statuses or on the apply-audit message
command: grep -n -e 'reinstated' -e 'a.get("id")' -e '"hunk" in' -- src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py tests/skills/test_stoprule_script.py
before:
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:908:        if a.get("id") and a.get("real") is True
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1106:        f"apply-audit: {len(items)} items audited; reinstated: {', '.join(real) or 'none'}"
tests/skills/test_stoprule_script.py:883:    assert sum("hunk" in i for i in items.values()) == 2
coupled sites: claim_statuses (audited set), audit_items (H items), cmd_apply_audit (message), compute_verdict in Task 5
after:
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:908:        if a.get("id") and a.get("real") is True
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:935:        a for a in of_kind(records, "audit") if "hunk" in a and a.get("real") is True
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1117:        if r["real"] and "hunk" in r
src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1120:    print(f"  claims reinstated as confirmed-audit: {', '.join(claims) or 'none'}")
tests/skills/test_stoprule_script.py:883:    assert sum("hunk" in i for i in items.values()) == 2
tests/skills/test_stoprule_script.py:1014:    assert "claims reinstated as confirmed-audit: none" in out
