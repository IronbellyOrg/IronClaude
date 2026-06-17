# QA Report — Content Crossref-Chain Lens (Phase 2, TFEP forensic→troubleshoot migration)

**Topic:** TFEP backend rename (forensic → troubleshoot) cross-reference chain integrity
**Date:** 2026-06-16
**Phase:** doc-qualitative (crossref-chain content lens)
**Lens:** crossref-chain (internal Step/heading/declaration reference resolution)
**Fix authorization:** false (REPORT ONLY)
**Target:** `src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5 (lines 133–263)

---

## Overall Verdict: FAIL

Five dangling references to the removed `/sc:forensic` / "forensic" surface survive the
rename. The renamed headings ("Invoke diagnostic escalation", "Consume diagnostic results")
and the new `**Diagnostic backend:**` declaration are internally inconsistent with the
step bodies they govern: the headings say "diagnostic", the bodies still say "forensic".

---

## Chain Trace (each link verified against the actual file)

| Link | Anchor (file:line) | Resolves? | Evidence |
|------|--------------------|-----------|----------|
| TFEP-trigger → Escalation Trigger Detection | SKILL.md:166 | PASS | Heading present; gradient line correctly reworded to "for diagnostic-backend escalation" (174). Research notes flagged the old "future forensic integration" wording — that token WAS fixed. |
| Step 1 Halt and freeze | SKILL.md:187 | PASS | "STOP/FREEZE"; targeted by sub-step 15 "return to Step 2" and the step-number machinery. |
| Step 2 Construct failure context | SKILL.md:192 | PASS | Writes `context.yaml` (205); "return to Step 2" (237) resolves. |
| Step 3 Invoke diagnostic escalation | SKILL.md:207 (heading) | PARTIAL | Heading correctly renamed. Targeted by "return to Step 3" (223) — resolves. BUT sub-step 6 body (214) still invokes `/sc:forensic` — see F1. |
| Step 4 Consume diagnostic results | SKILL.md:217 (heading) | PARTIAL | Heading correctly renamed. "Proceed to Step 5" / "return to Step 3" targets resolve. BUT sub-step 8 body (218) still reads the "**forensic** return contract" — see F2. |
| Step 5 Tasklist insertion | SKILL.md:226 | PASS | Targeted by Step 4 "Proceed to Step 5 (tasklist insertion)" (222). |
| Step 6 Resume | SKILL.md:233 | PASS | Final flow; "return to Step 2" (237) resolves. |
| Numbered sub-steps 1–15 | SKILL.md:189–237 | PASS | Contiguous 1→15, no gaps or duplicates, flow correctly across all renamed headings. |
| `**Diagnostic backend:**` declaration | SKILL.md:137 | FAIL | The declaration's own self-reference is broken — see F5. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| F1 | CRITICAL | SKILL.md:214 (Step 3, sub-step 6) | Invocation still `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick`. `/sc:forensic` no longer exists — there is no `src/superclaude/commands/forensic.md`; only `commands/troubleshoot.md` exists. This is a dangling reference to a removed command, and it directly contradicts the renamed heading "Invoke diagnostic escalation" two lines above. | Rename `/sc:forensic` → `/sc:troubleshoot`. (Flag-surface correctness — `--tier`/`--intent`/`--caller`/`--context` vs the actual troubleshoot flag set — is out of scope for this crossref lens; route to the flag-surface lens. The crossref defect is the dead command name.) |
| F2 | IMPORTANT | SKILL.md:218 (Step 4, sub-step 8) | "Read the **forensic** return contract from `{output_dir}/return-contract.yaml`." Dangling "forensic" adjective; contradicts renamed heading "Consume diagnostic results" one line above. | "Read the diagnostic return contract from ..." (drop/replace "forensic"). |
| F3 | CRITICAL | SKILL.md:260 (Escalation Budget block) | `1st TFEP trigger  → /sc:forensic --tier light --intent triage` — dead command reference. | Rename to `/sc:troubleshoot`. |
| F4 | CRITICAL | SKILL.md:261 (Escalation Budget block) | `2nd TFEP trigger  → /sc:forensic --tier standard` — dead command reference. | Rename to `/sc:troubleshoot`. |
| F5 | CRITICAL | SKILL.md:137 (`**Diagnostic backend:**` declaration) | The new declaration is the migration's load-bearing anchor and asserts: "swapping the backend changes only this declaration **and the invocation string**." But the invocation string was NOT swapped (F1, F3, F4 all still say `/sc:forensic`). The declaration therefore points to a body state that does not exist — it promises the invocations match `troubleshoot` when they do not. This is a dangling forward-reference from the new declaration into stale body content. | Resolve F1/F3/F4 so the declaration's promise holds, OR (if intentionally backend-neutral) the invocation strings must be sourced from the declared backend. As written, declaration and body are mutually contradictory. |

---

## Authoritative-intent confirmation

The findings are not stylistic preference — they violate the migration's own stated acceptance
gate. `research-notes.md` (same task dir):

- L50–51: "the analysis recommends renaming 'forensic' → 'diagnostic escalation' and adding
  `diagnostic_backend: troubleshoot`."
- L103–104 (VALIDATION_REQUIREMENTS): "rg '/sc:forensic' returns only intentional
  historical/archive references."

`rg '/sc:forensic'` over §4.5 returns 4 LIVE protocol invocations (lines 214, 260, 261 — plus
the "forensic return contract" prose at 218), none of which are historical/archive. The
migration's own validation gate is therefore not met.

---

## What is correctly migrated (so this FAIL is targeted, not blanket)

- Step 3 heading → "Invoke diagnostic escalation" (renamed). PASS.
- Step 4 heading → "Consume diagnostic results" (renamed). PASS.
- `**Diagnostic backend:** troubleshoot` declaration added (137). PASS structurally.
- Escalation-gradient subhead reworded "for diagnostic-backend escalation" (174). PASS.
- Incident-report fields "Diagnostic artifacts" (252) and "committed ... alongside other
  diagnostic artifacts" (255) — both correctly de-forensic'd. PASS (research-notes had flagged
  these at old lines 250/253).
- Numbered sub-steps 1–15 integrity across all renames. PASS.

The rename was applied to every HEADING and PROSE label but NOT to the four
invocation/command-name tokens. The headings now lie about the bodies beneath them.

---

## Self-Audit

**(a) Reliance list — items I did NOT independently re-verify (none inherited; standalone lens):**
- No `## Inherited Structural Verdict` block was provided in the spawn prompt. This lens ran
  standalone; every claim below is from my own tool engagement.

**(b) Independent verification (≥1 required):**
- `grep -ni forensic SKILL.md` → confirmed 4 live tokens at lines 214, 218, 260, 261 (tool output, not inferred).
- `ls src/superclaude/commands/ | grep forensic|troubleshoot` → confirmed `troubleshoot.md` exists, `forensic.md` does NOT — establishing `/sc:forensic` is a dead command, not a still-valid alias.
- `Read SKILL.md:133–267` → confirmed renamed headings (207, 217) and new declaration (137) against stale bodies (214, 218).
- `sed -n '183,238p' | grep Step` → confirmed numbered sub-steps 1–15 contiguous and step-number cross-targets ("return to Step 2/3", "Proceed to Step 5") all resolve.
- `research-notes.md:50–51,103–104` → confirmed authoritative migration intent + validation gate.

**Confidence:** Verified: 9/9 chain links | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 2 | Grep: 3 | Glob: 0 | Bash: (grep/ls/sed via Bash) 4

No web research performed (lens is local-file-bound; no external claim required).

---

## Recommendations

1. Replace `/sc:forensic` → `/sc:troubleshoot` at SKILL.md:214, 260, 261.
2. Replace "forensic return contract" → "diagnostic return contract" at SKILL.md:218.
3. After fix, re-run the migration's own gate `rg '/sc:forensic' src/superclaude/skills/sc-task-protocol/SKILL.md` — must return zero live protocol invocations.
4. Then `make sync-dev` + `make verify-sync` (do NOT hand-edit `.claude/` mirror).

## QA Complete
