import copy, json, sys
from superclaude.pr_submit import DetectionContract, actionable_finding_comments, classify
from superclaude.pr_submit.classifier import has_augment_activity, has_reviewer_activity
snap = json.load(open("tests/pr_submit/fixtures/cosmos-pr266.json"))
c = DetectionContract(augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode")
W = "2026-10-16T19:30:00Z"
snap["threads"][0]["isResolved"] = False
base = actionable_finding_comments(snap, c, watermark=W)
cx = copy.deepcopy(snap["threads"][0]); cx["id"] = "PRRT_codex_example"
root = cx["comments"]["nodes"][0]; root["id"] = "PRRC_codex"; root["databaseId"] = 9999999
root["author"] = {"login": "chatgpt-codex-connector"}
snap2 = copy.deepcopy(snap); snap2["threads"].append(cx)
mixed = actionable_finding_comments(snap2, c, watermark=W)
print("augment-only roots:", [r["comment_id"] for r in base], classify(snap, c, watermark=W))
print("with codex root   :", [r["comment_id"] for r in mixed], classify(snap2, c, watermark=W))
print("same selection    :", base == mixed)
codex = {"chatgpt-codex-connector", "chatgpt-codex-connector[bot]"}
print("has_reviewer_activity(codex) on mixed:", has_reviewer_activity(snap2, codex), "on augment-only:", has_reviewer_activity(snap, codex))
print("has_augment_activity unchanged:", has_augment_activity(snap2, c) == has_augment_activity(snap, c))
sys.exit(0 if base == mixed else 1)
