"""Path bootstrap shared by the E1 scripts: puts the E1 dir, the shared adapter ($JEV) and the central score_themes copy on sys.path."""
import pathlib
import sys

E1 = pathlib.Path(__file__).resolve().parent
SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
JEV = SP / "p15/jev"
CENTRAL = SP / "central"
for _p in (E1, JEV, CENTRAL):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
