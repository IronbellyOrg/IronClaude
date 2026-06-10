<!-- Provenance: produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Variant 1 (opus:architect) -->
<!-- Merge date: 2026-06-08 -->
<!-- Non-base sources incorporated: V2 (sonnet:analyzer), V3 (haiku:backend) -->
<!-- Convergence: 0.82 (PASS) -->

# Spec — `superclaude reflect run`: thin CLI wrapper for the post-execution reflect gate

> The wrapper is an **invocation + contract-consumption shell**, not a reimplementation of reflect. It turns the manual HALT gate into an unattended one by launching reflect as a **top-level `claude --print` subprocess** (escaping the Agent-tool nesting limit so Tier 2 actually fans out), then **fail-closed** routing the tasklist gate on the emitted contract.

## 1. Problem

Task-builder MDTM tasklists end with a POST reflection gate (`src/superclaude/skills/task-builder/SKILL.md`, Phase-N item) that writes `reflect_post: PENDING` and **HALTs for a human** to run `/sc:reflect --mode post` in a fresh session. The HALT is correct on the property that matters — **executor-disjoint** review — but fully manual. The naive automation (executor spawns an Agent-tool subagent running `/sc:reflect`) is structurally broken: an Agent-tool subagent cannot nest a skill that fans out its own subagents, so reflect's **Tier 2** (heterogeneous-model reviewers + `sc-adversarial` merge) silently never runs (memory `reference_subagent_cannot_nest_skill_fanout`). Tier 2 is mandatory for medium/complex tasklists (TCS-derived depth ≥ `standard`).

A **CLI subprocess (`claude -p`) is a top-level process**, not an Agent-tool subagent, so it does NOT hit the nesting limit. A thin wrapper can launch reflect there, let Tier 2 fan out, capture `return-contract.yaml`, and write a `reflect_post:` verdict back — automating the gate **without** weakening executor-disjointness and **without** copying reflect logic into Python.

**Central thesis (from the analyzer lens, load-bearing):** the wrapper is a *gate consumer*, so it must **never accept a silently degraded Tier-2 audit**. Reflect fail-opens (missing MCP → Grep/Glob; missing aliases → fewer reviewers) for interactive use; a completion gate must distinguish "full Tier-2 audit passed" from "reflect produced a report after losing the grounding/diversity that made Tier 2 valuable."

## 2. Functional Requirements

- **FR-1 Top-level launch.** Run `/sc:reflect --mode post` as a top-level `claude --print` subprocess via the existing `ClaudeProcess` (`src/superclaude/cli/pipeline/process.py`), never as an Agent-tool subagent. This is the sole reason Tier-2 fan-out succeeds.
- **FR-2 Skill is single source of truth.** The subprocess prompt is a single `/sc:reflect …` slash invocation. The wrapper MUST NOT compute coverage/deviation-classes/tier/promotion/verdict in Python — only *build the invocation* and *consume the contract*.
- **FR-3 Deterministic input derivation.** Derive: `--diff <BASE>..HEAD` (`<BASE>` = frontmatter `start_commit`, else `git merge-base HEAD <integration>`, else fail `base-unresolved`); `--tasklist` = the explicit absolute path passed in (no implicit cwd guessing — V2); `--spec` from frontmatter `spec_path` when it resolves to one absolute file; `--depth` from **TCS floored at `standard`** (POST never runs `quick`); `--executor-model` from frontmatter/`EXECUTOR_MODEL_CLASS` (feeds reflect's anti-self-confirmation exclusion). **Single TCS producer:** the builder bakes the resolved `--depth` (and `<BASE>`) into the item command; the wrapper treats them as **passthrough** to avoid builder/wrapper TCS drift (V1 R-6).
- **FR-4 Pinned output dir.** Pass an explicit `--output <run-unique abs dir>` (default `<task-dir>/reflect/post/<short-sha>/`) so the `return-contract.yaml` location is deterministic; the wrapper **owns output uniqueness** so reflect's collision `-N` suffixing is unreachable (V2 FM-7). Reject an `--output` under `.claude/{skills,agents,commands}` before launch (reflect STOP condition).
- **FR-5 Contract-driven verdict.** After exit, parse exactly `<output>/return-contract.yaml` and derive `verdict ∈ {pass, halted, degraded, blocked}` from contract fields (§6 table). Never invent a verdict the contract doesn't support; gate on `contract_version` (1.x tolerant; unknown major → `blocked`, fail-loud).
- **FR-6 Frontmatter write-back (atomic + race-safe).** Replace the `reflect_post:` block with the §6 structured block. Mechanism (merge of V3 + V2): read bytes → parse frontmatter → inject only `reflect_post` → serialize with a yamllint-safe dumper → write temp in same dir → **compare on-disk bytes still equal the bytes read** → `os.replace()` (atomic, POSIX). On compare mismatch (concurrent edit), do NOT overwrite: write `<output>/wrapper-result.yaml` sidecar and exit non-zero. Body byte-preserved.
- **FR-7 Dual gate signal.** Exit on the §6 exit-code contract AND leave the parsed `reflect_post:` block + a `<output>/wrapper-result.yaml` sidecar on disk. The completion-gate consumes the cheap path (exit code) and/or the rich path (`reflect_post.verdict == pass`).
- **FR-8 Fail-closed HALT.** Only `verdict: pass` (clean, full, non-degraded Tier-2) exits 0. `halted` (audit-found deviations: regression/drift/needs_human_decision/status:partial), `degraded` (lost Tier-2 grounding/diversity/adversarial-merge), and `blocked` (no usable contract / STOP / timeout) all exit non-zero and keep the Done item HALTed (`feedback_human_decision_items_must_halt`). No silent auto-proceed.
- **FR-9 Audit-only default.** Default `--no-promote`, passed as a **hard flag in the prompt string** (V3) — not merely omitted — so an upstream default-change can't enable promotion. Opt-in `--promote` passes reflect's own gated Wave-7 through. The wrapper itself performs **no** git add/commit/mv; the only mutation outside `<output>/` is the task frontmatter.
- **FR-10 Headless MCP/model parity.** The child inherits the operator's **real** env via bare `ClaudeProcess.build_env` (copy `os.environ`, pop `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` to dodge nested-session detection), preserving `HOME`/MCP registration (Serena/auggie) and `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`. **Explicitly NOT `HomeIsolation`/`ClaudeProcessAdapter`** (cliEval) — its hermetic mkdtemp HOME would strip exactly the MCP + aliases Tier-2 and grounding depend on (V1 load-bearing boundary). cwd stays the project root so `--diff` resolves against the same repo.
- **FR-11 Degradation detection (fail-closed).** Preflight: assert `claude` binary present; count `ANTHROPIC_DEFAULT_*` aliases in the exact child env; validate paths/diff/frontmatter. Post-contract: route to `degraded` (HALT) on any chain-critical loss — `degraded_components ⊇ {serena, auggie, env-aliases, evidence-validator, serena:context-excluded}`; expected-T2 but `tier_reached==1`; `t2_model_class_diversity != full`; `t2_vendor_diversity == single` (unless `--allow-single-vendor`); `adversarial_unavailable` / `merge_method: single-reviewer-fallback` / null `adversarial_convergence_score` at T2; `verification_ran == false` (unless exempted); `citations_dropped > 0`; `input_drift_detected`. This is intentionally **stricter** than reflect's interactive fail-open. `serena_summary_corroboration: unavailable` is **expected** cross-session and is NOT a halt (V2 FM-13).
- **FR-12 Dry-run.** `--dry-run` / `--print-command` performs input derivation, env preflight, command construction, output reservation, and frontmatter parse, but does not launch reflect or edit the task file.

## 3. Non-Functional Requirements

- **NFR-1 Thinness.** ≤ ~400 LOC; zero reflect-logic duplication (no deviation-taxonomy/tier-rubric/promotion-gate strings authored in the module). Wrapper inspects contract fields only for gate routing + write-back; it never parses diff hunks or classifies deviations (V2 FM-18).
- **NFR-2 Reuse-first.** Subprocess lifecycle, signal handling, timeout, env scrub, stdin prompt delivery, stdout/stderr separation inherited from `ClaudeProcess`.
- **NFR-3 Reversibility.** Template change is a single opt-in item swap behind a config flag; default restores the HALT item byte-for-byte.
- **NFR-4 Fail-closed posture.** Inability to prove a full, non-degraded Tier-2 audit for a medium/complex POST gate routes to HALT.
- **NFR-5 Bounded runtime.** Default timeout **3600 s** (`--timeout` overridable; majority of V1/V3 over V2's 1800) → `ClaudeProcess` exit 124 surfaced as `blocked`/timeout, never a hang or false pass; SIGTERM→SIGKILL via process group.
- **NFR-6 SoT discipline.** Edits in `src/superclaude/` → `make sync-dev` → `.claude/`; never stage `.claude/` mirrors (CLAUDE.md ABSOLUTE RULE).
- **NFR-7 No-nesting guard.** The item invokes the wrapper as a **Bash shell-out**, never via Agent/Task; a guard test documents this (V1 R-4).
- **NFR-8 Unknown-field tolerance.** Parser ignores unknown contract fields; fails on missing load-bearing fields.

## 4. Architecture & Reuse Map

```
tasklist.md frontmatter ──derive(FR-3)──▶ /sc:reflect invocation
        │                                        │  ClaudeProcess.start()  ◀ REUSE pipeline/process.py
        │                              (top-level claude --print, FR-1; stdin prompt, FR-10 real-env)
        │                                        ▼
        │                              <output>/return-contract.yaml  ◀ reflect writes (SKILL.md §9)
        │                          ┌── preflight + post-contract degradation checklist (FR-11, fail-closed)
        └── write-back(FR-6) ◀ parse+map(FR-5) ──┘
                                          │
                            exit-code + reflect_post + sidecar (FR-7) ──▶ completion-gate
```

| Need | Reused primitive | Anchor |
|---|---|---|
| Top-level `claude --print` w/ `--model`, stdin prompt, timeout→124, SIGTERM→SIGKILL, env scrub, stdout/stderr split | `ClaudeProcess` (construct directly) | `cli/pipeline/process.py` |
| Optional visible detached window + attach + sentinel exit code | `launch_in_tmux` idiom | `cli/sprint/tmux.py` |
| `<BASE>..HEAD` resolution | `git merge-base` idiom | `cli/sprint/process.py` |
| Subcommand registration | `main.add_command(reflect_group, name="reflect")` | `cli/main.py` |
| Contract-consumer precedent (null convergence → partial → halt) | sprint executor status routing | reflect `SKILL.md` §8 |

**Deliberately NOT reused:** `HomeIsolation`/`ClaudeProcessAdapter` (`cli/eval/claude_process.py`) — see FR-10.

## 5. Window Mechanic

**Default = blocking foreground `ClaudeProcess` (no window)**: `proc.start(); rc = proc.wait()`; the shelling Bash item blocks until the wrapper returns its own exit code — unattended, tmux-independent (works in CI / nested tmux), testable, no sentinel round-trip. **`--tmux` opt-in** reuses sprint's detached-session + `attach` + `.reflect-exitcode` sentinel for operators who want to watch the 8-15 min run live. **`--print-command`** is the degenerate dry-run (prints the exact invocation). Detached-and-poll is intentionally NOT a third mode (foreground already blocks; `--tmux` already gives detach/reattach — a bespoke poller adds machinery for no new capability).

## 6. Verdict, Write-back & Gate Consumption

**Verdict derivation (first match wins; all fields from reflect `SKILL.md` §9.1):**

| Condition | verdict | exit |
|---|---|---|
| contract missing/unparseable, child crash, frontmatter unwritable, or preflight STOP | `blocked` | 2 |
| child rc==124 (timeout) | `blocked` (timeout) | 2 |
| chain-critical degradation per FR-11 (degraded grounding / diversity / adversarial / verification / citations_dropped / input_drift) | `degraded` | 11 |
| `status: partial`, or `regression_present` / `unauthorized_deviation_present` / `needs_human_decision` / `user_decision_required` / `drift>0` / `regression>0` | `halted` | 10 |
| `status: success` AND none of the above AND expected tier reached | `pass` | 0 |

This mirrors reflect's own 9-condition promotion gate **by reading its outputs**, never recomputing them.

**Frontmatter block (write-back):**
```yaml
reflect_post:
  verdict: pass | halted | degraded | blocked
  status: success | partial | failed | null     # raw contract status
  run_id: <output-dirname / iso-timestamp>
  tier_reached: 1 | 2 | 3 | null
  report: <abs path to REPORT.md>
  contract: <abs path to return-contract.yaml>
  reason: <short slug>                            # e.g. degraded-tier2, regression, timeout
  deviations: { authorized: N, necessary: N, drift: N, regression: N }
  head: <HEAD sha at run time>                    # resume/staleness
  reviewed_at: <ISO-8601>
```

**Gate consumption:** the Done item requires **both** exit 0 **and** `reflect_post.verdict == pass`; any other value HALTs and routes `report` + `reason` + `deviations` into the tasklist `### Open Questions`. A `<output>/wrapper-result.yaml` sidecar always records verdict/derivation/env-audit/child-exit/write-status (critical when frontmatter is unwritable).

## 7. Resolved Open Questions

1. **Window** → foreground-blocking default; `--tmux` opt-in (sprint sentinel); `--print-command` dry-run.
2. **Home** → new `superclaude reflect run` Click subcommand under `src/superclaude/cli/reflect/`, registered in `main.py` like sprint/roadmap/prd (discoverable, `CliRunner`-testable, packaged). Not `scripts/`.
3. **Input derivation** → builder bakes `--depth`(TCS, floored `standard`) + `<BASE>`; wrapper passthrough; explicit absolute `--tasklist`; `--spec` from frontmatter; `--executor-model` from frontmatter/env.
4. **Verdict write-back + gate** → dual signal (exit code + `reflect_post` block + sidecar); 4-state verdict; deviations → Open Questions; fail-closed.
5. **Headless env** → bare `ClaudeProcess` real-env overlay (pop nested-session vars); NOT `HomeIsolation`; preflight alias-count + post-contract degradation checklist.
6. **Runtime/budget** → default `--timeout 3600`; timeout → `blocked`; reflect owns its TurnLedger; re-run idempotent at frontmatter; optional `--resume` skips a still-clean HEAD.
7. **Template** → opt-in `POST_REFLECT_MODE: wrapper|halt` (default `halt`) in BUILD_REQUEST; when `wrapper`, the Phase-N item's **Action** shells `superclaude reflect run {TASK_FILE}` (Bash) instead of printing the manual command; HALT text byte-identical when unset.
8. **Promotion** → default `--no-promote` (hard prompt flag); `--promote` opt-in delegates to reflect's gated Wave 7; wrapper never mutates outside frontmatter + `<output>/`.

## 8. Subprocess Contract (implementation surface)

Prompt (stdin, bypassing `MAX_ARG_STRLEN`):
```
/sc:reflect --mode post --no-promote --diff <BASE>..HEAD --tasklist <abs> [--spec <abs>] --depth <standard|deep> --executor-model <class> --output <abs-pinned-dir>
```
`claude` argv (model + headless + permissions only — **reflect's `--output`/`--diff`/etc. live in the prompt, NOT the `claude` argv**; correcting V3's argv bug):
```
claude --print --verbose --output-format stream-json --model <resolved> --dangerously-skip-permissions --max-turns <N>
```
via `ClaudeProcess(prompt=…, model=…, timeout_seconds=3600, output_format="stream-json", env_vars=build_env())`; `proc.start(); rc = proc.wait()`. Files: `cli/reflect/{__init__,commands,config,models,runner,contract}.py`; registration line appended to `cli/main.py`; tests under `tests/cli/reflect/` (CliRunner + monkeypatched `ClaudeProcess` + fixture contracts → verdict/exit/write-back/no-nesting-guard assertions).

## 9. Scope Boundaries

**In:** the `reflect run` subcommand (launch + parse + fail-closed route + atomic race-safe write-back + exit contract), `--tmux`/`--print-command`/`--no-promote`(default)/`--promote`/`--timeout`/`--depth`(passthrough)/`--output`/`--allow-single-vendor`/`--dry-run`, the opt-in `POST_REFLECT_MODE: wrapper` template branch, the `wrapper-result.yaml` sidecar. **Out (hard non-goals):** no `sc:cli-portify`/Python port of reflect waves/tiers/taxonomy/promotion; never run reflect in an Agent-tool subagent; no auto-commit (default audit-only); no second behavioral copy of reflect logic; no new isolation/budget/poller machinery; UC-1 deferred (a future `reflect pre` subcommand — same launch, different prompt flags).

## 10. Risks

- **Contract drift (1.3.0→future):** verdict map reads §9.1 by name; gate on `contract_version`, unknown major → `blocked` fail-loud; map isolated in one `contract.py` function.
- **Degraded-but-pass leak:** mitigated by FR-11 fail-closed `degraded` verdict — the load-bearing defense (see §11 invariant probe).
- **Output collision across re-runs:** HEAD-suffixed `<task-dir>/reflect/post/<short-sha>/`; latest path recorded in `reflect_post.contract`.
- **Wired via Agent/Task (re-introduces nesting bug):** template says Bash shell-out; guard test + SKILL note (`reference_subagent_cannot_nest_skill_fanout`).
- **Parallel sessions share git index/frontmatter:** compare-before-write (FR-6); run the gate from the tasklist's own worktree (`feedback_parallel_sessions_share_index`); no index ops.
- **Single-vendor alias setups (common in local dev):** `degraded` halt unless `--allow-single-vendor` — noisy but preferable to a homogeneous "Tier 2".

## 11. Invariant probe (sufficiency challenge, Round 2.5)

**Claim:** "launching reflect as a top-level subprocess greens the Tier-2 gate." **Falsifier:** top-level launch is **necessary but not sufficient** — Tier 2 also requires ≥2 model aliases in the child env (FM-4), MCP grounding present (FM-3), and the child actually invoking the skill non-degraded. **Resolution (HIGH, ADDRESSED):** the gate must VERIFY actual non-degraded Tier-2 from the contract (`tier_reached==2`, `t2_model_class_diversity==full`, non-null adversarial merge, `verification_ran`) — i.e., FR-11's fail-closed `degraded` verdict. Without it the wrapper would assert sufficiency it never demonstrated. This is why V2's degradation detection is merged in as load-bearing, not optional.
