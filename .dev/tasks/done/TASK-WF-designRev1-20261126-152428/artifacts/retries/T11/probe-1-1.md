71634ad3a5afaadb3ff865d69c51db7ee3df2eb6
## Family first-failing-gate (review r1-1, findings F1.1 and F1.2)
defect form: a SKIP row names G3 where the task text names the permanent gate (G5 for aidev02, G6 for coder_orca's tag ruleset)
command: grep -n -F -e 'SKIP(G' -e 'First failing gate' -e 'first gate that fails' -- .dev/issues/837/gates.md
before:
  32:| Repo | Ruleset file | Decision | First failing gate | Also fails or notes | Evidence |
  34:| CPA-Manager-Plus | branch role: `protect-main-mirror.json` (fork of seakee/CPA-Manager-Plus, `ahead_by` 0 on 2026-11-26) | `SKIP(G3)` | G3 | G4
  35:| CPA-Manager-Plus | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 passes: producer search `CLEAR` | `.dev/issues/837/audit
  36:| IronOrca | branch role: `protect-main-mirror.json` (fork of stablyai/orca, `ahead_by` 0 on 2026-11-26) | `SKIP(G3)` | G3 | G4: no written accep
  37:| IronOrca | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 passes: producer search `CLEAR` | `.dev/issues/837/audit/IronOrc
  38:| IronOrca | `protect-aidev02.json` (not created) | `SKIP(G3)` | G3 | G5: no written yes for `aidev02`, so the file does not exist | `.dev/issues
  39:| coder_orca | `protect-main.json` (not a fork, full role) | `SKIP(G3)` | G3 | G4 passes | `.dev/issues/837/audit/coder_orca.md` (Blocks, line 77
  40:| coder_orca | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 also fails: release tooling in another IronbellyOrg repository
  60:| Clay accepts the installations check as not runnable with his token (or an organisation owner posts the output of `gh api --paginate orgs/Ironb
coupled sites: the opening paragraph that states the first-failing-gate rule (line 3), the rows for IronOrca protect-aidev02.json and coder_orca protect-release-tags.json, the clearance table row about the installations check
after:
  32:| Repo | Ruleset file | Decision | First failing gate | Also fails or notes | Evidence |
  34:| CPA-Manager-Plus | branch role: `protect-main-mirror.json` (fork of seakee/CPA-Manager-Plus, `ahead_by` 0 on 2026-11-26) | `SKIP(G3)` | G3 | G4
  35:| CPA-Manager-Plus | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 passes: producer search `CLEAR` | `.dev/issues/837/audit
  36:| IronOrca | branch role: `protect-main-mirror.json` (fork of stablyai/orca, `ahead_by` 0 on 2026-11-26) | `SKIP(G3)` | G3 | G4: no written accep
  37:| IronOrca | `.github/rulesets/protect-release-tags.json` | `SKIP(G3)` | G3 | G6 passes: producer search `CLEAR` | `.dev/issues/837/audit/IronOrc
  38:| IronOrca | `protect-aidev02.json` (not created) | `SKIP(G5)` | G5 | G3 also fails (installations read); no written yes for `aidev02`, so the fi
  39:| coder_orca | `protect-main.json` (not a fork, full role) | `SKIP(G3)` | G3 | G4 passes | `.dev/issues/837/audit/coder_orca.md` (Blocks, line 77
  40:| coder_orca | `.github/rulesets/protect-release-tags.json` | `SKIP(G6)` | G6 | G3 also fails (installations read); release tooling in another Ir
  60:| Clay accepts the installations check as not runnable with his token (or an organisation owner posts the output of `gh api --paginate orgs/Ironb
