# Research: Spec Extraction + Doc Cross-Validation

**Topic type:** Spec Extraction (per-R-item implementation cards) + anchor cross-validation
**Scope:** `merged-report-v2.md` lines 1-33 (frontmatter + Path keys) and §(d) lines 151-657; `spec-panel-critique.md` (362 lines); anchors cross-checked against `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (602 lines), `refs/*.md`, `agents/confidence-calibrator.md`, `agents/evidence-validator.md`, `commands/troubleshoot.md`
**Spec:** `/config/workspace/Coder/.claude/worktrees/gh-automation-orca-run/.dev/research/sysbox-retrospective-20260918/merged-report-v2.md`
**Critique:** `/config/workspace/Coder/.claude/worktrees/gh-automation-orca-run/.dev/research/sysbox-retrospective-20260918/spec-panel-critique.md`
**Status:** Complete
**Date:** 2026-09-19

Conventions used below:
- `[CODE-VERIFIED]` = quoted anchor text exists at the cited line in the repo today (Read on 2026-09-19).
- `[CODE-CONTRADICTED: ...]` = spec's line hint or quoted anchor does not match the repo; actual text/line given.
- Path keys from v2:16-32: `SKILL` = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`; `CMD` = `src/superclaude/commands/troubleshoot.md`; `CAL` = `src/superclaude/agents/confidence-calibrator.md`; `VAL` = `src/superclaude/agents/evidence-validator.md`; `HCT` / `RUB` = `refs/hypothesis-card-template.md` / `refs/escalation-rubric.md`. All `refs/` paths are relative to the skill dir.
- All quoted insert content is verbatim from v2 (line refs `v2:NNN`).

---

## 0. Global extracts (apply to every card)

### 0.1 Design rule paragraph (v2:155, verbatim)

> Design rule for every change: it must be executable as a checklist by a model that cannot infer, it must not halt for approval, and it must carry a falsifiable "would have caught X at wave Y" claim. No mandatory step names a runtime, OS, tool, file node, or CI system; incident-specific content lives only in optional kind-keyed packs, worked examples, and regression fixtures. The parent's circular gate (`IMPLEMENTATION-AUTHORIZATION.txt:5`) is the cautionary case: any new step that requires an artifact producible only by the gated action is rejected. Agents are the primary detection venue; the orchestrator's inline fallback runs the identical assertion list; tests cover both paths (A-016, `LF` §7.8).

Line-pinning caveat (v2:33): "Every `SKILL:`/`refs/`/`CMD:`/`CAL:`/`VAL:` insertion point below is a hint; the anchoring sentence is quoted beside it (A-007)." — treat every line number as a hint; the anchor sentence governs.

### 0.2 v1 → v2 renumber map (v2:161-181, verbatim)

| v1 | v2 | Item | Status |
|---|---|---|---|
| R-01 | R-01 | Execution-locus card | replaced (winner A) |
| R-03 | R-02 | Producer enumeration | verbatim, field renames |
| R-04 | R-03 | S14 + emitter search | replaced (winner B) |
| R-05 | R-04 | Discriminator rows at S1.6.4 | replaced (winner C-in-B) |
| R-02 | R-05 | Primitive differential + threshold bracketing | replaced (winner A) |
| R-12 | R-06 | Falsifier columns | verbatim |
| R-06 | R-07 | Discriminator form + self-consistency | replaced (winner A) |
| R-07 | R-08 | Same-evidence split | verbatim, artifact renames |
| R-08 | R-09 | Behaviour-definition fetch | replaced (winner A) |
| R-09 | R-10 | Headline-confidence coupling | verbatim, artifact renames |
| R-14 | R-11 | Persist-on-receipt | verbatim |
| R-10 | R-12 | Cosmetic-loop counter | verbatim + GAP resolutions |
| R-11 | R-13 | Provenance timestamps | verbatim |
| R-13 | R-14 | Agent assertion sets | verbatim + A9/A10/C7/C8, C6 reworded |
| R-15 | R-15 | Triage cause-class row | replaced (winner A) |
| R-16 | R-16 | Contract verdict enum | verbatim, `re-run permitted` |
| R-17 | R-17 | HC0-HC5 rename | verbatim |
| R-18 | R-18 | Command-file surface | replaced (winner B) |
| R-19 | R-19 | Acceptance tests | replaced (winner A) |

NOTE: `spec-panel-critique.md` uses **v1** ids throughout (critique:12). Every critique id cited in the cards below has been translated to the v2 item it constrains.

### 0.3 Removed artifacts and names (v2:183, verbatim — the "do not create / do not reference" list)

> Removed artifacts and names: Wave 1.65; `discriminator-plan.md` (→ `diagnosability-tasklist.md` `## Discriminator rows`); the 7-cell `execution-locus.md` (→ four-question card); `refs/runtime-probe-pack.md` and P1-P8 (→ `refs/primitive-differential.md` table + optional `refs/probe-packs/<kind>.md`); `refs/discriminator-template.md` (→ form embedded in `HCT`); `bisect.md` (→ `bracket.md`); `push-allowed` (→ `re-run permitted`); `predicted-passing-arm` (→ `Reference-context value`); `runtime=` card field (→ `runs-in=`); `control_arm_unproven` (→ `control_unproven`); the mandatory `image-layers=` row (→ derived from an S14 predicate when the layer count is the unobserved datum).

### 0.4 Q1-Q6 dispositions (v2:187-194, verbatim)

| Q | Disposition | Where |
|---|---|---|
| Q1 Discriminator-before-hypothesis: mandatory wave or conditional gate? | **Neither a wave nor a gate.** A two-clause mechanical trigger evaluated inside the existing S1.6.4 branch sets `discriminator-required=yes`, forces the tasklist to be emitted, and adds probe rows to it; control flow is otherwise unchanged; never a halt | R-04 |
| Q2 Thin-client topology map: Tier 0 or Wave 1? | **Wave 1 step 1b**, four-question card (before "Reproduce or observe"; step 2 runs the repro via `OBSERVE-VIA`) | R-01 |
| Q3 Probe pack static or generated? | **Static and optional.** One mandatory generic probe-form table (six primitive kinds); incident-derived probes live in optional `refs/probe-packs/<kind>.md`, loaded by kind, append-only via retrospectives, never a decision input | R-05 |
| Q4 Budget guardrail | **Counter + audit line, forced action, never a halt** | R-12 |
| Q5 Weak model + same-evidence experiment: template library? | **One form / one archetype row**, not a library: the two-hypothesis form embedded in the card template; the exact/reference pair from the probe-form table | R-07, R-08 |
| Q6 Parent-orchestrator role | **Out of scope.** With R-01..R-19 in the skill, the parent's authorization files have no function for a single-agent run; `blocked-on-authorization` (R-16) is the only new verdict | Rejected list |

Inconsistency note: Q1 says "two-clause mechanical trigger" but R-04's trigger (v2:295) has THREE OR-clauses (≥2 surviving; datum absent; `producer-count=unknown`). The third clause was added by AD-02/GB-04 resolution; Q1's wording is stale. Implement the three-clause R-04 text.

### 0.5 Hard-stop tasklist composition S1.6.4a — shared section order for R-03..R-06 (v2:196-206, verbatim)

> When S1.6.4 emits `diagnosability-tasklist.md` (verdict ∈ {partial, insufficient}, including when R-04's trigger forced `partial`), the file has these sections in this order, each written by the item named:
>
> 1. Header: `Round: <N> of 3`, `re-run permitted: yes|no|unknown`, `discriminator-required: yes|no`, `capability-verdict: blocked|n/a`, `indistinguishable: <a>,<b>` (only when R-04 step 3 gave up), `probe-rows-truncated: <n>` (only when R-04 capped).
> 2. `## Emitter search` (R-03).
> 3. `## Discriminator rows` (R-04 pairs + control row; R-06 falsifier columns on every row; R-05 2×2 differential when both environments were observed).
> 4. `## Bracket` (R-05 step 5, only when its trigger fired).
> 5. `## Fix candidate` (R-03 step 5, optional).
>
> One file, one counter (`diagnosability-rounds.json`, R-04). Wave 5 renders unexecuted rows under Next Steps.

Inconsistency note: item 5 says "`## Fix candidate` (R-03 step 5, optional)" but R-03's paste-ready procedure has steps 1-4 only; the fix-candidate sentence is the trailing paragraph of constraint 5 ("A `fix-candidate` row (diff path) may accompany it in the same round under `## Fix candidate`"), not a "step 5". Also R-03's header text (v2:278) omits `discriminator-required:` which the S1.6.4a header (v2:200) requires — R-04 owns that header key; the implementer must merge both into one header line.

---

## 1. Per-R-item implementation cards

### R-01 Execution-locus card (Wave 1 step 1b)

**Layer**: skill (SKILL.md) + ref (`HCT`) + new optional ref (`refs/environment-deltas.md`) + new artifact `<output-dir>/execution-locus.md`.

**Target files**: `SKILL` (Output Contract table :41-77; wave map :97; Wave 1 steps :167-168; Wave 1.7 :280 analogy); `refs/hypothesis-card-template.md` (new mandatory `runs-in:` field); new `refs/environment-deltas.md` (optional).

**Anchors (repo)**:
- `SKILL:97` `Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)` [CODE-VERIFIED] — spec says change to "grounding + locus + reproduce".
- `SKILL:167` `- If \`--no-mcp\` or both MCPs are unavailable: fall back to \`Glob\` + \`Grep\` on the issue keywords; note the fallback in the audit log.` [CODE-VERIFIED] (step 1 fallback bullet; insert step 1b after this).
- `SKILL:168` `2. **Reproduce or observe** (when feasible and cheap):` [CODE-VERIFIED] — gains "run the repro via `OBSERVE-VIA` from the locus card".
- `SKILL:41-77` Output Contract table [CODE-VERIFIED] — add row `execution_locus_card_path`.
- `SKILL:280` `The hypothesis card MUST set \`consistency_with_docs\` to one of ...` [CODE-VERIFIED] (analogy for "returned unread").
- `refs/runtime-entrypoint-verification.md:13-24` producer/transformers/consumer schema [CODE-VERIFIED] — the schema R-01 must NOT duplicate.
- Greenfield check: `execution-locus`, `runs-in=`, `environment-deltas` return 0 hits in skill/refs/agents/commands today.

**Insert content (verbatim v2:216-228)** — the "Weak model must" checklist, to become SKILL Wave 1 step 1b:

> **Weak model must** write, one line each, `unknown` legal, blank illegal:
>   1. `PRINT-SITE:` the file / stream / job / terminal where the failing line appeared. Copy verbatim from the issue.
>   2. `RUN-SITE:` the `file:line` from step 1 that emits that line, `@` the process/host/environment label under which it executes. Initial value `pending-producers` if step 1 found none; overwritten by R-02 step 4 with the surviving producer's `file:line`. Validator A7 rejects the sentinel at finalize **only when `producers.md` has ≥1 producer row**; otherwise the sentinel is legal with `status: partial`.
>   3. `SAME-ENV:` `yes` / `no` / `unknown`. Derivation: `no` if the issue text or the step-1 grounding (CI matrix, workflow file) names more than one machine, process, job, or environment label; `yes` if exactly one is named and RUN-SITE is in it; otherwise `unknown`.
>   4. `OBSERVE-VIA:` `same-shell` / `remote-command` / `artifact-file` / `nobody` — how RUN-SITE's stdout and exit status can be read from here.
>   5. If the issue names more than one arm (matrix, "works in X, fails in Y"): repeat 1-4 per arm, then per *passing* arm add `CONTROL-PROOF:` `yes: <file:line>` / `no: <file:line>` / `unknown` — the line where that arm executes the RUN-SITE producer.
>
>   Rules:
>   - `SAME-ENV ≠ yes` ⇒ every probe result and every hypothesis card carries `runs-in=<RUN-SITE label>`; a card without it is returned unread (analogous to `consistency_with_docs` at `SKILL:280`). `runs-in=unknown` is legal but the calibrator caps Runtime check ≤0.5 with Notes `locus_unknown` (C3b, R-14).
>   - `SAME-ENV ≠ yes` ⇒ read optional `refs/environment-deltas.md`: a generic prompt list (`host, process, user, filesystem-view, network-view, clock, permissions, installed-versions, working-dir, env-vars`) and, per item, an optional sub-ref with concrete probes. Items the model cannot prove identical are candidate discriminator rows for S1.6.4 (R-04) and Wave 1.7. Loading is locus-triggered, never `--type`-triggered. Absent ref ⇒ audit line `optional_ref_absent: refs/environment-deltas.md`, no Grounding Gap.
>   - Step 2 executes any repro through `OBSERVE-VIA`; `nobody` ⇒ record "no repro available: run-site unobservable".
>   - **Verdict source** (INV-004/INV-007): when `OBSERVE-VIA = artifact-file` or the failing arm is a CI job, fetch the failing arm's job log to `<output-dir>/job-<id>.log` *before* reading any verdict; the verdict is the last line in that log matching the harness's result marker, never the workflow- or job-level conclusion; no marker line ⇒ `verdict: unobservable`, treated as FAIL. Worked example (incident): `gh run view <run-id> --json jobs --jq '.jobs[]|[.databaseId,.name,.conclusion]'` then `gh api repos/<owner>/<repo>/actions/jobs/<id>/logs > <output-dir>/job-<id>.log`; marker `^RESULT:` (`--log-failed` is empty under continue-on-error, `OC` B2). Validator A8 checks the log exists at finalize.
>   - A passing arm may be cited as a control only with `CONTROL-PROOF: yes: file:line`; otherwise Symptom coverage ≤0.5, Notes `control_unproven` (C3).

Additional insert facts (v2:212-214): output artifact `<output-dir>/execution-locus.md`; "Runs on every invocation including pasted-log issues; re-derived per invocation, never carried over (A-011)"; the `HCT` gains a mandatory `runs-in:` field. Additional R-05-owned rule that lands in R-01's text (v2:314): "load `refs/probe-packs/<kind>.md` if it exists for any primitive kind listed for a surviving producer; the load set is kind-based, never runtime- or `--type`-based."

`refs/environment-deltas.md` content: v2 gives only the prompt list (`host, process, user, filesystem-view, network-view, clock, permissions, installed-versions, working-dir, env-vars`) and "per item, an optional sub-ref with concrete probes". No further body text is specified — FLAG: the implementer must author this ref's body; v2 provides no paste-ready text for it.

**Must NOT** (v2:229): block on `unknown`; ask the user; add a flag; add an approval step; mandate any environment-specific cell; duplicate the producer/transformer/consumer schema of `refs/runtime-entrypoint-verification.md:13-24`.

**Critique constraints**:
- X-02 (CRITICAL) — verdict-source rule re-attached as an R-01 rule keyed on `OBSERVE-VIA = artifact-file`; `gh` pair is worked example only.
- X-04 — field map: `symptom-site`→`PRINT-SITE`; `code-site`→`RUN-SITE` file:line; `runtime`→`RUN-SITE @label` / card `runs-in=`; `who-can-observe-it`→`OBSERVE-VIA` (`same-shell`/`remote-command`/`artifact-file`/`nobody`); `control-arm-executes-producer`→`CONTROL-PROOF`; `kernel`/`fs` dropped; `SAME-ENV` new; Notes `control_arm_unproven`→`control_unproven`.
- AD-03 — `runs-in=unknown` legal but C3b caps Runtime check ≤0.5 `locus_unknown`.
- AD-04 — A7 fires only when `producers.md` has ≥1 producer row.
- RQ-04 — labels counted after step-1 grounding (CI matrix in repo counts even if issue text omits it).
- RQ-06 — pasted-log/unit-test issues: four lines, `SAME-ENV: yes`, `OBSERVE-VIA: same-shell`, no ref load.
- FM-04 — absent optional ref ⇒ `optional_ref_absent: <path>` audit line, never a Grounding Gap.

**R-19 tests**: T5 `test_locus_card.py` (four lines + CONTROL-PROOF; missing line ⇒ Wave 1 exit FAIL; SAME-ENV derivation on one-env/two-env/no-env; `runs-in=` absent ⇒ card returned); T5b `test_verdict_source.py`; T1 A7/A8 cases; T2 C3/C3b; T15 Astra ("cards lacking `runs-in=` returned at Wave 1.7, A7 does not fire").

**Dependencies**: R-02 step 4 overwrites `RUN-SITE` sentinel (R-01 must land first; R-02's overwrite rule references the sentinel value `pending-producers`). R-04 consumes `OBSERVE-VIA`, `CONTROL-PROOF`, and the deltas candidates. R-05 consumes `OBSERVE-VIA` + `CONTROL-PROOF` and owns the probe-pack load rule text placed here. R-14 defines A7/A8/C3/C3b. R-18 surfaces the card at `CMD:69`.

**Falsifiable claim** (v2:230) retained for the task file's acceptance wording: `SAME-ENV` derives `no` on the incident (two runners in the matrix); Astra cards lacking `runs-in=` returned at Wave 1.7; GLM passing arm fails `CONTROL-PROOF` (`no: startup.sh:753-754`); job-log rule yields `RESULT: FAIL` where the workflow said `success (masked)`.

### R-02 Producer enumeration (S1.6.0b) + primitive grep + menu-equality rule

**Layer**: skill (Wave 1.6 S1.6.0 extension + Wave 3 step 2 rule) + ref (`refs/triage-checklist.md` new section) + new artifact `<output-dir>/producers.md`.

**Target files**: `SKILL` (:230 S1.6.0; :342 Wave 3 step 2 bullet); `refs/triage-checklist.md` (after :44).

**Anchors (repo)**:
- `SKILL:230` `1. **S1.6.0 — Component identification**. ... Record as \`failing_component\` in the audit log. Branches A and B scope queries to this component first; expand outward only if no signal is found.` [CODE-VERIFIED] — insert S1.6.0b after this paragraph.
- `SKILL:342` `- An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, \`consistency_with_docs\` ... and a one-line "if I'm wrong it's probably because...".` [CODE-VERIFIED] — add one bullet after it (paste full `## Producers` table + menu-equality check).
- `refs/triage-checklist.md:44` `If none of these are available, the hypothesis card is marked \`unverified\` and the confidence dimension "Evidence grounding" is scored 0.0.` [CODE-VERIFIED] — new section after this line.
- Greenfield: `producers.md` 0 hits today.

**Insert content (verbatim v2:239-245)**:

> **Weak model must** always create `<output-dir>/producers.md` with header `observation-kind: categorical|string|trace`; when the observation is a categorical value (enum string, status word, exit code):
>   1. Repo-wide: `git grep -n -F '<value>' -- ':!*.md'` and `git grep -n -E '<var>=' -- ':!*.md'`; list every hit as a producer row. Computed enums (`rc=$prefix-unavailable`) ⇒ `producer-count=unknown`, treated as insufficient and as an R-04 trigger.
>   2. For each producer inside a function, list every `return`/`exit`/`break` line between the function header and the producer (`grep -n -E '^\s*(return|exit|break)'` within the range).
>   3. Write the `## Producers` table: `line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving=yes|no`. The partition writes `surviving` into the file **before** the R-04 trigger reads it — never from context (INV-002). Row count MUST equal grep hit count; the audit line records both numbers. Zero `surviving=yes` rows while ≥1 producer row exists ⇒ contradiction: mark every row `surviving=re-opened`, treat as `producer-count=unknown` (AD-02). A Wave 3 split (R-08) appends to a separate `## Mechanism rows` section, excluded from the count invariant.
>   4. Primitive grep targeting: one pattern per row of the R-05 probe-form table, run over `$(cut -d'|' -f1 producers.md | sort -u)`; the `read/parse` row's pattern is `/proc/|/sys/|/dev/` excluding `/dev/(null|stdout|stderr|tty|zero)` and lines matching `[0-9]*>\s*/dev/` (INV-005); emit one R-05 exact/reference pair per hit. On `df00c06` the expected first hit is `startup.sh:504` (`LA` §9), plus askpass `:37-38`; fixture bound ≤ 8 rows. Overwrite the R-01 `RUN-SITE` sentinel (`pending-producers` → the surviving `file:line`).
>   5. A control arm counts only if the R-01 `CONTROL-PROOF` is `yes: <file:line>`.
>   6. Every Wave 1.7/Wave 3 subagent prompt MUST paste the full `## Producers` table. Menu-equality check: count of distinct enum values in the prompt == count of `surviving=yes` rows.

Placement note (v2:237): "as S1.6.0b *(reconciled per debate X-005: the count must exist before the R-04 trigger reads it)*".

**Must NOT** (v2:246): rank producers by plausibility at this step; drop rows without a cited exclusion line; grep only `failing_component`; have each agent re-grep.

**Critique constraints**:
- X-04 — field renames (`code-site`→`RUN-SITE`; `runtime=`→`runs-in=`).
- X-03 — step 4 uses "one pattern per row of the R-05 probe-form table" (single table owned by R-05), not a `/proc` regex only. NOTE the `read/parse` pattern literally names `/proc/|/sys/|/dev/` — this is a mandatory-step file-node name that arguably violates the design rule (v2:155 "No mandatory step names a ... file node"). Rescore table (v2:638) accepts it as "`df00c06` cites remain as expected-value notes". FLAG for implementer judgement: keep the pattern as the read/parse row's example, or move to `probe-packs/read-parse.md`.
- AD-02 — zero-surviving ∧ ≥1 producer ⇒ `surviving=re-opened`, `producer-count=unknown`.
- AR-02 — file always created at S1.6.0b with `observation-kind` header and zero producer rows when non-categorical; `## Mechanism rows` excluded from count.
- Rejected list (v2:615) — "producer enumeration is S1.6.0b, before the 1.6 hard-stop (X-005)".

**R-19 tests**: T3 `test_producers_enumeration.py`; T4 `test_primitivegrep_targeting.py`; T19 `test_menu_equality.py`; T1 A7 neg case ("sentinel with empty producers.md").

**Dependencies**: R-01 (sentinel `pending-producers`, `CONTROL-PROOF`); R-05 (probe-form table rows drive step 4 patterns — R-05's table must exist before step 4 is meaningful); R-04 (reads `surviving` rows + `producer-count=unknown`); R-08 (writes `## Mechanism rows`); R-14 A7.

**Falsifiable claim** (v2:247): GLM retry-2 at Wave 1.6 rows `startup.sh:571`, `:579`, `:718`, `:752-760`, askpass `:23`, primitive-grep `:504`; Tier-2 prompt could not omit `runner-unavailable` without failing the count check (T19).

### R-03 Sufficiency row S14 + emitter search before `blocked` (Wave 1.6 hard-stop)

**Layer**: ref (`refs/diagnosability-audit.md`: S14 row, Section 7 constraint 5, tasklist skeleton header) + skill (`SKILL:241` hard-stop bullet).

**Target files**: `refs/diagnosability-audit.md` (:150, :247, :263); `SKILL` (:241).

**Anchors (repo)**:
- `refs/diagnosability-audit.md:150` `| **S13**: Intermittent keywords present AND 3-W's \`when_answerable != yes\` | \`insufficient\` (intermittent-with-no-trace short-circuit) |` [CODE-VERIFIED] — S14 row goes after it.
- `refs/diagnosability-audit.md:247` `4. **Revert annotation**: Patches added by the tasklist carry the comment \`# Diagnosability-tasklist instrumentation: revert after defect closed.\` so cleanup is mechanizable.` [CODE-VERIFIED] — constraint 5 goes after it.
- `refs/diagnosability-audit.md:263` `**Verdict**: <verdict>  **Complexity**: <complexity>  **failing_component**: <path>  **Round**: <N> of 3` [CODE-VERIFIED] — header append target (skeleton is inside a ```markdown fence, lines 260-274+).
- `SKILL:241` `... jump to Wave 5 with status \`partial\` (Waves 1.7-4 skipped). No hypothesis work happens in the same turn as the instrumentation patch.` [CODE-VERIFIED] — last sentence of the hard-stop bullet is replaced.
- Also touched by the same sentence: `SKILL:530` `- Emit an instrumentation tasklist ... no hypothesis work happens in the same turn as an instrumentation patch; the user re-runs after instrumenting.` [CODE-VERIFIED] — spec does not name it; FLAG as a consistency edit candidate (integration researcher scope).

**Insert content (verbatim v2:258-285)**:

`refs/diagnosability-audit.md` after row S13:

```markdown
| **S14**: the asserted value exists at a code-site (`file:line` known) but an intermediate layer between that site and what the model reads (filter, allowlist, projection, summary, formatter, wrapper) drops it or writes an expected/default value in its place | `insufficient` (the layer hides the datum) |
```

Section 7 after hard constraint 4:

```markdown
5. **Emitter search before `blocked`**. Before any task or verdict uses the word `blocked`, run this procedure and record it in the tasklist under `## Emitter search`:
   1. From the missing-evidence list, take every predicate that is a single boolean or enum expression at a known `file:line`. None → write `emitter-search: n/a (no single-expression predicate)` and skip 2-4.
   2. Grep the function containing the producer line and the one function that calls it (one level) for existing emit calls (print/log/echo/printf/write/tee/report append). Record `emitters-found: N` with `file:line` of each.
   3. N ≥ 1: add ONE line beside the nearest emitter: `<predicate-name>=<observed value>`; on any read error the line MUST print `<predicate-name>=unobserved`. Never print the expected value. N = 0: append ONE line to the most recently `Read` file in this run that is a log, report, transcript, or artifact — never a source file (`SKILL:545`); record `already-read-files: <count>`. That append IS the emitter.
   4. `capability-verdict: blocked` is valid ONLY when 2 found no emitter AND 3 found no eligible already-read file. The tasklist must then list every channel searched.
   Each line produced by 3 is a **task type 5 — fail-closed observed-value emission**, subject to constraints 1-4 (invocation site, additive, reversible, annotated). Any always-emit row (e.g. a count the symptom is asserted against) must name the S14 predicate it serves. A `fix-candidate` row (diff path) may accompany it in the same round under `## Fix candidate`; no later wave is a precondition (INV-013).
```

Tasklist skeleton header (line 263), append:

```markdown
**Round**: <N> of 3  **re-run permitted**: yes|no|unknown  **capability-verdict**: blocked|n/a
```

`SKILL:241`, replace the last sentence of the hard-stop bullet:

```markdown
No hypothesis work happens in the same turn as the instrumentation patch. The tasklist MUST contain the `## Emitter search` block (refs/diagnosability-audit.md Section 7, constraint 5); `capability-verdict: blocked` may appear only after that block records no emitter and no eligible already-read file. Precedence: emitters found ∧ `re-run permitted: no` ⇒ `blocked-on-authorization` (R-16), `status: blocked`; emitters found ∧ permitted or unknown ⇒ task rows, `status: partial`; no emitter ∧ no eligible file ⇒ `capability-verdict: blocked`, `status: blocked`.
```

Internal inconsistency: the skeleton line 263 already contains `**Round**: <N> of 3`; the append text repeats `**Round**: <N> of 3`. Implementer should append only `**re-run permitted**: yes|no|unknown  **capability-verdict**: blocked|n/a` (plus R-04's `**discriminator-required**: yes|no` and the conditional `indistinguishable:` / `probe-rows-truncated:` keys from S1.6.4a item 1). Also note "task type 5" — the existing ref has no numbered task types 1-4; the phrase "constraints 1-4" refers to hard constraints, but "task type 5" has no defined types 1-4 anywhere in v2 or the repo. FLAG.

Second inconsistency: the SKILL:241 replacement introduces `status: blocked` for the report, but the Output Contract `status` field (`SKILL:43`) is `success | partial | failed` today. R-16 says "status `blocked`, never `partial`". No R-item adds `blocked` to the `status` enum at `SKILL:43` or to the audit footer at `SKILL:457` (`status: <success|partial>`). FLAG: implementer must extend the `status` enum (also `VAL:72` Suggested report status `<success | partial>`, `VAL:99-103` Status Decision).

**Must NOT** (v2:287): add a new upload step; require the probe results before forming a hypothesis when `OBSERVE-VIA = nobody` (the circular gate); instrument production source (`SKILL:545` unchanged); treat a source file as an append target.

**Critique constraints**:
- AD-01 (CRITICAL) — N=0 append target restricted to log/report/transcript/artifact; only-source-Read ⇒ `capability-verdict: blocked` valid.
- RQ-01 — "most recently `Read` file in this run that is a log, report, transcript, or artifact".
- RQ-02 — "the function containing the producer line, and the one function that calls it (one level)".
- X-05 — `re-run permitted` (not `push-allowed`); precedence order; `capability-verdict` is a tasklist header field `blocked|n/a`, not a contract enum; A10 asserts co-occurrence.
- AR-01 — S1.6.4a section order (`## Emitter search` first).
- FM-02 — all channels unreachable ⇒ `capability-verdict: blocked`, channels listed, tasklist still written, `status: blocked`.

**R-19 tests**: T10 `test_hardstop_verdicts.py` (four cases); T1 A10; T15 Astra ("T10 emitter rule fires").

**Dependencies**: R-16 (`blocked-on-authorization`, `re-run permitted`); R-14 (A10); R-04 (shares header + S1.6.4a order; R-04 step 5 references `## Fix candidate`); R-15 (evidence-or-drop bullet cites "S14, R-03"); R-01 (`OBSERVE-VIA = nobody` Must-NOT clause).

**Falsifiable claim** (v2:288): Fable retry-2's `6ced457` falls out of step 3; Astra's "Concrete patch intentionally not emitted" refused because step 2 finds the existing `seed_diag_rows` emit call.

### R-04 Discriminator rows at S1.6.4 — trigger, pair form, control, counter

**Layer**: skill (`SKILL:240-241` S1.6.4 branch; `:248` counter rule; `:266` cap row; also `:570` duplicate cap row) + ref (`refs/diagnosability-audit.md` Section 7 tasklist schema per S1.6.4a). Probe-form table is NOT here (R-05 owns it).

**Target files**: `SKILL` (:240-241, :248, :266, :570); `refs/diagnosability-audit.md` Section 7 (:238-274+).

**Anchors (repo)**:
- `SKILL:240` `5. **S1.6.4 — Apply sufficiency rubric + complexity gate**. Compute \`diagnosability_verdict ∈ {sufficient | partial | insufficient | unknown}\`. ... Branch on \`(verdict × complexity)\`:` [CODE-VERIFIED] — trigger is evaluated "before the verdict branch".
- `SKILL:248` `**Per-defect patch-round counter**: the Wave 1.6 orchestrator maintains \`<output-dir>/diagnosability-rounds.json\` keyed by the Wave 0 \`issue_slug\`. Each hard-stop fires the counter +1. After 3 rounds for the same defect, the off-ramp message escalates (see refs/report-template.md hard-stop variant + cap prose). Reset via \`--reset-diagnosability-rounds\`.` [CODE-VERIFIED] — the whole "keyed by issue_slug / each hard-stop fires +1" wording is replaced by the single counter rule.
- `SKILL:266` `| 3-round diagnosability cap reached for an \`issue_slug\` | Per-defect counter at \`<output-dir>/diagnosability-rounds.json\` reached 3 hard-stops | Emit the 3-round cap message (refs/report-template.md hard-stop variant + cap-specific prose); refuse next tasklist until \`--reset-diagnosability-rounds\` is set |` [CODE-VERIFIED] — "refuse next tasklist" must change (FM-07). Identical row duplicated at `SKILL:570` [CODE-VERIFIED] — spec does not name :570; FLAG as required companion edit.
- `SKILL:255` exit line `Emit \`Wave 1.6 complete: verdict=<v> complexity=<c> hard_stop=<bool> round=<N>/3\`.` [CODE-VERIFIED] — natural home for the `discriminator-required=<yes|no>` activation-metric audit line (spec says "on every Wave 1.6 exit").
- Greenfield: `discriminator-required` 0 hits.

**Insert content — Trigger (verbatim v2:295)**:

> **Trigger** (mechanical, evaluated at S1.6.4 before the verdict branch): (`producers.md` has ≥2 `surviving=yes` rows) OR (the observed datum is absent from every captured output of the failing run, **including `job-*.log`**) OR (`producer-count=unknown`, incl. the zero-surviving re-open of R-02 step 3). When true: audit line `discriminator-required=yes`; if `verdict ∈ {sufficient, unknown}` then `verdict := partial` so the tasklist is emitted; `insufficient` unchanged. Control flow is otherwise the existing branch table; no new hard-stop. A `NameError` with one producer never enters it.

**Insert content — Weak model must (verbatim v2:297-303)**:

> **Weak model must**, when `discriminator-required=yes`, write `## Discriminator rows`:
>   1. For each `surviving=yes` producer row, classify its primitive into one of `read/parse | call/return | lookup | reach | permission | timing` and copy the pair shape from the R-05 table: `<name>-exact` (the exact expression at the producer line, executed in isolation, exit status captured) and `<name>-ref` (the reference form the table gives for that kind). Probes are exit-status only, no secrets, targeted at an invocation site (`SKILL:545` unchanged). Cap: at most 8 pairs, nearest to the exit statement first; overflow ⇒ header `probe-rows-truncated: <n>`.
>      - 1b. For each card or producer whose mechanism asserts what a primitive *does*, run R-09 (behaviour-definition fetch) before writing the pair.
>   2. Add one control row whose expected value is already known from a passing run or control arm (R-01 `CONTROL-PROOF: yes`); if none exists, the control is the R-05 table's control column for the first pair's kind.
>   3. Fill `value-if-<claim>-true | value-if-false` per R-06 on every row; at least one pair must differ between any two surviving causes. Add at most two rows to achieve this; still indistinguishable ⇒ header `indistinguishable: <a>,<b>` and proceed (R-10 renders `UNDETERMINED — among {a,b}`).
>   4. If `OBSERVE-VIA ≠ nobody`, run the rows now via that venue, record outputs in `tier1-observation.md`, and **re-evaluate S14 with the new observations before the branch** (the datum may now be observed); hard-stop only when the rows could not run. If `OBSERVE-VIA = nobody`, the rows stay in the tasklist; proceed per the branch table — do not halt for approval.
>   5. If a `## Fix candidate` row exists (R-03), it ships in the same re-run as the probe rows; the pair, not a debate, decides.

**Insert content — Counter (verbatim v2:304)** replaces `SKILL:248` wording:

> **Counter** (single rule, replaces `SKILL:248` wording "each hard-stop fires the counter +1"): `diagnosability-rounds.json` keyed `<branch>:<repro-venue-id>` where `repro-venue-id` = the failing arm's label as written in the issue or matrix (job name, or the repro command), digits stripped; increments once per emitted tasklist with `discriminator-required=yes`. Bracket rounds (R-05 step 5) have their own cap and never touch this counter (AD-05). At the 3-round cap (`SKILL:266`) the tasklist is **still written**; the report renders the cap message with `status: blocked`; the cap suppresses the re-run recommendation, not the file (FM-07).

**Invalid** (v2:305): a tasklist with zero probe rows while `producers.md` has ≥1 surviving row; a pair with only the `-exact` half; a control row with no cited passing arm and no table fallback.

**Activation metric** (v2:307): audit line `discriminator-required=<yes|no>` on every Wave 1.6 exit; `yes` on >20% of `bug`-type runs ⇒ tighten trigger to "datum absent" only.

Internal inconsistency: counter key `<branch>` is undefined — v2 never says whether `<branch>` means the git branch or the S1.6.4 branch-table row taken. The critique X-01 recommendation says "prefixed by branch" with no definition either. FLAG for the implementer (git branch is the likely reading since the purpose is "persists across slugs", T9). Also the existing counter is keyed by `issue_slug` and reset via `--reset-diagnosability-rounds` — v2 does not say whether the reset flag survives; assume unchanged.

**Must NOT** (v2:306): require probe results before forming a hypothesis when `OBSERVE-VIA = nobody`; add a wave, a file, or a hard-stop; wait for the re-run before Wave 1.7 when the branch table says continue.

**Critique constraints**:
- X-01 — single home for probe rows = `diagnosability-tasklist.md` `## Discriminator rows`; no Wave 1.65; no `discriminator-plan.md`; counter key defined.
- X-03 — copy the pair shape from the R-05 table.
- X-06 — verdict forcing defined: `sufficient|unknown` → `partial`; `insufficient` unchanged.
- RQ-03 — at most two added rows; then `indistinguishable: <a>,<b>`.
- RQ-05 — activation metric recorded via audit line.
- FM-01 — re-evaluate S14 after in-run execution before the branch.
- FM-07 — cap still writes the tasklist; suppresses recommendation only.
- AD-02 — zero-surviving re-open enters trigger via `producer-count=unknown`.
- AD-05 — one counter rule; bracket rounds separate.
- GB-03 — pair cap 8, nearest-to-exit first, `probe-rows-truncated`.
- GB-04 — `producer-count=unknown` / zero-surviving ⇒ trigger true.
- AR-01 — S1.6.4a section order.

**R-19 tests**: T17 `test_discriminator_rows.py`; T9 `test_counter_key.py`; T7 (bracket rounds do not increment); T15 Astra.

**Dependencies**: R-02 (surviving rows, `producer-count=unknown`); R-05 (table for kinds/pair shape/control fallback; step 5 bracket separate cap); R-06 (falsifier columns on every row); R-09 (step 1b); R-03 (`## Fix candidate`, header); R-10 (`UNDETERMINED — among {a,b}`); R-01 (`OBSERVE-VIA`, `CONTROL-PROOF`); R-16 (`status: blocked` at cap).

**Falsifiable claim** (v2:308): Astra retry-3 at S1.6.4 (3 surviving rows) emits `uptime-exact`/`uptime-ref`/`tmp-writable`/`setsid-present`/`git-present` plus one control, no new wave.

### R-05 Primitive differential + threshold bracketing (`refs/primitive-differential.md`)

**Layer**: new ref (`refs/primitive-differential.md`) + optional pack dir (`refs/probe-packs/<kind>.md`) + skill Refs-table row + new artifact `<output-dir>/bracket.md` + rule text in R-01 (pack load).

**Target files**: new `refs/primitive-differential.md`; new `refs/probe-packs/read-parse.md` (example pack, optional); `SKILL` Refs table after :600; R-01 text (pack-load rule); R-04 step 1 (invokes); R-02 step 4 (patterns).

**Anchors (repo)**:
- `SKILL:600` `| \`refs/effective-input-proof.md\` | Wave 4.5 (H4 fail-closed effective-input manifest) |` [CODE-VERIFIED] — last Refs-table row; new row after it: `refs/primitive-differential.md | S1.6.4 discriminator rows (R-04 step 1) for every surviving producer`.
- `SKILL:602` `Each ref is loaded only by the wave that needs it. Do not pre-load.` [CODE-VERIFIED] — table ends at :600, blank :601.
- Greenfield: `primitive-differential`, `probe-packs`, `bracket.md` 0 hits. `refs/runtime-probe-pack.md` does not exist (spec v2:314 confirms; must not be created).

**Insert content — Weak model must (verbatim v2:317-332)**, the body of `refs/primitive-differential.md`:

> 1. For each `surviving=yes` producer, list every external primitive the line touches; classify each by the table (the one table; R-04 copies from it):
>
>    | kind | exact form | reference form | control (when no passing arm) |
>    |---|---|---|---|
>    | read/parse | the read/parse idiom in source, isolated | bulk read of the whole node/stream | read of a file known present |
>    | call/return | the call with its real args, rc captured | the documented minimal call, same callee | `true` |
>    | lookup | the key/name resolution in source | resolution of a key known to exist / direct dump | known key |
>    | reach | the client as invoked against the producer's endpoint | raw connect to host:port / same client, known endpoint | known-reachable endpoint |
>    | permission | the operation on the producer's path | `stat`/`access` / same op on a path known writable | `-w` on cwd |
>    | timing | the wait/threshold with elapsed captured | same op with a generous bound | elapsed of a no-op |
> 2. Run exact AND reference on the failing environment AND a passing one (R-01 `CONTROL-PROOF: yes`), via the venue R-01 `OBSERVE-VIA` names; one `key=value` line each, pasted verbatim; write the 2×2 into `## Discriminator rows`.
> 3. Decision: exact≠reference on failing AND both equal on passing ⇒ cause class `substituted primitive` (R-15 row); fix form = reference form at every producer hit; ship fix + pair in one re-run (R-04 step 5). Any cell unobserved or single environment ⇒ `comparator=none`, Diagnosis begins `UNDETERMINED — no comparator`, cap 0.4.
> 4. If `refs/probe-packs/<kind>.md` exists, append its rows as extra probes; informational only, never a decision input.
> 5. Threshold bracketing: trigger = error text or `producers.md` names a numeric limit, OR the same input passes at a smaller value of a countable quantity N. Record N; run N-2/N-4/N-6 in the venue where the symptom reproduces (CI matrix if CI-only, as task-type-5 rows), one fixed exit line per cell; no pass ⇒ one extension N-8/N-10/N-12; cap two rounds (own cap, not the R-04 counter); report `bracket=[<pass>,<fail>] width=<w>` or `UNDETERMINED — no passing value in [N-12, N]`; guard = highest passing value; append to `<output-dir>/bracket.md`; audit line `bracket_trigger=<limit-in-text|passes-smaller>`. The report says the bracket width, never the incident's numbers.
> 6. A hypothesis card naming an environment property MUST cite a 2×2 row; absent ⇒ Notes `uncited`, calibrated cap 0.5 (C7).

**Insert content — pack-load rule for R-01 (verbatim v2:314)**: "load `refs/probe-packs/<kind>.md` if it exists for any primitive kind listed for a surviving producer; the load set is kind-based, never runtime- or `--type`-based."

**Insert content — Pack example (verbatim v2:336-344)**, `refs/probe-packs/read-parse.md`:

```
# read/parse pack — optional, append-only, cited
fstype=$(stat -f -c %T "$NODE")          # sysbox-fs: fuseblk (D3/tier2-devops:1)
size=$(stat -c %s "$NODE")               # kernel procfs 0; FUSE emulation 4096 (LF §3)
seekable=$(python3 -c "import os;f=os.open('$NODE',0);os.lseek(f,1,0);print(1)" 2>/dev/null||echo 0)
# add rows only with an incident citation; never a decision input
```

Internal inconsistency: step 3 "cap 0.4" for `comparator=none` — no calibrator rule C1-C8 in R-14 implements a 0.4 cap; C7 caps at 0.5 for `uncited`. The 0.4 cap has no agent home; T16 asserts it ("cap 0.4"). FLAG: either add a C-rule or make it an orchestrator Wave 5 rule (R-10 territory). Also "task-type-5 rows" refers to R-03's undefined "task type 5" (see R-03 flag). Also step 5's `bracket.md` is persisted-on-receipt per R-11 and read by C6 (R-14).

**Must NOT** (v2:333): name an OS, runtime, or tool in a mandatory row; compare one environment to a table of expected values; run mutating commands beyond a self-removed temp file; require root; extend packs at run time; halt.

**Critique constraints**:
- X-01 — no Wave 1.65; write the 2×2 into `## Discriminator rows` (not `discriminator-plan.md`); "R-05 step 4b/6" references removed.
- X-03 — ONE table (six rows × three cols), owned here; `refs/runtime-probe-pack.md` gone; packs at `refs/probe-packs/<kind>.md`.
- X-04 — "locus is reachable" ⇒ `OBSERVE-VIA ≠ nobody`; control ⇒ `CONTROL-PROOF`.
- X-08 — step 6 `uncited` ⇒ C7 (cap 0.5).
- AD-05 — bracket rounds have own cap (2), never touch `diagnosability-rounds.json`.
- AR-05 — three refs survive: `primitive-differential.md`, `probe-packs/<kind>.md`, `environment-deltas.md`.
- FM-03 — both envs unobserved ⇒ `comparator=none`, `UNDETERMINED — no comparator`, cap 0.4 (every CI-only bug reports UNDETERMINED until one re-run).
- Rejected (v2:609-610) — guard = highest passing value, width 2; CI matrix not host rebuilds.

**R-19 tests**: T16 `test_primitive_differential.py`; T7 `test_threshold_bracket.py`; T4 (one pattern per table row); T2 C7.

**Dependencies**: R-01 (`OBSERVE-VIA`, `CONTROL-PROOF`, pack-load rule text lives in R-01); R-02 (step 4 patterns per table row; surviving producers); R-04 (step 1 invokes; step 5 co-ship; `## Bracket` section); R-06 (columns); R-15 (`Substituted primitive` cause class); R-14 (C6 reads `bracket.md`; C7); R-11 (persist `bracket.md`).

**Falsifiable claim** (v2:334): producer `startup.sh:504` → kind `read/parse`, exact `IFS=' ' read -r u _ <f`, reference `$(<f)`; 2×2 = sysbox `1/0`, DinD `0/0`; layer symptom k=2 ⇒ `bracket=[76,78] width=2`.

### R-06 Falsifier column on every instrumentation row

**Layer**: ref (`refs/diagnosability-audit.md:242-247` hard constraints; Section 7 tasklist schema) + skill (`SKILL:241` sentence).

**Target files**: `refs/diagnosability-audit.md` (:242-247 hard constraints list; :249-256 per-line task format); `SKILL` (:241); `refs/report-template.md` Next Steps (one line).

**Anchors (repo)**:
- `refs/diagnosability-audit.md:242` `### Hard constraints (non-negotiable)` and :244-247 constraints 1-4 [CODE-VERIFIED].
- `refs/diagnosability-audit.md:249-256` `### High-specificity per-line task format` — `Each task names:` Invocation site / Current code / Add ... / Rationale [CODE-VERIFIED] — natural place for the two new columns.
- `SKILL:241` `No hypothesis work happens in the same turn as the instrumentation patch.` [CODE-VERIFIED] — this sentence is ALSO replaced by R-03. FLAG: R-03 and R-06 both edit the same sentence; the merged replacement must contain R-03's precedence text AND R-06's "Every tasklist row carries `value-if-<claim>-true | value-if-false`; a row without both is invalid."

**Insert content (verbatim v2:351, 353)**:

`SKILL:241` gains:

> Every tasklist row carries `value-if-<claim>-true | value-if-false`; a row without both is invalid.

Weak model must:

> fill both columns per row from the producer statement (e.g. `uptime-regex | false | true`); write one line in REPORT.md Next Steps: "The report stays `partial` until `<row>=<value>`" (Fable's `D3/candidate-fixes.md:21` form). Validator A2 checks it.

**Must NOT** (v2:354): require a run before publishing.

**Critique constraints**: AR-01 (columns live on every `## Discriminator rows` row in the fixed section order); R-07 note (v2:361): "R-06's `value-if-true | value-if-false` columns stay for single-row tasklists; the 2×2 form is for two-hypothesis cases."

**R-19 tests**: T1 A2 (`instrumentation_without_falsifier`); T17 (rows carry both columns — implied by "pair completeness"); T15 GLM (A2 is NOT in the GLM expected set {A1,A3,A4,A5,C2,C3} — note the falsifiable claim at v2:355 says GLM lacked falsifiers, yet A2 is absent from the T15 GLM flag set; FLAG minor inconsistency: A2 requires `diff_path` touching a collector, which the GLM fixture may not include).

**Dependencies**: R-03 (same sentence at SKILL:241); R-04 (step 3 "per R-06 on every row"); R-14 (A2, C4 `no_prereg_falsifier`); R-10 (falsifier sentences rendered in UNDETERMINED Diagnosis).

**Falsifiable claim** (v2:355): GLM retry-2 would have pre-registered "dns=true ∧ https=true ⇒ clone-failed false".

### R-07 Discriminator form, pre-registered outcome table, probe self-consistency

**Layer**: ref (`HCT` — form embedded; filling rule) + skill (`SKILL:439` Evidence bullet self-consistency rule) + agent (VAL A6/A9 via R-14). NO new `refs/discriminator-template.md`.

**Target files**: `refs/hypothesis-card-template.md` (:80-82, :91, :93-105 unchanged); `SKILL` (:439).

**Anchors (repo)**:
- `HCT:80-82` `## Falsification standard` / `One sentence. What concrete evidence — an executable command and expected output ... would prove this hypothesis WRONG? ...` [CODE-VERIFIED] — keeps its one sentence for single-hypothesis cards; two-mechanism cards MUST embed the form.
- `HCT:91` `Filling rule: an empty or "Not applicable" value on \`evidence_class\` is a defect; cards with \`claim_class: runtime_behavior\` AND \`evidence_class ∈ {source_static, doc_static, none}\` MUST self-cap their confidence at 0.65 ...` [CODE-VERIFIED] — gains "a card whose claim names an enum token MUST cite `producers.md` row IDs".
- `HCT:93-105` `## Recommended evidence shape (v2.0 preview)` ... `This shape is **OPTIONAL in v1.5**` [CODE-VERIFIED] — stays optional.
- `SKILL:439` `   - Evidence (cited \`file:line\` and command outputs)` [CODE-VERIFIED] — gains the self-consistency rule.
- Greenfield: `Reference-context value`, `Pre-registered outcome` 0 hits.

**Insert content — Fill-in form (verbatim v2:364-379)**, embedded in `HCT` under Falsification standard:

```markdown
# Discriminator: <symptom or token>
Hypothesis A: <one sentence naming the runtime property that differs>
Hypothesis B: <one sentence>
Observable that differs: <one boolean; where it is emitted — file:line, log key, metric name, or column>
Exact probe: <one read-only command or query; result reduces to true|false>
Primitive under dispute, fetched verbatim: <locator + pasted text of the thing the two mechanisms disagree about: a function body, a library doc section, a config schema, an RFC/spec paragraph. NOT the observed output.>
Reference-context value: <true|false|n/a — what the observable reads in a known-good context (passing run, passing test, passing environment, known-good input). n/a only on the first instrumented run.>
Pre-registered outcome table (written before the probe runs):
| Probe result | A | B |
|---|---|---|
| true  | <consistent|refuted> | <consistent|refuted> |
| false | <consistent|refuted> | <consistent|refuted> |
Falsifier sentence: "If <observable>=<value> on the next run, <A|B> is false."
Self-consistency: if Reference-context value ≠ the value actually observed in the reference context, mark THIS PROBE `suspect` under Grounding Gaps; do not read the outcome table for it.
```

**Insert content — Validator rule (verbatim v2:381)** for `SKILL:439` / R-14:

> **Validator** (SKILL Evidence bullet; R-14): A6 — `Reference-context value` must be a single literal (reject `if|only|/|,`); A9 — mismatch with the observed reference ⇒ probe `suspect`, not hypothesis; first instrumented run ⇒ `n/a`, rule applies from the next run (INV-017).

**Worked examples (verbatim v2:382-383)** — both become fixtures (T6 io / nonio) and may be placed in `HCT` as appendix:

> **Worked example (real, verified — the incident)**: A: the pseudo-file is served non-seekable so the shell's 1-byte read fallback fails. B: temp dir unwritable at `mktemp` (`D3/REPORT.md:46`). Observable: `uptime-regex` (`IFS=' ' read -r up _ < /proc/uptime; [[ $up =~ ^[0-9] ]]`). Primitive under dispute: `procUptime.go Open()` sets `nonSeekable=true`; bash `read.def` `lseek … ESPIPE → zread(fd,&c,1)` (`D3/REPORT.md:27-28`). Reference-context value: `true`. Table: true → A refuted / B consistent; false → A consistent / B consistent (B needs its own probe `tmp-writable`). Falsifier: "If uptime-regex=true on the next run, A is false" (`D3/REPORT.md:51`). Observed `false`, `bulk=true`, `tmp-writable=true` (`Z:seed-checkout.txt:9-11`) → A confirmed, B refuted, one run. Companion probe `started-line`: reference value `true`, observed `false` beside `cloned` (`Z:seed-checkout.txt:13,1`) → probe suspect, not hypothesis.

> **Worked example 2 (illustrative, non-I/O — queue consumer ordering)**: Symptom: duplicate invoice emails. A: consumer acks after side-effect, so a crash between send and ack redelivers. B: producer publishes twice on HTTP retry. Observable: `redelivered` flag on the consumed message header. Probe: `SELECT bool_or(redelivered) FROM consumed_log WHERE invoice_id=:id`. Primitive under dispute (verbatim): broker doc §"Consumer acknowledgements": "If a consumer's channel closes before an ack is received, the message is requeued with `redelivered=true`." Reference-context value: `false`. Table: true → A consistent / B refuted; false → A refuted / B consistent. Falsifier: "If redelivered=false on the next duplicate, A is false."

Note: A6 regex `if|only|/|,` would reject the literal `n/a` (contains `/`). v2:371 says `n/a` is legal "only on the first instrumented run" and v2:381 says "first instrumented run ⇒ `n/a`, rule applies from the next run" — so A6 must be gated on not-first-run. FLAG for T1 A6 fixture design.

**Must NOT** (v2:384): multi-hypothesis cards; more than two arms per form; new claim classes (`HCT:93-105` optional table stays optional).

**Critique constraints**: X-07 — mismatch rule is **A9**, not A7. X-04 — `predicted-passing-arm` → `Reference-context value`. Rejected (v2:627) — no YAML block; validator checks kept, schema not. TS-02 — nonio fixture from example 2.

**R-19 tests**: T6 `test_discriminator_form.py`; T1 A6, A9.

**Dependencies**: R-08 (fills one R-07 form per pair); R-14 (A6, A9); R-02 (`producers.md` row IDs cited by enum-claim cards); R-06 (single-row columns vs 2×2 form split).

**Falsifiable claim** (v2:385): the filled form parses; outcome table has exactly one row consistent with observed `false/true/true` (T6).

### R-08 Same-evidence divergence → splitting experiment (Wave 3 step 4.5)

**Layer**: skill (Wave 3 new step 4.5; Wave 4 precondition; Wave 3 failure-handling row) + ref (`refs/escalation-rubric.md:63-69` one rule).

**Target files**: `SKILL` (:346 → insert 4.5 after; :348 header; :372; :381); `refs/escalation-rubric.md` (:63-69).

**Anchors (repo)**:
- `SKILL:346` `4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.` [CODE-VERIFIED] — step 4.5 goes after.
- `SKILL:348` `#### Tier 2 calibration completeness gate (hard precondition for report publishing)` [CODE-VERIFIED] — step 4.5 goes before this header.
- `SKILL:372` `| All agents converge with high confidence | Skip Wave 4 (adversarial); jump to Wave 5 | None |` [CODE-VERIFIED] — gains "skip Wave 4 only if the converged variable is *observed*, else `split-pending`".
- `SKILL:381` `**Preconditions**: Wave 3 marked ≥ 2 fixes as \`competing\` (or \`--depth deep\` + ≥ 2 distinct proposals, even if consensus).` [CODE-VERIFIED] — gains "and no mechanism disagreement remains un-probed".
- `SKILL:386-397` `2. **Invoke \`/sc:adversarial\` in compare mode** via \`Skill\`:` ... [CODE-VERIFIED] (the "rhetorical `--compare`" being bypassed).
- `refs/escalation-rubric.md:63-69` `3. **Signal-driven escalation** (any one triggers escalation)` ... six bullets [CODE-VERIFIED] — "gains one rule" (v2 does not give the rule's text; FLAG: v2:391 says the rubric "gains one rule" but never specifies it. Nearest inferable content: a `split-pending` cluster forces ESCALATE / blocks Wave 4 skip. Implementer must author.)

**Insert content (verbatim v2:394-395)**:

> **Weak model must**: when two cards cite the same `file:line` and assert different mechanisms, (1) write both mechanisms as one row each under `producers.md` `## Mechanism rows` (excluded from the R-02 count invariant); (2) fill one R-07 form per pair, naming the one command whose exit status differs if that mechanism is true (archetype: the R-05 `read/parse` row — exact idiom vs bulk read; incident instance `test-startup-boot.sh:443-444@39b526c`); (3) append both probes as rows to `diagnosability-tasklist.md` `## Discriminator rows` (create the file if Wave 1.6 emitted none); (4) mark the cluster `split-pending`, which satisfies the Wave 4 precondition without invoking the debate. Wave 4 debates only fix mechanism for a shared diagnosis (`PROTOCOL-CORRECTION.txt:11`).

> **Open question 5 answer**: one archetype row, not a library. The pair shape — same input, two idioms, exit status each — covers every read/parse disagreement; a library invites cargo-culting.

Edits to existing lines (v2:392): `:381` gains "and no mechanism disagreement remains un-probed"; `:372` gains "skip Wave 4 only if the converged variable is *observed*, else `split-pending`".

Internal inconsistency: (4) says `split-pending` "satisfies the Wave 4 precondition without invoking the debate" while `:381`'s added clause says Wave 4 requires "no mechanism disagreement remains un-probed" — i.e. `split-pending` should PREVENT Wave 4 for that cluster, not satisfy its precondition. Read as: split-pending clusters are excluded from Wave 4's competing set (skip debate for them); Wave 4 runs only for remaining fix-mechanism disagreements on a shared diagnosis. FLAG wording for the implementer.

**Must NOT** (v2:396): require both probes to return before Wave 5; block on the debate; add a third hypothesis agent to break ties.

**Critique constraints**: X-01 — probes go to `diagnosability-tasklist.md` `## Discriminator rows`, not `discriminator-plan.md`. AR-02 — `## Mechanism rows` section excluded from count invariant. AR-03 — create tasklist file if Wave 1.6 emitted none; Wave 5 Next Steps renders unexecuted rows.

**R-19 tests**: T3 (`## Mechanism rows` excluded from count); T6 (form); no dedicated test for step 4.5 or `split-pending` — FLAG coverage gap (T13 parity covers only flag sets).

**Dependencies**: R-02 (`## Mechanism rows`); R-07 (form); R-05 (`read/parse` archetype row); R-04 (`## Discriminator rows` section); R-10 (Wave 5 rendering of unexecuted rows).

**Falsifiable claim** (v2:397): Fable retry-3 Wave 3 — rca "single buffered read" vs devops "ESPIPE 1-byte path" — resolves to the shipped pair by rule.

### R-09 Behaviour-definition fetch (Wave 3 step 1 + S1.6.4 step 1b)

**Layer**: skill (Wave 3 step 1 new sub-bullet; referenced from R-04 step 1b) + new artifact `<output-dir>/behaviour-definitions.md` + agent input (`CAL` `behaviour_definitions_path`, R-14).

**Target files**: `SKILL` (:333-336; insert after :336); `CAL` inputs (via R-14).

**Anchors (repo)**:
- `SKILL:333` `1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals ...` [CODE-VERIFIED].
- `SKILL:336` `   - \`mcp__auggie__codebase-retrieval\` with a more targeted query than Tier 1 (e.g. "find every call site of \`<symbol>\` and how they handle the error case")` [CODE-VERIFIED] — new sub-bullet after it.
- Greenfield: `behaviour-definitions` 0 hits.

**Insert content — paste-ready (verbatim v2:407-417)**:

> - **Behaviour-definition fetch (conditional, never a halt).** Trigger: any hypothesis card whose `claim_class` is `environment_dependent`, or whose mechanism sentence asserts what a primitive (library call, config loader, scheduler, protocol, runtime builtin) *does*, when that behaviour has not been directly observed in this run. For each such card, append one row to `<output-dir>/behaviour-definitions.md` **before** issuing the fetch:
>
>   | # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
>   |---|---|---|---|---|---|
>
>   1. *Asserted behaviour*: the verb phrase copied verbatim from the card's mechanism sentence (e.g. "retries 3 times on 5xx", "later key wins", "returns empty at non-zero offset").
>   2. *Defining artifact*: the thing that makes that verb true — the function/method body that implements it, the spec or RFC clause, the schema rule, the doc section whose heading contains the verb. Never an example, sample output, format string, tutorial, or web-search summary.
>   3. *Fetch query*: built only from the words in column 3, phrased as "the code or clause that implements/specifies `<asserted behaviour>`". Adding words about output appearance or format is a violation.
>   4. Fetch verbatim: `mcp__context7__query-docs` → `WebFetch` → raw source via `gh api`. Paste the returned lines into `tier1-observation.md` under `## Behaviour definitions` with source coordinates; set Status `fetched:<source>`.
>   5. If the return is an example rather than a definition, or every fetch fails: Status `recalled, not load-bearing`; add a probe row that observes the asserted behaviour directly to `diagnosability-tasklist.md` `## Discriminator rows` (create the file if absent).
>   6. The hypothesis card's evidence section MUST reference its row (`behaviour-definition: row N`). Calibrator (C8) and the inline fallback assert the referenced row exists and Status is non-empty; a missing/empty row caps the card's confidence at 0.5 and logs `behaviour-cite: missing` in `audit.log`.

Note: step 4 names `gh api` in a mandatory step (design rule v2:155 forbids naming a tool in a mandatory step). The rescore (v2:645) claims "no `Open()`/`read.def` in mandatory text" but does not address `gh api`. FLAG minor; implementer may phrase as "raw source fetch (e.g. `gh api`)". Also `SKILL:340` "The MCP enrichment results" is where the behaviour-definitions rows reach agents — implied, not stated.

**Must NOT** (v2:419): substitute a web search summary for the file; make the fetch mandatory when the behaviour was observed in this run.

**Critique constraints**: X-01 — probe row goes to `diagnosability-tasklist.md` `## Discriminator rows`. X-08 — C8 (cap 0.5, "caps" not "floors"); calibrator input `behaviour_definitions_path`. AR-03 — create tasklist file if absent. FM-05 — all venues fail ⇒ `recalled, not load-bearing` + probe row. FM-06 — calibrator input paths.

**R-19 tests**: T18 `test_behaviour_definition_row.py`; T2 C8.

**Dependencies**: R-04 (step 1b calls this); R-14 (C8; `behaviour_definitions_path` input); R-07 ("Primitive under dispute, fetched verbatim" form field consumes the fetched text).

**Falsifiable claim** (v2:420): at Wave 3 of the sysbox run, mechanism "read at offset returns EOF" produces column 3 = "returns EOF at offset>0", column 4 = "the function that opens/reads the node".

### R-10 Headline-confidence coupling

**Layer**: skill (Wave 5 step 2) + ref (`refs/report-template.md` Diagnosis section) + agent (VAL A1, CAL C1 via R-14).

**Target files**: `SKILL` (:450 → insert after; :76 `root_cause_summary`); `refs/report-template.md` Diagnosis section.

**Anchors (repo)**:
- `SKILL:450` `   When \`diagnosability_hard_stop=true\`, replace the Diagnosis section with a "Halted — instrumentation required" prose block ...` [CODE-VERIFIED] — spec calls it "the last compose-step bullet"; it is actually the last indented paragraph of step 2, immediately before step 3 at :451. Position correct, description imprecise.
- `SKILL:76` `| \`root_cause_summary\` | string | ... Empty string when diagnosis is inconclusive. |` [CODE-VERIFIED].
- `SKILL:451` `3. **File:line validation pass (non-negotiable)** — spawn the \`evidence-validator\` agent ...` [CODE-VERIFIED] (boundary).

**Insert content (verbatim v2:429)**:

> **Weak model must**: if calibrated confidence < 0.5 (missing or non-numeric confidence counts as 0.0) OR the headline value fails the `grep -F` check against every artifact and every `job-*.log`, the Diagnosis section MUST begin `UNDETERMINED — among {<producers.md surviving rows>}` plus the falsifier sentences from `diagnosability-tasklist.md` `## Discriminator rows`; the word "probable" before an enum value is forbidden; `root_cause_summary` is the empty string (`SKILL:76`). Agent backstop: validator A1 (definite enum token in Summary/Diagnosis ∧ (max calibrated < 0.50 ∨ token in Grounding Gaps with `unobserved|deduced|pending` ∨ token fails `grep -F` against every artifact and `job-*.log`)) ⇒ `partial`/`blocked`; calibrator C1 ⇒ forced ESCALATE. Threshold 0.5 is pinned by the fixture interval (0.42, 0.72); the rubric's existing verdict cap may be reused if it falls inside (A-009).

Related UNDETERMINED variants defined elsewhere that this section must also render: `UNDETERMINED — among {a,b}` (R-04 step 3 `indistinguishable`); `UNDETERMINED — no comparator` (R-05 step 3); `UNDETERMINED — CI verdict unobserved` (A8, R-14).

**Must NOT** (v2:430): lower the escalation threshold; change the calibrator formula; add a confidence floor that blocks publishing.

**Critique constraints**: X-01 — falsifier sentences from `diagnosability-tasklist.md` `## Discriminator rows`. GB-05 — missing/non-numeric confidence ⇒ 0.0. Guard table: exactly 0.50 ⇒ definite allowed (A1 `< 0.50` agrees); 0.45 with token verbatim in artifact ⇒ UNDETERMINED forced (Risk 27 accepted). Rejected (v2:616) — A1 is a backstop, not the wave-where-caught.

**R-19 tests**: T11 `test_headline_threshold.py`; T1 A1; T2 C1; T15 GLM (A1 fires).

**Dependencies**: R-02 (`producers.md` surviving rows); R-04/R-06 (falsifier sentences); R-14 (A1, C1); R-01 (`job-*.log`); R-05 (`UNDETERMINED — no comparator`).

**Falsifiable claim** (v2:431): GLM retry-2 REPORT would read "UNDETERMINED — among {`:579`, `:581`, `:582-585`, `:718`}".

### R-11 Persist-on-receipt + cited-path check

**Layer**: skill (Wave 5 step 3).

**Target files**: `SKILL` (:451).

**Anchors (repo)**:
- `SKILL:451` `3. **File:line validation pass (non-negotiable)** — spawn the \`evidence-validator\` agent via \`Task\` with \`report_draft_path=<output-dir>/REPORT.md.draft\`, ... \`output_path=<output-dir>/evidence-validation.md\`, ... Apply its verdict: remove dropped citations from the final \`REPORT.md\`; if any were dropped, set the report's frontmatter \`status: partial\` and add a "Grounding Gaps" entry referencing them.` [CODE-VERIFIED].

**Insert content (verbatim v2:438)** — amend `SKILL:451`:

> "Write `evidence-validation.md` to disk *on receipt* (before touching REPORT.md.draft); persist `job-*.log` and `bracket.md` on receipt. The final REPORT.md may only cite `<output-dir>` paths that exist on disk at write time: run one `ls <all cited paths>` before REPORT.md and drop missing cites." Collapses to one `ls` + one Write, so it never trips R-12.

**Must NOT** (v2:440): add an agent; add a new upload step.

**Critique constraints**: X-01 / removed list — `bisect.md` → `bracket.md`. R-12 INV-012 — `ls`, `Write`, persist-on-receipt exempt from the cosmetic counter.

**R-19 tests**: none dedicated (v2 table has no test for R-11); T8 exempts persist calls. FLAG coverage gap.

**Dependencies**: R-01 (`job-*.log`); R-05 (`bracket.md`); R-12 (exemption).

### R-12 Cosmetic-loop counter — a nudge, not a gate

**Layer**: skill (Wave 5 step 3.5; Will Not list; Token Cost Profile note; audit-footer rule).

**Target files**: `SKILL` (:452 → insert 3.5 after; :532-545 Will Not; :582 cost profile; :358 marker verification; audit footer :455-465).

**Anchors (repo)**:
- `SKILL:452` `   - **Fallback**: if \`evidence-validator\` fails ... The inline path is the fallback — never ship without validation.` [CODE-VERIFIED] — step 3.5 after this, before `4. Append the machine-readable footer` at :453.
- `SKILL:532` `## Will Not Do` [CODE-VERIFIED]; :545 last bullet.
- `SKILL:582` `These are targets, not hard caps. Auggie tokens are offloaded ...` [CODE-VERIFIED] — keep, add cosmetic-counter sentence.
- `SKILL:358` `Verification command (run before publishing): for each \`tier2-*-hypothesis.md\` ... assert a matching \`*-calibration.md\` exists and contains the Calibration Report markers ...` [CODE-VERIFIED] — "a single command run once".
- Greenfield: `cosmetic_overrun` 0 hits.

**Insert content (verbatim v2:447-448)**:

Cost profile note (`:582`): keep "targets, not hard caps" and add "the cosmetic counter is the one hard cap; overrun is audit-logged as `cosmetic_overrun=<n>` and the run continues".

> **Open question 4 answer**: a counter with a forced *action*, never a halt *(reconciled per debate X-004: threshold 5; V2's ≥3 fires on legitimate marker check + two writes; V3's 12 "lets the $4.93 pass run to completion")*. After **5** consecutive `Read`/`Glob` calls on `<output-dir>/` with no Read/Bash on a source file or downloaded artifact, the orchestrator must do exactly one of: (a) finalize REPORT.md as-is with `status: partial` and stop; (b) issue one Read/Bash on source or artifact. `ls`, `Write`, and persist-on-receipt calls are exempt (INV-012). Exempt reads inside `<output-dir>`: `job-*.log`, `*.stream.jsonl`, `<output-dir>/artifacts/**`, and any file whose content is written into a probe row (GB-02). The counter resets only on a source/artifact Read; if the forced action is not taken it re-fires at every multiple of 5 with `cosmetic_overrun=<n>` (GB-01). Marker verification (`SKILL:358`) is a single command run once; a second marker grep in the same wave is a counter hit. Calibration reports are consumed from disk, never re-typed. Errored `AskUserQuestion` result ⇒ `remediation_accepted=false`, no inference.

**Must NOT** (v2:450): ask the user; count reads of the failing artifact as cosmetic; add a token cap that stops diagnosis mid-wave.

**Critique constraints**: GB-01 — re-fires at every multiple of 5; resets only on source/artifact Read. GB-02 — exempt set. Guard table rows (0, 1, 5, 12, sentinel, `ls`+Write). Rejected (v2:602) — no halting cap; ≥3 and 6/12 dropped.

**R-19 tests**: T8 `test_cosmetic_counter.py`.

**Dependencies**: R-11 (persist exempt); R-16 (errored `AskUserQuestion` ⇒ `remediation_accepted=false` feeds `blocked-on-authorization`); R-01 (`job-*.log` exempt).

**Falsifiable claim** (v2:451): GLM correction pass hits the counter at tool 9 (five marker greps).

### R-13 Provenance timestamps from command output only

**Layer**: skill (Will Not list) + ref (`refs/report-template.md` Rendering rules) + agents (VAL A3, CAL C5 via R-14; `card_mtime` input).

**Target files**: `SKILL` (:545); `refs/report-template.md` (:255-260); `CAL` (:47-51 inputs, via R-14).

**Anchors (repo)**:
- `SKILL:545` `- Allow the diagnosability tasklist to target the failing component's own source code — every task MUST target an invocation site ... Diagnostic code in production source leaks into release artifacts.` [CODE-VERIFIED] — last Will-Not bullet; spec says "append to" it. FLAG: appending a timestamp rule to a bullet about source targeting is semantically odd; a new sibling bullet is the cleaner reading (integration researcher to decide).
- `refs/report-template.md:255` `## Rendering rules` and :257-260 four bullets [CODE-VERIFIED].
- `CAL:47-51` Inputs list (`card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path`) [CODE-VERIFIED].

**Insert content (verbatim v2:460)**:

> **Weak model must**: copy every timestamp written into any artifact from a `date -u +%Y-%m-%dT%H:%M:%SZ` Bash result in the same turn or from `git log --format=%cI`; no other source. Agent check *(reconciled per debate X-012: ±5 min; V3's +60 s buys no recall)*: any `Timestamp|Date|pushed_at` > artifact mtime **+5 min** or matching `T00:00:00Z` ⇒ drop that line, reason `timestamp_invalid`; calibrator uses the orchestrator-supplied `card_mtime` input (`CAL:47-51`). Observed offsets 43 min / ~5.5 h / 29 min.

**Must NOT** (v2:461): add a new agent; add Bash to the calibrator.

**Critique constraints**: Rejected (v2:611) — A3/C5 on existing agents, not a new validator agent. Rejected (v2:617) — +60 s tolerance dropped for clock-skew.

**R-19 tests**: T12 `test_timestamp_tolerance.py` (+4m59s pass, +5m01s fail, `T00:00:00Z` always fails); T1 A3; T2 C5; T15 GLM (A3 fires).

**Dependencies**: R-14 (A3, C5, `card_mtime`, `artifact_mtimes`).

### R-14 Agent assertion sets (calibrator C1-C8, validator A1-A10)

**Layer**: agents (`CAL`, `VAL`) + skill inline-fallback parity (design rule: "the orchestrator's inline fallback runs the identical assertion list").

**Target files**: `src/superclaude/agents/confidence-calibrator.md` (:47-51 inputs; :62 step 5a → add 5b; :88-96 Stage-2 trace; :111-115 Notes); `src/superclaude/agents/evidence-validator.md` (:41-44 inputs; :51-58 responsibilities → add 2b; :63-97 output format → add `## Structural assertions` table).

**Anchors (repo)**:
- `CAL:5` `tools: Read` [CODE-VERIFIED] — no Bash.
- `CAL:47-51` inputs `card_path`, `rubric_path`, `card_tier`, `flags_context`, `output_path` [CODE-VERIFIED] — add `card_mtime`, `behaviour_definitions_path`, `tasklist_path`.
- `CAL:62` `5a. **Apply the verdict-direction modifier** per the rubric: ... Record whether the cap was binding in the Stage-2 trace.` [CODE-VERIFIED] — step 5b after.
- `CAL:88-96` Stage-2 trace table (rows `arithmetic_mean(all_six)` ... `spot_check_unverifiable`) [CODE-VERIFIED] — add `structural_flags` row.
- `CAL:111-115` `## Notes` three bullets [CODE-VERIFIED].
- `CAL:127-134` `**Will Not:**` list incl. `Re-write the card` [CODE-VERIFIED] — unchanged.
- `VAL:41-44` inputs `report_draft_path`, `evidence_section_locator`, `output_path`, `allow_command_reexec` [CODE-VERIFIED] — add `calibration_paths: list`, `diff_path: str|null`, `artifact_mtimes: dict`, `producers_path`, `tasklist_path`.
- `VAL:51-55` responsibility 2 `**For each \`file:line\` citation**` [CODE-CONTRADICTED: spec says `VAL:51-58`; responsibility 2 is :51-55 and responsibility 3 (command citations) is :56-58. Insert 2b between :55 and :56.]
- `VAL:58` `... The current toolset deliberately excludes Bash for v1, so this branch is unreachable until a future revision adds Bash.` [CODE-VERIFIED].
- `VAL:63-97` Output Format fence [CODE-VERIFIED].
- `RUB:20` `**Confidence** = \`min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)\`.` [CODE-VERIFIED] — unchanged.
- Note: rubric dimension names are `Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence` (`CAL:55`). R-14 C6 uses "evidence quality ≤0.3" — no such dimension exists. FLAG: read as "Evidence grounding ≤0.3"? But scores are 0.0/0.5/1.0 (`CAL:60`); "≤0.3" and "≤0.5" caps on dimensions imply either a new scoring granularity or a post-formula cap. Implementer must decide: cap the dimension to 0.0 (nearest legal value ≤0.3) or cap calibrated output.

**Insert content — Change (verbatim v2:467)**:

> `CAL:62` after step 5a as step 5b; Notes `CAL:111-115`; Stage-2 trace `CAL:88-96` gains a `structural_flags` row; new inputs `card_mtime`, `behaviour_definitions_path`, `tasklist_path` at `CAL:47-51`. `VAL:51-58` gains responsibility 2b "structural assertions" after citation verification; output `VAL:63-97` gains a `## Structural assertions` table; inputs `VAL:41-44` gain `calibration_paths: list`, `diff_path: str|null`, `artifact_mtimes: dict`, `producers_path`, `tasklist_path`.

**Insert content — Calibrator (verbatim v2:468)**:

> C1 (AP-09) headline enum token ∧ calibrated < 0.50 → `headline_definite_low_confidence`, verdict forced ESCALATE. C2 (AP-05) card excludes an enum without a `file:line` for that enum's exit statement → Runtime check := 0.0, `unproven_exclusion:<token>`. C3 (AP-21) control arm cited without `CONTROL-PROOF: yes` → Symptom coverage ≤0.5, `control_unproven`; C3b `runs-in=unknown` → Runtime check ≤0.5, `locus_unknown`. C4 (AP-11) instrumentation without falsifier → Fix directness ≤0.5, `no_prereg_falsifier`. C5 (AP-10) `Timestamp` > `card_mtime` + 5 min or `T00:00:00Z` → `timestamp_invalid`. C6 a numeric threshold or bracket asserted in the headline without a `bracket=` line in `bracket.md` ⇒ evidence quality ≤0.3. C7 card names an environment property without citing a 2×2 row ⇒ cap 0.5, `uncited`. C8 `behaviour-definition: row N` missing or row Status empty ⇒ cap 0.5, `behaviour-cite: missing`.

**Insert content — Validator (verbatim v2:469)**:

> A1 (AP-01/09) as in R-10 → `partial`, `deduced_headline`. A2 (AP-11) `diff_path` touches a collector/invocation site ∧ no falsifier sentence naming a row → `partial`, `instrumentation_without_falsifier`. A3 (AP-10) timestamp rule → drop line, `timestamp_invalid`. A4 (AP-20) `pipeline_hardening_verdict` ∉ `{pass, blocked, advisory, not_applicable, blocked-on-authorization}` → `partial`, `verdict_not_in_contract`. A5 (AP-06) `candidate-fixes.md` `consensus` ∧ `adversarial_invoked: false` ∧ any card `evidence_class ∈ {source_static, doc_static, none}` with dynamic claim_class → `partial`, `consensus_on_unobserved`. A6 `Reference-context value` not a single literal (matches `if|only|/|,`) → FAIL. A7 `RUN-SITE = pending-producers` at finalize **while `producers.md` has ≥1 producer row** → FAIL. A8 no `job-*.log` for the failing arm at finalize when `OBSERVE-VIA = artifact-file` → `status=blocked`, `UNDETERMINED — CI verdict unobserved`. A9 `Reference-context value` ≠ observed reference value → probe row `suspect`, Grounding Gap, outcome table skipped. A10 `capability-verdict: blocked` without an `## Emitter search` block recording `emitters-found: 0` and `already-read-files: 0` → `partial`, `capability_block_unproven`.

Gaps for the implementer: (a) A6/A7 say "FAIL" with no named flag — every other A-rule names a flag; T1 needs a flag name per assertion (suggest `reference_value_not_literal`, `run_site_unresolved`). (b) A9's output is "probe row suspect", not a report status — the `## Structural assertions` table needs a column that can express a non-status outcome. (c) VAL inputs lack `locus_path` (for A7/A8 `RUN-SITE`/`OBSERVE-VIA`) and `job_log_glob`; the validator cannot read `execution-locus.md` unless given its path — v2 lists only `producers_path`, `tasklist_path`. FLAG. (d) VAL has `Read, Grep, Glob` (`VAL:5`) so it can Glob `job-*.log` if told the output dir; CAL has `Read` only, so `tasklist_path`/`behaviour_definitions_path` must be absolute paths.

**Must NOT** (v2:470): add Bash to either agent (`CAL:5`, `VAL:58`); rewrite the card (`CAL:127-134` unchanged); change the formula at `RUB:20`.

**Critique constraints**: X-05 (A10), X-07 (A9 not A7), X-08 (C7, C8, inputs), X-09 (C6 reworded to `bracket=`), AD-03 (C3b), AD-04 (A7 scoped), FM-06 (inputs), X-04 (`control_unproven`).

**R-19 tests**: T1 `test_validator_assertions.py` (40 cases); T2 `test_calibrator_assertions.py` (36 cases); T13 parity; T14 (existing fixtures unchanged); T15 (GLM: {A1,A3,A4,A5,C2,C3} fire; Fable: none, 0.72 kept).

Internal inconsistency: T2 says "C1-C8 (incl. C3b) ... (36 cases)" = 9 rules × 2 domains × 2 polarities = 36 — consistent. T1 "A1-A10 ... (40 cases)" = 10 × 4 = 40 — consistent. TS-01 table said "C1-C8 (32 cases)"; v2 corrected to 36 by counting C3b. OK.

**Dependencies**: every R-item that names an A/C rule: R-01 (A7, A8, C3, C3b), R-03 (A10), R-06 (A2, C4), R-07 (A6, A9), R-09 (C8), R-10 (A1, C1), R-13 (A3, C5), R-05 (C6, C7), R-16 (A4 enum), R-02 (C2 exclusion lines).

### R-15 Triage cause-class row + evidence-or-drop bullet + complexity signal

**Layer**: refs (`refs/triage-checklist.md`, `refs/diagnosability-audit.md`).

**Target files**: `refs/triage-checklist.md` (:33, :42, :63); `refs/diagnosability-audit.md` (:176).

**Anchors (repo)**:
- `refs/triage-checklist.md:33` `| **Build / packaging** | Module not found at runtime, version mismatch, install step missing |` [CODE-VERIFIED] — insert new row after (before `| **Other** |` at :34).
- `refs/triage-checklist.md:42` `- A pointer to the failing test and the exact assertion that fires` [CODE-VERIFIED] — last evidence-or-drop bullet; add after.
- `refs/triage-checklist.md:63` `- The user's description is ambiguous in a way that a single hypothesis would have to guess at the actual symptom` [CODE-VERIFIED] — last refuse-Tier-1 bullet; add after.
- `refs/diagnosability-audit.md:176` `| Cause class from Wave 1 triage ∈ {Race/concurrency, Stale state/cache, Performance/resource} | Wave 1 checklist scan | +1 |` [CODE-VERIFIED] — replace.

**Insert content (verbatim v2:480-502)**:

`refs/triage-checklist.md`, insert after line 33 (the `Build / packaging` row):

```
| **Substituted primitive** | Same code + same input differs by environment; the differing call is to something the code does not implement (fs, clock, network, DB engine, mocked/polyfilled/vendored API); repro flips by swapping the provider, not the code. Not env drift: no config value differs, and the stack trace (if any) ends in your code, not the provider's |
```

evidence-or-drop check, add after line 42:

```
- The diagnostic output must be *read from the system*, not supplied by the harness: a mock, fixture, or assertion that returns the expected value is not evidence (S14, R-03)
```

refuse-Tier-1 list, add after line 63:

```
- The symptom is environment-dependent and only one of the environments is reachable, so no A/B probe is possible
```

`refs/diagnosability-audit.md`, signal table, replace line 176:

```
| Cause class from Wave 1 triage ∈ {Race/concurrency, Stale state/cache, Performance/resource, Substituted primitive} | Wave 1 checklist scan | +1 |
```

Note: the evidence-or-drop bullet carries "(S14, R-03)" — an R-number in shipped ref text is a spec artefact; the implementer should cite the ref section (`refs/diagnosability-audit.md` S14 / Section 7 constraint 5) instead. Also the refuse-Tier-1 bullet ("only one environment reachable ⇒ refuse") sits in tension with R-05 step 3 / FM-03 ("single environment ⇒ `comparator=none`, `UNDETERMINED — no comparator`, proceed") — one says refuse Tier 1, the other says proceed with UNDETERMINED. FLAG: refusal is "recommend `--depth deep`", not a halt (triage-checklist:58), so it is compatible, but wording should say so.

**Must NOT**: none listed in v2 for R-15.

**Critique constraints**: none directly; design rule (no OS/runtime names — row phrased by property; rescore v2:651 "no sysbox/gVisor/LXC names").

**R-19 tests**: none dedicated. T16's `substituted primitive` outcome references the cause class name. FLAG coverage gap (a content-assertion test in the existing `test_hardening_*` style would fit).

**Dependencies**: R-05 step 3 (cause class `substituted primitive`); R-03 (S14).

**Observed failure prevented** (v2:504): substrate never named as a cause class (AP-04); harness-echoed value accepted as evidence.

### R-16 Contract verdict enum + `blocked-on-authorization`

**Layer**: ref (`refs/hardening-output-contract.md`) + agent (VAL A4 via R-14) + (unlisted but required) every other four-token enum site.

**Target files**: `refs/hardening-output-contract.md` (:5, :15, :68). NOT listed by v2 but carry the same enum literal today and will drift if untouched: `SKILL:64`, `SKILL:420`, `SKILL:444`; `refs/report-template.md:223`, `:315`; `refs/pipeline-hardening-closure.md:13`; `refs/remediation-handoff.md:11`, `:35`, `:69`; existing tests `tests/troubleshoot/test_hardening_output_contract.py:93-94` and `tests/troubleshoot/test_hardening_verdict.py:51` assert the four-token string literally.

**Anchors (repo)**:
- `hardening-output-contract.md:5` `\`pipeline_hardening_verdict\` is the **four-token** enum \`pass | blocked | advisory | not_applicable\`. \`advisory\` is a first-class outcome and MUST NOT be removed ... Any artifact that drops \`advisory\` or uses a three-token enum is a defect.` [CODE-VERIFIED] — "four-token" must become five-token.
- `hardening-output-contract.md:15` `| \`pipeline_hardening_verdict\` | enum \`pass\|blocked\|advisory\|not_applicable\` | yes when applicable known | \`not_applicable\` | ...` [CODE-VERIFIED].
- `hardening-output-contract.md:68` `- **One-way latch (\`waiver_status\`).** ... Once \`latched\`, \`pipeline_hardening_verdict ∈ {blocked, advisory}\` ...` [CODE-VERIFIED].
- `SKILL:43` `| \`status\` | string | \`success\`, \`partial\` (some findings dropped for grounding), \`failed\` |` [CODE-VERIFIED] — `blocked` is NOT in the `status` enum today; R-16 says "status `blocked`, never `partial`". See R-03 flag.

**Insert content — Rule (verbatim v2:511)**:

> enum `pass | blocked | advisory | not_applicable | blocked-on-authorization`. `blocked-on-authorization` is valid only when an emitter row exists in the tasklist AND the re-run was refused (`re-run permitted: no`, or errored `AskUserQuestion` ⇒ `remediation_accepted=false`); status `blocked`, never `partial`; the tasklist file is still written. `capability-verdict: blocked` (R-03) is a tasklist header value, not a contract enum value. Any other contract string (e.g. `blocked_pending_retry_run`, `G/REPORT-RUN2.md:63`) fails A4.

Internal inconsistency: `blocked-on-authorization` is placed on `pipeline_hardening_verdict` — a Wave 4.5 hardening enum — but the condition (emitter row + refused re-run) is a Wave 1.6 diagnosability outcome. On a run where `pipeline_hardening_applicable=false` the verdict is `not_applicable` by truth-table row 1 (`hardening-output-contract.md:33`), and the §5.4 table has no row producing `blocked-on-authorization`. FLAG: implementer must add a truth-table row (or state precedence vs row 1) or the value is unreachable. Q6 says it "is the only new verdict".

**Must NOT** (v2:512): read authorization files; block any wave on an external authorization artifact.

**Critique constraints**: X-05 — `re-run permitted` everywhere (not `push-allowed`); `capability-verdict` is a tasklist header field; A4 enumerates contract enum only. R-12 — errored `AskUserQuestion` ⇒ `remediation_accepted=false`. AP-22 / Rejected (v2:599) — no authorization artifact gate.

**R-19 tests**: T10 (`blocked-on-authorization`, status `blocked`, tasklist written); T1 A4; T15 GLM (A4 fires on `blocked_pending_retry_run`). Existing `test_hardening_output_contract.py` / `test_hardening_verdict.py` will need their literal-string assertions updated.

**Dependencies**: R-03 (precedence text at SKILL:241 emits this value); R-14 (A4); R-12 (`AskUserQuestion` rule); `status` enum extension (no owner — see R-03 flag).

### R-17 Protocol-side `HC0-HC5` rename

**Layer**: skill + refs (mechanical rename) + test (regression guard grep).

**Target files**: `SKILL` (:104, :410-420, :595-600 named; plus :63, :68-71, :408, :444 which also carry `H0`-`H5` labels); all refs with `\bH[0-5]\b` hits. Output-contract *field names* unchanged (`SKILL:62`).

**Anchors (repo)** — `grep -cE '\bH[0-5]\b'` on 2026-09-19:
- `SKILL.md`: 23 hits at lines 63, 64, 67-71, 104, 408, 410, 414-420, 444, 595, 597-600 [CODE-VERIFIED].
- `refs/hardening-output-contract.md`: 20; `refs/pipeline-hardening-closure.md`: 19; `refs/report-template.md`: 7; `refs/unmask-and-sweep.md`: 7; `refs/runtime-entrypoint-verification.md`: 6; `refs/contract-enumeration.md`: 5; `refs/effective-input-proof.md`: 4; `refs/calibrator-eval-cases.md`: 2; `refs/escalation-rubric.md`: 1 [CODE-VERIFIED].
- agents + `commands/troubleshoot.md`: 0 hits [CODE-VERIFIED].
- `SKILL:104` `Wave 4.5: Pipeline Hardening Closure ← conditional, when pipeline_hardening_applicable=true (issue topology); runs gates H0-H5; loads the 6 hardening refs` [CODE-VERIFIED].
- `SKILL:414-419` `1. **H0 — Applicability + mechanism**` ... `6. **H5 — Off-path reviewer rule**` [CODE-VERIFIED].
- Existing tests reference H-labels in docstrings/messages: `tests/troubleshoot/test_hardening_h0.py` ... `test_hardening_h4.py`, `test_hardening_verdict.py:33` ("H5 mapping") — grep shows these are prose, but any content assertion on the literal `H0`..`H5` will break. FLAG: run the existing suite after the rename.

**Insert content (verbatim v2:518)**:

> **Change**: `SKILL:104`, `:410-420`, `:595-600`; refs; output-contract field names unchanged (`SKILL:62`) *(reconciled per debate X-008: "a rename the skill cannot enforce is not a rule")*. Regression guard: `grep -E '\bH[0-5]\b'` across skill and refs must return 0 hits outside contract field names.

Scope ambiguity: "outside contract field names" — no contract field NAME contains `H0`-`H5` (names are `pipeline_hardening_*`, `runtime_entrypoint_card_path`, etc.); only field DESCRIPTIONS at `SKILL:63,68-71` do. So the guard effectively requires 0 hits everywhere, including the Output Contract description cells. FLAG: confirm whether `SKILL:63-71` description text is renamed (recommended: yes, guard is then a clean `== 0`).

**Must NOT**: rename output-contract field names; (Rejected v2:614) rename hypotheses in briefs to `LH-1`.

**Critique constraints**: X-008 (debate) — protocol-side rename only.

**R-19 tests**: none in the T-table. The regression guard grep is the test; suggest a one-assert `test_hc_rename_guard.py` in the existing content-assertion style. FLAG coverage gap.

**Dependencies**: none (mechanical); must land AFTER R-16's enum edits or the two diffs collide in `hardening-output-contract.md` and `SKILL:64/420/444`.

**Observed failure prevented** (v2:519): label collision, `O/PROTOCOL-CORRECTION.txt:15`.

### R-18 Command-file surface

**Layer**: command (`src/superclaude/commands/troubleshoot.md`).

**Target files**: `CMD` (:69, :103). `CMD:8` unchanged — no new flag.

**Anchors (repo)**:
- `CMD:8` `argument-hint: "[<issue description>] [--type ...] ... [--caller <name>]"` [CODE-VERIFIED] — unchanged.
- `CMD:69` `4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, (if \`--fix\`) the Tier 3 remediation offer, and (if \`pipeline_hardening_applicable\`) the Pipeline Hardening Closure verdict + evidence-card paths, and (if \`caller=task-unified\`) the emitted \`return-contract.yaml\` path.` [CODE-VERIFIED] — replaced wholesale.
- `CMD:103` `- **\`Bash\`**: cheap reproducer commands (Tier 1) and diagnostic commands (Tier 2)` [CODE-VERIFIED] — replaced wholesale.

**Insert content (verbatim v2:528-538)**:

`CMD:69` becomes:

```
4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, (if `--fix`) the Tier 3 remediation offer, (if `pipeline_hardening_applicable`) the Pipeline Hardening Closure verdict + evidence-card paths, (if `caller=task-unified`) the emitted `return-contract.yaml` path, and any grounding artifacts the skill lists in its Output Contract — at minimum the execution-locus card (where the code ran vs where the symptom appeared), the discriminator rows in the diagnosability tasklist when produced (with whether they were executed or handed off), and the verdict source used.
```

`CMD:103` becomes:

```
- **`Bash`**: cheap reproducer commands (Tier 1), diagnostic commands (Tier 2), and read-only probes at the code-site as designed by the skill
```

**Must NOT** (v2:540): restate cell counts, probe IDs, filenames, or trigger clauses in the command file — those live only in the skill's Output Contract and refs.

**Critique constraints**: AR-04 — "the discriminator rows in the diagnosability tasklist (executed or handed off)" not "discriminator plan". X-02 — "the verdict source used" depends on R-01's re-attached rule.

**R-19 tests**: none. FLAG coverage gap (a content assertion that `CMD` contains "execution-locus card" and "verdict source" would suffice).

**Dependencies**: R-01 (locus card + verdict source exist in Output Contract as `execution_locus_card_path`); R-04 (discriminator rows). Note "the verdict source used" has no Output Contract field in any R-item — R-01 adds only `execution_locus_card_path`. FLAG: either the locus card carries the verdict-source line (it does, per the R-01 rule) or a field is missing; command wording is satisfiable via the card.

**Falsifiable claim** (v2:541): a user reading `CMD:69` learns a locus card and discriminator rows exist before running.

### R-19 Acceptance tests (19 generic + 1 regression)

**Layer**: test.

**Target files**: new `tests/troubleshoot/test_*.py` (20 files) + `tests/troubleshoot/fixtures/**` (new dir; does not exist today [CODE-VERIFIED: `ls tests/troubleshoot/fixtures` → No such file]). Existing `tests/troubleshoot/` contains `test_hardening_h0..h4.py`, `test_hardening_output_contract.py`, `test_hardening_verdict.py`, `backtest/`, `e2e-backtest-scenarios.md` — all content-assertion tests over the refs (pattern for the "tests" researcher).

**Anchors (repo)**:
- `refs/calibrator-eval-cases.md:81` `Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: \`tests/troubleshoot/test_calibrator_eval_cases.py\`.` [CODE-VERIFIED] — T14's home; file does not exist yet.

**Preamble (verbatim v2:547)**:

> Landing path `tests/troubleshoot/` (`refs/calibrator-eval-cases.md:81`). No LLM in CI. Every test runs both the agent-path assertion list and the inline fallback and compares flag sets (parity is a fixture-wide assertion, not a separate test). Regression fixtures are byte copies vendored under `tests/troubleshoot/fixtures/regression/sysbox-20260918/` with sha256 recorded in `MANIFEST`.

**Fixture layout (verbatim v2:551-565)**:

```
tests/troubleshoot/fixtures/
  assertions/<A1..A10|C1..C8>/{io,nonio}/{pos,neg}.md
  procedures/producers/{io.sh,nonio.py}
  procedures/primitivegrep/sink.sh
  procedures/locus/{complete,missing-run-site,one-env,two-env,no-env}.md
  procedures/verdict-source/{marker,no-marker,conclusion-only}.log
  procedures/discriminator/{io,nonio}.md
  procedures/rows/{distinguishing,indistinguishable,exact-only,overflow}.md
  procedures/differential/table.md
  procedures/behaviour/{fetched,recalled,missing}.md
  procedures/tasklist/{authorized,refused,no-emitter-no-file,source-only-read}.md
  counters/cosmetic-log.txt
  regression/sysbox-20260918/{GLM-RUN2,Fable-D3,Astra-A3}/ + MANIFEST (sha256)
```

**Full test table (verbatim v2:567-588)**:

| id | test | proves | fixture | kind |
|---|---|---|---|---|
| T1 | `test_validator_assertions.py` | A1-A10: pos fires with the named flag, neg does not; parametrized over assertion × domain × polarity (40 cases); A7 neg includes "sentinel with empty producers.md" | `assertions/A*/` | generic |
| T2 | `test_calibrator_assertions.py` | C1-C8 (incl. C3b) likewise, plus forced ESCALATE on C1, Runtime check := 0.0 on C2, caps on C7/C8 (36 cases) | `assertions/C*/` | generic |
| T3 | `test_producers_enumeration.py` | `producers.md` always created with `observation-kind`; 7 columns; row count == grep hit count over `## Producers` only; computed enum ⇒ `producer-count=unknown`; zero-surviving ⇒ `re-opened`; `## Mechanism rows` excluded from count | `procedures/producers/{io.sh,nonio.py}` | generic |
| T4 | `test_primitivegrep_targeting.py` | hits only from producer files; one pattern per table row; `/dev/null`, `2>/dev/null` excluded; ≤ 8 rows; `RUN-SITE` sentinel overwritten | `procedures/primitivegrep/sink.sh` | generic |
| T5 | `test_locus_card.py` | four lines + `CONTROL-PROOF` per passing arm required; missing line ⇒ Wave 1 exit FAIL; `SAME-ENV` derives `yes`/`no`/`unknown` on one-env / two-env / no-env texts; `runs-in=` absent ⇒ card returned | `procedures/locus/*` | generic |
| T5b | `test_verdict_source.py` | marker line ⇒ verdict from last marker; no marker ⇒ `unobservable`=FAIL; conclusion-only log never yields PASS | `procedures/verdict-source/*` | generic |
| T6 | `test_discriminator_form.py` | filled form parses (io and nonio); exactly one outcome row matches a truth vector; A/B verdict follows; A9 marks probe suspect on reference mismatch | `procedures/discriminator/{io,nonio}.md` | generic |
| T7 | `test_threshold_bracket.py` | trigger on "limit named in text" and "passes at smaller value"; for any monotone yes/no vector, guard == highest pass, width == 2; non-monotone ⇒ `UNDETERMINED`; bracket rounds do not increment `diagnosability-rounds.json` | inline integer table | generic |
| T8 | `test_cosmetic_counter.py` | 5 consecutive output-dir Read/Glob ⇒ forced action + `cosmetic_overrun=5`; re-fires at 10; `ls`/`Write`/persist/`job-*.log` exempt; source Read resets | `counters/cosmetic-log.txt` | generic |
| T9 | `test_counter_key.py` | same `<branch>:<repro-venue-id>` persists across slugs; only `discriminator-required=yes` tasklists increment; at round 3 the tasklist is still written and status is `blocked` | two synthetic runs | generic |
| T10 | `test_hardstop_verdicts.py` | emitter row + `re-run permitted: no` ⇒ `blocked-on-authorization`, status `blocked`, tasklist written; emitter row + permitted ⇒ tasklist row required, `capability-verdict: blocked` FAILS A10; N=0 + already-read log ⇒ append row; N=0 + only source files read ⇒ `capability-verdict: blocked` valid, no source edit | `procedures/tasklist/*` | generic |
| T11 | `test_headline_threshold.py` | threshold in (max neg calibrated, min pos calibrated) over T1/T2 fixtures; missing confidence ⇒ `UNDETERMINED` | derived | generic |
| T12 | `test_timestamp_tolerance.py` | mtime+4m59s passes, +5m01s fails, `T00:00:00Z` always fails | synthetic | generic |
| T13 | `test_inline_fallback_parity.py` | agent flag set == inline flag set on every fixture in T1-T12, T16-T19 | all | generic |
| T14 | `test_calibrator_eval_cases.py` | fixtures 1-9 and P1-P5 unchanged | existing ref | generic |
| T16 | `test_primitive_differential.py` | 2×2 truth table: exact≠ref failing ∧ equal passing ⇒ `substituted primitive`; any cell unobserved or single env ⇒ `comparator=none`, cap 0.4 | `procedures/differential/table.md` | generic |
| T17 | `test_discriminator_rows.py` | pair completeness (exact-only ⇒ invalid); distinguishing pair present or `indistinguishable` header after ≤2 added rows; control row present; ≤8 pairs with `probe-rows-truncated`; `verdict` forced from `sufficient\|unknown` to `partial` | `procedures/rows/*` | generic |
| T18 | `test_behaviour_definition_row.py` | row written before fetch; query built from column 3 words only; `recalled` ⇒ probe row appended to tasklist; missing row ⇒ C8 cap 0.5 | `procedures/behaviour/*` | generic |
| T19 | `test_menu_equality.py` | prompt enum count == `surviving=yes` rows; mismatch ⇒ FAIL | derived from T3 | generic |
| T15 | `test_regression_sysbox.py[GLM-RUN2\|Fable-D3\|Astra-A3]` | GLM: {A1,A3,A4,A5,C2,C3} fire; Fable: none fire, 0.72 kept; Astra: T10 emitter rule fires, cards lacking `runs-in=` returned at Wave 1.7, A7 does not fire | `regression/sysbox-20260918/` | regression |

**Coverage rule (verbatim v2:590)**:

> **Coverage rule (one line):** every assertion or procedure id under test has ≥1 `pos` and ≥1 `neg` fixture in both `io/` and `nonio/`, and appears in `regression/` at most as an expected-flag entry — never as the only fixture.

**Dropped from v1 (verbatim v2:592)**:

> Dropped from the v1 22: test 17 (rule (b) relative-path trigger — rule replaced by the generic threshold trigger, T7); tests 13/15/19's literal `startup.sh` line cites (absorbed into T3/T4 invariants and T15's expected-flag table); test 18's `N=82/85` (absorbed into T7's table as one row); test 10's 7-cell assertion (T5).

**Internal inconsistencies / gaps in the test plan**:
1. Heading says "19 generic + 1 regression" and the table has 20 rows (T1-T14, T16-T19 = 18 rows + T5b = 19 generic; T15 regression) — consistent.
2. Fixture layout `assertions/<A1..A10|C1..C8>/{io,nonio}/{pos,neg}.md` = 4 files per rule; T1 40 cases = 10 × 4; T2 36 cases needs C3b as a separate dir (`C3b/`) — the layout glob `C1..C8` does not include `C3b`. FLAG.
3. T14 "fixtures 1-9 and P1-P5 unchanged" — `refs/calibrator-eval-cases.md` says P1-P4 are hard properties and P5 is warning (line 77); fixtures 1-9 exist in that ref (verify with the tests researcher).
4. The tests must be LLM-free ("No LLM in CI"), yet T3/T4/T5/T10/T17 exercise procedures a model performs (grep, classify, write). The only executable path is a Python re-implementation of each procedure under `tests/troubleshoot/` (or `src/superclaude/`) — v2 never names where that code lives. FLAG: this is the single largest unstated implementation dependency in R-19 (a procedural library for producers/locus/rows/counter/timestamp parsing + the A1-A10/C1-C8 assertion functions). The "inline fallback" that T13 compares against IS that library.
5. Regression fixtures are "byte copies vendored" from `D`/`G`/`A3` paths (v2:25-27) that live on other machines (Fable/GLM/Astra `.dev/troubleshoot/`); the task builder must confirm source availability (`Z` = `/tmp/sysbox-pr170-retry3-public-evidence.zip`, likely gone).
6. Items with NO test row: R-08 step 4.5 / `split-pending`; R-11; R-15; R-17; R-18.

**Dependencies**: all R-01..R-18 (tests assert their outputs). Must land last, but the parity library (item 4) must exist before T13.

---

## 2. Transferability rescore (revision 2) — verbatim v2:635-657

Old scores are the caller's per v1 id, mapped to the v2 id via the renumbering table. Weight = approximate line volume of the v2 item.

| v2 | v1 | Item | Old | New | Weight | Justification |
|---|---|---|---|---|---|---|
| R-01 | R-01 | Locus card | 0.60 | 0.85 | 30 | Four generic questions; verdict-source rule generic with the `gh` pair demoted to example; `RESULT:` marker still incident-flavoured in the example only |
| R-02 | R-03 | Producers | 0.80 | 0.85 | 18 | Field renames; primitive grep is one pattern per kind row instead of a `/proc` regex; `df00c06` cites remain as expected-value notes |
| R-03 | R-04 | Emitter search | 0.50 | 0.90 | 22 | Harness-neutral S14; procedure generic; `6ced457` only in the claim |
| R-04 | R-05 | Discriminator rows | 0.70 | 0.90 | 22 | No wave; kind classification + copy; incident rows only in the claim |
| R-05 | R-02 | Primitive differential | 0.05 | 0.85 | 30 | Six-kind table with no OS/runtime names; sysbox tells confined to an optional pack; bracketing trigger generic |
| R-06 | R-12 | Falsifier columns | 1.00 | 1.00 | 8 | Unchanged |
| R-07 | R-06 | Discriminator form | 0.75 | 0.95 | 30 | Field names domain-neutral; non-I/O worked example added |
| R-08 | R-07 | Split experiment | 0.80 | 0.85 | 12 | Archetype is now a table row; collector cite is the incident instance |
| R-09 | R-08 | Behaviour fetch | 0.60 | 0.95 | 16 | Verb-phrase worksheet; no `Open()`/`read.def` in mandatory text |
| R-10 | R-09 | Headline coupling | 1.00 | 1.00 | 8 | Unchanged |
| R-11 | R-14 | Persist-on-receipt | 0.90 | 0.90 | 6 | Unchanged; `job-*.log` name is a convention |
| R-12 | R-10 | Cosmetic counter | 1.00 | 1.00 | 8 | Unchanged |
| R-13 | R-11 | Timestamps | 1.00 | 1.00 | 7 | Unchanged |
| R-14 | R-13 | Agent assertions | 0.85 | 0.90 | 10 | C6 no longer names `image-layers=` |
| R-15 | R-15 | Triage row | 0.30 | 0.90 | 10 | Row phrased by property; no sysbox/gVisor/LXC names |
| R-16 | R-16 | Contract enum | 0.90 | 0.90 | 7 | Unchanged |
| R-17 | R-17 | HC rename | 1.00 | 1.00 | 5 | Unchanged |
| R-18 | R-18 | Command surface | 0.60 | 0.95 | 10 | Category nouns only; no keys, cells, or filenames |
| R-19 | R-19 | Tests | 0.25 | 0.85 | 35 | Synthetic io/nonio fixtures per assertion; sysbox is one regression parameter set |

Unweighted mean: old **0.716** → new **0.921**. Volume-weighted mean (Σ weight = 294): old **0.598** → new **0.900**.

Arithmetic check: Σ weight = 30+18+22+22+30+8+30+12+16+8+6+8+7+10+10+7+5+10+35 = 294. Matches.

---

## 3. Cross-item inconsistency roll-up (v2 internal, plus references with no owner)

| # | Where | Issue | Suggested resolution |
|---|---|---|---|
| I-1 | Q1 (v2:189) vs R-04 trigger (v2:295) | Q1 says "two-clause" trigger; R-04 has three OR-clauses (AD-02/GB-04 added `producer-count=unknown`) | Implement R-04's three clauses; Q1 wording stale |
| I-2 | S1.6.4a item 5 (v2:204) | "`## Fix candidate` (R-03 step 5)" — R-03 has steps 1-4; fix-candidate is the trailing paragraph of constraint 5 | Cite "R-03 constraint 5 trailing rule" |
| I-3 | R-03 header (v2:278) vs S1.6.4a header (v2:200) | R-03's append repeats `**Round**` (already at skeleton :263) and omits `discriminator-required`, `indistinguishable`, `probe-rows-truncated` | One merged header line owned by the R-03/R-04 task |
| I-4 | R-03 constraint 5 / R-05 step 5 | "task type 5" / "task-type-5 rows" — no task types 1-4 defined anywhere in v2 or repo | Define once in Section 7 (e.g. "task type 5 (the other four being the existing per-line task shapes)") or rename to "fail-closed emission row" |
| I-5 | R-03 (v2:284), R-04 (v2:304), R-16 (v2:511), A8 | `status: blocked` introduced; `SKILL:43` status enum is `success|partial|failed`; audit footer `SKILL:457` `<success|partial>`; `VAL:72,99-103` `success|partial` | No R-item owns the `status` enum extension. Add to R-16 task: extend `status` enum + footer + VAL status decision |
| I-6 | R-04 counter key (v2:304) | `<branch>` undefined (git branch vs S1.6.4 branch row) | Define as git branch (T9 "persists across slugs" intent) |
| I-7 | R-04 (v2:294) | Names `SKILL:266` cap row but not its duplicate at `SKILL:570` | Edit both |
| I-8 | R-05 step 3 (v2:329), T16 | "cap 0.4" for `comparator=none` has no C-rule in R-14 (C7 = 0.5 `uncited`) | Add C9 or make it a Wave 5 orchestrator cap in R-10 |
| I-9 | R-14 C6 (v2:468) | "evidence quality ≤0.3" — no rubric dimension by that name; dimension scores are 0.0/0.5/1.0 | Read as Evidence grounding := 0.0, or a calibrated cap of 0.3 |
| I-10 | R-14 A6, A7 | "→ FAIL" with no flag name; every other A-rule names one; T1 asserts "the named flag" | Name them (e.g. `reference_value_not_literal`, `run_site_unresolved`) |
| I-11 | R-14 VAL inputs | A7/A8 need `RUN-SITE`/`OBSERVE-VIA` from `execution-locus.md` and `job-*.log` glob; inputs list only `producers_path`, `tasklist_path` | Add `locus_path`, `output_dir` (VAL has Glob) |
| I-12 | R-07 A6 regex vs `n/a` (v2:371, 381) | `if\|only\|/\|,` rejects the legal `n/a` on the first instrumented run | Gate A6 on not-first-run, or exempt literal `n/a` |
| I-13 | R-08 (4) vs `:381` clause (v2:392, 394) | `split-pending` "satisfies the Wave 4 precondition" vs "no mechanism disagreement remains un-probed" | Read as: split-pending clusters are excluded from the debate set |
| I-14 | R-08 (v2:391) | `refs/escalation-rubric.md:63-69` "gains one rule" — rule text never given | Implementer authors (e.g. `split-pending` cluster ⇒ ESCALATE reason `split_pending`) |
| I-15 | R-01 (v2:225) | `refs/environment-deltas.md` — only the prompt list is given; no body text | Implementer authors a minimal ref |
| I-16 | R-16 (v2:511) | `blocked-on-authorization` on `pipeline_hardening_verdict`; §5.4 truth table row 1 returns `not_applicable` when hardening n/a; no row yields the new value | Add a truth-table row with precedence 0, or move the value to `status` |
| I-17 | R-16 | Enum literal also at `SKILL:64,420,444`, `report-template.md:223,315`, `pipeline-hardening-closure.md:13`, `remediation-handoff.md:11,35,69`, tests `test_hardening_output_contract.py:93-94`, `test_hardening_verdict.py:51` | Edit all; update the two existing tests |
| I-18 | R-17 | "0 hits outside contract field names" — no field NAME contains H0-H5; only descriptions at `SKILL:63,68-71` | Rename descriptions too; guard is `== 0` |
| I-19 | R-15 (v2:489) | Ref text carries "(S14, R-03)" spec ids | Cite ref section instead of R-number |
| I-20 | R-15 refuse-Tier-1 vs R-05/FM-03 | "only one environment reachable ⇒ refuse Tier 1" vs "single environment ⇒ `comparator=none`, proceed UNDETERMINED" | Compatible if refusal = recommend `--depth deep` (triage-checklist:58); say so |
| I-21 | R-18 (v2:531) | "the verdict source used" — no Output Contract field; lives only inside the locus card | Acceptable via `execution_locus_card_path`; note it |
| I-22 | R-19 layout (v2:553) vs T2 | `assertions/<A1..A10\|C1..C8>/` omits `C3b`; T2 counts 36 = 9 rules | Add `C3b/` dir |
| I-23 | R-19 preamble | "No LLM in CI" + T13 parity ⇒ requires a Python procedural/assertion library; v2 never names its location | Task builder must add a "parity library" task before T1/T2/T13 |
| I-24 | R-19 T15 | Regression fixtures are byte copies from Fable/GLM/Astra machines + `/tmp` zip | Confirm source availability before scheduling T15 |
| I-25 | R-02 step 4 (v2:243) vs design rule (v2:155) | Mandatory step names file nodes `/proc/\|/sys/\|/dev/` | Keep as read/parse example or move to pack |
| I-26 | R-09 step 4 (v2:415) vs design rule | Mandatory step names tool `gh api` | Phrase as "raw source fetch (e.g. `gh api`)" |
| I-27 | R-03 vs R-06 | Both replace/extend the same `SKILL:241` sentence | One merged edit |
| I-28 | R-03 | `SKILL:530` duplicates the "no hypothesis work in the same turn" sentence; not named by spec | Consistency edit |
| I-29 | R-13 (v2:458) | "append to the last Will-Not bullet" (`SKILL:545`, about source targeting) — semantically unrelated | New sibling bullet |
| I-30 | Test coverage | No T-row for R-08 step 4.5, R-11, R-15, R-17, R-18 | Add content-assertion tests in the existing `test_hardening_*` style |

## 4. Landing-order dependencies (derived from the cards)

1. R-01 (locus card; sentinel, `OBSERVE-VIA`, `CONTROL-PROOF`, `job-*.log`) — first; everything downstream reads its fields.
2. R-05 (probe-form table) before R-02 step 4 and R-04 step 1 (both copy from the table).
3. R-02 (producers.md) before R-04 (trigger reads `surviving`) and R-10 (`UNDETERMINED — among {rows}`).
4. R-03 + R-04 + R-06 together (shared `SKILL:241` sentence, shared tasklist header, S1.6.4a order).
5. R-16 before R-03's precedence text can reference `blocked-on-authorization`; R-16 before R-17 (both touch `hardening-output-contract.md`, `SKILL:64/420/444`).
6. R-07 before R-08 (form) and R-09 (fetched primitive fills the form field).
7. R-14 last among skill/agent items (collects every A/C rule from R-01, R-03, R-05, R-06, R-07, R-09, R-10, R-13, R-16).
8. R-10, R-11, R-12, R-13 (Wave 5) independent of each other; R-12 after R-11 (exemption list).
9. R-15, R-18 independent; R-18 after R-01/R-04 names are final.
10. R-19 last; parity library (I-23) before T1/T2/T13.

---

**Status:** Complete

## Summary

1. Cards R-01..R-19 written with verbatim v2 insert content, Must-NOTs, critique ids (translated v1→v2), T-coverage, and dependencies; global extracts (design rule, renumber map, removed-names list, Q1-Q6, S1.6.4a order, full R-19 table + fixture layout + coverage rule, rescore table) included verbatim.
2. Anchor verification: all spec line hints for `SKILL`, `refs/*`, `CAL`, `VAL`, `CMD` matched the repo on 2026-09-19 (602-line SKILL baseline confirmed) except `VAL:51-58` (responsibility 2 is :51-55; 2b inserts before :56) and descriptive imprecision at `SKILL:450` ("bullet" is a paragraph). All new artifact/field names are greenfield (0 hits).
3. Unowned edits discovered: `status` enum extension to include `blocked` (I-5); duplicate cap row `SKILL:570` (I-7); enum literal in 8 other files + 2 existing tests (I-17); `SKILL:530` duplicate sentence (I-28).
4. Undefined references inside v2: "task type 5" (I-4); counter key `<branch>` (I-6); cap 0.4 with no C-rule (I-8); "evidence quality" dimension (I-9); flag names for A6/A7 (I-10); escalation-rubric "one rule" text (I-14); `environment-deltas.md` body (I-15); `blocked-on-authorization` unreachable via §5.4 truth table (I-16).
5. Largest hidden dependency: R-19's "No LLM in CI" + T13 parity requires a Python procedural + assertion library whose location v2 never names (I-23); regression fixture sources live off-machine (I-24).
