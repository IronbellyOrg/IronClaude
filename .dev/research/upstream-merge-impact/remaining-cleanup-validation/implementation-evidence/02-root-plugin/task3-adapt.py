#!/usr/bin/env python3
"""Reproduce the 22 source-derived Task 3 resources and their exact adaptation log."""

import hashlib
import json
import re
import runpy
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
CONTRACT = json.loads((OUT / "plugin-contract.json").read_text())

SKILLS = {
    "sc:reflect-protocol": "sc:sc-reflect-protocol",
    "sc-reflect-protocol": "sc:sc-reflect-protocol",
    "sc:adversarial-protocol": "sc:sc-adversarial-protocol",
    "sc-adversarial-protocol": "sc:sc-adversarial-protocol",
    "confidence-check": "sc:confidence-check",
}
AGENTS = {name: f"sc:{name}" for name in (
    "confidence-calibrator", "evidence-validator", "reflect-reviewer",
    "reuse-auditor", "debate-orchestrator", "merge-executor",
)}
AGENTS.update({name: f"sc:sc-{name}" for name in (
    "root-cause-analyst", "self-review", "requirements-analyst", "socratic-mentor",
)})

RESOLVER = """## Plugin-local resource resolution (binding)

This distribution runs without the Python package, global framework installation,
project development mirrors, or other plugins. Resolve all file reads from this
plugin: `${CLAUDE_PLUGIN_ROOT}/skills/<directory>/SKILL.md` and
`${CLAUDE_PLUGIN_ROOT}/agents/<filename>.md`. A `refs/<file>` path is relative to
the loaded skill directory, never the audited project's working directory.
Frontmatter logical names do not override native filename/directory identities.
Use the qualified names below for EVERY delegation, including tables and shorthand
`Task(...)` directives. Do not scan global directories, install dependencies, or
substitute an all-tools reviewer when a registered resource is absent.

| Resource | Native invocation | Local file |
|---|---|---|
| Reflection | `Skill sc:sc-reflect-protocol` | `${CLAUDE_PLUGIN_ROOT}/skills/sc-reflect-protocol/SKILL.md` |
| Adversarial merge | `Skill sc:sc-adversarial-protocol` | `${CLAUDE_PLUGIN_ROOT}/skills/sc-adversarial-protocol/SKILL.md` |
| Recommendation confidence | `Skill sc:confidence-check` | `${CLAUDE_PLUGIN_ROOT}/skills/confidence-check/SKILL.md` |
| Calibration | `Task(sc:confidence-calibrator)` | `${CLAUDE_PLUGIN_ROOT}/agents/confidence-calibrator.md` |
| Evidence gate | `Task(sc:evidence-validator)` | `${CLAUDE_PLUGIN_ROOT}/agents/evidence-validator.md` |
| Restricted reviewer | `Task(sc:reflect-reviewer)` | `${CLAUDE_PLUGIN_ROOT}/agents/reflect-reviewer.md` |
| Reuse search | `Task(sc:reuse-auditor)` | `${CLAUDE_PLUGIN_ROOT}/agents/reuse-auditor.md` |
| Debate coordination | `Task(sc:debate-orchestrator)` | `${CLAUDE_PLUGIN_ROOT}/agents/debate-orchestrator.md` |
| Merge execution | `Task(sc:merge-executor)` | `${CLAUDE_PLUGIN_ROOT}/agents/merge-executor.md` |
| Root-cause specialist | `Task(sc:sc-root-cause-analyst)` | `${CLAUDE_PLUGIN_ROOT}/agents/sc-root-cause-analyst.md` |
| Completion specialist | `Task(sc:sc-self-review)` | `${CLAUDE_PLUGIN_ROOT}/agents/sc-self-review.md` |
| Coverage specialist | `Task(sc:sc-requirements-analyst)` | `${CLAUDE_PLUGIN_ROOT}/agents/sc-requirements-analyst.md` |
| Optional probing specialist | `Task(sc:sc-socratic-mentor)` | `${CLAUDE_PLUGIN_ROOT}/agents/sc-socratic-mentor.md` |

The root reflection command is `/sc:sc-reflect`. Adversarial command examples
below mean the bundled `Skill sc:sc-adversarial-protocol`, not a separate command.
Dynamic advocates, fault-finders and scorers are native Task workers using the
inline briefs and model selection below, not missing named framework agents.
The reflection Tier-2 pool ALWAYS uses `sc:reflect-reviewer` with brief-supplied
personas; historical `rf-qa` / `rf-qa-qualitative` mentions describe structural
and document lenses, not alternate agent types to load.

### Optional unavailable resources (binding pre-dispatch gate)

`tech-research`, `audit-validator`, `sc-workflow-protocol` (including the logical
spelling `sc:workflow-protocol`), `task-builder` and `rf-task-builder` are
**UNAVAILABLE in this plugin-only distribution**. Do not invoke them, search a
global installation, copy them in, install them, or substitute another executor.
Before every optional dispatch described below, apply its source-defined fallback:

- Research: skip optional external best-practice lookup, record the missing
  resource and a loud degraded/grounding-gap warning; never claim it was checked.
- Spot-check auditor: use `sc:evidence-validator` alone (the source's stricter
  fallback), retaining the mandatory final citation gate.
- Remediation: without `--remediate`, never enter Wave 6. With an explicit request,
  surface `remediation_unavailable: true`, name the unavailable selected builder,
  keep the report, and emit `remediation_task_path: null`,
  `remediation_plan_path: null`, `task_file_path: null`,
  `remediation_accepted: false`, `handoff_memory_key: null`. Do not offer the other
  unavailable route as a working alternative, author a substitute plan, or run
  `/task` or `/sc:sc-implement`. The detailed source handoff phases below are
  unavailable integration documentation, not executable plugin-only instructions.
- MCPs are optional: check actual exposed tools; apply the specific native
  Grep/Glob/Read fallback and degraded/partial markers below. No fake successful
  memory, diagnostic, verification, external lookup, or reachability result.

Missing REQUIRED registered resources instead take the explicit failure/partial
fallback below; fallback evidence is never proof of a successful real merge,
independent calibration or evidence gate.

### Distribution output guard (before any write)

Retain all input overlap, pinned-realpath, traversal and symlink guards below.
Additionally refuse output equal to, inside, or containing any plugin distribution
component directory: `${CLAUDE_PLUGIN_ROOT}/skills`, `/agents`, `/commands`, or
`/.claude-plugin` (each suffix is relative to the same plugin root). Compare
resolved path components through the nearest existing ancestor, not string
prefixes; reject symlink aliases too. Never write audit artifacts into plugin
resources. Apply this guard to nested pipeline phases and every output override.

### Maintainer-only and external-package material

Source provenance, reverse-caller tables, framework registration, eval/build/CI,
checkout maintenance, and historical incident references below are maintainer-only
context, unavailable in plugin-only operation. They are NOT resources to read,
steps to run, files to create, or instructions to install the framework. In
particular `refs/grader-extensions.md`, `refs/cost-profile.yaml`, source specs and
eval workspaces are not bundled runtime dependencies. Budget preflight uses the
inline numeric table; no caller cost-profile file is read by this skill.
Package `superclaude reflect contract-status` readiness and Python-wrapper-only
isolation/auto-fix behavior require a separately available `superclaude` executable
and its package. This plugin does NOT bundle that prerequisite, import package
code, implement its wrapper, or launch a remediation executor. A readiness request
without that executable returns explicitly unavailable, not a UC-1/UC-2 audit.

"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def frontmatter(text):
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4) + 5
        return text[:end], text[end:]
    return "", text


def adapt(row):
    source = (ROOT / row["source"]).read_text()
    header, body = frontmatter(source)
    changes = []

    def change(old, new, reason, required=False):
        nonlocal body
        count = body.count(old)
        if required:
            assert count, (row["source"], old)
        if count:
            body = body.replace(old, new)
            changes.append({"kind": "literal", "old": old, "new": new,
                            "count": count, "reason": reason})

    # Complete token boundaries deliberately exclude paths and filename stems.
    for old, new in {**SKILLS, **AGENTS}.items():
        pattern = rf"(?<![A-Za-z0-9_/:.\-]){re.escape(old)}(?![A-Za-z0-9_/\-]|\.md)"
        updated, count = re.subn(pattern, new, body)
        if count:
            body = updated
            changes.append({"kind": "regex", "pattern": pattern, "new": new,
                            "count": count, "reason": "verified native invocation identity; never rewrite paths/frontmatter"})
    for agent in AGENTS:
        change(f"~/.claude/agents/{agent}.md",
               "${CLAUDE_PLUGIN_ROOT}/agents/" + agent + ".md",
               "plugin-root file lookup")
    for old in ("/sc:reflect", "/sc:implement", "/sc:workflow", "/sc:analyze"):
        new = "/sc:sc-" + old.removeprefix("/sc:")
        pattern = re.escape(old) + r"(?![A-Za-z0-9_:\-])"
        body, count = re.subn(pattern, new, body)
        if count:
            changes.append({"kind": "regex", "pattern": pattern, "new": new,
                            "count": count, "reason": "preserved root filename-derived command identity"})
    change("/sc:adversarial", "Skill sc:sc-adversarial-protocol", "bundled skill, no unregistered adversarial command")
    change("`~/.claude/commands/sc/spawn.md` Rule 2.5",
           "the caller's Stage 1 branch-trace provenance (spawn Rule 2.5; no external command read)",
           "branch-trace is caller evidence; inline enumeration remains mandatory fallback")

    dest = row["destination"]
    if dest == "skills/sc-reflect-protocol/SKILL.md":
        change("probe its existence via `mcp__serena__list_memories` for the skill's existence indicator OR a no-op `Skill('sc:sc-adversarial-protocol', args='--help')`. If the probe returns `skill not found`:",
               "check that `sc:sc-adversarial-protocol` appears in the native registered skills AND Read `${CLAUDE_PLUGIN_ROOT}/skills/sc-adversarial-protocol/SKILL.md` for local existence. This is a resource check only: NEVER invoke Skill with `--help` or run another audit as a probe. If registration or local existence is missing:",
               "safe plugin-local registered-resource existence check", required=True)
        change("STOP with explicit install instruction (per sc-brainstorm Wave 0 pattern)",
               "surface the explicit unavailable/fallback outcome from the plugin-local pre-dispatch gate; never install or search outside this plugin",
               "honest optional-unavailable boundary", required=True)
        change("*Replaces with:* `Skill sc-brainstorm-protocol` (upstream).", "*Upstream-only alternative, UNAVAILABLE in plugin-only operation:* sc-brainstorm-protocol (not a resource to invoke).", "brainstorm provenance is not a required dispatch", required=True)
        # Source's active Tier-2 rule already fixes this type. Make legacy table rows agree.
        change("| `rf-qa` |", "| `sc:reflect-reviewer` (structural persona; historical rf-qa) |", "existing restricted reviewer role mapping")
        change("| `rf-qa-qualitative` |", "| `sc:reflect-reviewer` (document persona; historical rf-qa-qualitative) |", "existing restricted reviewer role mapping")
        change("| `rf-qa` / `rf-qa-qualitative` fails in Wave 3 |", "| `sc:reflect-reviewer` structural / document persona fails in Wave 3 |", "restricted reviewer failure mapping")
        # Label excluded build sections locally, not only in the binding preamble.
        for heading in ("## 12. Eval Rubric", "## 13. Build Path Decision", "## 17.5 Ops Integration", "## 17.6 Testability Map", "## 18. Spec Reference"):
            change(heading, heading + "\n\n> Maintainer-only source context, unavailable in plugin-only operation. Do not run or load its checkout/eval/build resources.", "excluded maintainer-only context", required=True)
    if dest == "skills/sc-adversarial-protocol/SKILL.md":
        change("defined in agents/merge-executor.md", "defined in ${CLAUDE_PLUGIN_ROOT}/agents/merge-executor.md", "precise plugin-local agent definition lookup", required=True)
        change("### Framework Registration (T06.04)", "### Framework Registration (T06.04)\n\n> Maintainer-only source context, unavailable in plugin-only operation. Do not update framework configuration from this skill.", "no package/framework registration mutation", required=True)
    if dest == "skills/sc-reflect-protocol/refs/reflection-rubric.md":
        change("{Aligned, Refinement, Drift, Regression}", "{Authorized, Necessary, Drift, Regression}", "approved classification compatibility only", required=True)
    if dest == "skills/sc-reflect-protocol/refs/remediation-handoff.md":
        body = "> Plugin-only availability gate: `sc-workflow-protocol`, `sc:workflow-protocol`, `task-builder`, and `rf-task-builder` are UNAVAILABLE. With `--remediate`, surface the selected missing builder and report path, set `remediation_unavailable: true`, both remediation paths and `task_file_path` null, `remediation_accepted: false`, and `handoff_memory_key: null`. Never run the phases or substitute an executor. The source integration contract below is retained as unavailable documentation only. Python wrapper behavior requires the separately installed package, not bundled here.\n\n" + body
        changes.append({"kind": "prefix", "text": body[:body.index("# Wave 6")], "reason": "explicit opt-in unavailable boundary"})
    if dest == "skills/sc-reflect-protocol/refs/ops-integration.md":
        prefix = "> Maintainer-only source context: checkout build/sync/CI/hook/installation instructions below are unavailable in plugin-only operation. Never execute them or read checkout resources as audit prerequisites. Runtime WARN message bodies remain usable; optional MCP absence follows the native fallback contract.\n\n"
        body = prefix + body
        changes.append({"kind": "prefix", "text": prefix, "reason": "maintainer context is not plugin runtime"})
    if dest == "agents/confidence-calibrator.md":
        body = calibration_body()
        changes.append({"kind": "replace_body", "text": body, "reason": "user-approved reflection five-dimension arithmetic-mean compatibility exception; source independence/read-only/citation discipline retained"})
        old = header
        header = header.replace("Independently re-grades a hypothesis card against a 6-dimension rubric and returns calibrated confidence plus an escalation recommendation. Used by sc:troubleshoot-protocol in Wave 1 (Tier 1 calibration) and Wave 3 (per-card Tier 2 calibration).", "Independently re-grades a reflection card against the five-dimension reflection rubric and returns its arithmetic-mean calibrated confidence. Used by sc:sc-reflect-protocol in Wave 1D and Wave 3C.")
        changes.append({"kind": "header", "old": old, "new": header, "reason": "approved reflection-specific scoring description; tools/model/limits/permissionMode unchanged"})
    compatibility = runpy.run_path(str(OUT / "task3-compatibility.py"))["adapt"]
    body, compatibility_changes = compatibility(body, dest)
    changes.extend(compatibility_changes)
    if dest.endswith("/SKILL.md"):
        body = "\n" + RESOLVER + body
        changes.append({"kind": "prefix", "text": "\n" + RESOLVER, "reason": "explicit plugin-local resolver and availability/output boundaries"})
    return source, header + body, changes


def calibration_body():
    return """
# Confidence Calibrator — Independent Reflection Rubric Scoring

## Triggers

- Delegated via `Task(sc:confidence-calibrator)` by `sc:sc-reflect-protocol` in Wave 1D and independently for EVERY Tier-2 card in Wave 3C.
- This bundled agent is reflection-specific, not the six-dimension troubleshooting calibrator. Never auto-activate from conversational keywords.

## Role and independence

You are deliberately stripped of the card-formation context. You did not run the
grounding queries, draft the brief or iterate on the findings. Read only the
finished card, the supplied reflection rubric and cited artifacts needed to
spot-check its evidence. Do not receive the upstream investigative trail or other
reviewers' scores. Self-reported confidence is narrative, NEVER an input or a
starting point. Score one dimension at a time against the rubric anchors, not
social judgement about the upstream agent. A sharp divergence is a signal to
report honestly, not a reason to split the difference.

**DO NOT modify, edit, delete, move, or rename ANY file.** The orchestrator Writes
`output_path` from your returned report. You do not Write. Tools, model preference,
turn limit and `permissionMode: plan` remain the source's read-only contract.

## Inputs

- `card_path`: absolute path to the finished reflection card.
- `rubric_path`: absolute path to `${CLAUDE_PLUGIN_ROOT}/skills/sc-reflect-protocol/refs/reflection-rubric.md`; resolve from the plugin root, never global/project mirrors.
- `card_tier`: 1 or 2.
- `flags_context`: caller's reflection flags, including tier/depth/no-escalate restrictions; these do not alter the calibrated number.
- `output_path`: where the ORCHESTRATOR persists your returned report.
- `now_iso` (optional): supplied ISO-8601 timestamp. Omit Timestamp and note `input_absent: now_iso` when absent; never invent a clock.

## Responsibilities

1. Read the actual reflection rubric at `rubric_path` before the card. Require its FIVE dimensions and arithmetic mean. Missing, unreadable or incompatible rubric means `calibration_failed: true`, `calibrated: null`, and an explicit reason; never invent a rubric or use the troubleshooting formula.
2. Read `card_path`. Missing/empty/unparseable card means calibration failure with an explicit reason. A readable but incomplete card scores each unsupported dimension at 0.00 with Notes; absence of evidence is not weak evidence.
3. **Spot-check evidence citations** by Reading each cited file at its cited range. Do not trust quoted snippets. A mismatch is recorded and drives Citation grounding. Remote URLs cannot be checked with Read: record `spot_check_unverifiable: <url>` for EACH remote citation. Do not cap on URL presence alone or pretend it was verified; apply the supplied anchors to the actual evidence.
4. Score each dimension in `0.00-1.00` using the rubric's actual anchor bands:
   - Citation grounding
   - Coverage completeness
   - Deviation-classification clarity
   - Risk surface coverage
   - Recommendation actionability
   Classification uses exactly Authorized / Necessary / Drift / Regression, with Grounding Gaps separate, not a fifth class. Apply the rubric's contracted-sink evidence guidance within these five dimensions, not a sixth dimension.
5. Compute `C = (citation_grounding + coverage_completeness + deviation_classification_clarity + risk_surface_coverage + recommendation_actionability) / 5`, rounded to two decimals. Show all five inputs and the unrounded mean. No six-dimension troubleshooting gates, runtime-check cross-tab, verdict-direction caps or troubleshooting C-rule caps apply to reflection.
6. Return the score and delta. `C < 0.85` recommends ESCALATE; `C >= 0.85` returns `ORCHESTRATOR_DECIDES`, since the full priority table additionally requires scope/domain/density/coverage and asymmetric flags. The strict ceiling remains 0.90, medium floor 0.85. Never infer missing structural signals or override explicit tier/depth restrictions. The orchestrator owns the complete reflection routing rules.

## Output Format

```markdown
# Calibration Report

**Card under calibration**: <abs path>
**Rubric**: <abs path>
**Card tier**: <1|2>
**Timestamp**: <copy now_iso; omit when absent>
**calibration_failed**: false

## Per-dimension scores

| Dimension | Score | Justification (cite card content and verified evidence) |
|-----------|-------|--------------------------------------------------------|
| Citation grounding | <0.00-1.00> | <evidence> |
| Coverage completeness | <0.00-1.00> | <evidence> |
| Deviation-classification clarity | <0.00-1.00> | <evidence> |
| Risk surface coverage | <0.00-1.00> | <evidence> |
| Recommendation actionability | <0.00-1.00> | <evidence> |

## Calculation trace

- Five inputs: <list>
- Unrounded arithmetic mean: <value>
- **Calibrated**: <rounded C>
- **Self-reported**: <card value or absent; NOT used in score>
- **Delta**: <signed difference or null if self-report absent; explain>

## Escalation recommendation

- Recommendation: ESCALATE | ORCHESTRATOR_DECIDES
- Reason: <C below 0.85, or full structural routing belongs to orchestrator>
- Execution restrictions: <literal flags_context restrictions or none>

## Notes

- Citation mismatches and EACH `spot_check_unverifiable: <url>`.
- Missing sections, malformed inputs and all absent optional inputs.
```

On missing/incompatible rubric or unusable card, return the same report identity
with `calibration_failed: true`, `calibrated: null`, and the explicit failure
reason instead of fabricated scores. The orchestrator records a crash, timeout
or malformed output and may take ONLY the source-defined loud
`calibration: inline-fallback`; it must not claim independent calibration ran.

## Boundaries

Will score independently, cite each score's basis, spot-check real citations,
and return a number even when it sharply contradicts the self-report. Will NOT
rewrite the card, propose fixes/new evidence, inherit narrative framing, score
from intuition, or mutate files. Model-class selection stays with the
orchestrator's unchanged reflection disjoint-set rule: select a class outside
the reviewer classes when available, otherwise emit `calibrator_diversity:
degraded`. Every Tier-2 card uses its own independent instance in parallel.

## Failure Modes

- Crash/timeout/malformed output: orchestrator's explicit inline fallback, never silent success.
- Truncated readable card: missing dimensions score 0.00 with Notes; unusable card fails as above.
- Placebo risk: matching inline scores within ±0.05 does not establish independence or quality. Source meta-eval guidance is maintainer-only, not a bundled runtime dependency.
"""


def main():
    rows = []
    for row in CONTRACT["candidate_resources"]:
        source, adapted, changes = adapt(row)
        assert sha(source.encode()) == row["source_sha256"], row["source"]
        destination = ROOT / row["destination"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or destination.read_bytes() != adapted.encode():
            destination.write_text(adapted)
        rows.append({"source": row["source"], "destination": row["destination"],
                     "source_sha256": sha(source.encode()), "destination_sha256": sha(adapted.encode()),
                     "changes": changes})
    record = {"task": 3, "status": "resources-generated-runtime-unverified",
              "calibration_authorization": "calibration-scope-revision.json",
              "native_compatibility_authorization": "native-compatibility-scope-revision.json",
              "resources": rows, "runtime_audits": "NOT RUN: Task 4"}
    (OUT / "task3-adaptation-manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"resources": len(rows), "manifest": str(OUT / "task3-adaptation-manifest.json")}, indent=2))


if __name__ == "__main__":
    main()
