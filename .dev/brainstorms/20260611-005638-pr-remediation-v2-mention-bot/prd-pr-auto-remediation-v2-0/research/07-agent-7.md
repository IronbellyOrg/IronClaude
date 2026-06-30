# Research: Investigation topic 7 (research-notes did not contain an Agent 7 block — investigate broadly using the planning inputs).

**Investigation type:** Investigator
**Scope:** Broad verification of the reuse foundations the V2.0 spec rests on — `ClaudeProcess` (cli/pipeline/process.py), swarm loop-guard counter (cli/swarm/commands.py), severity rubric + gh posting precedent (sc-auggie-review-protocol), env/secret-sourcing models (~/.aienv), and the V1.0 predecessor spec. The unassigned-agent value-add is validating that the spec's CODE-cited primitives actually exist and behave as claimed.
**Status:** Complete
**Date:** 2026-06-11

---

## Investigation Framing & Differentiation

This is a degenerate fan-out: Agents 1–8 all received the same "no Agent N block — investigate
broadly" mandate, and stubs 01–08 all converge on the same target (verify the spec's Reuse Map).
Rather than re-derive the same surface confirmations, **this agent goes deep on the two CODE
citations in the spec and tests them against the exact cited lines** — because the highest-value
finding in a reuse-anchored spec is a *mis-cited primitive*, which every downstream agent that
trusts the citation inherits. I found **two load-bearing contradictions** plus a secret-hygiene
mismatch that the broad agents are unlikely to surface.

**Headline findings (detail below):**
1. **`cli/swarm/commands.py:2269` is CODE-CONTRADICTED** — the spec §9 cites it as a "monotonic,
   disk-authoritative, survives-restarts" bounded counter. Line 2269 is the *opposite*: an
   in-memory `--watch` poll-iteration cap that resets every invocation.
2. **`build_env()` cannot deliver the allowlist the spec requires (INV-001/SC-7) as-is** — the
   `env_vars` parameter *merges over* `os.environ.copy()`; it cannot *exclude* inherited secrets.
   R2 reuse is therefore **not "as-is"** — it needs a code change, not a wrapper.
3. **The `~/.aienv` "chmod-600 exemplar" is actually 644** on disk — the cited secret-hygiene
   precedent does not exemplify the practice the spec attributes to it.

---

## R2 — `ClaudeProcess` (`cli/pipeline/process.py:72`) — **CODE-VERIFIED (class)**, **CODE-CONTRADICTED (env claim)**

**Existence & shape — [CODE-VERIFIED] at `src/superclaude/cli/pipeline/process.py:72`.**
The class is exactly where the spec cites it. `build_command()` (lines 121–143) emits
`claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default
--max-turns N --output-format <fmt>` — matching §7 verbatim. Prompt is delivered via **stdin**
(`_write_prompt_to_stdin`, lines 221–258, chunked 64 KiB, EINTR-retry, BrokenPipe-safe),
confirming §7's "bypasses 128KB argv limit" claim. Defaults: `max_turns=100`, `timeout_seconds=6300`
(~105 min), `permission_flag="--dangerously-skip-permissions"`, `output_format="stream-json"`.
So the spec's "propose ≈ 30 / fix ≈ 60" max_turns are **caller-set overrides**, not defaults —
correct, but the build plan must remember to pass them (the default 100 is too high for propose).

**The §7 env claim is the critical gap — [CODE-CONTRADICTED].**
Spec §7: *"`build_env()` MUST be wrapped with an explicit allowlist `env_vars` (not the current
full `os.environ.copy()`)… The Runner receives only minimal Claude auth… **No `GH_TOKEN`, no push
credential** in the Runner env (INV-001/SC-7)."*

Read `build_env()` (lines 145–160):
```python
env = os.environ.copy()           # line 155 — full inheritance
env.pop("CLAUDECODE", None)
env.pop("CLAUDE_CODE_ENTRYPOINT", None)
if env_vars:
    env.update(env_vars)          # lines 158-159 — MERGE/OVERRIDE, not REPLACE
return env
```
The `env_vars` parameter **merges over** the full inherited environment via `dict.update()`. It can
*add* or *override* keys — it **cannot remove** an inherited `GH_TOKEN` / `ANTHROPIC_*` / push token.
There is no `env_replace`, no base-allowlist, no deny-list. **Passing `env_vars` does not and cannot
produce an allowlist environment.** If the Dispatcher spawns the Runner via the current
`ClaudeProcess` and the Dispatcher process holds a push token in its own environ (which §11 says it
does — read+comment credential long-lived in the Dispatcher), that token is inherited by the Runner
**by construction**, defeating INV-001/SC-7 and failing **AC-7** (`/proc/<pid>/environ` secret-scrape).

**Consequence for the build plan:** R2 is mis-labeled **"Reuse as-is"**. It is **"Reuse + required
modification"**: `build_env()` needs either (a) a new `base_env`/`env_replace` path that starts from
`{}` (or a fixed allowlist) instead of `os.environ.copy()`, or (b) the Runner must be spawned from a
**pre-scrubbed parent process** whose environ already excludes every secret. Option (b) is the
cleaner fit for the split-host model (the sandbox is a separate process tree anyway), but the spec
does not say so — it implies the `env_vars` param suffices, which it does not. **This must land in
§19 step 5 (R2 at propose-only) as a code change, gated by AC-7, or the secret boundary is
cosmetic.** Note also: even a scrubbed env does not protect argv — but argv is already safe here
since the prompt goes via stdin (verified) and no secret is passed as a flag.

**Key Takeaways**
- `ClaudeProcess` exists exactly as cited (process.py:72); `build_command`/stdin behavior match §7.
- `build_env()`'s `env_vars` is **merge-over-`os.environ`**, *incapable* of the spec's allowlist.
- R2 is **reuse-with-modification**, not reuse-as-is; AC-7 is unmet by the naive wrapping the spec implies.
- Caller must pass low `max_turns` (default 100 ≫ propose-30/fix-60).

---

## H1/H2 — Swarm "bounded-counter" (`cli/swarm/commands.py:2269`) — **CODE-CONTRADICTED (citation)**, concept exists elsewhere

Spec §9: *"**Counter** mirrors swarm bounded-counter (`cli/swarm/commands.py:2269`): monotonic,
disk-authoritative, survives restarts."* And the Reuse Map: *"Swarm loop-guard idiom
(`cli/swarm/commands.py:2269`) — round/budget counter pattern."*

**Read the exact line — [CODE-CONTRADICTED].** `src/superclaude/cli/swarm/commands.py:2269` is:
```python
            if watch_max_iterations is not None and iterations >= watch_max_iterations:
```
This is inside the **`superclaude swarm status --watch`** poll loop (≈ lines 2250–2280). The
`iterations` variable is a **local in-memory counter** (`iterations = 0` initialized at loop entry,
`iterations += 1` per poll), bounded by `watch_max_iterations` whose sole documented purpose is
*"keeps the test surface fast"* (comment at commands.py:2028, 2308, 2419). It is:
- **NOT monotonic across runs** — reset to 0 on every `status --watch` invocation.
- **NOT disk-authoritative** — never persisted; lives only in the polling process.
- **Does NOT survive restarts** — it is the antithesis of a durable round counter.

So the cited line does the **opposite** of all three properties the spec attributes to it. A build
agent that "mirrors `commands.py:2269`" would copy an ephemeral poll-throttle and get **none** of
the loop-safety guarantees SC-5/SC-6/INV-002 require.

**The concept the spec wants DOES exist — but in a different file [CODE-VERIFIED].** The
"monotonic, disk-authoritative, survives-restarts" pattern is `SwarmState` (DM-014), the
persistent `.swarm-state.json` dataclass at `src/superclaude/cli/swarm/models.py:1141`, whose
persistence is owned by `src/superclaude/cli/swarm/state.py`. That module's **NFR-002 atomicity
contract** (state.py:14–22, 143–175) writes via `path.with_suffix(suffix + ".tmp")` then
**`os.replace(tmp, target)`** (state.py:173–175) — the live path is never opened for partial write,
so a concurrent reader sees prior-or-next state atomically. **This is the real reuse target for H1's
ledger.** The spec §10 even describes this mechanism ("Atomic writes (temp + `os.rename`)") — but
two corrections:
1. The implementation uses **`os.replace`**, not `os.rename`. On POSIX they're equivalent for the
   atomic-swap case, but `os.replace` is the correct cross-platform primitive; the spec's wording
   should track the code.
2. The **citation must be repointed** from `commands.py:2269` → `models.py:1141` (`SwarmState`
   dataclass) + `state.py:143–175` (`_write_state` atomic persistence). Leaving the §9/Reuse-Map
   citation at `commands.py:2269` will mis-route the build.

**Caveat on the analogy:** even `SwarmState` is a *wave-level coarse state* (models.py:1148), not a
per-thread round/budget counter. The remediation ledger (H1) is genuinely **new logic** that
*borrows the persistence idiom* (tmp+`os.replace`, JSON round-trip), not a counter that already
exists. The spec's "mirrors swarm" framing slightly oversells the reuse: the durable-counter
*pattern* is reusable; no drop-in counter is. This matches §2 marking H1 as **New** (good) — but
§9's specific line citation undercuts that honesty.

**Key Takeaways**
- `commands.py:2269` is an in-memory `--watch` poll cap — **CODE-CONTRADICTED** vs the spec's
  "disk-authoritative, survives-restarts" claim.
- The real durable-persistence reuse target is `SwarmState` (`models.py:1141`) + `state.py`'s
  tmp+`os.replace` atomic write (`state.py:173–175`) — **repoint §9 / Reuse Map there**.
- Spec §10 says `os.rename`; code uses `os.replace` (the correct primitive) — align wording.
- H1 is correctly **New**; only the persistence *idiom* is reused, not a counter.

---

## S1 — Severity rubric (`sc-auggie-review-protocol/refs/severity-rubric.md`) — **CODE-VERIFIED**

The rubric exists (`.claude/skills/.../refs/severity-rubric.md`; SoT under
`src/superclaude/skills/sc-auggie-review-protocol/refs/`). It defines **five tiers** — 🔴 Critical
/ 🟠 High / 🟡 Medium / 🟢 Low / 💬 Nit (headers at lines 13/24/37/49/55) — and a **Wave-3
severity-remap algorithm** (line 63+) mapping Augment categories → canonical severity
(`security`→Critical/High, `data-integrity`→High, `correctness`→Medium, `concurrency`→Medium…).
This **supports** §17's "Augment severity is a hint, not authoritative; re-grade each finding" and
the Critical/High→`--depth deep --fix`, Medium→`--fix`, Low/Nit→report-only routing. One consistency
note: the rubric's tiers are *inline-vs-summary posting* tiers (Critical gets summary+inline; High
inline only in `--depth deep`); §17 reuses them as *autonomy-routing* tiers. The mapping is clean,
but the build should not assume the rubric file encodes the *action* routing — it encodes
*severity*; the action matrix (§17) is net-new on top.

**Key Takeaways**
- Rubric is **CODE-VERIFIED**, five tiers + Wave-3 remap; §17's "hint not authoritative" is faithful.
- Rubric encodes severity + posting tier, **not** autonomy routing — §17's action matrix is additive.

---

## H4/H5 — gh posting precedent (`sc-auggie-review-protocol/SKILL.md`) — **CODE-VERIFIED (reply)**, **net-new confirmed (resolve + fork-injector)**

`SKILL.md` shows the reply/post precedent §12 reuses: `gh pr review <PR> --comment --body-file …`
(line 304) and `gh api repos/<owner>/<repo>/pulls/<PR>/comments` for inline (lines 307–314), plus
capturing the review URL (line 314). This is the template for **H4 reply-to-thread**. Two spec
claims confirmed:
- **`resolveReviewThread` (GraphQL) is genuinely net-new** — no occurrence in the SKILL; §12's
  pagination-by-`databaseId` resolve path has no prior art. [CODE-VERIFIED that it's new.]
- **H5 unconditional `--repo IronbellyOrg/IronClaude` injector is net-new** — the SKILL's `gh`
  commands use `<PR>` / `<owner>/<repo>` **placeholders**; *no* existing wrapper hard-injects the
  fork repo. So §3's "no code path can call `gh` without `--repo`" guarantee (C5/SC-4) is **not yet
  enforced anywhere** — H5 must build it from scratch. The SKILL also enforces `--comment` only
  (line 349: never `--approve`/`--request-changes`), consistent with §20's "humans merge".

**Key Takeaways**
- Reply/inline-comment `gh` precedent **CODE-VERIFIED** (SKILL.md:304–314) — good H4 template.
- `resolveReviewThread` and the fork-only `--repo` injector are **net-new** — spec correctly marks them New.
- No existing wrapper enforces fork-only `--repo`; C5/SC-4's "structurally impossible to omit" is a *to-build* invariant, not a reuse.

---

## Secret-sourcing model (`~/.aienv`) — **CODE-CONTRADICTED (chmod claim)**

Spec Reuse Map: *"`~/.aienv` / `ccsession.env` chmod-600 — model for systemd `EnvironmentFile=`
secret sourcing."* §11 leans on this as the at-rest-secret exemplar.

**On disk — [CODE-CONTRADICTED].** `/config/.aienv` (i.e., `~/.aienv` in this environment) is
`-rw-r--r--` = **mode 644 — world-readable**, not 600. The *practice* the spec prescribes
(secret files `chmod 600`, owner `root:remediation-bot`, systemd `EnvironmentFile=`, §11) is correct
and standard — but the **cited precedent file does not exemplify it**. Presenting `.aienv` as a
"chmod-600 model" is factually wrong about the live file. Recommendation: either (a) drop `.aienv`
as the *exemplar* and cite the systemd `EnvironmentFile=` + `chmod 600` requirement on its own
merits, or (b) note that `.aienv` is the *content-sourcing* model (KEY=VALUE lines read into env),
**not** the *permissions* model. The permissions discipline in §11 is sound; only the "this file
already does it" provenance is false.

**Key Takeaways**
- `~/.aienv` is **644 on disk**, not 600 — the "chmod-600 model" provenance is **CODE-CONTRADICTED**.
- §11's permission requirements are correct on their own; sever them from the false `.aienv` exemplar.

---

## `cli/remediate/` package — **CODE-VERIFIED greenfield**

`src/superclaude/cli/remediate/` **does not exist** (`No such file or directory`). All
components D1–D6, R1–R4, H1–H5, S2, T1 in §2 are confirmed **net-new** — consistent with the
inventory's "New" labels. The reuse anchors are only the three external primitives audited above
(ClaudeProcess, swarm-persistence idiom, auggie rubric/gh template). This is an accurate inventory:
the spec does **not** overclaim reuse at the package level — its overclaims are at the *line-citation*
level (§9 swarm:2269) and the *capability* level (§7 build_env allowlist, `.aienv` chmod).

---

## Gaps and Questions

1. **[BUILD-BLOCKING] `build_env()` allowlist is impossible as cited.** The spec's secret boundary
   (INV-001/SC-7, AC-7) requires the Runner env to *exclude* `GH_TOKEN`/push token. The current
   `ClaudeProcess.build_env()` (process.py:155–159) merges `env_vars` over `os.environ.copy()` and
   cannot exclude inherited keys. **Decision needed:** add an `env_replace`/`base_env` param to
   `build_env()`, OR spawn the Runner from a pre-scrubbed parent. Without one, AC-7 fails silently.
   → Belongs in §19 step 5, gated by an AC-7 secret-scrape test.
2. **[CITATION] Repoint §9 / Reuse Map** from `cli/swarm/commands.py:2269` (ephemeral `--watch` cap)
   to `cli/swarm/models.py:1141` (`SwarmState`) + `cli/swarm/state.py:143–175` (tmp+`os.replace`).
   Confirm with the operator that the durable-persistence *idiom* (not a drop-in counter) is what
   H1 reuses.
3. **[WORDING] §10 says `os.rename`; code uses `os.replace`.** Align the spec to the correct
   cross-platform atomic primitive.
4. **[PROVENANCE] `.aienv` is 644, not 600.** Decide whether to drop it as the chmod-600 exemplar or
   re-scope it to a *content-sourcing* (KEY=VALUE) model only.
5. **[CONFIG] max_turns defaults.** `ClaudeProcess` defaults `max_turns=100`; the build must pass
   propose≈30/fix≈60 explicitly. Is there a config surface for these, or hardcoded per autonomy level?
6. **[OPEN — inherited from spec §21]** OD-1 sandbox tech, OD-2 push-token mechanism, OD-3 push-budget
   default, OD-4 `patch` level — all remain genuinely open; nothing in the code resolves them. Not
   re-litigated here (other agents/§21 own them).

## Stale Documentation Found

- **Spec §9 + Reuse Map — `cli/swarm/commands.py:2269` citation is STALE/WRONG.** The line is an
  in-memory poll-iteration cap, not a disk-authoritative round counter. The "monotonic,
  disk-authoritative, survives restarts" prose describes `SwarmState`/`state.py`, which live at
  different paths. **[CODE-CONTRADICTED]**
- **Spec §7 — "wrap `build_env()` with allowlist `env_vars`" implies the existing param suffices.**
  It does not (merge-not-replace). **[CODE-CONTRADICTED]** — the doc describes an intent the code
  cannot currently satisfy.
- **Spec §10 — "temp + `os.rename`"** is imprecise; the reused code uses `os.replace`. **[minor]**
- **Reuse Map — "`~/.aienv` … chmod-600"** misdescribes a 644 file. **[CODE-CONTRADICTED]**
- **VERIFIED-ACCURATE:** ClaudeProcess location/shape (§7), severity rubric (§17), gh reply
  precedent (§12), `resolveReviewThread`/fork-injector as net-new (§3/§12), full `cli/remediate/`
  greenfield (§2). The spec is honest at the inventory level; its errors are at the line/capability level.

## Summary

The V2.0 spec is **architecturally sound and inventory-honest**, but rests on **three load-bearing
citation/capability errors** that a reuse-trusting build agent would inherit:

| # | Spec claim | Verdict | Impact | Fix |
|---|-----------|---------|--------|-----|
| 1 | §7 `build_env()` wrap → allowlist env | **CODE-CONTRADICTED** | AC-7 secret boundary unmet by construction | Add `env_replace`/`base_env`, OR spawn from scrubbed parent; gate on AC-7 |
| 2 | §9 swarm counter @ `commands.py:2269` | **CODE-CONTRADICTED** | Build mirrors an ephemeral poll cap, loses SC-5/6/INV-002 durability | Repoint to `models.py:1141` + `state.py:143–175` (`os.replace`) |
| 3 | `.aienv` chmod-600 exemplar | **CODE-CONTRADICTED** | False provenance for §11 secret hygiene | Drop exemplar or rescope to content-sourcing |

**CODE-VERIFIED (safe to trust):** `ClaudeProcess` at process.py:72 (stdin delivery, build_command
flags, defaults); severity rubric five-tier + Wave-3 remap; gh reply/inline precedent in
auggie SKILL.md:304–314; `resolveReviewThread` + fork-only `--repo` injector correctly flagged
net-new; `cli/remediate/` confirmed greenfield.

**Net:** the spec converges cleanly, but **finding #1 is build-blocking** (silent secret leak into
the Runner unless `build_env` is modified) and **#2 will mis-route H1** unless the citation is
repointed before parser/ledger code is written (§19 step 2). Recommend the TDD/build phase treat R2
as **reuse-with-modification** and correct the §9 citation as a pre-build doc fix.

**EXIT_RECOMMENDATION: CONTINUE**
