# Scope Discovery — PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot)

> **Scope:** product · **Scenario:** A · **Date:** 2026-06-11
> **Driving spec:** `.dev/brainstorms/20260611-005638-pr-remediation-v2-mention-bot/merged-requirements.md`
> (force-bound; treated as authoritative ground truth, read in full).
> All file/line anchors below were verified against disk during discovery.

## Project Overview

**IronClaude** (package `superclaude`, v4.2.0) is a Python framework that packages a
pytest plugin, a `superclaude` Click CLI, a suite of slash-command "skills", and agent
definitions for Claude Code. Source of truth lives under `src/superclaude/`; `.claude/` is
gitignored sync-dev output. The CLI already hosts a family of subcommand groups
(`sprint`, `roadmap`, `swarm`, `prd`, `tasklist`, `eval`, `cli-portify`, `cleanup-audit`,
`recommend`, `init-lite`) that **wrap headless `claude --print` subprocesses** to run
multi-agent pipelines.

**This PRD's subject — PR Auto-Remediation V2.0 — is a net-new feature** within that
monorepo: a `superclaude remediate` CLI group implementing a mention-triggered, headless,
on-prem PR remediation bot. The architecture (per the merged spec) is a **split host**:

- a **long-lived Dispatcher** (systemd daemon) that polls GitHub for `@bot` mentions in PR
  review-comment replies, runs a live authorization gate, claims triggers in an on-disk
  ledger, and pushes host-side with short-lived tokens; and
- an **ephemeral per-trigger Runner** (sandboxed, disposable) that runs `claude -p` against
  an isolated PR-head checkout, treating the parent review comment (`opComment`) as untrusted
  data inside a trusted prompt envelope.

The central engineering risk the product must neutralize: **executing an LLM agent with
file-write + git-push authority in response to untrusted GitHub comment text.** The whole
design is organized around authorization, injection containment, a conservative
propose-only default, secret separation, and bounded loop-safety.

**V2.0 replaces V1.0's in-session Monitor-tool host** (which died when the terminal closed).
The V1.0 spec lives at `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/`
(`merged-requirements.md` + a 74 KB `merged-spec.md`) and is the lineage for the severity
rubric, autonomy `needs_human_decision` classes (V1.0 FR-4.4), and the fork-only `gh` rule.

## Directory Structure

| Path | Purpose | Relevance to this PRD |
|------|---------|----------------------|
| `src/superclaude/cli/` | All CLI subcommand groups (SoT) | **Home of the net-new `remediate/` group (D1–H5).** Does not exist yet (greenfield, confirmed). |
| `src/superclaude/cli/pipeline/process.py` | Generic `claude -p` subprocess primitive | **Reuse anchor R2** — `ClaudeProcess` class at **line 72**; `build_env()` at line 145; stdin prompt delivery. |
| `src/superclaude/cli/swarm/` | Multi-agent swarm orchestrator | **Reuse anchor** — bounded-counter / `--watch-max-iterations` loop-guard idiom (`commands.py` ~line 2269) is the model for the round/budget counter. |
| `src/superclaude/cli/main.py` | Click root group + deferred subcommand registration | Wiring target — `remediate` group registers via the same `main.add_command(..., name=...)` deferred-import pattern (lines 400–438). |
| `src/superclaude/cli/sprint/`, `roadmap/`, `prd/`, `eval/`, `cli_portify/`, `cleanup_audit/` | Existing pipeline groups that wrap `ClaudeProcess` | Precedent that a CLI group spawning `claude -p` is the established pattern (18+ callers of the process primitive). |
| `src/superclaude/skills/sc-auggie-review-protocol/` | Auggie code-review skill | **Reuse anchor S1** — `refs/severity-rubric.md` (5-tier rubric, remap lines 63–101); `SKILL.md` is the `gh` inline/summary posting precedent (template for H4 reply/resolve). |
| `tests/cli/` | CLI test suite | **Home of net-new `tests/cli/remediate/` (T1).** `test_cli_registration.py` is the registration-test precedent. |
| `deploy/` | (does not exist) | **Greenfield S2** — `deploy/remediate-bot/` systemd units + sandbox image are net-new. |
| `remediation/` (top-level) | Empty placeholder dir | Currently empty; not the feature's source home (source goes under `src/superclaude/cli/remediate/`). Flag for clarification. |
| `.dev/brainstorms/20260611-.../` | This feature's brainstorm artifacts | Holds the merged-requirements spec, seed-brief, adversarial/enrichment outputs, and this PRD pipeline dir. |
| `.dev/brainstorms/20260610-234750-.../` | V1.0 spec lineage | V1.0 merged-requirements + merged-spec + prior-art-evaluation. |

## Product Areas

The merged spec decomposes cleanly into **seven functional areas**. Each maps to spec
sections and the component inventory (§2).

### PA-1 — GitHub Ingress & Mention Detection
Polling-based comment ingest with ETag/304 conditional requests, `@bot` trigger-grammar
filtering, and parent-comment (`opComment`) resolution via `in_reply_to_id`. Components D3
(ingest + ETag cursor), D4 (mention grammar whitelist parser), D6 (parent resolver +
integrity re-check). Spec §1 (detection = polling, webhooks deferred), §3, §4.
**Greenfield** — no `issue_comment` polling, `in_reply_to`, or webhook handling exists today.

### PA-2 — Authorization & Trust Boundary
Live, per-trigger collaborator-permission gate (`admin|write` only), re-run before every
dangerous action; authority-invariant enforcement (only the live event `sender`, `type ==
User`, grants authority — never comment text, parent author, or bots); enumerated bypass
defenses (spoofed login, edited mention/parent, fork author, TOCTOU). Component D5. Spec §5.
**Greenfield** — no `collaborators/{user}/permission` gating exists.

### PA-3 — Injection Containment & Sandboxing
`opComment`-as-data discipline (JSON-encoded, length-capped, stdin-delivered inside a CONTROL
envelope, never shell-interpolated); ephemeral non-root sandbox with no host-home/`.aienv`/
`/config/.claude`/Docker-socket/SSH mounts; deny-by-default egress allowlist
(`:4000/cli` + `api.github.com` + single repo git endpoint). Components R3 (envelope
builder), R4 (sandbox provisioner). Spec §6, §7. Sandbox tech is OD-1 (container vs microVM).

### PA-4 — Headless Execution Host
Reuse of `ClaudeProcess` (R2) with an **allowlist `env_vars`** wrapper (not full
`os.environ.copy()`) so the Runner receives only minimal Claude/proxy auth — **no
`GH_TOKEN`, no push credential**. Severity→action routing (S1) re-grades findings via the
rubric (Critical/High → `/sc:troubleshoot --depth deep --fix`, etc.). Components R1 (runner
entrypoint), R2 (executor wrapper). Spec §7, §17.

### PA-5 — Autonomy, Idempotency & Loop-Safety
Autonomy lattice (`propose < patch < fix < push < resolve`, default propose) with
effective-level = lattice-min of parsed-flag/authz/validation, then off-lattice HALT
short-circuits (`needs_human_decision`, `pr_push_budget == 0`). Two-phase intent/outcome
JSONL ledger (intent-without-outcome = RESUME), per-PR push budget, exact-SHA round
correlation. Components H1 (ledger), H2 (autonomy gate). Spec §8, §9, §10.
**Greenfield logic**, modeled on the swarm bounded-counter idiom.

### PA-6 — Mutation, Reply & Resolve (host-side)
Host-side git push with a short-lived per-trigger repo+branch-scoped token (H3, never in the
Runner); reply-to-thread (`pulls/<N>/comments/<id>/replies`) + GraphQL
`resolveReviewThread` matched on `databaseId` with pagination (H4); the H5 `gh` wrapper that
**unconditionally** injects `--repo IronbellyOrg/IronClaude` so no code path can call `gh`
without it. Spec §3, §11, §12. **Greenfield** — reply/resolve endpoints absent from repo.

### PA-7 — Secrets, Deploy, Audit & Observability
Three-way credential separation (Anthropic/proxy → Runner only; GitHub read+comment →
long-lived Dispatcher; GitHub push → short-lived host-side); secret redaction
(`TOKEN|KEY|AUTH|SECRET` masking, `sys.excepthook` stripping); systemd unit hardening
(`Restart=always`, `WatchdogSec`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`);
append-only per-trigger audit JSONL (distinct from the §10 state ledger); rate-limit safety
(≥30s poll, `Retry-After`, backoff); alerts (`RemediationLoopDetected`, `AuthzFailureSpike`,
etc.). Components S2 (systemd + sandbox image), §11, §13, §14, §15. **Greenfield** (`deploy/`
dir absent).

## Technology Stack

| Layer | Choice | Evidence |
|-------|--------|----------|
| Language | Python ≥3.10 | `pyproject.toml`, CLAUDE.md |
| Package/runtime | UV (never bare pip/python) | CLAUDE.md absolute rule |
| Build | hatchling (PEP 517) | CLAUDE.md package info |
| CLI framework | Click ≥8.0 | `cli/main.py` `@click.group()`, all subcommand groups |
| Subprocess host | `ClaudeProcess` (`subprocess.Popen` + process groups, stdin prompt) | `cli/pipeline/process.py:72` |
| GitHub API surface | `gh` CLI (REST `gh api` + GraphQL) | spec §3/§12; precedent in `sc-auggie-review-protocol/SKILL.md` |
| Agent runtime | `claude --print --dangerously-skip-permissions --max-turns N --output-format stream-json` | `process.py:121` `build_command()` |
| Auth/proxy | LiteLLM proxy at `:4000/cli` via `~/.aienv` (`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`) | seed-brief, memory `feedback_aienv_only_proxy_contract` |
| State store | On-disk JSONL ledger (atomic temp+`os.rename`, `O_APPEND`, flock) | spec §10 |
| Deploy | systemd (daemon) + container/microVM sandbox (OD-1) | spec §15, §21 |
| Tests | pytest (markers: `confidence_check`, `self_check`, `reflexion`) | `pyproject.toml`, CLAUDE.md |
| Lint/format | ruff (`make lint` = check only; CI also `ruff format --check`) | memory `reference_make_lint_vs_ci_ruff_format` |

**Key dependencies named in spec:** GitHub App installation token *or* fine-grained PAT
(OD-2); rootless Docker/Podman or Firecracker microVM (OD-1). Neither is wired today.

## Existing Documentation

| Path | Description |
|------|-------------|
| `.dev/brainstorms/20260611-005638-.../merged-requirements.md` | **Authoritative driving spec** (25 KB, 21 sections + reuse/handoff). Force-bound ground truth. |
| `.dev/brainstorms/20260611-005638-.../seed-brief.md` | Original problem statement, known-context reuse anchors, user constraints C1–C5, open questions OQ-A–E. |
| `.dev/brainstorms/20260611-005638-.../adversarial/` | Invariant-probe + adversarial-merge artifacts (4 HIGH / 10 MEDIUM resolutions cited in §16). |
| `.dev/brainstorms/20260610-234750-.../merged-requirements.md` + `merged-spec.md` (74 KB) | **V1.0 lineage** — propose/fix autonomy, severity rubric, `needs_human_decision` (FR-4.4), monitor-host design now replaced. |
| `.dev/brainstorms/20260610-234750-.../prior-art-evaluation.md` | V1.0 prior-art survey. |
| `CLAUDE.md` (project) | Absolute rules: fork-only `--repo IronbellyOrg/IronClaude` PR target; never stage `.claude/`; UV-only; sync-dev discipline. |
| `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | 5-tier severity rubric (reused by S1, §17). |
| `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | `gh` inline/summary PR-posting precedent (H4 template). |
| `KNOWLEDGE.md`, `PROJECT_INDEX.md`, `SECURITY.md` | Repo-wide insight/index/security docs. |

## Integration Points

- **GitHub REST API** (`gh api`): `pulls/comments?since=&sort=created`, `issues/comments`,
  `pulls/comments/{id}` (parent body), `collaborators/{login}/permission`,
  `pulls/<N>/comments/{parent}/replies`. ETag/`If-None-Match` conditional requests.
- **GitHub GraphQL API**: `resolveReviewThread(threadId)` mutation; `reviewThreads`
  pagination matched on `databaseId` (NOT node `id`).
- **Anthropic via LiteLLM proxy** (`:4000/cli`): the Runner's `claude -p` agent auth; models
  per `~/.aienv` contract (T2Model01..NN) — proxy-only, never `:4000/v1` (memory).
- **Git** (PR-head checkout + host-side push): credential-less clone in Runner; short-lived
  scoped token push in Dispatcher (H3). Egress allowlist = single repo endpoint only.
- **systemd**: Dispatcher supervision (`Restart=always`, `WatchdogSec=60`,
  `EnvironmentFile=` chmod-600, SIGHUP rotation).
- **Container/microVM runtime** (OD-1): Runner sandbox isolation.
- **GitHub App / fine-grained PAT** (OD-2): short-lived push-token minting.
- **On-disk state dir** (e.g. `/opt/remediate-bot/state/`, gitignored): ledger + audit logs.

**Greenfield integration gaps confirmed by grep** (none exist in `src/` today):
`resolveReviewThread`, `comments/.../replies`, `in_reply_to`, collaborator-permission
gating, webhook/`issue_comment` ingress. The matches for "permission"/"webhook" in grep were
unrelated (sprint `rerun_tasks.py`, eval YAML, doc refs).

## Complexity Assessment

- **Estimated research agents needed: 6**
- **Key areas requiring dedicated investigation:**
  1. Security & trust boundary (authz, injection, sandbox, secret separation) — the spec's
     dominant risk surface and `base_variant = sonnet:security`.
  2. GitHub API integration (ingest, threading, reply/resolve, rate-limits) — entirely
     net-new endpoints with subtle correctness (databaseId pagination, ETag cursors,
     TOCTOU re-checks).
  3. Headless execution & reuse seam (`ClaudeProcess` allowlist-env wrapper, envelope, model
     routing) — depends on correctly extending a verified primitive.
  4. State, idempotency & loop-safety (two-phase ledger, per-PR push budget, SHA correlation)
     — net-new logic where bugs cause double-push or infinite loops.
  5. Architecture & control flow (split Dispatcher/Runner host, component seams, build
     sequencing §19) — the system-level decomposition that binds the other areas.
  6. Deploy / ops / observability (systemd hardening, sandbox image, audit schema, alerts) —
     the production-readiness surface.
- **Cross-cutting concerns:**
  - Fork-only `--repo IronbellyOrg/IronClaude` injection (C5) threads through every GitHub call.
  - SoT/sync-dev discipline (`src/` → `make sync-dev` → never stage `.claude/`).
  - Autonomy HALT semantics (`needs_human_decision` must never ship as a push) span PA-2/PA-5/PA-6.
  - Secret redaction + "opComment raw never stored" spans execution, ledger, and audit.
  - Four residual open decisions (OD-1 sandbox tech, OD-2 push-token mechanism, OD-3 push-budget
    default, OD-4 `patch` level) must surface as PRD open questions.

## Recommended Research Assignments

### RA-1 — Security & Trust-Boundary Analysis
- **Topic:** Authorization gate, injection containment, sandbox isolation, and secret
  separation — verify the spec's safety invariants are buildable and complete against the
  acceptance criteria (AC-1, AC-3, AC-7, AC-9).
- **Type:** Architecture Analyst (security lens)
- **Files:** spec §5/§6/§7/§11; `cli/pipeline/process.py` (`build_env` line 145, env handling);
  `~/.aienv` proxy contract (memory); CLAUDE.md secret rules; V1.0 `merged-spec.md` autonomy/
  `needs_human_decision` lineage.
- **Rationale:** Executing a write/push-capable LLM agent on untrusted comment text is the
  product's reason-for-existing risk; `base_variant = sonnet:security`. Highest-stakes area.

### RA-2 — GitHub API Integration Mapping
- **Topic:** Net-new GitHub ingress/threading/reply/resolve surface — REST + GraphQL shapes,
  ETag cursoring, `in_reply_to_id` parent resolution, `databaseId` thread matching, rate-limit
  handling, and the §19.1 probe-first requirement.
- **Type:** Integration Mapper
- **Files:** spec §3/§4/§12/§13; `sc-auggie-review-protocol/SKILL.md` (`gh` posting precedent);
  confirmed-absent endpoints (greenfield). Cross-check against GitHub REST/GraphQL docs.
- **Rationale:** All four greenfield gaps (threading, authz, reply/resolve, ingress) are here;
  correctness is subtle (node-id vs databaseId, 304 semantics) and untested in-repo.

### RA-3 — Headless Execution Reuse Seam
- **Topic:** Extending `ClaudeProcess` with an allowlist-`env_vars` wrapper; prompt-envelope
  construction; max-turns/output-format tuning; severity→action routing; model routing via
  `~/.aienv`.
- **Type:** Feature Analyst
- **Files:** `cli/pipeline/process.py:72` (class), `:121` (`build_command`), `:145`
  (`build_env`); existing callers (`sprint/executor.py`, `roadmap/executor.py`,
  `prd/process.py`, `eval/runner.py`); `severity-rubric.md`; spec §7/§17.
- **Rationale:** The product's only major *reuse* (vs build); must confirm the env-allowlist
  change is the right seam and that 18+ existing callers establish a safe pattern.

### RA-4 — State, Idempotency & Loop-Safety
- **Topic:** Two-phase intent/outcome JSONL ledger, RESUME semantics, per-PR push budget,
  exact-SHA round correlation, atomic-write/flock durability — against AC-5/AC-6.
- **Type:** Architecture Analyst
- **Files:** spec §8/§9/§10; `cli/swarm/commands.py` bounded-counter idiom (~line 2269) and
  `cli/swarm/state.py`; memory `reference_sprint_rerun_tasks` for recovery-verb precedent.
- **Rationale:** Net-new correctness-critical logic; failure modes are double-push and
  infinite loops. The swarm counter is prior art but the two-phase ledger is novel.

### RA-5 — Split-Host Architecture & Control Flow
- **Topic:** Dispatcher/Runner decomposition, component inventory (D1–H5, R1–R4, S1–S2),
  the §3 control-flow ordering, CLI-group wiring, and §19 build sequencing.
- **Type:** Architecture Analyst
- **Files:** spec §1/§2/§3/§19/§21; `cli/main.py` (deferred-registration pattern, lines
  400–438); `cli/swarm/` and `cli/sprint/` as multi-module-group precedents;
  `tests/cli/test_cli_registration.py`.
- **Rationale:** Binds all other areas; the split-host decision (§1) and component seams drive
  the PRD's functional decomposition and the four open decisions (OD-1..4).

### RA-6 — Deploy, Ops & Observability
- **Topic:** systemd unit hardening, Runner sandbox image (OD-1), three-way secret sourcing,
  audit-log schema (§14), rate-limit/backoff, alerting, rollback/replay.
- **Type:** Integration Mapper (DevOps lens)
- **Files:** spec §11/§13/§14/§15; absent `deploy/` dir (greenfield S2); `~/.aienv` /
  `ccsession.env` chmod-600 precedent; CLAUDE.md UV/sync-dev constraints.
- **Rationale:** Production-readiness surface entirely net-new; on-prem ops simplicity vs
  isolation strength (OD-1) and push-token mechanism (OD-2) are unresolved and PRD-relevant.

---

**Discovery confidence:** High. Every reuse anchor in the spec (`ClaudeProcess` at
`process.py:72` with `build_env` at `:145`; swarm bounded-counter ~`commands.py:2269`;
`severity-rubric.md`; fork-only `gh` rule) was verified on disk, and all four greenfield gaps
were confirmed absent via grep. The feature is a cohesive, security-dominated greenfield CLI
group reusing exactly one major primitive — six research agents give one-per-product-area
coverage with the security and GitHub-integration areas weighted as highest-risk.

EXIT_RECOMMENDATION: CONTINUE
