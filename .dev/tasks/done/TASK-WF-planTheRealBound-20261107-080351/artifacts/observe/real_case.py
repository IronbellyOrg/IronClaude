"""One real Claude --print case through the runner (shared by Tasks 2 to 4).

Imported by the task drivers: it builds the literal command script, the settings
file with the Bash observer hook, runs Claude through Runner.run (so the run is in
run-status.jsonl) and returns only redacted facts: identities, field names, hashes,
selector results, exit codes and counts. The model's own report is never read.
"""

import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import observe as ob  # noqa: E402


def real_case(runner, group, case_id, variant, sid, label, *, tools=("Bash",), timeout=120, prompt=None, body=None,
              persist=False, resume=None, fork=False, record_sid=None, **run_kw):
    rid = ob.new_rid()
    script = ob.write_cmd(group, rid, body)
    log = group.tmp / ("hook-events-%s.jsonl" % rid)
    settings = ob.write_settings(group, variant, log)
    text = prompt(script) if callable(prompt) else (prompt or ob.prompt_for(script))
    argv = ob.claude_argv(ob.claude_bin(), settings, sid, text, tools=tools, persist=persist, resume=resume, fork=fork)
    box = {"measured": False}

    def classify(rc, mp):
        result, more = ob.classify_claude(rc, mp)
        found = ob.depth_capture(group, rid)
        if found:
            box.update(found, measured=True)
        return result, more

    res = runner.run(group, case_id, argv, label=label, timeout=timeout, real_claude=True, ok_result="observed",
                     classify=classify, rid=rid, sid=record_sid or sid, depth=box, **run_kw)
    events, init = ob.parse_stream(res["out"])
    hooks = []
    if log.exists():
        for line in log.read_text().splitlines():
            try:
                hooks.append(json.loads(line))
            except ValueError:
                pass
    selector = ob.selector_capture(group, rid)
    extra = res["extra"]
    return {
        "run_id": rid,
        "case_id": case_id,
        "variant": variant,
        "requested_session_id": sid,
        "ledger_exit": res["exit"],
        "result": res["result"],
        "held_s": res["held_s"],
        "timed_out": res["timed_out"],
        "failure": {k: extra[k] for k in ("reason", "assistant_error_category", "result_subtype", "result_is_error",
                                           "api_error_status", "stderr_bytes", "refusal_observed") if k in extra},
        "store_check": extra.get("store_check"),
        "stream_event_types": [e["type"] for e in events if e.get("type")],
        "stream_reported_session_ids": sorted({e["session_id"] for e in events if e.get("session_id")}),
        "hook_events": hooks,
        "selector_captured_by_runner": selector,
        "depth": box,
        "ran_a_tool": bool(selector or any(h.get("hook_event_name") == "PostToolUse" for h in hooks)),
        "out": res["out"],
        "err": res["err"],
    }


def public(case):
    """The case without the temporary-file paths, for writing into an artifact."""
    return {k: v for k, v in case.items() if k not in ("out", "err")}
