# sc:reflect Rebuild — Variant Diff Analysis (Step 1)

## 1. Metadata

- Generated: 2026-05-26T22:19:03Z
- Variants compared: 5
- Total differences found: 64
- Categories: structural (12), content (18), contradictions (14), unique (15), shared assumptions (5)

Source files (all under `.dev/brainstorms/sc-reflect-rebuild/adversarial/`):

- `variant-1.md` (658 lines)
- `variant-2.md` (650 lines)
- `variant-3.md` (569 lines)
- `variant-4.md` (586 lines)
- `variant-5.md` (864 lines)

---

## 2. Structural Differences

| # | Area | V1 | V2 | V3 | V4 | V5 | Severity |
|---|------|----|----|----|----|----|----------|
| S-001 | Total H2 section count | 16 | 18 | 15 | 16 | 13 | Low |
| S-002 | Total file length (lines) | 658 | 650 | 569 | 586 | 864 | Low |
| S-003 | Tier-Decision Rubric placement (vs Wave/Tier Architecture) | Embedded inside Wave Architecture §4 (Wave 2.5) | Dedicated §5 BEFORE Wave Architecture §4 reference | §4 BEFORE Wave Architecture §5 | §8 (after Eval Rubric §9), separate from Wave §3 | §3 BEFORE Wave Architecture §4 | Medium |
| S-004 | Wave count (top-level) | 9 (Wave 0-8) | 7 (Wave 0-6) | 6 (Wave 0-5) | 9 (Wave 0-8) | 7 (Wave 0-6) | Medium |
| S-005 | Wave numbering uses fractional waves (e.g., Wave 1.5, 2.5) | Wave 2.5 (Tier Gate) | None — linear | None — linear | None — linear | Wave 1.5 (Memory Load) | Low |
| S-006 | Hierarchy max nesting depth | H4 (### 3.1, 5.1, etc.) | H4 (### 3.1, 5.1, 5.2…) | H3 only | H3 + ### subsections | H4 (### 8.1, 9.1…) | Low |
| S-007 | Build Path section position | §11 (after Eval Rubric §10) | §13 (after Eval §12) | §10 (after Eval §9) | §12 (after Eval §9–11) | §8 (BEFORE Eval §11) | Medium |
| S-008 | Return Contract section position | §5 (early, after Wave Arch) | §9 (mid, after Cross-Skill) | §3 (very early, before Tier Rubric) | §13 (late, near end) | §10 (late, after Ops §9) | Medium |
| S-009 | "Triggers" section present as required by sibling pattern | Yes §1 | Yes §2 | Yes (after frontmatter) | Yes (after frontmatter) | Yes (after frontmatter) | Low |
| S-010 | Dedicated "Hallucination Guardrails" section | No (inline in §10 Eval + §6) | Yes §11 (5 subsections) | No | No (inline in §1 + §6) | No (inline in §1 + §5) | Medium |
| S-011 | Dedicated "Kill List" / "Will Not Do" section structure | §15 "Will / Will Not" | §17 "Boundaries: Will/Will Not" | §12 Boundaries + §13 Kill List (separate) | §15 Boundaries | §13 Boundaries (Will/Will Not) | Low |
| S-012 | "Ops Integration" / Makefile / sync-dev section | Absent | Absent | Absent | Absent | Yes §9 (4 subsections) | High |

**Mandate coverage gap audit:**

- All 5 variants present: Triggers, Required Input + Mode Selection, Wave Architecture, Tier-Decision Rubric, Eval Rubric, Build Path Decision, Cross-Skill Integration, Return Contract, Modern Serena Usage, Error Handling, Boundaries.
- Variant 5 is the ONLY variant with a dedicated Ops Integration section (Makefile targets, PreToolUse hook awareness, sync-dev/verify-sync compliance, CI cadence) — this drives S-012 to High severity.
- Variant 3 is the ONLY variant with a dedicated "Kill List" section enumerating deliberately-excluded features with justification.
- Variant 2 is the ONLY variant with a dedicated "Hallucination Guardrails" section (5 enumerated structural guards in §11).
- Variant 4 is the ONLY variant with a dedicated "Testability Map" section (§16) linking each protocol decision to an eval assertion.

---

## 3. Content Differences

| # | Topic | V1 Approach | V2 Approach | V3 Approach | V4 Approach | V5 Approach | Severity |
|---|-------|-------------|-------------|-------------|-------------|-------------|----------|
| C-001 | Tier-decision rubric structure | 9-row table of named signals + override matrix (rule-based; numeric thresholds inline) | Hard-overrides table + 8-row priority decision logic (priority-rule based) | 4-signal threshold table + scope rules (rule-based, fewer signals) | Additive `complexity_score` formula (4 weighted scores summing to ≤1.0) + bonus | 5-signal 0-2 point composite scoring (max 10 points) + override modifiers | High |
| C-002 | Coverage threshold for T1 STOP | ≥0.95 AND drift=0 AND regression=0 AND ≤5 files | C≥0.90 + S_scope≤5 + S_domains==1 + density≤0.05 (rule 1) | coverage_pct≥0.85 AND deviations=0 AND ≤3 files | coverage_gap_rate=0 AND stakes<0.30 AND confidence≥0.85 | coverage≥90% AND single-domain AND confidence≥0.85 | High |
| C-003 | Coverage threshold for T2 escalation | <0.80 | (covered by S_dev_density >0.20 rule 5) | <0.70 | coverage_gap_rate>0 OR conflict>0.20 | (covered by composite score ≥6) | High |
| C-004 | Convergence threshold for adversarial PASS | 0.75 (default) | 0.75 (matches sc-adversarial default; PARTIAL ≥0.60) | 0.65 | not explicitly numeric — "two reviewers disagree on final verdict" | 0.65 PASS / 0.50 PARTIAL | High |
| C-005 | Convergence threshold for adversarial FAIL | <0.60 | <0.60 (FAIL) | <0.65 surfaces both as `unresolved_conflict` | not explicit | <0.50 | Medium |
| C-006 | think_about_* Serena tools handling | Optional scripted "MAY be wired in"; NOT load-bearing (§7 + §15) | Mandatory scripted nudges with audit-log capture; NOT load-bearing (§6.4) | Explicitly eliminated entirely ("Zero references", §6) | Mandatory checkpoint gates with logged routing decisions (§4 Wave 1.5 + §5) | Mandatory scripted checkpoints at defined moments (Wave 1, Wave 5) (§5) | High |
| C-007 | think_about_* tools in allowed-tools frontmatter | NOT listed | NOT listed | NOT listed | LISTED (`mcp__serena__think_about_collected_information` etc.) | NOT listed | High |
| C-008 | Build path pick | Hybrid (skill-creator iterations → sprint CLI production) | Hybrid (skill-creator + local grader.py → sprint CLI later) | Skill-creator first → Sprint CLI for production | Skill-creator-style iteration first → Sprint CLI after stabilizes | Hybrid (skill-creator + hand-author + sync → Sprint CLI integration) | Low |
| C-009 | UC-1 vs UC-2 mode selection mechanism | Auto-detect, 6 ordered rules, first match wins; `--mode` overrides | Explicit `--mode` wins unconditionally; auto-detect only when unset (4 rules) | Auto-detect from input shape (3 rules); ambiguous → STOP | Auto-detect from 4-row signal table; both present → `post` | Auto-detect from 4-row signal table; both present → `post`; ambiguous → STOP | Medium |
| C-010 | T2 multi-model topology | 2-3 reviewers; rotate opus/sonnet/haiku; 3rd reviewer "explicitly heterogeneous" cross-vendor | 2 (sonnet+haiku) or 3 (+ qwen/kimi/deepseek or opus); enterprise = sonnet+haiku+opus | 2-3 agents (calibrator sonnet, root-cause sonnet/opus, optional quality-engineer haiku) | 5-role reviewer topology table (coverage/qualitative/root-cause/code-system/calibrator) | 2-3 reviewers based on available aliases; opus+sonnet+haiku trio default | High |
| C-011 | Reviewer agent role assignments (UC-2 default) | rf-qa + rf-qa-qualitative + root-cause-analyst | rf-qa + rf-qa-qualitative + root-cause-analyst (with calibrator) | confidence-calibrator + root-cause-analyst + optional quality-engineer | rf-qa + rf-qa-qualitative + root-cause-analyst + quality-engineer/auggie-reviewer + calibrator | root-cause-analyst + rf-qa + rf-qa-qualitative + confidence-calibrator | Medium |
| C-012 | New agents proposed vs reuse-only | Reuse only; explicitly defers coverage-mapper / deviation-classifier to v1.1 (§9) | Reuse only; §7.2 explicitly rejects 4 candidate new agents | Reuse only; §13 Kill List explicitly excludes coverage-mapper + deviation-classifier | Reuse only; §7 closing note: new agents must be justified by eval failures | Reuse only; no new agents proposed | Low |
| C-013 | Eval rubric dimension count | 6 dimensions | 5 dimensions | 5 dimensions | 7 dimensions | 5 dimensions | Medium |
| C-014 | Eval rubric aggregate ship threshold | T1 ≥80% assertion pass; T2 ≥90%; ≥4.0 average per dimension | T1 ≥80%, T2 ≥90%; per-dim threshold 0.75-0.95 by dimension | Aggregate ≥3.5/5 (70%) on held-out | Aggregate qual ≥4.0/5 + deterministic ≥0.85 (≥0.90 held-out) | T1 ≥80% / T2 ≥90% / ship ≥85% held-out; ≥3.5/5 weighted | Medium |
| C-015 | Deviation taxonomy (4-category specification) | 4-cell defined inline in Wave 2 step 4 (Authorized expansion / Necessary deviation / Drift / Regression) | 4-category with full definitions, detection signals, gold-standard refs, default remediation per category (§10) | 4-category in Wave 1 step 5 (Authorized expansion / Necessary deviation / Drift / Regression) | 5-category (adds `unknown` to the 4) | 4-category table in Wave 3 with examples | High |
| C-016 | Deviation classification precedence rule | Not stated explicitly | Stated explicitly: Regression > Drift > Necessary > Authorized (§10.5) | Default to Drift on ambiguity (conservative) | Not stated explicitly (uses `unknown` class as escape) | Not stated explicitly | Medium |
| C-017 | Iteration-cycle convergence signal | Iteration N+1 vs N improvement <5% absolute on held-out | <5% absolute improvement on held-out (60/40 split) | <5% absolute improvement | <5pp deterministic AND <0.20/5 qualitative on held-out with no auto-fail | <5% absolute improvement on held-out (60/40 split) | Low |
| C-018 | Judge-model selection strategy | Different + more capable than skill-under-test; opus solo grader | Different + more capable; default opus; optional 3-model jury via `--jury` | Opus grading Sonnet/Haiku; never self-grade | Different + more capable + not a reviewer participant; optional second-judge calibration on ≥20% | Different (implied; not strongly specified beyond rubric description) | Medium |
| C-019 | Return contract field count (stable block) | ~28 fields including asymmetric_flags sub-block | ~22 fields including deviation_count_by_class sub-block | ~14 fields (leanest) | ~18 fields | ~15 fields | Medium |
| C-020 | Number of refs files (loaded on-demand) | 6 (tier-rubric, coverage-matrix-template, deviation-taxonomy, reflection-card-template, report-template, remediation-handoff) | 7 (input-resolution, reflection-rubric, deviation-taxonomy, coverage-mapping, reviewer-spec, report-template, remediation-handoff) | 2 (coverage-map-template, report-template) — explicitly minimalist | (Not explicitly listed as a refs section) | 4 (calibration-rubric, report-template, deviation-taxonomy, review-checklist) | Medium |

---

## 4. Contradictions

| # | Claim | V1 | V2 | V3 | V4 | V5 | Severity |
|---|-------|----|----|----|----|----|----------|
| X-001 | T1 coverage-floor threshold | ≥0.95 | ≥0.90 (rule 1) | ≥0.85 | =1.00 (`coverage_gap_rate=0`) | ≥0.90 | High |
| X-002 | T2 coverage-trigger threshold | <0.80 | uses S_dev_density>0.20 (not coverage directly) | <0.70 | >0 gap | composite score ≥6 (not coverage directly) | High |
| X-003 | Convergence threshold for adversarial PASS | 0.75 | 0.75 | 0.65 | not explicit numeric | 0.65 | High |
| X-004 | T1 max-files for stop | ≤5 files | ≤5 files (rule 1); ≤10 files (rule 2) | ≤3 files | not file-count based (uses blast_radius_score) | scope_size <5 = 0pts | Medium |
| X-005 | think_about_* status — current vs deprecated vs load-bearing | CURRENT but optional self-nudges; NOT load-bearing (§7) | CURRENT scripted nudges; NOT load-bearing (§6.4) | DEPRECATED ("legacy surface"); eliminated entirely (§6) | CURRENT mandatory checkpoint gates (§4 Wave 1.5 + listed in allowed-tools) | CURRENT mandatory scripted checkpoints (§5) | High |
| X-006 | Whether think_about_* tools appear in allowed-tools frontmatter | No | No | No | Yes (all three listed) | No | High |
| X-007 | Number of waves | 9 | 7 | 6 | 9 | 7 | Medium |
| X-008 | Whether mode selection allows "both present" → which mode | "input includes both tasklist AND completed-work" → post (rule 4) | "if diff/log/working tree" → post (rule 2) | "diff/commit/output-dir" → post; ambiguous → STOP | "Both plan and diff present" → post with plan as source-of-truth | "Both present" → post (post subsumes pre) | Low |
| X-009 | Deviation taxonomy category count | 4 | 4 | 4 | 5 (4 + `unknown`) | 4 | Medium |
| X-010 | Whether classification precedence is explicitly defined | No | Yes (Regression > Drift > Necessary > Authorized, §10.5) | Yes (Drift as default on ambiguity, §1.5) | No (uses `unknown` to escape) | No | Medium |
| X-011 | Eval rubric dimension count | 6 | 5 | 5 | 7 | 5 | Medium |
| X-012 | T2 reviewer agent set (UC-2 default) | rf-qa + rf-qa-qualitative + root-cause-analyst (drop rf-qa-qualitative on N=2 fallback) | rf-qa + rf-qa-qualitative + root-cause-analyst (with implicit calibrator pass) | confidence-calibrator + root-cause-analyst (+ optional quality-engineer) — CALIBRATOR-AS-REVIEWER | 5-role topology: rf-qa + rf-qa-qualitative + root-cause-analyst + (quality-engineer OR auggie-reviewer) + calibrator | root-cause + rf-qa + rf-qa-qualitative + confidence-calibrator | High |
| X-013 | Build path pick (Sprint vs skill-creator vs hybrid) | Hybrid (skill-creator iter → sprint production) | Hybrid (skill-creator + grader.py → sprint later) | Skill-creator first → Sprint CLI for production (sequential, not hybrid label) | Skill-creator iterative first → Sprint CLI after stabilizes (sequential) | Hybrid explicitly named (skill-creator + hand-author + Sprint CLI integration) | Medium |
| X-014 | Whether the protocol persists Serena memory keys with project-slug suffix | Yes (`reflection/last-pass-{project-slug}`, `/deviation-patterns/{slug}`, `/false-positives/{slug}`) | Yes (`reflect/last-pass-{slug}`, `/deviation-patterns-{slug}`) | Yes (`reflection-last-pass-{project-slug}`) — single key only | Yes (`reflection/last-pass/<project-slug>`, `/deviation-patterns/<slug>`, `/false-positives/<slug>`) | Yes (`reflection/<project-slug>/last-pass`, `/deviation-log-<date>`) — different ordering | Low |

---

## 5. Unique Contributions

| # | Idea | Variant | Description | Value |
|---|------|---------|-------------|-------|
| U-001 | Ops Integration section (Makefile targets + PreToolUse hook + CI cadence) | V5 | Dedicated §9 enumerating `make reflect-eval`, `make reflect-eval-quick`, `make eval-skill SKILL=...`, plus hook compliance and verify-sync pre-commit workflow | High |
| U-002 | Dedicated Hallucination Guardrails section (5 structural guards) | V2 | §11 enumerates Grounded vs `[INFERRED]` binary, evidence-validator final gate, blind calibration, heterogeneous reviewer ensemble, citation re-Read window, inferred-claim audit | High |
| U-003 | Classification precedence rule (Regression > Drift > Necessary > Authorized) | V2 | §10.5 — "rationale does not authorise contradiction"; resolves multi-signal ambiguity deterministically | High |
| U-004 | `[INFERRED]` tag as a first-class claim category (binary with Grounded) | V2 | §11.1 — every claim is one of two tags; un-taggable findings are dropped; inferred count surfaced in report header | High |
| U-005 | Zero-drop evidence-validator pass treated as audit FLAG (suspicious, not clean) | V2 | §11.2 — "a pass that drops zero items is suspect"; 0-dropped sets `zero-drop-flag: true` for meta-eval spot-check | High |
| U-006 | Inferred-claim audit threshold (auto-WARN when inferred > total/2) | V2 | §11.6 — soft signal that report is more inference than evidence | Medium |
| U-007 | Testability Map (each protocol decision → eval assertion) | V4 | §16 — protocol step that cannot map to assertion should be simplified or removed | High |
| U-008 | Detailed `citation_resolves` Python implementation sketch | V4 | §11 — provides actual implementation code with fixture-root remapping for synthetic eval diffs | High |
| U-009 | 6 new grader.py assertion types proposed (vs 1-3 in others) | V4 | §11 — `citation_resolves`, `regex_present`, `regex_absent`, `yaml_list_contains`, `matrix_covers_items`, `checkpoint_logged` | Medium |
| U-010 | think_about_* tools declared in `allowed-tools` frontmatter | V4 | Frontmatter line 7 — only variant that wires the three tools as first-class declared MCP surface | Medium |
| U-011 | Iteration-3 "held-out hardening" pass with seeded traps | V4 | §9.4 — third iteration adds 12-15 cases with seeded false citations, authorized deviation, regression, missing tests, recommendation-scrutiny traps | Medium |
| U-012 | Composite tier score as additive 0-2-point system (5 signals → 0-10 scale) | V5 | §3 — explicit point-based scoring vs others' threshold-based rule matching | Medium |
| U-013 | Explicit env-var awareness for model aliases (ANTHROPIC_DEFAULT_*) | V5 | §4 Wave 0 step 6 + §13 — checks env vars and degrades gracefully on missing aliases | Medium |
| U-014 | Kill List as dedicated section with justifications | V3 | §13 — 5 deliberately-excluded features with rationale (coverage-mapper, deviation-classifier, streaming dialogue, knowledge graph, T1 multi-model) | Medium |
| U-015 | Multi-domain detection adds +3 to tier score (special rule) | V5 | §3 override — "Multi-domain span detected... adds +3 to score" | Low |

---

## 6. Shared Assumptions (AD-2)

All 5 variants implicitly agree on the following points. Each is classified as STATED (explicitly named in at least 4 variants) / UNSTATED (assumed without statement in any variant) / CONTRADICTED. UNSTATED assumptions are promoted to synthetic [SHARED-ASSUMPTION] diff points (A-NNN).

| # | Assumption | Classification | Promotion |
|---|------------|----------------|-----------|
| A-001 | The user is technically capable of reading a 400-700 line SKILL.md and translating section refs into action | UNSTATED across all 5 | PROMOTED as A-001 |
| A-002 | The `ANTHROPIC_DEFAULT_OPUS_MODEL` / SONNET / HAIKU env-var aliases will remain set in the user's environment (only V5 partially addresses with a degraded-mode warning; others assume present) | UNSTATED in V1-V4; partially STATED in V5 | PROMOTED as A-002 |
| A-003 | The `.dev/eval-workspaces/sc-reflect/` workspace path is the right naming (no variant proposes `.dev/eval-workspaces/sc-reflect-protocol/` — except V5 which uses `sc-reflect-protocol` in §9.2, contradicting the others) | STATED in 4 (V1-V4); CONTRADICTED in V5 | Already counted in S-NNN context (contradiction noted) |
| A-004 | sc-adversarial Mode A (`--compare`) is the right merge mechanism (none considers Mode B `--generate` or any other merge approach) | STATED in all 5 | Not promoted (consensus) |
| A-005 | The user wants reflection to STOP and ask rather than auto-execute when confidence is low or input is ambiguous | STATED in all 5 (via STOP conditions) | Not promoted (consensus) |
| A-006 | Reusing existing agents (confidence-calibrator, evidence-validator, rf-qa, root-cause-analyst) is strictly better than authoring new agents (coverage-mapper, deviation-classifier) | STATED in all 5 — universal reuse-only posture | Not promoted (consensus) |
| A-007 | The output dir convention `.dev/reflect/<mode>-<slug>-<timestamp>/` is acceptable (V1, V2, V3, V5 all use this shape; V4 uses `.dev/reflect/<timestamp>-<slug>/`) | UNSTATED — no variant justifies why `.dev/reflect/` is the right parent vs `.dev/reflections/` or `.dev/sc-reflect/` | PROMOTED as A-003 |
| A-008 | The 60/40 train/test split (Anthropic skill-creator default) is the right split for reflect's eval matrix specifically | UNSTATED — all cite it as Anthropic-default, none justify why it fits reflect's narrow eval domain | PROMOTED as A-004 |
| A-009 | The 4-category deviation taxonomy is exhaustive (covers every real-world divergence; V4 alone hedges with a 5th `unknown` class) | STATED-as-axiom in V1, V2, V3, V5; CONTRADICTED by V4 | Already counted (X-009) |
| A-010 | The skill operates on a single repo / single project context (no variant considers multi-repo or cross-project reflection state) | UNSTATED in all 5 | PROMOTED as A-005 |

---

## 7. Summary

- Total S-NNN: **12**
- Total C-NNN: **20**
- Total X-NNN: **14**
- Total U-NNN: **15**
- Total A-NNN promoted: **5**
- Highest-severity items: **X-001, X-002, X-003, X-005, X-006, X-012, C-001, C-002, C-003, C-004, C-006, C-007, C-010, C-015, S-012, U-001, U-002, U-003, U-004, U-005, U-007, U-008**
- Convergence-detection denominator: **total_diff_points = S + C + X + A = 12 + 20 + 14 + 5 = 51** (per spec)
