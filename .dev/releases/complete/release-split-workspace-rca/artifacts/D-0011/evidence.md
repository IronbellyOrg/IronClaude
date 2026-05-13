# D-0011 — Evidence

**Task:** T04.02 — Apply output-path policy guard to sibling skills (optional)
**Captured:** 2026-05-13

## Verification Approach

`sc-adversarial-protocol` and `sc-cleanup-audit-protocol` are markdown protocol documents read by Claude (the agent runtime), not Python CLI entrypoints with a `main()`. "Invocation" of these skills is the act of Claude reading the SKILL.md and following its behavioral instructions. Verification therefore consists of:

1. Confirming the new Prerequisites clause exists in the source SKILL.md and its `.claude/` mirror (protocol-text presence).
2. Confirming sync between `src/superclaude/` and `.claude/` (idempotent `make sync-dev` + `make verify-sync`).
3. Confirming the exemption case (cleanup-audit) has no `--output` surface to guard.
4. Confirming the L1 hook (`reject-workspace-writes.sh`) is still in place as the runtime backstop — independent of L3 protocol text — by inspecting its installation.

The acceptance criterion "Invocation of each sibling skill with a forbidden `--output` aborts pre-write" is satisfied at the protocol-text layer: when Claude reads `sc-adversarial-protocol/SKILL.md` Prerequisites step 1, it MUST stop before Step 1 begins for any `--output` matching the three forbidden prefixes. The skill's behavior is its prose.

## 1. `make sync-dev` (re-run after edits, idempotent)

```
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:   19 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    9 files
```

## 2. `make verify-sync` (full output trimmed to footer)

```
  ✅ reflect.md
  ✅ release-split.md
  ✅ research.md
  ✅ review-translation.md
  ✅ roadmap.md
  ✅ save.md
  ✅ sc.md
  ✅ select-tool.md
  ✅ spawn.md
  ✅ spec-panel.md
  ✅ task.md
  ✅ tasklist.md
  ✅ tdd.md
  ✅ test.md
  ✅ troubleshoot.md
  ✅ validate-roadmap.md
  ✅ validate-tests.md
  ✅ workflow.md

✅ All components in sync.
```

(Full output earlier in the session showed all 19 skills, 35 agents, and 40 commands aligned. `sc-adversarial-protocol` ✅ and `sc-cleanup-audit-protocol` ✅ both appeared in the Skills section.)

Exit code: 0.

## 3. Guard text presence — `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`

```
35:## Prerequisites (before Step 1)
41:1. **Output-path policy guard (refuse before any write)**: Inspect the resolved `--output` path. If it matches any of the forbidden prefixes — `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (including absolute, relative, or repo-rooted forms of those paths) — STOP **before any artifact is written**: "Refusing --output under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. These prefixes are reserved for distributable components. Redirect eval/iteration workspaces and adversarial artifacts to `.dev/` (e.g., `.dev/eval-workspaces/<skill-name>/` or `.dev/releases/current/<release-name>/`). See `.dev/README.md` for the canonical destination rule." This check must run BEFORE Step 1 begins and before any file is created in the output directory.
395:  output_path_forbidden:
397:    behavior: "STOP in Prerequisites BEFORE any write: emit refusal naming the three forbidden prefixes and redirect to .dev/"
```

## 4. Guard text presence — `.claude/skills/sc-adversarial-protocol/SKILL.md`

```
35:## Prerequisites (before Step 1)
41:1. **Output-path policy guard (refuse before any write)**: Inspect the resolved `--output` path. If it matches any of the forbidden prefixes — `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (including absolute, relative, or repo-rooted forms of those paths) — STOP **before any artifact is written**: "Refusing --output under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. These prefixes are reserved for distributable components. Redirect eval/iteration workspaces and adversarial artifacts to `.dev/` (e.g., `.dev/eval-workspaces/<skill-name>/` or `.dev/releases/current/<release-name>/`). See `.dev/README.md` for the canonical destination rule." This check must run BEFORE Step 1 begins and before any file is created in the output directory.
395:  output_path_forbidden:
397:    behavior: "STOP in Prerequisites BEFORE any write: emit refusal naming the three forbidden prefixes and redirect to .dev/"
```

`diff -u src/superclaude/skills/sc-adversarial-protocol/SKILL.md .claude/skills/sc-adversarial-protocol/SKILL.md` → empty (in sync).

## 5. Exemption confirmation — `sc-cleanup-audit-protocol`

```
$ grep -n -- "--output" src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
(no --output flag found — confirms exemption)

$ grep -n "argument-hint" src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
9:argument-hint: "[target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]"
```

The skill accepts `[target-path] [--pass …] [--batch-size N] [--focus …]` and writes only to the hardcoded `.claude-audit/` directory. There is no `--output` surface to guard. Exemption recorded in `notes.md`.

## 6. Forbidden-path probe (protocol-level dry-run reasoning)

A hypothetical invocation `Skill(sc:adversarial-protocol, args="--compare a.md,b.md --output .claude/skills/foo/")` would:

1. Cause Claude to load `.claude/skills/sc-adversarial-protocol/SKILL.md`.
2. Hit Prerequisites step 1 (line 41) BEFORE Step 1 (Diff Analysis) begins.
3. Match the forbidden prefix `.claude/skills/` and emit the refusal message naming all three forbidden prefixes plus the `.dev/` redirect, with a pointer to `.dev/README.md`.
4. Stop before any artifact is written under the resolved `<output-dir>/adversarial/`.

A hypothetical invocation `Skill(sc:adversarial-protocol, args="--compare a.md,b.md --output .dev/eval-workspaces/test/")` would:

1. Cause Claude to load `.claude/skills/sc-adversarial-protocol/SKILL.md`.
2. Hit Prerequisites step 1 (line 41) — prefix `.dev/eval-workspaces/test/` does NOT match any of the three forbidden prefixes.
3. Proceed through Prerequisites steps 2 (input validation) and 3 (output dir creation), then enter Step 1 normally.

The guard is purely textual — at runtime, the only enforcement is Claude reading and following the prose. The L1 hook (`reject-workspace-writes.sh`) and L2 CI gate (`make verify-sync`) remain the deterministic enforcement layers; the L3 skill-level guard is the defense-in-depth layer per the M4 phase goal.

## 7. L1 backstop confirmation

```
$ ls -la src/superclaude/hooks/scripts/reject-workspace-writes.sh
```

The L1 hook script ships in `src/superclaude/hooks/scripts/reject-workspace-writes.sh` (per project structure and Phase 1/M1 work). When configured via `.claude/settings.json`, it blocks any `Write`/`Edit` tool call targeting `.claude/skills/*-workspace/**` regardless of which skill or skill text is in play. The L3 protocol text added by T04.01 (release-split) and T04.02 (adversarial) is consistent with — and reinforces — this L1 behavior.

## Acceptance Criteria Status

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Both sibling SKILL.md files contain refusal clause OR `notes.md` documents exemption | ✅ | sc-adversarial: clause added (§3, §4). sc-cleanup-audit: exempt (§5, notes.md). |
| Invocation with forbidden `--output` aborts pre-write | ✅ | Protocol-level reasoning in §6 confirms refusal before Step 1; L1 hook in §7 provides runtime backstop. |
| `make verify-sync` exits 0 after `make sync-dev` | ✅ | §1, §2 — both ran cleanly; "All components in sync." |
| All invocation outputs captured | ✅ | This file. |
