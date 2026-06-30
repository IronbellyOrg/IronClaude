---
Date: 2026-06-11
Scenario: A
Tier: heavyweight
---

# Research Notes: PR Auto-Remediation V2.0

> **Driving spec (force-bound, authoritative):**
> `.dev/brainstorms/20260611-005638-pr-remediation-v2-mention-bot/merged-requirements.md`
> **V1.0 lineage:** `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/{merged-requirements.md,merged-spec.md}`
>
> **Verification stance:** Every file:line anchor below was re-Read from disk during this
> research pass (2026-06-11). The headline reuse seam — `ClaudeProcess.build_env` at
> `process.py:145` — was confirmed to hard-code `os.environ.copy()` at `process.py:155`,
> and the existing `env_vars` param (`process.py:100`) merges with *override* semantics
> *after* the copy (`process.py:158-159`), so it can **add** but cannot **restrict**. The
> spec's allowlist-env requirement (PA-4) therefore needs a new seam, not the existing param.
> All four greenfield GitHub gaps were re-confirmed ABSENT in `src/` via grep.

## EXISTING_FILES

### PA-1 — GitHub Ingress & Mention Detection (greenfield; no prior art in src/)
- `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` -- the only in-repo `gh api` REST usage precedent (inline/summary PR comment posting); template for ingest call shapes, but no polling/ETag/`in_reply_to` logic exists.
- *(confirmed ABSENT in src/):* `issue_comment` polling, `in_reply_to` parent resolution, ETag/304 conditional-request cursoring — all net-new (grep returned ABSENT for `in_reply_to`, `issue_comment`).

### PA-2 — Authorization & Trust Boundary (greenfield)
- *(confirmed ABSENT in src/):* `collaborators/{login}/permission` gating (grep `collaborators/` → ABSENT). No live per-trigger permission check exists anywhere in the codebase.
- `CLAUDE.md` (project) -- fork-only `--repo IronbellyOrg/IronClaude` absolute rule; the authority/trust-boundary cultural precedent the gate must encode.

### PA-3 — Injection Containment & Sandboxing (greenfield)
- `src/superclaude/cli/pipeline/process.py:24-58` -- `_parse_prompt_max_bytes` + `PROMPT_MAX_BYTES` (16 MiB guard) and the **stdin prompt-delivery** model (`build_command` docstring `:124-125` — prompt via stdin, never argv). This is the precedent for "opComment as stdin-delivered data, never shell-interpolated."
- `src/superclaude/cli/pipeline/process.py:61-69` -- `PromptTooLargeForArgv` typed guard (length-cap precedent for the length-capped envelope).
- *(greenfield):* CONTROL/DATA envelope builder (R3) and sandbox provisioner (R4) — no envelope or sandbox-mount-restriction code exists.

### PA-4 — Headless Execution Host (reuse-dominant)
- `src/superclaude/cli/pipeline/process.py:72-119` -- **`ClaudeProcess.__init__`** (PRIMARY REUSE ANCHOR R2). Note `env_vars: dict[str,str] | None` param at `:100` and `tool_write_mode` at `:101`.
- `src/superclaude/cli/pipeline/process.py:121-143` -- `build_command()`: emits `claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns N --output-format <fmt>`; optional `--model` at `:140-141`; `extra_args` appended `:142`.
- `src/superclaude/cli/pipeline/process.py:145-160` -- **`build_env()`** (THE REUSE SEAM). Hard-codes `os.environ.copy()` at `:155`, pops `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` (`:156-157`), then `env.update(env_vars)` at `:158-159` (override-merge — additive only). **This is where the Runner allowlist must intervene; current code leaks the full host env including `GH_TOKEN`.**
- `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/process.py`, `src/superclaude/cli/eval/claude_process.py` -- the 3 existing `env_vars=` callers (grep-confirmed) establishing the merge pattern; precedent that env injection is an accepted extension point.
- `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md:63-101` -- 5-tier severity-remap algorithm (category floors/ceilings, confidence/diff-locality adjustments) — reused by S1 for severity→action routing.

### PA-5 — Autonomy, Idempotency & Loop-Safety (greenfield logic, swarm prior art)
- `src/superclaude/cli/swarm/commands.py:2266-2271` -- **bounded-counter idiom** (`iterations += 1`; `if watch_max_iterations is not None and iterations >= watch_max_iterations: break`) and terminal-state break (`phase=<TERMINAL_STATE_VALUE>`) — the model for the per-PR round/push-budget counter.
- `src/superclaude/cli/swarm/state.py:143-175` -- **atomic-write ledger precedent**: tmp-sibling + `os.replace(tmp, target)` at `:173-175` (NFR-002 atomicity contract, `:14-22`). Direct model for the two-phase JSONL ledger's durability, though the two-phase intent/outcome RESUME semantics are net-new.
- *(greenfield):* two-phase intent/outcome JSONL ledger, per-PR push budget, exact-SHA round correlation, autonomy lattice (`propose < patch < fix < push < resolve`) — none exist.

### PA-6 — Mutation, Reply & Resolve (greenfield)
- *(confirmed ABSENT in src/):* `resolveReviewThread` GraphQL mutation (grep → ABSENT), `comments/.../replies` reply endpoint (grep → ABSENT). Reply-to-thread and resolve are entirely net-new.
- `CLAUDE.md` -- mandatory `gh ... --repo IronbellyOrg/IronClaude` shape; the H5 wrapper must inject this unconditionally on every `gh` invocation.

### PA-7 — Secrets, Deploy, Audit & Observability (greenfield)
- *(greenfield):* `deploy/` directory does **not exist** (ls → No such file or directory). `deploy/remediate-bot/` systemd units + sandbox image are net-new (S2).
- `~/.aienv` (proxy contract, per memory `feedback_aienv_only_proxy_contract`) -- chmod-600 `EnvironmentFile=` precedent; Anthropic/proxy auth source for the Runner only.

### Wiring / Cross-Cutting Anchors
- `src/superclaude/cli/main.py:400-438` -- **deferred-registration pattern**: each group does `from superclaude.cli.<group> import <group>` (E402/I001-suppressed) then `main.add_command(<group>, name="<group>")`. The `remediate` group registers identically. Confirmed groups today: sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval, swarm, recommend, init-lite.
- `src/superclaude/cli/prd/` (18 modules) and `src/superclaude/cli/swarm/` (state/dispatch/transports/recipes/...) -- **multi-module CLI-group precedents** for structuring the Dispatcher/Runner split as sibling modules under `cli/remediate/`.
- `tests/cli/test_cli_registration.py` (5,330 bytes, exists) -- registration-test precedent; net-new `tests/cli/remediate/` (ABSENT today) is the test home (T1).
- `remediation/` (top-level) -- **empty dir** (only `.`/`..`); NOT the feature source home. Source belongs under `src/superclaude/cli/remediate/`. **Flag for user clarification** (see AMBIGUITIES).

## PATTERNS_AND_CONVENTIONS

- **CLI group = deferred import + `main.add_command(group, name=...)`** (`main.py:400-438`). All 10 existing groups follow this; circular-import avoidance is why imports sit at module bottom with `# noqa: E402,I001`. The `remediate` group must follow it verbatim.
- **`claude -p` host = `ClaudeProcess`** (`process.py:72`). Subprocess via `Popen` + process groups (`os.setpgrp`) for whole-tree kill; stdout/stderr redirected to files; lifecycle hooks `on_spawn/on_signal/on_exit`. 18+ callers across sprint/roadmap/prd/eval/swarm establish this as THE established headless pattern — Runner reuses it.
- **Prompt delivery is stdin, never argv** (`process.py:124-125`, comment referencing commit `4799719`). MAX_ARG_STRLEN (128 KB) no longer applies. This is the mechanical foundation for "opComment delivered as stdin data inside a CONTROL envelope, never shell-interpolated" (PA-3).
- **Env injection is additive-merge, post-copy** (`process.py:155-159`). `os.environ.copy()` → pop nested-session vars → `env.update(env_vars)`. **Convention gap:** there is no "start from empty + allowlist" mode. The Runner allowlist (PA-4/AC-3 "no `GH_TOKEN` in Runner") requires extending this seam (new param e.g. `env_mode="allowlist"` or `base_env={}`), NOT just passing `env_vars`.
- **Atomic state writes = tmp-sibling + `os.replace`** (`swarm/state.py:173-175`). NFR-002 contract: every write goes to `path + ".tmp"` then atomic rename so concurrent readers never see a torn file. The two-phase ledger inherits this durability idiom; adds `O_APPEND`/flock for the append-only JSONL (spec §10), which swarm's whole-file-replace does not cover.
- **Bounded-counter loop-guard** (`swarm/commands.py:2266-2271`). `iterations` counter + `watch_max_iterations` ceiling + terminal-state-string break. Model for round-count + push-budget short-circuit (spec §9/§10).
- **Severity-remap is table-driven** (`severity-rubric.md:63-101`): category floor/ceiling → confidence adjustment → diff-locality adjustment → cross-source agreement. S1 reuses this to map findings to `/sc:troubleshoot` action tiers (spec §17).
- **Fork-only `gh`** (`CLAUDE.md`): every `gh` call carries `--repo IronbellyOrg/IronClaude`. H5 must make this structurally unbypassable (wrapper that injects unconditionally).
- **SoT/sync-dev** (`CLAUDE.md`): source under `src/superclaude/`, never edit/stage `.claude/` (except `settings.json`). Skill changes (if any) flow `src/ → make sync-dev`.
- **UV-only, ruff** (`CLAUDE.md` + memory `reference_make_lint_vs_ci_ruff_format`): `make lint` = `ruff check` only; CI also runs `ruff format --check src/ tests/`. New code must pass both.

## FEATURE_ANALYSIS

User-facing features, each tied to spec evidence and the component inventory (D/R/H/S IDs):

1. **Mention-triggered remediation** — a human collaborator replies `@bot <directive>` to a PR review comment; the bot detects, authorizes, remediates, replies, and (optionally) resolves the thread. *Evidence:* spec §1/§3/§4; PA-1 grammar parser (D4), parent resolver (D6). The `@bot` trigger grammar is a whitelist (D4), not free-form NL.
2. **Live, per-trigger authorization gate** — only a live event `sender` with `admin|write` collaborator permission (and `type == User`) can authorize; re-checked before every dangerous action. *Evidence:* spec §5; D5. Defends spoofed login, edited mention/parent, fork author, TOCTOU.
3. **Conservative propose-only default** — autonomy lattice `propose < patch < fix < push < resolve`; effective level = lattice-min(parsed-flag, authz, validation); default `propose`. *Evidence:* spec §8; H2. V1.0 lineage FR-4.4 `needs_human_decision`.
4. **Injection-contained agent execution** — `opComment` treated as untrusted DATA inside a trusted CONTROL prompt envelope, JSON-encoded, length-capped, stdin-delivered; runs in a non-root ephemeral sandbox with no host-home/`.aienv`/`/config/.claude`/Docker-socket/SSH mounts and deny-by-default egress. *Evidence:* spec §6/§7; R3/R4; stdin precedent `process.py:124-125`.
5. **Secret-separated push** — Runner gets only minimal Claude/proxy auth (no `GH_TOKEN`); host-side Dispatcher performs git push with a short-lived per-trigger repo+branch-scoped token. *Evidence:* spec §7/§11; H3; reuse seam `process.py:145-160`.
6. **Idempotent, loop-safe operation** — two-phase intent/outcome JSONL ledger (intent-without-outcome ⇒ RESUME), per-PR push budget, exact-SHA round correlation prevent double-push and infinite loops. *Evidence:* spec §8/§9/§10; H1; swarm idioms `state.py:173-175`, `commands.py:2266-2271`.
7. **Thread reply + resolve** — bot replies to the originating review thread (`pulls/<N>/comments/<id>/replies`) and resolves it via GraphQL `resolveReviewThread`, matched on `databaseId` (not node id) with pagination. *Evidence:* spec §3/§12; H4 (greenfield, grep-confirmed absent).
8. **Production daemon + observability** — systemd-supervised Dispatcher (`Restart=always`, `WatchdogSec`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`), append-only per-trigger audit JSONL, secret redaction (`TOKEN|KEY|AUTH|SECRET` masking + `sys.excepthook` stripping), rate-limit safety (≥30s poll, `Retry-After`, backoff), and alerts (`RemediationLoopDetected`, `AuthzFailureSpike`). *Evidence:* spec §11/§13/§14/§15; S2.

## RECOMMENDED_OUTPUTS

The PRD pipeline (post-research) should produce:

1. **`prd.md`** — the heavyweight PRD itself: problem/vision, personas (repo maintainer / on-call reviewer), the 7 functional areas (PA-1..PA-7) as FR sections, NFRs (security, isolation, durability, rate-limit), acceptance criteria AC-1..AC-9 (mapped from spec §16), the autonomy lattice + HALT semantics, and the 4 open decisions OD-1..OD-4 surfaced as explicit PRD open questions.
2. **Component inventory table** — D1–D6 (Dispatcher), R1–R4 (Runner), H1–H5 (host-side), S1–S2 (severity/deploy), each with reuse-vs-build classification and the verified anchor (e.g. R2 → `process.py:72`).
3. **Trust-boundary / threat-model section** — the bypass-defense matrix (spoofed login, edited mention/parent, fork author, TOCTOU) and the secret-separation three-way split, mapped to AC-1/AC-3/AC-7/AC-9.
4. **Reuse-seam delta note** — precise statement that `build_env` (`process.py:145`) must gain an allowlist mode; the additive-only `env_vars` param is insufficient for AC-3.
5. **Build-sequencing appendix** — ordered phase plan from spec §19 (probe-first GitHub validation, then Dispatcher skeleton, ledger, authz, Runner+envelope, sandbox, push/reply/resolve, deploy hardening).
6. **Open-questions register** — OD-1 (sandbox tech), OD-2 (push-token mechanism), OD-3 (push-budget default), OD-4 (`patch` level semantics) + the `remediation/` vs `cli/remediate/` source-home clarification.
7. **(Downstream handoff)** — the PRD should be TDD-ready: clear seams for `superclaude roadmap`/`tasklist` so the split-host decomposition maps onto a sprint plan.

## SUGGESTED_PHASES

Heavyweight tier → **7 codebase agents + 3 web agents = 10 total**. The six product-area
codebase agents mirror the scope-discovery RAs; a seventh isolates the highest-risk reuse
seam (env allowlist) because a wrong call there breaks AC-3. Three web agents resolve the
two residual open decisions (OD-1, OD-2) and the net-new GitHub API surface.

### Codebase agents

1. **Topic:** Security & trust-boundary — authorization gate (live `sender`, `admin|write`, re-check-before-dangerous-action), injection containment (opComment-as-data, envelope, no shell interpolation), sandbox isolation (no host mounts, deny-by-default egress), secret three-way separation. Verify the spec's safety invariants are buildable & complete vs AC-1/AC-3/AC-7/AC-9.
   - **Agent type:** Architecture Analyst (security lens)
   - **Files:** spec §5/§6/§7/§11; `src/superclaude/cli/pipeline/process.py:145-160` (env handling), `:124-125` (stdin); `CLAUDE.md` (secret + fork rules); `~/.aienv` contract (memory `feedback_aienv_only_proxy_contract`); V1.0 `merged-spec.md` (`needs_human_decision` lineage).
   - **Output path:** `research/01-security-trust-boundary.md`

2. **Topic:** GitHub API integration mapping — REST ingest (`pulls/comments?since=&sort=created`, ETag/304 cursoring), `in_reply_to_id` parent resolution, collaborator-permission gate, reply endpoint (`pulls/<N>/comments/<id>/replies`), GraphQL `resolveReviewThread` + `databaseId` thread matching with pagination, rate-limit/`Retry-After`. Confirm §19.1 probe-first requirement.
   - **Agent type:** Integration Mapper
   - **Files:** spec §3/§4/§12/§13; `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (`gh api` precedent); grep-confirmed-absent endpoints.
   - **Output path:** `research/02-github-api-integration.md`

3. **Topic:** Headless execution reuse seam — extend `ClaudeProcess` with an allowlist-env mode; prompt-envelope construction; `--max-turns`/`--output-format` tuning; severity→action routing; model routing via `~/.aienv`. **Must produce the concrete `build_env` extension design** (new param vs base_env override).
   - **Agent type:** Feature Analyst
   - **Files:** `src/superclaude/cli/pipeline/process.py:72-160`; callers `sprint/executor.py`, `sprint/process.py`, `eval/claude_process.py`; `severity-rubric.md:63-101`; spec §7/§17.
   - **Output path:** `research/03-headless-execution-reuse-seam.md`

4. **Topic:** State, idempotency & loop-safety — two-phase intent/outcome JSONL ledger, RESUME semantics, per-PR push budget, exact-SHA round correlation, atomic-write + `O_APPEND`/flock durability vs AC-5/AC-6.
   - **Agent type:** Architecture Analyst
   - **Files:** spec §8/§9/§10; `src/superclaude/cli/swarm/state.py:143-175` (atomic write), `src/superclaude/cli/swarm/commands.py:2266-2271` (bounded counter); memory `reference_sprint_rerun_tasks`.
   - **Output path:** `research/04-state-idempotency-loop-safety.md`

5. **Topic:** Split-host architecture & control flow — Dispatcher/Runner decomposition, component inventory D1–H5/R1–R4/S1–S2, §3 control-flow ordering, CLI-group wiring, §19 build sequencing.
   - **Agent type:** Architecture Analyst
   - **Files:** spec §1/§2/§3/§19/§21; `src/superclaude/cli/main.py:400-438` (deferred registration); `src/superclaude/cli/prd/` & `src/superclaude/cli/swarm/` (multi-module group precedents); `tests/cli/test_cli_registration.py`.
   - **Output path:** `research/05-split-host-architecture.md`

6. **Topic:** Deploy, ops & observability — systemd hardening (`Restart=always`, `WatchdogSec`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`), Runner sandbox image (OD-1), three-way secret sourcing, audit-log schema (§14), rate-limit/backoff, alerting, rollback/replay.
   - **Agent type:** Integration Mapper (DevOps lens)
   - **Files:** spec §11/§13/§14/§15; absent `deploy/` dir (greenfield S2); `~/.aienv`/`ccsession.env` chmod-600 precedent; `CLAUDE.md` UV/sync-dev constraints.
   - **Output path:** `research/06-deploy-ops-observability.md`

7. **Topic:** Reuse-seam env-allowlist deep-dive — exhaustively trace what `os.environ` contains in the Dispatcher context, which vars (`GH_TOKEN`, push creds, `.aienv` proxy auth) must/must-not cross into the Runner, and design the minimal `build_env` change + a regression test that asserts `GH_TOKEN ∉ runner_env`. Highest-risk reuse delta for AC-3.
   - **Agent type:** Feature Analyst
   - **Files:** `src/superclaude/cli/pipeline/process.py:145-160`; all `env_vars=` callers (`sprint/executor.py`, `sprint/process.py`, `eval/claude_process.py`, `pipeline/process.py`); `~/.aienv` var inventory; spec §7/§11.
   - **Output path:** `research/07-env-allowlist-deep-dive.md`

### Web agents

8. **Topic:** GitHub REST + GraphQL reference for the exact surfaces — review-comment threading & `in_reply_to_id`, `pulls/{n}/comments/{id}/replies`, `resolveReviewThread` mutation, `reviewThreads { databaseId }` pagination, `collaborators/{user}/permission` response shape, ETag/`If-None-Match` 304 semantics, secondary-rate-limit/`Retry-After` behavior. Resolve node-id-vs-databaseId correctly.
   - **Agent type:** Doc Analyst (web)
   - **Files:** GitHub REST & GraphQL docs (prefer Context7 `gh`/GitHub API; fall back to docs.github.com). Cross-check against spec §12.
   - **Output path:** `research/08-web-github-api-reference.md`

9. **Topic:** Sandbox isolation tech for OD-1 — rootless Docker vs Podman vs Firecracker microVM for an ephemeral, non-root, no-host-mount, deny-egress-by-default per-trigger runner on a single on-prem host. Trade-offs: isolation strength vs ops simplicity, egress-allowlist mechanism, startup latency, root-daemon footprint.
   - **Agent type:** Integration Mapper (web/DevOps)
   - **Files:** Podman/Firecracker/rootless-Docker docs + security guidance; map to spec §6/§7/§15 isolation requirements.
   - **Output path:** `research/09-web-sandbox-isolation-od1.md`

10. **Topic:** Short-lived GitHub push-token mechanism for OD-2 — GitHub App installation tokens (repo+permission-scoped, ~1h TTL) vs fine-grained PATs; how to mint a per-trigger repo+branch-scoped token host-side without exposing it to the Runner; rotation/revocation. Also survey untrusted-input-in-LLM-prompt containment best practices to validate the §6 envelope design.
   - **Agent type:** Doc Analyst (web, security lens)
   - **Files:** GitHub Apps / fine-grained-PAT docs; OWASP/industry LLM prompt-injection guidance; map to spec §7/§11 and OD-2.
   - **Output path:** `research/10-web-push-token-and-injection-od2.md`

## TEMPLATE_NOTES

- **Threat model / security section needs first-class treatment** — this product's reason-for-existing is "run a write+push-capable LLM on untrusted comment text." The PRD's security/NFR section is not boilerplate; it carries the bypass-defense matrix and the three-way secret split. `base_variant = sonnet:security` confirms this is the weighted area.
- **Autonomy lattice + HALT semantics need a dedicated FR + a state diagram** — the `propose<patch<fix<push<resolve` lattice, lattice-min effective-level computation, and off-lattice HALT short-circuits (`needs_human_decision`, `pr_push_budget==0`) are subtle; a default-to-propose narrative plus a worked example prevents the V1.0-class drift the reflect memory warns about (`needs_human_decision` must HALT, never auto-default — memory `feedback_human_decision_items_must_halt`).
- **Open-questions section must carry OD-1..OD-4 explicitly** — sandbox tech, push-token mechanism, push-budget default, `patch`-level semantics are genuinely unresolved and decision-shaping; do not let the PRD paper over them with a default.
- **Acceptance-criteria traceability** — map AC-1..AC-9 (spec §16: 4 HIGH / 10 MEDIUM adversarial resolutions) to FRs so the downstream TDD/roadmap can gate on them.
- **Reuse-vs-build column in the component table** — only R2 (`ClaudeProcess`) and S1 (severity rubric) are true reuse; everything else is greenfield. Flag this so the roadmap doesn't under-estimate build cost.
- **Idempotency/ledger needs a schema block** — two-phase intent/outcome record fields, the RESUME rule (intent-without-outcome), and the per-PR push-budget counter belong in a concrete JSONL schema, not prose.
- **Non-goals** — webhooks (deferred to polling per spec §1), multi-repo (fork-only `IronbellyOrg/IronClaude`), and any V1.0 in-session Monitor-host behavior should be explicit non-goals.

## AMBIGUITIES_FOR_USER

1. **Source home: `remediation/` (empty top-level dir) vs `src/superclaude/cli/remediate/`?** An empty `remediation/` dir exists at repo root (verified: only `.`/`..`). Scope discovery recommends source under `src/superclaude/cli/remediate/` (consistent with all 10 existing CLI groups + SoT discipline). Confirm the empty `remediation/` is a stale placeholder to ignore/remove, and that the feature lives under `cli/remediate/`.
2. **OD-1 — sandbox technology:** rootless container (Docker/Podman) or Firecracker microVM? Drives the isolation-strength-vs-ops-simplicity trade-off and the egress-allowlist mechanism. Web agent 9 will inform, but the final call is the user's (on-prem ops constraints).
3. **OD-2 — push-token mechanism:** GitHub App installation token or fine-grained PAT for the short-lived host-side push credential? Affects the secret-sourcing model and rotation story.
4. **OD-3 — per-PR push-budget default:** what numeric default (e.g. 1, 3, unbounded-with-alert) for `pr_push_budget`? Determines when the loop-safety HALT fires.
5. **OD-4 — `patch` autonomy level semantics:** the lattice includes `patch` between `propose` and `fix`; the spec leaves its exact behavior (propose-a-diff-without-applying? apply-but-don't-push?) under-specified. Confirm the intended meaning so the autonomy gate encodes it correctly.
6. **`base_variant` confirmation:** scope discovery cites `base_variant = sonnet:security` for the dominant-risk framing. Confirm the security-weighted lens is the intended PRD posture (vs a balanced systems-design lens).

EXIT_RECOMMENDATION: CONTINUE
