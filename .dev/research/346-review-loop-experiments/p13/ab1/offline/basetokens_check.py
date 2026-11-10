import sys, glob, pathlib
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1")
import analysis as A
SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
G = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
loops, auds = [], []
for r in range(1, 7):
    run = f"a3-r{r}"
    steps = {}
    for st in ("R1", "V1", "R2", "V2", "R3", "AUD"):
        p = SP / "p11/runs" / run / f"PROMPT-{st}.md"
        if p.exists():
            s = A.step_tokens(p, G, "sonnet")
            steps[st] = s["out"] if s else None
    loop = sum(v or 0 for k, v in steps.items() if k != "AUD")
    print(run, steps, "loop", loop)
    loops.append(loop); auds.append(steps.get("AUD") or 0)
print("mean loop", sum(loops) / 6, "mean AUD", sum(auds) / 6, "B", (sum(loops) + sum(auds)) / 6)
