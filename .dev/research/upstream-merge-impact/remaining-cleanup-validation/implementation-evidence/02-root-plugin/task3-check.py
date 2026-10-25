#!/usr/bin/env python3
"""Check Task 3 source derivation, closure and preservation; optionally copy/probe inventory."""

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inherited_namespace_checks():
    """Execute every Task 2 exact check, changing ONLY Task 3 inventory allowance."""
    source = (OUT / "task2-check.py").read_text()
    substitutions = {
        'agent_paths == {row["path"] for row in contract["existing_agents"]}':
            'agent_paths == {row["path"] for row in contract["existing_agents"]} | {row["destination"] for row in contract["candidate_resources"] if row["destination"].startswith("agents/")}',
        'skill_paths == {path for path in contract["protected_sha256"] if path.startswith("skills/")}':
            'skill_paths == {path for path in contract["protected_sha256"] if path.startswith("skills/")} | {row["destination"] for row in contract["candidate_resources"] if row["destination"].startswith("skills/")}',
        'check("no_task3_additions", not added_candidates, added_candidates)':
            'check("exact_task3_additions", set(added_candidates) == {row["destination"] for row in contract["candidate_resources"]} and len(added_candidates) == 22, added_candidates)',
        '"task2-check-output.json"': '"task3-namespace-check-output.json"',
        'raise SystemExit(bool(failures))': 'return record',
    }
    for old, new in substitutions.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    namespace = {"__name__": "task3_inherited_namespace", "__file__": str(OUT / "task2-check.py")}
    exec(compile(source, str(OUT / "task2-check.py"), "exec"), namespace)
    return namespace["main"]()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-fixture")
    parser.add_argument("--inventory-label")
    parser.add_argument("--snapshot-proof")
    args = parser.parse_args()
    contract = json.loads((OUT / "plugin-contract.json").read_text())
    manifest = json.loads((OUT / "task3-adaptation-manifest.json").read_text())
    module = load("task3_adapt", OUT / "task3-adapt.py")
    checks = {}

    def check(name, condition, details):
        checks[name] = {"pass": bool(condition), "details": details}

    inherited = inherited_namespace_checks()
    check("all_task2_exact_checks_retained", inherited["verdict"] == "PASS", inherited["failed_checks"])
    destinations = {row["destination"] for row in contract["candidate_resources"]}
    check("exact_22_manifest_destinations", len(destinations) == 22 and destinations == {row["destination"] for row in manifest["resources"]}, sorted(destinations))
    source_checks = []
    for row in contract["candidate_resources"]:
        source, generated, edits = module.adapt(row)
        saved = next(item for item in manifest["resources"] if item["destination"] == row["destination"])
        actual = (ROOT / row["destination"]).read_bytes()
        source_checks.append({"path": row["destination"],
                              "pass": sha(source.encode()) == row["source_sha256"] == saved["source_sha256"]
                              and actual == generated.encode()
                              and sha(actual) == saved["destination_sha256"] and edits == saved["changes"]})
    check("source_derived_reproducible_bytes_and_manifest", all(item["pass"] for item in source_checks), source_checks)
    frontmatters = []
    for row in contract["candidate_resources"]:
        if not row["destination"].startswith("agents/"):
            continue
        old, _ = module.frontmatter((ROOT / row["source"]).read_text())
        actual, _ = module.frontmatter((ROOT / row["destination"]).read_text())
        protected_fields = ("name", "category", "tools", "model", "maxTurns", "permissionMode")
        fields = {key: re.findall(rf"^{key}:.*$", old, re.MULTILINE) == re.findall(rf"^{key}:.*$", actual, re.MULTILINE) for key in protected_fields}
        full_match = old == actual or (row["destination"] == "agents/confidence-calibrator.md" and re.sub(r"^description:.*$", "", old, flags=re.MULTILINE) == re.sub(r"^description:.*$", "", actual, flags=re.MULTILINE))
        frontmatters.append({"path": row["destination"], "fields": fields, "full_header_except_approved_description": full_match})
    check("agent_readonly_frontmatter_byte_equality", all(all(row["fields"].values()) and row["full_header_except_approved_description"] for row in frontmatters), frontmatters)
    known_agents = {row["frontend"] for row in contract["existing_agents"]} | {row["frontend"] for row in contract["candidate_resources"] if "frontend" in row}
    known_skills = {row["frontend"] for row in contract["skills"]}
    refs = []
    calls = []
    unresolved = []
    excluded_refs = {"refs/grader-extensions.md": "maintainer-only eval", "refs/cost-profile.yaml": "caller-only, not read by reflect", "refs/model-capability-tiers.md": "source Open Question proposes a future file, not a runtime read"}
    for path in sorted(destinations):
        text = (ROOT / path).read_text()
        if path.startswith("skills/"):
            skillroot = Path(*Path(path).parts[:2])
            for name in sorted(set(re.findall(r"\brefs/[A-Za-z0-9_.-]+\.(?:md|yaml)", text))):
                target = skillroot / name
                found = (ROOT / target).is_file()
                refs.append({"caller": path, "reference": name, "exists": found, "excluded": excluded_refs.get(name)})
                if not found and name not in excluded_refs:
                    unresolved.append({"caller": path, "ref": name})
        for token in re.findall(r"\bSkill\s+(sc:[A-Za-z0-9_:.-]+)|\bTask\((sc:[A-Za-z0-9_:.-]+)", text):
            skill, agent = token
            name = skill or agent
            # Source handoff docs are explicitly unavailable, never dispatched.
            unavailable = name == "sc:workflow-protocol" and "remediation" in path or name == "sc:workflow-protocol" and path.endswith("sc-reflect-protocol/SKILL.md")
            exists = name in (known_skills if skill else known_agents)
            calls.append({"caller": path, "kind": "skill" if skill else "agent", "frontend": name, "exists": exists, "unavailable_documentation": unavailable})
            if not exists and not unavailable:
                unresolved.append({"caller": path, "frontend": name})
    check("all_required_ref_and_qualified_call_edges_resolve", not unresolved, {"unresolved": unresolved, "refs": refs, "calls": calls})
    read_paths = []
    for path in destinations:
        text = (ROOT / path).read_text()
        for lookup in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/((?:skills|agents)/[A-Za-z0-9_./-]+\.md)", text):
            read_paths.append({"caller": path, "lookup": lookup, "exists": (ROOT / lookup).is_file()})
    check("all_concrete_plugin_root_lookups_exist", all(row["exists"] for row in read_paths), read_paths)
    reflect = (ROOT / "skills/sc-reflect-protocol/SKILL.md").read_text()
    adv = (ROOT / "skills/sc-adversarial-protocol/SKILL.md").read_text()
    checks_required = {
        "real_merge_disk_guards": (reflect, ("ORCHESTRATOR-VERIFIES-ON-DISK", "merged-verdict.yaml", "MALFORMED", "up to 2 additional times", "single-reviewer-fallback", "Reflect MUST NOT synthesize its own merge")),
        "input_output_guards": (reflect, ("output_input_overlap", "output_symlink_escape", "VERIFICATION_ARTIFACT_EXCLUDES", "input_drift", "before any write", "Distribution output guard", "nearest existing ancestor")),
        "real_debate_scoring_merge_preserved": (adv, ("steelman", "round_2_5_invariant_probe", "sufficiency_challenge", "quant_score", "qual_score", "position_bias_mitigation", "sc:merge-executor", "write this return contract on every invocation")),
        "independence_and_evidence_gates": (reflect, ("disjoint-set", "independent calibrator instance in parallel", "non-negotiable final gate", "All reviewers are spawned as the fixed read-only `sc:reflect-reviewer` agent-type")),
        "honest_optional_unavailable": (reflect, ("tech-research", "audit-validator", "task-builder", "sc-workflow-protocol", "UNAVAILABLE in this plugin-only distribution", "remediation_unavailable: true", "remediation_plan_path: null", "Do not invoke them", "No fake successful")),
        "package_prerequisite_not_bundled": (reflect, ("separately available `superclaude` executable", "does NOT bundle", "readiness request", "explicitly unavailable")),
    }
    for name, (text, tokens) in checks_required.items():
        missing = [token for token in tokens if token not in text]
        check(name, not missing, {"missing": missing})
    check("no_unsafe_skill_help_probe", "args='--help'" not in reflect and "native registered skills AND Read" in reflect, "local resource existence, no Skill execution")
    rubric_source = (ROOT / "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md").read_text()
    rubric = (ROOT / "skills/sc-reflect-protocol/refs/reflection-rubric.md").read_text()
    # Native-name mapping is allowed; every anchor/threshold remains source-identical.
    _, expected_rubric, _ = module.adapt(next(row for row in contract["candidate_resources"] if row["destination"].endswith("refs/reflection-rubric.md")))
    check("approved_rubric_categories_anchors_thresholds", rubric == expected_rubric and "{Authorized, Necessary, Drift, Regression}" in rubric and "{Aligned, Refinement" in rubric_source, "only native name mapping and two obsolete classification names changed")
    calibrator = (ROOT / "agents/confidence-calibrator.md").read_text()
    _, calibrator_body = module.frontmatter(calibrator)
    check("reflection_five_dimension_mean_no_active_old_gates", all(token in calibrator_body for token in ("/ 5", "C < 0.85", "0.90", "calibration_failed: true", "calibrated: null", "spot_check_unverifiable", "independent instance in parallel")) and not any(token in calibrator_body for token in ("min(arithmetic_mean(all_six)", "gate_M1:", "C1-C8", "refs/escalation-rubric.md")), "independent reflection-only scoring; null on missing/incompatible rubric")
    input_ref = (ROOT / "skills/sc-reflect-protocol/refs/input-resolution.md").read_text()
    input_contract_checks = []
    for text in (reflect, input_ref):
        input_contract_checks.append("None of `--spec`, `--tasklist`, `--diff`/`--commit-range`, or `--task-log` provided." in text
                                     and "with no `--diff`, no `--commit-range`, AND no `--task-log`" in text
                                     and "with no `--diff` AND no `--task-log`" not in text
                                     and "`--mode pre` with no `--spec`" in text
                                     and "Neither `--spec`, `--tasklist`, nor `--diff` provided." not in text)
    check("post_diff_or_log_and_real_missing_input_guards", all(input_contract_checks) and "Tasklist file. Recommended for UC-2, not required" in input_ref and "UC-2 requires this OR `--task-log`" in input_ref and "(always present in UC-2)" not in reflect, input_contract_checks)
    input_assertions = []
    cases = [("post", {"--diff"}, True), ("post", {"--commit-range"}, True), ("post", {"--task-log"}, True), ("post", {"--tasklist"}, False), ("post", {"--spec"}, False), ("post", set(), False), ("pre", {"--spec"}, True), ("pre", {"--task-log"}, False), ("pre", set(), False)]
    for label, text in (("skill", reflect), ("input-ref", input_ref)):
        post_guards = [line for line in text.splitlines() if "`--mode post` with no" in line]
        accepted_sets = [set(re.findall(r"`(--[a-z-]+)`", line)) - {"--mode"} for line in post_guards]
        for mode, flags, expected_result in cases:
            accepted = all(bool(flags & options) for options in accepted_sets) if mode == "post" else "--spec" in flags
            input_assertions.append({"source": label, "mode": mode, "flags": sorted(flags), "expected_accept": expected_result, "actual_accept": accepted, "pass": accepted == expected_result and bool(post_guards) and all(options == {"--diff", "--commit-range", "--task-log"} for options in accepted_sets)})
    check("all_post_hardguards_accept_range_and_refuse_missing_input", all(row["pass"] for row in input_assertions), input_assertions)
    artifacts = (ROOT / "skills/sc-adversarial-protocol/refs/artifact-templates.md").read_text()
    debate = (ROOT / "skills/sc-adversarial-protocol/refs/debate-protocol.md").read_text()
    scorer = (ROOT / "skills/sc-adversarial-protocol/refs/scoring-protocol.md").read_text()
    source_scorer = (ROOT / "src/superclaude/skills/sc-adversarial-protocol/refs/scoring-protocol.md").read_text()
    check("scoring_scaffolds_match_existing_30_criterion_algorithm", "/25" not in artifacts and "25-criterion" not in debate and "**<N>/30 = <score>**" in artifacts and all("Invariant & Edge Case Coverage" in text and "<1/5" in text for text in (artifacts, debate, scorer)) and "30-criterion" in debate and "25-criterion" not in adv and "Full 30-criterion qualitative rubric with CEV" in adv and "Same 30-criterion rubric with CEV (independent evaluation)" in adv and scorer == source_scorer, "sixth dimension, /30 denominator, forward/reverse count and floor agree; actual scorer unchanged")
    recipe = reflect.split("<!-- native-snapshot-recipe:start -->\n```python\n", 1)[1].split("\n```\n<!-- native-snapshot-recipe:end -->", 1)[0] + "\n"
    reviewer_spec = (ROOT / "skills/sc-reflect-protocol/refs/reviewer-spec.md").read_text()
    check("real_native_snapshot_recipe_and_frozen_brief_contract", recipe == (OUT / "task3-native-snapshot-recipe.py").read_text() and all(token in reflect for token in ("native-selected-inputs", "sha256_before", "sha256_copy", "sha256_after", "native_snapshot_drift", "untracked/new", "Never copy `.git`", "No teardown deletion")) and all(token in reviewer_spec for token in ("source_path -> snapshot_path", "Rewrite ALL reviewer-facing paths", "snapshot-mcp-unindexed", "not a fourth section", "not a live-root escape", "immediately before dispatch AND after")), "delivered executable recipe, path rewrite, no live-root MCP escape and retained evidence")
    if args.snapshot_proof:
        proof_path = OUT / args.snapshot_proof
        proof = json.loads(proof_path.read_text())
        check("actual_snapshot_recipe_proof", proof["verdict"] == "PASS" and len(proof["checks"]) == 16 and all(proof["checks"].get(name) is True for name in ("selection_file_tamper_rejected_separately", "out_of_scope_unrelated_file_does_not_invalidate", "pinned_output_reviewer_artifact_does_not_invalidate", "excluded_verification_cache_does_not_invalidate", "in_scope_new_untracked_file_rejected_with_prior_bytes_unchanged", "discovery_metadata_and_selection_hash_are_pinned")) and all(proof["checks"].values()) and proof["delivered_recipe_sha256"] == sha(recipe.encode()) and Path(proof["proof_root"]).parent == OUT and all(Path(proof["proof_root"]).joinpath(path).exists() for path in ("happy/reviewer-snapshot/provenance-manifest.json", "missing/reviewer-snapshot/provenance-manifest.json")), {"proof": str(proof_path), "checks": proof["checks"], "recipe_hash": proof["delivered_recipe_sha256"]})
    if args.prepare_fixture:
        fixture = OUT / args.prepare_fixture
        if fixture.exists() or fixture.parent != OUT:
            raise SystemExit("Fixture must be a FRESH immediate child of task evidence")
        for folder in (".claude-plugin", "commands", "agents", "skills"):
            shutil.copytree(ROOT / folder, fixture / "plugin" / folder)
        (fixture / "home").mkdir()
        (fixture / "config").mkdir()
        (fixture / "config/settings.json").write_text("{}\n")
        files = {str(path.relative_to(fixture / "plugin")): sha(path.read_bytes()) for path in (fixture / "plugin").rglob("*") if path.is_file()}
        fixture_record = {"fixture": str(fixture), "source": "current actual root four component directories", "files": files, "global_resources": False, "package_resources": False, "project_mirrors": False}
        (OUT / f"{args.prepare_fixture}-contents.json").write_text(json.dumps(fixture_record, indent=2) + "\n")
        check("fresh_fixture_actual_copy_hashes", all((ROOT / path).is_file() and sha((ROOT / path).read_bytes()) == digest for path, digest in files.items()) and not any(path.is_symlink() for path in (fixture / "plugin").rglob("*")), fixture_record)
    if args.inventory_label:
        init = json.loads((OUT / f"loader-{args.inventory_label}-init.json").read_text())
        probes = json.loads((OUT / f"loader-{args.inventory_label}-probes.json").read_text())
        wanted_agents = set(module.AGENTS.values())
        wanted_skills = set(module.SKILLS.values())
        env = probes["env"]
        fixture = Path(env["HOME"]).parent
        fixture_record = json.loads((OUT / f"{fixture.name}-contents.json").read_text())
        hashes_match = all(sha((fixture / "plugin" / path).read_bytes()) == digest == sha((ROOT / path).read_bytes()) for path, digest in fixture_record["files"].items())
        check("native_inventory_observed_all_resources_isolated", wanted_agents <= set(init["agents"]) and wanted_skills <= set(init["skills"]) and not init["mcp_servers"] and env["PATH"] == "/usr/bin:/bin" and Path(probes["cwd"]).parent == Path("/tmp") and all(row["returncode"] == 0 for row in probes["probes"].values()) and hashes_match and any(plugin["name"] == "sc" and plugin["path"] == str(fixture / "plugin") for plugin in init["plugins"]), {"wanted_agents": sorted(wanted_agents), "wanted_skills": sorted(wanted_skills), "probes": probes, "fixture_hashes_match_current": hashes_match})
    failed = [name for name, result in checks.items() if not result["pass"]]
    record = {"task": 3, "verdict": "FAIL" if failed else "PASS", "checks": checks, "failed_checks": failed, "runtime_audits": "NOT RUN: Task 4; native inventory is not an audit"}
    (OUT / "task3-static-check-output.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"verdict": record["verdict"], "checks": len(checks), "failed_checks": failed}, indent=2))
    raise SystemExit(bool(failed))


if __name__ == "__main__":
    main()
