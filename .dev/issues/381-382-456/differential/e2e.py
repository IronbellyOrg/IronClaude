"""End to end: real poll-script output -> the SKILL's entry points, OLD (master) vs NEW.

uv run --no-sync python -I /tmp/fix381/e2e.py <evidence_dir>
Mirrors SKILL.md Wave 1 (classify, actionable_finding_comments, classify_codex, reviewer_activity,
poll_outcome, augment_wait_outcome, codex_wait_outcome, merge_wait) for one poll. A simulated loop polls every
30 s and stops at the first non-polling round outcome or at --timeout 600.
"""

import glob
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, "/tmp/fix381/old")
import oldpr as old  # noqa: E402
import oldpr.fsm as old_fsm  # noqa: E402
import oldpr.models as old_models  # noqa: E402

import superclaude.pr_submit as new  # noqa: E402
import superclaude.pr_submit.fsm as new_fsm  # noqa: E402

EV = Path(sys.argv[1])
TIMEOUT, POLL, SILENCE = 600, 30, 120
IDS = {"augmentcode[bot]", "augmentcode"}
out_lines = []


def say(*a):
    line = " ".join(str(x) for x in a)
    out_lines.append(line)
    print(line)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso(d):
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def contract(pkg):
    return pkg.DetectionContract(
        augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode",
        codex_bot_login="chatgpt-codex-connector[bot]", codex_app_slug="chatgpt-codex-connector",
    )


def one_poll(pkg, fsm, payload, elapsed, *, watermark=None, is_new, codex_override=None):
    c = contract(pkg)
    head = payload.get("head_sha")
    state = pkg.classify(payload, c, watermark=watermark, current_head_sha=head)
    found = pkg.actionable_finding_comments(payload, c, watermark=watermark, current_head_sha=head) if state == "findings" else []
    codex_state = pkg.classify_codex(payload, c, watermark=watermark, current_head_sha=head)
    activity = pkg.reviewer_activity(payload, c)
    silent = pkg.poll_succeeded(payload) and not pkg.has_augment_activity(payload, c)
    nxt = fsm.poll_outcome(state, elapsed, TIMEOUT, silent=silent, silence_timeout=SILENCE, monitor_ordinal=3)
    kwargs = {}
    defect = None
    if is_new:
        defect = pkg.augment_marker_defect(payload, c, watermark=watermark, current_head_sha=head)
        kwargs["marker_defect"] = defect
    aug = pkg.augment_wait_outcome(state, nxt, **kwargs)
    if codex_override:
        cx_state, cx = codex_override
    else:
        cx_state = codex_state
        cx = pkg.codex_wait_outcome(cx_state, active=activity["codex"], elapsed=elapsed, timeout=TIMEOUT,
                                    silence_timeout=SILENCE, other_settled=aug != "pending")
    decision = pkg.merge_wait((aug, state), (cx, cx_state))
    return {
        "augment_state": state, "findings": len(found), "codex_state": cx_state, "aug_wait": aug, "codex_wait": cx,
        "round": decision["outcome"], "used": decision["used"], "incomplete": decision["incomplete"],
        "reason": (defect or {}).get("reason"), "settled": (defect or {}).get("settled"),
        "open_threads": (defect or {}).get("open_threads"),
    }


def slice_payload(p, head, at):
    out = {k: v for k, v in p.items() if k not in ("reviews", "comments", "threads")}
    out["head_sha"], out["observed_at"] = head, iso(at)
    out["reviews"] = [r for r in p["reviews"] if ts(r["submitted_at"]) <= at]
    out["comments"] = [c for c in p["comments"] if ts(c.get("created_at") or c["createdAt"]) <= at]
    out["threads"] = []
    for t in p["threads"]:
        if ts(t["comments"]["nodes"][0]["createdAt"]) <= at:
            t = json.loads(json.dumps(t))
            t["isResolved"] = False  # the threads were open then; they are resolved on GitHub now
            out["threads"].append(t)
    return out


def loop(p, head, start, *, watermark=None, codex_override=None, label=""):
    """Poll every 30 s from ``start``; return per-version (outcome, elapsed, last decision)."""
    results = {}
    for name, pkg, fsm, is_new in (("OLD", old, old_fsm, False), ("NEW", new, new_fsm, True)):
        elapsed, first_report = 0, None
        while True:
            payload = slice_payload(p, head, start + timedelta(seconds=elapsed))
            d = one_poll(pkg, fsm, payload, elapsed, watermark=watermark, is_new=is_new, codex_override=codex_override)
            if is_new and d["reason"] and first_report is None:
                first_report = (elapsed, d["reason"], d["open_threads"])
            if d["round"] != "polling" or elapsed >= TIMEOUT:
                break
            elapsed += POLL
        results[name] = (d["round"], elapsed, d, first_report)
    say(f"  {label}")
    for name, (rnd, el, d, fr) in results.items():
        say(f"    {name}: round outcome={rnd!r} after {el} s | augment={d['augment_state']} aug_wait={d['aug_wait']} codex={d['codex_state']}/{d['codex_wait']} used={d['used']} incomplete={d['incomplete']}"
            + (f" | reason line at {fr[0]} s: 'Augment review present but its status marker is malformed ({fr[1]})', open threads {fr[2]}" if fr else ""))
    return results


say("=== A. live snapshots from the REAL poll script (read-only), classified now ===")
for n in (377, 455):
    p = json.loads((EV / f"poll-pr{n}.json").read_text())
    say(f"PR {n}: head {p['head_sha'][:8]} observed {p['observed_at']} flags ok={all(p[k] for k in ('reviews_ok','comments_ok','threads_ok'))}")
    for name, pkg, fsm, is_new in (("OLD", old, old_fsm, False), ("NEW", new, new_fsm, True)):
        d = one_poll(pkg, fsm, p, 30, is_new=is_new)
        say(f"    {name}: {d}")

p377 = json.loads((EV / "poll-pr377.json").read_text())
p455 = json.loads((EV / "poll-pr455.json").read_text())
CODEX_CLEAN = ("clean", "done")  # PR 455's reported Codex result; its live marker was overwritten later
CODEX_ABSENT = ("polling", "absent")
CODEX_PENDING = ("polling", "pending")

say("")
say("=== B. #381: PR 377 first review 5776286053 (21:44:59Z) + comment 21:45:00Z, head a2136867 ===")
loop(p377, "a2136867100d17295aacae92abfb8c54eac0eb14", ts("2026-11-04T21:45:09Z"), codex_override=CODEX_ABSENT,
     label="poll every 30 s from 10 s after the review, Codex absent")

say("")
say("=== C. #382: PR 377 second review 5776522857 (22:04:49Z, marker missing '}'), head 60e0030, watermark = re-trigger 22:01:24Z ===")
loop(p377, "60e0030cb50eb7a823826a48371fd94cdffa613d", ts("2026-11-04T22:04:59Z"), watermark="2026-11-04T22:01:24Z",
     codex_override=CODEX_ABSENT, label="Codex absent (Augment-only PR)")
loop(p377, "60e0030cb50eb7a823826a48371fd94cdffa613d", ts("2026-11-04T22:04:59Z"), watermark="2026-11-04T22:01:24Z",
     codex_override=CODEX_CLEAN, label="Codex already clean on this head (stand-in)")
loop(p377, "60e0030cb50eb7a823826a48371fd94cdffa613d", ts("2026-11-04T22:04:59Z"), watermark="2026-11-04T22:01:24Z",
     label="REAL Codex data of PR 377 (Codex active, its marker stays on the old head, so it never completes on this one)")

say("")
say("=== D. #456: PR 455 first review 5819041100 (18:15:01Z, 1 suggestion, marker missing '}'), head 6f6c46a ===")
loop(p455, "6f6c46aace41587f47520b49d4570f3c0ddf62b7", ts("2026-11-08T18:15:11Z"), codex_override=CODEX_CLEAN,
     label="Codex clean (as the issue reports)")
loop(p455, "6f6c46aace41587f47520b49d4570f3c0ddf62b7", ts("2026-11-08T18:15:11Z"), codex_override=CODEX_ABSENT,
     label="Codex absent")

say("")
say("=== E. a later readable review is still accepted: PR 455 head 029a451, malformed 18:29:51Z then well formed 18:30:18Z ===")
loop(p455, "029a45179d78667bb50ec53185d47cde85451bf8", ts("2026-11-08T18:29:56Z"), codex_override=CODEX_CLEAN,
     label="poll from 5 s after the malformed review")

say("")
say("=== F. healthy and legacy paths unchanged: every repo fixture, OLD vs NEW, at elapsed 0/30/300/600 and ordinals 0-3 ===")
same = diff = 0
for path in sorted(glob.glob("/home/coder/workspaces/worktrees/IronClaude/pr-monitor-381-382-456/tests/pr_submit/fixtures/*.json")):
    try:
        fx = json.loads(Path(path).read_text())
    except ValueError:
        continue
    if not isinstance(fx, dict) or "reviews" not in fx:
        continue
    name = Path(path).name
    if name.startswith(("cosmos-pr377-malformed", "cosmos-pr455-malformed")):
        continue  # the new cases; compared in C-E
    for elapsed in (0, 30, 300, 600):
        for wm in (None, "2026-10-16T19:30:00Z"):
            a = one_poll(old, old_fsm, fx, elapsed, watermark=wm, is_new=False)
            b = one_poll(new, new_fsm, fx, elapsed, watermark=wm, is_new=True)
            b.pop("reason"), b.pop("settled"), b.pop("open_threads")
            a.pop("reason"), a.pop("settled"), a.pop("open_threads")
            if a == b:
                same += 1
            else:
                diff += 1
                say("  DIFF", name, elapsed, wm, a, b)
say(f"  fixture polls compared: {same + diff}; identical: {same}; different: {diff}")
fsm_same = all(
    old_fsm.poll_outcome(s, e, TIMEOUT, silent=sil, silence_timeout=SILENCE, monitor_ordinal=o).name
    == new_fsm.poll_outcome(s, e, TIMEOUT, silent=sil, silence_timeout=SILENCE, monitor_ordinal=o).name
    for s in ("polling", "clean", "findings", "declined") for e in range(0, 700, 30) for sil in (False, True) for o in range(4)
)
say(f"  poll_outcome (finite timeout, silence, autonomy ordinals 0-3) identical old vs new over 4x24x2x4 inputs: {fsm_same}")
(EV / "e2e-results.txt").write_text("\n".join(out_lines) + "\n")
