"""Glue between a Packet, the Jev client and the truth table (used by replay.py offline and by the live harness in session 2)."""
import e3lib  # noqa: F401
import policy
import questions


def result_json(r):
    if r is None:
        return None
    return {"status": r.status, "error": r.error, "answers": r.answers, "usage": r.usage, "model": r.model,
            "attempts": r.attempts, "latency_ms": r.latency_ms, "request_sha256": r.request_sha256}


def screen_packet(client, packet, case_id, data_classes, thr, purpose="E3 confirmation screen"):
    """-> (decision, result|None).  EXCEPTION and QUOTE_FAIL never reach Jev.  KeyMissing/KeyRejected propagate (configuration errors)."""
    if packet.code_outcome != "OK":
        return policy.decide(packet.code_outcome, None, thr), None
    r = client.ask(packet.state, questions.build_questions(packet.state), case_id=case_id,
                   qset_version=questions.QSET_VERSION, data_classes=set(data_classes), purpose=purpose)
    return policy.decide("OK", r, thr, evidence_count=packet.state["facts"]["evidence_count"]), r
