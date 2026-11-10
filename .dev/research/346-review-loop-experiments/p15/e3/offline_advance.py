#!/usr/bin/env python3
"""offline_advance.py  Offline worker driver (contract J9): prints LAUNCH <abs prompt> model=<m>, RUNNING n, MANUAL ..., ALL DONE.
At most 6 workers at once (env AB_MAX may lower it).  No token or cost check exists in this file (D6)."""
import sys

import e3lib
from p15common.offline_driver import advance

if __name__ == "__main__":
    sys.exit(advance(e3lib.WORKERS, r"p15/e3/offline", e3lib.decision()["launch"]["max_concurrent"]))
