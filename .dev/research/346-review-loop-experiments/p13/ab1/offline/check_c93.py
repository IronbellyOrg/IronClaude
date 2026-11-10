import sys, pathlib
sys.path.insert(0, "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1")
import c93
P11 = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p11/runs")
R = ".dev/orca-command-refactor/review"
for a in (2, 3):
    for r in range(1, 7):
        run = f"a{a}-r{r}"
        r1 = c93.blocking_tags(P11 / run / "ws" / R / "round1.md")
        au = c93.blocking_tags(P11 / run / "aud/ws" / R / "audit.md")
        print(run, "R1", r1, "| AUD", au)
