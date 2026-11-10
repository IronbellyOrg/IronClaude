import pathlib
import sys

E2 = pathlib.Path(__file__).resolve().parents[1]
JEV = E2.parent / "jev"
for p in (str(E2), str(JEV)):
    if p not in sys.path:
        sys.path.insert(0, p)
