"""Render the four verbatim reviewer briefs for a replay by swapping ONLY machine paths.

usage: uv run --no-project python -I render_briefs.py <briefs-dir> <replay-root> <evidence-root> <out-dir>
  replay-root    checkout that holds .dev/tasks/to-do/<id> (your replay worktree)
  evidence-root  folder where you unpacked inputs/evidence (worker-sessions, executor-asof-R<k>, protocol)
Substitutions (nothing else is touched; every other byte of the brief stays as logged):
  original checkout path                         -> <replay-root>
  ~/.claude/projects/...p0-live-<name>           -> <evidence-root>/worker-sessions/<name>
  ~/.claude/projects/...OrcaCLICommandRefactor-Specs/aaee1ebf-....jsonl (and its folder)
                                                 -> <evidence-root>/executor-asof-R<k>/aaee1ebf-....jsonl
  ~/.claude/skills/sc-implement-protocol/refs/qa.md -> <evidence-root>/protocol-as-loaded/qa.md
  /tmp/ironclaude-p0live/                        -> <out-dir>/state/   (you write stateK.json there)
"""
import re
import sys
from pathlib import Path

briefs, root, ev, out = (Path(a) for a in sys.argv[1:5])
ORIG = "/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs"
PROJ = "/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-"
SESS = "aaee1ebf-4ec9-494f-85e0-52f3697170b5"
FILES = {1: "R1-reviewer-brief-L1988-final-prompt.md", 2: "R2-reviewer-brief-L2142-final-prompt-2.md",
         3: "R3-reviewer-brief-L2335-final-prompt-3.md", 4: "R4-reviewer-brief-L2487-final-prompt-4.md"}
out.mkdir(parents=True, exist_ok=True)
(out / "state").mkdir(exist_ok=True)
for k, name in FILES.items():
    t = (briefs / name).read_text(encoding="utf-8")
    t = t.replace(ORIG, str(root))
    t = re.sub(re.escape(PROJ) + r"p0-live-(\{troubleshoot,workflow,adversarial\}|troubleshoot|workflow|adversarial)",
               lambda m: f"{ev}/worker-sessions/" + ("{troubleshoot,workflow,adversarial}" if m.group(1).startswith("{") else m.group(1)), t)
    t = t.replace(PROJ + "OrcaCLICommandRefactor-Specs/" + SESS, f"{ev}/executor-asof-R{k}/{SESS}")
    t = t.replace("/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md", f"{ev}/protocol-as-loaded/qa.md")
    t = t.replace("/tmp/ironclaude-p0live/", f"{out}/state/")
    (out / f"R{k}-brief.md").write_text(t, encoding="utf-8")
    sp = (briefs / f"R{k}-spawn-prompt-L{ {1: 2001, 2: 2157, 3: 2342, 4: 2499}[k] }.txt").read_text(encoding="utf-8")
    sp = sp.replace("/tmp/ironclaude-p0live/", f"{out}/").replace("final-prompt", f"R{k}-brief").replace("-2.md", ".md").replace("-3.md", ".md").replace("-4.md", ".md")
    (out / f"R{k}-spawn-prompt.txt").write_text(sp, encoding="utf-8")
    # RECONSTRUCTED variant: the original reviewers 1 to 3 found the executor session by listing the project folder of the
    # checkout path (agent logs: round 2 L258, round 3 L130). In a replay that folder holds the replay session, so point at the
    # as-of copy. Round 4's brief already names it; the variant is still written for symmetry.
    ptr = (f" Added by the replay driver (not in the original): the executor session log for this package is "
           f"{ev}/executor-asof-R{k}/{SESS}.jsonl and its subagent logs are in the folder of the same name next to it; "
           f"judge the executor's own behaviour from that log, not from any other session.")
    (out / f"R{k}-spawn-prompt+pointer.txt").write_text(sp.rstrip("\n") + ptr + "\n", encoding="utf-8")
    print(f"R{k}: wrote {out / f'R{k}-brief.md'}")
