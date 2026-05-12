# Workflow Plan: Apply Reflection Fixes to `sc-reflect-rescrutiny-design.md`

## Metadata

| Field | Value |
|---|---|
| **Generated** | 2026-05-07 |
| **Source design** | `/config/workspace/IronClaude/.dev/releases/current/sc-reflect-rescrutiny-design.md` |
| **Reflection origin** | `/sc:reflect --type task --validate` (this session) — produced blockers B1–B5 and hedges H1–H3 |
| **Strategy** | systematic |
| **Depth** | normal |
| **Scope** | Two-stage, single workflow: (1) repair the design doc — Waves 1–4; (2) propagate the design's §7 directives into `src/superclaude/commands/reflect.md` and run sync — Wave 5. |
| **Total edits** | 8 design-doc fixes (B1–B5 + H1–H3) + 7 reflect.md updates (§7.0–§7.6) + 2 sync commands = **17 discrete tasks** |
| **Estimated LOC** | ~30 lines edited in design + ~25 lines added/edited in reflect.md = **~55 total** |
| **Risk** | LOW — additive behavioral phase, gated by activation rule; no change to existing 5-phase semantics; sync chain is well-trodden |

---

## Executive Summary

The reflection identified 5 blockers (must-fix before `/sc:implement`) and 3 hedges (specification gaps, can ship with caveats) in the design document. This workflow sequences those fixes by document section (top-to-bottom) so the editor never has to scroll back. All edits target a single file. After the design is repaired, a separate workflow (out of scope here) drives the implementation against `src/superclaude/commands/reflect.md` and the sync chain.

**On `make sync-dev` / `make verify-sync`:** The design doc at `.dev/releases/current/sc-reflect-rescrutiny-design.md` is **not** part of the `src/` → `.claude/` sync chain — its repair (Waves 1–3) is in-tree only. Once the design is repaired and verified (Wave 4), Wave 5 carries the design's §7 directives into `src/superclaude/commands/reflect.md` (which IS in the sync chain), then runs `make sync-dev` + `make verify-sync` to propagate to `.claude/commands/sc/reflect.md`. The single workflow covers both stages; Gate G4 separates them so the executor can checkpoint between repair and propagation if desired.

---

## Section-Anchor Index (read order)

The design doc repair (Waves 1–3) processes fixes in document order:

| Order | File | Anchor | Fix ID | Type |
|---|---|---|---|---|
| 1 | design | §3.1 Activation | B5 | Blocker |
| 2 | design | §3.3 Extract step | H1 | Hedge |
| 3a | design | §3.6 stakes-tier table seam | B4 | Blocker |
| 3b | design | §3.6 (after B4 paragraph) | H2 | Hedge |
| 3c | design | §3.6 (after H2 paragraph) | H3 | Hedge |
| 4 | design | §7.1 reflect.md Behavioral Flow directive | B2 | Blocker |
| 5 | design | §7.3 reflect.md Tool Coordination directive | B1 | Blocker |
| 6 | design | §10 Implementation handoff | B3 | Blocker |

The reflect.md propagation (Wave 5) processes the design's §7 directives in §7.x order:

| Order | File | Anchor | Source directive |
|---|---|---|---|
| 8 | reflect.md | YAML frontmatter `mcp-servers` line | design §7.0 |
| 9 | reflect.md | `## Behavioral Flow` numbered list | design §7.1 |
| 10 | reflect.md | `## MCP Integration` section | design §7.2 |
| 11 | reflect.md | `## Tool Coordination` section | design §7.3 |
| 12 | reflect.md | `## Key Patterns` section | design §7.4 |
| 13 | reflect.md | `## Boundaries — Will` section | design §7.5 |
| 14 | reflect.md | `## Boundaries — Will Not` section | design §7.6 |
| 15 | repo root | `make sync-dev` | (sync chain) |
| 16 | repo root | `make verify-sync` | (sync chain) |

Design §2 already lists 6 phases correctly; no edit needed there. The phase-numbering contradiction lives in §7.1's directive, fixed by Task 4.

---

## Wave Structure

### Wave 1 — Document body fixes (sections 3.x), TOP-DOWN SEQUENTIAL

Sequential because the edits are inside the same file. Going top-down minimizes anchor drift.

#### Task 1 — §3.1 Activation: add false-positive exclusion (B5)

- **Anchor:** `### 3.1 Activation`, end of section, after the existing bullet list and the "Most reflections will skip this phase entirely." sentence.
- **Method:** Insert new paragraph after the existing closing sentence.
- **Old → New (sketch):**

  *Old (closing):*
  > If none match, phase is a no-op and reflection proceeds straight to Document. **Most reflections will skip this phase entirely.**

  *New (append):*
  > If none match, phase is a no-op and reflection proceeds straight to Document. **Most reflections will skip this phase entirely.**
  >
  > **False-positive exclusion.** Illustrative content does not activate the phase. A candidate is treated as illustrative — and the activation rule does NOT fire — when any of the following hold:
  > - The verb is in past tense (`started`, `pushed`, `deleted`).
  > - The verb is surrounded by hedging or framing words: `would`, `caught`, `rejected`, `blocked`, `example`, `imagine`, `suppose`.
  > - The verb appears inside a quote block introduced by `> **Re-scrutiny caught:**` (this is the design's own re-scrutiny output format; recursing on it would be silly).
  > - The verb appears inside a section explicitly marked as a worked example, table cell, or audit-annotation example (e.g., the rows of §3.2 or the prose of §5 in this design).
  >
  > Activation is reserved for content the user is plausibly meant to act on, not content that explains what the phase will do.

#### Task 2 — §3.3 Extract step: tighten variable resolution (H1)

- **Anchor:** `### 3.3 Extract step`, the second bullet ("Resolve variable references where possible (`$CTID` from a heredoc array → concrete CTID).").
- **Method:** Replace the bullet with a more concrete spec.
- **Old → New (sketch):**

  *Old:*
  > - Resolve variable references where possible (`$CTID` from a heredoc array → concrete CTID).

  *New:*
  > - Resolve variable references along a tiered policy:
  >   - **Resolve eagerly** when the value is a literal in scope: heredoc array entries, immediate `VAR=value` assignments above the use site, and let-binding-style fixed values.
  >   - **Mark `<unresolved>` and route to HEDGE** when the value depends on `$(...)` command substitution, env-var interpolation (`$HOME`, `$CI_*`), or multi-step construction across files. Never PASS a tuple whose object is `<unresolved>` — the gate cannot verify what it cannot read.
  >   - When in doubt, prefer `<unresolved>` over a guessed resolution; a hedge annotation is cheaper than a wrong PASS.

#### Task 3a — §3.6 environment classification (B4)

- **Anchor:** `### 3.6 Decision gate — stratified by action stakes`, the unique line `Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:` (the intro sentence above the gate-behavior table).
- **Method:** Insert one paragraph immediately before that intro line.
- **Old → New (sketch):**

  *Old (the unique anchor line):*
  > Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

  *New (replace with):*
  > **Environment classification (B4).** Stakes tier for verbs whose tier depends on environment (`kubectl apply`, `docker push`, `terraform apply`, cloud `update-*` against named resources) is derived in this priority order:
  > 1. **Explicit environment markers in the recommendation text** — comments like `# prod`, flags like `--env prod`, manifest paths like `k8s/prod/*.yaml`, or prose framing ("deploy to production").
  > 2. **Inferred markers from context** — `kubectl` context name, `terraform` workspace name, branch name (`main`, `master`, `prod`, `release/*`), or registry path patterns (`*.prod.example.com`).
  > 3. **Default to HIGH** when neither is present. The cost of being wrong against prod is asymmetric — false-HIGH causes a hedge annotation, false-MEDIUM lets a destructive command ship.
  >
  > Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

#### Task 3b — §3.6 flag-set as matching key (H2)

- **Anchor:** End of Task 3a's just-inserted paragraph (the line `false-HIGH causes a hedge annotation, false-MEDIUM lets a destructive command ship.`). **Depends on Task 3a having run.**
- **Method:** Insert one paragraph between the close of B4 and the gate-behavior intro line.
- **Old → New (sketch):**

  *Old (post-3a unique seam):*
  > 3. **Default to HIGH** when neither is present. The cost of being wrong against prod is asymmetric — false-HIGH causes a hedge annotation, false-MEDIUM lets a destructive command ship.
  >
  > Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

  *New:*
  > 3. **Default to HIGH** when neither is present. The cost of being wrong against prod is asymmetric — false-HIGH causes a hedge annotation, false-MEDIUM lets a destructive command ship.
  >
  > **Flag-set as part of the matching key (H2).** Stakes tier and gate decisions key on `(verb, critical-flag-set)`, not verb alone. The §3.2 allowlist explicitly distinguishes `git push` from `git push --force`, `rsync` from `rsync --delete`, `docker build` from `docker build --push`, `kubectl apply` from `kubectl apply --prune`. Critical flags promote tier (e.g., `git push` MEDIUM → `git push --force` HIGH). Flags that don't change the verb's effect on target state (e.g., `--quiet`, `--verbose`) are ignored for keying.
  >
  > Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

#### Task 3c — §3.6 empty / ambiguous object handling (H3)

- **Anchor:** End of Task 3b's just-inserted paragraph. **Depends on Task 3b.**
- **Method:** Insert one paragraph between the close of H2 and the gate-behavior intro line.
- **Old → New (sketch):**

  *Old (post-3b seam):*
  > Critical flags promote tier (e.g., `git push` MEDIUM → `git push --force` HIGH). Flags that don't change the verb's effect on target state (e.g., `--quiet`, `--verbose`) are ignored for keying.
  >
  > Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

  *New:*
  > Critical flags promote tier (e.g., `git push` MEDIUM → `git push --force` HIGH). Flags that don't change the verb's effect on target state (e.g., `--quiet`, `--verbose`) are ignored for keying.
  >
  > **Empty / ambiguous object (H3).** A state-changing verb whose object is missing, blank, or `<unresolved>` (per §3.3) is **always BLOCK**. The gate cannot verify a target it cannot identify; running such a command would let shell expansion or interactive selection make the choice for the user — exactly the failure mode this phase exists to prevent.
  >
  > Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

### Wave 2 — reflect.md spec-text changes (section 7.x), TOP-DOWN SEQUENTIAL

Same file, same sequential constraint, lower in the document.

#### Task 4 — §7.1 Behavioral Flow change: 6-phase renumber (B2)

> **Layering note:** §7.1 is a *meta-directive* — its body describes a change to be applied to `reflect.md`. This task edits the description, not `reflect.md` itself. `reflect.md` is touched in Wave 5, which reads this updated directive.

- **Anchor:** `### 7.1 \`## Behavioral Flow\` — add phase between Reflect and Document`.
- **Method:** Replace the entire sub-section body. The current body uses sub-step `3.5`; replace with a 6-phase renumber that matches §2's already-correct 6-phase list.
- **Old → New (sketch):**

  *Old:*
  > Insert after current step 3:
  >
  > > 3.5. **Re-scrutinize**: For any executable artifacts produced (shell commands, code blocks, action recommendations), extract `(verb, object)` tuples; pass each through session-fact lookup; for allowlisted CLI verbs unresolved by session, fetch external preconditions via context7; block or rewrite contradictions before delivery. Skipped entirely when no executable artifacts are present.

  *New:*
  > Replace the existing 5-phase numbered list with the 6-phase list below. Renumber Document (5) and Optimize (6) accordingly. The new phase 4 reads:
  >
  > > 1. **Analyze**: Examine current task state and session progress using Serena reflection tools
  > > 2. **Validate**: Assess task adherence, completion quality, and requirement fulfillment
  > > 3. **Reflect**: Apply deep analysis of collected information and session insights
  > > 4. **Re-scrutinize**: For any executable artifacts produced (shell commands, code blocks, action recommendations), extract `(verb, object)` tuples; pass each through session-fact lookup; for allowlisted CLI verbs unresolved by session, fetch external preconditions via context7; block or rewrite contradictions before delivery. Skipped entirely when no executable artifacts are present.
  > > 5. **Document**: Update session metadata and capture learning insights
  > > 6. **Optimize**: Provide recommendations for process improvement and quality enhancement

#### Task 5 — §7.3 Tool Coordination Grep entry: fix internal contradiction (B1)

- **Anchor:** `### 7.3 \`## Tool Coordination\` — add Grep and WebSearch`, the first appended bullet (Grep).
- **Method:** Replace the Grep bullet only. WebSearch bullet stays as-is.
- **Old → New (sketch):**

  *Old:*
  > > - **Grep**: Conversation-transcript scan for asserted facts about objects named in reflection-emitted recommendations.

  *New:*
  > > - **Grep**: File-anchored augmentation during the session-fact pass — pattern lookup within config files, mirror files, or pasted log paths the conversation references. Grep operates on files, not the transcript; transcript scanning is handled by in-context reasoning per §3.4.

### Wave 3 — Implementation handoff (section 10), STANDALONE

#### Task 6 — §10: correct source-of-truth path (B3)

- **Anchor:** `## 10. Implementation handoff`.
- **Method:** Replace the entire section body with the project-canonical chain.
- **Old → New (sketch):**

  *Old:*
  > Next step: `/sc:implement` against this design document, applied to `/config/.claude/commands/sc/reflect.md`. Per the global CLAUDE.md component-sync rule, the same edit must propagate to the canonical source at `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/_src/superclaude/commands/reflect.md` (or wherever the active SuperClaude install treats as source-of-truth — verify before editing). After both edits, run `make verify-sync` if the project's source tree is in scope, or perform a manual diff if the SuperClaude install is the only source.
  >
  > Verification of the change: re-run the §5 worked-example scenario by hand-feeding the same draft output to a refactored `/sc:reflect` and confirm the bug is caught. No other functional regression test is needed; the phase is purely additive and skipped on reflections with no executable output.

  *New:*
  > Next step: `/sc:implement` against this design document, applied to the canonical source `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`. Per the project's component-sync rule (`CLAUDE.md` §"Component Sync"), `src/superclaude/` is the source of truth and `.claude/commands/sc/reflect.md` is a synced dev copy. After editing the source, run:
  >
  > ```bash
  > make sync-dev      # copies src/superclaude/{skills,agents,commands} → .claude/
  > make verify-sync   # confirms src/ and .claude/ match
  > ```
  >
  > Do **not** edit the pipx-installed copy at `/config/.local/share/pipx/venvs/superclaude/lib/...` — that path is downstream of the source tree and will be overwritten on the next package install.
  >
  > Verification of the change: re-run the §5 worked-example scenario by hand-feeding the same draft output to a refactored `/sc:reflect` and confirm the bug is caught. No other functional regression test is needed; the phase is purely additive and skipped on reflections with no executable output.

### Wave 4 — Verification (no edits, design-doc only)

#### Task 7 — Internal-consistency verification on the repaired design

**Absence checks** (these strings should be GONE from the design):
- `grep -n "3\.5" sc-reflect-rescrutiny-design.md` — expected: zero hits in §7.1's body.
- `grep -n "pipx" sc-reflect-rescrutiny-design.md` — expected: only inside a "do not edit" caveat in §10.
- `grep -n "Conversation-transcript scan" sc-reflect-rescrutiny-design.md` — expected: zero hits.

**Presence checks** (these strings MUST be present after fixes land):
- `grep -n "False-positive exclusion" sc-reflect-rescrutiny-design.md` → §3.1 (B5).
- `grep -nE "Resolve eagerly|<unresolved>" sc-reflect-rescrutiny-design.md` → §3.3 (H1).
- `grep -n "Environment classification" sc-reflect-rescrutiny-design.md` → §3.6 (B4).
- `grep -nE "Flag-set as part of the matching key|critical-flag-set" sc-reflect-rescrutiny-design.md` → §3.6 (H2).
- `grep -n "Empty / ambiguous object" sc-reflect-rescrutiny-design.md` → §3.6 (H3).
- `grep -n "make sync-dev" sc-reflect-rescrutiny-design.md` → §10 (B3).
- `grep -n "Re-scrutinize" sc-reflect-rescrutiny-design.md` → §7.1 directive (B2).

**Cross-consistency checks:**
- §2 (current 6-phase list) and §7.1 (post-fix directive) describe the same 6 phases in the same order. Expected: yes; §2 needs no edit.
- §3.4 and §7.3 both describe Grep as file-anchored only. Expected: B1 cleared the contradiction.
- §3.6's three new clauses (B4 → H2 → H3) appear in order between the stakes-tier table and the gate-behavior table.

**Gate G4** (above) summarizes pass criteria. **G4 PASSING is a precondition for Wave 5.**

### Wave 5 — `reflect.md` propagation + sync chain

**Precondition:** Gate G4 has passed — the design is verified internally consistent. Wave 5 takes the design's §7.0–§7.6 directives and applies them to the canonical `src/superclaude/commands/reflect.md`, then propagates via `make sync-dev` and verifies via `make verify-sync`.

**Source-of-truth chain:** edit `src/superclaude/commands/reflect.md` first (canonical), then `make sync-dev` propagates to `.claude/commands/sc/reflect.md`, then `make verify-sync` confirms parity. Per the project's `CLAUDE.md` §"Component Sync", do **not** edit `.claude/commands/sc/reflect.md` directly.

#### Task 8 — `reflect.md` YAML frontmatter (design §7.0)

- **Anchor:** YAML frontmatter line `mcp-servers: [serena]`.
- **Method:** Replace the line.
- **Old → New (sketch):**

  *Old:*
  > `mcp-servers: [serena]`

  *New:*
  > `mcp-servers: [serena, context7]`

#### Task 9 — `reflect.md` Behavioral Flow numbered list (design §7.1)

- **Anchor:** `## Behavioral Flow` heading, the 5-item numbered list immediately after the heading.
- **Method:** Replace the 5-item list with the 6-item list specified by design §7.1's repaired directive. Insert `Re-scrutinize` as item 4; renumber Document → 5, Optimize → 6.
- **Old → New (sketch):**

  *Old (5 items, current text in `reflect.md`):*
  > 1. **Analyze**: Examine current task state and session progress using Serena reflection tools
  > 2. **Validate**: Assess task adherence, completion quality, and requirement fulfillment
  > 3. **Reflect**: Apply deep analysis of collected information and session insights
  > 4. **Document**: Update session metadata and capture learning insights
  > 5. **Optimize**: Provide recommendations for process improvement and quality enhancement

  *New (6 items):*
  > 1. **Analyze**: Examine current task state and session progress using Serena reflection tools
  > 2. **Validate**: Assess task adherence, completion quality, and requirement fulfillment
  > 3. **Reflect**: Apply deep analysis of collected information and session insights
  > 4. **Re-scrutinize**: For any executable artifacts produced (shell commands, code blocks, action recommendations), extract `(verb, object)` tuples; pass each through session-fact lookup; for allowlisted CLI verbs unresolved by session, fetch external preconditions via context7; block or rewrite contradictions before delivery. Skipped entirely when no executable artifacts are present.
  > 5. **Document**: Update session metadata and capture learning insights
  > 6. **Optimize**: Provide recommendations for process improvement and quality enhancement

#### Task 10 — `reflect.md` MCP Integration: append Context7 entry (design §7.2)

- **Anchor:** `## MCP Integration` section, end of the bullet list (after the existing `Performance Critical` bullet).
- **Method:** Append one new bullet.
- **New (append):**
  > - **Context7 MCP**: Conditional invocation during Recommendation Re-scrutiny for CLI verb precondition lookup when session-fact pass is silent.

#### Task 11 — `reflect.md` Tool Coordination: append Grep + WebSearch (design §7.3, post-B1)

- **Anchor:** `## Tool Coordination` section, end of bullet list.
- **Method:** Append two new bullets. Use the **post-B1 (file-anchored)** Grep description, not the original transcript-scan wording.
- **New (append):**
  > - **Grep**: File-anchored augmentation during the session-fact pass — pattern lookup within config files, mirror files, or pasted log paths the conversation references. Grep operates on files, not the transcript; transcript scanning is handled by in-context reasoning.
  > - **WebSearch**: Fallback CLI precondition lookup when Context7 doesn't cover the tool.

#### Task 12 — `reflect.md` Key Patterns: append Re-scrutiny pattern (design §7.4)

- **Anchor:** `## Key Patterns` section, end of bullet list.
- **Method:** Append one new bullet.
- **New (append):**
  > - **Recommendation Re-scrutiny**: Extract executable artifacts → session-fact lookup → conditional external-doc lookup → decision gate (pass/block/hedge) → audit annotation.

#### Task 13 — `reflect.md` Boundaries → Will: append 3 bullets (design §7.5)

- **Anchor:** `**Will:**` block under `## Boundaries`, end of its bullet list.
- **Method:** Append three new bullets.
- **New (append):**
  > - Re-scrutinize executable artifacts emitted by the reflection itself before delivery.
  > - Block reflection-emitted recommendations that contradict facts asserted in the current session or in authoritative external documentation.
  > - Annotate every cleared recommendation with the basis on which it was cleared.

#### Task 14 — `reflect.md` Boundaries → Will Not: append 3 bullets (design §7.6)

- **Anchor:** `**Will Not:**` block under `## Boundaries`, end of its bullet list.
- **Method:** Append three new bullets.
- **New (append):**
  > - Maintain a persistent cross-session entity registry or knowledge graph; the session-fact set is ephemeral and lives only within one reflect call.
  > - Block on hedge cases for LOW/MEDIUM stakes — when neither session nor external docs resolve a precondition question for a non-HIGH-stakes verb, surface the unverified status and recommend a check, but do not refuse to deliver. (HIGH-stakes verbs DO block on hedge per §3.6 — see design.)
  > - Validate non-executable commentary, prose analysis, or reasoning narratives — only artifacts the user is expected to act on are in scope.

#### Task 15 — `make sync-dev`

- **Method:** Run `make sync-dev` from the repo root (`/config/workspace/IronClaude`). Expected: copies `src/superclaude/{skills,agents,commands}` → `.claude/`, no errors. The reflect.md delta is the change of interest; other components should be no-ops.

#### Task 16 — `make verify-sync`

- **Method:** Run `make verify-sync` from the repo root. Expected: exit code 0, output indicates `src/` and `.claude/` are in sync. **This is gate G6 — the final completion criterion for the workflow.**

---

## Dependency Graph

```
Wave 1: Task 1 (§3.1) ──> Task 2 (§3.3) ──> Task 3a ──> Task 3b ──> Task 3c (§3.6 ×3)
                                                                          │
Wave 2: Task 4 (§7.1) ──> Task 5 (§7.3) ─────────────────────────────────┤
                                                                          │
Wave 3: Task 6 (§10) ─────────────────────────────────────────────────────┤
                                                                          ▼
                                                            Wave 4: Task 7 (verify)
                                                                          │
                                                              Gate G4 ────┤
                                                                          ▼
       Wave 5: Tasks 8–14 (reflect.md §7.0–§7.6) ──> Task 15 (sync) ──> Task 16 (verify-sync)
```

All anchors are **section-header-based** (`### 3.1 Activation`, `### 3.6 …`, etc.), which are stable across edits within the same file. Line-number drift from earlier insertions does not invalidate later anchors. Within §3.6, Tasks 3a → 3b → 3c are strictly sequential because each task's anchor is text introduced by the previous task. Wave 5 is gated by Wave 4 success (a broken design must not propagate to `reflect.md`).

---

## Execution Order (final)

1. **Wave 1, sequential, top-down:** Task 1 → Task 2 → Task 3a → Task 3b → Task 3c.
2. **Wave 2, sequential, top-down:** Task 4 → Task 5.
3. **Wave 3, standalone:** Task 6.
4. **Wave 4, design-doc verification:** Task 7. **Gate G4 must pass before Wave 5.**
5. **Wave 5, reflect.md propagation, sequential:** Task 8 (frontmatter) → Task 9 (Behavioral Flow) → Task 10 (MCP Integration) → Task 11 (Tool Coordination) → Task 12 (Key Patterns) → Task 13 (Boundaries Will) → Task 14 (Boundaries Will Not) → Task 15 (`make sync-dev`) → Task 16 (`make verify-sync`).

---

## Quality Gates / Checkpoints

| Gate | After | Pass criteria |
|---|---|---|
| G1 | Wave 1 complete (Tasks 1, 2, 3a–3c) | §3.1 contains the string `False-positive exclusion`. §3.3 second bullet contains both `<unresolved>` and `Resolve eagerly`. §3.6 contains all three of: `Environment classification`, `Flag-set as part of the matching key`, `Empty / ambiguous object`, in that order. |
| G2 | Wave 2 complete | The string `Conversation-transcript scan` no longer exists anywhere in the design; the string `3.5` no longer exists in §7.1's body; §7.1's directive lists 6 numbered phases with `Re-scrutinize` as phase 4. |
| G3 | Wave 3 complete | §10 references `src/superclaude/commands/reflect.md` and `make sync-dev`; the pipx path appears only inside a "do not edit" caveat. |
| G4 | Wave 4 complete | All 8 design-doc fix IDs (B1–B5, H1–H3) trace to a confirmed change. No edits outside the listed anchors. **Gates Wave 5 entry.** |
| G5 | Wave 5 Tasks 8–14 complete | `reflect.md` frontmatter shows `mcp-servers: [serena, context7]`. `## Behavioral Flow` lists 6 phases with `Re-scrutinize` as phase 4. `## MCP Integration` includes a Context7 entry. `## Tool Coordination` includes Grep + WebSearch entries (Grep description matches design §3.4 — file-anchored, not transcript). `## Key Patterns` includes a `Recommendation Re-scrutiny` bullet. `## Boundaries — Will` and `## Boundaries — Will Not` each have 3 new bullets. |
| G6 | Wave 5 sync complete | `make verify-sync` exits 0; `.claude/commands/sc/reflect.md` and `src/superclaude/commands/reflect.md` are byte-identical for the reflect.md file. |

---

## Implementation Handoff

**Single command** to execute the entire plan (Waves 1–5):

```
/sc:task "Execute the workflow plan in /config/workspace/IronClaude/.dev/releases/current/sc-reflect-rescrutiny-workflow.md end-to-end. Process all five waves in order. Wave 4's gate G4 must pass before Wave 5 begins; Wave 5's gate G6 (make verify-sync exit 0) is the final completion criterion."
```

If the executor wants to checkpoint between design repair and reflect.md propagation (e.g., for review of the repaired design before it ships into the active behavioral spec), run Waves 1–4 first and stop at G4, then run Wave 5 separately:

```
# Stage 1 — design repair only
/sc:task "Execute Waves 1–4 only of the workflow plan in /config/workspace/IronClaude/.dev/releases/current/sc-reflect-rescrutiny-workflow.md. Stop after gate G4 passes."

# Stage 2 — propagation (after stage 1 review)
/sc:task "Execute Wave 5 of the workflow plan in /config/workspace/IronClaude/.dev/releases/current/sc-reflect-rescrutiny-workflow.md. Precondition: gate G4 has passed."
```
