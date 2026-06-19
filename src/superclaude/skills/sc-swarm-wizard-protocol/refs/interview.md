# Interview + goal→lens mapping (load in Wave 1–2)

Keep it short and human. Use `AskUserQuestion` (multiple choice) so a non-expert never has to free-type a
flag. Most users only need Q1–Q3; infer the rest and confirm in one sentence. Under `--yes`, ask only Q1
and Q2 and default the rest.

Golden rule: **lead with plain "I want to…" options, never raw lens IDs.** Translate the pick to a lens
silently. Explain *why* you're asking, not just what.

## Q1 — What do you want to do? (drives the lens)

`AskUserQuestion`, header "Goal", options (label → lens):

- "Find bugs / review my code for correctness" → `bare-review`  *(the solid, stable default)*
- "Find small safe cleanups I could apply" → `refactor-find`
- "Find edge cases / inputs that break my code" → `edge-case-hunt`
- "Check whether a spec/design is complete" → `spec-completeness`
- "Check whether an approach will actually work" → `feasibility-probe`
- "Figure out why something is failing (root cause)" → `troubleshoot-hypothesis`
- "Audit my docs for gaps or staleness" → `doc-completeness`
- (advanced only) "Something custom — my own prompt" → custom branch

If the user's free-text goal clearly matches one, skip the menu and confirm ("Sounds like a bug review —
I'll use the bare-review lens. Good?"). If two fit equally (e.g. "review and clean up"), ask which matters
more rather than guessing.

## Q2 — What should I look at? (target)

Ask for the file or path. Then verify: it exists and holds ≥50 non-whitespace bytes. If too small,
explain plainly ("swarm needs a bit more content to review — that file is nearly empty; point me at the
real source file?"). A single source file is the typical target.

## Q3 — Real models, or a safe practice run first?

`AskUserQuestion`, header "Run type":

- "Just show me it works first (free, instant, no setup)" → stub only
- "I want real model analysis" → real (still dry-runs first; needs the T2 proxy configured)

Always dry-run with stub regardless. If they pick real, verify the env contract now (names only) and, if
missing, offer to help set up `~/.aienv` or fall back to stub.

## Q4 (optional) — How many independent reviewers?

Only ask if they want to tune it. Explain the tradeoff: "More reviewers = broader coverage but slower."
Default = the lens default (3, or 4 for edge-case-hunt / troubleshoot-hypothesis). Range is 2–4.

## Q5 (optional) — Watch it live, or run in the background?

Only relevant for a real run that may take a while:

- "Watch a live dashboard" → `--tui` (only if on a real terminal; else explain it'll just print normally)
- "Run it in the background, tell me when it's done" → `--detached`

## Q6 (advanced only) — Custom prompt?

Only on `--advanced`. Warn: custom prompts need a small prompt directory and, if they use a `custom-py:`
recipe, that runs arbitrary code on their machine — only use prompts they trust. Most users never need this.

## Goal → settings mapping (the translation table)

| User picked | lens | transport (default) | reviewers | watch default | hands off to |
|---|---|---|---|---|---|
| bugs/correctness | `bare-review` | stub→openai_compat | 3 | tui (if TTY) | `/sc:adversarial` |
| cleanups | `refactor-find` | stub→openai_compat | 3 | tui | `/sc:code-review --apply` |
| edge cases | `edge-case-hunt` | stub→openai_compat | 4 | tui | `/sc:adversarial` |
| spec complete? | `spec-completeness` | stub→openai_compat | 3 | tui | `/sc:reflect` |
| approach work? | `feasibility-probe` | stub→openai_compat | 3 | tui | `/sc:research` |
| why failing? | `troubleshoot-hypothesis` | stub→openai_compat | 4 | tui | `/sc:troubleshoot` |
| docs audit | `doc-completeness` | stub→openai_compat | 3 | tui | `/sc:document` |

After mapping, restate the plan in one plain sentence and confirm before building:
"I'll run a 3-reviewer bug review on `src/auth.py`, starting with a free practice run. Sound right?"
