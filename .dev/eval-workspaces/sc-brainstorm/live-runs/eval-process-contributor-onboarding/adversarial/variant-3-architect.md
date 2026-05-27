---
variant: 3
agent: haiku:architect
focus: system-level onboarding touchpoints
created: 2026-05-27T00:00:00Z
---

# Variant 3 — Tooling / Environment-First Onboarding (Architect / Haiku)

## Premise

The biggest invisible cost to newcomers isn't docs or process — it's the 60-90 minutes spent fighting environment setup, hook failures, and the source-of-truth dance. Invest sprint capacity in tooling that makes the right thing the easy thing, and onboarding improves whether docs are read or not.

## Proposed Improvements

### 1. `make onboard` one-shot bootstrap target

- Idempotent target that: checks UV install (instructs install if missing), runs `make dev`, runs a smoke-test suite (`uv run pytest -k smoke`), prints next-step links.
- Single command replaces the 5-step setup sequence in current CONTRIBUTING.md.
- Exits non-zero with clear remediation hints if any step fails.

### 2. Devcontainer / Codespaces config

- Add `.devcontainer/devcontainer.json` so contributors can open the repo in GitHub Codespaces or VS Code Dev Containers and have UV, pre-commit hooks, and dev deps preinstalled.
- Zero local setup for contributors on Windows or constrained machines.
- Lightweight — reuses existing Makefile targets; no new build pipeline.

### 3. Pre-commit hook UX overhaul

- Each hook (verify-sync, markdownlint, freshness-pre-edit) gets a `--explain` mode invoked on failure.
- Output format: "BLOCKED: <hook>. Why: <one-sentence>. Fix: <exact command>. Docs: <link>."
- Wraps existing hook logic; doesn't loosen any gate.

### 4. `superclaude doctor --contributor` mode

- Extend existing `superclaude doctor` with a contributor-focused profile that checks:
  - UV installed and active
  - Editable install present (`pip show superclaude` shows local path)
  - `make sync-dev` produces no diff
  - Pre-commit hooks are registered
  - Git remote is fork (warns if pointing at upstream directly)
- Single command newcomers can run when "something feels off."

### 5. Smoke-test marker for fast feedback

- Tag a handful of foundational tests with `@pytest.mark.smoke`.
- `uv run pytest -m smoke` completes in <30 seconds — newcomers can validate their env without waiting for the full suite.
- Documented as the "did my setup work?" check in QUICKSTART references.

## Success Metrics

- Setup-related GitHub issues (`pip install failed`, `verify-sync confusing`) drop by 50%.
- Median environment-setup time (clone → green smoke test) drops below 15 minutes.
- Codespaces usage grows to ≥30% of first-time contributors within 3 months (signal that the friction floor is meaningful).
- Hook-failure issues quote the new `--explain` output (signal contributors are self-serving).

## Sprint Plan (one 2-week sprint)

- Week 1: `make onboard`, smoke-test marker, devcontainer.json.
- Week 2: pre-commit `--explain` mode, `doctor --contributor` profile, end-to-end test on a clean VM.

## Risks

- Devcontainer maintenance burden if base image drifts. Mitigation: pin base image, add to dependabot.
- `make onboard` may mask underlying failures. Mitigation: verbose mode by default; quiet flag opt-in.
- Hook `--explain` output may go stale as hook logic evolves. Mitigation: explain strings live in same file as hook logic; review together.

## Out-of-Scope Acknowledged

- No documentation rewrite, no process changes, no maintainer rotation. Pure tooling-surface improvements.
