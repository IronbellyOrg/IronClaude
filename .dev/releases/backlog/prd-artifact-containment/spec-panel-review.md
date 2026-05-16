# Spec Panel Review — PRD Artifact Containment

**Spec under review:** `/config/workspace/IronClaude/.dev/releases/backlog/prd-artifact-containment/spec.md`
**Review date:** 2026-05-14
**Mode:** critique
**Focus areas:** correctness, architecture, completeness, testability, operability
**Expert panel:** Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower
**Spec type:** refactoring (per frontmatter)

---

## Quality Assessment Snapshot

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 8.0/10 | Stage A.0 workflow is clear; placeholder semantics are well-defined. |
| Completeness | 6.5/10 | Several edge cases unresolved: empty/missing `.dev/releases/`, slug collisions across products, multi-PRD per release semantics, file-locking. |
| Testability | 7.5/10 | Test plan exists but acceptance criteria reference T-codes never defined in this doc (T-RES-EXPLICIT, T-RES-SESSION-CWD, etc.). |
| Consistency | 7.0/10 | Section 4.1 says "no new files" but Section 4.2 specifies a new test file. Section 4.5 missing. Variable naming drift between SKILL example and spec (`RESEARCH:` vs `RESEARCH_DIR`). |
| Operability | 6.5/10 | Concurrency model under-specified; no rollback for half-bootstrapped releases; no observability for resolution-method outcome. |
| **Overall** | **7.1/10** | Strong direction, but several correctness/operability gaps before implementation. |

---

## 1. KARL WIEGERS — Requirements Quality

### HIGH
- **W-H1: Acceptance criteria reference T-codes not defined.** §3 ACs name T-codes (e.g., "tested via T-AGENT-PATH-DISCIPLINE") that only appear in §8.1 as test names. The implicit binding is fragile. **Recommendation:** Annotate each AC checkbox with the exact test function name so traceability is byte-level.
- **W-H2: FR-PRD-CONTAIN.1 conflates resolution with bootstrap side effects.** The bootstrap step writes a `README.md` stub — a side-effecting requirement embedded inside a resolution algorithm.

### MEDIUM
- **W-M1: "Concurrent-developer collisions" (NFR-CONTAIN.3) lacks a definition.** What is a collision?
- **W-M2: FR-PRD-CONTAIN.5 default behaviour ambiguous.** Does `PUBLISH_MODE` default to `none` if unset?

### LOW
- **W-L1: Quality scores in frontmatter are unsourced.**

---

## 2. GOJKO ADZIC — Specification by Example

### HIGH
- **A-H1: Stage A.0 step 3 ("Branch matches `feat/<name>` or `fix/<name>`") has no Given/When/Then.** Match semantics unspecified.
- **A-H2: Slug-based reverse lookup — match semantics (substring/fuzzy/exact/regex) unspecified.**

### MEDIUM
- **A-M1: PUBLISH_MODE=symlink behaviour on Windows / read-only filesystems is unspecified.**
- **A-M2: No example of resolved variable expansion.**

### LOW
- **A-L1: "Stub line citing the skill and timestamp" — show the literal stub content.**

---

## 3. ALISTAIR COCKBURN — Use Case / Actor Analysis

### HIGH
- **C-H1: Primary actor for Stage A.0 is unidentified.** Human developer? Claude orchestrator? Subagent? If invoked by `/sc:pm` there is no human for the consent prompt. Add an "Actors" subsection.

### MEDIUM
- **C-M1: "Cancel" option (A.0 step 5c) — what state remains?**
- **C-M2: Legacy folder detection prompts three options. No spec for what each does step-by-step.**

---

## 4. MARTIN FOWLER — Architecture / Interface

### CRITICAL
- **F-C1: `TASK_DIR` alias for `PRD_WORKSPACE` creates a referential ambiguity.** Two names for one thing is an interface smell. Either remove the alias entirely or document it as deprecated with a removal target.

### HIGH
- **F-H1: No single source of truth for the resolved variable block at runtime.** SKILL.md, BUILD_REQUEST template, task file, and refs/* all carry variables. Add §4.7 "Variable Schema".
- **F-H2: §4.1 "No new files" contradicts §4.2 (new test file).**

### MEDIUM
- **F-M1: §4.5 "Data Models" missing.** The 11 new variables ARE a data model.
- **F-M2: Module dependency graph doesn't show resolution-time vs. execution-time boundary.**

---

## 5. MICHAEL NYGARD — Reliability / Failure Modes

### CRITICAL
- **N-C1: No precondition that CWD is an IronClaude project.** If a user runs `/prd` from a foreign repo, bootstrap could create `.dev/releases/backlog/<slug>/` in someone else's tree. Add a precondition guard.

### HIGH
- **N-H1: Concurrent bootstrap race condition.** Two `/prd` invocations within ms both bootstrap → race on `mkdir`. Define semantics + post-create verification.
- **N-H2: Half-bootstrapped release rollback unspecified.**
- **N-H3: PUBLISH symlink failure semantics — what if target exists?**

### MEDIUM
- **N-M1: Slug-based reverse lookup has no upper bound; NFR-2 targets <2s but no measurement scaffold.**
- **N-M2: No observability for resolution method.**

---

## 6. JAMES WHITTAKER — Adversarial Probing

### CRITICAL
- **WH-C1: Sentinel Collision Attack on `PRD_SLUG`.** Invariant at FR-PRD-CONTAIN.2 (PRD_SLUG regex) fails when a user supplies `prd-workspace` as slug (legal under `^[a-z0-9][a-z0-9-]*$`). Resolution computes `PRD_WORKSPACE=.dev/releases/current/foo/prd-workspace/prd-workspace/`. Resumability logic then conflates the container directory with a PRD workspace. **Fix:** Reserve `prd-workspace`, `research`, `synthesis`, `qa`, `reviews`, `sources-archive` as forbidden slugs.

- **WH-C2: Sequence Attack on Stage A.0 → A.1.** Invariant at §2.2 fails on resume of a partially-bootstrapped release. First `/prd` reaches step 5a (bootstrap), creates `.dev/releases/backlog/wizard-system/`, crashes before A.1. User re-invokes. Step 4 (slug-match) returns the stub release but `prd-workspace/<slug>/` is empty. **Fix:** A.0 step 4 MUST verify `prd-workspace/<PRD_SLUG>/` exists; if only the stub exists, treat as bootstrap-completion path.

### HIGH
- **WH-H1: Empty-slug response unspecified.** Hang? Halt? Re-prompt?
- **WH-H2: Multi-match priority unspecified.** Release named `wizard-system` vs. another release containing `prd-workspace/wizard-system/`. Define priority.
- **WH-H3: No bound on multi-PRD-per-release accumulation.**

### MEDIUM
- **WH-M1: `PUBLISH_MODE` case-sensitivity unspecified.** `NONE`, `Copy`?
- **WH-M2: "Finish in legacy" sequence — TASK_DIR already remapped. Rewind?**

---

## 7. SAM NEWMAN — Service Boundaries / Evolution

### MEDIUM
- **NW-M1: BUILD_REQUEST has no version field.**
- **NW-M2: No deprecation path for `TASK_DIR` alias.**

---

## 8. GREGOR HOHPE — Integration / Data Flow

### MEDIUM
- **H-M1: Resolution-method telemetry buried in `research-notes.md`.**
- **H-M2: PUBLISH event recorded in Task Log; no machine-parseable schema.**

---

## 9. LISA CRISPIN — Testability / Test Strategy

### HIGH
- **CR-H1: 15 unit tests but no fixtures or factory definitions.** Add §8.4 Test Infrastructure.
- **CR-H2: T-CONCURRENT-DEV is integration/E2E not unit.**

### MEDIUM
- **CR-M1: No negative tests.** Invalid slug, PUBLISH_PATH outside repo, missing `.dev/releases/`, read-only FS.
- **CR-M2: `grep` semantics differ BSD/GNU.** Specify exact command.

### LOW
- **CR-L1: No coverage target.**

---

## 10. JANET GREGORY — Quality Practices

### MEDIUM
- **G-M1: No "Three Amigos" sign-off requirement.**
- **G-M2: OQ-1 (bootstrap default), OQ-5 (slug uppercasing) should be resolved pre-implementation.**

---

## 11. KELSEY HIGHTOWER — Operability / Cloud-Native

### MEDIUM
- **K-M1: No CI behaviour defined.** `--non-interactive` mode needed.
- **K-M2: No env var for default RELEASE_BUCKET.**

### LOW
- **K-L1: No artifact retention / cleanup for empty release stubs.**

---

## Mandatory Output: Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Explicit RELEASE_PATH | A.0 step 1 | Empty | `""` | falsy | (implied fall through) | GAP |
| Explicit RELEASE_PATH | A.0 step 1 | Doesn't exist | `"x"` | truthy | (silent) | GAP |
| Explicit RELEASE_PATH | A.0 step 1 | Outside tree | `"/tmp/foo"` | truthy | (silent) | GAP |
| CWD under .dev/releases/ | A.0 step 2 | Empty | repo root | false | fall through | OK |
| CWD under .dev/releases/ | A.0 step 2 | Nested | `.dev/releases/backlog/foo/prd-workspace/bar/` | true | (which level?) | GAP |
| Branch match | A.0 step 3 | Empty | `master` | false | fall through | OK |
| Branch match | A.0 step 3 | Multi-match | `feat/foo` w/ releases `[foo, foo-v2]` | ambiguous | (silent) | GAP |
| Slug reverse-lookup | A.0 step 4 | Zero | `PRD_SLUG=zzz` | none | proceed to step 5 | OK |
| Slug reverse-lookup | A.0 step 4 | Single | one matches | one | use it | OK |
| Slug reverse-lookup | A.0 step 4 | Multi | two matches | many | halt + prompt | OK |
| Slug reverse-lookup | A.0 step 4 | Reserved word | `PRD_SLUG=prd-workspace` | matches container | (silent) | GAP (CRIT) |
| PRD_SLUG regex | FR-2 | Empty | `""` | false | (silent) | GAP |
| PRD_SLUG regex | FR-2 | Sentinel | `prd-workspace` | true | (allowed!) | GAP (CRIT) |
| PRD_SLUG regex | FR-2 | Long | 64+ chars | true | (allowed) | GAP |
| PUBLISH_MODE | FR-5 | Unset | undefined | (silent) | should default `none` | GAP |
| PUBLISH_MODE | FR-5 | Case-variant | `COPY` | (silent) | (silent) | GAP |
| PUBLISH_MODE | FR-5 | Missing path | mode=copy, path empty | error | halt | OK |

**GAP count:** 10 of 17 → MAJOR-severity gaps per FR-8.

---

## Severity Tally

| Severity | Count |
|---|---|
| CRITICAL | 4 (F-C1, N-C1, WH-C1, WH-C2) |
| HIGH | 15 |
| MEDIUM | 22 |
| LOW | 4 |

---

## Top 5 Most Impactful Issues

1. **WH-C1** — Reserved-slug collision (`prd-workspace` as PRD_SLUG).
2. **N-C1** — No precondition that CWD is an IronClaude project.
3. **F-C1** — `TASK_DIR` alias creates referential ambiguity.
4. **WH-C2** — Sequence attack: half-bootstrapped release on re-resolve.
5. **F-H1 / W-H1** — Variable schema and T-code traceability lack a single source of truth.

---

## Remediation Plan

| ID | Severity | Decision | Target | Status |
|---|---|---|---|---|
| F-C1 | CRIT | fix spec | §2.1 + Glossary + §4.7 | applied |
| N-C1 | CRIT | fix spec | New AC on FR-1; promote BG-4 | applied |
| WH-C1 | CRIT | fix spec | FR-2 AC + Glossary | applied |
| WH-C2 | CRIT | fix spec | FR-1 AC | applied |
| W-H1 | HIGH | fix spec | §8.1 annotate ACs with test names | applied |
| W-H2 | HIGH | defer | Cosmetic split; ACs sufficient | deferred |
| A-H1 | HIGH | fix spec | Branch-match rule on FR-1 | applied |
| A-H2 | HIGH | fix spec | Match priority rule | applied |
| C-H1 | HIGH | fix spec | §2.3 Actors + non-interactive | applied |
| F-H1 | HIGH | fix spec | §4.5 Variable Schema | applied |
| F-H2 | HIGH | fix spec | Rephrase §4.1 | applied |
| N-H1 | HIGH | fix spec | Concurrent-bootstrap AC | applied |
| N-H2 | HIGH | fix spec | §9 rollback subsection | applied |
| N-H3 | HIGH | fix spec | Publish symlink precondition AC | applied |
| WH-H1 | HIGH | fix spec | Empty-slug error AC | applied |
| WH-H2 | HIGH | fix spec | Match priority (folded A-H2) | applied |
| WH-H3 | HIGH | fix spec | Soft cap warning | applied |
| CR-H1 | HIGH | fix spec | §8.4 Test Infrastructure | applied |
| CR-H2 | HIGH | fix spec | Move T-CONCURRENT-DEV to §8.2 | applied |
| W-M1 | MED | fix spec | Define collision in NFR-3 | applied |
| W-M2 | MED | fix spec | Explicit PUBLISH_MODE default | applied |
| A-M1 | MED | fix spec | Symlink-unsupported failure | applied |
| A-M2 | MED | fix spec | Worked example §2.2 | applied |
| C-M1 | MED | fix spec | Cancel postcondition | applied |
| C-M2 | MED | fix spec | Legacy-option subcases | applied |
| F-M1 | MED | fix spec | §4.5 Variable schema (folded) | applied |
| F-M2 | MED | defer | Annotation adds noise | deferred |
| N-M1 | MED | defer | OQ for resolution latency | deferred |
| N-M2 | MED | fix spec | NFR-7 observability | applied |
| WH-M1 | MED | fix spec | PUBLISH_MODE case AC | applied |
| WH-M2 | MED | fix spec | Folded with C-M2 | applied |
| NW-M1 | MED | fix spec | BUILD_REQUEST_VERSION | applied |
| NW-M2 | MED | defer | OQ added | deferred |
| H-M1 | MED | fix spec | Folded with N-M2 | applied |
| H-M2 | MED | fix spec | Publish log schema | applied |
| CR-M1 | MED | fix spec | Negative tests in §8.1 | applied |
| CR-M2 | MED | fix spec | Specify command | applied |
| G-M1 | MED | fix spec | Three-amigos rollout note | applied |
| G-M2 | MED | fix spec | Resolve OQ-1, OQ-5 inline | applied |
| K-M1 | MED | fix spec | Non-interactive (folded C-H1) | applied |
| K-M2 | MED | defer | OQ added | deferred |
| W-L1 | LOW | reject | Cosmetic | rejected |
| A-L1 | LOW | fix spec | Stub literal content | applied |
| CR-L1 | LOW | fix spec | Coverage target | applied |
| K-L1 | LOW | defer | OQ added | deferred |
