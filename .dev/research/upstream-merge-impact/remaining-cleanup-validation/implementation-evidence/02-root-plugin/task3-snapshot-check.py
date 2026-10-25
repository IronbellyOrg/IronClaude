#!/usr/bin/env python3
"""Execute the DELIVERED inline snapshot recipe against dirty/new inputs and failure cases."""

import argparse
import hashlib
import json
import subprocess
import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-name", default="snapshot-proof-" + uuid.uuid4().hex[:8])
    args = parser.parse_args()
    run = OUT / args.run_name
    if run.parent != OUT or run.exists():
        raise SystemExit("Use a fresh immediate child directory; previous proofs are retained")
    run.mkdir()
    skill = (ROOT / "skills/sc-reflect-protocol/SKILL.md").read_text()
    code = skill.split("<!-- native-snapshot-recipe:start -->\n```python\n", 1)[1].split("\n```\n<!-- native-snapshot-recipe:end -->", 1)[0] + "\n"
    assert code == (OUT / "task3-native-snapshot-recipe.py").read_text()
    tracked = ROOT / "commands/sc-reflect.md"
    original_tracked = tracked.read_bytes()
    dirty = subprocess.check_output(["git", "diff", "--name-only", "--", str(tracked)], cwd=ROOT, text=True)
    assert "commands/sc-reflect.md" in dirty, "Proof requires an actual dirty tracked audit input"
    audited = run / "audited"
    audited.mkdir()
    fresh = audited / "new-input.txt"
    fresh.write_text("new untracked audit input\n")
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "--", str(fresh)], cwd=ROOT, text=True)
    assert fresh.name in untracked, "Proof requires an actual untracked audit input"
    checks = {}
    executions = []

    def invoke(*arguments):
        command = ["uv", "run", "--no-project", "python", "-", *map(str, arguments)]
        process = subprocess.run(command, input=code, cwd=ROOT, text=True, capture_output=True, timeout=60)
        executions.append({"command": command, "returncode": process.returncode,
                           "stdout": process.stdout, "stderr": process.stderr})
        return process

    happy = run / "happy"
    happy.mkdir()
    evidence = happy / "t1-card.txt"
    evidence.write_text("captured T1 evidence, not a user input\n")
    selection = run / "selected-inputs.json"
    selection.write_text(json.dumps({"enumeration_complete": True,
                                    "coverage_basis": "actual dirty tracked command, Git-observed new input and captured run evidence",
                                    "discovery": {"scopes": [str(audited.relative_to(ROOT)), str(happy.relative_to(ROOT))]},
                                    "files": [{"source": str(tracked), "kind": "audit-input"},
                                              {"source": str(fresh), "kind": "audit-input"},
                                              {"source": str(evidence), "kind": "run-evidence"}]}))
    first = invoke(ROOT, happy, selection)
    assert first.returncode == 0, first.stdout + first.stderr
    manifest_path = happy / "reviewer-snapshot/provenance-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    checks["actual_dirty_untracked_and_run_evidence_frozen"] = manifest["status"] == "verified" and len(manifest["files"]) == 3
    checks["real_distinct_readonly_root_and_equal_three_hashes"] = Path(manifest["reviewer_grounding_root"]) != ROOT and all(
        row["sha256_before"] == row["sha256_copy"] == row["sha256_after"]
        and Path(row["snapshot_path"]).read_bytes() == Path(row["source_path"]).read_bytes()
        and Path(row["snapshot_path"]).stat().st_mode & 0o222 == 0 for row in manifest["files"])
    checks["before_dispatch_verifier_passes"] = invoke("--verify", manifest_path).returncode == 0
    checks["stale_snapshot_reuse_rejected"] = invoke(ROOT, happy, selection).returncode != 0
    frozen_new = Path(next(row["snapshot_path"] for row in manifest["files"] if row["source_path"] == str(fresh)))
    original_new = fresh.read_bytes()
    fresh.write_bytes(original_new + b"changed AFTER freeze\n")
    changed = invoke("--verify", manifest_path)
    checks["source_drift_detected_without_changing_frozen_copy"] = changed.returncode != 0 and "audited source changed" in changed.stdout and frozen_new.read_bytes() == original_new
    # Restore only this task-owned fixture's content to isolate the copy-tamper case.
    fresh.read_bytes()
    fresh.write_bytes(original_new)
    frozen_new.read_bytes()
    frozen_new.chmod(0o644)
    frozen_new.write_bytes(b"tampered copy\n")
    tampered = invoke("--verify", manifest_path)
    checks["frozen_copy_tamper_detected"] = tampered.returncode != 0 and "snapshot copy changed" in tampered.stdout
    membership_output = run / "membership"
    membership_output.mkdir()
    member_evidence = membership_output / "t1-card.txt"
    member_evidence.write_text("captured membership-case evidence\n")
    membership_selection = run / "membership-selection.json"
    membership_selection.write_text(json.dumps({"enumeration_complete": True, "coverage_basis": "scoped membership regression",
                                               "discovery": {"scopes": [str(audited.relative_to(ROOT)), str(membership_output.relative_to(ROOT))]},
                                               "files": [{"source": str(tracked), "kind": "audit-input"}, {"source": str(fresh), "kind": "audit-input"}, {"source": str(member_evidence), "kind": "run-evidence"}]}))
    member_result = invoke(ROOT, membership_output, membership_selection)
    assert member_result.returncode == 0, member_result.stdout + member_result.stderr
    member_manifest = membership_output / "reviewer-snapshot/provenance-manifest.json"
    original_selection = membership_selection.read_bytes()
    membership_selection.write_bytes(original_selection + b"\n")
    selection_changed = invoke("--verify", member_manifest)
    checks["selection_file_tamper_rejected_separately"] = selection_changed.returncode != 0 and "selection file changed" in selection_changed.stdout
    membership_selection.read_bytes()
    membership_selection.write_bytes(original_selection)
    (run / "unrelated-out-of-scope.txt").write_text("unrelated work\n")
    checks["out_of_scope_unrelated_file_does_not_invalidate"] = invoke("--verify", member_manifest).returncode == 0
    (membership_output / "reviewer-result.txt").write_text("later reviewer output\n")
    checks["pinned_output_reviewer_artifact_does_not_invalidate"] = invoke("--verify", member_manifest).returncode == 0
    cache = audited / "__pycache__"
    cache.mkdir()
    (cache / "generated.pyc").write_bytes(b"verification cache")
    checks["excluded_verification_cache_does_not_invalidate"] = invoke("--verify", member_manifest).returncode == 0
    members_before = json.loads(member_manifest.read_text())["files"]
    prior_hashes = {row["source_path"]: hashlib.sha256(Path(row["source_path"]).read_bytes()).hexdigest() for row in members_before}
    new_member = audited / "new-handler.py"
    new_member.write_text("new in-scope production source\n")
    membership_changed = invoke("--verify", member_manifest)
    checks["in_scope_new_untracked_file_rejected_with_prior_bytes_unchanged"] = membership_changed.returncode != 0 and "scoped audit membership changed" in membership_changed.stdout and membership_selection.read_bytes() == original_selection and all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == value for path, value in prior_hashes.items())
    checks["discovery_metadata_and_selection_hash_are_pinned"] = all(key in json.loads(member_manifest.read_text()) for key in ("selection_sha256", "discovery_metadata", "scoped_inventory_before", "scoped_inventory_after", "output_root"))
    failed = run / "incomplete"
    failed.mkdir()
    incomplete = run / "incomplete-selection.json"
    incomplete.write_text(json.dumps({"enumeration_complete": False, "files": []}))
    checks["incomplete_selection_refused"] = invoke(ROOT, failed, incomplete).returncode != 0
    missing = run / "missing"
    missing.mkdir()
    missing_selection = run / "missing-selection.json"
    missing_selection.write_text(json.dumps({"enumeration_complete": True, "coverage_basis": "negative missing input", "discovery": {"scopes": [str(audited.relative_to(ROOT))]}, "files": [{"source": str(run / "absent.txt"), "kind": "audit-input"}]}))
    failure = invoke(ROOT, missing, missing_selection)
    failed_manifest = missing / "reviewer-snapshot/provenance-manifest.json"
    checks["missing_input_retains_failed_manifest_no_live_fallback"] = failure.returncode != 0 and json.loads(failed_manifest.read_text())["status"] == "failed"
    checks["audited_tracked_input_never_mutated"] = tracked.read_bytes() == original_tracked
    checks["all_snapshots_retained"] = manifest_path.exists() and failed_manifest.exists() and frozen_new.exists()
    result = {"verdict": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
              "proof_root": str(run), "delivered_recipe_sha256": hashlib.sha256(code.encode()).hexdigest(),
              "executions": executions, "runtime_audits": "NOT RUN: snapshot recipe proof only, Task 4 remains unverified"}
    (run / "snapshot-check-output.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verdict": result["verdict"], "checks": len(checks), "output": str(run / "snapshot-check-output.json")}, indent=2))
    raise SystemExit(not all(checks.values()))


if __name__ == "__main__":
    main()
