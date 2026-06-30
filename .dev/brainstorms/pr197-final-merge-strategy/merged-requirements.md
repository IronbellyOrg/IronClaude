---
topic: "Plan the merge of open PR #197 (feat/rf-harness-sync) into master of IronbellyOrg/IronClaude"
domain: process
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
created: 2026-06-28T17:50:00Z
grounding:
  master_head: cda6e2d4526c73a3d2739a3bf6efb500c4402f60
  pr197_head: b01b33e3b2bb009e9be2da8e798e9015a5d22821
  pr197_state: "OPEN, MERGEABLE, 5 ahead / 0 behind, zero git conflict, 18 files, +7920/-664"
  verified: "gh pr diff 197 + git show origin/master:<path> + 3-agent adversarial panel"
adversarial:
  decision_a_split: "instance-level 0.72 (pro) vs exclusion 0.62 (pro) — genuine near-even fork"
  decision_b_convergence: "REJECT directive+guard-loosening, 0.9 (falsification attempt failed)"
---

# PR #197 → master: Final Merge Strategy

**Bottom line.** PR #197 is git-clean but **not safe to merge wholesale** — as-is it would *regress* master on two axes (it deletes master's executor-class anti-self-confirmation guarantee and loosens the no-nesting safety guard). The high-value play is to **reduce #197 to its net-new additive value** (3 doc skills, EV-1…EV-4 on-disk verification gates, `reflect_post_mode`/`--cli`, `/task` lens QA, rf-agent fixes) **ported onto master's canonical 1.7.0 reflect shell**, and **drop the reflect runner/guard changes entirely**. One genuine product fork (Decision A) needs your sign-off; everything else is determinate.

Two decisions drive the whole plan:

- **Decision A (anti-self-confirmation model):** near-even adversarial split. **Recommended default: KEEP master's executor-class EXCLUSION** (reject #197's instance-level rewrite) — but this is a real product call; a hybrid "Option C" is documented and is arguably best.
- **Decision B (runner `inline_directive` + guard loosening):** **REJECT** with high confidence. The directive is not merely dead on master's ensemble route — it instructs the Tier-1 recipient to run waves that don't exist on its path, and its only side effect is to force-weaken a load-bearing safety guard.

---

## 1. ACCEPT-FROM-197 AS-IS

Additive, model-agnostic, no coupling to either decision. These are why the PR exists; land them first.

| # | Path | Nature | Evidence |
|---|------|--------|----------|
| 1 | `src/superclaude/skills/operational-guide/SKILL.md` | **NEW** doc skill (+1656) | pure addition |
| 2 | `src/superclaude/skills/readme/SKILL.md` | **NEW** doc skill (+2161) | pure addition |
| 3 | `src/superclaude/skills/roadmap/SKILL.md` | **NEW** doc skill (+2678) | pure addition |
| 4 | `src/superclaude/skills/tech-reference/SKILL.md` | rewrite (±437) | no reflect-model coupling tokens (verified grep) |
| 5 | `src/superclaude/skills/tech-research/SKILL.md` | rewrite (±827) | no `executor-class`/`instance-level`/`class-removing` tokens (verified) |
| 6 | `src/superclaude/skills/task/SKILL.md` | `/task` lens-based multi-agent QA (±343): ≥6 agents (3+ rf-qa structural lenses + 3+ rf-qa-qualitative content lenses) + serialized fix + post-completion validation | model-agnostic; the `subagent_type: rf-qa` references live in a **markdown skill**, not `runner.py`/`ensemble.py`, so the no-nesting guard never inspects them |
| 7–11 | `src/superclaude/agents/{rf-assembler,rf-task-builder,rf-task-executor,rf-task-researcher,rf-team-lead}.md` | tavily MCP-name fixes + RF sync (small, corrective) | additive agent-def tweaks; zero git conflict with master |

**Note on #6 (`/task` lens QA):** it embeds the `**ADVERSARIAL STANCE**` + `fix_authorization: false` pattern (matches project memory `feedback_rfqa_adversarial_pattern`) — good. It is independent of the reflect decisions.

---

## 2. REJECT-OR-DROP-FROM-197

Dead, weaker, or actively harmful on master. Restore master's version / do not add.

| Path | Disposition | Why |
|------|-------------|-----|
| `src/superclaude/cli/reflect/runner.py` (the `inline_directive` in `_build_prompt`) | **DROP** — `git checkout origin/master -- <path>` | Master's Tier-2 route is `run_tier2_ensemble` (in-process swarm dispatch). `_build_prompt()` is consumed **only on the Tier-1 branch** (`runner.py:462`), never the ensemble branch (`runner.py:452`). Tier-1 has **no Wave 3/3C/4** (SKILL.md:688) — so the directive tells its only recipient to "spawn Wave 3/3C/4 reviewers as YOUR OWN subagents," waves that don't run there. The directive's own comment concedes it is "best-effort defense-in-depth only" (`runner.py:382-385`). **Decision B.** |
| `tests/cli/reflect/test_no_nesting_guard.py` (guard loosening `subagent` → `subagent_type`/`Agent(`) | **DROP** — keep master's strict guard | The loosening exists *only* to admit the directive's prose: the sole new `"subagent"` tokens are inside the directive (`runner.py:381/389/391`). Master's bare-`"subagent"` ban is load-bearing precisely against **prose-described nesting** — the exact regression class #197 reintroduces. Remove the directive → master's strict ban passes at zero cost. |
| `tests/cli/reflect/test_inline_directive.py` (**NEW**, +50) | **DROP** — do not add | Locks in the directive's presence; meaningless once the directive is dropped. |
| `…/sc-reflect-protocol/refs/reviewer-spec.md` (instance-level rewrite, ±24) | **REJECT** (under recommended Decision A) — keep master | Entirely the instance-level-independence rewrite; replaces master's "Executor-class exclusion rule" + "Post-removal logic". |
| `…/sc-reflect-protocol/refs/reflection-rubric.md` (instance-level rewrite, ±13) | **REJECT** (under recommended Decision A) — keep master | Entirely the rewrite of the §11.3 three-way partition → two-way; deletes the `executor_model_class NOT IN reviewer_model_classes` grader assertion. |
| Instance-level hunks **within** `…/sc-reflect-protocol/SKILL.md` (§7.1, §11.3, input-resolution `--executor-model` "ignored" line, telemetry deletion) | **REJECT** (under recommended Decision A) | Same file also carries EV-1/EV-2 (see §3) — this file needs **hunk-level** surgery, not file-level accept/reject. |

---

## 3. PORT-WITH-MODIFICATION

Net-new value bundled in files that also carry rejected hunks → land the value onto master's 1.7.0 + exclusion shell, reworded.

### 3.1 EV-1 + EV-2 → `sc-reflect-protocol/SKILL.md` (hunk-level port)

- **EV-1 — Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate** (§8): orchestrator must read disk (Glob/Bash, not a self-written field) to confirm `adversarial/merged-verdict.yaml` with `merge_method: adversarial` AND `reviewer-cards/` ≥ resolved `--reviewers` (min 2), OR a corroborated loud F2/F3 fallback; MALFORMED → bounded re-run ×2, do not halt-and-end. **Port verbatim.** Its reference to "§7.1 N=2 T2 floor" **survives** — master §7.1:620 carries "N=2 minimum for T2" (verified).
- **EV-2 — `merge_method` legal-values guard** (§9 + `metrics.json`): legal values are exactly `{adversarial, single-reviewer-fallback}`; any other (`inline`, `convergence-inline`) is MALFORMED; reflect MUST NOT synthesize its own merge. **Port verbatim** (model-agnostic).
- **§12 eval-matrix detector** line: `dir_count min_files=6` → `file_present + card_count` (`merged-verdict.yaml` present + `reviewer-cards` ≥ `--reviewers`). **Port** (tied to EV-1).
- **MODIFY — contract changelog comment:** master keeps `contract_version: "1.7.0"`. Rewrite #197's `# … 1.5.1: instance-level … replaces executor-class exclusion …` note to drop the instance-level claim; keep only: `1.7.x runtime/semantic hardening: EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate + EV-2 merge_method legal-values guard (no stable-field change)`. **No stable field changes; contract_version stays 1.7.0.**

### 3.2 EV-3 + EV-4 + `reflect_post_mode`/`--cli` → `task-builder/SKILL.md` (hunk-level port)

- **EV-3/EV-4 — task-builder POST on-disk verification** (both the dedicated-subagent-runner POST item and the CLI-wrapper POST item): executor must independently read the runner's/wrapper's on-disk `adversarial/` dir and confirm `merged-verdict.yaml` + reviewer-cards ≥ reviewers, OR corroborated fallback; `exit==0`/`waves_attestation`/`reflect_post` are necessary-not-sufficient. **Port** (model-agnostic).
- **`reflect_post_mode: cli|skill` + `--cli` flag + `CLI_MODE` BUILD_REQUEST field** (default OFF = skill mode): emits the `superclaude reflect run` wrapper POST gate instead of the in-session subagent runner; writes `start_commit`/`executor_model_class` frontmatter. **Port.** (Aligns with project memory `reference_subagent_cannot_nest_skill_fanout` — the disclosure that only the `--cli` wrapper path is session-validated is accurate and worth keeping.)
- **MODIFY — "CLI mode anti-self-confirmation (POST engine binding)" clause 1:** #197 wording pins the POST engine to *"OUR `sc-reflect-protocol` SKILL (instance-level independence), NOT IC's class-removing variant."* Under the recommended Decision A this polarity is **inverted** — flip to: *"…OUR `sc-reflect-protocol` skill (the canonical executor-class-exclusion model), and MUST NOT resolve to a non-excluding/instance-only variant."* (If Decision A selects instance-level instead, leave #197's wording as-is.)

> `start_commit`/`executor_model_class` frontmatter is **doubly justified**: it feeds EV-3/EV-4 base resolution *and* (under exclusion) supplies a **reliable** executor-class identity to `--executor-model`, closing master's brittle commit-author-heuristic tail. Land it regardless of Decision A.

---

## 4. KEEP-MASTER-CANONICAL

Do not touch. #197 introduces nothing stronger on these.

- **`contract_version: "1.7.0"`** — FR-RH1 `reachability_*` + FR-RSR `runtime_surface_*` additive fields. #197's only contract delta is a changelog comment (see §3.1).
- **FR-RH2 headless Tier-2 swarm ensemble** — `run_tier2_ensemble` (`runner.py:36, 439`); the in-process swarm dispatch IS the structural fix for single-reviewer degradation (makes Decision B's directive redundant).
- **Reviewer-isolation hardening** — read-only `reflect-reviewer` agent + `--isolate-reviewers` git-worktree snapshot gate (default off). Orthogonal to both decisions.
- **Strict no-nesting guard** — `test_no_nesting_guard.py` banning `{import anthropic, from anthropic, subagent, Task(}` over `runner.py` + `ensemble.py`.
- **FR-RH1 reachability gate** and **FR-RSR runtime_surface** fields.
- **(Recommended Decision A)** executor-class **EXCLUSION** — §7.1 rule + `executor_class_source`/`executor_class_resolved`/`executor_exclusion_degraded` telemetry + §11.3 three-way partition + `executor_model_class NOT IN reviewer_model_classes` grader assertion.

---

## 5. DECISION A — Anti-self-confirmation model

> **EXCLUSION (master, canonical)** vs **INSTANCE-LEVEL INDEPENDENCE (#197, commit 658bf8f).**
> Adversarial panel: **pro-instance honest verdict 0.72**, **pro-exclusion honest verdict 0.62** — a genuine near-even fork. Both independently proposed the same hybrid as superior to either pole.

### Case for INSTANCE-LEVEL INDEPENDENCE (#197)
- **Literal §1/Mehta reading:** "the same *instance*, carrying the formation context… re-grading that work" is the named failure; a fresh subagent already defeats it. Keeps all three §1 mechanisms (heterogeneous ensemble, blind calibration, evidence-validator).
- **Diversity arithmetic:** excluding the executor's class can only shrink the frame (`{sonnet,haiku,opus}` minus `opus` = `{sonnet,haiku}`); instance-level keeps the executor's class as one more frame *and* prefers diversity.
- **No tier collapse:** never degrades T2→T1 on executor identity (master's `executor_exclusion_degraded` throws away the whole ensemble — mechanism #1 — on collision).
- **No brittle resolver:** deletes the commit-author heuristic that fails open (`executor_class_resolved: false`).

### Case for EXECUTOR-CLASS EXCLUSION (master) — **recommended default**
- **Representational bias lives in the weights, not the instance.** §1 mechanism #1 (byte-identical on both branches): reviewers on "different model classes *so per-model representational bias does not stack*." A fresh **same-class** reviewer shares the executor's systematic blind spots — #197 *concedes* this ("A fresh same-class reviewer still shares the executor's representational stack"). Instance-freshness removes anchoring/context bias but **cannot reach weight-level blind spots**; only class diversity does, and only exclusion *forces* it.
- **#197 demotes the §1-load-bearing property to a "soft good"** and explicitly redefines `t2_model_class_diversity: degraded` as "NOT a weakened anti-self-confirmation guarantee" — so a same-class-as-executor panel can pass silently.
- **Deletes the only graded invariant** (`executor_model_class NOT IN reviewer_model_classes`) with no replacement → unenforceable guarantee.
- **#197's two downsides are mitigated in THIS environment:** rich multi-vendor proxy ⇒ exclusion+backfill keeps the panel full *and* class-disjoint-from-executor (master:630); frontmatter `executor_model_class` ⇒ reliable identity, so the brittle heuristic is a non-issue on the primary path. Collapse is therefore rare, and when it fires it is a **loud true signal** of a real diversity deficit, not a silent same-class pass.
- **Minimum-change / canonical stability:** master is merged + tested; rejecting the rewrite is also the *smaller* change.

### Interaction with reviewer-isolation
Orthogonal. `--isolate-reviewers` + read-only `reflect-reviewer` prevent reviewers **mutating** the repo; neither decision affects that. But note the *composability*: instance-level independence + reviewer-isolation tells a clean "fresh + can't-mutate" story **without** class exclusion — which is the seed of Option C below.

### Recommendation
**Default: KEEP master's executor-class EXCLUSION; REJECT #197's instance-level rewrite.** Rationale: on the *specific guarantee under debate*, exclusion is stronger in this rich-alias environment (panel 0.62), it preserves the protocol's core diversity mechanism and its graded invariant, and it is the smaller change. **This is a product/reliability call, not a correctness call — it warrants your explicit sign-off** (the panel split is near-even).

**Option C (hybrid — arguably best, but net-new work, out of scope for a minimum merge):** adopt instance-level independence as the structural **floor** (never degrade tier on class identity) **plus** keep executor-class diversity as a **hard preference with the graded invariant** whenever executor class reliably resolves (frontmatter/flag), degrading *loudly* only when it genuinely cannot be satisfied. This captures both poles: never collapse on a guess, but force executor∉reviewers when identity is known. Recommend filing as a follow-up, not blocking this merge.

> **DEEP ADVERSARIAL UPDATE (`adversarial-decisionA/`, 3 rounds + invariant probe).** The above was stress-tested in a 3-option debate. It did **not** rubber-stamp the prior — the Option C advocate **reversed onto A** for the near-term and the invariant probe **falsified** the cheap-C framing. **Near-term = A confidence rose 0.62 → ~0.82.** Decisive findings: **INV-201** — "instance-level floor + dormant exclusion machinery" cannot exist (#197 deleted master's grader/backfill/telemetry and occupies the same §7.1/§11.3 regions ⇒ near-term is **binary A-or-B**, and the cheapest path to C is *subtractive editing from A*, not re-authoring from B); **INV-207** — A defends the agreed-**real** weight-level miss **at merge time (1 gate)** vs B's **6 unenforced post-merge gates** ⇒ **A is safer-by-default**. Net: **merge A now; open a *funded, non-blocking* A→C fast-follow** (remove tier-collapse → stay-T2 + `executor_exclusion_unsatisfiable`; drop the commit-author `log-heuristic` from the trigger; add the reflect-side reader for the written-but-unread `executor_model_class`, INV-202; gate the grader *waived-not-failed*). One de-risk: emit `executor_class_source` telemetry and sample real runs — if `log-heuristic`/`unknown` dominates, raise the fast-follow's priority. Full evidence: `adversarial-decisionA/merged-decisionA-recommendation.md`.

### Files to update **together** for whichever side wins (atomicity)
`SKILL.md §7.1` + `SKILL.md §11.3` + `SKILL.md` input-resolution `--executor-model` line + `SKILL.md` §9.3 telemetry block (`executor_class_*`, `executor_exclusion_degraded`) + `SKILL.md` metrics.json block + `refs/reviewer-spec.md` + `refs/reflection-rubric.md` + the `executor_model_class NOT IN reviewer_model_classes` grader assertion + reflect eval fixtures referencing those telemetry fields + `task-builder/SKILL.md` CLI-mode clause 1 (§3.2). **Recommended default = leave all the master ones untouched; only flip task-builder clause 1 polarity.**

---

## 6. DECISION B — runner `inline_directive` + guard loosening

> Keep master's strict guard vs accept #197's directive. **Panel: REJECT, confidence 0.9** (skeptic's falsification attempt failed).

- **The directive is not just dead — it's wrong where it lands.** `_build_prompt()` is consumed only on the Tier-1 branch (`runner.py:462`); the Tier-2/ensemble branch calls `run_tier2_ensemble` and never builds this prompt (`runner.py:452-456`). Tier-1 has no Wave 3/3C/4 (`SKILL.md:688`). So the directive instructs the Tier-1 recipient to spawn reviewer-waves that don't run on Tier-1.
- **The structural fix already exists** on master (`run_tier2_ensemble`), and the directive's own comment says it is "best-effort defense-in-depth only."
- **The guard loosening is causally entangled and weakens safety.** The only new `"subagent"` tokens are inside the directive (`runner.py:381/389/391`); the loosening from bare-`"subagent"` → `subagent_type`/`Agent(` exists solely to admit them. The bare-`"subagent"` ban is load-bearing against **prose/string-described nesting** (a future docstring or directive smuggling a Task-style spawn) — the very regression class #197 reintroduces, adjacent to the #181 nesting-crash surface the guard exists to prevent.

### Recommendation
**KEEP master's strict guard. REJECT the directive, the guard loosening, and `test_inline_directive.py`.** Restore master's `runner.py` and `test_no_nesting_guard.py`; do not add the new test.

---

## 7. SEQUENCED MERGE PLAN

**Do NOT `gh pr merge 197` wholesale** — it would land the Decision-A rewrite and Decision-B regressions. Instead, reduce the #197 branch to the accepted subset (additive-first, then adjudicated drops/ports), then merge the slimmed PR. All work happens on `feat/rf-harness-sync` in this worktree; PR target stays the fork.

> Single-line commands only (terminal can't paste multi-line). Run from the worktree root.

**Step 0 — baseline green (master subset already merges clean).**
`git fetch origin && git status` → confirm 1U only; `uv run pytest tests/cli/reflect tests/swarm -q` to capture pre-state.

**Step 1 — ACCEPT additive (doc skills, tech-*, /task QA, rf-agents).** Already on the branch; no edit. Validate:
`make sync-dev && make verify-sync` then `npx markdownlint-cli2 "src/superclaude/skills/{operational-guide,readme,roadmap,task,tech-reference,tech-research}/SKILL.md"` (or the repo's markdownlint invocation).

**Step 2 — DROP Decision-B pieces (high-confidence, do first among reflect changes).**
`git checkout origin/master -- src/superclaude/cli/reflect/runner.py tests/cli/reflect/test_no_nesting_guard.py` then `git rm tests/cli/reflect/test_inline_directive.py`.
Validate: `uv run pytest tests/cli/reflect -q` (strict guard passes; no directive test).

**Step 3 — REJECT Decision-A rewrite, KEEP EV-1/EV-2 (hunk surgery).**
`git checkout origin/master -- src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` (full restore — these are pure rewrite). Then **manually edit** `…/sc-reflect-protocol/SKILL.md`: restore master's §7.1 / §11.3 / input-resolution `--executor-model` line / §9.3 + metrics telemetry blocks, while **retaining** the EV-1 §8 paragraph, the EV-2 `merge_method` note (§9 + metrics.json), and the §12 `file_present + card_count` detector; reword the contract changelog comment per §3.1 (contract_version stays `1.7.0`).
Validate: `uv run pytest tests/cli/reflect -q`; `grep -n "executor_exclusion_degraded\|executor_class_source\|executor_class_resolved" src/superclaude/skills/sc-reflect-protocol/SKILL.md` (present); `grep -n "ORCHESTRATOR-VERIFIES-ON-DISK\|merge_method legal\|merged-verdict.yaml" src/superclaude/skills/sc-reflect-protocol/SKILL.md` (EV-1/EV-2 present); `grep -n 'contract_version: "1.7.0"' …/SKILL.md`.

**Step 4 — PORT EV-3/EV-4 + reflect_post_mode/--cli; reword clause 1.**
Keep the task-builder EV-3/EV-4 + `reflect_post_mode`/`--cli`/`CLI_MODE` hunks; flip the "CLI mode anti-self-confirmation" clause 1 polarity to the exclusion model (§3.2).
Validate: `uv run pytest tests -q -k "task_builder or taskbuilder or post_reflect"` (or the repo's task-builder test selector); `make verify-sync`.

**Step 5 — full validation gate (all must be green before push).**
`make sync-dev && make verify-sync` ; `uv run pytest tests/cli/reflect tests/swarm -q` ; `uv run ruff format --check src/ tests/` (per memory `make lint ≠ CI ruff format`) ; `make lint`.

**Step 6 — PR hygiene & re-review (fork only).**
`git rev-list --count HEAD..origin/master` (if >0, rebase onto `origin/master`); `git push origin feat/rf-harness-sync`; then comment `auggie review` on the PR (per memory `reference_augment_review_triggers` — pushes don't re-trigger Augment); confirm the PR URL is `https://github.com/IronbellyOrg/IronClaude/pull/197`.

> SoT discipline (CLAUDE.md): edit `src/superclaude/` then `make sync-dev`; **never stage `.claude/` mirrors**; if any `git add` wants `-f` on `.claude/`, STOP.

---

## 8. RISKS IF THE WRONG SIDE WINS

### Decision A
- **If exclusion is kept but instance-level was actually right:** retain a (mitigated) commit-author heuristic and a rare T2→T1 collapse path in alias-poor moments; task-builder clause-1 reword required (already in plan). **Low-cost, reversible**, telemetry stays loud.
- **If instance-level is accepted but exclusion was right (the regression to avoid):** **delete a graded structural invariant** (`executor∉reviewers`) + 3 telemetry fields with **no replacement graded invariant** → same-class-as-executor panels can pass **silently** (the protocol's core anti-self-confirmation value, weakened without a detector). Hard to notice post-merge precisely because the telemetry that would flag it is removed. This is the asymmetric, high-cost failure → favors the conservative default.
- **Either way, Option C beats both** but is net-new work; not landing it is a deferred-upside risk, not a regression.

### Decision B
- **If the directive is kept:** ships a directive that is dead on the ensemble route and **actively wrong** on the Tier-1 route (orders nonexistent waves), *and* permanently **weakens the no-nesting guard** so a future prose/string-described nesting spawn slips through — reintroducing the #181-class nesting-crash surface the guard exists to prevent. Asymmetric downside; near-zero upside (structural fix already exists).

### Process
- **If #197 is merged wholesale:** both regressions land at once and the contract changelog falsely advertises "instance-level replaces exclusion" — avoid `gh pr merge` until the branch is reduced (Steps 2–4).
- **Sync drift:** skipping `make verify-sync` (Step 5) after editing `src/` desyncs `.claude/` and breaks the pre-commit hook for the next contributor.

---

## Appendix — File disposition matrix (18 files)

| File | Disposition |
|------|-------------|
| `skills/operational-guide/SKILL.md` (NEW) | ACCEPT |
| `skills/readme/SKILL.md` (NEW) | ACCEPT |
| `skills/roadmap/SKILL.md` (NEW) | ACCEPT |
| `skills/tech-reference/SKILL.md` | ACCEPT |
| `skills/tech-research/SKILL.md` | ACCEPT |
| `skills/task/SKILL.md` | ACCEPT |
| `agents/rf-assembler.md` | ACCEPT |
| `agents/rf-task-builder.md` | ACCEPT |
| `agents/rf-task-executor.md` | ACCEPT |
| `agents/rf-task-researcher.md` | ACCEPT |
| `agents/rf-team-lead.md` | ACCEPT |
| `skills/sc-reflect-protocol/SKILL.md` | PORT EV-1/EV-2 hunks; REJECT instance-level hunks; reword changelog |
| `skills/task-builder/SKILL.md` | PORT EV-3/EV-4 + reflect_post_mode/--cli; reword CLI clause 1 |
| `skills/sc-reflect-protocol/refs/reviewer-spec.md` | REJECT (keep master) |
| `skills/sc-reflect-protocol/refs/reflection-rubric.md` | REJECT (keep master) |
| `cli/reflect/runner.py` | DROP (keep master) |
| `tests/cli/reflect/test_no_nesting_guard.py` | DROP loosening (keep master) |
| `tests/cli/reflect/test_inline_directive.py` (NEW) | DROP (do not add) |

*Decision A REJECT rows flip to ACCEPT only if you select instance-level independence; then `task-builder` clause 1 keeps #197's wording and master's §7.1/§11.3/telemetry are replaced together (§5 atomicity list).*
