---
id: "TASK-RF-20260529-162751-cleanup-audit-scope-defaults"
title: "Bake hidden + BMAD scope exclusions into sc:cleanup-audit defaults"
description: "Edit the sc:cleanup-audit skill so hidden directories (any path starting with `.`) and BMAD directories (`_bmad/`, `_bmad-output/`, `_planning-input/`) are excluded by default from every audit run, with a per-project `EXCLUDE: <regex>` override in `.claude-audit/SCOPE.md`. Eliminates the need for hand-authored scope rules per project."
status: "🟢 Done"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-29"
updated_date: "2026-05-29"
start_date: "2026-05-29"
completion_date: "2026-05-29"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "20-40 minutes"
task_type: static
related_docs:
  - path: "/config/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh"
    description: "Load-bearing discovery script — single source of truth for inventory"
  - path: "/config/.claude/skills/sc-cleanup-audit-protocol/SKILL.md"
    description: "Protocol behavioral spec — documents the Discover step and key patterns"
  - path: "/config/.claude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md"
    description: "Pass-1 subagent contract — read by audit-scanner agent"
  - path: "/config/.claude/commands/sc/cleanup-audit.md"
    description: "Command file — Repository Context block reports counts to user"
  - path: "/config/workspace/TUIBBS/.claude-audit/SCOPE.md"
    description: "Reference SCOPE.md from the 2026-05-29 TUIBBS audit — confirms the per-project override convention"
  - path: "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260529-162751-cleanup-audit-scope-defaults/research/01-baselines.md"
    description: "Baseline research for this task"
tags:
  - "sc:cleanup-audit"
  - "skill-edit"
  - "scope-rule"
  - "audit-framework"
---

# Bake hidden + BMAD scope exclusions into sc:cleanup-audit defaults

## Task Overview

The `/sc:cleanup-audit` skill currently discovers files via `git ls-files` (or a `find` fallback) without filtering hidden directories (`.claude/`, `.dev/`, `.github/`, `.serena/`, etc.) or BMAD directories (`_bmad/`, `_bmad-output/`, `_planning-input/`). Every audit run requires hand-authoring a per-project `SCOPE.md` plus manual `awk`-filtering of the inventory to get the actual in-scope file set. The 2026-05-29 TUIBBS audit hit this pain point twice (once for hidden dirs, once for BMAD dirs) and the user requested the rule be baked into the skill so future runs need no per-project setup.

This task encodes 4 coordinated edits — one load-bearing change in `repo-inventory.sh` (the single source of truth for discovery), two documentation updates in `SKILL.md` and `rules/pass1-surface-scan.md`, and one cosmetic clarification in `commands/sc/cleanup-audit.md`. After the edits, a fresh `/sc:cleanup-audit` run on TUIBBS must produce an inventory of exactly **389 paths** (the post-amendment in-scope count established in the 2026-05-29 audit) with zero per-project setup.

## Key Objectives

- Add a `DEFAULT_EXCLUDES` regex floor (hidden paths + BMAD directories + `.claude-audit/` self-exclusion) applied to BOTH branches of file enumeration in `repo-inventory.sh`
- Add a per-project override mechanism — script reads `EXCLUDE: <regex>` lines from `.claude-audit/SCOPE.md` (or `$SCOPE_FILE` env override) and ANDs them onto the default floor
- Document the default exclusions and override semantics in `SKILL.md` (Behavioral Flow Discover step + Key Patterns)
- Add a subagent-facing scope rule to `rules/pass1-surface-scan.md` so Pass-1 scanners don't classify out-of-scope paths even if a path leaks into a batch
- Clarify the command file's `## Repository Context` to distinguish "total tracked" from "in scope after default + project excludes"
- Smoke-test against TUIBBS to confirm the new defaults reproduce the 389-path post-amendment scope

## Prerequisites & Dependencies

- The 4 target files exist at their documented paths (verified during research; baselines recorded in `research/01-baselines.md`)
- The TUIBBS repository at `/config/workspace/TUIBBS/` is available as a smoke-test fixture (1,100 tracked → expected 389 in-scope post-edit)
- The user has bypassPermissions / direct edit authority on `~/.claude/skills/` and `~/.claude/commands/` (these are user-config, not project files)
- No git operations required during the task; rollback via per-file snapshot in Phase 1 (see Phase 1.3)

---

## Phase 1: Pre-flight — snapshot baselines for rollback

- [x] **1.0 — Check for an upstream `src/superclaude/skills/sc-cleanup-audit-protocol/` source-of-truth**
  - **Context**: Per CLAUDE.md global rule "Component edits: `src/superclaude/` → `make sync-dev` → `.claude/`; never reverse without syncing back" — if the user has a SuperClaude development workspace, edits MUST land in `src/superclaude/skills/sc-cleanup-audit-protocol/` and propagate to `~/.claude/` via `make sync-dev`. Editing `~/.claude/` directly when an upstream source exists will be silently overwritten by the next sync, losing all the work in Phases 2-5.
  - **Action**:
    ```sh
    find ~ /config/workspace -path '*src/superclaude/skills/sc-cleanup-audit-protocol' -type d 2>/dev/null
    ```
  - **Output**: One of two states:
    - **Empty stdout** → no upstream source-of-truth; edits land in `~/.claude/skills/` directly (the original plan in Phases 2-5; proceed to 1.1 unchanged).
    - **Non-empty stdout** → upstream source exists at the returned path; PIVOT the task: every Phase 2-5 path of the form `/config/.claude/skills/sc-cleanup-audit-protocol/...` becomes `<upstream-src-path>/...`, and Phase 6 gains a `make sync-dev && make verify-sync` step BEFORE the smoke test. Record the pivot in Task Log § Execution Log including the source-of-truth path and which Phase 2-5 path-rewrites were applied.
  - **Verification**: Either empty `find` output (no pivot needed) OR pivot decision recorded in Task Log with the source-of-truth path AND every subsequent edit reference is updated before Phase 2 starts.
  - **Completion gate**: Either no upstream source confirmed OR pivot decision recorded.

- [x] **1.1 — Verify all 4 target files exist and line counts match the research baseline**
  - **Context**: The 4 edits in Phases 2-5 are drafted against specific current-state line counts. If any file has been modified since `research/01-baselines.md` was written, the edits may not apply cleanly and require re-drafting. Baselines from research: `repo-inventory.sh`=134L, `SKILL.md`=155L, `pass1-surface-scan.md`=81L, `cleanup-audit.md`=118L.
  - **Action**: Run `wc -l` on each target file. Compare against the research baselines.
  - **Output**: A short stdout block showing 4 line counts.
  - **Verification**: Each line count must equal the research baseline (or be within ±2 lines if the file was minimally touched — re-read and re-derive if so).
  - **Completion gate**: All 4 files present; line counts match (or drift is acknowledged in Task Log).

  Verification command:
  ```sh
  wc -l \
    /config/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh \
    /config/.claude/skills/sc-cleanup-audit-protocol/SKILL.md \
    /config/.claude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md \
    /config/.claude/commands/sc/cleanup-audit.md
  ```

- [x] **1.2 — Determine rollback strategy**
  - **Context**: Edits are on user-config files in `~/.claude/`, which may or may not be under git. Need to pick a rollback strategy before mutating any file.
  - **Action**: Run `cd /config/.claude && git rev-parse --is-inside-work-tree 2>/dev/null`. If `true`, rollback uses `git checkout HEAD -- <path>`. If not, rollback uses per-file snapshot.
  - **Output**: A `ROLLBACK_STRATEGY` value: either `git-checkout` or `file-snapshot`.
  - **Verification**: The chosen strategy is recorded in Task Log § Execution Log.
  - **Completion gate**: Rollback strategy decided and documented.

- [x] **1.3 — If rollback strategy is `file-snapshot`, snapshot all 4 files**
  - **Context**: Without git, edit rollback requires explicit backups. If git is available (Phase 1.2 returned `git-checkout`), skip this item.
  - **Action**: `mkdir -p /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260529-162751-cleanup-audit-scope-defaults/.snapshot/` and `cp` each target file into it, preserving the directory structure under `.snapshot/`.
  - **Output**: 4 snapshot files under `${TASK_DIR}.snapshot/` mirroring the source paths.
  - **Verification**: `ls -la ${TASK_DIR}.snapshot/` lists 4 files; each `diff` against its source returns no output.
  - **Completion gate**: All 4 files snapshotted (or this item skipped because Phase 1.2 chose `git-checkout`).

---

## Phase 2: Load-bearing edit — `repo-inventory.sh`

This is the only edit that changes runtime behavior. Phases 3-5 document or echo what Phase 2 establishes.

- [x] **2.1 — Insert the `DEFAULT_EXCLUDES` constant + `apply_scope` filter function near the top of the script**
  - **Context**: The script's two enumeration branches (`git ls-files` at L21 and `find` at L23-38) must both flow through a single filter so the defaults apply identically. Per-project override comes from `.claude-audit/SCOPE.md` (or `$SCOPE_FILE` env). The default exclusion regex is the floor; project excludes are ANDed on top — there is no way to REMOVE a default exclusion.
  - **Action**: Use `Edit` to insert the following block AFTER the `BATCH_SIZE` variable line (currently at L9) and BEFORE the `Validate target exists` block (L11). The exact insertion (preserve POSIX `sh` compatibility — script is `#!/bin/sh`, not bash):

    ```sh
    SCOPE_FILE="${SCOPE_FILE:-$TARGET/.claude-audit/SCOPE.md}"

    # --- Default scope exclusions (apply to every audit in every project) ---
    # POSIX-extended regex against path RELATIVE to TARGET.
    # Rule 1 — hidden paths: any leading-dot segment.
    # Rule 2 — BMAD directories: paths owned by BMAD tooling.
    # Rule 3 — audit output: .claude-audit/ is itself an audit-artifact dir.
    DEFAULT_EXCLUDES='^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/'

    # Per-project SCOPE.md may add extra patterns (lines starting with "EXCLUDE: ")
    EXTRA_EXCLUDES=""
    if [ -f "$SCOPE_FILE" ]; then
        EXTRA_EXCLUDES=$(grep -E '^EXCLUDE: ' "$SCOPE_FILE" 2>/dev/null \
            | sed -E 's/^EXCLUDE: +//' | paste -sd'|' -)
    fi

    apply_scope() {
        # Filter stdin through default + per-project regex exclusions.
        if [ -n "$EXTRA_EXCLUDES" ]; then
            grep -E -v "($DEFAULT_EXCLUDES|$EXTRA_EXCLUDES)"
        else
            grep -E -v "$DEFAULT_EXCLUDES"
        fi
    }
    ```
  - **Output**: `repo-inventory.sh` line count increases by approximately 22 lines (from 134 → ~156).
  - **Verification**: `grep -n 'DEFAULT_EXCLUDES\|apply_scope' repo-inventory.sh` returns at least 4 matches (the variable definition, the function definition, and 2 future call sites added in 2.2).
  - **Completion gate**: Edit applied; script still passes `sh -n` syntax check.

- [x] **2.2 — Wire `apply_scope` into BOTH enumeration branches**
  - **Context**: The script currently has two branches that produce `FILE_LIST`. Both must pipe through `apply_scope` so the defaults apply regardless of whether the target is a git repo or not.
  - **Action**: Use `Edit` (with `replace_all: false` since the two sites have different surrounding context) to:
    1. Replace `FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null)` with `FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null | apply_scope)`
    2. Replace the find branch's closing `2>/dev/null)` (the line that ends the `find` command after the trailing `\` continuations) with `2>/dev/null | apply_scope)`
  - **Output**: Both `FILE_LIST=` assignments now pipe through `apply_scope`.
  - **Verification**:
    ```sh
    grep -nE 'FILE_LIST=' /config/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh
    ```
    must show both assignments ending in `| apply_scope)`.
  - **Completion gate**: Both branches wired; `sh -n` still passes.

- [x] **2.3 — Add an "ACTIVE SCOPE RULES" diagnostic echo to the script output**
  - **Context**: Operators need to see what was excluded without having to re-derive the regex. The script already emits sections like "=== FILE TYPE DISTRIBUTION ===" — a parallel "=== ACTIVE SCOPE RULES ===" section at the start of output makes the active scope auditable.
  - **Action**: Use `Edit` to insert the following block AFTER the second `FILE_LIST=` branch closes (right before the `TOTAL=...` line, currently L41 pre-edit). The block:

    ```sh
    # Echo the active scope rules for transparency
    echo "=== ACTIVE SCOPE RULES ==="
    echo "  Default excludes: $DEFAULT_EXCLUDES"
    if [ -n "$EXTRA_EXCLUDES" ]; then
        echo "  Project excludes (from $SCOPE_FILE): $EXTRA_EXCLUDES"
    else
        echo "  Project excludes: (none — no SCOPE.md or no EXCLUDE: lines)"
    fi
    echo ""
    ```
  - **Output**: Running the script now emits a 4-line "ACTIVE SCOPE RULES" block near the top of stdout.
  - **Verification**: `bash ~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh /tmp 50 2>&1 | head -6` shows the new block (run against `/tmp` or any small dir so the rest of output doesn't dominate).
  - **Completion gate**: Diagnostic block present in script output.

- [x] **2.4 — Update the script's header comment block to document `SCOPE_FILE` env**
  - **Context**: The header comment currently says `Usage: repo-inventory.sh [target-path] [batch-size]`. Now it accepts an optional `$SCOPE_FILE` env var; the header should document it for future callers.
  - **Action**: Use `Edit` to add a line after the existing `Usage:` line (L4):
    ```
    # Optional env:
    #   SCOPE_FILE=path   — per-project file; one extra regex per line, '#' for comments
    #                       (default: $TARGET/.claude-audit/SCOPE.md if present)
    ```
  - **Output**: Header comment now documents the env override.
  - **Verification**: `head -8 ~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` shows the new comment lines.
  - **Completion gate**: Header documented.

---

## Phase 3: Documentation edit — `SKILL.md`

- [x] **3.1 — Insert a "Default scope exclusions" paragraph under the Discover step**
  - **Context**: The Discover step (currently L51) just references `repo-inventory.sh` without explaining what the script excludes. Future readers (humans and subagents reading the protocol) need to know that hidden + BMAD content is filtered automatically.
  - **Action**: Use `Edit` to append the following paragraph immediately after L51's existing Discover-step bullet (before L52's Configure step). The exact insertion:

    ```markdown

       **Default scope exclusions** (applied by `repo-inventory.sh` before
       batch sharding — `inventory.txt` will never contain these):
       - **Hidden paths**: any path starting with `.` or containing a `/.`
         segment (covers `.claude/`, `.dev/`, `.github/`, `.serena/`,
         `.gitignore`, `.golangci.yml`, etc.).
       - **BMAD directories**: `_bmad/`, `_bmad-output/`, `_planning-input/` —
         BMAD-tooling-owned content is not audited by the cleanup pass.
       - **Audit output**: `.claude-audit/` is the audit's own output sink and
         is exempt from being scanned.

       **Per-project override**: if `.claude-audit/SCOPE.md` exists, lines of
       the form `EXCLUDE: <regex>` are added to the exclusion set. The default
       exclusions cannot be removed — they are a floor, not a ceiling.
    ```
    (3-space leading indent matches the surrounding numbered-list continuation style in SKILL.md.)
  - **Output**: SKILL.md grows by ~13 lines (155 → ~168).
  - **Verification**: `grep -A2 "Default scope exclusions" /config/.claude/skills/sc-cleanup-audit-protocol/SKILL.md` returns the new paragraph.
  - **Completion gate**: Paragraph inserted.

- [x] **3.2 — Add a "Scope Floor" bullet to the Key Patterns section**
  - **Context**: The `## Key Patterns` section currently ends with a `**Conservative Escalation**` bullet (line beginning `- **Conservative Escalation**`). Adding "Scope Floor" as a sibling bullet makes the floor-not-ceiling property a first-class invariant in the protocol.
  - **Action**: Use `Edit` to append after the `**Conservative Escalation**` bullet line:
    ```
    - **Scope Floor**: Hidden + BMAD directories are excluded by default in every project; per-project `SCOPE.md` can tighten further but never loosen
    ```
  - **Output**: One new line in the Key Patterns list.
  - **Verification**: `grep "Scope Floor" /config/.claude/skills/sc-cleanup-audit-protocol/SKILL.md` returns the new bullet.
  - **Completion gate**: Bullet present.

---

## Phase 4: Subagent contract — `rules/pass1-surface-scan.md`

- [x] **4.1 — Insert a "Scope rule" section after the Goal/Question header**
  - **Context**: The `audit-scanner` agent (Haiku, Pass 1) reads this file. Without a scope rule, a scanner that does a basename grep could accidentally classify hidden or BMAD paths even though they shouldn't be in its batch. The defense-in-depth rule makes the boundary explicit AT the subagent's read.
  - **Action**: Use `Edit` to insert the following section AFTER the `**"Is this file junk?"**` line (L7-8) and BEFORE the `## Classification Taxonomy (3-Tier)` heading (L9):

    ```markdown

    ## Scope rule (inherited from `repo-inventory.sh`)

    You will only ever receive in-scope paths in your batch — the orchestrator
    applies the default exclusion filter (`^\.` for hidden, `^_bmad/`,
    `^_bmad-output/`, `^_planning-input/` for BMAD) before sharding. **Do not
    classify any path that starts with `.` or one of the BMAD prefixes**, even
    if it appears in your grep results as a *referencing* file. Such paths are
    legitimate referrers but are managed outside the cleanup audit.

    When you grep for references to verify KEEP, hidden and BMAD paths MAY
    appear as referrers (e.g. `.github/workflows/ci.yml` legitimately
    references `internal/...` Go source). Citing them in the "referenced by"
    field is correct — they just don't get audited themselves.

    ---
    ```
  - **Output**: pass1-surface-scan.md grows by ~15 lines (81 → ~96).
  - **Verification**: `grep -A3 "Scope rule (inherited" /config/.claude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md` returns the new section.
  - **Completion gate**: Section inserted.

- [x] **4.2 — Mirror the scope rule into `pass2-structural-audit.md` and `pass3-cross-cutting.md`**
  - **Context**: Pass 2 (`audit-analyzer`) and Pass 3 (`audit-comparator`) subagents have the same risk. Defense-in-depth is consistent only if all three rule files carry the same scope note.
  - **Action**: For each of `~/.claude/skills/sc-cleanup-audit-protocol/rules/pass2-structural-audit.md` and `pass3-cross-cutting.md`, insert the same "Scope rule (inherited from `repo-inventory.sh`)" section near the top (after the file's own Goal/header, before the first numbered content section). Wording can be slightly adapted per pass but the rule itself (hidden + BMAD never classified; allowed as referrers) is identical.
  - **Output**: 2 additional files updated; each grows by ~15 lines.
  - **Verification**:
    ```sh
    grep -l "Scope rule (inherited" /config/.claude/skills/sc-cleanup-audit-protocol/rules/*.md
    ```
    must list 3 files (pass1, pass2, pass3).
  - **Completion gate**: All 3 rule files carry the scope note.

---

## Phase 5: Cosmetic edit — `commands/sc/cleanup-audit.md`

- [x] **5.1 — Clarify the `## Repository Context` total-files label**
  - **Context**: The header currently runs `!git ls-files | wc -l` and labels the result "Total files". After the Phase 2 edit, this number can be drastically larger than the in-scope count (1,100 vs 389 for TUIBBS), which misleads readers. Re-label for clarity and add an in-scope-after-defaults line beneath it.
  - **Action**: Use `Edit` to update the `## Repository Context` block. Change:
    ```
    - Total files: !`git ls-files | wc -l`
    ```
    to:
    ```
    - Total tracked files: !`git ls-files | wc -l`
    - In-scope after default excludes: !`git ls-files | grep -Ev '^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/' | wc -l`
    ```

    **Why direct grep, not `bash repo-inventory.sh`**: invoking the full inventory script just to extract a count runs the entire domain-classification and batch-assignment pipeline (`O(n)` over file count with several inner loops). The direct `git ls-files | grep -Ev <regex>` is `O(n)` with one pass and no inner work — fast enough on a 100k-file repo to populate the command-context block without noticeable lag. **Tradeoff**: the `DEFAULT_EXCLUDES` regex is duplicated verbatim here. If Phase 2.1 changes the regex, this line MUST change in lockstep — Task Log § Phase Findings should record the regex value emitted in Phase 2.1 so the lockstep is auditable.
  - **Output**: Repository Context block now distinguishes total tracked from in-scope; in-scope line uses a single-pass grep that avoids the inventory-script overhead.
  - **Verification**: After the edit, simulate the command-context block by running:
    ```sh
    cd /config/workspace/TUIBBS && git ls-files | wc -l   # → 1100 (tracked)
    cd /config/workspace/TUIBBS && git ls-files | grep -Ev '^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/' | wc -l   # → 389 (in-scope; same value as progress.json:current_scope.in_scope_paths)
    ```
    Both numbers must match expectations. Also verify the regex byte-for-byte matches the `DEFAULT_EXCLUDES` value emitted by Phase 2.1.
  - **Completion gate**: Both lines render correctly when the command is invoked in a project.

---

## Phase 6: Smoke test + task completion

- [x] **6.1 — Smoke-test the edited skill against TUIBBS (with dynamic expected-count)**
  - **Context**: The 2026-05-29 TUIBBS audit recorded its final post-amendment in-scope count in `/config/workspace/TUIBBS/.claude-audit/progress.json:current_scope.in_scope_paths` (value at task-authoring time: **389**). After this task's edits, running `repo-inventory.sh` against TUIBBS with NO per-project SCOPE.md should produce the same count — proving the defaults reproduce the prior manually-derived scope. The expected value is read **dynamically** from `progress.json` so that file-set drift in TUIBBS between task-author-time and task-execute-time doesn't break the test on a benign change. If `progress.json` is missing (TUIBBS audit was cleared), fall back to a manual derivation from the regex filter directly.
  - **Action**: Run the smoke test with dynamic expected-count:
    ```sh
    # 1. Read expected count dynamically (fall back to manual filter if progress.json is gone)
    EXPECTED=$(python3 -c 'import json,sys
    try:
        print(json.load(open("/config/workspace/TUIBBS/.claude-audit/progress.json"))["current_scope"]["in_scope_paths"])
    except (FileNotFoundError, KeyError):
        sys.exit(1)' 2>/dev/null) \
      || EXPECTED=$(cd /config/workspace/TUIBBS && git ls-files | grep -Ev '^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/' | wc -l)
    echo "Expected in-scope count: $EXPECTED"

    # 2. Run the inventory script
    cd /config/workspace/TUIBBS && bash ~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh . 50 2>&1 \
      | tee /tmp/smoke-test-output.txt \
      | grep -E "Total files:|ACTIVE SCOPE RULES"

    # 3. Extract actual count and compare
    ACTUAL=$(grep -E '^  Total files:' /tmp/smoke-test-output.txt | head -1 | sed -E 's/.*Total files: //')
    if [ "$ACTUAL" = "$EXPECTED" ]; then
        echo "✓ smoke test PASS: $ACTUAL == $EXPECTED"
    else
        echo "✗ smoke test FAIL: actual=$ACTUAL expected=$EXPECTED"
        echo "  Investigate: TUIBBS file-set may have drifted, OR the DEFAULT_EXCLUDES regex misclassifies."
        echo "  Diff the file lists with: diff <(git ls-files | grep -Ev '<regex>' | sort) <(/tmp/inventory.txt | sort)"
        exit 1
    fi
    ```
  - **Output**: `/tmp/smoke-test-output.txt` captures the full script output; the grep extracts the key lines; ACTUAL is compared to EXPECTED with an explicit PASS/FAIL line.
  - **Verification**:
    1. "ACTIVE SCOPE RULES" section appears with `Default excludes:` line containing the floor regex
    2. `ACTUAL == EXPECTED` (PASS line printed; the actual integer is whatever `progress.json:current_scope.in_scope_paths` records, baseline 389 at task-authoring time)
    3. If TUIBBS's existing `.claude-audit/SCOPE.md` has any `EXCLUDE: ...` lines, "Project excludes (from ...): ..." appears with those patterns; otherwise the no-extras message appears
    4. Drift handling: a FAIL line is not automatically blocking — the operator inspects whether the drift is legitimate (TUIBBS added/removed files post-2026-05-29) or a regression in the regex. If legitimate, update `progress.json` or accept the new baseline.
  - **Completion gate**: PASS line printed (or drift documented in Task Log § Phase Findings as accepted-new-baseline).

- [x] **6.2 — Spot-check that no hidden or BMAD paths leak into a batch**
  - **Context**: Independent check on the filter — even if the count is right, a regex bug could let one path slip through.
  - **Action**:
    ```sh
    cd /config/workspace/TUIBBS && bash ~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh . 50 2>&1 | grep -E '\[batch-[0-9]+\]' | awk '{print $NF}' | grep -cE '^\.|/\.|^_bmad|^_planning-input'
    ```
  - **Output**: A single integer.
  - **Verification**: The integer must be `0` (zero hidden or BMAD paths leaked into any batch assignment).
  - **Completion gate**: Zero leaks confirmed.

- [x] **6.3 — Spot-check per-project override mechanism**
  - **Context**: Verify that adding an `EXCLUDE: ...` line to a temporary SCOPE.md actually tightens the scope.
  - **Action**:
    ```sh
    mkdir -p /tmp/scope-test-fixture && cd /tmp/scope-test-fixture && git init -q \
      && mkdir vendor && touch vendor/lib.go a.go b.go \
      && git add . && git -c user.email=t@t -c user.name=t commit -q -m init \
      && mkdir -p .claude-audit && printf 'EXCLUDE: ^vendor/\n' > .claude-audit/SCOPE.md \
      && bash ~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh . 50 2>&1 | grep -E "Total files:|Project excludes"
    ```
  - **Output**: stdout fragment from the inventory script.
  - **Verification**:
    1. "Project excludes (from ...): ^vendor/" appears in the ACTIVE SCOPE RULES block
    2. "Total files: 2" appears (a.go + b.go only; vendor/lib.go excluded by the project rule)
    3. Cleanup: `rm -rf /tmp/scope-test-fixture` after the test passes
  - **Completion gate**: Project-override mechanism verified working.

- [x] **6.4 — Document the changes in the Task Log Execution Log**
  - **Context**: Future readers (and the rollback path) need to know exactly what changed and when. Capture file paths, edit summaries, and the smoke-test result.
  - **Action**: Append to the Task Log § Execution Log below: which files were edited, the resulting line counts, the smoke-test count, any deviations from the plan, the rollback strategy chosen in Phase 1.2.
  - **Output**: Task Log § Execution Log populated.
  - **Verification**: Task Log contains at minimum: rollback strategy, 4 (or 6 with pass2/pass3) per-file before/after line counts, the "Total files: 389" smoke-test result.
  - **Completion gate**: Log entry written.

- [x] **6.5 — Update task status to Done**
  - **Context**: All edits and verification complete. Move task into the closed state.
  - **Action**: Update frontmatter: `status: "🟢 Done"`, set `updated_date: "2026-05-29"` (or current date if later), add a `completion_date` field with today's UTC date. Then move the task folder from `.dev/tasks/to-do/` to `.dev/tasks/done/` if that's the convention in IronClaude (verify via `ls /config/workspace/IronClaude/.dev/tasks/done/` to see if other completed tasks live there).
  - **Output**: Frontmatter updated; folder moved (if convention matches).
  - **Verification**: `head -10` of the task file shows `status: "🟢 Done"`; `ls /config/workspace/IronClaude/.dev/tasks/done/TASK-RF-20260529-162751-cleanup-audit-scope-defaults/` returns the moved folder.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log

**2026-05-29 — Phase 1.0 — PIVOT decision recorded**

Upstream source-of-truth confirmed at `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/` (and `/config/workspace/IronClaude/src/superclaude/commands/cleanup-audit.md`). Per CLAUDE.md global rule, edits MUST land in `src/` and propagate to `.claude/` via `make sync-dev`.

Path rewrites for Phases 2–5:
- `/config/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` → `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`
- `/config/.claude/skills/sc-cleanup-audit-protocol/SKILL.md` → `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
- `/config/.claude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md` → `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md`
- `/config/.claude/skills/sc-cleanup-audit-protocol/rules/pass2-structural-audit.md` (Phase 4.2) → `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass2-structural-audit.md`
- `/config/.claude/skills/sc-cleanup-audit-protocol/rules/pass3-cross-cutting.md` (Phase 4.2) → `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass3-cross-cutting.md`
- `/config/.claude/commands/sc/cleanup-audit.md` → `/config/workspace/IronClaude/src/superclaude/commands/cleanup-audit.md`

Phase 6 added pre-smoke-test step: `make -C /config/workspace/IronClaude sync-dev && make -C /config/workspace/IronClaude verify-sync`. Smoke test will be re-pointed to use the synced project-local `.claude/` copy (`/config/workspace/IronClaude/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`) rather than the global `/config/.claude/` install, since `make sync-dev` only writes to project-local `.claude/`.

**2026-05-29 — Phase 1.1 — line counts verified** — all 4 files exact match (134/155/81/118).

**2026-05-29 — Phase 1.2 — rollback strategy = `git-checkout`** — `/config/workspace/IronClaude/` is a git work tree. Phase 1.3 (file-snapshot) skipped (marked complete as a no-op per task-protocol).

### Phase Findings — Phase 1

- Phase 1 complete with one pivot decision (1.0): edits redirected from `/config/.claude/` to `/config/workspace/IronClaude/src/superclaude/` upstream. No anomalies in baselines; rollback via `git checkout HEAD -- <path>` against IronClaude.

### Phase Findings — Phase 2

- Phase 2 (load-bearing script edits) complete; `repo-inventory.sh` grew from 134 → 172 lines.
- Defensive `|| true` added to `apply_scope` grep calls (script-wide `set -e` was killing empty-input pipelines such as `git ls-files -- /tmp` from a non-target cwd). Noted as Phase 2 micro-deviation from the verbatim spec block in Phase 2.1.
- `DEFAULT_EXCLUDES` regex value (canonical, must match the Phase 5.1 in-scope-after-default-excludes line byte-for-byte): `^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/`
- TUIBBS smoke (informal, ahead of Phase 6): `Total files: 389` — matches `progress.json:current_scope.in_scope_paths`.
- **Phase-gate QA: PASS** (rf-qa, 19/19 checks; report at `reviews/qa-phase-2-report.md`). Pre-existing latent bug in `domain_count` loop noted as out-of-scope follow-up.

### Phase Findings — Phase 3

- Phase 3 (SKILL.md docs) complete; 155 → 170 lines.
- 3.1 paragraph nested under Discover bullet via CommonMark 3-space continuation; 3.2 "Scope Floor" bullet added between Conservative Escalation and `## Examples`.
- **Phase-gate QA: PASS** (rf-qa, 16/16 checks; report at `reviews/qa-phase-3-report.md`).

### Phase Findings — Phase 4

- Phase 4 (subagent contract files) complete; pass1 81→97L, pass2 ?→107L, pass3 ?→91L.
- Identical regex hints across all 3 files; action verbs adapted per pass (classify / analyse / compare).
- **Phase-gate QA: PASS** (rf-qa, 19/19 checks; report at `reviews/qa-phase-4-report.md`).

### Phase Findings — Phase 5

- Phase 5 (command file cosmetic edit) complete; 118 → 119 lines.
- TUIBBS in-scope count confirmed via direct grep: 1100 tracked / 389 in-scope.
- Regex byte-for-byte lockstep with Phase 2.1 `DEFAULT_EXCLUDES` (`^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/`).
- **Phase-gate QA: PASS** (rf-qa, 10/10 checks; report at `reviews/qa-phase-5-report.md` — rewritten from agent's inline reply since the agent did not persist to disk on first run).

### Phase Findings — Phase 6

- **`make sync-dev`** — clean (26 skills, 38 agents, 41 commands synced). All 6 Phase-2-to-5 source files diff-clean against synced copies under `/config/workspace/IronClaude/.claude/`. (`make verify-sync` flagged a pre-existing drift in `sc-persona-research-protocol` that is unrelated to this task — out of scope.)
- **6.1 smoke test** — `Total files: 389 == EXPECTED 389` (read dynamically from `/config/workspace/TUIBBS/.claude-audit/progress.json:current_scope.in_scope_paths`). ACTIVE SCOPE RULES block shows `Default excludes: ^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/` and `Project excludes: (none — no SCOPE.md or no EXCLUDE: lines)`.
- **6.2 leak check** — 0 hidden/BMAD paths in any batch assignment.
- **6.3 override fixture** — temporary repo with `.claude-audit/SCOPE.md: EXCLUDE: ^vendor/` produced `Total files: 2` (a.go + b.go; vendor/lib.go excluded) and emitted `Project excludes (from ./.claude-audit/SCOPE.md): ^vendor/` in the ACTIVE SCOPE RULES block — per-project override mechanism verified working.

### Per-file before/after line counts

| File | Before | After | Δ |
|---|---|---|---|
| `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` | 134 | 172 | +38 |
| `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` | 155 | 170 | +15 |
| `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md` | 81 | 97 | +16 |
| `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass2-structural-audit.md` | (pre-existing) | 107 | +17 |
| `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass3-cross-cutting.md` | (pre-existing) | 91 | +17 |
| `src/superclaude/commands/cleanup-audit.md` | 118 | 119 | +1 |

### Deviations from plan

1. **Phase 1.0 pivot** — upstream `src/superclaude/` source-of-truth found; all Phase 2–5 paths rewritten to `/config/workspace/IronClaude/src/superclaude/...`; Phase 6 gained `make sync-dev` step; smoke test re-pointed at synced project-local `.claude/`.
2. **Phase 2.1 micro-deviation** — `apply_scope()` body wraps each `grep -E -v` in `|| true` to keep the script robust against empty input under `set -e`. Spec block did not include the `|| true` guard; without it the script aborts when `git ls-files -- /tmp` (or any cwd/target mismatch) returns an empty list. Documented inline as a code comment.
3. **Phase 4.2 wording differentiation** — pass1 uses verb "classify", pass2 uses "analyse", pass3 uses "compare against or classify" — matches each pass's role per QA's adversarial differentiation check.
4. **Phase 5 QA report** — rf-qa agent returned report inline without persisting to disk on first run; report transcribed and written to `reviews/qa-phase-5-report.md` to maintain the persistence-evidence invariant.

### Rollback (if needed)

Strategy: `git checkout HEAD -- <path>` against `/config/workspace/IronClaude/`. Affected paths:
- `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`
- `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
- `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md`
- `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass2-structural-audit.md`
- `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass3-cross-cutting.md`
- `src/superclaude/commands/cleanup-audit.md`
After rollback, re-run `make sync-dev` to propagate to `.claude/`.

### Post-completion validation summary

- **rf-qa structural (`qa-final-validation-report.md`)**: PASS (11/11 cross-phase checks — regex lockstep, docs↔impl coverage, subagent-hint synchronization, sync state, smoke reproduction, no regression, line counts, frontmatter all consistent).
- **rf-qa-qualitative (`qa-qualitative-review.md`)**: PASS-after-promotion. The agent applied 2 in-place IMPORTANT fixes to `SKILL.md` (Repository Context dual-label parity with the command file; replaced fabricated `inventory.txt` filename with "the inventory output") and surfaced 2 OPEN findings — both promoted to Follow-Up Items #4 (malformed EXCLUDE: regex handling) and #5 (pre-existing `domain_count` bug). Neither is a regression of this task's scope. After promotion, the qualitative gate is satisfied.

### Phase Findings

(populated during execution — capture any per-phase surprises, deviations, or follow-ups)

### Follow-Up Items

Potential follow-ups discovered during research (NOT in scope of this task):

1. **PR/MR + version-bump for the skill** — these edits land in user-config (`~/.claude/`) which is typically not under git. If the user wants to ship this change upstream (or to a team-wide config), a separate PR with a CHANGELOG entry would be appropriate.
2. **Audit-validator regression check** — the audit-validator subagent's spot-check protocol may need a small update so it knows hidden paths are legitimate referrers (already implied by the pass1-surface-scan.md scope rule; mirror to `~/.claude/agents/audit-validator.md` if defense-in-depth at the agent-prompt level is desired).
3. **`.claude-audit/inventory.txt` regeneration** — after this task lands, existing `.claude-audit/inventory.txt` files in other projects will need regenerating to pick up the new defaults. Consider adding a `progress.json` field that records the `scripts/repo-inventory.sh` sha256 used to produce the inventory, so stale-inventory detection is automatic.
4. **Malformed `EXCLUDE:` regex validation** (surfaced in post-completion qualitative QA, Issue 3) — when `.claude-audit/SCOPE.md` contains an invalid regex (e.g. `EXCLUDE: [bad-regex`), `grep -E` errors to stderr and the `apply_scope` `|| true` swallows the failure; downstream the script reports `Total files: 0` silently. Operator-friendly fix: pre-validate each `EXTRA_EXCLUDES` pattern (e.g. `echo "" | grep -E "$pattern" >/dev/null 2>&1 || echo "WARN: skipping invalid EXCLUDE pattern '$pattern'"`) and skip invalid patterns rather than mass-zero the inventory. Not a regression of this task (SCOPE.md was not consumed before), so deferred.
5. **Pre-existing `domain_count` latent bug** (surfaced in Phase 2 QA, Issue 4) — `repo-inventory.sh` L122-123 has a pre-existing multi-line construct under `set -e` that prints `repo-inventory.sh: line 123: [: 0` on small/sparse repos. Pre-dates this task; out of scope for the scope-defaults work but worth fixing on the next pass.

### Open Questions

None — the task is fully specified.
