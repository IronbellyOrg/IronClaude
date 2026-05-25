---
proposal_id: 2
persona: frontend
model: sonnet
domain: product
strategy: agile
simulated: true
---

# Proposal 2: Frontend — Ship the Editorial Surface First, Treat the Pipeline as Plumbing

## Framing

The user's pain isn't "the LLM doesn't summarize well enough" — it's "I'm rewriting and reformatting AI output for 45 minutes after the model finishes." The wedge is the **editorial surface**: a fast, opinionated UI that turns a draft into a publishable changelog in under 5 minutes. The LLM pipeline is plumbing — important but not the differentiator.

## In-Product Placement

**GitHub App + lightweight web editor**, in that order:

1. **GitHub App** posts the draft changelog as a PR comment on the release PR (or as a comment on the GitHub release). One click "Open in editor" → opens our web surface.
2. **Web editor** (the actual product surface):
   - Draft on the left, three theme columns on the right (Features / Fixes / Breaking).
   - Drag-and-drop to re-group an entry.
   - Inline "rewrite tone" buttons per entry: developer-facing / business-facing / executive.
   - Per-entry "exclude from changelog" toggle (some PRs are internal-only and shouldn't appear).
   - Live preview of the final Markdown on the right edge.
   - "Copy as Markdown" / "Publish to GitHub release" as the two terminal actions.

## User Experience Flows

**Primary flow (90% of usage)**:
1. Release manager merges release PR → GitHub App auto-posts draft.
2. Click "Open in editor" → loads web UI with the draft pre-populated.
3. Three minutes of dragging, toggling, re-toning → click "Publish".
4. Done. Release notes land on the GitHub release.

**Edge flow**:
- "Regenerate with different persona" button if the whole draft is the wrong vibe.
- "Add custom section" for highlights that don't fit the three themes.

## UX Decisions That Matter

- **No long-form text editor.** Editing is structured (drag, toggle, retone), not free-form rewriting. This is the wedge over Release.com's editorial-heavy approach: faster, more opinionated, less blank-page anxiety.
- **Cost telemetry is a status-bar element**, not a modal. Release managers want to know but not be confronted.
- **Persona tuning is a per-entry inline button**, not a global setting. Lets the release manager mix tones if they want (most won't, a few will, and that flexibility costs us nothing once it's built).
- **Accessibility from day 1**: keyboard navigation for the drag-and-drop (arrow keys + space-to-pick-up), screen-reader labels on theme columns. Standard a11y, no compromise.
- **Mobile**: don't bother. This is a desktop release-manager workflow. Build a "view-only" mobile page and stop.

## Build vs. Buy

- Use a proven drag-and-drop lib (dnd-kit) — don't roll our own.
- Use a proven Markdown renderer (react-markdown + remark plugins).
- LLM pipeline: smallest viable shim — single-pass with one model is *fine* for MVP. We'll learn whether two-pass quality matters from real usage; if MVP quality is "good enough" we ship sooner.

## Risks I'd Surface in Debate

- "Web editor MVP" is more product surface than "GitHub App MVP". Could push us past the 2-sprint window.
- Single-pass LLM may produce worse drafts than two-pass — but if the editor is good, users edit the draft anyway, and we save the architecture work.
- Drag-and-drop on long lists (50+ entries) needs perf attention.

## MVP Scope I'd Ship First

1. GitHub App that posts a draft (single-pass LLM — start simple).
2. Web editor with the three-column theme view + drag-to-regroup + per-entry retone.
3. "Publish to GitHub release" as the one-click terminal action.
4. BYO-key only — no hosted inference for MVP.
5. Cost telemetry as a status-bar item.

## Why This Wins

Release managers don't buy "structured extraction pipeline". They buy "I finished my release notes in 5 minutes instead of 45". The editor is the product. The pipeline is the engine. Optimize for the product surface; the engine can be upgraded behind the scenes once we see real usage patterns.
