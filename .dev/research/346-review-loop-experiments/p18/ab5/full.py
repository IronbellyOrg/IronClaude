#!/usr/bin/env python3
"""ab5 variant `full` (run names d5f-r*): ab4 + everything in PN1.

PN1 mechanisms, from the PN1 product code (byte copies under vendor/superclaude/cli/review/, hash-pinned in decision.json) and from
$SP/p13/ab1/harness.py:
  - merge with the typed finding ledger: ledger.merge_round + ledger.render_merged_report + ledger.save, called in-process exactly as
    PN1's `superclaude review merge --ledger review/ledger.json --doc <spec> --round n --resolution panel.json --out review/round<n>.md
    --report rid=path ...` (merge_cmd.command) does; result logged as M<n> (PN1 run_merge).
  - ADJ over ALL ledger rows, shuffled with random.Random(run), anchor / anchor2 / refs / claim per X<k> (PN1 prep_adj, verbatim logic).
  - ledger-driven revise: after V<n>, ledger.apply_revision(ledger, spec-v<n>, spec, findings.parse_fixmap(revise<n>.md).items)
    (PN1 `superclaude review ledger revise`, run_ledger_revise), logged as L<n>.
  - re-review inputs as PN1 prep_reviewer: fresh sandbox r<n>-t1b-1 with the run's spec, specs/history/spec-v<n-1>.md and the merged
    prior review/round<n-1>.md (ledger table with open / resolved_check / resolved / regressed / deferred statuses); its report is merged
    into the ledger as round n (also for a single reviewer, per the PN1 rules file's "Review panel" section).
ab4 layers on top: lint-1/2/3 (lint value in every review brief, file in every reviewer sandbox), AC sweep on R1.t1b-1, cleaned finding
blocks (finding_block clean=True + check_findings_text on every VF list), the clean VF verifier (VF1 after M1, VF2 after M2, VF3 after M3),
reconcile_confirmed, ids_from (recorded per report as a cross-check of the PN1 findings block), token matcher.

Interlock (where PN1's ledger and ab4's VERIFY overlap):
  M<n> decision PASS -> loop PASS.  Otherwise VF<n> verifies the ledger's Reviser-brief rows (brief_ids). A row the verifier rejects is
  parked with ledger.defer(lid, "verifier rejected (VF<n>): ...") (PN1's own parking command) so it leaves brief_ids and later rounds,
  and is recorded as noted, unactioned. The confirmed rows are the IDS of V<n>; round<n>.md gets the VERIFY block and its "Blocking finding
  ids" line narrowed to them. No row confirmed -> VERIFIED-PASS. VF3 with a confirmed row -> ESCALATED (cap 3, as ab4 and PN1)."""
import json
import pathlib
import random
import re
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "vendor"))
from superclaude.cli.review import findings as F  # noqa: E402  (vendored PN1 product code)
from superclaude.cli.review import ledger as LED  # noqa: E402
import harness as h  # noqa: E402  (module-level attributes are read at call time)


def ledger_path(run): return h.ws(run) / h.REVIEW / "ledger.json"


def check_vendor():
    v = h.decision()["frozen"]["pn1_vendor"]
    for name, want in v.items():
        assert h.sha(HERE / "vendor/superclaude/cli/review" / name) == want, f"vendored PN1 file {name} changed"


# ---------------------------------------------------------------- merge with the ledger (PN1 run_merge / merge_cmd.command)
def merge(run, n):
    """Merge the round-n reports into review/ledger.json and render review/round<n>.md. -> printable result (verdict, decision, brief_ids ...)."""
    check_vendor()
    st = h.load(run)
    if f"M{n}" in st["log"]:
        return st["log"][f"M{n}"]
    R = h.ws(run) / h.REVIEW
    if n == 1:
        used = [(h.rid_of(s), R / f"round1-{h.rid_of(s)}.md") for s in h.r1_steps(st) if s not in st.get("r1_lost", [])]
        res_rows = st["panel"]["reviewers"]
    else:
        used = [("t1b-1", R / f"round{n}-t1b-1.md")]
        res_rows = st["panel_rr"]["reviewers"]
    models = {r["reviewer_id"]: r["model"] for r in res_rows}
    reviewers = [{"reviewer_id": rid, "model": models.get(rid), "report_path": str(p), "text": p.read_text(encoding="utf-8", errors="ignore")}
                 for rid, p in used]
    lp = ledger_path(run)
    doc = str(h.ws(run) / h.SPEC)
    doc_text = (h.ws(run) / h.SPEC).read_text(encoding="utf-8")
    led = LED.load(str(lp)) if lp.exists() else LED.new_ledger(doc, 3)
    result = LED.merge_round(led, doc_text, n, reviewers)
    merged = LED.render_merged_report(led, result, doc, doc_text, n)
    (R / f"round{n}.md").write_text(merged, encoding="utf-8")
    LED.save(led, str(lp))
    out = {k: v for k, v in result.items() if not k.startswith("_")}
    st = h.load(run)
    st["log"][f"M{n}"] = dict(out, stratum=st["stratum"], reviewers=[rid for rid, _ in used])
    if n == 1:
        blk = sum(1 for rv in reviewers for f in F.parse_block(rv["text"])["findings"] if f["blocking"])
        st["merge"] = {"raw_count": blk, "merged_count": len(out["brief_ids"]), "rows": len(led["rows"]), "done": True, "lost": [h.rid_of(s) for s in st.get("r1_lost", [])],
                       "reviewers": {rid: {"verdict": h.sc.verdict_of(p.read_text(errors="ignore")), "sha256": h.sha(p)} for rid, p in used},
                       "groups": [{"mid": r["lid"], "theme": "other", "cited": [], "heading": r.get("claim", ""), "members": []} for r in led["rows"]],
                       "stratum": st["stratum"]}
    if out["brief_ids"]:
        st["log"].setdefault(f"VF{n}", {})["finding_ids"] = list(out["brief_ids"])
    h.save(run, st)
    return out


def ledger_revise(run, n):
    """PN1 run_ledger_revise: rows the reviser's fix map names as applied and a hunk touches -> resolved_check; spans re-mapped."""
    check_vendor()
    R = h.ws(run) / h.REVIEW
    led = LED.load(str(ledger_path(run)))
    fm = F.parse_fixmap((R / f"revise{n}.md").read_text(encoding="utf-8", errors="ignore"))
    res = LED.apply_revision(led, (h.ws(run) / h.HIST / f"spec-v{n}.md").read_text(encoding="utf-8"),
                             (h.ws(run) / h.SPEC).read_text(encoding="utf-8"), fm["items"])
    LED.save(led, str(ledger_path(run)))
    res["fixmap_ok"] = fm["ok"]
    st = h.load(run)
    st["log"][f"L{n}"] = dict(res, stratum=st["stratum"])
    h.save(run, st)
    return res


# ---------------------------------------------------------------- VF over the ledger's brief rows (ab4 clean verifier)
def vf_findings(run, n):
    """Finding list for VF<n>: the ### L<k> sections of the ledger-rendered round<n>.md for the brief ids, cut and cleaned (ab4 4a)."""
    st = h.load(run)
    ids = list(st["log"].get(f"M{n}", {}).get("brief_ids") or [])
    text = (h.ws(run) / h.REVIEW / f"round{n}.md").read_text(errors="ignore")
    parts = []
    for lid in ids:
        heading, body = h.sc.finding_block(text, lid, clean=True)
        parts.append(f"### {lid}\n" + "\n".join([heading or f"(no section for {lid})"] + (body or "").splitlines()))
    out = "\n\n".join(parts)
    bad = h.check_findings_text(out)
    if bad:
        raise ValueError(f"finding list for VF{n} still carries non-finding lines: {bad[:3]}")
    (h.ws(run) / h.REVIEW / f"findings-{n}.md").write_text(out + "\n")
    return out, ids


def ingest_vf(run, st, n, outp):
    text = outp.read_text(errors="ignore")
    R = h.ws(run) / h.REVIEW
    ids = st["log"].get(f"VF{n}", {}).get("finding_ids") or []
    table, ok = h.parse_verify(text, ids)
    table = h.reconcile_confirmed(table, ids, text)
    confirmed = [i for i in ids if table[i][0] == "confirm"]
    rejected = {i: table[i][1] for i in ids if table[i][0] == "reject"}
    shutil.copy(outp, R / f"verify-{n}.md")
    led = LED.load(str(ledger_path(run)))
    for lid, reason in rejected.items():
        LED.defer(led, lid, f"verifier rejected (VF{n}): {reason}")
        row = LED._row(led, lid)
        h.noted(run, st, f"VF{n}", lid, "other", [], row.get("claim", ""), reason)
    LED.save(led, str(ledger_path(run)))
    rp, orig = R / f"round{n}.md", R / f"round{n}.orig.md"
    if not orig.exists():
        shutil.copy(rp, orig)
    block = h.VERIFY_BLOCK.format(n=n, c=", ".join(confirmed) or "none",
                                  r="; ".join(f"{i} (verifier: {r})" for i, r in rejected.items()) or "none")
    lines = orig.read_text(errors="ignore").splitlines()
    lines.insert(1, block)                                        # after the ledger's `review: n of 3` line
    lines = [(f"Blocking finding ids: {', '.join(confirmed)}." if confirmed else "Blocking finding ids: none.")
             if ln.startswith("Blocking finding ids:") else ln for ln in lines]
    rp.write_text("\n".join(lines) + "\n")
    return {"finding_ids": ids, "confirmed": confirmed, "rejected": rejected, "parse_ok": ok}


# ---------------------------------------------------------------- ADJ (PN1 prep_adj, verbatim logic)
def prep_adj(run):
    d = h.run_dir(run)
    led = json.loads(ledger_path(run).read_text())
    rows = list(led["rows"])
    order = list(range(len(rows)))
    random.Random(run).shuffle(order)
    sbx = d / "adj"
    if sbx.exists():
        shutil.rmtree(sbx)
    (sbx / "home").mkdir(parents=True)
    shutil.copytree(h.S1 / "inputs/repo-overlay", sbx / "ws")
    (sbx / "ws" / h.D / "review").mkdir(parents=True, exist_ok=True)
    mapping, parts = {}, []
    for k, idx in enumerate(order, 1):
        row = rows[idx]
        mapping[f"X{k}"] = row["lid"]
        lines = [f"### X{k}", "", f"- anchor: {json.dumps(row['anchor'], ensure_ascii=False)}"]
        if row.get("anchor2"):
            lines.append(f"- anchor2: {json.dumps(row['anchor2'], ensure_ascii=False)}")
        lines.append(f"- refs: {', '.join(row.get('refs') or []) or '-'}")
        lines.append(f"- claim: {row.get('claim', '')}")
        parts.append("\n".join(lines))
    (sbx / "ws" / h.D / "review/adj-input.md").write_text("# Findings to adjudicate\n\n" + "\n\n".join(parts) + "\n")
    (d / "adj-map.json").write_text(json.dumps(mapping, indent=1))
    p = d / "PROMPT-ADJ.md"
    p.write_text(h.wrap(sbx, h.ADJ_BRIEF, False))
    st = h.load(run)
    st["log"].setdefault("ADJ", {})["map"] = mapping
    h.save(run, st)
    return p


# ---------------------------------------------------------------- re-review sandbox (PN1 prep_reviewer, n >= 2) + ab4 lint brief
def prep_rereview(run, n):
    d = h.run_dir(run)
    st = h.load(run)
    sb = d / f"r{n}-t1b-1"
    if sb.exists():
        shutil.rmtree(sb)
    (sb / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(h.S1 / "inputs/repo-overlay", sb / "ws")
    (sb / "ws" / h.D / "review").mkdir(parents=True, exist_ok=True)
    (sb / "ws" / h.D / "specs/history").mkdir(parents=True, exist_ok=True)
    shutil.copy(d / "command.md", sb / "command.md")
    shutil.copy(d / "home/.claude/rules/prompts/document_review_loop_prompts.md", sb / "home/.claude/rules/prompts/document_review_loop_prompts.md")
    shutil.copy(h.ws(run) / h.SPEC, sb / "ws" / h.SPEC)
    base = f"{h.HIST}/spec-v{n - 1}.md"
    prior = f"{h.REVIEW}/round{n - 1}.md"
    shutil.copy(h.ws(run) / base, sb / "ws" / base)
    shutil.copy(h.ws(run) / prior, sb / "ws" / prior)
    shutil.copy(h.ws(run) / h.lint_rel(n), sb / "ws" / h.lint_rel(n))
    assert reviewer_ok(st)
    return h.wrap(sb, h.brief_re(prior, base, h.OUT[f"R{n}"], n), True)


def reviewer_ok(st):
    return [r["reviewer_id"] for r in st["panel_rr"]["reviewers"]] == ["t1b-1"]


def telemetry_record(run, step):
    """PN1 append_telemetry record (review-telemetry/1) for one reviewer, written next to the run (not appended to the PN1 clone's
    shared telemetry dir; `task` from `telemetry taskvars` is not computed)."""
    st = h.load(run)
    n = 1 if h.is_r1(step) else int(step[1])
    rid = h.rid_of(step) if h.is_r1(step) else "t1b-1"
    pr = st["panel"] if n == 1 else st["panel_rr"]
    row = next(r for r in pr["reviewers"] if r["reviewer_id"] == rid)
    lg = st["log"][step]
    m = st["log"].get(f"M{n}", {})
    rec = {"schema_version": "review-telemetry/1", "kind": "reviewer_run", "run_id": run, "step": f"R{n}", "round": n, "reviewer_id": rid,
           "panel": {k: pr[k] for k in ("template_id", "template_version", "template_sha256", "tiers_version", "tiers_sha256", "environment")},
           "slot": {k: row[k] for k in ("slot_id", "tier", "alias", "strategy", "seed", "fallback_depth", "stand_in")},
           "model": {"resolved": row["model"], "launch": lg.get("model"), "observed": lg.get("observed_model"), "live": row.get("live_model")},
           "output": {"block_ok": lg.get("block_ok"), "findings": lg.get("block_findings"), "verdict": lg.get("verdict"),
                      "verdict_mismatch": lg.get("verdict") != m.get("verdict")},
           "cost": {"tokens_out": lg.get("output_tokens")}, "context": {"experiment": "ab5", "variant": "full", "stratum": st["stratum"]},
           "stratum": st["stratum"]}
    (h.run_dir(run) / f"telemetry-{step}.json").write_text(json.dumps(rec))
    return rec
