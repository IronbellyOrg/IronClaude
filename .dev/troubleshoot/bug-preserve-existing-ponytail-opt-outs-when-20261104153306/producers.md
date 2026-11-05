observation-kind: string

## Producers

| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|---|---|---|---|---|---|---|---|
| P1 | src/superclaude/cli/install_user_setup.py:177 | current[name] = entry | none (loop continues; no return between header :150 and :177) | n/a | yes | yes (tier1-observation.md) | yes |

Grep hits for the observed value ("ponytail@ironclaude": true written into settings): 1 code producer (the defaults-merge write above; the value comes from src/superclaude/cli/user_settings_defaults.json:36). Row count 1 = grep hit count 1 (markdown excluded).
