9eb70f97089038b7ecaeea0b0458e48df64f9ebf
family acceptance-scope: defect form = a scoped/clean acceptance derived from labels instead of blocking grade
command: grep -n -e held -e acceptance -e LABELS_COUNTED src/superclaude/skills/sc-diffgate/scripts/diffgate.py
before: 346:LABELS_COUNTED = ("critical", "major")
before: 457:    held=None,
before: 469:        "held": dict(held or {}),
before: 672:    """Blocking, origin, prior statuses, deferral, verdict, acceptance, fix
before: 676:    findings, deferred, held = [], [], dict(ctx["held"])
before: 725:        rec["demoted"] = sev in LABELS_COUNTED and not rec["blocking"] and not reason
before: 726:        if sev in LABELS_COUNTED and (reason or rec["demoted"]):
before: 727:            held.setdefault(
before: 743:        if status == "withdrawn" and p.get("sev") in LABELS_COUNTED:
before: 744:            held.setdefault(p["id"], {"review": n, "why": "withdrawn", "sev": p["sev"]})
before: 764:    counted = {r["id"] for r in findings if r["sev"] in LABELS_COUNTED}
before: 769:        and p.get("sev") in LABELS_COUNTED
before: 771:    counted |= set(held)
before: 777:        "acceptance": "scoped" if held else "clean",
before: 785:        "held": held,
before: 844:                    f"lock held by running pid {pid}: {lock}; wait for that step to finish",
family via-anchor-unchanged: defect form = a via finding whose anchor is not checked against changed tokens
command: grep -n -e via_quote -e '"via"' src/superclaude/skills/sc-diffgate/scripts/diffgate.py
before: 334:    "via",
before: 335:    "via_quote",
before: 515:    for key in ("hunk", "via", "via_quote", "cites", "side", "outcome", "anchor"):
before: 520:        bad = [k for k in ("hunk", "via", "via_quote", "cites", "side") if k in kv]
before: 530:        if f["hunk"] and (f["via"] or f["cites"]):
before: 532:        if bool(f["via"]) != bool(f["via_quote"]):
before: 533:            errs.append(("C2", "via= and via_quote= go together"))
before: 569:    if f["via"]:
before: 570:        h = ctx["hunks"].get(f["via"])
before: 575:        vq = _collapse(f["via_quote"] or "")
before: 579:                ("C7", f"via_quote does not overlap a changed token of {f['via']}")
before: 686:            "via": f.get("via"),
before: 700:        elif n >= 2 and f.get("via"):
before: 714:        owners = ctx["owners"].get(rec["hunk"] or rec["via"] or "", [])
family origin-vocab: defect form = an origin value outside full/changed/unchanged
command: grep -n -e origin tests/skills/test_diffgate_script.py src/superclaude/skills/sc-diffgate/scripts/diffgate.py
before: tests/skills/test_diffgate_script.py:304:    assert {f["id"]: f["origin"] for f in res["findings"]} == {
before: tests/skills/test_diffgate_script.py:360:    assert res["findings"][0]["origin"] == "cites"
before: tests/skills/test_diffgate_script.py:373:    assert all(f["origin"] == "unchanged" for f in res["findings"])
before: tests/skills/test_diffgate_script.py:433:    assert res["findings"][0]["origin"] == "full"
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:672:    """Blocking, origin, prior statuses, deferral, verdict, acceptance, fix
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:707:            rec["origin"] = "full"
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:709:            rec["origin"] = "changed"
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:711:            rec["origin"] = "cites"
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:713:            rec["origin"] = "unchanged"
family c3-missing: defect form = the spec-hash rule C3 absent from the checker
command: grep -n -e C3 -e sha src/superclaude/skills/sc-diffgate/scripts/diffgate.py
before: 112:def sha256(text: str) -> str:
before: 113:    return hashlib.sha256(text.encode("utf-8")).hexdigest()
before: 134:def _shape(lines) -> tuple[int, int, int]:
before: 159:    within MERGE_GAP lines of each other share one hunk id H<review>.<n>; the
before: 182:            if _shape(old_lines[i1:i2]) == _shape(new_lines[j1:j2]):
coupled sites: derive (held, acceptance, origin), _check_finding (via branch), make_ctx and check_report (C3), tests test_cites_adds_no_blocker and the via-cap test
after (acceptance-scope): 346:LABELS_COUNTED = ("critical", "major") 457:    held=None, 458:    scoped=None, 473:        "held": dict(held or {}), 474:        "scoped": dict(scoped or {}), 693:    """Blocking, origin, prior statuses, deferral, verdict, acceptance, fix 697:    findings, deferred, held = [], [], dict(ctx["held"]) 698:    scoped = dict(ctx["scoped"])  # blocking-grade findings the script took out 745:        rec["demoted"] = sev in LABELS_COUNTED and not rec["blocking"] and not reason 747:        if sev in LABELS_COUNTED and (reason or rec["demoted"]): 748:            held.setdefault(rec["id"], {"review": n, "why": why, "sev": sev}) 750:            scoped.setdefault(rec["id"], {"review": n, "why": why, "sev": sev}) 766:            scoped.setdefault(p["id"], mark) 767:            if p.get("sev") in LABELS_COUNTED: 768:                held.setdefault(p["id"], mark) 788:    counted = {r["id"] for r in 
after (via-anchor-unchanged): 335:    "via_quote", 521:    for key in ("hunk", "via", "via_quote", "cites", "side", "outcome", "anchor"): 526:        bad = [k for k in ("hunk", "via", "via_quote", "cites", "side") if k in kv] 538:        if bool(f["via"]) != bool(f["via_quote"]): 539:            errs.append(("C2", "via= and via_quote= go together")) 566:    f["on_changed"] = f["side"] != "old" and any(o & changed for o in occ) 583:        vq = _collapse(f["via_quote"] or "") 587:                ("C7", f"via_quote does not overlap a changed token of {f['via']}") 589:        if f["on_changed"]: 730:        elif (f.get("hunk") and not reason) or f.get("on_changed"): 
after (origin-vocab): tests/skills/test_diffgate_script.py:304:    assert {f["id"]: f["origin"] for f in res["findings"]} == { tests/skills/test_diffgate_script.py:360:    assert res["findings"][0]["origin"] == "unchanged" tests/skills/test_diffgate_script.py:366:    assert errors == [] and res["findings"][0]["origin"] == "changed" tests/skills/test_diffgate_script.py:367:    assert {f["origin"] for f in res["findings"]} <= {"changed", "unchanged"} tests/skills/test_diffgate_script.py:412:    assert all(f["origin"] == "unchanged" for f in res["findings"]) tests/skills/test_diffgate_script.py:472:    assert res["findings"][0]["origin"] == "full" src/superclaude/skills/sc-diffgate/scripts/diffgate.py:729:            rec["origin"] = "full" src/superclaude/skills/sc-diffgate/scripts/diffgate.py:731:            rec["origin"] = "changed" src/superclaude/skills/sc-diffgate/scripts/diffgate.py:733:            rec["origin"] = "unchanged" 
after (c3-missing): 459:    spec_sha=None, 462:    `spec_sha` is the current specification's hash (C3); None skips C3, as a 475:        "spec_sha": spec_sha, 598:    """Hard rules C1 to C10. C3 (the specification changed since `begin`) 604:    if ctx.get("spec_sha") is not None and ctx["spec_sha"] != sha256(ctx["doc"]): 607:            f"C3: the specification changed during review {n}; " 
