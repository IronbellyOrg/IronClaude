# Finding 1 — SPEC.md `--generate` mode inconsistency (r3312667799)

## Reviewer claim

> The pipeline diagram shows `/sc:adversarial --generate requirements`, but later sections (and `refs/handoff-routing.md`) describe using `--generate spec`. This inconsistency could cause readers to invoke an unsupported generate mode or implement the wrong integration.

## Validation result

**CONFIRMED** (with one factual correction to the reviewer's framing — `refs/handoff-routing.md` does not exist on this branch).

Evidence on `origin/chore/brainstorm-live-evals`:

- `.dev/eval-workspaces/sc-brainstorm/SPEC.md:55` (pipeline diagram, Section 1): `├── /sc:adversarial --source seed-brief.md --generate requirements --agents <built-spec>`
- `.dev/eval-workspaces/sc-brainstorm/SPEC.md:264` (Section: Flags, default value example): `   --generate requirements           # New generate type, see §10`
- `.dev/eval-workspaces/sc-brainstorm/SPEC.md:472` (Section 10, the authoritative decision): `**Decision (post-spec-panel review)**: v2 ships using `--generate spec` and reframes its contract as **"spec-style requirements"**. No blocker on adding `--generate requirements` to `/sc:adversarial`.`
- `.dev/eval-workspaces/sc-brainstorm/SPEC.md:477,693,707`: §16 Followups explicitly tracks "Add `--generate requirements` to `/sc:adversarial` and switch v2 to it" as a **future** enhancement; §15 Decisions records "Decided on `--generate spec` path for adversarial integration (§10) — unblocks v2 ship".
- `src/superclaude/commands/adversarial.md:44` (PR branch) — supported types are documented as `roadmap, spec, design, etc.`; `requirements` is not currently a supported value (confirmed by §10's "No blocker on adding `--generate requirements`" language — i.e., it does not exist yet).
- `src/superclaude/commands/brainstorm.md:133` (PR branch): `5. Wave 3: delegate to Skill sc-adversarial-protocol with --generate spec` — the shipped command file matches §10's decision.
- `.dev/eval-workspaces/sc-brainstorm/refs/handoff-routing.md` does NOT exist on `origin/chore/brainstorm-live-evals` (verified via `git show ... fatal: path ... does not exist`). The reviewer's reference is incorrect on that point, but the substantive inconsistency between the pipeline diagram and §10 / `brainstorm.md` is real.

## Root cause

The pipeline diagram (line 55) and the §3 flags default example (line 264) were authored against the original aspirational design (`--generate requirements`) and were not updated when the §10 spec-panel decision pivoted v2 to `--generate spec` to unblock the ship. They are stale relative to the authoritative decision in §10 and the actual integration in `brainstorm.md:133`. Classic "decision recorded in one section, prior diagrams not back-propagated."

## Proposed fix

**Files to change** (on `chore/brainstorm-live-evals`):

- `.dev/eval-workspaces/sc-brainstorm/SPEC.md` line `55`: replace `--generate requirements` with `--generate spec` and update the immediately following node label.
- `.dev/eval-workspaces/sc-brainstorm/SPEC.md` line `264`: replace the flag default + comment.

**Exact diff sketch:**

```diff
@@ SPEC.md line 55 (pipeline diagram in §1)
-   ├── /sc:adversarial --source seed-brief.md --generate requirements --agents <built-spec>
+   ├── /sc:adversarial --source seed-brief.md --generate spec --agents <built-spec>
    ↓
-   ├── merged-requirements.md  + 6 adversarial artifacts
+   ├── merged-requirements.md  + 6 adversarial artifacts   # spec-shaped per §10
@@ SPEC.md line 264 (§3 flags example)
-   --generate requirements           # New generate type, see §10
+   --generate spec                   # Reframed as "spec-style requirements" per §10
```

Note: the output filename `merged-requirements.md` (lines 57, 286, 299, 302, 307, 325, 388, 453, 525, 581, 582, 583, 681) should remain unchanged — §10 is explicit that v2 reframes a spec-shaped output as "spec-style requirements" and the filename is part of v2's external contract. Touching it would be scope creep and contradict §10.

## Risk / blast radius

Very low. Two surgical text edits to a doc-only file in `.dev/eval-workspaces/`; no code, no skill, no command file affected. Post-fix grep on the PR branch should show zero remaining `--generate requirements` occurrences in `SPEC.md` outside §10/§15/§16 (which discuss the future enhancement and must be preserved). Run: `git grep -n "generate requirements" .dev/eval-workspaces/sc-brainstorm/SPEC.md` — expected hits only on lines 472, 477, 479, 693 (all in §10/§16 context).

## Confidence

**95%** — Reviewer claim is confirmed by §10's explicit decision and by `brainstorm.md:133`'s shipped integration; the only uncertainty is whether the author intentionally left the diagram aspirational, which §10 and §16's explicit "future enhancement" framing rules out.
