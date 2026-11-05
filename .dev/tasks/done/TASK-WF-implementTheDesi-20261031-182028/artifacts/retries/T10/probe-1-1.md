038aeed101ea35b2e5bdf1218cf7992eded2e970
## family coverage-gap
defect form: a design section 16 presence case (Augment only / Codex only / both / neither) not asserted through reviewer_activity
command: grep -n "reviewer_activity(" tests/pr_submit/test_codex_reviews.py
before:
234:    assert reviewer_activity(findings336, CONTRACT) == {"augment": True, "codex": True}
245:    assert reviewer_activity(augment_only, CONTRACT) == {
259:    assert reviewer_activity(payload, CONTRACT)["augment"] is False
coupled sites: merge_wait rows for the same four cases (:268-318) already present
after:
255:    assert reviewer_activity(findings336, CONTRACT) == {"augment": True, "codex": True}
256:    assert reviewer_activity(_only(findings336, keep_codex=False), CONTRACT) == {
260:    assert reviewer_activity(_only(findings336, keep_codex=True), CONTRACT) == {
265:    assert reviewer_activity(empty, CONTRACT) == {"augment": False, "codex": False}
276:    assert reviewer_activity(payload, CONTRACT)["augment"] is False
