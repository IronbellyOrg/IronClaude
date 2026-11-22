# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 76.5% (13 of 17 points)
- Convergence threshold: 80% (command default; none passed)
- Focus areas: All
- Advocate count: 2 (default model each; Mode A has no `--agents`)
- Taxonomy coverage: L1 = 2 points, L2 = 8, L3 = 7. All levels covered, so no forced round.
- Caveat: both variants were written by the same session that ran the debate. The advocates were separate agents that re-read repo files, and they found real errors in Variant B (X-001, X-002, A-004). Treat the scores as one evaluator's judgment.

## Round 1: Advocate Statements

### Variant A Advocate (default model, persona: none)
**Position**: Variant A is closer to right, but only because of A-004. Spawning Orca workers from inside the brainstorm skill violates WC-8, so Variant B as written cannot ship. Best recommendation: keep Task fan-out inside the skill, harden it, and add `--unattended` so a coordinator can run brainstorm as ONE worker.

**Steelman of Variant B**:
"Multi-model" brainstorm today means opus, sonnet and haiku: one vendor, correlated blind spots. Orca's `--agent codex|cursor|opencode` is a real route to other model families. Worker output on disk survives a parent crash, a person can watch or stop one proposer, and an S2-only rollout behind a flag is a sensible low-risk start. B's worker contract (prompt file in, one result file out, verify on disk) matches how the repo already treats delivery signals.

**Key strengths claimed**:
1. Work is small: advocates run with `max_turns: 5`, get text inputs (`sc-adversarial-protocol/SKILL.md:1021-1028`), and are dispatched in one message block (`:1054`).
2. Retry exists today: a single failed advocate is retried once, then N-1 proceeds (`:1065-1072`). This defeats B's "only retried whole" claim (X-001).
3. The budget guard depends on Task: abort if cumulative tokens > 1.25 x estimate (`sc-brainstorm-protocol/SKILL.md:240`); Orca help shows no token field.
4. Blast radius: S2-S5 live in the shared 2985-line adversarial skill.
5. Cross-family diversity needs no Orca: `sc-bare-review` dispatches to external models.
6. The contract settles the layering: WC-8 ("A command never calls `worker-start`, `dispatch` or `task-create`"), WC-7 ("A command's own Agent-tool fan-out stays as it is"), and the fan-in example "N workers, then `/sc:adversarial --compare`".

**Weaknesses identified in Variant B**:
1. B's whole plan puts `worker-start` inside a skill, which WC-8 forbids.
2. B's context benefit (point 2) does not follow from its staged plan (point 6): `Skill sc-adversarial-protocol` runs in-session (X-002, A-002).
3. B's `--resume-from` reattach claim is unsupported; WC-6 says every retry is a new Task and `--retry-of` is never used.
4. B offers no replacement for the 1.25x kill rule.
5. B cites no repo file:line (S-001).

**Concessions**:
- `src/superclaude/commands/brainstorm.md` on this branch has no `## Unattended mode` section (0 matches), so the coordinator route is not usable from this checkout.
- A's "two dispatch paths forever" rests on the same wrong assumption as B (A-004).
- A's cold-start cost point is unquantified; so is B's.
- Cross-tier diversity is a real weakness; whether bare-review can generate proposals (not just reviews) is unverified.
- A has no answer for observability or resume.
- Only the 500K/650K thresholds were re-confirmed (`SKILL.md:238-239`).

### Variant B Advocate (default model, persona: none)
**Position**: Variant B as written is wrong about where Orca spawning belongs. WC-8 and WC-13 forbid a command or skill from calling `worker-start`. B's goals (cross-family diversity, isolation, resumability) are valid but belong to a coordinator-driven design: one `/sc:brainstorm --unattended` worker per Task, with the existing Task fan-out kept inside it.

**Steelman of Variant A**:
The spawned work is small and text-in/text-out. The hard-kill rule at 1.25 x estimate (`SKILL.md:240`, `:399`) depends on `token_usage.wave_3` "measured from Task notification" (`:371`), and Orca has no verified token field. S2-S5 live in the shared skill, and `sc-bare-review` is the cheapest route to diversity.

**Key strengths claimed**:
1. Orca coordination is a sanctioned pattern: WORKER-CONTRACT.md section 4 fan-in rule uses "N workers, then `/sc:adversarial --compare`".
2. The contract gives the context benefit when the whole `/sc:brainstorm` run is a worker: WC-4 `return-contract.yaml` on every outcome and WC-15 handoff files keep the coordinator on paths.
3. Resumability and control exist as coordinator rules: WC-6 (new Task per retry, carrying a resume note) and the S6/L4 ladder. `--retry-of` is forbidden, so B's mechanism is wrong though its intent survives.
4. Verify the file on disk, never the signal: WC-4 ("Orca does not check the file, so the coordinator opens it").

**Weaknesses identified in Variant A**:
1. The "two dispatch paths forever" cost assumes in-skill spawning; under WC-8 the skill holds no Orca code.
2. A frames the problem as Task versus Orca per agent; the unit that fits the contract is the whole command (A-001).
3. A is silent on parent-context pressure and on resume after a crash.
4. WC-10 accepts the heartbeat gap during a command's own Agent-tool fan-out, so A's "harden" path is compatible with the coordinator model; A frames them as exclusive.

**Concessions**:
- B's "only retried whole" claim is false for S2/S3 (`SKILL.md:1065-1072`).
- B's context benefit does not follow from its own staging plan.
- B's `--retry-of` contradicts WC-6.
- B cites no repo lines and ignores portability.
- B's telemetry fallback does not satisfy the hard-kill rule.
- Neither variant has latency or cost numbers.
- Not read: `refs/agent-spec-builder.md` and the adversarial command file; the threshold mismatch and the Unattended state were taken from the diff analysis.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | A | 78% | A cites file:line (`SKILL.md:1021-1028`, `:240`); B cites none |
| S-002 | Split | 60% | A's actions and B's mitigations both matter; B's are partly void under WC-8 |
| C-001 | A | 65% | `max_turns: 5`, text-in/text-out; B's S1+S2 merge is low value |
| C-002 | Unresolved (lean A) | 55% | A: split; B: A. Shared-skill blast radius is real, flag-gating helps little |
| C-003 | Split | 62% | A right on portability, B right in form; both moot under WC-8 |
| C-004 | Unresolved (lean A) | 52% | A: split; B: A. bare-review needs no Orca; its proposal support is UNVERIFIED |
| C-005 | A | 78% | 1.25x rule needs usage data Orca does not expose |
| C-006 | B | 60% | Only if the whole command is the worker (A-002) |
| C-007 | B | 70% | Live view, `worker-stop`, WC-6 retry; Task is opaque until return |
| C-008 | Unresolved | 50% | A: A (WC-6 forbids `--retry-of`); B: B (new Task with resume note recovers) |
| C-009 | Unresolved (lean B) | 55% | A: split; B: B. Verify-on-disk matches WC-4; Orca failure risk is real |
| X-001 | A | 90% | Single-advocate retry at `SKILL.md:1065-1072` |
| X-002 | A | 85% | The skill runs in-session; B's staging does not isolate context |
| A-001 | Agreed | 80% | A: QUALIFY, B: REJECT. Both say the whole command or Wave 3 is the right unit |
| A-002 | Agreed | 85% | Both ACCEPT |
| A-003 | Agreed | 80% | Both ACCEPT; cold-start cost must be measured |
| A-004 | Agreed | 90% | Both REJECT: WC-8, WC-13, WC-7 contradict in-skill spawning |

Omissions: none. Both advocates answered A-001 to A-004.

## Convergence Assessment
- Points resolved: 13 of 17
- Alignment: 76.5%
- Threshold: 80%
- Status: NOT_CONVERGED
- Unresolved points: C-002, C-004, C-008, C-009
- Note: the four open points are secondary. Both advocates independently reached the same recommendation (do not spawn Orca from inside the skills; use the coordinator layer), so the disagreement does not change the verdict.
