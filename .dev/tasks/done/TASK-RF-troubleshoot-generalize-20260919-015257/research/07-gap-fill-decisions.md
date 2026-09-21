# 07 — Gap-Fill Decisions (Round 1)

**Status:** Complete
**Date:** 2026-09-19
**Scope:** Resolve the 15 open decisions / spec-silences (D1–D15) flagged by the research QA gate (`../qa/*.md`) so the task builder can proceed. Each item is labelled `DECISION` (orchestrator-derivable from the spec's Must-NOTs + repo conventions) or `OPEN QUESTION` (needs user). All repo line numbers re-read 2026-09-19; all v2 cites are `v2:L<n>`.

**Sources:**
- v2 spec: `/config/workspace/Coder/.claude/worktrees/gh-automation-orca-run/.dev/research/sysbox-retrospective-20260918/merged-report-v2.md`
- `SKILL` = `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `VAL` = `/config/workspace/IronClaude/src/superclaude/agents/evidence-validator.md` (the task prompt's `troubleshoot-validator.md` does not exist; v2:23 and 01 §12 both name `evidence-validator.md`)
- `CAL` = `/config/workspace/IronClaude/src/superclaude/agents/confidence-calibrator.md`
- Prior research: `01-file-inventory.md`, `03-spec-extraction.md`, `04-test-verification.md`, `05-integration-points.md` (same dir)

**Tally:** 13 DECISION, 2 items each carrying one OPEN QUESTION sub-part (D1-b, D14-b). Every other item is fully derivable; the builder may proceed on them without waiting.

---

## D1 (CRITICAL) — `make verify-sync` RED at baseline: validation pass criterion — `DECISION` + `OPEN QUESTION`

### Baseline (re-run 2026-09-19, `make verify-sync`, exit 1)

```
  ⚠️  DIFFERS: sc-bare-review
      Only in .claude/skills/sc-bare-review/refs: output-template.md
      Only in .claude/skills/sc-bare-review/refs: prompts.md
      Only in .claude/skills/sc-bare-review: scripts
  ❌ MISSING in src/superclaude/skills/: sc-persona-research-protocol (not distributable!)
  ❌ MISSING in src/superclaude/skills/: sc-recommend-protocol (not distributable!)
  ❌ MISSING in src/superclaude/hooks/scripts/: offer-pr-review.sh (not distributable!)
❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
```

All six are `.claude/`-only orphans in the **main checkout**. None exist in `src/` at `origin/master` (`git ls-tree origin/master src/superclaude/skills/` has `sc-recommend`, not `sc-recommend-protocol`; no `sc-persona-research-protocol`; no `hooks/scripts/offer-pr-review.sh`). They are unrelated to this track.

### DECISION D1-a — scoped pass criterion (paste-ready)

The task's validation gate is the **scoped** sync check below, not the full `make verify-sync`. Run after every `make sync-dev`:

```bash
cd /config/workspace/IronClaude   # or the worktree root, see D14
make sync-dev >/dev/null
diff -rq --exclude='__init__.py' --exclude='__pycache__' \
  src/superclaude/skills/sc-troubleshoot-protocol .claude/skills/sc-troubleshoot-protocol \
  && for f in confidence-calibrator evidence-validator root-cause-analyst; do
       diff -q src/superclaude/agents/$f.md .claude/agents/$f.md || exit 1; done \
  && diff -q src/superclaude/commands/troubleshoot.md .claude/commands/sc/troubleshoot.md \
  && echo "TROUBLESHOOT-SCOPE IN SYNC"
```

Expected output: exactly one line, `TROUBLESHOOT-SCOPE IN SYNC`, exit 0. Any `Only in …` / `Files … differ` line = FAIL. (Verified today on the unmodified tree: prints the success line.)

The `diff -rq` on the skill dir is the same command `verify-sync` uses per skill (`Makefile:178`), so it catches the two hazards 05 §6b names: a new ref present only in `src/` before sync (`refs/primitive-differential.md`, `refs/agent-assertions.md`, `refs/environment-deltas.md`, `refs/probe-packs/read-parse.md`) and any `.claude/`-only orphan inside the troubleshoot skill dir.

**Additionally**: the full `make verify-sync` MUST print no NEW lines beyond the six baseline lines above. Paste-ready delta check:

```bash
make verify-sync 2>&1 | grep -E 'DIFFERS|MISSING|Only in|❌' \
  | grep -vE 'sc-bare-review|sc-persona-research-protocol|sc-recommend-protocol|offer-pr-review\.sh|Drift detected' \
  > /tmp/verify-sync-delta.txt
[ ! -s /tmp/verify-sync-delta.txt ] && echo "NO NEW DRIFT" || cat /tmp/verify-sync-delta.txt
```

Expected: `NO NEW DRIFT` (verified today: the delta file is empty at baseline). Any printed line is new drift introduced by this branch. CI (`quick-check.yml:47-53`, per 05 §6c) runs `make sync-dev && make verify-sync` on a clean checkout where the orphans do not exist, so CI will be GREEN for this branch even though the local full run is RED. **If the builder works in the D14 worktree, the full `make verify-sync` is GREEN there** (fresh `.claude/` has no orphans) and D1-a collapses to `make sync-dev && make verify-sync`.

### OPEN QUESTION D1-b — fix the six pre-existing orphans in this PR?

**Recommendation: NO — out of scope.** They belong to other tracks (bare-review parity, persona-research, recommend, PR-review hook); folding them in doubles the PR's review surface and violates Core Rule 8 (scope discipline). If the user wants them gone locally without a commit: `rm -rf .claude/skills/sc-persona-research-protocol .claude/skills/sc-recommend-protocol .claude/hooks/offer-pr-review.sh .claude/skills/sc-bare-review/refs/output-template.md .claude/skills/sc-bare-review/refs/prompts.md .claude/skills/sc-bare-review/scripts` — but that deletes possibly-unsaved local work in those dirs, so it needs an explicit yes. Default if no answer: leave them; use D1-a.

---

## D2 — `status: blocked` enum extension + sc-task consumer — `DECISION`

R-03 (v2:284), R-04 (v2:304), R-16 (v2:511), A8 (v2:469) all emit `status: blocked`; no R-item extends the `status` enum (03 I-5). Sites re-read today:

| Site | Current | Proposed |
|---|---|---|
| `SKILL:43` | `` \| `status` \| string \| `success`, `partial` (some findings dropped for grounding), `failed` \| `` | `` \| `status` \| string \| `success`, `partial` (some findings dropped for grounding), `blocked` (a Wave 1.6 hard-stop that cannot proceed without an external action — `capability-verdict: blocked`, `blocked-on-authorization`, the 3-round cap, or an unobservable CI verdict (validator A8); the tasklist is still written and Wave 5 still renders), `failed` (the run itself errored) \| `` |
| `SKILL:73` `recommended_escalation` description | `… synthesized from `status` + `tier_reached` + `confidence` + the Wave 5 Next Steps section. `none` = …; `halt` = full stop.` | append: `` `status: blocked` always derives `halt` (a same-depth or deeper re-run cannot lift an external block). `` |
| `SKILL:106` wave map | `sets diagnosability_hard_stop=true and status=partial` | `sets diagnosability_hard_stop=true and status=partial (or `blocked` per the S1.6.4 precedence rule)` |
| `SKILL:457` audit footer | `status: <success\|partial>` | `status: <success\|partial\|blocked>` (`failed` never reaches the footer — the footer is written by Wave 5) |
| `SKILL:529` Will Do | `(sets `diagnosability_hard_stop=true` and `status=partial`)` | `(sets `diagnosability_hard_stop=true` and `status=partial`, or `status=blocked` per the S1.6.4 precedence rule)` |
| `refs/report-template.md:161` | `status: <success\|partial\|failed>` | `status: <success\|partial\|blocked\|failed>` |
| `VAL:72` | `**Suggested report status**: <success \| partial>` | `**Suggested report status**: <success \| partial \| blocked>` |
| `VAL:99-103` Status Decision | 3 bullets (`success`, `partial`, orchestrator decides `failed`) | insert after the `partial` bullet: `` - `blocked`: only when structural assertion A8 fires (no `job-*.log` for the failing arm while `OBSERVE-VIA = artifact-file`). Never suggested for dropped citations alone. `` — keep the existing "The orchestrator decides `failed`" bullet verbatim. |

Eval-suite pins (`agent_grounding_drift.yaml:107,111,166,170,174`) assert only `Dropped**: 0`, `Suggested report status`, `file-missing`, `partial`, `## Dropped citations` — all survive.

**sc-task caller (`src/superclaude/skills/sc-task-protocol/SKILL.md:224-232`, re-read):** branches are, in order, `test_is_wrong`, `remediation_target == "docs"`, `status == "success"`, `recommended_escalation == "none"`, `== "retry"`, `== "escalate_depth"`, `== "halt" (or status == "failed")`. A `blocked` contract therefore routes purely by `recommended_escalation`. With the `SKILL:73` derivation above (`blocked ⇒ halt`), it lands in the FULL STOP branch — the correct outcome (retry at the same depth would reproduce the block; INV-013 already forbids `blocked` gating a fix). **Do NOT map `blocked` → `failed`** in the contract: `failed` means the run errored; `blocked` means the run finished and wrote a tasklist the caller can surface. **Do NOT edit `sc-task-protocol`** — first-match-wins plus the derivation rule already covers it, and touching a second skill expands the PR (Core Rule 8). Also set for `blocked`: `tasklist_insertion_path: null`, `remediation_target: none`, `solution_summary: ""` (same as the existing `halt` rules at `SKILL:74-77`).

Owner: fold into the R-16 task (03 §4 landing order item 5), since R-16 already edits the enum sites and precedes R-03.

---

## D3 — `contract_version` `1.1.0` → `1.2.0` — `DECISION: bump`

Repo rule (re-read): `refs/hardening-output-contract.md:9` "All fields are **additive** under `contract_version`"; `:25` "it is monotonic and additive-only within a major version". History: `1.0.0` stamped the hardening fields (FR-13); `1.1.0` stamped the TFEP adapter fields, each annotated `(contract v1.1.0+)` at `SKILL:73-77` (commit `71f16e13`).

This track adds one field (`execution_locus_card_path`, R-01) and two enum values (`status: blocked`, D2; `pipeline_hardening_verdict: blocked-on-authorization`, R-16). All additive ⇒ minor bump.

Paste-ready `SKILL:62` edit — replace `` default `1.1.0`. Additive version stamp for the Pipeline Hardening Closure fields (FR-13) and the TFEP adapter fields (…); `` with:

`` default `1.2.0`. Additive version stamp: `1.0.0` = Pipeline Hardening Closure fields (FR-13); `1.1.0` = TFEP adapter fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`); `1.2.0` = `execution_locus_card_path` plus the `status: blocked` and `pipeline_hardening_verdict: blocked-on-authorization` enum values; ``

New R-01 row (after `SKILL:77`) carries the same precedent tag: `` | `execution_locus_card_path` | string | Absolute path to `<output-dir>/execution-locus.md` (Wave 1 step 1b; re-derived every invocation). Contract v1.2.0+. | ``

Side note (pre-existing drift, one-line, same task): `refs/hardening-output-contract.md:13` still says default `` `1.0.0` `` — set to `1.2.0` in the same edit so the ref and `SKILL:62` agree; `:25` "(default `1.0.0`)" likewise. `tests/troubleshoot/test_hardening_output_contract.py:45` asserts only the field name `contract_version`, not the value.

---

## D4 — Merged `SKILL:241` hard-stop bullet (R-03 + R-04 + R-06) — `DECISION`

Inputs: R-03 replacement (v2:281-285), R-04 step 4 "re-evaluate S14 … before the branch; hard-stop only when the rows could not run" (v2:302), R-06 "Every tasklist row carries `value-if-<claim>-true | value-if-false`; a row without both is invalid" (v2:351). R-04's *trigger* (v2:295) is evaluated "at S1.6.4 before the verdict branch" and is not contested — it lands at the end of `SKILL:240` before `Branch on (verdict × complexity):`; only the hard-stop bullet is three-way contested.

**Replace the whole `SKILL:241` bullet** (current text begins `` - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop**: emit … `` and ends `No hypothesis work happens in the same turn as the instrumentation patch.`) with:

```markdown
   - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop** — but first, when `discriminator-required=yes` and `OBSERVE-VIA ≠ nobody`, run the `## Discriminator rows` now via that venue, record their outputs in `tier1-observation.md`, and re-evaluate S14 against the new observations (the datum may now be observed); if the verdict changes, re-enter this branch table with the new verdict. The hard-stop fires only when the rows could not run, or when `OBSERVE-VIA = nobody` (the rows stay in the tasklist — never halt for approval): emit `diagnosability-tasklist.md` in the section order of refs/diagnosability-audit.md Section 7 ("Hard-stop tasklist composition"), set `diagnosability_hard_stop=true`, jump to Wave 5 (Waves 1.7-4 skipped). No hypothesis work happens in the same turn as the instrumentation patch. Every tasklist row carries `value-if-<claim>-true | value-if-false`; a row without both is invalid. The tasklist MUST contain the `## Emitter search` block (refs/diagnosability-audit.md Section 7, constraint 5); `capability-verdict: blocked` may appear only after that block records `emitters-found: 0` and `already-read-files: 0`. Status precedence: emitters found ∧ `re-run permitted: no` ⇒ `pipeline_hardening_verdict: blocked-on-authorization`, `status: blocked`; emitters found ∧ `re-run permitted: yes|unknown` ⇒ task rows, `status: partial`; no emitter ∧ no eligible already-read file ⇒ `capability-verdict: blocked`, `status: blocked`.
```

Satisfies: R-03 (emitter block, three-way precedence, `re-run permitted`), R-04 step 4 (re-evaluate S14 before the branch, no halt on `nobody`), R-06 (falsifier columns, invalid-row rule). R-03's "(R-16)" spec-id cross-reference is dropped from the ref text per 03 I-19 convention (cite the field, not the R-number). Every Must-NOT holds: no new wave/file/hard-stop, no approval step, no source-file append target, no probe-results-before-hypothesis when `OBSERVE-VIA = nobody`.

**`SKILL:530` (Will Do near-twin, "no hypothesis work happens in the same turn as an instrumentation patch; the user re-runs after instrumenting"): DO NOT TOUCH.** It is a one-line summary that stays true under the merged rule; the only Will-Do line that becomes wrong is `SKILL:529` (`status=partial`), fixed in D2's table. Rationale: shortest diff; L530 carries no precedence semantics to keep in sync.

Also in the same task (03 I-7, 01 §1 hazard): the 3-round cap row is byte-identical at `SKILL:266` and `SKILL:570`; R-04's counter rewrite ("the tasklist is still written; the report renders the cap message with `status: blocked`; the cap suppresses the re-run recommendation, not the file") must be applied to **both** rows (use `replace_all`), and `refs/diagnosability-audit.md:284` counter prose aligned to the new `<branch>:<repro-venue-id>` key (03 I-6: `<branch>` = git branch).

---

## D5 — "task type 5" has no 1-4: define the list — `DECISION`

Verified: no "task type" vocabulary exists anywhere in `SKILL.md`, `refs/diagnosability-audit.md`, or `refs/report-template.md` (`grep -in "task type|task-type|type [1-5]"` → 0 hits). The only shape list is the per-line task format bullet at `refs/diagnosability-audit.md:253`:

`- **Add env override OR add fixture wrapper OR wrap subprocess.run**: the concrete code change (additive, invocation-site-only, with the revert annotation comment)`

and the five skeleton tasks at `:269-273` (env override, fixture wrapper, strace wrap, telemetry breadcrumb, CI artifact upload). v2's "task type 5" (v2:272, v2:331) and "task-type-5 rows" are Fable-lineage jargon with no repo referent (03 I-4).

**Resolution: make the shapes explicit, numbered 1-5, in the ref's own bullet style; keep v2's "task type 5" phrase because both R-03 and R-05 use it.** Replace `refs/diagnosability-audit.md:253` with:

```markdown
- **Task type** (exactly one of the five below): the concrete code change (additive, invocation-site-only, with the revert annotation comment)
  1. **Env override** — set a log-level / debug / trace env var at the invocation site (skeleton Task 1)
  2. **Fixture wrapper** — a test fixture or harness wrapper that captures correlation, timing, or state around the existing call (skeleton Task 2)
  3. **Subprocess wrap** — wrap the invocation in a tracer or verbose mode (skeleton Task 3)
  4. **Telemetry / artifact capture** — breadcrumb, metric, or CI artifact-upload step so the signal survives the run (skeleton Tasks 4-5)
  5. **Fail-closed observed-value emission** — one line `<predicate-name>=<observed value>` beside an existing emitter, or appended to a log/report/artifact already read in this run (never a source file); prints `<predicate-name>=unobserved` on any read error and never the expected value; produced only by the constraint-5 emitter search below and MUST name the S14 predicate it serves
```

R-03's constraint-5 sentence "Each line produced by 3 is a **task type 5 — fail-closed observed-value emission**" (v2:272) then resolves to this entry unchanged. Add to the skeleton at `:260-278` a sixth heading line under `## Implementation tasks`: `### Task 6: Fail-closed observed-value emission beside the nearest existing emitter (task type 5)` so the T4 example and the skeleton show all five shapes.

---

## D6 — `refs/triage-checklist.md` new section after `:44` (R-02) — `DECISION`

Context: R-02 (v2:236-247) names the ref but gives no body. The consumer of this ref is the hypothesis agent (`root-cause-analyst`, Wave 1 + Wave 1.7 brief, `SKILL:588`), so the section is the **agent-facing** side of producer enumeration: cite rows, never re-grep (R-02 Must-NOT "have each agent re-grep"), exclusion needs the exit-statement line (AP-05), no plausibility ranking. Style matches the existing `## Evidence-or-drop check` (heading, one-sentence lead, short bullets, one closing rule).

Insert after `:44` (`"Evidence grounding" is scored 0.0.`), before `## Fix sketch`:

```markdown
## Producer citation (categorical symptoms)

When the observed symptom is a categorical value — an enum string, a status word, an exit code — the orchestrator has already written `<output-dir>/producers.md` (Wave 1.6, S1.6.0b) and pasted its `## Producers` table into your brief: `line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving`.

- Cite producers by row, never by re-grepping: any claim that names the value MUST cite the row(s) with `surviving=yes`.
- Excluding a producer requires the `file:line` of the `return` / `exit` / `break` statement that rules it out (the row's *exit statement* column). "Excluded by source logic" without that line is an unverified counterfactual: Evidence grounding is scored 0.0 for that claim.
- If the table is absent, says `producer-count=unknown`, or has zero `surviving=yes` rows, the claim is `UNDETERMINED — among {<all rows>}`. Do not pick the most plausible producer.
- Do not rank producers by plausibility. Until a probe row has run, the partition columns (started marker, wall time, cheap observable) are the only discriminators.
- A passing arm counts as a control only when the execution-locus card records `CONTROL-PROOF: yes: <file:line>` for it.

If the table is in your brief and your card cites none of its rows, the card is returned unread.
```

No OS/runtime/tool names (design rule v2:155). Menu-equality (R-02 step 6) stays in `SKILL` Wave 3 step 2, not here.

---

## D7 — R-12 Will-Not bullets + audit-footer line — `DECISION`

Derived from R-12's rule text (v2:448) and Must-NOTs (v2:450: never ask the user; never count reads of the failing artifact as cosmetic; never add a token cap that stops diagnosis mid-wave). Style = existing `## Will Not Do` bullets (`SKILL:534-545`: `- <Verb> … — <reason>`).

Append after `SKILL:545` (the last Will-Not bullet, ending `leaks into release artifacts.`), then R-13's new sibling bullet (03 I-29) follows these:

```markdown
- Spend more than 5 consecutive `Read`/`Glob` calls on `<output-dir>/` without one Read/Bash on a source file or downloaded artifact — the cosmetic-loop counter (Wave 5 step 3.5) forces exactly one of: finalize REPORT.md as-is with `status: partial`, or one source/artifact read. Exempt: `ls`, `Write`, persist-on-receipt calls, and reads of `job-*.log`, `*.stream.jsonl`, `<output-dir>/artifacts/**`, or any file whose content is written into a probe row.
- Halt a wave on the cosmetic counter or on any token cap — an overrun is audit-logged as `cosmetic_overrun=<n>` at every multiple of 5 and the run continues; the counter is a nudge, not a gate.
- Re-type a calibration report into context, or grep the calibration markers a second time in the same wave — reports are consumed from disk; the Wave 3 marker verification is one command, run once.
- Infer consent from an errored `AskUserQuestion` — the result is `remediation_accepted=false`, no inference.
```

**Audit-footer rule** (v2:446 "audit-footer rule", no text). Two surfaces, matching the file's two conventions:

1. In-run audit-log line (`key=value`, like `discriminator-required=yes`): `cosmetic_overrun=<n>` written each time the counter reaches a multiple of 5 without the forced action.
2. Footer (`key: value` inside `<!-- SC:TROUBLESHOOT:SUMMARY … -->`, `SKILL:456-468`): insert after `adversarial_invoked: <bool>` the line `cosmetic_overrun: <n>` — `n` = the highest overrun value logged this run, `0` when the counter never fired.

`SKILL:582` cost-profile sentence (v2:447): after `These are targets, not hard caps.` append ` The cosmetic counter is the one hard cap; overrun is audit-logged as `cosmetic_overrun=<n>` and the run continues.`

---

## D8 — `refs/escalation-rubric.md:63-69` "gains one rule" (R-08) — `DECISION`

The list at `:63-69` is `3. **Signal-driven escalation** (any one triggers escalation)` with six `- <condition> → ESCALATE (`escalation_reason: <token>`).` bullets; `:69` is the last (`source_only_dynamic_claim`). Trigger from R-08 (v2:394): two cards cite the same `file:line` and assert different mechanisms ⇒ `split-pending`, never STOP.

Insert after `:69`:

```markdown
   - Two cards cite the same `file:line` and assert different mechanisms (Wave 3 cluster marked `split-pending`) → ESCALATE (`escalation_reason: split_pending`); neither card may STOP the investigation until the splitting probe pair has an observed result. This rule applies from Wave 3 onward; a single Tier 1 card cannot trigger it.
```

Companion one-token edits so the reason is legal everywhere it is enumerated: `CAL:108` Reason enum gains `| `split_pending``; `SKILL:460` footer `escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>` gains `|split_pending` (this footer is already missing `not_reproducible|security_caution|source_only_dynamic_claim` — pre-existing; add all four while there, it is the same line). `RUB:20` formula untouched (R-14 Must-NOT).

---

## D9 — `refs/environment-deltas.md` body (≤25 lines) — `DECISION`

R-01 (v2:225) gives only a ten-item prompt list (`host, process, user, filesystem-view, network-view, clock, permissions, installed-versions, working-dir, env-vars`) and the load rule. The task prompt's eight-item menu folds it: `user`+`permissions` → `identity`; `working-dir`+`env-vars` → `config-source`. Body (22 lines, no OS/runtime/tool names; `stat`/`access` are the same generic verbs the R-05 table already uses):

```markdown
# Environment deltas (optional ref)

Loaded by Wave 1 step 1b only when the execution-locus card derives `SAME-ENV ≠ yes`. Absent ⇒ audit line `optional_ref_absent: refs/environment-deltas.md`, no Grounding Gap. This is a prompt list, never a decision input: each delta you cannot prove identical between PRINT-SITE and RUN-SITE becomes a candidate `## Discriminator rows` entry (Wave 1.6 S1.6.4) and a candidate `runs-in=` qualifier on Wave 1.7 cards. Concrete, incident-derived probes live only in `refs/probe-packs/<kind>.md`.

| Delta | How to check (one read-only read or command at RUN-SITE; record exit status or one `key=value` line) |
|---|---|
| host | print the machine identity (hostname / node id) at RUN-SITE and at PRINT-SITE; equal? |
| process | print pid, parent pid, and session id of the process that executes the producer line; is it the process you assumed? |
| clock | read the monotonic and wall clocks once, using the producer's own idiom, then once by bulk read; same value and format? |
| filesystem-view | `stat` the node the producer reads (type, size, mount source) at RUN-SITE; compare with the same node on a passing arm |
| network-view | resolve and connect to the producer's endpoint from RUN-SITE; rc only, no payload |
| identity | print effective user, group, and capability set at RUN-SITE; compare with the arm where it passes |
| installed-versions | print the version of the interpreter / shell / binary that executes the producer line at RUN-SITE |
| config-source | list the config files and env vars the producer line reads and their effective values at RUN-SITE, not at PRINT-SITE |

Rows are unordered; check first the ones whose kind (per `refs/primitive-differential.md`) matches a `surviving=yes` producer. Any row you cannot run is `unknown`, never blank.
```

---

## D10 — Refs-table rows + `## Loading discipline` footers for the optional refs — `DECISION`

Convention (re-read `SKILL:584-602` and all 14 refs): the Refs table is the load registry — every ref a wave loads at runtime has a row (`| File | When loaded |`), and `:602` states "Each ref is loaded only by the wave that needs it. Do not pre-load." `refs/calibrator-eval-cases.md` (a test corpus, never loaded at runtime) has no row. A `## Loading discipline` footer exists in only **2 of 14** refs (`diagnosability-audit.md:338`, `doc-discovery.md`), both large multi-section refs whose sections are consumed by different parties.

Decision:
- **Rows: YES** for both optional refs and the mandatory new refs. Append after `SKILL:600`:
  ```markdown
  | `refs/primitive-differential.md` | Wave 1.6 S1.6.4 discriminator rows (probe-form table copied per surviving producer) and S1.6.0b primitive grep (one pattern per table row) |
  | `refs/agent-assertions.md` | Wave 1.7 / Wave 3 (passed to `confidence-calibrator` as `assertions_path`) and Wave 5 (passed to `evidence-validator`; read by the orchestrator's inline fallback) |
  | `refs/environment-deltas.md` | Wave 1 step 1b, only when the locus card derives `SAME-ENV ≠ yes` — **optional**; absent ⇒ audit line `optional_ref_absent`, no Grounding Gap |
  | `refs/probe-packs/<kind>.md` | Wave 1.6 S1.6.4, only when a `surviving=yes` producer's primitive kind matches `<kind>` — **optional**, informational, never a decision input |
  ```
- **Footers: NO** for `environment-deltas.md` and `probe-packs/read-parse.md` (each is a single table; their load condition is in their first paragraph and in the Refs row). **YES** for `primitive-differential.md` only if it ends up multi-section (procedure + table + bracketing per v2:314-333 — it will); use the `diagnosability-audit.md:338-340` wording pattern: "This ref is loaded by Wave 1.6 only. Other waves do not import it. R-02 step 4 reads the table's pattern column; R-04 step 1 copies the pair shape; the file is not re-read during the wave."

`tests/agents/test_tavily_tool_parity.py` rglobs all skill `.md` files but skips those without frontmatter (05 §4c) — refs have none, so no test impact.

---

## D11 — R-17 rename seams: what renames, what stays, guard allow-list, test token — `DECISION`

Spec (v2:518): rename `SKILL:104, :410-420, :595-600` + refs; "output-contract field names unchanged (`SKILL:62`)"; guard `grep -E '\bH[0-5]\b'` = 0 hits outside contract field names. Fact (05 §2a, re-verified): **no field name contains an H-token** — the H-tokens at `SKILL:63-71` are all in the *description* column. So "field names unchanged" is satisfied automatically; every H-token in prose renames.

**RENAME (prose/labels) — all of these:**

| File | Lines | Note |
|---|---|---|
| `SKILL.md` | 63, 64, 67, 68, 69, 70, 71 | description column only; keys `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `off_path_review_decision`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path` untouched |
| `SKILL.md` | 104 (`H0-H5`, hyphen), 408, 410 (`H0–H5`, `H1–H5` en-dash), 414-420 (`**H0 — …**` … `**H5 — …**`, `H0–H5 statuses`, `H1–H5 cannot be silently skipped`), 444, 595, 597, 598, 599, 600 | both dash forms |
| `refs/hardening-output-contract.md` | 3, 14-23 (Wave column values only), 29, 33, 34, 36, 38, 39, 43-48 (heading + column headers `H5 Decision`/`H5 Status`), 58, 69 | **keep verbatim**: `NOT PROVEN — failed hardening wave: <wave>`, both `ADVISORY — …` strings, the 4 H5 mapping rows' cell values, `{blocked, advisory}`, `| No |` ×7 (pinned by `test_hardening_verdict.py:27,36-39,51,73-74,79`) |
| `refs/pipeline-hardening-closure.md` | 19 hits | |
| `refs/report-template.md` | 230-235, 316 | keep `NOT PROVEN` token (`test_hardening_output_contract.py:98`) |
| `refs/unmask-and-sweep.md` | 7 hits | |
| `refs/runtime-entrypoint-verification.md` | 1, 3, 7, 9, 11, 28 (6 hits) | line 7 and 28 contain `satisfy H1` → `satisfy HC1` — see test below |
| `refs/contract-enumeration.md` | 5 hits | |
| `refs/effective-input-proof.md` | 4 hits | |

**STAY (allow-list — hypothesis-card labels, the exact collision R-17 exists to disambiguate):** `refs/escalation-rubric.md:35` ("the H3 0.95-REFUTE case"), `refs/calibrator-eval-cases.md:49` ("actual H2 card from T4"), `:54` ("actual H1 card from T4"). Leaving them byte-identical also satisfies T14 "fixtures 1-9 and P1-P5 unchanged".

**STAY (out of scope, self-contained Python/JSON):** `tests/troubleshoot/backtest/git_replay.py:52-58`, `test_git_replay_unit.py:85`, `test_catch_rate_*`, `fixtures/catch_rate/*.json` `"wave": "H1"` — never compared against markdown; `wave` field VALUES emitted by the protocol (`known_escapes_caught`, `report-template.md:244`) become `HC<n>`, the backtest constants stay `H<n>` (nomenclature drift, note in the task file, no fix). `tests/troubleshoot/e2e-backtest-scenarios.md` (15 hits): not collected; optional cosmetic.

**Guard (paste-ready; expected after the rename: `GUARD OK`):**

```bash
cd /config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol
if ! grep -nE '\bH[0-5]\b' SKILL.md refs/*.md refs/probe-packs/*.md 2>/dev/null \
     | grep -qvE '^refs/(escalation-rubric\.md:35|calibrator-eval-cases\.md:(49|54)):'; then
  echo "GUARD OK"
else
  echo "GUARD FAIL:"; grep -nE '\bH[0-5]\b' SKILL.md refs/*.md | grep -vE '^refs/(escalation-rubric\.md:35|calibrator-eval-cases\.md:(49|54)):'
fi
```

Verified today at baseline (pre-rename): `GUARD FAIL: 91 hits`, and the allow-list filter removes exactly the three hypothesis-label lines and nothing else (0 residual hits in `escalation-rubric.md` + `calibrator-eval-cases.md`). `\b` treats both `-` and `–` as non-word, so both dash forms are caught; `HC0` does not match `\bH[0-5]\b`. Codify as `tests/troubleshoot/test_hc_rename_guard.py` (03 I-30 asks for an R-17 content test) with the same three-line allow-list.

**Test token:** `tests/troubleshoot/test_hardening_h1.py:46` `assert "satisfy h1" in low` → `assert "satisfy hc1" in low` (source lines `runtime-entrypoint-verification.md:7,28` become `satisfy HC1`). Same commit as the rename. Also tighten `test_hardening_verdict.py:51` to the 5-token string once R-16 appends `blocked-on-authorization` at the END of the enum (04 B1), and keep `{blocked, advisory}` at OC:68 unchanged (04 B2 — authorization block is a hard-stop outcome, not a latch outcome).

---

## D12 — SKILL-side `Task` spawn kwargs for R-14's new inputs — `DECISION`

Authoritative names (v2:467; 03 R-14 card — NOT 05's `artifact_paths`):
- CAL: `card_mtime`, `behaviour_definitions_path`, `tasklist_path`
- VAL: `calibration_paths: list`, `diff_path: str|null`, `artifact_mtimes: dict`, `producers_path`, `tasklist_path`
- Plus one gap-fill (03 I-11, R-14 gap (c)): VAL `locus_path` — A7 (`RUN-SITE`) and A8 (`OBSERVE-VIA`) are unimplementable without the locus card; `output_dir` is NOT needed because VAL has `Glob` (`VAL:5`) and can glob `job-*.log` under `dirname(report_draft_path)`.
- Plus `assertions_path` on both agents (D13) so the assertion list has one home.

Three spawn sites (not two — `SKILL:345` is the Wave 3 per-card calibrator spawn):

**`SKILL:281`** — after `` `output_path=<output-dir>/tier1-calibration.md` `` append:
`` , `card_mtime=<ISO-8601 mtime of card_path from `date -u -r <card_path> +%Y-%m-%dT%H:%M:%SZ`>`, `behaviour_definitions_path=<output-dir>/behaviour-definitions.md`, `tasklist_path=<output-dir>/diagnosability-tasklist.md`, `assertions_path=<skill-dir>/refs/agent-assertions.md` ``

**`SKILL:345`** — after `` `output_path=<output-dir>/tier2-<agent-name>-calibration.md` `` append:
`` , plus the same `card_mtime` (per card), `behaviour_definitions_path`, `tasklist_path`, and `assertions_path` inputs as Wave 1.7 step 2 ``

**`SKILL:451`** — after `` `allow_command_reexec=false` `` append:
`` , `calibration_paths=[<output-dir>/tier1-calibration.md, <output-dir>/tier2-*-calibration.md]`, `diff_path=<path of the instrumentation or fix diff written this run, else null>`, `artifact_mtimes={<abs path>: <ISO-8601 mtime>}` for every `<output-dir>` file the draft cites (from the single `ls` of Wave 5 step 3 persist-on-receipt), `producers_path=<output-dir>/producers.md`, `tasklist_path=<output-dir>/diagnosability-tasklist.md`, `locus_path=<output-dir>/execution-locus.md`, `assertions_path=<skill-dir>/refs/agent-assertions.md` ``

**All new inputs are optional with defaults** (precedent `CAL:56` "If `claim_class` is absent, default to … Record all defaults in Notes"). Paste-ready agent Inputs text, one line each:

CAL (after `CAL:51` `` - `output_path`: … ``):
```markdown
- `assertions_path` (optional): absolute path to `refs/agent-assertions.md`. Absent ⇒ skip step 5b entirely; Stage-2 row `structural_flags | skipped | no assertions_path`.
- `card_mtime` (optional): ISO-8601 mtime of `card_path` supplied by the orchestrator (you have no Bash). Absent ⇒ C5 evaluates only the `T00:00:00Z` clause; record `input_absent: card_mtime` in Notes.
- `behaviour_definitions_path` (optional): absolute path to `<output-dir>/behaviour-definitions.md`. Absent or file missing ⇒ C8 skipped; record in Notes.
- `tasklist_path` (optional): absolute path to `<output-dir>/diagnosability-tasklist.md`. Absent ⇒ C4 and C7 evaluate against the card text only; record in Notes.
```

VAL (after `VAL:44`):
```markdown
- `assertions_path` (optional): absolute path to `refs/agent-assertions.md`. Absent ⇒ no `## Structural assertions` table is emitted and responsibility 2b is skipped (v1 behaviour).
- `calibration_paths` (optional, list): calibration reports for every card in the draft. Absent ⇒ A1's "max calibrated < 0.50" clause is unknown; A1 fires only on its other two clauses.
- `diff_path` (optional, str|null): the diff written this run. `null`/absent ⇒ A2 skipped.
- `artifact_mtimes` (optional, dict): `{abs path: ISO-8601 mtime}`. Absent ⇒ A3 evaluates only the `T00:00:00Z` clause.
- `producers_path`, `tasklist_path`, `locus_path` (optional): absent ⇒ A7 / A10 / A7+A8 skipped respectively. Every skipped assertion is listed in `## Notes` as `assertion_skipped: <id> (<missing input>)`.
```

Compatibility check against 05 §5b: sc-reflect (W1D/3C/5), sc-pr-submit (W3), sc-cli-eval (W6), and the nightly `agent_grounding_drift.yaml:96-100,155-159` all pass exactly the current 4/5 inputs ⇒ every new assertion is skipped, output format unchanged (`**Dropped**:`, `**Suggested report status**:`, `## Dropped citations`, `file-missing`, `partial` all intact; the `## Structural assertions` table is only emitted when `assertions_path` is given). `docs/eval/suites-guide.md:408-409` still says re-run the suite after editing these agents — record in the task file as a post-merge step, not a gate.

---

## D13 — Single source of truth for the assertion list: `refs/agent-assertions.md` — `DECISION`

Design rule (v2:155): "Agents are the primary detection venue; the orchestrator's inline fallback runs the identical assertion list; tests cover both paths." Three candidate homes: (a) duplicated in CAL + VAL + SKILL fallback (drift bait), (b) SKILL only (agents cannot read the SKILL), (c) one ref cited by all three. **(c)**, as 04 §4 recommends: `refs/agent-assertions.md`; both agents receive it as optional `assertions_path` (D12); `SKILL:282` and `SKILL:452` fallback bullets gain "apply the identical list in `refs/agent-assertions.md`"; T13 parity reduces to markdown table ⇔ `tests/troubleshoot/_assertions.py` `FLAGS` ⇔ fixture `expected_flags:`.

Flag names for the rules v2 leaves unnamed (03 I-10; T1 asserts "the named flag"): A6 `reference_value_not_literal`, A7 `run_site_unresolved`, A8 `ci_verdict_unobserved`, A9 `probe_suspect`, C6 `bracket_uncited`. Severity column = the consequence token the rule names.

**Skeleton (assertion text verbatim from 03 R-14 card / v2:468-469):**

```markdown
# Agent structural assertions (calibrator C1-C8, validator A1-A10)

One list, three consumers: `confidence-calibrator` step 5b, `evidence-validator` responsibility 2b, and the orchestrator's inline fallbacks (SKILL Wave 1.7 step 2 / Wave 5 step 3). All three MUST produce the same flag set on the same inputs; `tests/troubleshoot/test_inline_fallback_parity.py` pins it. No Bash anywhere: every input an assertion needs is passed in by the orchestrator (see each agent's Inputs). A rule whose input is absent is *skipped* and listed in Notes, never silently passed.

## Calibrator (C-rules) — evaluated after step 5a, before the escalation decision

| id | trigger | flag | severity |
|---|---|---|---|
| C1 | headline enum token ∧ calibrated < 0.50 | `headline_definite_low_confidence` | verdict forced ESCALATE |
| C2 | card excludes an enum without a `file:line` for that enum's exit statement | `unproven_exclusion:<token>` | Runtime check := 0.0 |
| C3 | control arm cited without `CONTROL-PROOF: yes` | `control_unproven` | Symptom coverage ≤0.5 |
| C3b | `runs-in=unknown` | `locus_unknown` | Runtime check ≤0.5 |
| C4 | instrumentation without falsifier | `no_prereg_falsifier` | Fix directness ≤0.5 |
| C5 | `Timestamp` > `card_mtime` + 5 min or `T00:00:00Z` | `timestamp_invalid` | note; timestamp not load-bearing |
| C6 | a numeric threshold or bracket asserted in the headline without a `bracket=` line in `bracket.md` | `bracket_uncited` | Evidence grounding := 0.0 (nearest legal value ≤0.3; 03 I-9) |
| C7 | card names an environment property without citing a 2×2 row | `uncited` | cap calibrated 0.5 |
| C8 | `behaviour-definition: row N` missing or row Status empty | `behaviour-cite: missing` | cap calibrated 0.5 |

Caps apply after the formula at `refs/escalation-rubric.md:20` (unchanged); record every fired rule in the Stage-2 `structural_flags` row.

## Validator (A-rules) — evaluated after citation verification (responsibility 2b)

| id | trigger | flag | severity |
|---|---|---|---|
| A1 | definite enum token in Summary/Diagnosis ∧ (max calibrated < 0.50 ∨ token in Grounding Gaps with `unobserved\|deduced\|pending` ∨ token fails `grep -F` against every artifact and `job-*.log`) | `deduced_headline` | `partial` |
| A2 | `diff_path` touches a collector/invocation site ∧ no falsifier sentence naming a row | `instrumentation_without_falsifier` | `partial` |
| A3 | `Timestamp\|Date\|pushed_at` > artifact mtime + 5 min or `T00:00:00Z` | `timestamp_invalid` | drop that line |
| A4 | `pipeline_hardening_verdict` ∉ `{pass, blocked, advisory, not_applicable, blocked-on-authorization}` | `verdict_not_in_contract` | `partial` |
| A5 | `candidate-fixes.md` `consensus` ∧ `adversarial_invoked: false` ∧ any card `evidence_class ∈ {source_static, doc_static, none}` with dynamic claim_class | `consensus_on_unobserved` | `partial` |
| A6 | `Reference-context value` not a single literal (matches `if\|only\|/\|,`); literal `n/a` is exempt on the first instrumented run (03 I-12) | `reference_value_not_literal` | FAIL |
| A7 | `RUN-SITE = pending-producers` at finalize while `producers.md` has ≥1 producer row | `run_site_unresolved` | FAIL |
| A8 | no `job-*.log` for the failing arm at finalize when `OBSERVE-VIA = artifact-file` | `ci_verdict_unobserved` | `status=blocked`, Diagnosis `UNDETERMINED — CI verdict unobserved` |
| A9 | `Reference-context value` ≠ observed reference value | `probe_suspect` | probe row `suspect`, Grounding Gap, outcome table skipped (not a status change) |
| A10 | `capability-verdict: blocked` without an `## Emitter search` block recording `emitters-found: 0` and `already-read-files: 0` | `capability_block_unproven` | `partial` |

## Output shape (both agents, same table)

`## Structural assertions` — `| id | fired | flag | consequence applied | evidence (file:line or "input absent") |`, one row per rule, in the order above. Skipped rules show `fired: skipped`.

## Loading discipline

Passed to agents as `assertions_path`; read by the orchestrator only inside the two inline-fallback branches. Not pre-loaded.
```

`tests/troubleshoot/_assertions.py` (04 §2) exposes `FLAGS = {"C1": "headline_definite_low_confidence", …, "A10": "capability_block_unproven"}` parsed from this ref, so the Python evaluator and the prose cannot drift.

---

## D14 — Branch cut + handling the dirty tree — `DECISION` + `OPEN QUESTION`

Facts (re-run 2026-09-19): `origin` = `https://github.com/IronbellyOrg/IronClaude.git`; `master..origin/master` = 17 commits, `origin/master..master` = 0; `git diff --stat master..origin/master -- <all target paths>` = empty (none of the 17 touch the skill dir, the two agents, `commands/troubleshoot.md`, or `tests/troubleshoot/`). Dirty tree: 17 modified/deleted + 5 untracked entries (22 lines of `git status --porcelain`), including this task's own untracked dir `.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/`. `.dev/worktrees/` is gitignored (`.gitignore:233-235`) and already hosts two worktrees; CLAUDE.md mandates `.dev/worktrees/<name>` and forbids `EnterWorktree`.

### DECISION D14-a — worktree, not stash

`git stash -u` would sweep the 5 untracked entries **including this task directory and the research you are reading**; a plain `git stash` leaves the untracked ones but still parks 17 files another track is mid-edit on. A worktree touches neither. Paste-ready:

```bash
cd /config/workspace/IronClaude
git fetch origin
git worktree add .dev/worktrees/troubleshoot-generalize -b feature/troubleshoot-generalize origin/master
cd .dev/worktrees/troubleshoot-generalize
uv sync --extra dev 2>/dev/null || make dev          # editable install for the worktree
make sync-dev && make verify-sync                    # expected: GREEN (fresh .claude/, no orphans)
uv run pytest tests/troubleshoot/ -q                 # expected baseline: 70 passed, 1 failed (backtest/test_backtest_e4.py:105, pre-existing — 04 §0)
```

Expected: `git branch --show-current` → `feature/troubleshoot-generalize`; `git log --oneline -1` → the tip of `origin/master`; full `make verify-sync` exits 0 (D1-a's scoped check is then unnecessary). The builder references the task dir by absolute path (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/`) because it is untracked and therefore absent from the worktree. PR at the end: `gh pr create --repo IronbellyOrg/IronClaude --base master --head feature/troubleshoot-generalize …` (CLAUDE.md absolute rule); verify the returned URL is `IronbellyOrg/IronClaude/pull/N`.

Session note: open the Claude Code session in the worktree root so `.claude/skills/` read at runtime is the worktree's synced copy.

### OPEN QUESTION D14-b — main-checkout `master` is 17 behind `origin/master`

Fast-forwarding local `master` (`git checkout master && git merge --ff-only origin/master`) is safe for the 17 commits themselves but would be done in a dirty tree with unrelated in-progress edits; nothing in this track needs it (the worktree branches from `origin/master` directly). **Recommendation: do not touch local `master` in this task**; leave it to whoever owns the 17 dirty files. Default if no answer: skip.

---

## D15 — Correction to `01-file-inventory.md:409` — `DECISION`

`01-file-inventory.md:409` states: "New files the spec creates (do not exist today — confirmed by `ls refs/`): … `tests/troubleshoot/**`." **The `tests/troubleshoot/**` clause is false.** Verified `ls tests/troubleshoot/` 2026-09-19:

- **Exists:** `tests/troubleshoot/__init__.py`; 7 top-level test modules `test_hardening_h0.py`, `test_hardening_h1.py`, `test_hardening_h2.py`, `test_hardening_h3.py`, `test_hardening_h4.py`, `test_hardening_output_contract.py`, `test_hardening_verdict.py`; `e2e-backtest-scenarios.md`; and `backtest/` holding 14 test modules (`test_backtest_e1..e5.py`, `test_backtest_status_separation.py`, `test_catch_rate_aggregation.py`, `test_catch_rate_schema.py`, `test_git_replay_integration.py`, `test_git_replay_unit.py`, `test_path_resolution.py`, `test_replay_executor.py`, `test_waiver_regreen.py`) plus helpers (`_impl_guard.py`, `catch_rate.py`, `catch_rate_report.py`, `git_replay.py`, `replay_executor.py`, `conftest.py`), `backtest/fixtures/`, `backtest/schemas/`. (04 §0: 70 pass / 1 pre-existing fail.)
- **Absent (the only R-19 targets that are truly new):** `tests/troubleshoot/fixtures/` (the R-19 layout root, v2:552-565 — distinct from the existing `backtest/fixtures/`), `tests/troubleshoot/test_calibrator_eval_cases.py` (T14), and every T1-T19/T15 test module named at v2:569-588 plus `_assertions.py` and `test_hc_rename_guard.py` (D11).

The task prompt's "8 test files" counts the 7 `test_hardening_*.py` modules plus `__init__.py`; the pytest-collected count at top level is 7. Corrected sentence for the builder: *"New files the spec creates: `refs/primitive-differential.md`, `refs/agent-assertions.md` (D13), `refs/environment-deltas.md` (optional), `refs/probe-packs/read-parse.md` (optional), `tests/troubleshoot/fixtures/**`, `tests/troubleshoot/_assertions.py`, `tests/troubleshoot/test_calibrator_eval_cases.py`, and the T1-T19/T15 modules; `tests/troubleshoot/` itself and `backtest/` already exist and must be extended, not created."* Consequence for the builder: R-17's rename must update `test_hardening_h1.py:46` (D11) and R-16 must tighten `test_hardening_verdict.py:51` — both are edits to existing files, not greenfield.

---

## Summary

| Item | Label | One-line resolution |
|---|---|---|
| D1 | DECISION (a) + OPEN QUESTION (b) | Scoped `diff -rq`/`diff -q` gate + "no new drift" delta grep; full `verify-sync` is GREEN in the D14 worktree and in CI. Fixing the six orphans: recommend NO. |
| D2 | DECISION | Extend `status` at `SKILL:43,106,457,529`, `report-template.md:161`, `VAL:72,99-103`; `blocked ⇒ recommended_escalation: halt` (`SKILL:73`); no `sc-task-protocol` edit — it already FULL-STOPs on `halt`. |
| D3 | DECISION | Bump `1.1.0` → `1.2.0`; annotate the new field `Contract v1.2.0+`; align `hardening-output-contract.md:13,25`. |
| D4 | DECISION | One merged `SKILL:241` bullet (text above); `SKILL:530` untouched; `SKILL:266`+`:570` cap rows edited together. |
| D5 | DECISION | Replace `diagnosability-audit.md:253` with a numbered 5-shape list; type 5 = fail-closed observed-value emission. |
| D6 | DECISION | `## Producer citation (categorical symptoms)` section after `triage-checklist.md:44` (text above). |
| D7 | DECISION | Four Will-Not bullets after `SKILL:545`; audit line `cosmetic_overrun=<n>`; footer `cosmetic_overrun: <n>`; `SKILL:582` sentence. |
| D8 | DECISION | New bullet after `escalation-rubric.md:69` (`escalation_reason: split_pending`); add token to `CAL:108` and `SKILL:460`. |
| D9 | DECISION | 22-line `refs/environment-deltas.md` body, eight generic deltas, no OS/runtime/tool names. |
| D10 | DECISION | Refs-table rows for all four new refs (optional ones marked); footer only on `primitive-differential.md`. |
| D11 | DECISION | Rename every prose H-token in SKILL + 7 hardening refs; keep 3 hypothesis-label lines (allow-listed guard); `test_hardening_h1.py:46` → `"satisfy hc1"`; backtest constants stay. |
| D12 | DECISION | Exact kwargs at `SKILL:281`, `:345`, `:451`; v2 names + `locus_path` + `assertions_path`; all optional with `CAL:56`-style defaults; external spawners and the nightly suite unaffected. |
| D13 | DECISION | `refs/agent-assertions.md` is the single source; skeleton with C1-C8(+C3b), A1-A10, `id \| trigger \| flag \| severity`; flag names supplied for A6-A9, C6. |
| D14 | DECISION (a) + OPEN QUESTION (b) | Worktree `.dev/worktrees/troubleshoot-generalize` on `feature/troubleshoot-generalize` from `origin/master`; never stash. Fast-forwarding local `master`: recommend skip. |
| D15 | DECISION | `tests/troubleshoot/` exists (7 + backtest 14 modules); only `fixtures/`, `_assertions.py`, `test_calibrator_eval_cases.py`, and the T-modules are new. |
