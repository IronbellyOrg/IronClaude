import sys
sys.path.insert(0,"/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab3")
import score_themes as s
P11="/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs"
for a in ("a2","a3"):
    for r in range(1,7):
        for nm,rel in (("R1","ws/.dev/orca-command-refactor/review/"+("spec-panel.md" if False else "round1.md")),("AUD","aud/ws/.dev/orca-command-refactor/review/audit.md")):
            p=f"{P11}/{a}-r{r}/{rel}"
            fs=s.blocking_findings(p)
            print(a,r,nm,[(f["id"],f["theme"],len(f["cited"]),(f["heading"] or "NOSEC")[:50]) for f in fs] or s.verdict_of(open(p).read()))
