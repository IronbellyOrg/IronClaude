## ✅ Review remediation pushed (R1–R5 + HD-1)

The `/sc:auggie-review` findings have been remediated and pushed to `feat/rf-harness-sync` in two clean commits:

| Commit | Scope |
|--------|-------|
| `d2504c00` | `style(rf-agents)` — fix pre-existing markdownlint debt (59 MD040 fence languages + MD022/031/032 blank-line rules) in 5 rf-* agents. Separated so the remediation diff stays pure. |
| `dd669148` | `fix(rf-agents,task-builder,reflect-cli)` — the R1–R5 + HD-1 remediation (12 files). |

**Verification:** `pytest tests/cli/reflect/` → **81 passed, 1 xpassed, 0 failed** · `ruff format --check` clean · `make verify-sync` clean · `git grep` for the broken `mcp__tavily__tavily_(search|extract)` form → **0 matches** across all 8 agents.

This change was independently audited by `/sc:reflect --mode post` (Tier-1, deterministic-evidence): 100% tasklist completion, **0 regressions**, no Drift.

> ⚠️ **One item needs the maintainer (@RyanW): HD-1 is PENDING by design.** The remediation added an honest "not yet session-validated" disclosure but did **not** change the default POST-reflect mode (`--cli` stays default-OFF, O4 floors untouched). Whether to change that default is your design call — see `HD-1-default-mode-decision.md`. This is the correct terminal state, not a blocker.

---

<details>
<summary><b>📖 Plain-English summary of what each fix does (click to expand)</b></summary>

### R1 — Tavily tool-id revert  *(the merge-blocker)*
- **What:** Eight research agents reference their web-search tools by an exact machine name. A prior edit swapped one character — hyphen (`tavily-search`) → underscore (`tavily_search`).
- **Why:** The underscore spelling is registered to *nothing*, like dialing a phone number with one wrong digit. All 8 agents would have **silently** lost web search — no error, just degraded research.
- **How:** Strict find-and-replace back to the hyphen form (matching the known-good `deep-research.md`), proven by a search that returns **zero** of the broken form.

### R2a — Honest "not yet validated" disclosure  *(the second merge-blocker)*
- **What:** The `task-builder` docs called a chained-automation capability "confirmed." It isn't.
- **Why:** A docs file is trusted. "Confirmed" tells readers it was tested — but it had never run end-to-end, and we'd recorded a case where this exact chain quietly fell back to a fake stand-in. An overconfident claim is worse than an honest "not sure yet."
- **How:** Text-only — adds a disclosure at two spots and softens three "confirmed" claims to "expected … not yet validated"; points readers to the proven `--cli` path. No logic/defaults changed.

### R2b / HD-1 — The human-decision halt
- **What:** R2a raises a follow-up an automated worker may **not** answer: should the *default* change? Three options exist; instead of guessing, it wrote a labeled PENDING note and stopped.
- **Why:** Picking a shipped tool's default is a fork only the owner should take — guessing could silently ship a risky default. "Halt and ask" beats "auto-default."
- **How:** PENDING record with all three options; existing default left untouched; adjacent "depth floor" left alone.

### R3 — Test + document the inline directive
- **What:** The reflect runner appends a plain-English note telling the AI worker to run the job itself, not hand it off. The fix adds a code comment explaining it, plus an automatic test guarding it.
- **Why:** The note *looked* like the real guarantee but is only a polite request — the actual guarantee is a separate locked-door check ("EV-1"). And nothing stopped a future edit from deleting the note, which would silently shrink the review from several reviewers to one.
- **How:** A one-line comment (note for humans) + a 3-check test (an automatic tripwire that fails if the note is removed or duplicated). One older test was retightened to ban the real spawn-commands instead of the English word "subagent."

### R4 — Mode bifurcation table
- **What:** The final safety check runs in two modes (CLI vs skill) needing *different paperwork* across four dimensions. The fix adds a side-by-side cheat-sheet table + an explicit "which fields are required" rule.
- **Why:** The rules were scattered with no single comparison, so people (and tooling) kept filling the wrong form.
- **How:** A glance-once table + a validator rule (CLI ⇒ two fields present; skill ⇒ both absent; a mix is malformed), cross-referenced from the checklist. Documents existing behavior; no defaults changed.

### R5 — Reference fix + spec_path qualifier
- **What:** A cross-reference pointed to "§4.2," which doesn't exist; and a sentence read as always-true when it only applies in one mode.
- **Why:** A dangling reference is a footnote pointing to a missing page — it erodes trust in the whole doc. The over-absolute sentence is an "always turn left" sign at an intersection where you only turn left half the time.
- **How:** Renamed the reference to the note that actually exists (0 bare "§4.2" left); added a one-clause skill-vs-CLI qualifier. Low-severity clarity only.

</details>

<details>
<summary><b>🪤 Process note — the diff-scope footgun this surfaced</b></summary>

The remediation lived **only as uncommitted working-tree changes** in the worktree — so an audit pointed at `origin/master...feat/rf-harness-sync` would have shown the *pre-fix committed state* (still broken) plus unrelated commits, and falsely reported "R1 undone." The real change was `git diff HEAD`. This is now committed (resolving it), and the footgun is recorded so future audits of worktree work check `git diff HEAD` and resolve the tasklist path against the main checkout. *(This whole comment is now moot for future readers — the work is committed above.)*

</details>
