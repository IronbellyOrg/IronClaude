# Wave 1.6 Branch B (log-config inspection) — returned by troubleshoot-analyst

degraded: true (Grep/Glob/Read only)

## Hits

| location | config_type | effective level / note |
|---|---|---|
| local-gateway-alias-proxy.py:70-72 `LOGFILE = os.environ.get("GW_PROXY_LOGFILE")` | env_var | unset by default (opt-in) |
| local-gateway-alias-proxy.py:128-133 (audit() LOGFILE append, OSError swallowed) | env_var consumer | only audit() writes to it |
| ccsession:801-804 `nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &` | pipeline_config | stdout+stderr -> /dev/null on every default launch; GW_PROXY_LOGFILE never set |
| ccsession:811 `shim failed to start (try: python3 $CC_SHIM_SCRIPT)` | pipeline_config | only debug path offered |
| ccsession:667-671 (sources ~/.claude/ccsession.env) | file | a user-added `export GW_PROXY_LOGFILE=...` would reach the shim; nothing ships it |
| ccsession.env.example:25-30 | file | no log/debug setting |
| install.sh:68-80, seed-env.py:46 | pipeline_config | never set GW_PROXY_LOGFILE |
| README.md:494-495 (manual restart recipe) | pipeline_config | also /dev/null; no section on shim logs |
| models.py:836-837 CCSESSION_MODELS_VERBOSE | env_var | models refresh only; shim never reads it |
| local-gateway-alias-proxy.py:80,98,112-117,164,185,192 | env_var | no CCSESSION debug/verbose/log switch for the shim |
| hooks/session-start.sh:21-45, src/superclaude/hooks/hooks.json:38,58,69 | file | no shim reference |
| tests/unit/test_ccsession_tiers.py:597 | pipeline_config | test-only shim.log capture |

## Reachability verdicts

| site | verdict | reason |
|---|---|---|
| local-gateway-alias-proxy.py:123 audit() | filtered_out | stderr is /dev/null; LOGFILE unset in both live shims (parent-observed) |
| local-gateway-alias-proxy.py:490 Handler.log_message | filtered_out | stderr only -> /dev/null |
| local-gateway-alias-proxy.py:871 startup print | filtered_out | stderr -> /dev/null |
| ccsession:779-824 setup_shim echo lines | reaches_sink | the launching terminal (not saved); startup choices only |

Summary: the shim has no output that persists by default; the only persistence path is the opt-in GW_PROXY_LOGFILE, which nothing sets.
