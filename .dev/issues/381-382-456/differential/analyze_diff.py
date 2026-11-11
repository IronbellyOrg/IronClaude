import csv
import sys
from collections import Counter, defaultdict

rows = list(csv.DictReader(open(sys.argv[1] + "/differential.csv")))
by = defaultdict(list)
for r in rows:
    by[(r["pr"], r["review"])].append(r)

print("== malformed-marker reviews (13): what old and new did")
print("pr review submitted marker | cases with new defect | changed cases | old states seen | new reasons")
for key, rs in sorted(by.items(), key=lambda kv: kv[1][0]["submitted_at"]):
    if rs[0]["marker"] != "BAD":
        continue
    changed = sum(r["changed"] == "True" for r in rs)
    defects = sum(r["new_defect"] != "" for r in rs)
    olds = dict(Counter(r["old_state"] for r in rs))
    reasons = sorted({r["new_defect"] for r in rs if r["new_defect"]})
    print(key[0], key[1], rs[0]["submitted_at"], "| defect-cases", defects, "| changed", changed, "| old", olds, "|", reasons)

print()
print("== late-inline-comment reviews (11): old vs new state, thread=open, no watermark, +20s and +120s")
for key, rs in sorted(by.items(), key=lambda kv: kv[1][0]["submitted_at"]):
    if rs[0]["late_comments"] == "0":
        continue
    cells = [r for r in rs if r["threads"] == "open" and r["watermark"] == "none"]
    print(key[0], key[1], "late", rs[0]["late_comments"], "marker", rs[0]["marker"],
          "|", ", ".join(f"{r['at']}: old={r['old_state']} new={r['new_state']}" for r in cells),
          "| any change:", any(r["changed"] == "True" for r in rs))

print()
print("== healthy reviews: any non-empty new_defect or any changed field?")
healthy = [r for r in rows if r["marker"] == "ok" and r["late_comments"] == "0"]
print("healthy cases:", len(healthy), "| with a defect:", sum(r["new_defect"] != "" for r in healthy),
      "| changed:", sum(r["changed"] == "True" for r in healthy))
print("old state counts over healthy cases:", dict(Counter(r["old_state"] for r in healthy)))
print("healthy: state/findings/aug_wait/round identical old vs new:",
      all(r[f"old_{k}"] == r[f"new_{k}"] for r in healthy for k in ("state", "findings", "aug_wait", "round_codex_absent", "round_codex_clean")))
print()
print("== whole table: old==new on state and findings in every case:",
      all(r["old_state"] == r["new_state"] and r["old_findings"] == r["new_findings"] for r in rows))
print("changed cases by (at, threads, watermark):", dict(Counter((r["at"], r["threads"], r["watermark"]) for r in rows if r["changed"] == "True")))
