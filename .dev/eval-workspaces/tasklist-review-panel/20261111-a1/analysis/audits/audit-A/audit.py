import json, os, re, glob, hashlib, subprocess, collections, sys
E = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
PKGS = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
SKIP = ("i1-grok-sonnet", "i2-haiku-sonnet", "contaminated", "superseded", "quarantine")
flags = []
def flag(check, row, pkg, rid, sev, reason):
    if check=='1b-name-derived-mismatch' and row=='n5-sonnet': sev='WARN'; reason+=' [downgraded: n5-sonnet name does not list muse/glm; observed models equal sibling rows n5-sol/n5-terra resolution.json (t2b muse-wonder, t3 glm-5.3); intended UNVERIFIED]'
    flags.append((check, row, pkg, rid, sev, reason))
def norm(m): return (m or "").lower()
def ok_eq(a, b):
    a, b = norm(a), norm(b); return a == b or a == b + "-build" or b == a + "-build"
def family(row): return re.sub(r"-r\d+$", "", row)
def jl(path):
    try: return json.load(open(path))
    except Exception: return None
stats = collections.defaultdict(lambda: collections.Counter())
runs = 0
hashes = collections.defaultdict(list)
bymodel = collections.defaultdict(set)
pres = collections.defaultdict(set)
xpk = collections.defaultdict(set)
for pkg in PKGS:
    base = f"{E}/{pkg}/reviews/combos"
    for row in sorted(os.listdir(base)):
        if any(s in row for s in SKIP): continue
        d = f"{base}/{row}"
        if not os.path.isdir(d): continue
        res = jl(f"{E}/combos/{row}/{pkg}/resolution.json")
        intended = {}
        if res:
            for r in res["reviewers"]: intended[r["reviewer_id"]] = r["model"]
        else:
            stats[fam]['no_resolution_row']+=1
        rids = sorted({f.split(".")[0] for f in os.listdir(d) if f.endswith(".meta.json") and ".attempt" not in f})
        for rid in intended:
            if rid not in rids: flag("R1-missing-run", row, pkg, rid, "WARN", "reviewer in resolution.json has no run output")
        for rid in rids:
            runs += 1; fam = family(row); stats[fam]["runs"] += 1
            p = f"{d}/{rid}"
            meta = jl(p + ".meta.json") or {}
            cost = jl(p + ".cost.json") or {}
            exp, obs = meta.get("expected_model", ""), meta.get("observed_model", "")
            inten = intended.get(rid)
            if inten is None:
                stats[fam]['no_resolution']+=1; bymodel[(row,rid)].add(pkg)
            else:
                if not (ok_eq(inten, exp) and ok_eq(inten, obs)):
                    flag("1-intended-mismatch", row, pkg, rid, "EXCLUDE", f"intended={inten} meta.expected={exp} observed={obs}"); stats[fam]["c1"] += 1
            if os.path.exists(p + ".fallback.log"):
                flag("2-fallback", row, pkg, rid, "EXCLUDE", open(p + ".fallback.log").read().strip().replace("\n", " | ")); stats[fam]["c2"] += 1
            if not obs or obs == "<synthetic>" or "," in obs:
                flag("3-bad-observed", row, pkg, rid, "EXCLUDE", f"observed_model={obs!r}"); stats[fam]["c3"] += 1
            atts = sorted(int(re.search(r"attempt(\d+)\.meta", f).group(1)) for f in os.listdir(d) if f.startswith(rid + ".attempt") and f.endswith(".meta.json"))
            if not atts:
                flag("4-no-attempts", row, pkg, rid, "EXCLUDE", "no attempt meta"); continue
            n = meta.get('attempt') or max(atts)
            stale = [k for k in atts if k > n]
            if stale:
                flag('5-stale-attempt-leftover', row, pkg, rid, 'WARN', f'attempt files {stale} are older leftovers from an earlier run (final meta.attempt={n}); cost.json counts them')
                stats[fam]['stale'] += 1
            fin_md, att_md, att_json = p + ".md", f"{p}.attempt{n}.md", f"{p}.attempt{n}.json"
            if not (os.path.exists(fin_md) and os.path.exists(att_md)) or subprocess.run(["cmp", "-s", fin_md, att_md]).returncode != 0:
                flag("4-final-md-differs", row, pkg, rid, "EXCLUDE", f"final .md != attempt{n}.md"); stats[fam]["c4"] += 1
            try:
                j = json.load(open(att_json))
            except Exception as e:
                flag("4-json-unreadable", row, pkg, rid, "EXCLUDE", f"attempt{n}.json unreadable {e}"); stats[fam]["c4"] += 1; continue
            mm = sorted({m["message"].get("model") for m in j if m.get("type") == "assistant" and m.get("parent_tool_use_id") is None})
            if not mm or mm != [m for m in mm if m] or len(mm) != 1 or not ok_eq(mm[0], obs):
                flag("4-independent-obs-differs", row, pkg, rid, "EXCLUDE", f"raw={mm} meta.observed={obs}"); stats[fam]["c4"] += 1
            elif inten and not ok_eq(mm[0], inten):
                flag("4-raw-vs-intended", row, pkg, rid, "EXCLUDE", f"raw={mm} intended={inten}"); stats[fam]["c4"] += 1
            am = jl(f"{p}.attempt{n}.meta.json") or {}
            if am.get("observed_model") != obs or am.get("expected_model") != exp:
                flag("X-meta-vs-attemptmeta", row, pkg, rid, "WARN", "final meta differs from last attempt meta")
            # 5 cost
            if cost.get("attempts") != len(atts):
                flag("5-cost-attempts", row, pkg, rid, "WARN", f"cost.attempts={cost.get('attempts')} files={len(atts)}"); stats[fam]["c5"] += 1
            am_all = [jl(f"{p}.attempt{k}.meta.json") or {} for k in atts]
            am_run = [a for k,a in zip(atts,am_all) if k <= n]
            if cost.get("total_output_tokens_all") != sum(a.get("output_tokens_all", 0) for a in am_all):
                flag("5-cost-tokens", row, pkg, rid, "WARN", f"cost={cost.get('total_output_tokens_all')} sum={sum(a.get('output_tokens_all',0) for a in am_all)}"); stats[fam]["c5"] += 1
            if cost.get("total_wall_s") != sum(a.get("wall_s", 0) for a in am_all):
                flag("5-cost-wall", row, pkg, rid, "WARN", f"cost={cost.get('total_wall_s')} sum={sum(a.get('wall_s',0) for a in am_all)}"); stats[fam]["c5"] += 1
            if n >= 2:
                a1 = am_run[0]; err = ""
                try: err = open(f"{p}.attempt1.err", errors="replace").read()[:200].replace("\n", " ")
                except Exception: pass
                outage = ("native binary not installed" in err) or (a1.get("exit") == 127 and a1.get("output_tokens_all", 0) == 0 and a1.get("wall_s", 9) == 0)
                flag("5-retry", row, pkg, rid, "WARN", f"final_attempt={n} a1: exit={a1.get('exit')} tok={a1.get('output_tokens_all')} wall={a1.get('wall_s')} obs={a1.get('observed_model')!r} outage={outage} err={err[:100]}")
                stats[fam]["c5retry"] += 1
                if outage: stats[fam]["outage"] += 1
            # 6 misrouting
            tok = meta.get("output_tokens_all", 0)
            if tok == 0 and meta.get("model_ok"): flag("6-zero-tokens-ok", row, pkg, rid, "EXCLUDE", "output_tokens_all==0 with model_ok"); stats[fam]["c6"] += 1
            md = open(fin_md, errors="replace").read() if os.path.exists(fin_md) else ""
            if tok < 400 and tok != 0 or len(md) < 1200 and False: flag("6-short-tokens", row, pkg, rid, "WARN", f"output_tokens_all={tok}"); stats[fam]["c6"] += 1
            for k in atts:
                try:
                    et = open(f"{p}.attempt{k}.err", errors="replace").read()
                    if "unrecognized_model" in et: stats[fam]["unrec_warn_lines"] += 1
                    rest = "\n".join(l for l in et.splitlines() if l.strip() and "unrecognized_model" not in l)
                    if rest: flag("6-other-stderr", row, pkg, rid, "WARN", f"attempt{k}.err: {rest[:150]}"); stats[fam]["c6"] += 1
                except Exception: pass
            # extra checks
            # E1: system init model / modelUsage keys / subagent models
            init = [m.get("model") for m in j if m.get("type") == "system" and m.get("subtype") == "init"]
            mu = set()
            for m in j:
                if m.get("type") == "result": mu |= set((m.get("modelUsage") or {}).keys())
            sub = {m["message"].get("model") for m in j if m.get("type") == "assistant" and m.get("parent_tool_use_id") is not None}
            for im in init:
                if im and not ok_eq(im.split("[")[0], obs) and not ok_eq(im, obs):
                    flag("E1-init-model-differs", row, pkg, rid, "WARN", f"init.model={im} observed={obs}"); stats[fam]["E1"] += 1
            extra = {x for x in mu if not ok_eq(x.split("[")[0], obs)}
            if extra:
                flag("E2-modelUsage-extra-models", row, pkg, rid, "WARN", f"modelUsage keys={sorted(mu)} observed={obs}"); stats[fam]["E2"] += 1
            if sub - {None, obs} and any(s and not ok_eq(s, obs) for s in sub):
                flag("E3-subagent-model-differs", row, pkg, rid, "WARN", f"subagent models={sorted(x for x in sub if x)}"); stats[fam]["E3"] += 1
            inits=[]
            for k in atts:
                if k>n: continue
                try:
                    jj=json.load(open(f"{p}.attempt{k}.json"))
                    inits.append((k,[m.get('model') for m in jj if m.get('type')=='system' and m.get('subtype')=='init']))
                except Exception: pass
            flat={x for _,l in inits for x in l if x}
            if len({x.split('[')[0] for x in flat})>1: flag('E9-init-model-varies-across-attempts', row, pkg, rid, 'WARN', f'init models {inits}')
            if inten is None:
                allowed=set(); nm=row
                for tok,mod in (('muse','muse-wonder-1.0'),('ember','muse-ember-1.0'),('luna','gpt-6-luna'),('haiku','claude-haiku-5-5'),('sonnet','claude-sonnet-5-5'),('terra','gpt-6.1-terra'),('grok','grok-4.7'),('glm','glm-5.3'),('sol','gpt-6.1-sol')):
                    if tok in nm: allowed.add(mod)
                if 'muse' in nm and 'ember' in nm: allowed.discard('muse-wonder-1.0') if False else None
                if not any(ok_eq(obs,a) for a in allowed):
                    flag('1b-name-derived-mismatch', row, pkg, rid, 'EXCLUDE', f'observed {obs} not among models named in row name {sorted(allowed)}')
                elif any(ok_eq(i.split('[')[0], obs) is False for i in flat): pass
                else: stats[fam]['name_ok']+=1
            # E4: model_ok recomputed
            if meta.get("model_ok") is not True: flag("E4-model_ok-not-true", row, pkg, rid, "EXCLUDE", f"model_ok={meta.get('model_ok')}"); stats[fam]["E4"] += 1
            if meta.get("findings_block") is not True: flag("E4b-no-findings-block", row, pkg, rid, "WARN", "findings_block false in final"); stats[fam]["E4b"] += 1
            # E5: earlier attempt observed different model than final (silent within-model-switch)
            for k, a in zip(atts, am_all):
                if k < n and a.get("observed_model") and not ok_eq(a.get("observed_model"), obs):
                    flag("E5-earlier-attempt-other-model", row, pkg, rid, "WARN", f"attempt{k} observed={a.get('observed_model')} final={obs}"); stats[fam]["E5"] += 1
            xpk[(row,rid)].add(norm(obs).replace('-build',''))
            pres[(row,rid)].add(pkg)
            # E6: duplicate final report text across runs (copy/contamination)
            h = hashlib.sha256(md.encode()).hexdigest()
            hashes[h].append((row, pkg, rid))
            # E7: report lacks 'review: 1 of 3' first line, or is empty/API error
            if not md.strip(): flag("E7-empty-report", row, pkg, rid, "EXCLUDE", "empty final md"); stats[fam]["E7"] += 1
            elif "API Error" in md[:400]: flag("E7-api-error-report", row, pkg, rid, "EXCLUDE", "API Error in report"); stats[fam]["E7"] += 1
            # E8: report self-identifies as a different model family (e.g. 'I am Claude' in a non-Claude run)
            m = re.search(r"\b(I am|I'm|as) (Claude|GPT|Grok|Gemini|GLM|Qwen)[^.\n]{0,40}", md)
            if m: flag("E8-self-identification", row, pkg, rid, "WARN", f"report says {m.group(0)!r}; observed={obs}"); stats[fam]["E8"] += 1
for (row,rid),ps in pres.items():
    for pk in PKGS:
        if pk not in ps: flag('E11-run-missing-in-package', row, pk, rid, 'WARN', f'present in {len(ps)} of 3 packages (missing here; outage rerun in progress or never run)')
for (row,rid),ms in xpk.items():
    if len(ms)>1: flag('E10-cross-package-model-differs', row, '*', rid, 'EXCLUDE', f'models across packages {sorted(ms)}')
for h, lst in hashes.items():
    if len(lst) > 1:
        for (row, pkg, rid) in lst:
            flag("E6-duplicate-report", row, pkg, rid, "EXCLUDE", f"identical final md as {len(lst)-1} other run(s): {[x for x in lst if x != (row,pkg,rid)][:2]}")
with open("/tmp/audit-A/flags.tsv", "w") as f:
    f.write("check\trow\tpackage\treviewer\tseverity\treason\n")
    for t in flags: f.write("\t".join(str(x).replace("\t", " ") for x in t) + "\n")
json.dump({k: dict(v) for k, v in stats.items()}, open("/tmp/audit-A/stats.json", "w"), indent=1)
print("runs", runs, "flags", len(flags))
c = collections.Counter((t[0], t[4]) for t in flags)
for k, v in sorted(c.items()): print(k, v)
