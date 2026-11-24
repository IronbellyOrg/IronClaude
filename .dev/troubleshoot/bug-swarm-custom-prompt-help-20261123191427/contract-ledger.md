# Contract Enumeration Ledger

## Contract rows

| contract_token | role | component_path | discovery_method | classification | unreachability_proof |
|---|---|---|---|---|---|
| --custom-prompt-dir | producer | commands.py:438 | exact Grep, source Read, public help capture | classified: stale docstring help | n/a live |
| --custom-prompt-dir | producer | commands.py:3785 | same | classified: stale option help | n/a live |
| help literals | transformer | swarm/__init__.py:136-154 and Click help formatter | registration Read and actual captures | classified: public help output | n/a live |
| directory CLI option | consumer | swarm run public parser, run-rejection.txt:4 | actual public invocation | classified: rejected unknown option | n/a live |
| custom_prompt_dir | consumer | preflight.py:1569-1615 | source Read | classified: JobSpec custom-lens directory loading | n/a live |
| custom_prompt_dir | evaluator | schema.py:685-734 | source Read | classified: nonempty field requires custom lens | n/a live |
| custom_prompt_dir | producer | commands.py:1167,3830 | exact search and Read | classified: existing correct rejection guidance | n/a live |
| --custom-prompt-dir | producer | commands.py:125,1160,3718,3824 | exact-token sweep | classified: non-emitted internal comments, not additional public help | comments, not dead code claim |

Paths are relative to src/superclaude/cli/swarm unless a captured artifact. No row is declared dead/legacy.

## Sibling sweep

Exact-token search commands.py yielded six hits:125,438,1160,3718,3785,3824. Only438 and3785 are rendered help passages in scope. Others are comments, not reason to expand the fix. run-help.txt's <custom-prompt-dir>/system.txt is a path placeholder, not that option. Existing diagnostics at1167/3830 correctly name the field. Docs command-reference.md:56-61 also name the supported field. Job behavior is source-verified only, not executed.

## Verdict

HC2 PASS for bounded contract inventory: nonempty ledger, all discovered in-scope consumers classified, actual help/parser captures bind source to product path. Augment403 reduces semantic discovery recall; no whole-repository exhaustive inventory or runtime custom-job proof claimed.
