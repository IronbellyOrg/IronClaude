#!/usr/bin/env python3
"""Isolated reproduction of the sprint phase-boundary SIGSEGV.

Drives the EXACT unsafe pattern from src/superclaude/cli/pipeline/process.py:190
  popen_kwargs["preexec_fn"] = os.setpgrp
from a parent process carrying the same thread topology the runner has at a
phase boundary:
  - Rich Live auto-refresh thread          (tui.py:101  Live(refresh_per_second=2))
  - a malloc-churning monitor daemon       (monitor.py:280 OutputMonitor thread)
  - concurrent-fork "summarizer" daemons   (summarizer.py:596 + subprocess.run @339)
  - main thread spawning the next phase     (executor.py:1815 ClaudeProcess.start)

MODE=unsafe   -> preexec_fn=os.setpgrp           (the current code path)
MODE=fixed    -> start_new_session=True          (the proposed fix)

faulthandler is enabled so a SIGSEGV prints the faulting thread's Python stack,
and a dump_traceback_later watchdog catches a fork deadlock (the other failure
mode of the same bug). Either outcome confirms the pattern is unsafe.
"""
from __future__ import annotations

import faulthandler
import os
import shutil
import subprocess
import sys
import threading
import time

faulthandler.enable(all_threads=True)
# Backstop: if the process deadlocks in a fork child, dump every thread and die.
faulthandler.dump_traceback_later(150, exit=True)

MODE = os.environ.get("MODE", "unsafe")
ITERS = int(os.environ.get("ITERS", "20000"))
TRUE_BIN = shutil.which("true") or "/bin/true"

stop = threading.Event()
progress = {"spawns": 0, "summarizer_forks": 0}


def monitor_thread():
    """Mimic OutputMonitor: poll + heavy malloc churn to contend the glibc arena lock."""
    buf = []
    while not stop.is_set():
        # allocate/free to keep the malloc arena lock hot at fork time
        buf = [bytearray(4096) for _ in range(256)]
        del buf
        time.sleep(0)  # yield


def summarizer_thread():
    """Mimic SummaryWorker daemon: concurrent fork via subprocess.run (no preexec)."""
    while not stop.is_set():
        try:
            subprocess.run([TRUE_BIN], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, check=False)
            progress["summarizer_forks"] += 1
        except Exception:
            pass


def spawn_next_phase(i: int):
    """Mimic ClaudeProcess.start(): the main-thread fork carrying the unsafe flag."""
    kwargs = dict(stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                  stderr=subprocess.DEVNULL)
    if MODE == "unsafe":
        if hasattr(os, "setpgrp"):
            kwargs["preexec_fn"] = os.setpgrp          # <-- process.py:190
    else:
        kwargs["start_new_session"] = True             # <-- proposed fix
    p = subprocess.Popen([TRUE_BIN], **kwargs)
    try:
        p.stdin.close()
    except Exception:
        pass
    p.wait()


def main() -> int:
    print(f"[repro] MODE={MODE} ITERS={ITERS} pid={os.getpid()} true={TRUE_BIN}",
          flush=True)
    # Rich Live auto-refresh background thread, exactly like tui.py
    try:
        from rich.console import Console
        from rich.live import Live
        from rich.table import Table

        console = Console()

        def render():
            t = Table()
            t.add_column("phase"); t.add_column("status")
            t.add_row(str(progress["spawns"]), "RUNNING")
            return t

        live = Live(render(), console=console, refresh_per_second=2, screen=False)
        live.start()
    except Exception as exc:  # pragma: no cover
        print(f"[repro] Rich Live unavailable ({exc}); continuing without it", flush=True)
        live = None

    threads = [threading.Thread(target=monitor_thread, daemon=True)]
    for _ in range(3):  # a small pool of concurrent-fork summarizer daemons
        threads.append(threading.Thread(target=summarizer_thread, daemon=True))
    for th in threads:
        th.start()

    t0 = time.time()
    try:
        for i in range(ITERS):
            spawn_next_phase(i)
            progress["spawns"] = i + 1
            if live is not None and (i % 200 == 0):
                try:
                    live.update(render())
                except Exception:
                    pass
            if i % 1000 == 0:
                print(f"[repro] boundary spawn {i}/{ITERS} "
                      f"(summarizer_forks={progress['summarizer_forks']}) "
                      f"elapsed={time.time()-t0:.1f}s", flush=True)
    finally:
        stop.set()
        if live is not None:
            try:
                live.stop()
            except Exception:
                pass

    print(f"[repro] SURVIVED {ITERS} boundary spawns in {time.time()-t0:.1f}s "
          f"with MODE={MODE} — no SIGSEGV/deadlock observed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
