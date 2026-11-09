e1b4a3a15d33066fb845bbf2666f1794120b3235
# Blocking-family probe

## incomplete-implicit-selection-guard
Defect form: the source-contract inventory rejects only four double-quoted model values and misses haiku/fable and differently quoted unconditional native model fields.

Read-only search command:
```text
grep -n -E -e 'implicit_pin|assert_no_native|task_dispatch_config|parallel_dispatch|Merge Executor Dispatch' -- tests/skills/test_native_model_defaults.py src/superclaude/skills/ccsession-tag/README.md plugins/superclaude/commands/brainstorm.md src/superclaude/skills/sc-adversarial-protocol/SKILL.md Makefile tests/unit/test_install_ccsession.py
```
Before-output: focused tests:118,144,150,209,211,222,223; adversarial SKILL.md:575,1030,1970,2213. The four-value guard is at test line 222. No hits in README, plugin, Makefile or isolated installer tests. Coupled sites: all three native dispatch blocks (generation, advocacy, merge), orchestration descriptions and their inventory entries need model-field absence checks; the shared model-validation catalog at adversarial lines 590 and 972 must remain legal and outside this dispatch-field rule. Add negative regression snippets for every alias/marker and quote form, preserving explicit-selection prose/catalogs. This remains test-only; no production dispatch rewrite is needed.

after: saved command re-run. Focused tests now contain the value-independent native model-field assertion at line 18, rejection snippets at 29, explicit-selection prose preservation at 33, and its inventory application at 244. Dispatch anchors remain at adversarial SKILL.md:1030,1970,2213. All inventoried adversarial generation/advocacy/orchestration/merge sections reject a native model key regardless of value or quotes. Shared grammar/catalog sections are outside that field-absence guard and remain covered separately. No production source changed.
