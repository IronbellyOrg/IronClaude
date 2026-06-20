#!/usr/bin/env python3
"""Additively wire Phase-2 assertions into each case 4-11 eval_metadata.json.

Reads `assertions_cases_4_11_acceptance` from `evals.json` and translates the
abstract assertion names into concrete grader-format assertion objects per case,
appending them to the existing `assertions` array. Original assertions are
preserved (additive — never removed) so before/after comparison remains fair.

Usage: uv run python wire-phase2-assertions.py
"""
import json
from pathlib import Path

ROOT = Path("/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2")
EVAL_WS = ROOT / ".dev/eval-workspaces/sc-brainstorm"
EVALS_JSON = EVAL_WS / "evals/evals.json"
ITER2 = EVAL_WS / "iterations/iteration-2"

# Acceptance scope: cases 4-11 (case 12 deferred)
ACCEPTANCE_CASES = [4, 5, 6, 7, 8, 9, 10, 11]


def build_phase2_assertions(case: dict) -> list:
    """Build the list of new Phase-2 assertion objects for a single case.

    These are ADDITIVE — they are appended to the existing `assertions` array,
    never replacing it. Both live runs and the iteration-2 baseline are scored
    against the combined set so before/after deltas measure remediation effect
    on the new contract.
    """
    case_id = case["id"]
    name = case["name"]
    expected = case.get("expected", {})
    handoff = expected.get("handoff", "none")
    expected_domain = expected.get("domain")
    expected_proposal_count = expected.get("proposal_count")
    expected_depth = case.get("expected_depth")
    expected_blind_mode = case.get("expected_blind_mode", False)
    expected_interactive_mode = case.get("expected_interactive_mode", False)

    new_assertions = []
    seed = "with_skill/outputs/seed-brief.md"
    merged = "with_skill/outputs/merged-requirements.md"
    contract = "with_skill/outputs/return-contract.yaml"
    debate = "with_skill/outputs/adversarial/debate-transcript.md"

    # --- Phase-2 seed-brief mandatory sections (4 unconditional + 2 conditional) ---
    new_assertions.append({
        "text": "[Phase-2] seed-brief has ## Intent Summary section",
        "type": "section_present",
        "target": seed,
        "section_pattern": "Intent Summary",
    })
    new_assertions.append({
        "text": "[Phase-2] seed-brief has ## Context Anchors section",
        "type": "section_present",
        "target": seed,
        "section_pattern": "Context Anchors",
    })
    new_assertions.append({
        "text": "[Phase-2] seed-brief has ## Must Preserve section",
        "type": "section_present",
        "target": seed,
        "section_pattern": "Must Preserve",
    })
    new_assertions.append({
        "text": "[Phase-2] seed-brief has ## Out of Scope section",
        "type": "section_present",
        "target": seed,
        "section_pattern": "Out of Scope",
    })

    # Conditional: interactive_mode_when_expected (only when case explicitly expects it)
    if expected_interactive_mode:
        new_assertions.append({
            "text": "[Phase-2] seed-brief frontmatter declares interactive_mode: true (case expects interactive)",
            "type": "frontmatter_field",
            "target": seed,
            "field": "interactive_mode",
            "expected": "true",
        })

    # Conditional: blind_mode_when_expected
    if expected_blind_mode:
        new_assertions.append({
            "text": "[Phase-2] seed-brief frontmatter declares blind_mode: true (case expects blind)",
            "type": "frontmatter_field",
            "target": seed,
            "field": "blind_mode",
            "expected": "true",
        })

    # --- Phase-2 merged-requirements ---
    new_assertions.append({
        "text": "[Phase-2] merged-requirements has dedicated ## Provenance section",
        "type": "section_present",
        "target": merged,
        "section_pattern": "Provenance",
    })
    new_assertions.append({
        "text": "[Phase-2] merged-requirements has ## Functional Requirements section",
        "type": "section_present",
        "target": merged,
        "section_pattern": "Functional Requirements",
    })
    new_assertions.append({
        "text": "[Phase-2] merged-requirements has ## Non-Functional Requirements section",
        "type": "section_present",
        "target": merged,
        "section_pattern": "Non-Functional Requirements",
    })
    new_assertions.append({
        "text": "[Phase-2] merged-requirements has Risks section with at least 1 item (table rows OR bullets)",
        "type": "section_items_or_table_rows",
        "target": merged,
        "section_pattern": "Risks",
        "min_items": 1,
    })
    new_assertions.append({
        "text": "[Phase-2] merged-requirements frontmatter has adversarial_status field with passing value",
        "type": "frontmatter_field_in",
        "target": merged,
        "field": "adversarial_status",
        "allowed_values": ["pass", "passed", "success"],
    })
    new_assertions.append({
        "text": "[Phase-2] merged-requirements frontmatter has fit_to_intent status",
        "type": "frontmatter_field_in",
        "target": merged,
        "field": "fit_to_intent",
        "allowed_values": ["pass", "partial", "high"],
    })
    # spec_type — Phase-2 uses schema_version in frontmatter; substitute that as the
    # closest equivalent (the contract calls this the merged-requirements schema marker).
    new_assertions.append({
        "text": "[Phase-2] merged-requirements frontmatter has schema_version (spec_type equivalent)",
        "type": "frontmatter_field",
        "target": merged,
        "field": "schema_version",
        "expected": "1.0",
    })

    if expected_blind_mode:
        new_assertions.append({
            "text": "[Phase-2] merged-requirements frontmatter declares blind_mode: true",
            "type": "frontmatter_field",
            "target": merged,
            "field": "blind_mode",
            "expected": "true",
        })

    # --- Phase-2 return-contract ---
    new_assertions.append({
        "text": "[Phase-2] return-contract has status: success",
        "type": "yaml_field",
        "target": contract,
        "field": "status",
        "expected": "success",
    })
    if expected_domain:
        new_assertions.append({
            "text": f"[Phase-2] return-contract has domain: {expected_domain}",
            "type": "yaml_field",
            "target": contract,
            "field": "domain",
            "expected": expected_domain,
        })
    if expected_proposal_count is not None:
        new_assertions.append({
            "text": f"[Phase-2] return-contract has proposal_count: {expected_proposal_count}",
            "type": "yaml_field",
            "target": contract,
            "field": "proposal_count",
            "expected": str(expected_proposal_count),
        })
    new_assertions.append({
        "text": f"[Phase-2] return-contract has handoff_action: {handoff}",
        "type": "yaml_field",
        "target": contract,
        "field": "handoff_action",
        "expected": handoff,
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract has seed_schema_version",
        "type": "yaml_field",
        "target": contract,
        "field": "seed_schema_version",
        "expected": "1.0",
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract has merged_requirements_schema_version",
        "type": "yaml_field",
        "target": contract,
        "field": "merged_requirements_schema_version",
        "expected": "1.0",
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract has context_anchors_count >= 1",
        "type": "yaml_field_min",
        "target": contract,
        "field": "context_anchors_count",
        "min_value": 1,
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract has fit_to_intent in {pass, partial}",
        "type": "yaml_field_in",
        "target": contract,
        "field": "fit_to_intent",
        "allowed_values": ["pass", "partial", "high"],
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract has source_of_truth_paths referencing sc-brainstorm-protocol",
        "type": "yaml_contains_any_recursive",
        "target": contract,
        "substring_any": ["sc-brainstorm-protocol"],
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract agent_spec contains persona aliases (architect/refactorer/security/devops/qa/analyzer/scribe/pm/backend/performance/Agent)",
        "type": "yaml_contains_any_recursive",
        "target": contract,
        "substring_any": ["architect", "refactorer", "security", "devops", "qa", "analyzer", "scribe", "pm", "backend", "performance", "Agent A"],
    })
    new_assertions.append({
        "text": "[Phase-2] return-contract agent_spec contains model aliases (opus/sonnet/haiku)",
        "type": "yaml_contains_any_recursive",
        "target": contract,
        "substring_any": ["opus", "sonnet", "haiku"],
    })

    # --- Blind mode (case 11 only) ---
    if expected_blind_mode:
        new_assertions.append({
            "text": "[Phase-2 blind] return-contract agent_spec uses anonymized labels (Agent A-E)",
            "type": "yaml_contains_any_recursive",
            "target": contract,
            "substring_any": ["Agent A", "Agent B", "Agent C", "Agent D", "Agent E"],
        })
        new_assertions.append({
            "text": "[Phase-2 blind] debate-transcript uses anonymized labels (Agent A-E)",
            "type": "text_contains_any",
            "target": debate,
            "substring_any": ["Agent A", "Agent B", "Agent C", "Agent D", "Agent E"],
        })
        new_assertions.append({
            "text": "[Phase-2 blind] debate-transcript does NOT leak persona-role labels",
            "type": "text_not_contains_any",
            "target": debate,
            "substring_any": ["opus:architect", "sonnet:security", "sonnet:refactorer", "haiku:qa"],
        })

    return new_assertions


def already_wired(existing: list) -> bool:
    """Return True if Phase-2 assertions are already present (idempotent guard)."""
    for a in existing:
        if a.get("text", "").startswith("[Phase-2]") or a.get("text", "").startswith("[Phase-2 blind]"):
            return True
    return False


def main():
    evals_data = json.loads(EVALS_JSON.read_text())
    cases = {c["id"]: c for c in evals_data["evals"]}

    summary = []
    for case_id in ACCEPTANCE_CASES:
        if case_id not in cases:
            summary.append((case_id, "MISSING from evals.json", 0))
            continue
        case = cases[case_id]
        name = case["name"]
        meta_path = ITER2 / f"eval-{name}" / "eval_metadata.json"
        if not meta_path.exists():
            summary.append((case_id, f"NO eval_metadata.json at {meta_path}", 0))
            continue

        meta = json.loads(meta_path.read_text())
        existing = meta.get("assertions", [])
        before_count = len(existing)

        if already_wired(existing):
            summary.append((case_id, f"already wired (skipping); {before_count} existing", 0))
            continue

        new = build_phase2_assertions(case)
        meta["assertions"] = existing + new
        meta_path.write_text(json.dumps(meta, indent=2) + "\n")
        summary.append((case_id, f"appended {len(new)} new", len(new)))

    print(f"{'Case':<6} {'Status':<60} {'Added':>6}")
    print("-" * 75)
    total_added = 0
    for case_id, status, added in summary:
        print(f"{case_id:<6} {status:<60} {added:>6}")
        total_added += added
    print("-" * 75)
    print(f"{'TOTAL':<6} {'':<60} {total_added:>6}")


if __name__ == "__main__":
    main()
