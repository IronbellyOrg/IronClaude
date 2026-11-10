import pathlib
import sys

E1 = pathlib.Path(__file__).resolve().parents[1]
if str(E1) not in sys.path:
    sys.path.insert(0, str(E1))
import _boot  # noqa: E402,F401
