# Anti-Omission Report 3 of 3

**Status:** Complete
**Date:** 2026-11-08

---

## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md` (1795 lines when read; line numbers below are lines of that file as read in this session)
**Input files checked:** `research/05-startup-boot-test-docs-and-decision-trail.md` (417 lines), `research/web-01-claude-code-user-skills-hooks-and-live-reload.md` (237 lines), `research/web-02-bmad-upstream-user-scope-and-new-project-install.md` (271 lines), `synthesis/synth-04-plan-questions-evidence.md` (473 lines). Total findings enumerated: see Summary (counted from the enumeration tables below).
**Date:** 2026-11-08
**Stop-and-re-scope branch:** Section 7 of the report (L1276-1349) states "Stop condition: not triggered" (L1325), and Section 8 (L1351) is an implementation plan, not a `RE-SCOPE PROPOSAL`. The normal rule applies: a pinned test or document counts as present only if it appears in Section 8.
**Method:** coverage judged by MEANING, never by ID. Candidate omissions were confirmed by searching the report for distinctive terms (zero hits) and then by re-reading the neighbouring report text for the same substance.

### Omissions Found

Severity key: CRITICAL = foundational finding or pinned test / document-to-change missing from Section 8; IMPORTANT = distinct secondary finding dropped (or a pinned test case absent from Table 5.1); MINOR = redundant or low-relevance detail. COVERED-BY-DEDUP rows are notes, not omissions.

| # | Source finding | Source file | Status (OMITTED or COVERED-BY-DEDUP) | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| OM-1 | Managed-settings source ranking and default `first-wins`: the highest-ranked source that delivers at least one policy key is used and the rest are ignored (order: remote settings, then MDM/OS policy, then the managed files `managed-settings.d/*.json` + `managed-settings.json` merged); `managedSourcesBehavior: "merge"` is the alternative. Consequence for D2 and for the `allowManagedHooksOnly` / `strictPluginOnlyCustomization` check: a drop-in under `/etc/claude-code/` can be ignored when a higher-ranked source delivers any policy key. Report W01-16/W01-17 (L848-855) carry only the within-files merge order and the remote-fetch condition; searches for `first-wins`, `highest-ranked`, `ignores the rest`, `managedSourcesBehavior` return no hits. | web-01 section 3.3 (lines 143) | OMITTED | n/a | IMPORTANT |
| OM-2 | Skill-frontmatter hooks: "Hooks that Claude Code registers when the skill is invoked and keeps running for the rest of the session", and project skill hooks register on invocation "including in a `-p` run in a folder you haven't trusted". This is a variant of B that is not held back by the workspace-trust rule. Report W01-18 (L856-859) says the trust hold-back "applies to project-level hooks too, so no hook-based option escapes it", and step 4D.4 (L1518) repeats the hold-back; the frontmatter-hook variant that the same source lists, which the source's own text says runs in untrusted `-p` folders, is nowhere in the report (a search for `frontmatter` finds only the unrelated stub frontmatter at L1496), so the report's absolute statement is stronger than the source supports. | web-01 section 3.1 (line 127) and section 4.1 (line 157) | OMITTED | n/a | IMPORTANT |
| OM-3 | Pinned test cases in `test-19-catalogue-cli-presence.sh` at lines 200, 743-746 and 820 (and 838): `first_token 'bmad --version'` is `bmad` (820); an echo-verb fixture regression named for bmad (743-746); welcome message must contain the declared invocation token and `help_command` by mechanical comparison (OQ-1). The report's Table 5.1 (L1568-1570) lists test-19 at 517-529, 1137-1152, 1175-1190, 545-561, 496-505, 1106-1114 only; lines 200, 743-746, 820 are absent, so two pinned cases (a first-token pin on the health command that any manifest edit must keep, and the echo-verb regression) are not in Section 8. | 05 (a-supplement) test-19 row (line 52) | OMITTED | n/a | IMPORTANT |
| OM-4 | The `test-49` scanned-surface list (`SPEC2_CHANGED_SURFACES`) also holds `test-startup-boot.sh` (confirmed by Grep of `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.github/contract-tests/test-49-spec2-evidence.sh:305`). Source says "Same list holds `startup.sh`, `Dockerfile.coder` and `test-startup-boot.sh`". The report names the other files (L339, L1571) but not `test-startup-boot.sh`, and plan step 5.5 (L1536) edits `test-startup-boot.sh` (optional ledger row), so the no-lifecycle-string rule of Table 5.1 row `test-49:310, 326, 355-399` must also cover that edit. Also 05 and 04 disagree about the list; the disagreement is not reported. | 05 (a-supplement) test-49 row (line 53) | OMITTED | n/a | IMPORTANT |
| OM-5 | If the plan introduces a new boot-record result word (example `CREATED-ON-FIRST-USE`), the `case` at `test-startup-boot.sh:234` must be extended and a projection assertion added next to line 1201; no option A-F needs it. | 05 row a1 (line 16) | OMITTED | n/a | MINOR |
| OM-6 | Fixture detail: the fresh-seed clean-tree check uses the public repo `https://github.com/octocat/Hello-World.git` (`test-startup-boot.sh:429, 433-435`), and the Orca status assertions run against a fake `orca_fake` transport (1100-1111). | 05 rows a8 and a3 (lines 18, 23) | OMITTED | n/a | MINOR |
| OM-7 | Update-box observation is narrower than the report states: `bmad --help` and `bmad --version` printed no "Update Available" box (inference: they exit before the async check completes); only `--list-tools` printed it under `NPM_CONFIG_OFFLINE=true`. Report CC-22 / C7 (L423, L716) states only the `--list-tools` case. | 05 d6 (line 185) | OMITTED | n/a | MINOR |
| OM-8 | `.memlog.md` and `SPEC.md` of both specs are SHA-256 snapshot-hashed in `.dev/reviews/local-snapshots-20261019/README.md:14-20`; whether any check compares those hashes to the live files is unverified. Report G-27 (L686) says only "snapshot hashes", with no file, path or consequence for the memlog/SPEC edits of Phase 1. | 05 c1 process note (line 155) and U12 (line 253) | OMITTED (weak mention only) | n/a | MINOR |
| OM-9 | Other specs use a different decision file (`spec-aidev02-v2/.decision-log.md`, entries like "## 2026-05-30 - CAP-8 placement resolved"); the `spec-orca-*` specs do not, so do not add a decision log there. Report L410 keeps only "IDs are per spec; `spec-aidev02-v2` uses CAP-8 for something else". | 05 open question 5 (line 293) | OMITTED | n/a | MINOR |
| OM-10 | CHANGELOG convention details: released dates are UTC; scope is the template tree, `catalogue/`, `scripts/`, `docs/`, `.github/` and `.dev/releases/`; dated entry variant `(2026-11-05, issue 450, capture only)` at line 288; a removal entry cites its spec path (line 232). Report L412 and step 2.6 (L1404) keep format, `[Unreleased]`, `### Added/Changed`, retag note. | 05 c2 (lines 162-165) | OMITTED | n/a | MINOR |
| OM-11 | Live slug directories under `/catalogue/`: claude-code, ironclaude, bmad, mcp-bundle-core, vibe-kanban, orca, test-slug (seven), including the `test-slug` fixture directory. | 05 d8 (line 187) | OMITTED | n/a | MINOR |
| OM-12 | markdownlint ignore list and rule detail: ignores also include `node_modules/`, `.*/**`, `**/.*/**`, `openspec/**`, `docs/generated/**`, `templates/VSCode-AIDev01/**`; MD026 punctuation limited to `.,;:`. Report L428 and step 2.7 (L1405) keep only the bmad-related ignores and MD013/MD024/MD033/MD034/MD041. | 05 (e) rows 6-7 (lines 207-208) | OMITTED | n/a | MINOR |
| OM-13 | `companions:` of the gap-closure SPEC also list the catalogue-bundle SPEC and glossary and the #205 PRD (report names only `fr-audit.md` and `owner-decisions.md`, L1384, L1387). | 05 c1 contract row (line 150) | OMITTED | n/a | MINOR |
| OM-14 | If the first-use project IS the recorded seed repo, the next boot takes the "already has BMad ... left untouched" branch (`install.sh:24-25`) and health reports `Configured` only when `_bmad/_config/manifest.yaml` exists; no test pins that sequence (`test-57:413-419` pins only a pre-existing bare `_bmad/`). Report step 7.9 (L1617) states only that a seed repo that already received BMAD at boot is "has BMad" for FIRST_USE(P). | 05 evidence for X6 (line 379) | OMITTED (half covered) | n/a | MINOR |
| OM-15 | Personal skills do not load in Cowork or cloud sessions; project skills do not load in cloud threads. | web-01 section 1.1 (line 21) | OMITTED | n/a | MINOR |
| OM-16 | A `` !`command` `` injected by a skill synced from a claude.ai account is not run locally; `allowed-tools` does not restrict which tools are available. | web-01 sections 1.5 and 5.2 (lines 49-50) | OMITTED | n/a | MINOR |
| OM-17 | PreToolUse decision semantics: `deny` blocks, `allow` skips the prompt (except actions no mode auto-approves), `ask` prompts, `updatedInput` replaces arguments, precedence deny > defer > ask > allow, deny and ask rules are still evaluated whatever the hook returns; UserPromptSubmit cannot replace the prompt (only add `additionalContext`) and blocks with `decision: "block"` plus exit 2. Report W01-9 (L817) says only that UserPromptSubmit and PreToolUse "can block". | web-01 section 2.2 (lines 83-87) | OMITTED | n/a | MINOR |
| OM-18 | SessionStart JSON output also accepts `initialUserMessage`, `watchPaths` (absolute paths watched for FileChanged events) and `sessionTitle`. | web-01 section 2.4 (line 100) | OMITTED | n/a | MINOR |
| OM-19 | Settings precedence for single-valued keys (managed, command line, project local, shared project, user); `managed-settings.d` ignores hidden files and files not ending in `.json`; file-based managed policy is "read at startup and reloaded when a file changes". | web-01 sections 3.2, 3.3 (lines 134, 140, 144) | OMITTED | n/a | MINOR |
| OM-20 | Advice for a user-facing first-use message (send it as context Claude is asked to relay, or via `systemMessage` if SessionStart supports it: unverified), and the alternative to frontmatter `allowed-tools` for a prompt-free install: a `permissions.allow` entry in user settings, with `disableSkillShellExecution` unset. Report W01-6 and step 4B.3 (L802, L1496) cover only `allowed-tools`. | web-01 sections 4.3 and 5.2 (lines 169, 186) | OMITTED | n/a | MINOR |
| OM-21 | Reading limits of the docs fetch: the skills page was read only to 100000 of 118986 characters and the hooks page (289837 characters) only in part (0-200000 plus a security slice). Negatives such as "no re-scan field found for UserPromptSubmit" rest on partial reads. Report L769 names only the small-model summary caveat. | web-01 method (lines 12, 17, 67) | OMITTED | n/a | MINOR |
| OM-22 | npm registry details: dist-tags `next` = `6.12.3-next.1` and `rollback` = `4.39.0`, `gitHead` values of 6.9.0 and 6.12.4, both bins `bmad` and `bmad-method` point at `tools/installer/bmad-cli.js`. | web-02 section 1 (lines 21, 38) | OMITTED | n/a | MINOR |
| OM-23 | 6.9.0 skills also contain 33 `uv run ` lines in 8 files next to the 41 `python3 ` lines in 31 files (a mixed set). Report W02-7 and G-06 (L903, L665) give the 6.12.4 `uv run` count and the 6.9.0 `python3` count only. | web-02 section 3 table (line 72) | OMITTED | n/a | MINOR |
| OM-24 | 6.11.0 release note (#2680): the 6.9.0-era interactive directory prompt "could install to a directory you never typed" (it returned the focused autocomplete option instead of the typed text). Relevant to a user who runs the interactive installer instead of the one-command form; our command always passes `--directory`. | web-02 section 5 (line 114) | OMITTED | n/a | MINOR |
| OM-25 | Further install-affecting release items not in W02-5/W02-6: 6.9.0 WSL rejects Windows Node, cleanup removes empty directories of retired skills, hermes-agent target; 6.10.0 `bmad-loop` opt-in module and Automator deprecation; 6.11.0 layered TOML configuration, `bmad-spec` and `bmad-deep-recon` moves, "Rendered skills require uv and Python 3.11+", AGY target; 6.12.0 `persistent_facts` ships empty (re-add `project-context.md` to the override); 6.12.1 #3019 (23 bmm skills load config through `resolve_config.py`); 6.12.2 CIS and TEA pinned to last v6 releases. | web-02 sections 4-5 (lines 85-93, 109-116) | OMITTED | n/a | MINOR |
| OM-26 | 6.9.0 install guide interactive flow and prerequisites: five first-time questions (directory, modules, "Ready to install (all stable)?", AI tools, per-module config); re-running where `_bmad/` exists shows a Quick Update / Modify Install menu; prerequisites Node 20.12+, Git (for cloning external modules), an AI tool; no `uv` requirement. | web-02 section 7.1 (lines 153-156) | OMITTED | n/a | MINOR |
| OM-27 | 6.9.0 guide: `--pin bmm=...` and `--next=bmm` are "silently ineffective against bundled modules" (core and bmm ship inside the installer package, so the bundled module version equals the installer version); `--set` routing rule (a key already in `config.user.toml` goes there, else `config.toml`; plus `_bmad/<module>/config.yaml`); the guide's default recipe (`--yes --modules bmm,bmb,cis --tools claude-code`); `non-interactive-installation.md` is only a redirect. | web-02 section 7.1 (lines 158-163) | OMITTED | n/a | MINOR |
| OM-28 | v7 main-branch page details: v6.12 requirements Node 20.12+, Python 3.10+, `uv`; marketplace route "Not v7-ready yet"; "Keep project and global installation scopes consistent"; v7 locations incl. `_bmad/custom/` retained across setup refreshes; no headless v7 install documented; `bmad status` verify step. | web-02 section 6 (lines 133-137) | OMITTED | n/a | MINOR |
| OM-29 | v7 side details: `setup_check.py` writes its note to stderr as an instruction to the agent (line 174), "the closest upstream analogue of option B and of a hook"; `~/.bmad/ingest-templates/` is user-level template content, not a runtime; upstream's generic advice "restart it or reload the window" (`skills-and-agents.md:218`); `references/setup.md:37,49` update commands and the "deleting a global path affects every project" warning. | web-02 section 8 items 3, 5, 7, 8 (lines 195, 197, 199-200) | OMITTED | n/a | MINOR |
| OM-30 | Upstream issue titles seen in search results: #2937 (closed `not_planned`), #2768 and #2736 (flat skills tree via `npx skills`), #2588 (HALT renderers on missing config keys), #2796 / #2802 (project root from working directory), #2597 (stop `find_project_root` walk-up at a repository boundary), #3149 (open, `_bmad/render/` not git-ignored); #2624 counts 101 call sites in 33 `SKILL.md` on main; #2677 reporter mix at 6.10.0 (34 `python3`, 15 `uv run`, 54 call sites without fallback). The report cites #1852, #2313, #2624, #2677, #3016 only (L1771); #2796/#2802/#2597 bear on owner question D-3 (which folder is the project). | web-02 section 9 (lines 216, 221, 223) | OMITTED | n/a | MINOR |
| OM-31 | The 6.9.0 package ships `bmad-generate-project-context`, not `bmad-project-context` (which exists from 6.11.0). | web-02 section 10 (line 236) | OMITTED | n/a | MINOR |
| DD-1 | Recommendation 4 of web-01 (a user-level artifact is visible in every project, so the stub/hook must test project type and `_bmad/`) | web-01 recommendations | COVERED-BY-DEDUP | Plan step 3.2 condition 5 (L1457) and Section 9 row 6 (L1696) | n/a (note) |
| DD-2 | Key Takeaways blocks of file 05 (parts a, a-supplement, b, c, d, e, f) restate table rows | 05 | COVERED-BY-DEDUP | Section 2.4 impact summary (L356-367), 2.5 (L383-440), Table 5.1 | n/a (note) |
| DD-3 | synth-04 trailing Self-Audit block (what was read, counts, plan elements that are the author's design, contradictions) | synth-04 lines 438-470 | COVERED-BY-DEDUP | The file header (line 7) says the assembler omits it; the design-choice marks are inline in the report (L1457 "a plan addition", L1460 "design choice of this plan", L1507 "Design choice of this plan", L1534 "name proposed") | n/a (note) |
| DD-4 | web-02 "Evidence index and limits" (fetched files kept under `/tmp/web02-*`, nothing run, search API returns only 10-12 items) | web-02 lines 267-271 | COVERED-BY-DEDUP | Section 5.2 intro (L872) and W02-17 (L949) | n/a (note) |


### Enumeration (per input file)

Counting convention: one row = one distinct finding (every test-case row, document-change row and web finding is its own row). Status values: REP = represented (substance present, regardless of wording); OMIT = see the Omissions table; DEDUP = merged into another item. "Loc" = report line(s) where the substance appears.

#### File 05: `research/05-startup-boot-test-docs-and-decision-trail.md`

Part (a): BMAD cases in `test-startup-boot.sh`

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-a0 | Anomaly: file has no case that runs `bmad install`, checks `_bmad/` or `_bmad-output/`, or calls the binary; it consumes boot records only | REP | L430, L353 |
| 05-a1 | PARITY enum includes `bmad`; result enum incl. `NOT_CONFIGURED` (231, 233-234) | REP (+OM-5) | L430, L1554 |
| 05-a2 | SPEC2 slug enum includes `bmad` (200-201) | REP | L430, L1552 |
| 05-a3 | Orca status assertion fixtures embed a bmad `Installed-not-Configured` row (1099, 1121-1137) | REP (+OM-6) | L1554 |
| 05-a4 | Projection of the blank-seed row to the exact line (1197-1201) | REP | L1554 |
| 05-a5 | Missing-record row pin (1217) | REP | L1554 |
| 05-a6 | Rejected-row error text `contract=bmad` (1282-1286) | REP | L1554 |
| 05-a7 | Out-of-profile bmad skipped in reprofile/readiness loops (502, 1223, 2482-2528); not pinned either way | REP (report corrects it: marker loop does not skip bmad) | L430, L1562 |
| 05-a8 | Fresh seed stays git-clean when bmad in profile (2089-2098) | REP (+OM-6) | L1556 |
| 05-a9 | Install marker present for in-profile bmad (2100-2127), runtime-network distinction | REP | L1557 |
| 05-a10 | Configure step timing: bmad + ironclaude sum at most 75 s (2129-2156); `timeout 120` in install.sh | REP | L1558, L1152 |
| 05-a11 | Health record: `Configured` with seed, `Installed-not-Configured` without (2160-2246); classifier reads only the seed repo (`spec2-health.sh:99-114`) | REP | L1559, L211 |
| 05-a12 | CLI presence only through the health record (`bmad --version`, manifest.yaml:24-25; install.sh:18 exit 2) | REP | L1570, L630 |
| 05-a13 | IronClaude CLAUDE.md fresh-home seed `cmp` (2082-2088); user-level writes must not touch CLAUDE.md | REP | L1555, L1178 |
| 05-a14 | No-seed behaviour of install.sh (21-23 nothing to configure, marker only 58-60; 24-26 existing BMAD untouched) | REP | L176-177 |
| 05-a15 | Key takeaway: only projection, clean seed, marker, timing, health and CLI presence are pinned | REP | L430 |
| 05-a16 | Key takeaway: option A and first-use action leave rows unchanged, but not B1/D1 delivery; B2/C/D2 and B3/D3 carry BREAKS-IF | REP | L356-367 |
| 05-a17 | Key takeaway: no case pins a deselected bmad marker | REP | L430, L1562 |
| 05-a18 | Key takeaway: a first-use bootstrap not through install.sh needs no change to this file; new case needed for cover | REP | L1544, L1528 |

Part (a-supplement): sibling tests

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-s1 | test-57 header lines 4, 10 ("bmad excluded, OD-1") | REP | L1543, L1537 |
| 05-s2 | test-57:323-324 seed manifest exists, clean seed | REP | L1547 |
| 05-s3 | test-57:413-427 guards (bare `_bmad/`, tracked skills) | REP | L1551, L329 |
| 05-s4 | test-57:431-444 non-Git seed, tracked-but-deleted skill | REP | L1551 |
| 05-s5 | test-57:449-452 "no seed: bmad writes nothing" oracle, with the corrected B/D delivery-vs-execution reading | REP | L320-331, L1544-1545 |
| 05-s6 | test-57:457-465 dirty seed configures; `_bmad-output/` user file kept | REP | L1551 |
| 05-s7 | test-46:835-847, 905-933 deselected bmad marker untouched | REP | L1564, L337 |
| 05-s8 | test-46:1092-1115, 1297, 1317, 1439-1446, 1480-1499 reader rejects bmad row; `bmad not-selected`; summary string | REP | L1565-1566 |
| 05-s9 | test-19:200, 743-746, 820, 838, 509-531 first token, echo-verb regression, welcome tokens | REP for 509-531 / 517-529; OMIT for 200, 743-746, 820 | L1568-1570; OM-3 |
| 05-s10 | test-49:310 manifest in scanned list; lifecycle regex at 326; same list holds startup.sh, Dockerfile.coder, test-startup-boot.sh | REP for the regex and most files; OMIT for test-startup-boot.sh | L339, L1571; OM-4 |
| 05-s11 | test-52:1382 profile table `orca: [claude-code, orca, ironclaude, bmad, mcp-bundle-core]` | REP | L1574 |
| 05-s12 | Key takeaway: the "writes nothing" oracle is test-57:449-452; first-use outside install.sh leaves it intact | REP | L1544 |
| 05-s13 | Key takeaway: deselected-marker oracle is test-46:905-933 plus startup.sh:1116-1117 | REP | L1564, L1438 |
| 05-s14 | Key takeaway: welcome_message edits constrained by test-19 tokens, renovate version line, test-49 strings | REP | L1403 |

Part (b): documents that state or imply the rule

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-b0 | Nuance: the bmad CLI IS global (`Dockerfile.coder:139-143`); wording must be "no global or user-level install of BMad framework content" | REP | L622, L711, L1015 |
| 05-b1.1 | owner-decisions.md:5 OD-1 row; add OD-4; pointer in OD-1 | REP | L391, L1384 |
| 05-b1.2 | .memlog.md:32 "never globally or at user level"; append new bullet; bump `updated:` | REP | L392, L1383 |
| 05-b1.3 | .memlog.md:33 seed behaviour unchanged for boot | REP | L394, L1698 |
| 05-b1.4 | .memlog.md:27 OD-1=A void history, stale | REP | L393, L712 |
| 05-b1.5 | .memlog.md:34 non-goal narrowed | REP | L394, L1383 |
| 05-b1.6 | SPEC.md:12 do not hand-edit; memlog first | REP | L395, L1379 |
| 05-b1.7 | SPEC.md:29 CAP-1 retired, new CAP-8 | REP | L395, L1385 |
| 05-b1.8 | SPEC.md:77 narrow the non-goal | REP | L395, L1385 |
| 05-b1.9 | SPEC.md:37 non-BMad installers 30 s bound; BMad outside the supervisor | REP | L1385, L184 |
| 05-b1.10 | fr-audit.md:12 FR-6 cancelled; stale `install.sh:38-66` | REP | L396, L1387 |
| 05-b1.11 | sprint-status-orca-gap-closure.yaml:23, 42 | REP | L437, L1387 |
| 05-b1.12 | 2-1-remove-deselected-markers.md:38, 101 | REP | L1387, L1427 |
| 05-b1.13 | 3-1-readiness-file.md:47, 85 | REP | L1387, L1427 |
| 05-b1.14 | epics-orca-gap-closure.md:14 | REP | L1387 |
| 05-b1.15 | ARCHITECTURE-SPINE.md:32 | REP | L1387 |
| 05-b2.1 | catalogue-bundle SPEC.md:65 no seed, welcome gives one-command path | REP | L397, L1386 |
| 05-b2.2 | SPEC.md:126 "User repos stay clean": needs first-use clean-tree rule | REP | L397, L1386, L1695 |
| 05-b2.3 | SPEC.md:141 worktrees carry only tracked files; narrow to Orca worktrees | REP | L397, L1386 |
| 05-b2.4 | SPEC.md:142 multiple repos / catalogue project arm unchanged | REP | L397, L1429 |
| 05-b2.5 | SPEC.md:166 `agile-full` profile does not exist; assumption | REP | L397, L714 |
| 05-b2.6 | SPEC.md:174 BMad in Orca worktrees open question | REP | L397, L1386 |
| 05-b2.7 | SPEC.md:139 BMad beyond 6.9.0 | REP | L1429 |
| 05-b2.8 | slug-configuration.md:48 no target, exit 0 | REP | L1430 |
| 05-b2.9 | slug-configuration.md:53 literal `{output_folder}/` re-tagged, keep `--output-folder` | REP | L398, L121 |
| 05-b2.10 | slug-configuration.md:54 "73 skill files" vs 75 | REP | L399, L722 |
| 05-b2.11 | slug-configuration.md:55 partial `_bmad/` ceiling inherited | REP | L1430, L1458 |
| 05-b2.12 | catalogue-bundle .memlog.md:20, 82, 95, 96 cross-reference | REP | L436, L1386 |
| 05-b2.13 | PRD addendum.md:75-76 Option A stale, Option B risks | REP | L400, L1388 |
| 05-b2.14 | PRD .memlog.md:13 stale | REP | L1431 |
| 05-b3.1 | manifest.yaml:12-14 welcome text; keep manual command; keep tokens and version line | REP | L402, L1403 |
| 05-b3.2 | manifest.yaml:7 "opt-in" unchanged | REP | L1436 |
| 05-b3.3 | install.sh:2-3 comment | REP | L1437 |
| 05-b3.4 | install.sh:23, 41 messages | REP | L1437 |
| 05-b3.5 | startup.sh:1114-1117 explicit owner-decision exception | REP | L402, L1438 |
| 05-b3.6 | startup.sh:1170-1176 original invocation | REP | L1438 |
| 05-b3.7 | startup.sh:673 sole writer of seed-repo-path | REP | L631, L1461 |
| 05-b3.8 | spec2-health.sh:77, 99-114 seed-only observation | REP | L211, L1439 |
| 05-b3.9 | README.md:241 Default-profile cell | REP | L1399-1400 |
| 05-b3.10 | README.md:308 `bmad-planning/` leave alone | REP | L1412, L1433 |
| 05-b3.11 | catalogue README.md:26, keep "Pair Orca" | REP | L1435 |
| 05-b3.12 | test-57:10 comment | REP | L1440, L1537 |
| 05-b3.13 | test-startup-boot:233, 1197-1198 | REP | L1441 |
| 05-b4.1 | docs/architecture.md:47 slugs only | REP | L1446 |
| 05-b4.2 | docs/component-inventory.md:24 | REP | L1446 |
| 05-b4.3 | docs/source-tree-analysis.md:25, 37 (root `_bmad/` unverified) | REP | L1446, L686 |
| 05-b4.4 | docs/index.md, project-overview.md | REP | L1446 |
| 05-b4.5 | docs/operations/upstream-monitor.md:61 | REP | L1446 |
| 05-b4.6 | docs/operations/aidev02-operator.md:1977; no per-project rule there | REP | L402, L1446 |
| 05-b4.7 | CHANGELOG.md:232 only bmad-matching line | REP | L402, L1442 |
| 05-b4.8 | SECURITY.md:138 gitleaks allowlist | REP | L1446 |
| 05-b4.9 | repo-root README.md no bmad hit | REP | L402, L1446 |
| 05-b5 | Key takeaways (4): binding trail; slug-configuration:53; "never globally" inaccurate for CLI; no change in operator guide/README/SECURITY/CHANGELOG | REP | L391, L398, L711, L402 |

Part (c): decision recording and CHANGELOG

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-c1.1 | Contract = SPEC + companions; SPEC derived from memlog | REP (+OM-13) | L408, L1384 |
| 05-c1.2 | Memlog front matter and typed bullets; append-style | REP | L409, L1383 |
| 05-c1.3 | Decision table `ID \| Decision \| Consequence`, bold verdicts | REP | L410, L1384 |
| 05-c1.4 | Numbering OD-1..OD-3 (next OD-4), CAP-1..CAP-7 (next CAP-8), IDs per spec; `.decision-log.md` of spec-aidev02-v2 | REP (+OM-9) | L410 |
| 05-c1.5 | Where a new entry goes (memlog, OD row, SPEC re-derive, cross-reference) | REP | L411, L1383-1386 |
| 05-c1.6 | Snapshot-hashed memlog/SPEC files, unverified check | REP weak (+OM-8) | L686 |
| 05-c1.7 | `.dev/issues/478/` accuracy-check row 6; only call site `install.sh:42` | REP | L413, L440 |
| 05-c2.1 | Keep a Changelog 1.1.0 + SemVer; UTC dates | REP (+OM-10) | L412 |
| 05-c2.2 | Scope of CHANGELOG | REP weak (+OM-10) | L412 |
| 05-c2.3 | `[Unreleased]` headings at 22, 58, 225, 285 | REP | L1404 |
| 05-c2.4 | Entry shape, contract-test naming, retag sentence, dated variant | REP (+OM-10) | L412, L1404 |
| 05-c2.5 | No BMad precedent in CHANGELOG | REP | L402, L1442 |
| 05-c2.6 | Fit: shipped change under Added/Changed; option A still earns a Changed line; issue 478 unverified | REP | L1404 |
| 05-c3 | Key takeaways (3): OD-4 + memlog + SPEC, CAP-8, never reuse; SPEC not hand-edited; CHANGELOG shape | REP | L1383-1385, L1404 |

Part (d): cross-validation of doc claims

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-d1 | CLI `bmad`, package `bmad-method`, version 6.9.0 verified | REP | L421 |
| 05-d2 | Pin 6.9.0 (manifest.yaml:2; install.sh:18; Dockerfile.coder:139) | REP | L421, L1443 |
| 05-d3 | Seed-case welcome claim verified by code; this workspace has no seed | REP | L425, L260 |
| 05-d4 | Manual command flags valid; `--directory .` accepted; works end to end unverified | REP | L422, L1048 |
| 05-d5 | `--output-folder` rationale, re-tagged | REP | L121, L398 |
| 05-d6 | `npm view` per invocation (`bmad-cli.js:17-35`); offline does not suppress banner for `--list-tools` | REP (+OM-7) | L164-165, L423 |
| 05-d7 | 73 vs 75 files hard-reference `{project-root}/_bmad` | REP | L399 |
| 05-d8 | Slug list verified (seven dirs) | REP (+OM-11) | L1446 |
| 05-d9 | Welcome rendered to `~/.aidev/status/welcome/<slug>.txt` (startup.sh:1189-1206) | REP | L424 |
| 05-d10 | bmad marker never removed on deselect | REP | L1438, L1564 |
| 05-d11 | Partial `_bmad/` left by a failed run is skipped by the guard | REP | L184, L519 |
| 05-d12 | Memlog bug claims (6 files, 41 files) not run | REP | L426, L133 |
| 05-d13 | Key takeaways (3): one-command text valid but unrun; install accepts a not-yet-existing target and `~`; offline claim to correct | REP | L422, L423 |

Part (e): README edit constraints

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-e1 | Line 241 verbatim, five cells | REP | L1399 |
| 05-e2 | Line 241 true per profiles.yaml / parameters.tf | REP | L402 |
| 05-e3 | What the reconciled text must state; paragraph below the table | REP | L1400 |
| 05-e4 | Line 308 leave alone | REP | L1412 |
| 05-e5 | Anchor line 100 `upstream GitHub CLI release v` (releases.json:113, verify_release.py:159-165) | REP | L428, L1413 |
| 05-e6 | markdownlint applies to README; ignore list | REP (+OM-12) | L428, L1405 |
| 05-e7 | Disabled/relaxed rules; table rules unverified version | REP (+OM-12) | L1405 |
| 05-e8 | markdownlint workflow triggers, runner, fix false | REP | L1405, L1597 |
| 05-e9 | Safe-edit rules for line 241 | REP | L1399 |
| 05-e10 | Build context invisible to workspace users; `/catalogue` visible | REP | L428, L1414 |
| 05-e11 | Retag effect: `image/catalogue/` edits retag; README does not | REP | L428, L1403 |
| 05-e12 | No README inside a slug dir (test-1-catalogue-shape:112-117) | REP | L1575 |
| 05-e13 | Key takeaways (3): line 241 plus optional paragraph; catalogue README "Pair Orca"; README must carry the command | REP | L1399-1400, L1435 |

Part (f): upstream-monitor

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-f1 | expected.txt header rule | REP | L1443 |
| 05-f2 | expected.txt:6 Dockerfile extraction | REP | L1443, L1584 |
| 05-f3 | expected.txt:7 install.sh extraction | REP | L1443 |
| 05-f4 | expected.txt:8 manifest.yaml `^version:`; welcome edit safe | REP | L1403, L1443 |
| 05-f5 | renovate-global.json5:44-50 Dockerfile manager | REP | L1444 |
| 05-f6 | renovate-global.json5:51-58 slug-copy manager; new version copy needs pattern + row | REP | L1443-1444 |
| 05-f7 | releases.json has no bmad entry | REP | L1445 |
| 05-f8 | Key takeaways (2): no edit if three sites keep shape; new version copy is the only trigger | REP | L1443, L1701 |

Gaps and Questions

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-U1..U3 | Option F/E effects on readiness wording, 75 s budget, CLAUDE.md edits unverified | REP (F void per G-25; E CLAUDE.md at L1148) | L1148, L684 |
| 05-U4 | "worktrees carry only tracked files" | REP | L686 |
| 05-U5 | "73 skill files" | REP | L399, L686 |
| 05-U6 | Literal `{output_folder}/` outcome | REP | L121, L673 |
| 05-U7 | Failed install leaves partial `_bmad/` | REP | L672 |
| 05-U8 | Manual command completes end to end | REP | L422, L675 |
| 05-U9 | Seed-repo runtime result | REP | L686 |
| 05-U10 | Memlog bug claims | REP | L673, L426 |
| 05-U11 | Offline banner cause | REP | L674, L716 |
| 05-U12 | Snapshot hash check | REP weak (+OM-8) | L686 |
| 05-U13 | Issue 478 as the GitHub number | REP | L413, L1404 |
| 05-U14 | markdownlint version / table rules | REP | L1405 |
| 05-U15 | Invisibility of non-copied `image/` files | REP | L428, L1400 |
| 05-U16 | Root-level `_bmad/` | REP | L686 |
| 05-U17 | Owner wording on git cleanliness | REP | L415, L1695 |
| 05-UF1 | U-F1-1..U-F1-6 (E/F write sites, matrix rows from 04, 48 hits, drop-in hooks/heredoc, tests not run, rows not re-derived) | REP (6 items) | L1148, L1736, L679 |
| 05-CF1 | C-F1-1 test-49 row wording; C-F1-2 Summary wording about C; C-F1-3 test-57:386 comment | REP (3 items) | L717-718 |
| 05-C1..C7 | CODE-CONTRADICTED list (six items, C5 withdrawn): never globally; memlog:27; fr-audit lines; agile-full; PRD Option A; offline claim | REP (6 items) | L711-716 |
| 05-OQ1..OQ4 | Open questions: boot unchanged; hide or visible; three extraction sites; deselected marker | REP (4 items) | L1698, L1695, L1701, L1697 |
| 05-OQ5 | Other specs use `.decision-log.md` | OMIT | OM-9 |
| 05-SD | Stale documentation list (five STALE DOC bullets + wording hazard) | REP (6 items) | L691-722, L391 |
| 05-SUM | Summary paragraph | REP | L356-367, L430 |

Fix-cycle-1 addendum (matrix)

| ID | Finding | Status | Loc |
|---|---|---|---|
| 05-F1.1a | Why 04 and 05 disagree: different questions (delivery by install.sh vs first-use execution) | REP | L536, L1270 |
| 05-F1.1b | B2, B3, D2, D3 never pass through install.sh, invisible to test-57 | REP | L360-364, L1270 |
| 05-F1.1c | C is not invisible to test-57 (install.sh:42 runs through the wrapper) | REP | L430, L537 |
| 05-F1.1d | `snap` definition and `mk_home` fixture | REP | L325, L1624 |
| 05-F1.1e | Definitions BREAKS / BREAKS-IF / WEAKENS / none; E and F column assumption | REP | L360, L1544 |
| 05-S1 | whole-HOME snap equality (B1, D1, E, F at boot break) | REP | L1544 |
| 05-S2 | second run byte-identical, no new `settings.json.bak.*` | REP | L1548, L1519 |
| 05-S3 | FR-21 proxy BUDGET_MS 30000 | REP | L1546 |
| 05-S4 | foreign Stop hook, Orca hook, `deniedMcpServers` survive; ironclaude fails if hook vanishes | REP | L1550, L1519 |
| 05-S5 | `ic_hooks` substring weakens test-57:187, 372, 376 | REP | L1549, L1516 |
| 05-S6 | CLAUDE.md byte-unchanged (test-57:171,188,338,349,363,381; startup-boot:2083-2087) | REP | L1555 |
| 05-S7 | seed git status clean / seed byte-unchanged (C through wrapper) | REP | L1547 |
| 05-S8 | seedless = Installed-not-Configured | REP | L1545, L1559 |
| 05-S9 | install.sh IMAGE_BAKED shape (test-19:192-220, 1137-1152) | REP | L1569 |
| 05-S10 | `bmad` executable file, `--version`/`--help` exit 0 (test-19:1175-1190, 545-561) | REP | L1570 |
| 05-S11 | no lifecycle strings on listed surfaces (test-49:326) | REP (+OM-4) | L1571 |
| 05-S12 | nine section markers (test-7) | REP | L1578, L1561 |
| 05-S13 | test-60 COPY and seed_if_absent lines, claude printf block | REP | L1580 |
| 05-S14 | test-67 COPY sources in image_input_files | REP | L1581 |
| 05-S15 | test-3 reserved words | REP | L1577 |
| 05-S16a | marker present after boot (startup-boot:2100-2108; install.sh set -euo) | REP | L1557 |
| 05-S16b | 75 s sum | REP | L1558 |
| 05-S16c | one agent / one aidev-startup row; lifecycle ready after run-on-start | REP | L1560-1561 |
| 05-S17 | test-73 copy_ok / tier_ok | REP | L1583 |
| 05-S18 | test-52:1374-1377 orca_retirement pin | REP | L1572 |
| 05-S19 | test-51:386-396 first `locals {` block | REP | L1579 |
| 05-S20 | test-1 slug_shape_ok three files | REP | L1575 |
| 05-S21 | certain breaks in group 1: only S1 | REP | L360, L1528 |
| 05-S22 | Rows not re-derived (test-46:929-933, 1804-1815, 1479-1499; startup-boot:1099-1137; test-52:1378-1384; whitelists) | REP | L1564-1567, L1552 |
| 05-X1 | first-use execution: test-57:450 none | REP | L367, L1528 |
| 05-X2 | other test-57 assertions (C BREAKS-IF) | REP | L1546-1548 |
| 05-X3 | `bmad --version`/`--help` non-interactive (C BREAKS-IF) | REP | L1570 |
| 05-X4 | any test-startup-boot case: none | REP | L430 |
| 05-X5 | any test-46 case: none | REP | L430 |
| 05-X6 | health/readiness records: none; first use in seed repo sequence | REP (+OM-14) | L211, L1617 |
| 05-X7 | Evidence for the "none" rows (Grep of test-57, run_slug, snap brackets) | REP | L367, L430 |
| 05-F1.4a | Reconciliation: "B and D break" true for B1/D1 only | REP | L536, L1270 |
| 05-F1.4b | "B and D leave every row unchanged" too strong for B2/C/D2 | REP | L356-367 |
| 05-F1.4c | Boot path unchanged only for B2, B3, C, D2, D3 | REP | L1698 |
| 05-F1.4d | Cheapest non-breaking delivery B3/D3, their S16c/S18/S19 conditions | REP | L1311, L1344 |
| 05-F1.5a | Open question: stub when no seed (B1/D1)? | REP | L1698 |
| 05-F1.5b | Owner preference for variants with no certain break | REP | L1698 |
| 05-F1.6 | Summary (3 sentences) | REP | L356-367 |

#### File web-01: `research/web-01-claude-code-user-skills-hooks-and-live-reload.md`

Report mapping: Section 5.1 (L773-868) carries W01-1..W01-19; also L632 (K-12), L660-663 (G-01..G-04), L964-967, L1094, L1133, L1331-1333.

| ID | Finding (source URL in the file) | Status | Loc |
|---|---|---|---|
| W1-m | Provenance: WebSearch/WebFetch, Tavily unavailable; WebFetch is a small-model summary; docs version caveat | REP (truncation: OM-21) | L769, L775 |
| W1-1.1 | Skill locations table: personal, project, enterprise, plugin (skills page) | REP (+OM-15) | L779 |
| W1-1.2 | Name collision: enterprise over personal over project; skill beats same-named command; stub must not reuse `bmad-*` | REP | L783 |
| W1-1.3 | Live pickup split: watched dirs live; new top-level skills dir needs `/reload-skills`; SKILL.md text only | REP | L787 |
| W1-1.4 | Subdirectory skills: parents to repo root at start; below-start dirs load on file read or `/add-dir` (v2.1.257) | REP | L791 |
| W1-1.5 | Bundled scripts, `${CLAUDE_SKILL_DIR}`, `` !`cmd` `` injection, `allowed-tools`, `disableSkillShellExecution` | REP (+OM-16) | L802 |
| W1-1.6 | Commands merged into skills; `~/.claude/commands/` row not on the skills page | REP | L795 |
| W1-1.7 | Docs do not forbid skills writing to the project; examples of skills that write | REP | L806 |
| W1-2.1 | Events and common input; `cwd` versus `CLAUDE_PROJECT_DIR`; `source` values; UserPromptSubmit `prompt` | REP | L813 |
| W1-2.2 | Output: stdout as context, stderr never seen, SessionStart no blocking; UserPromptSubmit and PreToolUse can block | REP (+OM-17) | L817 |
| W1-2.3 | Timeouts 600 s default, 30 s UserPromptSubmit, SessionStart background | REP | L821 |
| W1-2.4 | SessionStart `reloadSkills`; skill discovery runs before SessionStart finishes | REP (+OM-18) | L825 |
| W1-2.5 | Hooks run with full user permissions; can modify files | REP | L837 |
| W1-2.6 | `reloadSkills` version 2.1.152 from a user-authored issue; this workspace `claude --version` 2.1.319 | REP | L829, L775 |
| W1-3.1 | Hook scopes table; user-level hooks apply to all projects | REP (frontmatter-hook variant: OM-2) | L844 |
| W1-3.2 | Hook entries merge, identical handler runs once, parallel; list merge; precedence | REP (+OM-19) | L844 |
| W1-3.3 | Managed drop-in dir: alphabetical merge, hooks list-merged by inference; `allowManagedHooksOnly`, `strictPluginOnlyCustomization`; source ranking, first-wins, remote settings, `ANTHROPIC_BASE_URL` | REP for merge, keys, remote condition; OMIT for ranking / first-wins | L848-855; OM-1 |
| W1-4.1 | Workspace-trust hold-back of hooks in interactive sessions; skills not gated | REP | L856 |
| W1-4.2 | Hook/settings edits applied to a running session; project `.claude/` created mid-session loads | REP | L833 |
| W1-4.3 | What SessionStart output the user sees: unverified | REP (+OM-20) | L817, L868 |
| W1-5.1 | Default Bash behaviour: approval required except read-only; effect of `skipDangerousModePermissionPrompt` unverified | REP | L802, L868 |
| W1-5.2 | Skill `allowed-tools` and `!`command` injection; prompt-free install settings | REP (+OM-20) | L802 |
| W1-5.3 | Statement on modifying the project directory (consolidated) | REP | L806, L837 |
| W1-D1 | Discrepancy: none CODE-CONTRADICTED | REP | L868, L982 |
| W1-D2 | Q-1 of the gaps log answered by the skills page | REP | L868 |
| W1-D3 | "hooks run without Bash prompt" has no one-sentence source | REP | L837, L1704 |
| W1-K(a) | Answer (a): split answer on same-session pickup | REP | L660, L787 |
| W1-K(b) | Answer (b): user/project locations, commands, collisions | REP | L779-783, L795 |
| W1-K(c) | Answer (c): scripts, `!cmd`, permissions | REP | L802 |
| W1-K(d) | Answer (d): hook inputs, outputs, timeouts, user-level hooks all projects, trust hold-back | REP | L813-821, L856 |
| W1-K(e) | Answer (e): hook merge and managed drop-in | REP | L844-851 |
| W1-K(f) | Answer (f): no source forbids modifying the project | REP | L806, L837 |
| W1-K+1 | Hooks and settings are live; skills differ | REP | L833 |
| W1-K+2 | Skill listing adds context every turn | REP | L863 |
| W1-K+3 | Skills below start dir load on read | REP | L791 |
| W1-K+4 | Docs version caveat v2.1.314 / 2.1.319 | REP | L775 |
| W1-K+5 | Not answered by official sources (held-back timing, stdout display, `skipDangerousModePermissionPrompt`, PermissionRequest hook, Bash pattern grammar, reloadSkills version) | REP | L868 |
| W1-R1 | Shape D as SessionStart plus `reloadSkills`; not UserPromptSubmit | REP | L825, L1517 |
| W1-R2 | Plan for trust hold-back; open-risk list; stub as alternative; CI observation | REP | L1518, L1705 |
| W1-R3 | Name B stub outside `bmad-*`; `allowed-tools` only if owner accepts prompt-free; tell user `/reload-skills` | REP | L1496-1497 |
| W1-R4 | User-level artifact fires in every project: test project type and `_bmad/` | DEDUP (DD-1) | L1457, L1696 |
| W1-R5 | D2: check image's `/etc/claude-code/` for the two managed keys | REP | L852, L1705 |
| W1-R6 | Closing items for implementation (version in image, reloadSkills works, output shown, held-back hook) | REP | L1478-1488, L1705 |
| W1-R7 | Codebase is source of truth; external facts change ranking inputs for B and D | REP | L769, L1315 |
| W1-S | Summary: pages read; all of (a)-(f) answered; provenance | REP | L769-775 |

#### File web-02: `research/web-02-bmad-upstream-user-scope-and-new-project-install.md`

Report mapping: Section 5.2 (L870-956) carries W02-1..W02-18; also L621, L627, L664-669, L968-980, L1163, L1189-1202, L1303.

| ID | Finding (source in the file) | Status | Loc |
|---|---|---|---|
| W2-m | Method: untrusted data, nothing executed, Tavily unavailable, curl GET only, /tmp dirs | REP / DEDUP (DD-4) | L869-872 |
| W2-1.1 | `latest` 6.12.4; 6.9.0 published 2026-06-22; stable lines 6.10.0..6.12.4 with dates; Node >=20.12 | REP | L876 |
| W2-1.2 | dist-tags `next`, `rollback`, `gitHead`, bins | OMIT | OM-22 |
| W2-1.3 | Update banner is genuine | REP | L876, L165 |
| W2-2.1 | `global_target_dir` in one YAML file only (43/43/46 hits), no `.js` reader | REP | L880 |
| W2-2.2 | 6.12.4 header still says "User-home directory for global install" | REP | L880, L651 |
| W2-2.3 | Install options differ only by `--shims`/`--no-shims`; no scope flag | REP | L884 |
| W2-2.4 | "scope" means team vs user CONFIG keys (trap) | REP | L884, L887 |
| W2-2.5 | Other `os.homedir()` uses are caches and `~` expansion | REP | L884 |
| W2-2.6 | Answer (a): no; limits (11 other tarballs, -next, main) | REP | L883, L964 |
| W2-2.7 | Option F needs an upstream feature; a newer pin does not enable it | REP | L880, L1163 |
| W2-3.1 | 6.9.0 `python3 ` 41 in 31; `uv run ` 33 in 8; 6.12.4 0 and 105 in 39 | REP for python3 / 6.12.4; OMIT for 33-in-8 | L903; OM-23 |
| W2-3.2 | 6.12.4 skills call resolver via `uv run`; missing-config tolerance wording | REP | L903, L907 |
| W2-3.3 | Effect: bump removes the hook interaction at the cost of changed set and layout; trade-off not recommendation | REP | L903, L1703 |
| W2-4.1 | First-pass release notes: 6.9.0 hermes/CodeWhale/WSL/cleanup; 6.10.0; 6.11.0; 6.12.0..6.12.4 | REP partly (CodeWhale, Antigravity); rest OMIT | L895; OM-25 |
| W2-4.2 | No release note mentions user-level or `~/.claude` install | REP | L895 |
| W2-4.3 | `bmad-project-context` independent of install (6.11.0) | REP | L949 |
| W2-4.4 | 6.12.1 new checkout renders without user config | REP | L899, L953 |
| W2-4.5 | uv hard requirement from 6.11.0; v7 preview announced from 6.12.2 | REP | L899 |
| W2-5.1 | Verbatim notes: 6.12.4, 6.12.3, 6.12.2 (`--yes` without `--directory`) | REP partly | L899 |
| W2-5.2 | Verbatim notes: 6.12.1 (#3016, #3019), 6.12.0 (--shims, persistent_facts) | REP (#3016, --shims); #3019 and persistent_facts OMIT | L899; OM-25 |
| W2-5.3 | Verbatim 6.11.0 notes: project-context, core-only (#2680), directory prompt (#2680), `--set` ordering (#2671), uv (#2704), nonint pages, AGY | REP (#2671, core-only, uv); #2680 prompt, AGY, nonint pages OMIT | L899; OM-24, OM-25 |
| W2-5.4 | 6.10.0 and 6.9.0 notes (bmad-loop; CodeWhale; uv standard) | REP partly | L895, L899; OM-25 |
| W2-5.5 | Reading: release notes agree with tarball check | REP | L895 |
| W2-5.6 | Install-affecting changes (i) `--directory` default (ii) `--set` ordering (iii) config.user.toml correction (iv) uv warns | REP | L899, L982 |
| W2-5.7 | Only upstream "runs without install" statement is `bmad-project-context` | REP | L949 |
| W2-5.8 | Release notes confirm 6.9.0 `uv` advisory; custom skills should migrate to `uv run` | REP | L899 |
| W2-6.1 | Main-branch docs describe v7 preview; "does not apply to v6.12" | REP | L922 |
| W2-6.2 | v6.12 requirements (Python 3.10+, uv); v7 install commands; marketplace "Not v7-ready" | REP partly (OM-28) | L922, L930 |
| W2-6.3 | v7 locations; "Keep project and global installation scopes consistent"; no headless; install-on-demand discussion | OMIT detail | OM-28 |
| W2-6.4 | v7 pattern = skills first, project runtime second; alpha | REP | L929, L932 |
| W2-6.5 | Reader on the website gets v7; cite v6.9.0 tag | REP | L922 |
| W2-7.1a | 6.9.0 guide: `npx bmad-method install`, headless flags, `--tools` required | REP | L914 |
| W2-7.1b | Prerequisites and interactive five-question flow; Quick Update / Modify menu | OMIT | OM-26 |
| W2-7.1c | `--yes` defaults to quick-update on existing install | REP | L914, L129 |
| W2-7.1d | Flag reference table; no scope flag | REP | L914 |
| W2-7.1e | Default recipe line; `--set` post-install patch and routing | REP for post-install patch; OMIT for routing and recipe | L914; OM-27 |
| W2-7.1f | "What got installed": `_bmad/_config/manifest.yaml` records modules, versions, channel; bundled modules carry no sha | REP (manifest creation and its role are in the code-derived table; the sha detail is not needed for any plan step) | L92, L1458 |
| W2-7.1g | Rate limit 60/hour per IP per external module | REP | L914, L671 |
| W2-7.1h | Bundled modules; `--pin`/`--next` ineffective for them | OMIT | OM-27 |
| W2-7.1i | `non-interactive-installation.md` redirect | OMIT | OM-27 |
| W2-7.2 | What the guide does NOT say (empty dir, no `.git`, global, `~/.claude`, first-use) | REP | L914, L669 |
| W2-7.3 | Tutorial: "two folders"; `bmad-help` next; understates code | REP | L918 |
| W2-7.4 | Answer (b) and 6.9.0 `--yes` without `--directory` stops at a prompt (unverified) | REP | L899, L914 |
| W2-8.1 | v7 distribution via `npx skills add`, not by npm pin | REP | L930 |
| W2-8.2 | Skills CLI scopes: project default, `-g`, `-y`, `-a`, symlink/`--copy` | REP partly | L930 |
| W2-8.3 | v7 BMAD knows both scopes (setup.md:37, 49) | OMIT detail | OM-29 |
| W2-8.4 | Project runtime created by explicit setup; `uv` mandatory | REP | L930 |
| W2-8.5 | No automatic bootstrap in v7: offer-and-ask; stderr note analogue | REP (offer-and-ask); OMIT (stderr analogue) | L929; OM-29 |
| W2-8.6 | `{project-root}` = nearest folder containing `_bmad/` | REP | L929 |
| W2-8.7 | `~/.bmad/` user-level templates | OMIT | OM-29 |
| W2-8.8 | "Skills not appearing after install" advice | OMIT | OM-29 |
| W2-8.9 | Option F as defined does not exist in 6.x; v7 mechanism differences (i)-(v) | REP | L1163, L975 |
| W2-8.10 | A newer pin does not enable F; v7 would need owner reading of OD-1 | REP | L1163, L1168 |
| W2-8.11 | v7 pattern validates the shape of B and D but not full automation | REP | L932 |
| W2-9.1 | #2677 is our scenario; `resolve_config.py` does not degrade; plugin cache path | REP (+OM-30) | L933, L1200 |
| W2-9.2 | Maintainer answer: redesign, installer removed; no 6.x bootstrap | REP | L933 |
| W2-9.3 | #2624 trust concern; 101 call sites | REP (count OMIT) | L937; OM-30 |
| W2-9.4 | #1852 declined with workspace-folder workaround (variant of E) | REP | L941, L1148 |
| W2-9.5 | #2313 origin of `global_target_dir` | REP | L888 |
| W2-9.6 | #3016 incomplete first-use state HALT | REP | L953 |
| W2-9.7 | Plugin channel in 6.x tarballs (2 plugins at 6.8.0; 1 plugin in 6.12.4) | REP | L945, L1193 |
| W2-9.8 | Searches that found nothing (five PRs, 110 hits) | REP | L949 |
| W2-9.9 | Issue titles #2937, #2768, #2736, #2588, #2796, #2802, #2597, #3149 | OMIT | OM-30 |
| W2-9.10 | Answer (e): upstream knows the problem, no 6.x fix | REP | L933, L941 |
| W2-10.1 | `bmad-project-context` standalone; 6.9.0 has `bmad-generate-project-context` | REP / OMIT (name) | L949; OM-31 |
| W2-10.2 | `bmad-customize` script-missing continue | REP | L907 |
| W2-10.3 | Most skills treat failing resolver as non-blocking; `bmad-help` has no behaviour for absence | REP | L907 |
| W2-10.4 | No upstream document describes bootstrap on first use | REP | L949 |
| W2-10.5 | Answer (c) | REP | L949, L1012 |
| W2-K(a)..(e) | Key external findings (a) global_target_dir/no consumer; (b) documented flow; (c) no bootstrap; (d) versions; (e) upstream discussion | REP (5 items) | L876-949 |
| W2-K-s1 | Side finding: `uv run` vs `python3`; bump trade-off | REP | L903 |
| W2-K-s2 | Side finding: plugin marketplace route already in 6.x tarballs | REP | L945 |
| W2-R1 | Option F does not need a newer pin | REP | L1163 |
| W2-R2 | Option A is the per-project flow; cite v6.9.0 tag | REP | L922, L1048 |
| W2-R3 | Per-project first-use consistent with upstream; check `config.toml`; ask first or explicit; #2624 | REP | L937, L1702 |
| W2-R4 | Workspace-level install is a variant of E | REP | L941, L1148 |
| W2-R5 | If the pin is bumped: list of changes | REP | L980, L1703 |
| W2-R6 | Gaps narrowed (G-05, G-07, G-06, G-12, G-14; G-01..G-04 not answered here) | REP | L964-970 |
| W2-R7 | Discrepancy: tutorial lists two folders vs code | REP | L918 |
| W2-E | Evidence index and limits | DEDUP (DD-4) | L872 |
| W2-S | Summary | REP | L869 |

#### File synth-04: `synthesis/synth-04-plan-questions-evidence.md`

The report's Sections 8 (L1351-1683), 9 (L1685-1745) and 10 (L1746-1795) are the assembled form of this file; every row below was compared with the report text meaning by meaning (the report carries later fix-cycle changes: the `memlog.py` / `bmad-spec` route in Phase 1, the gate procedure table in Phase 4, cases (h) and (i) of step 5.3, the T78 step in 6.5, Section 9 row 19). Column n = number of distinct findings in the row group.

| ID | n | Findings | Status | Loc |
|---|---|---|---|---|
| S4-hdr | 1 | Reference keys, tag legend, no `bmad install` or test run, 6.10.0 tracked-tree rows not a basis | REP | L994-998, L1013 |
| S4-8.0 | 3 | Plan basis (Stage 0 + one owner-selected trigger; B3 / C / D3; not built E, F, B1, D1, B2, G, H, I); feasibility and branch; what is not decided | REP | L1353-1357 |
| S4-map | 10 | Gap-to-step map rows F-01..F-11 (F-10 and F-11 one row) | REP | L1361-1372 |
| S4-P1 | 8 | Steps 1.1-1.8 (memlog, OD-4, SPEC re-derive, cross-reference, companions, Option B risks, overridden positions R1..R16, owner gate) | REP (expanded with `memlog.py`) | L1383-1390 |
| S4-P2 | 7 | Steps 2.1-2.7 (README row, note below table, constraints, health unchanged, welcome wording, CHANGELOG, lint/monitor) | REP | L1399-1405 |
| S4-RC | 5 | README constraints 1-5 | REP | L1409-1415 |
| S4-reg | 27 | Document register rows (owner-decisions, memlog, SPEC, fr-audit, sprint-status, epics/SPINE, story files, catalogue-bundle memlog and SPEC, slug-configuration, PRD addendum, README 241/308/96-101, catalogue README, manifest, install.sh, startup.sh, spec2-health, test-57:10, test-startup-boot, CHANGELOG, expected.txt, renovate, releases.json, irrelevant docs, PROJECT_INDEX) | REP | L1419-1447 |
| S4-P3 | 6 | Steps 3.1-3.6 (command, FIRST_USE(P) incl. condition 5, broken install, git rule H/V, single block, prohibitions) | REP | L1454-1461 |
| S4-P3h | 1 | Phase 3 header: conditional on a built branch; CLI reading keeps it as specification | REP (expanded with memlog bullet types) | L1452 |
| S4-P4sel | 5 | Branch selection table (any/CLI; yes/skill; no/skill BLOCKED; yes/session; no/session) | REP | L1470-1476 |
| S4-P4g | 1 | Gate before any branch (claude behaviour must be observed) | REP (expanded to a procedure table) | L1478-1488 |
| S4-4B | 6 | Steps 4B.1-4B.6 | REP | L1494-1499 |
| S4-4C | 5 | Steps 4C.1-4C.5 | REP | L1505-1509 |
| S4-4D | 7 | Steps 4D.1-4D.7 | REP | L1515-1521 |
| S4-P5 | 6 | Steps 5.1-5.6 | REP (5.3 expanded with cases h, i) | L1532-1537 |
| S4-T51 | 43 | Table 5.1 rows (test-57 x9, test-startup-boot x12, test-46 x4, test-19 x3, test-49 x1, test-52 x3, and eleven single-test rows: test-1, -2, -3, -7, -51, -60, -67, -71, -73, -78, -22) | REP | L1543-1585 |
| S4-P5c | 1 | "Certain breaks under the branches of this plan: none"; only test-57:450 certain for B1/D1 | REP | L1528 |
| S4-P6 | 7 | Steps 6.1-6.7 | REP (6.3 and 6.5 corrected to named jobs) | L1594-1600 |
| S4-P7 | 10 | Steps 7.1-7.10 | REP | L1609-1618 |
| S4-v1 | 6 | (v)(1) snapshot table (Stage 0, 4B, 4C, 4D D3, 4D D2) + HOME-cache note | REP | L1624-1634 |
| S4-v2 | 4 | (v)(2) persistence table | REP | L1638-1643 |
| S4-v3 | 4 | (v)(3) overwrite table | REP | L1647-1652 |
| S4-chk | 28 | Integration Checklist items | REP (28 items in the report, several rewritten for the later fix cycles) | L1656-1683 |
| S4-9 | 18 | Section 9 rows 1-18 | REP (row 19 added) | L1691-1708 |
| S4-9.1 | 28 | Register: 27 open-gap rows (G-01..G-30 less G-22, G-24, G-25) and the "resolved by fix" line | REP | L1715-1745 |
| S4-10 | 14 | Section 10 evidence trail: 5 codebase files with agent types, "also read" files, 2 web files, source URLs, 4 synthesis files, gaps log counts | REP | L1752-1784 |
| S4-sa1 | 1 | Self-audit: what was read / what was not read | DEDUP (DD-3) | n/a |
| S4-sa2 | 1 | Key-findings trace table (R01..R05, W01/W02, gaps log, S03) | DEDUP (DD-3) | L1752-1784 |
| S4-sa3 | 1 | Excluded or reduced with rationale (E, F, G, H, I; Ponytail half; T1-T55) | REP | L1302, L1447, L1353 |
| S4-sa4 | 1 | Plan elements that are the author's design (condition 5, Variant H, single block, helper, test-80 name, no pre-approval, no removal) | REP (inline marks) | L1457, L1459, L1460, L1507, L1534, L1496, L1498 |
| S4-sa5 | 1 | Doc-only facts and plan steps: no step rests unconditionally on a doc-only claim | REP | L996, L1478, L1705 |
| S4-sa6 | 1 | Why nothing was dropped (shape of the three sections) | DEDUP (DD-3) | n/a |
| S4-sa7 | 1 | Contradictions found: R04 vs R05 on B/D; E/F tag disagreement; G-30; R03 "both" corrections; research-notes not read | REP | L1270, L1269, L1743, L708 |

### Self-Audit

**Prompt source.** The caller said the embedded prompt is on line 453 of the task file. Line 453 holds the orchestrator's consolidation step (`qa-anti-omission-consolidated-findings.md`) and has no BEGIN/END AGENT PROMPT markers. A Grep for "anti-omission agent 3 of 3" found the real agent-3 item on line 451 with the same assigned files, the same output path and the same markers. I used that prompt (read with Read, offset 451, limit 1) and ignored the text outside the markers. The orchestrator should correct the line number in its brief.

**What I read, in full, in this session.**
- `research/05-startup-boot-test-docs-and-decision-trail.md` lines 1-417 (one Read, no truncation).
- `research/web-01-claude-code-user-skills-hooks-and-live-reload.md` lines 1-237 (one Read).
- `research/web-02-bmad-upstream-user-scope-and-new-project-install.md` lines 1-271 (one Read).
- `synthesis/synth-04-plan-questions-evidence.md` lines 1-473 (two Reads: 1-240, 240-473).
- The final report `RESEARCH-REPORT-bmad-first-use.md` lines 1-1795 in eight Reads (1-300, 300-530, 530-790, 790-990, 990-1150, 1150-1329, 1329-1559, 1559-1795). I read Section 7 first-hand (L1276-1349) before judging Section 8: it states "Stop condition: not triggered", and Section 8 is a plan, so the normal rule for pinned tests and documents applied.

**Searches run on the report (to confirm absence, not to test coverage by ID).** Three alternation Greps over the report with the distinctive terms of every candidate omission (for example `first-wins`, `highest-ranked`, `frontmatter`, `watchPaths`, `initialUserMessage`, `updatedInput`, `Cowork`, `claude.ai`, `rollback`, `gitHead`, `#2680`, `Python 3.10`, `silently ineffective`, `ingest`, `octocat`, `orca_fake`, `CREATED-ON-FIRST-USE`, `decision-log`, `local-snapshots`, `test-slug`, `Modify Install`, `generate-project-context`, `#2937`, `#2597`, `#2796`, `#3149`, `WSL`, `persistent_facts`, `#3019`). Terms with zero hits became OM rows only after I re-read the neighbouring report text and found no equivalent wording. One source check outside the report: Grep of `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.github/contract-tests/test-49-spec2-evidence.sh` confirmed `test-startup-boot.sh` is listed at line 305 of `SPEC2_CHANGED_SURFACES` (OM-4).

**Why I believe the counts are right.**
- synth-04 produced no omission. I compared it row by row with report Sections 8, 9 and 10: all 8 Phase 1 steps, 7 Phase 2 steps, the 27-row document register, 6 Phase 3 steps, the 5-row branch table, 4B/4C/4D steps, 6 Phase 5 steps and the 43 Table 5.1 rows, 7 Phase 6 steps, 10 Phase 7 steps, the three persistence tables, 28 checklist items, 18 open-question rows (plus a new row 19), 27 register rows and Section 10 are present. The report is a superset of synth-04 (fix cycles added `memlog.py`/`bmad-spec`, the gate procedure, cases (h) and (i), the T78 step). The synth-04 Self-Audit block is excluded by design (`synth-04:7`, "the assembler omits it") and its substantive marks are inline in the report (DD-3).
- file 05: every test-startup-boot case (a1-a13), every sibling-test row except the test-19 and test-49 details, every document row of parts (b)-(f), all U/C/OQ items and the F1 matrix rows S1-S20 and X1-X6 have a counterpart in Sections 2.4, 2.5, 3.2, 4.2, 4.3, 5, 8 or 9. The omissions are low-weight details (OM-5 to OM-14) plus the two IMPORTANT pinned-test items (OM-3, OM-4).
- web-01 and web-02: all 19 + 18 findings of report Section 5 map to the sources; the omissions are secondary details and four findings that carry decision weight (OM-1, OM-2 for web-01 and, at MINOR, OM-24 and OM-30 for web-02).
- CRITICAL count is 0 because no foundational finding is missing and every pinned test of file 05 that the plan can break is in Table 5.1 (L1543-1585); the two pinned items that are missing (test-19:200/743-746/820; test-49's scan of `test-startup-boot.sh`) are rated IMPORTANT because the plan does not edit what they pin except step 5.5, and recovery is a one-row addition.
- IMPORTANT is used four times: OM-1 (managed-settings ranking decides whether D2 and the managed-key check can work at all), OM-2 (a source finding that qualifies an absolute report statement), OM-3 and OM-4 (pinned test cases absent from Table 5.1).

**What I did not observe (UNVERIFIED).**
- I did not re-read `test-19-catalogue-cli-presence.sh` lines 200, 743-746, 820 or 838; OM-3 relies on file 05's description of them.
- I did not fetch any Claude Code or BMAD web page; OM-1, OM-2 and the web-02 items rest on what web-01 and web-02 state, not on the pages.
- Line numbers in the "Loc" columns are the lines of the report as read in this session; several cite a range or a table start rather than the exact row. If the report is edited, they shift.
- Counts of enumerated findings treat each table row as one finding and each "key takeaways" row as the number of bullets it holds (see the Summary); a different grouping would change the total but not the omission list.

### Summary

- Findings enumerated: **630** (file 05: 231; web-01: 45; web-02: 86; synth-04: 268), counted as stated above.
- Represented: **603** (of which 27 lose one minor detail, listed as OM rows).
- Covered by dedup: **6** (W1-R4, W2-m, W2-E, S4-sa1, S4-sa2, S4-sa6); the four DD notes in the Omissions table name the report items.
- Omitted (wholly or partly): **21** enumerated findings, which hold **31** distinct omitted items in the Omissions table (OM-1 to OM-31).
- Omission severity: CRITICAL **0**, IMPORTANT **4** (OM-1, OM-2, OM-3, OM-4), MINOR **27** (OM-5 to OM-31).
- Blocking omissions (CRITICAL or IMPORTANT): **4**.

Recovery targets for the IMPORTANT items: OM-1 and OM-2 to Section 5.1 (add to W01-16/W01-17 and W01-18) and to Section 9 row 15; OM-3 to Table 5.1 (add test-19:200, 743-746, 820 as KEEP rows); OM-4 to Table 5.1 row `test-49:310, 326, 355-399` and step 5.5.

Verdict: FAIL (4 blocking omissions)

