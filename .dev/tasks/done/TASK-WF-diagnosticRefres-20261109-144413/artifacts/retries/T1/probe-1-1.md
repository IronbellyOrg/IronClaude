8365c62c3b202c1af844fd81a67754e15788d65a
family=mode-drift-gate (covers F1.1, F1.2 of review-1.md)
defect: the before-phase gate must stop on any drift beyond the three stale files, mode-only included, unless an owner authorization naming the exact entries is recorded in compatibility-before.json and authorization-and-binding.json. No authorization was recorded when the first run proceeded.
authorization: owner reply '1' at 2026-11-10T00:02Z relayed by the coordinator; covers exactly the 19 mode-only entries (2 directories, 17 refs files), source 700/600 against installed 755/644, tightening only.
command: grep -n -E 'selected_mode_tightening|mode_changes|EXPECTED_DRIFT|mode_drift' compatibility_state.py
before:
42:EXPECTED_DRIFT = ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"]
202:    mode_changes = {
210:    assert all((v["source"] & ~v["installed"]) == 0 for v in mode_changes.values()), (
213:    state["selected_mode_tightening"] = mode_changes
216:    if drift != EXPECTED_DRIFT or mode_changes:
225:        state["mode_drift"] = sorted(
239:                    "mode_drift_count": len(state["mode_drift"]),
245:                        for k in state["mode_drift"][:5]
334:        assert changed == EXPECTED_DRIFT, changed
339:                "selected_mode_tightening": before["selected_mode_tightening"],
coupled sites: compatibility_state.py:216 (the stop condition); :213 (the record of the mode changes); :262 and :265-266 (the backup is created and refuses an existing one, so a re-run of the before phase must verify the existing backup instead); :271-285 (authorization-and-binding.json writer); :334-339 (after phase); rebaseline-record.json (decision B provenance).
after: (re-run 2026-11-10 after the fix)
  42:EXPECTED_DRIFT = ["SKILL.md", "refs/diagnosability-audit.md", "refs/doc-discovery.md"]
  66:AUTHORIZED_MODE_TIGHTENING = {
  70:OWNER_DECISION_A = {
  84:    "entries": sorted(AUTHORIZED_MODE_TIGHTENING),
  86:OWNER_DECISION_B = {
  253:    mode_changes = {
  261:    assert all((v["source"] & ~v["installed"]) == 0 for v in mode_changes.values()), (
  264:    state["selected_mode_tightening"] = mode_changes
  267:    if drift != EXPECTED_DRIFT or mode_changes != AUTHORIZED_MODE_TIGHTENING:
  276:        state["mode_drift"] = sorted(
  290:                    "mode_drift_count": len(state["mode_drift"]),
  296:                        for k in state["mode_drift"][:5]
  327:    state["owner_decision_A"] = OWNER_DECISION_A
  328:    state["owner_decision_B"] = OWNER_DECISION_B
  336:                "owner_decision_A": OWNER_DECISION_A,
  337:                "owner_decision_B": OWNER_DECISION_B,
  395:        assert changed == EXPECTED_DRIFT, changed
  400:                "selected_mode_tightening": before["selected_mode_tightening"],
after-result: stop condition at the drift gate is 'drift != EXPECTED_DRIFT or mode_changes != AUTHORIZED_MODE_TIGHTENING' (exact 19 keys, exact value pairs, tightening only); before phase re-run passed (before-rerun.log); owner decision A and B recorded in compatibility-before.json and authorization-and-binding.json; backup verified and reused, not overwritten.
