---
name: reflect
description: "Pre-execution coverage and post-execution deviation audits with independent calibration, restricted heterogeneous reviewers, real adversarial merge, and citation validation"
category: analysis
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily]
personas: [analyzer, qa, refactorer]
argument-hint: "[--mode pre|post] [--spec <path>] [--tasklist <path>] [--diff <ref-or-path>|--commit-range <range>|--task-log <path>] [--scope <path>] [--tier 1|2|auto] [--depth quick|standard|deep] [--reviewers 2|3] [--output <dir>] [--no-mcp] [--no-promote] [--remediate] | legacy: --type task --analyze|--validate with real inputs"
---

# /sc:sc-reflect - Tiered Reflection and Validation

## Purpose and activation

Audit a proposed plan against its driving specification (pre), or completed work
against its specification/tasklist and actual evidence (post). This is an audit,
not a generic session summary or a self-confirming completion claim. The physical
command filename is retained; its native frontend is `/sc:sc-reflect`.

**MANDATORY:** Invoke `Skill sc:sc-reflect-protocol` with the resolved arguments
before executing the audit waves. The bundled implementation is
`${CLAUDE_PLUGIN_ROOT}/skills/sc-reflect-protocol/SKILL.md`. Never load a global
framework copy, project development mirror, checkout source tree or package
wrapper. All `refs/...` reads are relative to that bundled skill directory.
The command's validation and return obligations below bind that handoff; this
file does not replace or reimplement the protocol's debate/scoring machinery.
In the protocol, logical `Task` delegation means the client's native Agent tool,
using the exact registered plugin-qualified subagent type and model slot.

## Native audit-root binding

Resolve `audit_repo_root` from the explicit scope/input paths, never from the
plugin's location or a shell cwd used to read plugin resources. For Git inputs,
use the nearest actual Git root of the selected scope/input directory through a
read-only `git -C <directory> rev-parse --show-toplevel`. For a standalone pre
review without Git, use the explicit input set's common directory. Record that
root and the actual selected inputs in the audit log before delegation.

EVERY Agent brief, including adversarial advocates, fault-finders, scorers and
merge-executor, must carry this root, its allowed input/snapshot roots, output
root and the required plugin-resource root. Propagate the same boundary through
secondary handoffs. Missing configuration in the audited repository is an
explicit absence/gap: never fill it by reading an ancestor checkout's
`pyproject.toml`, `CLAUDE.md`, development mirrors, or package resources. Keep
shell cwd at the launch directory or the selected audit root; read plugin assets
by absolute path rather than changing cwd into their containing checkout.
Restricted reviewers retain the stricter frozen-snapshot-only boundary.

Pass an explicit available model slot whenever model class is load-bearing, and
record the actual returned provider model as well as the requested slot. An
omitted Agent model inherits the caller; it is not evidence of a Sonnet slot.
For Tier 1, prefer a Sonnet-slot card author and an available disjoint calibrator
(Opus when those configured aliases differ), then retain the protocol's actual
alias, executor exclusion and degraded-diversity rules. Tier-2 card calibration
must still use a class outside the reviewer set when available; never invent a
fourth model when the three configured slots are already reviewers.

## Input and mode resolution

- **Pre:** `--spec <path>` is required. `--tasklist <path>` is recommended.
- **Post:** supply `--diff <ref-or-path>`, `--commit-range <range>`, OR
  `--task-log <path>`. A tasklist and driving spec are recommended, not mandatory.
- `--commit-range` is a diff-source alternative BEFORE every hard input guard.
  Resolve genuine Git refs read-only; do not invent commits or substitute another
  range. A supplied diff file is read as evidence, not applied to the repository.
- An explicit `--mode pre|post` wins. Otherwise the bundled six-rule first-match
  resolution applies: diff/range/task-log implies post; modified scope and
  completed-artifact combinations may imply post; spec with a proposed tasklist
  (or spec alone for coverage-only review) implies pre. Unresolved mode STOPs.
- Read and validate every supplied input path. An empty, unreadable or unresolved
  input is not evidence. Under-specified deep inputs must STOP rather than invent
  work to review. No spec/tasklist/diff/range/task-log means STOP.
- Pre without a spec STOPs. Post without any of diff/range/task-log STOPs.
  Merely providing a tasklist or spec does not satisfy a post audit.

### Supported legacy task mapping

| Legacy flags | Resolved mode | Real inputs still required |
|---|---|---|
| `--type task --analyze` | `--mode pre` | `--spec`; proposed tasklist recommended |
| `--type task --validate` | `--mode post` | diff, commit-range, or task-log; tasklist recommended |

The words `session` and `completion` are not supported `--type` values. Neither
legacy flag pair authorizes an input-free audit. Reject ambiguous analyze AND
validate. When modern and legacy mode flags conflict, STOP and report the
conflict and ignored legacy flags; do not silently audit the wrong mode.

## Output and input safety (before any write)

Resolve the output through its nearest existing ancestor and pin that realpath
for the run. Use `.dev/reflect/<mode>-<slug>-<timestamp>/` unless `--output <dir>`
is supplied. Reject `..` components, symlink escapes, and any output that equals
or contains an explicit input or the audited work-unit root. Compare resolved
path components, never string prefixes. Prior reports used as inputs require a
fresh run directory, never overwriting their evidence. Retain the protocol's
input-tree hash and drift checks and its precise current-output/cache exclusions.

Refuse output in `.claude/skills`, `.claude/agents`, `.claude/commands`, or equal
to, inside, or containing any plugin distribution directory:
`${CLAUDE_PLUGIN_ROOT}/skills`, `${CLAUDE_PLUGIN_ROOT}/agents`,
`${CLAUDE_PLUGIN_ROOT}/commands`, `${CLAUDE_PLUGIN_ROOT}/.claude-plugin`.
Do not create a forbidden directory or artifact to report its refusal.
For precondition refusal, return a truthful stopped-precondition result inline;
write a refusal contract only if an independently safe output is available.

## Audit flow and native role binding

1. **Ground the inputs and evidence.** Load the needed bundled refs on demand.
   Build the real spec-to-task coverage map for pre, or task/spec-to-work map and
   four-category deviation register for post. Read actual cited files, not just
   summaries or commit messages. Authorized / Necessary / Drift / Regression are
   the four classes; insufficient evidence goes to the separate Grounding Gaps.
2. **Always run Tier 1.** Use `sc:sc-requirements-analyst` for coverage and
   `sc:sc-root-cause-analyst` or `sc:sc-self-review` for a grounded card as directed
   by the protocol. Persist the actual card before calibration.
3. **Independent blind calibration.** Invoke `sc:confidence-calibrator` on the
   finished card and bundled five-dimension reflection rubric, without formation
   context. Persist its returned scores and arithmetic mean. Choose a model class
   outside the reviewer class set when available; honestly mark degraded
   diversity when not. Never label inline scoring independent calibration.
   **Blind does not mean evidence-blind:** the card and rubric are the supplied
   inputs, but the calibrator MUST independently Read the card's cited artifacts
   at the cited ranges, within the bound audit/snapshot roots, before scoring
   Citation grounding. Say this explicitly in EVERY calibration assignment.
   Never instruct it to read "only those two files" or forbid citation checks.
   Exclude the formation trail and other reviewers' scores, not the real evidence
   the finished card cites. Persist its actual citation spot-check results and
   five scores; missing/unreadable evidence is recorded honestly, not verified.
4. **Tier routing.** Default `--tier auto` and `--depth standard` use the actual
   calibrated confidence and structural rules. `--tier 1`/`--depth quick` pins
   Tier 1; `--tier 2`/`--depth deep` forces the supported Tier-2 path. Keep the
   source thresholds, budget constraints, executor exclusion and disjoint-set
   rules. Do not silently satisfy forced Tier 2 with an inline single pass.
5. **Tier 2 when reached.** Spawn 2-3 distinct model-class reviewers as the fixed
   **`sc:reflect-reviewer`** type with brief-supplied personas, never all-tools
   specialist substitutes. Provision the REAL native selected-input snapshot
   using the bundled inline recipe first, including relevant dirty/new files and
   pinned scoped membership/hash checks before dispatch and after review. Rewrite
   all brief paths through its provenance manifest. A snapshot that is not MCP
   indexed uses native Read/Grep/Glob with an explicit degraded marker, never
   live-project MCP lookup. Keep reviewers read-only; the orchestrator persists
   their returned findings. Independently calibrate EVERY reviewer card.
6. **Real adversarial merge.** Invoke `Skill sc:sc-adversarial-protocol` in Mode A
   with the calibrated cards. `sc:debate-orchestrator` coordinates actual
   advocates/debate/scoring and `sc:merge-executor` executes its actual merge plan.
   Consume the producer's `artifacts_dir` as `adversarial_artifacts_dir`. Verify the
   returned merged file on disk; render/persist the merged verdict as
   `<output>/adversarial/merged-verdict.yaml` with `merge_method: adversarial`
   from that actual result, never inventing convergence or replacing debate with
   inline consensus. Honor the protocol's parse/missing-file/MALFORMED retry and
   loud F1/F2/F3 fallback contracts. Fallback is not successful adversarial proof.
7. **Mandatory final evidence gate.** Synthesize the bundled report template,
   then invoke **`sc:evidence-validator`** on the real draft to re-Read citations.
   Persist its returned validation, drop unfounded citations, recompute affected
   coverage, and apply the protocol's partial/vacuous-success rules. Only then
   finalize `REPORT.md` and the versioned `return-contract.yaml`. A missing or
   crashed validator uses only the loud source-defined partial fallback, never a
   fabricated independent pass. Use `sc:confidence-check` before actionable chat
   recommendations.
8. **Return actual results.** Surface report/contract paths, resolved mode, tier,
   calibrated confidence, pre coverage or post class counts, citation drops,
   degradation/grounding gaps, merge method and promotion/remediation disposition.
   Persist the step audit log and role/model/calibration/merge artifacts required
   by the bundled contract. A native process exiting zero is not an audit verdict.

## MCP absence, remediation and mutation boundaries

MCP integrations are optional. With `--no-mcp` or absent exposed MCP tools, use
native Read/Grep/Glob, skip unavailable memory/diagnostic/verification/research
capabilities, and emit the corresponding loud degraded/partial/grounding-gap
result. Do not claim unperformed symbolic, dynamic or external verification.
The Serena `think_about_*` tools are optional checkpoint signals, never the sole
reflection mechanism or a hard installation prerequisite.

Without `--remediate`, never enter Tier-3 handoff. This plugin does NOT bundle
`sc-workflow-protocol`, `task-builder`, `rf-task-builder`, `tech-research` or
`audit-validator`. Optional spot-check auditing uses the stricter bundled
`sc:evidence-validator` fallback. An explicit remediation request must report
`remediation_unavailable: true`, name the missing selected builder, retain the
report and set `remediation_task_path`, `remediation_plan_path`, `task_file_path`
and `handoff_memory_key` to null, `remediation_accepted: false`. No substitute plan,
installation, corrective executor, `/task`, or `/sc:sc-implement` is launched.

Waves 0-6 are read-only outside the output. `--no-promote` suppresses Wave 7; honor
it without moves, archive writes or mutation. Otherwise promotion follows ONLY
the bundled strict gate, collision, hash and explicit override rules. Never
stage, commit, push, or auto-execute remediation as part of reflection.

## Separate package readiness surface

Detection-contract readiness is NOT a pre/post audit. Its separate command is
`superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>`.
It requires the separately installed **`superclaude` package executable**, which
this plugin does not bundle. If absent, report readiness UNAVAILABLE and do not
run an audit, import package code, install anything or impersonate the CLI.
That readiness surface diagnoses/validates existing evidence only; it does not
arm a monitor, modify PR state, push, reply, resolve, retrigger or dump raw payloads.

## Examples

```text
/sc:sc-reflect --mode pre --spec spec.md --tasklist proposed.md --tier 1 --no-promote
/sc:sc-reflect --mode post --diff changes.patch --spec spec.md --tier 1 --no-promote
/sc:sc-reflect --mode post --task-log execution.log --no-promote
/sc:sc-reflect --mode post --commit-range <real-range> --no-promote
/sc:sc-reflect --mode post --diff changes.patch --tier 2 --reviewers 2 --no-promote
/sc:sc-reflect --type task --analyze --spec spec.md --tasklist proposed.md --no-promote
/sc:sc-reflect --type task --validate --task-log execution.log --no-promote
```
