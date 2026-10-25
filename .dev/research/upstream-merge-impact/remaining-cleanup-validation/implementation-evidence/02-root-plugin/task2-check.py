"""Check the exact approved Task 2 namespace repair, not reflection runtime."""

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from namespace_expected import TOKEN, expected

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
BAD_NAMESPACE = re.compile(r"/sc:(?:sc:)+")
LABEL = re.compile(r"UNAVAILABLE\(([A-Za-z][A-Za-z0-9-]*)\)")
AVAILABILITY = "**Availability fallback**"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).splitlines()


def main():
    contract = json.loads((OUT / "plugin-contract.json").read_text())
    frozen = json.loads((OUT / "expected-namespace-commands.json").read_text())
    references = json.loads((OUT / "namespace-scope-conflict.json").read_text())["references"]
    allowed = set(contract["allowed_command_edits"])
    frontends = {Path(row["path"]).stem.removeprefix("sc-"): row["frontend"] for row in contract["commands"]}
    available = {"/" + name for name in frontends.values()}
    unavailable = {(row["path"], row["name"]) for row in references}
    failures = []
    checks = {}

    def check(name, condition, details):
        checks[name] = {"pass": bool(condition), "details": details}
        if not condition:
            failures.append(name)

    check("exact_allowed_set", len(allowed) == 26 and set(frozen) == allowed, sorted(allowed))
    command_results = {}
    changed_references = Counter()
    unresolved = []
    actual_labels = Counter()
    availability_paths = []
    for path in sorted(allowed):
        original_bytes = (OUT / "isolation/plugin" / path).read_bytes()
        original = original_bytes.decode()
        actual_bytes = (ROOT / path).read_bytes()
        actual = actual_bytes.decode()
        regenerated = expected(path, original, frontends, unavailable)
        command_results[path] = {
            "baseline_hash_valid": sha(original_bytes) == contract["protected_sha256"][path],
            "expected_file_matches_helper": frozen[path] == regenerated,
            "actual_matches_expected_bytes": actual_bytes == frozen[path].encode(),
            "original_sha256": sha(original_bytes),
            "actual_sha256": sha(actual_bytes),
        }
        actual_labels.update((path, name) for name in LABEL.findall(actual))
        original_fallbacks = [line for line in original.splitlines() if AVAILABILITY in line]
        actual_fallbacks = [line for line in actual.splitlines() if AVAILABILITY in line]
        if original_fallbacks:
            availability_paths.append(path)
            check("availability:" + path, actual_fallbacks == [expected(path, line, frontends, unavailable) for line in original_fallbacks], len(actual_fallbacks))
        for line in original.splitlines(keepends=True):
            if path == "commands/sc-help.md" and line.startswith(("| `/sc:sc:estimate` |", "| `/sc:sc:select-tool` |")):
                continue
            for match in TOKEN.finditer(line):
                old = match.group(0)
                new = expected(path, old, frontends, unavailable)
                if new == old:
                    continue
                changed_references[new] += 1
                if new not in available and new != "/sc:sc-*" and not LABEL.fullmatch(new):
                    unresolved.append({"path": path, "old": old, "new": new})
    check("all_26_exact_transformations", all(row["baseline_hash_valid"] and row["expected_file_matches_helper"] and row["actual_matches_expected_bytes"] for row in command_results.values()), command_results)
    check("changed_references_resolve", not unresolved, {"unresolved": unresolved, "changed_tokens": dict(sorted(changed_references.items()))})
    expected_labels = Counter((row["path"], row["name"]) for row in references)
    check("exact_15_unavailable_labels", len(references) == 15 and actual_labels == expected_labels, {"count": sum(actual_labels.values()), "counts": {f"{path}:{name}": count for (path, name), count in sorted(actual_labels.items())}})
    check("nine_availability_passages", len(availability_paths) == 9, availability_paths)

    protected = {path: digest for path, digest in contract["protected_sha256"].items() if path not in allowed and path != ".claude-plugin/plugin.json"}
    changed_protected = [path for path, digest in protected.items() if not (ROOT / path).is_file() or sha((ROOT / path).read_bytes()) != digest]
    check("protected_hashes", not changed_protected, {"count": len(protected), "changed": changed_protected})
    original_manifest = (OUT / "isolation/plugin/.claude-plugin/plugin.json").read_bytes()
    manifest = (ROOT / ".claude-plugin/plugin.json").read_bytes()
    check("corrected_manifest_preserved", manifest == original_manifest.replace(b'  "homepage": "",\n', b"", 1) and sha(manifest) == contract["manifest_exception"]["corrected_sha256"], sha(manifest))
    command_paths = {str(path.relative_to(ROOT)) for path in (ROOT / "commands").rglob("*") if path.is_file() or path.is_symlink()}
    agent_paths = {str(path.relative_to(ROOT)) for path in (ROOT / "agents").rglob("*") if path.is_file() or path.is_symlink()}
    skill_paths = {str(path.relative_to(ROOT)) for path in (ROOT / "skills").rglob("*") if path.is_file() or path.is_symlink()}
    check("commands_agents_skills_inventory_preserved", command_paths == {row["path"] for row in contract["commands"]} and agent_paths == {row["path"] for row in contract["existing_agents"]} and skill_paths == {path for path in contract["protected_sha256"] if path.startswith("skills/")}, {"commands": len(command_paths), "agents": len(agent_paths), "skill_files": sorted(skill_paths)})
    malformed = [str(path.relative_to(ROOT)) for folder in ("commands", "agents") for path in (ROOT / folder).rglob("*.md") if BAD_NAMESPACE.search(path.read_text())]
    check("zero_malformed_namespaces_commands_agents", not malformed, malformed)
    retired = list(contract["producer_retirement"]) + ["commands/sc-estimate.md", "commands/sc-sc.md", "commands/sc-select-tool.md"]
    restored = [path for path in retired if (ROOT / path).exists() or (ROOT / path).is_symlink()]
    check("retired_producer_and_commands_absent", not restored, restored)
    help_text = (ROOT / "commands/sc-help.md").read_text()
    original_help = (OUT / "isolation/plugin/commands/sc-help.md").read_text()
    removed_rows = [line for line in original_help.splitlines() if line.startswith(("| `/sc:sc:estimate` |", "| `/sc:sc:select-tool` |"))]
    check("exact_two_retired_help_rows_removed", len(removed_rows) == 2 and not re.search(r"^\| `[^`]*(?:estimate|select-tool)` \|", help_text, re.MULTILINE) and len(original_help.splitlines()) - len(help_text.splitlines()) == 2, removed_rows)
    added_candidates = [row["destination"] for row in contract["candidate_resources"] if (ROOT / row["destination"]).exists() or (ROOT / row["destination"]).is_symlink()]
    check("no_task3_additions", not added_candidates, added_candidates)
    tracked_diff = set(git("diff", "--name-only", contract["baseline"]["head"]))
    check("exact_tracked_product_diff", tracked_diff == allowed | {".claude-plugin/plugin.json"}, sorted(tracked_diff))
    index_diff = git("diff", "--cached", "--name-only")
    check("index_unchanged", not index_diff, index_diff)
    check("branch_head_unchanged", git("branch", "--show-current") == [contract["baseline"]["branch"]] and git("rev-parse", "HEAD") == [contract["baseline"]["head"]], {"branch": git("branch", "--show-current"), "head": git("rev-parse", "HEAD")})
    record = {"task": 2, "verdict": "FAIL" if failures else "PASS", "checks": checks, "failed_checks": failures, "runtime_audit_proofs": "NOT RUN: Task 4 only"}
    (OUT / "task2-check-output.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"verdict": record["verdict"], "checks": len(checks), "exact_commands": len(command_results), "unavailable_labels": sum(actual_labels.values()), "availability_passages": len(availability_paths), "preserved_hashes": len(protected), "failed_checks": failures}, indent=2))
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
