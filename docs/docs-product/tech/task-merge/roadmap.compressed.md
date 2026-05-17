---
spec_source: "TDD_TASK_DIRECTIONAL_MERGE.compressed.md"
complexity_score: 0.92
complexity_class: HIGH
primary_persona: architect
adversarial: true
base_variant: "A"
variant_scores: "A:86 B:86"
convergence_score: 1.0
---

# Task Directional Merge (/sc:task → /task) — Project Roadmap

## Executive Summary

This roadmap sequences the directional merge of the donor `/sc:task` command+skill pair into the recipient `/task` skill across five technical-layer milestones, transplanting 8 Transfer Units (TU-1..TU-8) under 5 load-bearing invariants (INV-01..INV-05) and 9 manifest exceptions (ME-1..ME-9), with the 7-foundation-row M1 atomic commit (ME-6) gated by CR-7 ORDERING sentinel + AST-grade grep, donor SKILL.md hard-deleted at Step 6 (CR-DEP-03), and 144 residual deprecation-surface occurrences eliminated via the FR-CR-DEP-06 one-shot manifest. The TDD's 10-step canonical commit sequence is folded into this layered phasing such that S-1 (in-flight discharge), S-2 (CLI atomicity), and S-3 (Makefile flock atomicity) bindings are enforced at the boundaries between milestones.

**Business Impact:** Internal framework consolidation eliminating dual-surface maintenance burden (K-08: 2→1 paired SKILL.md files), reducing visible command surface (K-07: 2→1 paired `/sc:help` entries), and closing the audit-pass discipline gap from 144 residual `/sc:task` occurrences to 0 outside authorized buckets (K-03), enabling rf-qa floor (INV-03) to be enforced uniformly at all 4 invocation points post-merge.

**Complexity:** HIGH (0.92) — heavyweight feature merge with ~108 entities (37 requirements + 71 entity IDs), 5 load-bearing invariants with INV-04 split into parse/semantic layers (HIGHEST EXPOSURE per validation-spec §9 L285), three coarse-grained atomic commits (Steps 1, 5, 6) under ME-6, server-side CI enforcement required (AC-ATK-17), 136-file live in-flight floor (monotonic upward), 144 residual occurrences across 40+ files, 47 adversarial-validation artifacts converged at 0.86, and 5 R-DRIFT items requiring patches (R-DRIFT-03 MEDIUM is M3-blocking).

**Critical path:** M1 foundation atomic commit (CR-FM-01..03 + CR-TASK-01..04 + CR-7 sentinel + AC-ATK-05 register) → M2 TFEP cluster (TU-5..TU-8 byte-for-byte) → M3 CLI re-route + donor command stubification (S-2 atomic binding) → M4 donor SKILL.md hard-delete + flock-guarded sync (S-3 atomic binding) → M5 validation walkthrough + CR-DEP-06 manifest + audit closure. R-DRIFT-03 anchor patch (`:200-210` → `:157-161`) is a M3 pre-commit blocker; S-1 in-flight discharge (132+ refs in live `TASK-PRD-20260514-121039`) blocks M3 entry.

**Key architectural decisions:**

- CR-7 ORDERING enforcement via HTML-comment sentinel PLUS AST-grade ordering grep (NOT markdown discipline alone); closes R-ATK-01
- Server-side CI push-policy hook at `.github/workflows/push-policy.yml` for ME-6 atomicity (NOT local `.git/hooks/pre-push` which is `--no-verify` bypassable); closes H-2 / R-ATK-17
- TFEP baseline persists on disk at `${TASK_DIR}/research/test-baseline.yaml` (ADAPT from donor in-memory form); load-bearing for INV-04 across session boundaries
- `flock(2)` on `.claude/skills/.sync-lock` wraps `make sync-dev` + `make verify-sync`; closes H-3 worktree race + live copy-overwrite race (Q-GAP-04 macOS/BSD portability via `brew install flock` fallback)
- CR-FM-03 default-to-STANDARD parse-layer shim PLUS AC-ATK-18 semantic-layer content audit at resume time (warn-and-continue per ME-3, NEVER HALT) — two-layer INV-04 closure
- Content-keyed anchors (CR-FM-04) replace line-number anchors for load-bearing INV-03 rf-qa block; closes R-ATK-06 line-number brittleness

**Open risks requiring resolution before M1:**

- OQ-TIER-VOCABULARY must confirm canonical post-merge tier set `{STRICT, STANDARD, LIGHT, EXEMPT}` (retire vestigial `TRIVIAL` from validation-spec §4 L103) — blocks CR-FM-01 canonicalization rules authoring
- OQ-FM-03-SUNSET must bind CR-FM-03 shim sunset condition `N` (recommended: `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`) — blocks AC-ATK-12(a) closure
- Q-GAP-02 HTML-vs-shell sentinel form must be pinned — blocks CR-7 ORDERING sentinel authoring at Step 1
- Q-GAP-05/06 helper modules `preflight.py` and `frontmatter_validator.py` authoring decision — blocks AC-ATK-10 + AC-ATK-12(c) fixture binding

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|---|---|---|---|---|---|---|---|
|M1|Foundation — Atomic 7-Row Landing + CR-7 Sentinel|Foundation|P0|XL|none|34|HIGH (ME-6 atomicity, INV-01/-04/-05 binding)|
|M2|TFEP Cluster — Core Logic (TU-5..TU-8 Byte-For-Byte)|Core Logic|P0|XL|M1; R-DRIFT-03 patch|28|HIGH (INV-04 disk persistence, ME-6 byte-preservation)|
|M3|CLI Re-Route + Donor Stubification (S-2 Atomic)|Integration|P0|L|M2; S-1 in-flight discharge|26|HIGH (rebase-split bypass H-2, 6 CLI emission sites)|
|M4|Donor Hard-Delete + Flock-Guarded Sync (S-3 Atomic)|Hardening|P0|L|M3; rf-qa F-07 verifier PASS|22|HIGH (destructive-by-default, INV-04 highest exposure)|
|M5|Validation, Manifest, Docs, Audit Closure|Production Readiness|P0|M|M4|22|MEDIUM (R-DOC-01 content audit, K-01..K-08 baseline)|

## Dependency Graph

M1 → M2 → M3 → M4 → M5
   (R-DRIFT-02 patch pre-M4 audit window; R-DRIFT-03 patch pre-M2 TFEP commit)
   (S-1 in-flight discharge: 14d max-wait gate pre-M3 entry)
   (S-2 atomic binding: M3 commit must include CR-DEP-01 + CR-REF-01..05 + CR-DOC-01 atomically)
   (S-3 atomic binding: M4 commit must include CR-DEP-03 + CR-DEP-04 + CR-DIST-02 atomically)
   (Server-side AC-ATK-17 hook active from M3 push-time onward)

## M1: Foundation — Atomic 7-Row Landing + CR-7 Sentinel

**Objective:** Land the 7 mutually-presupposing foundation rows (ME-6 M1 atomicity) plus AC-ATK-05 closed-enum register in a single source-tree commit, establishing CR-7 ORDERING sentinel + row-1 call-site (`path_override_check → tier_field_validate → gate_1_dispatch`), `Tier:` frontmatter contract with CR-FM-03 default-STANDARD shim, and Gate-1 dispatch infrastructure. | **Duration:** Week 1 (T+0 to T+5d; anchored 2026-05-16 → 2026-05-21) | **Entry:** OQ-TIER-VOCABULARY + OQ-FM-03-SUNSET + Q-GAP-02 sentinel form + Q-GAP-05/06 helper module decisions resolved by Engineering Lead | **Exit:** Step-1 pre-commit gate returns 0; CR-FM-04 row-1 ordering grep PASS; AC-SM-12 100% in-flight resume PASS against 136-file live population; M1 single-commit atomicity verified via `git log --name-only`

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-TU-1|Tier field + Gate-1 dispatch + per-item marker|Recipient frontmatter gains optional Tier field; TEXT-ONLY classification header emitted; Gate-1 dispatch fires once per task entry (ME-1 binding); per-item (Tier:...) marker is read-only|task/SKILL.md|—|AC-ATK-05 closed-enum register; AC-SM-01 single Gate-1 emit per entry|L|P0|
|2|FR-TU-2|Critical/Trivial Path Override at row-1 (CR-7 ORDERING)|3 call sites fire in fixed order: path_override_check → tier_field_validate → gate_1_dispatch; critical paths force STRICT (ANY-match); trivial paths take LIGHT (ALL-match); CR-7 sentinel at Step 1|task/SKILL.md|FR-TU-1|AC-ATK-01 AST/line-range check; AC-ATK-13 sentinel audit; AC-SM-07 ordering grep; AC-SM-08 verbatim diff|M|P0|
|3|FR-CS-1|Step 1: Foundation row landing + CR-7 ORDERING sentinel|Land 7 mutually-presupposing foundation rows atomically (ME-6 M1 atomicity); CR-FM-01..03 + CR-TASK-01..04 + CR-7 sentinel + row-1 call-site + AC-ATK-05 register; single commit|task/SKILL.md|FR-TU-1; FR-TU-2|CR-FM-04 ordering grep + sentinel grep PASS|XL|P0|
|4|DM-001|Tier frontmatter field schema (CR-FM-01)|Closed enum {STRICT,STANDARD,LIGHT,EXEMPT}; optional row-1 position; default STANDARD via CR-FM-03; never mutated by runtime|task/SKILL.md|OQ-TIER-VOCABULARY|AC: id:row-1-position; type:closed-enum-string; cardinality:0..1; default:STANDARD-via-CR-FM-03; mutability:author-set-immutable; canonicalization:case-strict; refusal:HALT-on-non-enum; consumers:closed-via-AC-ATK-05|S|P0|
|5|DM-002|Per-item inline marker schema (CR-FM-02 / AC-ATK-05)|Marker token `(Tier: <VALUE>)`; regex `^- \[[ x]\] \(Tier: (STRICT\|STANDARD\|LIGHT\|EXEMPT)\) `; 3-level fallback chain|task/SKILL.md|DM-001|AC: token-form:parenthesized; regex:checkbox-prefix; values:same-enum-as-DM-001; cardinality:0..N; placement:after-checkbox-before-text; default:fallback-to-DM-001; malformed:warn-continue-never-HALT; re-dispatch:forbidden-per-ME-1|S|P0|
|6|API-001|path_override_check function|Position FIRST in CR-7 ORDERING; ANY-match critical globs → STRICT; ALL-match trivial globs → LIGHT; emits 1 Task Log line; pure-read no side effect beyond log|task/SKILL.md|FR-TU-2|AC: signature:list-str-to-stance-enum; critical-globs:{auth/,security/,crypto/,models/,migrations/}; trivial-globs:{*.md,docs/,*test*.py}; precedence:critical-before-trivial; INV-bindings:INV-01,INV-04,INV-05|S|P0|
|7|API-002|tier_field_validate function|Position SECOND in CR-7 ORDERING; closed-enum validation; absent→STANDARD via CR-FM-03 shim; non-enum→ValueError HALT pre-loop|task/SKILL.md|API-001|AC: signature:dict-to-tier-enum; valid-values:STRICT-STANDARD-LIGHT-EXEMPT; absent-handling:return-STANDARD-no-mutation; non-enum:raise-ValueError; negative-set-guard:{ITERATIVE,SIMPLE,IMPLEMENT,COMPLEX}; side-effect:none-read-only|S|P0|
|8|API-003|gate_1_dispatch function|Position THIRD in CR-7 ORDERING; resolution precedence: forced_stance=STRICT→STRICT, forced_stance=LIGHT→LIGHT, else map tier_field; fires ONCE per task entry (ME-1); ships atomic with TU-1 (ME-6)|task/SKILL.md|API-001; API-002|AC: signature:stance-str-tier-str-to-profile; precedence:forced-then-declared; ME-1-binding:single-fire-per-entry-not-per-iteration; ME-6-binding:atomic-with-D09a|S|P0|
|9|COMP-001|TU-1 Tier field parser + Gate 1 dispatch module|Pre-loop classifier read-only; ~20 LOC post-merge; insertion at row-0 sentinel + new subsection after L73 + bullet in F1 EXECUTE dispatch|task/SKILL.md|API-001..003|AC: kind:pre-loop-classifier; LOC:~20; insertion:row-0-sentinel+L73-subsection+F1-EXECUTE-bullet; INV-protected:INV-04-parse-INV-05; ME-bound:ME-1-ME-6; CR-row-author:CR-FM-01..03+CR-TASK-01..03|M|P0|
|10|COMP-002|TU-2 Path override module|Pre-loop classifier read-only; ~10 LOC; row-0 shared sentinel + new subsection adjacent to TU-1|task/SKILL.md|API-001|AC: kind:pre-loop-classifier; LOC:~10; pattern-source:donor:121:critical-globs+:123:trivial-globs; INV-protected:INV-05; ME-bound:ME-6; CR-row-author:CR-TASK-01+CR-7-sentinel|S|P0|
|11|NFR-INV-1|F1 progress monotonicity|F1 loop READ→IDENTIFY→EXECUTE→UPDATE→REPEAT preserved; no new HALT semantic mid-checklist; environment-non-ideal MUST warn-and-continue; per-item dispatch forbidden (ME-1)|task/SKILL.md|COMP-001..002|AC-ATK-02 5-row matrix; AC-ATK-13 sentinel test; AC-ATK-10 asymmetry; grep:no-new-HALT-clause|M|P0|
|12|NFR-INV-5|Refusal-of-definition|Tier field + per-item marker = metadata conditioning audits NOT work-definition; closed list of authorized consumers (initial {CR-TASK-07 baseline-skip}); new consumer requires new ME-NN|task/SKILL.md|COMP-001|AC-ATK-05 closed-enum committed; tests/audit/test_marker_consumers.py; ME-1 design-review checklist; no-embedded-classifier-grep|S|P0|
|13|NFR-ME-1|PRE-LOOP DISPATCH ONLY (Load-bearing)|Per-item dispatch forbidden; protects INV-05; Tier marker is tier-conditioned READ only; AC-ATK-05 register is operational manifestation|task/SKILL.md|NFR-INV-5|CR-TASK-02 + CR-TASK-03 acceptance; closed-enum register present|S|P0|
|14|NFR-ME-6|M1 atomicity TIER FIELD + GATE 1 SHIP TOGETHER (Load-bearing)|Seven foundation rows mutually presupposing; land in one source-tree merge; rebase-split prevented server-side|task/SKILL.md|FR-CS-1|M1 atomicity rule audit at merge-master.md:60; AC-ATK-06 frozen fixture; AC-ATK-17 server-side hook|M|P0|
|15|TEST-001|AC-ATK-01 Row1 call order test|tests/skills/task/test_row1_call_order.py::test_path_override_first; AST/grep ordering check|tests/|API-001..003|AC: gate:Step-4-pre-commit; assertion:monotonic-line-order; failure:blocks-commit|S|P0|
|16|TEST-013|AC-ATK-13 Row1 ordering grep|tests/skills/task/test_row1_ordering_grep.py::test_executable_grep|tests/|TEST-001|AC: both-CR-FM-04-greps-return-3-names-monotonic; 0-reorders-detected|S|P0|
|17|TEST-005|AC-ATK-05 Marker consumers closed set|tests/audit/test_marker_consumers.py::test_closed_consumer_set; verifies {CR-TASK-07 baseline-skip} only|tests/|DM-002|AC: authorized-consumer-list=1; new-consumer-requires-new-ME-NN-row|S|P0|
|18|TEST-012|AC-ATK-12 Incident schema + canonical enum|tests/skills/task/test_tfep_incident_schema.py + test_cr_fm_01_canonical.py|tests/|DM-001|AC: schema-7-fields; tier-enum-closed-STRICT-STANDARD-LIGHT-EXEMPT|S|P0|
|19|TEST-025|AC-SM-07 CR-FM-04 ordering|tests/skills/task/test_cr_fm_04_ordering.py::test_row_1_order + test_row_10_order|tests/|API-001..003|AC: 2-greps-x-3-names=6-hits-monotonic; 0-reorders|S|P0|
|20|MIG-001|Step 1 atomic foundation row landing|7-row atomic per ME-6/CR-7/CR-9 commit; helper modules tier_field_validate + path_override_check + gate_1_dispatch authored; deferred-regen initial|src/|FR-CS-1|Step-1-pre-commit-gate:0; AC-SM-07-cleared; AC-SM-12-100pct-resume-PASS-against-136-floor|L|P0|
|21|MIG-FF-1|Feature flag: CR-FM-03 default-to-STANDARD shim|Always-on from Step 1; sunset binding TBD per OQ-FM-03-SUNSET; cleanup date: after CR-MIGR-FM-03 + 50 generations + 90 days post-Step-6|src/|OQ-FM-03-SUNSET|AC: emission:gate-1.4-shim-status-line-per-resume; sunset-row-authored:bool; generations-remaining:int|S|P0|
|22|MIG-FF-2|Feature flag: gate-1.4 shim-status counter|Always-on from Step 1; co-removed with CR-FM-03 shim; emits per resume|src/|MIG-FF-1|AC: format:gate-1.4:-shim-status-surface=CR-FM-03-generations_remaining=N-sunset_row_authored=bool|XS|P0|
|23|OPS-EM-1|Task Log emission schema TU-1 gate-1|Append-only line `gate-1: dispatch_profile=<X> source=<frontmatter\|default\|path-override>` per task entry|task/SKILL.md|API-003|AC: append-only-no-mutation; single-line-per-entry; INV-04-resumability-preserved|XS|P0|
|24|OPS-EM-2|Task Log emission schema TU-2 path-override|Append-only line `path-override: forced_stance=<X> (matched: <glob>)\|no-match` per task entry|task/SKILL.md|API-001|AC: exactly-1-line-per-call; emission-order:before-gate-1; INV-bindings:INV-01-INV-04-INV-05|XS|P0|
|25|OPS-A-1|Pre-commit gate Step-1|`uv run pytest && make verify-sync && grep -q 'CR-7 ORDERING' && grep -q 'CR-8 ORDERING'`; 0=pass|scripts/|MIG-001|AC: exit-code:0-pass-nonzero-block; failure-disposition:investigate-sentinel-or-sync-drift|S|P0|
|26|FR-TU-3|Gate-2 verification roster widening|Phase-Gate QA at task/SKILL.md:181-211 widens verifier_roster to [rf-qa, quality-engineer] on STRICT; quality-engineer additive only; rf-qa always present (ME-2)|task/SKILL.md|MIG-001|AC-ATK-11 retroactive ME-10 or non-generalization annotation; AC-SM-02 ME traceability|M|P0|
|27|FR-TU-4|D15b git pre-flight (warn-and-continue)|F1 entry block gains Layer-2 pre-flight `git status` check with 5-row disposition matrix; no HALT (ME-3; INV-01 progress guarantee)|task/SKILL.md|MIG-001|AC-ATK-02 5-row matrix; AC-ATK-10 input-invalid-vs-environment-non-ideal asymmetry|M|P0|
|28|FR-CS-2|Step 2: Tier classification + Gate 1 dispatch|Land Tier frontmatter contract + Gate 1 dispatch + closed-enum canonicalization (CR-FM-01) + parse-error HALT for malformed Tier (CR-TASK-02)|task/SKILL.md|FR-CS-1|Step-2-pre-commit-gate:0; CR-TASK-05-CR-TASK-06-CR-TASK-07-acceptance|M|P0|
|29|COMP-003|TU-3 Verification roster widening module|Phase-gate + post-completion expansion (additive spawn); ~14 LOC; +Step 3b inside L191-198 + Step 1b inside L219-226 + Step 4 verdict-processing edit + bullet in agent-type list L290-299|task/SKILL.md|FR-TU-3|AC: kind:additive-spawn; pattern-source:donor:89-quality-engineer+:116-STRICT-routing; INV-protected:INV-03-floor-preserved; ME-bound:ME-2; CR-row-author:CR-TASK-05|S|P0|
|30|COMP-004|TU-4 Git pre-flight Task Log emission module|F1 pre-execution side-channel 5-row warn-and-continue; ~12 LOC; new subsection between L102 and L104|task/SKILL.md|FR-TU-4|AC: kind:F1-pre-execution-side-channel; LOC:~12; pattern-source:donor:82-verify-git-clean; INV-protected:INV-01-additive-no-HALT; ME-bound:ME-3; CR-row-author:CR-TASK-06|S|P0|
|31|TEST-002|AC-ATK-02 Git dirty dispatch test|tests/skills/task/test_git_dirty_dispatch.py::test_5_row_matrix; parametrize R1..R5 with exact Task Log line per row|tests/|FR-TU-4|AC: gate:Step-2-pre-commit; 5-rows-all-warn-continue-or-graceful-skip; 0-HALT-rows; defensive-negative-existence-no-Halt-classes|S|P0|
|32|TEST-010|AC-ATK-10 Pre-loop HALT policy 2-category|tests/skills/task/test_preloop_halt_policy.py::test_2_category_table; input-invalid Tier HALT exit-2 vs env-non-ideal git-dirty WARN-CONTINUE exit-0|tests/|FR-TU-4|AC: 2-rows-input-invalid-HALT-environment-non-ideal-warn-continue; asymmetry-table-present-in-merged-skill|S|P0|
|33|OPS-A-2|Pre-commit gate Step-2|`uv run pytest && make verify-sync` no new gates beyond Step-1 baseline|scripts/|FR-CS-2|AC: gate:Step-2-pre-commit; failure:re-author-CR-TASK-05-or-CR-TASK-06-row|XS|P0|
|34|OPS-EM-3|Task Log emission schema TU-4 gate-1.5 pre-flight|`gate-1.5: pre-flight tier=<tier> git_status=<value> action=<action> [reason=<token>]` per pre-flight invocation|task/SKILL.md|COMP-004|AC: 5-row-matrix-coverage; closed-token-set:{timeout,permission,index-locked,nfs-stale,unknown}; never-HALT|XS|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|path_override_check()|API call-site|Row-0 sentinel + row-1 site|M1|gate_1_dispatch (sequence dependency); F1 EXECUTE|
|tier_field_validate()|API call-site|Row-1 site after path_override|M1|gate_1_dispatch (resolution chain)|
|gate_1_dispatch()|API call-site|Row-1 site after tier_field_validate|M1|F1 EXECUTE dispatch table|
|CR-7 ORDERING sentinel|HTML comment marker|Above row-1 in task/SKILL.md|M1|CR-FM-04 grep audit; CR-TASK-12 verbatim-diff|
|AC-ATK-05 closed-enum register|Audit-row registry|src/superclaude/skills/task/rules/ or adjacent|M1|tests/audit/test_marker_consumers.py|
|CR-FM-03 shim|Parser default fallback|frontmatter_validator.py|M1|All in-flight task resume paths|

### Milestone Dependencies — M1

- none (foundation)

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-TIER-VOCABULARY|Confirm canonical post-merge tier vocabulary `{STRICT, STANDARD, LIGHT, EXEMPT}` (retire vestigial `TRIVIAL` from validation-spec §4 L103). CR-FM-01 canonicalization table mis-anchored if wrong enum codified.|Blocks CR-FM-01 canonicalization-rules table authoring; blocks DM-001 schema commit; blocks AC-ATK-12(c) closure|Engineering Lead|Before M1 commit (T+0..T+2d)|
|2|OQ-FM-03-SUNSET|Confirm CR-FM-03 default-STANDARD shim sunset binding N. Recommended: `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`. Source: TDD §22 + research/10:349.|Blocks MIG-FF-1 feature-flag cleanup-date binding; blocks AC-ATK-12(a) closure; downstream impact: all 136 in-flight files validate clean only while shim active|Engineering Lead|Before M1 commit|
|3|Q-GAP-02|HTML-vs-shell sentinel form (CR-7 ORDERING canonical form). PRD S24.2 commits to HTML-comment form `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->`. Decide: sentinel-presence grep (AC-ATK-13) OR AST-level (AC-ATK-01) OR informational.|Blocks sentinel authoring at Step 1; blocks TEST-013 fixture definition|Engineering Lead|Before M1 commit|
|4|Q-GAP-05|Helper module `superclaude/skills/task/preflight.py` to-be-authored (per AC-ATK-10 fixture binding).|Blocks TEST-010 implementation; blocks TU-4 git pre-flight realization|Engineering Lead|Before M1 commit|
|5|Q-GAP-06|Helper module `superclaude/skills/task/frontmatter_validator.py` to-be-authored (per CR-FM-01 binding + AC-ATK-12(c)).|Blocks API-002 `tier_field_validate` implementation; blocks CR-FM-03 shim realization|Engineering Lead|Before M1 commit|
|6|Q-GAP-11|Acknowledgment-gate persistence shape — Schema 5 one-shot ack mechanism (single Task Log line vs separate ack file) under-specified. From TDD §22.|Blocks AC-ATK-18(c) one-shot ack gate implementation; defers to M4 if not resolved at M1|§7 Data Models author|Before M4 (acceptable to defer past M1)|

### Risk Assessment and Mitigation — M1

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-ATK-01: CR-7 markdown discipline weakness — sentinel comment is parseable but not load-bearing to any interpreter|MEDIUM|MEDIUM|Wrong-order dispatch at runtime breaks INV-05; ordering claim relies on grep alternation that does not enforce executable order|Sentinel + AST-grade grep (AC-ATK-13); CR-FM-04 ordering grep at Step-4 pre-commit; defensive negative-existence test asserts no `Halt` class in preflight module|Engineering Lead|
|2|R-ATK-06: Line-number anchor brittleness — load-bearing INV-03 rf-qa block anchored at `:191-198` is brittle to formatting edits|MEDIUM|MEDIUM|One-line insertion above spawn block silently breaks citation while semantic guarantee holds|Content-keyed anchors (CR-FM-04 extension); convert all line-number anchors to AST/regex/content-hash|Engineering Lead|
|3|R-RES-01: Tier-conditioned read boundary conceptually thin — wrapper-routed dispatch could describe forbidden per-item dispatch as "read"|MEDIUM|MEDIUM|INV-05 erodes; per-item marker becomes runtime classifier; F1 progress monotonicity (INV-01 indirect) degrades|AC-ATK-05 closed-enum + ME-1 design-time review + CI lint step in `make verify` fails on undeclared marker consumers|Engineering Lead|
|4|R-FM-04: CI/local env divergence — `uv run pytest` CI vs local env divergence (PYTHONHASHSEED, locale, timezone)|MEDIUM|MEDIUM|Step-1 pre-commit gate passes locally but fails CI or vice-versa; no-progress state at atomic commit boundary|Pin env vars (PYTHONHASHSEED=0, LC_ALL=C, TZ=UTC) in pyproject.toml or CI image; documented dual-run attestation pre-merge|Engineering Lead|

## M2: TFEP Cluster — Core Logic (TU-5..TU-8 Byte-For-Byte)

**Objective:** Transplant the TFEP block from donor `sc-task-protocol/SKILL.md:125-244` into recipient `task/SKILL.md` byte-for-byte under ME-6 atomicity: TU-5 on-disk baseline YAML at `${TASK_DIR}/research/test-baseline.yaml`, TU-6 additive F2 prohibitions (10→13 entries) + 3 carve-outs, TU-7 mid-phase rf-qa as 4th invocation point (F-05 one-time carve-out per AC-ATK-11), TU-8 incident-report side-effect file with 7-field schema. R-DRIFT-03 anchor patch (`:200-210` → `:157-161`) is a hard prerequisite — without it CR-TASK-12 verbatim-diff returns non-zero against D23 forensic-results content and erroneously blocks the M3 commit. | **Duration:** Week 2 (T+5d to T+10d; 2026-05-21 → 2026-05-26) | **Entry:** M1 commit landed; R-DRIFT-03 anchor patch applied to all 3 artifacts + CR-TASK-12 audit anchors | **Exit:** AC-ATK-03 4-state observer test PASS; AC-ATK-12(b) 7-field schema fixture PASS; AC-CR-TASK-09-F04 over-escalate PASS; CR-TASK-12 verbatim-diff audit fires successfully (deferred PASS to M3 close)

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|35|FR-TU-5|TFEP baseline snapshot on disk|Before F1 fires on STRICT/STANDARD, writes ${TASK_DIR}/research/test-baseline.yaml with `uv run pytest --collect-only -q` output; disk persistence load-bearing for INV-04 across session boundaries (ME-4 tier-gated; LIGHT/EXEMPT skip)|task/SKILL.md|MIG-001|AC-ATK-03 4-state observation {absent,empty,parse-fail,schema-fail} with order pinned os.path.exists→getsize→safe_load→schema|M|P0|
|36|FR-TU-6|TFEP Prohibitions + Carve-outs additive to F2|F2 catalog at L104-117 (10 entries pre-merge) absorbs 3 additive VIOLATION prohibitions + 3 permitted-exception carve-outs via byte-for-byte verbatim transplant from sc-task-protocol/SKILL.md:127-142 under CR-TASK-08; post-merge count 13|task/SKILL.md|MIG-001|AC-ATK-11 disposition matrix; CR-TASK-12 verbatim-diff audit|M|P0|
|37|FR-TU-7|TFEP escalation gradient + mid-phase rf-qa (4th invocation)|TFEP escalation routes to rf-qa mid-phase as 4th invocation point (alongside Phase-Gate L191, post-completion structural L221, post-completion qualitative L230); 6-step flow with tier ladder light/standard/FULL-STOP|task/SKILL.md|FR-TU-3|AC-ATK-11 F-05 paragraph-level surface-widening precedent; AC-SM-02 ME-2 traceability|L|P0|
|38|FR-TU-8|TFEP incident reporting side-effect file|Executor writes ${TASK_DIR}/research/tfep-incident-report.md with 7-field schema (donor literal :225-233); Outcome enum byte-identical to donor :232; no in-task heading|task/SKILL.md|FR-TU-5|AC-ATK-12(b) 7-field schema enumeration; AC-SM-04|M|P0|
|39|FR-CS-3|Step 3: Path overrides + Gate-2 roster widening|TU-2 path overrides + TU-3 verification roster widening on STRICT; pre-commit gate CR-FM-04 row-1 ordering + ME-2 anchor check|task/SKILL.md|FR-CS-2|Step-3-pre-commit-gate:0; rf-qa-PASS-at-all-3-pre-merge-invocation-points|M|P0|
|40|DM-003|TFEP Baseline YAML schema (Schema 3, AC-ATK-03)|File-resident at ${TASK_DIR}/research/test-baseline.yaml; cardinality 0..1 per task (STRICT/STANDARD only); written once at First Item Protocol entry; 4-state observation order canonical|${TASK_DIR}/|FR-TU-5|AC: path:${TASK_DIR}/research/test-baseline.yaml; schema-fields:schema_version-captured_at-tier-tests; tier-enum:{STRICT,STANDARD}; 4-state-observation-order:absent-empty-parse-fail-schema-fail; persistence:disk-file-not-memory; mutability:write-once-at-FIP-entry; retention:lifetime-of-task-git-tracked|S|P0|
|41|DM-004|TFEP Incident Report 7-field schema (Schema 4, AC-ATK-12)|File-resident at ${TASK_DIR}/research/tfep-incident-report.md; cardinality 0..1 per task STRICT post-fire; donor verbatim transplant from sc-task-protocol/SKILL.md:225-233 (ME-6)|${TASK_DIR}/|FR-TU-8|AC: path:${TASK_DIR}/research/tfep-incident-report.md; field-1:Trigger; field-2:Escalation-count-int-1-2-3; field-3:Failing-tests-list-test_id-classification; field-4:Root-cause-markdown; field-5:Solution-markdown; field-6:Outcome-enum-success-escalated-failed-byte-identical-donor-232; field-7:Forensic-artifacts-path-or-list; not-in-task-heading-INV-04-binding|S|P0|
|42|API-013|rf-qa Invocation #4 (Mid-phase TFEP, NEW per TU-7)|NEW inside TFEP block between L179 and L181; qa_phase=tfep-incident-N; output path ${TASK_DIR}/reviews/qa-tfep-incident-N-report.md; authoritative count post-merge: 4 invocations|task/SKILL.md|FR-TU-7|AC: anchor:new-inside-TFEP-block; qa-phase:tfep-incident-N; additional-fields:trigger-classification+baseline-diff+failing-tests-list+escalation-gradient-stage; spawn-pattern-reuse:from-L191-198|S|P0|
|43|API-010|rf-qa Invocation #1 (Phase-Gate)|Existing rf-qa stance at task/SKILL.md:191-198; YAML spawn envelope; output path ${TASK_DIR}/reviews/qa-phase-N-report.md; partitioning >6 output files|task/SKILL.md|FR-TU-3|AC: anchor:191-198; qa-phase:phase-validation; partitioning-rule:>6-files-multiple-parallel-instances-with-assigned-files|S|P0|
|44|API-011|rf-qa Invocation #2 (Post-Completion Structural)|task/SKILL.md:219-226; qa_phase=report-validation; output path ${TASK_DIR}/reviews/qa-final-validation-report.md|task/SKILL.md|FR-TU-3|AC: anchor:219-226; qa-phase:report-validation; additional-fields:ALL-outputs-ALL-phases-cross-phase-consistency|S|P0|
|45|API-012|rf-qa-qualitative Invocation #3 (Post-Completion Operational)|task/SKILL.md:228-239; qa_phase=task-qualitative; output path ${TASK_DIR}/reviews/qa-qualitative-review.md; document_type=Executed-Task-File; 15-item checklist|task/SKILL.md|FR-TU-3|AC: anchor:228-239; qa-phase:task-qualitative; additional-fields:TARGET_FILE_LIST+modified-sources+CLAUDE.md-conventions+research-dir+15-item-checklist|S|P0|
|46|COMP-005|TU-5 TFEP baseline snapshot module|Pre-F1 side-effect file emitter YAML; ~10 LOC + on-disk file; new subsection between L179 and L181 + bullet inside Session Resumption Step 4|task/SKILL.md|FR-TU-5; DM-003|AC: kind:pre-F1-side-effect-emitter; LOC:~10+on-disk-yaml; pattern-source:donor:144-153-in-memory-adapted-file-resident-INV-04; INV-protected:INV-04; ME-bound:ME-3-ME-4; CR-row-author:CR-TASK-07|S|P0|
|47|COMP-006|TU-6 TFEP prohibitions + carve-outs module|F2 catalog additive insertion + carve-out subsection; +3 bullets (F2: 10→13) + ~6 lines carve-out; append after L117 + carve-out subsection inside TFEP block|task/SKILL.md|FR-TU-6|AC: kind:F2-catalog-additive; LOC:+3-bullets+6-lines; pattern-source:donor:133-135-VIOLATION-rules+:137-140-carve-outs; INV-protected:INV-02-INV-01; ME-bound:ME-3; CR-row-author:CR-TASK-08-CR-TASK-12|S|P0|
|48|COMP-007|TU-7 TFEP escalation trigger module (mid-phase rf-qa)|F1-side-channel escalation router; 4th rf-qa invocation surface; ~15 LOC; new subsection inside TFEP block|task/SKILL.md|FR-TU-7; API-013|AC: kind:F1-side-channel-escalation-router; LOC:~15; pattern-source:donor:157-161-3-MUST-escalate-triggers; INV-protected:INV-03-additive-ME-2-preserved; ME-bound:ME-2-ME-3; CR-row-author:CR-TASK-09; AC-ATK-11-carve-out:one-time-non-generalizing|S|P0|
|49|COMP-008|TU-8 TFEP incident report module|Post-resolution side-effect file emitter Markdown; ~12 LOC + on-disk file; new subsection inside TFEP block|task/SKILL.md|FR-TU-8; DM-004|AC: kind:post-resolution-side-effect-emitter; LOC:~12+on-disk-md; pattern-source:donor:222-234-7-field-schema-byte-for-byte-Outcome-:232; INV-protected:INV-04; ME-bound:ME-3-ME-6-byte-preservation; CR-row-author:CR-TASK-10-CR-TASK-12|S|P0|
|50|NFR-INV-2|F2 catalog additivity|F2 Prohibited Actions at :104-117 extended only additively; pre-merge count 10; TU-6 adds 3 → ≥12 (target 13); no existing prohibition deleted/weakened/narrowed|task/SKILL.md|FR-TU-6|pytest test_prohibitions_additive.py; AC-ATK-11; pre-merge-vs-post-merge-diff:additive-only|S|P0|
|51|NFR-INV-3|Phase-gate rf-qa floor|rf-qa remains named role at all 4 invocation points; widenings permitted; replacements/displacements prohibited (ME-2); content-keyed anchor (CR-FM-04)|task/SKILL.md|API-010..013|grep returns >=3 matches subagent_type:rf-qa; AC-ATK-07 F-07 chain verifier; AC-ATK-11; CR-FM-04 content-keyed anchor|S|P0|
|52|NFR-INV-4a|Resumability — parse layer|Every existing MDTM TASK-* file parses/resumes cleanly post-merge at structural/parse layer; CR-FM-03 default-to-STANDARD shim handles absent Tier|task/SKILL.md|MIG-FF-1|tests/skills/task/test_compat_shim_parse.py parametrized over 136 floor; AC-ATK-12(c) sunset binding|S|P0|
|53|NFR-ME-2|rf-qa SUPPLEMENTED NOT REPLACED (Load-bearing)|4 invocation points (Gate-2, post-completion structural, post-completion qualitative, mid-phase TU-7); widenings permitted; replacements prohibited; content-keyed anchor CR-FM-04|task/SKILL.md|NFR-INV-3|CR-TASK-05 acceptance; AC-ATK-11; AC-ATK-07|S|P0|
|54|NFR-ME-3|SIDE-CHANNEL ONLY NO F1 HALT (Load-bearing)|No new HALT semantics in F1 from TU-4/6/7/8 + TU-5; AC-ATK-02 5-row matrix → warn-and-continue; input-invalid (HALT) vs environment-non-ideal (warn-continue) asymmetry per AC-ATK-10|task/SKILL.md|COMP-005..008|CR-TASK-08 acceptance; AC-ATK-02; AC-ATK-10; AC-ATK-18|S|P0|
|55|NFR-ME-4|BASELINE TIER-GATED (Ancillary)|TU-5 baseline collection runs only on STRICT/STANDARD; HELD without per-row deltas|task/SKILL.md|FR-TU-5|CR-TASK-07 acceptance|XS|P0|
|56|TEST-003|AC-ATK-03 Baseline trinary 4-state test|tests/skills/task/test_baseline_trinary.py::test_4_state_observer; parametrize {absent,empty,parse-fail,schema-fail}|tests/|DM-003|AC: gate:Step-3-pre-commit; observer-order-pinned:exists-getsize-safe_load-schema; all-4-states-classification-new-all|S|P0|
|57|TEST-007|AC-ATK-07 rf-qa F-07 chain test|tests/audit/test_rf_qa_step6_gate.py::test_chain_links; 5 chain anchors verified|tests/|NFR-INV-3|AC: rf-qa-returns-PASS-pre-Step-6; gate:Step-6-pre-commit-deferred|S|P0|
|58|TEST-011|AC-ATK-11 ME-10 carve-out test|tests/audit/test_me10_carve_out.py::test_me10_authored_or_annotated|tests/|FR-TU-7|AC: ME-10-row-authored-OR-explicit-non-generalization-annotation-present|S|P0|
|59|MIG-003|Step 3: M3 TFEP cluster|R-DRIFT-03 anchor patch applied to 3 artifacts + CR-TASK-12 audit BEFORE this commit; TU-5 baseline + TU-6 prohibitions + TU-7 mid-phase rf-qa + TU-8 incident report|src/|FR-CS-3; R-DRIFT-03-patch|AC-ATK-03 4-state observer PASS; AC-ATK-12(b) 7-field schema PASS; AC-CR-TASK-09-F04 over-escalate PASS|L|P0|
|60|OPS-EM-4|Task Log emission schema TU-5 baseline|`tfep: baseline=ran files=<list> reason=fresh` or fallback `tfep: baseline=absent classification=new-all reason=<token>` per 4-state observer|task/SKILL.md|COMP-005|AC: 4-state-tokens:{ran,absent-empty-parse-fail-schema-fail}; reasons:{fresh,absent,empty,malformed,schema-fail}; always-warn-continue|XS|P0|
|61|OPS-EM-5|Task Log emission schema TU-6 prohibition refusal|`tfep: prohibition-refusal item=<id> rule=<VIOLATION-NN> reason=<reason>` per F2 violation fired|task/SKILL.md|COMP-006|AC: 3-prohibition-types-covered; warn-continue-never-HALT|XS|P0|
|62|OPS-EM-6|Task Log emission schema TU-7 escalation trigger|`tfep: escalation-trigger fired=<count> tests=<list> classification=<new\|pre-existing>` per trigger event; precedes mid-phase rf-qa spawn|task/SKILL.md|COMP-007|AC: 3-trigger-types-coverage:pre-existing-fail-3+new-fail-runtime-exception; classification-baseline-driven|XS|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|${TASK_DIR}/research/test-baseline.yaml|Disk file|First Item Protocol entry|M2|TU-7 TFEP escalation; AC-ATK-03 4-state observer|
|${TASK_DIR}/research/tfep-incident-report.md|Disk file|Post-Completion Validation|M2|Post-Completion validation read; AC-ATK-12 enumeration|
|4th rf-qa invocation (mid-phase TFEP)|Subagent spawn|TFEP block new subsection|M2|TFEP escalation gradient|
|F2 prohibitions catalog 10→13|F2 catalog rows|task/SKILL.md:104-117 append|M2|CR-TASK-12 verbatim-diff; INV-02 audit|
|TFEP carve-outs (3 exceptions)|Subsection|TFEP block carve-out subsection|M2|F1 EXECUTE prohibition disposition matrix|

### Milestone Dependencies — M2

- M1 (CR-FM-01..03 foundation + CR-7 sentinel + AC-ATK-05 register)
- R-DRIFT-03 anchor patch applied BEFORE M3 (donor `:200-210` → `:157-161` in transfer-manifest TU-7 L277 + integration-sketches IS-ADOPT-9 L142 + invariant-survival-walkthrough §2.6 step 4 L277 + CR-TASK-12 audit anchors)

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-TFEP-FIELD-COUNT|Resolve TU-8 incident-report 6-vs-7 field cardinality. §7 Schema 4 commits to 7 (donor literal at sc-task-protocol/SKILL.md:225-233); confirm field-name canonical form (e.g., `failing_tests` vs `commits/diff`).|Blocks DM-004 schema commit; blocks TEST-012 fixture freezing|Engineering Lead|Before M2 commit (T+7d..T+8d)|
|2|OQ-F-05-MANIFESTIZATION|Decide retroactive ME-10 vs one-time carve-out for F-05 (4th rf-qa invocation point post-merge — TU-7 mid-phase TFEP) per AC-ATK-11.|Blocks AC-ATK-11 disposition closure; blocks TEST-011 expected-state binding|Engineering Lead|Before M2 commit|
|3|OQ-PROHIBITION-DISPOSITION-MATRIX|Decide verifier-spawned F1 disposition (root F1 vs verifier-spawned F1 vs mid-phase rf-qa) per AC-ATK-11 generalization.|Blocks TU-6 prohibition disposition matrix authoring; blocks NFR-INV-2 acceptance criterion|Engineering Lead|Before M2 commit|
|4|Q-R-DRIFT-03|MEDIUM (mechanical, multi-artifact): donor anchor `:200-210` should be `:157-161` (anchor off-by-43). If CR-TASK-12 verbatim-diff runs against `:200-210` literally, it returns non-zero (content there is D23 forensic-results REJECTed by ledger LR-DEFER-6) and erroneously blocks M3 commit.|Hard blocker for M3 commit; patch single-source 3 artifacts + CR-TASK-12 audit anchors|Documentation/Release Owner (patch task)|Before M2 close|
|5|Q-GAP-10|`${TASK_DIR}/research/tfep-incident-report.md` template (CR-TASK-10) — 7-field schema fields enumeration must match donor `:222-234` verbatim. Current TDD inference `{tier, item_id, trigger, classification, action, timestamp, sha}` is research-time; donor canonical names owed.|Blocks DM-004 final commit; defers to OQ-TFEP-FIELD-COUNT closure|Engineering Lead|Before M2 commit|

### Risk Assessment and Mitigation — M2

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-DRIFT-03: Donor anchor off-by-43 (`:200-210` → `:157-161`) in transfer-manifest TU-7 L277, integration-sketches IS-ADOPT-9 L142, invariant-survival-walkthrough §2.6 step 4 L277|MEDIUM (M3-blocking)|HIGH|CR-TASK-12 verbatim-diff returns non-zero against D23 forensic-results content; erroneously blocks M3 commit|Pre-M2 patch single-source: replace `:200-210` → `:157-161` in all 3 artifacts + CR-TASK-12 audit anchors|Documentation/Release Owner|
|2|R-RES-02: F-05 widens INV-03 surface beyond canonical anchor language; `extension-point-contracts.md:11-17` NOT amended|MEDIUM|MEDIUM|Future reviewer applying strict-anchor-only discipline treats mid-phase invocation as out-of-scope|AC-ATK-11 retroactive ME-10 OR one-time non-generalizing carve-out; OQ-F-05-MANIFESTIZATION resolution before M2 commit|Engineering Lead|
|3|R-RES-03: F-04 over-escalation unbounded by design — rf-qa queue flood risk on absent/empty/malformed baseline|MEDIUM|MEDIUM|rf-qa verifier queue saturates; classification=new for every failure produces noisier escalation queue without throttling|Reactive refusal threshold post queue-depth telemetry; PRD §20.3 R-OPS-03; monitor via R5 runbook|Engineering Lead|
|4|R-ATK-11: F-05 ME-10 carve-out paragraph-level surface-widening precedent could be re-cited by future TU-style merges|MEDIUM|MEDIUM|Future widenings invoke F-05 as precedent with weaker justification|AC-ATK-11 explicit one-time non-generalizing carve-out in source plan; block precedent claims by future TU-style merges in CR-7|Engineering Lead|

## M3: CLI Re-Route + Donor Stubification (S-2 Atomic)

**Objective:** Land Step 4 verbatim-diff audit (CR-TASK-12 seven-diff against frozen donor-block fixtures) followed by Step 5 atomic soft-deprecation: stubify `/sc:task` command surface (CR-DEP-01), emit sha256 baseline (CR-DEP-02), re-route 6 CLI emission sites in `cli/sprint/process.py:170` + `cli/cleanup_audit/prompts.py:{26,47,69,92,116}` to `/task` (CR-DEP-04), update docs (CR-DOC-01), and activate server-side push-policy hook (AC-ATK-17). S-1 in-flight discharge precondition: `TASK-PRD-20260514-121039` (258 refs, 12 files, LIVE Doing) + companion `TASK-TDD-20260514-121250` (LIVE) + broader 136-file in-flight floor must complete OR snapshot-freeze with decision record OR `--max-wait 14d` auto-invoke option (b) per AC-ATK-08 before this milestone enters. R-DRIFT-02 anchor patch (`:127-135` → `:133-135`) is a Step-4 audit-window prerequisite. | **Duration:** Weeks 2.5-3.5 (T+10d to T+15d; 2026-05-26 → 2026-05-31) | **Entry:** M2 close + S-1 in-flight discharge attested + R-DRIFT-02 patch applied + Q-GAP-07 donor-block fixtures authored | **Exit:** AC-ATK-15 Step-5 atomicity test PASS; AC-ATK-17 server-side pre-receive hook PASS (no rebase-split bypass); AC-SM-09 commit roster equality test PASS; CR-TASK-12 7-diff returns 0

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|63|FR-CS-4|Step 4: TU/donor verbatim diff audits + sentinel landing|CR-TASK-12 seven-diff audit pass (6 donor strings + 1 sentinel-comment block) against donor blocks; pre-commit gate zero-diff against tests/fixtures/donor-blocks/|tests/|MIG-003; R-DRIFT-02-patch|7-zero-diffs-PASS; AC-SM-08 gate|M|P0|
|64|FR-CS-5|Step 5: Donor command stubification (atomic, S-2 binding)|CR-DEP-01 stubify /sc:task command + CR-DEP-02 sha256 baseline + CR-DEP-05 CLI residual grep + CR-DOC-01 doc redirect + CR-REF-01..02 sprint CLI re-route + CR-REF-09 sprint TUI re-route|src/|FR-CS-4; S-1-in-flight-discharge|AC-ATK-15 Step-5 atomicity; AC-ATK-17 server-side pre-receive hook PASS; AC-SM-09 commit roster equality|L|P0|
|65|API-004|Sprint CLI emission site (sprint/process.py:170)|Pre-merge literal `f"/sc:task Execute all tasks in @{phase_file} "`; post-merge `f"/task Execute all tasks in @{phase_file} "`; AC-ATK-17 boundary contract grep|src/superclaude/cli/sprint/process.py|FR-CS-5|AC: pre-merge-literal:`/sc:task Exec`; post-merge-literal:`/task Exec`; assertion-1:prompt.startswith("/task Exec"); assertion-2:`/sc:task`-not-in-prompt|XS|P0|
|66|API-005|Cleanup-Audit Surface Scan emission (prompts.py:26)|Builder build_surface_scan_prompt; pre-merge `/sc:task Perform a surface-level scan ...`; post-merge `/task Perform a surface-level scan ...`; caller executor.py:197 (G-001)|src/superclaude/cli/cleanup_audit/prompts.py|FR-CS-5|AC: literal-swap-1-line; caller-executor.py:197-binding-G-001; assertion:prompt.startswith("/task ")|XS|P0|
|67|API-006|Cleanup-Audit Structural Analysis emission (prompts.py:47)|Builder build_structural_analysis_prompt; pre-merge `/sc:task Perform deep structural analysis ...`; post-merge `/task Perform deep structural analysis ...`; callers executor.py:211 (G-002), :228 (G-003)|src/superclaude/cli/cleanup_audit/prompts.py|FR-CS-5|AC: literal-swap-1-line; callers-G-002-G-003; assertion:prompt.startswith("/task ")|XS|P0|
|68|API-007|Cleanup-Audit Cross-Cutting emission (prompts.py:69)|Builder build_cross_cutting_prompt; pre-merge `/sc:task Detect duplication, sprawl, and consolidation ...`; post-merge `/task Detect duplication, sprawl, and consolidation ...`; caller executor.py:245 (G-004)|src/superclaude/cli/cleanup_audit/prompts.py|FR-CS-5|AC: literal-swap-1-line; caller-G-004; assertion:prompt.startswith("/task ")|XS|P0|
|69|API-008|Cleanup-Audit Consolidation emission (prompts.py:92)|Builder build_consolidation_prompt; pre-merge `/sc:task Consolidate audit findings ...`; post-merge `/task Consolidate audit findings ...`; caller executor.py:263 (G-005)|src/superclaude/cli/cleanup_audit/prompts.py|FR-CS-5|AC: literal-swap-1-line; caller-G-005; assertion:prompt.startswith("/task ")|XS|P0|
|70|API-009|Cleanup-Audit Validation emission (prompts.py:116)|Builder build_validation_prompt; pre-merge `/sc:task Validate audit findings ...`; post-merge `/task Validate audit findings ...`; caller executor.py:278 (G-006)|src/superclaude/cli/cleanup_audit/prompts.py|FR-CS-5|AC: literal-swap-1-line; caller-G-006; assertion:prompt.startswith("/task ")|XS|P0|
|71|API-014|Donor Command Stubification (CR-DEP-01)|Source line src/superclaude/commands/task.md:100; current `> Skill sc:task-protocol`; post-merge `> Skill task` (Form 1, synth-05 binding); 8 adjacent brand-name rewrites|src/superclaude/commands/task.md|FR-CS-5|AC: stubify-line-100-rewrite; adjacent-rewrites-lines-12-19-41-106-117-128-139-169; HTML-marker-preserve:SC:TASK-UNIFIED:CLASSIFICATION-verbatim|S|P0|
|72|FR-CS-6|Step 6: Donor skill hard-delete (atomic, S-3 binding)|CR-DEP-03 hard-delete donor SKILL.md + CR-DEP-04 directory absence + CR-DIST-02 sync rule; pre-commit gate AC-ATK-07 rf-qa F-07 verifier PASS + make verify-sync 0|src/|FR-CS-5|AC-ATK-07 chain verifier PASS; make verify-sync returns 0; donor sc-task-protocol/ absent both src/ and .claude/|L|P0|
|73|FR-CS-7|Step 7: Sprint/pipeline integrator fix-up|No runtime caller emits /sc:task post-stubification; pre-commit gate pytest pass + AC-ATK-17 server-side pre-push hook active|src/|FR-CS-5; FR-CS-6|pytest-PASS; AC-ATK-17 server-side hook active and tested|S|P0|
|74|NFR-S-1|In-flight discharge (population-generalized)|Any in-flight PRD/TDD task in .dev/tasks/ whose body references donor surfaces MUST complete before Step 5 OR be snapshot-frozen with decision record; --max-wait 14d default|.dev/tasks/|FR-CS-5|AC-ATK-08 three sub-bindings: (a) --max-wait-14d-arg; (b) scripts/embed_git_sha.py; (c) CR-DEP-05 grep extension|M|P0|
|75|NFR-S-2|CLI runtime atomicity|Step-5 commit MUST be atomic with CLI fix-forward; server-side push-policy enforcer on landing commit at master prevents rebase-split bypass H-2; grep scope src/superclaude/cli/{sprint,cleanup_audit}/**|.github/workflows/|FR-CS-5; FR-CS-7|AC-ATK-17 server-side pre-receive hook; fallback scripts/atomic_step_5.sh flock|S|P0|
|76|NFR-ME-9|DONOR-CEREMONY DROP AUDIT (Load-bearing)|10 named donor-ceremony drops remain dropped; rejected-pattern axis + surviving-citation axis (CR-DEP-06)|src/|FR-CS-5|CR-DEP-01 soft-deprecate; CR-DEP-05 audit; R-RULE-11 audit; AC-ATK-17|S|P0|
|77|TEST-006|AC-ATK-06 Donor diffs seven zero-diffs|tests/skills/task/test_cr_task_12_donor_diffs.py::test_seven_zero_diffs; 7 diff invocations zero against tests/fixtures/donor-blocks/*.txt|tests/|FR-CS-4|AC: 7-diffs-zero; gate:Step-4-pre-commit; fixtures-frozen-pre-Step-6|S|P0|
|78|TEST-008|AC-ATK-08 Git SHA embedding|tests/scripts/test_embed_git_sha.py::test_idempotent + tests/audit/test_cr_dep_05_grep.py::test_post_step5_stale_verification|tests/|NFR-S-1|AC: every-CODE-VERIFIED-tag-carries-git-sha-suffix; idempotent-script-execution|S|P0|
|79|TEST-009|AC-ATK-09 sha256 digests|tests/skills/task/test_cr_task_11_digest.py::test_sha256_matches_baseline|tests/|FR-CS-5|AC: 3-audit-digests-use-sha256-NOT-md5; baseline-pinned|S|P0|
|80|TEST-014|AC-ATK-14 CR-DEP-05 grep 4 sub-resolutions|tests/audit/test_cr_dep_05_grep.py::test_4_sub_resolutions|tests/|FR-CS-5|AC: (a)-grep-scope-correct; (b)-cluster-root-named; (c)-gate-at-Step-6-pre-commit; (d)-CR-DOC-13-scope-widened|S|P0|
|81|TEST-015|AC-ATK-15 CR-DOC-01 atomic Step-5|tests/audit/test_cr_doc_01_step.py::test_landed_with_dep_01|tests/|FR-CS-5|AC: Step-5-commit-roster-includes-commands/task.md+docs/user-guide/commands.md; Step-8-fallback-only-AUTHORIZE_HOT_FIX=1|S|P0|
|82|TEST-017|AC-ATK-17 Server-side pre-receive hook|tests/ci/test_pre_receive_hook.py::test_rebase_split_rejected; fabricate rebase-split commit pair; hook exits non-zero on intermediate broken state|tests/|NFR-S-2|AC: rebase-split-rejected-server-side; bypass-resistant-via-CI-not-local-hook|M|P0|
|83|TEST-027|AC-SM-09 Step-5 commit roster|tests/audit/test_step_5_commit_roster.py::test_exact_file_list; git log --name-only set-equal to final-merge-plan.md:375|tests/|FR-CS-5|AC: exact-file-list-match-final-merge-plan-line-375|S|P0|
|84|MIG-004|Step 4: Donor verbatim diff audit window|R-DRIFT-02 anchor patch applied to 3 artifacts + CR-TASK-12 anchors BEFORE this commit; CR-TASK-12 seven-diff audit fixture at tests/fixtures/donor-blocks/; AC-ATK-06 frozen-fixture snapshot script|tests/|FR-CS-4|CR-TASK-12 returns 7 zero-diffs (AC-SM-08 gate)|M|P0|
|85|MIG-005|Step 5: Soft-deprecation (S-2 atomic binding)|CR-DEP-01 + CR-DEP-02 + CR-DEP-05 + CR-DOC-01 + CR-REF-01..05 + In-flight target population frozen (S-1 binding); atomic commit|src/|FR-CS-5|AC-ATK-15 atomicity; AC-ATK-17 server-side hook PASS; AC-SM-09 commit roster equality|L|P0|
|86|OPS-A-3|Pre-commit gate Step-4 (verbatim diff audit)|`uv run pytest tests/skills/task/test_cr_task_12_donor_diffs.py` + R-DRIFT-02 patch verified|scripts/|MIG-004|AC: 7-zero-diffs; failure-disposition:investigate-anchor-drift-vs-content-drift|S|P0|
|87|OPS-A-4|Pre-commit gate Step-5 (atomic soft-deprecation)|`uv run pytest tests/sprint/ tests/cleanup_audit/ tests/cli/` + sha256 baseline + CR-DEP-05 grep 0|scripts/|MIG-005|AC: S-2-binding-enforced; commit-blocked-on-CLI-residual-OR-S-1-uncomplete|M|P0|
|88|OPS-A-5|Server-side push-policy hook (.github/workflows/push-policy.yml)|GitHub Actions workflow re-greps `/sc:task\b` against `src/superclaude/cli/**/*.py` on landing commit; rejects push if grep matches AND donor task.md deletion absent|.github/workflows/|NFR-S-2|AC: hook-fires-on-master-integration-push; bypass-resistant-via-CI-not-developer-hook; signed-commits-and-branch-protection-defense-in-depth|M|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|6 CLI emission sites|f-string literal swap|sprint/process.py:170 + cleanup_audit/prompts.py:26,47,69,92,116|M3|All sprint runs + cleanup-audit pipeline; AC-ATK-17 server-side grep|
|`/task` command stub|Stubified command file|src/superclaude/commands/task.md:100|M3|All `/sc:task` invocations post-Step-5; one-shot deprecation banner|
|.github/workflows/push-policy.yml|CI workflow|.github/workflows/|M3|Every push to master/integration; rejects rebase-split bypass|
|tests/cleanup_audit/test_prompts.py|Test module (NEW)|tests/cleanup_audit/|M3|AC-ATK-17 closure for cleanup-audit pipeline; 5 fixtures one per builder|
|sha256 baseline manifests|Digest files|tests/fixtures/digest-baselines/|M3|CR-DEP-02 audit; CR-TASK-11 audit; CR-DIST-02 mirror audit|
|CR-DEP-05 grep extension|Audit script|scripts/audit/|M3|Post-Step-5 stale-tag verification; CODE-VERIFIED tag drift detection|

### Milestone Dependencies — M3

- M2 close (TFEP cluster landed)
- R-DRIFT-02 anchor patch applied to 3 artifacts + CR-TASK-12 audit anchors (donor `:127-135` → `:133-135`)
- S-1 in-flight discharge attested: `TASK-PRD-20260514-121039` LIVE 258 refs + `TASK-TDD-20260514-121250` LIVE + broader 136-file population EITHER complete OR snapshot-frozen OR `--max-wait 14d` expiry auto-invoke option (b)
- Q-GAP-07 donor-block fixtures authored at `tests/fixtures/donor-blocks/{TU2_path,TU2_redirect,TU6_prohibitions,TU6_carve_outs,TU7_triggers,TU8_schema,CR7_sentinel}.txt`
- Q-GAP-01 `tests/cleanup_audit/test_prompts.py` authored (asymmetric closure with `tests/sprint/test_process.py:80-89`)
- Q-GAP-08 `docs/condensation-table.md` authored (per AC-ATK-04)
- Q-GAP-09 server-side pre-receive hook hosting decision (GitHub Actions vs self-hosted)

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-R-DRIFT-02|LOW (mechanical): donor anchor `:127-135` should be `:133-135` (anchor off-by-2). Content verbatim is preserved. Patch single-source: replace in 3 artifacts + CR-TASK-12 audit anchors.|Pre-Step-4 audit window blocker; CR-TASK-12 may erroneously fail|Documentation/Release Owner (patch task)|Before M3 Step-4 commit|
|2|Q-GAP-01|`tests/cleanup_audit/test_prompts.py` absence — spec under-counts CLI emission sites by 5/6 (cleanup_audit/prompts.py L26,47,69,92,116 not named in spec §7.2). 5 NEW test fixtures must be authored.|Blocks AC-ATK-17 closure for cleanup-audit pipeline|Engineering Lead (CR-DEP-05 author)|Before M3 Step-5 commit|
|3|Q-GAP-09|Server-side pre-receive hook hosting (per AC-ATK-17). Assumes GitHub Actions OR self-hosted-git pre-receive availability. GitHub.com lacks pre-receive; defense-in-depth via Actions + branch-protection-required-checks + signed-commits + code-owners review.|Blocks AC-ATK-17 server-side enforcement; defense-in-depth substitution required|Engineering Lead / DevOps|Before M3 Step-5 push-time|
|4|Q-GATE-1-5-TOKEN-COLLISION|Open: Pin grammar `gate-1.5: <subtype> ...` with closed subtype set to disambiguate AC-ATK-18(b) `legacy-surface-reference` from existing CR-TASK-06 `pre-flight` token.|Blocks AC-ATK-18 emission grammar; defers to M4 if not resolved at M3|Engineering Lead / §7-§8 author|Before M4 (acceptable to defer past M3)|

### Risk Assessment and Mitigation — M3

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-ATK-17: Local pre-push bypassable via --no-verify|HIGH|HIGH|Rebase-split intermediate SHA carries stubified /sc:task in task.md but live emission in 6 CLI sites; sprint runs pinned to that SHA fail|Server-side push-policy hook at .github/workflows/push-policy.yml (AC-ATK-17); branch protection + signed commits + code-owners review on src/superclaude/cli/** as defense-in-depth (GitHub.com gap)|Engineering Lead / DevOps|
|2|R-DRIFT-02: Donor anchor off-by-2 (`:127-135` → `:133-135`) in 3 artifacts + CR-TASK-12 audit|LOW|HIGH|CR-TASK-12 verbatim-diff erroneously blocks Step-4 audit; Step-5 cannot land|Pre-Step-4 patch single-source 3 artifacts + CR-TASK-12 audit anchors; verify against on-disk donor file|Documentation/Release Owner|
|3|R-S-2: Step 5 atomic flaky pytest no-progress (FM-02)|MEDIUM|MEDIUM|Pytest flakes intermittently; atomicity creates no-progress state; commit cannot land but soft-deprecation authored locally|Pin env vars per FM-04; CI gate sign-off; explicit rollback policy `git checkout HEAD -- <files>` on Step-5 pre-commit failure; retry budget 3 before HALT|Engineering Lead|
|4|R-S-1: Live in-flight tasks reference donor surfaces (`TASK-PRD-20260514-121039` 258 refs + `TASK-TDD-20260514-121250` LIVE + 136-floor population)|HIGH|HIGH|Step 5 stalls indefinitely if `--max-wait 14d` enforcer not authored; H-1 scenario condition live across multiple tasks|AC-ATK-08 14d default + auto-invoke option (b) snapshot-freeze; pinned-SHA discipline on `[CODE-VERIFIED]` tags via scripts/embed_git_sha.py; weekly review of in-flight set|Engineering Lead|

## M4: Donor Hard-Delete + Flock-Guarded Sync (S-3 Atomic)

**Objective:** Land Step 6 atomic hard-delete: remove donor `src/superclaude/skills/sc-task-protocol/SKILL.md` (CR-DEP-03), `make sync-dev` prune to `.claude/skills/` (CR-DEP-04), CR-DIST-02 sync rule update under flock-guarded `make sync-dev` + `make verify-sync` (AC-ATK-16 closing H-3 worktree race + live copy-overwrite race), and emit CR-DEP-06 one-shot residual-reference manifest enumerating 144 surviving deprecation-surface strings across 40+ files with per-bucket disposition. Pre-commit gate: rf-qa F-07 chain-integrity verifier returns PASS before destructive hard-delete fires. AC-ATK-18 semantic-layer resume-time content audit (`gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>`) activates from this milestone onward at every in-flight task resume across the 136-file floor. | **Duration:** Week 3.5 (T+15d to T+17d; 2026-05-31 → 2026-06-02) | **Entry:** M3 close; rf-qa F-07 chain verifier authored and ready; CR-DEP-06 manifest emitter script ready; flock portability fallback documented (Q-GAP-04) | **Exit:** AC-SM-10 Step-6 commit roster PASS; `make verify-sync` returns 0; donor `sc-task-protocol/` directory absent from both `src/` and `.claude/`; CR-DEP-06 manifest residual count outside authorized buckets = 0

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|89|FR-CR-DEP-06|Post-Step-6 one-shot residual-reference manifest (elevated Must)|Post-Step-6 script scripts/audit/cr_dep_06_manifest.sh writes ${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml} enumerating every surviving deprecation-surface string outside authorized leave-as-is buckets with per-string disposition; pre-commit gate residual count outside authorized buckets MUST equal zero|scripts/audit/|FR-CS-6|AC-ATK-18(d) one-shot post-Step-6 manifest; AC-ATK-14(a) CR-DEP-05 grep spec; 144→0 residuals outside authorized buckets|M|P0|
|90|FR-CS-9|Step 9: Leave-as-is enforcement across buckets|Buckets A, C, D, E, F, G, H; CR-REF-12 scoped to [src] + [.claude]; CR-REF-18 DEPRECATION-NOTE.md cluster root check|src/|FR-CS-6|bucket-grep returns zero unauthorized residuals; CR-DEP-06 manifest scoped|S|P0|
|91|DM-005|Gate-1.5 Emission Token schema (Schema 5, polymorphic, AC-ATK-18)|Emission-only Task Log lines; cardinality 0..N per resume; single polymorphic schema with two variants discriminated by event token (NOT 6th canonical schema)|Task Log|FR-CS-6|AC: storage:emission-only-no-disk-persistence; cardinality:0..N-per-resume; variant-A:legacy-surface-reference; variant-B:deleted-related-doc; folding-decision:single-schema-with-token-type-discriminator-Q-GATE-1-5-SCHEMA-resolved|S|P0|
|92|NFR-S-3|Makefile sync-rule atomicity with flock|make sync-dev + make verify-sync MUST acquire exclusive flock on .claude/skills/.sync-lock; covers (a) forward-looking prune-loop race AND (b) LIVE copy-overwrite race at Makefile:121|Makefile|FR-CS-6|AC-ATK-16 pytest concurrency fixture; KPI target 0 flakes across 30 consecutive CI runs|S|P0|
|93|NFR-INV-4b|Resumability — semantic layer (HIGHEST EXPOSURE)|Meaningful resume path through in-flight checklist body MUST survive merge; content-level deprecated-surface references detected at resume; executor emits Gate-1.5 token; one-shot ack gate; continue execution (warn-and-continue per ME-3, NOT HALT)|task/SKILL.md|FR-CS-6; DM-005|AC-ATK-18 four sub-bindings: (a) content-layer grep at resume; (b) sprint-emit boundary content-grep; (c) one-shot ack gate via legacy-surface-ack:1; (d) CR-DEP-06 manifest|M|P0|
|94|TEST-016|AC-ATK-16 Make sync-dev flock|tests/audit/test_make_sync_dev_flock.py::test_concurrent_worktree; 2 parallel make sync-dev subprocesses; flock held during prune|tests/|NFR-S-3|AC: 2-parallel-make-sync-dev; flock-held-during-prune; post-prune-find-type-d-match-expected; 0-flakes-30-CI-runs|S|P0|
|95|TEST-018|AC-ATK-18 Resume content audit + sprint-emit + manifest|tests/skills/task/test_cr_fm_03_resume_grep.py + tests/cli/test_sprint_emit_legacy_grep.py + tests/audit/test_cr_dep_06_manifest.py|tests/|DM-005; FR-CR-DEP-06|AC: (a) Gate-1.5 emission canonical grammar; (b) sprint-emit blocks on content match; (c) post-Step-6 manifest enumerates >=144 residuals|M|P0|
|96|TEST-028|AC-SM-10 Step-6 commit roster|tests/audit/test_step_6_commit_roster.py::test_exact_file_list|tests/|FR-CS-6|AC: git-log-name-only-Step-6-commit-set-equal-final-merge-plan-line-381|S|P0|
|97|TEST-030|AC-SM-12 Step gates + in-flight resume|tests/audit/test_step_gates.py + tests/skills/task/test_in_flight_mdtm_resume.py::test_step_1_gate_zero + test_step_5_gate_zero + test_step_6_gate_zero + test_live_inflight_mdtm_resume_clean|tests/|NFR-INV-4b|AC: gates-1-5-6-exit-zero; fixture-iterates-LIVE-in-flight-count-at-gate-execution-time-NOT-hardcoded-25-96-132; 100pct-resume-clean-under-CR-FM-03-shim|M|P0|
|98|MIG-006|Step 6: Hard-delete (S-3 atomic binding)|CR-DEP-03 donor SKILL.md hard-delete; CR-DEP-04 directory absence + make sync-dev prune; AC-ATK-07 rf-qa F-07 chain verifier PASS pre-hard-delete; AC-ATK-16 flock guard; CR-DEP-06 residual manifest|src/|FR-CS-6|AC-SM-10 commit roster PASS; make verify-sync 0; donor directory absent both src/ and .claude/; CR-DEP-06 residual count outside authorized buckets=0|L|P0|
|99|MIG-009|Step 9: CR-DEP-06 residual manifest one-shot|Post-Step-6 one-shot residual-reference manifest finalized; AC-ATK-18(d) closure|.dev/releases/|FR-CR-DEP-06|Manifest archived to docs/generated/; weekly re-emit cadence established|S|P0|
|100|MIG-FF-3|Feature flag: gate-1.5 legacy-surface content audit (AC-ATK-18)|Always-on; indefinite (semantic-layer INV-04 guarantee); one-shot acknowledgment gate per resume entry|task/SKILL.md|DM-005|AC: always-on; indefinite-no-cleanup-date; one-shot-ack-per-resume-entry; ME-3-warn-continue-NEVER-HALT|S|P0|
|101|MIG-FF-4|Feature flag: Server-side pre-push hook (AC-ATK-17)|Activates at Step 8; indefinite (CLI surveillance)|.github/workflows/|OPS-A-5|AC: activates-Step-8; indefinite; grep-scope-src/superclaude/cli/{sprint,cleanup_audit}/**; word-boundary-regex|XS|P0|
|102|OPS-EM-7|Task Log emission AC-ATK-18 legacy-surface-reference (Variant A)|`gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` per content-grep match at resume time|task/SKILL.md|DM-005|AC: surface-enum:{/sc:task,sc-task-protocol,task-unified}; action:warn-and-continue-literal-NEVER-refuse-entry; emission-per-match|S|P0|
|103|OPS-EM-8|Task Log emission AC-ATK-18 deleted-related-doc (Variant B)|`gate-1.5: deleted-related-doc file=<path> action=warn-and-continue referenced_from=<path>` per related_docs frontmatter ENOENT traversal|task/SKILL.md|DM-005|AC: action:warn-and-continue; referenced_from-field-required; emission-per-ENOENT|S|P0|
|104|OPS-EM-9|One-shot acknowledgment gate|Single user-facing acknowledgment per resume entry recorded as `gate-1.5: ack received user=<id> ts=<ISO-8601>`; idempotent within ack-token-set state|task/SKILL.md|DM-005|AC: one-shot-per-resume-entry-NOT-per-emission-line; idempotent; NEVER-HALT-trigger; advisory-only|S|P0|
|105|OPS-A-6|Pre-commit gate Step-6 (hard-delete + flock)|`make verify-sync && AC-ATK-07 rf-qa F-07 verifier PASS && find src/superclaude/skills/sc-task-protocol/ -type d|grep -q 'No such file' && find .claude/skills/sc-task-protocol/ -type d|grep -q 'No such file' && CR-DEP-05 grep returns zero on both [src] and [.claude]`|scripts/|MIG-006|AC: S-3-enforcement-boundary; destructive-by-default; block-if-mirror-sync-drift-OR-rf-qa-PASS-fails-OR-donor-persists|M|P0|
|106|OPS-A-7|CR-DEP-06 manifest emitter script (scripts/audit/cr_dep_06_manifest.sh)|One-shot post-Step-6 script; greps {`/sc:task\b`, `sc-task-protocol`, `task-unified`} outside authorized buckets; emits {md,yaml} with per-string disposition|scripts/audit/|FR-CR-DEP-06|AC: 144-residuals-enumerated-with-per-bucket-disposition; outside-authorized-buckets-count=0; weekly-re-emit-cadence|S|P0|
|107|OPS-A-8|`flock` portability fallback (Q-GAP-04)|macOS / BSD lacks flock(1); `brew install flock` OR fallback `lockfile-create` from procmail-lockfile; documented in Makefile header and CLAUDE.md|Makefile|NFR-S-3|AC: flock-installed-via-brew-on-macOS; lockfile-create-fallback-on-BSD; WSL2-uses-Linux-semantics; documented-in-Makefile-header-and-CLAUDE.md|XS|P0|
|108|OPS-R-1|R5 Runbook — In-flight resume triage|Post-merge resume of in-flight MDTM task (136-file floor); may emit Gate-1.5 token, may ENOENT on related_docs paths|docs/runbooks/|MIG-FF-3|AC: 5-step-procedure:CR-FM-03-shim+content-grep+related_docs-traversal+warn-continue+escalation-4h-if-parser-bug|S|P0|
|109|OPS-R-2|R2 Runbook — Gate-1.5 emission triage|Task resume emits gate-1.5 legacy-surface-reference detected; diagnose token grammar + ack state + manifest disposition|docs/runbooks/|MIG-FF-3|AC: 3-step-diagnosis; resolution:one-shot-ack-NEVER-HALT-per-ME-3; escalation-30min-if-bucket=src|S|P0|
|110|OPS-R-3|R3 Runbook — Tier mis-classification recovery|Item executes under wrong tier; diagnose frontmatter + per-item marker + 3-level fallback + Task Log dispatch|docs/runbooks/|MIG-001|AC: 4-step-diagnosis; resolution:log-incident-fix-canonicalization-page-Engineering-Lead-1h-if-parser-bug|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`make sync-dev` flock-guarded prune|Makefile target wrapper|.claude/skills/.sync-lock|M4|Every `make sync-dev` invocation; concurrent worktree safe|
|CR-DEP-06 residual manifest|Audit output file|${RELEASE_DIR}/cr-dep-06-residual-manifest.{md,yaml}|M4|Post-Step-6 audit; archived weekly to docs/generated/|
|`gate-1.5: legacy-surface-reference` emission|Task Log emission point|F1 entry (resume time)|M4|All resumed in-flight tasks across 136-file floor|
|`gate-1.5: deleted-related-doc` emission|Task Log emission point|F1 entry related_docs traversal|M4|All resumed tasks with related_docs frontmatter|
|One-shot ack gate|Acknowledgment-token state|task frontmatter `legacy-surface-ack: 1`|M4|All in-flight resumed tasks; idempotent within ack-state|
|rf-qa F-07 chain-integrity verifier|Subagent invocation|Pre-Step-6 commit gate|M4|Step-6 pre-commit gate; AC-ATK-07 PASS required pre-hard-delete|

### Milestone Dependencies — M4

- M3 close (CLI re-route + donor stubification atomic)
- AC-ATK-07 rf-qa F-07 chain-integrity verifier authored and tested
- CR-DEP-06 manifest emitter script (`scripts/audit/cr_dep_06_manifest.sh`) authored
- `flock` portability fallback documented (Q-GAP-04 macOS `brew install flock` OR BSD `lockfile-create` OR WSL2 Linux semantics)

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-GAP-04|`flock` portability. `flock` is GNU-coreutils only. macOS/BSD lacks `flock(1)` by default. Either require `brew install flock` or fallback to `lockfile-create` from `procmail-lockfile`. AC-ATK-16 binding must specify portable invocation.|Blocks AC-ATK-16 closure on macOS/BSD; needs Makefile header documentation + CLAUDE.md note|Engineering Lead|Before M4 commit|
|2|Q-GATE-1-5-SCHEMA|6th Gate-1.5 schema decision: identifies a third emission token `gate-1.5: deleted-related-doc` (ENOENT on related_docs paths). Decide: author as 6th canonical schema OR fold into Schema 5 as additional `surface=` value. Recommendation: fold-into-Schema-5 with token-type discriminator.|Affects DM-005 schema commit; decision implemented as polymorphic Variant A/B; resolved at M4 commit|§7 author|Before M4 commit|

### Risk Assessment and Mitigation — M4

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-OPS-02: H-4 manual operator intervention — surviving in-flight target `TASK-RESEARCH-20260403-sprint-task-exec` (48 occurrences across 10 files in subtree)|MEDIUM|HIGH|Subagent acting on legacy-surface-reference may silently degrade post-Step-6; FileNotFoundError on Read of deleted donor file|AC-ATK-18 + pre-flag at-risk task ID + operator runbook (OPS-R-1); first-resume acknowledgment gate idempotent|Engineering Lead|
|2|R-FM-08: Donor file-rename evasion (`*.deprecated` rather than deleted bypasses absence check)|LOW|MEDIUM|R-RULE-11 violation indirect; CR-DEP-04 absence check passes but donor file persists|CR-DEP-04 enforces directory absence not just file absence; `git diff --diff-filter=D` assertion on Step-6 commit verifies inode deleted not renamed; reject any `*.deprecated` artifact|Engineering Lead|
|3|R-FM-01: Symlink defeat of `make verify-sync` — `[.claude]` symlinked to `[src]` (defeats R-RULE-10)|LOW|HIGH|md5sum/sha256sum/content checks pass trivially; sync verification silently false-positive|Pre-Step-6 audit: `find -type l` returns empty in both .claude/skills and src/superclaude/skills; require manual find audit pre-merge|Engineering Lead|
|4|R-FM-03: Parallel subagent SKILL.md conflict — same-file in-tree concurrent edits|MEDIUM|MEDIUM|Two implementation sub-agents land conflicting edits to SKILL.md at row 1 vs row 10|Ban parallel parallel subagent dispatch on `task/SKILL.md` during Step 5/Step 6; single-executor discipline during merge window|Engineering Lead|

## M5: Validation, Manifest, Docs, Audit Closure

**Objective:** Land Steps 7-10 production-readiness work: invariant-survival walkthrough audit (AC-SM-03 + AC-SM-04 with R-DOC-01 content-audit cross-checks against on-disk artifacts), documentation rollup (CR-DOC-02..09, CR-DOC-11 partial) with mkdocs build returning 0 broken-link warnings, deferred-regen initial + frozen-pre-merge banner for `docs/generated/*` (FR-CS-10), AC-SM-01..12 audit closure on clean checkout, K-01..K-08 KPI baseline measurements, and final R-RULE-11 audit clean. This milestone closes Phase 7.5 — all 18 AC-ATK rows in PASS state, all 12 AC-SM rows verified or downgraded per R-DOC-01 reframe, 144→0 residuals outside authorized buckets confirmed via CR-DEP-06 manifest. CR-FM-03 shim sunset audit row (CR-AUDIT-FM-03-SUNSET) authored with binding N. Server-side AC-ATK-17 hook remains active indefinitely as CLI surveillance. | **Duration:** Week 4 (T+17d to T+27d; 2026-06-02 → 2026-06-12) | **Entry:** M4 close (donor hard-delete + flock-guarded sync atomic landed) | **Exit:** All 18 AC-ATK + 12 AC-SM PASS; K-01..K-08 baseline measured; Phase 7.5 traceability matrix returns zero OPEN/PARTIAL rows; release-readiness gate passed

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|111|FR-CS-8|Step 8: Documentation rollup + mkdocs build|CR-DOC-01 fallback (only if Step-5 gate failed with AUTHORIZE_HOT_FIX=1) + CR-DOC-13 R-RULE-11 scope; mkdocs build returns 0 broken-link warnings|docs/|FR-CS-7|mkdocs build 0 warnings; FM-05 caveat mkdocs version pinned pre-Step-8|S|P0|
|112|FR-CS-10|Step 10: Deferred-regen initial + frozen-pre-merge banner|docs/generated/* deferred-regen initial with banner string in every file referencing /sc:task OR sc-task-protocol|docs/generated/|FR-CS-6; FR-CS-8|Banner present in all files; FM-06 deferred-regen risk acknowledged|XS|P0|
|113|TEST-019|AC-SM-01 V/C/K byte-match|tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match; 8/8 V/C/K verdicts identical byte-for-byte|tests/|M4-close|AC: 8/8-VCK-verdicts-byte-identical-against-transfer-manifest-§4-CONTENT-AUDIT-PASS|S|P0|
|114|TEST-020|AC-SM-02 ME traceability|tests/audit/test_me_traceability.py::test_each_me_has_cr_row; for ME ∈ {1..9}, >=1 grep hit in final-merge-plan.md §5 OR §6|tests/|M4-close|AC: 9-MEs-trace-to-CR-rows-each|S|P0|
|115|TEST-021|AC-SM-03 Invariant walkthrough|tests/audit/test_invariant_walkthrough.py::test_inv_1_through_5_re_readable; 5 paragraphs one per INV-01..INV-05|tests/|M4-close|AC: 5/5-INVs-re-readable-with-worked-example-anchor; INV-01-monotonic-progress; INV-02-F2-additivity; INV-03-rf-qa-floor; INV-04-resumability-2-layer; INV-05-refusal-of-definition|S|P0|
|116|TEST-022|AC-SM-04 F-findings cite anchors|tests/audit/test_f_findings_cite_anchors.py::test_each_f_row_has_artifact_anchor; for F ∈ {01..08}, >=1 line-range cite|tests/|M4-close|AC: 8-F-rows-cite-valid-Phase-7-artifact-line-ranges|S|P0|
|117|TEST-023|AC-SM-05 S-constraints cite HZ|tests/audit/test_s_constraints_cite_hz.py::test_s_1_cites_hz03 + test_s_2_cites_hz06_hz07 + test_s_3_cites_hz14|tests/|M4-close|AC: 3/3-S-rows-cite-HZ-NN-named-hazards|S|P0|
|118|TEST-024|AC-SM-06 Row + step counts|tests/audit/test_row_and_step_counts.py::test_67_rows_in_master + test_10_steps_in_sequence|tests/|M4-close|AC: 67-row-line-items-merge-master-§1; 10-commit-steps-sequence|S|P0|
|119|TEST-026|AC-SM-08 CR-TASK-12 seven-diff|tests/skills/task/test_cr_task_12_donor_diffs.py::test_6_donor_plus_1_sentinel|tests/|M4-close|AC: 7-diffs-return-zero-6-donor-strings+1-sentinel-comment-block|S|P0|
|120|TEST-029|AC-SM-11 Zero ledger re-proposal|tests/audit/test_no_rejected_re_proposal.py::test_zero_ledger_re_introductions|tests/|M4-close|AC: 0-N-ledger-entries-LR-REJECT-appear-as-binding-rows-in-final-merge-plan-§5|S|P0|
|121|TEST-004|AC-ATK-04 Condensation table|tests/audit/test_condensation_table.py::test_79_to_67_to_65; 6 bucket rows sum to 79 row-instances → 65 distinct CR-IDs → 67 PASS-line-items; names 2 duplicate CR-IDs|tests/|FR-CS-8|AC: 79-to-65-condensation-table-published-2-duplicate-CR-IDs-named|S|P0|
|122|MIG-007|Step 7: Invariant survival walkthrough audit|AC-SM-03 walkthrough re-read (5 of 5 INVs); AC-SM-04 8 of 8 F-rows cite valid line ranges; Q-2 content audit complete (downgrades R-DOC-01)|docs/|FR-CS-6|All 5 INV walkthrough paragraphs present and re-readable; F-findings citations valid against on-disk artifacts|M|P0|
|123|MIG-008|Step 8: Documentation rollup|CR-DOC-02..09, CR-DOC-11 partial; mkdocs build returns 0 broken-link warnings; CR-DOC-13 R-RULE-11 audit clean; FM-05 mkdocs version pin recommended pre-Step-8|docs/|FR-CS-8|mkdocs version pinned; build 0 warnings; CR-DOC-13 audit clean|S|P0|
|124|MIG-010|Step 10: Audit closure|CR-DOC-10..12 final; CR-DEFER-T06.04 ack; AC-SM-01..12 audits re-run from clean checkout; K-01..K-08 baseline measurements taken|tests/audit/|MIG-007; MIG-008|AC: all-AC-SM-PASS-or-CONTENT-AUDIT-resolved; K-01..K-08-baseline-measured; clean-checkout-audit-PASS|M|P0|
|125|OPS-002|OPS-001 Critical Path Override Invocation Runbook (R1)|F1 dispatched to STRICT for item under auth/security/crypto/models/migrations/ despite frontmatter Tier=LIGHT/EXEMPT|docs/runbooks/|MIG-001|AC: 3-step-diagnosis; resolution:honor-override-STRICT-wins; escalation-rf-qa-1h+Engineering-Lead-4h; prevention:operator-training+sentinel-AST-grep-Step-4|S|P0|
|126|OPS-003|OPS-004 TFEP Escalation Handling Runbook (R4)|F-05 authorized TFEP-escalation invocation logged; baseline classifies >=1 new-test fail|docs/runbooks/|MIG-003|AC: 4-step-diagnosis; baseline-state-4-state-observer+TFEP-incident-report+carve-out-classification+prohibition-disposition-matrix; escalation-rf-qa-30min|S|P0|
|127|OPS-005|On-Call Expectations|rf-qa primary (Phase-Gate QA + post-completion + TFEP escalation); Engineering Lead secondary (parser bugs, S-1/S-2/S-3 atomicity violations, V3 security-probe regressions); DevOps (CI hook failures, server-side pre-receive misfires)|docs/runbooks/|MIG-006|AC: expected-page-volume:<2/week-steady-state; rf-qa-ack-15min+mitigate-60min; Engineering-Lead-ack-30min+5min-atomicity-violations; DevOps-ack-30min|S|P0|
|128|OPS-A-9|Pre-commit gate Step-7 (walkthrough audit)|AC-SM-03 walkthrough fixture pass + AC-SM-04 F-row citation audit|scripts/|MIG-007|AC: 5/5-INVs-walkthrough-PASS; 8/8-F-rows-cite-anchors-PASS|S|P0|
|129|OPS-A-10|Pre-commit gate Step-8 (docs + mkdocs)|`mkdocs build` returns 0 broken-link warnings AND pre-push hook installed AND landing commit re-grep returns zero `/sc:task` in CLI sources|scripts/|MIG-008|AC: mkdocs-0-warnings; pre-push-active; FM-05-mkdocs-version-pinned-in-commit-msg|S|P0|
|130|OPS-A-11|Pre-commit gate Step-10 (audit closure)|R-RULE-11 audit clean (zero ledger entries re-proposed) AND K-01..K-08 measurement pass|scripts/|MIG-010|AC: 0-ledger-re-introductions; K-01-K-08-baseline-measured-and-recorded|S|P0|
|131|OPS-AL-1|Alert: Pre-receive hook reject on master/integration push|Critical — author re-composes commit (atomic CR-DEP-01 + CR-DOC-01 + CR-REF-01..05); re-push|.github/workflows/|MIG-FF-4|AC: alert-severity:critical; response:author-re-compose-commit|XS|P0|
|132|OPS-AL-2|Alert: Step-5 pre-commit gate fail|Critical — author fixes failing tests; hot-fix Step-8 fallback requires AUTHORIZE_HOT_FIX=1|scripts/|OPS-A-4|AC: alert-severity:critical; hot-fix-gated-by-AUTHORIZE_HOT_FIX=1-env-var|XS|P0|
|133|OPS-AL-3|Alert: Resume legacy-surface match|Warning — operator acknowledges via one-shot ack gate (idempotent)|task/SKILL.md|OPS-EM-7|AC: alert-severity:warning; resolution:one-shot-ack-gate-idempotent|XS|P0|
|134|OPS-AL-4|Alert: `make verify-sync` non-zero|Critical — run make sync-dev; re-verify; manual reconcile under R-RULE-10 if diff persists|Makefile|NFR-S-3|AC: alert-severity:critical; resolution:sync-dev+re-verify+manual-reconcile-R-RULE-10|XS|P0|
|135|OPS-CP-1|Capacity Planning — In-flight MDTM file count|136→200-300 (6mo)→400-600 (12mo); scaling trigger emission rate >10/day → batch ack pass|docs/runbooks/|MIG-FF-3|AC: scaling-trigger-defined; capacity-bounds-6mo-12mo; batch-ack-pass-pattern|XS|P0|
|136|OPS-CP-2|Capacity Planning — CR-DEP-06 residual manifest entries|144→50-100 (6mo)→<50 (steady state); audit if residual count grows post-Step-6|.dev/releases/|FR-CR-DEP-06|AC: capacity-bounds-6mo-steady-state; alert-if-growth-post-Step-6|XS|P0|
|137|MIG-FF-5|CR-AUDIT-FM-03-SUNSET row authored|Audit row binding CR-FM-03 shim sunset condition; recommendation `N=50 generations AND ≥90 days post Step 6 AND CR-MIGR-FM-03 authored`; emitted every resume via gate-1.4|src/|OQ-FM-03-SUNSET|AC: sunset-condition-N-bound-and-published; gate-1.4-shim-status-line-tracks-N-countdown|S|P0|
|138|OPS-EM-10|Task Log emission CR-FM-03 sunset audit (gate-1.4)|`gate-1.4: shim-status surface=CR-FM-03 generations_remaining=<N> sunset_row_authored=<bool>` per resume|task/SKILL.md|MIG-FF-5|AC: emission-per-resume; sunset-countdown-visible; co-removed-with-shim|XS|P0|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|mkdocs build CI gate|CI workflow|.github/workflows/|M5|Every push touching docs/; FM-05 version pin required|
|CR-AUDIT-FM-03-SUNSET row|Audit-row registry|src/superclaude/skills/task/rules/|M5|All resume paths; gate-1.4 emission per resume|
|K-01..K-08 KPI dashboard|Measurement records|.dev/releases/current/task-sc-task-directional-merge/kpi-baseline.md|M5|Post-Phase-7.5 release-readiness review|
|R-RULE-11 audit clean|Audit-output snapshot|.dev/releases/current/task-sc-task-directional-merge/r-rule-11-audit.md|M5|Step-10 commit gate|
|Phase 7.5 traceability matrix|Spreadsheet/markdown|.dev/releases/current/task-sc-task-directional-merge/traceability-matrix.md|M5|Final release sign-off|

### Milestone Dependencies — M5

- M4 close (donor hard-delete + flock-guarded sync atomic landed)
- All M1..M4 pre-commit gates returned 0
- AC-ATK-01..18 all in PASS or PARTIAL state with documented residuals
- R-DOC-01 content audit completed (recommended; defers to per-row R-DRIFT-NN findings if drift discovered against on-disk artifacts)

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|Q-R-DOC-01|Downgrade candidate: originally framed as "7 absent upstream artifacts"; fix-cycle 2 confirms all 7 named artifacts PRESENT at `.dev/releases/current/task-sc-task-directional-merge/artifacts/`. Recommendation: downgrade R-DOC-01 from "artifact gaps" to "artifact-content verification owed" with cascading downgrade of `[ARTIFACT-ABSENT]` flags on AC-SM-01,-03,-04,-05,-06,-07,-09,-10,-11,-12 to `[CONTENT-AUDIT-OWED]`.|Affects AC-SM closure flags; 7 rows promotable to `[CODE-VERIFIED]` immediately, 5 rows remain `[UNVERIFIED]` pending POST-MERGE state|Documentation/Release Owner|Before M5 Step-7 commit|
|2|OQ-F-NN-BIJECTION|Confirm canonical F-NN ↔ TU-NN bijection once `final-merge-plan.md` content audit completes. Pre-Phase-7 obligation.|Blocks AC-SM-04 final pairing verification; defers to post-content-audit per Q-R-DOC-01|Engineering Lead|Before M5 Step-7 commit|
|3|Q-GAP-12|Schema-version uniformity. Schema 3 includes `schema_version: 1`; no other schema does. Decide whether all 5 schemas adopt a uniform version field.|Affects DM-001..005 schema versioning posture; pre-publish design choice|§7 author|Pre-publish (M5 close)|

### Risk Assessment and Mitigation — M5

|#|Risk|Severity|Likelihood|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|1|R-DOC-01: Anchor artifact content drift between PRD claims and on-disk artifacts|MEDIUM|MEDIUM|AC-SM-01,-03,-05,-06,-11 cross-checks fail; per-row R-DRIFT-NN findings surface|Pre-Step-7 content audit; reconcile any drift as per-row R-DRIFT-NN findings; do not block Phase 7.5 on resolution unless drift invalidates load-bearing claim|Documentation/Release Owner|
|2|R-FM-05: mkdocs version drift — broken-link semantics could pass or fail same source tree|MEDIUM|MEDIUM|Step-8 gate passes locally but fails CI or vice-versa|Pin mkdocs version in pyproject.toml/docs/requirements.txt pre-Step-8; record version in commit msg|Engineering Lead|
|3|R-FM-06: docs/generated/* regen unscheduled — permanently disagrees with docs/ source (83 occurrences live)|MEDIUM|HIGH|Generated docs frozen pre-merge state diverges from canonical source indefinitely|CR-DEP-06 manifest archives weekly to docs/generated/; investigate regen scheduler; FR-CS-10 banner string in every affected file|Engineering Lead|
|4|R-FM-07: UTF-16 grep evasion — auditor scripts may miss UTF-16-authored markdown|LOW|LOW|Adversarial-or-accidental UTF-16 in recipient surface evades grep-based audit class|Surfaced as TDD §22 gap (Q-GAP-N); document UTF-8-only authoring discipline; `file -i` pre-grep encoding check Phase 7.5.b|Engineering Lead|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|`git` binary on every executing host (system PATH ≥2.0)|M1, M2, M3, M4, M5|Live|Graceful-skip per ME-3 (warn-and-continue, NEVER HALT — INV-01); operator manual fallback for delete|
|`uv` runtime (project-pinned)|M1, M2, M3, M4, M5|Live|None — hard project requirement per CLAUDE.md|
|`pytest` (via `uv run pytest`)|M1, M2, M3, M4, M5|Live|Pin env vars (PYTHONHASHSEED, locale, timezone) per FM-04; CI gate sign-off|
|`pyyaml` (frontmatter parsing + baseline YAML + incident schema)|M2, M3, M4|Live|Conservative over-escalate per AC-CR-TASK-09-F04; never refuse task entry|
|`click` (≥8.0.0) CLI entry points|M3 (CLI re-route)|Live|None — hard project requirement|
|`rich` CLI terminal output rendering|M3|Live|Plain stdout fallback|
|`mkdocs` (build only)|M5 Step-8 gate|Live (FM-05 risk: unpinned)|Pin mkdocs version in pyproject.toml/docs/requirements.txt before Step 8|
|`flock(2)` / POSIX file-locking|M4 (AC-ATK-16)|Linux native; macOS/BSD gap|`brew install flock` on macOS; `lockfile-create` from procmail-lockfile on BSD; WSL2 uses Linux semantics|
|`sha256sum` (or `shasum -a 256`)|M3, M4|System PATH universal POSIX|`openssl dgst -sha256` fallback|

### Infrastructure Requirements

- Server-side CI workflow hosting: `.github/workflows/push-policy.yml` for AC-ATK-17 server-side pre-receive enforcement (GitHub Actions free tier OR self-hosted git pre-receive on enterprise)
- Pre-commit hook infrastructure: `.pre-commit-config.yaml` exists; `.git/hooks/` currently contains only `*.sample` (no active enforcement) — server-side hook is the structural barrier (NOT bypassable via `git commit --no-verify`)
- Git worktree support: parallel sessions authorized by CLAUDE.md; `flock` on `.claude/skills/.sync-lock` required for AC-ATK-16 closure
- Test infrastructure: pytest fixtures + `tests/fixtures/donor-blocks/` (8 files: 6 donor + 2 sentinel) for CR-TASK-12 verbatim-diff audit
- Docs infrastructure: mkdocs version pinned in `pyproject.toml`/`docs/requirements.txt` pre-Step-8

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|---|---|---|---|---|---|---|
|R-RES-01|Tier-conditioned read boundary thin — wrapper-routed dispatch could describe forbidden per-item dispatch as "read"|M1, M5|MEDIUM|MEDIUM|AC-ATK-05 closed-enum + ME-1 design-time review + CI lint step|Engineering Lead|
|R-RES-02|F-05 4th rf-qa invocation widens INV-03 surface beyond canonical anchor language|M2, M5|MEDIUM|MEDIUM|AC-ATK-11 retroactive ME-10 OR one-time non-generalizing carve-out|Engineering Lead|
|R-RES-03|F-04 over-escalation unbounded by design — rf-qa queue flood risk|M2, M3, M4|MEDIUM|MEDIUM|Reactive refusal threshold post queue-depth telemetry|Engineering Lead|
|R-RES-04|S-1 hierarchy recorded but not decided — `--max-wait` carrier surface ambiguous|M3|MEDIUM|MEDIUM|AC-ATK-08 + Engineering Lead disposition pre-Step-5|Engineering Lead|
|R-RES-05|F-07 procedural chain not manifest binding|M4|LOW|LOW|AC-ATK-07 rf-qa rebound as F-07 chain-integrity verifier at Step 6 pre-commit|Engineering Lead|
|R-ATK-01|CR-7 markdown discipline weakness|M1|MEDIUM|MEDIUM|Closed by sentinel + AST-grade grep (AC-ATK-13)|Engineering Lead|
|R-ATK-06|Line-number anchor brittleness|M1, M2|MEDIUM|MEDIUM|Closed by content-hash anchors (CR-FM-04 extension)|Engineering Lead|
|R-ATK-16|Make sync-dev worktree race|M4|HIGH|HIGH|Closed by `flock` (AC-ATK-16); Q-GAP-04 macOS/BSD portability fallback|Engineering Lead|
|R-ATK-17|Local pre-push bypassable via `--no-verify`|M3, M4, M5|HIGH|HIGH|Closed by server-side push-policy hook (AC-ATK-17); GitHub.com defense-in-depth via Actions + branch-protection + signed commits|Engineering Lead / DevOps|
|R-DRIFT-02|Donor anchor off-by-2 (`:127-135` → `:133-135`)|M3 Step-4|LOW|HIGH|Patch single-source in 3 artifacts + CR-TASK-12 anchors pre-Step-4|Documentation/Release Owner|
|R-DRIFT-03|Donor anchor off-by-43 (`:200-210` → `:157-161`)|M2 Step-3|MEDIUM|HIGH|Patch single-source in 3 artifacts + CR-TASK-12 anchors pre-Step-3 (M3-blocking)|Documentation/Release Owner|
|R-FM-01|Symlink defeat of `make verify-sync`|M4|LOW|HIGH|Pre-Step-6 audit: `find -type l` returns empty|Engineering Lead|
|R-FM-02|Step-5 atomic flaky pytest no-progress|M3|MEDIUM|MEDIUM|Pin env vars; CI gate sign-off|Engineering Lead|
|R-FM-03|Parallel subagent SKILL.md conflict|M3, M4|MEDIUM|MEDIUM|Ban parallel dispatch on `task/SKILL.md` during Step 5/6|Engineering Lead|
|R-FM-04|CI/local env divergence|M1, M3|MEDIUM|MEDIUM|Pin env vars (PYTHONHASHSEED, locale, timezone)|Engineering Lead|
|R-FM-05|mkdocs version drift|M5 Step-8|MEDIUM|MEDIUM|Pin mkdocs version pre-Step-8|Engineering Lead|
|R-FM-06|`docs/generated/*` regen unscheduled|M5|MEDIUM|HIGH|CR-DEP-06 manifest archives weekly; FR-CS-10 banner string|Engineering Lead|
|R-FM-07|UTF-16 grep evasion|M5|LOW|LOW|Surfaced as TDD §22 gap; UTF-8-only authoring discipline|Engineering Lead|
|R-FM-08|Donor file-rename evasion|M4|LOW|MEDIUM|CR-DEP-04 enforces directory absence not just file absence|Engineering Lead|
|R-OPS-02|H-4 manual operator intervention required|M4, M5|MEDIUM|HIGH|AC-ATK-18 + pre-flag at-risk task ID + operator runbook (OPS-R-1)|Engineering Lead|
|Q-GAP-04|`flock` portability on macOS/BSD|M4|MEDIUM|MEDIUM|`brew install flock` or `lockfile-create` fallback documented|Engineering Lead|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|KPI-01 TU verdict fidelity|V/C/K verdicts identical byte-for-byte|8/8|`tests/audit/test_vck_verdicts.py::test_transfer_manifest_byte_match`|M5|
|KPI-02 ME traceability|ME rows trace to ≥1 CR-row|9/9|`tests/audit/test_me_traceability.py`|M5|
|KPI-03 INV walkthrough survival|INVs re-readable with worked-example anchor|5/5|`tests/audit/test_invariant_walkthrough.py`|M5|
|KPI-04 F-finding anchor citations|F-rows cite valid line ranges|8/8|`tests/audit/test_f_findings_cite_anchors.py`|M5|
|KPI-05 S-constraint HZ citations|S-rows cite named hazard|3/3|`tests/audit/test_s_constraints_cite_hz.py`|M5|
|KPI-06 Row + step counts|67 row-line-items + 10 commit steps|67+10|`tests/audit/test_row_and_step_counts.py`|M5|
|KPI-07 CR-FM-04 row-1 ordering|2 greps × 3 function names monotonic|6 hits|`tests/skills/task/test_cr_fm_04_ordering.py`|M1|
|KPI-08 CR-TASK-12 seven-diff|Zero-diffs against fixtures|7/7|`tests/skills/task/test_cr_task_12_donor_diffs.py`|M3 Step-4|
|KPI-09 Step-5 commit roster|Exact-match per final-merge-plan.md:375|set-equal|`tests/audit/test_step_5_commit_roster.py`|M3|
|KPI-10 Step-6 commit roster|Exact-match per final-merge-plan.md:381|set-equal|`tests/audit/test_step_6_commit_roster.py`|M4|
|KPI-11 Zero ledger re-proposals|LR-REJECT-* grep hits in final-merge-plan.md §5|0|`tests/audit/test_no_rejected_re_proposal.py`|M5|
|KPI-12 In-flight resume + step-gate zero|Live in-flight floor resume clean; gates 1/5/6 exit 0|100% of 136-floor|`tests/audit/test_step_gates.py` + live-recount fixture|M1, M3, M4|
|KPI-13 Zero unmitigated AC-ATK|AC-ATK rows in OPEN or PARTIAL|0|Post-Phase-7.5 traceability matrix|M5|
|KPI-14 Sprint-runner pytest|Pass rate on `tests/cli/` after CR-DEP-05|100%|`uv run pytest tests/cli/ -v`|M3|
|KPI-15 Residual occurrences|Outside authorized leave-as-is buckets|144→0|CR-DEP-06 manifest residual count|M4, M5|
|KPI-16 `make verify-sync` flake rate|Flakes across 30 CI runs post-flock|0|CI log retention scan|M4, M5|
|KPI-17 Post-merge audit pass rate|Across 33 spec-named CR rows|100% PASS|Aggregated pre-commit gate output|M5|
|KPI-18 Donor SKILL.md absent|`src/` and `.claude/` copies absent|both absent|`find` checks; CR-DEP-04 gate|M4|
|KPI-19 Visible command + skill surface count|Paired entries → 1 paired|2→1|`superclaude install --dry-run` roster diff|M4|
|KPI-20 Maintenance surface-pair count|SKILL.md pair count|2→1|Repo census of `src/superclaude/skills/*/SKILL.md`|M4|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|---|---|---|---|
|CR-7 ORDERING enforcement|HTML-comment sentinel + AST-grade ordering grep|(a) markdown discipline alone (R-ATK-01 weakness); (b) sentinel-presence grep only (AC-ATK-13 informational downgrade option)|Closes R-ATK-01 markdown-discipline weakness; provides structural enforcement at Step-4 pre-commit gate; AST-grade check prevents future formatting commits from silently breaking ordering|
|TFEP baseline persistence|On-disk YAML at `${TASK_DIR}/research/test-baseline.yaml`|(a) Donor in-memory form at `sc-task-protocol/SKILL.md:147` (ADAPT delta — breaks INV-04 across session boundaries)|Donor in-memory form breaks INV-04 resumability across session boundaries; on-disk YAML is load-bearing for HIGHEST-EXPOSURE invariant; tier-gated (LIGHT/EXEMPT skip per ME-4)|
|Rebase-split bypass enforcement|Server-side CI push-policy hook at `.github/workflows/push-policy.yml`|(a) Local `.git/hooks/pre-push` (--no-verify bypassable, R-ATK-17 score HIGH); (b) Branch protection alone (admin override possible)|Closes H-2 / R-ATK-17 by structural barrier (NOT bypassable via `--no-verify`); defense-in-depth via signed commits + branch protection + code-owners review on `src/superclaude/cli/**`; GitHub.com lacks pre-receive (Q-GAP-09)|
|Sync atomicity primitive|`flock(2)` on `.claude/skills/.sync-lock`|(a) No locking (live copy-overwrite race + forward-looking prune-loop race H-3); (b) File-level lock convention (no enforcement)|Closes R-ATK-16; covers both forward-looking prune race AND live copy-overwrite race at `Makefile:121`; portable via `brew install flock` (macOS) or `lockfile-create` (BSD) per Q-GAP-04|
|INV-04 closure approach|Two-layer: CR-FM-03 parse-layer shim + AC-ATK-18 semantic-layer content audit|(a) Parse-layer only (semantic exposure unaddressed across 136-floor); (b) Migration script writing back to frontmatter (mutates source-of-truth, breaks Incremental Writing Protocol)|HIGHEST EXPOSURE invariant per validation-spec §9 L285; parse-layer shim alone leaves 136 in-flight files semantically exposed; AC-ATK-18 warn-and-continue per ME-3 (NEVER HALT, preserves INV-01)|
|F-05 4th rf-qa invocation manifestization|One-time non-generalizing carve-out per AC-ATK-11|(a) Retroactive ME-10 row in `merge-master.md §4.5` (heavier manifest authoring); (b) Drop TU-7 mid-phase invocation (would re-open D25 LR-REJECT-2)|Reuses existing rf-qa identity at `:191-198` spawn pattern; preserves ME-2 (rf-qa never replaced); blocks precedent claims by future TU-style merges|
|Donor stubification command form|Form 1 `> Skill task` (recipient name wins per CR-DEP-01)|(a) Form 2 `> Skill sc-task-protocol` (donor name preserved); (b) Hard-delete command file directly|Recipient skill is named `task` (not `task-protocol`); 6 caller emissions re-route to `/task` (no `-protocol` suffix); internal consistency between caller emission and skill-stub invocation|
|Outcome enum literal|`{success, escalated, failed}` byte-identical to donor `sc-task-protocol/SKILL.md:232`|(a) Long-form glosses `{resolved, escalated-FULL-STOP, test_is_wrong-presented-to-user}` (synth-06 drift, corrected at fix-cycle 1)|ME-6 byte-preservation binding; donor literal authoritative for forensic schema compatibility|
|Sentinel form|HTML-comment `<!-- CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder. -->`|(a) Shell-comment form; (b) JavaScript-comment form; (c) Markdown-italic note|HTML comments do not render in Markdown views; serve as out-of-band machine-grep anchor; commonly used across Markdown ecosystem|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1 Foundation|5d (T+0..T+5d)|2026-05-16|2026-05-21|M1 atomic commit; CR-7 sentinel landed; 7 foundation rows + AC-ATK-05 register|
|M2 TFEP Cluster|5d (T+5d..T+10d)|2026-05-21|2026-05-26|TU-5..TU-8 byte-for-byte; R-DRIFT-03 patch applied; 4th rf-qa invocation live|
|M3 CLI Re-Route + Stubification|5d (T+10d..T+15d)|2026-05-26|2026-05-31|Step-4 audit window; Step-5 atomic soft-deprecation; AC-ATK-17 server-side hook active|
|M4 Hard-Delete + Flock-Guarded Sync|2d (T+15d..T+17d)|2026-05-31|2026-06-02|Donor SKILL.md hard-deleted; flock-guarded sync; CR-DEP-06 manifest emitted; AC-ATK-18 semantic-layer audit active|
|M5 Validation + Audit Closure|10d (T+17d..T+27d)|2026-06-02|2026-06-12|All 18 AC-ATK + 12 AC-SM PASS; K-01..K-08 baseline; Phase 7.5 traceability matrix zero OPEN/PARTIAL|

**Total estimated duration:** 27 days (T+0 → T+27d; 2026-05-16 → 2026-06-12); anchored to TDD §23 timeline (M1 commit T+5d, Phase 7.5 complete T+27d)
