"""Check the authorized ledger correction and digest coverage without editing live files."""
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

root, package, helper, manifest_path = map(Path, sys.argv[1:])
before = (package / "artifacts/progress-before-final-repairs.md").read_text().splitlines()
after = (package / "progress.md").read_text().splitlines()
expected = []
omitted = []
for line in before:
    match = re.search(r" (notes@[^\s]+)$", line) if " files=" in line else None
    if match:
        note = match.group(1)
        original = line[:match.start()]
        omitted.append(original.split(" files=", 1)[1].split(",")[-1])
        expected.append(original.replace(" evidence=", f" evidence={note},", 1))
    else:
        expected.append(line)
assert len(omitted) == 8
assert after[:len(expected)] == expected, "Unexpected ledger change beyond eight note relocations"
print("Ledger correction: exactly eight note relocations; prior verdicts, citations, Ruling and FINAL preserved")
manifest = json.loads(manifest_path.read_text())
files = manifest["files"]
assert all(" notes@" not in f and (root / f).is_file() for f in files)
assert set(omitted).issubset(files)
print(f"Manifest: {len(files)} actual delivery files, no absent annotated names")
spec = importlib.util.spec_from_file_location("archive_helper_probe", helper)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
plan_sha, source_sha = re.fullmatch(r"PLAN: sha256=(\w+) source_sha256=(\w+)", after[1]).groups()
assert module._digest(root, plan_sha, source_sha, files) == manifest["state"]
with tempfile.TemporaryDirectory(prefix="441-digest-probe-") as tmp:
    copy = Path(tmp)
    for rel in files:
        dest = copy / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, dest)
    baseline = module._digest(copy, plan_sha, source_sha, files)
    for rel in omitted:
        dest = copy / rel
        saved = dest.read_bytes()
        dest.write_bytes(saved + b"\n# digest sensitivity probe\n")
        assert module._digest(copy, plan_sha, source_sha, files) != baseline, rel
        dest.write_bytes(saved)
        assert module._digest(copy, plan_sha, source_sha, files) == baseline
        print("Byte-change detected: " + rel)
print("PASS: all eight formerly omitted files affect the digest; no live delivery bytes changed")
