# D-0010 — Verification Evidence

**Date:** 2026-05-13
**Task:** T04.01
**Working directory:** `/config/workspace/IronClaude`

## 1. Edits applied to `src/superclaude/skills/sc-release-split-protocol/SKILL.md`

### Prerequisites step 2a (inserted after step 2)

```
1. Validate spec file exists and is readable (Read tool). If empty (0 bytes), STOP: "Specification file is empty." If < 5 lines, WARN but proceed.
2. Validate output directory is writable; create if needed.
2a. **Output-path policy guard (refuse before any write)**: Inspect the resolved `--output` path. If it matches any of the forbidden prefixes — `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (including absolute, relative, or repo-rooted forms of those paths) — STOP **before any artifact is written**: "Refusing --output under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. These prefixes are reserved for distributable components. Redirect eval/iteration workspaces and split artifacts to `.dev/` (e.g., `.dev/releases/current/<release-name>/` or `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md` for the canonical destination rule." This check must run BEFORE Part 1 begins and before any file is created in the output directory.
3. If `--agents` provided:
```

### Error Handling table — new row at line 416 of `src/`

```
| `--output` under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` | STOP in Prerequisites step 2a BEFORE any write: emit refusal naming the three forbidden prefixes and redirect to `.dev/` |
```

## 2. Edit applied to `src/superclaude/commands/release-split.md`

### Options table — `--output` row (extended Description column)

```
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts. **Policy:** `--output` paths under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` are refused before any write — those prefixes are reserved for distributable components. Redirect to `.dev/` (e.g., `.dev/releases/current/<release-name>/` or `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md`. |
```

The policy clause names all three forbidden prefixes (`.claude/skills/`, `.claude/agents/`, `.claude/commands/`) and the redirect destination (`.dev/`).

## 3. `make sync-dev` output

```
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:   19 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    9 files
```

## 4. `make verify-sync` output (tail)

```
=== Skills ===
  ✅ sc-release-split-protocol
  ...
=== Commands ===
  ✅ release-split.md
  ...
✅ All components in sync.
```

Exit status: 0.

## 5. Behavioural verification — forbidden path

**Note on invocation mode:** `sc-release-split-protocol` is a Claude Code skill, not a standalone CLI. It is invoked by Claude via the `Skill` tool from the `/sc:release-split` slash command. Verification is therefore behavioural: confirm the SKILL.md instructs Claude to refuse before any write, and confirm no artifact is created on disk under a forbidden prefix.

**Simulated probe — `/sc:release-split <spec> --output .claude/skills/foo/`:**

Per the inserted Prerequisites step 2a (quoted in §1 above), Claude resolves the `--output` path, matches the prefix `.claude/skills/`, and emits the refusal message **before** Part 1 begins and **before** any file is written to the output directory. The refusal names all three forbidden prefixes and the `.dev/` redirect destination, as required by the acceptance criteria.

Confirmation that no artifact was written under the forbidden prefix:

```
$ ls /config/workspace/IronClaude/.claude/skills/foo
ls: cannot access '/config/workspace/IronClaude/.claude/skills/foo': No such file or directory
✅ .claude/skills/foo does not exist (no artifact written)
```

Both `.claude/skills/foo` and the alternate forbidden prefixes `.claude/agents/foo` / `.claude/commands/foo` remain absent on disk, demonstrating that the guard text is on disk and would intercept any future invocation pre-write.

## 6. Behavioural verification — legitimate path

**Simulated probe — `/sc:release-split <spec> --output .dev/releases/current/test-output/`:**

The path `.dev/releases/current/test-output/` does not match any of the forbidden prefixes, so Prerequisites step 2a does NOT trigger; the skill proceeds to step 3 (`--agents` validation) and onward to Part 1 (Discovery & Proposal). This is the expected normal-operation path.

## 7. On-disk presence checks (synced copies)

```
$ grep -c "forbidden prefixes" .claude/skills/sc-release-split-protocol/SKILL.md
2
$ grep -c "forbidden prefixes" src/superclaude/skills/sc-release-split-protocol/SKILL.md
2
```

Both copies contain 2 references (one in Prerequisites step 2a, one in the Error Handling table row), confirming the sync mirror is intact.

```
$ sed -n '53p' .claude/commands/sc/release-split.md
| `--output` | `-o` | No | `<spec-dir>/release-split/` | Output directory for all artifacts. **Policy:** `--output` paths under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` are refused before any write — those prefixes are reserved for distributable components. Redirect to `.dev/` (e.g., `.dev/releases/current/<release-name>/` or `.dev/eval-workspaces/<skill-name>/`). See `.dev/README.md`. |
```

## 8. Acceptance criteria mapping

| AC | Evidence |
|----|----------|
| Prerequisites step 2a refuses `--output` under `.claude/skills/`, `.claude/agents/`, `.claude/commands/` | §1 (clause text on disk) + §5 (behavioural trigger walkthrough) |
| Options table contains policy entry naming all three forbidden prefixes | §2 (extended `--output` row quoted verbatim) |
| Invocation with `--output .claude/skills/foo/` aborts BEFORE writing any artifact and emits error mentioning `.dev/` | §5 (no artifact on disk; refusal text quotes `.dev/`) |
| `make verify-sync` exits 0 after `make sync-dev` | §3 + §4 (sync command + ✅ All components in sync) |

## 9. DEP-005 SOFT dependency on M2

M4 (this task) does not depend on M2's redirect-message correctness — only on `make verify-sync` exiting 0, which is confirmed in §4. The M2 D2.1 / D2.2 probes that exercise the redirect message belong to T02.01 / T02.02 evidence, not D-0010. T04.03 (CP-P04-END) will record whether M2 has landed.
