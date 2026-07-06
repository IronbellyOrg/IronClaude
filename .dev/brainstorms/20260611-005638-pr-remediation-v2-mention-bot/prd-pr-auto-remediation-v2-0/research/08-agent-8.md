# Research: Investigation topic 8 (research-notes did not contain an Agent 8 block — investigate broadly using the planning inputs).

**Investigation type:** Investigator
**Scope:** Broad gap-fill across planning inputs (merged-requirements, seed-brief, research-notes, scope-discovery) + the reusable code surfaces the PRD depends on (ClaudeProcess, swarm counter, gh wrappers, severity rubric).
**Status:** Complete
**Date:** 2026-06-11

---

## 0. Orienting note — why this agent exists

The research-notes `SUGGESTED_PHASES` block planned 10 agents; agents **1–7** are codebase
analysts and **8–10** are *web* doc analysts (8 = GitHub REST/GraphQL reference, 9 = sandbox
tech for OD-1, 10 = push-token + injection for OD-2). The orchestrator did not emit a discrete
"Agent 8 block" for a codebase investigator, so this slot is routed as a **broad Investigator**.

Rather than re-run a web doc-survey (which the spec already partially internalised in §4/§12/§13)
or duplicate agents 1–7, the highest-value contribution here is to **independently code-verify the
load-bearing reuse/greenfield claims the entire PRD rests on**. If any of these anchors is wrong,
the PRD's "reuse-dominant" framing and build-cost estimate are wrong. Everything below was
re-Read from disk on 2026-06-11. The product surface is the `superclaude` CLI; this feature adds
a `remediate` command group + a deploy story.

---

## 1. Load-bearing reuse anchors — independently CODE-VERIFIED

### R2 / PA-4 — `ClaudeProcess` headless spawn primitive

**[CODE-VERIFIED]** `src/superclaude/cli/pipeline/process.py:72` — `class ClaudeProcess`. This is
the single most-cited reuse anchor (the Runner's executor wraps it). Confirmed capabilities:

- **Constructor** (`:85-119`) is keyword-only, with exactly the knobs the spec needs:
  `prompt`, `output_file`, `error_file`, `max_turns=100`, `model=""`,
  `permission_flag="--dangerously-skip-permissions"` (default!), `timeout_seconds=6300`,
  `output_format="stream-json"`, `extra_args`, three lifecycle hooks, `env_vars`, `tool_write_mode`.
- **`build_command()`** (`:121-143`) **[CODE-VERIFIED]** emits exactly what the spec §7 quotes:
  `claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default
  --max-turns N --output-format <fmt>`, then optional `--model`, then `extra_args`. The spec's §7
  command string is accurate to the byte.
- **Stdin prompt delivery** **[CODE-VERIFIED]** `:124-125` docstring + `:205-210` `_write_prompt_to_stdin`
  via `os.write` with EINTR retry + chunked 64 KiB writes (`:218`). Prompt is **never** an argv value.
  This is the mechanical foundation for spec §6 "opComment delivered as stdin DATA, never
  shell-interpolated." The claim is real and robust (chunked, deadlock-safe, BrokenPipe-captured).
- **16 MiB prompt guard** **[CODE-VERIFIED]** `PROMPT_MAX_BYTES` (`:56`) + `PromptTooLargeForArgv`
  (`:61`) raised at `:169-173` before any handle/process is created. The envelope's length-cap (spec §6)
  has a pre-existing enforcement point to lean on.

### THE REUSE SEAM — `build_env()` is additive-only (the spec's #1 correctness dependency)

**[CODE-VERIFIED — and this is the critical finding]** `process.py:145-160`:

```python
def build_env(self, *, env_vars=None):
    env = os.environ.copy()          # :155  <-- starts from FULL host env
    env.pop("CLAUDECODE", None)      # :156
    env.pop("CLAUDE_CODE_ENTRYPOINT", None)
    if env_vars:
        env.update(env_vars)         # :158-159  <-- override-MERGE (additive only)
    return env
```

And **[CODE-VERIFIED]** `start()` wires it at `:187`:
`"env": self.build_env(env_vars=self._extra_env_vars)` — where `self._extra_env_vars` is the
constructor's `env_vars` (`:115`). **There is no code path that starts from an empty base env.**

**Consequence for the PRD (high-confidence):** the spec's INV-001 / SC-7 / AC-3 requirement —
"the Runner env contains **no** `GH_TOKEN` / push credential" — **cannot be met by passing
`env_vars`**. `env_vars` can only *add/override*, never *subtract*, and the base is the
Dispatcher's full `os.environ` (which, per the split-host design, holds the read+comment GH
credential and possibly more). The PRD must specify a **new seam** on `build_env` — e.g.
`base_env: dict | None = None` (default `os.environ.copy()`, allowlist callers pass `{}` +
explicit allowlist) or an `env_mode="allowlist"` flag. This matches research-notes line 67 and
spec §7, but I am stating it as an independently verified, load-bearing PRD requirement, not an
inherited assertion. **This is the single highest-risk reuse delta in the whole feature.**

### PA-5 — swarm bounded-counter idiom (round/push-budget model)

**[CODE-VERIFIED]** `src/superclaude/cli/swarm/commands.py:2268-2269`:
`iterations += 1` then `if watch_max_iterations is not None and iterations >= watch_max_iterations: break`.
Spec §9 cites `:2269` — **exact match**. Also a terminal-state break (`if "phase=" + TERMINAL_STATE_VALUE
in line: break`, `:2265`). This is a sound model for the monotonic per-PR round/push counter, but
note it is an **in-memory loop counter**, not disk-authoritative — the spec correctly upgrades it to
a disk-backed ledger (the swarm idiom supplies the *shape*, not the durability).

### PA-5 — swarm atomic-write ledger precedent

**[CODE-VERIFIED]** `src/superclaude/cli/swarm/state.py` `write_state`:
`tmp = target.with_suffix(target.suffix + ".tmp"); tmp.write_text(payload); os.replace(tmp, target)`.
Atomic whole-file replace via temp-sibling + `os.replace`. **[CODE-CONTRADICTED — nuance]** this is
**whole-file JSON replace**, NOT append-only JSONL. The spec's §10 two-phase ledger needs
`O_APPEND` + `flock` for append-only intent/outcome records; swarm's idiom gives durability for
*snapshot* state but does **not** cover the append-only concurrency model. The PRD must flag the
ledger as **greenfield with a borrowed atomicity idiom**, not a drop-in reuse. (Also note
`confine_path` / `OutputConfinementError` here — a path-confinement precedent the ledger's state-dir
writes could reuse.)

### PA-4 — severity rubric reuse (S1)

**[CODE-VERIFIED]** `sc-auggie-review-protocol/refs/severity-rubric.md:63` — "Severity-remap
algorithm (applied in Wave 3)": start from Auggie hint → category floor/ceiling table → (per
research-notes) confidence + diff-locality adjustments. Real and table-driven; S1's
severity→`/sc:troubleshoot`-tier routing (spec §17) can reuse it directly.

### Wiring — deferred CLI-group registration

**[CODE-VERIFIED]** `src/superclaude/cli/main.py:400-438` — every group uses the
`from superclaude.cli.<g> import <g>  # noqa: E402,I001` + `main.add_command(<g>, name="<g>")`
idiom. Confirmed live groups: sprint, roadmap, cleanup-audit, tasklist, cli_portify, prd, eval,
swarm, recommend, init-lite (10). The `remediate` group registers identically.
**[Minor anomaly]** `cli_portify` calls `main.add_command(cli_portify_group)` **without** `name=`
(relies on the group's own declared name) — a small inconsistency; the PRD should pin
`name="remediate"` explicitly to match the majority pattern and keep `superclaude remediate`
discoverable.

**Key Takeaways**
- Every reuse anchor the PRD cites is real and at the cited line — the "reuse-dominant for
  execution" framing holds for R2 (ClaudeProcess) and S1 (severity rubric).
- **The env-allowlist seam is the load-bearing exception:** `build_env` is structurally
  additive-only; AC-3 forces a *new* parameter, not reuse of `env_vars`. Treat as a first-class
  PRD requirement + a named regression test (`assert "GH_TOKEN" not in runner_env`).
- The swarm counter (shape) and atomic-write (durability) are *idioms to borrow*, not
  drop-in components; the two-phase append-only ledger is genuinely greenfield.

---

## 2. Greenfield gaps — independently CONFIRMED ABSENT in `src/`

Grep over `src/` (2026-06-11) returned **zero hits** for all four claimed greenfield surfaces —
the spec's "must build" framing is accurate:

| Surface | Grep target | Result | Component |
|---|---|---|---|
| Review-comment parent resolution | `in_reply_to` | **ABSENT** | D6 |
| Thread resolve | `resolveReviewThread` (case-insensitive) | **ABSENT** | H4 |
| Authorization gate | `collaborators/` | **ABSENT** | D5 |
| Thread reply | `/replies` | **ABSENT** | H4 |

Source homes **[CODE-VERIFIED]**:
- `remediation/` (top-level) — **exists but empty** (`ls` → only `.`/`..`). Confirms
  research-notes AMBIGUITY #1: it is a stale placeholder, not the feature home.
- `src/superclaude/cli/remediate/` — **ABSENT** (the spec's intended SoT home; to be created).
- `deploy/` — **ABSENT** (S2 systemd units + sandbox image are fully greenfield).

The only in-repo `gh api` REST precedent is **[CODE-VERIFIED]**
`sc-auggie-review-protocol/SKILL.md:307` (`gh api repos/<owner>/<repo>/pulls/<PR>/comments`) —
inline/summary posting only; no polling, threading, or resolve. H4's reply+resolve endpoints have
**no** prior art and carry the most GitHub-API-shape risk (this is exactly what planned web-agents
8/10 are meant to de-risk; the §19.1 probe-first gate is non-optional for these).

**Key Takeaways**
- All four "must build" claims hold; the PRD's reuse-vs-build column should mark D5/D6/H4 (and the
  whole `deploy/` tree) as **greenfield with no in-repo prior art**.
- The empty `remediation/` dir is a trap — the PRD should explicitly state the feature lives under
  `cli/remediate/` and recommend deleting/ignoring `remediation/`.

---

## 3. Product surface & user flow (synthesised, spec-grounded)

**Who/what the product is:** a `superclaude remediate` CLI group running headless **outside** any
Claude session, as an on-prem systemd service. It is not a skill, not a slash command — it
*spawns* `claude -p`, mirroring `sprint`/`swarm`/`pipeline`. The end user is a **repo maintainer /
on-call reviewer** on the `IronbellyOrg/IronClaude` fork.

**The one user flow that matters (happy path):**
1. Augment (or a human) leaves a PR **review comment** flagging an issue.
2. An authorized collaborator **replies** to that comment: `@bot fix --depth deep`.
3. Dispatcher (polling ≤30–60s) sees the mention, runs the **live authz gate** on the *replier*,
   claims the trigger in the ledger, resolves the **parent** comment as `opComment`, parses the
   whitelisted flags.
4. A one-shot sandboxed Runner checks out PR-head, runs `/sc:troubleshoot` against
   `OP_COMMENT_JSON.body` (as DATA), validates, emits a diff (propose) or a sandbox-branch commit (fix).
5. Dispatcher pushes host-side with a short-lived token, replies to the thread with the summary +
   SHA, and (at `resolve` level) resolves the thread.

**The control surface the user actually touches** is the **@-mention grammar** (D4): a tiny
whitelist — autonomy level (`propose|patch|fix|push|resolve`), `--depth`, `--scope`, `--rounds`.
Everything else is config/operator-set. **Default with no flag = `propose`** (safest). This is the
entire UX: one comment, a few whitelisted tokens.

**Critical UX safety property:** the *replier* is the sole authority; the *parent author* supplies
only data. A `read`-permission user mentioning the bot gets a polite ack-reject, zero action (AC-1).

**Key Takeaways**
- The product's "interface" is a 4-token comment grammar + a systemd service; there is no GUI,
  no web surface, no new slash command for end users.
- The conservative default (propose-only) is the dominant UX decision — it must be impossible to
  reach `push` without an explicit flag AND write-permission AND passing validation (lattice-min).

---

## 4. Integration opportunities & touchpoints

- **`offer-pr-review.sh` hook** **[CODE-VERIFIED, refines seed-brief]** — exists at
  `src/superclaude/hooks/scripts/offer-pr-review.sh` (canonical) and is **registered project-local
  in `.claude/settings.json`** as a PostToolUse Bash hook. The seed-brief's "not wired into
  hooks.json" is precise only about the **distributable** `src/superclaude/hooks/hooks.json` (where
  it is indeed absent — a known SoT drift flagged in `.dev/reviews/pr-67-.../auggie-parsed-C.json`).
  *Integration opportunity:* V2.0 could surface the mention-trigger path via this existing
  PR-review-offer touchpoint, but the PRD should **not** depend on it being distributed until the
  hooks.json drift is reconciled. Low priority; note as optional.
- **Severity rubric decision-mode** **[CODE-VERIFIED]** `severity-rubric.md` "Decision-mode summary":
  explicitly states the verdict "does NOT translate into a `gh pr review --approve` or
  `--request-changes` — those decisions belong to the human." This **directly reinforces** spec §20
  non-goal ("Modifying merge state — humans merge"). The PRD can cite this as an *existing,
  code-enforced cultural invariant*, not a new rule it invents.
- **CLI-group siblings** — `cli/prd/` (18 modules) and `cli/swarm/` are the structural template for
  decomposing Dispatcher (D1–D6) / Runner (R1–R4) / host-side (H1–H5) into sibling modules under
  `cli/remediate/`. The registration test home is `tests/cli/remediate/` (ABSENT today; mirror
  `tests/cli/test_cli_registration.py`).
- **`~/.aienv` proxy contract** (per memory `feedback_aienv_only_proxy_contract`) — the Runner's
  Anthropic auth must come from the `:4000/cli` proxy base + `T2Model*` model ids only; this is the
  **only** credential class allowed into the sandbox env (everything GitHub stays host-side).

---

## 5. Edge cases & divergences worth flagging to the PRD

- **Seed-brief vs merged-requirements injection model [CODE-CONTRADICTED — important evolution].**
  The seed-brief (line 21, 32) describes the execution primitive literally as
  `/sc:troubleshoot "${opComment}" --depth deep --fix` — i.e. **shell-interpolating** opComment.
  The adversarial merge **hardened this away**: merged-requirements §6 states opComment is
  *"**never** interpolated as `/sc:troubleshoot \"${opComment}\"`"* and is instead JSON-encoded in a
  CONTROL/DATA envelope delivered via stdin. **The PRD MUST use the §6 envelope form**, never the
  seed-brief's literal interpolation — citing the seed verbatim would re-introduce the exact
  injection vuln (SC-2/AC-3) the design exists to prevent. This is the clearest example of the
  spec evolving past its own seed; the PRD writer should not regress to the seed's phrasing.
- **`permission_flag` defaults to `--dangerously-skip-permissions`** **[CODE-VERIFIED]**
  (`process.py:93`). Spec §6 says this is acceptable *only inside the sandbox*. Since it is the
  **default**, the Runner inherits it for free — but the PRD must make explicit that this default is
  only safe **because** of the sandbox boundary (no host mounts, deny-egress); outside that boundary
  the same default would be dangerous. The safety is in the sandbox, not the flag.
- **In-memory vs disk-authoritative counter.** The swarm counter resets on restart; the spec's
  SC-5/SC-6 require survival across restarts. The PRD must state the ledger is the SoT and the
  counter is derived from it on startup (not the reverse).
- **`cli_portify` registration omits `name=`** — minor; pin `name="remediate"` explicitly.

---

## Gaps and Questions

1. **Env-allowlist seam design is the #1 open implementation gap.** `build_env` is additive-only
   (verified §1). The PRD must specify the new seam (`base_env={}` vs `env_mode="allowlist"`) AND a
   regression test asserting `GH_TOKEN`/push-token ∉ Runner env (AC-3/AC-7). Without this, the
   feature's central safety claim is unbuildable on the cited reuse anchor.
2. **`remediation/` (empty) vs `cli/remediate/` (absent) source home** — needs explicit user
   confirmation (research-notes AMBIGUITY #1). Recommend: feature → `cli/remediate/`; delete the
   stale `remediation/`.
3. **OD-1 sandbox tech** (container vs Firecracker), **OD-2 push-token** (App vs fine-grained PAT),
   **OD-3 push-budget default** (2? confirm vs real Augment re-review cadence in the §19.1 probe),
   **OD-4 `patch` level semantics** — all genuinely unresolved; the PRD must carry them as explicit
   open questions, not paper over with defaults (per `feedback_human_decision_items_must_halt` and
   research-notes TEMPLATE_NOTES).
4. **Two-phase append-only ledger has no in-repo prior art for the append/flock concurrency model** —
   only the *whole-file* atomic-replace idiom exists. The PRD should budget this as greenfield and
   specify the `O_APPEND` + per-PR `flock` design + truncated-last-line replay tolerance (spec §10).
5. **H4 reply/resolve GitHub API shapes are unverified against the live API** — `databaseId` vs node
   `id`, `reviewThreads` pagination, `in_reply_to_id` reliability. The §19.1 probe-first spike
   against a throwaway fixture PR is a hard gate before parser code (web-agents 8/10 inform but do
   not replace the live probe).
6. **Distributable-hooks drift** — if V2.0 wants to use `offer-pr-review.sh` as a touchpoint, the
   `src/superclaude/hooks/hooks.json` registration gap must be reconciled first. Optional/low-pri.

## Stale Documentation Found

- **Seed-brief injection phrasing is stale relative to the merged spec.** seed-brief §"Known
  Context" + Problem Statement describe `/sc:troubleshoot "${opComment}"` (literal interpolation);
  merged-requirements §6 supersedes this with the JSON envelope. **Use §6.** [CODE-CONTRADICTED by
  the spec's own later synthesis.]
- **Seed-brief "Hook … not wired into hooks.json"** is *partially* stale: the hook IS registered in
  project-local `.claude/settings.json`; only the distributable `hooks.json` lacks it. [Refined by
  code.]
- **`build_env` docstring** (`process.py:151-153`) says `env_vars` lets callers "inject isolation
  variables … without affecting the base environment" — accurate, but it does **not** mention that
  there is no way to *restrict* the base. A reader could over-trust it as an isolation mechanism. The
  PRD's reuse-seam note should pre-empt this misreading. [CODE-VERIFIED limitation, doc-silent.]

## Summary

As the broad gap-fill Investigator, I independently **code-verified every load-bearing claim** the
PRD depends on, rather than duplicate agents 1–7 or re-survey GitHub docs. Findings:

1. **Reuse anchors are real and exact.** `ClaudeProcess` (`process.py:72`), its `build_command`
   string, stdin delivery, and 16 MiB guard all match the spec to the line. Severity rubric
   (`severity-rubric.md:63`) and the swarm counter (`commands.py:2269`) are confirmed at the cited
   lines. The "reuse-dominant for execution" framing is sound.
2. **The one load-bearing exception is the env-allowlist seam.** `build_env` (`process.py:145-160`)
   is structurally **additive-only** — `os.environ.copy()` base + `env.update(env_vars)`, no restrict
   path, wired into `start()` at `:187`. The spec's no-`GH_TOKEN`-in-Runner invariant (INV-001/SC-7/
   AC-3) **cannot** be met with the existing `env_vars` param; a **new seam is mandatory**. This is the
   single highest-risk reuse delta and must be a first-class PRD FR + regression test.
3. **All four greenfield GitHub surfaces (D5/D6/H4) confirmed ABSENT** in `src/`; `deploy/` and
   `cli/remediate/` absent; `remediation/` is an empty stale placeholder. The reuse-vs-build column
   must mark these as no-prior-art greenfield, and the §19.1 live probe is a hard gate for H4.
4. **The spec has evolved past its seed-brief** on the most safety-critical point: opComment is a
   JSON envelope (DATA), never `"${opComment}"` interpolation. The PRD must follow §6, not the seed.
5. **Existing cultural invariants reinforce the spec:** the severity rubric already forbids
   merge-state changes (matches §20 non-goal); fork-only `--repo` and SoT/sync-dev discipline are
   code+CLAUDE.md-enforced. The PRD can cite these as existing constraints, not new inventions.

Net: the PRD is well-grounded; its reuse claims survive independent verification. The two things the
PRD writer must not get wrong are (a) the **env-allowlist seam is new, not the existing param**, and
(b) **opComment is an envelope, not interpolation** — both are points where a careless reading of the
anchors or the seed would silently reintroduce the exact risks the feature exists to eliminate.
