# Diff Analysis: fix-proposal Comparison

## Metadata
- Generated: 2026-11-08T02:10:57Z
- Variants compared: 3 (variant-1-original.md = fix-1 installed-core/`--all`; variant-2-original.md = fix-2 core+project/single-handle; variant-3-original.md = fix-3 project-only/`--all`)
- Total differences found: 18
- Categories: structural (1), content (7), contradictions (4), unique (7), shared assumptions (3 promoted)
- Layout note: `--output` was given as the troubleshoot run's `adversarial/` directory; artifacts are written directly into it (the caller, sc:troubleshoot Wave 4, expects the six artifacts at `<output-dir>/adversarial/`).
- Focus: correctness, risk, test-coverage

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|------|-----------|-----------|-----------|----------|-------|
| S-001 | Section layout | Problem / Proposed change / Evidence / Risks / Test plan / Documented constraints (6 H2) | same 6 H2 | same 6 H2 | Low | L1 (cosmetic: identical template) |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity | Level |
|---|-------|--------------------|--------------------|--------------------|----------|-------|
| C-001 | Fix location | Installed core only: `src/superclaude/core/CLAUDE.md` + `ccsession-tag/README.md`; explicitly no project CLAUDE.md change | Both installed copies + one project CLAUDE.md bullet after :310 | Project CLAUDE.md only (bullet after :310 + example block :318-324); installed core rejected | High | L2 |
| C-002 | Closing command | `orca terminal close --worktree path:<path> --all` | `orca terminal list --worktree path:<path> --json`, then if exactly one terminal `orca terminal close --terminal <handle>`; "Never use `--all`" | `orca terminal close --worktree path:<path> --all` | High | L3 (guard/boundary) |
| C-003 | Precondition / guard on the close | "if you will work in the new checkout from your current session", "right after the create" | "without `--agent` and without a setup script", "right after that create, before any `agent launch`", "exactly one terminal", "never close terminals in a worktree you did not just create" | "If you will work in the checkout from your own session", "right after the create, before anything is started there" | Medium | L3 (guard) |
| C-004 | Hand-off case (new session should work there) | Use `worktree create --agent` instead of a bare create | Not addressed separately; the close step applies before any `agent launch` (so it also covers bare create + `agent launch`) | Put `--agent claude` on the create; `/sc:issue` and supervised workers keep their own launch steps | Medium | L2 |
| C-005 | Delivery to running agents | `make sync-dev` then `superclaude update` (plain `install` skips existing files, install_core.py:70-72) | `make sync-dev`, `make verify-sync`; no reinstall step | None needed: project CLAUDE.md is read from the checkout (only on branches containing the fix) | High | L2 |
| C-006 | Test | Add 13th pinned phrase "`orca terminal close`" to tests/core/test_orca_session_launch_guidance.py | Add phrases "`orca terminal close --terminal`" and "before any `agent launch`" + `assert "--all" not in section`; run three test files | New test asserting the project CLAUDE.md worktree section contains `orca terminal close --worktree` | Medium | L2 |
| C-007 | /sc:issue orca_worktree.py | Not addressed | Explicitly deferred to a separate issue (unobserved, N11; pinned `test_fo18_exact_commands_and_no_forbidden_flag`) | Exempted in wording ("keep their own launch steps") | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Is `--all` acceptable? | Yes: "The close is only for own use, where no other tab exists yet, so `--all` cannot kill an agent" (fix-1 via card) | No: "Never use `--all`"; `--all` can kill a running setup script, a reused worktree's sessions, or the agent's own shell | Yes, guarded by "before anything is started there" | High |
| X-002 | Should the project CLAUDE.md change? | "No project CLAUDE.md change" | Yes, one bullet | Yes, it is the only change | Medium |
| X-003 | Intra-variant (V2): wording vs test | — | Sentence contains "Never use `--all`" while the test asserts `"--all" not in section` for both copies: the new assertion fails on the variant's own text | — | High |
| X-004 | Does another tab exist right after a bare create? | No ("no other tab exists yet") | Yes when the repo has a setup hook or default tabs: provisioning opens those tabs in the background (IronOrca runtime-local-worktree-terminal-startup.ts:187-201, `void provisioning`), possibly after the reply | Implicitly no ("before anything is started there") | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Reinstall step: `superclaude update`, because `install` skips existing files and the installed ~/.claude/CLAUDE.md lacks the section (N12) | High |
| U-002 | 1 | Hand-off → `worktree create --agent` instead of bare create, aligned with the existing core rule (core/CLAUDE.md:49) | Medium |
| U-003 | 2 | Guard: "never close terminals in a worktree you did not just create" | High |
| U-004 | 2 | Setup-script exclusion and the setup/default-tab race analysis | Medium |
| U-005 | 2 | Explicit deferral of orca_worktree.py naming the pinned test it would break | Medium |
| U-006 | 3 | Edit the rule that forces the bare create (CLAUDE.md:307-324) so IronClaude sessions get the step from the checkout without a reinstall | High |
| U-007 | 3 | Wording that exempts `/sc:issue` and supervised workers | Medium |

## Shared Assumptions

Agreement points: all three accept the same diagnosis (P1: bare create seeds a plain first terminal; no instruction covers it), all choose an instruction-level fix, and none changes Orca.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All close the seeded tab | Closing the only terminal of a just-created worktree leaves the worktree intact and Orca does not re-seed a new plain tab (e.g. on next activation) | UNSTATED | Yes |
| A-002 | All rely on wording | Agents will follow a new instruction sentence; the observed bare creates happened when no rule covered the tab (rule added 2026-11-06 per N13; hand-offs 11-01..11-04) | UNSTATED | Yes |
| A-003 | V1/V3 `--all` safety; V2's "agent's own shell" risk | The creating Claude session's own Orca terminal belongs to its original worktree, so `cd`-ing into the new checkout in the Bash tool does not put that terminal under `--worktree path:<new>` | UNSTATED | Yes |
| A-004 | All | The seeded tab exists by the time the create command returns (no setup/default tabs) | STATED (N13: create awaits startRuntimeLocalWorktreeTerminals; QE/RCA risk notes) | No |
| A-005 | All | Installed Orca 1.4.245 behaves like the IronOrca checkout | STATED (all list it as unproven) | No |

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | Close leaves worktree intact, no re-seed | High: if false, the fix removes the worktree's UI presence or the tab reappears | [SHARED-ASSUMPTION] open; V-CLOSE checks worktree still listed |
| A-002 | Agents follow the sentence | High: the whole fix is text | [SHARED-ASSUMPTION] open |
| A-003 | Agent's own terminal is not owned by the new worktree | High for `--all` safety | [SHARED-ASSUMPTION] open (L3: boundary) |

## Summary
- Total structural differences: 1
- Total content differences: 7
- Total contradictions: 4
- Total unique contributions: 7
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-005, X-001, X-003, X-004, A-001, A-002, A-003
- Taxonomy: L1 = S-001; L2 = C-001, C-004, C-005, C-006, C-007, X-002; L3 = C-002, C-003, X-001, X-003, X-004, A-001, A-002 (fallback L2→ kept L3 because it is a guard on behaviour), A-003
- Debate denominator (S + C + X + A): 1 + 7 + 4 + 3 = 15
- Similarity check: not substantially identical; debate proceeds.
