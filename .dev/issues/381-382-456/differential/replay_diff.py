"""Differential replay: OLD (master) vs NEW classifier/wait logic over every real Augment review.

Run with the worktree venv:  uv run python -I /tmp/fix381/replay_diff.py <out_dir>
Input: /tmp/fix381/diff/payloads/pr-<N>.json = real snapshots from the unmodified poll script.
For each Augment review R we rebuild what the monitor could see at two moments after R
(R+20s inside the grace window, R+120s after it), with threads in their real current state and
forced open (as they were then), and three watermark settings. Each case is classified by
the old and the new code; the full table is written to <out_dir>/differential.csv.
"""

import csv
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, "/tmp/fix381/old")
import oldpr.classifier as old_c  # noqa: E402
import oldpr.detection as old_d  # noqa: E402
import oldpr.fsm as old_f  # noqa: E402
import oldpr.reviewers as old_r  # noqa: E402

import superclaude.pr_submit.classifier as new_c  # noqa: E402
import superclaude.pr_submit.detection as new_d  # noqa: E402
import superclaude.pr_submit.fsm as new_f  # noqa: E402
import superclaude.pr_submit.reviewers as new_r  # noqa: E402

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
PAYLOADS = Path("/tmp/fix381/diff/payloads")
IDS = {"augmentcode[bot]", "augmentcode"}


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso(d):
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slice_payload(p, review, at, force_open):
    """What the poll script would have returned at time ``at`` for ``review``'s head."""
    out = {k: v for k, v in p.items() if k not in ("reviews", "comments", "threads")}
    out["head_sha"] = review["commit_id"]
    out["observed_at"] = iso(at)
    out["reviews"] = [r for r in p["reviews"] if ts(r["submitted_at"]) <= at]
    out["comments"] = [
        c for c in p["comments"] if ts(c.get("created_at") or c["createdAt"]) <= at
    ]
    threads = []
    for t in p["threads"]:
        root = t["comments"]["nodes"][0]
        if ts(root["createdAt"]) <= at:
            t = json.loads(json.dumps(t))
            if force_open:
                t["isResolved"] = False
            threads.append(t)
    out["threads"] = threads
    return out


def decision(c, f, r, d, payload, contract, watermark, elapsed, new):
    state = c.classify(payload, contract, watermark=watermark, current_head_sha=payload["head_sha"])
    found = c.actionable_finding_comments(
        payload, contract, watermark=watermark, current_head_sha=payload["head_sha"]
    )
    nxt = f.poll_outcome(state, elapsed, 600, silent=False)
    defect = None
    if new:
        defect = c.augment_marker_defect(
            payload, contract, watermark=watermark, current_head_sha=payload["head_sha"]
        )
        aug = r.augment_wait_outcome(state, nxt, marker_defect=defect)
    else:
        aug = r.augment_wait_outcome(state, nxt)
    # Codex absent (Augment-only repo) and Codex already clean: the two shapes that decide the round.
    m_absent = r.merge_wait((aug, state), ("absent", "polling"))["outcome"]
    m_done = r.merge_wait((aug, state), ("done", "clean"))["outcome"]
    return {
        "state": state,
        "findings": ",".join(sorted(str(x["comment_id"]) for x in found)),
        "aug_wait": aug,
        "round_codex_absent": m_absent,
        "round_codex_clean": m_done,
        "defect": (defect or {}).get("reason", ""),
        "defect_settled": (defect or {}).get("settled", ""),
        "defect_open_threads": (defect or {}).get("open_threads", ""),
    }


old_contract = old_d.DetectionContract(augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode")
new_contract = new_d.DetectionContract(augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode")

rows = []
for path in sorted(PAYLOADS.glob("pr-*.json")):
    try:
        p = json.loads(path.read_text())
    except ValueError:
        continue
    if not p.get("head_sha") or not all(p.get(k) is True for k in ("reviews_ok", "comments_ok", "threads_ok")):
        rows.append({"pr": path.stem, "note": "snapshot incomplete (skipped)"})
        continue
    for review in p["reviews"]:
        if (review.get("user") or {}).get("login") not in IDS or not review.get("submitted_at"):
            continue
        body = review.get("body") or ""
        marker_text = body.split("cosmos-review-status:v1 ", 1)[-1].split(" -->")[0] if "cosmos-review-status:v1 " in body else None
        try:
            json.loads(marker_text) if marker_text is not None else None
            marker_ok = marker_text is not None
        except ValueError:
            marker_ok = False
        late = [
            c for c in p["comments"]
            if c.get("pull_request_review_id") == review["id"]
            and ts(c["created_at"]) > ts(review["submitted_at"])
        ]
        sub = ts(review["submitted_at"])
        for at_name, at in (("+20s", sub + timedelta(seconds=20)), ("+120s", sub + timedelta(seconds=120))):
            for force_open in (False, True):
                payload = slice_payload(p, review, at, force_open)
                for wm_name, wm in (("none", None), ("older", iso(sub - timedelta(hours=1))), ("newer", iso(sub + timedelta(hours=1)))):
                    elapsed = int((at - sub).total_seconds())
                    o = decision(old_c, old_f, old_r, old_d, payload, old_contract, wm, elapsed, False)
                    n = decision(new_c, new_f, new_r, new_d, payload, new_contract, wm, elapsed, True)
                    rows.append(
                        {
                            "pr": p["pr"], "review": review["id"], "submitted_at": review["submitted_at"],
                            "marker": "ok" if marker_ok else "BAD", "late_comments": len(late),
                            "at": at_name, "threads": "open" if force_open else "current", "watermark": wm_name,
                            **{f"old_{k}": v for k, v in o.items()},
                            **{f"new_{k}": v for k, v in n.items()},
                            "changed": any(o[k] != n[k] for k in ("state", "findings", "aug_wait", "round_codex_absent", "round_codex_clean")),
                        }
                    )

cases = [r for r in rows if "review" in r]
fields = list(cases[0].keys())
with open(OUT / "differential.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(cases)

reviews = {(r["pr"], r["review"]) for r in cases}
bad = {(r["pr"], r["review"]) for r in cases if r["marker"] == "BAD"}
late = {(r["pr"], r["review"]) for r in cases if r["late_comments"]}
changed = [r for r in cases if r["changed"]]
changed_reviews = {(r["pr"], r["review"]) for r in changed}
healthy = reviews - bad - late
summary = {
    "snapshots_skipped": [r for r in rows if "note" in r],
    "reviews_replayed": len(reviews),
    "cases": len(cases),
    "reviews_with_malformed_marker": len(bad),
    "reviews_with_late_inline_comment": len(late),
    "healthy_reviews": len(healthy),
    "cases_changed": len(changed),
    "reviews_with_any_changed_case": len(changed_reviews),
    "changed_reviews_that_are_healthy": sorted(changed_reviews & healthy),
    "changed_reviews_not_malformed": sorted(changed_reviews - bad),
    "classify_or_findings_changed": sum(
        1 for r in cases if r["old_state"] != r["new_state"] or r["old_findings"] != r["new_findings"]
    ),
    "changed_by_transition": Counter(
        f"aug_wait {r['old_aug_wait']}->{r['new_aug_wait']} | codex-absent round {r['old_round_codex_absent']}->{r['new_round_codex_absent']} | codex-clean round {r['old_round_codex_clean']}->{r['new_round_codex_clean']} | marker={r['marker']}"
        for r in changed
    ),
    "old_state_counts": Counter(r["old_state"] for r in cases),
}
(OUT / "differential-summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
print(json.dumps(summary, indent=2, default=str))
