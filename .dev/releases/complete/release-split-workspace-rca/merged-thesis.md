# Merged Thesis & Solution Proposal — `sc-release-split-protocol-workspace` Misplacement RCA

**Date:** 2026-05-08
**Inputs:** rca-1-skill-spec.md, rca-2-eval-harness.md, rca-3-naming-convention.md
**Method:** Structured adversarial debate with custom 65/35 (root-cause / solution) weighting, layered-fix synthesis.

---

## TL;DR

> **Proximate cause:** Anthropic's vendored `skill-creator` plugin has a hardcoded SKILL.md instruction (line 167) — *"Put results in `<skill-name>-workspace/` as a sibling to the skill directory."* When Claude executed this plugin's procedure for `sc-release-split-protocol`, the mechanically-required sibling location was `.claude/skills/sc-release-split-protocol-workspace/`. The placement was inevitable given the plugin's instruction and the skill's location — there is no flag, env var, or config-file override in the upstream plugin. (RCA #2, confidence 0.92.)
>
> **Systemic cause:** The repo had no governance to catch the misplacement before commit. `make verify-sync` *would* have flagged it but isn't run in CI, and its error message ("not distributable!") would have led an author toward the wrong fix (copy to `src/`) rather than the right one (move to `.dev/`). Project CLAUDE.md's pointers to `PLANNING.md`/`TASK.md`/`KNOWLEDGE.md` are broken, and `.dev/` has no README. (RCA #3, confidence 0.7.)
>
> **Verdict:** RCA #2 is the **why-it-happened**; RCA #3 is the **why-it-stayed**. Both must be fixed. RCA #1's defensive guards are belt-and-suspenders for a different (unlikely) entry path and are kept as tertiary defense.

---

## Per-RCA Final Weighted Scores (65% root cause / 35% solution)

| RCA | Root Cause Score (×0.65) | Solution Score (×0.35) | **Total** | Verdict |
|---|---|---|---|---|
| **RCA #1 — Skill-spec / output-path** | 0.367 → **0.238** | 0.450 → **0.158** | **0.396** | Components: dead-end on cause; defensive guards retained as tertiary |
| **RCA #2 — Eval harness / plugin convention** | 0.933 → **0.607** | 0.750 → **0.263** | **0.870** | **BASE** — proximate cause + primary occurrence-prevention fix |
| **RCA #3 — Governance / naming** | 0.717 → **0.466** | 0.817 → **0.286** | **0.752** | Systemic cause + primary persistence-prevention fix |

**Margin:** RCA #2 leads RCA #3 by 0.118 (no tiebreaker needed; >0.05 threshold).
**Edge-case-coverage floor:** All three RCAs declared limitations and gaps; all clear the 1/5 floor.

### Score breakdown — RCA #1

| Axis | Score | Reasoning |
|---|---|---|
| RC.likelihood | 0.10 | Author self-declared 0.95 confidence the skill spec is **NOT** the cause |
| RC.evidence | 0.90 | Exhaustive grep across 600 lines + 2 sibling skills; verifiable citations |
| RC.explanatory | 0.10 | Explicitly cannot explain placement; admits skill is downstream of misnaming |
| Sol.effectiveness | 0.30 | Guard fires only if skill is invoked with bad `--output`; RCA #2 proves the skill wasn't the entry point |
| Sol.cost | 0.85 | Cheap; ~3 small edits |
| Sol.alignment | 0.20 | Solution targets a non-cause; structurally weak fit |

### Score breakdown — RCA #2

| Axis | Score | Reasoning |
|---|---|---|
| RC.likelihood | 0.95 | Smoking gun: skill-creator SKILL.md L167; mechanical inevitability provable from one quoted line |
| RC.evidence | 0.95 | Quoted L167/180/185/188/225-229; every artifact filename matches plugin spec verbatim; argparse audit of upstream |
| RC.explanatory | 0.90 | Explains placement completely; honestly notes it doesn't explain *why this skill* used skill-creator |
| Sol.effectiveness | 0.80 | PreToolUse hook is the only enforcement that doesn't rely on Claude obedience |
| Sol.cost | 0.55 | Hook needs careful path-matching to avoid breaking legitimate `.claude/skills/` writes |
| Sol.alignment | 0.90 | Directly addresses the upstream plugin's behavior; redirect lands artifacts in `.dev/` |

### Score breakdown — RCA #3

| Axis | Score | Reasoning |
|---|---|---|
| RC.likelihood | 0.55 | Governance gap is real but author self-flags 0.7; not the *occurrence* trigger but is the *survival* trigger |
| RC.evidence | 0.95 | Verified missing files, exact Makefile lines, exhaustive `*-workspace` inventory, broken CLAUDE.md pointers |
| RC.explanatory | 0.65 | Explains why nothing caught it; doesn't explain initial occurrence (RCA #2's territory) |
| Sol.effectiveness | 0.85 | 5-pronged fix (R1–R5) addresses CI gap, error-message redirect, gitignore gap, CLAUDE.md corrosion |
| Sol.cost | 0.65 | Five separate changes across Makefile, CI workflows, docs, meta-docs |
| Sol.alignment | 0.95 | Every R-change traces to a specific F-finding; tight cause→fix mapping |

---

## Debate Outcomes — What Survived, What Was Superseded

### Survived

- **RCA #2's smoking gun (skill-creator SKILL.md L167).** No alternative explanation matches the artifact filenames or the mechanical sibling-path inevitability. Adopted as the proximate-cause statement of the merged thesis.
- **RCA #2's Option D (PreToolUse hook) + Option C (CLAUDE.md addendum) pairing.** The combination of *enforced redirect* (D) plus *documented rule* (C) closes the occurrence vector without depending on either alone.
- **RCA #3's R1–R5 governance fixes.** Each addresses a verifiable governance gap (.dev/ has no README; CI doesn't run verify-sync; the error message misdirects; `*-workspace` suffix has no blocklist; CLAUDE.md pointers are broken). Adopted wholesale; these prevent recurrence-by-other-means and harden the safety net.
- **RCA #1's defensive output-path guard at the skill level.** Kept as tertiary defense in the unlikely event a future workflow routes a `.claude/skills/...` path through `sc-release-split` directly.
- **RCA #2's Option B (`make eval-skill SKILL=<name>` convenience target).** Not a fix to the bug, but a usability nudge that pre-creates `.dev/eval-workspaces/<name>/` and prints the path — reducing the chance an author types the wrong path.

### Superseded / Rejected

- **RCA #1 as "the cause" of the misplacement.** Author self-rejected at 0.95 confidence. The skill spec is silent on `.claude/skills/`, `-workspace`, and sibling conventions; the breadcrumbs in the workspace artifacts show the skill *received* the bad path, it didn't *generate* it.
- **RCA #3 framed as "the dominant cause."** RCA #3 explains *survival to commit*, not *occurrence*. Demoted to systemic-cause role, paired with RCA #2's proximate-cause role.
- **Standalone interpretations.** No single-RCA fix is sufficient. RCA #2 alone misses persistence/commit governance. RCA #3 alone misses the per-occurrence redirect. RCA #1 alone fixes nothing demonstrable. The merged proposal is layered.

### Unaddressed / Open

From Round 2.5 invariant probe (`adversarial/invariant-probe.md`):
- **INV-002 (HIGH):** The plan's effectiveness depends on R3 (CI wiring) actually landing. Until the GitHub workflow change is merged, `verify-sync` remains opt-in. Status: **UNADDRESSED in this thesis** — listed as the highest-priority next action below.
- **INV-001 (MEDIUM):** Plan assumes the `skill-creator` plugin remains vendored at the cited path. If the plugin is updated upstream or moved (e.g., npm-style global install), the L167 reference may go stale. Status: ADDRESSED via R5 ("CLAUDE.md addendum cites the plugin's behavior, not the file path").
- **A-001 (UNSTATED ASSUMPTION):** All three RCAs assume `.dev/eval-workspaces/<skill-name>/` is correct, yet RCA #3 noted the only prior art (`.dev/releases/complete/v2.15-cli-portify/sc-cli-portify-workspace`) used a release-relative location. The merged thesis adopts `.dev/eval-workspaces/` as the new convention but flags this as a documentation decision (R1).

---

## Final Solution — Layered Defense

**Three layers, each closes a different vector. Apply all three.**

### Layer 1 — Stop the occurrence (RCA #2)

| Action | File / Location | Owner | Effort |
|---|---|---|---|
| **L1.1** Add PreToolUse hook in `.claude/settings.json` rejecting `Write`/`Edit` to `.claude/skills/*-workspace/**`. The hook rewrites the path to `.dev/eval-workspaces/<skill-name>/<remainder>` and emits an explanatory error pointing at `.dev/eval-workspaces/`. | `.claude/settings.json` | Project | S |
| **L1.2** CLAUDE.md addendum (project-level) explicitly overriding the skill-creator plugin's "sibling to the skill directory" convention. Names the override and the destination. | `/config/workspace/IronClaude/CLAUDE.md` | Project | S |
| **L1.3** (Convenience) Add `make eval-skill SKILL=<name>` target that creates `.dev/eval-workspaces/<name>/` and prints the absolute path for use as the workspace root. | `Makefile` | Project | S |

### Layer 2 — Stop the persistence (RCA #3)

| Action | File / Location | Owner | Effort |
|---|---|---|---|
| **L2.1** (R2) Replace `make verify-sync`'s misleading `"MISSING in src/superclaude/skills/: <name> (not distributable!)"` message with a context-aware variant. When the missing entry has no `SKILL.md`, emit `"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."` | `Makefile` | Project | S |
| **L2.2** (R3) Wire `make verify-sync` and `make lint-architecture` into `.github/workflows/quick-check.yml`. PRs fail on drift before merge. | `.github/workflows/quick-check.yml` | Project | S |
| **L2.3** (R4) Add a `*-workspace` blocklist pattern to either `verify-sync` or `lint-architecture` with explicit message: *"Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`."* | `Makefile` | Project | S |
| **L2.4** (R1) Add `.dev/README.md` documenting all 11 subdirectories, especially the `eval-workspaces/` rule: *"Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`."* | `.dev/README.md` (new) | Project | M |
| **L2.5** (R5) Repair the broken pointers in `/config/workspace/IronClaude/CLAUDE.md` to `PLANNING.md`/`TASK.md`/`KNOWLEDGE.md` — either restore the files at the documented paths, or update the references to the actual locations. | `CLAUDE.md` (project) | Project | S |
| **L2.6** Add `.gitignore` entries: `.claude/skills/*-workspace/` (prevents re-occurrence under same skill directly) and document `.dev/eval-workspaces/<name>/` as **optional** (some workspaces may legitimately be tracked, e.g., reproducible eval inputs; let the author decide per workspace via explicit `git add`). | `.gitignore` | Project | S |

### Layer 3 — Defense in depth (RCA #1)

| Action | File / Location | Owner | Effort |
|---|---|---|---|
| **L3.1** Add output-path policy guard in `sc-release-split-protocol/SKILL.md` Prerequisites step 2a: refuse `--output` paths under `.claude/skills/`, `.claude/agents/`, `.claude/commands/`. Document the policy in `release-split.md` Options table. | `src/superclaude/skills/sc-release-split-protocol/SKILL.md`, `src/superclaude/commands/release-split.md` | Project | S |
| **L3.2** (Optional) Apply the same guard to `sc-adversarial-protocol` and `sc-cleanup-audit-protocol` for consistency across skills that produce outputs. | Two SKILL.md files | Project | M |

---

## Acceptance Criteria for the Merged Solution

A future skill author, in good faith, attempting to run `skill-creator` against any IronClaude skill:

1. **L1 fires first**: Claude reads project CLAUDE.md, sees the override (L1.2), and writes to `.dev/eval-workspaces/<name>/` directly. If Claude ignores the override, the PreToolUse hook (L1.1) blocks the write to `.claude/skills/*-workspace/**` and emits a redirect-pointing error.
2. **L2 fires if L1 is bypassed (e.g., fresh clone without hooks installed)**: a directory under `.claude/skills/<X>-workspace/` is created without a `SKILL.md`. `make verify-sync` (L2.1) flags it with the correct error message, and CI (L2.2) blocks the PR.
3. **L3 fires if a different code path tries to route a `.claude/skills/...` value through `sc-release-split-protocol --output`**: the skill itself refuses (L3.1) before writing.
4. **Documentation is internally consistent**: project CLAUDE.md's references resolve (L2.5), `.dev/README.md` exists and names the rule (L2.4), and the convention is therefore *findable* by a new contributor without tribal knowledge.
5. **No regression in the relocated workspace**: `/config/workspace/IronClaude/.dev/eval-workspaces/sc-release-split-protocol/` continues to function with `aggregate_benchmark.py` and `generate_review.py` (both accept positional paths).

---

## Risk Register (Layered-Fix-Specific)

| ID | Risk | Layer | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| R-01 | PreToolUse hook (L1.1) breaks legitimate writes inside `.claude/skills/<skill>/` (i.e., the actual skill files, not workspaces). | L1 | Medium | High (dev friction) | Pattern must match `*-workspace/**` precisely, not `.claude/skills/**`. Test with positive (skill file edit) and negative (workspace write) cases. |
| R-02 | CI wiring (L2.2) lengthens PR time noticeably. | L2 | Low | Low | `make verify-sync` runs in seconds; concurrent with existing checks. |
| R-03 | New `.dev/eval-workspaces/` convention diverges from the v2.15 prior art (`.dev/releases/complete/v2.15-cli-portify/sc-cli-portify-workspace`). | L2 | Resolved | Medium | L2.4 (.dev/README.md) explicitly documents the new rule. Backwards compatibility: prior workspace remains where it is; rule applies forward only. |
| R-04 | The skill-creator plugin updates upstream and the L167 reference goes stale. | L1 | Low | Low | L1.2 cites *behavior* ("sibling-workspace convention") not *file path*; remains accurate. |
| R-05 | A future skill *should* legitimately have a workspace inside `.claude/` for some reason (none currently identified). | L1, L2 | Very Low | Low | Hook + Makefile checks emit override-able errors; future reviewer can suppress if intentional. |

---

## Required Next Action — INV-002 Resolution

The Round 2.5 fault-finder flagged one HIGH-severity unaddressed invariant: **the layered fix is only effective once L2.2 (CI wiring) is actually merged.** Until that change lands, `verify-sync` remains a developer's local opt-in and provides no PR-blocking guarantee.

**Recommendation:** L2.2 ships **first**, ahead of all other layers. The PR can be a single-line addition to `quick-check.yml`. Even before any other fix lands, this turns the existing (correct) detection logic into an enforced gate.

---

## Provenance

| Section | Source |
|---|---|
| TL;DR | Synthesis of RCA #2 (proximate) + RCA #3 (systemic) |
| Score table | New computation per user-specified 65/35 weighting |
| Survived/Superseded | Adversarial debate transcript (`adversarial/debate-transcript.md`) |
| Layer 1 | RCA #2 §"Refactor proposal" Options C+D+B |
| Layer 2 | RCA #3 §"Refactor proposal" R1–R5 (full adoption) |
| Layer 3 | RCA #1 §"Refactor proposal" Edits 1–2 (defensive subset) |
| Risk Register | New synthesis; R-01 derived from RCA #2 caveat about hook precision |
| Required Next Action | RCA #3 R3 + Round 2.5 INV-002 |
