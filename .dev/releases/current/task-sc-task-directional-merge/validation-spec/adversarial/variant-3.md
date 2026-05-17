---
spec_type: validation
target_release: task-sc-task-directional-merge
stance: security-probe
focus: [tradeoffs, invariants, failure-modes, evidence]
source_plan: .dev/releases/current/task-sc-task-directional-merge/artifacts/final-merge-plan.md
plan_assertion_under_probe: "18/18 compat hazards MITIGATED" (line 43)
canonical_invariants: [INV-04 resumability, INV-03 verifier-floor, INV-01 progress]
inflight_evidence_root: .dev/tasks/to-do/
---

# Validation Spec — Variant 3 (Security-Probe Stance)

## 1. Threat model

The Steps 5–10 deprecation chain (`final-merge-plan.md:315-411`)
creates a time-windowed attack surface where three asset classes can
be silently corrupted between commits:

1. **On-disk in-flight MDTM task files** authored against the
   pre-merge `/sc:task` surface — their F2 prohibition language,
   dispatch assumptions, and PRIMARY ARTIFACT pointers may reference
   symbols the merge mutates or deletes.
2. **Downstream CLI build_prompt sites** (`sprint/process.py:124+170`,
   `cleanup_audit/prompts.py:26/47/69/92/116`) emit `/sc:task` at
   runtime; S-2 acknowledges these but only via pre-commit pytest.
3. **Sync-rule and verifier-floor invariants** — R-RULE-10 contract
   that `[src]` and `[.claude]` agree, and INV-03's guarantee that a
   resumed task still routes to `rf-qa` on stale triggers.

"Attacker" here is **time, partial commits, post-merge rebases, and
the resumption of frozen MDTM tasks** — each can land the system in a
state the plan asserts is impossible. The "18/18 MITIGATED" claim at
line 43 is **convention-bound** (S-1..S-3 are commit-message and
pre-commit-grep obligations); the probe finds gaps between the
convention and an adversarial timeline.

## 2. In-flight MDTM enumeration

Live grep across `.dev/tasks/`:

| Pattern | Files |
|---|---|
| `/sc:task` OR `sc-task-protocol` OR `task-unified` (union) | 96 |
| `/sc:task` | 92 |
| `sc-task-protocol` | 8 |
| `task-unified` | 30 |

The S-1 precondition target — `TASK-PRD-20260514-121039` — has
`status: "🟠 Doing"` and emits **149+ references to `/sc:task`** across
its subtree: `research/01-features-and-user-flows.md` (36),
`synthesis/synth-01-features-ux.md` (37), `research/02-architecture-
and-integration.md` (19), the task file itself (21),
`research-notes.md` (9). The PRD's subagent prompts explicitly name
PRIMARY ARTIFACTS including `src/superclaude/commands/task.md` and
`src/superclaude/skills/sc-task-protocol/SKILL.md` — files CR-DEP-01
stubifies and CR-DEP-03 hard-deletes.

Other in-flight tasks referencing deprecation surfaces:
`TASK-TDD-20260514-121250` (invariant-preservation research),
`TASK-RF-20260515-195758` (git-history audit),
`TASK-RF-20260403-tasklist-e2e`,
`TASK-RESEARCH-20260403-sprint-task-exec`. None of these task files
carry a `Tier:` frontmatter field today, so under CR-FM-03 they
default to `STANDARD` at resume. The "NO migration" promise
(`final-merge-plan.md:214`) is the load-bearing assertion this
validation probes.

## 3. S-1 PRD-precondition probe

**Plan text (lines 319–325):** TASK-PRD-20260514-121039 must reach
`🟢 Done` before Step 5 lands. Option (a) "sequence completion first"
is preferred; (b) snapshot and (c) abort-restart are listed without
selection rules or clock bounds.

**Hazards:**

- **(a) PRD stalls 30+ days in `🟠 Doing`.** No time-bounded abort.
  S-1 reads as "indefinitely block Step 5." Pressure to ship the
  deprecation produces review-pressure to invoke option (b) with no
  decision record. S-1 is a **soft-block**.
- **(b) PRD abandoned.** No row in § 6 names a disposition for
  abandoned PRDs; a reviewer can unilaterally declare abandonment.
- **(c) PRD completes but outputs cite deleted surfaces.** The
  deliverable carries `[CODE-VERIFIED]` tags pinned to `task.md`,
  `SKILL.md`, `COMMANDS.md:86-119`, `ORCHESTRATOR.md:151-213`. After
  Step 5, all four mutate or vanish. The PRD becomes a frozen record
  whose verification tags point at non-existent file-states. The
  plan acknowledges the "frozen historical record" framing
  (line 323) but does not require a pinned-SHA disclaimer.

**Mitigation:** add to Step 5 (a) `--max-wait` (e.g. 14 days) past
which option (b) auto-invokes with merge-message annotation;
(b) require PRD final commit to embed pinned git-SHA refs at every
`[CODE-VERIFIED]` tag; (c) extend CR-DEP-05 grep to flag post-Step-5
docs asserting `[CODE-VERIFIED]` against the stubified body.

## 4. S-2 atomic-commit probe

**Plan text (lines 327–333):** Step 5 commit MUST include CR-DEP-01 +
CR-DEP-02 + CR-REF-01 + CR-REF-02 + CR-REF-09 + CR-DOC-01.
Enforcement is a pre-commit pytest gate.

**Runtime breakage by split:**

- **CR-DEP-01 alone.** The two CLIs keep emitting `/sc:task`; the
  command resolves to a redirect stub that exits. Sprint runs stop
  executing tasks; every `cleanup_audit` prompt is a no-op. Exact
  S-2 scenario — but enforcement is a pytest gate, **not a
  structural barrier**. Nothing prevents `git commit --no-verify` or
  a post-author commit split during interactive rebase.
- **CR-REF-09 split off.** Test files still assert against the
  deprecated invocation; CI fails on the three-assertions-per-test
  pattern, cause hidden one layer behind.
- **CR-DOC-01 split off (HZ-09).** Docs describe `/task` as canonical
  before the recipient skill carries it.

**Post-merge rebase risk.** `git rebase -i` permits commit-split. The
pre-commit gate runs on `git commit`, not on rebase. A rebase that
splits Step 5 into "CR-DEP-01 only" + "everything else" creates a
transient broken state. If pushed (force-push to a feature branch
the merge sprint executor later reads), that SHA becomes a bisection
landing point with broken runtime.

**Mitigation:** § 7 obligation #3: add a **structural barrier** —
server-side pre-push hook (or CI check) that re-greps `/sc:task\b`
against `src/superclaude/cli/` **on the commit landing at master**,
not the working tree, and rejects the push if grep matches AND the
same commit does not also delete the donor `task.md` body. Binds
the six rows at the merge-policy layer.

## 5. S-3 sync-rule probe

**Plan text (lines 335–341):** CR-DIST-02 must land atomically with
CR-DEP-03 + CR-DEP-04; enforcement = `make verify-sync` returns 0.

**Drift modes not enumerated:**

- **Worktree race.** CLAUDE.md authorizes parallel sessions via `git
  worktree`. Session A runs `make sync-dev` at T+0; Session B writes
  `.claude/skills/sc-task-protocol-experimental/` at T+0.1. The
  prune loop enumerated at T+0 includes that directory and deletes
  it at T+0.2. No lock discipline is required.
- **`verify-sync` window.** Between `make sync-dev` and `git commit`,
  an editor backup file under `.claude/skills/sc-task-protocol/`
  would leave an untracked orphan that `git commit -am` skips and
  that persists on disk.
- **R-RULE-10 violation under partial commit.** If CR-DIST-02 ships
  but CR-DEP-04 does not (staged Makefile, forgot `git add` on
  `.claude/`), post-merge `verify-sync` returns non-zero with a
  confusing diagnostic.

**Mitigation:** § 7 obligation #1 should require `flock` on
`.claude/skills/` during prune, and a post-prune `find -type d` diff
against the expected directory set.

## 6. Post-CR-DEP-03 residual-reference probe

After CR-DEP-03 hard-deletes the donor SKILL.md, residuals survive
that the plan's audits do not scope:

- **CR-TASK-12's seven-diff audit** (line 367, 422) runs **before**
  Step 6 deletion. The diff scripts are source-controlled; a future
  re-run post-deletion errors out rather than passing clean. The
  audit should be declared **single-use** and snapshot-frozen.
- **CR-REF-BUCKET-A, C, D, E, F, G, H** are "leave-as-is" per Step 9
  (line 405). These archived debate/refactor/analysis files may
  retain `/sc:task` strings. CR-DEP-05 and CR-REF-12 grep audits
  scope to `[src]` and `[.claude]`, not to `.dev/releases/backlog/`
  or the bucket archive. A future auto-rewriter could "fix" archived
  text against a deleted surface.
- **`docs/generated/*`.** Step 10 (line 409) defers regeneration.
  Between Step 6 and the next regenerator run, generated docs
  describe `/sc:task` as live without a frozen-pre-merge banner.

**Mitigation:** add CR-DEP-06 — a one-shot post-Step-6 grep that
emits a structured manifest of every surviving deprecation-surface
string outside authorized leave-as-is buckets, with per-string
disposition.

## 7. In-flight task resumability probe (INV-04) — highest severity

**Plan claims:**
- "existing TASK-* files validate clean; default `STANDARD`; NO
  migration" (line 214).
- "INV-04 SURVIVES — CR-FM-03 compat shim; ... task-log lines
  append-only" (line 86).

**Probe:** what is the resume behavior of a task file authored
**before** the merge whose F2 / TFEP language references patterns
the merge changes?

- **CR-FM-03 validates parse, not semantics.** The validator is
  unspecified beyond "validates clean." Any task whose YAML
  frontmatter parses today will parse tomorrow — but INV-04's spirit
  is **resumability of meaning**, not resumability of parse.
- **Default STANDARD strips implicit STRICT.** Many in-flight
  checklists embed STRICT-equivalent obligations ("spawn rf-qa here")
  that pre-date the formal `Tier:` field. Defaulting to STANDARD
  silently downgrades those checklist items; INV-03 holds at the
  skill layer but the task's checklist layer loses precedence.
- **"NO migration" is over-broad.** Migration **is** needed for any
  task whose checklist text references `/sc:task`, `sc-task-protocol`,
  or `task-unified` literally — **96 files**. Resume of any one will
  invoke a stub command, attempt to read a deleted skill, or follow
  a checklist step pointing at a hard-deleted path. CR-FM-03 detects
  none of this; the parse succeeds.
- **F2 prohibitions catalog drift.** INV-02 SURVIVES because no
  absorbed feature **weakens** F2, but TU-6's catalog is not
  byte-identical to the donor's. A checklist saying "follow F2 rule
  X" now routes to a recipient catalog where rule X may be
  enumerated under a different name. The checklist item silently
  changes meaning.

**Mitigation:** extend CR-FM-03 with a content-level audit at resume
time: `grep -E "(/sc:task\b|sc-task-protocol|task-unified)"` against
the task body; on match, emit
`gate-1.5: legacy-surface-reference detected file=<path>
action=warn-and-continue surface=<symbol>` and route the resume
through a one-shot acknowledgment gate. Preserves INV-01 while
honoring INV-04 **semantic** resumability.

## 8. Concrete hazard scenarios

**H-1 — PRD stalls; merge bypassed.** Day 0: PRD `🟠 Doing`. Day 14:
2/4 research subagents complete; analyst blocked on a research-gate
question. Day 28: deprecation ship pressure; reviewer invokes S-1
option (b) "snapshot." Day 30: Step 5 lands. The remaining subagent
reads the stubified `task.md` and emits `[CODE-CONTRADICTED]` tags;
the PRD's findings become self-contradictory. INV-04 holds (file
parses) but the deliverable is corrupted.

**H-2 — Rebase splits Step 5.** Author commits Step 5 atomically. A
reviewer requests a CR-DOC-01 wording tweak. Author runs
`git rebase -i HEAD~3` + `edit`, amends, `--continue`. Then splits
the commit with `git reset HEAD^ && git add -p`. The intermediate
state passes the pre-commit gate (working tree still carries the
unstaged CR-REF-01 changes). The split intermediate commit lands
and is pushed. **Master then carries one SHA** where `/sc:task` is
stubified but `sprint/process.py` still emits `/sc:task`. Any sprint
run pinned to that SHA is dead; any bisection lands there.

**H-3 — Worktree race during sync-dev prune.** Session A on
`feat/task-merge` runs `make sync-dev` at T+0. Session B on
`feat/other-feature` (worktree per CLAUDE.md) writes
`.claude/skills/sc-task-protocol-experimental/` at T+0.1. The prune
loop enumerated at T+0 includes that directory and deletes it at
T+0.2. Session B loses uncommitted work; `verify-sync` in B's tree
fails on the next run.

**H-4 — Resumed task hits deleted PRIMARY ARTIFACT.**
TASK-RESEARCH-20260403-sprint-task-exec's research subagent prompt
names `src/superclaude/skills/sc-task-protocol/SKILL.md` as a
PRIMARY ARTIFACT. Pre-merge: parked at checklist item 7/14.
Post-CR-DEP-03: resumed. CR-FM-03 "validates clean"; the subagent
spawned at item 8 fails `Read` on the deleted file. The task
transitions to `⚪ Blocked` per its own exception. INV-01 holds by
transition; INV-04 is technically satisfied (the task is
"resumable") but the **meaningful resume path is dead**. The
line-43 "MITIGATED" verdict does not account for this transition.

## 9. Invariant-survival corrections

- **INV-03.** Survives at skill layer (TU-3, ME-2). The F-05
  mid-phase invocation routes through `SKILL.md:191-198` — a future
  "consistency" rewrite that changes the spawn-pattern line range
  breaks the anchor silently. Extend CR-FM-04 (which already audits
  row 1/10 ordering) to also pin the 191–198 block by anchor-line
  grep.
- **INV-04.** Survives at schema layer; at risk at semantic layer
  for 96 in-flight files. The plan should not assert unqualified
  "SURVIVES" without naming the 96-file content-level exposure.
- **INV-01.** Survives — F-03 correctly forbids new HALT semantics.
  The H-4 `⚪ Blocked` transition is a definitional gray zone, not a
  violation.

## 10. Mitigation recommendations (summary)

| Probe | Hazard | Recommended addition |
|---|---|---|
| § 3 | PRD soft-block; unframed abandonment | Step 5: `--max-wait` (14d); pinned git-SHAs at every `[CODE-VERIFIED]` tag |
| § 4 | Rebase-split bypasses pre-commit gate | § 7 obligation #3: server-side pre-push hook re-greps landing commit |
| § 5 | Worktree race during sync-dev prune | § 7 obligation #1: `flock` on `.claude/skills/`; post-prune dir-diff |
| § 6 | Residual `/sc:task` in leave-as-is buckets | CR-DEP-06: post-Step-6 one-shot residual-reference manifest |
| § 7 | 96 files reference stubbed/deleted surfaces; CR-FM-03 over-broad | Extend CR-FM-03: content-level grep + warn-and-continue + one-shot ack gate |
| § 8 H-1..H-4 | Compound timeline failures not in compat-hazard-report.md | Add HZ-19..HZ-22; assign S-4 (PRD timeout) + S-5 (rebase-ban on Step 5/6 commits) |

## 11. Verdict

The "18/18 compat hazards MITIGATED" claim (line 43) holds **at the
level the plan defines mitigation**: per-CR row, per-acceptance-
criterion, per-pre-commit gate. The probe finds **six new hazards**
(H-1..H-4 plus sync-race and residual-reference classes) that live
at a **timeline / tooling layer** the plan's row-level mitigations
do not reach. **INV-04 is the most exposed invariant**: 96 in-flight
files reference the deprecated surfaces, will all default to STANDARD
on resume, and CR-FM-03's "validate clean / NO migration" detects
**none** of the legacy references their checklists contain.

The recommended additions in § 10 close the surfaced gaps without
re-opening any rejected-features-ledger entry and without weakening
INV-01..INV-05. They extend, not replace, the plan's mitigation
discipline.
