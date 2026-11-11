f21839dcbefcf43d281b8d331a7ba65f00a0d9fe
family begin-exit-code: defect form = begin gating on a fix record without its accepted flag
command: grep -n -e 'fix.get(' -e EXIT_REJECT src/superclaude/skills/sc-diffgate/scripts/diffgate.py
before: 28:EXIT_OK, EXIT_REJECT, EXIT_USAGE, EXIT_INPUT, EXIT_CLOSED, EXIT_ORDER, EXIT_LEDGER = (
before: 1061:        "declined": sorted(fix.get("declined", {})),
before: 1062:        "owners": fix.get("owners", {}),
before: 1153:        if fix.get("doc_sha") != sha:
before: 1167:                EXIT_REJECT,
before: 1296:                "exit": EXIT_REJECT,
before: 1314:            "exit": EXIT_REJECT,
before: 1399:    code = EXIT_OK if res["accepted"] else EXIT_REJECT
before: 1422:            fix["failed_runs"] = fix.get("failed_runs", 0) + 1
before: 1486:        if fix.get("accepted") and fix.get("doc_sha") == current:
family cap-enforcement: defect form = the review cap or closed state read from a mutable ledger flag only
command: grep -n -e CAP_REVIEWS -e '"closed"' -e 'closed=' src/superclaude/skills/sc-diffgate/scripts/diffgate.py
before: 23:CAP_REVIEWS = 3  # the cap is a constant, never a flag
before: 254:        f"# Diffgate surface: review {review} of {CAP_REVIEWS}",
before: 963:    if led.get("closed"):
before: 1100:                "closed": False,
before: 1214:        f"# Reviser brief: review {n} of {CAP_REVIEWS}",
before: 1239:    if result["verdict"] == "PASS" or n == CAP_REVIEWS:
before: 1240:        out += [f"## Diffgate close (review {n} of {CAP_REVIEWS})", ""]
before: 1303:                    led.update(closed=True, halt="invalid")
before: 1320:    elif n == CAP_REVIEWS:
before: 1346:            led.update(closed=True, halt=halt)
before: 1350:        if result["verdict"] == "FAIL" and n < CAP_REVIEWS:
before: 1427:            if fix["failed_runs"] >= CAP_REVIEWS:
before: 1429:                led.update(closed=True, halt="escalate")
before: 1469:    if led.get("closed"):
before: 1470:        state = "invalid" if led.get("halt") == "invalid" else "closed"
family test-coverage: defect form = a delivered behaviour with no test
command: grep -n -e 'close-r' -e 'fixmap-r' tests/skills/test_diffgate_script.py
before: 895:    close = (lp.d / "close-r1.md").read_text(encoding="utf-8")
before: 905:        fh.write((lp.d / "close-r1.md").read_text(encoding="utf-8") + "\nmore text\n")
before: 942:    close = (lp.d / "close-r2.md").read_text(encoding="utf-8")
coupled sites: cmd_begin gating, replay, test_begin_review_two_needs_an_accepted_fix_map, test_flg_r1_shaped_loop
after (begin-exit-code): 28:EXIT_OK, EXIT_REJECT, EXIT_USAGE, EXIT_INPUT, EXIT_CLOSED, EXIT_ORDER, EXIT_LEDGER = ( 1045:            or not fix.get("accepted") 1046:            or fix.get("fix_rejected") 1088:        "declined": sorted(fix.get("declined", {})), 1089:        "owners": fix.get("owners", {}), 1187:        if not fix.get("accepted") or fix.get("doc_sha") != sha: 1201:                EXIT_REJECT, 1330:                "exit": EXIT_REJECT, 1348:            "exit": EXIT_REJECT, 1433:    code = EXIT_OK if res["accepted"] else EXIT_REJECT 1456:            fix["failed_runs"] = fix.get("failed_runs", 0) + 1 1520:        if fix.get("accepted") and fix.get("doc_sha") == current: 
after (cap-enforcement): 23:CAP_REVIEWS = 3  # the cap is a constant, never a flag 254:        f"# Diffgate surface: review {review} of {CAP_REVIEWS}", 963:    if led.get("closed"): 1050:    halt = _expected_halt(led) 1051:    if bool(led.get("closed")) != (halt is not None) or led.get("halt") != halt: 1055:def _expected_halt(led: dict): 1062:    if check and n >= CAP_REVIEWS: 1127:                "closed": False, 1173:        if m > CAP_REVIEWS: 1176:                f"the cap is {CAP_REVIEWS} reviews; do not review, escalate", 1248:        f"# Reviser brief: review {n} of {CAP_REVIEWS}", 1273:    if result["verdict"] == "PASS" or n == CAP_REVIEWS: 1274:        out += [f"## Diffgate close (review {n} of {CAP_REVIEWS})", ""] 1337:                    led.update(closed=True, halt="invalid") 1354:    elif n == CAP_REVIEWS: 1380:            led.update(closed=True, halt=halt) 1384:        if result["verdict"] == "FAIL" and n < CAP_REVIEWS: 1461:            if fix["failed_runs"] >= CAP_REVIEWS: 1463:                led.update(closed=True, halt="escalate") 1503:    if led.get("closed"): 1504:        state = "invalid" if led.get("halt") == "invalid" else "closed" 
after (test-coverage): 904:    close = (lp.d / "close-r1.md").read_text(encoding="utf-8") 914:        fh.write((lp.d / "close-r1.md").read_text(encoding="utf-8") + "\nmore text\n") 951:    close = (lp.d / "close-r2.md").read_text(encoding="utf-8") 1048:    kept = (lp.d / "fixmap-r1.txt").read_text(encoding="utf-8").splitlines() 1070:    close = (lp.d / "close-r3.md").read_text(encoding="utf-8") 
