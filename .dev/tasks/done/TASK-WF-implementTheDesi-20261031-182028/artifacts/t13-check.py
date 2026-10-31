import dataclasses, json
from superclaude.pr_submit import DetectionContract, classify_codex, reviewer_identities, reviewer_activity
base = DetectionContract.load()
data = {f.name: getattr(base, f.name) for f in dataclasses.fields(base)}
p = json.load(open("tests/pr_submit/fixtures/codex-findings-pr336.json"))
for blank in (("codex_bot_login",), ("codex_bot_login", "codex_app_slug")):
    c = DetectionContract.from_yaml({**data, **{k: "" for k in blank}})
    print(blank, sorted(reviewer_identities(c, "codex")), reviewer_activity(p, c)["codex"], classify_codex(p, c))
