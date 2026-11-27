# Qualitative Scoring — Pass 1 (input order A, B, C)

Evaluator: independent qualitative layer, Step 3. Inputs read in full: `blind/variant-A.md`, `blind/variant-B.md`, `blind/variant-C.md`, `seed-brief.md`, `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.2). Debate transcripts, advocate statements, diff analysis and the other pass were not read.

Protocol: Claim-Evidence-Verdict per criterion; binary; no evidence means NOT MET. The Claim column states whether the criterion is met in that variant. Repository claims used for Correctness were spot-checked read-only in this worktree (2026-11-26).

Repository checks used as evidence (all read-only):

- `src/superclaude/commands/git.md`: usage at line 22, `merge feature-branch --interactive` example at lines 72-77, front matter `category: utility`, `complexity: basic`.
- `tests/recommend/fixtures/routing_refresh_cases.json` S23 (lines 312-333): `mode_flags: []`, the only repeat has `mode_flags: ["--smart-commit"]`; `activation: {"sc:git": "self-contained"}`; three pinned guide phrases.
- `tests/recommend/test_routing_refresh.py:306-317`: flag check covers only the flags the fixture lists.
- `src/superclaude/core/WORKER-CONTRACT.md`: :23 never-as-worker list includes `/sc:git`; :42 K3 parking; :43 "A command's own commit step stays off under `--unattended`"; :57 "executor-invented approval"; :346 `/sc:graph init` "user's own message starts with" precedent.
- `src/superclaude/skills/sc-implement-protocol/SKILL.md`: :51 closed STOP sentence; :57 Wave 0 known options; :71 step 5 resolve ledger path; :72 step 6 "Open or create ledger (header first, before any product edit)"; :110 parallel rules (a)-(c), batch size ≤3.
- `src/superclaude/skills/sc-implement-protocol/refs/retry.md`: :41 HEAD equals `q0-head`; :212 submodule paths excluded from revert.
- `src/superclaude/commands/implement.md:100` "Auto-commit, open PRs, or release"; no `Unattended mode` section.
- `src/superclaude/core/HOW-WE-WORK.md:293` `/sc:git` row (lists "branch or merge operations"; "Do not append push, merge or PR creation").
- `src/superclaude/hooks/scripts/launch-level-guard.sh`: :46-49 LL-COMMIT; :58-60 LL-PROTECTED (master, main, integration); :135 `git commit -F <file>` advice; :713-724 git subcommand table (no `submodule`, falls to UNKNOWN); :786 `--no-verify` TAMPER; :806-808 COMMIT allowed only at FS; :816 UNKNOWN denied at every level.
- `src/superclaude/commands/worktrees.md`: :17 `archive` writes without `--apply`; :55 exit codes 0/64/69, "No skill is activated".
- `scripts/worktree_cleanup.py`: :2636-2647 `_remove_branch` uses `git branch -d`; :385-394 branch allow-list.
- Developer guide `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:276-279` category list includes `version-control`; complexity list is `simple, moderate, advanced, high`.
- `docs/developer-guide/git-standards-protocols.md`: id `GFXAI-GIT-STANDARDS-PROTOCOLS`, status "To Do", `[GFXA-XXX]` subject format at ~:431.
- `src/superclaude/cli/main.py:585-592` sweep and review groups registered; no `vcs` group exists.
- `src/superclaude/cli/install_skills.py:47-59` strips only the `sc-` prefix.
- `git symbolic-ref --short refs/remotes/origin/HEAD` → `origin/master`; `git --version` → 2.47.3; `git submodule status` → `-98669c1... .vendor/anthropic-skills` (uninitialized).
- `git ls-files commands/` → 21 files including `commands/sc-git.md` (79 lines, `# /sc:sc:sc:git`, usage `/sc:sc:git`); `tests/commands/test_help_text_fixes.py` names `sc-business-panel.md`, `sc-cleanup.md`, `sc-pm.md` at :17/:41/:92.
- `pyproject.toml` wheel/sdist include only `src/` and `plugins/` (plus tests/README/LICENSE in sdist).
- `.claude/commands/sc/git.md` does not exist in this worktree.
- `Makefile` `verify-sync` (line 166) compares src with the dev copy; no plugin reference in that target.

---

## Variant A

### Completeness (A)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| completeness.1 | Met | §1.3 items 1-4 map to the four seed success criteria; FR-014 decides `commands/sc-git.md`; FR-015/FR-016 source → plugin → dev sync; FR-050-FR-066 `--commit-tasks`, Conventional subject (FR-066), named paths plus `git add -- .dev/tasks` (FR-061 step 3), no commit inside a batch (FR-058), hook refusal reported (FR-064); FR-040-FR-042 submodule status/update/commit-pointer under the same authorization table (§3); FR-080/FR-081 reuse and no remote deletion; T-18 gate. Seed "never merges" honored: FR-004 STOPs on `merge`, D7 removes it | MET |
| completeness.2 | Met | FR-054 STOP tokens `detached-head`, `protected-branch`, `operation-in-progress`, `index-locked`, `dirty`; FR-064 hook failure and formatter rewrite; FR-065 resume after refusal; FR-058 halted batch member; FR-041 submodule refusals | MET |
| completeness.3 | Met | §1.5 baseline facts table (git 2.47.3, retry `q0-head`, closed STOP table, pre-commit hooks); FR-013 `MIN_GIT = (2, 23)`; FR-054 Wave 0 preflight; FR-015 "Edit `<pkg>` first. Then copy"; NFR-009 `vcs_contract` | MET |
| completeness.4 | Met | §13 AC-01..AC-15, each with a Check column (e.g. AC-07 "HEAD does not move ... T-04") | MET |
| completeness.5 | Met | §1.4 "Explicitly out of scope (decided)": relay, push/fetch/pull/merge/rebase/PR, remote branch deletion, second cleanup, level table, fixing git-standards doc, nested submodules/`foreach`/`update --remote`, new PM workflows | MET |

### Correctness (A)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| correctness.1 | Met | 20+ cited facts spot-checked and all held: `git.md:22`, `:72-77`; `implement.md:100`; `WORKER-CONTRACT.md:23`, `:42`, `:43`, `:57`, `:346`; `SKILL.md:51`, `:110`; S23 expects `--smart-commit` and pins three phrases; `launch-level-guard.sh:46-49`, `:58-60`, `:135`, `:786`; `worktrees.md:55` codes 0/64/69; developer-guide values `version-control`/`moderate` (FR-001); `origin/HEAD` → `origin/master`; git 2.47.3; uninitialized `.vendor/` submodule; `commands/sc-git.md` 79 lines with doubled prefix; `main.py:585-592`, no `vcs` group. No factual error found | MET |
| correctness.2 | Met | Writes are visible Bash argv planned by a read-only helper so host hooks see them (§2 intro, NFR-002); commit only when "no task is open" (FR-056, FR-059), so retry check 3 holds; no push/merge (FR-004); consistent with every seed constraint | MET |
| correctness.3 | Met | Terms defined once and reused: "open"/"pending" (FR-056), four `COMMIT:` record forms (FR-068), refusal tokens `blocked-by-host`/`commit-failed` (FR-064), operation classes (§3 table) | MET |
| correctness.4 | Not met | FR-052: "No primitive other than `implement.md`, `sc-implement-protocol` and `HOW-WE-WORK.md` may contain the string `--commit-tasks` ... A static test enforces this" (T-15), but FR-091 rewrites `WORKER-CONTRACT.md:42` (an installed core primitive) to say per-task commits "are delivered as `/sc:implement --commit-tasks`" and "`--commit-tasks` is refused under `--unattended`". A's own required text fails A's own T-15 | NOT MET |
| correctness.5 | Met | §1.5 Evidence column for every baseline fact; D1-D8 each give a "Why" (D3: "a flag can be checked mechanically. A plan field is written by automation ... executor-invented approval") | MET |

### Structure (A)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| structure.1 | Not met | The shared prerequisite rules sit in §6 ("Commit rules shared by `/sc:git commit` and the implement step": FR-030 forbidden flags, FR-031 path rules, FR-032 preflight) after their dependents: FR-004 (§2.1) STOPs on "any token in the forbidden-flag list (FR-030)", the §3 table cites FR-031/FR-032/FR-034, FR-043 (§5) relies on "The detached-HEAD refusal in FR-032" | NOT MET |
| structure.2 | Met | H3 subsections only under §1 (1.1-1.5), §2 (2.1-2.5) and §4 (4.1-4.7); every group has ≥2 siblings; no orphan | MET |
| structure.3 | Met | Separate sections: structure (§2), authorization (§3), implement step (§4), submodules (§5), shared rules (§6), cleanup (§7), worker contract (§8), tests (§9), NFR (§10), risks (§11), decisions (§12), AC (§13) | MET |
| structure.4 | Met | Dense cross-references: FR ids, § refs (FR-072 "holds §4.3-§4.6"), AC "Check" column naming T ids, T table naming FRs | MET |
| structure.5 | Met | Requirements-spec conventions: numbered FR/NFR ids, test-obligation table, risk table, decisions, AC table | MET |

### Clarity (A)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| clarity.1 | Met | Requirements use must/never/only/refuses (FR-063 "never contain ..."); search for should/might/as appropriate/as needed/when applicable found no hit; "may" appears only in prohibitions (FR-016, FR-052) or risk descriptions | MET |
| clarity.2 | Met | Exact argv (FR-061 "`git commit --only -F <message_path> -- <commit_paths>`"), JSON fields (FR-010), exit codes (FR-012), ledger record forms (FR-068), constants (FR-013) | MET |
| clarity.3 | Met | §2 opens "The design has three layers..."; §3 opens "The person's own typed line is the only thing that authorizes a write"; other sections are one-topic | MET |
| clarity.4 | Not met | Placeholders (§1.1) and open/pending/Q8a/R0/L0 (FR-056/FR-057) are defined, but FR-057 uses "Q7", "Q8" and "Q0", FR-092 uses "(WC-4)", and §1.5 uses "TAMPER", none defined | NOT MET |
| clarity.5 | Met | §12 decisions D1-D8; §13 AC with checks; FR-082 records the accepted gap and when it may be revisited | MET |

### Risk Coverage (A)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| risk_coverage.1 | Not met | §11 table columns are "# / Risk / Mitigation / Residual"; 14 risks, none with a probability or impact rating | NOT MET |
| risk_coverage.2 | Met | All 14 rows have a Mitigation (e.g. #2 formatter hooks → "Classified `commit-failed`; STOP; resume plans again") | MET |
| risk_coverage.3 | Met | FR-064 classification and refusal log; FR-065 resume re-plans; FR-022 prints `git reset --soft <parent>` as undo; FR-058 halted batch resumes | MET |
| risk_coverage.4 | Met | Risk #2 pre-commit formatters, #6 wrong `origin/HEAD`, #7 launch-level guard, #9 installed skill vs CLI drift, #13 CI check; T-06/T-07 pinned hook version and CI `file://` protocol marked UNVERIFIED | MET |
| risk_coverage.5 | Met | Parity test (NFR-003, T-13), `vcs_contract` check (NFR-009), Wave 0 preflight (FR-054), no-deletion scan (T-17), absence test (FR-014) | MET |

### Invariant & Edge Case Coverage (A)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| invariant_edge_case.1 | Met | FR-062 "If nothing remains, the result is `nothing`"; FR-056 "the pending set is not empty"; FR-010 dirty "capped at 200, with `truncated`"; batch ≤3 (§1.5); NFR-007 64 KiB / 200 entries / 40 lines | MET |
| invariant_edge_case.2 | Met | FR-059 HEAD equals `q0-head` for open/halted tasks so retry check 3 and Ruling resume condition (6) hold; FR-069 ledger grammar ↔ `archive_workspace.py` parser; FR-062 managed package vs other `.dev/tasks` packages | MET |
| invariant_edge_case.3 | Met | Risk #1 "In ordinary sessions nothing enforces this mechanically"; #14 `allowed-tools` "is not treated as a security boundary"; T-05 "checks the FR-033 and FR-062 assumption instead of trusting it"; FR-011 runner raises before executing non-allow-listed argv | MET |
| invariant_edge_case.4 | Met | FR-056(b) only tasks whose `complete` line "comes after the first `COMMIT: on` line" (T-01 "tasks completed before `COMMIT: on` are excluded"); FR-061 one message rewrite then refusal; FR-066 subject "at most 72 characters"; FR-058 pending set recomputed after a halted member | MET |
| invariant_edge_case.5 | Met | FR-058 batch × commit; FR-054 `--commit-tasks` × `--unattended`; FR-093 launch level × commit; FR-067 Ruling × commit; FR-040 `submodule.recurse` × push warning | MET |

---

## Variant B

### Completeness (B)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| completeness.1 | Not met | Seed constraint: "`/sc:git` never pushes, merges or opens PRs". B FR-006 lists "`merge <branch> [--interactive]` / merge" and FR-013 defines a Merge class that runs `git merge <branch>` after a chat yes; §1.3 narrows the exclusion to "merging into a shared or protected branch". The other success criteria are covered (FR-007/FR-008, FR-022-FR-030, FR-033-FR-036, FR-038) | NOT MET |
| completeness.2 | Met | FR-020 closed refusal list; FR-021 `hook-failed`, `hook-rewrite`, `hook-rewrite-committed`, `guard`, `recovered`; FR-025 halted batch; FR-036 detached submodule | MET |
| completeness.3 | Met | FR-023 helper resolution order with `helper-missing`; NFR-009 git ≥2.38 for merge preview; FR-019 standard library via `uv run --no-project`; T-09 `protocol.file.allow=always` only in the fixture | MET |
| completeness.4 | Met | §13 AC-01..AC-15, "Each criterion is a command or an observation with a pass condition" (e.g. AC-04 `git ls-files commands/ | wc -l` prints `20`) | MET |
| completeness.5 | Met | §1.3 out-of-scope table with reasons (relay, push/PR, remote deletion, second cleanup, guard/probe changes, the other 20 `commands/` files, PM extension, a new `--no-verify` hook) | MET |

### Correctness (B)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| correctness.1 | Not met | FR-002: "`--smart-commit` and `--interactive` stay declared ... The fixture flag check requires this (`tests/recommend/test_routing_refresh.py:307-317`; S23 repeats at `routing_refresh_cases.json:327`)". Verified: S23 `mode_flags` is `[]` and its only repeat lists `["--smart-commit"]`; nothing requires `--interactive`. Other citations checked held (`launch-level-guard.sh:720/724/816`, `:806-808`; `pyproject.toml` includes; 21 tracked `commands/` files; `test_help_text_fixes.py:17/41/92`) | NOT MET |
| correctness.2 | Not met | FR-013 Merge class runs `git merge <branch>` after a confirmation, which conflicts with the seed constraint "`/sc:git` never pushes, merges or opens PRs" (Constraints) | NOT MET |
| correctness.3 | Met | Closed vocabularies used consistently: FR-020 refusal reasons, FR-021 verify tokens, `commits.md` line forms (FR-029), read/write/merge classes (FR-011-FR-013) | MET |
| correctness.4 | Not met | FR-023 runs the Wave 0 preflight "after step 6 (ledger) and before the first Q0" yet says the run stops "Before the ledger is created", and the STOP row gives Wave 0 "Ledger? No"; implement Wave 0 step 6 is "Open or create ledger (header first ...)" (`SKILL.md:72`), so the ledger already exists. Also FR-009 keeps "Do not append push, merge or PR creation" in the routing row while FR-013 adds a merge operation | NOT MET |
| correctness.5 | Met | §2 RC-1..RC-7, "Each root cause is stated as a falsifiable claim with its evidence"; §11 Q1-Q6 give reasons and rejected options | MET |

### Structure (B)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| structure.1 | Met | Root causes (§2) precede design; shared commit mechanics FR-016 and helper §4.1 (FR-019-FR-021) precede their consumers in §5 (implement) and §6 (submodules) | MET |
| structure.2 | Not met | §4 "Authorization model" has a single subsection "### 4.1 Helper script `commit_plan.py`" with no sibling (orphaned subsection); other H2s have 0 or ≥2 subsections | NOT MET |
| structure.3 | Met | Distinct sections for root causes, structure, authorization, implement, submodules, cleanup, worker contract, tests, risks, decisions, NFR, AC | MET |
| structure.4 | Met | Numbered sections, FR cross-refs, "Root cause addressed: RC-x" lines, test table "Covers" column, risk table "Root cause" column | MET |
| structure.5 | Met | FR/NFR ids, AC list, risk table, test obligations | MET |

### Clarity (B)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| clarity.1 | Not met | FR-009: "The `/sc:git` row in `HOW-WE-WORK.md:293` may gain the words ..." leaves the change optional; FR-006 pointer "everything else should be run by the person" | NOT MET |
| clarity.2 | Met | Concrete argv (FR-016 "`git commit --only -F <message-file> -- <paths>`"), header regex (FR-028), closed token lists (FR-020/FR-021), AC grep/cmp commands | MET |
| clarity.3 | Met | Purpose lines per section ("Root cause addressed: RC-2. The model gives a mechanism that can be tested"; §2 "Each root cause is stated as a falsifiable claim") | MET |
| clarity.4 | Not met | Aliases (Path notation table) and RC are defined, but FR-010 uses "`deferred:P4`", "(WC-9)" and "/sc:implement is converted in P4" with neither P4 nor WC-9 defined; R1 uses "TAMPER class" undefined | NOT MET |
| clarity.5 | Met | §11 decisions Q1-Q6 and D-7; R1 and R10 record follow-ups; §13 AC | MET |

### Risk Coverage (B)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| risk_coverage.1 | Not met | §10 table "Id / Risk / Root cause / Mitigation / Residual"; Residual is one Low/Medium level per row, with no separate probability and impact assessment | NOT MET |
| risk_coverage.2 | Met | R1-R13 each have a Mitigation | MET |
| risk_coverage.3 | Met | FR-021 `verify` classification; FR-029 recover mode and resume-row clause; FR-030 refusal stops with the task kept `complete`; FR-018 printed undo hint | MET |
| risk_coverage.4 | Met | R9 plugin-only installs lack the helper; R11 local `pre-commit` hook not installed; FR-034 clone/fetch from `.gitmodules` URL; FR-037b/FR-044 launch-level guard denial | MET |
| risk_coverage.5 | Met | `verify` (FR-021) also lists dirty paths left behind; tests T-01..T-09; NFR-007 fail closed | MET |

### Invariant & Edge Case Coverage (B)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| invariant_edge_case.1 | Met | FR-021 `empty` and `T<id>: commit skipped reason=empty` (FR-029); batch of up to three "`(T<a>,T<b>[,T<c>])`" (FR-028); NFR-002 size caps | MET |
| invariant_edge_case.2 | Met | RC-3 coupled invariants (`q0-head`, pins, closed ledger grammar); FR-029 pin deletion deferred until the `commits.md` line; FR-044 `update-ref` on `refs/<name>/implement/...` not classed COMMIT | MET |
| invariant_edge_case.3 | Met | RC-2 "no deny rule for `git commit` or `--no-verify`"; R13 "`files=` content is agent-written" so a rename can miss the old path; FR-014 `SKIP=` and `-c core.hooksPath=` bypass vectors; NFR-007 unknown token → refusal | MET |
| invariant_edge_case.4 | Met | FR-021 `committed` requires "HEAD moved by one commit"; `recovered` checks "HEAD's parent equals `--old-head`"; NFR-005 "Each commit point adds at most one commit"; R6 commit repeated or lost | MET |
| invariant_edge_case.5 | Met | FR-025 batch × commit with shared `q0-head`; FR-044 `--commit-tasks` × launch levels; FR-037a status vs sweep `--ignore-submodules` trade-off; FR-029 resume with and without the flag | MET |

---

## Variant C

### Completeness (C)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| completeness.1 | Met | FR-001 included outcomes; FR-004/FR-005 thin command (options table, STOP rules, outputs, boundaries) + protocol skill; FR-008 removes `commands/sc-git.md`; FR-009 sync; FR-011-FR-019 authorized between-task commit, Conventional subject (FR-019), `files=` + `.dev/tasks/` (FR-015/FR-016), parallel barrier (FR-014), hook refusal (FR-020); FR-024-FR-027 status/update/pointer with separate grants (FR-012); FR-029/FR-030 reuse, no remote deletion; FR-036 sync and tests; FR-002 excludes merge | MET |
| completeness.2 | Met | FR-018 lock/unmerged/moved-HEAD refusals; FR-020 hook rewrite, interruption, timeout; FR-022 crash before/after commit reconciliation; FR-028 partial multi-repository failure | MET |
| completeness.3 | Met | Implement section names the integration points (`SKILL.md`, `refs/ledger.md`, `refs/retry.md`, `refs/managed-workspace.md`, `implement.md`); NFR-006 missing helper / contract version; NFR-008 no new runtime dependency; FR-009 sync order | MET |
| completeness.4 | Met | AC-01..AC-08, each naming the FRs that must pass (AC-03 "the authorized first commit occurs strictly after the first `complete` and before task two's Q0") | MET |
| completeness.5 | Met | FR-002 Exclusions (relay, automatic push, merge, PR, remote deletion, replacement cleanup, PM integration, destructive recovery); Decision 4 excludes remote-tip update, module add/remove, URL edits | MET |

### Correctness (C)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| correctness.1 | Met | Checked claims held: `D/commands/sc/git.md` absent in this checkout; `implement.md` has no unattended section (FR-032); `archive` writes without `--apply` (FR-029); `make verify-sync` compares src with the dev copy only (FR-009); git-standards doc uses another ticket-message style (risk table). No factual error found | MET |
| correctness.2 | Met | Commit only after `complete` and before the next Q0 (FR-013), batch barrier (FR-014), `git add -- <paths>` / `git commit --only -- <paths>` (FR-015), hooks honored (FR-020), no publication (FR-002); consistent with each seed constraint | MET |
| correctness.3 | Met | "boundary", "boundary key", "grant", "journal" and the six outcomes `committed`/`already-committed`/`no-change`/`refused`/`failed`/`uncertain` (FR-021) used consistently in FR-022, FR-023, AC-05 | MET |
| correctness.4 | Met | No contradiction found: "No new command-line flag is specified" (intro) matches FR-011 and Decision 3; FR-016 evidence staging matches FR-015; FR-023 keeps journals outside the ledger grammar as FR-021 requires; FR-007 "Missing operation defaults to read-only status" does not conflict with its STOP list | MET |
| correctness.5 | Met | Decisions 1-7 each give a reason (3: "avoids treating arbitrary plan text as consent, and makes revocation and resumed-session limits explicit"); FR-003 and FR-029 cite evidence files | MET |

### Structure (C)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| structure.1 | Met | Scope → structure (helper boundary FR-006 defined early) → authorization (FR-010-FR-012) → implement (uses FR-010/FR-011) → submodules ("uses the shared safety checks") → cleanup → worker → NFR → tests → risks → decisions → AC | MET |
| structure.2 | Met | Flat, consistent hierarchy: every section is H2 with requirement bullets; no H3, so no orphaned subsection | MET |
| structure.3 | Met | One H2 per concern (authorization, implement boundary, submodules, cleanup, worker contract, NFR, tests, risks) | MET |
| structure.4 | Met | Risk table cites "FR-010/011 require", "FR-017 blocks"; ACs cite "FR-004–009 and FR-036 pass" | MET |
| structure.5 | Met | FR/NFR ids, risk table, decisions, AC list | MET |

### Clarity (C)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| clarity.1 | Not met | FR-025 "including nested inspection when applicable"; NFR-007 "must be detected where observable"; NFR-003 "a documented finite deadline ... Exact timeout values are UNVERIFIED"; FR-003 "Other repositories use their own verified branch policy" | NOT MET |
| clarity.2 | Not met | Key interfaces left abstract: FR-019 boundary-key trailer "Its exact token is UNVERIFIED: proposed interface"; FR-021 "versioned structured request" with no format and no STOP code named ("any required STOP-table change must be explicit"); FR-033 "New test filenames are UNVERIFIED"; NFR-003 no timeout values | NOT MET |
| clarity.3 | Met | Each H2 summarizable; implement section intro: "Change only that boundary policy, not quality verdict semantics or retry restoration" | MET |
| clarity.4 | Not met | Aliases S/P/D/G are defined in "Path notation", but FR-013 uses "Q0 snapshot" and "a valid scoped user Ruling" with neither defined | NOT MET |
| clarity.5 | Met | "Decisions for the seed brief's open questions" 1-7; AC-01..AC-08 | MET |

### Risk Coverage (C)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| risk_coverage.1 | Not met | Risk table has only "Risk / Required mitigation"; 12 risks, no probability or impact | NOT MET |
| risk_coverage.2 | Met | Each of the 12 rows has a Required mitigation | MET |
| risk_coverage.3 | Met | FR-020 classify and stop before the next Q0; FR-022 journal reconciliation on resume; FR-028 per-module partial results without destructive rollback | MET |
| risk_coverage.4 | Met | FR-026 module initialization "may fetch from the configured module remote ... reject newly substituted or unapproved remote identities"; NFR-003 unavailable signing credentials or authentication prompt; FR-020 hooks; NFR-006 missing installed helper | MET |
| risk_coverage.5 | Met | NFR-001 verify committed parent, path set and contents after success; NFR-004 observability fields; FR-034 fault-injection tests | MET |

### Invariant & Edge Case Coverage (C)

| ID | Claim | Evidence | Verdict |
|---|---|---|---|
| invariant_edge_case.1 | Met | FR-024 "No submodules produces an empty list, not an error"; FR-022 "never create an empty commit"; FR-014 batch union; NFR-003 bounded output with truncation disclosed | MET |
| invariant_edge_case.2 | Met | FR-013/FR-014 HEAD unmoved during Q0-to-complete for retry; FR-023 journal kept across archive movement; FR-022 reconcile "before the existing all-complete short-circuit" | MET |
| invariant_edge_case.3 | Met | FR-018 literal paths with spaces, leading dashes and pathspec metacharacters; FR-025 symlink escapes, unregistered nested repositories, no whitespace splitting; FR-021 reject missing/unknown fields; NFR-007 trust boundary | MET |
| invariant_edge_case.4 | Met | FR-034 "Reinvoke twice and assert at most one commit for a boundary key"; FR-022 "duplicate matching commits ... produce `uncertain`"; FR-015 "both ends of renames" | MET |
| invariant_edge_case.5 | Met | FR-014 parallel barrier × commit; FR-023 journal × archive; FR-032 attended boundary vs WC-9 worker grant; FR-016 mandatory evidence × another live writer | MET |

---

## Verdict table

| Variant | Criterion | Verdict |
|---|---|---|
| A | completeness.1 | MET |
| A | completeness.2 | MET |
| A | completeness.3 | MET |
| A | completeness.4 | MET |
| A | completeness.5 | MET |
| A | correctness.1 | MET |
| A | correctness.2 | MET |
| A | correctness.3 | MET |
| A | correctness.4 | NOT MET |
| A | correctness.5 | MET |
| A | structure.1 | NOT MET |
| A | structure.2 | MET |
| A | structure.3 | MET |
| A | structure.4 | MET |
| A | structure.5 | MET |
| A | clarity.1 | MET |
| A | clarity.2 | MET |
| A | clarity.3 | MET |
| A | clarity.4 | NOT MET |
| A | clarity.5 | MET |
| A | risk_coverage.1 | NOT MET |
| A | risk_coverage.2 | MET |
| A | risk_coverage.3 | MET |
| A | risk_coverage.4 | MET |
| A | risk_coverage.5 | MET |
| A | invariant_edge_case.1 | MET |
| A | invariant_edge_case.2 | MET |
| A | invariant_edge_case.3 | MET |
| A | invariant_edge_case.4 | MET |
| A | invariant_edge_case.5 | MET |
| B | completeness.1 | NOT MET |
| B | completeness.2 | MET |
| B | completeness.3 | MET |
| B | completeness.4 | MET |
| B | completeness.5 | MET |
| B | correctness.1 | NOT MET |
| B | correctness.2 | NOT MET |
| B | correctness.3 | MET |
| B | correctness.4 | NOT MET |
| B | correctness.5 | MET |
| B | structure.1 | MET |
| B | structure.2 | NOT MET |
| B | structure.3 | MET |
| B | structure.4 | MET |
| B | structure.5 | MET |
| B | clarity.1 | NOT MET |
| B | clarity.2 | MET |
| B | clarity.3 | MET |
| B | clarity.4 | NOT MET |
| B | clarity.5 | MET |
| B | risk_coverage.1 | NOT MET |
| B | risk_coverage.2 | MET |
| B | risk_coverage.3 | MET |
| B | risk_coverage.4 | MET |
| B | risk_coverage.5 | MET |
| B | invariant_edge_case.1 | MET |
| B | invariant_edge_case.2 | MET |
| B | invariant_edge_case.3 | MET |
| B | invariant_edge_case.4 | MET |
| B | invariant_edge_case.5 | MET |
| C | completeness.1 | MET |
| C | completeness.2 | MET |
| C | completeness.3 | MET |
| C | completeness.4 | MET |
| C | completeness.5 | MET |
| C | correctness.1 | MET |
| C | correctness.2 | MET |
| C | correctness.3 | MET |
| C | correctness.4 | MET |
| C | correctness.5 | MET |
| C | structure.1 | MET |
| C | structure.2 | MET |
| C | structure.3 | MET |
| C | structure.4 | MET |
| C | structure.5 | MET |
| C | clarity.1 | NOT MET |
| C | clarity.2 | NOT MET |
| C | clarity.3 | MET |
| C | clarity.4 | NOT MET |
| C | clarity.5 | MET |
| C | risk_coverage.1 | NOT MET |
| C | risk_coverage.2 | MET |
| C | risk_coverage.3 | MET |
| C | risk_coverage.4 | MET |
| C | risk_coverage.5 | MET |
| C | invariant_edge_case.1 | MET |
| C | invariant_edge_case.2 | MET |
| C | invariant_edge_case.3 | MET |
| C | invariant_edge_case.4 | MET |
| C | invariant_edge_case.5 | MET |

## Dimension subtotals

| Dimension | Variant A | Variant B | Variant C |
|---|---|---|---|
| completeness | 5/5 | 4/5 | 5/5 |
| correctness | 4/5 | 2/5 | 5/5 |
| structure | 4/5 | 4/5 | 5/5 |
| clarity | 4/5 | 3/5 | 2/5 |
| risk_coverage | 4/5 | 4/5 | 4/5 |
| invariant_edge_case | 5/5 | 5/5 | 5/5 |

## Totals

| Variant | Criteria met | qual_score |
|---|---|---|
| A | 26/30 | 0.867 |
| B | 22/30 | 0.733 |
| C | 26/30 | 0.867 |

Edge case floor (≥1/5 on invariant_edge_case): A 5/5, B 5/5, C 5/5, all eligible.

Evaluator note: A and C tie on the qualitative layer for different reasons. A loses points on two specific internal defects (the FR-052/FR-091 contradiction and shared rules placed after their consumers). C loses points on specificity: its interfaces, tokens, timeouts and test names are left open, which also leaves it fewer concrete claims that could be wrong. B's losses come from the seed-constraint conflict (a merge operation), a wrong fixture claim about `--interactive`, and a Wave 0 ledger-ordering contradiction.
