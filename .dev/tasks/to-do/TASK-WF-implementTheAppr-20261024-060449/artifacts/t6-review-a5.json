{
  "verdict": "missing",
  "ac": [
    {
      "id": "T6.AC1",
      "status": "met",
      "evidence": [
        "tests/recommend/fixtures/routing_refresh_cases.json:673",
        "tests/recommend/test_routing_refresh.py:152"
      ],
      "reason": "T01-T76 each map to existing test functions, which are checked through the code's syntax tree, or carry a Task8 marker (T14-T22, T47). Every S01-S29 case has the required keys, a request, an environment, a target, mode flags checked against declared Usage/argument-hint/option tables (test:270), Required positionals retained or clarified (test:379), routing-row mandatory flags (test:437) and a side-effect/authority boundary (test:221)."
    },
    {
      "id": "T6.AC2",
      "status": "unmet",
      "evidence": [
        "tests/recommend/fixtures/routing_refresh_cases.json:606",
        "tests/recommend/test_routing_refresh.py:490"
      ],
      "reason": "S26's unavailable-plugin variant removes sc-pm-protocol and expects 'pm stays unavailable', but the variant has no request and S26's own request is the sc:agent startup, which needs no pm protocol. The check at test:490 accepts any primitive listed in activation, including ones used only by a repeat. S25's load repeat (fixture:581) silently inherits a seeded-cache expectation that 'selects /sc:save' (fixture:585), because test:553 skips repeats on the same block. S24's coordinated-docs repeat (fixture:559) has no competitor of its own: its case competitor is its own target, so test:206 subtracts it and a default /sc:index-repo step in document-built would pass. The specialist cases themselves (cleanup-audit, cliEval create/run, release split/no-split/continuation, swarm, tier missing-suite) are correct."
    },
    {
      "id": "T6.AC3",
      "status": "met",
      "evidence": [
        "tests/recommend/test_routing_refresh.py:1",
        "tests/recommend/fixtures/routing_refresh_cases.json:4"
      ],
      "reason": "The tests only read files and use no subprocess, network or authentication. The fixture and tests are labelled static, with Task8 owning generation."
    },
    {
      "id": "T6.AC4",
      "status": "met",
      "evidence": [
        "tests/recommend/test_routing_refresh.py:609",
        "tests/recommend/test_routing_refresh.py:660"
      ],
      "reason": "Exact equality with Appendix C plus inventory.json, 43 active and 4 retired, and the formatting-only list is pinned. Analyst reports and Appendix D are kept, and T76 is labelled research evidence (fixture:749)."
    },
    {
      "id": "T6.AC5",
      "status": "met",
      "evidence": [
        ".dev/tasks/to-do/TASK-WF-implementTheAppr-20261024-060449/artifacts/t6-a5-tests.log:64",
        "tests/recommend/fixtures/routing_refresh_cases.json:741"
      ],
      "reason": "The 4 recorded failures are all Task7 mirror/level-copy work and are marked pending, not skipped. Rerun: 330 passed, 2 failed (Task7 parity)."
    }
  ],
  "extra_scope": [],
  "misunderstood": [],
  "findings": [
    "S26 unavailable_plugin is aimed at the pm repeat, not the S26 request; the test permits it.",
    "Same-block repeats (S25 load, S26 pm) have no seeded-cache expectation of their own, and the inherited text names the wrong target.",
    "The S24 repeat has no negative competitor, so interchanging index-repo and index on document-built goes undetected.",
    "side_effects is only checked for presence, not for being non-empty."
  ],
  "self_audit": "Checked all 29 cases, every repeat and both variants against the live routing table, the Other-commands block (HOW-WE-WORK.md:318-391), the SKILL Step 0 checks used at test:561, the auggie/workflow/swarm argument-hints, and README mirror list :9. I spot-checked the T19/T20/T36/T37/T48/T51/T56/T62/T65/T66 assertions. I did not read the retries folder or earlier reviews."
}
