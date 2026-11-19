# A3 approach (implementer claims, per brief step 5)
- Comment sweep results in setup-github-selftest.sh:
  line 2 kept; lines 16-19 kept (send-arm rotation, verified against stub);
  line 26 REWRITTEN (wait -> send arm, per brief step 1);
  lines 61-62 REWRITTEN (PATH set per-command, not exported);
  lines 70-71 REWRITTEN (create-count only, template content not inspected, per brief step 2);
  line 90 kept (generator labels h2-T*, verified); lines 100-101 kept (EXISTS case, verified);
  stub-internal comments kept (45 "each send advances the scripted screen", 95 OB-root rewrite).
- STUB_ORCA export deleted (adviser B's finding; no reader). setup-github.sh and selftest.sh
  otherwise untouched except re-adding the T5 case registration and the gh-stub issue-URL arm,
  both reverted by the Q0 revert and restored as task-owned wiring.
- bash -n OK; full selftest 109 checks SELFTEST_OK.
