# Gate 1 (research-gate) consolidated findings: cycle 0

- Gate: Gate 1 (Phase 3, research gate), cycle 0 (first review)
- Sources:
  - `qa/analyst-completeness-report.md` (rf-analyst, completeness lens): FAIL
  - `qa/qa-research-gate-report.md` (rf-qa, evidence-quality lens): FAIL
  - `qa/qa-research-qualitative-report.md` (rf-qa-qualitative, research-depth lens): FAIL
- Severities are copied from the reports. None was lowered.
- Duplicate findings are merged into one row, and the row lists every lens that raised them.
- Source lens codes:
  - A = analyst
  - Q = rf-qa
  - QL = qualitative

Blocking count: 4

## Blocking findings (CRITICAL + IMPORTANT)

| # | Severity | Source lens | Research file | Finding | Proposed fix |
|---|---|---|---|---|---|
| B1 | IMPORTANT | A (I-1) | 04 | There is no Key Takeaways section. It is the only research file without one (checklist item 4). | Add a Key Takeaways block to 04 with 5-10 bullets. Suggested content: field 3 is authoritative; the empty-stdin cases; one nonzero exit aborts the whole push (E19); `--dry-run` runs the hook; the bypass set (E14-E17, E29 fail-open, E31 per-worktree hooksPath); the common-dir hook placement (E30); environment passthrough and the uv PATH gap (E28c). |
| B2 | IMPORTANT | A (I-2) | 02, 04, research-notes | Sub-question (b) "push via other tools" is open. It is not known whether pygit2/libgit2, dulwich, GitPython (which shells out to git) and JGit run the client-side pre-push hook. 02 leaves this [UNVERIFIED] (Gap 6, line 264; line 190). 04 does not test it (it only tests `send-pack`, E17). It is not routed to Phase 4 either: the web-01 sources in research-notes line 73 are git-scm only. | Pick one. (a) Test locally in a `mktemp -d` sandbox, only with packages already available offline (`uv run python ...`, no network installs), and record the result as a (b) row in 04. (b) Record in 04 Gaps an explicit `ROUTE web-01: (b) other tools` line, naming each library and its official documentation source, so that Phase 4 covers it. Either way, keep the [UNVERIFIED] tags for anything not observed. |
| B3 | IMPORTANT | Q (#1) | 03 lines 22, 299, 316 and Summary | False absence claim. 03 says Glob `.dev/brainstorms/2026110[56]*` returned no files, and that `.dev/brainstorms/20261105-170229-launch-level-hook/` (design line 487) is absent. The directory exists and is git-tracked (commit `4f7e3e7e`). It has 25 `.md` files, including `merged-requirements.md`, `enrichment/research-light.md`, `adversarial/adversarial/plan-review{,-2,-3}.md` and `refactor-plan.md`. `20261105-024132-issue-claim-orca-worktree-flag` also matches the glob. | Correct line 22 to say the line-487 corpus exists, with a fresh Glob result. Remove the corpus from the [STALE DOC] entry at line 316; that entry should then cite only the absent `20261106-l2-prepush-decisions/` files. Remove it from the open question at line 299, and fix the Summary. Then re-check whether any §19 statement attributed to that corpus can now be tagged. |
| B4 | IMPORTANT | QL (F1) | 01 §4 item 5 (line 194); 04 lines 1530 and 2245 | A failure mode that matters for the spec is missing, and the proposed remedy does not work. 01 item 3 (line 192) maps "no verdict" (identify exits 2 because uv is absent, launch-job-identity.sh line 53) to unknown, so a push to main/master is refused. 04 E28c shows uv can be missing from the hook's PATH. The no-store early exit (script lines 19-24) applies only to `$# == 0` or `hook`, not to `identify`, and line 25 requires uv. As a result, a human whose PATH lacks uv cannot push to main/master, and 01 item 5 omits this. 04's remedy, "call uv by absolute path", is not enough, because the script itself runs `command -v uv` (line 25) and `exec uv run ...` (line 566) through PATH. | In 01 item 5, add the case "a human whose PATH lacks uv (exit 2, treated as unknown) cannot push to main/master". List the hook-side options: (i) the hook sets a fixed PATH that contains the uv directory recorded at install time; (ii) the hook applies the no-store early exit itself; (iii) a pure-shell hook. In 04 lines 1530 and 2245, correct the remedy: an absolute uv path alone is not enough, because of script lines 25 and 566. Optional: confirm (i) or (ii) with one sandbox run using `PATH=/usr/bin:/bin` and no store, never running scripts under `src/superclaude/hooks/` (per the fix-agent rules, describe the behaviour from Read evidence instead). |

## Notes (MINOR, not applied by the fix agent, not rechecked)

| # | Severity | Source lens | Research file | Finding | Proposed fix |
|---|---|---|---|---|---|
| N1 | MINOR (note) | A (m-1), Q (#3) | 01 §7; 03 /tmp `l2_status` observations | The /tmp experiments lack a verbatim command, its output and a `git remote -v` record. Their safety is self-attested. | Add the command and output blocks, or mark the results as summarised. |
| N2 | MINOR (note) | A (m-2) | 04 | [CODE-VERIFIED] is used for runtime observations. | Use an empirical tag, or define the usage in the header. |
| N3 | MINOR (note) | A (m-3) | 04 | The ref listings and the E28b/E28c env blocks are abridged. The abridgement is declared. | None required. |
| N4 | MINOR (note) | A (m-4), Q (#7), QL (F5) | 04 lines 1791, 2247, 2254 | The D19-47 label is inconsistent: Stale Documentation says "None contradicted", while the table and Gaps say contradicted in part. | Attach the tag to the 03 paraphrase. At line 2254, add "(line 534 is incomplete; see Gaps)". |
| N5 | MINOR (note) | A (m-5), Q (#6), QL (F3) | 04 lines 2241-2242 | Two gap bullets are stale; F3a and F2 already resolved them (line 2248). | Strike them or retag them as RESOLVED. |
| N6 | MINOR (note) | A (m-6) | 01, 02, 04 | The 01 and 04 pair and the 02 and 04 pair have no explicit cross-links. | Add one-line references. |
| N7 | MINOR (note) | A (m-7) | 02 Gap 11 | The `remote.<name>.mirror` default is untested and unrouted. | Test it in a sandbox. |
| N8 | MINOR (note) | A (m-8), QL (F7 part) | 02 Gap 9 (line 267) | `refs//heads/main` is untested ("probably" rejected). | Run a one-line sandbox check, or mark it deferred. |
| N9 | MINOR (note) | A (m-9) | 04 | `--path-format=absolute` was not exercised. | Test it in a sandbox. |
| N10 | MINOR (note) | A (m-10) | 04 | Network transports, case folding and record order are [UNVERIFIED]. | Carry these as open questions. |
| N11 | MINOR (note) | A (m-11) | 03, 04 | 04 Step 2.5 supersedes 03's UNVERIFIED-GIT tags. | The synthesis uses 04's verdicts. |
| N12 | MINOR (note) | A (m-12) | 01 line 252 | It cites design line 514 without the CODE-CONTRADICTED context of D19-16. | Note the contradiction there. |
| N13 | MINOR (note) | A (m-13) | 01 line 236; 02 line 250 | External git claims are untagged; they are confirmed by 04 E29/E20. | Tag them, citing 04. |
| N14 | MINOR (note) | A (m-14) | 01, research-notes | (e) and (f) depend on Phase 4, and the PID-reuse consequence is inferred. | Confirm web-01/web-02 coverage, and mark the PID-reuse point as inferred. |
| N15 | MINOR (note) | Q (#2) | 01 line 55 | The quote omits `IFS=`. | Quote it exactly. |
| N16 | MINOR (note) | Q (#4) | 02 §5 | "cd persists between Bash calls" is stated as fact, but Gap 7 marks it [UNVERIFIED]. | Tag it [UNVERIFIED]. |
| N17 | MINOR (note) | Q (#5) | 03 §4 heading | It gives `install_hooks.py` as 612 lines; `wc -l` gives 611. | Change it to 611. |
| N18 | MINOR (note) | Q (#8) | 04 E0 | The commands that created `x.sh` and `hook-logging.sh` are not shown. | Show the creation lines. |
| N19 | MINOR (note) | Q (#9) | scope | web-01/web-02 are outside this gate. | They are gated at Gate 2/3. |
| N20 | MINOR (note) | QL (F2) | 01 line 246 | "with `core.hooksPath` unset" is ambiguous. | Reword it to say the printed path already follows the effective hooksPath. |
| N21 | MINOR (note) | QL (F4) | 04 lines 1530, 1699 | The cross-references are wrong: line 1530 cites E9-E11 (should be E19), and line 1699 cites E7/E8 (should be E15/E16). | Correct the references. |
| N22 | MINOR (note) | QL (F6) | 01 lines 140-142 | uv 0.11.8 is stated without a command, and the sections are out of order. | Record the `uv --version` output. |
| N23 | MINOR (note) | QL (F7 part) | 02 line 141 | The git-push docs are cited as "fetched" with no URL. | Add the URL. |
| N24 | MINOR (note, informational) | QL (F8) | 04 | No experiment covers a hook that does not read stdin during a large push. The QA sandbox found exit 0 with 3001 branches on 2.47.3. | Carry this as an observed QA fact, or have the hook drain stdin. |

## Result

Blocking count: 4 (B1-B4). Gate 1 is not yet passed. Step 3.2 (fix) and Step 3.3 (verification) are required for cycle 0.
