# QA Report - Qualitative, Actionability Lens (Gate 3)

**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**QA phase:** qual-actionability (tech-ref-qualitative)
**Lens:** actionability
**Date:** 2026-11-20
**Fix authorization:** false
**Status:** Complete

Source root used: /home/coder/.cache/ic-snap-20261120/master (read only; nothing written there). Removed code read only through `git -C /home/coder/workspaces/IronClaude show/ls-tree 01e7a9e23^`. The whole document (2,369 lines) was read in chunks.
Stance: assume defects exist; only evidenced defects are reported; zero BLOCKING would be valid if shown.

## Working notes (Section 13 Extension Guide, checked against the snapshot)

- 13.1.1 (reason word): files and functions exist (`audit.py:26-102/104`, `cycle.py:466-477/480-482/587-592`, `_Stop(reason, stamp=False)` at `cycle.py:503-513`, pins `test_audit.py:214/223` exist). Gap: title says "skip or stop" but the skeleton only shows `_Stop`/`_cond`; a per-issue skip is raised with `_Skip` (`cycle.py:491`), which this scenario never names (it is named in 5.1.6 and 5.1.9). The "kinds" comment omits `warning` and `skip/warning` (`audit.py:96-101`). Pitfall cites `audit.py:229-243` for the note rule; that range is `_RULES`; the note rule is `audit.py:280-284`.
- 13.1.2 (config key): `_TOP_KEYS` `cycle.py:58-69`, `Config` `:96-107`, `load_config` `:195-283`, `_invalid` `:110` all exist and match the skeleton.
- 13.1.3 (gh read): builders `github.py:175-262`, `_call` `:557-577`, helper names exist. Skeleton shows only an argv builder; the typed reader function (like `events` `:845`, `reread` `:934`) and the call site in `cycle.py` are not named.
- 13.1.4 (pipeline level): `BLOCK_MARKER` `orca_worktree.py:743`, `render_prompt` `:746-761`, `choices` `:1873/:1883/:1891`, guard word table `launch-level-guard.sh:264-269`, grid `:785-803` all exist and match; pin tests exist (`test_issue_protocol.py:295`).
- 13.1.5 (guard class): ranges exist. "not determinable from research" for the classifier is not true of the files: classes are added with `LL_CLASSES+='NAME '` (`launch-level-guard.sh:409-412, 761, 767, 774`).
- 13.1.6 (hook script): `_FRESHNESS_SCRIPTS` `install_hooks.py:42-97` (launch scripts at 90/93/96), registration shape, pins `test_install_hooks.py:1086/1104/897`, `test_freshness_subagent_start_policy.py:105-115` all exist and match.
- 13.1.7 (worker tier): `WORKERS` `test_issue_worker_agents.py:21-26`, `ISSUE_WORKER_PINS` `test_model_alias_policy.py:29-33`, `TIER_TEXT_ALLOWED` `:38-44`, test `:104`, `ccsession-models.json` tier keys at 85/93/104/113 all exist. Skeleton frontmatter omits `description`, which `test_issue_worker_agents.py:82` asserts.
- 13.1.8 (contract rule): `RULE_PHRASES` `test_worker_contract.py:25-436`, `test_contract_states_rule` `:876-878`, `_check_never_as_worker` `:734`, `NEVER_AS_WORKER` `:444-454` exist. The skeleton shape is wrong (see finding F-01).
- Section 15.2: all 18 commands were run read-only against the snapshot (and `git show`/`ls-tree` on `01e7a9e23^`); 15 produce exactly the stated expected result. Three (#7, #15, #16) contain a table-escaped pipe (see F-02).

## Verdict: FAIL

Two BLOCKING findings (F-01, F-02). Minor findings M-01 to M-09 are notes and do not affect the verdict.

## Entry check table

| Entry | Specific yes/no | Problem |
|-------|-----------------|---------|
| 13.1.1 Add a watcher skip or stop reason | Yes, with notes | Files, functions, pins exist. Skeleton shows only `_Stop`/`_cond`; `_Skip` (the per-issue skip primitive, `cycle.py:491`) is not named here (M-01). |
| 13.1.2 Add a watcher config key | Yes | All named symbols and lines match. Test names for the config rules are not given (file only). |
| 13.1.3 Add a read-only gh call | Yes, with notes | Builder, `_call`, helpers exist. Call site in `cycle.py` and the typed reader function are not named (M-02). |
| 13.1.4 Add a `--pipeline` level | Yes | Every file, line, regex and `choices` site checked and matches. |
| 13.1.5 Add a guard level or class | Mostly | Classifier mechanism marked "not determinable" although the files show it (M-03). |
| 13.1.6 Register a new hook script | Mostly | Ordering constraint on the guard group not stated (M-04). |
| 13.1.7 Add a claim worker tier or template | Mostly | Skeleton frontmatter omits `description` required by a pinned test (M-03). |
| 13.1.8 Add a coordinator contract rule | No | Skeleton for `RULE_PHRASES` has the wrong value shape (F-01). Plugin-copy question marked "not determinable" although the snapshot answers it (M-03). |
| 13.2 Testing requirements table | Yes | Test files exist; line pins checked. |
| 9.1 Watcher configuration file | Yes | 8 top-level keys, defaults, valid values all match `load_config` (`cycle.py:195-283`, `_label` `:127-139`). No sample config (M-08). |
| 9.2 Claim, guard and install settings | Yes | `main.py:219/412`, `install_hooks.py:282-289`, `IR7_REFUSE` match. |
| 9.3 Environment variables and paths | Yes, with notes | Names/defaults match (`orca_worktree.py:88-91/798-799`, `clickup_claim.py:74/88-94/164-172`, `ccsession:159-163`). `CCSESSION_PERMISSIONS` other values exit 2 (not stated). |
| 9.4 Not configurable | Yes | Matches constants `cycle.py:33-47`. |
| 2.3 Ledger (18 rows) | Yes | Every row has a status word, evidence and trigger; no "may/seems/probably" wording (grep: 0 hits). |
| 4.4 Trigger table | Yes | Every row has trigger, runner, frequency, evidence, live status. |
| 4.5 Writes-to-GitHub table | Yes, with note | Exact commands per piece; no status-word column (M-07). |
| 14.2.1 Defect candidates (D-01..D-31) | Yes | Every row has declaring doc line, code evidence, class, status word. 18 rows re-read against code: all true. |
| 14.3 Future considerations | Yes | "Revisit When" present. |
| 14.3.1 Open questions U-1..U-11 | Partly | State what is unknown and why; no "what would resolve it"; Q-12, Q-13, Q-17, C-36..C-38, C-64 not defined in Section 14 (M-05). |
| 15.2 Spot-check protocol (18 commands) | Partly | All read-only and runnable; 3 depend on how a table-escaped pipe is decoded (F-02). |

## Findings

| ID | Severity | Location | Issue | Evidence | Required fix |
|----|----------|----------|-------|----------|--------------|
| F-01 | BLOCKING | Section 13.1.8 skeleton (doc lines 1834-1836) | The skeleton `RULE_PHRASES["<rule-name>"] = ["<required phrase 1>", "<required phrase 2>"]` assigns a plain list. The real value is a 2-tuple `(identifier-or-None, [phrases])`. Following the skeleton makes `ident, phrases = RULE_PHRASES[rule]` unpack the list wrongly: with two phrases `phrases` becomes a string (each character is checked as a "phrase"), so the pin passes vacuously or fails confusingly; with 1 or 3+ phrases it raises ValueError. The new rule would be pinned by a broken test. | `/home/coder/.cache/ic-snap-20261120/master/tests/skills/test_worker_contract.py:24` (comment "rule -> (identifier ..., or None; phrases)"), `:25-32` (entries are `(None, [ ... ])`), `:724-731` (`ident, phrases = RULE_PHRASES[rule]`) | Change the skeleton to `RULE_PHRASES["<rule-name>"] = (None, ["<required phrase 1>", "<required phrase 2>"])` and say what the first element is (an identifier that must share a line with the first phrase, or None; `test_worker_contract.py:728-731`). |
| F-02 | BLOCKING | Section 15.2 commands #7, #15, #16 (doc lines 2025, 2033, 2034) | Commands are written inside Markdown table cells with the pipe escaped as `\|`. Copied raw (backslash kept), #15 and #16 are wrong: the pipe becomes a literal argument (run: `ls DIR \| wc -l` prints a directory listing, not `19`). Copied from a rendered table (backslash removed), #7 becomes `grep -c 'WC-17|Issue pipeline duties' FILE`; in grep's default (basic) syntax a bare `|` is a literal character, so it prints `0` for any input and the check "the contract has no WC-17 / no Issue pipeline duties" cannot fail (run: the same form with the existing term `WC-16` also prints `0`; the raw form with `\|` prints `1`). A spot-check that returns the expected value for the wrong reason is not a usable check for ledger row 7. | Ran against the snapshot: raw `ls ... \| wc -l` gives a file listing; rendered `grep -c 'WC-16|Issue pipeline duties' .../WORKER-CONTRACT.md` gives `0` while raw `grep -c 'WC-16\|Issue pipeline duties'` gives `1` | Move the 18 commands out of the table into a fenced code block (no pipe escaping needed), and rewrite #7 without a pipe: `grep -c -e 'WC-17' -e 'Issue pipeline duties' "$S/src/superclaude/core/WORKER-CONTRACT.md"`. |
| M-01 | MINOR | Section 13.1.1 (doc lines 1750-1760) | Title says "skip or stop reason" but the skeleton shows only `raise _Stop(...)` / `self._cond(...)`. A per-issue skip is raised with `_Skip` (`cycle.py:491`, `raise _Skip` at `:845, :892, :913, :921`); a `_Stop` ends the cycle with no decision line (`cycle.py:824-834`). The right primitive is stated in 5.1.6 (doc line 931), so the guide is incomplete, not wrong. Also: the "kinds" comment omits `warning` and `skip/warning` (`audit.py:96-101`); the pitfall cites `P/audit.py:229-243` for "a note word must have kind note" but that range is `_RULES`, the rule is at `audit.py:280-284`; "the `df42_...` tests" are in `tests/issue_watch/test_record.py:1518, 1522`, not named. | `cycle.py:491-513, 824-834`; `audit.py:26-102, 229-243, 280-284`; `test_record.py:1518, 1522` | Add `raise _Skip("new_reason")  # one issue; the loop continues` to the skeleton, list all kinds, fix the citation to `audit.py:280-284`, name `test_record.py`. |
| M-02 | MINOR | Section 13.1.3 | Registration point incomplete: only the argv builder is shown. A new read also needs a typed reader like `events` (`github.py:845`) or `reread` (`:934`) and a call in `cycle.py` (`_examine`), neither named. | `github.py:557-577, 804, 845, 934` | Name the reader function pattern and the call site. |
| M-03 | MINOR | Sections 13.1.5, 13.1.7, 13.1.8 | "Not determinable from research" is used where the snapshot answers it. (a) 13.1.5: classes are added with `LL_CLASSES+='NAME '` (`launch-level-guard.sh:409-412, 761, 767, 774`). (b) 13.1.8: no plugin copy of the contract exists (Glob `**/WORKER-CONTRACT.md` in the snapshot returns only `src/superclaude/core/WORKER-CONTRACT.md`; installer lists it at `install_core.py:28`). (c) 13.1.7: the skeleton frontmatter omits `description`, which `test_issue_worker_agents.py:82` asserts (`fields["description"]`), and `category`/`effort` present in `issue-worker-t3.md:4-7`. | files cited | State the mechanism, state "no plugin copy exists", add `description` to the skeleton. |
| M-04 | MINOR | Section 13.1.6 skeleton | Says only that the identity group stays last. The pinned test also requires the guard group at index `len-2` (`test_launch_level_guard_registration.py:115-118`) and exactly three Bash PreToolUse commands (`:107-111`). A new group placed between guard and identity fails it. | `test_launch_level_guard_registration.py:99-118` | Say "insert before the guard group". |
| M-05 | MINOR | Section 14.3.1 (doc lines 1976-1988), 5.3 line 1258, 5.4 line 1362 | Checklist item (4) not fully met: rows U-1..U-11 give "what is unknown" and "why not resolvable from files" but no "what would resolve it". Ids Q-12, Q-13, Q-17 (and gap-log ids C-36..C-38, C-64) are cited in Sections 5.3/5.4 but never defined in Section 14 (the same questions appear as U-4, U-6, D-25 without those ids). | doc grep for `Q-1x` | Add a "What would resolve it" column and map every Q/C id to a U/D row. |
| M-06 | MINOR | Section 13 header | Path shorthand (`P/`, `T/`, `GUARD`, `OW`, `WCT`, `DES`) is defined at the start of Section 12, not in Section 13; `T/` means `tests/issue_watch/` in 12-14 but `tests/` in 5.2-5.4. A reader jumping to Section 13 must find the key one section up. | doc lines 1697, 984 | Restate the shorthand key under the Section 13 heading. |
| M-07 | MINOR | Section 4.5 writes table | No status-word column (BUILT-ON / BUILT-OFF); the watcher rows are BUILT-OFF only per the ledger (2.3). | doc lines 591-615 | Add the status word per row or a pointer to 2.3. |
| M-08 | MINOR | Sections 9.1, 9.3, 14.2.1 D-13 | (a) 9.1 says "no sample file ships" and gives no sample; the runbook holds one at `docs/designs/issue-watcher-setup.md:73-82` (not cited). (b) `CCSESSION_PERMISSIONS`: valid values are `default` or unset; any other value exits 2 (`ccsession:159-163`), not stated. (c) D-13 cites `swarm/atomic.py:33-38`; the repository-relative path is `src/superclaude/cli/swarm/atomic.py`. (d) 15.2 #7 expected cell holds two results for one command (`0` and `339`). | files cited | Cite the sample, state the values, expand the path, add `wc -l` as its own command. |
| M-09 | MINOR | Section 5.3 extension row "change a hook script" | Does not say that a byte change to `launch-level-pre-push.sh` also needs `L2_VERSION_LINE` and `L2_HOOK_SHA256` re-pinned (`tests/cli/test_install_hooks.py:1098-1124`). | same | Add the sha re-pin step. |

## Checks performed

Lens checklist (6 of 6 applied with tool evidence):

1. Extension Guide, 8 scenarios: every named file, function, constant, line range and pin test was opened or grepped in the snapshot. About 95 individual names/ranges checked; 0 non-existent files or functions; 1 wrong skeleton (F-01); other gaps are minor (M-01 to M-04).
2. Configuration (Section 9): 9 config keys, 6 claim/install settings, 16 environment/path rows, 8 fixed behaviours checked against `cycle.py`, `orca_worktree.py`, `clickup_claim.py`, `ccsession`, `install_hooks.py`, `main.py`; all names, defaults and valid values match.
3. Decision aids: ledger (18 rows), trigger table (21 rows), writes table (22 rows), defect candidates (31 rows, 18 re-read against code, 0 without evidence). Grep for hedging words ("probably", "seems", "appears to", "likely", "perhaps", "presumably", "maybe", "might"): 0 hits; "may/could/should": only in quoted rule text.
4. Open questions (14.3.1): 11 rows read; gaps in resolution path and ids (M-05).
5. Spot-check protocol: 18 of 18 commands executed against the snapshot (and the removed tree with read-only `git`); all read-only; 15 give the stated result unambiguously; 3 depend on pipe-escape decoding (F-02).
6. Testability: expected results are stated per command; ledger statuses use four fixed words.

Counts: Read 49 | Grep about 30 | Glob 4 | Bash 8 (read-only; no file written outside this report; nothing written under the snapshot). Tool calls exceed the 6 lens items.

## Self-Audit

- Independently verified against source: about 190 claims (named files, functions, constants, line numbers, env names, defaults, test names, 18 shell commands).
- Files read for verification: `cli/issue_watch/{audit,cycle,github,launch,record,cli}.py`, `cli/swarm/atomic.py`, `cli/install_hooks.py`, `cli/main.py`, `skills/sc-issue-protocol/{SKILL.md,refs/tiers.md,scripts/orca_worktree.py,scripts/clickup_claim.py,templates/launch-prompt.md}`, `hooks/scripts/launch-level-guard.sh`, `hooks/scripts/launch-job-identity.sh`, `hooks/hooks.json`, `core/WORKER-CONTRACT.md`, `agents/issue-worker-t3.md`, `skills/ccsession-tag/ccsession-models.json`, `docs/designs/issue-watcher-setup.md`, and the tests named in Section 13 (`test_audit.py`, `test_worker_contract.py`, `test_issue_worker_agents.py`, `test_model_alias_policy.py`, `test_install_hooks.py`, `test_launch_level_guard.py`, `test_launch_level_guard_registration.py`, `test_freshness_subagent_start_policy.py`, watcher tests by line).
- Why the verdict is FAIL: F-01 is a skeleton that produces a malformed test pin (evidenced at `test_worker_contract.py:724-731`); F-02 is a set of spot-check commands whose result depends on how a table pipe is decoded, one of which (#7) cannot fail in the rendered reading (run and shown).
- Reliance on inherited structural verdicts: none was passed in the prompt; no structural re-check was skipped.
- Web research: none performed (no external lookup needed); no repository or owner detail was sent anywhere.

Status: Complete
