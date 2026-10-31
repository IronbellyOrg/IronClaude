"""T9 check: dedup_groups, pending_retriggers and package exports."""
import sys

from superclaude.pr_submit import classify_codex, dedup_groups, merge_wait  # noqa: F401
from superclaude.pr_submit.models import Finding
from superclaude.pr_submit.reviewers import pending_retriggers

ok = []


def check(name, got, want):
    ok.append(got == want)
    print(f"{'PASS' if got == want else 'FAIL'} {name}: got={got!r} want={want!r}")


aug = Finding(path="a.md", line=41, body="staged changes", reviewer="augment")
cdx = Finding(path="a.md", line=41, body="staged changes too", reviewer="codex")
other = Finding(path="a.md", line=48, body="fallback", reviewer="codex")
outdated = Finding(path="a.md", line=None, original_line=63, body="edge", reviewer="codex")
same63 = Finding(path="a.md", line=63, body="edge", reviewer="augment")
groups = dedup_groups([aug, other, cdx, outdated, same63])
check("Augment+Codex same path/line -> one group of two", [len(g) for g in groups], [2, 1, 2])
check("group members keep their reviewers", [f.reviewer for f in groups[0]], ["augment", "codex"])
check("different lines -> separate groups", groups[1] == [other], True)
check("null line groups by original_line", groups[2] == [outdated, same63], True)
check("every finding kept", sum(len(g) for g in groups), 5)
check("empty input -> no groups", dedup_groups([]), [])
events = [{"event_type": "rereview_requested", "cycle_id": "c1", "reviewer": "augment"}]
check("augment posted, codex missing", pending_retriggers(events, "c1", ["augment", "codex"]), ["codex"])
check("reviewer-less event counts as augment", pending_retriggers([{"event_type": "rereview_requested", "cycle_id": "c1"}], "c1", ["augment", "codex"]), ["codex"])
check("other cycle does not count", pending_retriggers(events, "c2", ["augment", "codex"]), ["augment", "codex"])
check("no present reviewers -> nothing to post", pending_retriggers(events, "c1", []), [])
print("imports ok:", merge_wait.__name__, classify_codex.__name__, dedup_groups.__name__)
sys.exit(0 if all(ok) else 1)
