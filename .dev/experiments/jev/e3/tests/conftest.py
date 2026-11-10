import pathlib
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import e3lib  # noqa: E402,F401  (puts the jevlib / p15common root on sys.path)
