<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (option-a-recommended) -->
<!-- Merge date: 2026-11-07 -->

<!-- Source: Base (original) -->
# D-P2-24, option A (recommended): two call sites that no spec row names are skipped, not nested

1. release-split Part 4 (fidelity verification) says "Skill `sc:analyze` or inline verification" (`src/superclaude/skills/sc-release-split-protocol/SKILL.md` near line 331). Under `--unattended` it uses inline verification and makes no `sc:analyze` call; no nested directory, no nested-list entry.
2. reflect's Wave 1B optional `tech-research` call (`src/superclaude/skills/sc-reflect-protocol/SKILL.md` near line 632, `--depth deep` only) is skipped and recorded, because `tech-research` has no Unattended mode (as D-P2-1 decides for brainstorm).

<!-- Source: Base (original) -->
Claimed strengths: both are optional or have an inline fallback already in the skill; no new nested directory or test pin; the spec's nested list for release-split and reflect stays as written.

<!-- Source: Base (original, modified) - Claimed weakness sentence replaced per Change 1: the debate rejected the "richer verification" premise (A-001 / X-002, analyze.md:3 describes code analysis) -->
Claimed weakness: release-split Part 4 loses an optional `sc:analyze` pass that a coordinator might sometimes want; reflect `--depth deep` loses its research enrichment. The earlier claim that `sc:analyze` gives richer verification is dropped: `analyze.md` (line 3) describes code analysis, and Part 4's checks come from `refs/verification-protocol.md` and Behavioral Instructions 1-3, which run the same way whichever way Part 4 is delegated.

<!-- Source: Base (original) -->
## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.

<!-- Source: Variant 2 / debate, Change #2 (debate item X-001; spec section 2.1; Variant B item 1) -->
## Why this respects the spec

Spec section 2.1 reads "a command that invokes another ... passes `--unattended` when the invoked command accepts it". The rule fires on an invocation. The skill's own alternative for Part 4 (inline verification) invokes nothing, so choosing it breaks no part of the rule. The skip-and-record clause of section 2.1 applies to callees that do not accept the flag (`tech-research` at the reflect site), not to Part 4. The debate decided this point for option A at 76% confidence, and the Variant B advocate conceded the literal "duty to call" reading.

<!-- Source: Variant 2 / debate, Change #3 (Variant B item 1 and claimed weakness; diff-analysis C-003; debate cost list) -->
## Option B rejected because

Option B (nest `sc:analyze --unattended --report-dir <report-dir>/nested/analyze-<n>/` for Part 4) needs edits in at least five places for a call that no section 3 row of the spec names (the release-split row at spec line 149 lists only the tasklist-input and `--r1-scope custom` gates):

- the spec's nested list for release-split;
- `EXPECTED_NESTING` in `tests/skills/test_worker_contract.py` (defined at line 1388; release-split entry `["brainstorm", "adversarial"]` at line 1391);
- the second hard-coded copy of that list in the same test file (`assert EXPECTED_NESTING == {` at line 1461; entry at line 1466);
- `UNATTENDED_EXPECT["release-split"]["nested"]` in the same test file (block at line 472, nested value near line 482);
- `release-split.md:119` and `SKILL.md:330-331` (the lines that now say Part 4 uses inline verification).

B would also add one more artifact (`analyze-report.md`, analyze.md:98) and a failure path. The benefit B claims (a stronger or independent check) is not shown in any file.

<!-- Source: Variant 2 / debate, Change #4 (Variant B item 1 fallback, diff-analysis C-004; B advocate strength 1, independence) -->
## Decision and residual risk

**Decision**: option A for both sites. release-split Part 4 uses inline verification and makes no `sc:analyze` call; reflect Wave 1B skips the optional `tech-research` call and records the skip (same outcome as option B at the reflect site).

**Edits needed in command or skill files**: none. The working tree already says Part 4 uses inline verification at `SKILL.md:331` and `release-split.md:119`, and reflect skips `tech-research` at `SKILL.md:640`.

Part 4 therefore has one path (inline verification). There is no failure branch to specify, so option B's inline fallback after a failed nested call is not needed.

**Residual risk**: option B's one surviving argument is independence. With inline-only Part 4, one context performs both Part 3 and Part 4. This is unproven (`sc:analyze` is a code-analysis command and does not run the 8-check list of `refs/verification-protocol.md`) but not refuted. It is recorded so the owner can revisit it later; it is a risk, not a defect.
