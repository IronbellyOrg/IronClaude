# Research: Investigation topic 2 (research-notes did not contain an Agent 2 block — investigate broadly using the planning inputs).

**Investigation type:** Investigator
**Scope:** Codebase reuse-target verification + architectural feasibility for PR Auto-Remediation V2.0 (the merged-requirements spec's `Reuse Map`, `Component Inventory`, and integration seams). Focus: validate the spec's load-bearing reuse claims against CURRENT source code.
**Status:** Complete
**Date:** 2026-06-11

---

## Investigation Framing

No Agent 2 block existed in research-notes, so this investigation targets the highest-risk
assumptions in the merged-requirements spec: its **reuse claims**. The spec proposes ~18 new
components but anchors feasibility on a small set of "Reuse" primitives. If those primitives do
not behave as claimed, the build sequencing (§19) and invariant resolutions (§16) collapse. This
report verifies each claimed reuse against actual source, then maps integration seams and gaps.

The four load-bearing reuse claims to verify:
1. `ClaudeProcess` at `cli/pipeline/process.py:72` — headless `claude --print` spawn (R2).
2. Swarm bounded-counter idiom at `cli/swarm/commands.py:2269` — round/budget pattern (H1/H2).
3. Severity rubric `sc-auggie-review-protocol/refs/severity-rubric.md` — depth routing (S1).
4. `gh` inline/summary posting in `sc-auggie-review-protocol/SKILL.md` — reply/resolve template (H4/H5).

---

## Reuse Claim 1 — `ClaudeProcess` (R2): **[CODE-VERIFIED, with one real caveat the spec already flags]**

**Location confirmed.** `class ClaudeProcess` is defined at `src/superclaude/cli/pipeline/process.py:72`
— the spec's `:72` citation is exact. This is the primitive the entire Runner (R2) depends on.

**`build_command()` matches the spec verbatim.** `process.py:121-143` emits:
`claude --print --verbose <permission_flag> --no-session-persistence --tools default --max-turns
<N> --output-format <fmt>` then appends `--model` (if set) and `extra_args`. The spec §7 quotes
this exactly, including `--dangerously-skip-permissions` as the default `permission_flag`
(`process.py:93`). **[CODE-VERIFIED]**

**stdin prompt delivery is real and robust** — this is the single most important feasibility fact
for the bot, because opComment + envelope can be large:
- Prompt is delivered via **stdin**, NOT argv (`process.py:162-205`, `_write_prompt_to_stdin` at
  `:221-258`). The spec's claim "prompt delivered via stdin (bypasses 128KB argv limit)" is
  **[CODE-VERIFIED]**. The 128KB ceiling (Linux `MAX_ARG_STRLEN`) is explicitly bypassed.
- Delivery is **chunked** (64 KiB chunks, `_STDIN_CHUNK_SIZE` at `:219`), **EINTR-retrying**
  (`:242-244`), and **BrokenPipe/OSError-safe** (errors captured in `self._stdin_error`, surfaced
  via `_log.warning` in `wait()`, not raised out of `start()` — `:249-253`, `:269-272`).
- A **pre-spawn size guard** (`PROMPT_MAX_BYTES`, default 16 MiB, env-overridable via
  `SUPERCLAUDE_PROMPT_MAX_BYTES`) raises the typed `PromptTooLargeForArgv` before any handle is
  opened (`:169-173`). The envelope builder (R3) gets a clean, typed failure mode for over-large
  opComments — directly useful for SC-2 length-capping.
- stdout/stderr are redirected to **real file handles, not pipes** (`:180-181`, `:185-186`), so a
  blocked stdin write **cannot deadlock** (`:194-197`). This matters: the Runner can stream a
  long `claude -p` session to a file without the Dispatcher having to pump pipes.

**Process-group kill is built in.** `os.setpgrp` as `preexec_fn` (`:189-190`) + `terminate()`
(SIGTERM→10s→SIGKILL, `:278`) means the whole child tree dies on shutdown. This satisfies the
sandbox-teardown / `StuckRun` requirements (§14) without new code.

**THE CAVEAT (spec is correct to flag it — INV-001/SC-7 is a genuine gap, not paranoia):**
`build_env()` at `process.py:145-160` does `env = os.environ.copy()` (`:155`), pops only
`CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`, then `env.update(env_vars)` if provided (`:158-159`).
**There is NO subtractive allowlist.** The `env_vars` parameter only *adds/overrides* on top of a
full inherited environment. **[CODE-VERIFIED]** Consequence: a Runner spawned with the primitive
as-is would inherit **every** secret in the Dispatcher's environment — `GH_TOKEN`, `ANTHROPIC_*`,
anything in `~/.aienv` that got exported. The spec's §7 requirement —
> "`build_env()` MUST be wrapped with an explicit allowlist `env_vars` (not the current full
> `os.environ.copy()`)"

— is therefore **load-bearing and correct**. But note carefully: passing `env_vars` does NOT
achieve this today, because update-semantics can't *remove* inherited vars. The build will need
**either** (a) a new `build_env()` mode/param that starts from `{}` instead of `os.environ.copy()`,
**or** (b) a Runner that wraps `ClaudeProcess` and constructs a clean env itself, **or** (c)
process-level isolation (the §6 sandbox with no host env passthrough) so `os.environ` is already
minimal. Option (c) is the strongest and aligns with §6's "no host home mount". **This is a real
code change to a shared primitive — flag for TDD: do not subclass-and-hope; verify the env actually
starts empty (AC-7 `/proc/<pid>/environ` grep = 0 is the right test).**

**Key Takeaways (Claim 1):**
- `ClaudeProcess` is genuinely reusable for the Runner; the stdin/chunked/size-guard/pgroup
  machinery is exactly what a headless remediation spawn needs. **Highest-confidence reuse in the spec.**
- The lone modification (env allowlist) is real, is on a *shared* primitive (sprint/roadmap/swarm
  also call it), and **must not regress those callers** — `env_vars` defaults to `None`, so adding
  an opt-in clean-env path is backward-safe. This is the one place the build touches existing code.

---

## Reuse Claim 2 — Swarm bounded-counter (H1/H2): **[CODE-CONTRADICTED on the line cite; IDIOM-VERIFIED elsewhere in the file]**

The spec (§9 + Reuse Map) cites `cli/swarm/commands.py:2269` as the "swarm bounded-counter idiom
(monotonic, disk-authoritative, survives restarts)."

**The exact line is mis-cited.** Code at `commands.py:~2230-2290` is the `swarm status --watch`
**polling loop**: an in-memory `iterations` counter bounded by `watch_max_iterations` that re-reads
a state file and stops on `phase=<TERMINAL_STATE_VALUE>` (`commands.py:2253-2275`). That is an
**ephemeral watch-iteration bound**, NOT a disk-authoritative round counter that survives restart.
A ledger built by copying *this* line would get the wrong property. **[CODE-CONTRADICTED]** —
the `:2269` citation does not point at what the spec describes.

**But the IDIOM the spec actually needs genuinely exists in the same file** — just elsewhere:
- **Atomic disk-state writes** are pervasive: `.swarm-state.json` written via an atomic COMP-011
  writer (`commands.py:699-706`), `write_state` as the canonical atomic writer (`:2822`), tmp +
  `os.replace` scaffold writes (`_write_scaffold_atomic` at `:3074-3081`), and an explicit
  IMM-6/NFR-002 "atomic-write discipline" with a dedicated enforcement test
  (`tests/swarm/test_imm6_atomic_write.py`, referenced at `:2869`). **[CODE-VERIFIED]** The spec's
  §10 ledger requirements (atomic temp+`os.rename`, survives restart, no half-written file) have a
  **real, battle-tested precedent** — the spec just pointed the reader at the wrong line for it.
- Terminal-state idempotency exists: a state writer that becomes a **no-op transition** when it
  finds `done.json` already on disk and re-stamps `updated` atomically (`:2844-2915`). This is
  directly analogous to the spec's §9 "intent-without-outcome = RESUME, never silent re-execute".

**Net:** the reuse is *sound in spirit* (swarm is the right place to crib atomic disk-state +
terminal idempotency from), but **H1's two-phase ledger is effectively net-new code** modeled on
swarm's atomic-write discipline — it is NOT a thin copy of one function at line 2269. The
two-phase intent/outcome split (§9) and per-PR push budget have **no direct swarm analogue**; only
the *atomic-write substrate* is reusable. Treat H1 as "New, pattern-borrowed", which is exactly how
the Component Inventory already tags it (**New** (OQ-E, SC-5/6, INV-002/011)) — so the inventory is
honest even though the Reuse-Map line cite is loose.

**Key Takeaways (Claim 2):**
- Correct the citation: the reusable substrate is swarm's **atomic-write/terminal-idempotency
  discipline** (`write_state`, `_write_scaffold_atomic`, IMM-6), not the `status --watch`
  iteration counter at `:2269`.
- The two-phase ledger, per-PR push budget, and SHA-correlation are **new logic**; budget them as
  build cost, not reuse savings. §19.2 ("test H1 in isolation") correctly treats it as net-new.

---

## Reuse Claim 3 — Severity rubric (S1): **[CODE-VERIFIED — clean reuse, no modification needed]**

`refs/severity-rubric.md` exists at `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`
(and its synced `.claude/` mirror). Content fully supports §17's "Severity → Action Matrix":
- It is explicitly **decision-term** graded (Critical = "Block merge", High = "Should fix before
  merge", Medium = "Fix in this PR if cheap"), which maps cleanly onto the spec's depth routing
  (Critical/High → `--depth deep --fix`; Medium → `--fix`; Low/Nit → report-only). **[CODE-VERIFIED]**
- The rubric's stated *raison d'être* — "Auggie's `severity_hint` is a starting point, not
  authoritative … remapped through this rubric" — is **exactly** what spec §17 asserts ("Augment
  severity is a hint, not authoritative; re-grade each finding"). The spec did not invent this; it
  inherited a real, documented contract. **[CODE-VERIFIED]**
- Bonus alignment: the rubric *already* encodes the inline-vs-summary posting split per tier
  ("Critical findings receive both a summary comment AND an inline `gh` comment"; "High findings
  receive inline `gh` comments in `--depth deep` mode"). The bot's autonomy/depth gating can read
  this directly instead of re-deriving it.

**Key Takeaways (Claim 3):** Pure-reuse, zero modification. This is the safest reuse claim in the
spec and needs no TDD attention beyond "import the ref, don't fork it."

---

## Reuse Claim 4 — `gh` posting precedent (H4/H5): **[PARTIALLY VERIFIED — posting precedent real; reply/resolve + `--repo` injection genuinely net-new]**

The auggie SKILL.md (`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`) contains real gh
precedent for **posting** review content:
- Summary comment: `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md` (`SKILL.md:304`).
- Inline file:line comment: `gh api repos/<owner>/<repo>/pulls/<PR>/comments` (`SKILL.md:307`).
- Review-URL capture: `gh pr view <PR> --json reviews -q '.reviews[-1].url'` (`SKILL.md:314`).
- Hard guard: "strictly `--comment`" — never `--approve`/`--request-changes` (`SKILL.md:349`),
  which the spec §20 "Out of Scope" echoes ("humans merge"). **[CODE-VERIFIED]** The precedent is a
  good template for posting and shares the spec's no-merge-state discipline.

**Two things the precedent does NOT provide — confirming the spec's "net-new" tags:**
1. **Reply-to-thread + resolve is entirely absent.** A targeted grep of SKILL.md for
   `replies`, `resolveReviewThread`, `reviewThreads`, `databaseId`, `in_reply_to` returned **zero
   hits**. The spec §12 / H4 claim "Net-new (absent from repo today)" is **[CODE-VERIFIED as
   absent]**. The reply endpoint (`.../comments/<parent_id>/replies`) and the GraphQL
   `resolveReviewThread(threadId)` with `databaseId` pagination must be built and tested from
   scratch — there is no precedent to crib threading semantics from. This is the spec's highest-risk
   net-new GitHub surface (INV-010), and the §19.1 "probe first against a throwaway fixture PR" gate
   is well-targeted at de-risking exactly this.
2. **The precedent does NOT pin `--repo IronbellyOrg/IronClaude`.** SKILL.md uses generic
   `<owner>/<repo>` placeholders (`:307`) and bare `gh pr view <id>` / `gh pr review <PR>`
   (`:304`, `:314`) — it relies on gh's ambient repo resolution. **[CODE-VERIFIED]** This is
   precisely the failure mode CLAUDE.md warns about (gh defaults to the fork's *parent*). So H5's
   "unconditional `--repo` injector" (§3, C5, SC-4) is **NOT inherited from the precedent — it is a
   new safety invariant the precedent actually lacks.** The spec is right to make H5 a mandatory
   chokepoint ("no code path can call `gh` without it"); the reuse template would, if copied
   naively, reproduce the unpinned-repo bug.

**Key Takeaways (Claim 4):** Posting template = reusable. Reply/resolve threading (H4) and the
fork-only `--repo` injector (H5) = net-new, correctly tagged **New** in the inventory. The probe-first
gate (§19.1) is the right mitigation for the threading unknowns.

---

## Integration Landscape — Prior Art Sweep for the Net-New Components

To gauge how much of the spec is truly greenfield, I swept `src/superclaude` for prior art behind
the Dispatcher-side components (D2/D3/D5, S2). Findings (all `--include=*.py`, test files excluded):

| Capability needed | Component | Prior art in repo? | Evidence |
|---|---|---|---|
| GitHub polling w/ ETag / `If-None-Match` / `since=` / rate-limit headers | D3 ingest | **NONE** | grep for `If-None-Match\|ETag\|X-RateLimit\|Retry-After\|since=` → 0 non-test hits |
| `gh` fork-only `--repo` wrapper / injector | H5 | **NONE** | grep `IronbellyOrg/IronClaude\|def gh_call` → 0 hits in `src/**/*.py` |
| systemd unit / `deploy/` dir / `.service` files | S2 | **NONE** | no `deploy/` dir; no `*.service` files in tree |
| GitHub collaborator-permission authz (`collaborators/{login}/permission`, `sender.login`) | D5 | **NONE** | the only `permission` hits are `--permission-flag` for the *claude* CLI (`sprint/commands.py:110`, `sprint/tmux.py:188`) — unrelated to GitHub authz |

**Interpretation.** The Runner half of the system (R2 executor) sits on a mature, verified primitive
(`ClaudeProcess`). The **Dispatcher half is almost entirely greenfield**: polling/ingest (D3),
authz (D5), the gh-injector (H5), and deploy (S2) have **no reusable prior art** in this codebase.
This is consistent with the spec's own Component Inventory (12 of ~18 rows tagged **New**), but it
sharpens the build-risk picture: **the spec's "Reuse" column is thin** — effectively one strong
reuse (`ClaudeProcess`), one pure-reference reuse (severity rubric), one pattern-borrow (swarm
atomic writes), and one partial-template (gh posting). Everything operationally novel (the 24/7
daemon, GitHub event plumbing, secret-scoping, sandbox) is new code. The §19 build sequencing
already front-loads the riskiest net-new pieces (probe → H5/H1 → ingest/authz), so the ordering is
defensible — but anyone estimating this should price it as a **mostly-new subsystem with a few
sturdy anchors**, not a "wire up existing parts" job.

**Key Takeaways (Integration Landscape):**
- Reuse surface is narrower than the Reuse Map's four-item list implies; only `ClaudeProcess` is a
  substantial code-reuse. The rest is reference/pattern/template.
- The Dispatcher is the cost center and the risk center. Probe-first (§19.1) and isolated H5/H1
  testing (§19.2) are correctly prioritized.

---

## Gaps and Questions

1. **`build_env()` clean-env mechanism is unspecified at the code level (HIGH).** §7 mandates an
   allowlist env but the current API can only *add* vars, not *subtract* the inherited environment.
   TDD must decide: new `build_env(base_env=...)` param vs sandbox-level isolation vs Runner-owned
   env construction. Without one of these, AC-7 (`/proc/<pid>/environ` grep = 0) cannot pass. The
   spec asserts the requirement but does not pin the mechanism — this is OD-adjacent and should be
   an explicit open decision.
2. **Reply/resolve threading has zero in-repo precedent (HIGH).** H4's `databaseId` pagination +
   `resolveReviewThread` is the most novel GitHub surface and the §19.1 probe is the only thing
   standing between the spec and an INV-010 "resolved the wrong thread" bug. Is the throwaway-PR
   probe budgeted as a hard gate before any H4 code, or advisory? Spec says "Gate before parser
   code" for §19.1 — confirm H4 is also behind it.
3. **Swarm reuse line-cite is wrong (MEDIUM, doc-quality).** `:2269` points at the watch loop, not
   the atomic-write discipline. Low functional risk (inventory tags H1 **New**), but a builder who
   trusts the cite will read the wrong code. Fix the citation to the `write_state`/IMM-6 region.
4. **Sandbox tech is unresolved (OD-1) and gates D5→R4 sequencing (MEDIUM).** The env-isolation
   answer in Gap 1 is partly determined by OD-1 (container vs microVM). These two open decisions are
   coupled and should be resolved together, not independently.
5. **No existing daemon/long-lived-service pattern in the CLI (MEDIUM).** Every current CLI surface
   (sprint/roadmap/swarm) is invoke-and-exit; there is no `Restart=always` watchdog service
   precedent. D2's supervision/watchdog/rate-limit loop is a new operational shape for this repo —
   worth a spike to validate the systemd `WatchdogSec`/`sd_notify` integration in Python.

## Stale Documentation Found

- **Reuse Map → `cli/swarm/commands.py:2269`**: stale/imprecise line citation. At `:2269` the code
  is the `swarm status --watch` iteration loop, not the "monotonic, disk-authoritative, survives
  restarts" counter the prose describes. The described property lives in the atomic-write discipline
  (`write_state` `:2822`, `_write_scaffold_atomic` `:3074`, IMM-6 enforcement). **[CODE-CONTRADICTED]**
- **§7 implication that passing `env_vars` achieves the allowlist**: the prose "wrapped with an
  explicit allowlist `env_vars`" can be misread as "just pass `env_vars`". Code shows `env_vars` is
  additive over `os.environ.copy()`, so it cannot *remove* inherited secrets. The requirement is
  correct; the mechanism implied by "env_vars" is insufficient. **[CODE-CONTRADICTED as written]**
- All other reuse citations (`process.py:72`, severity-rubric path, SKILL.md gh-posting lines)
  are **accurate and current**. **[CODE-VERIFIED]**

## Summary

The merged-requirements spec rests on four reuse claims; verification against current source:

| Claim | Verdict | Notes |
|---|---|---|
| `ClaudeProcess` `process.py:72` (R2) | **VERIFIED** | Exact line; stdin/chunked/size-guard/pgroup all real. One genuine modification needed (env allowlist) — spec correctly flags it, but the `env_vars` API as-is can't achieve it. |
| Swarm counter `commands.py:2269` (H1) | **LINE CONTRADICTED / idiom verified** | `:2269` is the watch loop, not a disk counter. The needed atomic-write/terminal-idempotency discipline exists elsewhere in the file (`write_state`/IMM-6). H1 is effectively net-new, pattern-borrowed. |
| Severity rubric (S1) | **VERIFIED** | Clean, zero-mod reuse. Rubric's own "hint not authoritative" contract == spec §17. Even pre-encodes inline-vs-summary posting per tier. |
| gh posting `SKILL.md` (H4/H5) | **PARTIAL** | Posting template real (`:304`,`:307`). Reply/resolve threading + fork-only `--repo` injector are net-new (0 grep hits) — spec's "New" tags are honest; precedent actually *lacks* `--repo` pinning. |

**Bottom line for the PRD:** the architecture is feasible and the reuse anchors are real, but the
**reuse surface is narrower than the four-item Reuse Map suggests** — one substantial code reuse
(`ClaudeProcess`), one reference (rubric), one pattern-borrow (swarm atomic writes), one partial
template (gh posting). The Dispatcher half (polling, authz, gh-injector, systemd) is greenfield with
**no in-repo prior art**. The two highest-risk net-new surfaces — the env-allowlist mechanism
(AC-7) and reply/resolve threading (INV-010) — are exactly the ones the spec's §19 build sequencing
front-loads behind a probe-first gate, so the plan is sound; estimators should simply price this as
a *mostly-new subsystem with a few sturdy anchors*, not a wiring job. Two documentation fixes are
warranted before TDD: correct the swarm line-cite, and disambiguate the §7 env-allowlist mechanism.

**EXIT_RECOMMENDATION: CONTINUE**
