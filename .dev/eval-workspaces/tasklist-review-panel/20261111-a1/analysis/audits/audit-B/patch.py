s = open("audit.py").read()
old_start = s.index("    if r[\"size\"] < 600:")
old_end = s.index("    # 2\n")
new = '''    pre = re.sub(r"\\b(not|n't|no|never)\\s+(be\\s+)?incomplete\\b", "", pre)
    zero_valid = (fs is not None and len(fs) == 0 and r["verdict"] in ("PASS", "FAIL") and re.search(r"coverage|covered", low))
    if r["size"] < 600:
        if zero_valid and r["verdict"] == "PASS": flag("1-short", r, "WARN", f"report {r['size']} bytes but a valid zero-finding PASS with coverage statement")
        else: flag("1-short", r, "EXCLUDE", f"report {r['size']} bytes")
    inc_verdict = re.search(r"^\\W*verdict:?\\W*incomplete", t, re.M | re.I)
    if inc_verdict or re.search(r"\\bincomplete\\b", pre) or re.search(r"^\\W*(#+\\s*)?review incomplete", low, re.M):
        flag("1-incomplete", r, "EXCLUDE", "positive 'incomplete' refusal" + (" (verdict: INCOMPLETE)" if inc_verdict else "") + "; " + ("empty findings block" if fs == [] else "findings=%s" % (len(fs) if fs is not None else None)))
    else:
        body_pre = re.split(r"```findings-v1", t)[0].lower()
        mm = re.search(r"(?<!no )(?<!not )(?<!nor )(source\\.md|source document|requirements document|input file|merged-requirements\\.md)[^.\\n]{0,80}(is missing|are missing|unreadable|not found|could not be read|cannot be read|does not exist|missing or unreadable)", body_pre)
        if mm:
            neg = re.search(r"(no input (was )?missing|nothing (was )?missing|no input is missing|not incomplete)", body_pre)
            if not neg:
                hit = mm.start() < 600
                flag("1-missing-input", r, "EXCLUDE" if (hit or r["size"] < 2500) else "WARN", "mentions missing/unreadable input: ..." + ws(body_pre[max(0, mm.start()-20):mm.end()+20])[:120])
    if "API Error" in t[:600] or ("api error" in low and r["size"] < 2000): flag("1-apierror", r, "EXCLUDE", "'API Error' text")
    if "unrecognized_model" in low and not ("unrecognized_model" in cand[p].lower()):
        flag("1-unrecognized_model", r, "EXCLUDE" if (r["size"] < 2000 or fs is None) else "WARN", "'unrecognized_model' text (not in candidate)")
'''
s = s[:old_start] + new + s[old_end:]
# verdict capture: also INCOMPLETE
s = s.replace('(PASS|FAIL)\\b", t, re.M | re.I)', '(PASS|FAIL)\\b", t, re.M | re.I)')
open("audit.py","w").write(s)
