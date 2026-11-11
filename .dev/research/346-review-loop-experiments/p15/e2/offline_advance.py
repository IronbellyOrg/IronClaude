"""E2 offline worker driver wrapper (contract J9).  Prints LAUNCH <abs prompt path> model=<m>, RUNNING n, MANUAL ..., ALL DONE."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "jev"))
from p15common.offline_driver import advance   # noqa: E402

if __name__ == "__main__":
    sys.exit(advance(HERE / "offline" / "workers.json", r"p15/e2/offline", 6))
