"""Finish real cwd-fix smoke first, then run the current-body matrix and strict checker."""
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

OUT = Path(__file__).resolve().parent
RUNTIME = "task4-runtime-cwd-fix1"
CASES = ["post-tier2", "post-default", "pre-default", "post-tier1", "legacy-pre", "legacy-post", "post-log-only", "missing-pre", "missing-post", "unsafe-output", "remediation-unavailable", "readiness-unavailable", "invalid-commit-range"]
smoke = OUT / RUNTIME / "runs/pre-smoke-attempt-1/execution.json"
started = time.monotonic()
while True:
    try:
        state = json.loads(smoke.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        state = {"state": "not-started"}
    if state["state"] in ("exited", "timeout"):
        break
    if time.monotonic() - started > 2500:
        raise SystemExit("Cwd-fix smoke did not terminate; matrix not launched")
    time.sleep(1)
if state["state"] != "exited" or state["returncode"] != 0:
    raise SystemExit("Cwd-fix smoke native failure; matrix not launched")
check = ["uv", "run", "--no-sync", "python", str(OUT / "task4-check.py"), "--runtime", RUNTIME]
if subprocess.run(check + ["--case", "pre-smoke-attempt-1"]).returncode:
    raise SystemExit("Cwd-fix smoke semantic/guard failure; matrix not launched")
record = {"runtime": RUNTIME, "state": "running", "cases": {}}


def persist():
    (OUT / "task4-fix1-native-matrix.json").write_text(json.dumps(record, indent=2) + "\n")


def run_case(name):
    negative = name in {"missing-pre", "missing-post", "unsafe-output", "readiness-unavailable", "invalid-commit-range"}
    command = ["uv", "run", "--no-project", "python", str(OUT / "task4-runtime.py"), "--runtime", RUNTIME, "--case", name, "--timeout", "900" if negative else "6000", "--persist-session"]
    result = subprocess.run(command, capture_output=True, text=True)
    return name, {"command": command, "native_harness_exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


persist()
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(run_case, name) for name in CASES]
    for future in as_completed(futures):
        name, result = future.result()
        record["cases"][name] = result
        persist()
        print(name, "native harness exit", result["native_harness_exit"], flush=True)
full = check + ["--require-all", "--case", "pre-smoke-attempt-1"]
for name in CASES:
    full.extend(["--case", name + "-attempt-1"])
result = subprocess.run(full)
record["checker_command"] = full
record["checker_exit"] = result.returncode
record["state"] = "complete" if result.returncode == 0 else "failed"
persist()
raise SystemExit(result.returncode)
