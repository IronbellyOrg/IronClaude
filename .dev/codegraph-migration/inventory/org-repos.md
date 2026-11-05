# IronbellyOrg repository reference inventory

## Method and limits

Observed 2026-10-29. This is a read-only GitHub inventory, not removal work. IronClaude is included only in the organization listing and excluded from findings. Scope estimates use search excerpts only; implementation details and actual installations were not investigated.

GitHub CLI reports that `gh search code` uses the legacy code-search engine, which can differ from the website. Code search indexes default branches, not all work branches or local/untracked files. Each required query requests at most 100 file results, so counts at 100 are capped lower bounds, not occurrence totals. Search eligibility, fork indexing, private-repository visibility and index freshness can hide references: no returned hit does not prove absence. Repository listing is limited to 200 visible repositories.

Commands were first run exactly as requested with `--json repository,path`. They were repeated with `--json repository,path,textMatches,url` to preserve source excerpts and links for classification. The enrichment queries for `DeusData` and `mcp__serena` initially returned HTTP 403; `gh api rate_limit --jq .resources` showed the specific code-search pool exhausted (0/10), while core API access remained available. Those failed attempts are negative evidence, not zero-hit results. Later retries are recorded below.

Historical policy: paths containing `.dev/` or `claudedocs/`, including open task artifacts, are kept unchanged. Other logs, reports and decision records are also marked historical only when their matching excerpts establish recorded past activity. `.serena/memories/` records remain explicitly listed and are not assumed disposable. Source URLs identify actual returned search hits; snippets, not full-file reads, support the limited scope estimates.

## Organization repositories

Exact command: `gh repo list IronbellyOrg --limit 200 --json name,isArchived,isFork,defaultBranchRef`.

Returned 45 repositories, including the excluded IronClaude repository: 44 target repositories. Empty branch names are recorded as returned, not interpreted as a search result. Source: the command's live GitHub response, with repository links below.

| Repository (IronbellyOrg) | Archived | Fork | Default branch |
|---|---|---|---|
| [Coder](https://github.com/IronbellyOrg/Coder) | false | false | main |
| [Iroborus](https://github.com/IronbellyOrg/Iroborus) | false | false | main |
| [Ironeye](https://github.com/IronbellyOrg/Ironeye) | false | false | main |
| [IronFlow](https://github.com/IronbellyOrg/IronFlow) | false | false | main |
| [IronClaude](https://github.com/IronbellyOrg/IronClaude) (excluded) | false | true | master |
| [Ironbrain](https://github.com/IronbellyOrg/Ironbrain) | false | false | main |
| [Octodive](https://github.com/IronbellyOrg/Octodive) | false | false | main |
| [IronOrca](https://github.com/IronbellyOrg/IronOrca) | false | true | main |
| [coder_orca](https://github.com/IronbellyOrg/coder_orca) | false | false | main |
| [IBAssetFactory](https://github.com/IronbellyOrg/IBAssetFactory) | false | false | (empty) |
| [InfraDocs](https://github.com/IronbellyOrg/InfraDocs) | false | false | main |
| [IronOps](https://github.com/IronbellyOrg/IronOps) | false | false | main |
| [Financials](https://github.com/IronbellyOrg/Financials) | false | false | main |
| [TUIBBS-scp](https://github.com/IronbellyOrg/TUIBBS-scp) | false | false | main |
| [CPA-Manager-Plus](https://github.com/IronbellyOrg/CPA-Manager-Plus) | false | true | main |
| [ironboros-slackbot](https://github.com/IronbellyOrg/ironboros-slackbot) | false | false | master |
| [IronbellyStudios-Site](https://github.com/IronbellyOrg/IronbellyStudios-Site) | false | false | main |
| [IronbellyOrg_Coder](https://github.com/IronbellyOrg/IronbellyOrg_Coder) | false | false | main |
| [TUIBBS](https://github.com/IronbellyOrg/TUIBBS) | false | false | main |
| [shrapnel-gov](https://github.com/IronbellyOrg/shrapnel-gov) | false | false | main |
| [teamtailor](https://github.com/IronbellyOrg/teamtailor) | false | false | main |
| [Communitai](https://github.com/IronbellyOrg/Communitai) | false | false | main |
| [IronFlowBacklog](https://github.com/IronbellyOrg/IronFlowBacklog) | false | false | main |
| [shrapnel-frontend](https://github.com/IronbellyOrg/shrapnel-frontend) | false | false | main |
| [ironops-marketplace](https://github.com/IronbellyOrg/ironops-marketplace) | false | false | main |
| [tracel3t](https://github.com/IronbellyOrg/tracel3t) | false | false | main |
| [ClaudeCodeCodeAudit](https://github.com/IronbellyOrg/ClaudeCodeCodeAudit) | false | false | main |
| [GameCompKPI](https://github.com/IronbellyOrg/GameCompKPI) | false | false | main |
| [DevOps](https://github.com/IronbellyOrg/DevOps) | false | false | main |
| [shrapnel-backend](https://github.com/IronbellyOrg/shrapnel-backend) | false | false | main |
| [shrapnel-sds-ui](https://github.com/IronbellyOrg/shrapnel-sds-ui) | false | false | main |
| [Evals](https://github.com/IronbellyOrg/Evals) | false | false | main |
| [IronHands-CLI](https://github.com/IronbellyOrg/IronHands-CLI) | false | true | main |
| [IBOpenCode](https://github.com/IronbellyOrg/IBOpenCode) | true | false | main |
| [Ironhands-CLI_dev](https://github.com/IronbellyOrg/Ironhands-CLI_dev) | false | false | main |
| [IronHandsDev](https://github.com/IronbellyOrg/IronHandsDev) | false | false | main |
| [IronHands](https://github.com/IronbellyOrg/IronHands) | true | true | main |
| [llm-workflows](https://github.com/IronbellyOrg/llm-workflows) | false | false | main |
| [cloudbrain](https://github.com/IronbellyOrg/cloudbrain) | false | false | main |
| [proj-management-clickup-integration](https://github.com/IronbellyOrg/proj-management-clickup-integration) | false | false | main |
| [ai-devops-mcp](https://github.com/IronbellyOrg/ai-devops-mcp) | false | false | main |
| [click2dev](https://github.com/IronbellyOrg/click2dev) | false | false | main |
| [ElectronLauncher](https://github.com/IronbellyOrg/ElectronLauncher) | false | false | (empty) |
| [recruiting-tailscale](https://github.com/IronbellyOrg/recruiting-tailscale) | false | false | master |
| [IB_ReportingPlatform](https://github.com/IronbellyOrg/IB_ReportingPlatform) | false | false | main |

## Search commands and counts

The initial required commands all succeeded. Counts below were also confirmed in the saved enriched responses after both HTTP 403 retries succeeded. Counts are file results per query, not matching lines, and overlap across queries.

| Term | Exact required command used | Returned files | Coverage |
|---|---|---:|---|
| codebase-memory | `gh search code 'codebase-memory org:IronbellyOrg' --limit 100 --json repository,path` | 100 | capped |
| codebase_memory | `gh search code 'codebase_memory org:IronbellyOrg' --limit 100 --json repository,path` | 3 | below cap |
| DeusData | `gh search code 'DeusData org:IronbellyOrg' --limit 100 --json repository,path` | 15 | below cap |
| serena | `gh search code 'serena org:IronbellyOrg' --limit 100 --json repository,path` | 100 | capped |
| mcp__serena | `gh search code 'mcp__serena org:IronbellyOrg' --limit 100 --json repository,path` | 100 | capped |
| serena-agent | `gh search code 'serena-agent org:IronbellyOrg' --limit 100 --json repository,path` | 100 | capped |

Exact enrichment commands used (the last two were retried once after reset):

```sh
gh search code 'codebase-memory org:IronbellyOrg' --limit 100 --json repository,path,textMatches,url
gh search code 'codebase_memory org:IronbellyOrg' --limit 100 --json repository,path,textMatches,url
gh search code 'serena org:IronbellyOrg' --limit 100 --json repository,path,textMatches,url
gh search code 'serena-agent org:IronbellyOrg' --limit 100 --json repository,path,textMatches,url
gh search code 'DeusData org:IronbellyOrg' --limit 100 --json repository,path,textMatches,url
gh search code 'mcp__serena org:IronbellyOrg' --limit 100 --json repository,path,textMatches,url
```

Inspection commands: `gh search code --help`, `gh repo list --help`, and `gh api rate_limit --jq .resources`. No issue, pull request, comment, clone or remote mutation was made.

Evidence was retained in `/tmp/org-inventory-w3/` as one JSON response per term plus `repos.json`; this is temporary supporting evidence, not an additional repository deliverable. Tables below use the union of those six enriched result sets, deduplicated by repository and path. The enrichment pass may return a different capped subset from the first pass because search ranking is not a stable completeness guarantee.

**Local read-only exception:** the first JSON summary invocation, `uv run python -I /tmp/w3-inventory-render.py`, unexpectedly created an ignored `.venv` and installed the local package (observed UV output). This violated the strict local write boundary. It was reported to the coordinator; the environment was left untouched rather than deleted without approval. Later parsing used `uv run --no-project python -I /tmp/w3-inventory-render.py`. No tracked source or MCP registration changed.

## Per-repository live references

Tables enumerate the returned non-historical paths. A comma-separated filename cell means each exact file under the stated prefix, with the same terms and kind. "Live config" includes executable command/skill/agent instructions, not just JSON/YAML. "Doc" means a current-location document, not proof of active runtime use. No CI or test-code hits were returned outside historical artifacts; that does not establish absence.

### Coder

Source snapshot: [Dockerfile](https://github.com/IronbellyOrg/Coder/blob/e25f787ccaef04312f64347714a7791221564219/templates/VSCode-AIDev02/Dockerfile.coder), [bundle installer](https://github.com/IronbellyOrg/Coder/blob/e25f787ccaef04312f64347714a7791221564219/templates/VSCode-AIDev02/catalogue/mcp-bundle-core/install.sh), [bundle manifest](https://github.com/IronbellyOrg/Coder/blob/e25f787ccaef04312f64347714a7791221564219/templates/VSCode-AIDev02/catalogue/mcp-bundle-core/manifest.yaml).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |
| `templates/VSCode-AIDev02/Dockerfile.coder` | codebase-memory, DeusData | Dockerfile or installer |
| `templates/VSCode-AIDev02/catalogue/mcp-bundle-core/install.sh` | serena-agent | Dockerfile or installer |
| `templates/VSCode-AIDev02/catalogue/mcp-bundle-core/manifest.yaml` | serena-agent | live config |
| `_bmad-output/implementation-artifacts/6-3-mcp-register-and-proxy-betas.md` | serena-agent | doc (implementation instructions) |
| `_bmad-output/planning-artifacts/architecture/architecture-Coder-github-automation-orca-restart-2026-09-09/ARCHITECTURE-SPINE.md` | serena-agent | doc (baseline architecture) |
| `_bmad-output/specs/spec-aidev02-v2/catalogue-slugs.md` | serena | doc (bundle specification) |

### Financials

Source snapshot: [project config](https://github.com/IronbellyOrg/Financials/blob/d04e3ac4bab0e43086cd71354af60c05987d8e39/grants-credits/.serena/project.yml), [agent tools](https://github.com/IronbellyOrg/Financials/blob/d04e3ac4bab0e43086cd71354af60c05987d8e39/.claude/agents/auggie-reviewer.md), [settings](https://github.com/IronbellyOrg/Financials/blob/d04e3ac4bab0e43086cd71354af60c05987d8e39/.claude/settings.json), [reflection skill](https://github.com/IronbellyOrg/Financials/blob/d04e3ac4bab0e43086cd71354af60c05987d8e39/.claude/skills/sc-reflect-protocol/SKILL.md).

| Path prefix | Filename(s) | Term | Kind |
|---|---|---|---|
| `grants-credits/.serena/` | `project.yml` | serena | live config |
| `.claude/` | `settings.json` | mcp__serena | live config |
| `.claude/agents/` | `auggie-reviewer.md`, `reuse-auditor.md` | serena, mcp__serena | live config |
| `.claude/agents/` | `pm-agent.md` | serena | live config |
| `.claude/commands/sc/` | `cli-eval.md`, `cli-portify.md`, `help.md`, `init-lite.md`, `load.md`, `pm.md`, `pr-submit.md`, `research.md`, `save.md`, `select-tool.md`, `task.md`, `workflow.md` | serena | live config |
| `.claude/commands/sc/` | `reflect.md`, `troubleshoot.md`, `validate-roadmap.md` | serena, mcp__serena | live config |
| `.claude/skills/sc-brainstorm-protocol/refs/` | `handoff-routing.md` | mcp__serena | live config |
| `.claude/skills/sc-crash-recovery/` | `SKILL.md` | serena | live config |
| `.claude/skills/sc-crash-recovery/refs/` | `investigators.md` | serena | live config |
| `.claude/skills/sc-reflect-protocol/` | `SKILL.md` | mcp__serena | live config |
| `.claude/skills/sc-reflect-protocol/refs/` | `ops-integration.md` | serena | live config |
| `.claude/skills/sc-task-protocol/` | `SKILL.md` | mcp__serena | live config |
| `.claude/skills/sc-troubleshoot-protocol/` | `SKILL.md` | mcp__serena | live config |
| `.claude/skills/sc-validate-roadmap-protocol/` | `SKILL.md` | mcp__serena | live config |

### IronFlow

Source snapshot: [reflection command](https://github.com/IronbellyOrg/IronFlow/blob/f72263b7dbdd3abfaffc09ffacefa886d7e8ce23/.claude/commands/sc/reflect.md), [skill](https://github.com/IronbellyOrg/IronFlow/blob/f72263b7dbdd3abfaffc09ffacefa886d7e8ce23/.claude/skills/sc-reflect-protocol/SKILL.md), [settings](https://github.com/IronbellyOrg/IronFlow/blob/f72263b7dbdd3abfaffc09ffacefa886d7e8ce23/.claude/settings.json).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |
| `.claude/settings.json` | mcp__serena | live config |
| `.claude/commands/sc/reflect.md` | serena, mcp__serena | live config |
| `.claude/skills/sc-reflect-protocol/SKILL.md` | mcp__serena | live config |

### IronOps

Source snapshot: [settings](https://github.com/IronbellyOrg/IronOps/blob/a001541936c10b909474b30eee3a9bdf18b14080/.claude/settings.json), [project config](https://github.com/IronbellyOrg/IronOps/blob/a001541936c10b909474b30eee3a9bdf18b14080/.serena/project.yml), [owned skill source](https://github.com/IronbellyOrg/IronOps/blob/a001541936c10b909474b30eee3a9bdf18b14080/src/ironops/skills/ironops-troubleshoot-protocol/SKILL.md).

| Path | Term | Kind |
|---|---|---|
| `.claude/settings.json` | codebase-memory | live config |
| `.serena/project.yml` | serena | live config |
| `src/ironops/skills/ironops-troubleshoot-protocol/SKILL.md` | mcp__serena | live config (distributable skill source) |

### InfraDocs

Source snapshot: [project config](https://github.com/IronbellyOrg/InfraDocs/blob/3a7e37b6a9e8edb32e8c53c886bd73e9373ce28a/.serena/project.yml), [context-refresh guidance](https://github.com/IronbellyOrg/InfraDocs/blob/3a7e37b6a9e8edb32e8c53c886bd73e9373ce28a/configurations/jenkins/artifacts/phase5.1-context-refresh-requirements.md).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |
| `configurations/jenkins/artifacts/phase5.1-context-refresh-requirements.md` | mcp__serena | doc (guidance, not executable CI) |

Two additional runbook evidence paths are historical and appear below.

### ClaudeCodeCodeAudit

Source snapshot: [overview](https://github.com/IronbellyOrg/ClaudeCodeCodeAudit/blob/6cdfdd830c1b86aeba11c04508db156625d91944/00-MASTER-PROCESS-OVERVIEW.md), [quick start](https://github.com/IronbellyOrg/ClaudeCodeCodeAudit/blob/6cdfdd830c1b86aeba11c04508db156625d91944/01-QUICK-START.md), [project index](https://github.com/IronbellyOrg/ClaudeCodeCodeAudit/blob/6cdfdd830c1b86aeba11c04508db156625d91944/docs/generated/PROJECT_INDEX.md).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |
| `README.md` | serena | doc |
| `00-MASTER-PROCESS-OVERVIEW.md` | serena, mcp__serena | doc (audit workflow and persistence) |
| `01-QUICK-START.md` | serena | doc |
| `02-OUTPUT-SCHEMAS.md` | serena | doc (example tool accounting) |
| `03-ACCEPTANCE-CRITERIA.md` | serena | doc (requires Serena tool evidence) |
| `04-LITE-VARIANT.md` | serena | doc |
| `PHASE-0-DISCOVERY.md` | serena, mcp__serena | doc |
| `PHASE-0A-PRD-VALIDATION.md` | serena, mcp__serena | doc |
| `PHASE-2-CHUNKING.md` | serena | doc |
| `PHASE-3-NARROW-REVIEW.md` | serena, mcp__serena | doc |
| `PHASE-4-HOLISTIC-REVIEW.md` | serena | doc |
| `PHASE-6-FINAL-REPORT.md` | serena, mcp__serena | doc (template instructions, not completed evidence) |
| `docs/generated/PROJECT_INDEX.md` | serena | doc (mentions a language-server dependency; dependency file not inspected) |

Two additional evidence-only paths appear below.

### Ironbrain

Source snapshot: [planning document](https://github.com/IronbellyOrg/Ironbrain/blob/914e1c891ea3fef78c46ac22fbd350f36e624146/PLANNING.md).

| Path | Term | Kind |
|---|---|---|
| `PLANNING.md` | codebase-memory | doc (selective repository-local structural retrieval proposal) |

### Octodive

Source snapshot: [project config](https://github.com/IronbellyOrg/Octodive/blob/63854063c6c31b271c078b6ec94eda67c1b5d157/.serena/project.yml).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |

### TUIBBS

Source snapshot: [project config](https://github.com/IronbellyOrg/TUIBBS/blob/3e9ea096053a452754a4cf8ce8026034d92d1cde/.serena/project.yml), [review protocol](https://github.com/IronbellyOrg/TUIBBS/blob/3e9ea096053a452754a4cf8ce8026034d92d1cde/docs/governance/post-merge-review-protocol.md).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |
| `docs/governance/post-merge-review-protocol.md` | mcp__serena | doc (symbol cross-reference review step) |

Memory and decision records appear below.

### TUIBBS-scp

Source snapshot: [project config](https://github.com/IronbellyOrg/TUIBBS-scp/blob/a6d7e7f0a346a44317a1c3fffdd39dc0e14fab59/.serena/project.yml).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |

Three completed evidence/decision paths appear below.

### shrapnel-gov

Source snapshot: [settings](https://github.com/IronbellyOrg/shrapnel-gov/blob/d3875c8dd71245f2f3b83ac02b2e83afb56426d7/.claude/settings.json), [workflow instructions](https://github.com/IronbellyOrg/shrapnel-gov/blob/d3875c8dd71245f2f3b83ac02b2e83afb56426d7/workflows/resolution-charter-rpt-workflow.md).

| Path | Term | Kind |
|---|---|---|
| `.serena/project.yml` | serena | live config |
| `.claude/settings.json` | mcp__serena | live config |
| `workflows/resolution-charter-rpt-workflow.md` | mcp__serena | doc (workflow memory lookup, auto-memory fallback) |

Two memory records and the completed workflow log appear below. Do not delete project knowledge as a side effect of removing a tool.

### llm-workflows

Source snapshot: [opinion command](https://github.com/IronbellyOrg/llm-workflows/blob/2d8f62e56e0a01f5e09ffac0d5cef400729224a1/.claude/commands/rf/opinion.md).

| Path | Term | Kind |
|---|---|---|
| `.claude/commands/rf/opinion.md` | serena | live config (future integration mention; excerpt explicitly has an empty server list) |

### Ironeye

No live hit returned. Its two historical paths are listed below; no removal implementation is inferred.

## Keep (historical)

Every row in this section means **keep (historical)**, not a removal candidate. Prefix plus each filename gives the exact returned path. Terms are the queries that returned that file, not an assertion that the file lacks other terms. Source: the six GitHub search responses retained above; repository URLs are in the organization table. These are path-classified records and were not investigated beyond search excerpts.

### Historical .dev and claudedocs paths

| Repository | Path prefix | Filename(s) | Term | Kind |
|---|---|---|---|---|
| ClaudeCodeCodeAudit | `.dev/analysis/` | `AUDIT-FRAMEWORK-COMPARISON-REPORT.md` | mcp__serena | keep (historical) |
| ClaudeCodeCodeAudit | `.dev/analysis/` | `AUDIT-VERIFICATION-REPORT.md` | serena | keep (historical) |
| ClaudeCodeCodeAudit | `.dev/releases/Backlog/v3.3/` | `SC-ANALYZE-REFACTOR-GUIDE.md`, `SC-ANALYZE-SPEC.md` | mcp__serena | keep (historical) |
| ClaudeCodeCodeAudit | `.dev/releases/Backlog/v3.3/` | `SC-ANALYZE-REFACTOR-TASK-LIST.md` | serena, mcp__serena | keep (historical) |
| ClaudeCodeCodeAudit | `.dev/runs/rf-crossLLM/20260102-042754__file__claude>gpt/` | `input.md`, `judgement.md`, `upgrade.md` | mcp__serena | keep (historical) |
| ClaudeCodeCodeAudit | `.dev/runs/rf-crossLLM/20260102-050143__file__claude>gpt/` | `input.md`, `judgement.md` | mcp__serena | keep (historical) |
| Coder | `.dev/manual-qa/ccsession-orca-rollout-20261026/` | `EVIDENCE.md` | codebase-memory, DeusData | keep (historical) |
| Coder | `.dev/plans/issue-251-mobile/diagnosis/` | `audit.log` | serena | keep (historical) |
| Coder | `.dev/releases/complete/v1.3-2026Upgrade/remediation-proposals/` | `R1-manifest-interpolation.md` | mcp__serena | keep (historical) |
| Coder | `.dev/releases/complete/v1.3-2026Upgrade/results/` | `phase-1-output.txt`, `phase-5-output.txt` | mcp__serena | keep (historical) |
| Coder | `.dev/releases/complete/v1.3-2026Upgrade/validation/Artifacts/` | `reflect-phase-1-agent-opus.md`, `reflect-phase-2-agent-opus.md`, `reflect-phase-3-agent-opus.md`, `reflect-phase-3-agent.md`, `reflect-phase-5-agent-opus.md`, `reflect-phase-6-agent-opus.md`, `reflect-phase-7-agent-opus.md`, `reflect-phase-8-agent-opus.md` | mcp__serena | keep (historical) |
| Coder | `.dev/releases/complete/v1.3-2026Upgrade/validation/` | `reflect-phase-5-merged.md`, `reflect-phase-6-merged.md` | mcp__serena | keep (historical) |
| Coder | `.dev/releases/current/v2-m2/` | `02-research.md` | serena, serena-agent | keep (historical) |
| Coder | `.dev/releases/current/v2-m2/post-release/` | `audit.log` | serena | keep (historical) |
| Coder | `.dev/releases/current/v2-m2/research/` | `web-02-mcp-bundle.md` | serena, serena-agent | keep (historical) |
| Coder | `.dev/releases/current/v2-m2/tasks/` | `T2-mcp-bundle-core.md` | serena-agent | keep (historical) |
| Coder | `.dev/releases/current/v2-m2/tasks/mcp-bundle-core/phase-outputs/discovery/` | `install-vector-confirmed.md` | serena-agent | keep (historical) |
| Coder | `.dev/releases/current/v2-m2/tasks/mcp-bundle-core/research/` | `web-03-upstream.md` | serena-agent | keep (historical) |
| Coder | `.dev/reviews/orca-catalogue-bundle-20260924/` | `03-ironclaude.md` | serena-agent | keep (historical) |
| Coder | `.dev/tasks/archive/TASK-WF-remediationSourc-20261026-010025/` | `TASK-WF-remediationSourc-20261026-010025.md` | codebase-memory, DeusData | keep (historical) |
| Coder | `.dev/tasks/archive/TASK-WF-remediationSourc-20261026-010025/artifacts/` | `reflect-pre-review-REPORT.md` | codebase-memory | keep (historical) |
| Coder | `.dev/tasks/archive/TASK-WF-remediationSourc-20261026-010025/` | `source.md` | codebase-memory, codebase_memory, DeusData | keep (historical) |
| Coder | `.dev/tasks/done/TASK-RF-20260528-152121/research/` | `03-edit-sequencing-and-conflicts.md` | mcp__serena | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-remediationSourc-20261026-013053/` | `TASK-WF-remediationSourc-20261026-013053.md` | codebase-memory, DeusData | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-remediationSourc-20261026-013053/artifacts/` | `pr-body.md`, `t1-image-binary.txt`, `t2-pin-install.txt` | codebase-memory | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-remediationSourc-20261026-013053/artifacts/` | `t1.diff` | DeusData | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-remediationSourc-20261026-013053/artifacts/` | `t3-test-57-negative.log` | DeusData, serena-agent | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-remediationSourc-20261026-013053/artifacts/` | `t3-test-57.log` | serena-agent | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-remediationSourc-20261026-013053/` | `source.md` | codebase-memory, codebase_memory, DeusData | keep (historical) |
| Coder | `.dev/tasks/done/TASK-WF-takeThePlanConfi-20261023-173430/artifacts/` | `ironclaude-status.baseline.txt` | codebase-memory | keep (historical) |
| Coder | `.dev/tasks/to-do/TASK-RF-serena-uv-migration-20260711/` | `TASK-RF-serena-uv-migration-20260711.md` | serena, serena-agent | keep (historical) |
| Coder | `.dev/tasks/to-do/TASK-WF-devDesignAidev02-20261027-174057/artifacts/retries/T2/` | `prompt-1-1.md` | codebase-memory | keep (historical) |
| Coder | `.dev/troubleshoot/deployment-mcp-bundle-core-marker-20260710152800/fix-proposals/` | `fix-A-install-robustness.md` | serena-agent | keep (historical) |
| Coder | `.dev/troubleshoot/deployment-mcp-bundle-core-marker-20260710152800/` | `tier1-observation.md` | serena-agent | keep (historical) |
| Coder | `.dev/troubleshoot/ironclaude-pipeline-escape-20260706/` | `INVESTIGATION-PROMPT.md` | mcp__serena | keep (historical) |
| Coder | `.dev/troubleshoot/readme-vs-actual-20260706-050000/` | `VALIDATION-PROMPT.md` | mcp__serena | keep (historical) |
| Coder | `.dev/troubleshoot/swarm-model-aliasing-20260706-234000/swarm/real-run3/` | `merged.md` | mcp__serena | keep (historical) |
| Coder | `.dev/troubleshoot/test-spec2-mcp-handshake-20260927190114/` | `REPORT.md`, `REPORT.md.draft`, `doc-context.md`, `tier1-observation.md` | serena-agent | keep (historical) |
| Coder | `claudedocs/` | `HANDOFF_orca_coder_consolidation_20260803.md` | codebase-memory | keep (historical) |
| Coder | `claudedocs/orca-consolidation/adversarial/` | `variant-2-original.md` | codebase-memory | keep (historical) |
| Financials | `.dev/research/sred-evidence-reconstruction-20260828/06-synthesis/gameframe/` | `ironclaude-rollup-013-015.md` | serena-agent | keep (historical) |
| InfraDocs | `.dev/reflect/post-adr0001-devtasks-reconciliation-20260723235853/` | `serena-checkpoints.log` | serena | keep (historical) |
| InfraDocs | `.dev/releases/v0.1-Org/` | `00-plan.md` | serena | keep (historical) |
| InfraDocs | `.dev/tasks/to-do/TASK-RF-runner-readiness-20260916/coder/base/templates/VSCode-AIDev02/catalogue/mcp-bundle-core/` | `install.sh`, `manifest.yaml` | serena-agent | keep (historical) |
| InfraDocs | `.dev/tasks/to-do/TASK-RF-runner-readiness-20260916/coder/patched/templates/VSCode-AIDev02/catalogue/mcp-bundle-core/` | `install.sh`, `manifest.yaml` | serena-agent | keep (historical) |
| InfraDocs | `.dev/tasks/to-do/TASK-RF-runner-readiness-20260916/phase-outputs/troubleshoot-20260918/CON-007/` | `audit.json` | codebase_memory | keep (historical) |
| InfraDocs | `.dev/tasks/to-do/TASK-RF-runner-readiness-20260916/reflect/pre/` | `serena-checkpoints.log` | serena | keep (historical) |
| InfraDocs | `.dev/troubleshoot/deployment-pve5-8-receiver-missing-20260725001106/` | `audit.log` | codebase-memory | keep (historical) |
| IronFlow | `.dev/baselines/skills-agents-20260610/skills/sc-reflect-protocol/` | `SKILL.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/baselines/skills-agents-20260625/skills/sc-reflect-protocol/` | `SKILL.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/patches/reflect-cli-fixes-20260619/backups/` | `sc-reflect-SKILL.md.bak` | mcp__serena | keep (historical) |
| IronFlow | `.dev/patches/reflect-cli-fixes-20260619/staging/` | `sc-reflect-SKILL.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/plans/` | `PLAN-ccsession-context-save-load-20260520.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/plans/ironclaude-pr-analysis-20260619/pr-staging/` | `sc-reflect-PR.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/reflect/persona-core-gap-spec-post-20260916-run1-fail/artifacts/` | `serena-memory-before.yaml` | serena | keep (historical) |
| IronFlow | `.dev/reflect/persona-core-gap-spec-post-20260916/artifacts/` | `serena-memory-after.yaml`, `serena-memory-before.yaml` | serena | keep (historical) |
| IronFlow | `.dev/reflect/persona-core-gap-spec-post-20260916/` | `audit.log` | mcp__serena | keep (historical) |
| IronFlow | `.dev/reflect/persona-core-gap-spec-post-20260916/` | `serena-config-snapshot.yaml` | serena | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/` | `MCP-FINAL-REPORT.md`, `_frag_tables.md` | codebase-memory | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/` | `candidates.md` | codebase-memory, DeusData | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/discovery/` | `sweep-code-intel.md` | codebase-memory, DeusData | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/findings/` | `code-index-mcp.md`, `codebase-memory-mcp.md` | codebase-memory, DeusData | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/findings/` | `codegraphcontext.md`, `graph-codebase-mcp.md` | codebase-memory | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/findings/` | `serena.md` | serena | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/verification/` | `code-index-mcp.md`, `codegraphcontext.md`, `graph-codebase-mcp.md` | codebase-memory | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/verification/` | `codebase-memory-mcp.md` | codebase-memory, DeusData | keep (historical) |
| IronFlow | `.dev/research/mcp-rankings-20260724/verification/` | `serena.md` | serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-RESEARCH-persona-core-gap-20260915-082754/qa/` | `serena-reflect-tool-probe.json` | serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-RESEARCH-persona-core-gap-20260915-082754/reflect/pre/` | `serena-checkpoints.log` | serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-RESEARCH-spine-design-20260614-133005/probes/` | `Q-03-glob-grep-in-subagents.md`, `Q-04-mcp-in-subagents.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-RF-bake-bringup-20260714-141419/reflect/pre/` | `serena-config-snapshot.yaml` | serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-RF-skilleval-invocation-20260710-171545/reflect/pre/` | `audit.log` | mcp__serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-RF-task-execution-research-20260926-101310/reflect/pre/` | `serena-checkpoints.log` | serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-USKILLS-ironflow-20260704-100030/.understand-anything/sources/agents/` | `auggie-reviewer.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-USKILLS-ironflow-20260704-100030/baseline/sources/agents/` | `auggie-reviewer.md`, `reuse-auditor.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/TASK-USKILLS-ironflow-20260704-100030/sources/agents/` | `auggie-reviewer.md`, `reuse-auditor.md` | mcp__serena | keep (historical) |
| IronFlow | `.dev/tasks/to-do/nested-subagents/evidence/round2-skill-probes/pr2/` | `depth1-consolidated.md`, `rf-researcher-nested-findings.md` | mcp__serena | keep (historical) |
| IronOps | `.dev/brainstorms/20260831T124705Z-pve-wrapper-cluster-certificate-management/enrichment/` | `codebase-context.md` | codebase-memory | keep (historical) |
| IronOps | `.dev/tasks/to-do/TASK-RF-runner-hook-parity-20261003-051227/research/` | `06-gap-fill.md` | mcp__serena | keep (historical) |
| IronOps | `.dev/troubleshoot/cleanup-hook-round3-20261002-2225/` | `audit.log` | codebase-memory, serena | keep (historical) |
| IronOps | `.dev/troubleshoot/installer-parity-20261003-0044/` | `audit.log` | codebase-memory, serena | keep (historical) |
| IronOps | `.dev/troubleshoot/installer-parity-20261003-0044/` | `contract-ledger.md` | serena | keep (historical) |
| IronOps | `pve/.dev/troubleshoot/deployment-pve5-8-receiver-missing-20260725001106/` | `audit.log` | codebase-memory | keep (historical) |
| Ironbrain | `.dev/research/` | `Ironbrain-GPT.md` | codebase-memory, DeusData | keep (historical) |
| Ironbrain | `.dev/research/` | `Ironbrain-Gemini.md`, `Ironbrain-merged.md`, `SESSION-HANDOFF-v0.1.md` | codebase-memory | keep (historical) |
| Ironbrain | `.dev/research/adversarial/` | `diff-analysis.md`, `invariant-probe.md`, `variant-2-original.md` | codebase-memory | keep (historical) |
| Ironbrain | `.dev/research/adversarial/` | `variant-3-original.md` | codebase-memory, DeusData | keep (historical) |
| Ironeye | `.dev/` | `SESSION_HANDOFF.md` | serena | keep (historical) |
| Ironeye | `.dev/research/specstory-litellm-20261001/` | `ironbrain-analysis.md` | codebase-memory | keep (historical) |
| Octodive | `.dev/` | `README.md` | serena | keep (historical) |
| Octodive | `.dev/historical/brainstorm-v1-lenses-on-deep-research/` | `01-declarative-purist.md`, `04-hook-driven.md` | mcp__serena | keep (historical) |
| Octodive | `.dev/historical/brainstorm/` | `04-sc-brainstorm-wave2a.md`, `05-sc-troubleshoot-command.md` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v0.1/results/` | `phase-6-task-T06.18-output.txt`, `phase-6-task-T06.20-output.txt`, `phase-7-task-T07.06-output.txt`, `phase-7-task-T07.20-output.txt`, `phase-9-task-T09.17-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v0.1/tasklists/artifacts/D-0175/` | `notes.md` | serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/` | `phase-1-task-T01.02-output.txt`, `phase-1-task-T01.07-output.txt`, `phase-1-task-T01.09-output.txt`, `phase-1-task-T01.10-output.txt`, `phase-1-task-T01.13-output.txt`, `phase-1-task-T01.16-output.txt`, `phase-1-task-T01.30-output.txt`, `phase-1-task-T01.35-output.txt`, `phase-2-task-T02.03-output.txt`, `phase-2-task-T02.08-output.txt`, `phase-2-task-T02.10-output.txt`, `phase-2-task-T02.14-output.txt`, `phase-2-task-T02.15-output.txt`, `phase-2-task-T02.16-output.txt`, `phase-2-task-T02.17-output.txt`, `phase-2-task-T02.19-output.txt`, `phase-2-task-T02.22-output.txt`, `phase-2-task-T02.23-output.txt`, `phase-2-task-T02.25-output.txt`, `phase-2-task-T02.26-output.txt`, `phase-2-task-T02.27-output.txt`, `phase-2-task-T02.28-output.txt`, `phase-2-task-T02.29-output.txt`, `phase-2-task-T02.30-output.txt`, `phase-2-task-T02.32-output.txt`, `phase-3-task-T03.09-output.txt`, `phase-3-task-T03.13-output.txt`, `phase-3-task-T03.14-output.txt`, `phase-3-task-T03.18-output.txt`, `phase-3-task-T03.30-output.txt`, `phase-3-task-T03.36-output.txt`, `phase-3-task-T03.42-output.txt`, `phase-3-task-T03.43-output.txt`, `phase-3-task-T03.48-output.txt`, `phase-3-task-T03.49-output.txt`, `phase-3-task-T03.50-output.txt`, `phase-3-task-T03.53-output.txt`, `phase-4-task-T04.06-output.txt`, `phase-4-task-T04.31-output.txt`, `phase-4-task-T04.32-output.txt`, `phase-5-task-T05.09-output.txt`, `phase-5-task-T05.12-output.txt`, `phase-5-task-T05.14-output.txt`, `phase-5-task-T05.33-output.txt`, `phase-5-task-T05.35-output.txt`, `phase-5-task-T05.37-output.txt`, `phase-6-task-T06.33-output.txt` | codebase-memory | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/` | `phase-3-task-T03.20-output.txt`, `phase-5-task-T05.26-output.txt`, `phase-5-task-T05.30-output.txt`, `phase-5-task-T05.36-output.txt`, `phase-5-task-T05.38-output.txt`, `phase-6-task-T06.43-output.txt`, `phase-6-task-T06.48-output.txt`, `phase-6-task-T06.51-output.txt` | codebase-memory, mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/rerun-20260914T105701/results/` | `phase-3-task-T03.20-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/rerun-20260914T105817/results/` | `phase-5-task-T05.26-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/rerun-20260914T110108/results/` | `phase-6-task-T06.43-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/rerun-20260914T110426/results/` | `phase-3-task-T03.24-output.txt`, `phase-3-task-T03.52-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/rerun-20260914T114959/results/` | `phase-5-task-T05.30-output.txt`, `phase-5-task-T05.36-output.txt`, `phase-5-task-T05.38-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/releases/current/v1/results/rerun-20260914T115524/results/` | `phase-6-task-T06.48-output.txt`, `phase-6-task-T06.51-output.txt` | mcp__serena | keep (historical) |
| Octodive | `.dev/research/` | `octocode-research.md`, `top-5-targets.md` | serena | keep (historical) |
| Octodive | `.dev/research/raw/` | `02-integration-points.md`, `web-03-octocode-weaknesses.md` | serena | keep (historical) |
| Octodive | `.dev/troubleshoot/bug-pr6-residual-findings-20260915000043/` | `unmask-sweep.md` | codebase-memory | keep (historical) |
| TUIBBS-scp | `.dev/archive/20261012-environment-migration/` | `README.md` | serena | keep (historical) |
| TUIBBS-scp | `.dev/reflect/post-story-1-2-20260911143435/` | `audit.log`, `serena-config-snapshot.yaml` | serena | keep (historical) |
| TUIBBS-scp | `.dev/reflect/post-story-1-6-20260915-delegated/` | `REPORT.md` | serena | keep (historical) |
| TUIBBS-scp | `.dev/reflect/pre-wsdial-remediation-20260705/` | `audit.log` | serena | keep (historical) |
| TUIBBS-scp | `.dev/releases/current/v1-MVP/tasklists/artifacts/D-0169/` | `notes.md` | serena | keep (historical) |
| TUIBBS-scp | `.dev/troubleshoot/anti-instinct-deeper-20260526192013/` | `audit.log` | serena | keep (historical) |
| TUIBBS-scp | `.dev/troubleshoot/phase12-gate-error-20260604/` | `audit.log` | serena | keep (historical) |
| llm-workflows | `.dev/taskplanning/backlog/` | `01_MCP_INTEGRATION_ANTI_SYCOPHANCY.md`, `03_MCP_SERENA_INTEGRATION.md`, `README.md` | serena | keep (historical) |
| llm-workflows | `.dev/taskplanning/v5.2/` | `BACKLOG.md` | serena | keep (historical) |
| llm-workflows | `.dev/tasks/TASK-RF-20260207-health-analyzer/outputs/` | `worker_session_batch3.json`, `worker_session_batch3.raw`, `worker_session_batch4.json`, `worker_session_batch4.raw` | mcp__serena | keep (historical) |

### Octodive repeated investigation snapshots

All paths in this subsection match **serena-agent** and are **keep (historical)**. To avoid repeating very long paths, the following exact prefix definitions compose the returned paths:

- `I` = `.dev/tasks/to-do/TASK-RF-pr6-finalization-20260915-015432/investigation-20260917T125000Z/`
- `R` = `.dev/tasks/to-do/TASK-RF-pr6-finalization-20260915-015432/reflect/post-7/snapshot/`
- `C` = `closure-20260917T2105/phase4-fix-cycle1/pre-fix/investigation-20260917T125000Z/`
- Report filenames = `REPORT.md.draft`, `evidence-validation.md`, `parent-capability-evidence.md`, `parent-implementation-validation.json`, `proposal-1.prompt.txt`, `proposal-2.prompt.txt`, `proposal-3.prompt.txt`, `proposal-brief.md`.
- Debate filenames = `extraction-ledgers.json`, `finalize.py`, `merge-executor.prompt.txt`, `merge-log-v2.md`, `merged-output-v2.md`, `refactor-plan-addendum.md`, `source-brief.md`, `v2-evidence-review.md`, `v2-self-review.md`, `validation-results-v2.json`.

`+` means literal string concatenation, not a glob; each set enumerates exact returned filenames.

| Path prefix expression | Filename(s) | Term | Kind |
|---|---|---|---|
| I | Report filenames | serena-agent | keep (historical) |
| I + C | Report filenames | serena-agent | keep (historical) |
| I + `parent-offline-inspection-7zytkxs3/` | `inspection.json` | serena-agent | keep (historical) |
| I + C + `parent-offline-inspection-7zytkxs3/` | `inspection.json` | serena-agent | keep (historical) |
| I + `proposal-debate/` | Debate filenames | serena-agent | keep (historical) |
| I + C + `proposal-debate/` | Debate filenames | serena-agent | keep (historical) |
| R + I | Report filenames | serena-agent | keep (historical) |
| R + I + C | Report filenames | serena-agent | keep (historical) |
| R + I + `parent-offline-inspection-7zytkxs3/` | `inspection.json` | serena-agent | keep (historical) |
| R + I + C + `parent-offline-inspection-7zytkxs3/` | `inspection.json` | serena-agent | keep (historical) |
| R + I + `proposal-debate/` | Debate filenames | serena-agent | keep (historical) |
| R + I + C + `proposal-debate/` | Debate filenames | serena-agent | keep (historical) |
| I | `serena-agent-probe.stderr.txt` | serena | keep (historical) |

### Additional historical records outside .dev and claudedocs

These classifications rely on the matching excerpts showing logs, completed decisions, or historical memory. They are not blanket directory exclusions.

| Repository | Path | Term | Kind |
|---|---|---|---|
| ClaudeCodeCodeAudit | `checklists/generated/repo-files-modified-last-24h.txt` | serena | keep (historical), timestamped file list |
| ClaudeCodeCodeAudit | `EMERGENCY-SCOPE-AUDIT.md` | serena | keep (historical), memory inventory audit |
| InfraDocs | `runbooks/storage/retroactive-pve-storage-remediation/artifacts/2026-07-22-access-check-raw/mcp-list.txt` | codebase-memory | keep (historical), MCP health snapshot |
| InfraDocs | `runbooks/storage/retroactive-pve-storage-remediation/security-incident/2026-07-22-metadata-command-log.md` | codebase-memory | keep (historical), command log |
| Octodive | `docs/testing/v1.0.0/audit.log.txt` | serena | keep (historical), release validation log |
| TUIBBS | `.serena/memories/brainstorming_session_2026-04-12.md` | serena | keep (historical), brainstorming memory |
| TUIBBS | `_planning-input/prd-decision-log.md` | serena | keep (historical), past artifact-update record |
| TUIBBS-scp | `.claude-audit/final-report.md` | serena | keep (historical), completed audit exclusions |
| TUIBBS-scp | `_bmad-output/adversarial-decisions.md` | serena | keep (historical), dated prior decision |
| TUIBBS-scp | `docs/research/agentbbs-idea-harvest-20260720/self-review.md` | serena | keep (historical), completed study evidence |
| shrapnel-gov | `.serena/memories/board_prep_arc_and_state.md` | serena | keep (historical), project knowledge; preserve |
| shrapnel-gov | `.serena/memories/resolution_charter_workflow_pointer.md` | serena | keep (historical), project knowledge; preserve |
| shrapnel-gov | `legal/_workflow-log.md` | mcp__serena | keep (historical), completed workflow log |

Historical classification does not mean a memory has no present value. A future removal owner must preserve accessible project knowledge rather than recursively deleting memory directories.

## Removal scope and ownership

The enriched search union contains **377 distinct repository/path pairs across 13 target repositories**. After separating the additional historical records above, **67 paths are non-historical and 310 are keep (historical)**. These counts describe the sampled search union, not organization-wide complete counts.

| Owning repository | Live/non-historical paths | Keep (historical) paths | Estimated scope |
|---|---:|---:|---|
| ClaudeCodeCodeAudit | 14 | 12 | Audit workflow documentation and project config |
| Coder | 7 | 48 | Image binary, MCP bundle installer/manifest, project config and specifications |
| Financials | 28 | 1 | Broad project-local command/skill/agent/settings migration |
| InfraDocs | 2 | 11 | Project config and context-refresh documentation |
| IronFlow | 4 | 39 | Reflection command/skill, permissions and project config |
| IronOps | 3 | 6 | Owned troubleshooting skill, permissions and project config |
| Ironbrain | 1 | 8 | Planning-document terminology only in returned live hits |
| Ironeye | 0 | 2 | Historical only; no removal inferred |
| Octodive | 1 | 159 | Project config only in returned live hits |
| TUIBBS | 2 | 2 | Project config and review guidance; preserve memory |
| TUIBBS-scp | 1 | 11 | Project config only in returned live hits |
| llm-workflows | 1 | 8 | Future integration wording in one command |
| shrapnel-gov | 3 | 3 | Project config, permissions and workflow lookup guidance; preserve memory |
| **Total** | **67** | **310** | **377 distinct paths** |

**Coder owns the image and bundle removal.** The Dockerfile excerpt downloads architecture-specific codebase-memory release assets from DeusData and verifies checksums, while the bundle installer constructs Serena launch arguments and checks its UV package installation; the manifest advertises Serena to users. Removal therefore needs coordinated Dockerfile, bundle registration/health checks, manifest and local project configuration changes, plus reconciliation of the three current-location specification/instruction documents. Existing-workspace cleanup and fresh-image behavior need verification in Coder, but their actual implementation paths are UNVERIFIED here. Evidence: the three Coder source links in its live table.

**Financials owns reconciliation of its checked-in project-local tooling.** Returned excerpts show Serena server declarations, symbol-navigation permissions, startup/session memory requirements, fallback routing and reflection/validation instructions across 28 paths. The work is broader than deleting a server registration: replace or remove those instructions and permissions, reconcile the grants-credits project configuration, and identify whether the local copies should instead be refreshed from their owning distributable source. Provenance of these copies is UNVERIFIED; do not apply IronClaude's local gitignore rules to Financials without checking there. Evidence: Financials source links in its live table.

**IronFlow owns its project configuration and reflection tooling reconciliation.** Its four returned live paths combine Serena permissions, a reflection command, the matching reflection skill, and project configuration. Replace the symbol-navigation and memory dependencies together rather than leaving a command that calls removed tools; whether the local command/skill copies are generated is UNVERIFIED. Evidence: IronFlow source links in its live table.

**IronOps owns its distributable troubleshooting skill and local settings/configuration.** The skill source explicitly allows Serena symbol tools, while settings allow codebase-memory indexing/search operations. Removal needs to update that owned source and permission list alongside the Serena project configuration; downstream regeneration requirements are UNVERIFIED. Evidence: IronOps source links in its live table.

**InfraDocs owns its project configuration and context-refresh guidance.** One returned document routes symbolic queries through Serena and the project configuration identifies InfraDocs. Replace that guidance and reconcile the project configuration; the Jenkins directory name does not make this Markdown document executable CI. Preserve the dated incident and access-check records. Evidence: InfraDocs source links in its live table.

**ClaudeCodeCodeAudit owns a documentation-led workflow migration.** Its overview, quick start, acceptance criteria and phase documents prescribe Serena navigation and memory persistence, so removal must replace those tool-specific instructions and evidence requirements rather than merely removing project configuration. The generated index mentions a language-server dependency, but the actual package file was not inspected and dependency removal is UNVERIFIED. Preserve audit/file-list history. Evidence: the overview, quick-start and index source links in its live table.

**Ironbrain owns a small planning-document update.** The sole returned non-historical hit describes codebase-memory as selective repository-local structural retrieval. Reconcile that proposal with the chosen replacement; no runtime installation or integration was demonstrated by this search. Preserve research history. Evidence: the PLANNING.md source link in its live table.

**Octodive owns reconciliation of its Serena project configuration.** That is its only returned non-historical hit; the large release/investigation result volume is historical evidence, not evidence of many live integrations. Runtime cleanup requirements beyond the project configuration are UNVERIFIED. Evidence: the project-config source link in its live table.

**TUIBBS owns its project configuration and post-merge review guidance.** The review document names a Serena symbol cross-reference step, so removal needs a replacement for that step plus reconciliation of project configuration. Preserve the historical brainstorming memory and decision log. Evidence: the project-config and review-protocol source links in its live table.

**TUIBBS-scp owns reconciliation of its Serena project configuration.** The remaining returned paths are prior audit, study, decision and .dev records; keep them unchanged. No application-code removal is established. Evidence: its project-config source link and historical classifications above.

**shrapnel-gov owns its local permissions, project configuration and workflow guidance.** The workflow excerpt reads Serena memories and explicitly falls back to auto-memory when unavailable; update that lookup guidance and remove obsolete tool permissions/configuration without deleting the project knowledge or completed workflow log. Whether any memory remains needed operationally must be assessed by that repository's owner before removal. Evidence: its settings and workflow source links in the live table.

**llm-workflows owns a wording-level command update.** Its opinion command mentions future Serena integration while the excerpt explicitly declares an empty server list. Remove or replace that future dependency wording; do not describe it as an installed server or implemented integration. Evidence: its opinion-command source link in the live table.

### Targets with no returned hits

The other 31 target repositories returned no files in the six required capped queries: Iroborus, IronOrca, coder_orca, IBAssetFactory, CPA-Manager-Plus, ironboros-slackbot, IronbellyStudios-Site, IronbellyOrg_Coder, teamtailor, Communitai, IronFlowBacklog, shrapnel-frontend, ironops-marketplace, tracel3t, GameCompKPI, DevOps, shrapnel-backend, shrapnel-sds-ui, Evals, IronHands-CLI, IBOpenCode, Ironhands-CLI_dev, IronHandsDev, IronHands, cloudbrain, proj-management-clickup-integration, ai-devops-mcp, click2dev, ElectronLauncher, recruiting-tailscale and IB_ReportingPlatform. This is **not a clean bill of health**, especially for forks and queries capped at 100. Non-default branches, inaccessible repositories, local configuration and search-index omissions remain outside this inventory.

## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| Use the task brief's required report outline as the governing structure | Requested inventory outline; unrelated implementation/report machinery | self | The shared rules require a stub-first report and this task provides the required sections; no implementation plan or extra skill is needed for read-only inventory. |
| Keep all .dev and claudedocs records, including open tasks and embedded source snapshots | Preserve historical artifacts; treat source-looking files inside artifacts as live | self | Shared rules explicitly preserve historical .dev content; path ownership takes precedence over a copied installer's filename. |
| Keep completed logs/decision records and historical memories outside those folders | Preserve evidence; mechanically rewrite every mention | self | Matching excerpts show completed activity or historical context; tool removal must not erase provenance or project knowledge. |
| Treat current-location instructions/specifications as non-historical unless excerpts establish otherwise | Include for owner reconciliation; assume every generated document is historical | self | Coder bundle specifications and audit phase templates still prescribe tool use; folder names alone do not establish obsolescence. |
| Label project-local commands, skills and agents as live config | Executable instruction/configuration surface; ordinary prose docs | self | Their tool lists, server declarations and imperative steps can continue calling removed servers. |
| Use returned hit sets and expose the caps instead of claiming an exhaustive scan | Bounded requested queries with stated limits; broader implementation investigation | self | The task explicitly limits investigation to hit lines and requires the 100-result commands. Further per-repository discovery belongs to the eventual owners. |
| Retry only the two failed enrichment queries after rate-limit reset | Recover excerpts after reset; treat errors as empty results | self | Initial required searches succeeded; the limited retries recovered evidence without silently reporting false zero counts. |
| Assign follow-up ownership to each repository, not named people | Repository owner; invent an individual/team owner | self | Repository names are verified; individual ownership was not investigated. No cross-repository edits are authorized here. |

No middle-level or architectural choice required adversarial comparison; this report inventories and classifies evidence, without selecting a replacement design. No removal has been performed. The local UV environment side effect is explicitly recorded under Search commands and counts and was reported to the coordinator.

## Verification

**PASS: independent evidence review.** The separate reviewer read this report and all seven saved GitHub JSON responses, then mechanically expanded the direct paths, prefix/filename tables and Octodive concatenation sets. Result: 377 exact distinct paths, zero missing or extra paths, zero duplicate entries and zero per-path query-term mismatches; repository metadata, all six query counts, all per-repository live/historical totals and all 26 blob source links matched the saved evidence. They also checked every non-historical excerpt and the 13 additional historical records outside the preserved directory trees. Review artifact: `/tmp/w3-independent-review.md`.

This PASS is limited to inventory fidelity against the saved sample. It does not establish exhaustive GitHub coverage, implementation/runtime state, or compliance with the original local read-only boundary: the disclosed unintended `.venv` creation remains a run deviation. No removal or installation test was performed, as the assignment is inventory only.
