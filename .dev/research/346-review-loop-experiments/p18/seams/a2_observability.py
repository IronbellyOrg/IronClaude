#!/usr/bin/env python3
"""A2 acceptance-check observability seam (ab6).  Code first, Jev second, flag-only output.

Stages
  1. extract the check rows of a spec: 7.1 / 7.3 table rows (AC-n) and the 7.2 live-check steps;
  2. code stage on every row (all deterministic, none uses a model):
       LINT   widened reqlint (REF + PATH + PHASE) findings whose line sits on the row;
       D20    additive-edit grep pitfall  grep -E '^-[^-]'  (misses a deleted '- bullet' and '---', which diff as '-- bullet', '----');
       D21    table-escaped pipe  \\|  inside a code span (copied raw the alternation/pipe is literal and the gate passes vacuously);
       EXEC   the shell / grep / YAML commands of the row are RUN in a scratch directory (never in the repo): a plain run against a clean
              fixture, a mutation probe (plant a violation, see whether the check finds it, raw copy versus unescaped), and the YAML snippet
              against a valid contract and against a markdown report;
  3. only rows that raised no code flag go to Jev, question `observability`
       {can_pass, cannot_pass, cannot_discriminate, insufficient};
  4. output = at most 8 lint-style UNVERIFIED lines (flag only: no severity, no finding, no closure).  LINT flags stay in lint-N.md (they are
     already there through the free widening F1), so they are not repeated as A2 lines.

Any Jev error, refusal, invalid answer or `insufficient` produces NO line for that row (the ab5 path).
Conventional control: `control_items` exports the identical packets (no Jev) for a same-packet Sonnet judge; `apply_answers` ingests it.
CLI:  a2_observability.py SPEC.md [--out DIR] [--mock MODE]        (code stage only without --mock; live calls only through replay.py)
"""
import argparse
import json
import pathlib
import re
import shlex
import shutil
import subprocess
import sys

import seamlib as S

QSET_VERSION = "a2-q1"
QNAME = "observability"
MAX_LINES = 8
EXEC_TIMEOUT_S = 10

OBS_OPTIONS = {
    "can_pass": "An implementer who follows the check exactly as written, on an implementation that meets the spec, can run it, observe the stated "
                "pass condition, and a wrong or empty result would not satisfy it.",
    "cannot_pass": "Following the check exactly as written, the pass condition cannot be met or observed: the command, file, field, flag or state "
                   "it needs does not exist at that point, or the check contradicts a cited row or the code-stage facts.",
    "cannot_discriminate": "The check can be run and its pass condition met, but it would also be met by a wrong, empty or unrelated result, so a pass "
                           "proves nothing about the thing it claims to test.",
    "insufficient": "The state does not contain what is needed to decide between the other options.",
}
OBS_INSTRUCTIONS = (
    "Read `check` (one acceptance or live-check row of a requirements spec), the cited rows in `cited`, and the facts a program already established "
    "in `code_stage`. Decide whether the check, executed exactly as written, can show its pass condition for a correct implementation and fail for "
    "an incorrect one. Judge only the check against the text in the state; do not assume files or behaviour that the state does not mention."
)


def obs_question():
    return S.choice(OBS_INSTRUCTIONS, OBS_OPTIONS)


# ----------------------------------------------------------------------------- 1. extraction
_ID_RE = re.compile(r"\b(WC-\d+|SA-\d+|AC-C\d|AC-\d\.\d|D[1-5])\b")
_STEP_REF_RE = re.compile(r"\bstep\s+(\d+)\b", re.I)


def _is_code_line(doc, ln):
    return doc.code[ln - 1]


def extract_rows(text: str):
    """-> (rows, defs).  rows: [{id, kind, phase, line, check, pass, raw, commands}], defs: {id: text} of every row/requirement cited by id."""
    doc = S.parse_spec(text)
    rows, defs = [], {}
    # requirement definitions (for the cited rows): WC / SA / D rows of any table whose first cell is such an id
    for t in doc.tables:
        for ln, cells in t.rows:
            if cells and re.fullmatch(r"(WC|SA)-\d+", S.strip_md(cells[0]).strip()):
                defs[S.strip_md(cells[0]).strip()] = S.clip(S.plain(cells[1] if len(cells) > 1 else ""), 600)
    for t in S.find_tables(doc, "check", "pass"):
        phase_col = t.header[0].strip().lower() == "phase"
        for ln, cells in t.rows:
            if (phase_col and len(cells) < 4) or (not phase_col and len(cells) < 3):
                continue
            if phase_col:
                phase, rid, check, passc = cells[0], cells[1], cells[2], cells[3]
            else:
                phase, rid, check, passc = "C", cells[0], cells[1], cells[2]
            rid = S.strip_md(rid).strip()
            rows.append({"id": rid, "kind": "table", "phase": S.strip_md(phase).strip(), "line": ln, "check": check, "pass": passc,
                         "raw": doc.lines[ln - 1]})
            defs[rid] = S.clip(S.plain(check) + " => " + S.plain(passc), 700)
    h = S.heading_line(doc, r"live worker check")
    if h:
        a, b = S.section_range(doc, h)
        for ln in range(a + 1, b + 1):
            if _is_code_line(doc, ln):
                continue
            m = re.match(r"^\s*(\d+)\.\s+(.*)$", doc.lines[ln - 1])
            if not m:
                continue
            body = m.group(2)
            if "**Pass:**" in body:
                chk, pas = body.split("**Pass:**", 1)
            else:
                chk, pas = body, ""
            rid = f"7.2#{m.group(1)}"
            rows.append({"id": rid, "kind": "step", "phase": "7.2", "line": ln, "check": chk.strip(), "pass": pas.strip(), "raw": doc.lines[ln - 1]})
            defs[rid] = S.clip(S.plain(chk) + " => " + S.plain(pas), 700)
    for r in rows:
        r["commands"] = [c for c in code_spans(r["check"]) if looks_like_command(c)]
    return rows, defs


def code_spans(cell: str):
    return [m.strip() for m in re.findall(r"`([^`\n]+)`", cell)]


_CMD_HEADS = ("grep", "git", "test", "cmp", "make", "uv", "sha256sum", "gh", "ORCA", "orca", "orca-ide", "claude", "diff", "cat", "ls", "wc")


def looks_like_command(span: str) -> bool:
    w = span.split(None, 1)[0] if span.split() else ""
    return w in _CMD_HEADS


def cited_rows(row, defs, limit=4):
    """Rows/requirements the check cites by id (WC-n, SA-n, AC-n, step n of 7.2, 'section 7.2'), excluding the row itself."""
    text = S.strip_md(row["check"]) + " " + S.strip_md(row["pass"])
    out, seen = [], {row["id"]}
    for m in _ID_RE.finditer(text):
        i = m.group(1)
        if i in defs and i not in seen:
            seen.add(i)
            out.append({"id": i, "text": defs[i]})
    if "7.2" in text or row["kind"] == "table":
        for m in _STEP_REF_RE.finditer(text):
            i = f"7.2#{m.group(1)}"
            if i in defs and i not in seen and row["kind"] == "table" and ("7.2" in text):
                seen.add(i)
                out.append({"id": i, "text": defs[i]})
    return out[:limit]


# ----------------------------------------------------------------------------- 2. code stage
RE_D20 = re.compile(r"""grep\s+(?:-\S+\s+)*['"]\^-\[\^-\]['"]""")
RE_D21 = re.compile(r"\\\|")


def d20(row) -> dict | None:
    for c in row["commands"]:
        if RE_D20.search(c):
            return {"check": "D20", "msg": "the additive-edit grep '^-[^-]' does not match a deleted '- bullet' or '---' line (a diff shows them as '-- bullet' and '----'), so deletions pass as additive"}
    return None


def d21(row) -> dict | None:
    for span in code_spans(row["raw"]):
        if RE_D21.search(span):
            return {"check": "D21", "msg": "the command is written with a table-escaped pipe (backslash-pipe): copied as written, the escaped alternation or pipe is literal, so the check may pass vacuously"}
    return None


def lint_flags(text: str, rows):
    """Widened lint (REF+PATH+PHASE) -> (all findings, {row line: [finding]})."""
    res = S.reqlint.run_lint_text(text, ("REF", "PATH", "PHASE"))
    by_row = {}
    for f in res["findings"]:
        for r in rows:
            if f["lines"][0] <= r["line"] <= f["lines"][1] or any(o and o[0] <= r["line"] <= o[1] for o in [f.get("other_lines")]):
                by_row.setdefault(r["line"], []).append(f)
    return res["findings"], by_row


# ---- tiny ERE sampler (literals, \b, [[:space:]], [...], groups with alternation, ? + *) used for the mutation probe
def sample_ere(p: str, limit=8):
    def parse_alt(i, close):
        alts, cur = [], [[""]]
        while i < len(p):
            ch = p[i]
            if ch == close:
                break
            if ch == "|":
                alts.append(cur)
                cur = [[""]]
                i += 1
                continue
            atom, i = parse_atom(i)
            q = p[i] if i < len(p) else ""
            if q in "?*":
                atom = atom + [""] if "" not in atom else atom
                i += 1
            elif q == "+":
                i += 1
            cur.append(atom)
        alts.append(cur)
        outs = []
        for seq in alts:
            acc = [""]
            for atom in seq:
                acc = [a + b for a in acc for b in atom][:limit]
            outs += acc
        return outs[:limit], i

    def parse_atom(i):
        ch = p[i]
        if ch == "(":
            sub, j = parse_alt(i + 1, ")")
            return sub, j + 1
        if ch == "[":
            j = p.index("]", i + 2 if p[i + 1:i + 3] == "[:" else i + 1)
            if p[i:].startswith("[[:space:]]"):
                return [" "], i + len("[[:space:]]")
            body = p[i + 1:j]
            return [body.lstrip("^")[:1] if not body.startswith("^") else "x"], j + 1
        if ch == "\\":
            nxt = p[i + 1] if i + 1 < len(p) else ""
            if nxt == "b":
                return [""], i + 2
            return [nxt], i + 2
        if ch == ".":
            return ["x"], i + 1
        if ch in "^$":
            return [""], i + 1
        return [ch], i + 1
    try:
        outs, _ = parse_alt(0, "\0")
        return [o for o in outs if o][:limit]
    except Exception:
        return []


_PLACEHOLDER = re.compile(r"<[A-Za-z][\w .:/-]*>")
_ALLOWED_HEADS = {"grep", "test", "cmp", "git"}
_ALLOWED_GIT = {"diff", "status", "log"}
_FORBIDDEN = re.compile(r"[;&`$><]|\|\||\bsudo\b|\brm\b|\bcurl\b|\bwget\b")


def _stages(cmd: str):
    """Split a command into pipeline stages on unquoted '|' (None when it does not tokenise)."""
    try:
        toks = shlex.split(cmd, posix=True)
    except ValueError:
        return None
    stages, cur = [], []
    for t in toks:
        if t == "|":
            stages.append(cur)
            cur = []
        else:
            cur.append(t)
    stages.append(cur)
    return stages


def _grep_pattern(stage):
    args = stage[1:]
    for i, a in enumerate(args):
        if a in ("-e", "--regexp") and i + 1 < len(args):
            return args[i + 1]
        if not a.startswith("-"):
            return a
    return None


def make_fixture(root: pathlib.Path):
    for d in ("src/superclaude/commands", "src/superclaude/skills/ccsession-tag", "src/superclaude/agents", "src/superclaude/core",
              "plugins/superclaude/skills/sc-recommend/refs", "tests/skills", ".dev"):
        (root / d).mkdir(parents=True, exist_ok=True)
    (root / "src/superclaude/core/HOW-WE-WORK.md").write_text("routing\n")
    (root / "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md").write_text("routing\n")
    env = _env(root)
    for c in (["git", "init", "-q", "-b", "master", "--template="], ["git", "add", "-A"], ["git", "commit", "-q", "-m", "fixture", "--allow-empty"]):
        subprocess.run(c, cwd=root, env=env, capture_output=True, timeout=EXEC_TIMEOUT_S)


def _env(root):
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(root), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
            "GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@example.invalid", "GIT_COMMITTER_NAME": "f", "GIT_COMMITTER_EMAIL": "f@example.invalid",
            "LC_ALL": "C"}


def _run(cmd: str, root: pathlib.Path, stdin: str | None = None):
    p = subprocess.run(["bash", "-c", cmd], cwd=root, env=_env(root), input=stdin, capture_output=True, text=True, timeout=EXEC_TIMEOUT_S)
    return p.returncode, p.stdout


def _unquoted(cmd: str) -> str:
    """The command with single-quoted segments blanked (a `$` or `>` inside single quotes is a literal); double quotes still expand, so they stay."""
    return re.sub(r"'[^']*'", "''", cmd)


def _executable(cmd: str):
    """(ok, reason).  Only pure text/git-read pipelines without placeholders are run."""
    if _PLACEHOLDER.search(_unquoted(cmd)):
        return False, "placeholder in command"
    if _FORBIDDEN.search(_unquoted(cmd)):
        return False, "shell construct not allowed"
    st = _stages(cmd)
    if not st or not all(s for s in st):
        return False, "does not tokenise"
    for s in st:
        if s[0] not in _ALLOWED_HEADS:
            return False, f"command `{s[0]}` is not run offline"
        if s[0] == "test" and len(s) < 3:
            return False, "incomplete command (no operand)"
        if s[0] == "git" and (len(s) < 2 or s[1] not in _ALLOWED_GIT):
            return False, "git subcommand is not read-only"
    return True, ""


def expectation(pass_cell: str):
    p = S.strip_md(pass_cell).lower()
    if "prints nothing" in p:
        return "empty"
    if re.search(r"\bexits?\s+0\b", p):
        return "exit0"
    return None


def exec_row(row, root: pathlib.Path) -> list:
    """Run the row's commands in `root` (a scratch dir).  -> list of {cmd, executed, exit, stdout_empty, verdict, flag, msg}."""
    out = []
    exp = expectation(row["pass"])
    for cmd in row["commands"]:
        res = {"cmd": S.clip(cmd, 200), "executed": False, "flag": False, "verdict": "", "msg": ""}
        # YAML snippet: run against a valid contract and a markdown report
        if cmd.startswith("uv run python -c") or cmd.startswith("python -c"):
            res.update(exec_yaml(cmd, row, root))
            out.append(res)
            continue
        ok, why = _executable(cmd)
        if not ok:
            res["verdict"] = f"not executed: {why}"
            out.append(res)
            continue
        try:
            code, so = _run(cmd, root)
        except subprocess.TimeoutExpired:
            res["verdict"] = "not executed: timeout"
            out.append(res)
            continue
        res.update({"executed": True, "exit": code, "stdout_empty": so.strip() == ""})
        res["verdict"] = f"clean fixture: exit {code}, stdout {'empty' if so.strip() == '' else 'non-empty'}"
        if exp == "exit0" and code != 0:
            res["flag"] = True
            res["msg"] = f"run on a clean scratch fixture it exits {code}, but the pass condition says it exits 0"
        out.append(res)
        # mutation probes for 'prints nothing' greps
        if exp == "empty" and cmd.split()[0] in ("grep", "git"):
            out.extend(mutation_probes(row, cmd, root))
    return out


def _first_grep_E(st):
    for s_ in st:
        if s_[0] == "grep" and any(a.startswith("-") and not a.startswith("--") and "E" in a for a in s_[1:]):
            return s_
    return None


def mutation_probes(row, cmd, root):
    """Plant a violation and see whether the check finds it.  D20: a deleted '- bullet' / '---' stream through an additive-edit grep.
    D21: the same command as written in the table source (backslash-pipes) versus unescaped, against a planted violation."""
    res = []
    st = _stages(cmd)
    if not st:
        return res
    for s_ in st:
        if s_[0] == "grep" and _grep_pattern(s_) == "^-[^-]":
            code, so = _run(f"printf '%s\\n' '-- bullet' '----' | {shlex.join(s_)}", root)
            miss = so.strip() == ""
            res.append({"cmd": "probe: deleted bullet / rule line", "executed": True, "exit": code, "flag": miss,
                        "verdict": "probe " + ("not caught" if miss else "caught"),
                        "msg": "a deleted '- bullet' and a deleted '---' (diff lines '-- bullet' and '----') are not matched by the additive-edit grep" if miss else ""})
    raw_span = next((sp for sp in code_spans(row["raw"]) if RE_D21.search(sp) and sp.split()[0] == cmd.split()[0]), None)
    if raw_span is None:
        return res
    g = _first_grep_E(st)
    if st[0][0] == "git" and "--cached" in st[0]:
        g1 = next((s_ for s_ in st[1:] if s_[0] == "grep"), None)
        samples = sample_ere(_grep_pattern(g1) or "") if g1 else []
        if not samples:
            return res
        name = samples[0].rstrip("/") + "/probe.md" if samples[0].endswith("/") else samples[0] + "probe.md"
        pth = root / name
        pth.parent.mkdir(parents=True, exist_ok=True)
        pth.write_text("x\n")
        _run(f"git add -f -- {shlex.quote(name)}", root)
    elif g is not None:
        samples = sample_ere(_grep_pattern(g) or "")
        if not samples:
            return res
        d = next((a for a in st[0][1:] if not a.startswith("-") and a != _grep_pattern(st[0]) and (root / a).is_dir()), None)
        if d is None:
            return res
        (root / d / "probe.md").write_text("\n".join(samples) + "\n")
    else:
        return res
    c_un, o_un = _run(cmd, root)
    c_raw, o_raw = _run(raw_span, root)
    if not o_un.strip():
        res.append({"cmd": "probe: planted violation", "executed": True, "exit": c_un, "flag": False, "verdict": "probe unavailable: the unescaped command did not see the planted violation"})
        return res
    vac = o_un.strip() != o_raw.strip()
    res.append({"cmd": "probe: planted violation, command as written in the table source", "executed": True, "exit": c_raw, "flag": vac,
                "verdict": f"unescaped command prints {len(o_un.splitlines())} line(s), the source text copied raw prints {len(o_raw.splitlines())}",
                "msg": (f"against a planted violation the unescaped command prints {len(o_un.splitlines())} line(s) but the command copied raw from the table "
                        f"source prints {len(o_raw.splitlines())}: the copied gate does not behave like the intended one") if vac else ""})
    return res


_YAML_PY = []


def yaml_python():
    """First interpreter with PyYAML among sys.executable, python3, /usr/bin/python3 (the spec's own check needs it); None when there is none."""
    if not _YAML_PY:
        for c in (sys.executable, "python3", "/usr/bin/python3"):
            try:
                if subprocess.run([c, "-c", "import yaml"], capture_output=True, timeout=EXEC_TIMEOUT_S).returncode == 0:
                    _YAML_PY.append(c)
                    break
            except (OSError, subprocess.TimeoutExpired):
                continue
        else:
            _YAML_PY.append(None)
    return _YAML_PY[0]


def exec_yaml(cmd: str, row, root: pathlib.Path) -> dict:
    m = re.search(r'-c\s+"((?:[^"\\]|\\.)*)"', cmd) or re.search(r"-c\s+'([^']*)'", cmd)
    if not m or "yaml" not in m.group(1) or "import" not in m.group(1):
        return {"verdict": "not executed: python snippet is not a YAML check"}
    body = m.group(1)
    if "superclaude" in body:
        return {"verdict": "not executed: needs the package"}
    py = yaml_python()
    if py is None:
        return {"verdict": "not executed: PyYAML is not available to any interpreter here"}
    ok_y = root / "contract.yaml"
    ok_y.write_text("status: succeeded\ncommand: /sc:analyze x --unattended\nreport_path: r.md\nartifacts: []\n")
    md = root / "REPORT.md"
    md.write_text("# Report\n\n## Findings\n- item one\n- item two\n\nstatus: draft\n")
    def go(f):
        try:
            p = subprocess.run([py, "-c", body, str(f)], cwd=root, env=_env(root), capture_output=True, text=True, timeout=EXEC_TIMEOUT_S)
            return p.returncode, (p.stderr.strip().splitlines() or [""])[-1][:120]
        except subprocess.TimeoutExpired:
            return None, "timeout"
    c_ok, _ = go(ok_y)
    c_md, e_md = go(md)
    res = {"executed": True, "exit": c_ok, "verdict": f"valid contract: exit {c_ok}; markdown report: exit {c_md}"}
    text = S.strip_md(row["check"] + " " + row["pass"]).lower()
    on_md = bool(re.search(r"existing report file|report\.md|markdown|\.md\b", text))
    if c_ok == 0 and c_md not in (0, None) and on_md:
        res["flag"] = True
        res["msg"] = "the YAML assertion exits non-zero on a markdown report file, but the row applies it to the command's existing (markdown) report"
    elif c_ok not in (0, None):
        res["verdict"] += " (snippet failed on a valid contract: environment, not flagged)"
    return res


_STEP_MD_RE = re.compile(r"step\s+(\d+)\b([^.;]{0,90}?)(existing report file|REPORT\.md|markdown report|\.md\b)", re.I)
_STEP_NEG_RE = re.compile(r"\b(instead|replaced?|skips?|skipped|only checks?|test -s|non-empty|is not run|not applied|not run)\b", re.I)


def cross_row_yaml(row, rows, root):
    """A row (e.g. AC-0.4) that says live-check step N uses the command's existing (markdown) report file: run step N's YAML snippet on a markdown report."""
    text = S.strip_md(row["check"] + " " + row["pass"])
    for m in _STEP_MD_RE.finditer(text):
        if _STEP_NEG_RE.search(m.group(0)):
            continue
        step = next((r for r in rows if r["id"] == f"7.2#{m.group(1)}"), None)
        if step is None:
            continue
        for cmd in step["commands"]:
            if cmd.startswith(("uv run python -c", "python -c")):
                r = exec_yaml(cmd, dict(step, check=step["check"] + " existing report file", pass_=step["pass"], **{"pass": step["pass"]}), root)
                if r.get("flag"):
                    return {"source": "exec", "check": "EXEC",
                            "msg": f"live-check step {m.group(1)} runs a YAML assertion, which exits non-zero on a markdown report file, yet this row applies it to the command's existing (markdown) report"}
    return None


def code_stage(row, text_lint_by_row, root: pathlib.Path, rows=None) -> dict:
    flags = []
    for f in text_lint_by_row.get(row["line"], []):
        flags.append({"source": "lint", "check": f["check"], "msg": f"lint {f['lint_id']}: " + S.clip(f["message"], 220)})
    for fn in (d20, d21):
        f = fn(row)
        if f:
            flags.append({"source": "regex", "check": f["check"], "msg": f["msg"]})
    sub = root / re.sub(r"[^A-Za-z0-9]+", "_", row["id"])        # a fresh fixture per row: no cross-row contamination
    make_fixture(sub)
    exec_res = exec_row(row, sub)
    for e in exec_res:
        if e.get("flag"):
            flags.append({"source": "exec", "check": "EXEC", "msg": e["msg"]})
    if rows:
        cf = cross_row_yaml(row, rows, sub)
        if cf:
            flags.append(cf)
    shutil.rmtree(sub, ignore_errors=True)                       # the verdicts are in the result; the per-row fixture (a git repo) is not kept
    return {"flags": flags, "exec": exec_res}


def code_summary(cs) -> dict:
    """The facts for the Jev state (flags are absent by construction: a flagged row never reaches Jev)."""
    runs = [e for e in cs["exec"]]
    if not runs:
        ex = "the row has no shell command to run"
    else:
        ex = "; ".join(S.clip(f"{e['cmd']}: {e['verdict']}", 160) for e in runs[:3])
    return {"lint_widened_ref_path_phase": "no finding on this row", "pitfall_regexes_d20_d21": "no match", "scratch_execution": ex}


# ----------------------------------------------------------------------------- 3. Jev items / control
def build_items(text: str, scratch: pathlib.Path, sid: str = "spec"):
    """-> (rows, analysis, items).  analysis[i] = {row, code_flags, exec, to_jev}; items = Jev packets for rows that raised no code flag."""
    rows, defs = extract_rows(text)
    lint_all, by_row = lint_flags(text, rows)
    root = pathlib.Path(scratch)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    analysis, items = [], []
    for r in rows:
        cs = code_stage(r, by_row, root, rows)
        to_jev = not cs["flags"]
        analysis.append({"id": r["id"], "line": r["line"], "kind": r["kind"], "phase": r["phase"], "code_flags": cs["flags"],
                         "exec": cs["exec"], "to_jev": to_jev})
        if to_jev:
            state = {"check": {"id": r["id"], "phase": r["phase"], "text": S.scrub(S.clip(S.plain(r["check"]), 900)),
                               "pass_condition": S.scrub(S.clip(S.plain(r["pass"]), 600))},
                     "cited": [{"id": c["id"], "text": S.scrub(c["text"])} for c in cited_rows(r, defs)],
                     "code_stage": code_summary(cs)}
            items.append(S.question_item(f"{sid}:a2:{r['id']}", QSET_VERSION, state, QNAME, obs_question(), row_id=r["id"], row_line=r["line"]))
    return rows, analysis, items, lint_all


def make_lines(analysis, outcomes, cap=MAX_LINES) -> list:
    """UNVERIFIED lines (flag only), one per check row.  Order: execution / pitfall flags, then Jev cannot_pass, then Jev cannot_discriminate;
    at most `cap`.  Lint flags are not repeated (they are in lint-N.md already).  A row with no usable Jev answer produces nothing."""
    cand = []
    by_id = {o["id"].split(":a2:", 1)[1]: o for o in outcomes if o.get("usable")}
    for a in analysis:
        code = [f for f in a["code_flags"] if f["source"] != "lint"]
        if code:
            tags = sorted({f["check"] for f in code})
            msgs = []
            for f in code:
                if f["msg"] not in msgs:
                    msgs.append(f["msg"])
            rank = 0 if any(f["source"] == "exec" for f in code) else 1
            cand.append((rank, a["line"], a["id"], "code:" + "+".join(tags), "; ".join(msgs[:2])))
            continue
        o = by_id.get(a["id"])
        if not o:
            continue
        if o["choice"] == "cannot_pass":
            cand.append((2, a["line"], a["id"], "jev:cannot_pass", "a judgment model read this check, the rows it cites and the code-stage facts and answered that it cannot show its pass condition as written"))
        elif o["choice"] == "cannot_discriminate":
            cand.append((3, a["line"], a["id"], "jev:cannot_discriminate", "a judgment model answered that this check would also pass for a wrong or empty result"))
    cand.sort()
    return [f"UNVERIFIED A2-{n} [{rid}, spec line {ln}] ({src}) {msg}. Verify against the spec text; this is not a finding."
            for n, (_, ln, rid, src, msg) in enumerate(cand[:cap], 1)]


def control_items(items) -> list:
    """The identical packets for the conventional same-packet judge: {id, state, question, options}.  No Jev involved."""
    return [{"id": it["id"], "state": it["state"], "question": it["questions"][QNAME]["instructions"], "options": it["questions"][QNAME]["criteria"]}
            for it in items]


def apply_answers(items, answers: dict) -> list:
    """Ingest a judge's answers {packet id: option} as outcomes shaped like Jev outcomes (usable unless insufficient / unknown option)."""
    outs = []
    for it in items:
        c = answers.get(it["id"])
        ok = c in it["questions"][QNAME]["criteria"]
        outs.append({"id": it["id"], "status": "ok" if ok else "invalid", "choice": c if ok else None, "usable": bool(ok and c != "insufficient"),
                     "fallback": None if ok and c != "insufficient" else "insufficient" if ok else "invalid"})
    return outs


def run_spec(text, sid, scratch, runner=None):
    rows, analysis, items, lint_all = build_items(text, scratch, sid)
    outs = [runner.ask(it) for it in items] if runner else []
    return {"sid": sid, "rows": len(rows), "analysis": analysis, "items": items, "outcomes": outs, "lint_all": [
        {"id": f["lint_id"], "lines": f["lines"], "check": f["check"]} for f in lint_all], "lines": make_lines(analysis, outs)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("--out", default=str(S.SEAMS / "out" / "a2-cli"))
    ap.add_argument("--mock", choices=["ok", "insufficient", "malformed", "timeout", "http500", "mixed"], help="ask the mock transport (never Jev)")
    ap.add_argument("--control", action="store_true", help="write the conventional-control packets (no Jev)")
    a = ap.parse_args(argv)
    text = pathlib.Path(a.spec).read_text(encoding="utf-8")
    out = pathlib.Path(a.out)
    runner = None
    if a.mock:
        with S.mock_env():
            runner = S.Runner(seam="a2", mode="mock", out_dir=out, mock_mode=a.mock)
            res = run_spec(text, "cli", out / "scratch", runner)
    else:
        res = run_spec(text, "cli", out / "scratch")
    print(f"rows {res['rows']}  to_jev {sum(1 for x in res['analysis'] if x['to_jev'])}  code-flagged {sum(1 for x in res['analysis'] if x['code_flags'])}")
    for ln in res["lines"]:
        print(ln)
    if a.control:
        S.write_json(out / "control-packets.json", control_items(res["items"]))
        print(f"control packets: {out / 'control-packets.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
