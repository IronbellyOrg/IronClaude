---
variant: 2
persona: sonnet-analyzer
approach: root-cause-driven
created: 2026-05-25
---

# Specification: Onboarding Workflow Improvement (Variant 2 — Analyzer)

## 1. Root-Cause Diagnosis

The evidence points to four root causes, ranked by leverage (how much downstream friction each removes when fixed):

**RC-1: Stale, contradictory documentation is worse than no documentation.**

`docs/developer-guide/contributing-code.md` references `python3 -m setup`, Python 3.8+, `pip`, and a flat `superclaude/` directory that no longer exists. `docs/developer-guide/README.md` claims "SuperClaude is NOT software" and "NOT Testable" — both false for a project with a CLI, pytest plugin, and real test suite. A new contributor who trusts these docs will fail at setup and lose confidence in all project documentation. This is the highest-leverage cause because it actively misleads rather than merely under-informs.

**RC-2: No single verifiable "green bar" moment in the first 30 minutes.**

The README lists `make dev` and `make verify` but does not guarantee a contributor knows what success looks like. There is no `make onboard` target that exercises the full happy path (clone, install, sync, test-green, identify-where-to-edit) and exits with a clear pass/fail. Without a checksum moment, contributors stall on "did I do this right?" and ping the maintainer.

**RC-3: The src/ -> sync-dev -> .claude/ SoT model is unique and undocumented as a workflow.**

CLAUDE.md states the rule, but nowhere is there a 3-line "why it exists, what it means for you, what happens if you get it wrong" explanation at contributor-appropriate depth. The `.gitignore` and hooks enforce this mechanically, but the conceptual model is learned only through failure (or reading the gitignore). This causes `git add -f .claude/` violations and repeated maintainer questions.

**RC-4: CONTRIBUTING.md covers CI hygiene but not how to make a first contribution.**

The existing CONTRIBUTING.md is well-scoped (rot-budget rule, pre-PR checks) but assumes the reader already has a working environment and knows what to edit. There is no bridge from "I just cloned this" to "here is a specific file I can open and change."

### Causes vs. Symptoms

| Symptom (observed friction) | Root cause |
|---|---|
| Contributor runs `pip install` | RC-1 (stale docs say pip) |
| Contributor asks "where do I edit?" | RC-4 (no guided first task) |
| Contributor runs `git add .claude/skills/` | RC-3 (model not explained at contributor level) |
| Contributor DMs maintainer with "did this work?" | RC-2 (no green-bar checksum) |
| Contributor abandons after env setup failure | RC-1 + RC-2 combined |

---

## 2. Targeted Interventions

**INT-1: Delete and replace `docs/developer-guide/` stale content.** (Targets RC-1)

Remove or rewrite the four developer-guide documents that reference the pre-v4 architecture. Replace with a single `docs/contributor-guide.md` that reflects the actual codebase: UV, `src/superclaude/` SoT, Make targets, pytest suite. This is the highest-ROI intervention because it removes active misinformation.

**INT-2: Add a `make onboard` Makefile target.** (Targets RC-2)

A single Make target that runs the documented happy path and exits 0 on success, non-zero on any failure. It should: (a) verify UV is installed, (b) run `make dev`, (c) run `make sync-dev`, (d) run `make verify-sync`, (e) run `make verify` (package + plugin check), (f) run `uv run pytest tests/ -x --timeout=60` (smoke test subset), (g) print a summary with next-step instructions. This replaces "read 6 docs and hope" with one command and a deterministic outcome.

**INT-3: Add a "SoT Model" section to CONTRIBUTING.md (or the new contributor guide).** (Targets RC-3)

A 10-line explanation block: what `src/superclaude/` contains, what `.claude/` is for, what `make sync-dev` does, what happens if you edit `.claude/` directly (hooks block you, or `verify-sync` catches drift), and the one-line fix (`make sync-dev`). Positioned prominently, not buried in a subsection.

**INT-4: Add a "First Contribution" guided walkthrough.** (Targets RC-4)

A concrete, copy-pasteable example: "Change the description of the `python-expert` agent" or "Add a test assertion to `tests/pm_agent/test_confidence.py`." The walkthrough touches `src/superclaude/`, runs `make sync-dev`, runs `make verify-sync`, runs the relevant test, and shows the `git diff` the contributor should expect. This converts abstract knowledge into a concrete, repeatable action.

---

## 3. Functional Requirements

**FR-001** The files `docs/developer-guide/contributing-code.md` and `docs/developer-guide/README.md` shall not contain any reference to `pip`, `python3 -m`, Python 3.8, or a flat `superclaude/` directory structure. Any content that describes the pre-v4 architecture shall be removed or replaced. Falsifiable: `grep -c 'pip\|python3 -m\|3\.8\|superclaude/Agents\|superclaude/Commands' docs/developer-guide/contributing-code.md docs/developer-guide/README.md` returns 0.

**FR-002** A new file `docs/contributor-guide.md` (or equivalent path under `docs/`) shall exist and contain: (a) UV-only setup instructions matching the Makefile, (b) the SoT model explanation per INT-3, (c) the first-contribution walkthrough per INT-4, (d) a reference to the existing CONTRIBUTING.md CI hygiene rules. Falsifiable: the file exists and contains sections matching (a)-(d).

**FR-003** The Makefile shall include a target `onboard` that: (a) checks `uv --version` exits 0, (b) runs `make dev`, (c) runs `make sync-dev`, (d) runs `make verify-sync`, (e) runs `uv run pytest tests/ -x --timeout=60`, (f) prints a pass/fail summary with a "next steps" message. Falsifiable: `make onboard` exits 0 on a clean clone after UV is installed, and exits non-zero if any step fails.

**FR-004** `make onboard` shall complete in under 5 minutes on a machine with UV pre-installed and reasonable network access. Falsifiable: `time make onboard` on a clean clone reports < 300 seconds.

**FR-005** The SoT model explanation (INT-3) shall be reachable in at most 2 clicks from README.md. Falsifiable: starting from `README.md`, count link hops to the section that explains `src/superclaude/` vs `.claude/`. Must be <= 2.

**FR-006** The first-contribution walkthrough (INT-4) shall reference at least one specific file path under `src/superclaude/` and at least one `make` target. Falsifiable: `grep -c 'src/superclaude/' <walkthrough-file>` >= 1 and `grep -c 'make ' <walkthrough-file>` >= 1.

**FR-007** No new onboarding artifact shall be committed under `.claude/skills/`, `.claude/commands/`, or `.claude/agents/`. Falsifiable: `git diff --name-only <base>..<branch>` contains no paths matching `.claude/skills/*`, `.claude/commands/*`, `.claude/agents/*`.

---

## 4. Falsification Plan

**INT-1 (stale doc removal):** Open `docs/developer-guide/contributing-code.md` and search for `pip`, `python3 -m`, `3.8`. Each must return 0 hits. Additionally, the claim "SuperClaude is NOT software" must not appear in any file under `docs/`. If any hit remains, the intervention failed.

**INT-2 (`make onboard`):** On a fresh VM or container with UV installed, clone the repo and run `make onboard`. If it exits 0 and prints a summary with "next steps", the intervention succeeded. If it exits non-zero or hangs, it failed. Record the wall-clock time.

**INT-3 (SoT model explanation):** Recruit one person unfamiliar with the project. Ask them to find "where should I edit a skill file?" starting from README.md. If they answer `src/superclaude/skills/` within 2 minutes and can explain why `.claude/` is not the answer, the intervention worked. If they open `.claude/skills/` first, it failed.

**INT-4 (first-contribution walkthrough):** Have the same person follow the walkthrough end-to-end. If they produce a valid diff touching `src/superclaude/` and passing `make verify-sync`, the intervention succeeded. If they stall or edit `.claude/` directly, it failed.

---

## 5. What We Are NOT Doing

**NOT building a `superclaude onboard` CLI command.** A Makefile target is sufficient, does not require code changes to the Python package, and avoids coupling onboarding to the package's release cycle. A future CLI command could wrap the Make target, but that is a separate decision.

**NOT creating a `skill: contributor-onboarding`.** Discoverability through the skills system is a nice property but adds coupling. The contributor guide is markdown in `docs/`, discoverable from README, version-controlled, and reviewable through standard PRs. A skill can wrap it later if the onboarding surface stabilizes.

**NOT building a "first-PR sandbox" with scaffolded task files.** This is a good idea for a future phase but introduces maintainer overhead (curating good-first-issues, keeping scaffolds current). The walkthrough in INT-4 provides the same guidance at lower maintenance cost.

**NOT adding interactive/choose-your-own-adventure onboarding paths by contribution type.** The seed brief asks whether onboarding should be linear or contextual. The evidence says: linear first. Most contributors fail at setup, not at "which path do I pick." A single path that gets them to a green test run and a successful first edit removes more friction than a branching taxonomy. Branching can be added later for repeat contributors.

**NOT rearchitecting the SoT model to eliminate the sync step.** The constraint is non-negotiable. The intervention is to explain it clearly, not to change it.

---

## 6. Success Metrics

**Leading indicators (measurable within 30 days):**

- `make onboard` success rate on clean clones: target >= 95% (measure: CI run on a clean docker image, or maintainer tests on a fresh VM).
- Zero `.claude/` paths in PR diffs from new contributors for 30 days after merge (measure: `git log --diff-filter=A -- '.claude/skills/*' '.claude/commands/*' '.claude/agents/*'`).
- `docs/developer-guide/` grep hit count for stale references: target 0 (measure: the grep in FR-001).

**Lagging indicators (measured at 90 days):**

- Time-to-first-PR for new contributors (proxy: time from first commit on a fork to PR open). Baseline: unknown; instrument by adding a `<!-- first-contribution: walkthrough -->` HTML comment to PR template and counting occurrences.
- Maintainer DMs / issue comments containing "how do I set up" or "where do I edit": baseline from current rate, target 50% reduction.
- CONTRIBUTING.md page views (if GitHub insights are available): trending up indicates the doc is being found and used.

**Baseline measurement plan:** Before merging, the maintainer records: (a) count of open issues labeled "question" or "good first issue" that are actually setup-blocked, (b) count of recent PRs (last 30 days) that touch `.claude/` paths incorrectly, (c) wall-clock time for a clean clone -> `make verify` green run using the current README alone (no new docs). These three numbers form the baseline.

---

## 7. Open Assumptions

**A1: Contributors have UV installed or can install it without guidance.** If UV installation is itself a friction point (e.g., contributors on managed machines without `curl | sh` access), the `make onboard` target will fail at step 1. Mitigation: the contributor guide should link to the UV installation page. If UV installation is a recurring blocker, a future intervention could vendor a UV binary or add a `make install-uv` target.

**A2: The test suite passes on a clean clone.** If `make test` has pre-existing failures (the rot mentioned in CONTRIBUTING.md), `make onboard` will fail even with correct setup. Mitigation: `make onboard` should run `uv run pytest tests/ -x --timeout=60` (fail-fast, with timeout) rather than the full suite, and the summary should distinguish "environment broken" from "test suite has known failures." If the suite is too flaky, the onboard target should pin to a specific smoke test directory.

**A3: A single linear onboarding path is sufficient for the current contributor volume.** If the project attracts contributors across wildly different domains (designers, technical writers, Python devs, ops engineers), a single path will underserve some. The current contributor base appears to be primarily Python-aware developers, so this assumption holds for now. If the contributor profile changes, revisit the "NOT doing contextual paths" decision.

**A4: The maintainer can commit to reviewing and merging the stale-doc removal within one session.** INT-1 is a deletion-heavy change. If it stalls in review, it does not block INT-2 through INT-4 (which can merge independently), but the stale docs remain active misinformation. The assumption is that removing false documentation is uncontroversial and fast to merge.

**A5: `docs/developer-guide/` can be replaced without breaking external links or the `superclaude install` surface.** If any external documentation or the install CLI references paths under `docs/developer-guide/`, removing those files breaks those references. Mitigation: grep for `docs/developer-guide/` across the codebase before deletion. If references exist, redirect or update them in the same PR.
