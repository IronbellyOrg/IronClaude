# Research: sc:spec-panel Full Audit

**Investigation type:** Code Tracer + Doc Analyst
**Scope:** .claude/commands/sc/spec-panel.md, .claude/skills/sc-spec-panel*/
**Status:** Complete
**Date:** 2026-03-24

---

## Step 1: Skill Directory Check

**Result:** No `.claude/skills/sc-spec-panel*/` directory exists.

The command has **no companion skill package**. It is a standalone command file with no separate `SKILL.md`, `rules/`, `templates/`, or `refs/` subdirectory. All logic is embedded in the single command file.

---

## Step 2: Command File — Full Read

**File:** `/Users/cmerritt/GFxAI/IronClaude/.claude/commands/sc/spec-panel.md`
**Lines:** 624
**File read in full — no truncation.**

### YAML Frontmatter
```yaml
name: spec-panel
description: "Multi-expert specification review and improvement using renowned specification and software engineering experts"
category: analysis
complexity: enhanced
mcp-servers: [sequential, context7]
personas: [technical-writer, system-architect, quality-engineer]
```

---

## Step 3: Targeted Findings

### 3.1 — Template File References

**Does it mention `release-spec-template.md`, `tdd_template.md`, or any template file by path?**

NO. There are zero references to any template file by path anywhere in the command. The file does not import, reference, or mention `release-spec-template.md`, `tdd_template.md`, `prd_template.md`, or any other external template file. The command is self-contained.

---

### 3.2 — YAML Frontmatter Fields in Output

**Does it read or write `spec_type`, `complexity_score`, `complexity_class`, `quality_scores`?**

NO. None of those field names appear in the command file. The command produces its own quality metrics with different names:
- `overall_score` (e.g., `7.2/10`)
- `requirements_quality` (e.g., `8.1/10`)
- `architecture_clarity` (e.g., `6.8/10`)
- `testability_score` (e.g., `7.5/10`)

These are part of the `quality_assessment` block in its Standard format output. They are output artifacts of the review, not YAML frontmatter fields written back to a spec file.

Named quality metrics in the "Quality Assurance Features" section:
- **Clarity Score** (0-10)
- **Completeness Score** (0-10)
- **Testability Score** (0-10)
- **Consistency Score** (0-10)

None map to `complexity_score` or `complexity_class`.

---

### 3.3 — Sentinel System Knowledge

**Does it know about the `{{SC_PLACEHOLDER:*}}` sentinel system?**

NO. The word "sentinel" appears 5 times in the file, but every occurrence refers to the adversarial testing concept of "sentinel values" (magic numbers or reserved constants in specifications that could collide with legitimate data). The FR-2.3 "Sentinel Collision Attack" is about attacking specification logic, not the SuperClaude template placeholder system. There is no awareness of `{{SC_PLACEHOLDER:*}}` or any related template token.

---

### 3.4 — Output Format

**What is the output format?**

The command produces a **review document**, not a spec. Three format options exist:

- **`--format standard`**: YAML-structured review containing `specification_review`, `quality_assessment`, `critical_issues`, `expert_consensus`, `improvement_roadmap`, and `adversarial_analysis` blocks.
- **`--format structured`**: Token-efficient format using SuperClaude symbol system.
- **`--format detailed`**: Full expert commentary, examples, and implementation guidance.

When `--focus correctness` is active, mandatory artifact outputs are also produced:
- **State Variable Registry** (table)
- **Guard Condition Boundary Table** (7-column table)
- **Pipeline Quantity Flow Diagram** (when pipelines are present)

All are structured markdown, explicitly described as "machine-parseable" per NFR-5.

---

### 3.5 — Can It CREATE a New Spec?

**Can it CREATE a new spec from raw instructions, or does it only REVIEW/IMPROVE an existing spec?**

It primarily REVIEWS and IMPROVES existing specs. The `Boundaries > Will Not` section is explicit:

> "Generate specifications from scratch without existing content or context"

Usage syntax requires `[specification_content|@file]` — the spec content is a required input. The command does not offer a creation mode.

The `Behavioral Flow` step 6 is labeled "**Improve**: Create enhanced specification incorporating expert feedback and best practices" — but "Improve" here means modifying/enhancing an existing spec, not originating one.

---

### 3.6 — What the "Improve" Step Produces

**What does the Improve step produce — what format?**

The command describes "Improve" (step 6 of Behavioral Flow) as producing an "enhanced specification incorporating expert feedback." However, the command's `Output` section (line 618-621) says:

> **Output**: Expert review document containing:
> - Multi-expert analysis (11 simulated experts)
> - Specific, actionable recommendations
> - Consensus points and disagreements
> - Priority-ranked improvements

The output is described as a **review document**, not a revised spec file. The "Improve" step likely means the review document contains the improved spec content inline, rather than writing a new file. The `Tool Coordination` section lists `Write` as a tool for "Improved specification generation and report creation" — so the panel _can_ write an improved spec, but the primary output is the review document.

---

### 3.7 — Integration Wiring to sc:roadmap or sc:tasklist

**Is there any integration wiring to sc:roadmap or sc:tasklist?**

**Partial — sc:roadmap yes; sc:tasklist NO.**

The "Downstream Integration Wiring" table (lines 484-494) shows:

| Source | Target | Integration Point |
|--------|--------|-------------------|
| SP-3 (Guard Condition Boundary Table) | `sc:adversarial` AD-1 | Invariant probe input |
| SP-2 (Whittaker Attack Findings) | `sc:adversarial` AD-2 | Assumption challenge input |
| SP-1 (Correctness Focus findings) | `sc:adversarial` AD-5 | Edge case input |
| SP-4 (Quantity Flow Diagram) | **`sc:roadmap` RM-3** | Risk input — dimensional mismatches inform risk-weighted roadmap prioritization |
| SP-2 (Whittaker Assumptions) | **`sc:roadmap` RM-2** | Assumption input — identified assumptions feed roadmap assumption tracking |

Integration to `sc:roadmap` exists at two points (RM-2 and RM-3). Integration to `sc:tasklist` is **not mentioned anywhere** in the file.

The `Integration Patterns` section also documents a workflow pairing with `/sc:code-to-spec` but not with `sc:roadmap` as a direct next step for the user (the "Next Step" suggestion is `/sc:design` or `/sc:implement`).

---

**Status:** Complete

---

## Summary

`sc:spec-panel` is a pure **specification review and improvement** command. It accepts an existing specification (file or inline text) and routes it through a panel of 11 simulated domain experts in a fixed review sequence, producing a structured review document with quality scores, prioritized findings, and adversarial attack analysis. It has no companion skill directory, no knowledge of the `{{SC_PLACEHOLDER:*}}` sentinel system, and no awareness of the project's `release-spec-template.md` or `tdd_template.md` files. The command does not create specs from scratch — it explicitly states this in its Boundaries section. Its machine-parseable output is designed to feed downstream into `sc:adversarial` (for invariant probing) and `sc:roadmap` (for risk and assumption tracking), but there is no wiring to `sc:tasklist`.

---

## Gaps and Questions

1. [Important] **"Improve" output ambiguity**: Step 6 of Behavioral Flow says "Create enhanced specification" but the Output section says the result is a "review document." It is unclear whether the panel actually writes a new spec file or embeds the improved content inside the review document. The `Write` tool is listed but no explicit artifact path or file naming convention is defined.
2. [Minor] **No template awareness**: The command is entirely self-contained. If the project uses `release-spec-template.md` or `tdd_template.md` as structured inputs, `sc:spec-panel` will treat them as opaque text with no special handling of frontmatter or placeholders.
3. [Important] **quality_scores field gap**: The command produces quality metrics under its own schema (`overall_score`, `requirements_quality`, etc.) but does not produce or consume the `quality_scores` YAML frontmatter field used elsewhere in the pipeline. No bridge exists between the two schemas.
4. [Minor] **sc:tasklist not wired**: Despite the command producing prioritized findings and improvement roadmaps, there is no integration point to `sc:tasklist` to automatically generate tasks from findings.
5. [Minor] **NFR-8 false positive rate**: The spec mentions "Target false positive rate <30% per NFR-8; measurement deferred to Gate B (T05.02)" for the correctness-focus auto-suggestion. NFR-8 and Gate B are referenced but not defined in this file — they presumably live in a separate spec or roadmap document.

---

## Key Takeaways

- **Review-only, not creation**: The command reviews and improves existing specs. It explicitly refuses to generate specs from scratch.
- **No skill package**: No `.claude/skills/sc-spec-panel*/` directory exists; the entire command is a single 624-line `.md` file.
- **No template file awareness**: Zero references to `release-spec-template.md`, `tdd_template.md`, or any external template path.
- **No sentinel system knowledge**: The `{{SC_PLACEHOLDER:*}}` system is unknown to this command. "Sentinel" in the file refers to adversarial testing concepts only.
- **No YAML frontmatter field alignment**: Does not read or write `spec_type`, `complexity_score`, `complexity_class`, or `quality_scores`.
- **11-expert fixed panel**: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower — always in this order.
- **Three output modes**: `--mode discussion | critique | socratic` control how experts interact.
- **Mandatory artifacts under correctness focus**: State Variable Registry, Guard Condition Boundary Table, and Quantity Flow Diagram are hard gates that block synthesis output if incomplete.
- **Partial downstream wiring**: Feeds `sc:adversarial` (AD-1, AD-2, AD-5) and `sc:roadmap` (RM-2, RM-3). No wiring to `sc:tasklist`.
- **Primary output is a review document**: Not a revised spec file, though the panel can write an improved spec as a secondary artifact using the `Write` tool.
