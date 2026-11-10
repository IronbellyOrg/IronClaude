import pathlib
import sys

JEV = pathlib.Path(__file__).resolve().parents[1]
if str(JEV) not in sys.path:
    sys.path.insert(0, str(JEV))
