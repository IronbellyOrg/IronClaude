Goal: Generate a Sprint CLI-compatible tasklist bundle from the checkout-v2 spec at `docs/specs/checkout-v2-spec.md`.

Recommended delegation: `/sc:tasklist` — this is the project's dedicated tasklist-bundle generator, owns the deterministic phasing/tier-classification/validation pipeline, and accepts a `--spec` flag for supplementary spec context. Net-value win: structured artifact + template enforcement + roadmap-validation pass; native Read/Write cannot reproduce the tier scoring, deliverable IDs, or Sprint CLI compatibility self-checks.

Important caveat surfaced during verification: `/sc:tasklist` takes `<roadmap-path>` as its **primary** positional argument, not a spec. The skill's auto-derivation logic (`TASKLIST_ROOT` from `.dev/releases/current/<segment>/` or `v<digits>` token) and Stage 7 roadmap-validation phase both depend on roadmap content. Running `/sc:tasklist` against a spec directly will either fall back to `v0.0-unknown` output dir and produce a tasklist with no roadmap to validate against, or fail input validation. The canonical pipeline is **spec → `/sc:roadmap` → roadmap.md → `/sc:tasklist <roadmap> --spec <spec>`**. Two paste-ready prompts below cover (A) the full canonical pipeline and (B) the direct attempt if a roadmap already exists.

---

**Path A — Canonical pipeline (recommended if no roadmap exists yet):**

Paste-ready prompt:

```text
First generate a roadmap from the spec, then generate a tasklist bundle from that roadmap with the spec as supplementary context.

Step 1:
/sc:roadmap docs/specs/checkout-v2-spec.md

Wait for roadmap pipeline to complete. Note the output directory (printed on completion) and the roadmap.md path inside it.

Step 2:
/sc:tasklist @<roadmap-path-from-step-1> --spec @docs/specs/checkout-v2-spec.md

Deliverable: a Sprint CLI-compatible tasklist bundle (tasklist-index.md + phase-N-tasklist.md files) plus validation artifacts under TASKLIST_ROOT/validation/. Report the final tasklist-index.md path when done.
```

**Path B — Direct invocation (only if a roadmap already exists in `.dev/releases/current/` for this work):**

Paste-ready prompt:

```text
/sc:tasklist @<existing-roadmap.md> --spec @docs/specs/checkout-v2-spec.md

If no roadmap exists yet for the checkout-v2 work, stop and run /sc:roadmap docs/specs/checkout-v2-spec.md first — /sc:tasklist requires a roadmap as its primary input.

Deliverable: Sprint CLI-compatible tasklist bundle + roadmap-validation report.
```

Disambiguator: pick A by default; pick B only if you already have a checkout-v2 roadmap.md committed under `.dev/releases/current/`.

Sources verified:

- `src/superclaude/commands/tasklist.md` (Read) — flags `<roadmap-path>`, `--spec`, `--output`; TASKLIST_ROOT auto-derivation; activation hands off to `sc:tasklist-protocol`.
- `src/superclaude/commands/roadmap.md` (Read) — accepts spec/TDD/PRD inputs; output dir defaults to parent of first input.
- `src/superclaude/skills/task-builder/SKILL.md` (Read) — produces a single MDTM task file in `.dev/tasks/to-do/`, **not** a Sprint tasklist bundle. Considered and rejected: user asked for a tasklist (multi-phase Sprint bundle), not a single MDTM task file.
- Auggie semantic rank: confirmed `/sc:tasklist` is the canonical roadmap→tasklist generator; confirmed `task-builder` is for single MDTM task creation (different artifact). Auggie also surfaced the deterministic generation primitives (R-### / T<PP>.<TT> / D-#### IDs, tier scoring, TASKLIST_ROOT derivation) that confirm spec-only input is out-of-contract for `/sc:tasklist`.
