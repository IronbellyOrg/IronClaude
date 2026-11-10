import pathlib
import sys

C = pathlib.Path(__file__).resolve().parents[1]
if str(C) not in sys.path:
    sys.path.insert(0, str(C))
