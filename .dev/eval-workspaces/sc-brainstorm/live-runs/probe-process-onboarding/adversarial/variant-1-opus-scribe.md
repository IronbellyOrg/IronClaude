---
variant: 1
persona: opus:scribe
topic: improve onboarding workflow for new contributors
created: 2026-05-25
---

# Variant 1 — The Curated Documentation Spine (scribe lens)

## 1. Proposal Summary

Onboarding is fundamentally a *discoverability and sequencing* problem, not a tooling problem. The fix is a small, deliberately layered documentation set anchored by a single linear entry point (`CONTRIBUTING.md`), backed by a thin `docs/contributing/` folder that decomposes the dense CLAUDE.md mental model into four short, audience-tagged guides (Setup, Mental Model, First PR Walkthrough, Troubleshooting). A modest `make onboard-check` target verifies the documented happy path in CI so the docs cannot silently rot. No new CLI surface, no skill, no scaffolding script — just *the right documents, in the right order, with a maintenance contract*.

## 2. Functional Requirements

- **FR-001 — Single canonical entry point.** `CONTRIBUTING.md` at repo root MUST be the only document a first-time contributor needs to open. Every other onboarding document MUST be linked from it.
- **FR-002 — 30-minute green path.** Following `CONTRIBUTING.md` top-to-bottom on a clean Linux/macOS machine with Python 3.10+ and git installed MUST produce a passing `make test` run in ≤30 minutes of wall-clock time, with no maintainer DM.
- **FR-003 — Layered topic guides.** `docs/contributing/` MUST contain exactly these four files: `01-setup.md`, `02-mental-model.md`, `03-first-pr.md`, `04-troubleshooting.md`. No nested subfolders.
- **FR-004 — Two-click rule for confusion points.** Each of the five canonical confusion points (UV-only, src→sync-dev→.claude SoT, worktrees, skills/agents/commands surfaces, MCP server roles) MUST be reachable in ≤2 clicks from `README.md` and MUST have exactly one authoritative paragraph (no duplication across guides; other docs link to it).
- **FR-005 — `make onboard-check` target.** A new Make target MUST execute the documented happy-path commands in order (`uv --version`, `make dev`, `make verify`, `make verify-sync`, `make test`) and exit non-zero if any step fails. It MUST run in CI on every PR that touches `CONTRIBUTING.md`, `docs/contributing/**`, or `Makefile`.
- **FR-006 — Audience tags.** Each guide MUST open with an audience header in the form `**Audience:** <role> | **Time:** <minutes> | **Prereqs:** <list>`. Roles: `first-time-contributor`, `returning-contributor`, `maintainer`.
- **FR-007 — Worked first-PR example.** `03-first-pr.md` MUST walk through one specific, reproducible "good first PR" (a typo fix in a skill `SKILL.md`) end-to-end: branch creation, edit in `src/`, `make sync-dev`, `make verify-sync`, `uv run pytest`, commit, push, PR open. Every command MUST be copy-pasteable single-line.
- **FR-008 — SoT discipline is taught, not just enforced.** `02-mental-model.md` MUST contain a section "Why `.claude/` is gitignored" that explains the SoT model in ≤200 words and shows the one allowed exception (`.claude/settings.json`).
- **FR-009 — Doctor integration.** `superclaude doctor` output MUST be the first diagnostic referenced in `04-troubleshooting.md`; new failure modes encountered during onboarding MUST be added to `doctor`'s checks rather than to prose-only troubleshooting steps.
- **FR-010 — Anti-violation guardrail.** `03-first-pr.md` MUST include a "Things that will fail your PR" callout listing the top three foot-guns (`git add -f .claude/...`, `pip install ...`, committing without `make verify-sync`).

## 3. Non-Functional Requirements

- **NFR-001 — Brevity budget.** No guide MUST exceed 400 lines. `CONTRIBUTING.md` MUST be ≤150 lines.
- **NFR-002 — Markdown-lint clean.** All onboarding docs MUST pass the repo's existing markdownlint config; CI gate already in place.
- **NFR-003 — Solo-maintainer ergonomics.** Total ongoing maintenance burden MUST be ≤30 min/quarter (measured by edits required to keep `make onboard-check` green after framework changes).
- **NFR-004 — No new runtime dependencies.** Implementation MUST use only existing tools: Make, UV, pytest, the `superclaude` CLI. No new Python packages, no shell frameworks, no doc generators.
- **NFR-005 — Discoverability.** `README.md` MUST surface "New contributor? Start with [CONTRIBUTING.md](CONTRIBUTING.md)" in the first 20 lines.
- **NFR-006 — Tone neutrality.** Voice MUST be procedural and second-person ("You will run…"); no jokes, no emoji, no condescension toward beginners, no jargon without first-use definition.
- **NFR-007 — Single-line command discipline.** Every command in onboarding docs MUST be runnable as a single pasted line (no heredocs, no `\` continuations) per the user's terminal constraint (see memory `feedback_no_multiline_paste.md`).
- **NFR-008 — Version-pinned references.** Any reference to a tool version (UV, Python, pipx) MUST cite the minimum tested version, not "latest".

## 4. Artifacts to Produce

| Artifact | Purpose | Audience | Maintenance Contract |
|---|---|---|---|
| `CONTRIBUTING.md` (new/rewritten) | Single linear entry: install → first PR → where to ask | first-time-contributor | Reviewed when `make dev` or `make test` semantics change |
| `docs/contributing/01-setup.md` | UV install, pipx install, repo clone, `make dev`, `make verify` | first-time-contributor | Updated when minimum tool versions change |
| `docs/contributing/02-mental-model.md` | The 5 confusion points, each in one paragraph, each with a "see also" link | all contributors | Updated when SoT or component layout changes |
| `docs/contributing/03-first-pr.md` | Worked "fix a typo in a skill" walkthrough, end-to-end | first-time-contributor | Re-run quarterly; any drift = bug in `make onboard-check` |
| `docs/contributing/04-troubleshooting.md` | Top 10 failure modes (sync-dev drift, hook block, UV missing, etc.) keyed to `superclaude doctor` output | all contributors | Append-only; new entries when issues reported |
| `Makefile` (add `onboard-check` target) | Verifies happy path runs end-to-end | CI + maintainers | Touched only when underlying targets change |
| `.github/workflows/onboard-check.yml` (or addition to existing CI) | Runs `make onboard-check` on PRs touching onboarding surface | CI | Touched only when CI runner changes |
| `README.md` (edit only) | Add "Start here" pointer in first 20 lines | all readers | One-line change; rarely revisited |

Explicitly **not** producing: a `superclaude onboard` CLI, a `skill: contributor-onboarding`, a scaffolded first-PR sandbox, an interactive bootstrap script. Each was considered and rejected (see §7).

## 5. Adoption Path

**Days 0–30 — Author and merge the spine.**
Write `CONTRIBUTING.md` + the four `docs/contributing/` guides + `make onboard-check`. Run the green-path manually on a fresh container. Merge as a single PR titled `docs(contributing): add layered onboarding spine`. Update `README.md` pointer in the same PR.

**Days 30–60 — Wire CI and observe.**
Add the CI gate. Watch the next 3–5 external contributor PRs. Log every maintainer clarification into `04-troubleshooting.md` (append-only). If any onboarding question is asked twice, the doc has failed — fix the source paragraph, not the answer.

**Days 60–90 — Measure and prune.**
Compare maintainer-DM volume and `git add -f .claude/...` incident count against the 30-day baseline. Prune any guide section that wasn't referenced or revisited. If `02-mental-model.md` is reliably the most-visited, consider promoting one section into `CONTRIBUTING.md` itself.

## 6. Success Metrics

- **M-001** — `make onboard-check` exits 0 on every CI run for 60 consecutive days (CI-checkable).
- **M-002** — Time-to-first-green-test for a new contributor ≤30 minutes (self-reported in a one-line PR template question).
- **M-003** — Zero `git add -f .claude/...` violations in the 90-day window (greppable in git history).
- **M-004** — Zero repeated maintainer clarifications on the five canonical confusion points (tracked by maintainer in `04-troubleshooting.md` git history — if the same Q gets answered twice, that's a doc bug).
- **M-005** — `CONTRIBUTING.md` ≤150 lines and each `docs/contributing/*.md` ≤400 lines, enforced by a tiny `wc -l` check in `make onboard-check`.
- **M-006** — At least one external contributor PR per 30 days that cites `CONTRIBUTING.md` in its description (qualitative; measured by maintainer).

## 7. Open Risks and Mitigations (addresses seed-brief open questions)

- **Linear vs contextual?** *Linear, with contextual depth.* `CONTRIBUTING.md` is one path; `docs/contributing/02-mental-model.md` provides the contextual branches. Multiple entry points fragment maintenance and violate the two-click rule.
- **Setup-failure vs conceptual-understanding priority?** *Setup first, concepts second.* A contributor with a broken env can read no docs; a contributor with a working env can ask questions. `01-setup.md` and `03-first-pr.md` carry the weight; `02-mental-model.md` is the depth tier.
- **Where does it live?** *In-repo markdown only.* A `superclaude onboard` CLI was rejected: it adds a maintenance surface (versioning, install path, output drift) without solving discoverability — the new contributor still needs to know the command exists. Markdown is grep-able, diff-able, and CI-checkable.
- **First-PR sandbox?** *No.* A scaffolded sandbox creates a separate code path that drifts from real contribution flow. The worked example in `03-first-pr.md` (typo fix in a real skill) gives the same pedagogical benefit at zero infra cost.
- **Skill integration?** *No.* A `skill: contributor-onboarding` would only be discovered *after* the contributor knows what skills are. Wrong layer.
- **Ceremony tolerance?** *Minimum viable.* Four short guides + one Make target + one CI line = ~600 lines of markdown total, ≤30 min/quarter maintenance.

**Residual risk — Docs rot.** Mitigated by `make onboard-check` running in CI and by the append-only discipline on `04-troubleshooting.md`.
**Residual risk — Contributor still asks before reading.** Mitigated by maintainer's standing reply: "See `CONTRIBUTING.md` §<n>; if that doesn't answer it, open an issue tagged `onboarding-gap` so we can fix the doc." This turns every DM into a doc improvement signal.
