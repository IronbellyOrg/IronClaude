267fd7bdbb2bfb69c5f6ebd1bba701e6f253b046
family=env-dependent-expected-output
defect form: exact expected output that depends on env variables the step does not set or unset
command: grep -n -e "env -u" -e "missing: T2" -- docs/testing/v5.0.0/user/D12-reflect.md
before:
225:**Do:** (from `/tmp/d12/repo`; `env -u ANTHROPIC_MODEL` shows the built-in default model)
228:env -u ANTHROPIC_MODEL superclaude reflect run TASK.md --print-command; echo "exit=$?"
553:env -u T2ProxyUrl -u T2ProxyKey PATH="/tmp/d12/stub:$PATH" superclaude reflect run TASK.md --output /tmp/d12/out/s16 > /tmp/d12/out/s16.log 2>&1; echo "exit
563:superclaude.cli.swarm.transports.openai_compat.TransportEnvError: T2 proxy env contract incomplete; missing: T2ProxyUrl, T2ProxyKey. Set T2ProxyUrl, T2Proxy
coupled sites: src/superclaude/cli/swarm/transports/openai_compat.py:213-227; src/superclaude/cli/swarm/config.py:59,65
after:
225:**Do:** (from `/tmp/d12/repo`; `env -u ANTHROPIC_MODEL` shows the built-in default model)
228:env -u ANTHROPIC_MODEL superclaude reflect run TASK.md --print-command; echo "exit=$?"
553:env -u T2ProxyUrl -u T2ProxyKey -u T2Model01 -u T2Model02 -u T2Model03 -u T2Model04 -u T2Model05 -u T2Model06 -u T2Model07 -u T2Model08 -u T2Model09 PATH="/
563:superclaude.cli.swarm.transports.openai_compat.TransportEnvError: T2 proxy env contract incomplete; missing: T2ProxyUrl, T2ProxyKey, T2Model01..9. Set T2Pro

family=overbroad-claim
defect form: 'every run' claim that has an exception path
command: grep -n -e "Every run" -e "every run" -- docs/testing/v5.0.0/user/D12-reflect.md
before:
25:- Every run that gets past the configuration check writes `wrapper-result.yaml` in the output folder; every run that reaches the verdict writes a `reflect_po
coupled sites: src/superclaude/cli/reflect/runner.py:653-668
after:
25:- Every run that gets past the configuration check, except `--print-command` and `--dry-run` (they print and return before any file is written, `runner.py:65
