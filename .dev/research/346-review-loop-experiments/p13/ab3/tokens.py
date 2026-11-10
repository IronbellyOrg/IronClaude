"""C9.1 token counting: output tokens per (run, step), each message id counted ONCE (max over its lines)."""
import glob
import json
import re

TASKS_GLOB = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"


def transcript_stats(path):
    """(first-6-lines text, {message_id: max output_tokens}, set of assistant models)."""
    head, msgs, models = [], {}, set()
    try:
        fh = open(path, errors="ignore")
    except OSError:
        return "", {}, set()
    with fh:
        for i, line in enumerate(fh):
            if i < 6:
                head.append(line)
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message")
            if not isinstance(m, dict) or m.get("role") != "assistant":
                continue
            if m.get("model"):
                models.add(m["model"])
            u = m.get("usage") or {}
            mid = m.get("id") or d.get("uuid")
            if mid is not None:
                msgs[mid] = max(msgs.get(mid, 0), u.get("output_tokens") or 0)
    return "".join(head), msgs, models


def step_tokens(prompt_re, expected_model=None, glob_pat=TASKS_GLOB, warn=print):
    """Return {(run, step): output_tokens} for every transcript whose first 6 lines match prompt_re
    (two named groups: run, step). Several matches for one step: keep the expected model with most tokens, WARN."""
    found = {}
    for f in glob.glob(glob_pat):
        head, msgs, models = transcript_stats(f)
        m = re.search(prompt_re, head)
        if not m:
            continue
        found.setdefault((m.group("run"), m.group("step")), []).append((sum(msgs.values()), models, f))
    out = {}
    for key, cands in found.items():
        if len(cands) > 1:
            warn(f"WARN {key}: {len(cands)} transcripts match; keeping the expected model with most tokens")
            if expected_model:
                ok = [c for c in cands if any(expected_model in x for x in c[1])]
                cands = ok or cands
        out[key] = max(cands, key=lambda c: c[0])[0]
    return out
