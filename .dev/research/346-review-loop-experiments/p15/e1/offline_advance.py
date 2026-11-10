"""Offline worker driver wrapper (contract J9): prints LAUNCH / RUNNING / MANUAL / ALL DONE for offline/workers.json."""
import _boot
import os
import sys

from p15common.offline_driver import advance

if __name__ == "__main__":
    sys.exit(advance(_boot.E1 / "offline/workers.json", r"p15/e1/offline", int(os.environ.get("AB_MAX", "6"))))
