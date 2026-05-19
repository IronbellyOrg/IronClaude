---
name: hook-sync-and-matcher-fix
type: release-spec
version: 1.0
generated: 2026-05-17T18:21:00Z
includes:
  - hook-sync-coverage-spec.md (Part 1 — verify-sync hook coverage, drafted earlier this session)
target_branch: master
target_head_at_design_time: 516bb46
---

# Release: `hook-sync-and-matcher-fix`

Two-part hardening of the hooks distribution pipeline, bundled because each part's
acceptance test is the other part's catch.

- **Part 1** — `make verify-sync` extension to cover hooks (today: covers
  skills/agents/commands only).
- **Part 2** — `auggie-flag-clear.sh` PostToolUse matcher gap fix
  (`mcp__auggie-mcp__*` missing).
- **Part 3** — verify-sync cross-consistency assertion: same prefix list in
  `hooks.json:60` and `auggie-flag-clear.sh` case body.

Each part has independent rollback; the bundle ships as a single PR because
Part 1's verify-sync would catch any regression Part 2 might introduce.

---

## 1. Motivation

### 1.1 Two confirmed bugs on current master (verified 2026-05-17T18:21Z)

**Bug A — `auggie-flag-clear.sh` matcher misses `mcp__auggie-mcp__*`.**
The PostToolUse matcher at `src/superclaude/hooks/hooks.json:60` reads
`"mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"` and the case body at
`src/superclaude/hooks/scripts/auggie-flag-clear.sh:22` reads
`mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*`. Neither covers the
`mcp__auggie-mcp__*` prefix used by the auggie-mcp MCP server actually
installed in this project's SessionStart registry. Consequence: when an
agent calls `mcp__auggie-mcp__ask_question`, the v2.1 sticky never clears
and subsequent actionable Bash commands hit downstream gates as
false-positives. The brainstorm in `hook-sync-coverage-spec.md`'s sibling
record selected **Option 1 (minimal two-file patch)** after adversarial
debate against substring-matching (Option 3, rejected on honor-system
erosion) and externalized prefix list (Option 2, rejected on
over-engineering at N=3 prefixes).

**Bug B — `make verify-sync` does not check hooks.**
`Makefile:154-247` iterates `src/superclaude/skills/`,
`src/superclaude/agents/`, `src/superclaude/commands/` and stops. Hooks
are entirely outside the verification surface. Adding a new hook to
`src/` and forgetting to update `_FRESHNESS_SCRIPTS` in
`install_hooks.py` produces silent end-user-install divergence. Full
problem statement in `hook-sync-coverage-spec.md` (Part 1 of this
release — kept as a separate file because it stands alone).

### 1.2 Concrete evidence — current orphan on master

`.claude/hooks/auggie-bash-gate.sh` exists as an executable file on
disk (`-rwxr-xr-x ... May 17 17:58`) but `src/superclaude/hooks/scripts/auggie-bash-gate.sh` does NOT exist in the
master tree. The file is gitignored. There is a hook deployed to the
dev `.claude/` directory with no source-of-truth counterpart.
`make sync-dev` will not remove it (sync-dev only adds). `make verify-sync`
does not detect it (hooks are outside its scope). It would survive a
re-clone of `.claude/` from `src/`. **This is precisely the failure
mode Part 1 closes** — and the example is real, not hypothetical.

### 1.3 Why bundle

Part 1 and Part 2 are independent fixes, but Part 3 (cross-consistency
assertion) is the structural prevention layer that ensures Bug A
doesn't recur under a different prefix. Part 3 lives in `Makefile`
(verify-sync), so it ships naturally with Part 1. Splitting the parts
into separate PRs would land Bug A's recurrence guard in a different
PR from Bug A's fix, complicating revert ordering. Bundle is the
correct unit.

---

## 2. Scope

### 2.1 In scope

| Part | Surface | Diff size |
|---|---|---|
| 1 | `Makefile` — new `=== Hooks ===` + `=== Installer Registration ===` sections in `verify-sync` | ~50 LOC added |
| 2 | `src/superclaude/hooks/hooks.json` — line 60 matcher widened | 1 LOC changed |
| 2 | `src/superclaude/hooks/scripts/auggie-flag-clear.sh` — line 22 case body widened | 1 LOC changed |
| 3 | `Makefile` — new `=== Hooks Cross-Consistency ===` section in `verify-sync` | ~25 LOC added |
| Tests | `tests/cli/test_verify_sync_hooks.py` (NEW) — pytest wrapper exercising the new verify-sync sections | ~80 LOC |

**Surface total: 1 modified `Makefile`, 1 modified JSON, 1 modified shell script, 1 new test file. ~155 LOC.**

### 2.2 Out of scope

- **The orphan `.claude/hooks/auggie-bash-gate.sh`.** Part 1 will detect
  it. Whether to delete it or re-introduce its src/ source is a
  separate decision the user/maintainer makes after the release lands.
  See §6.
- **`_FRESHNESS_SCRIPTS` ↔ `hooks.json` matcher registration cross-check.**
  Part 1's "Installer Registration" section checks
  `src/superclaude/hooks/scripts/*.sh` against `_FRESHNESS_SCRIPTS`. It does
  NOT check that every `_FRESHNESS_SCRIPTS` entry also has a corresponding
  matcher registration in `hooks.json`. That's a different (and rarer)
  drift class; defer.
- **`session-init.sh`'s legacy path.** Kept special-cased in both
  Makefile and `install_hooks.py`; not touched by this release.
- **The auggie-bash-gate Option 3 work.** Reverted off master; if the
  user wants to re-introduce it, that's a separate PR.

---

## 3. Part 1 — `make verify-sync` hook coverage

Full design in `hook-sync-coverage-spec.md` (sibling file in this dir).
Summary of what lands:

### 3.1 New section: `=== Hooks ===`

Inserted in `Makefile`'s `verify-sync` target between `=== Commands ===`
and the final drift check. Mirrors the existing
skill/agent/command pattern verbatim:

- Forward (src → .claude): for every `src/superclaude/hooks/scripts/*.sh`,
  assert a counterpart exists at `.claude/hooks/<name>` and `diff -q`
  matches.
- Reverse (.claude → src): for every `.claude/hooks/*.sh`, assert a
  counterpart exists at `src/superclaude/hooks/scripts/<name>`.
  Case-skip `session-init.sh` (lives in `src/superclaude/scripts/`).

### 3.2 New section: `=== Installer Registration ===`

Asserts every `src/superclaude/hooks/scripts/*.sh` appears in
`_FRESHNESS_SCRIPTS`. Mechanism: `uv run python -c "from
superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; print(...)"`
combined with `comm`. Reports MISSING and STALE.

---

## 4. Part 2 — matcher gap fix (Option 1, post adversarial debate)

### 4.1 `src/superclaude/hooks/hooks.json:60`

```diff
- "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
+ "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",
```

### 4.2 `src/superclaude/hooks/scripts/auggie-flag-clear.sh:22`

```diff
-    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
+    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)
```

Also update the file-header comment at `auggie-flag-clear.sh:2` to
reflect the widened prefix set:

```diff
-# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.
+# PostToolUse: clear auggie-first sticky after any auggie-prefixed tool call
+# (mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*).
```

### 4.3 Why Option 1 over Options 2 and 3

The companion brainstorm document captured the full adversarial debate.
Verdict summary: Option 3 (substring `mcp__.*auggie.*`) was rejected
because honor-system contract erodes (a future tool named for the auggie
*pattern* but not actually invoking codebase-retrieval would clear the
sticky). Option 2 (externalized prefix list) was rejected because the
abstraction cost exceeds the maintenance cost at today's N=3 prefixes;
revisit if N grows past ~5-7. Option 1 ships the fix and Part 3
structurally prevents the lockstep-drift risk that Option 1 alone
carries.

---

## 5. Part 3 — verify-sync cross-consistency assertion

### 5.1 New section: `=== Hooks Cross-Consistency ===`

Inserted in `Makefile`'s `verify-sync` target after `=== Installer
Registration ===` and before the final drift check.

**What it asserts:** the auggie-prefix set referenced by
`hooks.json:60` matcher (PostToolUse, auggie-flag-clear path) is the
same as the set in `auggie-flag-clear.sh` case body, modulo
regex-vs-glob syntax normalization.

**Implementation sketch:**

```make
echo ""; \
echo "=== Hooks Cross-Consistency ==="; \
matcher_prefixes=$$(jq -r '.hooks.PostToolUse[].matcher // empty' \
    src/superclaude/hooks/hooks.json 2>/dev/null \
    | grep -oE 'mcp__[a-z_-]+(\.\*|_\.\*|__\.\*)?' \
    | grep -i 'auggie' \
    | sed -E 's/\.\*$$//' | sort -u); \
case_prefixes=$$(grep -oE 'mcp__[a-z_-]+(_\*|__\*|\*)' \
    src/superclaude/hooks/scripts/auggie-flag-clear.sh \
    | grep -i 'auggie' \
    | sed -E 's/\*$$//' | sort -u); \
if [ "$$matcher_prefixes" = "$$case_prefixes" ]; then \
    echo "  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes"; \
else \
    echo "  ❌ DRIFT between hooks.json:60 matcher and auggie-flag-clear.sh case body"; \
    echo "      hooks.json prefixes: $$matcher_prefixes"; \
    echo "      auggie-flag-clear.sh prefixes: $$case_prefixes"; \
    drift=1; \
fi; \
```

The normalization strips trailing `.*` (regex) and `*` (glob) so that
`mcp__auggie__.*` and `mcp__auggie__*` compare equal. Edge case: the
gateway prefix has `auggie_.*` vs `auggie_*` (note the underscore inside,
asterisk-or-regex outside) — the regex strip handles both forms.

**Caveat:** this check uses `jq` and assumes `hooks.json` parses
cleanly. If `jq` is missing or the JSON is malformed, the matcher list
is empty and the comparison fails loudly. Both are existing project
prerequisites (`jq` is used in multiple hooks already).

**Why this matters:** Without Part 3, Part 2 ships Option 1's two-file
patch as a maintenance burden the project has already accidentally
violated once (the trailing-comma divergence between `_*` and `_.*`
captured in `hook-sync-coverage-spec.md` Round 1 PRO debate). Part 3 is
the structural prevention that justifies choosing Option 1 over
Option 2.

---

## 6. Concrete consequences this release will surface (orphan handling)

When this release lands and `make verify-sync` first runs on master:

```
=== Hooks ===
  ...
  ❌ MISSING in src/superclaude/hooks/scripts/: auggie-bash-gate.sh (not distributable!)
  ...
```

This is **the orphan `.claude/hooks/auggie-bash-gate.sh` finally being
visible**. The orphan has existed since some point earlier today; on
master it has no source. Three responses are reasonable:

1. **Delete the orphan**: `rm .claude/hooks/auggie-bash-gate.sh` and
   commit. The deployed dev `.claude/` no longer has a stranded script.
2. **Re-introduce the src/ source**: re-add
   `src/superclaude/hooks/scripts/auggie-bash-gate.sh` (verbatim from
   the Option 3 spec at
   `.dev/releases/complete/auggie-first/...` if archived, or
   reconstruct). Run `make sync-dev` and commit.
3. **Defer**: gitignore the path explicitly with a comment explaining
   it's a known-orphan pending a decision. Not recommended — verify-sync
   will block on it on every CI run.

**Out of scope for this release.** The release ships the *detection*;
the *response* is a separate decision by the maintainer. This spec
intentionally avoids choosing for them.

---

## 7. Acceptance criteria

### Part 1
- **AC-1.1**: `make verify-sync` on the post-merge tree (with orphan
  resolved per §6) exits 0.
- **AC-1.2**: `rm .claude/hooks/auggie-flag-clear.sh && make verify-sync`
  reports `❌ MISSING in .claude/hooks/: auggie-flag-clear.sh` and exits
  non-zero. After `make sync-dev`, verify-sync exits 0.
- **AC-1.3**: Temporarily removing an entry from `_FRESHNESS_SCRIPTS` and
  running verify-sync produces `❌ MISSING from _FRESHNESS_SCRIPTS:
  <name>`.

### Part 2
- **AC-2.1**: After patches, `grep mcp__auggie-mcp__ src/superclaude/hooks/hooks.json src/superclaude/hooks/scripts/auggie-flag-clear.sh` returns
  matches in BOTH files.
- **AC-2.2**: Manual end-to-end test in a fresh session: call
  `mcp__auggie-mcp__ask_question(...)`, observe the sticky at
  `~/.claude/state/auggie-first-pending/<session_id>.txt` is removed
  AND a `sticky_cleared` event is appended to
  `~/.claude/logs/auggie-first.jsonl`.

### Part 3
- **AC-3.1**: `make verify-sync` reports `✅ hooks.json matcher and
  auggie-flag-clear.sh case body agree on auggie prefixes` after Part 2
  is applied.
- **AC-3.2**: If a developer adds a prefix to ONE of the two files but
  not the other, `make verify-sync` reports `❌ DRIFT between
  hooks.json:60 matcher and auggie-flag-clear.sh case body` and exits
  non-zero.
- **AC-3.3**: A test in `tests/cli/test_verify_sync_hooks.py` programmatically reproduces AC-3.2 by mutating
  one file at a time in a `tmp_path` checkout and asserting on the
  verify-sync exit code + stderr pattern.

### Aggregate
- **AC-A.1**: `uv run pytest tests/ -v` passes including the new
  `test_verify_sync_hooks.py`. Existing test suite has zero regressions.
- **AC-A.2**: `make lint` clean.

---

## 8. Rollback

Each part rolls back independently. **Recommended order if multiple
parts need backing out:** Part 3 → Part 1 → Part 2. (Part 3 depends on
Part 2's matcher widening; Part 1 is independent of Part 2; Part 2 is
the actual user-facing fix and should be the last to revert.)

- **Part 1 rollback**: delete the `=== Hooks ===` and `=== Installer
  Registration ===` blocks from `Makefile` `verify-sync`.
- **Part 2 rollback**: revert the two one-line patches.
- **Part 3 rollback**: delete the `=== Hooks Cross-Consistency ===`
  block from `Makefile` `verify-sync`.

No state to migrate. No external system dependencies. No data loss
on rollback.

---

## 9. Test plan

**One new test file: `tests/cli/test_verify_sync_hooks.py`.**

Test harness: pytest with `subprocess.run(["make", "verify-sync"], ...)`
invocations, mirroring the pattern from `tests/hooks/test_auggie_first.py`
that already proved successful in this project.

Scenarios:

| # | Setup | Assertion |
|---|---|---|
| V1 | Clean tree | exit=0; stdout contains `=== Hooks ===` and `✅` entries |
| V2 | `rm .claude/hooks/auggie-flag-clear.sh` | exit≠0; stdout contains `❌ MISSING in .claude/hooks/: auggie-flag-clear.sh` |
| V3 | `_FRESHNESS_SCRIPTS` minus one entry (via temp monkey-patch in a `tmp_path` copy) | exit≠0; stdout contains `❌ MISSING from _FRESHNESS_SCRIPTS:` |
| V4 | `_FRESHNESS_SCRIPTS` with extra fake entry | exit≠0; stdout contains `❌ STALE in _FRESHNESS_SCRIPTS:` |
| V5 | hooks.json matcher with one prefix removed, case body unchanged | exit≠0; stdout contains `❌ DRIFT between hooks.json:60 matcher and auggie-flag-clear.sh case body` |
| V6 | case body with one prefix removed, matcher unchanged | exit≠0; same DRIFT message |
| V7 | Both files with `mcp__auggie-mcp__*` removed (regression to current master) | exit≠0; DRIFT message AND the matcher gap is the root cause |

For V3/V4/V5/V6, the tests must operate on a `tmp_path` copy of the
repo so they don't mutate the developer's working tree.

---

## 10. Implementation outline (for downstream `/task-builder`)

If a granular tasklist is needed, the natural phase decomposition is:

1. **Phase 1 — Part 2 patches (smallest, highest user impact)**
   - 2 single-line edits (hooks.json:60, auggie-flag-clear.sh:22)
   - 1 comment-line update (auggie-flag-clear.sh:2)
   - Smoke-test via `make sync-dev` propagation
2. **Phase 2 — Part 1 verify-sync hook sections**
   - Append `=== Hooks ===` block
   - Append `=== Installer Registration ===` block
   - Smoke-test by removing a hook and confirming verify-sync catches it
3. **Phase 3 — Part 3 cross-consistency section**
   - Append `=== Hooks Cross-Consistency ===` block
   - Smoke-test by removing one prefix from one file
4. **Phase 4 — Tests**
   - Create `tests/cli/test_verify_sync_hooks.py` with V1-V7
   - `uv run pytest tests/cli/test_verify_sync_hooks.py -v`
5. **Phase 5 — Orphan resolution (see §6)**
   - This phase is the **decision point**, not an automatable step.
   - User picks: delete orphan, re-add src, or gitignore-with-rationale.
6. **Phase 6 — Final QA gate (rf-qa task-integrity)**

---

## 11. Risks

- **R1**: `jq` dependency in Part 3. Already a project prerequisite
  (used in hook scripts); zero new dependency.
- **R2**: `uv run` dependency in Part 1's installer-registration check.
  Already required by `make test`; zero new dependency.
- **R3**: The orphan detection in §6 may surprise developers on first
  CI run after merge. Mitigation: include a CHANGELOG entry naming the
  orphan, with the three response options enumerated.
- **R4**: If the orphan resolution decision is "re-add src/", the Option 3
  auggie-bash-gate work has to be re-derived. The shipped spec at
  `.dev/releases/complete/auggie-first/` (per the closeout commit
  f64ea62) should contain the source. Out of scope for this release.

---

## 12. Provenance & verification

Verified live 2026-05-17T18:21Z against master HEAD 516bb46:
- `src/superclaude/hooks/hooks.json:60` matcher reads
  `"mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"` (gap confirmed).
- `src/superclaude/hooks/scripts/auggie-flag-clear.sh:22` case body reads
  `mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*` (gap confirmed).
- `src/superclaude/hooks/scripts/auggie-bash-gate.sh` does NOT exist
  (Option 3 implementation reverted off master).
- `.claude/hooks/auggie-bash-gate.sh` exists as a gitignored orphan
  (Part 1's verify-sync extension will detect this).
- `Makefile:154-247` `verify-sync` target iterates only skills, agents,
  commands; no hook coverage.
- Brainstorm and adversarial debate captured at
  `hook-sync-coverage-spec.md` (Part 1 standalone spec) and the
  conversation transcript of session "auggie-gate-Cleanup".

---

**Status:** Specification complete. Ready for `/task-builder` to produce
a granular tasklist against §7 acceptance criteria, then `/task` to
execute.

Suggested PR title: `feat(verify-sync,hooks): cover hooks + close
mcp__auggie-mcp__* matcher gap`.
