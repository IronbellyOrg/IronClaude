# Remediation: Gateway tier contexts and picker duplicates

Goal: Apply the fix described in /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker/.dev/troubleshoot/bug-ensure-the-850k-limit-of-20261106114037/REPORT.md.

## Summary

Issue408: bare tier aliases exported for opus/sonnet/haiku select200k in Claude Code while gateway Tier[1m] entries obtain their configured larger windows; default aliases and custom profile options duplicate gateway rows. Installed runtime2.1.318 controls reproduce bare200k,suffixed850k and native modelPicker replacement leaving only Default+curatedTier rows. Normalize repository-controlled tier selections to context-capable spelling, retain original routing alias identity, recognize tier IDs for named-model context resolution, and use the existing ACTUAL curated shim list with native picker replacement. No user-global settings, gateway changes or runtime patch. Do not promise to fix manually typing a bare ID in a running Claude Code session; document external limit. Preserve explicit +models/show-all and explicit individual-model selection routing; do not silently reroute a GPT selection to a tier. Coordinator explicitly approved this scope and separately authorized the eventual /sc:implement command after reading plan/check.

## Files

- src/superclaude/skills/ccsession-tag/ccsession: access-aware context-capable alias exports and compose picker settings after real shim curation/warm-up; preserve per-model settings and compact overrides.
- src/superclaude/skills/ccsession-tag/models.py: bare/suffixed tier-ID context resolution before model-slot fallback, preserve actual window and access checks.
- tests/unit/test_ccsession_tiers.py: extend existing launcher harness and parameterized regressions, no new dependency.
- Do not change other source files unless root-cause integration genuinely requires it and coordinator approves expanded scope. Do not edit another worktree. Run make sync-dev from canonical source; never stage generated .claude mirrors.

## Acceptance

- All configured tiers (including0,1a,1b,2) preserve their own T<N>_WINDOW: observed workspace850000/850000/850000/500000, never hardcode850k universally. Bare and suffixed named tier launches resolve to same intended window and normalized context-capable selected spelling; limited-owner forbidden tiers still reject.
- Access-aware opus/sonnet/haiku exports resolve to their existing allowed tier with context capability; unavailable tier variables preserve inherited values. Non-tier behavior unchanged.
- Ordinary tier-only mode shows Default plus exactly the actual curated gateway Tier rows with their labels/descriptions; no default-alias custom rows, no unrelated GPT custom profile row. Preserve explicit show-all/+models individuals; native runtime can re-add an explicitly selected individual outside list, document rather than reroute.
- Reuse actual curated shim model rows after synchronous warm-up; do not duplicate model-label/curation policy in another path. Preserve graceful warm-up failure and no stale foreign-base cache use. Native picker settings merge with existing inline compaction settings on all tier paths, including CCSESSION_COMPACT_WINDOW override; user --settings precedence remains unchanged.
- Smallest runnable regression for every tier alias/window and picker exactness plus restricted owner/show-all/compactoverride edge cases using existing tests. Include alias routing boundary proof (existing shim gets bare routing ID after CC context suffix handling); do not claim request routing preservation from a comment alone.
- Execute uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py tests/skills/test_model_alias_policy.py and record observed pass/fail output; baseline tiers147passed beforefix. Add no dependency. Run targeted lint/format checks and make sync-dev/make verify-sync.
- Repeat installed-runtime tool-free restricted controls using repo-produced configuration for tiers0,1a,1b,2, with850k/500k effective windows and only curated rows in tier-only mode; actual provider inference is not required or authorized by this proof.
- No new lint/type errors, no global settings/env mutation, no commit,push,PR or Orca linkflags. Always stage .dev/tasks package/ledger/artifacts; never stage .claude mirrors or project-root artifacts.

## References

- REPORT.md: /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker/.dev/troubleshoot/bug-ensure-the-850k-limit-of-20261106114037/REPORT.md
- Audit log: /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker/.dev/troubleshoot/bug-ensure-the-850k-limit-of-20261106114037/audit.log
- Hypothesis: /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker/.dev/troubleshoot/bug-ensure-the-850k-limit-of-20261106114037/tier1-hypothesis.md
- Impact report: /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker/.dev/troubleshoot/bug-ensure-the-850k-limit-of-20261106114037/impact/impact.md (partial, graph:empty and graph:unresolved). Production dependent counts: compact_settings1,model_window1,transform_models4; shell export_selection/apply_tier_selection unclassified. Not proof of absence; inspect actual callers/tests.
- Actual runtime control captures and script under this run's artifacts/. Baseline pytest artifacts/baseline-pytest.log.

## Pipeline Hardening

pipeline_hardening_verdict: advisory
waiver_status: latched
Downstream stages must not re-green advisory closure into pass/success. Accepted-substitute runtime config proof is not completed launcher integration proof.
