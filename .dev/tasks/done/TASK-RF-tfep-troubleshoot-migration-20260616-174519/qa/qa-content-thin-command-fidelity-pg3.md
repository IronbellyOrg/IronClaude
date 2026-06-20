# QA Report — Thin-Command-Fidelity (doc-qualitative lens)

**Topic:** TFEP troubleshoot migration — Phase 3 (`--context`/`--caller` wiring)
**Date:** 2026-06-16
**Phase:** doc-qualitative (thin-command-fidelity lens, NFR-5)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Adversarial framing:** "Assume the command leaked at least 3 pieces of skill-side logic. Find them."

---

## Overall Verdict: PASS

The Phase 3 edits to `src/superclaude/commands/troubleshoot.md` keep the command a thin
advertiser per NFR-5. Despite an explicit adversarial hunt for ≥3 leaks of skill-side
logic, **zero leaks were found**. Every parse/resolve/emit responsibility for `--context`
and `--caller` lives in the skill (`sc-troubleshoot-protocol/SKILL.md`); the command only
advertises the flags and surfaces a return value.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Options rows DESCRIBE the flags (advertise), do not implement parsing | PASS | `troubleshoot.md:59-60`. `--context` row reads "Path to a caller-supplied context file … **Ingested in Wave 0**; recorded in the audit-log header and **echoed in the Wave 5 return**." `--caller` row reads "Name of the invoking pipeline/command … **When set, Wave 5 emits** a `return-contract.yaml` adapter …". Both are noun-phrase descriptions that *attribute the action to a wave of the skill* (Wave 0 / Wave 5). No parse code, no file-read, no path-resolution, no emission template in either row. |
| 2 | "On skill return, surface:" clause only SURFACES the return path, does not emit | PASS | `troubleshoot.md:69`. Clause appended: "… and (if caller=task-unified) **the emitted return-contract.yaml path**." The word "emitted" is past-participle: the skill already produced it; the command surfaces its path. Mirrors the pre-existing surface convention `(if pipeline_hardening_applicable) the Pipeline Hardening Closure verdict + evidence-card paths` (same line). No write/compose/serialize verb. |
| 3 | Parse-step enumeration only NAMES the flags; resolution/emission live in skill | PASS | `troubleshoot.md:66`. Behavioral Summary step 1: "**Parse arguments** → resolve `--type` (auto-detect if absent), `--scope`, `--depth`, `--context`, `--caller`, etc." This is the command-file's standing self-description of "the command file performs only:" (line 64) — it merely lists `--context`/`--caller` among the tokens recognized, identical treatment to `--scope`/`--depth`. The actual resolution (file read, abs-path, STOP-on-unreadable, audit-header record, Wave 5 emit-marking) is in skill Wave 0 step 6. |
| 4 | No business logic (file reading, path resolution, contract emission) leaked into command | PASS | Full-file scan of `troubleshoot.md`. No file-read instruction, no `abs-path` resolution, no `STOP if … unreadable`, no `return-contract.yaml` field schema, no audit-header key list, no emission template anywhere in the command. The only mentions of `return-contract.yaml` are the two advertise/surface references (rows 59-60, line 69). |
| 5 | Skill genuinely owns the logic the command attributes to it (no phantom delegation) | PASS | `SKILL.md:143` (Wave 0 step 6): "If `--caller` is set, record it in the audit header `caller:` field … If `--context <path>` is set, **read it** … and **resolve it to an absolute path**; **STOP if the path is unreadable**. When `caller=task-unified`, **mark Wave 5 to emit** `return-contract.yaml`." `SKILL.md:115` (Wave 0 step 1) lists `--context`, `--caller` in the parse set. `SKILL.md:448-462` (Wave 5 step 4) emits the audit footer including `caller:` and `return_contract_path:`. Delegation targets are real, not advertised vapor. |
| 6 | Behavioral Summary step 2 ("Validate environment") not over-scoped by the new flags | PASS | `troubleshoot.md:67`. Step 2 still reads "at least one of MCPs is available (or `--no-mcp` is set); output dir is writable." It was NOT amended to add `--context` readability validation — correctly, because the `STOP if … unreadable` check lives in skill Wave 0 step 6 / STOP-conditions (`SKILL.md:143,147`). No validation logic crept into the command. |
| 7 | Edit blast radius is exactly the 4 advertised touchpoints (no incidental leakage) | PASS | `git diff master -- troubleshoot.md` shows exactly 4 hunks: argument-hint (line 8), two Options rows (59-60), parse enumeration (66), surface clause (69). No edits to Boundaries, CRITICAL BOUNDARIES, Activation, MCP Integration, or Examples. Scope-disciplined; nothing leaked outside the advertise/surface surface. |
| 8 | argument-hint advertises tokens only (no semantics embedded) | PASS | `troubleshoot.md:8`. Appended ` [--context <path>] [--caller <name>]` in the same `[--flag <arg>]` bracket style as siblings. Pure token advertisement in frontmatter — structurally incapable of holding logic. |

---

## Summary
- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Leaks found (adversarial target ≥3): **0**

## Adversarial Hunt — Where Logic COULD Have Leaked (and didn't)

I specifically probed the five most common thin-command leak patterns. None present:

1. **Inline file-read of `--context`** — would appear as "read the context file / load the brief"
   in the command. ABSENT. The read is at `SKILL.md:143` only. The Options row says "Ingested in
   Wave 0" (attribution), not "read the file here".
2. **Path-resolution / unreadable-STOP for `--context`** — would appear as a STOP condition or
   abs-path step in the command's "Validate environment" (step 2). ABSENT. Step 2 (`:67`) was left
   untouched; the STOP lives at `SKILL.md:143,147`.
3. **return-contract.yaml field schema / emission template** — would appear as a YAML block or
   field list in the command. ABSENT. The footer schema (`caller:`, `return_contract_path:`) is at
   `SKILL.md:448-462` exclusively. The command only names the file as a surfaced *path*.
4. **`caller=task-unified` branching logic** — would appear as command-side conditional behavior
   ("if caller is task-unified, do X"). The command's only `caller=task-unified` reference (`:69`)
   is a *display condition* on what to surface, not an emission trigger. The emit-trigger
   conditional is at `SKILL.md:143` ("When `caller=task-unified`, mark Wave 5 to emit"). Correct
   split.
5. **Audit-header key authoring** — would appear as the command specifying the `caller:` header
   field. ABSENT. The Options row (`:60`) says "the audit header records `caller:`" as a
   description of skill behavior; the actual header write is `SKILL.md:143` + the footer template
   at `SKILL.md:460`.

The linguistic tell that confirms fidelity: every command-side mention of an action is
**wave-attributed** ("Ingested in Wave 0", "Wave 5 emits", "echoed in the Wave 5 return") or
**past-participial** ("the emitted return-contract.yaml path"). Advertisers describe; they do not
act. This command describes.

## Issues Found
None.

## Actions Taken
None (fix_authorization: false; verdict is PASS with no issues).

## Self-Audit (mandatory)
1. **How many factual claims independently verified against source?** 8 checklist rows + 5
   adversarial-pattern probes, each tied to a specific `file:line`. The central claim — "the skill,
   not the command, owns parse/resolve/emit" — was verified by reading the actual skill at three
   distinct sites (Wave 0 parse list `SKILL.md:115`, Wave 0 resolve/record `SKILL.md:143`, Wave 5
   emit footer `SKILL.md:448-462`), not inferred from the command's self-description.
2. **What specific files did I read?** `src/superclaude/commands/troubleshoot.md` (full, 205 lines);
   `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Wave 0 lines 109-147, Wave 5 lines
   421-490); `git diff master` on the command file; the task file's Phase 3 item specs (R-002
   §A1/§A5/§A6) and `research/02-troubleshoot-surface.md` for the NFR-5 convention anchor (command
   line 169).
3. **If 0 issues, why trust the check was thorough?** Because the verdict rests on cross-file
   evidence, not a single read. A thin-command violation would necessarily manifest as either
   (a) imperative action verbs in the command (read/resolve/emit/write) — I grepped the diff and
   full file and found only descriptive/past-participial mentions; or (b) the skill *lacking* the
   logic the command attributes to it (phantom delegation) — I confirmed the skill genuinely
   contains it at `SKILL.md:115/143/448-462`. Both failure modes were actively tested and both came
   back clean. The adversarial ≥3-leak prior was discharged by enumerating the 5 likeliest leak
   sites and showing each is in the skill.
4. **Web research?** None performed; this review is entirely local-file-bound (command + skill +
   task specs). Tavily not required.

## Confidence
Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 3 (troubleshoot.md full; SKILL.md Wave 0; SKILL.md Wave 5) | Grep/Bash-grep: 3 (diff vs master; NFR-5 spec refs; skill context/caller grep) | Glob: 0

## Recommendations
- None blocking. The Phase 3 edits are a textbook thin-command advertise/surface change. Phase 3
  gate may proceed.
- Forward note (NOT a Phase 3 defect): the argument-hint at `troubleshoot.md:8` remains missing the
  pre-existing `--no-diagnosability-audit` / `--diagnosability-handoff` /
  `--reset-diagnosability-rounds` tokens that DO exist in the skill parse list (`SKILL.md:115`).
  This predates Phase 3 and was explicitly declared out-of-scope by the task item (R-002 §A1). Flagged
  for visibility only — it is `[OUT-OF-SCOPE]` for this gate and unrelated to thin-command fidelity.

## QA Complete
```
