"""Apply only the three additional user-approved native compatibility repairs."""

from pathlib import Path

OUT = Path(__file__).resolve().parent

BRIEF_RULES = """## Native snapshot handoff (required before reviewer dispatch)

Consume the REAL `native-selected-inputs` snapshot and its verified provenance
manifest from SKILL.md Step 0.5e. Never set `reviewer_grounding_root` to the live
checkout, the output parent, or an unpopulated directory. The snapshot captures
the selected current working-tree bytes, including relevant dirty tracked and
untracked/new files, not only a committed revision. Do not use or claim the
separately unavailable Python wrapper's `snapshot-children-only` isolation.

Keep exactly the three brief sections below. Put the snapshot-root path,
provenance-manifest path, `snapshot_kind: native-selected-inputs`, and a
`source_path -> snapshot_path` map in the existing **Grounding hunks** section,
not a fourth section. Rewrite ALL reviewer-facing paths, including `spec_path`,
optional `tasklist_path`, task-log, diff evidence, prior reports, T1-card excerpt
citations, verification/hierarchy/runtime ledgers, coverage citations and linked
evidence, through that manifest. Excerpts remain verbatim apart from mechanical
citation-path relocation. Preserve original locations in the provenance map for
later report rendering. A missing mapping blocks dispatch: expand the selected
set and create a NEW frozen snapshot, never point back at the live tree.

The brief permits native Read/Grep/Glob ONLY within the snapshot root. MCP calls
are permitted only when the orchestrator has verified that their actual project
or index root is this exact snapshot. Otherwise prohibit live-root MCP lookups
and use native Read/Grep/Glob with `reviewer_grounding_degraded:
["snapshot-mcp-unindexed"]`; never query the live project or claim symbolic
coverage that did not run. A needed but uncopied file becomes an explicit
evidence gap, not a live-root escape. Keep the fixed `sc:reflect-reviewer`
tools/permission allowlist unchanged; never replace it with an all-tools agent.
The reviewer RETURNS findings and runs no shell/git commands.

Re-verify snapshot and source hashes immediately before dispatch AND after all
reviewers return. Also recheck the pinned selection-file digest and recompute
scoped audited membership with the identical pinned-output/snapshot and
VERIFICATION_ARTIFACT_EXCLUDES rules. New or removed relevant files invalidate
findings; unrelated out-of-scope work and this run's output/cache artifacts do
not. Never compare whole raw repository status. A mismatch blocks acceptance of those findings and records
input/snapshot drift; retain all evidence. The orchestrator translates returned
snapshot citations back through the verified map only for final report
rendering, then the independent evidence-validator re-Reads the original source
and the manifest. Snapshot citations themselves still resolve on retained disk.

"""

SNAPSHOT_TEXT = """**Step 0.5e (native selected-input snapshot provisioning — L2).** This is the
native plugin route, not the package wrapper. At Wave 0 select/reserve the frozen
input set; at Step 3B.0, AFTER T1/verification evidence exists and BEFORE any fixed
read-only reviewer is spawned, the ORCHESTRATOR provisions the actual snapshot.
Every restricted reviewer requires this gate, even without `--isolate-reviewers`.
The Python wrapper's opt-in git-worktree snapshot and its `snapshot-children-only`
telemetry are unavailable package behavior, NOT proof supplied by this plugin.

1. Apply every pinned-output, explicit-input-overlap, traversal, symlink and plugin
   distribution guard FIRST. Create a fresh run output, never reuse a prior
   snapshot or delete intermediates. Keep snapshot files under this pinned output.
2. Enumerate the COMPLETE selected audit state into `<output>/selected-inputs.json`:
   explicit spec, optional tasklist, task-log/diff file, all in-scope changed files
   from the requested ref/diff, relevant dirty tracked files, relevant untracked/new
   files discovered from scoped `git ls-files --others --exclude-standard` and the
   task log, linked evidence and needed dependency sources. Include existing/base
   evidence for deletions as captured diff/base artifacts; do not invent a current
   deleted file. Do not infer that `git diff` includes new files. Resolve narrowing
   scope against both changed paths AND new/log-declared paths. Freeze all files a
   reviewer may cite or inspect, not just the hunks. Missing/unreadable inputs or an
   incomplete enumeration block reviewer dispatch. Never copy `.git` or plugin
   distribution directories wholesale.
3. Schema: `{"enumeration_complete": true, "coverage_basis": "<requested diff,
   scope, dirty/new discovery and links>", "discovery": {"scopes": ["<repo-relative
   audited path>"]}, "files": [{"source": "<absolute path>",
   "kind": "audit-input" | "run-evidence"}]}`. `run-evidence` is ONLY this run's
   already-written T1 card, coverage matrix, captured verification/base/diff and
   other ledgers under the pinned output; it is not an explicit user input and is
   not added to the audited input-tree hash. Every explicit user input stays
   subject to the original output/input overlap guard. Do not include the snapshot
   itself or later reviewer outputs in the selection. Supply the exact selection
   path to the recipe below. Discovery scopes are REQUIRED literal repository-relative
   paths derived from the declared audit scope (or explicit selected source parents
   when no scope was supplied), not a whole-repo status shortcut. The recipe pins
   this metadata, auto-includes current regular tracked/untracked files in those
   scopes, and records missing tracked paths as membership evidence. It excludes
   only the pinned output subtree, selection metadata, and the unchanged
   VERIFICATION_ARTIFACT_EXCLUDES floor from discovery, never explicit inputs.
   Capture current working-tree bytes, not HEAD-only.
4. Use the following stdlib recipe INLINE through native Bash, for example
   `uv run --no-project python - <repo-root> <pinned-output> <selection-json>` with
   the code block as stdin. It imports no package, installs nothing and writes no
   new production module. `uv` and `git` must actually be available to this
   orchestrator; otherwise report snapshot provisioning unavailable and STOP
   reviewer dispatch, never fall back to live roots. The recipe refuses stale
   output, symlinks and missing/non-regular inputs, captures before/copy/after
   SHA256 plus source Git inventory, retains a provenance manifest, and makes
   frozen copies read-only. A nonzero exit or non-verified manifest blocks dispatch.
5. Supply `reviewer_grounding_root: <output>/reviewer-snapshot/root` and
   `snapshot_kind: native-selected-inputs`, `native_reviewer_snapshot: verified`,
   `native_reviewer_snapshot_manifest_path: <output>/reviewer-snapshot/provenance-manifest.json`
   to every brief per `refs/reviewer-spec.md`. Do NOT emit wrapper
   `reviewer_isolation: snapshot-children-only`. Rewrite every source/evidence path
   through the manifest; no live-root fallback. An unindexed snapshot uses native
   Read/Grep/Glob with a loud MCP-unindexed degraded marker.
6. Run this SAME inline recipe with
   `uv run --no-project python - --verify <provenance-manifest>` immediately before
   dispatch and after reviewers finish. This re-Reads the original selection file,
   checks its pinned SHA256 and discovery metadata, recomputes the SAME scoped
   inventory/exclusions, compares additions/removals, and then validates all
   source/copy rows. No raw whole-repository status comparison. Selection,
   scoped-membership, source or frozen-copy hash mismatch means
   `input_drift` / `native_snapshot_drift`, `status: partial`, no acceptance of those
   reviewer findings and no promotion. Keep failed snapshots and intermediates;
   choose a new run/output for retry. No teardown deletion or package wrapper.

<!-- native-snapshot-recipe:start -->
```python
{recipe}
```
<!-- native-snapshot-recipe:end -->

"""


def adapt(body, destination):
    changes = []

    def replace(old, new, reason, expected=1):
        nonlocal body
        count = body.count(old)
        assert count == expected, (destination, old[:100], count)
        body = body.replace(old, new)
        changes.append({"kind": "literal", "old": old, "new": new, "count": count,
                        "reason": "native-compatibility-scope-revision.json: " + reason})

    if destination in ("skills/sc-reflect-protocol/SKILL.md", "skills/sc-reflect-protocol/refs/input-resolution.md"):
        replace("Neither `--spec`, `--tasklist`, nor `--diff` provided.",
                "None of `--spec`, `--tasklist`, `--diff`/`--commit-range`, or `--task-log` provided.",
                "generic no-input STOP accepts the supported log-only post input")
        replace("**`--diff` OR `--commit-range`** flag present", "**`--diff`, `--commit-range`, OR `--task-log`** flag present",
                "post-mode evidence is diff OR task log")
        replace("with no `--diff` AND no `--task-log`", "with no `--diff`, no `--commit-range`, AND no `--task-log`", "every post hard guard accepts all three declared evidence alternatives", expected=2 if destination.endswith("/SKILL.md") else 1)
        if destination.endswith("/SKILL.md"):
            replace("or path to a diff file (required for UC-2)", "or path to a diff file (UC-2 requires this OR `--task-log`)", "post minimum declaration")
            replace("`--task-log <path>` — task execution log (optional, UC-2 only)", "`--task-log <path>` — task execution log (UC-2 only; required when no diff/commit-range is supplied)", "post minimum declaration")
            replace("(1) the `tasklist_path` itself (always present in UC-2);", "(1) the `tasklist_path` itself (when supplied), plus `task_log_path` and a `--diff` file when supplied;", "optional tasklist and actual post evidence participate in snapshot")
            replace("(first two entries of `file_list`)", "(named entries of `file_list`, null when an optional input is absent)", "optional tasklist hash is not a fabricated mandatory input")
            replace("  tasklist: <hex>\n", "  tasklist: <hex> | null\n", "optional tasklist digest declaration")
            start = body.index("**Step 0.5e (")
            end = body.index("**Step 0.6 (", start)
            old = body[start:end]
            recipe = (OUT / "task3-native-snapshot-recipe.py").read_text().rstrip()
            replace(old, SNAPSHOT_TEXT.replace("{recipe}", recipe), "real native selected-state snapshot provider replaces unavailable wrapper provider")
            replace("reviewers ground in an isolated `git worktree` snapshot, never the live tree", "reviewers ground in a real frozen native selected-input snapshot, never the live tree", "native snapshot mechanism is not a package git-worktree claim")
            replace("Before spawning N reviewers, materialize one brief per reviewer", "Before spawning N reviewers, provision and verify the native Step-0.5e snapshot, rewrite every reviewer path through its provenance manifest per `refs/reviewer-spec.md`, then materialize one brief per reviewer", "mandatory snapshot-grounded brief handoff")
        else:
            replace("Tasklist file. Required for UC-2; recommended for UC-1 if a tasklist already exists.", "Tasklist file. Recommended for UC-2, not required; recommended for UC-1 if a tasklist already exists.", "tasklist recommended, not a post precondition")
            replace("or path to a diff file. Required for UC-2.", "or path to a diff file. UC-2 requires this OR `--task-log`.", "diff-or-log minimum")
            replace("Task execution log. Optional, UC-2 only.", "Task execution log, UC-2 only. Required when no diff/commit-range is supplied.", "diff-or-log minimum")
            replace("Hard-STOP cases that prevent invocation (verbatim from §3.3):", "Hard-STOP cases that prevent invocation (consistent with §3.3):", "adapted minimum is not verbatim stale source")
    if destination == "skills/sc-reflect-protocol/refs/reviewer-spec.md":
        replace("## Brief template", BRIEF_RULES + "## Brief template", "real snapshot path mapping, retained evidence and honest MCP fallback")
    if destination == "skills/sc-adversarial-protocol/refs/debate-protocol.md":
        replace("Qualitative layer (50%): 25-criterion additive binary rubric with CEV protocol", "Qualitative layer (50%): 30-criterion additive binary rubric across six dimensions with CEV protocol. Invariant & Edge Case Coverage is the sixth dimension (5 criteria); variants scoring <1/5 there are ineligible as base, unless ALL variants score 0/5, in which case suspend the floor with a warning.", "summary matches existing scorer, no weight or algorithm change")
    if destination == "skills/sc-adversarial-protocol/refs/artifact-templates.md":
        replace("### Qualitative Summary", "### Invariant & Edge Case Coverage (5 criteria)\n\n| Criterion | Variant A | Evidence | Variant B | Evidence |\n|-----------|-----------|----------|-----------|----------|\n| Addresses boundary conditions for collections (empty, single-element, maximum size) | MET/NOT MET | <CEV evidence> | MET/NOT MET | <CEV evidence> |\n| Handles state variable interactions across component boundaries | MET/NOT MET | <CEV evidence> | MET/NOT MET | <CEV evidence> |\n| Identifies guard condition gaps (missing validation, unguarded type assumptions) | MET/NOT MET | <CEV evidence> | MET/NOT MET | <CEV evidence> |\n| Covers count divergence scenarios (off-by-one, inclusive/exclusive ranges) | MET/NOT MET | <CEV evidence> | MET/NOT MET | <CEV evidence> |\n| Considers interaction effects when features or components combine | MET/NOT MET | <CEV evidence> | MET/NOT MET | <CEV evidence> |\n| **Subtotal** | **<N>/5** | | **<N>/5** | |\n\n### Edge Case Floor Check\n\nVariants scoring <1/5 on Invariant & Edge Case Coverage are ineligible as base variant. When ALL variants score 0/5, suspend the floor with a warning, per `scoring-protocol.md`.\n\n| Variant | Sixth-dimension subtotal | Eligible | Floor suspended with warning |\n|---------|---------------------------|----------|------------------------------|\n| A | <N>/5 | yes/no | yes/no |\n| B | <N>/5 | yes/no | yes/no |\n\n### Qualitative Summary", "actual sixth scorer dimension and its unchanged eligibility floor in artifact scaffold")
        replace("| **qual_score** | **<N>/25 = <score>** | **<N>/25 = <score>** | ... |", "| Invariant & Edge Case Coverage | <N>/5 | <N>/5 | ... |\n| **qual_score** | **<N>/30 = <score>** | **<N>/30 = <score>** | ... |", "existing /30 denominator, no scoring weight change")
    if destination == "skills/sc-adversarial-protocol/SKILL.md":
        replace("Full 25-criterion qualitative rubric with CEV", "Full 30-criterion qualitative rubric with CEV", "exact stale forward-pass count, CEV/algorithm unchanged")
        replace("Same 25-criterion rubric with CEV (independent evaluation)", "Same 30-criterion rubric with CEV (independent evaluation)", "exact stale reverse-pass count, independence/algorithm unchanged")
    return body, changes
