# S3 Adversarial Debate — Auto-Enable allow-regeneration After First Rejection

**Reviewer role:** Adversarial. The default position is that S3 is wrong until
proven otherwise.

**Sources of truth consulted (re-read this turn):**
- `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/spec-fidelity.md`
- `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/deviation-registry.json`
- `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/remediate-roadmap.md`
- `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap/remediate-TDD_TASK_BUILDER_CONVERGENCE.md`
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py` (lines 386–607)
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/remediate_executor.py` (lines 40–55, 307–427, 737–820)
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/executor.py` (lines 1380–1457)
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/commands.py` (lines 84–100, 163, 238)
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/models.py` (line 113)
- `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` (lines 257–317)

---

## 1. Does `allow_regeneration=True` actually fix the failure?

**No.** This is the most damaging finding. The failure summary frames the
3-run loop as "patch rejected by diff-size threshold," but the actual
remediation outputs say otherwise.

- `remediate-roadmap.err` is empty (0 lines).
- `remediate-TDD_TASK_BUILDER_CONVERGENCE.err` is empty (0 lines).
- `remediate-roadmap.md` reports success: *"All five HIGH-severity findings
  resolved. Renamed the roadmap-coined IDs `R-SC-001..004` →
  `RSC.001..004` …"* That matches the registry: the five `signatures`
  findings (`D-001`, `SC-001..004`) flipped to `status: FIXED` after Run 2
  (`last_seen_run: 2`).
- The 10 surviving HIGHs are **not** rejected patches. They are
  `dimension: data_models` (6) and `dimension: nfrs` (4) findings emitted
  by `structural_checkers.check_data_models` and the NFR checker, against
  spec parsing artifacts the agent can't legitimately fix:
  - `'docs/error-grouping-best-practices'` — a slug, not a path
  - `'docs/grouping-algorithm'` — a slug, not a path
  - `'src/superclaude/{skills,agents}'` — brace expansion, not a path
  - `` 'src/x.py:88`' `` — note the trailing backtick; this is a markdown
    code-fence artefact
  - `'src/superclaude/examples/prd_template.md'`,
    `'src/superclaude/examples/tdd_template.md'` — real files, but
    structural checker requires the *exact path string* in the roadmap;
    a reasonable agent doesn't add fictional cross-references just to
    silence a structural gate
  - NFR primitives `'encryption'`, `'hash'`, thresholds `'<1%'`, `'<2%'`
    — also greedy regex hits, not real NFRs of this PRD

So the diff-size guard never even fires for these. The agent either
(a) declines to edit, (b) edits trivially with a small diff that passes,
or (c) produces no patch at all because the finding has no actionable
`files_affected`. `allow_regeneration=True` changes none of this.

**Concrete failure mode of S3 as written:** turning the threshold off
on Run 2 lets the agent submit a *larger* diff, but doesn't make the
agent more able to silence the structural gate. Expected behaviour:
indistinguishable from current run, except more risk to the roadmap
content. Net effect: 0 HIGHs closed, possibly more HIGHs introduced
when the agent over-edits.

## 2. Is the 30% threshold the disease or a symptom?

**The 30% threshold is fine. It's not what's failing here.** Even on
the runs where it *did* matter (the 71.3% and 38.1% rejections the
failure summary mentions), the threshold was doing its job — large
rewrites of a roadmap by an LLM are a known regression vector.
FR-9 documents the deliberate reduction from 50% to 30% in
`remediate_executor.py:50`: this was an intentional tightening, not an
oversight.

The disease is upstream: **the spec parser
(`parse_document(...).file_paths`) is too greedy and emits structural
findings against non-paths.** The threshold tightening is downstream of
where the bug actually lives.

## 3. Does relaxing the threshold break other gates?

Yes, plausibly. Three concrete attack vectors I would worry about:

- **Anti-instinct audit (`anti-instinct-audit.md`)**: this gate scans the
  roadmap for "instinct" patterns (over-confident claims, hand-wavy
  reasoning, etc.). Wholesale section regeneration by an agent under
  diff-size relaxation is more likely to introduce optimistic prose
  than a small targeted edit.
- **Wiring verification (`wiring-verification.md`)**: cross-checks that
  every roadmap section references the agents/components it claims to
  wire. A regenerating agent can delete or rename section IDs (this
  already happened benignly in Run 2: `R-SC-001 → RSC.001`). Under
  relaxation, mass renames are likely to break downstream ID
  cross-refs.
- **Deletion attack**: with `allow_regeneration=True`, an agent that
  receives a vague finding ("file not in roadmap") could rewrite by
  *deleting* the conflicting section instead of *adding* the missing
  reference, satisfying the structural checker by making the deviation
  unobservable. Per-file rollback only triggers on agent failure, not
  on "agent satisfied the finding by deleting context the user wanted."

## 4. FR-9 rationale — what we'd be violating

FR-9 is documented in three places:
- `models.py:113` — `allow_regeneration: bool = False  # FR-9: override diff-size guard for full regeneration`
- `remediate_executor.py:50` — `# FR-9 (v3.05): Per-patch diff-size threshold — changed from 50 to 30`
- `commands.py:93` — CLI flag help: *"Allow patches that exceed the diff-size threshold (FR-9). Use with caution."*

The pattern is unambiguous: the flag is **opt-in, per-invocation, with a
'use with caution' warning**. Auto-enabling on Run 2 silently is exactly
the failure mode FR-9 was written to prevent. Any change here MUST be
opt-in via CLI flag or config, with a clear deprecation path if the
default ever flips.

## 5. Plumbing verification (your claim 2)

Claim: *"Run 1 should be strict and Runs 2–3 should be relaxed."*

The convergence loop at `convergence.py:572-588` calls
`run_remediation(registry)` with **no `run_idx` argument**.
`run_remediation` is a closure (`executor.py:1395-1446`) over `config`,
and reads `config.allow_regeneration` *once at construction time*. So:

- Current code path: `config.allow_regeneration` is fixed at CLI parse
  time and identical on Run 1, Run 2, Run 3. The S3 author's premise
  ("today, all three runs use the same 30% threshold") is correct.
- S3's proposed signature change (`run_remediation(registry,
  allow_regeneration=...)`) requires editing both the convergence
  protocol AND the closure signature in `executor.py:1395` to accept
  the per-run override. This is a real refactor, not a one-liner.
  Confirmed.

So the *mechanism* in S3 works; my objection is to the **policy** it
implements, not the plumbing.

## Verdict on the original S3

- The proposal **misdiagnoses** the failing run (claims diff-size
  rejection; reality is structural false positives + agent declining to
  fix non-paths).
- The proposal **does plumb** a real gap (per-run policy override),
  which is a legitimate building block.
- The proposal **under-mitigates** the deletion attack and the
  anti-instinct/wiring interactions.
- The proposal's "Run 2 wholesale rewrite" claim is unsupported — the
  failing case has no rewrite-needing finding.

## What the refactored S3 must do

1. Stop claiming this fixes the observed failure. Reframe S3 as a
   *defensive tool for a different failure shape* (the real >30%
   rejection case in Run 1 the summary mentions, which is not the
   current state).
2. Tier the relaxation: Run 1 strict (30%), Run 2 moderate (60%) and
   *only if* Run 1 rejected any patch, Run 3 full regeneration *only
   if* Run 2 also failed to reduce HIGHs. Don't blanket-relax.
3. Add a finding-set-size heuristic: never auto-relax if the active
   HIGH count is below a small constant (say 3) — single-finding cases
   should never warrant wholesale rewrites.
4. Add explicit deletion-attack defence: track section count and
   heading count pre/post, reject if structural section count drops
   while findings drop (likely "fix by deletion").
5. Require all relaxation steps to be opt-in via CLI/config; default
   stays strict to preserve FR-9 invariant.
6. Acknowledge the upstream parser bug as the real root cause and link
   to whichever solution addresses it (S1/S2/S4 territory). S3 is at
   best a partial mitigation that helps a future *different* failure.

## Confidence

- **Standalone confidence S3 fixes the documented failure:** 10%
  (it doesn't — wrong root cause).
- **Standalone confidence the refactored S3 is a safe convergence-tier
  feature for a future >30% rejection case:** 70%.
- **Combined confidence with S1/S2 (parser fix) addressing the actual
  root cause:** 78%.
