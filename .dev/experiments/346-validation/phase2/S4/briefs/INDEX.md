# briefs/INDEX.md

Every file below is the prompt string of one Agent/Skill call, byte for byte as stored in the session log.
`L` = 1-based jsonl line in the main session log (BM). The agent's own log: `<BM folder>/subagents/agent-<agentId>.jsonl`.
`taskfile line` = the line of the task file that the wrapper tells the agent to read (the real, long brief).

| file | L | time (UTC) | subagent_type | description | agentId | task-file line | sha256[:12] |
|---|---|---|---|---|---|---|---|
| S-skill-tech-research_L138.json | 138 | 13:25:32 | Skill | tech-research |  |  | 9a2e4a75f2b6 |
| S-skill-task_L156.json | 156 | 13:25:36 | Skill | task |  |  | 8273210adb3f |
| W1-research-01_L330.md | 330 | 15:39:14 | rf-task-researcher | Research agent 01 installer | a7508f46d9368b4b0 | 193 | 2e92a5142fb7 |
| W1-research-02_L334.md | 334 | 15:39:17 | rf-task-researcher | Research agent 02 CLI and slug | a6f0b32db9feef327 | 197 | 0eaa02c50916 |
| W1-research-03_L338.md | 338 | 15:39:20 | rf-task-researcher | Research agent 03 startup and HOME | a64796ab21af6561b | 201 | 1d134ccc722d |
| W1-research-04_L342.md | 342 | 15:39:22 | rf-task-researcher | Research agent 04 pinned tests | a88e6aa094a2a2e15 | 205 | 46125d0bec58 |
| W1-research-05_L346.md | 346 | 15:39:25 | rf-task-researcher | Research agent 05 docs and decisions | a58e271aeaf1a6ebd | 209 | df9b81a260ba |
| G1-R1-analyst-completeness_L676.md | 676 | 15:52:20 | rf-analyst | Gate 1 analyst completeness | adb7f31e826776d9f | 218 | 05a7d231e535 |
| G1-R1-rf-qa-evidence-quality_L680.md | 680 | 15:52:23 | rf-qa | Gate 1 rf-qa evidence quality | a61cc48b1c9410d23 | 222 | 2cbc090fae3f |
| G1-R1-qualitative-research-depth_L684.md | 684 | 15:52:26 | rf-qa-qualitative | Gate 1 qualitative research depth | a8eb2106d0ccf8b20 | 226 | d20acd2daecc |
| G1-F1-fix_L841.md | 841 | 16:05:17 | rf-qa | Gate 1 fix agent cycle 1 | af31560593f76e747 | 234 | bc8f559b35e8 |
| G1-R2-verify-structural_L924.md | 924 | 16:19:11 | rf-qa | Gate 1 verification structural c1 | a1fbcae1d9e33eed8 | 238 | 19498fa351f6 |
| G1-R2-verify-qualitative_L928.md | 928 | 16:19:13 | rf-qa-qualitative | Gate 1 verification qualitative c1 | a5ecf4eb689fb9907 | 242 | 2b70e2fc77a9 |
| G1-F2-fix_L1075.md | 1075 | 16:32:24 | rf-qa | Gate 1 fix agent cycle 2 | afa3a5a3346fdc8dd | 254 | 2da7f49551fb |
| G1-R3-verify-structural_L1120.md | 1120 | 16:37:47 | rf-qa | Gate 1 verification structural c2 | a0bb655287313c4ed | 258 | 62649e6c1cf7 |
| G1-R3-verify-qualitative_L1124.md | 1124 | 16:37:50 | rf-qa-qualitative | Gate 1 verification qualitative c2 | a5c85d7683a23ce80 | 262 | ff851ef1ed5a |
| G1-X-gaps-log_L1545.md | 1545 | 17:19:57 | rf-analyst | Compile Gate 1 gaps log | a7bbfacaff2c8968d | 270 | e0c9159328d6 |
| W2-web-01_L1589.md | 1589 | 17:33:27 | rf-task-researcher | Web research web-01 Claude Code | adacc2f39796ea4e3 | 279 | 84c1427350f0 |
| W2-web-02_L1593.md | 1593 | 17:33:30 | rf-task-researcher | Web research web-02 upstream BMAD | aaae50def4963466b | 283 | 6e6fa7c8fd06 |
| W3-synth-01_L1729.md | 1729 | 17:46:04 | rf-analyst | Synthesis agent synth-01 | a4ee5ae560e76b0fa | 292 | dc825c9bf685 |
| W3-synth-02_L1733.md | 1733 | 17:46:07 | rf-analyst | Synthesis agent synth-02 | a28d3483534f338fb | 296 | 469d93cbade2 |
| W3-synth-03_L1737.md | 1737 | 17:46:11 | rf-analyst | Synthesis agent synth-03 | a204bca90bc282cde | 300 | b2653e01c1ae |
| W3-synth-04_L1856.md | 1856 | 17:58:32 | rf-analyst | Synthesis agent synth-04 | aa1c9a3a0bba3be50 | 304 | ac2e3b6fec98 |
| G2-R1-analyst-synthesis-accuracy_L1899.md | 1899 | 18:11:58 | rf-analyst | Gate 2 analyst synthesis accuracy | a43c8c87c351dd201 | 308 | 2998abba1f55 |
| G2-R1-rf-qa-synthesis-structure_L1903.md | 1903 | 18:12:01 | rf-qa | Gate 2 rf-qa synthesis structure | a43627cf89dbfb856 | 312 | 19cf7ade4dec |
| G2-R1-qualitative-synthesis-coherence_L1907.md | 1907 | 18:12:04 | rf-qa-qualitative | Gate 2 qualitative synthesis coherence | a0b7a15a9edccb39a | 316 | ed058b43bd16 |
| G2-C1-consolidate_L1985.md | 1985 | 18:23:53 | rf-analyst | Consolidate Gate 2 findings cycle 1 | a1552743b42750138 | 320 | fbd5c283a8d6 |
| G2-F1-fix_L2018.md | 2018 | 18:27:46 | rf-qa | Gate 2 fix agent cycle 1 | a52890586867b302f | 324 | 36960e44268a |
| G2-R2-verify-structural_L2061.md | 2061 | 18:36:18 | rf-qa | Gate 2 verification structural c1 | ab496102f7fbc66a4 | 328 | 873a0d7df412 |
| G2-R2-verify-qualitative_L2065.md | 2065 | 18:36:21 | rf-qa-qualitative | Gate 2 verification qualitative c1 | a0c0a4ba91f6f27bf | 332 | ae08fa35a523 |
| G2-F2-fix_L2202.md | 2202 | 18:41:01 | rf-qa | Gate 2 fix agent cycle 2 | ac3d57d0216ea58da | 344 | 7337bd100e87 |
| G2-R3-verify-structural_L2244.md | 2244 | 18:45:35 | rf-qa | Gate 2 verification structural c2 | a109335565023ab94 | 348 | 6c7e4184cf6a |
| G2-R3-verify-qualitative_L2248.md | 2248 | 18:45:38 | rf-qa-qualitative | Gate 2 verification qualitative c2 | a254fad7954bd3a56 | 352 | 06c05554461b |
| W4-assemble-report_L2758.md | 2758 | 18:58:13 | rf-assembler | Assemble final research report | a9c6678fe08ab2dda | 365 | 9e6e98d2d579 |
| G3-R1-lens-template-conformance_L2802.md | 2802 | 19:00:32 | rf-qa | Gate 3 lens template-conformance | a5118305900ff8197 | 371 | a4412e688991 |
| G3-R1-lens-internal-consistency_L2806.md | 2806 | 19:00:35 | rf-qa | Gate 3 lens internal-consistency | a13ddcb66b088bde4 | 373 | 921961072b4d |
| G3-R1-lens-evidence-quality_L2810.md | 2810 | 19:00:39 | rf-qa | Gate 3 lens evidence-quality | a24a47875bd73d157 | 375 | 19c6828ac62a |
| G3-R1-lens-actionability_L2814.md | 2814 | 19:00:42 | rf-qa-qualitative | Gate 3 lens actionability | af03ba5f4a6bf800c | 379 | 9ef907c880b8 |
| G3-R1-lens-domain-accuracy_L2818.md | 2818 | 19:00:45 | rf-qa-qualitative | Gate 3 lens domain-accuracy | ac93e48c931e3c369 | 381 | a1c4ceaa02ad |
| G3-R1-lens-crossref-chain_L2822.md | 2822 | 19:00:49 | rf-qa-qualitative | Gate 3 lens crossref-chain | a8a7a4718d48d3b75 | 383 | 82b7b9fc34a6 |
| G3-R1-lens-finding-reproducibility_L2826.md | 2826 | 19:00:52 | rf-qa-qualitative | Gate 3 lens finding-reproducibility | ae7fb1b0e358dc701 | 387 | 91d5c00589f3 |
| G3-C1-consolidate_L2965.md | 2965 | 19:15:40 | rf-analyst | Consolidate Gate 3 findings cycle 1 | ae8290b60be8b2c48 | 391 | 928eab2c87ed |
| G3-F1-fix_L3080.md | 3080 | 19:22:40 | rf-qa | Gate 3 fix agent cycle 1 | a6d4640dcb29511a6 | 393 | 37300efdf2ab |
| G3-R2-verify-structural_L3122.md | 3122 | 19:41:35 | rf-qa | Gate 3 verification structural c1 | ab6068785b4ee25d9 | 397 | e69bbf28c1dc |
| G3-R2-verify-qualitative_L3126.md | 3126 | 19:41:39 | rf-qa-qualitative | Gate 3 verification qualitative c1 | a16adb392c5b25eb7 | 399 | dcdf4f194fdb |
| G3-F2-fix_L3289.md | 3289 | 19:50:25 | rf-qa | Gate 3 fix agent cycle 2 | a8c898470d50f017e | 405 | ea499ecf3427 |
| G3-R3-verify-structural_L3332.md | 3332 | 19:55:43 | rf-qa | Gate 3 verification structural c2 | a649f9696806b9bcd | 407 | 6b630640cfdf |
| G3-R3-verify-qualitative_L3336.md | 3336 | 19:55:47 | rf-qa-qualitative | Gate 3 verification qualitative c2 | a14f9ad56fe83727f | 409 | ee677b0a9f64 |
| G4-R1-fidelity-agent-1_L3718.md | 3718 | 20:15:23 | rf-qa | Gate 4 fidelity agent 1 | a26ffd32ace0b2afb | 417 | 5bd3f1d5fd62 |
| G4-R1-fidelity-agent-2_L3722.md | 3722 | 20:15:27 | rf-qa | Gate 4 fidelity agent 2 | abcd45de4c3365334 | 419 | 1e3731c6a26e |
| G4-R1-fidelity-agent-3-with-web-check_L3726.md | 3726 | 20:15:31 | rf-qa | Gate 4 fidelity agent 3 with web check | a1e9a27e828c3f3c7 | 421 | 6c16e1cc1f92 |
| G4-C1-consolidate_L3804.md | 3804 | 20:25:21 | rf-analyst | Consolidate Gate 4 fidelity findings | abce93f8bda095ffc | 423 | 26b82f1d3847 |
| G4-F1-fix_L3841.md | 3841 | 20:32:49 | rf-qa | Gate 4 fix agent cycle 1 | a48809ebd35041c6c | 425 | 48a68faecaff |
| G4-R2-verify-structural_L3883.md | 3883 | 20:34:47 | rf-qa | Gate 4 verification structural c1 | ad47ae857f5554ed0 | 427 | 31b2dd029a5d |
| G4-R2-verify-qualitative_L3887.md | 3887 | 20:34:51 | rf-qa-qualitative | Gate 4 verification qualitative c1 | a03cdb3e3d7f64f2e | 429 | 9eee4a0bb84e |
| G5-R1-anti-omission-agent-1_L3986.md | 3986 | 20:37:58 | rf-analyst | Gate 5 anti-omission agent 1 | a87955acf1ad1cbf7 | 449 | 5c12c82c5b4a |
| G5-R1-anti-omission-agent-2_L3990.md | 3990 | 20:38:01 | rf-analyst | Gate 5 anti-omission agent 2 | a01540c41f3b5932e | 451 | ea8af8e4e7bd |
| G5-R1-anti-omission-agent-3_L3994.md | 3994 | 20:38:05 | rf-analyst | Gate 5 anti-omission agent 3 | a2db640f53a99c857 | 453 | e615264698a3 |
| G5-R1-anti-omission-slice-1_L4031.md | 4031 | 20:48:52 | rf-analyst | Gate 5 anti-omission slice 1 | ac3949215dfcae1ea | 447 | 18c7119d4c83 |
| G5-C1-consolidate_L4113.md | 4113 | 21:00:37 | rf-analyst | Consolidate Gate 5 anti-omission findings | a457b91b6e2422e4a | 453 | 8563f272dc69 |
| G5-F1-fix_L4153.md | 4153 | 21:06:57 | rf-qa | Gate 5 fix agent cycle 1 | a16743412ab501355 | 455 | 1b338764d5b7 |
| G5-R2-verify-structural_L4196.md | 4196 | 21:13:42 | rf-qa | Gate 5 verification structural c1 | aaaca943419e896da | 457 | d401aca8335d |
| G5-R2-verify-qualitative_L4200.md | 4200 | 21:13:45 | rf-qa-qualitative | Gate 5 verification qualitative c1 | a75b34defa4ed1dbd | 459 | 6edc7b3fcfde |
| G5-F2-fix_L4299.md | 4299 | 21:21:33 | rf-qa | Gate 5 fix agent cycle 2 | abac12ba69dd639f3 | 465 | d42e6da8001a |
| G5-R3-verify-structural_L4342.md | 4342 | 21:23:22 | rf-qa | Gate 5 verification structural c2 | a909e73645aee2bfc | 467 | 09bb998bb328 |
| G5-R3-verify-qualitative_L4346.md | 4346 | 21:23:26 | rf-qa-qualitative | Gate 5 verification qualitative c2 | a51401fb49261a230 | 469 | ee12f8904a38 |
| Z-final-validation_L4631.md | 4631 | 21:48:01 | rf-qa | Final validation checklist Step 6.8 | ac7352b940df95a02 | 475 | 90d40b7a130a |
| S-skill-sc-workflow-protocol_L5109.json | 5109 | 21:56:59 | Skill | sc-workflow-protocol |  |  | ad820deb1e5b |
| S-skill-sc-reflect-protocol_L5306.json | 5306 | 21:59:17 | Skill | sc-reflect-protocol |  |  | 07d87af80071 |

## Embedded prompts (text between `BEGIN AGENT PROMPT.` and `END AGENT PROMPT.` on that task-file line, task file state `32d05845d5285d52@v2`)

| task-file line | file | used by | sha256[:12] |
|---|---|---|---|
| 193 | taskfile-L193_embedded-prompt.md | W1-research-01 | cae1ca173da6 |
| 197 | taskfile-L197_embedded-prompt.md | W1-research-02 | 77faea99b1bc |
| 201 | taskfile-L201_embedded-prompt.md | W1-research-03 | 0dc51e0d1e7d |
| 205 | taskfile-L205_embedded-prompt.md | W1-research-04 | 9c4feaf34720 |
| 209 | taskfile-L209_embedded-prompt.md | W1-research-05 | ef20b05be6d3 |
| 218 | taskfile-L218_embedded-prompt.md | G1-R1-analyst-completeness | a5f404701fb6 |
| 222 | taskfile-L222_embedded-prompt.md | G1-R1-rf-qa-evidence-quality | d00258317c3a |
| 226 | taskfile-L226_embedded-prompt.md | G1-R1-qualitative-research-depth | acef877b5a12 |
| 234 | taskfile-L234_embedded-prompt.md | G1-F1-fix | 46cb659670e4 |
| 238 | taskfile-L238_embedded-prompt.md | G1-R2-verify-structural | 07768c315d60 |
| 242 | taskfile-L242_embedded-prompt.md | G1-R2-verify-qualitative | aac8d46064d0 |
| 254 | taskfile-L254_embedded-prompt.md | G1-F2-fix | 0c64fa5076ee |
| 258 | taskfile-L258_embedded-prompt.md | G1-R3-verify-structural | 841f2f01cafe |
| 262 | taskfile-L262_embedded-prompt.md | G1-R3-verify-qualitative | 3513848660e0 |
| 270 | taskfile-L270_step-text-full-line.md | G1-X-gaps-log | 792209a86d04 |
| 279 | taskfile-L279_embedded-prompt.md | W2-web-01 | b30aac48d82b |
| 283 | taskfile-L283_embedded-prompt.md | W2-web-02 | 22842f13b6fa |
| 292 | taskfile-L292_embedded-prompt.md | W3-synth-01 | 591a03193582 |
| 296 | taskfile-L296_embedded-prompt.md | W3-synth-02 | 4a0025e73cb2 |
| 300 | taskfile-L300_embedded-prompt.md | W3-synth-03 | 172ef74ff052 |
| 304 | taskfile-L304_embedded-prompt.md | W3-synth-04 | d1599363b556 |
| 308 | taskfile-L308_embedded-prompt.md | G2-R1-analyst-synthesis-accuracy | 7ceb1daf4f12 |
| 312 | taskfile-L312_embedded-prompt.md | G2-R1-rf-qa-synthesis-structure | 994c9c528684 |
| 316 | taskfile-L316_embedded-prompt.md | G2-R1-qualitative-synthesis-coherence | 47297890badc |
| 320 | taskfile-L320_step-text-full-line.md | G2-C1-consolidate | f0cf0b630ec4 |
| 324 | taskfile-L324_embedded-prompt.md | G2-F1-fix | 70d66e462e9a |
| 328 | taskfile-L328_embedded-prompt.md | G2-R2-verify-structural | df38000902a6 |
| 332 | taskfile-L332_embedded-prompt.md | G2-R2-verify-qualitative | 9e937be303a5 |
| 344 | taskfile-L344_embedded-prompt.md | G2-F2-fix | 0a68fad6363f |
| 348 | taskfile-L348_embedded-prompt.md | G2-R3-verify-structural | da4d49635355 |
| 352 | taskfile-L352_embedded-prompt.md | G2-R3-verify-qualitative | 9f103950d0a2 |
| 365 | taskfile-L365_embedded-prompt.md | W4-assemble-report | b15158d4b79d |
| 371 | taskfile-L371_embedded-prompt.md | G3-R1-lens-template-conformance | c23a47e4df33 |
| 373 | taskfile-L373_embedded-prompt.md | G3-R1-lens-internal-consistency | fd76d39a2e6a |
| 375 | taskfile-L375_embedded-prompt.md | G3-R1-lens-evidence-quality | 9680408ed637 |
| 379 | taskfile-L379_embedded-prompt.md | G3-R1-lens-actionability | eb39d7bcd975 |
| 381 | taskfile-L381_embedded-prompt.md | G3-R1-lens-domain-accuracy | 83165cdc4862 |
| 383 | taskfile-L383_embedded-prompt.md | G3-R1-lens-crossref-chain | 22352035f8e7 |
| 387 | taskfile-L387_embedded-prompt.md | G3-R1-lens-finding-reproducibility | d77a0daed13b |
| 391 | taskfile-L391_step-text-full-line.md | G3-C1-consolidate | 3059f134d36a |
| 393 | taskfile-L393_embedded-prompt.md | G3-F1-fix | dfb7d0b36993 |
| 397 | taskfile-L397_embedded-prompt.md | G3-R2-verify-structural | a8762456ca31 |
| 399 | taskfile-L399_embedded-prompt.md | G3-R2-verify-qualitative | c123a393511e |
| 405 | taskfile-L405_embedded-prompt.md | G3-F2-fix | 6269f4565a09 |
| 407 | taskfile-L407_embedded-prompt.md | G3-R3-verify-structural | 971c9e23af40 |
| 409 | taskfile-L409_embedded-prompt.md | G3-R3-verify-qualitative | 44b04ff22c2a |
| 417 | taskfile-L417_embedded-prompt.md | G4-R1-fidelity-agent-1 | c0356fd8c811 |
| 419 | taskfile-L419_embedded-prompt.md | G4-R1-fidelity-agent-2 | 13125b492c41 |
| 421 | taskfile-L421_embedded-prompt.md | G4-R1-fidelity-agent-3-with-web-check | 0cb94c44e45e |
| 423 | taskfile-L423_step-text-full-line.md | G4-C1-consolidate | 8e79a02331c8 |
| 425 | taskfile-L425_embedded-prompt.md | G4-F1-fix | 688ad01a2133 |
| 427 | taskfile-L427_embedded-prompt.md | G4-R2-verify-structural | 1dad5d0eec4b |
| 429 | taskfile-L429_embedded-prompt.md | G4-R2-verify-qualitative | 70c647b17416 |
| 447 | taskfile-L447_embedded-prompt.md | G5-R1-anti-omission-slice-1 | 0296af5d1d7f |
| 449 | taskfile-L449_embedded-prompt.md | G5-R1-anti-omission-agent-1 | a20f27f360c8 |
| 451 | taskfile-L451_embedded-prompt.md | G5-R1-anti-omission-agent-2 | 6392ae253791 |
| 453 | taskfile-L453_step-text-full-line.md | G5-R1-anti-omission-agent-3, G5-C1-consolidate | 298a4a98178b |
| 455 | taskfile-L455_embedded-prompt.md | G5-F1-fix | 838aef152b5c |
| 457 | taskfile-L457_embedded-prompt.md | G5-R2-verify-structural | d3a69f5de06e |
| 459 | taskfile-L459_embedded-prompt.md | G5-R2-verify-qualitative | 7366bef3f2d6 |
| 465 | taskfile-L465_embedded-prompt.md | G5-F2-fix | 983fb52f01b6 |
| 467 | taskfile-L467_embedded-prompt.md | G5-R3-verify-structural | b77690c21418 |
| 469 | taskfile-L469_embedded-prompt.md | G5-R3-verify-qualitative | 8e689fded490 |
| 475 | taskfile-L475_step-text-full-line.md | Z-final-validation | 4ac605ee0290 |

## Notes

- The last two Skill rows (`sc-workflow-protocol` L5109, `sc-reflect-protocol` L5306) belong to the spec and plan work after the gates; they are listed for completeness and are not part of the replay.
- Not extracted: the prompts the Gate 1 fix agent (L841) wrote for its 6 gap researchers; they are agent-written. Their logs are the `G1-F1-fix-nested-*` rows of `../evidence/agent-costs.tsv`.
- The Gate 1 consolidation had no agent; its instruction is task-file line 230. The Gate 5 round 1 wrappers L3986, L3990, L3994 point at the wrong task-file lines (449, 451, 453; the prompts are on 447, 449, 451); this is recovered as it happened (`../ANALYSIS.md` section 8, finding 6).
- The wrapper text is written by the executor at run time; a replay session writes its own wrappers for the same task-file lines.
