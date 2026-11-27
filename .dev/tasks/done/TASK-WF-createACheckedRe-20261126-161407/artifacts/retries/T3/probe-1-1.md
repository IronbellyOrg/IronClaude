6a3111a5b8739a608013e6dd8ac08e54c5f808f4
family=terminal-order-proof
Defect: old contract presence masks current-attempt contract-versus-terminal ordering in genuine-old-marker matrix.
Search: grep -n -E 'test_resume_completion_policy_status_and_order|def state|def marker|emit_contract|events' -- tests/swarm/test_resume_crash_recovery.py
Coupled sites: publication test state/marker observers, actual emit_contract observer and expected event sequence.
Before:
604:def test_resume_completion_policy_status_and_order(
646:    events = []
649:    def state(root, value, job_id):
653:            events.append("terminal")
656:            events.append("accepted")
659:    def marker(status, contract_path):
664:        events.append("marker")
672:    assert events == (
725:        monkeypatch.setattr(reducer, "emit_contract", fail)
1201:            patch.setattr(reducer, "emit_contract", fail)

After:
604:def test_resume_completion_policy_status_and_order(
646:    events = []
648:    real_contract = reducer.emit_contract
652:        assert events == ["accepted"]
653:        events.append("contract")
656:    def state(root, value, job_id):
659:            assert events == ["accepted", "contract"]
661:            events.append("terminal")
664:            events.append("accepted")
667:    def marker(status, contract_path):
672:        events.append("marker")
676:    monkeypatch.setattr(reducer, "emit_contract", contract)
681:    assert events == (
736:        monkeypatch.setattr(reducer, "emit_contract", fail)
1212:            patch.setattr(reducer, "emit_contract", fail)
