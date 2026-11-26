# Shadow-run architecture analysis

Structure: analyze skeleton registered in ../../450/report-template.md, derived from the loaded analyze command.

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/531/analyze`.

The CLI directory is the narrowest common source directory covering the review-manifest helpers, reflect adapter and evaluation scheduler named by issue 531. Only these relevant subpackages were inspected in detail, not the entire CLI. Supporting reads cover reflect's prose adapter, its exit script, tests and the recorded experiment.

Codegraph: index_state=fresh, checked_at=2026-11-24T02:44:12Z; degraded: graph:truncated.
Access: mcp. Worktree: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup. The capped caller lookup showed 5 of 36 rows; no absence-of-callers conclusion is drawn. No source changes or model runs were made.
## Architecture and metrics
- Indexed layout: 254 files in the requested CLI view (238 Python, 16 YAML). These are discovery counts, not review coverage or test results.
- Reflect's opt-in shadow path is prose-driven, not a general shadow-job executor. Legacy owns the verdict, and shadow reuses the legacy reviewer dispatch while collecting panel artifacts: `src/superclaude/skills/sc-reflect-protocol/SKILL.md:338-349`, especially step 3 at line 342.
- The review manifest is a local persistence building block with nine fixed stages, review engine names and three publication filenames: `src/superclaude/cli/review/manifest.py:38-63`. Its CLI fixes the path to `panel/manifest.json`: `src/superclaude/cli/review/manifest_cmd.py:19-20`.
- Non-interference has code support: `publish_files` rejects shadow before touching authoritative files, while `hash_published_files` reads their hashes: `src/superclaude/cli/review/manifest.py:476-534`. A rejection assertion exists at `tests/review/test_review_manifest.py:323-326`; not executed here.
- Evaluation scheduling runs an injected worker once per spec with configurable concurrency clamped to 1-15, cancellation and disk-budget handling: `src/superclaude/cli/eval/orchestrator.py:110-198`. However, the default CLI executor factory still returns `_NullLifecycleExecutor`: `src/superclaude/cli/eval/commands.py:1386-1405`. That execution wiring is STUBBED, not a ready experiment service.
- Review telemetry describes local JSONL/SQLite records, not a central upload service: `src/superclaude/cli/review/telemetry.py:1-19,30-80`.
- Exit measurement is explicitly a file-only, reflect-specific aggregator requiring 20 published runs by default; it does not schedule runs: `scripts/reflect_shadow_exit.py:2-34,55-57`.
## Severity-rated findings
1. **P2, missing feature:** no general central percentage gate, command-variable fetcher, central uploader or continuous experiment queue was identified. Existing behavior is explicit opt-in and review-specific bookkeeping, not centrally controlled arbitrary pipeline variations. Evidence: reflect steps at `src/superclaude/skills/sc-reflect-protocol/SKILL.md:338-349`; fixed stages at `src/superclaude/cli/review/manifest.py:38-63`; search limits below.
2. **P2, reuse constraint:** recommending the eval CLI as a working execution backend would be false while its factory returns a null implementation (`src/superclaude/cli/eval/commands.py:1386-1405`). Issue 487 is an architectural overlap to resolve before adding a competing scheduler.
3. **P2, measurement gap:** dispatch and the authoritative verdict are shared with legacy (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:338,342`). The recorded five-combination experiment states no blind quality scoring was performed (`.dev/eval-workspaces/shadow-model-combos/FINDINGS.md:1-3,40-42`). Published records do not establish which variation produces better reviews.
4. **Design safety requirement, not a discovered vulnerability:** centrally supplied prose, real developer inputs and uploaded results need an explicit authorization, privacy and spend boundary. Local writer isolation (`src/superclaude/cli/review/manifest.py:491-500`) does not define that future central-service boundary.
## Recommendations and roadmap
Keep issue 531 open as still-relevant. First settle the contradictory gate rule, supported commands and trust/privacy/cost boundary. Then decide reuse with issue 487: shared execution, queue and results infrastructure there versus a thin on-command sampling adapter here; this split is a recommendation, not an approved design. Reuse existing manifest and scheduler ideas where their contracts fit. Before rollout, check probability endpoints, offline behavior, variable validation, isolated prose copies, real execution, run-count/parallel caps and safe result uploads.
## Verification limits
Static quick-depth pass only. Tests, model calls and end-to-end execution were not run. No runtime performance, security-vulnerability count or coverage percentage is asserted.

Negative evidence: `**/*shadow*` filename discovery found the reflect script/tests and development experiments, not a general distributable module. CLI-wide `shadow|experiment` and source-wide `shadow|experiment|gate[_-]?percent|sampling[_-]?rate` searches found review/reflect, watcher, swarm and unrelated references, not issue 531's full flow. A broader probability/sampling/queue search had generic matches and a capped response; it is not proof that no differently named mechanism exists. No `lab` package appeared in the indexed CLI layout. Unmerged-branch implementation remains UNVERIFIED.

Issue 531 and all returned comments were read, as were PRs 519 and 581. Full non-comment timeline events are UNVERIFIED: the allowed `gh issue view/list` surface exposes no timeline field. An initial combined `--comments --json` read failed because this CLI refuses those flags together; the successful JSON retry included `comments`. Freshness hooks also refused the first report Edits until the stubs were explicitly Read; no source or GitHub mutation resulted from either failure.
