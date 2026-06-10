# sc:reflect — UC-1 Pre-Execution Coverage / Gap Audit

- **Mode:** pre (UC-1 coverage + best-practice audit)
- **Tier reached:** 1 (grounded single-pass; see Tier note)
- **Spec:** `.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md` (FR-1..12, NFR-1..8, §6 verdict table, §8 subprocess contract, §9 scope, §11 invariant probe)
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-20260608-185553/TASK-RF-20260608-185553.md` (42 checklist items, 7 phases + 4 adversarial QA gates)
- **Coverage:** 20/20 requirements have ≥1 addressing item (presence 1.00); **3 have material fidelity gaps** → effective coverage **0.90**
- **Best-practice grade:** 4/5
- **Calibrated confidence:** 0.88
- **Citations:** all Grounded (source-verified); 0 inferred-only load-bearing claims

---

## Verdict

**PROCEED WITH 3 FIXES.** This is a high-quality, well-grounded tasklist: every FR/NFR maps to a concrete checklist item, the safety-critical verdict map is isolated and protected by a dedicated adversarial QA gate (PG-2), and the §11 invariant probe (verify *actual* non-degraded Tier-2 from the contract) is explicitly tested. Three implementation-fidelity gaps sit *inside* otherwise-covered requirements and should be closed before execution — one of them (G1) can systematically defeat the spec's headline success criterion.

---

## Findings

### G1 — `--max-turns` left at the `ClaudeProcess` default of 100 (HIGH)

**Requirement:** §8 subprocess contract (`claude … --max-turns <N>`); seed success criterion "full reflect run incl. Tier 2 with zero human intervention in the common path."

**Evidence:**
- `src/superclaude/cli/pipeline/process.py:43` — `max_turns: int = 100` (constructor default).
- `process.py:73-95` `build_command()` emits `--max-turns str(self.max_turns)` → child always gets a turn ceiling.
- Step 3.5 constructs `ClaudeProcess(prompt=…, output_file=…, error_file=…, model=…, timeout_seconds=…, output_format="stream-json", env_vars=None)` — **`max_turns` is not passed**, so it defaults to 100.
- `grep -niE 'max.?turns'` over the tasklist → **zero matches** (the knob is never set, tested, or raised as an Open Question).
- research `01-claudeprocess-primitive.md:40` documents the default=100 but no override guidance.

**Why it matters:** A Tier-2 POST reflect is a heavy single-session orchestration (heterogeneous reviewers + `sc-adversarial` merge + `evidence-validator` + promotion gate). 100 top-level turns is plausibly insufficient; on the ceiling the child truncates → no/partial `return-contract.yaml` → wrapper routes `blocked`/`degraded` → gate HALTs. The failure is *fail-closed* (safe), **but** it can make the common path HALT for exactly the medium/complex tasklists the wrapper exists to automate — silently negating "zero human intervention in the common path." The 3600 s timeout (NFR-5) does not help: the turn ceiling binds first.

**Recommendation:** Add an explicit `max_turns` to the Step 3.5 `ClaudeProcess(...)` call sized for T2 reflect (suggest a `--max-turns` config knob defaulting ~200–300, or a justified fixed value), and add a verdict/e2e fixture-test asserting it is passed. At minimum, promote this to an Open Question with a flagged default rather than inheriting 100 implicitly.

### G2 — `--resume` is declared but inert (no skip-on-clean-HEAD behavior) (MEDIUM)

**Requirement:** §9 scope (`--resume`); §7 resolved-OQ-6 "re-run idempotent at frontmatter; optional `--resume` skips a still-clean HEAD."

**Evidence (`grep -niE 'resume'` over the tasklist):** `resume` appears only as declarations —
- Step 2.1 `models.py`: `resume: bool` dataclass field.
- Step 2.2 `config.py`: `resume=False` `resolve_config` parameter.
- Step 4.1 `commands.py`: `--resume` (is_flag) option + help-text assertion (Step 4.5).
- **No step implements behavior.** Step 3.5 `ReflectRunner.run()` never reads `config.resume`; there is no "if HEAD unchanged and prior `reflect_post.verdict == pass`, skip and exit 0" branch anywhere.

**Why it matters:** `--resume` ships as a no-op flag — present in `--help`, accepted, and silently ignored. An operator re-running the gate on a clean HEAD will pay a full 8–15 min Tier-2 run that `--resume` promised to skip.

**Recommendation:** Either (a) add a runner short-circuit in Step 3.5 — read existing frontmatter `reflect_post.head`; if it equals current HEAD and prior `verdict == pass`, skip launch and exit 0 — plus a test; or (b) drop `--resume` from §9 scope for v1 and remove the field/flag. Do not ship a declared-but-inert flag.

### G3 — FR-3 depth passthrough dropped in the wrapper template arm (MEDIUM)

**Requirement:** FR-3 — "the builder bakes the resolved `--depth` (and `<BASE>`) into the item command; the wrapper treats them as **passthrough** to avoid builder/wrapper TCS drift (V1 R-6)."

**Evidence:**
- The existing halt-arm bakes TCS depth: `src/superclaude/skills/task-builder/SKILL.md:1996` emits `… --depth {DEPTH} …` (`{DEPTH}` floored at `standard`).
- Step 5.3 wrapper-arm emits **`superclaude reflect run {TASK_FILE}`** — no `--depth {DEPTH}`.
- Step 2.2/4.1: config/CLI `--depth` defaults to `standard`; config.py performs **no** TCS derivation.

**Why it matters:** A `complex` tasklist whose TCS resolves to `deep` would run reflect at `standard` through the wrapper — the exact builder/wrapper TCS drift FR-3 was written to prevent. **Mitigating factor:** `expected_tier == 2` for both `standard` and `deep` (POST floors at `standard`), so Tier-2 *still fires*; the loss is `deep`-specific rigor (3rd reviewer / socratic pass), not Tier-2 itself. That is why this is MEDIUM, not HIGH.

**Recommendation:** Step 5.3's wrapper-arm should emit `superclaude reflect run {TASK_FILE} --depth {DEPTH}` (TCS passthrough), mirroring the halt-arm. The config `--depth` option already accepts it — only the emitted template string needs the baked token.

### G4 — NFR-1 ≤~400 LOC budget never measured (LOW)

**Requirement:** NFR-1 "≤ ~400 LOC."

**Evidence:** PG7.2 checks thinness *qualitatively* ("genuinely THIN — no reflect-logic duplication"); no item measures package LOC. Soft "~" target, so low risk.

**Recommendation (optional):** add a one-line `wc -l src/superclaude/cli/reflect/*.py` assertion to Step 7.1 or PG7.2.

### G5 — halt-arm vs wrapper-arm base-branch asymmetry (LOW / informational)

**Evidence:** existing halt item uses `git merge-base HEAD <integration>` (`SKILL.md:1996`); wrapper `config.py` defaults `base_branch="master"` (OQ1). The two arms can compute a different `<BASE>`.

**Assessment:** Acceptable — OQ1 correctly identifies `master` as the right trunk for this repo (`origin/HEAD → master`) and flags `integration` as the wrong-base hazard. Recorded so the asymmetry is conscious, not accidental.

---

## Strengths (recorded so they are not regressed during execution)

- **Full requirement coverage:** all 12 FR + 8 NFR map to ≥1 checklist item; the In-scope §9 flag set is declared exactly (Step 4.1).
- **Safety-critical core isolated + gated:** `contract.py` (verdict map + FR-11 routing + version gate) imports only `.models` + stdlib, and is verified by a dedicated adversarial QA gate **PG-2** *before* the runner is built on top of it — the load-bearing defense per §11.
- **Invariant probe operationalized:** PG7.1/PG7.2 explicitly verify *actual* non-degraded Tier-2 (`tier_reached==2`, `t2_model_class_diversity==full`, non-null adversarial merge, `verification_ran`) and that a single-vendor "Tier 2" / expected-T2-but-ran-T1 is rejected and benign telemetry tokens do not over-HALT.
- **Reused primitive is sound:** `ClaudeProcess.build_command()` already supplies `--dangerously-skip-permissions`, `--no-session-persistence`, `--tools default`, `--output-format`, and `build_env()` scrubs `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` while copying `os.environ` (verified `process.py:73-112`) — FR-1/FR-10 rest on real behavior, not assumption.
- **Task self-corrected a real source drift:** Step 5.4's AX-1 note is **accurate** — `SKILL.md:2108` is the genuine Rule #19 `/sc:reflect` hardcode to broaden; `SKILL.md:2051` is presence/position only and must stay byte-unchanged (both verified). The task correctly forbids inventing a hardcode into L2051.
- **OQ posture is correct** per memory `feedback_human_decision_items_must_halt`: the 5 Open Questions use *recommended default + flag in Task Log*, none ship a destructive wrong-base silently (OQ1 default `master` is correct), and Post-Completion Step 338 mandates documenting each OQ's resolution.
- Fail-closed exit contract (only clean non-degraded T2 → 0), atomic compare-before-write write-back, always-on sidecar, and the two-layer no-nesting guard are all explicitly specified and tested.

---

## Tier note

The §5.3 rubric would **escalate to Tier 2** on rule 4 (`S_domains ≥ 3`: Python CLI + skill template + tests). I capped at **Tier 1** because all three load-bearing findings (G1, G2, G3) are **factual and directly source-verified** (`process.py:43`, the `resume` declaration-only grep, `SKILL.md:1996/2051/2108`), not judgement calls a heterogeneous reviewer ensemble would overturn. If you want independent cross-model confirmation before acting, re-run with `--depth deep` (forces Tier 2) — see next-move prompts.

## Grounding gaps

None. Every load-bearing citation was re-Read from current source this turn.
