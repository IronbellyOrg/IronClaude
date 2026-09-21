# Phase 6 M3 consolidated findings (cycle 1)

VERDICT: FAIL

cycle: 1
|F_1| = 42

PASS_1: [template-conformance/(a-h1), template-conformance/(a-no-yaml), template-conformance/(a-tagged-fences), template-conformance/(a-x12), template-conformance/(b-step-numbering), template-conformance/(b-fence-close), template-conformance/(c-12-section), template-conformance/(c-will-blocks), template-conformance/(d-no-claude), internal-consistency/(c-contract_version-1.2.0), internal-consistency/(d-cap-rows-byte-identical), internal-consistency/(e-near-twin-SKILL:529), internal-consistency/(g-forbidden-names), completeness/(1), completeness/(2), completeness/(3), completeness/(4), completeness/(5), completeness/(6), completeness/(7), completeness/(8), completeness/(9), completeness/(10), hc-rename/(1-inventory), hc-rename/(2-H-guard), hc-rename/(3-both-dashes), hc-rename/(4-field-names), hc-rename/(5-NOT-PROVEN), hc-rename/(6-ADVISORY), hc-rename/(7-HC5-cells), hc-rename/(8-blocked-advisory), hc-rename/(9-No-x7), hc-rename/(10-filenames), hc-rename/(11-allowlist), hc-rename/(12-satisfy-HC1), hc-rename/(13-markdownlint), hc-rename/(14-no-fix-rewrite), hc-rename/(15-fence-parity), hc-rename/(16-MD024), hc-rename/(17-rename-coverage), domain-accuracy/(existing-test-pins), domain-accuracy/(tavily-pins), domain-accuracy/(eval-contains)]

**Sources:** 10 lens reports in `qa/exec-md/`. Completeness PASS (103/103 seams). 9 other lenses FAIL. Deduplicated; highest severity kept. Binding ledger (`### Phase Gate Findings`) honored: validator 3-value status, cosmetic nudge, restore-to-yes after re-opened, digits-stripped counter key, 8-pair budget are not defects.

**Scope:** in-scope = 19 markdown files + `.pre-commit-config.yaml` under `${WT}src/superclaude/` (and the two existing tests already landed). Out-of-scope logged below, not in |F_1|.

Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/`

---

## In-scope findings (apply in cycle 1)

| id | Sev | File:loc | Issue | Required fix | Lenses |
|---|---|---|---|---|---|
| M6-F01 | CRITICAL | SKILL.md:183 vs :185 | Step 1b forbids asking the user; step 2 still asks for a repro command. | Delete the ask. Drive repro only through OBSERVE-VIA; if no command write `no repro available: run-site unobservable` and continue. Never AskUserQuestion. | actionability F01, mustnot 1 |
| M6-F02 | CRITICAL | SKILL.md:64,:178,:259,:490,:591; HOC:5; DA | `blocked-on-authorization` keys on `re-run permitted: no` OR errored AskUserQuestion; no setter; AskUserQuestion not in allowed-tools. | Closed table: yes = authorized same-shell/remote already granted; no = explicit refuse; else unknown. Unknown → pending rows, never blocked-on-authorization. Delete AskUserQuestion from the story. | actionability F02, domain 7 |
| M6-F03 | CRITICAL | refs/hypothesis-card-template.md:97-100 | Discriminator 3-col table splits to 7 cols: unescaped `\|` in `<consistent\|refuted\|inconclusive>`. | Escape pipes in both A and B cells. | template 1 |
| M6-F04 | CRITICAL | refs/primitive-differential.md:26-34 | Spec IDs `R-01`, `R-15`, `R-04` leaked. | Name Wave 1 step 1b CONTROL-PROOF/OBSERVE-VIA; triage Substituted primitive row; shared diagnosability round counter. | evidence 1-3 |
| M6-F05 | CRITICAL | SKILL.md:259 | Cite Section 7 `"Hard-stop tasklist composition"` does not exist. Live: `### Section order (S1.6.4a)`. | Quote `Section order (S1.6.4a)`. | evidence 4, crossref 4 |
| M6-F06 | CRITICAL | refs/agent-assertions.md:3 | Cites `tests/troubleshoot/test_inline_fallback_parity.py` (does not exist yet). | Remove the path until Phase 7, or `<!-- evidence-absence -->`. | evidence 5 |
| M6-F07 | CRITICAL | SKILL.md:302; CAL:3 vs :60; rubric `all_six` | Spawn/description say 5-dimension; live rubric is six. | All sites: 6-dimension rubric. Grep `5-dimension` in 19 files = 0. | evidence 6-8, numbers 1, crossref 6, domain 14 |
| M6-F08 | CRITICAL | SKILL.md:61 vs :43/:259 | `diagnosability_hard_stop` mutually informative with `status: partial` only. Hard-stops also yield blocked. | Bind hard-stop to partial OR blocked per S1.6.4 precedence (failed retained). | consistency 3, numbers 11, crossref 5, domain 6, mustnot 3 |
| M6-F09 | CRITICAL | SKILL.md Wave 3 step 3.5 | Missing `card_path`, `rubric_path`, `flags_context` (Wave 1.7 names them). | Enumerate the full Wave 1.7 kwarg set at 3.5. | crossref 1 |
| M6-F10 | CRITICAL | SKILL.md Wave 5 2.5 vs 3 | 2.5 says pass null for absent producer/tasklist; step 3 always passes concrete paths. Same for Wave 1.7 `tasklist_path` when no file. | Pass null/omit when file does not exist so skip rules fire. | crossref 2-3 |
| M6-F11 | CRITICAL | command:69 vs Output Contract | On-return requires `verdict source` and `return_contract_path`; neither is a contract field. | Add `verdict_source` and `return_contract_path` to Output Contract (nullable) OR drop those on-return categories. Prefer add both fields. | crossref 7-8 |
| M6-F12 | CRITICAL | agent-assertions A2 vs RT Next Steps | Sentence `The report stays \`partial\` until <row>=<value>` missing (Grep 0). | Restore exact sentence as required Next Steps / A2 form. Extra measurement-row prose may remain as commentary. | domain 1 |
| M6-F13 | CRITICAL | agent-assertions A10 vs DA skeleton | A10 harness wants `## Emitter search` + `emitters-found: 0` + `already-read-files: 0`. Docs inverted to `usable-capture-routes: 0`. | Restore the three mechanical lines in the skeleton; usable-capture-routes may stay as extra. | domain 2 |
| M6-F14 | CRITICAL | agent-assertions A8 vs SKILL OBSERVE-VIA | A8 polarity: harness is artifact-file + missing job log; docs say artifact-file alone is not CI identity. | Put both forms in A8 trigger: OBSERVE-VIA artifact-file missing log AND CI-job identity missing marker. | domain 3 |
| M6-F15 | CRITICAL | SKILL.md:268; DA:333 vs reconcile gap-7c | Shipped: do not strip digits. Ledger/reconcile: digits stripped. | Restore "digits stripped" on the 3-round key in SKILL counter, DA patch-round, cap rows. | numbers 2 |
| M6-F16 | CRITICAL | SKILL.md:490 vs :588 | Fire after 5 consecutive vs "more than 5". | Will Not byte-match 3.5: after 5, re-fire 10, 15. Delete "more than 5". | numbers 3 |
| M6-F17 | CRITICAL | SKILL S1.6.0b | `surviving=yes\|no` has no partition algorithm. | Default grep hits `surviving=yes`. Set `no` only with cited taken exit file:line. | actionability F07 |
| M6-F18 | IMPORTANT | primitive-differential.md:26-28 | Section 2 list starts at `2.`. | Renumber 1/2/3. | template 3, hc-rename 1, evidence 17 |
| M6-F19 | IMPORTANT | primitive-differential.md:44,:56 | Unnumbered `## Constraints`; footer does not list sections. | `## Section 5: Constraints`; name S1–S5 in footer. | template 4-5 |
| M6-F20 | IMPORTANT | SKILL.md:248,:371,:490,:480 | New steps pack (1)(2)(3)/(a)(b) instead of 3-space sub-bullets. | Split into `   -` sub-bullets (house 1.3). | template 6-8,15 |
| M6-F21 | IMPORTANT | VAL:49 | Three kwargs in one Inputs bullet. | One bullet per path + skip rule. | template 10 |
| M6-F22 | IMPORTANT | SKILL / DA header keys | `discriminator-required=` vs `**:` vs `:`. | One wire form: tasklist `discriminator-required: yes\|no`; align SKILL audit/cap. | consistency 1 |
| M6-F23 | IMPORTANT | split-pending vs split_pending | Cluster mark hyphen; escalation_reason underscore. | Cluster/index keep `split-pending`; `escalation_reason` stays `split_pending`; add both to naming in SKILL once (alias sentence). Do not collapse cluster mark into underscore (Wave 3 already uses hyphen). Add `split-pending` as cluster verdict token in the skill text. | consistency 2, crossref 20 |
| M6-F24 | IMPORTANT | SKILL:471 vs :64/:445 | Hardening enum uses slashes vs pipes. | Pipe-separated five-token listing at :471. | consistency 6 |
| M6-F25 | IMPORTANT | HOC:25 vs schema | Changelog claims `execution_locus_card_path` at 1.2.0; schema table omits it. | Add schema row OR stop claiming HOC owns the field (field lives on SKILL contract — prefer stop claiming in HOC:25). | consistency 7, evidence 15 |
| M6-F26 | IMPORTANT | SKILL Refs table | Never names `refs/probe-packs/read-parse.md`. Agent-assertions header omits Wave 3. | Name read-parse in When-loaded cell; add Wave 3 to agent-assertions header. | consistency 8-9 |
| M6-F27 | IMPORTANT | SKILL:107,:259 | Skip `Waves 1.7-4` silently drops Wave 4.5. | State skip as Waves 1.7–4.5 (hardening does not run on diagnosability hard-stop). | consistency 10 |
| M6-F28 | IMPORTANT | HCT / CAL / PD / pack | Spec tags `[V2 merged]`, `v2.0 preview`, FR/NFR IDs, fake `D3/REPORT.md` cites, sysbox D3 comments. | Delete tags; rename v2.0 heading; replace FR/NFR with operational names in *new* text only if they were added this task — **do not strip pre-existing FR/NFR in HOC/PHC/EIP that tests pin**. Drop fake D3 paths in HCT:104. Strip D3/LF labels from read-parse comments. | evidence 10-14, domain 20 |
| M6-F29 | IMPORTANT | agent-assertions.md | Missing `## Calibrator` / `## Validator` H2s (D13). | Add two H2s; keep A-then-C table order as landed (reconcile X-3 A-then-C wins over D13 C-before-A). | hc-rename 2 |
| M6-F30 | IMPORTANT | SKILL S1.6.0b table vs consumers | No row-ID column; triage/Wave 3/HCT require row ID + file:line. | Add stable `id` column (`P1…Pn` grep-hit order). Bind S1.6.4 `<name>` to that id. | actionability F09-F10, crossref 14 |
| M6-F31 | IMPORTANT | SKILL:480 | `date -u -r` is BSD; this host is Linux. | Document GNU+BSD one-liners; missing mtime ⇒ drop that citation. | actionability F03, domain 19 |
| M6-F32 | IMPORTANT | primitive-differential mandatory table | Names `stat`/`access`/`true`/`-w` despite Constraints Must-NOT. | Generic property language in the mandatory table; tools only in optional packs. | actionability F05, mustnot 5 |
| M6-F33 | IMPORTANT | environment-deltas.md | Missing spec names user/permissions/working-dir/env-vars; has identity/config-source. How-to-check names `stat`. | Restore ten spec Delta names; aliases allowed. Property language, no `stat`. Skip row with `unknown — could-not-run` when gate forbids. | mustnot 6,14; actionability F06 |
| M6-F34 | IMPORTANT | HCT:34 | `environment-property:` always in fenced template (C7 false positive). | Remove from default fence; document as optional in Filling. | actionability F19, domain 13 |
| M6-F35 | IMPORTANT | HCT:33,:47,:115 | `runs-in=` unknown buried; `row <N>` not `row 1`; "seven" claim classes vs six. | Two example lines `runs-in=…` and `runs-in=unknown`. `behaviour-definition: row 1` in fence. "seven"→"six". | domain 11-12, numbers 7 |
| M6-F36 | IMPORTANT | CAL WebFetch / Write | Names WebFetch without the tool; instructs Write with `tools: Read`. | Rename WebFetch headings; state orchestrator Writes `output_path`. Pass `now_iso` for Timestamp. | domain 15-16, actionability F20 |
| M6-F37 | IMPORTANT | VAL Role vs blocked | Role still success/partial only. | Role `success \| partial \| blocked`. | domain 18 |
| M6-F38 | IMPORTANT | SKILL Wave 4 arity | ≥2 vs "2-3 competing". | Replace "2-3 competing" with "≥2 competing". | numbers 4 |
| M6-F39 | IMPORTANT | rubric:9 vs CAL:65 | Rubric 0.0–1.0 continuous vs triad 0.0/0.5/1.0. mixed row 2 cells vs 7-col header. | Rubric: score 0.0/0.5/1.0. Pad mixed row. | numbers 5-6, hc-rename 4 |
| M6-F40 | IMPORTANT | SKILL S1.6.4 / PD §2 | 2×2 has no step 1; SKILL never says when to run it. CONTROL-PROOF short `yes` vs `yes: file:line`. | Number §2 from 1. SKILL: if CONTROL-PROOF yes:file:line AND SAME-ENV≠yes, copy §2; else comparator=none. Every CONTROL-PROOF site uses `yes: <file:line>` / `no: <file:line>` / `unknown`. | actionability F17, mustnot 2,16 |
| M6-F41 | IMPORTANT | Wave 5 3.5 after publication | Cosmetic monitor numbered after REPORT write. | State as run-wide monitor from Wave 1; on threshold take (a) or (b) instead of another cosmetic Read; never a halt. Keep step 3.5 text but add "may fire in any wave; Wave 5 is the last check". | actionability F13 |
| M6-F42 | IMPORTANT | SKILL:359, command:103, RT:150, VAL:482, A1 backstop | Behaviour-definition bold+period; command says code-site not RUN-SITE; Grounding Gaps gated on partial only; validator crash forces partial; A1⇒blocked. | Em-dash on behaviour-definition; RUN-SITE; Grounding Gaps if status ≠ success; :482 does not assign status; A1⇒partial A8⇒blocked. | template 11, actionability F21, mustnot 4,7; crossref 19 |

---

## Out of scope (Follow-Up; do not fix here)

- Completeness #2: `refs/remediation-handoff.md` four-token enum (G-07 untouched-by-design).
- Completeness #1: da Loading discipline SUPERSEDED wording (P3-F06/F07) — keep replacement.
- hc-rename #3: dangling `OI-2/3-PENDING.md` in REV/CE — pre-existing at HEAD; do-not-touch contract-enumeration content beyond HC-rename.
- FR/NFR IDs in HOC/PHC/EIP that existing tests pin — do not strip.
- Harness `_assertions.py` FLAGS (Phase 7) — docs restored in F12–F14; do not author tests now.
- primitive-differential 38/3 attempt caps (numbers 10) — delete 38/3 if present; do not invent a second budget.
- Wave 0 STOP "ask the user" (mustnot 9 MINOR, pre-existing) — optional: refuse+list tokens; skip if it risks Wave 0 STOP tests.

## Fixer constraints

- Edit `${WT}src/superclaude/**` ONLY. Never `.claude/`. Then `make sync-dev && make verify-sync`.
- D11 keep-verbatim strings unchanged.
- Do-not-touch: SKILL Will-Do near-twin (`no hypothesis work happens in the same turn as an instrumentation patch`); escalation-rubric formula line; CAL `**Will Not:**`; both agents `tools:` frontmatter; H-token allow-list lines; remediation-handoff; contract-enumeration beyond rename; output-contract FIELD NAMES (adding new rows is allowed); `{blocked, advisory}` latch; docs/mistakes, docs/memory.
- Binding ledger wins over original item 2.17/2.26 strings.
- After edits: markdownlint on the 19 files (exit 0, no rewrite); HC guard 0 extra hits.
