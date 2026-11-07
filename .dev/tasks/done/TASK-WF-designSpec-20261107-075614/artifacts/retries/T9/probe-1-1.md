4e6a6df7dfa46c8c0d4c1c0d3b7cde488dfdff79
family wave0-test-gate-coverage
defect form: the Wave 0 check lists four literal gate phrases, so other wordings of an L3 or draft condition pass it.
command: grep -n -e "L3 only" -e "only at L3" -e "loading = " -e "gate" -- tests/pr_submit/test_merge_guard_protocol.py
before:
  381:    loading = bullet.split("At L3 with", 1)[0]
  382:    for gate in ("L3 only", "only at L3", "--merge-guard draft", "`draft`"):
  383:        if gate in loading:
  384:            problems.append(f"the loading sentence carries the gate {gate!r}")
  409:    assert any("gate" in p for p in _wave0_problems(gated))
coupled sites: the gate loop of _wave0_problems and the mutation test test_the_wave0_check_fails_on_each_way_the_bullet_can_go_wrong.
after:
  383:    loading = bullet.split("At L3 with", 1)[0]
  384:    loading = loading.replace("draft_guard_requested", "").replace(
  387:    for gate in (r"\bL[0-3]\b", r"ordinal", r"--monitor", r"draft"):
  388:        if re.search(gate, loading):
  389:            problems.append(f"the loading sentence carries the gate {gate!r}")
  393:def test_the_wave0_bullet_is_flat_early_and_ungated():
  410:        "at L3 only, ",
  417:        gated = text.replace(
  422:        assert any("gate" in p for p in _wave0_problems(gated)), added
