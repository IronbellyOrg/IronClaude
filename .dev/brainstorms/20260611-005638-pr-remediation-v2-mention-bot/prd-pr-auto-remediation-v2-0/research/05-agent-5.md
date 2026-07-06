# Research: Investigation topic 5 — Reuse-Map & Foundational-Primitive Verification (broad investigation)

**Investigation type:** Investigator
**Scope:** Verify the PRD's "Reuse Map" and §2 Component-Inventory reuse claims against the real codebase — `ClaudeProcess` (`cli/pipeline/process.py`), swarm loop-guard (`cli/swarm/commands.py`), `sc-auggie-review-protocol` (severity rubric + posting precedent), `gh` usage precedent, secret-sourcing (`~/.aienv`/systemd `EnvironmentFile`), and existing `cli/` command-group conventions. Differentiated focus (8 agents converged on the same reuse scope): the **uncited V1.0 `pr_submit` prior-art package** and **net-new surfaces with zero codebase precedent**.
**Status:** Complete
**Date:** 2026-06-11

---

## Investigation Rationale

The research-notes contained no Agent 5 block, so this agent takes the broad mandate.
The single highest-leverage broad investigation for THIS PRD is **verifying the reuse
claims** — the merged-requirements spec hangs its entire build sequencing (§19) and
component inventory (§2) on a small set of existing primitives it promises to "Reuse".
If those primitives are mis-cited (wrong line, wrong signature, different behavior than
described), the whole build plan inherits the error. This agent code-verifies each one.

**De-confliction note:** all 8 parallel agents independently chose "reuse-map verification"
as their scope (Agents 1, 2, 3, 4, 6, 7, 8 headers all cite `ClaudeProcess`/swarm-counter/
severity-rubric). To avoid 8 redundant reports, this agent does a *fast self-contained
confirm* of the 3 over-covered primitives, then spends the bulk of its effort on two
**under-covered** areas: (A) the **V1.0 `pr_submit` prior-art package that the V2 Reuse Map
omits**, and (B) **net-new surfaces with ZERO codebase precedent** (GraphQL
`resolveReviewThread`, ETag/304 polling, `deploy/`+systemd, the Python `gh` wrapper).

---

## Part 1 — Fast confirm of the over-covered reuse primitives

### R2 — `ClaudeProcess` (`cli/pipeline/process.py:72`)  **[CODE-VERIFIED]**

- Class **is** declared at line 72 (`process.py:72`). Exact citation correct.
- `build_command()` (`process.py:121`) emits exactly what §7 claims:
  `claude --print --verbose <permission_flag> --no-session-persistence --tools default
  --max-turns N --output-format <fmt>` (+ optional `--model`, + `extra_args`). **Matches.**
- Default `permission_flag="--dangerously-skip-permissions"` (`process.py:93`) — §7's claim
  that this is the default is correct. **Matches.**
- Prompt delivered via **stdin** (`_write_prompt_to_stdin`, `process.py:221`), chunked
  64 KiB, EINTR-retried, closes stdin in `finally`. §7's "prompt delivered via stdin
  (bypasses 128KB argv limit)" is **accurate and already hardened** (commit 1b0264f1 in this
  branch's log is exactly this work). **Matches — better than claimed.**
- Constructor already has an `env_vars: dict|None` param (`process.py:100`) and
  `timeout_seconds` (default 6300, `process.py:94`) — §14's `ClaudeProcess.timeout_seconds`
  reference is valid.

### R2 env-allowlist gap — §7's central reuse caveat is **[CODE-VERIFIED as a real gap]**

§7 insists: *"`build_env()` MUST be wrapped with an explicit allowlist `env_vars` (not the
current full `os.environ.copy()`)."* Reading `build_env()` (`process.py:145-160`):

```python
env = os.environ.copy()          # full parent environment, INCLUDING secrets
env.pop("CLAUDECODE", None)
env.pop("CLAUDE_CODE_ENTRYPOINT", None)
if env_vars:
    env.update(env_vars)         # MERGE/override semantics -- ADD only, cannot REMOVE
return env
```

The `env_vars` kwarg uses **`.update()` (additive)**, so it can inject vars but **cannot
strip** an inherited secret (`GH_TOKEN`, `ANTHROPIC_AUTH_TOKEN`, push token) from the child.
The Runner's INV-001/SC-7 requirement ("no `GH_TOKEN`, no push credential in the Runner env")
**cannot be met by passing `env_vars` alone** — it requires either a new `build_env`
code path that starts from an *empty* dict + allowlist, or running the Runner in a sandbox
whose parent process already lacks the secrets (the §6 sandbox boundary). The spec's caveat is
**correct and load-bearing**; this is the single most important nuance in the whole Reuse Map.
**Recommendation:** add an `env_mode="allowlist"` branch to `build_env()` (start from `{}`),
or have the sandbox's init process hold no secrets — do NOT rely on `env_vars` override.

### H1/H2 — swarm "bounded-counter" (`cli/swarm/commands.py:2269`)  **[CODE-CONTRADICTED — citation mis-describes the code]**

§9 claims: *"Counter mirrors swarm bounded-counter (`cli/swarm/commands.py:2269`):
**monotonic, disk-authoritative, survives restarts**."* The code at lines 2255-2290 is the
**`watch` sub-command's in-memory poll loop**:

```python
iterations += 1
if watch_max_iterations is not None and iterations >= watch_max_iterations:
    break
time.sleep(watch_interval)
```

`iterations` is a **local variable in a CLI watch loop** — it is *not* disk-persisted, *not*
restart-surviving, and *not* a per-PR/per-thread round ledger. The "monotonic,
disk-authoritative, survives restarts" properties §9 attributes to this line **do not exist
at that citation.** The disk-authoritative round/budget counter the spec needs is **net-new
work**, not a reuse. (See Part 2 — V1's `pr_submit/loop_guard` + `run_log` are the *actual*
nearest prior art, and the spec cites neither.) **Action for TDD:** drop the swarm:2269
citation or downgrade it to "iteration-cap idiom only"; source the durable counter from
`pr_submit` instead.

### S1 — severity rubric (`sc-auggie-review-protocol/refs/severity-rubric.md`)  **[CODE-VERIFIED]**

File exists (10,768 bytes, 5 explicit tiers with decision-term definitions:
Critical=block merge … Nit). §17's "re-grade via the rubric, Augment severity is a hint"
is the rubric's own stated purpose ("`severity_hint` is a starting point, not
authoritative"). **Reuse claim valid.**

### H4 precedent — `gh` posting in `sc-auggie-review-protocol/SKILL.md`  **[CODE-VERIFIED, partial]**

- Inline-comment precedent confirmed: `gh api repos/<owner>/<repo>/pulls/<PR>/comments`
  (SKILL.md:307) — a valid template for H4's reply body POST.
- Summary precedent: `gh pr review <PR> --comment --body-file …` (SKILL.md:304).
- Guardrail precedent: SKILL.md:349 enforces `--comment` **only**, *never*
  `--approve`/`--request-changes` — exactly matches V2 §20 "modifying merge state out of
  scope." Good reusable discipline.
- **BUT** there is **no `/replies` endpoint and no GraphQL `resolveReviewThread`** anywhere
  in auggie-review (or `src/`). So H4's *reply-to-thread* + *resolve* halves are genuinely
  net-new (consistent with spec §12 "net-new, absent from repo today" and V1 C4 "New").

**Key Takeaways (Part 1)**
- `ClaudeProcess` reuse is **solid** — citation, signature, and stdin behavior all verified.
- The **env-allowlist caveat is real**: `env_vars` is additive and cannot strip secrets;
  INV-001/SC-7 needs a new empty-base `build_env` path or a secret-free sandbox parent.
- The **swarm:2269 counter citation is wrong** — it's an in-memory watch-loop cap, not the
  durable round ledger §9 describes. Durable counter = net-new (or reuse V1 `loop_guard`).
- Severity rubric + gh inline-comment precedents are **verified**; reply/resolve are net-new.

---

## Part 2 — THE KEY FINDING: V1.0 `pr_submit` is already (partially) BUILT and the V2 Reuse Map omits it entirely

The V2 spec treats V1.0 as a discardable design — §20 lists "V1.0's in-session Monitor-tool
host (fully replaced)" as **out of scope**, and the Reuse Map names only `ClaudeProcess`,
swarm-counter, and the severity rubric. **This is materially incomplete.** V1.0 was *built*
into an importable, **tested** Python package at `src/superclaude/pr_submit/`, and several V2
components the spec marks **New** have a direct, tested ancestor there.

### What actually exists in `src/superclaude/pr_submit/`  **[CODE-VERIFIED]**

| Module | Size | Built? | Key public API |
|--------|------|--------|----------------|
| `fsm.py` | 17 KB | ✅ built + tested | `RunConfig`, `parse_args`, `evaluate_push_decision`, `should_halt_rounds`, `transition`, `MonitorState` |
| `severity_router.py` | 6.4 KB | ✅ built | `remap_severity`, `route` |
| `classifier.py` | 3.6 KB | ✅ built + tested | `classify` (3-state, bot-login-keyed) |
| `detection.py` | 6.5 KB | ✅ built + tested | `DetectionContract`, `DetectionContractLocked`, `poll_augment_review` |
| `models.py` | 7.5 KB | ✅ built | `Finding`, `Severity`, `MonitorState`, `PushDecision`, `EventType`, `SkillResult` |
| `loop_guard` | — | ❌ **named in `__init__` docstring, NOT created** | (designed: loop-guard fence-post) |
| `run_log` | — | ❌ **named in `__init__` docstring, NOT created** | (designed: write-ahead JSONL run-log) |
| `recovery` | — | ❌ **named in `__init__` docstring, NOT created** | (designed: crash-window recovery) |

Tests present and passing-shaped: `tests/pr_submit/{test_autonomy_gates,test_detection_contract,test_monitor_arm,test_skill_parse}.py`.
The package's `__init__.py` re-exports `classify`, `poll_augment_review`, `DetectionContract`,
`run_skill`, `transition`, `evaluate_push_decision`, `remap_severity`, `route`, and the models.
**Note:** the `__init__` docstring lists `loop_guard`/`run_log`/`recovery` as part of the
intended package, but the files do not exist and are not imported — so V1 is *partially* built:
decision core + detection + severity done; durable run-log/recovery still on paper.

### V2 "New" components that have a BUILT V1 ancestor (Reuse Map omission map)

| V2 component (spec marks **New**) | V1 prior art (`pr_submit/…`) | Reuse verdict |
|-----------------------------------|------------------------------|---------------|
| **H2** autonomy gate — level→allowed-actions, `needs_human_decision` HALT, budget HALT (§8) | `fsm.evaluate_push_decision` (INV-016 **5-predicate G-push conjunction**), `needs_human_decision` **pre-gate override** (fsm.py:204), `should_halt_rounds` (`>=`, fsm.py:129) — **tested** by `test_autonomy_gates.py` | **extract-shared / extend.** V2 §8's "min-over-lattice cap + off-lattice HALT short-circuits" is a *generalization* of V1's verified 5-predicate conjunction. Do not greenfield. |
| **S1 / §17** severity routing | `severity_router.remap_severity` + `route` — **built** | spec cites the *rubric* but not the *coded router*. **Reuse the router**, not just the .md. |
| **§19.1 probe** → "lock bot login + `in_reply_to_id`/`databaseId` as config constants" | `DetectionContract` / `DetectionContractLocked` — **tested** "locked-contract" container | **reuse-by-import.** The locked-contract is exactly the probe-output vessel §19.1 specifies. |
| **D5** authz classifier (reject-by-default, bot-login keyed) | `classifier.classify` — 3-state, keys ONLY on `contract.augment_bot_login`, "different login ⇒ not detected" (T-211) | **mirror-shape.** Different decision (review-state vs authz) but the *bot-login-as-config-constant + unknown→safe-default* discipline is directly transferable. |
| **H1** durable round/budget ledger (§9/§10) | `run_log` (write-ahead JSONL) + `recovery` (crash-window) — **designed in V1, never built** | **net-new in BOTH versions.** V1's unbuilt `run_log`/`recovery` design is the closest spec-level prior art; V2 §9's two-phase intent/outcome ledger supersedes it. Build once, here. |

### The architecture V2 wants is already proven in V1  **[CODE-VERIFIED]**

`pr_submit/__init__.py` states the **NFR-6 "core purity"** invariant verbatim: *"the modules
in this package contain ZERO `gh`/`git` tokens. All `gh`/`git` I/O lives in the skill's bash
scripts and the SKILL.md VAL validator; the core consumes already-fetched, already-classified
data."* This **pure-decision-core + I/O-at-the-edges** separation is *precisely* the seam V2's
split host needs: the Dispatcher does all `gh`/`git` I/O, the pure core (FSM, router,
autonomy) decides, the Runner executes. V2 can adopt the same boundary the V1 tests already
enforce, rather than re-deriving it.

### The honest caveat (why it's "extend", not "import wholesale")

- **Trigger differs:** V1 = *Augment-review*-triggered (poll for a review); V2 = *@-mention*-
  triggered (poll comments + **authz gate** + parent resolution). V1 has no authz concept.
- **Autonomy encoding differs:** V1 = numeric `--monitor {0,1,2,3}` ordinal; V2 = named lattice
  `propose<patch<fix<push<resolve`. The *gating logic* (HALT predicates, round budget) carries
  over; the *level vocabulary* must be remapped.
- **Host differs:** V1 = in-session Monitor tool + skill bash; V2 = systemd Dispatcher + ephemeral
  sandbox Runner. The pure core is host-agnostic and ports cleanly; the I/O edges are rewritten.

So the correct framing for the PRD/TDD is **"extract-and-extend `pr_submit`'s pure core into
`cli/remediate/`"**, not "reuse `ClaudeProcess` + greenfield everything else." Roughly
**5 of the spec's ~10 `New` host components (H1/H2/D4/D5/D6-adjacent) have 40-80% prior art**
that the Reuse Map does not credit.

**Key Takeaways (Part 2)**
- `src/superclaude/pr_submit/` is **built and tested** (FSM/router/classifier/detection/models)
  — the V2 Reuse Map's biggest omission.
- V1 `fsm.evaluate_push_decision` (5-predicate G-push conjunction + `needs_human_decision`
  pre-gate, **tested**) is the direct ancestor of V2's H2 autonomy gate — extend, don't rebuild.
- V1 `DetectionContractLocked` is the ready-made vessel for V2's §19.1 probe-lock constants.
- V1's **NFR-6 pure-core/I-O-edge** architecture already matches V2's Dispatcher/Runner split.
- V1's `run_log`/`recovery` were **designed but never built** — V2's §9 two-phase ledger is the
  place to finally build the durable state core (genuinely net-new, agreeing with §16 INV-002).

---

## Part 3 — Second uncited reuse: `cli/roadmap/remediate_executor.py` (the closest analog to V2's R2/R4)

The V2 Reuse Map cites the **raw** `ClaudeProcess` primitive but misses
`src/superclaude/cli/roadmap/remediate_executor.py` — an existing **agent-driven remediation
orchestrator** that already sits one abstraction level closer to V2's Runner/executor/sandbox.
**[CODE-VERIFIED]** Its module docstring + signatures show:

- **It already composes `ClaudeProcess`** (`remediate_executor.py:26`) to run remediation
  agents in parallel (`ThreadPoolExecutor`, `_run_agent_for_file`, `_run_agent_with_retry`).
  This is a *working* example of the exact "spawn `claude -p` to remediate a finding" pattern
  V2 R2 needs — not just the primitive, but the primitive *in remediation use*.
- **`enforce_allowlist(findings) -> (allowed, rejected)`** (`remediate_executor.py:155`) — a
  **pure** (NFR-004) file allowlist gate: any finding touching a file outside `EDITABLE_FILES`
  is SKIPPED with a warning. This is a direct analog of V2 §6's "never modify files outside the
  workspace" file-write boundary. The *reject-by-default + log* shape is reusable for the
  sandbox's write-scope enforcement.
- **`create_snapshots` / `restore_from_snapshots` / `cleanup_snapshots`** (atomic
  read→tmp→`os.replace`, NFR-005) + **per-file rollback** (`_handle_file_rollback`,
  `remediate_executor.py:431`) — the snapshot/rollback discipline V2's sandbox checkout +
  per-PR `flock` tree-mutation (§9) and "validation fails → don't push" (§8) want.
- **`check_patch_diff_size` / `_check_diff_size`** (`remediate_executor.py:309`) — a patch-size
  guard relevant to V2's push blast-radius / budget concerns (R4 §9 INV-009/018).
- **`_check_cross_file_coherence`** (`remediate_executor.py:453`) — multi-file fix coherence,
  relevant to V2 fix-level validation (SC-4).
- **`RemediationPatch` dataclass (MorphLLM-compatible)** + **`fallback_apply()`** deterministic
  text replacement (`remediate_executor.py:643`) — analog to V2 §3 step (j) "emit patch-bundle."
- **`update_remediation_tasklist`** writes back **atomically** (tmp + `os.replace`, NFR-005,
  `remediate_executor.py:563-589`).

**Verdict:** `remediate_executor.py` is **mirror-shape / extract-shared** for V2's R2 executor,
R4 sandbox-allowlist, and the patch-emit/rollback path. The Reuse Map should cite it alongside
`ClaudeProcess`. Caveat: it edits a **fixed `EDITABLE_FILES` allowlist** in-process (roadmap
remediation has a known target set), whereas V2's Runner edits an **arbitrary PR-head
checkout** — so the allowlist becomes "stay inside the sandbox workspace," not a named file
set. The *mechanism* ports; the *policy* widens.

### Atomic-write precedent for the H1/§10 ledger  **[CODE-VERIFIED]**

§10 specifies "atomic writes (temp + `os.rename`), append-only with `O_APPEND`." Two proven
templates already exist:

- **`cli/recommend/cache.py:save()`** (`cache.py:127-160`) — crash-safe atomic write:
  *randomized same-directory* temp name (`.{name}.tmp.{pid}.{id}`) + `os.replace` +
  `finally`-cleanup if `os.replace` never ran. Its own comment calls out bounding the
  *"worktree-concurrency last-write-wins window"* — directly relevant to the §9 per-PR `flock`
  requirement and the repo's known "parallel sessions share the git index" hazard.
- **`cli/roadmap/remediate_executor.py`** uses `os.replace` for every snapshot/restore/tasklist
  write (≥8 call sites). Consistent house style: **`os.replace`, not `os.rename`** (atomic on
  POSIX, and atomic-overwrite on Windows where `os.rename` is not).

**Recommendation for TDD:** the §10 ledger should follow `cache.py`'s randomized-tmp +
`os.replace` + `finally`-cleanup pattern (not the bare `os.rename` the spec names), and combine
it with `O_APPEND` for the JSONL event stream. Both halves have a verified in-repo precedent.

**Key Takeaways (Part 3)**
- `roadmap/remediate_executor.py` is the **single closest existing analog** to V2's R2/R4 —
  it already runs `ClaudeProcess` for remediation with allowlist + snapshot-rollback + retry +
  patch-apply. The Reuse Map omits it; it should be the *primary* executor reuse citation.
- The ledger's "atomic write" is **already solved twice** in-repo (`cache.py`,
  `remediate_executor.py`) with `os.replace` (not `os.rename`) + randomized tmp + crash cleanup.

---

## Part 4 — Net-new surfaces with ZERO codebase precedent (effort/risk concentrators)

These are the components where the build has **no in-repo prior art at all** — they dominate
the genuine net-new effort and risk. Each is **[CODE-VERIFIED]** by exhaustive grep returning
empty.

| V2 component | Grep target | Result | Implication |
|--------------|-------------|--------|-------------|
| **H4 resolve** — GraphQL `resolveReviewThread` (§12, INV-010) | `graphql\|resolveReviewThread\|reviewThreads` in `src/` | **0 hits** | No GraphQL anywhere in the repo. Pagination-by-`databaseId` + the GraphQL mutation are net-new; **highest unknown-shape risk** → belongs in the §19.1 probe. |
| **D3 ingest** — ETag/304 conditional polling (§13) | `If-None-Match\|ETag\|304` in `src/` | **0 hits** | Conditional-request rate-limit discipline is net-new; no polling loop to copy. |
| **H5 gh-wrapper** — Python `--repo` injector (C5/SC-4) | any Python shelling out to `gh` in `src/superclaude/` | **0 hits** | ⚠️ **Critical:** *no Python code in the repo calls `gh` at all.* Every `--repo IronbellyOrg/IronClaude` guard today lives in **skill markdown prose** (instructions to Claude), never machine-enforced. The spec's C5 invariant ("no code path can call `gh` without `--repo`") therefore *requires* H5 — and validates exactly why it's needed: prose discipline is unenforceable in a headless daemon. |
| **S2 deploy** — systemd unit + sandbox image (§15) | `systemd\|WatchdogSec\|EnvironmentFile=\|NoNewPrivileges` | **0 hits** | No service/deploy infra in-repo (`deploy/` does not exist). Fully net-new ops surface. |
| **R4 sandbox** — container/microVM execution (§6, OD-1) | `docker\|podman\|firecracker\|sandbox` (`.py`) | only **incidental** hits (`install_mcp.py` Docker-for-MCP-gateway; `audit/profiler`) | No code-execution sandbox harness exists; the Docker references are for the MCP gateway, not for running untrusted code. OD-1 is genuinely greenfield. |

### The one net-new claim that *does* have a precedent  **[CODE-VERIFIED]**

§11's secret-sourcing reuse — *"`~/.aienv` / `ccsession.env` chmod-600 — model for systemd
`EnvironmentFile=`"* — is **valid**: `~/.aienv` is already read by Python (`cli/sprint/
summarizer.py`), and `src/superclaude/skills/ccsession-tag/ccsession.env.example` +
`install.sh` demonstrate the chmod-600 env-file model. So the *secret-file pattern* is reusable
even though the *systemd packaging around it* is net-new.

**Key Takeaways (Part 4)**
- **GraphQL `resolveReviewThread`, ETag/304 polling, systemd deploy, and the execution
  sandbox have zero in-repo precedent** — they are the real net-new effort, and the GraphQL +
  detection-shape unknowns are correctly routed to the §19.1 probe.
- **The H5 `gh` wrapper is the most under-appreciated net-new item:** no Python in the whole
  repo calls `gh`; `--repo` safety is currently *prose-only*. A headless daemon cannot rely on
  prose, so H5 is load-bearing — the spec is right to make it a build-sequencing gate (§19.2).
- Only the **chmod-600 secret-file** half of §11/§15 has a real precedent.

---

## Part 5 — V1.0 → V2.0 lineage (what's replaced, what's inherited)

**[CODE-VERIFIED against `…/20260610-234750-pr-review-auto-remediation/merged-requirements.md`]**

| Dimension | V1.0 (built as `pr_submit` + `sc-pr-submit-protocol`) | V2.0 (this spec) |
|-----------|--------------------------------------------------------|------------------|
| Trigger | Augment **review** lands → poll detects it | Augment/human **@-mention** on a review comment |
| Host | **In-session** Monitor tool + skill bash (dies on session close — V1 R3) | **Headless** systemd Dispatcher + ephemeral Runner |
| Form factor | Skill + command (`/sc:submit-pr --monitor`) | **CLI group** (`superclaude remediate`) |
| Autonomy | numeric `--monitor {0,1,2,3}` | named lattice `propose<patch<fix<push<resolve` |
| Authorization | none (the operator runs it locally) | **live per-trigger collaborator-permission gate** (C4) — entirely new |
| Injection model | n/a (operator-driven) | opComment-as-DATA envelope + sandbox (SC-2) — entirely new |
| Loop-guard | `fsm.should_halt_rounds` + `max_rounds`/`HARD_CAP` (built) | two-phase intent/outcome ledger + per-PR push budget (§9) |
| `needs_human_decision` HALT | FR-4.4 + `fsm` pre-gate override (built, tested) | **inherited verbatim** (§8 "inherit V1.0 FR-4.4") |
| Severity routing | `severity_router` + rubric (built) | same rubric, same router (§17) |
| Reply/resolve | C4 "New (mirrors gh patterns)" — **designed, not built** | H4 net-new (reply + GraphQL resolve) |

**Inheritance the spec acknowledges:** §8 explicitly inherits "V1.0 FR-4.4" `needs_human_decision`
classes; §17 reuses the rubric; §19.1 mirrors V1's R1 "probe-first" discipline. **Inheritance the
spec MISSES:** the *built, tested* `pr_submit` decision core (FSM/router/contract/models) — see
Part 2. Net: V2 correctly identifies the *conceptual* lineage but under-credits the *code* lineage.

---

## Gaps and Questions

1. **Reuse Map omits `pr_submit` and `remediate_executor.py`.** The two largest reuse
   opportunities (V1 decision core; the existing `ClaudeProcess`-driven remediation executor)
   are absent from §2 / the Reuse Map. **Q for TDD:** extend `pr_submit`'s pure core into
   `cli/remediate/`, or greenfield? (This agent's evidence says extract-and-extend.)
2. **swarm:2269 mis-citation.** §9 attributes "monotonic, disk-authoritative, survives
   restarts" to an in-memory watch-loop counter. The durable counter is net-new. Fix the
   citation before it propagates into the TDD/tasklist.
3. **`build_env` cannot strip secrets.** INV-001/SC-7 needs either a new empty-base
   allowlist `build_env` path or a secret-free sandbox parent — `env_vars` override alone is
   insufficient. Is this slated as a `process.py` change or a sandbox-only guarantee?
4. **H5 has no Python precedent and current `--repo` safety is prose-only.** Confirm H5 is
   built and unit-tested *before* any `gh`-calling code (spec §19.2 already sequences this —
   reinforce it). A single un-wrapped `gh` call in the daemon re-introduces the upstream-PR
   hazard the CLAUDE.md rule exists to prevent.
5. **GraphQL `resolveReviewThread` shape is unknown.** Zero repo precedent; route the
   `databaseId`-pagination + mutation shape capture into the §19.1 probe (alongside
   `in_reply_to_id` and the Augment bot login).
6. **`loop_guard`/`run_log`/`recovery` are V1 vapor.** They are named in `pr_submit/__init__.py`
   but unbuilt. V2's §9 two-phase ledger should be where this durable-state core is finally
   built — don't assume V1 left a reusable run-log.
7. **Sandbox tech (OD-1) is greenfield.** No container/microVM execution harness exists; the
   Docker refs are MCP-gateway-only. The §6 boundary is well-specified but the implementation
   has no scaffold to start from — likely the single biggest net-new ops lift.

## Stale Documentation Found

- **Spec §9 (swarm:2269 citation)** — **[CODE-CONTRADICTED]** The cited line is a CLI watch-loop
  `iterations += 1` cap (in-memory, non-durable), not the "monotonic, disk-authoritative,
  survives restarts" counter the prose claims. The described primitive does not exist at that
  citation.
- **Spec Reuse Map / §20** — **[CODE-CONTRADICTED in spirit]** §20 calls V1.0 "fully replaced"
  and the Reuse Map credits no V1 code, but `src/superclaude/pr_submit/` is a built, tested
  package whose FSM/router/detection/models are 40-80% applicable to V2's "New" H2/D5/§19.1
  components. "Fully replaced" overstates the discontinuity at the code level.
- **`pr_submit/__init__.py` docstring** — **[CODE-CONTRADICTED]** lists `loop_guard`, `run_log`,
  `recovery` as package modules; those files do not exist (the docstring hedges "wired
  incrementally as the modules land," but a reader scanning the docstring would assume they're
  present). V1 is partially built.

## Summary

The V2.0 merged-requirements spec is **architecturally sound and its CODE-cited primitives are
mostly accurate** — `ClaudeProcess` (`cli/pipeline/process.py:72`), its stdin/`build_command`
behavior, the severity rubric, and the `gh` inline-comment posting precedent all verify, and
the spec's own §7 env-allowlist caveat is a real, correctly-identified gap. But this agent's
differentiated sweep surfaced **three findings the spec's Reuse Map does not capture**, all
pointing the same direction — *the build is less greenfield than §2 implies*:

1. **`src/superclaude/pr_submit/` (V1.0) is built and tested** and is the direct ancestor of
   V2's "New" H2 autonomy gate (`fsm.evaluate_push_decision` — tested 5-predicate G-push
   conjunction + `needs_human_decision` pre-gate), severity routing, and §19.1 probe-lock
   (`DetectionContractLocked`). Its NFR-6 pure-core/I-O-edge architecture already matches V2's
   Dispatcher/Runner split. **Extract-and-extend, don't greenfield.**
2. **`cli/roadmap/remediate_executor.py` already runs `ClaudeProcess` for remediation** with a
   file allowlist, atomic snapshot/rollback, retry, diff-size guards, and patch-apply — the
   closest analog to V2's R2/R4, and the proper primary executor reuse citation. The §10
   ledger's atomic-write is likewise already solved twice (`cache.py`, `remediate_executor.py`)
   via `os.replace`.
3. The genuine net-new surface is narrower but sharper than the spec's ~10 "New" rows suggest:
   **GraphQL `resolveReviewThread`, ETag/304 polling, the Python `gh` wrapper (no Python in the
   repo calls `gh` — `--repo` safety is currently prose-only), systemd deploy, and the
   execution sandbox** have **zero** in-repo precedent and concentrate the real effort/risk.

Two **[CODE-CONTRADICTED]** citation errors (swarm:2269 durable-counter claim; "V1 fully
replaced") should be corrected before the spec feeds a TDD/tasklist, so the downstream build
plan credits the right prior art and budgets the right net-new work.

**Status:** Complete
