# Reviewer 1 brief: persona analyzer, model sonnet (UC-1 pre-execution plan review)

Audit target: the plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md` (Read it in full) against its spec `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/source.md` and the design it implements, `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md`, with the spec's two overrides (always-on mode `lite`, ledger on). Lens: root cause and evidence. Question: will executing these four tasks, as written, deliver the spec and design, and is every factual claim in the plan (repo line refs and upstream Ponytail behaviour) true? Assume mistakes exist. Classify each divergence as authorized | necessary | drift | regression (plan-vs-spec), or route it to a grounding gap; grade each finding blocking or minor (blocking = wrong behaviour, false claim, missing required deliverable, or a security/data-loss risk).

## T1 card excerpt

From `reflection-card.yaml` (verbatim):

```yaml
  - id: F-2
    kind: scope-ambiguity
    claim: "INF-003 says every place the brainstorm says 'off' is rewritten to lite. The plan applies lite to the delivery files (defaults, tests, docs, CHANGELOG) and declares the override in its header; it does not edit merged-requirements.md itself. Whether the spec meant editing the brainstorm file is ambiguous."
  - id: F-4
    kind: unverified-claim
    claim: "[INFERRED] Task 3's 'bare /ponytail switches to full' rests on the brainstorm's citation of upstream ponytail-mode-tracker.js:110-118, which this session did not re-read."
  - id: F-6
    kind: confirmed
    claim: "Lite facts in the plan header match upstream source ..."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T12:45:03Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin

### src/superclaude/cli/install_user_setup.py:251-311

`install_plugins`: wanted = defaults whose settings value is True (:266); marketplace add per missing market (:271-279); install commands `["plugin","install",p,"--scope","user","-y"]` (:280-284); failure labels use `args[3]` (:292, :303, :305). Read it.

### src/superclaude/cli/install_user_setup.py:150-164

`apply_settings_defaults` fills `_NESTED_KEYS` (`env`, `enabledPlugins`, `extraKnownMarketplaces`, `modelSettings`, :36) entry by entry; other top-level keys only when absent.

### Upstream Ponytail v5.3.3 source (fetched this session to /tmp/ponytail-src-t14b/)

- `/tmp/ponytail-src-t14b/hooks_ponytail-activate.js` (SessionStart: off exit, flag, ruleset, map, statusline nudge)
- `/tmp/ponytail-src-t14b/hooks_ponytail-config.js` (mode resolution env > config file > full)
- `/tmp/ponytail-src-t14b/hooks_ponytail-subagent.js` (SubagentStart injection, PONYTAIL_SUBAGENT_MATCHER)
- `/tmp/ponytail-src-t14b/runtime.js` (flag files, per-project mode under ponytail-modes/)
- `/tmp/ponytail-src-t14b/skill.md:50` (lite row)

Verify every lite claim in the plan's "Lite behaviour" block against these files.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-001 implement merged-requirements.md | none (Design reference line) | unmapped by containment | source.md:1 |
| INF-003 rewrite every 'off' default to lite | none (header override) | unmapped by containment | source.md:1 |
| INF-005 lite SessionStart flag + ruleset documented | none (Lite block, Task 3) | unmapped by containment | source.md:1 |
| INF-007 statusline nudge documented, Orca worker sees it | none (Lite block, Task 3) | unmapped by containment | source.md:1 |
| INF-008 /ponytail default has no effect while env set | Task 3 | covered | source.md:1 |
| INF-011 failure-label fix at most 5 lines | Task 2 | covered | source.md:1 |

Return a reviewer card (YAML) with: reviewer, persona, model, verdict, findings (id, claim, evidence as file:line, deviation_class or grounding_gap, severity blocking|minor, recommendation), self_reported_confidence. Do not write files.
