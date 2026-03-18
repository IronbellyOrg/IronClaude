#!/usr/bin/env python3
"""
Adversarial fidelity checker for release-split outputs.

Uses a two-pass approach:
  Pass 1 (regex): Fast structural check — are the key terms/values present?
  Pass 2 (LLM):  Semantic verification — is the meaning preserved, weakened, or mutated?

Does NOT trust the skill's own fidelity audit — this is independent verification.

Usage:
    python3 fidelity_checker.py \
        --original <path-to-original-spec> \
        --facts <path-to-facts-json> \
        --outputs <path-to-split-output-dir> \
        [--report <path-to-report-json>]
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Fact:
    """A verifiable fact extracted from the original spec."""

    id: str
    category: str
    description: str
    search_patterns: list[str]
    anti_patterns: list[str]  # kept for reference but NOT used for grading
    required_context: list[str]  # kept for reference but NOT used for grading
    source_section: str
    severity: str


@dataclass
class FactCheckResult:
    """Result of checking a single fact against the outputs."""

    fact_id: str
    category: str
    description: str
    severity: str
    status: str  # PRESERVED, WEAKENED, MUTATED, MISSING, CONTEXT_LOST
    evidence: str
    found_in_files: list[str]
    llm_verdict: str
    llm_reasoning: str


def load_facts(facts_path: Path) -> list[Fact]:
    """Load fact definitions from JSON."""
    with open(facts_path) as f:
        data = json.load(f)
    return [Fact(**fact) for fact in data["facts"]]


def read_outputs(output_dir: Path) -> dict[str, str]:
    """Read spec deliverable files from the output directory."""
    spec_files = {
        "release-spec-validated.md",
        "release-1-spec.md",
        "release-2-spec.md",
        "boundary-rationale.md",
    }
    contents = {}
    for md_file in sorted(output_dir.glob("*.md")):
        if md_file.name in spec_files:
            contents[md_file.name] = md_file.read_text()
    if not contents:
        for md_file in sorted(output_dir.glob("*.md")):
            contents[md_file.name] = md_file.read_text()
    return contents


def llm_grade_fact(
    fact: Fact,
    original_excerpt: str,
    output_contents: dict[str, str],
) -> tuple[str, str]:
    """Use claude CLI to semantically grade whether a fact is preserved.

    Returns (verdict, reasoning) where verdict is one of:
      PRESERVED, WEAKENED, MUTATED, MISSING, CONTEXT_LOST
    """
    # Build the combined output text, labelled by file
    output_text = ""
    for fname, content in output_contents.items():
        output_text += f"\n\n=== FILE: {fname} ===\n{content}"

    # Truncate if too long (keep first 15K chars per file)
    if len(output_text) > 60000:
        truncated = ""
        for fname, content in output_contents.items():
            truncated += f"\n\n=== FILE: {fname} ===\n{content[:15000]}"
        output_text = truncated

    prompt = f"""You are a specification fidelity auditor. Your job is to determine whether a specific fact from an original specification has been faithfully preserved in the output documents.

FACT TO VERIFY:
- ID: {fact.id}
- Category: {fact.category}
- Severity: {fact.severity}
- Description: {fact.description}
- Source section: {fact.source_section}

IMPORTANT: You must check whether the SEMANTIC MEANING is preserved, not just whether keywords appear. Specifically watch for:
- Quantitative values changed (e.g., 500ms became 1000ms, 5 seconds became 10 seconds)
- Behavioral contracts weakened (e.g., "MUST NOT" became "SHOULD NOT" or was omitted)
- Conditional logic simplified (e.g., a two-condition guard lost one condition)
- Negative requirements dropped (e.g., "X is NOT supported" was omitted entirely)
- Ordering constraints lost (e.g., "A before B" no longer specified)
- Exception paths removed (e.g., timeout handling or error cases dropped)
- Cross-requirement coupling broken (e.g., R3 references R1's contract but the contract details are missing)

OUTPUT DOCUMENTS TO CHECK:
{output_text}

Respond with EXACTLY this JSON format and nothing else:
{{"verdict": "PRESERVED|WEAKENED|MUTATED|MISSING|CONTEXT_LOST", "reasoning": "2-3 sentence explanation with specific evidence"}}

Verdict definitions:
- PRESERVED: The fact is present with its full meaning intact. Paraphrasing is OK if semantically equivalent.
- WEAKENED: The fact is partially present but some important detail is missing or softened.
- MUTATED: The fact is present but a specific value, condition, or behavior has been changed incorrectly.
- MISSING: The fact cannot be found in any output document.
- CONTEXT_LOST: The core fact is present but the surrounding context needed to understand it correctly is gone."""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--model", "haiku"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return "ERROR", f"claude CLI failed: {result.stderr[:200]}"

        response = result.stdout.strip()
        # Extract JSON from response
        # Try to find JSON object in the response
        json_match = re.search(r'\{[^{}]*"verdict"[^{}]*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return data.get("verdict", "ERROR"), data.get(
                "reasoning", "No reasoning provided"
            )
        else:
            # Try parsing the whole response as JSON
            data = json.loads(response)
            return data.get("verdict", "ERROR"), data.get(
                "reasoning", "No reasoning provided"
            )

    except subprocess.TimeoutExpired:
        return "ERROR", "LLM grading timed out after 60s"
    except json.JSONDecodeError:
        return "ERROR", f"Could not parse LLM response as JSON: {response[:300]}"
    except FileNotFoundError:
        return "ERROR", "claude CLI not found — install Claude Code"
    except Exception as e:
        return "ERROR", f"Unexpected error: {str(e)[:200]}"


def check_fact(
    fact: Fact,
    outputs: dict[str, str],
    use_llm: bool = True,
) -> FactCheckResult:
    """Check whether a single fact survived the split.

    Pass 1: Regex check for presence of key terms
    Pass 2: LLM semantic verification (if use_llm=True)
    """
    found_in_files = []
    search_hits = []

    # Pass 1: Check search patterns for presence
    for pattern in fact.search_patterns:
        for filename, content in outputs.items():
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                if filename not in found_in_files:
                    found_in_files.append(filename)
                search_hits.append(pattern)
                break

    # If nothing found at all, it's MISSING — no need for LLM
    if not search_hits:
        return FactCheckResult(
            fact_id=fact.id,
            category=fact.category,
            description=fact.description,
            severity=fact.severity,
            status="MISSING",
            evidence=(
                f"None of the search patterns matched in any output file. "
                f"Patterns tried: {fact.search_patterns}"
            ),
            found_in_files=[],
            llm_verdict="SKIPPED",
            llm_reasoning="No regex matches — fact is clearly missing, LLM grading skipped.",
        )

    # Pass 2: LLM semantic verification
    if use_llm:
        llm_verdict, llm_reasoning = llm_grade_fact(fact, "", outputs)

        if llm_verdict == "ERROR":
            # Fall back to regex-only: if search patterns matched, call it PRESERVED
            status = (
                "PRESERVED"
                if len(search_hits) == len(fact.search_patterns)
                else "WEAKENED"
            )
            evidence = f"LLM grading failed ({llm_reasoning}). Regex fallback: {len(search_hits)}/{len(fact.search_patterns)} patterns matched."
        else:
            status = llm_verdict
            evidence = llm_reasoning
    else:
        llm_verdict = "SKIPPED"
        llm_reasoning = "LLM grading disabled"
        if len(search_hits) < len(fact.search_patterns):
            status = "WEAKENED"
            matched = set(search_hits)
            missing = [p for p in fact.search_patterns if p not in matched]
            evidence = f"Partially preserved — {len(search_hits)}/{len(fact.search_patterns)} patterns matched. Missing: {missing}"
        else:
            status = "PRESERVED"
            evidence = f"All {len(fact.search_patterns)} search patterns matched."

    return FactCheckResult(
        fact_id=fact.id,
        category=fact.category,
        description=fact.description,
        severity=fact.severity,
        status=status,
        evidence=evidence,
        found_in_files=found_in_files,
        llm_verdict=llm_verdict,
        llm_reasoning=llm_reasoning,
    )


def generate_report(
    results: list[FactCheckResult],
    original_path: str,
    output_dir: str,
) -> dict:
    """Generate the fidelity check report."""

    total = len(results)
    by_status = {}
    by_category = {}
    by_severity = {}
    critical_failures = []

    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
        by_category.setdefault(r.category, []).append(r)
        by_severity.setdefault(r.severity, []).append(r)

        if r.status != "PRESERVED" and r.severity == "critical":
            critical_failures.append(r)

    preserved = by_status.get("PRESERVED", 0)
    fidelity_score = preserved / total if total > 0 else 0.0

    return {
        "metadata": {
            "original_spec": original_path,
            "output_dir": output_dir,
            "total_facts_checked": total,
            "checker": "adversarial_fidelity_checker_v1",
        },
        "summary": {
            "fidelity_score": round(fidelity_score, 4),
            "preserved": by_status.get("PRESERVED", 0),
            "weakened": by_status.get("WEAKENED", 0),
            "mutated": by_status.get("MUTATED", 0),
            "missing": by_status.get("MISSING", 0),
            "context_lost": by_status.get("CONTEXT_LOST", 0),
            "critical_failures": len(critical_failures),
        },
        "critical_failures": [asdict(r) for r in critical_failures],
        "all_results": [asdict(r) for r in results],
        "by_category": {
            cat: {
                "total": len(items),
                "preserved": sum(1 for i in items if i.status == "PRESERVED"),
                "failures": sum(1 for i in items if i.status != "PRESERVED"),
            }
            for cat, items in by_category.items()
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Adversarial fidelity checker for release-split outputs"
    )
    parser.add_argument("--original", required=True, help="Path to original spec")
    parser.add_argument("--facts", required=True, help="Path to facts JSON")
    parser.add_argument(
        "--outputs", required=True, help="Path to split output directory"
    )
    parser.add_argument("--report", default=None, help="Path to write report JSON")
    parser.add_argument(
        "--no-llm", action="store_true", help="Disable LLM grading (regex only)"
    )
    args = parser.parse_args()

    facts = load_facts(Path(args.facts))
    outputs = read_outputs(Path(args.outputs))
    use_llm = not args.no_llm

    if not outputs:
        print(f"ERROR: No .md files found in {args.outputs}", file=sys.stderr)
        sys.exit(1)

    mode = "regex + LLM semantic" if use_llm else "regex only"
    print(
        f"Checking {len(facts)} facts against {len(outputs)} output files ({mode})..."
    )

    results = []
    for i, fact in enumerate(facts, 1):
        print(f"  [{i}/{len(facts)}] {fact.id}: {fact.description[:60]}...", flush=True)
        result = check_fact(fact, outputs, use_llm=use_llm)
        status_marker = (
            "PASS" if result.status == "PRESERVED" else f"FAIL:{result.status}"
        )
        print(f"           -> {status_marker}", flush=True)
        results.append(result)

    report = generate_report(results, args.original, args.outputs)

    # Print summary
    s = report["summary"]
    print(f"\n{'=' * 60}")
    print(f"FIDELITY CHECK RESULTS")
    print(f"{'=' * 60}")
    print(
        f"Score: {s['fidelity_score']:.1%} ({s['preserved']}/{report['metadata']['total_facts_checked']} facts preserved)"
    )
    print(f"  PRESERVED:    {s['preserved']}")
    print(f"  WEAKENED:     {s['weakened']}")
    print(f"  MUTATED:      {s['mutated']}")
    print(f"  MISSING:      {s['missing']}")
    print(f"  CONTEXT_LOST: {s['context_lost']}")
    print(f"  CRITICAL FAILURES: {s['critical_failures']}")

    if report["critical_failures"]:
        print(f"\n{'=' * 60}")
        print("CRITICAL FAILURES:")
        print(f"{'=' * 60}")
        for cf in report["critical_failures"]:
            print(f"\n  [{cf['fact_id']}] {cf['description']}")
            print(f"    Status: {cf['status']}")
            print(f"    Category: {cf['category']}")
            print(f"    Evidence: {cf['evidence'][:200]}")

    print(f"\nBy category:")
    for cat, stats in report["by_category"].items():
        marker = "✓" if stats["failures"] == 0 else "✗"
        print(f"  {marker} {cat}: {stats['preserved']}/{stats['total']} preserved")

    # Write report
    report_path = args.report or str(Path(args.outputs) / "fidelity-check-results.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nFull report written to: {report_path}")

    # Exit with failure code if critical failures exist
    if s["critical_failures"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
