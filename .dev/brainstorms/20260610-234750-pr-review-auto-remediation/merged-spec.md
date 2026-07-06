<!-- Provenance: produced by /sc:adversarial; Base: Variant C (haiku:qa); Merge date: 2026-06-11 -->
---
contract_version: "1.0"
artifact: adversarial-merged-spec
topic: "PR Review Auto-Remediation Monitor (V1.0)"
domain: qa
base: variant-3-haiku-qa.md
incorporates: [variant-1-opus-architect.md, variant-2-sonnet-backend.md]
invariant_resolutions: [INV-001, INV-007, INV-009, INV-015, INV-016]
synthesis_mode: adversarial-merge
created: 2026-06-11T00:00:00Z
source_requirements: ./adversarial/merged-requirements.md
---

# Merged Specification: PR Review Auto-Remediation Monitor (V1.0)

<!-- Source: Base (original) — Variant C overview; thesis line preserved -->
> **Spine:** Quality Engineer — edge cases, boundary conditions, test coverage, failure
> scenarios, acceptance-criteria rigor, off-by-one and loop-termination correctness. Every
> requirement maps to a concrete test ID (T-xxx).
> **Grafted:** the architect's capability-ceiling FSM and probe-locked detection seam (Variant A),
> the backend's write-ahead JSONL run-log substrate, failure-mode catalog, and idempotency sets
> (Variant B), and the five Round-3 normative invariant resolutions (INV-001/007/009/015/016),
> adopted verbatim and binding.

---

## 1. Overview / Goals

### 1.1 What this is

<!-- Source: Base (modified) — Variant A §1.1 + §3.2 capability-ceiling framing grafted onto C's list (Change CH-6) -->
A new skill `sc:submit-pr` (+ command `/sc:submit-pr` + a one-line `offer-pr-review.sh` hook edit)
with an in-session Monitor-driven loop that:

1. Opens a PR on `IronbellyOrg/IronClaude` under the existing CLAUDE.md PR-target discipline.
2. Arms an in-session monitor (hosted by the Monitor tool) that polls for the Augment Code GitHub
   App review.
3. Routes findings through severity re-grading, then **verifies each finding grounds in real code
   before remediating** (verify-before-remediate false-positive filter, §4 FR-3.5).
4. Dispatches only verified findings to `/sc:troubleshoot`; unverified findings are reported, never fixed.
5. At higher autonomy ordinals, fixes, validates, pushes, replies, and resolves.
6. Terminates deterministically under a capped, monotonic round counter.

The `--monitor` ordinal (0/1/2/3) is a **capability ceiling on a single state machine** (§5), not
four divergent code paths. There is one FSM; the ordinal is compared at exactly three gates plus one
override (§5.2).

### 1.2 Quality Goals

<!-- Source: Base (original) — Variant C §1.2 -->
- **Deterministic termination** — no infinite remediation loops (loop-guard off-by-one = P0 defect).
- **Zero-regression** — `--monitor 0` behaves identically to today.
- **Autonomy-gate enforcement** — level boundaries proven by behavioral tests, not prose.
- **Fail-safe by default** — unknown severity → Medium; unknown bot → "not detected".
- **Full test coverage** — every FR/NFR/AC has a concrete test; every edge case in §8 has a fixture.

<!-- Source: Variant A (opus:architect) §1.2 + Variant B (sonnet:backend) §Goals — Change CH-6/CH-9 -->
- **Isolation of the unknown** — only `detection-contract.md` knows the Augment emission shape; the
  deterministic core (FSM, router, loop-guard) contains zero `gh`/`git` calls (NFR-6, §7).
- **Recoverability** — the write-ahead JSONL run-log is both audit trail and resume checkpoint;
  every externally visible action is idempotent across crash, resume, and re-arming (§11, §12).

<!-- Source: prior-art-evaluation.md best practice #1 (two-wave verify) — adopted 2026-06-11 -->
- **False-positive resistance** — an external Augment finding must independently ground in real
  code before a remediation session (or a push) is spent on it (verify-before-remediate, §4 FR-3.5).
  No round and no push is ever burned on a hallucinated or stale finding.

### 1.3 Non-goals (V1.0)

<!-- Source: Base (original) — Variant C §1.3, union with A §1.3 / B §Non-goals -->
- Headless / detached execution; GitHub Actions hosting; server-side runner.
- Non-Augment review handling (human reviewers, unknown bots).
- Merge-state mutation (`--approve` / `--request-changes` / merge / branch deletion).
- Any persisted user preference that silently enables level-3 autonomy by default.
- Closure of INV-010 rewording-collision dedup (deferred — see §13 Known Limitations).
- Suggest-**instead-of**-push for trivial fixes. V1.0 posts the applied hunk as a ```` ```suggestion ````
  block for *evidence* only (FR-6.5); replacing an auto-push with a maintainer-applied suggestion (a
  candidate R4 blast-radius reduction) is a future-version design choice, not V1.0 behavior.

---

## 2. Component Inventory (SoT Decomposition)

<!-- Source: Variant A (opus:architect) §2.2 source-tree + §2.3 C1..C6 table — Change CH-8 -->
All components originate under `src/superclaude/`. After **any** edit: `make sync-dev` →
`make verify-sync`. **Never** `git add .claude/<anything-but-settings.json>`.

```
src/superclaude/
├── skills/sc-submit-pr-protocol/
│   ├── SKILL.md                          # C1 — orchestrator: FSM + ordinal gates
│   └── refs/
│       ├── detection-contract.md         # DET — UNKNOWN BOUNDARY, probe-locked constant (R1 gate)
│       ├── state-machine.md              # the FSM spec (§5) — single source for all ordinals
│       ├── severity-routing.md           # C3 — re-grade + tier map; defers to severity-rubric.md
│       ├── augment-poll.md               # C2 — poller contract (interval, timeout, backoff)
│       ├── troubleshoot-dispatch.md      # C3b — finding→/sc:troubleshoot seeding contract
│       ├── thread-reply.md               # C4 — gh api reply + GraphQL resolveReviewThread
│       └── loop-guard.md                 # FR-6 round-counter invariants + run-log schema
│   └── scripts/
│       ├── poll-augment-review.sh        # C2 — single poll → emits one JSON line (Monitor stream)
│       └── reply-resolve-thread.sh       # C4 — REST reply + GraphQL resolveReviewThread wrapper
├── commands/submit-pr.md                 # C1 — /sc:submit-pr command (frontmatter + triggers)
└── hooks/scripts/offer-pr-review.sh      # C5 — EDIT: add sc:submit-pr --monitor mention
tests/submit_pr/                          # C6 — FSM/unit/edge tests + AC fixtures (§6)
```

| ID | Component | Consumes | Produces | Reuse? |
|----|-----------|----------|----------|--------|
| C1 | Orchestrator / FSM (`SKILL.md` + `state-machine.md`) | ordinal, max-rounds, PR# | state transitions | New |
| C2 | Poller (`augment-poll.md` + `poll-augment-review.sh`) | PR#, DET | one JSON event/poll | New |
| **DET** | **Detection contract** (`detection-contract.md`) | R1 probe output | bot-login + emission-shape constant | New (R1-gated) |
| C3 | Severity router (`severity-routing.md`) | raw findings | `{finding, severity, tier}` | **Reuse** `severity-rubric.md` |
| C3a | Verification wave (`finding-verify.md`) | routed findings | `{finding, verification_status}` | New (read-only grounding; reuses `sc-auggie-review` grounding + `sc-troubleshoot` adversarial discipline) |
| C3b | Troubleshoot dispatcher (`troubleshoot-dispatch.md`) | **verified** findings | `/sc:troubleshoot` invocations | New |
| C4 | Reply/resolve helper (`thread-reply.md` + script) | comment_id, SHA | thread reply + resolved thread | New |
| LG | Loop-guard (`loop-guard.md`) | round counter, events | terminate/continue + run-log | New |
| VAL | Validator (in `SKILL.md`) | changed files | pass/fail | Reuse `make` targets |
| C5 | Hook edit (`offer-pr-review.sh`) | — | offer line | **Edit** |
| C6 | Tests (`tests/submit_pr/`) | fixtures | green suite | New |

**Decomposition rule:** C3 (re-grade, pure function), C3a (verify, read-only grounding), and C3b
(dispatch, I/O side effect) are separate refs so C3/C3a are unit-testable with zero subprocess mocking.

---

## 3. Build Sequencing (dependency DAG)

<!-- Source: Variant A (opus:architect) §12 build DAG + §7 probe-first gate — Change CH-8 -->
The ordering is a dependency DAG, not a preference. **DET gates everything.**

```
[0] R1 PROBE → lock detection-contract.md (locked:true)        ◄── HARD GATE (AC-8)
        ▼
[1] C1 SKILL skeleton + state-machine.md + ordinal 0/1 (POLLING, report; no edits)
        ├──► [2] C3 severity-routing.md (reuse rubric) + C3a finding-verify.md (verify-before-remediate) + C3b dispatcher (L1 diagnose-only)
        ▼
[3] L2: VAL gates (VG-1..VG-6) + S3_FIXING + HALT_BEFORE_PUSH
        ▼
[4] C4 thread-reply.md + reply-resolve-thread.sh + L3 S4_PUSHING/S6_REPLYING/RESOLVING
        ▼
[5] LG loop-guard.md + run-log substrate (§11) + AC-6 2-round fixture
        ▼
[6] C5 hook edit + C6 full suite → make sync-dev → make verify-sync
```

**Gate rule:** step 1 cannot begin until `detection-contract.md.locked == true` (§7, AC-8). Steps
2–5 are internal-pure and testable with fixtures (no network). Step 6 is the only step touching
`.claude/`, via `make sync-dev`, never a manual `git add`.

---

## 4. Functional Requirements (Elaborated with Testability Notes)

<!-- Source: Base (original) — Variant C §2, FR IDs preserved verbatim. ID-scheme note below (CH-12/normalization) -->
> **FR ID scheme:** Variant C's `FR-1..FR-7` IDs are canonical and preserved. Variant A's `FR-A1..A10`
> and Variant B's `FR-1..FR-10` map onto them (remap table in §16). No FR is dropped.

### FR-1 — PR submission skill with `--monitor` ordinal

<!-- Source: Base (modified) — Variant C FR-1; signature extended with B's --poll-interval/--timeout/--output-dir/--resume (Change CH-10) -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-1.1 | Signature: `/sc:submit-pr [--monitor {0,1,2,3}] [--max-rounds N] [--poll-interval SECONDS] [--timeout SECONDS] [--base master] [--head <branch>] [--title …] [--body …] [--output-dir <abs-path>] [--resume <abs-run-log-path>]` | T-101: parse --help, verify `--monitor` set {0,1,2,3} via argparse `choices`; T-102: `--max-rounds` default=2, hard cap max=5 (reject >5). |
| FR-1.2 | `--monitor` defaults to 0. | T-103: invoke with no `--monitor`; assert monitor not armed. |
| FR-1.3 | All `gh` calls pin `--repo IronbellyOrg/IronClaude`; every `gh api` path uses `repos/IronbellyOrg/IronClaude/...`. | T-104: static grep over all sources in `src/superclaude/skills/sc-submit-pr-protocol/` + `hooks/` for `gh ` without `--repo`. T-105: runtime mock asserts `--repo` present. |
| FR-1.4 | Pre-PR checks: confirm origin, `gh auth status`, `git fetch origin`, rebase if behind, verify returned URL. | T-106: wrong origin → HALT. T-107: behind `origin/master` → auto-rebase before create. T-108: `gh pr create` returns wrong-owner URL → HALT, instruct operator to close misrouted PR. |
| FR-1.5 | On `--monitor >= 1`, arm Monitor (initialize output-dir, run-log, baseline) after PR URL verification. | T-109: `--monitor 1` → Monitor spawned exactly once; T-110: `--monitor 0` → Monitor never spawned. |
| FR-1.6 | `--poll-interval` minimum 30s — a value below 30 is rejected, not rounded. `--timeout` default 1800s. | T-111: `--poll-interval 10` → reject before arm with "minimum is 30 seconds". T-112: `--timeout 60` honored (see FR-2.3). |
| FR-1.7 | `--resume <run-log-path>` reconstructs state from the JSONL run-log (see §12). | T-113: resume from a JSONL log → state rebuilt (AC-16). |

### FR-2 — In-session Augment review monitor

<!-- Source: Base (original) — Variant C FR-2 -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-2.1 | Poll PR via `gh pr view <N> --repo IronbellyOrg/IronClaude --json number,url,headRefName,headRefOid,baseRefName,reviews,comments` + `gh api …/pulls/<N>/reviews` + `…/comments` (+ `…/commits/<sha>/check-runs` if probe shows checks). | T-201: empty reviews → state = polling. T-202: Augment review, empty findings → state = clean. T-203: Augment review with findings → state = findings. |
| FR-2.2 | Detection contract: three states (no review / clean / findings), classified **only** against the probe-locked `DetectionContract` (§7). Key on the Augment App bot login from the locked constant. | T-210: contract `locked:false` (or absent) → skill HALTs with "probe first" error (R1). T-211: comment from different bot login → "review not detected" (NFR-4). T-212: two comments, one Augment one human → only Augment parsed. |
| FR-2.3 | Poll interval >= 30s; review-wait timeout default 1800s (~30 min), configurable; timeout is wall-clock since entering wait. | T-220: 29s interval → assertion fails. T-221: never-arriving review → timeout fires, state = "never arrived". T-222: `--timeout 60` → fires at 60s. |
| FR-2.4 | Monitor hosted by Monitor tool; session close = monitor lost (documented limitation, mitigated by `--resume`, §12). | T-230: close session mid-poll → run-log records `session_closed`; resume reconstructs (no code assertion beyond logging + resume). |
| FR-2.5 | Backoff on 403/429/secondary-limit: exponential 30→60→120…cap 300s; backoff counts toward timeout (see NFR-2). | T-231: 403 secondary-limit ×2 then success → backoff 30, 60, reset (AC-4). |

### FR-3 — Severity → troubleshoot-tier routing

<!-- Source: Base (original) — Variant C FR-3 -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-3.1 | Re-grade via reused severity rubric; Augment's self-reported severity is a hint, not authoritative. | T-301: `severity_hint=low` but category=security → remap to Critical. T-302: `severity_hint=critical` but `confidence=low` → downgrade to High. |
| FR-3.2 | Route: Medium → `troubleshoot --fix`; High/Critical → `troubleshoot --depth deep --fix`; Low/Nit → report only. | T-310: Medium → `--fix` only. T-311: High → `--depth deep --fix`. T-312: Low → troubleshoot NOT called; recorded in report-only list. |
| FR-3.3 | Seed troubleshoot with finding body + file:line + evidence (so troubleshoot does not re-derive). | T-320: mock troubleshoot receives `scope` containing file:line from finding. |
| FR-3.4 | Batch findings by file/area; never exceed round budget. Route decision appended to run-log before invoking troubleshoot. | T-330: 3 findings same file → single batch. T-331: findings exceed round budget → truncate and HALT with summary. |
| FR-3.5 | **Verify-before-remediate (two-wave grounding filter).** Executes between FR-3.2 (route) and FR-3.3 (dispatch): an independent verification wave (C3a) cross-checks each routed finding against the working-tree code before any `/sc:troubleshoot --fix` session is spent. A finding is `verified` only if its cited `file:line` exists **and** the described defect grounds in / reproduces against the real code; `verified` findings proceed to FR-3.3 dispatch, `unverified` findings are demoted to **report-only** (never auto-remediated, **no round consumed**) with the reason logged. Distinct from the structural ungroundable-drop (missing `file:line` → dropped, §8 EC-9): verification additionally rejects findings whose location exists but whose claimed defect does not reproduce (false positives). The wave fans out across findings in parallel (single batched message). | T-340: finding grounds in real defect → `verification_status=verified` → troubleshoot called. T-341: location exists but no such defect (false positive) → `verification_status=unverified` → troubleshoot NOT called, recorded report-only. T-342: N findings → verification dispatched in parallel (one batched message). |

<!-- Source: prior-art-evaluation.md §"Best practices to EXTRACT from official code-review" #1 (two-wave verify) — adopted 2026-06-11 -->
> **Verify-before-remediate (best practice #1, adopted from the official `code-review` plugin's
> two-wave verify).** The official review orchestrator runs primary scanners, then a *secondary wave
> of independent validators that cross-checks every finding before publishing* — only validated
> findings survive. V1.0 applies the same false-positive filter to the *external* Augment review: a
> routed finding must independently ground in real code before a remediation session is spent on it.
> This reuses the repo's existing grounding discipline (`sc-auggie-review`'s grounding pass and
> `sc-troubleshoot`'s adversarial fix-debate) rather than trusting Augment's findings verbatim, and
> directly attacks **R1** (detection-is-guesswork) and **R4** (auto-push blast radius) by ensuring the
> loop never burns a round — or a push — on a hallucinated or stale finding. The verifier is
> component **C3a** (`finding-verify.md`, §2); it emits `finding_verified` / `finding_unverified`
> run-log events (§11.3) and sits inside the deterministic-core purity boundary (read-only grounding,
> no `gh`/`git` mutation, NFR-6).

### FR-4 — Autonomy gates (capability-ceiling FSM)

<!-- Source: Base (modified) — Variant C FR-4 re-anchored onto Variant A's FSM gates (Change CH-6); CH-2 G-push conjunction inserted -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-4.1 | **Level 1** (`G-arm` only): diagnose + propose. **No edits** (FSM never enters `S3_FIXING`). | T-401: level 1 → zero Write/Edit/NotebookEdit. T-402: emit exact offer prompt "fix these? y/n". |
| FR-4.2 | **Level 2** (`G-edit`): implement fixes + validate locally. HALT before any commit/push/reply (`S3_FIXING → S4'_HALT_BEFORE_PUSH`). Changes left in working tree. | T-410: files modified on disk; T-411: `git push` never called; T-412: `git commit` never called; T-413: reply never posted. |
| FR-4.3 | **Level 3** (`G-push`): implement + validate + commit + push + reply + resolve, loop-guard governed. A push occurs **only if the §5.3 G-push 5-predicate conjunction (INV-016) holds**. | T-420: full end-to-end fixture (AC-2). T-ZERO-EDIT-NO-PUSH: `applied_edits==0` → no push (§5.3 predicate 5). |
| FR-4.4 | `needs_human_decision` findings HALT even at level 3 (override predicate, ignores the ordinal ceiling). | T-430: level 3 + `needs_human_decision` finding → HALT, no push, no reply. |

### FR-5 — Local validation before push

<!-- Source: Base (modified) — Variant C FR-5 reconciled with A §9 VG table + B 5-step order (Change CH-13). Full gate list in §10. -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-5.1 | Validation = the ordered gate list in §10. Targeted tests for changed files; escalate to `make test` when cross-cutting (5+ files / multiple dirs / shared infra / High-Critical broad blast radius). | T-501: single-file change → targeted `uv run pytest tests/path/`. T-502: cross-cutting → `make test`. |
| FR-5.2 | `make lint` AND `uv run ruff format --check src/ tests/` must both pass before push (the known green-lint≠green-CI gotcha). | T-510: lint failure → push blocked. T-511: format failure (lint green) → push blocked. |
| FR-5.3 | Validation fail → no push, no reply, no resolve; report failure; level 3 may retry once **within round budget**, else HALT. Validation retry does NOT increment `round_counter`. | T-520: test failure → no push, `round_counter` NOT incremented (retry within same round). T-521: 3 consecutive validation failures → HALT. |
| FR-5.4 | `validation_status == "validated"` (§10 all-green) is the single precise definition consumed by the §5.3 G-push predicate (2). | T-522: partial-green (lint only) → `validation_status != "validated"` → push blocked. |

### FR-6 — Reply, resolve, and loop termination

<!-- Source: Base (modified) — Variant C FR-6; FR-6.3 round semantics replaced by INV-001 verbatim (Change CH-1); dedup keys per INV-009 (Change CH-4) -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-6.1 | Fix posts a reply on the specific Augment comment thread, summarizing fix + commit SHA + passing validation commands, then resolves the thread. Reply MUST cite `applied_edits` status (§5.4 / INV-009): `applied_edits==0`/ungroundable MUST say "no code change applied", never "resolved". | T-601: reply posted to correct thread ID. T-602: resolve via GraphQL `resolveReviewThread`. T-603: `applied_edits==0` cycle → reply text contains "no code change applied", NOT "resolved". |
| FR-6.2 | Loop-stop: zero Medium+ findings OR `round_counter >= max_rounds` (gate evaluated before opening each fix cycle, §5/§9). | T-610: re-review clean → terminate. T-611: findings but `round_counter >= max_rounds` → terminate with summary. |
| FR-6.3 | **Loop-guard (INV-001, verbatim normative):** `round_counter` = the count of **completed monitor-triggered remediation cycles**; increments by exactly 1 at the single FSM transition `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`; increments **nowhere else** (not on inbound-review detection, diagnosis start, push emission, or validation retry); monotonic — a counted re-review that later vanishes does NOT decrement; gate `round_counter >= max_rounds ⇒ HALT_MAX_ROUNDS` evaluated before opening each fix cycle; user-facing label = `round_counter + 1`; `max_rounds=N` → exactly N pushes. Default 2, hard cap 5. | T-620 through T-629 (§9). T-626 canonical off-by-one; T-VANISHED-MONO irrevocability. |
| FR-6.4 | Max-rounds with residual findings → post summary listing unresolved findings, then hand back. | T-630: residual after max rounds → summary comment with exact list. |
| FR-6.5 | **Posting hygiene (best practice #3).** Replies are posted inline on the finding's source line. When a fix is **trivial** — a single contiguous hunk in a single file, ≤10 changed lines, no cross-file edits — the reply embeds a fenced ```` ```suggestion ```` block reproducing the applied hunk, giving the maintainer a precise, one-click re-applyable diff as evidence; non-trivial fixes carry the prose summary + commit SHA only. A clean re-review posts a **single summary thread**, not one comment per finding. Never duplicate annotations — reply idempotency is the thread-scoped `reply_key` (§11.4 / NFR-1). Gated by `applied_edits > 0`: an `applied_edits==0` cycle never emits a suggestion block (FR-6.1). | T-640: trivial fix → reply contains a ```` ```suggestion ```` block with the applied hunk on the cited line. T-641: non-trivial fix (>10 lines / multi-file) → no suggestion block, prose + SHA only. T-642: clean re-review → exactly one summary thread, not N per-finding comments. |

### FR-7 — Hook integration

<!-- Source: Base (original) — Variant C FR-7 -->
| ID | Requirement | Testability note |
|---|---|---|
| FR-7.1 | `offer-pr-review.sh` additionally mentions `sc:submit-pr --monitor` alongside the existing `/sc:auggie-review` offer. Hook stays fail-open, never spawns a monitor itself, never implies level-3 without explicit invocation. | T-701: hook output contains both `/sc:auggie-review` and `/sc:submit-pr --monitor`. T-702: exits 0 on non-matching input. T-703: exits 0 on failed `gh pr create`. |

---

## 5. State Machine — `--monitor` ordinal as a capability ceiling

<!-- Source: Variant A (opus:architect) §3 FSM + §3.2 gate table — Change CH-6; state names reconciled to R3 lexicon (Change CH-12) -->

### 5.1 The single FSM (all ordinals share it)

There are **not four implementations**. There is one FSM; the ordinal is compared at three gates
plus one override. Canonical state names (R3 lexicon, used verbatim by INV-001/007/016 — see §15
glossary for the A 7-state and B S0..S14 mappings):

```
                    arm(ordinal)
   [S0_IDLE] ──────────────────────────────► [S2_CLASSIFY/POLLING]
                                                │
              no review (interval ≥30s, t<timeout) │ loop back
                                                │◄───────┘
            review, 0 Medium+ ┌────────────────┤ review, ≥1 Medium+
                              ▼                 ▼
                     [TERMINAL_CLEAN]      [S2_CLASSIFY → gate: round_counter>=max_rounds?]
                                                │ False
                                                ▼
                                            [S2b_VERIFY]  ← verify-before-remediate (FR-3.5, C3a)
                                     verified  │   │ all findings unverified
                                                ▼   └──► [REPORT_ONLY] (no troubleshoot, no round consumed)
                                            [S3_DIAGNOSE]  ← /sc:troubleshoot
                                                │
              G-edit: ordinal==1 ┌─────────────┤ ordinal≥2
                                 ▼             ▼
                  [PROPOSED → HALT]      [S3_FIXING] ── needs_human_decision ──► [HALT_HUMAN]
                  (offer y/n, no edits)      │ (worktree edits)
                                             ▼
                                       [S7_VALIDATING] ── fail ──► [VALIDATION_FAIL]
                                             │ pass                  │ retry≤budget / HALT
              G-push: ordinal==2 ┌──────────┤ ordinal==3 ∧ G-push conjunction (§5.3)
                                 ▼           ▼
                  [S4'_HALT_BEFORE_PUSH]  [S4_PUSHING] → [S6_REPLYING] → [RESOLVING]
                  (ask before commit/push)    │
                                              ▼
                                  [S5_AWAITING_REREVIEW]
                                   on review_observed ∧ sha_attributed_to_our_push:
                                      round_counter += 1  → back to [S2_CLASSIFY]
                                   on rounds==max OR 0 Medium+:
                                      → [TERMINAL_*]  (FR-6.4 summary if residual)
```

### 5.2 Ordinal = capability ceiling, not a branch

| Gate | Predicate | L0 | L1 | L2 | L3 |
|------|-----------|----|----|----|----|
| G-arm | `ordinal >= 1` to enter polling | ✗ | ✓ | ✓ | ✓ |
| G-edit | `ordinal >= 2` to enter `S3_FIXING` | — | ✗ (→PROPOSED) | ✓ | ✓ |
| G-push | `ordinal >= 3` **AND §5.3 conjunction** to enter `S4_PUSHING` | — | — | ✗ (→HALT_BEFORE_PUSH) | conditional |

Plus one **override** ignoring the ordinal entirely: `needs_human_decision ⇒ HALT_HUMAN` even at L3
(FR-4.4). The only predicate allowed to short-circuit the ceiling.

**G-verify is a content gate, not an ordinal gate.** The `S2b_VERIFY` filter (FR-3.5) runs at *every*
armed ordinal (L1–L3) on the `S2_CLASSIFY → S3_DIAGNOSE` edge: it guards entry to `S3_DIAGNOSE` on
`verification_status == verified` and routes `unverified` findings to `REPORT_ONLY` without consuming a
round. It is independent of the capability ceiling — even L1 (diagnose-only) verifies before proposing —
so it never appears in the ordinal gate table above. INV-001's increment edge is unchanged: the round
counter still ticks only at `S5_AWAITING_REREVIEW → S2_CLASSIFY`, and the round-budget gate is still
evaluated at `S2_CLASSIFY`; verification merely filters which findings (if any) open the fix cycle.

**L0** is the FSM never leaving `S0_IDLE`: `--monitor 0` opens the PR and returns — byte-for-byte
identical to today (AC-1).

### 5.3 G-push — the 5-predicate runtime conjunction (INV-016, verbatim)

<!-- Source: r3-architect.md §INV-016 (owns) — Change CH-2, adopted verbatim -->
> **INV-016.** A push is authorized at the `S4_PUSHING` transition if and only if ALL of the
> following runtime predicates hold, evaluated as a conjunction immediately before `git push`:
> (1) `monitor_ordinal >= 3`; (2) `validation_status == "validated"` (targeted tests + lint +
> format all green this cycle); (3) `needs_human_decision == false` for every finding in the cycle;
> (4) `round_counter < max_rounds`; (5) the cycle produced at least one grounded, applied edit
> (`applied_edits > 0` — never push an empty or ungroundable-only cycle). If any predicate is false
> the FSM routes to `HALT_*` (HALT_HUMAN for (3), HALT_MAX_ROUNDS for (4), TERMINAL_CLEAN/report for
> (5), report-only for (1)–(2)) and NO push occurs. Every push, authorized or blocked, writes a
> **write-ahead `push_decision` audit record** to the run-log naming which predicates held; this
> record is mandatory at L3 and is the audit primitive (not a per-push interactive prompt). A
> one-time per-run confirmation applies: the FIRST push of a run requires `--yes` OR an interactive
> confirm unless the run is non-interactive, in which case the `push_decision` record + the explicit
> `--monitor 3` arming stands as the recorded authorization.

Predicate (5) closes the "push/announce-resolved with nothing actually changed" hole. The
`push_decision` write-ahead record is the real safety layer (verified by T-ZERO-EDIT-NO-PUSH).

### 5.4 Why a machine and not nested ifs

A nested-if implementation of four levels has 2³ = 8 reachable gate combinations; the bug surface is
every forgotten combination. The FSM has finite states × 3 one-line gate checks, expressible as a
transition table that C6 tests directly (AC-2..AC-6 become table-row assertions).

---

## 6. Test Strategy & Coverage Matrix

<!-- Source: Base (original) — Variant C §4; counts extended for grafted tests (Change CH-14) -->

### 6.1 Test Categories

| Category | Tool | Scope | Count |
|---|---|---|---|
| Unit | pytest | parse, route, **verify-before-remediate**, guard, validate, classifier, **reply suggestion-block formatting** | 42 |
| Integration | pytest + subprocess | hook scripts, skill end-to-end with mocks, parallel verification fan-out, single-summary-thread | 16 |
| Behavioral | pytest | autonomy gates, detection states, loop-guard, FSM transitions | 18 |
| Edge-case | pytest | boundary conditions, malformed input, race | 16 |
| Failure-mode / recovery | pytest | FM-1..12, crash-window resume, idempotency | 12 |
| Static analysis | grep + pytest | `--repo` pin, no relative paths, single-line commands, core purity | 5 |
| Invariant (R3 canonical) | pytest | T-626-OFF-BY-ONE, T-VANISHED-MONO, T-CRASH-WINDOW-NO-DOUBLE-PUSH, T-FRESH-COMMENT-NO-DOUBLE-FIX, T-ZERO-EDIT-NO-PUSH, T-VALIDATED-NOT-VERIFIED | 6 |

**Total: 115 tests.**

### 6.2 Coverage Matrix: Requirement → Test

```
FR-1.1  → T-101, T-102
FR-1.2  → T-103
FR-1.3  → T-104, T-105
FR-1.4  → T-106, T-107, T-108
FR-1.5  → T-109, T-110
FR-1.6  → T-111, T-112
FR-1.7  → T-113
FR-2.1  → T-201, T-202, T-203
FR-2.2  → T-210, T-211, T-212
FR-2.3  → T-220, T-221, T-222
FR-2.4  → T-230
FR-2.5  → T-231
FR-3.1  → T-301, T-302
FR-3.2  → T-310, T-311, T-312
FR-3.3  → T-320
FR-3.4  → T-330, T-331
FR-3.5  → T-340, T-341, T-342
FR-4.1  → T-401, T-402
FR-4.2  → T-410, T-411, T-412, T-413
FR-4.3  → T-420, T-ZERO-EDIT-NO-PUSH
FR-4.4  → T-430
FR-5.1  → T-501, T-502
FR-5.2  → T-510, T-511
FR-5.3  → T-520, T-521
FR-5.4  → T-522
FR-6.1  → T-601, T-602, T-603
FR-6.2  → T-610, T-611
FR-6.3  → T-620..T-629 (§9), T-626-OFF-BY-ONE, T-VANISHED-MONO
FR-6.4  → T-630
FR-6.5  → T-640, T-641, T-642
FR-7.1  → T-701, T-702, T-703
NFR-1   → T-N01, T-N02, T-FRESH-COMMENT-NO-DOUBLE-FIX
NFR-2   → T-N10, T-N11
NFR-3   → T-N20, T-N21, T-N22
NFR-4   → T-N30, T-N31
NFR-5   → T-N40, T-N41
NFR-6   → T-N50 (core purity)
INV-001 → T-626-OFF-BY-ONE, T-VANISHED-MONO
INV-007 → T-CRASH-WINDOW-NO-DOUBLE-PUSH
INV-009 → T-FRESH-COMMENT-NO-DOUBLE-FIX
INV-016 → T-ZERO-EDIT-NO-PUSH
INV-015 → T-VALIDATED-NOT-VERIFIED
AC-1    → T-103, T-110
AC-2    → T-310, T-311, T-420, T-601, T-602, T-610
AC-3    → T-401, T-402
AC-4    → T-410, T-411, T-412, T-413
AC-5    → T-430
AC-6    → T-620..T-629, T-626-OFF-BY-ONE
AC-7    → T-104, T-105
AC-8    → T-210 (locked:false → HALT)
AC-9    → T-N50 (core purity)
AC-10   → T-231 (backoff)
AC-11   → T-113 (resume reconstruction)
AC-12   → T-CRASH-WINDOW-NO-DOUBLE-PUSH (resume idempotency)
AC-13   → T-VALIDATED-NOT-VERIFIED
AC-14   → T-341 (false-positive finding → report-only, no remediation)
AC-15   → T-640, T-642 (suggestion-block + single summary thread)
```

### 6.3 Test File Layout

```
tests/submit_pr/
├── __init__.py
├── conftest.py                          # fixtures: mock_gh, mock_monitor, fixture_findings, tmp_skill_dir
├── test_skill_parse.py                  # T-101..T-103, T-111..T-113: flags, defaults, choices, resume
├── test_pre_pr_checks.py                # T-106..T-108: origin, rebase, URL verification
├── test_monitor_arm.py                  # T-109, T-110, T-230: monitor arming
├── test_detection_contract.py           # T-201..T-203, T-210..T-212: poll states, bot detection, locked gate
├── test_timeout.py                      # T-220..T-222, T-231: interval, timeout, backoff
├── test_severity_router.py              # T-301..T-302, T-310..T-312, T-N30: remap + routing
├── test_finding_verify.py               # T-340..T-342: verify-before-remediate (FR-3.5), parallel fan-out
├── test_troubleshoot_seed.py            # T-320, T-330, T-331: seeding + batching
├── test_autonomy_gates.py               # T-401..T-402, T-410..T-413, T-420, T-430, T-ZERO-EDIT-NO-PUSH
├── test_validation_gate.py              # T-501..T-502, T-510..T-511, T-520..T-522
├── test_loop_guard.py                   # T-620..T-629, T-626-OFF-BY-ONE, T-VANISHED-MONO
├── test_reply_resolve.py                # T-601..T-603, T-610, T-611, T-630, T-640..T-642, T-FRESH-COMMENT-NO-DOUBLE-FIX
├── test_idempotency.py                  # T-N01, T-N02: no double-post
├── test_rate_limit.py                   # T-N10, T-N11: 403 backoff
├── test_run_log.py                      # T-N20..T-N22: JSONL observability
├── test_crash_recovery.py               # FM-1..12, T-CRASH-WINDOW-NO-DOUBLE-PUSH, resume reconstruction
├── test_edge_cases.py                   # EC-1..EC-16: edge-case catalog (§8)
├── test_hook_update.py                  # T-701..T-703
├── test_static_grep.py                  # T-104, T-N40, T-N41, T-N50: static + core-purity checks
├── test_validated_not_verified.py       # T-VALIDATED-NOT-VERIFIED (INV-015 audit)
└── fixtures/
    ├── finding-medium.json
    ├── finding-high.json
    ├── finding-medium-high.json          # AC-2 fixture
    ├── finding-empty.json
    ├── finding-max.json                  # 50 findings (stress)
    ├── finding-duplicate.json
    ├── finding-fresh-comment-id.json      # INV-009: same body+file:line, new comment_id
    ├── finding-needs-human.json
    ├── finding-malformed.json
    ├── finding-ungroundable.json          # applied_edits==0 path (INV-016 predicate 5)
    ├── review-clean.json
    ├── review-with-findings.json
    ├── review-non-augment.json
    ├── review-interleaved.json
    ├── round-sequence-2.json              # AC-6
    ├── round-sequence-residual-x3.json    # T-626 canonical off-by-one
    ├── crash-after-push-before-completed.json  # INV-007 crash window
    └── behavioral-drift.json              # INV-015 validated_not_verified
```

---

## 7. Detection-Contract Design (DET) — the build-gated locked constant

<!-- Source: Variant A (opus:architect) §4.1 + §7 + AC-8/AC-9 — Change CH-7; replaces C's "config constant, not hard-guessed" prose -->

Detection is **configuration, not logic**. FR-2.2's three-state classifier
`classify(gh_payload, DetectionContract) → review_state` is a pure function. The contract is a single
YAML-fronted ref filled by the R1 probe and never guessed:

```yaml
# detection-contract.md — locked by R1 empirical probe (build BLOCKS while locked:false)
augment_bot_login: "<PROBE-LOCKED>"          # e.g. "augment-code[bot]" — NOT hard-guessed
augment_author_association: ["NONE", "CONTRIBUTOR"]
augment_app_slug: "augment-code"
emission_shape: "<review|issue_comment|check_run>"  # which gh surface carries findings
findings_locus: "<reviews[].body|comments[]|check_run.output>"
severity_field_path: "<jsonpath-or-null>"    # Augment's self-reported severity, if any
review_completeness_signal: "<state==COMMENTED|presence-of-summary-marker>"
probe_evidence: "<abs-path to captured gh json>"  # provenance for the lock
locked: false                                 # R1 flips this to true; build BLOCKS while false
```

Consequences:

1. **The parser is generic.** It contains `if login == contract.augment_bot_login`, never a literal
   string. The login lives in data.
2. **One change point on Augment drift.** If Augment moves from review-comments to check-runs,
   `emission_shape` flips and `findings_locus` re-points; no control-flow code changes.
3. **Build-gated (AC-8).** The pre-flight asserts `contract.locked == true` and refuses to arm
   against an unlocked contract — turning R1 from a "should" into a mechanically-enforced sequencing
   dependency (§3 step 0). C's T-210 ("config absent → HALT 'probe first'") is preserved and
   strengthened to a `locked == true` assertion.
4. **Purity seam (AC-9, NFR-6).** No `gh`/`git` token appears in `state-machine.md`,
   `severity-routing.md`, or `loop-guard.md` — protecting the seam from a future maintainer inlining
   a bot-login string (R5 seam-leakage). Tested by T-N50.

---

## 8. Edge-Case & Boundary Catalog

<!-- Source: Base (original) — Variant C §5 (EC-1..EC-16); EC-4 restructured for INV-009 fresh comment_id (Change CH-4) -->
Each edge case has a concrete test, dedicated fixture, and assertion. No edge case is "covered by
other tests."

### EC-1: Empty findings list (T-E01)
Augment review arrives with zero findings → state "clean", loop terminates, zero troubleshoot calls.
Fixture `review-clean.json`. `assert troubleshoot_mock.call_count == 0; assert state == "clean"`.

### EC-2: Single finding (T-E02)
Exactly one Medium → one troubleshoot, one reply, one resolve. Fixture `finding-medium.json`.

### EC-3: Max findings stress (T-E03)
50 findings → batched into N troubleshoot calls without exceeding round budget; overflow → truncate
and HALT (T-331). Fixture `finding-max.json`. `assert troubleshoot_mock.call_count <= max_batch_size`.

### EC-4: Duplicate / fresh-comment_id findings across rounds (T-E04, T-FRESH-COMMENT-NO-DOUBLE-FIX)
<!-- Source: Base (modified) — restructured per INV-009 (Change CH-4): fix-dedup is comment_id-INDEPENDENT -->
Same defect (`body + file:line`) reappears in round 2 under a **new `comment_id`** (Augment
re-reports). Deduplicated by `fix_key = sha256(path + line + finding_body)` — **comment_id-independent**
— so no second fix is computed. A reply MAY be posted on the fresh thread (its `reply_key` is
thread-scoped and unanswered), but MUST cite the prior `applied_edits` status, never falsely say
"resolved". Fixture `finding-fresh-comment-id.json`.
`assert troubleshoot_mock.call_count == 1; assert reply_posted_on_new_thread == True;
assert "resolved" not in reply_text unless status permits`.

### EC-5: Review arrives during a fix (T-E05)
Second poll fires while troubleshoot running → in-flight fix completes; new review queued for next
round, not processed mid-fix. `round_counter == 1` after both polls; `troubleshoot_mock.call_count == 1`.

### EC-6: Timeout fires mid-remediation (T-E06)
Current troubleshoot finishes (no orphaned work); loop terminates; summary posted with partial-fix
state. Run-log records `timeout_during_remediation`.

### EC-7: `needs_human_decision` at every level (T-E07, T-430)
L1: propose + offer. L2: fix locally then HALT. L3: HALT immediately (no fix, no push, no reply).
Fixture `finding-needs-human.json`. L1 `edits==0`; L2 `pushes==0, edits>0`; L3 `edits==0, pushes==0,
halted==True`.

### EC-8: `--max-rounds=0` (T-E08)
"Monitor but never remediate" — gate `0>=0` True at the first fix-cycle edge → HALT before any fix.
Equivalent to level-1 behavior regardless of `--monitor`. Poll fires, findings reported, zero rounds.
`round_counter` never increments past 0; `troubleshoot_mock.call_count == 0`. (Arm-time WARN if
ordinal>=2.)

### EC-9: Malformed Augment payload (T-E09)
Valid bot login but malformed JSON / missing `file:line` → unknown severity → Medium (T-N30), but
missing `file:line` → finding dropped per hallucination contract, reported as "ungroundable" in
run-log. Fixture `finding-malformed.json`. `dropped_count >= 1`, no troubleshoot for ungroundable.

### EC-10: Non-Augment comment interleaved (T-E10)
Human comment + Augment review → human ignored entirely (NFR-4). Only Augment bot login triggers
detection. Fixture `review-interleaved.json`. `human_comment_parsed == False; augment_review_detected
== True`.

### EC-11: Augment bot login not configured (T-E11 = T-210)
Contract `locked:false`/absent (R1 probe not done) → skill HALTs directing user to run the probe
first. `skill_exited_with_error == True`, error contains "probe".

### EC-12: Review arrives then disappears (T-E12)
Detected then gone on next poll → treated as transient; poll continues until timeout. Run-log records
`review_disappeared`. `state` transitions `findings` → `polling`; no troubleshoot.
**Note:** distinct from INV-001 vanished-review monotonicity (§9 T-VANISHED-MONO) — that concerns an
*already-counted* re-review vanishing, which does NOT decrement `round_counter`.

### EC-13: `--monitor 3` with `--max-rounds 5` (upper bound) (T-E13)
Loop runs at most 5 rounds; after round 5 with residual findings, summary posted.
`round_counter <= 5; summary_posted == True if residual`.

### EC-14: Multiple PRs in same session (T-E14)
Second `/sc:submit-pr --monitor 3` → separate monitor state, run-log, round counter. No state leakage.
Two distinct `.jsonl` logs; counters independent.

### EC-15: `gh` CLI not installed (T-E15)
`gh` not on PATH → HALT at Wave 0 with clear error. No partial execution.

### EC-16: `--base` branch does not exist (T-E16)
`--base develop` absent on fork → HALT with error listing available branches; `git ls-remote` called.

---

## 9. Loop-Guard Correctness Tests

<!-- Source: Base (modified) — Variant C §6; INV-1..INV-7 re-derived from the single INV-001 edge (Change CH-1) -->
The loop-guard is the single most critical correctness invariant. An off-by-one here causes infinite
remediation loops. This section re-derives every fence-post from the **single INV-001 increment edge**.

### 9.1 Round Counter Invariants (re-derived under INV-001)

> **Single normative definition (INV-001, verbatim — the ONLY counter definition in this spec):**
> `round_counter` is the count of **completed monitor-triggered remediation cycles**; it increments
> by exactly 1 at the single FSM transition
> `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`, and
> **nowhere else**. The gate `round_counter >= max_rounds ⇒ HALT_MAX_ROUNDS` is evaluated before
> opening each fix cycle (at the `S2_CLASSIFY → S3_DIAGNOSE` edge). The user-facing label is
> `round_counter + 1`. `max_rounds=N` → exactly N pushes.

Derived invariants (each a corollary of the single edge, not an independent definition):

- **INV-1:** `round_counter` starts at 0 (zero completed cycles at arm). The first inbound review is
  round 0; it triggers fix/push #1 but is never itself counted.
- **INV-2:** `round_counter` increments **only** on the `S5 → S2` edge above (one completed cycle =
  fix → push → our-push-attributed re-review).
- **INV-3:** A re-review SHA-attributed to the monitor's own push counts as completing the current
  cycle (the *next* round), never as a fresh independent trigger.
- **INV-4:** `round_counter` is monotonic and irrevocable — a counted re-review that later vanishes
  does NOT decrement (closes INV-014; tested by T-VANISHED-MONO).
- **INV-5:** `round_counter` never exceeds `max_rounds`; the gate uses `>=` (not `>`) — load-bearing,
  C T-626 proves `>` pushes 3 at `max_rounds=2`.
- **INV-6:** Validation failure (T-520) does NOT increment `round_counter` (retry within same round;
  governed by the separate `validation_retry` cap).
- **INV-7:** The "no review yet" poll state and push emission (`S4_PUSHING → S5`) do NOT increment.

### 9.2 Fence-Post Test Matrix (re-derived)

| Test ID | Setup | `--max-rounds` | Rounds | Expected outcome |
|---|---|---|---|---|
| T-620 | findings → fix → re-review clean | 2 | 1 | Terminates: clean |
| T-621 | findings → fix → findings → fix → clean | 2 | 2 | Terminates: clean |
| T-622 | findings → fix → findings → fix → findings | 2 | 2 | Terminates: HALT_MAX_ROUNDS, summary |
| T-623 | 3 cycles to clean | 5 | 3 | Terminates: clean |
| T-624 | findings × 5 | 5 | 5 | Terminates: HALT_MAX_ROUNDS, summary |
| T-625 | clean immediately | 2 | 0 | Terminates: clean, zero rounds |
| T-626 | residual ×3 at max 2 | 2 | 2 | **Canonical:** `round_counter == 2` NOT 3; exactly 2 pushes; no round-3 fix pushed |
| T-627 | `--max-rounds 1`, findings→fix→findings | 1 | 1 | Terminates: HALT_MAX_ROUNDS, summary |
| T-628 | `--max-rounds 0` (EC-8) | 0 | 0 | Terminates: no rounds, report-only |
| T-629 | findings→fix→validation fails→retry→fix→clean | 2 | 1 | Terminates: clean; validation retry did NOT consume a round |

### 9.3 Canonical Invariant Tests (R3, verbatim)

**T-626-OFF-BY-ONE** (INV-001 fence-post). Fixture `round-sequence-residual-x3.json`,
`arm_findings=3, max_rounds=2`. After cycle #1 attributed re-review: `round_counter==1`, gate `1>=2`
False → cycle #2. After cycle #2 attributed re-review: `round_counter==2`, gate `2>=2` True →
`HALT_MAX_ROUNDS`. `assert round_counter == 2; assert push_count == 2; assert state == HALT_MAX_ROUNDS`.

```python
def test_loop_guard_off_by_one_at_max_2(mock_skill_env):
    fixture = load_fixture("round-sequence-residual-x3.json")
    result = run_skill("--monitor 3 --max-rounds 2", fixture)
    assert result.round_counter == 2, f"Expected 2, got {result.round_counter}"
    assert result.push_count == 2, f"Expected 2 pushes, got {result.push_count}"
    assert result.reply_count == 2
    assert result.summary_posted == True
    assert third_fix_not_applied(result)
```

**T-VANISHED-MONO** (INV-001 irrevocability). Same as T-626 through HALT, then the `sha2` re-review is
dismissed (404/empty). `round_counter` remains exactly 2; FSM stays `HALT_MAX_ROUNDS`; no re-entry to
`S3_DIAGNOSE`. `assert round_counter == 2; assert state == HALT_MAX_ROUNDS; assert troubleshoot_mock.call_count == 2`.

---

## 10. Validation Gates (reconciled ordered list)

<!-- Source: Variant A (opus:architect) §9 VG table + Variant B (sonnet:backend) §Validation Gates 5-step + Variant C FR-5/§10 — Change CH-13 -->
Before any level-3 push or thread resolution, validation runs in this exact order. All-green ⇒
`validation_status == "validated"` (the single definition consumed by §5.3 G-push predicate (2)).

| # | Gate | Command | Blocks | Test |
|---|------|---------|--------|------|
| VG-1 | Targeted tests | `uv run pytest tests/<changed-area>/ -v` | push | T-501 |
| VG-2 | Cross-cutting escalation | `make test` (`uv run pytest`) when ≥2 packages / shared infra / hooks / CLI parsing / run-log FSM touched, or High/Critical broad blast radius | push | T-502 |
| VG-3 | Lint | `make lint` (`ruff check`) | push | T-510 |
| VG-4 | Format | `uv run ruff format --check src/ tests/` | push | T-511 |
| VG-5 | Sync (skill self-edits only) | `make verify-sync` | commit | — |
| VG-6 | PR-target | URL == `IronbellyOrg/IronClaude` | arm | T-108 |

VG-3 and VG-4 are **both** mandatory — the memory note "`make lint` ≠ CI ruff format" is encoded as
two distinct gates so green lint alone cannot authorize a push (T-511, the known gotcha).

### 10.1 No-push-on-failure
Any required gate exits non-zero → append `validation_completed{status:"failed"}`; do not commit
(if none yet), push, reply-as-fixed, or resolve. L2 halts. L3 may attempt one correction only if
`round_counter < max_rounds`; otherwise HALT with residual findings + validation details. The
validation retry does NOT increment `round_counter` (INV-6 / T-520).

### 10.2 Commit and push gate
<!-- Source: Variant B (sonnet:backend) §Commit and push gate — Change CH-13 -->
L3 may commit and push only if: the working-tree diff corresponds to the current round's findings;
required validation passed after the final diff; no `needs_human_decision` finding is active; the
branch is still the PR head branch; the push target is `origin`, never `upstream`; **and the §5.3
G-push 5-predicate conjunction holds.** Commit message convention includes the co-author trailer
`Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

## 11. Run-Log Substrate (write-ahead JSONL + snapshot cache)

<!-- Source: Variant B (sonnet:backend) §Idempotency & Run-log Schema — Change CH-9; replaces C's thin NFR-3 -->

### 11.1 Authority rule
The append-only `.jsonl` run-log is **authoritative**; `state.snapshot.json` is a materialized cache.
If snapshot and JSONL disagree, **rebuild from JSONL** (NFR-6). Every state transition appends a
`state_transition` event, and every external action is preceded by a **write-ahead** record fsynced
before the side effect.

### 11.2 Locations
```text
<output-dir>/monitor-run-<PR_NUMBER>.jsonl        # authoritative event log
<output-dir>/state.snapshot.json                  # materialized cache (rebuildable)
<output-dir>/findings.latest.json                 # latest normalized finding set
<output-dir>/validation/round-<N>/                # stdout/stderr + exit codes
<output-dir>/troubleshoot/round-<N>/              # troubleshoot prompts/outputs
```
Default `<output-dir>` = `/config/workspace/IronClaude/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/`
unless `--resume` supplies an existing log.

### 11.3 Event envelope & types
Each line is valid JSON (`schema_version`, `event_id` unique+monotonic, `event_type`, `timestamp`,
`run_id`, `pr{repo,number,url,base,head}`, `state_before`, `state_after`, `round_index`/`round_counter`,
`payload`). Required event types:

```
run_started · environment_check · pr_create_attempted · pr_created · monitor_armed ·
baseline_captured · poll_attempt · poll_result · api_backoff · classifier_unknown_shape ·
review_detected · findings_normalized · finding_verified · finding_unverified · round_incremented · route_decision ·
troubleshoot_started · troubleshoot_completed · fix_applied · validation_started ·
validation_completed · push_decision · push_initiated · push_completed · reply_posted ·
thread_resolved · idempotency_skip · terminal_clean · terminal_timeout · terminal_max_rounds ·
terminal_halted · terminal_failed
```
`push_decision`, `push_initiated`, `push_completed` are the write-ahead push triad (§12.1).
T-N20..T-N22 assert log existence, per-event timestamp+round+state, and JSONL validity.

### 11.4 Idempotency sets (5 durable sets)
<!-- Source: Variant B (sonnet:backend) §Idempotency keys — Change CH-11; processed_finding_ids keyed on CH-4 fix_key -->
Maintained in materialized state; `idempotency_skip` appended when an action is skipped:

- `processed_review_ids` — prevents re-processing the same Augment review emission.
- `processed_finding_ids` — **keyed on `fix_key = sha256(path + line + finding_body)`**
  (comment_id-independent, per INV-009 / §5.4); prevents applying a fix twice.
- `replied_comment_ids` — prevents duplicate thread replies (thread-scoped `reply_key`).
- `resolved_thread_ids` — prevents duplicate resolution calls.
- `pushed_commit_shas` — the SHA set INV-001 attributes re-reviews against (§9 / §12.1).

---

## 12. Failure Modes & Recovery

<!-- Source: Variant B (sonnet:backend) §Failure Modes (FM-1..12) + INV-007 crash-window (Change CH-10, CH-3) -->
Complementary to §8 (edge cases): the FM catalog adds **recovery** semantics. `--resume <run-log-path>`
is a first-class path.

### 12.1 Write-ahead push ordering & crash-window resume (INV-007, verbatim)
<!-- Source: r3-backend.md §INV-007 (owns) — Change CH-3, adopted verbatim -->
> Ordered sequence per authorized push: `push_decision{run_id, cycle_id, round_counter, predicates,
> authorized:true, pre_push_sha, target_branch, target_remote}` (fsync) → compute `target_sha` →
> `push_initiated{run_id, cycle_id, idempotency_key, pre_push_sha, target_sha, target_branch,
> target_remote, remote_ref}` (fsync **before** `git push`) → `git push <target_remote>
> <target_sha>:<target_branch>` → `push_completed{...pushed_at}` (fsync). Enter
> `S5_AWAITING_REREVIEW`; only a re-review attributed to a recorded `push_initiated.target_sha` may
> complete the cycle and tick `round_counter`. Idempotency key =
> `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` (PRE-push SHA, not post-hoc).

**Crash-window resume rule.** On `--resume`, if the latest event for an idempotency key is
`push_initiated` with no matching `push_completed`, the monitor MUST NOT create another commit or push
until it queries the remote for `target_sha`:
- reachable from the remote branch tip ⇒ append `push_completed{recovered:true}`, resume in
  `S5_AWAITING_REREVIEW`;
- not reachable (remote still at `pre_push_sha` / lacks the commit) ⇒ append
  `push_aborted_or_not_landed{recovered:true}`, return to the pre-push path for the same cycle
  **without recomputing the fix**;
- ambiguous (tip moved to unrelated SHA) ⇒ `HALT_HUMAN` with the original fields + observed remote SHA.

Verified by **T-CRASH-WINDOW-NO-DOUBLE-PUSH**: `assert push_executor.push_count == 2;
assert resume_state == S5_AWAITING_REREVIEW; assert push_completed.recovered == True`.

### 12.2 FM catalog
| FM | Trigger | Action | Recovery |
|----|---------|--------|----------|
| FM-1 | Review never arrives | `terminal_timeout`, no edits/push | `--resume` re-arm |
| FM-2 | Primary/secondary rate limit | `api_backoff`, exp backoff to 300s, continue to timeout | none unless timeout |
| FM-3 | Unknown Augment emission shape | `classifier_unknown_shape`, keep polling | add fixture before parser change |
| FM-4 | Unknown bot identity | ignore as no-review | re-probe + update DET constant |
| FM-5 | Validation failure | no push/reply/resolve; L2 halt; L3 one retry if in budget | inspect artifacts, resume |
| FM-6 | Crash after push before reply | resume: no re-fix; post missing replies once, then resolve | automatic via idempotency sets |
| FM-7 | Crash after reply before resolve | resume: resolve only missing thread, no duplicate reply | automatic |
| FM-8 | Duplicate review / poll payload | `idempotency_skip`; no route/fix/reply | none |
| FM-9 | Round cap with residual findings | `terminal_max_rounds`; optional L3 summary comment; no further fix | user re-runs with higher `--max-rounds` (≤5) |
| FM-10 | `needs_human_decision` finding | `terminal_halted`; no auto-mutation | user provides decision; resume |
| FM-11 | Misrouted PR URL | `terminal_failed`; do not monitor; instruct close | recreate with `--repo IronbellyOrg/IronClaude` |
| FM-12 | Corrupt run-log / snapshot | `terminal_failed`; require explicit recovery point | user picks last valid event ID; no guessing |

---

## 13. Non-Functional Requirements

<!-- Source: Base (original) — Variant C §3; NFR-6 core-purity added from A §6 (Change CH-7) -->
| ID | Requirement | Testability note |
|---|---|---|
| NFR-1 | Idempotent replies/resolves across crash, resume, duplicate polls, re-arming. Fix-dedup keyed on comment_id-independent `fix_key`; reply-dedup thread-scoped (§5.4 / §11.4). | T-N01: replay findings twice → reply once per thread. T-N02: reply-tracking persisted across polls. T-FRESH-COMMENT-NO-DOUBLE-FIX. |
| NFR-2 | Rate-limit safety: poll >= 30s; exponential backoff 30→60→120…cap 300s on 403/429/secondary-limit; backoff counts toward timeout. | T-N10: 403 → backoff 60s next poll. T-N11: 403 ×3 → bounded exponential. |
| NFR-3 | Observability = resumability: write-ahead JSONL run-log (§11) is both forensic record and resume checkpoint. | T-N20..T-N22 (§11.3). |
| NFR-4 | Fail-safe defaults: unknown severity → Medium; unknown/absent bot → "review not detected"; unknown emission shape → logged + ignored until timeout. | T-N30: unrecognized severity → Medium. T-N31: `github-actions[bot]` → ignored, stays "polling". |
| NFR-5 | All paths absolute in user-facing prompts; paste-ready commands single-line. | T-N40: scan stdout for relative paths → none. T-N41: no multi-line paste-ready commands. |
| NFR-6 | Purity of the deterministic core: FSM, router, loop-guard contain zero `gh`/`git` calls; all I/O isolated to poller/dispatcher/helper/validator. | T-N50: static — no `gh`/`git` token in `state-machine.md`, `severity-routing.md`, `loop-guard.md` (AC-9). |
| NFR-7 | Security: authenticated `gh` + local git only; no tokens in run-log; redact credential-bearing env/stderr. | T-N51: run-log scrubbed of token patterns. |
| NFR-8 | Determinism: same fixtures + same initial state → deterministic classifier, counter, routes, terminal outcome. | T-N52: replay → identical run-log decisions. |

### 13.1 Known Limitations

<!-- Source: r3-qa.md §INV-015 (owns, ADDRESSED-via-accepted-risk) — Change CH-5, adopted verbatim -->
> **INV-015 (validated-not-verified).** Validation authorizes a push within this gated envelope; it is
> NOT a correctness guarantee. A fix that passes targeted tests may break untested behaviors. Such
> pushes are recorded as `validated_not_verified` in the run-log (with the list of detected
> behavioral-test failures). Operators should maintain a comprehensive behavioral test suite to
> minimize this residual risk.

This is irreducible residual risk, bounded — not eliminated — by `max_rounds` (§9) and the §5.3
`applied_edits > 0` predicate. Audited by **T-VALIDATED-NOT-VERIFIED**: `assert push_executor.push_count
== 1; assert run_log_entry.validation_status == "validated_not_verified"; assert
len(run_log_entry.behavioral_test_failures) == 1`.

The §4 FR-3.5 verify-before-remediate gate further **reduces** (does not eliminate) this residual on the
*input* side: a false-positive Augment finding that does not ground in real code is filtered out before
any fix is attempted, so it can never reach a push. INV-015 remains the residual for findings that are
genuine *and* verified but whose fix drifts an untested behavior.

> **INV-010 (rewording-collision dedup) — DEFERRED.** Fix-dedup on `body + file:line` (§5.4) does not
> catch a reworded restatement of the same defect under a different body. A secondary near-duplicate
> detector or human-review fallback is out of V1.0 HIGH-closure scope (per `r3-backend.md`). Noted,
> not built.

---

## 14. Autonomy-Gate Behavioral Tests

<!-- Source: Base (original) — Variant C §7; assertions re-anchored onto FSM transitions (Change CH-6) -->

### 14.1 Level 1: Zero Edits Guarantee (T-401, T-402)
```python
def test_level1_zero_edits(mock_skill_env):
    result = run_skill("--monitor 1", load_fixture("finding-medium-high.json"))
    assert result.tool_calls_by_name("Write") == 0
    assert result.tool_calls_by_name("Edit") == 0
    assert result.tool_calls_by_name("NotebookEdit") == 0
    assert not any("git commit" in c for c in result.bash_commands)
    assert not any("git push" in c for c in result.bash_commands)
    assert "fix these? y/n" in result.stdout
    # FSM: never enters S3_FIXING (G-edit blocked at ordinal 1)
    assert "S3_FIXING" not in result.states_visited
```

### 14.2 Level 2: Zero Pushes Without Approval (T-410..T-413)
```python
def test_level2_fixes_but_no_push(mock_skill_env):
    result = run_skill("--monitor 2", load_fixture("finding-medium-high.json"))
    assert result.files_modified_count > 0
    assert result.validation_ran == True
    assert result.push_count == 0
    assert result.commit_count == 0
    assert result.reply_count == 0
    # FSM: reaches S4'_HALT_BEFORE_PUSH (G-push blocked at ordinal 2)
    assert "S4'_HALT_BEFORE_PUSH" in result.states_visited
```

### 14.3 Level 3: HALT on needs_human_decision (T-430)
```python
def test_level3_halts_on_human_decision(mock_skill_env):
    result = run_skill("--monitor 3", load_fixture("finding-needs-human.json"))
    assert result.tool_calls_by_name("Edit") == 0
    assert result.push_count == 0
    assert result.reply_count == 0
    assert result.halted == True
    assert result.halt_reason == "needs_human_decision"   # override predicate, not the ordinal
```

### 14.4 Level 3: G-push zero-edit block (T-ZERO-EDIT-NO-PUSH)
```python
def test_gpush_blocks_on_zero_applied_edits(mock_skill_env):
    # Cycle produces zero grounded edits; tests pass trivially.
    result = run_skill("--monitor 3 --max-rounds 2", load_fixture("finding-ungroundable.json"))
    assert result.push_count == 0                         # predicate (5) applied_edits>0 False
    assert "resolved" not in result.announcements
    assert result.push_decision.authorized == False
    assert result.push_decision.predicate_5_applied_edits == 0
```

### 14.5 Level 3: Full End-to-End (T-420 = AC-2)
```python
def test_level3_full_remediation_flow(mock_skill_env):
    result = run_skill("--monitor 3 --max-rounds 2", load_fixture("finding-medium-high.json"))
    assert result.troubleshoot_count == 2
    assert any("--depth deep" in c for c in result.troubleshoot_calls)  # High → deep
    assert result.validation_ran == True
    assert result.reply_count == 2
    assert result.resolve_count == 2
    assert result.round_counter <= 2
    assert result.terminated == True
```

---

## 15. Detection-Contract State Tests

<!-- Source: Base (original) — Variant C §8 -->

### 15.1 State: No Review Yet (T-201)
```python
def test_detection_no_review(mock_gh):
    mock_gh.pr_view_returns({"reviews": [], "comments": []})
    state = poll_augment_review(pr_num=42)
    assert state == "polling"; assert state.findings == []
```

### 15.2 State: Clean Review (T-202, T-E01)
```python
def test_detection_clean_review(mock_gh):
    mock_gh.pr_view_returns(review_from_augment_bot(findings=[]))
    state = poll_augment_review(pr_num=42)
    assert state == "clean"; assert state.terminated == True
```

### 15.3 State: Findings Review (T-203)
```python
def test_detection_findings_review(mock_gh):
    mock_gh.pr_view_returns(review_from_augment_bot(
        findings=[{"severity": "Medium", "file": "src/foo.py", "line": 42}]))
    state = poll_augment_review(pr_num=42)
    assert state == "findings"; assert state.findings[0].remapped_severity == "Medium"
```

### 15.4 Fail-Safe: Non-Augment Bot (T-211, T-N31)
```python
def test_detection_non_augment_bot(mock_gh):
    mock_gh.pr_view_returns(review_from_bot("github-actions[bot]", findings=[]))
    assert poll_augment_review(pr_num=42) == "polling"
```

### 15.5 Fail-Safe: Unknown Severity (T-N30)
```python
def test_severity_unknown_defaults_to_medium():
    finding = {"severity": "super_urgent", "file": "src/foo.py", "line": 1}
    assert remap_severity(finding).remapped_severity == "Medium"
```

### 15.6 FSM State Glossary (canonical R3 lexicon ↔ A/B states)

<!-- Source: integration glue (Change CH-12) — R3 names canonical; A 7-state + B S0..S14 mapped -->
The R3 names (used verbatim by INV-001/007/016) are canonical. No section references an orphan state.

| Canonical (R3) | Variant A (7-state) | Variant B (S0..S14) | Meaning |
|---|---|---|---|
| `S0_IDLE` | IDLE | S0_INIT | parsed; no PR action / L0 returns here |
| `S1_PR_CREATED` | (precondition, pre-arm) | S1_PR_CREATED | PR URL verified |
| `S2_CLASSIFY` (a.k.a. POLLING entry) | POLLING | S2_MONITOR_ARMED / S3_WAITING_FOR_REVIEW / S4_REVIEW_CLASSIFIED | poll + classify; gate evaluated here |
| `S3_DIAGNOSE` | DIAGNOSING | S5_DIAGNOSING | route Medium+ to troubleshoot |
| `S3_FIXING` | FIXING | S6_FIXING | apply worktree edits (G-edit) |
| `S7_VALIDATING` | VALIDATING | S7_VALIDATING | run §10 gates |
| `S4'_HALT_BEFORE_PUSH` | HALT_BEFORE_PUSH | (L2 halt) | L2 stop before commit/push |
| `S4_PUSHING` | PUSHING | S8_PUSHING | G-push conjunction → commit + push |
| `S6_REPLYING` / RESOLVING | REPLYING / RESOLVING | S9_REPLYING_RESOLVING | idempotent reply + resolve |
| `S5_AWAITING_REREVIEW` | AWAIT_REREVIEW | (post-push wait) | the single `round_counter++` edge origin |
| `TERMINAL_CLEAN` | TERMINATED_CLEAN | S10_TERMINAL_CLEAN | zero Medium+ |
| `HALT_MAX_ROUNDS` | TERMINATED (max) | S11_TERMINAL_MAX_ROUNDS | round cap with residual |
| `TERMINAL_TIMEOUT` | TERMINATED (timeout) | S12_TERMINAL_TIMEOUT | review never arrived |
| `HALT_HUMAN` | HALT_HUMAN | S13_TERMINAL_HALTED | needs_human_decision / validation halt |
| `TERMINAL_FAILED` | (failure) | S14_TERMINAL_FAILED | unrecoverable / corrupt-log |

---

## 16. Acceptance Criteria (superset, testable)

<!-- Source: Base (original) Variant C AC-1..AC-7 + Variant A AC-8/AC-9 + Variant B AC-1..AC-16 + R3 canonical tests — Change CH-14 (append/superset) -->
> **AC ID scheme:** C's `AC-1..AC-7` are canonical and preserved verbatim. A's build/purity ACs and
> B's resume/backoff/idempotency ACs are appended as `AC-8..AC-13`. The 6 R3 canonical tests bind to
> INV-001/007/009/015/016 in §6.2.

| ID | Criterion | Verification |
|---|---|---|
| AC-1 | `--monitor 0` → PR opens, FSM never leaves `S0_IDLE`, zero monitor activity | T-103 + T-110 |
| AC-2 | 1 Medium + 1 High → 2 troubleshoot sessions, 2 fixes, 2 replies, 2 resolves, ≤max-rounds, deterministic termination | T-420 |
| AC-3 | Level-1 run makes zero file edits, emits offer prompt verbatim | T-401 + T-402 |
| AC-4 | Level-2 run leaves changes in working tree, zero pushes | T-410..T-413 |
| AC-5 | `needs_human_decision` HALTs at level 3 | T-430 |
| AC-6 | Loop never exceeds `--max-rounds`; re-review increments same counter; off-by-one verified | T-620..T-629, T-626-OFF-BY-ONE |
| AC-7 | Every `gh` call carries `--repo IronbellyOrg/IronClaude`; every `gh api` uses `repos/IronbellyOrg/IronClaude/...` | T-104 (static) + T-105 (runtime) |
| AC-8 (A) | `detection-contract.md` `locked:false` → skill refuses to arm, reports R1 gate | T-210 |
| AC-9 (A) | No `gh`/`git` token in `state-machine.md` / `severity-routing.md` / `loop-guard.md` (core purity) | T-N50 |
| AC-10 (B) | 403 secondary-limit ×2 then success → backoff 30, 60, reset; never polls below interval | T-231 |
| AC-11 (B) | Given JSONL log + absent snapshot, `--resume` rebuilds processed reviews/findings, replied comments, resolved threads, pushed commits, round index, terminal status | T-113 |
| AC-12 (B) | Crash after push before `push_completed` → resume posts no duplicate push; idempotent reply/resolve | T-CRASH-WINDOW-NO-DOUBLE-PUSH |
| AC-13 (R3/INV-015) | Validated fix that drifts an untested behavior → push occurs, run-log records `validated_not_verified` + behavioral-test failures | T-VALIDATED-NOT-VERIFIED |
| AC-14 (verify-before-remediate) | A routed finding whose cited location exists but whose defect does not reproduce → `verification_status=unverified`, `/sc:troubleshoot` NOT called, finding recorded report-only, no round consumed | T-341 |
| AC-15 (posting hygiene) | A trivial fix (≤10-line single-file hunk) → reply embeds a ```` ```suggestion ```` block of the applied hunk; a clean re-review → exactly one summary thread, no per-finding duplication | T-640, T-642 |

---

## 17. Risks & Mitigations

<!-- Source: Base (original) — Variant C §12; R4 row updated per INV-015/INV-016 (Change CH-2/CH-5); R-seam from A (Change CH-7) -->
| Risk | Severity | Mitigation | Test |
|---|---|---|---|
| **R1: Augment bot login unknown** | P0 | `detection-contract.md` `locked:false` is a hard build gate (§7); skill HALTs; R1 probe is build step 0 | T-210, T-E11 |
| **R2: Loop-guard off-by-one** | P0 | Single INV-001 increment edge (§9); exhaustive fence-post matrix; T-626 canonical; `>=` gate | T-620..T-629, T-626-OFF-BY-ONE |
| **R3: Session-close mid-remediation** | P1 | Write-ahead run-log (§11) = resume checkpoint; `--resume` first-class (§12); documented V1 limitation | T-CRASH-WINDOW-NO-DOUBLE-PUSH, T-N20..T-N22 |
| **R4: Auto-push blast radius** | P1 | §4 FR-3.5 verify-before-remediate filters false-positive findings before any fix; §5.3 G-push 5-predicate conjunction (incl. `applied_edits>0`); human-decision HALT; `max_rounds=2` default; `push_decision` audit; INV-015 known-limitation (NOT a correctness guarantee) | T-341, T-ZERO-EDIT-NO-PUSH, T-510, T-511, T-430, T-VALIDATED-NOT-VERIFIED |
| **R5: Duplicate findings cause double-reply/fix** | P2 | comment_id-independent `fix_key` + thread-scoped `reply_key` (§5.4); 5 idempotency sets (§11.4) | T-N01, T-N02, T-FRESH-COMMENT-NO-DOUBLE-FIX |
| **R6: Review arrives during fix** | P2 | Monitor queues re-review for next round; no concurrent troubleshoot | T-E05 |
| **R7: Timeout mid-remediation** | P2 | Current fix completes; summary with partial state | T-E06 |
| **R8: `make lint` green but format fails** | P2 | VG-3 + VG-4 both required (§10) | T-511 |
| **R9: Non-Augment comment false detection** | P2 | Bot-login guard from locked DET (§7); unknown bot → not detected | T-E10, T-N31 |
| **R10: Malformed Augment payload** | P3 | Grounding failure → finding dropped, not downgraded | T-E09 |
| **R11: Seam leakage** | P2 | AC-9 core-purity static test (§7); no raw login string in deterministic core | T-N50 |
| **R12: Run-log corruption** | P2 | JSONL authoritative + monotonic event IDs; snapshot is cache; fail-closed recovery (FM-12) | T-crash-recovery (FM-12) |
| **R13: False-positive Augment finding triggers wasted/harmful remediation** | P1 | §4 FR-3.5 two-wave verify-before-remediate (C3a): finding must ground/reproduce in real code before a `troubleshoot --fix` session is spent; unverified → report-only, no round, no push (best practice #1, prior-art eval) | T-340, T-341 |

---

## 18. Test Execution Strategy

<!-- Source: Base (original) — Variant C §13 -->
### 18.1 CI Integration
```bash
uv run pytest tests/submit_pr/ -v --cov=superclaude.skills.sc-submit-pr-protocol
```

### 18.2 Test Markers
| Marker | Tests | Purpose |
|---|---|---|
| `@pytest.mark.unit` | T-101..T-331, T-N01..T-N52 | Fast, no I/O |
| `@pytest.mark.integration` | T-401..T-630, EC-1..EC-16, FM-1..12 | Mocked gh API, subprocess hooks |
| `@pytest.mark.loop_guard` | T-620..T-629, T-626-OFF-BY-ONE, T-VANISHED-MONO | Fence-post (every PR) |
| `@pytest.mark.autonomy` | T-401..T-430, T-ZERO-EDIT-NO-PUSH | Autonomy gates (every PR) |
| `@pytest.mark.recovery` | T-CRASH-WINDOW-NO-DOUBLE-PUSH, FM-6/7/12 | Crash-window + idempotent resume |
| `@pytest.mark.p0` | T-626-OFF-BY-ONE, T-430, T-210, T-511, T-ZERO-EDIT-NO-PUSH, T-CRASH-WINDOW-NO-DOUBLE-PUSH | Critical-path (fail-fast) |

### 18.3 Mock Strategy
All external dependencies mocked at the boundary: `gh` CLI via subprocess mock (pre-built JSON
fixtures); Monitor tool via callback firing poll events on a controlled timeline; `/sc:troubleshoot`
via function mock (asserts flags + seeded context); file system via `tmp_path` (no real repo
mutation); remote-reachability query (INV-007 resume) via mock returning reachable/not-reachable/
ambiguous.

### 18.4 Fixture Authenticity
Fixtures derive from the R1 empirical probe once completed. Until then they are synthetic but follow
the expected GitHub API response schema; a schema-validation test asserts parity after the probe
regenerates them from real data.

---

## 19. SoT & PR-Target Discipline (binding constraints)

<!-- Source: Variant A (opus:architect) §13 + Variant B (sonnet:backend) FR-10 — Change CH-8 -->
1. All component edits originate in `src/superclaude/`; `make sync-dev` regenerates `.claude/`;
   `make verify-sync` confirms parity before commit. **Never** `git add .claude/<not settings.json>`;
   an `-f` on a `.claude/` path is the violation siren — stop.
2. Every `gh` call pins `--repo IronbellyOrg/IronClaude`; `gh pr create` without `--repo` is forbidden
   (gh defaults to upstream). PRs target the fork; push target is `origin`, never `upstream`.
3. Any `skill-creator` eval workspace goes to `.dev/eval-workspaces/sc-submit-pr/`, never
   `.claude/skills/*-workspace/`.

---

## 20. QA-Specific Design Decisions

<!-- Source: Base (modified) — Variant C §14; QD-5 replaced by INV-009 two-key scheme (Change CH-4) -->
- **QD-1:** Validation failure does NOT increment `round_counter` (INV-6; the retry is within the same
  round). Tested T-520/T-629.
- **QD-2:** `--max-rounds=0` is valid — "monitor and report but never remediate" (gate `0>=0` True at
  the first fix-cycle edge). Tested T-E08/T-628.
- **QD-3:** Review *disappearance before counting* is transient (continue polling, EC-12); a *counted*
  re-review vanishing is irrevocable (INV-4 / T-VANISHED-MONO). These are distinct cases.
- **QD-4:** T-626-OFF-BY-ONE is the single most important test; runs `@pytest.mark.p0` every PR; its
  assertion messages are diagnostic (`Expected 2 pushes, got 3`).
- **QD-5 (REPLACED per INV-009):** Dedup uses **two keys**, not one — fix-dedup `fix_key =
  sha256(path + line + finding_body)` is **comment_id-independent**; reply/resolve-dedup `reply_key` is
  thread-scoped (includes comment_id/thread_id + fix_key + reply_purpose). A fresh `comment_id` for the
  same defect reuses the fix record (no second fix); a reply MAY post on the fresh thread but MUST cite
  `applied_edits` status and never falsely say "resolved". Tested T-FRESH-COMMENT-NO-DOUBLE-FIX.
  (C's original single-key "keyed on comment_id" scheme was correct for reply scope but insufficient
  for fix-dedup.)
- **QD-6:** Severity rubric is tested independently from the skill (`test_severity_router.py`) with all
  category-to-severity mappings + confidence + diff-locality adjustments — a pure unit test.
