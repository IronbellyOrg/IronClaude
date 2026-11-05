# Tier 1 callers

index_state: fresh (python only; the bash launcher is not indexed, token graph:unindexed-language). Rows from Grep/Read floor, resolution=call-site (Read).

| symbol | caller | resolution |
|---|---|---|
| setup_shim (ccsession:752) | ccsession:1330 `[ "$USE_SHIM" = 1 ] && setup_shim` | call-site |
| shim start statement (ccsession:801-804) | inside setup_shim when no listener on the chosen port (ccsession:772-774) | call-site |
| ccsession --shim | ccsession-orca:79, ccsession-orca:81 (`exec "$CCSESSION" ... --shim --claude-args "$@"`) | call-site |
| local-gateway-alias-proxy.py `__main__` | started only by ccsession:804 (and by tests) | call-site |
