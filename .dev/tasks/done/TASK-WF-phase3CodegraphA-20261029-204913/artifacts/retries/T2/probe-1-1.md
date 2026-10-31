0d6f67d7e2cdb6b5a496bfc7fb9e70c0487da3cd
family=evidence-accuracy
defect form: a result sentence claims a captured excerpt shows something the excerpt does not show
command: grep -n -E -e "same counts" -e "carries" -- .dev/codegraph-migration/experiments/P3-T0/E1-freshness.md .dev/codegraph-migration/progress/P3-0.md
before:
.dev/codegraph-migration/experiments/P3-T0/E1-freshness.md:7:- **Outcome A.** Without any daemon or MCP client on the sandbox, CLI `codegraph status` lists pend
coupled sites: E1-freshness.md step 4b excerpt label ("same moment, before the write above"); P3-0.md E-1 line (claims only the text output, no JSON claim)

family=group-comment-template
defect form: group comment decision list omits a decision-log row of the group
command: grep -n -F -e "| T1 |" -e "| T2 |" -- .dev/codegraph-migration/decisions/P3X-execution-log.md
before:
31:| 2026-10-31 | T1 | Run `$TESTSET` as two pytest invocations (group 1: every path excep
32:| 2026-10-31 | T1 | Tool-list branch is seven-tool | seven-tool; status-only | self (re
33:| 2026-10-31 | T2 | E-7: count the slots ledger by hand (117 step-table rows plus the 2
34:| 2026-10-31 | T2 | E-6: each smoke agent copy gets its target roster plus `mcp__codegr
35:| 2026-10-31 | T2 | E-6: discard the first matrix run and rerun with `--setting-sources
36:| 2026-10-31 | T2 | E-1: use a second nested scratch worktree (`cg-sandbox/.dev/worktre
coupled sites: .dev/codegraph-migration/progress/P3-0.md "Decisions made on my own" list (5 lines before the fix); the posted comment 6544339802

after (family=evidence-accuracy):
(no hit)
after (family=group-comment-template): P3-0.md decision lines
22:  - Tool-list branch: seven-tool, read from Phase 2's constant `install_codegraph.MCP_TOOLS` and the registered value.
