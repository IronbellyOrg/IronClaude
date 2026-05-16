---
artifact_type: test-strategy
spec_source: .dev/releases/current/release-split-workspace-rca/merged-thesis.md
generated: 2026-05-13
generator: sc-roadmap-protocol v2.0.0
complexity_class: MEDIUM
interleave_ratio: "1:2"
stop_and_fix_thresholds:
  critical: 1
  high: 2
  medium: 5
  low: unbounded
validation_milestones: [M5]
parallel_validation: true
---

# Test Strategy — Release-Split Workspace Misplacement Remediation

## Philosophy: Continuous Parallel Validation

Each milestone ships with parallel validation checks that fire at deliverable completion, not only at milestone end. The interleave ratio is **1:2** — every 2 deliverables triggers a validation checkpoint — appropriate for MEDIUM complexity with one HIGH-impact risk (R-01).

**Why parallel and not gated**: Most deliverables are independently shippable and verifiable (docs, Makefile edits, gitignore). Only D3.1 (the hook) has cross-deliverable coupling worth a strict gate. Running validation in parallel where possible lets M4 proceed alongside M3, per DEP-004.

## Stop-and-Fix Thresholds

| Severity | Definition | Threshold | Action |
|---|---|---|---|
| **CRITICAL** | False positive in hook (legitimate skill file edit blocked) | 1 | Halt M3 immediately; regress D3.1 pattern; do not proceed to M5 |
| **HIGH** | CI runtime delta > 60s OR `make verify-sync` false positive on clean repo | 2 | Investigate before next milestone start |
| **MEDIUM** | Documentation inconsistency between `.dev/README.md` and project CLAUDE.md addendum; or missing sync after src/ edit | 5 | Fix before M5 acceptance run |
| **LOW** | Style nits, message wording polish | unbounded | Track; address opportunistically |

## Per-Milestone Validation

### M1 — Pre-flight & Discoverability

| Deliverable | Validation | Tool | Severity if fails |
|---|---|---|---|
| D1.1 (`.dev/README.md`) | Lists every existing subdirectory of `.dev/`; explicitly contains the `eval-workspaces/` rule string | `Read` + visual check; `ls .dev/` cross-check | MEDIUM |
| D1.2 (CLAUDE.md pointers) | `for f in PLANNING.md TASK.md KNOWLEDGE.md; do grep -q "$f" CLAUDE.md && [ -f "$f" ] || echo "BROKEN: $f"; done` returns empty | Bash | MEDIUM |
| D1.3 (`.gitignore`) | `grep -F '.claude/skills/*-workspace/' .gitignore` returns 1 hit; `git check-ignore .claude/skills/test-workspace/dummy` exits 0 | Bash | LOW |

**Checkpoint CP-M1-END**: All three D1.x assertions pass.

### M2 — Detection Gate

| Deliverable | Validation | Tool | Severity if fails |
|---|---|---|---|
| D2.1 (verify-sync message) | Create synthetic `.claude/skills/foo-workspace/` (no SKILL.md), run `make verify-sync`, assert output contains the redirect-pointing message string `.dev/eval-workspaces/foo/` | Bash + grep | HIGH |
| D2.2 (`*-workspace` blocklist) | Create synthetic `.claude/skills/something-workspace/SKILL.md` (forces the blocklist path, not the missing-SKILL.md path), run check, assert blocklist message appears | Bash + grep | HIGH |
| D2.3 (CI wiring) | Open a draft PR introducing `.claude/skills/test-ws/` empty dir on a feature branch; assert `quick-check.yml` fails with non-zero exit and the error includes the redirect text | GitHub Actions | **HIGH** (closes INV-002) |
| D2.3 negative | Open a draft PR editing only a legitimate skill file (e.g., a typo fix in `src/superclaude/skills/<existing>/SKILL.md`); assert CI passes | GitHub Actions | HIGH |

**Checkpoint CP-M2-END**: Synthetic-bad PR fails, synthetic-good PR passes, message strings asserted.

### M3 — Occurrence Prevention (highest risk)

| Deliverable | Validation | Tool | Severity if fails |
|---|---|---|---|
| D3.1 (hook positive) | Edit a legitimate file inside `.claude/skills/<existing-skill>/` via Claude Code → must succeed without hook firing | Manual Claude session + `Bash` audit log read | **CRITICAL** if blocks |
| D3.1 (hook negative) | Attempt `Write` to `.claude/skills/foo-workspace/anything.md` via Claude Code → must fail with redirect-pointing error | Manual Claude session + `Bash` audit log | **CRITICAL** if allows |
| D3.1 (rewrite behavior) | Verify the hook *rewrites* path to `.dev/eval-workspaces/foo/anything.md` (or rejects clearly — design choice per FR-L1.1); whichever is chosen must be deterministic | Bash + filesystem check | HIGH |
| D3.2 (CLAUDE.md addendum) | `grep -c "skill-creator" CLAUDE.md` ≥ 1; addendum cites *behavior* not file path (no `/config/.claude/plugins/...` substring) | Bash + grep | MEDIUM |
| D3.3 (`make eval-skill`) | `make eval-skill SKILL=demo-skill` creates `.dev/eval-workspaces/demo-skill/` and prints absolute path; idempotent (second invocation does not error) | Bash | LOW |

**Checkpoint CP-M3-END**: Hook positive + negative both pass (R-01 mitigated); CLAUDE.md addendum present; eval-skill target works. **If CRITICAL fails here, M5 must not start.**

### M4 — Defense in Depth (parallel)

| Deliverable | Validation | Tool | Severity if fails |
|---|---|---|---|
| D4.1 (skill guard) | Mock invocation of `sc-release-split-protocol` with `--output .claude/skills/foo/` → must abort with policy message before writing | Manual skill invocation in dry-run | HIGH |
| D4.1 (sync) | `make sync-dev && make verify-sync` clean after edits | Bash | MEDIUM |
| D4.2 (optional siblings) | Same pattern applied to `sc-adversarial-protocol`, `sc-cleanup-audit-protocol` SKILL.md files | Bash + grep | LOW |

**Checkpoint CP-M4-END**: Skill refuses bad output paths; sync clean.

### M5 — Acceptance Validation

| Deliverable | Maps to AC | Validation | Severity if fails |
|---|---|---|---|
| D5.1 | AC1 | Good-faith author scenario — full path | HIGH |
| D5.2 | AC2 | Fresh-clone bypass scenario | HIGH |
| D5.3 | AC3 | Skill direct-routing refusal | HIGH |
| D5.4 | AC4 | Doc-pointer integrity (re-run M1 D1.2 check) | MEDIUM |
| D5.5 | AC5 | Relocated workspace regression | HIGH |

**Checkpoint CP-M5-END (release readiness)**: All 5 AC pass with evidence captured in `roadmap/evidence/` (recommended directory for the eventual tasklist bundle).

## Cross-Milestone Validation

Apart from per-milestone checks, three cross-milestone checks ensure the layered defense composes correctly:

- **X-V1 (after M3)**: Re-run M2.D2.3 negative case (legitimate skill edit PR) to confirm the new hook did NOT introduce a CI false positive. Coupling check between L1 and L2.
- **X-V2 (after M4)**: Run `make sync-dev` then `make verify-sync` — confirms M4's skill edits didn't drift src/ vs .claude/.
- **X-V3 (M5 only)**: AC1 + AC2 must pass on the SAME clone configuration — proves L1 and L2 are not mutually exclusive failure modes.

## Validation Persona Coverage

| Milestone | Reviewer | Focus |
|---|---|---|
| M1 | scribe | Documentation accuracy, pointer integrity |
| M2 | devops | CI behavior, Makefile correctness |
| M3 | security | Hook precision (R-01) — false-positive prevention is the dominant concern |
| M4 | architect | Skill-level policy coherence, sync hygiene |
| M5 | quality | End-to-end coverage; trace AC ↔ evidence |

## Edge Cases to Probe Explicitly

- **EC-1**: Hook pattern that matches `.claude/skills/foo/workspace.md` (a single file ending in "workspace.md", not a directory) — should NOT fire. Add to D3.1 negative test set.
- **EC-2**: A legitimate skill named `foo-workspace` (suffix collision) — extremely unlikely; if encountered, fall back to R-05 mitigation (overridable error).
- **EC-3**: Workspace path on Windows-style separators in the hook — N/A for Linux-only CI, document as known limitation.
- **EC-4**: `make verify-sync` invoked outside the repo root — confirm existing behavior unchanged by M2 edits.
