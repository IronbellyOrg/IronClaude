"""Build clean shadow re-runs of the 6 contaminated VF steps. Originals untouched; copies go to runs/<run>/vfN-clean with PROMPT.md inside."""
import re, shutil, pathlib
R = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs")
JOBS = [("b1-r3","VF1"),("b1-r4","VF1"),("b1-r6","VF1"),("b1-r6","VF2"),("b1h-r3","VF1"),("b1h-r4","VF3")]
HEAD = re.compile(r"^### [MN]\d+$")
for run, step in JOBS:
    sub = "vf" + step[2]
    src = R/run/f"PROMPT-{step}.md"
    lines = src.read_text().splitlines()
    out, skip, removed = [], False, []
    for ln in lines:
        if ln.startswith("=== ") and "FOLLOW-UP" not in ln or ln.startswith("=== FOLLOW-UP"):
            skip = True
        if skip and (HEAD.match(ln) or ln.startswith("Write your full reply")):
            skip = False
        if skip or ln.startswith("Reviser brief note:"):
            removed.append(ln); continue
        if run == "b1h-r4" and step == "VF3" and re.match(r"\s*- (\(a\)|\(b\)|Option|Origin:|Verification status)|\s+- \((a|b)\)", ln):
            removed.append(ln); continue
        out.append(ln)
    text = "\n".join(out) + "\n"
    old = f"/runs/{run}/{sub}"; new = f"/runs/{run}/{sub}-clean"
    text = re.sub(re.escape(old) + r"(?![\w-])", new, text)
    dst = R/run/f"{sub}-clean"
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(R/run/sub, dst, symlinks=True)
    # remove the original verify output copy so the shadow starts clean
    for p in dst.rglob("verify-*.md"): p.unlink()
    (dst/"PROMPT.md").write_text(text)
    print(run, step, "removed", len(removed), "lines; kept", len(out), "->", dst/"PROMPT.md")
