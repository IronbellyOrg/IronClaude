#!/usr/bin/env python3
"""Run the lint over the corpus. usage: run_lint.py OUTDIR [--lint-py PATH]
Without --lint-py the CLI is used: uv run --project $CLONE superclaude review lint DOC --format json."""
import json, os, pathlib, subprocess, sys, importlib.util
AB = pathlib.Path(os.environ["AB"]); CLONE = os.environ["CLONE"]
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
lint_py = sys.argv[sys.argv.index("--lint-py") + 1] if "--lint-py" in sys.argv else None
mod = None
if lint_py:
    spec = importlib.util.spec_from_file_location("lint_pass", lint_py); mod = importlib.util.module_from_spec(spec)
    sys.modules["lint_pass"] = mod; spec.loader.exec_module(mod)
n = 0
for rec in json.load(open(AB/"offline/corpus.json")):
    p = rec["path"]
    if mod:
        res = mod.run_lint(pathlib.Path(p).read_bytes())
        text = mod.render_json(res)
    else:
        r = subprocess.run(["uv", "run", "--project", CLONE, "superclaude", "review", "lint", p, "--format", "json"], capture_output=True, text=True)
        assert r.returncode == 0, (p, r.stderr)
        text = r.stdout
    (out/f"{rec['sha256']}.json").write_text(text); n += 1
print("linted", n, "documents ->", out)
