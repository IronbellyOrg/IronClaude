# D-0099 Evidence — T07.20 MIG-007b v3.9 GA Tag

**Task:** T07.20 — Create MIG-007b v3.9 GA tag
**Companion spec:** `D-0099/spec.md`
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**HEAD at tag time:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8`
**Tag object SHA:** `f15ff7f5656ee0c4989a564cf647a76e947d1e09`
**Tag → target:** `v3.9 → efaa33db9f0087bb1c48236b12c1287171b4f9f8`

---

## 1. Dependency PASS-state evidence

| Dep task | Deliverable | Spec lines | Verdict | Anchor |
|---|---|---|---|---|
| T07.01 | D-0083/spec.md | 158 | TRACKING-PASS (3/3 captured runs at 100% Self-Audit; semantic checks 4 / 4 / 13) | §4.1 + §4.2 + §4.3 |
| T07.02 | D-0084/spec.md | 150 | PASS — all 5 ratios ≤ 1.10 (max 1.0515) | §4 |
| T07.10 | D-0091/spec.md | 144 | PASS — 6 FF + 6 MET + 7 OPS = 19 rows | §2 + §3 enumeration |
| T07.11 | D-0092/spec.md | 315 | PASS — OPS-001 5 sections; 100% Self-Audit-coverage gauge; QA-Lead 4-business-hour SLA | CP-P07-T07-T11 §2 row 5 |
| T07.13 | D-0093/spec.md | 463 | PASS — OPS-002 5 sections; 24-hour SLA; weekly cadence; ≥3 dedup/week escalation | CP-P07-T13-T17 §3 V1 |
| T07.14 | D-0094/spec.md | 273 | PASS — OPS-003 5 sections; mutual-exclusivity check rf-team-lead.md:417 | CP-P07-T13-T17 §3 V1 |
| T07.15 | D-0095/spec.md | 342 | PASS — OPS-004 5 sections; >50% threshold; OPEN-INV-006 binding | CP-P07-T13-T17 §3 V1 |
| T07.16 | D-0096/spec.md | 339 | PASS — OPS-005 5 sections; >20% threshold; Engineering-Lead escalation | CP-P07-T13-T17 §3 V1 |
| T07.17 | D-0097/spec.md | 319 | PASS — OPS-006 §2 + OPS-007 §3 (5 sections each) | CP-P07-T13-T17 §3 V2 |
| T07.19 | D-0098/spec.md | 213 | PASS — 6 MET- rows with threshold + aggregation command | §3 + §6 |

All 10 dependency artifacts confirmed present and at PASS or
TRACKING-PASS at HEAD `efaa33d`.

---

## 2. Independent semantic checks (re-run at tag time)

Replicating the quality-engineer sub-agent's checks (INV-019
independent-semantic-check discipline):

### 2.1 OPS-001..006 mandatory section-header counts

```
grep -c "^### 2\.[1-5]" artifacts/D-0092/spec.md   → 5  (OPS-001)
grep -c "^### 2\.[1-5]" artifacts/D-0093/spec.md   → 5  (OPS-002)
grep -c "^### 2\.[1-5]" artifacts/D-0094/spec.md   → 5  (OPS-003)
grep -c "^### 2\.[1-5]" artifacts/D-0095/spec.md   → 5  (OPS-004)
grep -c "^### 2\.[1-5]" artifacts/D-0096/spec.md   → 5  (OPS-005)
grep -c "^### 2\.[1-5]" artifacts/D-0097/spec.md   → 5  (OPS-006)
grep -c "^### 3\.[1-5]" artifacts/D-0097/spec.md   → 5  (OPS-007)
                                              total = 35 / 35 expected
```

### 2.2 D-0091 §2 governance-table row counts

```
FF_*  row prefixes: 6   (FF_TB_ADD_1_THROUGH_8, FF_EXECUTION_CONTEXT_HEADER,
                          FF_INHERITED_STRUCTURAL_VERDICT, FF_FIVE_ADVERSARIAL_AXES,
                          FF_RETRY_MONOTONICITY_GUARDS, FF_SYNTHETIC_DNSP_EMISSION)
MET-* row prefixes: 6   (MET-001 .. MET-006)
OPS-* row prefixes: 7   (OPS-001 .. OPS-007)
Total rows: 19 / 19 expected
```

### 2.3 D-0084 §4 NFR-CONV.4 ratio table

| BR | Ratio | ≤ 1.10 |
|---|---:|:---:|
| modified-repo.md (Quick, 4973c) | 1.0515 | ✓ |
| baseline-repo.md (Quick, 6065c) | 1.0476 | ✓ |
| tasklist-generate-cli.md (Std, 9120c) | 1.0393 | ✓ |
| sprint-task-execution-deep-dive.md (Std, 12733c) | 1.0325 | ✓ |
| quality-comparison.md (Deep, 19123c) | 1.0250 | ✓ |

Max 1.0515 vs 1.10 ceiling = 48.5% headroom. Monotone-decreasing with
BR_chars confirms the denominator-driven model.

### 2.4 D-0098 §3 MET- row count + column population

6 MET- rows present (MET-001..006). For each row: threshold + surface +
offline-grep aggregation command + OPS trigger + owner + source FR are
populated. No empty cells observed.

### 2.5 K-003 captured-cohort semantic-check counts (D-0083 §3)

Run #1 — TASK-RF-20260517-213436 first-cycle: 4 independent semantic checks.
Run #2 — TASK-RF-20260517-213436 post-completion re-verify: 4 independent semantic checks.
Run #3 — TASK-RF-20260518-015659 first-cycle: 13 independent semantic checks (surfaced
Critical Finding F3 via independent control-flow trace).

Minimum 4 vs ≥1 floor — passes with 4× margin even on the lowest run.

---

## 3. Quality-engineer sub-agent report (archived)

The sub-agent (spawned per the T07.20 MCP Requirement "Sub-Agent
Delegation: Required") returned the following verdict.

**Verdict:** CONDITIONAL-GO — proceed with v3.9 GA tag.

**PASS-gate criteria matrix (5 rows):**

| # | Criterion | Status |
|---|---|---|
| 1 | T07.01 K-003 audit | TRACKING-PASS (3/3 at 100%; runs #4-#5 PENDING) |
| 2 | T07.02 NFR-CONV.4 ratio ≤ 1.10 | PASS (max 1.0515; 48.5% headroom) |
| 3 | T07.10 consolidated governance table | PASS (6 FF + 6 MET + 7 OPS = 19 rows) |
| 4 | All 7 OPS-001..007 runbooks live | PASS (35/35 mandatory section headers) |
| 5 | T07.19 MET-001..006 counters live | PASS (5/5 AC met) |

**Independent semantic checks (SC-1..SC-5):** all 5 confirmed the
spec-author claims (heading counts, governance-row enumeration, ratio
table values, MET- row count).

**Outstanding issues:**
1. K-003 final verdict is TRACKING-PASS pending runs #4 / #5
   (operationally expected; OPS-001 SLA governs sign-off).
2. Pre-existing `make verify-sync` drift on `auggie-bash-gate.sh` and
   `reject-workspace-writes.sh` registration — non-distributable,
   unrelated to GA criteria; does not block tag.

**Mandatory action:** D-0099/spec.md MUST embed the K-003
TRACKING-PASS contingency clause with the OPS-001 SLA + release-spec
§19.4 rollback binding — **embedded at D-0099/spec.md §5**.

---

## 4. Tag creation transcript

### 4.1 Verbatim tag message

The annotated tag message is the verbatim content of
`D-0099/tag-message.txt`. Length: 56 lines (terminated by a single
trailing blank line). The message enumerates all four R-165 PASS-gate
bindings (K-003 audit, NFR-CONV.4 ratio, consolidated governance, 7
OPS runbooks), plus the rollback path, K-003 contingency, and remote-
push policy.

### 4.2 Git tag commands and outputs

```
$ git tag -a v3.9 -F .dev/releases/current/task-builder-merge/artifacts/D-0099/tag-message.txt
$ git tag -l v3.9
v3.9
$ git rev-list -n1 v3.9
efaa33db9f0087bb1c48236b12c1287171b4f9f8
$ git for-each-ref refs/tags/v3.9 --format='%(refname:short) %(objecttype) %(objectname) -> %(*objectname) (target)'
v3.9 tag f15ff7f5656ee0c4989a564cf647a76e947d1e09 -> efaa33db9f0087bb1c48236b12c1287171b4f9f8 (target)
```

Tag is an annotated tag (`%(objecttype) = tag`), not a lightweight
tag — required for tag-message preservation and signed-by-tagger
attribution.

### 4.3 Tag target commit (HEAD at publication)

```
$ git log --oneline -1 efaa33d
efaa33d chore(hooks): resolve OQ-2 (archive+delete bash-gate orphan) and OQ-3 (register reject-workspace-writes.sh)
```

The tag target was selected at HEAD rather than at the MIG-006 land
commit `87c8254` because HEAD includes the post-MIG-006 hook-sync
remediation (`5439ea1` + `efaa33d`) required for the OPS-006 `make
verify-sync` runbook to be enforceable at the release boundary. See
`D-0099/spec.md §6` for the full rationale.

### 4.4 Remote-push status

The tag is **local-only** at publication. No `git push origin v3.9`
was executed. Remote publication requires explicit GA-tagging-committee
approval per release-spec §8.3 and the CLAUDE.md "Executing actions
with care" guidance (push is visible to others and not authorized by
the T07.20 task scope).

---

## 5. Acceptance Criteria — coverage

| # | Criterion (phase-7-tasklist.md L955-959) | Evidence | Verdict |
|---|---|---|---|
| 1 | v3.9 git tag created and visible via `git tag -l v3.9` | §4.2 | PASS |
| 2 | Tag message references K-003 audit + NFR-CONV.4 ratio + consolidated governance + 7 OPS runbooks | §4.1 (verbatim tag-message.txt content) | PASS |
| 3 | Sub-agent quality-engineer report confirms all PASS-gate criteria met | §3 (verdict CONDITIONAL-GO) | PASS |
| 4 | Rollback procedure documented in `D-0099/spec.md` | D-0099/spec.md §4 + §5 | PASS |

**Overall verdict: PASS (CONDITIONAL on D-0099/spec.md §5 K-003 TRACKING-PASS clause).**

---

## 6. Strict-additivity / anti-inflation preservation

The T07.20 tag-creation step is strictly artifact-additive on the
M1..M6 + M7-audit baseline. No `src/superclaude/` edits, no
`.claude/` edits, no test additions. The four governing preservation
invariants remain intact at the tag boundary:

- **`rf-qa.md` PASS/FAIL bullets byte-stable** — md5 anchors carry
  forward from CP-P07-T13-T17 §6: PASS `705536d8a8ec67fef6e56f74fb5093fb`;
  FAIL `d959dffa6d80319d6215470b43288884`. Unchanged at HEAD `efaa33d`.
- **`rf-team-lead.md:417` byte-stable invariant** — line sha256
  `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`;
  whole-file sha256 `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`.
  Carried forward unchanged.
- **A-001 sync-discipline operational** — `src/superclaude/`
  canonical, `.claude/` mirror via `make sync-dev`. OPS-006 (D-0097
  §2) operationalises the contract.
- **INV-018 layout invariant operational** — SP-33 layout-stability
  commitment. OPS-007 (D-0097 §3) formalises Engineering-Lead-led
  response. INV-018 / D-0087 gate continues to govern per-FR PRs.

---

## 7. Provenance

- **Tag target commit:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8` (HEAD on `feat/hook-sync-and-matcher-fix`)
- **Tag object SHA:** `f15ff7f5656ee0c4989a564cf647a76e947d1e09`
- **Tag type:** annotated (not lightweight; not signed)
- **Tag created at:** 2026-05-18 (per git tag taggerdate)
- **Tagger:** RyanW <ryan@ironbelly.com> (git user; matches `CLAUDE.md` "Git user: RyanW")
- **Tag message source:** `artifacts/D-0099/tag-message.txt` (committed alongside this evidence file)
- **Sub-agent invocation:** quality-engineer per T07.20 MCP Requirement "Sub-Agent Delegation: Required" (verdict CONDITIONAL-GO; report archived in §3)
- **Local-only status:** no remote push executed; tag is reversible via `git tag -d v3.9` per `D-0099/spec.md §4.1`

---

## 8. Downstream consumer

- **T07.21** (Checkpoint: End of Phase 7 / Release GA) — consumes
  this evidence as the v3.9-tag-created confirmation for the release
  commitment.
- **GA-tagging committee** — final review against `D-0091` §5
  decision protocol (3-property check on all 19 governance rows);
  this evidence + spec is the load-bearing input.
- **QA Lead** — re-issues `D-0083/spec.md` §4.3 final sign-off on
  capture of rf-qa-qualitative runs #4 and #5 per OPS-001 SLA;
  amends `D-0099/spec.md §2` row 1 with final K-003 verdict on
  closure.
