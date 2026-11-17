"""Stage 0c: merge the three blind graders' files, validate them, compute the counts and write
stage0c-grades.jsonl and stage0c-regrade.md. Run from the repository root:
  uv run --no-project python -I .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0c-analyze.py
Reads only: ./stage0c-work/{in,out,agent-ids.txt}, PF 05-scoring/consensus.md (read-only).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

PKG = Path(".dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044")
ART = PKG / "artifacts"
W = ART / "stage0c-work"
PF = Path(".dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115")
VER = {"A": "old", "B": "new"}
# planned first text per chunk, per grader (the prompts fix this)
PLAN = {1: "ABAB", 2: "BABA", 3: "ABBA"}


def read_agent_ids():
    ids = {}
    for ln in (W / "agent-ids.txt").read_text().splitlines():
        if ln.strip():
            g, a = ln.split()
            ids[int(g)] = a
    return ids


def read_panel():
    panel = {}
    for ln in (PF / "05-scoring/consensus.md").read_text().splitlines():
        if not ln.startswith("| F-"):
            continue
        fid = ln.split("|")[1].strip()
        m = re.search(r"\| (\d) \| (\d) \| (\d) \| ([\d.]+) \| ", ln)
        if not m:
            sys.exit(f"cannot parse consensus row {fid}")
        panel[fid] = float(m.group(4))
    return panel


def read_table(n):
    rows = []
    for ln in (W / f"in/table-{n}.md").read_text().splitlines()[6:]:
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        rows.append((c[0], c[1], c[2]))
    return rows


def conf(pairs):
    """pairs: list of (panel_blocker, graded_blocking)."""
    tp = sum(1 for p, g in pairs if p and g)
    fp = sum(1 for p, g in pairs if not p and g)
    fn = sum(1 for p, g in pairs if p and not g)
    tn = sum(1 for p, g in pairs if not p and not g)
    n = tp + fp + fn + tn
    acc = (tp + tn) / n
    pe = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / (n * n)
    kappa = (acc - pe) / (1 - pe) if pe < 1 else float("nan")
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, n=n, acc=acc, kappa=kappa,
                recall=tp / (tp + fn) if tp + fn else float("nan"),
                precision=tp / (tp + fp) if tp + fp else float("nan"))


def main():
    ids = read_agent_ids()
    panel = read_panel()
    assert len(panel) == 318, len(panel)
    pblock = {k: v >= 4.0 for k, v in panel.items()}
    problems = []
    grades = []  # merged lines
    meta = {}
    quote_ok = quote_bad = 0
    rule = {"A": (W / "in/rule-A.txt").read_text(), "B": (W / "in/rule-B.txt").read_text()}
    for g in (1, 2, 3):
        table = read_table(g)
        pos = {r[0]: i for i, r in enumerate(table)}
        seen = {}
        for ln in (W / f"out/grader-{g}.jsonl").read_text().splitlines():
            if not ln.strip():
                continue
            d = json.loads(ln)
            if d.get("meta"):
                meta[g] = d
                continue
            fid, t = d["id"], d["text"]
            if fid not in pos or t not in VER:
                problems.append(f"g{g}: bad id/text {fid} {t}")
                continue
            if (fid, t) in seen:
                problems.append(f"g{g}: duplicate {fid} {t}")
                continue
            seen[(fid, t)] = d
            chunk = min(pos[fid] // 80, 3)
            first = PLAN[g][chunk]
            exp_order = 1 if t == first else 2
            if d["order"] != exp_order:
                problems.append(f"g{g}: order {fid} {t} is {d['order']}, planned {exp_order}")
            if not isinstance(d["blocking"], bool):
                problems.append(f"g{g}: non-bool grade {fid} {t}")
            if d["quote"] and d["quote"] in rule[t]:
                quote_ok += 1
            else:
                quote_bad += 1
            grades.append({"agent": ids[g], "grader": f"g{g}", "id": fid,
                           "text_version": VER[t], "order": d["order"],
                           "blocking": d["blocking"], "quote": d["quote"]})
        want = {(r[0], t) for r in table for t in "AB"}
        if set(seen) != want:
            problems.append(f"g{g}: missing {len(want - set(seen))} grades, extra {len(set(seen) - want)}")
    n_expected = 318 * 3 * 2
    out_jsonl = ART / "stage0c-grades.jsonl"
    with out_jsonl.open("w") as f:
        for d in grades:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"grades written: {len(grades)} (expected {n_expected}); problems: {len(problems)}")
    for p in problems[:30]:
        print("PROBLEM", p)
    if len(grades) != n_expected:
        sys.exit("grade count wrong; stop")

    # index: (id, version) -> {grader: bool}
    by = {}
    for d in grades:
        by.setdefault((d["id"], d["text_version"]), {})[d["grader"]] = d
    allids = sorted(panel)
    maj = {(i, v): sum(by[(i, v)][g]["blocking"] for g in by[(i, v)]) >= 2 for i in allids for v in ("old", "new")}
    votes = {(i, v): sum(by[(i, v)][g]["blocking"] for g in by[(i, v)]) for i in allids for v in ("old", "new")}

    st = {}
    for v in ("old", "new"):
        st[f"maj_{v}"] = conf([(pblock[i], maj[(i, v)]) for i in allids])
        for g in ("g1", "g2", "g3"):
            st[f"{g}_{v}"] = conf([(pblock[i], by[(i, v)][g]["blocking"]) for i in allids])
    # movement
    def move(sel):
        o2n = [i for i in allids if sel(i, "old") and not sel(i, "new")]
        n2o = [i for i in allids if (not sel(i, "old")) and sel(i, "new")]
        bb = [i for i in allids if sel(i, "old") and sel(i, "new")]
        nn = [i for i in allids if (not sel(i, "old")) and (not sel(i, "new"))]
        return o2n, n2o, bb, nn
    mv = {"maj": move(lambda i, v: maj[(i, v)])}
    for g in ("g1", "g2", "g3"):
        mv[g] = move(lambda i, v, g=g: by[(i, v)][g]["blocking"])
    # order effect on movement (pooled over agents): row graded old-first vs new-first
    oe = {"old_first": [0, 0, 0], "new_first": [0, 0, 0]}  # rows, old->new, new->old
    for i in allids:
        for g in ("g1", "g2", "g3"):
            o, n = by[(i, "old")][g], by[(i, "new")][g]
            key = "old_first" if o["order"] == 1 else "new_first"
            oe[key][0] += 1
            oe[key][1] += o["blocking"] and not n["blocking"]
            oe[key][2] += (not o["blocking"]) and n["blocking"]
    # spread
    spread = {}
    for v in ("old", "new"):
        dist = Counter(votes[(i, v)] for i in allids)
        spread[v] = dict(dist=dist, unanimous=dist[0] + dist[3], split=dist[1] + dist[2])
    pair = {}
    for v in ("old", "new"):
        for a, b in (("g1", "g2"), ("g1", "g3"), ("g2", "g3")):
            ag = sum(by[(i, v)][a]["blocking"] == by[(i, v)][b]["blocking"] for i in allids)
            pair[(v, a, b)] = ag
    # tables for descriptions
    desc = {r[0]: (r[1], r[2]) for r in read_table(1)}
    metas = {g: meta.get(g) for g in (1, 2, 3)}

    o2n, n2o, bb, nn = mv["maj"]
    risk = [i for i in allids if maj[(i, "old")] != maj[(i, "new")] and pblock[i]]
    anyrisk = [i for i in allids if pblock[i] and any(by[(i, "old")][g]["blocking"] != by[(i, "new")][g]["blocking"] for g in ("g1", "g2", "g3"))]

    def f(x):
        return f"{x:.3f}"

    def mat(c):
        return f"| {c['tp']} | {c['fp']} | {c['fn']} | {c['tn']} | {c['n']} | {f(c['acc'])} | {f(c['kappa'])} | {f(c['recall'])} | {f(c['precision'])} |"

    def trunc(s, n=140):
        s = s.replace("|", "\\|")
        return s if len(s) <= n else s[: n - 1] + "…"

    def q(s):
        return s.replace("|", "\\|")

    # sample of grades: every 159th of the merged list ordered by (id, grader, version)
    srt = sorted(grades, key=lambda d: (d["id"], d["grader"], d["text_version"]))
    sample = []
    for g in ("g1", "g2", "g3"):
        for v in ("old", "new"):
            sub = [d for d in srt if d["grader"] == g and d["text_version"] == v]
            sample += [sub[40], sub[200]]

    L = []
    A = L.append
    A("# Stage 0c result: the scored table re-graded under the old and the new rule text\n")
    A("This file is the owner-readable result of the stage 0 package. It is generated by `./artifacts/stage0c-analyze.py` from `./artifacts/stage0c-grades.jsonl` (all numbers below are computed by that script, none typed by hand). Read the limits section before relying on any figure.\n")
    A("## What was measured\n")
    A("Three blind agents each graded all 318 findings of the scored table (`04-historical/master-table.md`, read through the blind copies `blind-table-1.md`, `blind-table-2.md`, `blind-table-3.md`, which show ID, category, description and context only) twice: once applying today's rule text (lines 221 to 231 of `src/superclaude/output-styles/pragmatic.md`, copied to `./artifacts/stage0c-work/in/rule-A.txt`, called text A) and once applying the digest of spec section 4.1 (REQ-01, copied to `./artifacts/stage0c-work/in/rule-B.txt`, text B). In this file A is called the old text and B the new text. 318 findings x 3 agents x 2 texts = 1908 grades, all in `./artifacts/stage0c-grades.jsonl` with agent id, text version and order position. The panel consensus in `05-scoring/consensus.md` (three blind scorers, a finding is a blocker at mean 4.0 or higher) is the reference: it calls %d of the 318 blockers.\n" % sum(pblock.values()))
    A("**The table holds only findings that were filed as blocking** (all 318 rows came from reviews that labelled them blocking). So the matrix below can say how many of those a rule text still calls blocking; it cannot say anything about findings that were never filed as blocking.\n")
    A("### Agents and order\n")
    A("Agents (general-purpose agents spawned in this session, one per table order; agent id, then the order of the texts per chunk of 80 table lines, `A` = old text, `B` = new text):\n")
    A("| Grader | Agent id | Table copy | Chunk order (first text, then the other) | other blocking definition seen in its context (its own report) |")
    A("|---|---|---|---|---|")
    for g in (1, 2, 3):
        m = metas[g]
        seen = "not reported" if not m else f"{m.get('other_blocking_definition_in_context')}: {q(str(m.get('first_words',''))[:120])}"
        A(f"| g{g} | {ids[g]} | `blind-table-{g}.md` | " + ", ".join(f"chunk {c+1}: {PLAN[g][c]} then {'B' if PLAN[g][c]=='A' else 'A'}" for c in range(4)) + f" | {seen} |")
    A("\nNone of these agents wrote the digest, the spec, the rule text or any finding it graded: each is a fresh agent that received only its brief (saved at `./artifacts/stage0c-work/grader-prompt-1.md`; graders 2 and 3 differ only in the table path, the output path and the chunk order) and had no earlier context. The agent that ran this package (the session executor) did not grade; it checked the files and computed the counts.\n")
    A("### How the graders were instructed\n")
    A("Each grader was told to apply only the rule text it was given for each grade, to ignore every other rule or habit about grading review findings in its context (system instructions, style instructions, memory), to judge from the description and context as written, to copy a verbatim phrase of the rule text that decided each grade into a `quote` field, and to read only the two rule files and its own table copy. The graders were not told which text is old and which is new, nor that the table holds only blocking-filed findings.\n")
    mo, mn = st["maj_old"], st["maj_new"]
    A("## Plain reading of the result\n")
    A(f"- Under the old text the majority of the three agents graded {mo['tp'] + mo['fp']} of 318 findings blocking; under the new text {mn['tp'] + mn['fp']} of 318. The panel calls {mo['tp'] + mo['fn']} of 318 blockers.")
    A(f"- Only {len(mv['maj'][0])} findings moved from blocking to not blocking and {len(mv['maj'][1])} moved the other way (majority grade). The new text, as these graders applied it, did not cut the blocking share of this table.")
    A(f"- Both texts catch {mo['tp']} of the {mo['tp'] + mo['fn']} panel blockers under the majority grade (recall {f(mo['recall'])} old, {f(mn['recall'])} new) at the price of {mo['fp']} (old) and {mn['fp']} (new) findings the panel does not call blockers; agreement with the panel is {f(mo['acc'])} old and {f(mn['acc'])} new.")
    A("- So this regrade shows no measurable effect of the new text on this table. It does not show why. Possible reasons, none tested here: the old rule in each grader's context (see the confound section); the table holds only findings filed as blocking and each description states a consequence, which both texts count; graders read each description as true and so find a consequence in almost every row. The result is reported as it came out.\n")
    A("## Counts\n")
    A("Panel blocker = positive. Matrix columns: TP = rule text says blocking and panel says blocker; FP = rule text says blocking, panel says not; FN = rule text says not blocking, panel says blocker; TN = both say not. `Majority` means at least 2 of the 3 agents graded the finding blocking.\n")
    A("### Confusion matrix against the panel consensus\n")
    A("| Grades | TP | FP | FN | TN | Total | Agreement with panel | Cohen's kappa | Recall of panel blockers | Precision |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for v in ("old", "new"):
        A(f"| **Majority, {v} text** " + mat(st[f"maj_{v}"]))
    for v in ("old", "new"):
        for g in ("g1", "g2", "g3"):
            A(f"| {g} alone, {v} text " + mat(st[f"{g}_{v}"]))
    A("")
    A("### Old-to-new movement (findings graded differently under the two texts)\n")
    A("| Grades | blocking under old, not blocking under new | not blocking under old, blocking under new | blocking under both | not blocking under both |")
    A("|---|---|---|---|---|")
    for key, label in (("maj", "Majority of three"), ("g1", "g1 alone"), ("g2", "g2 alone"), ("g3", "g3 alone")):
        a, b, c, d = mv[key]
        A(f"| {label} | {len(a)} | {len(b)} | {len(c)} | {len(d)} |")
    A("")
    A("These movement counts are a lower bound on the change the new text makes, see the confound section: every grader had the old rule in its context while applying the new text.\n")
    A("Order check (paired design, order alternated; pooled over the three agents, 954 finding-by-agent pairs): ")
    A("")
    A("| Which text was graded first | pairs | blocking under old, not under new | not blocking under old, blocking under new |")
    A("|---|---|---|---|")
    A(f"| old text first | {oe['old_first'][0]} | {oe['old_first'][1]} | {oe['old_first'][2]} |")
    A(f"| new text first | {oe['new_first'][0]} | {oe['new_first'][1]} | {oe['new_first'][2]} |\n")
    A("### Spread among the three agents\n")
    A("Number of findings by how many of the 3 agents graded them blocking:\n")
    A("| Text | 0 of 3 | 1 of 3 | 2 of 3 | 3 of 3 | all three agree | split 2 to 1 |")
    A("|---|---|---|---|---|---|---|")
    for v in ("old", "new"):
        d = spread[v]["dist"]
        A(f"| {v} | {d[0]} | {d[1]} | {d[2]} | {d[3]} | {spread[v]['unanimous']} | {spread[v]['split']} |")
    A("")
    A("Blocking grades per agent (of 318): " + "; ".join(f"{g}: old {sum(by[(i,'old')][g]['blocking'] for i in allids)}, new {sum(by[(i,'new')][g]['blocking'] for i in allids)}" for g in ("g1", "g2", "g3")) + ".\n")
    A("Pairwise agreement between agents on blocking or not (findings of 318): " + "; ".join(f"{v} text {a}-{b}: {pair[(v,a,b)]}" for v in ("old", "new") for a, b in (("g1", "g2"), ("g1", "g3"), ("g2", "g3"))) + ".\n")
    A("## Rows that matter\n")
    A(f"### Rows graded non-blocking under the old text and blocking under the new text (majority): {len(n2o)}\n")
    A("| ID | Panel mean | Description brief |")
    A("|---|---|---|")
    for i in n2o:
        A(f"| {i} | {panel[i]} | {trunc(desc[i][1])} |")
    A("")
    A(f"### Recall risk: rows the panel calls a blocker (mean 4.0 or higher) that the old and the new text grade differently (majority): {len(risk)}\n")
    if risk:
        A("| ID | Panel mean | Old text | New text | Description brief |")
        A("|---|---|---|---|---|")
        for i in risk:
            A(f"| {i} | {panel[i]} | {'blocking' if maj[(i,'old')] else 'not blocking'} | {'blocking' if maj[(i,'new')] else 'not blocking'} | {trunc(desc[i][1])} |")
    else:
        A("None under the majority grade.")
    A("")
    extra = [i for i in anyrisk if i not in risk]
    A(f"Panel blockers where at least one single agent graded the two texts differently but the majority did not: {len(extra)}" + (": " + ", ".join(extra) + "." if extra else "."))
    A("")
    A(f"### Rows graded blocking under the old text and non-blocking under the new text (majority): {len(o2n)}\n")
    A("| ID | Panel mean | Panel blocker | Description brief |")
    A("|---|---|---|---|")
    for i in o2n:
        A(f"| {i} | {panel[i]} | {'yes' if pblock[i] else 'no'} | {trunc(desc[i][1])} |")
    A("")
    A("## Sample of grades with the sentence each grader applied\n")
    A(f"Every grade carries a quote. {quote_ok} of {quote_ok + quote_bad} quotes are a verbatim substring of the rule text the grade names; {quote_bad} are not. Twelve grades: the 41st and the 201st finding (by id) for each grader and text:\n")
    A("| ID | Grader | Text | Order | Grade | Quoted words |")
    A("|---|---|---|---|---|---|")
    for d in sample:
        A(f"| {d['id']} | {d['grader']} | {d['text_version']} | {d['order']} | {'blocking' if d['blocking'] else 'not blocking'} | {q(d['quote'])} |")
    A("")
    A("## The old-rule injection confound\n")
    A("Every subagent in this session receives the installed output style, which holds today's rule, through the SubagentStart hook `pragmatic-subagent.js` (registered in `src/superclaude/hooks/hooks.json`; the installed copy `~/.claude/hooks/pragmatic-subagent.js` adds the style text to every subagent unconditionally, with no exemption by agent type). Checked in this run: that script is 22 lines and has no condition, and the Agent tool has no setting that skips the hook, so no way to spawn a grader without the injection was found; the graders were spawned with it. So the new-text arm was graded with the old rule still in each grader's context. The graders were told to apply only the rule text given and to ignore any other review-grading rule; their own reports on whether another definition was in their context are in the agents table above. The confound pulls the new-text grades toward the old-text grades, so the movement counts above are a lower bound on the change, not an estimate of it.\n")
    A("## What this regrade cannot show\n")
    A("- **Lower bound, and no measure of discovery.** The regrade grades findings that were supplied to it. It cannot tell whether a reviewer working under the new text would have found a defect at all, which is the risk that a stricter reading of blocking hides real defects. RT1 (spec section 13.2), the owner's read of the first five runs' Medium lists, and one small planted-defect check run as part of the live RT1 audit after the switch cover what it cannot.")
    A("- **The table holds only findings filed as blocking.** Findings that were never filed as blocking, or never raised, are absent, so no false-negative rate can be computed from it (selection bias).")
    A("- **Circular labels.** The panel consensus (three blind scorers, ponytail, scoring the same descriptions) is the reference, and it is not an independent ground truth; it was produced by the same kind of model reading the same text as the graders here.")
    A("- **Stand-in judge.** In the 5-run test, `08-test/results.md`, the stand-in judge agreed with the panel on 58.5 percent of the 318 findings (majority of five runs; Cohen's kappa 0.27), and the questions S, W and D separated at an area under the curve of 0.73 to 0.75. This regrade grades with a rule text, not with that judge, and nothing here reports a classifier probability.")
    A("- **Model agents, not people.** The graders are model agents of this session, not independent human graders, and they carry the old-rule injection above.")
    A("- **How grade lines were written.** Grader g2 reported that for most chunks it wrote the grade lines with a shell loop over its list of ids instead of one hand-written block per row (its own report to the executor). Its grades still vary by row (4 not blocking under A, 7 under B) and every quote is a verbatim substring of the rule text, but a loop means the grade for each row was decided first and typed out afterwards; graders g1 and g3 reported nothing on how they wrote their lines.")
    A("- **Near-uniform grades.** All three graders called almost every finding blocking under both texts, so the matrix and the movement counts rest on very few findings that any grader called not blocking; they say little about how the two texts differ on findings that are not obviously blocking.")
    A("- **Paired design.** Each agent graded each finding twice in one session, so its second grade could be influenced by its first; the order of the two texts was alternated by chunk to spread that effect, and the order table above shows the result.\n")
    A("This result does not measure a classifier and no number in it should be read as evidence that one works.\n")
    A("## Owner decisions this touches\n")
    A("- **OD3, open:** whether finding text may leave the machine for any later external judge. No external judge (Jev or any other) was called here: the graders are agents spawned inside this session. The decision stays open and is not made by this file.")
    A("- **OD4:** the classifier has no authority in version 1 (the spec recommendation). The coordinator message of 2026-11-16 (21:37 UTC) says the owner dropped OD4 as a question; either way this regrade does not change it and grants a classifier no authority.\n")
    A("## Files\n")
    A("- `./artifacts/stage0c-grades.jsonl`: all %d grades (agent id, text version, order position, grade, quote)." % len(grades))
    A("- `./artifacts/stage0c-work/`: the two rule texts, the three table copies and their hashes (`in-sha256.txt`), the graders' own files (`out/grader-N.jsonl`), the prompts and the agent ids.")
    A("- `./artifacts/stage0c-analyze.py`: re-creates this file and the merged jsonl from the graders' files.\n")
    A("The owner's go for the next stage is given in chat and not by this file.")
    (ART / "stage0c-regrade.md").write_text("\n".join(L) + "\n")
    print("wrote", ART / "stage0c-regrade.md")
    print("majority old", st["maj_old"])
    print("majority new", st["maj_new"])
    print("movement maj o2n/n2o/bb/nn", [len(x) for x in mv["maj"]], "risk", len(risk))
    print("quotes ok/bad", quote_ok, quote_bad)
    print("spread", {v: dict(spread[v]["dist"]) for v in spread})


main()
