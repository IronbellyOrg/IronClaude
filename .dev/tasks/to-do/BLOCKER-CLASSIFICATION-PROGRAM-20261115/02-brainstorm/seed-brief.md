---
topic: "@.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm-context-preamble.md"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-15T01:45:00Z
---

# Seed Brief: loosen blocker classification, record and offer follow-ups

Mode: worker (`--unattended`); the Socratic dialogue was answered from the preamble and the issue text, not from a person. Inputs read in full: `02-brainstorm-context-preamble.md`, `00-issue-description.md`, `jev-uses.md` (this folder, the Jev validation the owner asked for; its classifier section MUST feed the spec), `qa/grading-override.md` (run 2).

## Problem Statement

Review gates across the framework call too many findings "blocking". Each blocking finding halts the run, forces a fix cycle and a re-review, even when the finding changes no decision (run 2: a wrong docstring label, a miscounted "four versus six meanings", two one-character table-pipe defects each failed a gate; Gate 1 cost about 25 minutes extra). One definition ("blocking is a real defect: wrong behaviour, false claim, missing deliverable, security or data-loss risk") is copied across many installed primitives and says a false claim blocks whatever its consequence. A partial fix already exists (the Medium class and `follow-up candidates` in `pragmatic.md`) but is not enforced or generalised. The owner wants real blockers still found, non-decisive findings recorded and offered as follow-up issues, and a blocker classifier with a confidence score.

## Known Context

- Clarify batch (answered from the preamble): the scope is requirements and design options only (no code; edits nothing under `src/`); more than 5 files change, so a `/sc:workflow` plan must exist before any edit; the 35 percent score target "doesn't need to be strictly met"; security, data-loss and safety findings are never downgraded.
- Run-2 measurement: Gate 1, 11 blocking to 6 (minus 45 percent), average score 2.09 to 1.64 (minus 22 percent); Gate 2, reviewers' blocking counts 23, consolidated 8; Gate 3, 110 findings (2 blocking). Source: `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/`.
- Existing mechanisms to generalise, not reinvent: Medium and `follow-up candidates` (`src/superclaude/output-styles/pragmatic.md` lines 225-231, verified on disk); spec-panel's consequence test; `/sc:implement` qa.md derives severity from four yes/no answers; `finding-grader` (blind per-claim grader, installed only); loop caps in `src/superclaude/skills/task/SKILL.md`.
- Jev findings (`jev-uses.md`): Jev judges supplied text only; design is 10 atomic Noul questions plus a Score for severity, a truth table in code (4096 input combinations checked, monotone), thresholds as placeholders, verdict confidence by weakest link, a fallback judge chain (Jev, LLM judge, reviewer label), no API key in this environment, a privacy decision (finding text leaving the machine) that is the owner's.
- Validation data for the classifier (30+ scored findings) is produced by other steps of the program (step 01 inventory was empty when this ran).
- Preamble vs code: the preamble says 21 files and 109 occurrences. A Grep for the exact definition phrase found 11 files and 12 occurrences under `src/superclaude`; the code wins, and the spec must restate the file list from Grep with the pattern used.

## Constraints

- Requirements only. No edit under `src/`, `tests/`, `.claude/`, `~/.claude/`; no git write; no GitHub issue or post; Python only via `uv run`.
- Installed primitives must never point at `src/superclaude/` paths (dual-surface lookup rule in the repo CLAUDE.md); one shared rule document must be reachable by an installed path.
- A protocol with its own severity model (`/sc:implement` qa.md) keeps it; the pragmatic rule says so.
- No issue is created without the user's answer; unattended runs only record.
- No Jev API call, no account, no key request; the key is a dependency, stated as such.

## Success Criteria

- The spec states the proposed rule in plain words, the record-and-offer flow (ledger format, offer wording, unattended behaviour), the classifier concept with its Jev use and key dependency, guardrails against hiding real defects, the file list from Grep, the tests that pin the rule text, rollout stages, metrics, risks and owner decisions, and says what was verified and not.
- Every claim about a file, count or line is from a live Read or Grep.

## Open Questions

- Which primitives keep their own scale (qa.md, spec-panel, `card_convert.py`, reflect deviation taxonomy) and how each maps onto the shared rule.
- One shared rule document: where it lives so the installer copies it, and how a test detects drift in the copies.
- Where the follow-up ledger lives per run and how it batches into one issue through the `/sc:issue --create` templates.
- Whether the classifier ever gates, or stays advisory after shadow mode; whether it may fill qa.md's four checklist answers.
- Where `decision_basis` comes from for each deliverable kind (needed by the classifier's D question).
- Reconcile 21 files and 109 occurrences with the Grep counts.
- Whether finding text may be sent to an external API (privacy), and whether to request a key.

## Required Spec Shape (for every proposal agent)

Before writing, READ (absolute prefix `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/`): `02-brainstorm-context-preamble.md`, `00-issue-description.md`, `02-brainstorm/jev-uses.md`, and the three files in `02-brainstorm/enrichment/`. Do not re-derive their facts; cite them. Write a SPEC (requirements and design options, no code) with these sections: problem statement; goals and non-goals; the proposed rule in plain words (with the three blocking conditions and what is never downgraded); the record-and-offer behaviour (flow, follow-up ledger format, offer wording, what unattended runs do, batching into one issue); the classifier concept and its Jev use (use `jev-uses.md`: questions, truth table, confidence, key dependency, fallback judges, shadow mode); guardrails against hiding real defects; the one-source-of-truth design (shared rule document and drift test) and which primitives keep their own scale; the list of files and primitives that would change (from the enrichment Grep results, with counts and patterns); tests that pin the rule text and what changes; rollout stages; metrics and revert triggers; risks; the owner decisions, each with a recommendation; what was verified and what was not. Plain English, no em dashes.

## Enrichment Context

Full artifacts (read these; the spec must cite them): `enrichment/rule-copies-and-tests.md`, `enrichment/severity-models-and-loops.md`, `enrichment/follow-up-and-issue-mechanisms.md`, and the pre-supplied `jev-uses.md`. Codebase scan tier: primary (three read-only agents with Grep/Read; one `augment_code_search` call on master returned the earlier inventory at `.dev/review-severity-rule/`). Research-light: not run, because `jev-uses.md` already holds the external research (live TypeSafe docs); research-deep skipped under `--unattended`.

Headline facts (verified in this run by the agents and a spot-check by the orchestrator):

1. The rule is in 11 files with the exact definition sentence (not 21 files and 109 occurrences; no pattern reproduces that figure; "2 fix cycles" alone matches 22 files, 139 times). The plugin mirror holds none of the 11. The earlier inventory `.dev/review-severity-rule/inventory.md` (PR #343, commit `80f934de5`) is a plan of old-wording sites and matches the 11 files; it predates the Medium tier, the spec-panel scale and `card_convert.py`.
2. 8 test modules pin the rule or Medium text; the main one is `tests/skills/test_review_severity_rule.py` (5 pinned bullets in `pragmatic.md`, 10 copies, edit tables). Moving the bullets breaks `canonical_rule_bullets()` and every test that imports it.
3. A new `src/superclaude/core/REVIEW-SEVERITY.md` installs to `~/.claude/REVIEW-SEVERITY.md` with no installer change (`src/superclaude/cli/install_core.py` globs `core/*.md`, verified). Plugin mirror, project `.claude/` mirror and tests need hand-made steps.
4. About 10 severity model families (about 16 vocabularies). Derive-by-code exists in the stoprule variant (`stoprule.py`, installed only, no `src/` copy), the diffgate and ledger variants, `findings_v2.py` and `severity_router.py`; `/sc:implement` qa.md derives from four yes/no answers by an agent-followed rule. `card_convert.py` only translates a reviewer word (`important` and `medium` map to non-blocking there while rf-qa treats IMPORTANT as blocking).
5. The Medium and `follow-up candidates` mechanism is stated, never enforced: prose in `pragmatic.md:230`, `spec-panel.md:259-260`, `document_review_loop_prompts.md`; no code performs the once-per-loop question; tests are static text pins. Absent from rf-qa agents, the task skill, tech-research, reflect, pr-submit, `/sc:implement`. In the tasklist loop Medium is blocking today (`sc-tasklist-protocol/SKILL.md:1614`); reflect's Drift class blocks promotion (`sc-reflect-protocol/SKILL.md:1540`).
6. Minors already persist in four shapes (rf-qa tables under `qa/`, implement `notes.md`, troubleshoot follow-up tasks, reflect deviation blocks), so no single follow-up format exists. `/sc:issue --create` takes one description and files one issue (no batch, no ledger input, no unattended path, never-as-worker list).
7. Run 2 cost: five non-decisive findings (P3-001, P3-002, P3-006, P3-007, P3-013) plus two unescaped-pipe table rows forced the second fix cycle.
