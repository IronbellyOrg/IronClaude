"""T7 check: Codex completion, gate states and roots on recorded PR 334/336 snapshots."""
import copy, json, re, sys
from superclaude.pr_submit import DetectionContract
from superclaude.pr_submit.reviewers import classify_codex, codex_finding_comments, codex_review_state

A = sys.argv[1]
C = DetectionContract.load()
s336 = json.load(open(f"{A}/t7-pr336-snapshot.json")); s334 = json.load(open(f"{A}/t7-pr334-snapshot.json"))

def marker_sha(snap):
    for c in snap["comments"]:
        m = re.search(r'codex-review-state:v1 (\{.*?\}\}) -->', c["body"])
        if m:
            return json.loads(m[1])["code_review"]["commit_sha"]

def at_review_head(snap, unresolve=False):
    s = copy.deepcopy(snap); s["head_sha"] = marker_sha(s)
    if unresolve:
        for t in s["threads"]:
            if t["comments"]["nodes"][0]["author"]["login"].startswith("chatgpt-codex"):
                t["isResolved"] = False
    return s

results = []
def check(name, got, want):
    results.append(got == want); print(f"{'PASS' if got == want else 'FAIL'} {name}: got={got!r} want={want!r}")

p334 = at_review_head(s334)
check("PR334 shape (completed, no findings, no Codex review) -> clean", classify_codex(p334, C), "clean")
p336 = at_review_head(s336, unresolve=True)
check("PR336 shape (3 unresolved P2 roots) -> findings", classify_codex(p336, C), "findings")
roots = codex_finding_comments(p336, C)
check("PR336 roots count", len(roots), 3)
check("PR336 roots reviewer/hint", {(r["reviewer"], r["severity_hint"], r["codex_priority"]) for r in roots}, {("codex", "medium", "P2")})
p336r = at_review_head(s336)
check("resolved-only threads + Codex review on head -> clean", classify_codex(p336r, C), "clean")
check("live head (marker is for an older commit) -> polling", classify_codex(s336, C), "polling")

def mutate_marker(snap, fn):
    s = copy.deepcopy(snap)
    for c in s["comments"]:
        if "codex-review-state:v1" in c["body"]:
            fn(c)
    return s
def set_status(c, st):
    c["body"] = c["body"].replace('"status":"completed"', f'"status":"{st}"', 1)
check("running status -> polling", classify_codex(mutate_marker(p336, lambda c: set_status(c, "running")), C), "polling")
check("wrong head -> polling", classify_codex(p336, C, current_head_sha="0" * 40), "polling")
dup = copy.deepcopy(p336); dup["comments"].append(copy.deepcopy([c for c in p336["comments"] if "codex-review-state" in c["body"]][0]))
check("two summary markers with the same time -> polling", classify_codex(dup, C), "polling")
newer = copy.deepcopy(dup); newer["comments"][-1]["updated_at"] = "2026-10-31T16:30:00Z"; newer["observed_at"] = "2026-10-31T23:00:00Z"
check("A3: two markers, newest valid wins -> findings", classify_codex(newer, C), "findings")
check("malformed JSON -> polling", classify_codex(mutate_marker(p336, lambda c: c.update(body=c["body"].replace('{"code_review"', '{"code_review" x', 1))), C), "polling")
check("duplicate JSON key -> polling", classify_codex(mutate_marker(p336, lambda c: c.update(body=c["body"].replace('{"code_review":', '{"code_review":{},"code_review":', 1))), C), "polling")
late = copy.deepcopy(p336); late["observed_at"] = "2026-10-31T15:59:00Z"
check("completion after observed_at -> polling", classify_codex(late, C), "polling")
check("completion not newer than watermark -> polling", classify_codex(p336, C, watermark="2026-10-31T23:59:59Z"), "polling")
promised = mutate_marker(p334, lambda c: c.update(body=c["body"].replace('"has_any_findings":false', '"has_any_findings":true', 1)))
check("has_any_findings true, no roots, no Codex review -> polling", classify_codex(promised, C), "polling")
# A1: a root created after the marker edit but no later than the review submission is still selected.
a1 = copy.deepcopy(p336)
for c in a1["comments"]:
    if "codex-review-state:v1" in c["body"]:
        c["updated_at"] = "2026-10-31T15:57:20Z"
st = codex_review_state(a1, C)
check("A1: completion = later of marker and review (review 15:57:28)", st and st["completed_at"].isoformat(), "2026-10-31T15:57:28+00:00")
for r in a1["reviews"]:
    if r["user"]["login"].startswith("chatgpt-codex"):
        r["submitted_at"] = "2026-10-31T15:57:40Z"
check("A1: roots created after the marker edit still selected via the review time", classify_codex(a1, C), "findings")
flags = copy.deepcopy(p336); flags["threads_ok"] = False
check("incomplete snapshot -> polling", classify_codex(flags, C), "polling")
sys.exit(0 if all(results) else 1)
