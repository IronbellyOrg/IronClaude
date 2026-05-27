<!-- Provenance: This document was produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Variant 2 (sonnet:analyzer) -->
<!-- Merge date: 2026-05-25T19:32:45Z -->
<!-- Convergence: 1.00 (16/16 diff points resolved) -->
<!-- adversarial_status: success -->

# Specification: Onboarding Workflow Improvement (Merged Requirements)

## 1. Root-Cause Diagnosis

<!-- Source: Base (V2) — diagnosis-first framing retained per debate S-002 -->

The evidence points to four root causes, ranked by leverage (downstream friction each removes when fixed):

**RC-1 — Stale, contradictory documentation is worse than no documentation.** `docs/developer-guide/contributing-code.md` references `python3 -m setup`, Python 3.8+, `pip`, and a flat `superclaude/` directory that no longer exists. `docs/developer-guide/README.md` claims "SuperClaude is NOT software" and "NOT Testable" — both false. A new contributor who trusts these will fail at setup AND lose confidence in the rest of project documentation, including any new onboarding spine. Highest-leverage cause because it *actively misleads*.

**RC-2 — No single verifiable "green bar" moment in the first 30 minutes.** The README lists `make dev` and `make verify` but does not guarantee a contributor knows what success looks like. Without a checksum moment, contributors stall on "did I do this right?" and DM the maintainer.

**RC-3 — The src/ → sync-dev → .claude/ SoT model is unique and unexplained at contributor depth.** The rule is stated in CLAUDE.md and enforced mechanically (gitignore + hooks + `verify-sync`), but the *why* and *what-it-means-for-you* live nowhere at first-contributor reading level. Cause of repeated `git add -f .claude/...` violations and clarifying questions.

**RC-4 — No bridge from "I just cloned this" to "here is a specific file I can change."** Existing `CONTRIBUTING.md` covers CI hygiene but assumes a working environment and editing knowledge.

### Causes vs. Symptoms

<!-- Source: V2 (original) -->

| Symptom (observed friction) | Root cause |
|---|---|
| Contributor runs `pip install` | RC-1 (stale docs say pip) |
| Contributor asks "where do I edit?" | RC-4 (no guided first task) |
| Contributor runs `git add .claude/skills/` | RC-3 (model not explained at contributor level) |
| Contributor DMs maintainer with "did this work?" | RC-2 (no green-bar checksum) |
| Contributor abandons after env setup failure | RC-1 + RC-2 combined |

---

## 2. Targeted Interventions

<!-- Source: V2 (original) with Change #8 hybrid layout incorporation -->

**INT-1 — Remediate stale content in `docs/developer-guide/`.** (Targets RC-1) Rewrite or delete every file under `docs/developer-guide/` that contains pre-v4 references (pip, python3 -m, Python 3.8, flat `superclaude/Agents|Commands` paths) or the false claims "SuperClaude is NOT software" / "NOT Testable." Replace narrative with redirects to the new `docs/contributing/` spine.

**INT-2 — Add `make onboard` (contributor-facing) and `make onboard-check` (CI gate).** (Targets RC-2) `make onboard` runs the documented happy path with a pass/fail summary and explicit next-steps message; `make onboard-check` is the CI variant invoked on every PR touching onboarding surface (machine-parseable output, no interactive prompts). The CI target MAY delegate to `make onboard --ci`. [Change #9 hybrid]

**INT-3 — Document the SoT model at contributor depth.** (Targets RC-3) A ≤200-word section in `docs/contributing/02-mental-model.md` (and a 5-line synopsis in the rewritten `CONTRIBUTING.md`) explaining: what `src/superclaude/` is, what `.claude/` is for, what `make sync-dev` does, what happens if you edit `.claude/` directly (hooks block; `verify-sync` catches drift), and the one-line fix.

**INT-4 — Add a worked first-contribution walkthrough.** (Targets RC-4) `docs/contributing/03-first-pr.md` walks through one concrete reproducible PR end-to-end. Two candidate exemplars: editing a `python-expert` agent description, or adding an assertion to `tests/pm_agent/test_confidence.py`. Each command MUST be copy-pasteable single-line per NFR-007.

**INT-5 — Establish a 4-guide audience-tagged spine under `docs/contributing/`.** (Targets RC-2 + RC-3 + RC-4 structurally) Create the directory with: `01-setup.md`, `02-mental-model.md`, `03-first-pr.md`, `04-troubleshooting.md`. Each guide opens with the audience tag header (FR-008). Rewritten `CONTRIBUTING.md` is the single canonical entry that links to the four. [Change #8 hybrid]

---

## 3. Functional Requirements

<!-- Source: V2 (original) + V1 incorporations per Changes #2, #3, #4, #9, #13 -->

**FR-001 — No stale references.** Files under `docs/developer-guide/` shall contain zero references to `pip`, `python3 -m`, Python 3.8, or flat `superclaude/Agents|Commands|Skills` paths. Falsifiable: `grep -E 'pip install|python3 -m|3\.8|superclaude/(Agents|Commands|Skills)' docs/developer-guide/**/*.md` returns 0 matches; the strings "SuperClaude is NOT software" and "NOT Testable" do not appear in `docs/`.

**FR-002 — Onboarding spine exists.** `CONTRIBUTING.md` (rewritten) and exactly the files `docs/contributing/{01-setup,02-mental-model,03-first-pr,04-troubleshooting}.md` shall exist. Additional files MAY be added but each must justify itself against the brevity budget (NFR-001). Falsifiable: file existence check; `ls docs/contributing/` lists the four mandated files.

**FR-003 — `make onboard` (contributor-facing).** The Makefile shall include `onboard` that: (a) checks `uv --version` exits 0, (b) runs `make dev`, (c) runs `make sync-dev`, (d) runs `make verify-sync`, (e) runs `uv run pytest tests/ -x --timeout=60`, (f) prints a pass/fail summary with next-step instructions on success and a documented file:section pointer on failure (see FR-013). Falsifiable: `make onboard` exits 0 on a clean clone with UV installed and exits non-zero with a parseable pointer on injected failure.

**FR-004 — `make onboard-check` (CI gate).** The Makefile shall include `onboard-check` that runs the same verification with machine-parseable output. It shall be invoked by CI on every PR that modifies `CONTRIBUTING.md`, `docs/contributing/**`, or `Makefile`. Falsifiable: CI config includes the trigger; the target exits 0 on clean main, non-zero on injected breakage.

**FR-005 — Onboard timing budget.** `make onboard` shall complete in under 300 seconds (5 minutes) on a machine with UV pre-installed and reasonable network access. Falsifiable: `time make onboard` reports < 300s on the reference machine.

**FR-006 — Two-click discoverability rule.** Each of the 5 canonical confusion points (UV-only Python, src→sync-dev→.claude SoT, worktrees, skills/agents/commands surfaces, MCP server roles) shall be reachable in ≤2 clicks from `README.md` AND shall have exactly one authoritative paragraph in the spine (other docs link, do not duplicate). Falsifiable: a maintainer-run traversal report (script-checkable: count hops from `README.md` to the canonical anchor for each confusion-point heading).

**FR-007 — No `.claude/` artifacts committed.** No onboarding artifact shall be committed under `.claude/skills/`, `.claude/commands/`, `.claude/agents/`, `.claude/hooks/`, or `.claude/templates/`. Falsifiable: `git diff --name-only main..HEAD` contains no paths matching those prefixes (the only allowed `.claude/` path is `.claude/settings.json`).

**FR-008 — Audience-tag header.** Each file in `docs/contributing/` shall open with `**Audience:** <role> | **Time:** <minutes> | **Prereqs:** <list>` where role ∈ {`first-time-contributor`, `returning-contributor`, `maintainer`}. Falsifiable: `head -3 docs/contributing/*.md` produces the header on each file.

**FR-009 — `superclaude doctor` is the first diagnostic.** `docs/contributing/04-troubleshooting.md` shall reference `superclaude doctor` (or `make doctor`) as the first diagnostic action. Any new failure mode discovered during onboarding shall be added as a check in `doctor` rather than as a prose-only troubleshooting step. Falsifiable: first non-header content of `04-troubleshooting.md` references the doctor command.

**FR-010 — First-contribution walkthrough specificity.** `docs/contributing/03-first-pr.md` shall reference at least one specific file path under `src/superclaude/` and at least one `make` target, and shall show the expected `git diff`. Falsifiable: `grep -c 'src/superclaude/' docs/contributing/03-first-pr.md` ≥ 1 AND `grep -c '^make ' docs/contributing/03-first-pr.md` ≥ 1.

**FR-011 — Anti-violation callout.** `docs/contributing/03-first-pr.md` shall include a "Things that will fail your PR" callout enumerating at minimum: `git add -f .claude/...`, `pip install ...`, committing without `make verify-sync`.

**FR-012 — README entry pointer.** `README.md` shall surface "New contributor? Start with [CONTRIBUTING.md](CONTRIBUTING.md)" within the first 20 lines. Falsifiable: `head -20 README.md` contains the pointer.

**FR-013 — Failure recovery routing.** `make onboard`'s failure summary shall direct the contributor to a specific section anchor in `docs/contributing/04-troubleshooting.md` keyed to the failing step. Falsifiable: simulate failure at each of steps (a)–(e) and verify the printed pointer resolves to an addressable troubleshooting entry.

---

## 3.5 Non-Functional Requirements

<!-- Source: V1 §3 NFRs, filtered to non-duplicates per Change #1 -->

**NFR-001 — Brevity budget.** No guide MUST exceed 400 lines; `CONTRIBUTING.md` MUST be ≤150 lines. Falsifiable: `wc -l CONTRIBUTING.md docs/contributing/*.md` reports each file under cap (enforced via `make onboard-check`).

**NFR-002 — Markdownlint clean.** All onboarding docs MUST pass the repo's existing markdownlint configuration.

**NFR-003 — Solo-maintainer budget.** Total ongoing maintenance burden MUST be ≤30 min/quarter, measured by edits required to keep `make onboard-check` green after framework changes.

**NFR-004 — No new runtime dependencies.** Implementation MUST use only existing tools: Make, UV, pytest, the `superclaude` CLI. No new Python packages, no shell frameworks, no doc generators.

**NFR-005 — README discoverability.** README's onboarding pointer MUST appear in the first 20 lines (also covered by FR-012; included here for quality framing).

**NFR-006 — Tone neutrality.** Voice MUST be procedural and second-person ("You will run…"); no jokes, no emoji, no condescension toward beginners, no jargon without first-use definition.

**NFR-007 — Single-line command discipline.** Every command in onboarding docs MUST be runnable as a single pasted line — no heredocs, no `\` continuations, no multi-line quoted strings. Grounded in user terminal constraint (memory `feedback_no_multiline_paste.md`).

**NFR-008 — Version-pinned references.** Any reference to a tool version (UV, Python, pipx) MUST cite the minimum tested version, not "latest".

---

## 4. Falsification Plan

<!-- Source: V2 §4 (original) with Change #13 failure-recovery addition -->

**INT-1 (stale doc remediation):** Run `grep -REn 'pip install|python3 -m|3\.8|superclaude/(Agents|Commands|Skills)|SuperClaude is NOT software|NOT Testable' docs/developer-guide/`. Must return zero matches. If any hit remains, the intervention failed.

**INT-2 + INT-2-CI (`make onboard` / `make onboard-check`):** On a fresh container with UV installed, clone the repo and run `make onboard`. Must exit 0 in <300s with a summary including "next steps." Inject a controlled failure (e.g., temporarily break `make verify-sync`) and re-run; must exit non-zero AND print a pointer to a real `04-troubleshooting.md` anchor.

**INT-3 (SoT model explanation):** Recruit one tester unfamiliar with the project. Ask them to find "where should I edit a skill file?" starting from `README.md`. Pass: answers `src/superclaude/skills/` within 2 minutes and can explain why `.claude/skills/` is the wrong answer. Fail: opens `.claude/skills/` first or cannot articulate the SoT rule.

**INT-4 (first-contribution walkthrough):** Same tester follows `03-first-pr.md` end-to-end. Pass: produces a valid diff touching `src/superclaude/`, passes `make verify-sync`, and the diff matches the expected diff shown in the walkthrough.

**INT-5 (spine structure):** Verify file presence (FR-002), audience-tag headers (FR-008), brevity caps (NFR-001), two-click rule (FR-006), markdownlint (NFR-002) all pass as a single CI run via `make onboard-check`.

---

## 5. What We Are NOT Doing

<!-- Source: V2 §5 (original) + V1 §7 open-Q resolutions per Change #10 -->

**NOT building a `superclaude onboard` CLI command.** A Makefile target is sufficient, does not require code changes to the Python package, and avoids coupling onboarding to the package's release cycle. A future CLI wrapper is a separate decision.

**NOT creating a `skill: contributor-onboarding`.** Discoverability via the skills system is nice but adds coupling. The contributor guide is markdown in `docs/`, discoverable from README, version-controlled, reviewable through standard PRs.

**NOT building a "first-PR sandbox" with scaffolded task files.** The walkthrough in INT-4 (a real edit to a real file) provides the same pedagogical benefit at zero infra cost and zero drift surface.

**NOT adding interactive / choose-your-own-adventure onboarding paths by contribution type.** Single linear path first; branching can be added later for repeat contributors if evidence demands.

**NOT rearchitecting the SoT model to eliminate the sync step.** The constraint is non-negotiable. The intervention is to explain it clearly, not to change it.

---

## 6. Adoption Path

<!-- Source: V1 §5 (original Adoption Path) restructured against V2 intervention ordering -->

**Days 0–14 — Step 0: Remove active misinformation (RC-1).** Land a single PR titled `docs(developer-guide): remove stale pre-v4 references`. This is INT-1 and is a prerequisite for all later changes.

**Days 14–45 — Build the spine.** Land a PR titled `docs(contributing): add layered onboarding spine`. This adds INT-2 through INT-5: both Make targets, the four `docs/contributing/` guides, rewritten `CONTRIBUTING.md`, README pointer, CI wiring for `make onboard-check`.

**Days 45–75 — Observe.** Watch the next 3–5 external contributor PRs. Log every maintainer clarification into `04-troubleshooting.md` (append-only). Apply the DM-as-doc-bug rule (§7.5).

**Days 75–90 — Measure and prune.** Compare against baseline (§6.5) for maintainer-DM volume, `.claude/` violation count, and time-to-first-green-test. Prune any guide section unreferenced in 60 days.

---

## 6.5 Success Metrics

<!-- Source: V2 §6 (baseline plan + leading/lagging) + V1 M-001..M-006 incorporations + Change #6 DM rule -->

**Baseline measurement (pre-merge):** Maintainer records (a) count of open issues labeled `question` or `good first issue` that are actually setup-blocked, (b) count of recent PRs (last 30 days) that incorrectly touch `.claude/` paths, (c) wall-clock time for clean-clone → `make verify` green run using current README alone.

**Leading indicators (≤30 days):**

- `make onboard-check` success rate on CI: ≥95%
- `make onboard` success rate on clean clones (maintainer test): ≥95%
- Zero new `git add -f .claude/...` violations in PR diffs
- `grep` falsifiability checks for FR-001 + FR-007 + FR-008 + FR-010 all pass

**Lagging indicators (90 days):**

- Time-to-first-PR for new contributors (instrument via `<!-- first-contribution: walkthrough -->` HTML comment in PR template)
- Maintainer-DM volume containing "how do I set up" / "where do I edit" reduced ≥50% vs. baseline
- ≥1 external-contributor PR per 30 days that cites `CONTRIBUTING.md` in description

**Improvement loop (Change #6 DM-as-doc-bug rule):** Maintainer's standing reply: "See `<doc-section>`; if that doesn't answer it, open an issue tagged `onboarding-gap` so we can fix the doc." Any onboarding question answered twice = a doc bug; file the issue and fix the *source paragraph*, not just the questioner.

---

## 7. Decisions on Seed-Brief Open Questions

<!-- Source: V1 §7 (explicit Q-by-Q resolution) per Change #10 -->

- **Linear vs contextual?** Linear, with contextual depth via `02-mental-model.md`. Multiple entry points fragment maintenance and violate FR-006.
- **Setup-failure vs conceptual-understanding priority?** Setup first. A broken-env contributor reads no docs; a working-env contributor can ask questions. `01-setup.md` + `03-first-pr.md` carry weight; `02-mental-model.md` is depth tier.
- **Where does the workflow live?** In-repo markdown only. CLI / skill / sandbox alternatives all rejected (§5).
- **First-PR sandbox?** No (§5).
- **Skill integration?** No (§5).
- **Ceremony tolerance?** Minimum viable: 4 short guides + 2 Make targets + 1 CI line + 1 README pointer = ~600 lines markdown + ~30 lines Makefile + ~10 lines CI. NFR-003 caps maintenance at ≤30 min/quarter.

---

## 8. Open Assumptions

<!-- Source: V2 §7 (original A1–A5) — retained verbatim -->

**A1 — Contributors have UV installed or can install it.** If UV install is itself a friction point (managed machines without `curl | sh` access), `make onboard` fails at step 1. Mitigation: contributor guide links to UV install page; if recurring, add `make install-uv` or vendor a binary.

**A2 — The test suite passes on a clean clone.** If pre-existing failures exist, `make onboard` fails even with correct setup. Mitigation: smoke-subset via `-x --timeout=60`; summary distinguishes "env broken" from "known suite failures."

**A3 — Single linear onboarding path is sufficient.** Holds for current Python-aware contributor base. Revisit if contributor profile diversifies.

**A4 — Maintainer can review/merge INT-1 stale-doc removal in one session.** If stalled, INT-2 through INT-5 can merge independently — but stale docs remain active misinformation until INT-1 lands.

**A5 — `docs/developer-guide/` can be replaced without breaking external links or `superclaude install` surface.** Mitigation: pre-deletion grep for `docs/developer-guide/` across the codebase; redirect or update references in the same PR.

---

## 9. Promoted Shared Assumptions (AD-2 transparency)

<!-- Source: Adversarial AD-2 — UNSTATED preconditions surfaced during debate -->

These were implicit in both variants and were affirmed by both advocates; documented here so future re-reviews can challenge them.

- **SA-001 (L3, UNSTATED→accepted):** A Makefile target is the correct primitive for the green-bar moment (vs. shell script, Docker compose, or CLI subcommand). Challenge condition: if Make becomes a friction for non-Unix contributors.
- **SA-002 (L2, UNSTATED→accepted):** A single linear onboarding path is sufficient for the current contributor mix. Equivalent to A3; explicitly carried here as adversarial-surfaced assumption.
- **SA-003 (L2, UNSTATED→accepted):** README is the canonical discovery entry point. Challenge condition: if discovery moves to GitHub Wiki, a docs site, or in-CLI help (`superclaude --help-contribute`).

---

<!-- end merged-requirements.md -->
