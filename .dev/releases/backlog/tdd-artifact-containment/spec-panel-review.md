# Spec Panel Review — TDD Artifact Containment

**Spec under review:** `.dev/releases/backlog/tdd-artifact-containment/spec.md` (v1.0.0, status: draft)
**Mode:** `--mode critique`
**Focus:** correctness, architecture, completeness, testability
**Panel:** Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower
**Date:** 2026-05-14

---

## 1. Executive Summary

The spec is **substantially well-structured** for a refactoring release: clear problem statement, evidence-backed (28+13+14 reference index), per-FR acceptance criteria, dependency graph, and a self-anchored test plan. However, it has **several correctness gaps around the synthesis step of release resolution**, **ambiguous parser semantics for the `--release` flag**, **interactive-prompt assumptions that don't hold in non-TTY contexts**, **dangling gap references (G-REFLECT-1..3) that point nowhere**, **a flat-vs-nested final-TDD naming collision risk**, and **a missing concurrency guard on synthesized release directory creation**. The variable contract, builder hand-off, and backwards-compat layer are otherwise solid.

| Severity | Count |
|----------|-------|
| CRITICAL | 4 |
| HIGH     | 12 |
| MEDIUM   | 13 |
| LOW      | 5 |
| INFO     | 3 |
| **Total** | **37** |

---

## 2. Findings by Expert

### 2.1 Karl Wiegers — Requirements Quality

**F-W1 (HIGH) — FR-2 step 1 conflates "ambiguity" with "not-found".**
FR-2.AC1: "Step 1 (explicit `--release`): validates the path exists, errors on ambiguity or not-found." The flag is a single string — "ambiguity" only arises in **name-only** resolution (FR-4 line 162: "Flag accepts either `bucket/name` or just `name`"). Acceptance criterion is misplaced and untestable as written.
*Recommendation:* Split into two AC rows — one for `bucket/name` form (exact-path check), one for `name`-only form (cross-bucket scan + disambiguation error).

**F-W2 (HIGH) — COMPONENT_SLUG derivation rule not in FR text.**
OI-4 defers to "existing kebab-case rule from current SKILL.md line 173". That line says `COMPONENT_SLUG: A kebab-case identifier` — no algorithm. What is the rule for `"Auth/V2 (beta)"`? FR-1 should pin a deterministic derivation, otherwise tests T6-T22 are non-reproducible.
*Recommendation:* Add FR-1 AC: "Derivation rule: lowercase, replace non-alphanumeric runs with `-`, strip leading/trailing `-`, collapse repeated `-`. Empty result errors."

**F-W3 (MEDIUM) — NFR-1 "well-formed legacy path" is undefined.**
"100% of well-formed legacy paths resume" — what counts as well-formed? Spec needs a definition or a regex.
*Recommendation:* NFR-1 measurement column should reference a concrete pattern, e.g. `^\.dev/tasks/to-do/TASK-TDD-\d{8}-\d{6}(-[a-f0-9]{4})?/`.

**F-W4 (MEDIUM) — FR-6.AC3 ambiguous: where does the final TDD land on legacy resume?**
"completes the run under legacy layout and notes the deprecation in the final TDD's Document History" — does "completes under legacy layout" mean the final TDD goes to `docs/[domain]/...` (legacy default) or to a `${RELEASE_DIR}` (resolved how?) or stays beside the task folder?
*Recommendation:* State explicitly: on legacy resume, the final TDD writes to wherever the **legacy task file's metadata** already designated (typically `docs/[domain]/...`); no implicit migration.

---

### 2.2 Gojko Adzic — Specification by Example

**F-A1 (MEDIUM) — No Given/When/Then scenarios for the 4-step resolution.**
Tests T6-T13 name the resolution branches but never show before/after state. A reader cannot tell which input gives which output without reading test source.
*Recommendation:* Add a `### 5.2 Resolution Examples` table with 6-8 rows: (cwd, --release flag, --from-prd, expected RELEASE_DIR, branch taken).

**F-A2 (HIGH) — T22 asserts behavior not in any FR.**
T22 says `--release backlog/foo --output ../external/TDD.md` "warns user but proceeds". No FR specifies the warning. The test is the only place this behavior appears.
*Recommendation:* Add an FR-3 AC: "When `--output` resolves to a path outside RELEASE_DIR, the skill emits a single-line warning to stderr before proceeding."

**F-A3 (LOW) — T20 acceptance criterion vague.**
"New layout takes precedence over legacy" — undefined. Precedence in what dimension? Discovery? Write?
*Recommendation:* Restate as "When implicit-resume scan finds tasks in BOTH new and legacy trees for the same component, the new-tree task is selected; legacy hit logged."

---

### 2.3 Alistair Cockburn — Use Case / Stakeholder

**F-C1 (HIGH) — FR-2.AC5 assumes interactive prompt; non-TTY behavior unspecified.**
"Conflict between cwd and PRD detection prompts the user to disambiguate." `/sc:tdd` may be invoked by `/sc:pm`, CI, or a sub-agent where prompting is impossible.
*Recommendation:* Add deterministic fallback: "When stdin is not a TTY and a conflict is detected, error with a non-zero exit, listing both candidates and instructing the user to pass `--release` explicitly."

**F-C2 (LOW) — Primary actor not declared.**
Spec does not state who runs `/sc:tdd`. Single-developer? PM-agent? CI? Affects FR-2 ergonomics.
*Recommendation:* Add a one-line "Primary actor" note in Section 2.

---

### 2.4 Martin Fowler — Architecture / Interface

**F-F1 (CRITICAL) — Synthesized release directory is incomplete by construction.**
FR-2 step 4 creates `.dev/releases/backlog/tdd-<slug>/` but does not seed `spec.md` or any marker. The release index now contains a directory that looks like a real release but isn't one — it has only `TDD_*.md` and `tdd/...`. A reader running `ls .dev/releases/backlog/` cannot tell synthesized from real.
*Recommendation:* Drop a `README.md` in the synthesized dir flagging it as "synthesized-by-tdd, no spec/roadmap yet" and adopt the convention that synthesized releases are eligible for `/sc:roadmap` and `/sc:spec` promotion.

**F-F2 (HIGH) — Flat sibling `TDD_<COMPONENT>.md` collision under case-insensitive FS.**
Two designs `auth` and `Auth` produce `TDD_auth.md` and `TDD_Auth.md`. macOS default FS (APFS, case-insensitive default) collides.
*Recommendation:* Add an FR-1 AC: "COMPONENT_SLUG is always lowercase. Two designs whose names differ only by case map to the same slug; second invocation must use a different component name or accept the rand4 collision suffix."

**F-F3 (MEDIUM) — Bucket whitelist hard-codes 3 values; `.dev/README.md` may extend.**
FR-1.AC4 hard-codes `(backlog|current|complete)`. If `.dev/README.md` later adds buckets, this spec becomes the bottleneck.
*Recommendation:* Reference `.dev/README.md` as the authoritative bucket list; spec accepts "any direct child of `.dev/releases/`".

**F-F4 (MEDIUM) — Resolution algorithm has no explicit "deepest ancestor" rule in FR-2.**
Risk table (Section 7 row 2) says "deepest matching ancestor" but FR-2.AC2/AC3 just say "walks up".
*Recommendation:* Add to FR-2.AC2: "Returns the longest matching path prefix (deepest ancestor)."

---

### 2.5 Michael Nygard — Reliability / Failure Modes

**F-N1 (CRITICAL) — No race-free creation of synthesized RELEASE_DIR.**
Step 4 creates `.dev/releases/backlog/tdd-<slug>/`. Two parallel `/sc:tdd` invocations on the same new component both hit step 4 simultaneously. Then TASK_DIR rand4 collision-handling kicks in too late — both have already claimed the same RELEASE_DIR.
*Recommendation:* Step 4 must use `mkdir` with `exist_ok=True` and treat "already exists" as a normal merge (both runs become siblings under one synthesized release). Add FR-2.AC: "Step 4 is idempotent."

**F-N2 (HIGH) — `.dev/releases/` parent dir may not exist (greenfield repo).**
G2 acknowledges this but does not resolve.
*Recommendation:* FR-2 step 4 AC: "Creates parent directories as needed (`mkdir -p`). If `.dev/` is missing, error with a message pointing to project setup."

**F-N3 (HIGH) — Filesystem failure modes not specified.**
What if RELEASE_DIR is read-only, full, or on a stale NFS mount? Per-artifact write failure mid-run is silent.
*Recommendation:* Add NFR-7: "On write failure to RELEASE_DIR, the skill halts with the partial-write path printed; no implicit retry."

**F-N4 (MEDIUM) — `--output` override with non-existent parent directory.**
T21/T22 use `--output ./custom/path/MY_TDD.md`. What if `./custom/path/` doesn't exist?
*Recommendation:* Add to FR-3.AC: "Override path's parent directory must exist; the skill does not create it."

---

### 2.6 James Whittaker — Adversarial Probing

**F-WH1 (CRITICAL) — Zero/Empty Attack: empty `--release` value.**
Invariant at FR-2 step 1. Triggering condition: `/sc:tdd "foo" --release ""`. State before: flag value is empty. Step 1 sees a flag passed (not absent) and validates path `.dev/releases/` (empty resolves to root) — either passes or errors. State after: undefined; could create `.dev/releases//` artifact or silently fall to Step 2.
*Recommendation:* FR-2.AC: "Step 1 treats empty/whitespace flag values as not provided (fall to Step 2)."

**F-WH2 (HIGH) — Divergence Attack: cwd inside `${RELEASE_DIR}/tdd/...`.**
Triggering condition: `cd .dev/releases/current/foo/tdd/bar/TASK-TDD-*/research/ && /sc:tdd baz`. Step 2 walks up — without an explicit matcher, implementations could pick `tdd/` or wrong level.
*Recommendation:* FR-2.AC: "Ancestor matcher: longest path prefix matching `\.dev/releases/<bucket>/[^/]+/` where `<bucket>` is in the authoritative bucket list (F-F3). Deepest match wins."

**F-WH3 (HIGH) — Sentinel Collision Attack: synthesized release name collides.**
Real release `tdd-auth-system` exists; user runs `/sc:tdd "auth system"` → synthesized name collides → step 4 either overwrites or silently merges.
*Recommendation:* FR-2 step 4 AC: "If `tdd-<slug>/` already exists in backlog/ AND that dir contains a `spec.md` or `roadmap.md` (i.e., it's a real release), append `-YYYYMMDD-HHMMSS` to the synthesized name. If it exists as a prior synthesized dir (has the synthesized-marker README), merge as siblings (per F-N1)."

**F-WH4 (MEDIUM) — Sentinel Collision: release name `tdd` or `archive`.**
Release `current/tdd/` is valid but visually confusing (`tdd/tdd/`). Release `current/archive/` collides with FR-9's per-release `${RELEASE_DIR}/archive/`.
*Recommendation:* FR-1 note: "Release names `tdd` and `archive` are discouraged but not enforced; they produce visually confusing paths or shadow the archive convention."

**F-WH5 (MEDIUM) — Sequence Attack: `--resume` legacy + `--release` flag.**
`/sc:tdd --resume <legacy> --release backlog/bar` — unclear which wins.
*Recommendation:* FR-6.AC: "When `--resume` is given alongside `--release`, the resume path's layout wins; `--release` is ignored with a warning to stderr."

**F-WH6 (LOW) — Accumulation Attack: TASK-TDD-* siblings accumulate forever.**
*Recommendation:* Note in Risk table; defer cleanup to future release.

---

### 2.7 Sam Newman — API Evolution

**F-SN1 (HIGH) — `--resume` path classification (legacy vs new) is implicit.**
*Recommendation:* FR-6.AC: "Resume path is classified by prefix: paths starting with `.dev/tasks/to-do/` are legacy; paths matching `.dev/releases/.+/tdd/` are new; other paths error."

**F-SN2 (MEDIUM) — `--release` parsing ambiguity with internal slashes.**
*Recommendation:* FR-4.AC: "Flag value with exactly one `/` is parsed as `bucket/name`; with zero `/` is name-only; with 2+ `/` errors with an explanatory message."

---

### 2.8 Gregor Hohpe — Integration Patterns

**F-H1 (CRITICAL) — RELEASE_DIR resolution timing vs builder embedding is undefined.**
If builder embeds literal `${RELEASE_DIR}` placeholders in the task file's B2 items, a later subagent has no context. If it embeds resolved literals, the file becomes non-portable across worktrees.
*Recommendation:* FR-5.AC: "The builder MUST resolve all path variables to **repo-relative** literal paths (relative to repo root, not absolute filesystem paths) at task-file-write time. B2 items contain literal paths, not variable references. This preserves both worktree portability and self-containment of B2 items."

**F-H2 (MEDIUM) — `rf-assembler` final-TDD path: literal vs templated.**
Folded into F-H1.

---

### 2.9 Lisa Crispin — Testing Strategy

**F-CR1 (HIGH) — Dangling references G-REFLECT-1, G-REFLECT-2, G-REFLECT-3.**
Section 8 test rows mention these IDs but Section 12 only enumerates G1-G5.
*Recommendation:* Strip parenthetical "(resolves G-REFLECT-*)" citations from test rows; they reference a no-longer-relevant prior review pass.

**F-CR2 (HIGH) — Negative test coverage missing.**
No tests for: empty component name, non-existent `--from-prd`, permission denied on mkdir, malformed legacy resume path.
*Recommendation:* Add 4 negative tests to §8.1.

**F-CR3 (MEDIUM) — No test for NFR-3 (visual `ls`) or NFR-6 (lifecycle move).**
*Recommendation:* Add to §8.3 manual tests.

**F-CR4 (MEDIUM) — No test for slug derivation rule.**
*Recommendation:* Add `test_component_slug_derivation_rule` to §8.1.

---

### 2.10 Janet Gregory — Quality / Workshop

**F-G1 (MEDIUM) — Open Items with status "Decided" should not be open.**
OI-1, OI-2, OI-4, OI-5 all have "Decided" resolutions; they belong in §2.1 Key Design Decisions.
*Recommendation:* Move OI-1/2/4/5 into §2.1; retain only OI-3 (deferred hook) in §11.

**F-G2 (LOW) — Gap registry split.**
Resolved by F-CR1.

**F-G3 (INFO) — Date format.** No change.

---

### 2.11 Kelsey Hightower — Cloud-Native

**F-K1 (LOW) — Cross-platform path handling not asserted.**
*Recommendation:* No FR change; INFO note via Open Items.

**F-K2 (LOW) — No structured logging of resolution branch.**
*Recommendation:* Add as new OI-6.

**F-K3 (INFO) — Greenfield CI assumption.** No change.

---

## 3. Mandatory Output Artifacts (Correctness Focus)

### 3.1 State Variable Registry

| Variable | Type | Initial Value | Invariant | Read Operations | Write Operations |
|----------|------|---------------|-----------|-----------------|------------------|
| `RELEASE_DIR` | path string | unset until A.1b | Matches `\.dev/releases/<bucket>/[^/]+/$` after A.1b | All artifact path constructions; FR-3 default; FR-5 builder hand-off | Set exactly once by FR-2 resolution (steps 1-4) |
| `COMPONENT_SLUG` | kebab-case string | unset until A.2 | Non-empty, `^[a-z0-9-]+$`, no leading/trailing/repeated `-` | TASK_DIR construction; FR-2 step 4 synthesis | Set once by slug-derivation rule (F-W2) |
| `TASK_ID` | string | unset until A.3 | `^TASK-TDD-\d{8}-\d{6}(-[a-f0-9]{4})?$` | TASK_DIR construction; resume scan; final TDD doc history | Set by Stage A.3; suffix appended on collision (FR-7) |
| `TASK_DIR` | path string | unset until A.3 | `${RELEASE_DIR}tdd/${COMPONENT_SLUG}/${TASK_ID}/`; exists after A.3 | All B2 artifact writes | Created by Stage A.3 |

### 3.2 Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--release` provided | FR-2 step 1 | Zero/Empty | `--release ""` | "provided" | **unspecified** | GAP (F-WH1) |
| `--release` provided | FR-2 step 1 | Typical bucket/name | `--release backlog/foo` | match | resolves to `.dev/releases/backlog/foo/` | OK |
| `--release` provided | FR-2 step 1 | Name only, unique | `--release foo` | match | auto-resolved | OK |
| `--release` provided | FR-2 step 1 | Name only, ambiguous | `--release foo` (2 buckets) | error | "ambiguous, specify bucket/name" | OK |
| `--release` provided | FR-2 step 1 | Path with 2+ slashes | `--release a/b/c` | **unspecified** | **unspecified** | GAP (F-SN2) |
| `--release` provided | FR-2 step 1 | Not found | `--release backlog/zzz` | error | "release not found" | OK |
| cwd ancestor match | FR-2 step 2 | Inside release dir | cwd | match | RELEASE_DIR = ancestor | OK |
| cwd ancestor match | FR-2 step 2 | Inside nested `tdd/` | cwd | **unspecified** which level wins | risk table says deepest | GAP (F-WH2) |
| cwd ancestor match | FR-2 step 2 | At repo root | cwd | no match | fall to step 3 | OK |
| PRD ancestor match | FR-2 step 3 | PRD inside release | path | match | RELEASE_DIR = ancestor | OK |
| cwd vs PRD conflict | FR-2 step 2/3 | Both match, different | (both) | conflict | prompt user (TTY) | GAP — non-TTY (F-C1) |
| synthesize fallback | FR-2 step 4 | New synthesized name | `tdd-<slug>` | create | mkdir + inform | OK |
| synthesize fallback | FR-2 step 4 | Name collides with real release | exists | **unspecified** | risk says timestamp | GAP (F-WH3) |
| synthesize fallback | FR-2 step 4 | `.dev/releases/` parent missing | (no parent) | **unspecified** | **unspecified** | GAP (F-N2) |
| synthesize fallback | FR-2 step 4 | Concurrent same-second race | (race) | one succeeds | **unspecified** | GAP (F-N1) |
| TASK_DIR exists | FR-7 | Same-second collision | exists | suffix | append rand4 | OK |
| Legacy resume | FR-6 | `--resume .dev/tasks/...` | path | match | use legacy layout | OK |
| Legacy resume + --release | FR-6 | both flags | (both) | conflict | **unspecified** | GAP (F-WH5) |
| Output override scope | FR-3 / T22 | `--output` outside RELEASE_DIR | path | "outside" | **unspecified** warning | GAP (F-A2) |
| Output override parent | FR-3 | parent missing | path | "no parent" | **unspecified** | GAP (F-N4) |

**Status:** 10 GAPs. Per Hard Gate FR-8 of /sc:spec-panel, each GAP generates at least MAJOR (HIGH) severity finding — captured above.

### 3.3 Pipeline Dimensional Analysis

Not applicable. The spec scope is artifact-path refactoring, not pipeline count semantics.

---

## 4. Cross-Expert Consensus

1. **Synthesis step (FR-2.4) is the highest-risk surface** — three independent findings (F-F1, F-N1, F-WH3) converge on it. Must be hardened before implementation.
2. **`--release` flag parsing needs a precise grammar** — Wiegers, Newman, Whittaker all flag ambiguity.
3. **Non-TTY/non-interactive behavior is undefined** — Cockburn and Whittaker.
4. **Test plan references gap IDs that don't exist** — Crispin and Gregory.
5. **Builder hand-off variable-resolution timing is unspecified** — Hohpe alone but high-impact.

---

## 5. Remediation Plan

| ID | Severity | Action | Status |
|----|----------|--------|--------|
| F-F1 | CRITICAL | Synthesized dir gets README marker; FR-2.4 AC updated | applied |
| F-N1 | CRITICAL | FR-2.4 idempotent mkdir; collision merges as siblings | applied |
| F-WH1 | CRITICAL | FR-2.1 treats empty/whitespace --release as not-provided | applied |
| F-H1 | CRITICAL | FR-5: builder resolves variables to repo-relative literals at write time | applied |
| F-W1 | HIGH | FR-2.AC1 split into bucket/name vs name-only forms | applied |
| F-W2 | HIGH | FR-1.AC: explicit kebab-case derivation algorithm | applied |
| F-A2 | HIGH | FR-3.AC: warning when --output outside RELEASE_DIR | applied |
| F-C1 | HIGH | FR-2.AC: non-TTY error path on conflict | applied |
| F-F2 | HIGH | FR-1.AC: lowercase slug + case-collision behavior | applied |
| F-WH2 | HIGH | FR-2.AC: explicit deepest-ancestor regex matcher | applied |
| F-WH3 | HIGH | FR-2.4.AC: collision with real release appends timestamp | applied |
| F-N2 | HIGH | FR-2.4.AC: mkdir -p for parents; error on missing .dev/ | applied |
| F-N3 | HIGH | New NFR-7: halt + print partial-write path | applied |
| F-SN1 | HIGH | FR-6.AC: prefix-based resume path classification | applied |
| F-CR1 | HIGH | Strip dangling G-REFLECT-* citations from test rows | applied |
| F-CR2 | HIGH | Add 4 negative tests to §8.1 | applied |
| F-W3 | MEDIUM | NFR-1 measurement column gets legacy-path regex | applied |
| F-W4 | MEDIUM | FR-6.AC3: legacy resume keeps legacy output path | applied |
| F-A1 | MEDIUM | Add Resolution Examples table as §5.2 | applied |
| F-F3 | MEDIUM | FR-1.AC: reference `.dev/README.md` as bucket authority | applied |
| F-F4 | MEDIUM | Folded into F-WH2 fix | applied (folded) |
| F-N4 | MEDIUM | FR-3.AC: --output parent must pre-exist | applied |
| F-WH4 | MEDIUM | FR-1 note: release names `tdd`/`archive` discouraged | applied |
| F-WH5 | MEDIUM | FR-6.AC: --resume + --release: resume wins, warn | applied |
| F-SN2 | MEDIUM | FR-4.AC: 0/1/2+ slash grammar for --release | applied |
| F-H2 | MEDIUM | Folded into F-H1 fix | applied (folded) |
| F-CR3 | MEDIUM | Add NFR-3 and NFR-6 to §8.3 manual tests | applied |
| F-CR4 | MEDIUM | Add slug derivation unit test | applied |
| F-G1 | MEDIUM | Move OI-1/2/4/5 into §2.1; keep OI-3 | applied |
| F-A3 | LOW | Restate T20 acceptance criterion | applied |
| F-C2 | LOW | One-line primary-actor note in §2 | applied |
| F-WH6 | LOW | Add accumulation note to Risk table | applied |
| F-K2 | LOW | Add OI-6 for resolution-branch logging | applied |
| F-G2 | LOW | Resolved by F-CR1 | applied (folded) |
| F-K1 | LOW | Cross-platform paths | deferred — INFO note added to Open Items / Risk |
| F-G3 | INFO | Date format | rejected — already template-compliant |
| F-K3 | INFO | Greenfield CI assumption | rejected — out of scope |

**Totals:** 37 findings. 32 applied, 3 deferred/rejected with rationale (1 deferred + 2 rejected). 2 folded into others.

