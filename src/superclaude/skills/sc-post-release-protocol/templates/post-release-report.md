<!--
Template: post-release-report.md
Fill every section from real evidence. Gaps and red results are correct outcomes — report them, don't hide them (see refs/golden-rule-evidence.md).
Replace <bracketed> placeholders. Delete these comment blocks in the final file.
-->

# Post-Release Report — `<version>`

- **Version / tag:** `<version>` (`<tag>`)
- **Previous release:** `<prev_tag>` (or `none — first release`)
- **Run mode:** `<ground-up | additive>` — evidence: `<manifest path found, or "no prior manifest → ground-up">`
- **Install-surface class:** `<vm-e2e | local-deploy | package | no-install-surface>`
- **Date:** `<YYYY-MM-DD>`
- **Branch:** `<feature-branch>`

## Summary

<2–4 sentences: what shipped in this version's surface work, the headline coverage number, and the honest bottom line (e.g. "all user docs current; 1 install issue found and reported; no sysop surface").>

## Coverage matrix (headline)

| Capability | User doc (A) | Tech doc (B) | Install (C) | User guide (D) | Sysop guide (E) |
|---|---|---|---|---|---|
| `<capability>` | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌/n-a | ✅/⚠️/❌ | ✅/⚠️/❌/n-a |

<✅ present-and-current · ⚠️ present-but-stale (updated this run) · ❌ missing (created / gap) · n-a not applicable>

---

## Workstream A — User documentation

- **Scanned:** `<files/dirs>`
- **Updated:** `<files + one-line reason each>`
- **Gaps found:** `<capability → missing doc, with evidence>`
- **Created:** `<new files>`
- **Verification:** `<reflection/verification gate result / acceptance check>`

## Workstream B — Technical documentation

- **Scanned:** `<files/dirs>`
- **Stale claims reconciled:** `<[CODE-CONTRADICTED] → fix>`
- **Updated:** `<files>`
- **Gaps found:** `<missing ADR/runbook/reference, with evidence>`
- **Created:** `<new files>`
- **Verification:** `<result>`

## Workstream C — Install & deploy (e2e-validated)

- **Surface class:** `<class>` — evidence: `<what was found>`
- **E2E target:** `<VM coordinates (no secrets) / clean container / fresh venv / n-a>`
- **Result:** `<GREEN | RED | carried-forward | n-a>`
- **Transcript:** `<path to saved transcript (secrets scrubbed)>`
- **Updated/created scripts:** `<files + re-validation note>`

<!-- If RED: state exactly where it failed, the error, and the suspected cause. Do NOT mark C complete. -->
<!-- If carried-forward (additive): "install surface unchanged since <prev_tag>; prior green carried forward, not re-run." -->

### E2E transcript

```text
<paste the real transcript, or link the saved file. Secrets scrubbed.>
```

## Workstream D — User-facing e2e test guides

- **Feature surface scanned:** `<commands/entry points/flows>`
- **Guides created:** `<files>`
- **Coverage:** `<N of M user-facing capabilities have guides>`
- **Gaps / deferrals:** `<capability without a guide + why>`

## Workstream E — Sysop-facing e2e test guides

- **Sysop surface exists?** `<yes | no — how determined>`
- **Guides created:** `<files, or "none — no sysop surface found in <version>">`
- **Gaps / deferrals:** `<...>`

---

## Honest gap list (all workstreams)

| # | Workstream | Gap | Evidence | Proposed remedy |
|---|---|---|---|---|
| 1 | `<A–E>` | `<what's missing/broken>` | `<file:line / transcript>` | `<what to do>` |

## Artifacts

- Report: `<path>`
- Manifest: `<path>`
- Test guides: `<dir>`
- E2E transcript(s): `<path(s)>`

## Suggested next step

<Paste-ready commit/PR command, or "review the gap list before committing." Follow the skill's guardrails for THIS repo: feature branch off the auto-detected default branch; PR to the repo's own origin (resolve from `git remote -v`, never assume an owner/name); respect the host repo's own staging conventions for generated/vendored dirs; commit only when asked.>
