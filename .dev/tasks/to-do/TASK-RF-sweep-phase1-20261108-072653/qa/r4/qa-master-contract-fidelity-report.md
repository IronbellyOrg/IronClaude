# QA Report: master-contract fidelity lens (R4 gate)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` (1041 lines at review time; 1013 at build time), steps 1.17 to 1.19
**Date:** 2026-11-08
**Phase:** report-validation (domain lens, research/09 Gap 5)
**Fix authorization:** false. Only this report was written.
**Base checked:** HEAD `5dc29d23`. Contract and test file are unmodified (`WC-16` and `/sc:sweep` appear 0 times in either; `sweep.md` does not exist yet).

## Method

I predicted from DESIGN section 8 and step table 15.2 what steps 1.17 (WC-16 paragraph), 1.18 (contract line 23) and 1.19 (five test edits) will do. I then read each master test that touches the contract in `tests/skills/test_worker_contract.py`, in chunks of at most 150 lines, and checked whether the predicted end state or any intermediate state fails it. `uv run pytest` was not run, because the changes do not exist yet. The `_check_repo_setup_gated` regex was replayed with `grep -oP` over the DESIGN text that will become contract lines.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | `_check_rule` for the new `"WC-16"` entry: all four phrases occur verbatim in the final text (design 675-677; `grep -cF` gave 1 for each) and the ident `WC-16` shares a line with phrase 0 (the heading) | PASS |
| C2 | Dict-key collision: `"WC-14"` already exists at test :156-164 (worker rule). The design uses key `"WC-16"` and inserts after :172, before `"heartbeats"` :173, so no key is overwritten | PASS |
| C3 | `test_rule_check_fails_when_rule_removed[WC-16]` and `[never-as-worker]` (test :1044-1051) still fail the rule when phrases are removed | PASS |
| C4 | End state of `RULE_PHRASES["never-as-worker"]` (:86-92): the edited phrase equals new contract line 23 (design 701 contains the full concatenated phrase, `grep -cF` = 1) | PASS |
| C5 | Intermediate state after step 1.18 and before step 1.19: `test_contract_states_rule[never-as-worker]` | FAIL (finding F1) |
| C6 | `_check_never_as_worker` (:765-771) and `test_never_as_worker_check_fails_when_command_removed` (:1081-1090) with `/sc:sweep` appended as the 9th entry | PASS |
| C7 | `_check_repo_setup_gated` (:813-828, regex :798-803): replayed over design 677 (WC-16 paragraph) and 701 (line 23): 0 code-span hits, 0 setup flags | PASS |
| C8 | `_check_no_unattended_sections` (:831-839): `sweep.md` has no `## Unattended mode`, so the equality holds with no edit | PASS |
| C9 | `_check_p2_set` (:1556-1566, 31 entries) and `_check_p1_set` (:1355-1362): `sweep` is not added to `UNATTENDED_EXPECT`. `NOT_CONVERTED_IN_P1` (:1335) is checked per name (:1481), never compared to `NEVER_AS_WORKER` | PASS |
| C10 | Write-verb audit (`AUDIT_ROOTS` :1940-1944, `WRITE_VERB_RE` :1948-1951): the contract is outside the roots, and design 7.6 sweep.md and SKILL text carries no `git add/commit/push/merge/stash/update-ref/worktree`, `gh pr` or `gh api` | PASS (see F4) |
| C11 | Liveness pins `liveness-sweep-and-states` (:209-219), `liveness-ladder-and-restart` (:228-237), `liveness-wait`, `wc10-*`, `wc6-live-attempt-settlement`: WC-16 inserts at 274 and rewords nothing at contract :110 or :151. Its cadence clause only quotes "The sweep." | PASS |
| C12 | Slicing tests: `_TEMPLATE_HEADING` splits (:774-777, :1094, :1106) sit after the insertion. The `- **WC-4.` to `\n- **WC-8.` slice (:1237) is untouched. `_p2_bullet` (:941-944) needs lines starting `- From P2 `. `_check_nested_result_rule` (:958-969) needs the `- **Nested propagation rule**` line. WC-16 adds none of these. No test counts WC rules or heading order | PASS |
| C13 | Every contract and test line cited in design section 8 re-read at HEAD: contract :23, :110, :151, :273, :275; test :25, :86-92 (phrase :89), :165-172, :173, :209-219, :228-237, :382-391, :755-762, :765, :831-839, :837, :912, :1081-1082, :1318/:1322, :1556, :1940-1944, :1953-1955, :1966, :2016 | PASS |
| C14 | Other readers of the contract or the list: `grep` over `tests/` finds `WORKER-CONTRACT`/never-as-worker only in `test_worker_contract.py`. `src/superclaude/cli/install_core.py:27` only lists the file name. No second tracked copy of the contract. The developer-guide copy of the list (R7) is not read by any test | PASS |
| C15 | The rename of `test_never_as_worker_list_names_all_seven_commands`: no reference to the old name outside the test and the DESIGN (tracked files) | PASS |
| C16 | Literal accuracy of the pin-edit instruction at design 688 | PASS with MINOR F2 |

## Findings

### F1 (MAJOR): step 1.18 turns `test_contract_states_rule[never-as-worker]` red, and the fix sits in step 1.19

- Evidence: `docs/designs/orchestrator-mode.md:944` (step 1.18 edits only contract line 23, gate 1.17) and `:945` (step 1.19 carries the pins). The phrase pin that must change is the fifth pin edit at `:688`, listed under 1.19 only. The pin lives at `tests/skills/test_worker_contract.py:86-92` (phrase :89-90), and `_check_rule` (:755-758) asserts the phrase is a substring of the contract. After 1.18 the contract line reads `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, `` (design `:701`), so the old substring `` `/sc:spawn` and `/sc:swarm-wizard`, `` is gone.
- What breaks: `test_contract_states_rule[never-as-worker]` (:907-909) fails from the moment step 1.18 lands until step 1.19 edits :89. The step table gives 1.18 no test-free exemption, and a per-step QA of 1.18 that runs the contract test file will fail. Step 1.19 then gates on a red 1.18.
- The end state is green (C4). The defect is the step split, not the final text.
- Smallest fix: move the `RULE_PHRASES["never-as-worker"]` phrase edit (fifth pin, design `:688`) into the 1.18 row, so the contract line and its pin change in one step. Or state in the 1.18 row that its test check is deferred to 1.19.

### F2 (MINOR): the quoted "from" string in the phrase edit does not exist in the source

- Evidence: `docs/designs/orchestrator-mode.md:688` quotes the old text as `` "`/sc:spawn` and `/sc:swarm-wizard`, " `` with surrounding double quotes. Test line :89 is `"`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "`, so `"`/sc:spawn` ...` with a leading quote matches nothing literally. An exact-string Edit with the quotes fails.
- Fix: drop the quote marks around the fragment, or quote the whole :89 string.

### F3 (MINOR): `/sc:sweep` is inserted before `/sc:swarm-wizard`, which breaks the alphabetical order of line 23

- Evidence: `src/superclaude/core/WORKER-CONTRACT.md:23` lists agent, git, help, issue, pm, spawn, swarm-wizard in order. `swarm` sorts before `sweep`. Design `:701` puts sweep first. No test checks order (`_check_never_as_worker` :765-771 only tests membership), but the pin phrase at :89 is order-sensitive, so any later reorder must change line 23, the pin and R7 together.
- Fix: optional. Keep the order and say so, or order the three places the same way.

### F4 (MINOR): no step owns a `WRITE_VERB_CLASSIFICATION` row if sweep text gains a write verb

- Evidence: design `:694` says a row is needed for any write-verb text in `sweep.md` or `sc-sweep-protocol/`, and `:945` lists no row edit among the 1.19 pins. The audit (:1981-2012, `test_every_write_verb_hit_is_classified` :3129) scans `src/superclaude/{skills,commands,agents}` recursively. Design 7.6 (`:651-662`) prescribes no such verb, so I predict zero hits. Only step 1.27 would catch a later addition.
- Fix: add "or classified in 1.14/1.15 if a hit appears" to the 1.14 and 1.15 rows.

### F5 (MINOR): the new `RULE_PHRASES` entry is one 141-character line

- Evidence: design `:684`. `ruff format --check` (step 1.26) will want it wrapped. Not a test failure; step 1.26 catches it.

### F6 (MINOR): the `"sweep"` assertion goes into a test named for `load`

- Evidence: design `:687` places `assert "sweep" not in UNATTENDED_COMMANDS` inside `test_load_usage_line_declares_checkpoint_and_load_is_not_converted` (:1318-1322). It passes, but the test name will no longer describe it. A separate one-line test is cleaner.

## Notes

- Considered and cleared: a second `"WC-14"` key (C2); the 31-entry P2 set (C9); the `uv run ...` code-span trap in `_check_repo_setup_gated` (C7, the WC-16 text has only `` `/sc:sweep` `` and one `` `### Liveness supervision` ``, neither matches the launcher list); the worked-example and fan-in slicing (C12).
- Residual risk I could not close without running pytest: whether ruff format (F5) or an unseen formatting hook alters the entry. I did not run any test or tool that writes.

## Self-audit

Tool calls that back the verdict: Read of research/07 and 08, r4-mechanical, r4-wc14-hits and r4-reanchor; Read of DESIGN 640-740, 741-768, 822-853 and 881-980; Read of the contract at 15-84 and 262-291; Read of the test file at 1-110, 140-440, 743-1193, 1300-1475, 1540-1610 and 1920-2030, 3120-3195; `grep` over the test file for `COMMANDS_DIR`, `.glob`, `.split(`, `re.findall`, `CONTRACT_PATH`, `NEVER_AS_WORKER`, `NOT_CONVERTED_IN_P1`, `sweep`; `grep -P` replay of the repo-setup regex; `grep -rn` for other readers and copies of the contract. I found one sequencing defect and five minor items, no end-state break.

## Summary

- Checks passed: 15 / 16 (C5 failed; C16 passed with a MINOR note)
- BLOCKING findings: 0
- MAJOR findings: 1 (F1)
- MINOR findings: 5 (F2 to F6)

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 20 | Grep: 4 | Glob: 0 | Bash: 7

Verdict: FAIL
Blocking count: 1
