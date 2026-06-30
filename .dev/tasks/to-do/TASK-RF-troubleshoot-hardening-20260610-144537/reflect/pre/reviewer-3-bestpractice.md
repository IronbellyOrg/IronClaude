# Reviewer 3 — Best-Practice / Actionability Lens (Pre-Execution Reflection)

**Role:** REVIEWER 3 (refactorer/architect — "is it well-formed and will it execute cleanly")
**Task under review:** `TASK-RF-troubleshoot-hardening-20260610-144537`
**Spec:** `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md`
**Date:** 2026-06-10

All line citations below are to the tasklist file
`.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260610-144537/TASK-RF-troubleshoot-hardening-20260610-144537.md`
unless prefixed with `SPEC §`, `CLAUDE.md`, or `SKILL.md`. Live-source anchors were
re-verified by Read/Grep within this turn (S1/S3/S4 freshness discipline).

---

## Dimension 1 — Self-containment (B2) — Score: 5/5

Every build item embeds context + action + output + verification + completion gate, and
agent-spawning items embed the FULL adversarial prompt inline.

Evidence:

- Each Phase 2 build item follows the same five-part shape: a `Read <spec §> + discovery
  inventory + research §` context preamble, an explicit `then create/edit <abs path>`
  action, a literal section/field enumeration as the output spec, an `ensuring …`
  verification clause, and a templated blocker-log + "mark complete" gate. Example: Step
  2.1 (line 184) names the spec sections to extract (§4/§6.1/§6.2/§7-H0/§7-H5/§8), the
  target path, every `##` section to emit in order, the lowercase/uppercase token
  discipline, the MD024 no-dup-heading guard, and the blocker fallback — all in one item.
- Agent-spawning items embed the complete prompt verbatim, not a reference. Steps 4.2–4.9
  (lines 296–324), 4.12–4.13 (336, 340), 5.1–5.2 (352, 356), 5.5a (368) each contain a
  full quoted `"Assume … Find them. Read … verify … Report-only — do NOT modify any
  file."` prompt plus the exact output-report path and the binary PASS/FAIL verdict
  contract. The executor never has to author a prompt.
- Verification is concrete and re-runnable: Phase 3 items pin exact shell commands and
  literal success strings — Step 3.2 (line 276) requires the output contain
  `✅ All components in sync.`; Step 3.4 (line 284) pins the `git status --porcelain |
  grep '^[AM].*\.claude/'` discipline check.

No gap found. This is unusually strong self-containment.

---

## Dimension 2 — Granularity (A3) — Score: 5/5

One item per file/component; no batch items; the three declared item-splits are clean and
each half edits exactly one insertion point.

Evidence:

- Phase 2 header (line 178) states the invariant: "Each item creates or edits exactly ONE
  file (or ONE insertion point). DO NOT batch." The 5 new refs are 5 separate items (2.1–
  2.5, lines 182–208); the 4 edited files are decomposed by insertion point.
- **Output-contract split 2.8a/2.8b** (lines 222/226) is clean: 2.8a appends the 5
  non-gate rows; 2.8b appends the 4 `*_status` + 4 `*_card_path` rows and the M7 note.
  Both halves edit the same `## Output Contract` table but at sequential append points,
  and 2.8b explicitly reads the discovery inventory "to confirm the rows appended in Step
  2.8a are now the last rows" (line 228) — a correct intra-split ordering dependency.
- **Failure-wiring split 2.11a/2.11b/2.11c** (lines 238/242/246) is clean and targets
  three DISTINCT seams: 2.11a adds the calibration-style completeness gate; 2.11b tightens
  the Wave 6 precondition; 2.11c appends one `## Will Not Do` bullet. No overlap.
- **M4 verification split 5.5a/5.5b/5.5c** (lines 366/370/374) is clean: 5.5a spawns the 2
  report-only verifiers, 5.5b consolidates + spawns ONE serialized re-fixer, 5.5c is
  loop-control. This correctly separates the report-only and fix-authorized roles into
  different items (I20 serialized-fix discipline).

No batch items detected. No gap.

---

## Dimension 3 — Convention-compliance — Score: 5/5

Edits land ONLY under `src/superclaude/`; sync-dev then verify-sync; `.claude/` never
staged; new refs are no-frontmatter + single-H1 (MD025) with language-tagged fences
(MD040).

Evidence (all cross-checked against `CLAUDE.md` ABSOLUTE RULES and live source):

- **src-only edits:** Every Phase 2 path is under `src/superclaude/...` (lines 180, 186,
  192, 198, 204, 210, 220, 250, 260). Key Constraint (line 116): "Edit ONLY
  `src/superclaude/`; NEVER stage `.claude/` mirrors." This matches CLAUDE.md SoT rule.
- **sync → verify-sync:** Step 3.1 runs `make sync-dev` (line 272), Step 3.2 runs
  `make verify-sync` requiring the literal in-sync string (line 276). Correct order.
- **Never-stage `.claude/`:** Step 3.4 (line 284) actively greps for staged `.claude/`
  paths and FAILS if any (other than `settings.json`) is staged; the fix is
  `git restore --staged`, with an explicit "never use `git add -f`" — verbatim alignment
  with CLAUDE.md's `-f`-is-the-siren rule. The fix-agent items (4.11 line 332, 5.4 line
  364, 5.5b line 372) each repeat "NEVER the `.claude/` mirror."
- **MD025 / MD040:** Phase 2 header (line 178) mandates "NO YAML frontmatter and exactly
  ONE `# Title` heading on line 1 (MD025), every fenced block MUST carry a language tag
  (`text` … `markdown` — MD040) … no trailing whitespace and exactly one trailing
  newline (MD009/MD047)." Each new-ref item restates its single `# Title` (e.g. 2.2 line
  190 `# Runtime-Entrypoint Verification (Gate H1)`).
- **Column-count correctness [verified]:** I confirmed the live `## Output Contract` table
  in `SKILL.md` is 3-column `| Field | Type | Description |` with `diagnosability_hard_stop`
  as the last data row. Steps 2.8a/2.8b's CRITICAL instruction to FOLD the §6.2 `Default`
  into the Description cell rather than add a 4th column (lines 224/228) is exactly right —
  a 4th column would trip MD056. This is a precise, convention-correct call.

No gap.

---

## Dimension 4 — Anti-orphaning — Score: 5/5

Completion items are in the final phase; the POST-reflect gate is the penultimate item in
self-run form.

Evidence:

- The "Update status to 🟢 Done" item (line 390) is the LAST checklist item, preceded by
  the POST-reflect gate (line 388), which is explicitly tagged "This POST-reflect gate is
  the PENULTIMATE item — it runs immediately before the final 'Update task status to
  Done' item, so it audits the complete final state including the Task Summary." Correct
  anti-orphaning placement.
- **POST-reflect self-run form [verified against SPEC scope]:** Step (line 388) spawns a
  subagent running `/sc:reflect --mode post --remediate --diff <BASE> --tasklist … --spec
  …` where `<BASE> = git merge-base HEAD <integration-branch>`, `<integration-branch>`
  resolved via `git symbolic-ref --short refs/remotes/origin/HEAD` (→ `origin/master`),
  passed as a SINGLE ref so the diff is the merge-base WORKING-TREE diff. It also runs
  `git add -A` first "so newly-created untracked refs are captured in the diff surface."
  This is the correct penultimate self-run form and correctly avoids the `start_commit..HEAD`
  base bug (matches repo memory `reference_sprint_rerun_tasks` sibling fix and the recent
  commit `10723863 fix(task-builder): base POST-reflect --diff on merge-base working-tree`).
- Post-Completion Actions (lines 380–386) verify deliverables exist, record the
  no-testing rationale, re-confirm M3/M4 verdicts, and write the Task Summary — all in the
  final phase, none orphaned mid-pipeline.

No gap.

---

## Dimension 5 — QA-gate sufficiency — Score: 5/5

The M3 final gate has ≥8 lens agents + a serialized fixer; the M4 source-fidelity gate is
present and mandatory for the spec→protocol transform.

Evidence:

- **M3 = 8 lenses + serialized fixer:** Phase 4 (line 288) declares "4 rf-qa structural
  lens agents + 4 rf-qa-qualitative content lens agents (8 total), all spawned with
  `fix_authorization: false`, then serialized fix (one fixer, I20)." The 8 are individually
  itemized: structural template-conformance (4.2), internal-consistency (4.3),
  markdownlint-compliance (4.4), cross-reference-integrity (4.5); content spec-fidelity
  (4.6), completeness-vs-spec-§7 (4.7), command-thinness/acceptance-#1 (4.8),
  blocking-rule-accuracy (4.9). Serialized fixer at 4.11 (line 332) with the explicit
  "ONLY agent permitted to modify … NEVER spawn multiple fixers." Verification round +
  max-3-cycle control at 4.12–4.14.
- All 8 lens prompts carry the rf-qa adversarial pattern (`fix_authorization: false` +
  "Assume … at least N errors. Find them.") — aligned with repo memory
  `feedback_rfqa_adversarial_pattern`. Adversarial framing N=10 set for the 500–1500 line
  tier (line 288).
- **M4 source-fidelity gate present + mandatory:** Phase 5 (line 348) states "This task
  TRANSFORMS the driving spec into refs/skill content, so the M4 gate is MANDATORY (I21).
  Full intensity: ≥2 fidelity agents reading BOTH the spec and the generated output."
  Agents 5.1 (line 352) and 5.2 (line 356) each read BOTH spec AND output; 5.1 covers
  §4/§6/§8 + report/hub, 5.2 covers the §7 H1/H2/H3/H4 literal cards/ledgers — a sound
  division of the byte-faithful surface. Serialized fix + 2-agent verification +
  max-3-cycle control follow (5.4–5.5c).

No gap. Both gates meet the lens-count and serialization bar.

---

## Dimension 6 — Actionability — Score: 5/5

Every item names file + change + verifier; no vague "verify it works."

Evidence:

- Validation items pin exact commands and exact pass criteria, not prose: 3.1
  `make sync-dev 2>&1` → capture to a named file (line 272); 3.2 PASS REQUIRES literal
  `✅ All components in sync.` (line 276); 3.3 names the 9 exact `.md` paths and the
  `pre-commit run markdownlint --files <paths>` invocation with named rule codes (MD025/
  MD040/MD024/MD047) (line 280); 3.4 the porcelain grep (line 284).
- Edit items name the file, the anchor TEXT to match, and the literal content to write —
  e.g. 2.10 (line 236) gives the 5 exact registry rows verbatim
  (`` | `refs/pipeline-hardening-closure.md` | Wave 4.5 (pipeline-hardening mode) | ``,
  etc.); 2.11c (line 248) gives the exact `## Will Not Do` bullet string.
- Anchor discipline is explicit and correct: Step 1.4 (line 174) builds an
  `insertion-anchors.md` inventory of verbatim `old_string` anchors, and every edit item
  reads it and is told to "Anchor every Edit on exact current TEXT … NOT on absolute line
  numbers" (line 178, repeated per item). This is the right hedge against the known
  off-by-one trailing-newline artifact (GF-1, Key Constraint line 118).
- QA verdicts are binary and evidence-bound ("FAIL on ANY issue of any severity", line
  296), not "looks good."

No gap.

---

## Dimension 7 — G1 discipline — Score: 5/5

The tasklist correctly treats this as a G1-stage spec: it records the user's `/task`
execution instruction as the G1-approval basis and does not silently edit the
forbidden-until-G1 files without an acknowledgement.

Evidence:

- SPEC §5 (line 5), §9 (lines 396–400), and §12 (line 443) forbid editing
  `troubleshoot.md`, `SKILL.md`, `report-template.md`, and `remediation-handoff.md` until
  G1 approval. The tasklist Open Question 1 (line 150) records: "The user invoking
  task-builder and directing execution via `/task` IS the human G1-approval signal …
  Phase 1 records this approval basis (Step 1.3) as an acknowledgement before any edit
  item runs — it is NOT a blocking HALT."
- Step 1.3 (line 170) is a dedicated, ordered item that reads SPEC §5/§9/§12, re-reads
  Open Question 1, and writes a G1-approval acknowledgement entry naming the four
  forbidden files and the spec sections by number — BEFORE any Phase 2 edit item runs. It
  is explicitly "a RECORDED ACKNOWLEDGEMENT, not a human-HALT gate," which is the correct
  reading: the user's act of running `/task` on this tasklist is itself the approval, so a
  blocking HALT would be a deadlock, but a silent edit with no recorded basis would
  violate the spec's halt condition. The chosen middle path (acknowledge-then-proceed) is
  the best-practice resolution.
- This is consistent with repo memory `feedback_human_decision_items_must_halt` in spirit:
  the item does not auto-apply a forbidden change without surfacing the approval basis;
  it records the basis factually first.

No gap.

---

## Score summary

| Dimension | Score |
|---|---|
| 1. Self-containment (B2) | 5 |
| 2. Granularity (A3) | 5 |
| 3. Convention-compliance | 5 |
| 4. Anti-orphaning | 5 |
| 5. QA-gate sufficiency | 5 |
| 6. Actionability | 5 |
| 7. G1 discipline | 5 |

**Mean = 35 / 7 = 5.00**

## best_practice_grade = 5

---

## Findings (gaps) — by severity

No CRITICAL or IMPORTANT actionability/convention gaps found. The following are MINOR /
advisory observations only; none block execution.

- **[MINOR] F1 — POST-reflect placeholder tokens are runtime-resolved, not pre-filled
  (line 388).** The reflect command embeds `<BASE>`, `<integration-branch>`, and
  `<EXECUTOR_CLASS>` as literals to be computed at run time (`git merge-base`,
  `git symbolic-ref`, executor model class). The item gives the resolution recipe inline,
  so a careful executor resolves them correctly, but a literal paste without substitution
  would fail. This is standard for self-run reflect items and the recipe is present, so it
  is informational, not a defect. [INFERRED] severity MINOR.

- **[MINOR] F2 — markdownlint invocation is "discover-the-equivalent" rather than a single
  pinned command (line 280).** Step 3.3 says "via the pre-commit hook … or the project's
  equivalent markdownlint command discovered from `.pre-commit-config.yaml`." This is
  slightly less deterministic than the fully-pinned 3.1/3.2/3.4 commands, but the fallback
  ("discover from `.pre-commit-config.yaml`") plus the explicit 9-file list and named rule
  codes keep it actionable. Advisory only. [INFERRED] severity MINOR.

- **[MINOR] F3 — Step 2.1 is very large (single hub-ref item, ~1 screen of nested
  enumeration, line 184).** It is within the one-file/one-item granularity rule (it
  creates exactly one file), and the spec sections it must reproduce genuinely are that
  many, so the size is inherent to the deliverable rather than a batching defect. The
  per-`##`-section ordering is fully enumerated, so it remains executable. Noted as the
  single heaviest item; no split required. severity MINOR.

## Convention cross-checks that PASSED (no finding)

- `.claude/` staging discipline: enforced at Step 3.4 + repeated in every fix item. PASS.
- src-only edit surface: every Phase 2 path under `src/superclaude/`. PASS.
- New-ref no-frontmatter + single-H1 + tagged fences: mandated in Phase 2 header and per
  item. PASS.
- Column model (no MD056 drift) for the SKILL.md Output Contract table: verified the live
  table is 3-column; the fold-into-Description instruction is correct. PASS.
- Report-template four-backtick fence integrity: verified the fence opens at SKILL refs
  `report-template.md` line 7 and closes at line 203, with `## Follow-up tasks`/`## Grounding
  Gaps` inside and `## Behavior-is-documented rule` outside — Steps 2.12 (inside) and 2.13
  (after-EOF, outside) place the new content on the correct side of the fence. PASS.
- 5 new-ref path collision check: verified all 5 filenames are ABSENT in the live refs/
  dir (no collision); Step 1.4 also requires confirming "ABSENT — safe to create." PASS.

---

## Calibrated self-confidence: 0.90

Rationale: I read both inputs in full and re-verified every load-bearing structural claim
(3-column Output Contract table, the Wave 4/5 `---` seam, the four-backtick fence
boundaries, the calibration-gate precedent, the Wave 6 `status: success` precondition, the
remediation-handoff anchors, and the absence of the 5 new ref paths) directly against live
source within this turn. The grade is bounded below 1.0 because (a) I assessed
best-practice/actionability form, not deep spec-fidelity arithmetic (Reviewer 1/2's lens),
so a content-level spec divergence the tasklist faithfully transcribes would not surface
here; and (b) I did not re-read the research files R-001..R-007 the items cite, trusting
the tasklist's own characterization of them.
