"""Seed the schema_version-2 lookup cache with the 4 eval-backed rows.

Writes `.claude/cache/sc-recommend-lookup.yaml` THROUGH the atomic
`LookupCache.save()` writer (NOT hand-authored), with the current computed
surface_hash and full-digest per-row source_hash. best_model is null (rows are
unevaluated until --eval); native_fallback is false (all 4 are delegation rows).

Each row's flags are VERIFIED against the candidate's source file (no fabricated
flags per R1) and each prompt_envelope_template is a hand-off envelope, NOT a
protocol restatement (R3).
"""

from datetime import datetime, timezone
from pathlib import Path

from superclaude.cli.recommend.cache import (
    LookupCache,
    compute_source_hash,
    compute_surface_hash,
)

NOW = datetime.now(timezone.utc).isoformat()
CACHE_PATH = Path(".claude/cache/sc-recommend-lookup.yaml")


def src_hash(rel: str) -> str:
    return compute_source_hash(Path(rel).read_bytes())


rows = [
    {
        "key": "spec-generation",
        "candidate": "/sc:spec-panel",
        # Verified against src/superclaude/commands/spec-panel.md Usage line.
        "flags": [
            "--mode discussion|critique|socratic",
            '--experts "name1,name2"',
            "--focus requirements|architecture|testing|compliance|correctness",
            "--iterations N",
            "--format standard|structured|detailed",
        ],
        "prompt_envelope_template": (
            "Run: /sc:spec-panel @{spec_inputs} --focus {focus_areas} --mode {mode}\n\n"
            "Goal: {goal}\n"
            "Deliverable: {deliverable_shape}\n"
            "(Hand-off only — the panel owns its expert sequence and review logic.)"
        ),
        "rationale": "Multi-expert spec review/improvement; wins over native for structured spec generation.",
        "source_path": "src/superclaude/commands/spec-panel.md",
        "source_hash": src_hash("src/superclaude/commands/spec-panel.md"),
        "last_validated_at": NOW,
        "native_fallback": False,
        "best_model": None,
    },
    {
        "key": "codebase-research",
        "candidate": "tech-research skill (or deep-research agent / Explore / auggie)",
        "flags": [],  # skill/agent invoked by prompt; no slash-flag table
        "prompt_envelope_template": (
            "Invoke the tech-research skill (or the deep-research agent) on:\n"
            "Research question: {research_question}\n"
            "Scope: {scope}\n"
            "Deliverable: a structured research report (findings + gaps + recommendations).\n"
            "(Hand-off only — the skill owns its investigation pipeline.)"
        ),
        "rationale": "Deep codebase/system investigation; wins over native when the question spans many files.",
        "source_path": "src/superclaude/skills/tech-research/SKILL.md",
        "source_hash": src_hash("src/superclaude/skills/tech-research/SKILL.md"),
        "last_validated_at": NOW,
        "native_fallback": False,
        "best_model": None,
    },
    {
        "key": "tasklist-generation",
        "candidate": "/sc:tasklist (or task-builder)",
        # Verified against src/superclaude/commands/tasklist.md Usage/Arguments.
        "flags": [
            "<roadmap-path>",
            "--spec <spec-path>",
            "--output <output-dir>",
        ],
        "prompt_envelope_template": (
            "Run: /sc:tasklist {roadmap_path} --spec {spec_path} --output {output_dir}\n\n"
            "Goal: {goal}\n"
            "(Hand-off only — the protocol skill owns the generation algorithm; do NOT reimplement it.)"
        ),
        "rationale": "Deterministic roadmap->tasklist bundle generation; hands off, never reimplements.",
        "source_path": "src/superclaude/commands/tasklist.md",
        "source_hash": src_hash("src/superclaude/commands/tasklist.md"),
        "last_validated_at": NOW,
        "native_fallback": False,
        "best_model": None,
    },
    {
        "key": "parallel-agent-fanout",
        "candidate": "parallel Agent fan-out (multiple Agent tool calls in ONE message)",
        "flags": [],  # native harness pattern; no slash-flag table
        "prompt_envelope_template": (
            "Spawn N parallel Agent tool calls in a SINGLE message, one per item in:\n"
            "Items: {items}\n"
            "Each agent produces: {per_item_deliverable}\n"
            "Then synthesize the results into: {final_deliverable}\n"
            "(Hand-off only — wins on wall-clock + context isolation vs a sequential skill chain.)"
        ),
        "rationale": "Naturally-parallel work (research N items + synthesize); parallel fan-out beats serial chains.",
        # Pattern is documented in the sc-recommend net-value heuristics ref (line 64).
        "source_path": "src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md",
        "source_hash": src_hash(
            "src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md"
        ),
        "last_validated_at": NOW,
        "native_fallback": False,
        "best_model": None,
    },
]

surface_hash = compute_surface_hash()
cache = LookupCache(path=CACHE_PATH, surface_hash=surface_hash, rows=rows)
cache.save()
print(f"Seeded {len(rows)} rows -> {CACHE_PATH}")
print(f"surface_hash={surface_hash}")
for r in rows:
    print(f"  {r['key']:24s} source_hash={r['source_hash'][:12]}... (len={len(r['source_hash'])})")
