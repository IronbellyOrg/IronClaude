"""Release-level retrospective generator (TUI v2 Wave 3, v3.7).

Runs once, blocking, at the very end of a sprint. Consumes the
per-phase summaries collected by :class:`.summarizer.SummaryWorker`,
aggregates them programmatically across phases, asks Haiku for a 4-8
sentence narrative, and writes ``results/release-retrospective.md``.

Aggregation captures four cross-phase patterns:
1. **Multi-phase file modifications** — files touched in more than one
   phase (a classic source of merge friction).
2. **Error patterns** — total error count + top-recurring error tool.
3. **Validation gaps** — checks that never showed up in any phase
   summary; useful to flag phases that skipped tests.
4. **Timing trends** — longest and shortest phase for operator
   awareness.

All failures are silently logged so the retrospective never aborts a
successful sprint. Haiku subprocess failure writes the retrospective
without a narrative section (Section 6.3).

Spec refs: §3.2 (F10), §6.3 (Haiku subprocess), §6.4 (hook ordering),
§7.6 (ReleaseRetrospective dataclass).
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .models import SprintConfig, SprintResult
from .summarizer import PhaseSummary, invoke_haiku

_logger = logging.getLogger("superclaude.sprint.retrospective")


# ---------------------------------------------------------------------------
# Data class (spec §7.6)
# ---------------------------------------------------------------------------


@dataclass
class ReleaseRetrospective:
    sprint_result: SprintResult
    phase_outcomes: list[dict] = field(default_factory=list)
    all_files: list[dict] = field(default_factory=list)
    validation_matrix: list[dict] = field(default_factory=list)
    all_errors: list[dict] = field(default_factory=list)
    validation_coverage: str = ""
    narrative: str = ""

    @property
    def retrospective_path(self) -> Optional[Path]:
        """Return the destination path when the sprint config exposes one."""
        config = self.sprint_result.config
        try:
            return config.results_dir / "release-retrospective.md"
        except Exception:  # noqa: BLE001 - defensive path arithmetic
            return None


# ---------------------------------------------------------------------------
# Aggregation (pure functions)
# ---------------------------------------------------------------------------


def _aggregate_phase_outcomes(summaries: dict[int, PhaseSummary]) -> list[dict]:
    """Return one dict per phase ordered by phase number."""
    rows: list[dict] = []
    for phase_num in sorted(summaries):
        s = summaries[phase_num]
        pr = s.phase_result
        rows.append(
            {
                "phase": phase_num,
                "name": s.phase.display_name,
                "status": pr.status.value,
                "duration": pr.duration_display,
                "turns": pr.turns,
                "tokens_in": pr.tokens_in,
                "tokens_out": pr.tokens_out,
                "files_changed": len(s.files_changed),
                "errors": len(s.errors),
            }
        )
    return rows


def _aggregate_files(summaries: dict[int, PhaseSummary]) -> list[dict]:
    """Flatten every file touched across phases with the phases list."""
    by_path: dict[str, dict] = {}
    for phase_num in sorted(summaries):
        for entry in summaries[phase_num].files_changed:
            path = entry["path"]
            rec = by_path.setdefault(
                path, {"path": path, "phases": [], "tools": set()}
            )
            rec["phases"].append(phase_num)
            rec["tools"].add(entry["tool"])
    # Normalise sets → lists for deterministic serialisation.
    return [
        {
            "path": rec["path"],
            "phases": rec["phases"],
            "tools": sorted(rec["tools"]),
            "multi_phase": len(rec["phases"]) > 1,
        }
        for rec in sorted(by_path.values(), key=lambda r: r["path"])
    ]


def _aggregate_validation_matrix(summaries: dict[int, PhaseSummary]) -> list[dict]:
    """Per-check rollup of verdicts across phases."""
    by_check: dict[str, dict] = {}
    for phase_num in sorted(summaries):
        for v in summaries[phase_num].validations:
            check = v["check"].lower()
            rec = by_check.setdefault(
                check,
                {"check": check, "verdicts": [], "phases": []},
            )
            rec["verdicts"].append(v["verdict"])
            rec["phases"].append(phase_num)
    return sorted(by_check.values(), key=lambda r: r["check"])


def _aggregate_errors(summaries: dict[int, PhaseSummary]) -> list[dict]:
    """Flatten all per-phase errors, tagging each with its phase."""
    out: list[dict] = []
    for phase_num in sorted(summaries):
        for err in summaries[phase_num].errors:
            out.append({**err, "phase": phase_num})
    return out


def _assess_validation_coverage(
    summaries: dict[int, PhaseSummary],
    matrix: list[dict],
) -> str:
    """Return a one-line coverage verdict for the retrospective header."""
    if not summaries:
        return "no phases summarised"
    covered_phases = sum(1 for s in summaries.values() if s.validations)
    if covered_phases == len(summaries):
        return f"validation evidence in all {len(summaries)} phases"
    if covered_phases == 0:
        return "no validation evidence detected in any phase"
    return (
        f"{covered_phases}/{len(summaries)} phases carried validation evidence; "
        f"{len(matrix)} distinct checks surfaced"
    )


# ---------------------------------------------------------------------------
# Narrative prompt + markdown rendering
# ---------------------------------------------------------------------------


def _build_retrospective_narrative_prompt(retro: ReleaseRetrospective) -> str:
    sr = retro.sprint_result
    lines: list[str] = [
        (
            f"Release retrospective: sprint outcome {sr.outcome.value.upper()}, "
            f"{len(retro.phase_outcomes)} phases, {sr.total_turns} turns, "
            f"{sr.total_tokens_in} input / {sr.total_tokens_out} output tokens, "
            f"duration {sr.duration_display}."
        ),
        "",
        "Phase outcomes:",
    ]
    for row in retro.phase_outcomes[:20]:
        lines.append(
            f"- Phase {row['phase']} ({row['name']}): {row['status']} in "
            f"{row['duration']}, {row['turns']} turns, "
            f"{row['files_changed']} files, {row['errors']} errors"
        )
    if retro.all_files:
        multi = [f for f in retro.all_files if f["multi_phase"]]
        lines.append("")
        lines.append(
            f"Files touched: {len(retro.all_files)} total "
            f"({len(multi)} across multiple phases)."
        )
        for f in multi[:10]:
            lines.append(f"- {f['path']} in phases {f['phases']}")
    if retro.validation_matrix:
        lines.append("")
        lines.append("Validation matrix:")
        for v in retro.validation_matrix[:10]:
            verdict_hist = Counter(v["verdicts"]).most_common()
            verdict_desc = ", ".join(f"{name}×{cnt}" for name, cnt in verdict_hist)
            lines.append(f"- {v['check']}: {verdict_desc} ({len(v['phases'])} phases)")
    if retro.all_errors:
        by_tool = Counter(e.get("tool") or "-" for e in retro.all_errors)
        top = by_tool.most_common(3)
        lines.append("")
        lines.append(
            f"Errors: {len(retro.all_errors)} total — top tools: "
            + ", ".join(f"{t}×{c}" for t, c in top)
        )
    lines.append("")
    lines.append(f"Validation coverage: {retro.validation_coverage}")
    lines.append("")
    lines.append(
        "Write a concise 4-8 sentence retrospective covering: what shipped, "
        "key risks or regressions, validation posture, and whether the "
        "release is ready to hand off. Plain text only, no markdown, "
        "no lists."
    )
    return "\n".join(lines)


def _render_retrospective_markdown(retro: ReleaseRetrospective) -> str:
    sr = retro.sprint_result
    out: list[str] = [
        "# Release Retrospective",
        "",
        f"**Outcome:** {sr.outcome.value.upper()}  ",
        f"**Duration:** {sr.duration_display}  ",
        f"**Phases:** {len(retro.phase_outcomes)}  ",
        f"**Total turns:** {sr.total_turns}  ",
        f"**Tokens:** in={sr.total_tokens_in} / out={sr.total_tokens_out}  ",
        f"**Files changed:** {sr.total_files_changed}  ",
        f"**Validation coverage:** {retro.validation_coverage}",
        "",
    ]
    if retro.narrative:
        out.extend(["## Narrative", "", retro.narrative.strip(), ""])
    else:
        out.extend(
            [
                "## Narrative",
                "",
                "_Narrative unavailable (Haiku subprocess failed or skipped)._",
                "",
            ]
        )

    out.append("## Phase Outcomes")
    out.append("")
    if retro.phase_outcomes:
        out.append("| # | Phase | Status | Duration | Turns | Files | Errors |")
        out.append("|---|-------|--------|----------|-------|-------|--------|")
        for row in retro.phase_outcomes:
            out.append(
                f"| {row['phase']} | {row['name']} | {row['status']} | "
                f"{row['duration']} | {row['turns']} | {row['files_changed']} "
                f"| {row['errors']} |"
            )
    else:
        out.append("_No per-phase summaries available._")
    out.append("")

    out.append("## Files Changed")
    out.append("")
    if retro.all_files:
        out.append("| Path | Phases | Tools | Multi-phase |")
        out.append("|------|--------|-------|-------------|")
        for f in retro.all_files:
            phases = ",".join(str(p) for p in f["phases"])
            tools = ",".join(f["tools"])
            flag = "yes" if f["multi_phase"] else ""
            out.append(f"| `{f['path']}` | {phases} | {tools} | {flag} |")
    else:
        out.append("_None detected._")
    out.append("")

    out.append("## Validation Matrix")
    out.append("")
    if retro.validation_matrix:
        for v in retro.validation_matrix:
            hist = Counter(v["verdicts"]).most_common()
            out.append(
                f"- **{v['check']}** — "
                + ", ".join(f"{n}×{c}" for n, c in hist)
                + f" ({len(v['phases'])} phase(s))"
            )
    else:
        out.append("_No validation evidence detected in any phase._")
    out.append("")

    out.append("## Errors")
    out.append("")
    if retro.all_errors:
        by_tool = Counter(e.get("tool") or "-" for e in retro.all_errors)
        out.append(
            "Top tools: "
            + ", ".join(f"`{t}`×{c}" for t, c in by_tool.most_common(5))
        )
        out.append("")
        for err in retro.all_errors[:30]:
            msg = err["message"].replace("\n", " ")
            out.append(
                f"- Phase {err['phase']} / `{err.get('task_id') or '-'}` / "
                f"`{err.get('tool') or '-'}` — {msg[:120]}"
            )
        if len(retro.all_errors) > 30:
            out.append(f"- _+{len(retro.all_errors) - 30} more errors omitted_")
    else:
        out.append("_None detected._")
    out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Generator (blocking, runs once at sprint end)
# ---------------------------------------------------------------------------


class RetrospectiveGenerator:
    def __init__(self, config: SprintConfig):
        self.config = config

    def aggregate(
        self, sprint_result: SprintResult, summaries: dict[int, PhaseSummary]
    ) -> ReleaseRetrospective:
        matrix = _aggregate_validation_matrix(summaries)
        return ReleaseRetrospective(
            sprint_result=sprint_result,
            phase_outcomes=_aggregate_phase_outcomes(summaries),
            all_files=_aggregate_files(summaries),
            validation_matrix=matrix,
            all_errors=_aggregate_errors(summaries),
            validation_coverage=_assess_validation_coverage(summaries, matrix),
        )

    def narrate(self, retro: ReleaseRetrospective) -> str:
        """Invoke Haiku for a narrative, skipping when there is no content.

        A retrospective with zero phase outcomes conveys nothing Haiku
        could usefully summarise (e.g. an interrupted sprint that never
        ran a phase); calling out to a subprocess in that case only
        burns time and pollutes test environments that mock subprocess.
        """
        if not retro.phase_outcomes:
            return ""
        return invoke_haiku(_build_retrospective_narrative_prompt(retro))

    def write(self, retro: ReleaseRetrospective) -> Optional[Path]:
        target = self.config.results_dir / "release-retrospective.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_retrospective_markdown(retro))
        return target

    def generate(
        self,
        sprint_result: SprintResult,
        summaries: dict[int, PhaseSummary],
    ) -> ReleaseRetrospective:
        """Aggregate, narrate, and write the retrospective.

        Returns the :class:`ReleaseRetrospective` even when narrate/write
        fail — callers can inspect ``narrative`` to decide whether to
        surface a warning.
        """
        retro = self.aggregate(sprint_result, summaries)
        try:
            retro.narrative = self.narrate(retro)
        except Exception as exc:  # noqa: BLE001 - must not abort sprint wrap-up
            _logger.warning("RetrospectiveGenerator: narrate step raised %s", exc)
            retro.narrative = ""
        try:
            self.write(retro)
        except Exception as exc:  # noqa: BLE001 - must not abort sprint wrap-up
            _logger.warning("RetrospectiveGenerator: write step raised %s", exc)
        return retro
