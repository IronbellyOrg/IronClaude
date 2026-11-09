68f058e2aeb47a04fbd759c68653a368e529ed22

## unresolved-picker-forwarding
Defect form: a restricted picker selector passes its original-ID check, refresh cannot resolve it, and the request is forwarded without a concrete destination check.
Search command:
```bash
git grep -n -E 'check_model_access|alias_to_real.get|unknown alias|def test_post_checks' -- src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py src/superclaude/skills/ccsession-tag/models.py tests/unit/test_ccsession_tiers.py
```
Before-output:
```text
local-gateway-alias-proxy.py:586: model_data.check_model_access(m)
local-gateway-alias-proxy.py:597: real = alias_to_real.get(bare)
local-gateway-alias-proxy.py:600: model_data.check_model_access(m, real)
local-gateway-alias-proxy.py:605: audit unknown alias
local-gateway-alias-proxy.py:747: model_data.check_model_access(f"claude-gw-{name}", model)
models.py:904: def check_model_access
models.py:979: check_model_access(value)
models.py:1030: check_model_access(model)
test_ccsession_tiers.py:3529: permitted resolved destination
test_ccsession_tiers.py:3531: denied resolved destination
test_ccsession_tiers.py:3544: fake Handler destination/non-model regression
```
Coupled sites: _post original selector, resolved destination and missing-alias branch; shared policy's allowed-versus-defined owner distinction; fake Handler destination regression and no-tier/unrestricted compatibility. Keep resolved aliases, tier fallback, non-model requests and no-tier pass-through unchanged.
After-output:
```text
src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:586:                model_data.check_model_access(m)
src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:597:                    real = alias_to_real.get(bare)
src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:600:                        model_data.check_model_access(m, real)
src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:607:                        model_data.check_model_access(m, bare)
src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:608:                    audit(f"WARN  unknown alias {m} (not in upstream /v1/models)")
src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:750:            model_data.check_model_access(f"claude-gw-{name}", model)
src/superclaude/skills/ccsession-tag/models.py:904:def check_model_access(model: str, destination: str | None = None) -> None:
src/superclaude/skills/ccsession-tag/models.py:979:                check_model_access(value)
src/superclaude/skills/ccsession-tag/models.py:1030:            check_model_access(model)
tests/unit/test_ccsession_tiers.py:3529:    models.check_model_access("claude-gw-gpt-6.1-sol", "gpt-6.1-sol")
tests/unit/test_ccsession_tiers.py:3531:        models.check_model_access("claude-gw-gpt-6.1-sol", "gpt-6-astra")
tests/unit/test_ccsession_tiers.py:3544:def test_post_checks_alias_destination_and_preserves_non_model_body(
```
