---
QA Phase: research-gate
Date: 2026-06-12
Tier: heavyweight
Analyst report: NOT FOUND — full 11-item checklist applied independently
Verdict: PASS
Exit recommendation: CONTINUE
---

# QA Research-Gate Report — PR Auto-Remediation V2.0 PRD

> **Gate:** research-gate (pre-synthesis)
> **Tier:** heavyweight
> **Date:** 2026-06-12 (re-run on pipeline resume from build-task-file)
> **Analyst report:** NOT FOUND → full 11-item checklist applied independently
> **Verifier stance:** Last line of defense before synthesis. Assume everything is wrong
> until independently re-verified from disk. Zero tolerance — if it can't be verified, it fails.
> **Research dir:** `.dev/brainstorms/20260611-005638-pr-remediation-v2-mention-bot/prd-pr-auto-remediation-v2-0/research`

---

## VERDICT: **PASS**

**EXIT_RECOMMENDATION: CONTINUE**

All 11 checklist items pass under independent disk re-verification performed 2026-06-12.
Every load-bearing code anchor sampled was re-Read from live `src/` and held exactly as the
corpus claims. Research is complete, code-verified, and exceeds heavyweight-tier depth. No
Critical or Important gaps block synthesis.

One **freshness drift** (the in-parallel V1.0 `pr_submit/` build has advanced past the research
snapshot — `recovery.py` now exists on disk although agent-6 still records it as absent) is
recorded as a mandatory synthesis carry-forward. It **strengthens** the corpus's central reuse
thesis ("extract-and-extend `pr_submit`, do not greenfield") rather than invalidating it, and
therefore does not lower the verdict.

---

## File Inventory (11 files, all Complete)

| File | Bytes | Terminal Status | Summary/Takeaways | Evidence style |
|---|---|---|---|---|
| `01-agent-1.md` | 24,561 | Complete | ✅ | CODE-VERIFIED/CONTRADICTED + file:line |
| `02-agent-2.md` | 20,275 | Complete | ✅ | CODE-VERIFIED + reuse-claim table |
| `03-agent-3.md` | 26,295 | Complete | ✅ | CODE-VERIFIED + load-bearing finding |
| `04-agent-4.md` | 25,017 | Complete | ✅ | CODE-VERIFIED + greenfield audit |
| `05-agent-5.md` | 28,363 | Complete | ✅ | CODE-VERIFIED + reuse-omission map |
| `06-agent-6.md` | 23,359 | Complete | ✅ | CODE-VERIFIED + MAJOR OMISSION map (regen 16:03) |
| `07-agent-7.md` | 18,608 | Complete | ✅ | CODE-VERIFIED/CONTRADICTED line-cites |
| `08-agent-8.md` | 20,351 | Complete | ✅ | CODE-VERIFIED + user flow §3 |
| `web-01-web-research-topic-1.md` | 32,832 | 🟢 COMPLETE | ✅ | reliability-tiered (32 tags / 32 URLs) |
| `web-02-web-research-topic-2.md` | 26,423 | COMPLETE | ✅ | reliability-tiered (20 tags / 26 URLs) |
| `web-03-web-research-topic-3.md` | 32,645 | ✅ COMPLETE | ✅ | reliability-tiered (36 tags / 30 URLs) |

All 11 carry a terminal `Status: Complete` and a `Summary` / `Key Takeaways` /
`Key External Findings` block (grep-confirmed). ✅ **Item 1 PASS.**
Total corpus ≈ 298 KB.

---

## 11-Item Checklist Results

### 1. File inventory — ✅ PASS
8 codebase + 3 web files; every file Complete with a Summary/Key-Takeaways section
(table above). Each agent file opens with `**Status:** Complete`; web files use explicit
`🟢 COMPLETE` / `COMPLETE` / `✅ COMPLETE — incremental writing` terminal markers.

### 2. Evidence density — ✅ PASS
Independently re-Read load-bearing claims from live `src/` (2026-06-12):
- `class ClaudeProcess:` — **confirmed at `process.py:72`**.
- `build_env()` — **confirmed additive** (`process.py:145-160`): `env = os.environ.copy()` → pop
  `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` → `if env_vars: env.update(env_vars)`. Docstring states
  env_vars are "merged with override semantics after os.environ.copy()". Can **add**, cannot
  **strip** — matches the corpus reading exactly (the central AC-3 reuse-delta finding).
- `swarm/commands.py:2268-2269` — **confirmed** `iterations += 1` then
  `if watch_max_iterations is not None and iterations >= watch_max_iterations: break` (in-memory
  `--watch` cap, NOT a disk-durable counter).
- `swarm/state.py:173-175` — **confirmed** atomic write: `tmp.write_text(...)` → `os.replace(tmp, target)`.
- `main.py:400-405` — **confirmed** deferred-import + `main.add_command(..., name=...)` with
  `# noqa: E402,I001` circular-import-avoidance comment.
- `pr_submit/fsm.py` — **confirmed** `should_halt_rounds`:135, `transition`:560,
  `MonitorState.{HALT_HUMAN, HALT_MAX_ROUNDS, TERMINAL_CLEAN}` present.
- `pr_submit/severity_router.py` — **confirmed** `remap_severity`:88, `route`:140.
- `severity-rubric.md` — **confirmed** present (10,768 bytes).
No fabricated anchors found. ✅

### 3. Scope coverage — ✅ PASS
All 7 product areas (PA-1…PA-7) from `research-notes.md` are examined:
- **PA-1 Ingress/Mention** — web-01/02/03 + agents (ETag/304, `in_reply_to_id`).
- **PA-2 Authorization** — agents 4/5/6 (collaborator-permission gate; classifier reuse).
- **PA-3 Injection/Sandbox** — web files (OWASP/CSA) + agents 4/5 (sandbox greenfield, stdin DATA envelope).
- **PA-4 Headless Execution** — all 8 codebase agents (`ClaudeProcess` + `build_env` allowlist gap).
- **PA-5 Autonomy/Idempotency** — agents 1/3/4/5/6 (`pr_submit.fsm`, ledger, swarm atomic-write).
- **PA-6 Mutation/Reply/Resolve** — `resolveReviewThread`/`databaseId` coverage in 7 codebase files.
- **PA-7 Secrets/Deploy/Observability** — systemd/audit-JSONL/`Retry-After` coverage in 9 files.

### 4. Documentation cross-validation — ✅ PASS
Web files carry explicit reliability tiers (OFFICIAL/HIGH/MEDIUM/LOW + URLs): 32/20/36 tier tags
against 32/26/30 URLs respectively. Code claims carry CODE-VERIFIED/CODE-CONTRADICTED tags.
Spot-checked CODE-VERIFIED claims (process.py:72, build_env additive, commands.py:2269, fsm.py
members, severity_router) **all independently re-verified above** against live `src/`.

### 5. Contradiction resolution — ✅ PASS (no unresolved conflicts)
The one apparent tension — agent-8 calls `commands.py:2269` an idiom "match" while agents
1/2/3/5/7 tag it CODE-CONTRADICTED — is **not a conflict**. Agent-2:258 resolves it explicitly:
"LINE CONTRADICTED / idiom verified — `:2269` is the watch loop, not a disk counter. The needed
atomic-write/terminal-idempotency discipline exists elsewhere (`write_state`/IMM-6). H1 is
effectively net-new, pattern-borrowed." Both framings agree on the same independently-confirmed
fact (the line is an in-memory watch counter). Convergent findings are otherwise unanimous.

### 6. Gap severity — ✅ PASS (no Critical/Important gaps)
`sufficiency-review.md`: `"verdict": "PASS"`, `"coverage_score": 94`, 3 **minor** gaps only
(source-home ambiguity → correctly surfaced as AMBIGUITY #1; market scope → in fact covered by
3 web agents; per-component test depth beyond T1). The HIGH-severity items the agents raise
(`build_env` allowlist seam; `pr_submit` reuse omission; swarm `:2269` mis-cite;
`needs_human_decision` has no code populator) are **spec-correction inputs for the PRD**, not
research gaps — research correctly identified and characterized them.

### 7. Depth appropriateness (heavyweight) — ✅ PASS (exceeds)
~298 KB across 11 files; per-claim file:line anchors with disk re-Read; V1.0 lineage analysis;
dual codebase + web fan-out (8 + 3); 20–36 reliability-tiered web sources per web file. Exceeds
heavyweight expectations.

### 8. User-flow coverage — ✅ PASS
Agent-8 §3 (`159` / `166`) documents the happy-path flow: review comment → authorized collaborator
replies `@bot fix --depth deep` → live authz on replier → ledger claim → **parent** comment
resolved as `opComment` → grammar parse → sandboxed Runner → host-side push → thread reply/resolve,
with `propose` default and the 4-token `@bot` grammar.

### 9. Integration-point coverage — ✅ PASS
GitHub REST/GraphQL surfaces (reply endpoint, `resolveReviewThread`, `databaseId` pagination,
ETag/304, `collaborators/{login}/permission`) documented across 7 codebase files; plus the
`ClaudeProcess` seam, CLI registration (`main.py:400` deferred-import), `~/.aienv` proxy contract,
systemd `EnvironmentFile`, and sandbox tech (OD-1) — all with verified anchors and
ABSENT/greenfield confirmations.

### 10. Pattern documentation — ✅ PASS
Captured with code anchors: atomic-write (tmp + `os.replace`, `state.py:173-175`), bounded-counter
idiom (`commands.py:2268-2269`), deferred CLI-group registration (`main.py:400`, `# noqa: E402,I001`),
stdin prompt delivery, additive env-merge (`process.py:145-160`), table-driven severity-remap
(`severity_router.py:88/140` + `severity-rubric.md`), fork-only `--repo` injection contract,
`pr_submit.fsm` HALT state lattice (`fsm.py:135/560`).

### 11. Incremental-writing compliance — ✅ PASS
All files show structured iterative sections (per-section Key Takeaways, terminal
`Status: Complete`; web-01/web-03 explicitly note "incremental writing").

---

## Independent Spot-Check Log (zero-trust re-verification, 2026-06-12)

| Claim | Cited by | Re-Read result | Verdict |
|---|---|---|---|
| `ClaudeProcess` @ `process.py:72` | 01,02,03,05,07,08 | `class ClaudeProcess:` at L72 | ✅ accurate |
| `build_env` additive `os.environ.copy()`+`update` | all 8 | confirmed L145-160 | ✅ accurate |
| `commands.py:2269` = in-memory watch cap | 01,02,03,05,07 | confirmed L2268-2269 | ✅ accurate |
| `swarm/state.py` atomic write tmp+`os.replace` | 02,04,05 | confirmed L173-175 | ✅ accurate |
| `pr_submit/fsm.py` should_halt_rounds/transition/MonitorState | 06 | confirmed L135/560 + enum | ✅ accurate |
| `severity_router` remap/route | 03,05,06 | confirmed L88/140 | ✅ accurate |
| `severity-rubric.md` exists | 02,03,05,07,08 | 10,768 bytes present | ✅ accurate |
| `remediation/` empty / `cli/remediate/` & `deploy/` absent | 04,07,08 | confirmed (empty / ENOENT / ENOENT) | ✅ accurate |
| `main.py:400` deferred CLI registration | 03,05 | confirmed L400-405 | ✅ accurate |

---

## Non-Blocking Observations (for synthesis, not gate failures)

1. **Freshness drift — V1.0 `pr_submit/` build has advanced past the research snapshot.**
   Research ran 2026-06-11 12:26–12:38; agent-6 (regen 16:03) records `recovery.py` (crash-window
   recovery) as among modules that "none exist on disk" (`06-agent-6.md:158`). **As of this re-run
   (2026-06-12), `pr_submit/` is fully populated** — `classifier.py`, `detection.py`, `fsm.py`,
   `loop_guard.py`, `models.py`, **`recovery.py` (now present)**, `run_log.py`, `severity_router.py`,
   `__init__.py` — and `src/superclaude/skills/sc-pr-submit-protocol/` exists (SKILL.md + refs +
   scripts). **Consequence:** the agents' "greenfield, grep-confirmed absent" tags for
   reply/resolve/poll and the `recovery.py`-absent note are **partially stale** — in-repo precedent
   has landed. This *confirms and strengthens* the unanimous corpus thesis ("Reuse Map omits
   `pr_submit`; extract-and-extend, do not greenfield"); it does not contradict it. **Synthesis
   MUST:** (a) reclassify H4 (reply/resolve) and the polling ingest from "zero-precedent greenfield"
   to "extend `sc-pr-submit-protocol` scripts + `pr_submit` core"; (b) treat `pr_submit/` as a
   **moving target** and require the PRD to specify a V1↔V2 coordination/coexistence decision.

2. **Fan-out partitioning anomaly (producer-side, coverage intact).** `research-notes.md`
   `SUGGESTED_PHASES` planned 7 partitioned codebase topics with distinct named output paths
   (`01-security-trust-boundary.md` … `07-env-allowlist-deep-dive.md`). The orchestrator instead
   emitted `01-agent-1.md … 08-agent-8.md`, each noting "research-notes did not contain an Agent N
   block — investigate broadly." Agents self-differentiated (greenfield audit, integration seams,
   citation deep-dives, user flow), so all 7 PA areas are covered. **Synthesis should de-duplicate:**
   the `build_env` allowlist, `pr_submit` omission, and swarm-cite findings recur ~6–8× and must be
   merged, not over-counted.

---

## Convergent High-Value Findings the PRD Synthesis Must Carry Forward

(Unanimous across the corpus; independently verified by this gate.)

1. **`build_env()` allowlist is a code change, not a config.** `env_vars` is additive over
   `os.environ.copy()`; it cannot strip `GH_TOKEN`/push/`ANTHROPIC_*`. AC-3/SC-7/INV-001 require a
   new `base_env`/`env_mode="allowlist"` seam OR a secret-free sandbox parent. First-class PRD FR
   + regression test (`assert "GH_TOKEN" not in runner_env`).
2. **Reuse Map omits `src/superclaude/pr_submit/`** — the V1.0 decision core (fsm, severity_router,
   classifier, detection, models, loop_guard, run_log, recovery — all now on disk) maps near-1:1
   onto V2's H1/H2/S1/D3/D6. Plus the `sc-pr-submit-protocol` skill covers reply/resolve/poll.
   "Extract-and-extend," do not greenfield.
3. **Swarm `commands.py:2269` mis-cite** — repoint durability to `swarm/state.py:173-175` atomic
   write and the round-counter to `pr_submit/fsm.should_halt_rounds`.
4. **Genuine remaining greenfield** = systemd deploy unit (`deploy/` still absent), the execution
   sandbox (OD-1), and the host-side `gh` wrapper (H5). §19.1 probe-first is a hard gate for the
   GitHub surfaces now partially precedented by `sc-pr-submit-protocol`.
5. **External corroboration (web):** reasoning/execution split is prescribed as the fundamental
   prompt-injection mitigation; OWASP LLM01 validates the threat model; propose-only is the
   market-validated safe default.

Plus carry forward: OD-1…OD-4 + AMBIGUITY #1 (`remediation/` vs `cli/remediate/`) as explicit PRD
open questions; `needs_human_decision` must HALT (never auto-default).

---

## Gate Decision

**PASS** — green light for synthesis. All 11 checklist items satisfied under independent disk
re-verification (2026-06-12); every sampled code anchor held against live `src/`; sufficiency-review
PASS (coverage 94); no Critical or Important gaps. Synthesis must (a) de-duplicate recurring
cross-file findings, (b) reclassify reply/resolve/poll from greenfield to extend-`pr_submit`/
`sc-pr-submit-protocol` and treat `pr_submit/` as an in-flight moving target requiring a
coordination decision, and (c) carry the 5 convergent findings above plus OD-1…OD-4 as explicit
PRD open questions.

**EXIT_RECOMMENDATION: CONTINUE**
