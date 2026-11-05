#!/usr/bin/env bash
# Probe for C3: does `uv lock` execute an in-tree PEP 517 backend named by the merged
# pyproject.toml (backend-path = ["."]) when [project] has a dynamic field?
# Scratch project only, throwaway cache, offline; the "backend" only writes a marker file.
set -u
S=$(mktemp -d /tmp/lock-probe.XXXXXX)
trap 'rm -rf "$S"' EXIT
mkdir -p "$S/p"
cd "$S/p" || exit 1
cat > pyproject.toml <<'EOF'
[project]
name = "probe"
dynamic = ["version"]
requires-python = ">=3.10"

[build-system]
requires = []
build-backend = "evilbackend"
backend-path = ["."]
EOF
cat > evilbackend.py <<'EOF'
import os
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BACKEND_RAN"), "w").write("imported\n")
def prepare_metadata_for_build_wheel(md, config_settings=None):
    d = os.path.join(md, "probe-0.0.1.dist-info"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "METADATA"), "w").write("Metadata-Version: 2.1\nName: probe\nVersion: 0.0.1\n")
    return "probe-0.0.1.dist-info"
def get_requires_for_build_wheel(config_settings=None): return []
def build_wheel(*a, **k): raise RuntimeError("not needed")
EOF
echo "== uv lock --offline on a project with backend-path=[\".\"] and dynamic version"
UV_CACHE_DIR="$S/cache" uv lock --offline >"$S/out" 2>&1; rc=$?
echo "exit=$rc"
tail -3 "$S/out"
if [ -f BACKEND_RAN ]; then echo "in-tree backend executed: yes"; else echo "in-tree backend executed: no"; fi
