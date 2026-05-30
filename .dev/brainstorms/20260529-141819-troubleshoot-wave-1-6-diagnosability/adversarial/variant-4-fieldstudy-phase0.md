# Variant 4 — Field Study (Phase 0 Observability-Sufficiency Gate)

**Provenance**: This variant is NOT a fresh agent generation. It is a session-replay artifact authored from a real-world `sc:troubleshoot`-adjacent debugging session (T4 contract test, 2026-05-29) where ~50k tokens of hypothesis work and three CI rounds were spent before the breakthrough — `find /tmp -name '*zellij*'` — was discovered. Promoted to peer variant status by user decision (Option A, 2026-05-29) on the grounds that real-failure-mode evidence is debate-worthy alongside synthetic agent perspectives.

**Per-fork stance vs settled brief decisions**:

| Settled fork | Field-study position | Disposition in merge |
|---|---|---|
| Scope = "logging only (narrow)" | Field-study advocates broader (CLI flags + OS introspection + doctor commands) | **REJECTED by settled-fork lock — user maintained narrow scope.** Field-study's broader-scope arguments remain in this doc for record but do not promote to merged spec. |
| Placement = between Waves 1.5 and 1.7 | Field-study advocates pre-Wave-1 ("Phase 0") | **REJECTED by settled-fork lock — user maintained between-1.5-and-1.7 placement.** Field-study's earlier-gate argument is on record but does not promote. |
| Default-on, opt-out | Field-study: same (`--skip-phase-0`) | **CONVERGES** — variant adopts the field-study's "bypass-is-logged" discipline as an additive. |
| Hard-stop + tasklist on insufficient | Field-study: same, with sharper rhetoric ("no hypothesis work in the same turn as an instrumentation patch") | **CONVERGES** — adopt the field-study rhetorical framing. |

**Additives the field study brings that synthetic variants miss** (these promote into the merged spec):

1. **Byte-count metric** — every stream gets a captured-bytes column; `0 bytes` is a gap signal sharper than "do logger calls exist." (§3.3 S0.2)
2. **Invocation-site-only instrumentation rule** — the tasklist MUST patch test scripts, CI YAML, or dev harnesses, NEVER the failing component's own source. (§6 risk #2 mitigation)
3. **3-round patch-loop cap** — after 3 instrumentation rounds, escalate to "structural change needed." Closes Open Question #6 (re-run loop UX) cleanly. (§3.7)
4. **Heisenbug fallback** — if instrumentation alters timing and the bug stops reproducing, that is itself signal; fall back to lighter-weight instrumentation (env-vars only, no flag changes). (§6 risk #3 mitigation)
5. **Component-identification step (S0.1)** — explicitly named substep: "identify the smallest component whose output the failure is asserting against." Sharper than relying on `--scope` alone.
6. **"No hypothesis work in the same turn as an instrumentation patch"** — load-bearing temporal-discipline rule. Adopt as Wave 1.6's contract verbatim.
7. **Worked T4 example** — concrete grounded case study for the new `refs/diagnosability-audit.md` ref.
8. **`--skip-diagnosability-audit` logged on bypass** — auditability discipline. Adopt verbatim.

The verbatim source document follows, unmodified except for this provenance header.

---

# sc:troubleshoot — Observability-Sufficiency Gate (Phase 0)

**Author:** session replay 2026-05-29
**Trigger session:** T4 contract-test debugging across PR #43 / PR #45, ~7 turns of hypothesis generation before the first byte of actionable daemon evidence was captured.
**Driving insight:** Every Tier-1/Tier-2 analysis run on this defect re-asked "what is the root cause?" against a log set that contained *zero* daemon-side evidence. Models obediently produced hypotheses. Hypotheses cost tokens. None of them could be falsified by the data we had — so we picked the most plausible one, implemented it, and went back to CI for another empty `zellij.log`. Three CI rounds, three reflection passes, ~40k tokens of "deep analysis," and the actual breakthrough — `find /tmp -name '*zellij*'` revealing `/tmp/zellij-1000/zellij-log/zellij.log` — was a four-second shell command we never ran.

This document specifies the **Phase 0 Observability-Sufficiency Gate** that `sc:troubleshoot` must execute before any hypothesis-generation, multi-agent fanout, or remediation token is spent.

---

## 1. The failure mode this prevents

Current `sc:troubleshoot` flow (paraphrased from the protocol skill):

1. **Tier 1 triage** — auggie + serena grounding, single agent, fast triage.
2. **Tier 2 escalation** — parallel hypothesis agents + adversarial fix debate.
3. **Tier 3 remediation** — task-builder hand-off.

The skill assumes the **input evidence is adequate to discriminate hypotheses**. It does not validate that assumption. When the input is a one-line failure (`FAIL headless session 'aidev02-t4-1' did not register within 15s`) and an empty `zellij.log`, the skill happily generates hypotheses against an empty evidence set. The hypotheses are unfalsifiable by construction.

The pathology is structural, not a model failure:
- Models are trained to produce plausible explanations from whatever evidence is presented.
- When evidence is sparse, plausibility-ranking degenerates into prior-ranking.
- Priors come from training data + the user's framing.
- Confidence calibration cannot help — the rubric is "given this evidence, how confident am I?" with no term for "is this evidence sufficient at all?"

In this session that produced:
- Two competing PRs (#43, #45) embedding **opposite** fixes (CLI `--default-shell` vs config.kdl, `rename-pane --pane-id` vs OSC 0) — both perfectly defensible from the empty-evidence set, neither testable against it.
- A `deep-research-report.md` that confidently named `ZELLIJ_SOCKET_DIR` as the canonical CI fix, when (a) the env var exists but (b) the actual binding location was undocumented (`contract_version_1/` subdir, not `zellij/<version>/`) and (c) the daemon writes its real log to a hardcoded `/tmp/zellij-<uid>/zellij-log/zellij.log` that no doc or upstream issue mentioned.
- Three CI rounds, each producing empty `zellij.log`, each consumed by a fresh reflection pass that concluded "still an infrastructure issue."

The total cost of *not* asking "are our logs sufficient before we start guessing?" was ~3 days of wall-clock + ~50k tokens of agent work + two reviewer-hours.

---

## 2. The change in one sentence

> **Before any hypothesis generation, `sc:troubleshoot` MUST inventory the observability surface of the failing component, enumerate unused logging/diagnostic options available within that component, and either declare the surface sufficient (with evidence) or implement every cheap unused option and re-run the failure before proceeding.**

"Cheap" is defined narrowly: pure additions to existing log dumps, native `--debug`/`--verbose` flags, OS-level introspection commands (`ls`, `find`, `strace`, `lsof`), and `*-check`/`*-doctor` subcommands the failing tool ships with. **Not** new test scaffolding, not new code paths, not refactors.

---

## 3. Phase 0 specification

### 3.1 Trigger conditions (when Phase 0 runs)

Phase 0 runs **unconditionally** at the start of every `sc:troubleshoot` invocation. There is no opt-out. However, the gate may **exit fast** (Section 3.4) when sufficiency is trivially demonstrated.

### 3.2 Inputs

- Failure transcript / error output (as provided by user).
- All log files / artifacts referenced in the failure transcript.
- The repo (for locating logging-config files, CI workflow definitions, dockerfiles).

### 3.3 Phase 0 sub-steps

**S0.1 — Failing-component identification.** Identify the smallest component whose output the failure is asserting against. In our case: the `zellij attach --create-background` daemon, not "the contract test" and not "the CI runner."

**S0.2 — Log-surface inventory.** Enumerate every log/output stream produced by S0.1 in the current run. For each: Path or stream name; Capture mechanism in the failing run; **Byte count of actual content captured.**

For T4 this would have produced (rows with `0 bytes` or `NOT inspected` / `NOT enabled` are gaps): `zellij.log` captured via `> "${ZELLIJ_LOG}" 2>&1` on foreground client — 0 bytes; `zellij-shim.log` captured via shim 2>(...) redirect — 0 bytes (no STDERR entries); socket dir contents NOT inspected; zellij daemon log (/tmp/zellij-<uid>/) NOT inspected; zellij --debug flag output NOT enabled; zellij setup --check NOT invoked; syslog / journalctl NOT inspected; strace of daemon NOT enabled.

**S0.3 — Unused-options inventory.** For the failing component, list its `--help`, `setup --check`, `--version`, `--debug`, `--verbose`, `--log-level`, `--log-file`, `--diagnostic`, `--dump-config` and equivalent flags. For each, mark whether it is in use in the failing invocation.

Example for zellij 0.44.x: `--debug` not in use, `setup --check` not invoked, `setup --dump-config` not invoked, `setup --dump-layout` not invoked, `ZELLIJ_LOG_LEVEL` env not set, native daemon log at `/tmp/zellij-<uid>/zellij-log/zellij.log` not read.

**S0.4 — Sufficiency verdict.** The gate calls the evidence set **sufficient** iff: every output stream from S0.2 is captured with > 0 bytes of content, OR every gap in S0.2/S0.3 has a *documented* reason for being closed. In every other case the gate calls the evidence set **insufficient** and emits a **Phase-0 instrumentation patch** (Section 3.5).

**S0.5 — Sufficiency justification.** The verdict is accompanied by a one-sentence justification per stream/option.

### 3.4 Fast-exit conditions

Phase 0 MAY exit fast (skip S0.5 verbosity, skip patch generation) when: the failure is a syntax error / parse error / unambiguous single-line traceback with full stack to user-code; the failure is in a test the agent just authored in the same session AND the test file is the only artifact involved; the failing component is purely deterministic with no side channels (e.g., a pure function under unit test).

Default: do NOT fast-exit. CI failures, integration test failures, daemon/server failures, anything involving IPC or sockets — all require full Phase 0.

### 3.5 Phase-0 instrumentation patch

When sufficiency is denied, the gate produces a patch to the failing-component invocation site that: adds every cheap unused diagnostic option identified in S0.3; captures every uncaptured stream identified in S0.2; adds OS-level introspection that runs on failure (`ls -la`, `find`, `cat` of auto-rotated logs); **does not change the bootstrap line or production code path** — additions only.

The patch is committed and pushed. The pipeline is re-run. The troubleshoot then **HALTS** and waits for new evidence. It does NOT proceed to hypothesis generation, fanout, or remediation in the same turn.

**Load-bearing rule: no hypothesis work happens in the same turn as an instrumentation patch.** Mixing them re-creates the original failure mode (guessing while waiting for evidence). The gate's contract with the user is "I'm going to make this loud first; you re-run; we'll meet here with real signal."

### 3.6 Outputs

`phase0-log-surface-inventory.md`; `phase0-unused-options-inventory.md`; `phase0-sufficiency-verdict.md`; `phase0-instrumentation-patch.diff` (when insufficient); user-facing summary ending with either "**EVIDENCE SUFFICIENT — proceeding to Tier 1**" or "**EVIDENCE INSUFFICIENT — patch applied, halt for next-run signal**".

### 3.7 Exit criteria for re-entry

When the user returns with new evidence after a Phase-0 patch round, the troubleshoot re-enters at S0.4 against the new evidence set. **Hard cap: 3 Phase-0 patch rounds per defect.** After 3, escalate to user with a "this isn't observable through cheap additions; structural change needed" report.

---

## 4. What Phase 0 would have done in this session (T4 worked example)

S0.1 failing component: `zellij attach --create-background` (the daemon). S0.2 log-surface inventory: every row a gap (0 bytes captured, daemon log not inspected, socket dir not inspected, journalctl/dmesg not inspected). S0.3 unused options: 6 cheap options unused (`--debug`, `setup --check`, `setup --dump-config`, `ZELLIJ_LOG_LEVEL`, `RUST_LOG`, `RUST_BACKTRACE`). S0.4 verdict: INSUFFICIENT. S0.5 instrumentation patch:

```diff
+ # Phase-0 instrumentation: capture every cheap evidence stream.
+ export RUST_BACKTRACE=1 RUST_LOG=zellij=debug
+ "${ZELLIJ_BIN}" setup --check 2>&1 | tee -a "${WORK}/zellij-setup-check.log"
+ find "${ZELLIJ_SOCKET_DIR:-/tmp}" /tmp /run /var/run "${HOME}/.cache" \
+     -maxdepth 5 -name '*zellij*' 2>/dev/null | tee "${WORK}/zellij-host-inventory.txt"
- "${ZELLIJ_BIN}" attach --create-background "${SESSION}" options --default-layout default
+ "${ZELLIJ_BIN}" --debug attach --create-background "${SESSION}" options --default-layout default
+ cat "/tmp/zellij-$(id -u)/zellij-log/zellij.log" 2>/dev/null | tee -a "${ZELLIJ_LOG}"
```

This patch is <20 lines, additive, no behavior change to the bootstrap. Turn 2 would have begun with `/tmp/zellij-1000/zellij-log/zellij.log` in hand instead of three rounds of inferred hypotheses.

---

## 5. Risks and tradeoffs

**R1: latency.** Phase 0 adds at least one CI round to every troubleshoot. *Mitigation:* fast-exit conditions §3.4.

**R2: instrumentation drift.** Adding `--debug` flags and log-tee blocks to production-shipped code paths can leak into release artifacts. *Mitigation:* Phase 0 only instruments at the **invocation site** (test scripts, CI workflow YAML, dev harnesses). Never patches the failing component's own source. Patch annotated `# Phase-0 instrumentation: revert after defect closed.`

**R3: instrumentation hides the bug.** Adding `--debug` may alter timing and mask the failure. *Mitigation:* If the failure no longer reproduces under instrumentation, that itself is signal — record as Heisenbug finding, fall back to lighter-weight instrumentation (env-vars only, no flag changes), try again.

**R4: agent fixates on instrumentation and never advances.** The 3-round cap exists for this.

**R5: user wants a guess anyway.** *Mitigation:* allow `--skip-phase-0` flag, but require it to be explicit. Cannot be implicit. **The flag's presence is logged in the troubleshoot's output so post-mortems can see "this troubleshoot ran without observability validation."**

---

## 6. Persona-distinctive claims (positions to debate)

1. **"No hypothesis work in the same turn as an instrumentation patch."** This is the load-bearing temporal-discipline rule. Variants that emit a tasklist AND continue to Wave 1.7 in the same turn re-introduce the failure mode this gate exists to prevent. *Defensible because* the T4 session demonstrates the cost empirically — every hypothesis generated against the empty evidence set was wrong, despite being internally consistent. *If I'm wrong it's because* the soft-warn (`insufficient + trivial`) path is sometimes the right call — but even then, the temporal split (emit tasklist → halt → wait for re-run) is the correct discipline.

2. **"Byte-count is the right primitive metric for log-surface sufficiency, not call-density."** Synthetic variants count logger calls and grade by density. The field study grades by *captured-bytes-of-content*. A function with 5 `logger.info` calls but 0 bytes captured at runtime (filtered out by config, redirected to /dev/null, or never executed on the failing path) is identically blind to a function with 0 logger calls. Static call density without runtime byte-count is a degraded proxy. *Defensible because* the T4 session had logger calls; they captured nothing. *If I'm wrong it's because* runtime byte-counts are unavailable at audit time in many cases — but they ARE available for the failing run, which is what the audit is grading.

3. **"Instrument the invocation site, never the failing component's source."** This is a hard safety rule that synthetic variants did not surface. Patching production source for diagnostic purposes is how diagnostic code leaks into release artifacts. The audit's tasklist must explicitly constrain its targets to test scripts, CI workflows, and dev harnesses. *Defensible because* the alternative — patching `worker.py` with `logger.debug` calls that survive merge — is a well-documented industry anti-pattern. *If I'm wrong it's because* sometimes the source IS the right place (e.g., a long-running service whose invocation site is `systemd start foo.service` with no other surface) — but in those cases the patch is to the service config, not the source.

4. **"3-round patch-loop cap is non-negotiable."** Without it, agents will iterate indefinitely on instrumentation in pursuit of a never-arriving "sufficient" verdict. The cap forces escalation to "this defect isn't observable via cheap additions; structural change needed." *Defensible because* infinite iteration is the default failure mode for any rubric-gated loop without an explicit cap. *If I'm wrong it's because* 3 may be too few for genuinely complex defects — but the cap is a floor; users can bypass with `--skip-diagnosability-audit` if they accept the deeper investigation cost.

5. **"`--skip-phase-0` MUST be logged with the verdict."** Bypassing the audit is a legitimate user choice; hiding that bypass from post-mortem readers is not. Every troubleshoot REPORT.md must show whether the audit ran. *Defensible because* this is an auditability discipline borrowed from CI/CD norms (every skip is recorded). *If I'm wrong it's because* this adds a line of noise to every report — but the cost is one line, and the value is post-mortem accountability.

---

## 7. Generalization (out of scope for v1, noted for follow-up)

The same gate applies to any reasoning skill where the model's output quality is bottlenecked by input evidence richness — `sc:analyze`, `sc:reflect` UC-2, `sc:auggie-review` against opaque PRs. Phase 0 is fundamentally an **epistemic hygiene check**. A follow-up document should propose extracting Phase 0 into a shared `epistemic-sufficiency-gate` skill that other protocols can compose. **Tracked for v1.1; out of scope for this merge.**
