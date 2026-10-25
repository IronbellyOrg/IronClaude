"""Task-owned source for the exact inline native snapshot recipe in the bundled skill."""

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def under(path, root):
    return path == root or root in path.parents


def regular(path):
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("snapshot input must be an absolute, traversal-free path")
    if path.resolve(strict=True) != path or not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError("snapshot input must be a regular file with no symlink components")
    return path.read_bytes()


# Same verification-artifact floor as the input-tree guard; explicit inputs are
# never silently excluded. These exclusions affect scoped discovery only.
VERIFICATION_ARTIFACT_EXCLUDES = {
    "directories": ["__pycache__", ".pytest_cache", "htmlcov", ".mypy_cache", ".ruff_cache", "target", ".hypothesis"],
    "suffixes": [".pyc", ".pyo", ".pyd", ".egg-info"],
    "names": [".coverage", ".tsbuildinfo"],
    "prefixes": [".coverage."],
    "nested": ["node_modules/.cache"],
}


def discovery_metadata(selection):
    supplied = selection.get("discovery", {})
    scopes = supplied.get("scopes")
    if not isinstance(scopes, list) or not scopes or not all(isinstance(value, str) and value for value in scopes):
        raise ValueError("explicit audited discovery scopes required")
    for value in scopes:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or ".git" in path.parts:
            raise ValueError("discovery scopes must be repository-relative literal paths")
    return {"version": 1, "scopes": sorted(set(scopes)), "gitignore_policy": "exclude-standard",
            "verification_artifact_excludes": VERIFICATION_ARTIFACT_EXCLUDES}


def excluded(relative, metadata):
    parts = relative.parts
    rules = metadata["verification_artifact_excludes"]
    return (any(part in rules["directories"] or part.endswith(".egg-info") for part in parts)
            or relative.name.endswith(tuple(rules["suffixes"]))
            or relative.name in rules["names"]
            or relative.name.startswith(tuple(rules["prefixes"]))
            or any("/".join(parts[index:index + 2]) in rules["nested"] for index in range(len(parts) - 1)))


def discover(repo, output, selection_path, metadata):
    if metadata["verification_artifact_excludes"] != VERIFICATION_ARTIFACT_EXCLUDES:
        raise ValueError("discovery exclusion floor changed")
    command = ["git", "--literal-pathspecs", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", *metadata["scopes"]]
    result = subprocess.run(command, cwd=repo, capture_output=True, check=True, timeout=30)
    inventory = []
    for value in sorted(set(result.stdout.split(b"\0")) - {b""}):
        relative = Path(os.fsdecode(value))
        source = repo / relative
        if under(source, output) or source == selection_path or excluded(relative, metadata):
            continue
        if relative.is_absolute() or ".." in relative.parts or ".git" in relative.parts:
            raise ValueError("invalid discovered source path")
        kind = "missing" if not source.exists() and not source.is_symlink() else "regular" if stat.S_ISREG(source.lstat().st_mode) else "non-regular"
        inventory.append({"path": relative.as_posix(), "kind": kind})
    return inventory


def selected_items(selection, inventory, repo):
    items = list(selection["files"])
    supplied = {item["source"] for item in items}
    for row in inventory:
        source = str(repo / row["path"])
        if row["kind"] == "non-regular":
            raise ValueError("non-regular discovered audit input: " + source)
        if row["kind"] == "regular" and source not in supplied:
            items.append({"source": source, "kind": "audit-input"})
    return items


def verify(manifest_path):
    manifest = json.loads(regular(manifest_path))
    if manifest["status"] != "verified":
        raise ValueError("snapshot manifest was not verified")
    selection_path = Path(manifest["selection_path"])
    selection_bytes = regular(selection_path)
    if digest(selection_bytes) != manifest["selection_sha256"]:
        raise ValueError("selection file changed")
    selection = json.loads(selection_bytes)
    metadata = discovery_metadata(selection)
    if metadata != manifest["discovery_metadata"]:
        raise ValueError("discovery metadata changed")
    repo = Path(manifest["source_repo_root"])
    inventory = discover(repo, Path(manifest["output_root"]), selection_path, metadata)
    if inventory != manifest["scoped_inventory_after"]:
        raise ValueError("scoped audit membership changed")
    expected_sources = {item["source"] for item in selected_items(selection, inventory, repo)}
    actual_sources = [row["source_path"] for row in manifest["files"]]
    if len(actual_sources) != len(set(actual_sources)) or set(actual_sources) != expected_sources:
        raise ValueError("selected/copied membership mismatch")
    root = Path(manifest["reviewer_grounding_root"])
    if root.resolve(strict=True) != root:
        raise ValueError("snapshot root was retargeted")
    for row in manifest["files"]:
        snapshot = Path(row["snapshot_path"])
        if not under(snapshot, root):
            raise ValueError("manifest copy escapes snapshot root")
        if digest(regular(snapshot)) != row["sha256_copy"]:
            raise ValueError("snapshot copy changed: " + str(snapshot))
        if digest(regular(Path(row["source_path"]))) != row["sha256_after"]:
            raise ValueError("audited source changed: " + row["source_path"])
    return {"status": "verified", "reviewer_grounding_root": str(root), "files": len(manifest["files"])}


def provision(repo, output, selection_path):
    repo = repo.resolve(strict=True)
    output = output.resolve(strict=True)
    selection = json.loads(regular(selection_path))
    if selection.get("enumeration_complete") is not True or not selection.get("coverage_basis"):
        raise ValueError("explicit complete selected-input enumeration and coverage basis required")
    metadata = discovery_metadata(selection)
    before_inventory = discover(repo, output, selection_path, metadata)
    items = selected_items(selection, before_inventory, repo)
    if not items:
        raise ValueError("empty snapshot selection")
    # All protocol output/input/distribution guards MUST already have passed.
    destination = output / "reviewer-snapshot"
    destination.mkdir(exist_ok=False)
    root = destination / "root"
    root.mkdir()
    manifest_path = destination / "provenance-manifest.json"
    manifest = {"status": "pending", "snapshot_kind": "native-selected-inputs", "source_repo_root": str(repo),
                "reviewer_grounding_root": str(root), "selection_path": str(selection_path),
                "selection_sha256": digest(regular(selection_path)), "coverage_basis": selection["coverage_basis"],
                "enumeration_complete": True, "output_root": str(output),
                "discovery_metadata": metadata, "scoped_inventory_before": before_inventory, "files": []}
    try:
        payloads = []
        seen = set()
        for item in items:
            source = Path(item["source"])
            kind = item["kind"]
            if kind not in ("audit-input", "run-evidence") or under(source, destination):
                raise ValueError("invalid source kind or recursive snapshot source")
            if kind == "audit-input" and under(source, output):
                raise ValueError("explicit audited input overlaps output")
            if kind == "run-evidence":
                if not under(source, output):
                    raise ValueError("run-evidence must be produced within pinned output")
                relative = Path("__run_evidence__") / source.relative_to(output)
            elif under(source, repo):
                relative = source.relative_to(repo)
                if relative.parts[0] in ("__external__", "__run_evidence__"):
                    raise ValueError("reserved snapshot namespace collision")
            else:
                relative = Path("__external__") / digest(str(source).encode()) / source.name
            target = root / relative
            if target in seen:
                raise ValueError("duplicate selected path or snapshot collision")
            seen.add(target)
            content = regular(source)
            payloads.append((source, target, kind, content))
        for source, target, kind, content in payloads:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            target.chmod(0o444)
            copied = digest(regular(target))
            before = digest(content)
            after = digest(regular(source))
            manifest["files"].append({"kind": kind, "source_path": str(source), "snapshot_path": str(target),
                                      "sha256_before": before, "sha256_copy": copied, "sha256_after": after})
            if not before == copied == after:
                raise ValueError("source/copy hash mismatch: " + str(source))
        # Re-read EVERY source after ALL copies, not merely just after its own copy.
        for row in manifest["files"]:
            if digest(regular(Path(row["source_path"]))) != row["sha256_before"]:
                raise ValueError("input changed during snapshot: " + row["source_path"])
        after_inventory = discover(repo, output, selection_path, metadata)
        manifest["scoped_inventory_after"] = after_inventory
        if after_inventory != before_inventory or digest(regular(selection_path)) != manifest["selection_sha256"]:
            raise ValueError("selection or scoped audit membership changed during snapshot")
        manifest["status"] = "verified"
        for folder in sorted((path for path in root.rglob("*") if path.is_dir()), reverse=True):
            folder.chmod(0o555)
        root.chmod(0o555)
    except Exception as error:
        manifest["status"] = "failed"
        manifest["failure_reason"] = str(error)
        raise
    finally:
        # Preserve failed and successful snapshots/intermediates; NEVER teardown.
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return verify(manifest_path)


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--verify":
            result = verify(Path(sys.argv[2]))
        else:
            result = provision(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
        print(json.dumps(result))
    except Exception as error:
        print(json.dumps({"status": "failed", "reason": str(error)}))
        raise SystemExit(1)
