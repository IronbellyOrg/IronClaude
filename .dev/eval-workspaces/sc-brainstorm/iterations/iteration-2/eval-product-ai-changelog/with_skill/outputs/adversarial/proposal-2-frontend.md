---
proposal_id: 2
persona: frontend
model: sonnet
custom_instruction: "focus on user experience, accessibility, error states, and responsive behavior"
stance: editorial-first-mvp
created: 2026-05-25T00:00:00Z
---

# Proposal 2 — Frontend: Editorial-First MVP

## Stance

**The product is the editor, not the pipeline.** Release managers will judge this tool in the first 30 seconds after the GitHub-comment link drops into Slack: did the draft look right, can they fix the one wrong thing fast, and does it publish in one click. If the editor is bad, no platform abstraction matters; if the editor is excellent, even a v1 pipeline will earn a second look. Build the editor first, build the pipeline to feed it, build the platform abstractions only when a second consumer asks. The trust contract is real, but it must be expressed AS PRODUCT — visible, editable, trustable surfaces — not as a backend validator that throws errors.

## The Editor (the MVP)

**Three-column theme view, primary surface.** Columns = Features / Fixes / Breaking & Deprecations. Each card is a single changelog entry with: title, body (1–2 lines), source-PR chip with hover-preview of the original PR title + author, persona-tone selector (developer / business / executive — applied per-entry, not globally), exclude toggle, and a citation badge showing which PR(s) ground this entry.

**Drag-to-regroup between themes.** Keyboard-accessible: arrow keys move focus between cards, space-bar picks-up, arrow keys move, space-bar drops. Screen-reader announces "moved Fixes #1234 to Breaking." WCAG 2.1 AA on color contrast, focus indicators, drag affordances.

**Per-entry retone (3 personas).** Developer-facing keeps technical terms; business-facing rewrites for non-technical readers; executive collapses to a one-liner. The retone is a per-entry LLM call (cheap, structured) so the user can mix personas across the same draft — most changelogs have "the feature your CFO cares about" next to "the migration only your platform team cares about."

**Inline citation surface.** Every claim is followed by a small pill like `(#1234)`. Hover shows the PR title, author, and the structured-extraction record that grounded the claim. Click jumps to the PR. The "trust contract" is not an abstract validator — it is THIS PILL on every line. If a pill is red, the validator rejected this entry; the user clicks, sees why ("breaking claim without corroborating signal"), and can either add a label upstream or downgrade the claim.

**Live Markdown preview** (right rail). Toggles to "diff-vs-original-draft" view so the release manager can see exactly what they changed before publish. This view is what closes the trust loop: "here is what the model said; here is what I'm publishing; the audit log will record both."

**Publish to GitHub release** (terminal action). One button. Confirms cost, confirms citation-pass, posts to the release, writes the audit-log entry.

## Trust Contract — As Product

The architect persona will want the trust validator to HARD-BLOCK publish on any citation failure. **Disagree** for MVP. Hard-block produces a frustrating "you can't ship until you fix this thing in a different system" experience for the user — they'll Cmd+C the draft and paste into the GitHub release editor manually, which means we lose the audit log AND the trust contract simultaneously.

**Frontend stance:** all citation failures surface as red pills in the editor. Publish is enabled, but a confirmation modal lists "3 entries lack corroborating signal — publish anyway?" The user can publish, but the audit log records `published_with_overrides: [...]`. This is the strongest trust posture that does not destroy the editing workflow.

(Anticipated compromise with architect + scribe: hard-block on red-pill entries for repos with `strict_trust: true` configured, otherwise nudge. Default = nudge.)

## User Experience Detail

**Onboarding** — 4 steps, ≤10 minutes: (1) GitHub App install (OAuth), (2) BYO-key paste with "test" button that runs a $0.001 ping, (3) redaction-pattern selection from a curated set (secrets, customer-names-from-codenames file, embargoed-features file) + a "skip for now" option, (4) trigger first draft on the most recent release.

**Error states** — every error gets a "what happened, what to do, who to ask" template. Examples:
- "GitHub returned 422 on release fetch" → "Your release range looks empty. Try generating from a different release, or use the manual PR list."
- "Anthropic returned 429" → "Rate limited by your vendor. Retry in 30s, or switch to OpenAI in settings."
- "Validator rejected 4 of 23 entries" → see red-pill flow above.

**Responsive behavior** — desktop-first (release managers work at desks), but the read-only "view this draft" mode works on mobile so a PM can sanity-check from their phone. No mobile editing in MVP.

**Accessibility** — WCAG 2.1 AA enforced via axe-core CI gate; keyboard-only user journey test (install → edit → publish without mouse) in the test matrix; all drag-affordances have keyboard equivalents; screen-reader labels on every column header and per-entry action.

## What I Disagree With

- **Architect's provider abstraction in v1.** Premature. Ship Anthropic-only; add OpenAI in sprint 4. The interface costs us editor polish time we can't afford to lose; 80% of MVP users will be on one provider regardless.
- **Architect's redaction-config-in-user-repo.** Too friction. MVP redaction patterns live in our DB, configured via the web editor's settings page, with a clear "export to repo" affordance for users who want them version-controlled later.
- **Scribe's audit log as feature-blocking.** Audit log MUST exist in MVP (agree it's a real requirement), but it MUST NOT be user-visible in v1 — it sits behind an admin export. Release managers don't want to see the audit log on every draft; they want to see the draft.

## Why This Wins

A great editor with a competent pipeline closes the loop in 30 seconds and earns weekly active usage. A great pipeline with a competent editor loses every demo to "the AI got it wrong and I couldn't fix it without rewriting." Win the editor first.
