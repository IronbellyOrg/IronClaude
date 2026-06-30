---
contract_version: "1.0"
artifact: merged-requirements
topic: "PR Review Auto-Remediation Monitor (V1.0)"
domain: architecture
strategy: systematic
depth: standard
synthesis_mode: focused-synthesis-with-red-team
adversarial_status: not-run-by-user-prescription
created: 2026-06-10T23:47:50Z
source_seed: ./seed-brief.md
---

# Merged Requirements: PR Review Auto-Remediation Monitor — V1.0

> **Synthesis note.** The user's four Socratic answers pre-converged the design, so this spec
> is a focused synthesis rather than a 3-model adversarial merge. The "adversarial value"
> (blind-spot hunting) is preserved as the **§7 Red-Team** section, which pressure-tests the
> four highest-risk decisions. Run the full `/sc:adversarial` pass (command in the handoff
> section) if you want independent multi-model divergence before building.

## 1. Component Inventory (what gets built)

| # | Component | Type | Source path (SoT) | New / Reuse |
|---|-----------|------|-------------------|-------------|
| C1 | `sc:submit-pr` (working name) | Skill + command | `src/superclaude/skills/sc-submit-pr-protocol/` + `src/superclaude/commands/submit-pr.md` | **New** |
| C2 | Augment review poller | Skill ref/script | `…/sc-submit-pr-protocol/refs/augment-poll.md` (+ optional `scripts/poll-augment-review.sh`) | **New** |
| C3 | Severity→tier router | Skill ref | `…/refs/severity-routing.md` | **Reuse** rubric from `sc-auggie-review-protocol/refs/severity-rubric.md` |
| C4 | Reply-to-thread + resolve helper | Skill ref/script | `…/refs/thread-reply.md` | **New** (mirrors `gh api` patterns already in `sc-auggie-review-protocol`) |
| C5 | `offer-pr-review.sh` hook update | Hook | `src/superclaude/hooks/scripts/offer-pr-review.sh` | **Edit** — also mention `sc:submit-pr --monitor` |
| C6 | Tests | pytest + skill self-tests | `tests/…` | **New** |

After any source edit: `make sync-dev` → `make verify-sync`. Never stage `.claude/` except
`settings.json`.

## 2. Functional Requirements

### FR-1 — PR submission skill with `--monitor` ordinal
`sc:submit-pr` opens a PR on the fork and arms the in-session monitor at the requested level.

- `FR-1.1` Signature: `/sc:submit-pr [--monitor {0,1,2,3}] [--max-rounds N] [--base master] [--head <branch>] [--title …] [--body …]`
- `FR-1.2` `--monitor` defaults to `0` (open PR, no monitor — behaviorally identical to today).
- `FR-1.3` All `gh pr create` / review / reply calls **MUST** pin `--repo IronbellyOrg/IronClaude`.
- `FR-1.4` Pre-PR checks from `CLAUDE.md` are enforced (confirm `origin`, rebase onto
  `origin/master` if behind, verify returned URL is `IronbellyOrg/IronClaude`).
- `FR-1.5` On `--monitor ≥ 1`, after the PR is created the skill arms the Monitor tool (§FR-2).

### FR-2 — In-session Augment review monitor
- `FR-2.1` Poll the PR for the **Augment Code GitHub App** review using `gh` (e.g.
  `gh pr view <N> --repo … --json reviews,comments` and
  `gh api repos/IronbellyOrg/IronClaude/pulls/<N>/comments`).
- `FR-2.2` Detection contract: distinguish three states — (a) *no review yet* (keep polling),
  (b) *review posted, zero Medium+ findings* (terminate clean), (c) *review posted with
  findings* (route). Detection keys on the Augment App's bot login (resolved empirically per
  OQ1, stored as a config constant, not hard-guessed).
- `FR-2.3` Poll interval ≥ 30s (GitHub API rate-limit friendly); overall wait bounded by a
  timeout (default ~30 min, configurable) after which the monitor reports "review never
  arrived" and exits gracefully.
- `FR-2.4` The monitor is hosted by the **Monitor tool**; the live session must remain open.
  On session close before review lands, the monitor is lost (documented limitation; V2.0 fixes
  via headless host).

### FR-3 — Severity → troubleshoot-tier routing
- `FR-3.1` For each finding, derive a normalized severity (Critical/High/Medium/Low/Nit) by
  re-grading through the reused **severity rubric** (Augment's self-reported severity is a
  *hint*, not authoritative — same principle as `sc-auggie-review`).
- `FR-3.2` Route: **Medium → `/sc:troubleshoot --fix`**; **High or Critical →
  `/sc:troubleshoot --depth deep --fix`**; **Low / Nit → report only**, no remediation.
- `FR-3.3` The troubleshoot invocation is seeded with the finding body + `file:line` +
  evidence so the diagnosis is grounded (no re-deriving the problem from scratch).
- `FR-3.4` Multiple findings batch sensibly: group by file/area where troubleshoot can address
  several in one session; never exceed the round budget.

### FR-4 — Autonomy gates (the `--monitor` ordinal)
- `FR-4.1` **Level 1**: diagnose + propose only. Surface to the user: all Augment comments,
  the proposed remediation for each, and an explicit offer ("fix these? y/n"). **No edits.**
- `FR-4.2` **Level 2**: implement fixes + validate locally (§FR-5). Then **HALT**: ask the
  user before any `git commit`/`git push` and before posting any reply. Working tree changes
  are left in place for inspection.
- `FR-4.3` **Level 3**: implement + validate + commit + push to the PR branch + reply-to-thread
  + resolve, unattended — governed by the loop-guard (§FR-6).
- `FR-4.4` `needs_human_decision`-class findings (ambiguous intent, security trade-offs, API
  contract changes) **MUST HALT for human sign-off even at level 3** — never auto-ship a
  guessed default. (Mirrors the repo's "human-decision items must HALT" rule.)

### FR-5 — Local validation before push
- `FR-5.1` "Validated" = the relevant test command passes. Default: targeted tests for changed
  files; escalate to `make test` when changes are cross-cutting (decision recorded per round).
- `FR-5.2` `make lint` **and** `uv run ruff format --check src/ tests/` must pass before push
  (green `make lint` ≠ green CI format — known repo gotcha).
- `FR-5.3` If validation fails, do **not** push; report the failure and (level 3) retry within
  the round budget or HALT.

### FR-6 — Reply, resolve, and loop termination
- `FR-6.1` Each implemented fix posts a reply on the **specific** Augment review-comment thread
  (`gh api …/pulls/<N>/comments/<comment_id>/replies` or the review-comment reply endpoint),
  summarizing the fix + commit SHA, then resolves the thread.
- `FR-6.2` **Loop-stop**: after a remediation round + push, wait for Augment's re-review; stop
  when the re-review surfaces **zero Medium+ findings** OR `--max-rounds` is reached.
- `FR-6.3` **Loop-guard**: a re-review caused by the monitor's own push counts as the *next*
  round, not a new independent trigger; the round counter is monotonic and capped. Never exceed
  `--max-rounds` (default 2, max 5).
- `FR-6.4` On max-rounds-with-residual-findings, post a summary comment listing unresolved
  findings and hand back to the human.

### FR-7 — Hook integration (minimal)
- `FR-7.1` Update `offer-pr-review.sh` to additionally mention `sc:submit-pr --monitor` as the
  autonomous path (alongside the existing `/sc:auggie-review` offer). Hook stays **fail-open**,
  never blocks, never spawns anything.

## 3. Non-Functional Requirements
- `NFR-1` Idempotent replies: never double-post the same fix reply to a thread (track replied
  comment IDs).
- `NFR-2` Rate-limit safety: poll ≥30s; back off on `gh` API 403/secondary-limit.
- `NFR-3` Observability: write a per-run log (`.dev/…/monitor-run-<PR>.jsonl`) of every poll,
  finding, route decision, fix, push, reply — for forensic review and round auditing.
- `NFR-4` Fail-safe defaults: unknown severity → treat as Medium (fix tier), not Critical or
  ignore; unknown bot login → "review not detected" (never act on a non-Augment comment).
- `NFR-5` All paths absolute in user-facing prompts; all paste-ready commands single-line.

## 4. Out of Scope (V1.0)
- Detached / headless `claude -p` execution host.
- GitHub Actions / server-side hosting.
- The @bot-mention → headless trigger (entire V2.0 — separate brainstorm).
- Reviewing/replying to non-Augment human review comments.
- Modifying merge state (`--approve` / `--request-changes`) — humans merge.

## 5. Severity → Action Matrix (authoritative)

| Augment finding severity (post-rubric) | Troubleshoot tier | Acts at monitor level |
|----------------------------------------|-------------------|------------------------|
| Critical | `/sc:troubleshoot --depth deep --fix` | 1=propose · 2=fix+ask-push · 3=auto (HALT if `needs_human_decision`) |
| High | `/sc:troubleshoot --depth deep --fix` | same as Critical |
| Medium | `/sc:troubleshoot --fix` | same gating |
| Low / Nit | report only | never auto-remediated |

## 6. Acceptance Criteria (testable)
- `AC-1` `--monitor 0` ⇒ PR opens, zero monitor activity (regression-safe vs today).
- `AC-2` Given a fixture PR with one Medium + one High Augment finding, level-3 run produces:
  2 troubleshoot sessions (1 standard, 1 deep), 2 validated fixes, 2 thread replies, 2 resolved
  threads, ≤`--max-rounds` rounds, deterministic termination.
- `AC-3` Level-1 run makes **zero** file edits and emits the offer prompt verbatim.
- `AC-4` Level-2 run leaves changes in the working tree and makes **zero** pushes without
  approval.
- `AC-5` A `needs_human_decision` finding HALTs even at level 3.
- `AC-6` Loop never exceeds `--max-rounds`; a monitor-triggered re-review increments the same
  counter (no infinite loop) — verified with a 2-round fixture.
- `AC-7` Every `gh` call in the code path carries `--repo IronbellyOrg/IronClaude`.

## 7. Red-Team — the four risks that can sink this

> These are the points where a naive build breaks. Treated as MUST-resolve-before-build.

- **R1 (OQ1) — Augment review-detection is guesswork until probed.** We do **not** know the
  Augment App's exact GitHub emission shape (formal review vs. issue comments vs. check-run) or
  its bot login. **Mitigation:** before writing the parser, run an empirical probe — open one
  throwaway PR, let Augment review it, capture `gh pr view --json reviews,comments` +
  `gh api …/pulls/<N>/reviews` + `…/comments`, and lock the detection constant from real data.
  Building the parser on a guess is the #1 failure mode.
- **R2 — Loop-guard correctness (infinite remediation).** The monitor pushes a fix → Augment
  re-reviews → possibly new findings → fix → … A monotonic, capped round counter (FR-6.3) is
  **load-bearing**; an off-by-one or a "new review = new trigger" bug burns compute and spams
  the PR. **Mitigation:** AC-6 fixture + the round counter must key on "reviews observed since
  arm", not "reviews seen since last poll".
- **R3 — Session-longevity fragility (in-session host).** Augment's review can take minutes;
  the Monitor tool requires the session to stay open. If the user closes the terminal, the loop
  silently dies mid-remediation (possibly after a push, before replies). **Mitigation:**
  checkpoint state to the run-log (NFR-3) so a re-armed monitor can resume; document the
  limitation prominently; this fragility is the core reason V2.0 moves to a headless host.
- **R4 — Auto-push blast radius (level 3).** Fully autonomous commit+push to a PR branch is
  outward-facing and hard to reverse. A wrong fix that passes targeted tests but breaks
  something untested gets pushed + announced as resolved. **Mitigation:** FR-5.2 lint+format
  gate, FR-4.4 human-decision HALT, NFR-3 audit log, and a conservative `--max-rounds 2`
  default. Recommend level 3 be opt-in per-invocation, never a persisted default.

## 8. Build Sequencing (recommended)
1. **Probe first** (R1): empirical Augment-emission capture → lock detection + severity-parse
   constants. *Gate before any parser code.*
2. C1 skill skeleton + `--monitor 0/1` (open PR, poll, report) — no edits, no push.
3. C3 severity router + troubleshoot wiring (level 1 diagnose-only).
4. Level 2 (fix-local + validate + ask).
5. C4 reply-to-thread + resolve, then level 3 + loop-guard (R2) + AC-6 fixture.
6. C5 hook copy update; C6 full test suite; `make sync-dev` + `make verify-sync`.

## 9. Handoff Options (next step — see chat for paste-ready commands)
- **Full adversarial pressure-test** of this spec (independent multi-model divergence).
- **`/sc:tasklist`** to convert §8 into a Sprint-CLI tasklist.
- **`task-builder`** to produce an MDTM task file (domain=architecture → migration-template).
- **`/sc:design`** for the skill's internal architecture.
