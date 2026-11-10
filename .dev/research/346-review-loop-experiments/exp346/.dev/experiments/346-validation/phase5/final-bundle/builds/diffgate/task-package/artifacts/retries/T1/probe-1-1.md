db07fea14a627a52c2878b0e2471960a2fb11bc0
family input-limits: defect form = an input limit defined but not enforced or miscounted
command: grep -n -e MAX_MACHINE_LINES -e MAX_LINES -e MAX_DOC_BYTES src/superclaude/skills/sc-diffgate/scripts/diffgate.py tests/skills/test_diffgate_script.py
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:38:MAX_DOC_BYTES = 2 * 1024 * 1024
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:39:MAX_LINES = 100_000
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:40:MAX_MACHINE_LINES = 1_000
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:93:    if len(data) > MAX_DOC_BYTES:
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:103:    if text.count("\n") + 1 > MAX_LINES:
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:106:            f"{what} over the {MAX_LINES} line limit: {path}",
before: tests/skills/test_diffgate_script.py:184:    big.write_text("x\n" * (dg.MAX_LINES + 5), encoding="utf-8")
coupled sites: read_text (line limit), _validate_inputs (reads report and map before dispatch), test_input_over_the_limits_exits_2
family test-discrimination: defect form = a test that passes whether or not the behaviour it names holds
command: grep -n -e autojunk src/superclaude/skills/sc-diffgate/scripts/diffgate.py tests/skills/test_diffgate_script.py
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:165:    sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
before: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:173:            None, [t.text for t in ot], [t.text for t in nt], autojunk=False
before: tests/skills/test_diffgate_script.py:152:    # default autojunk=True difflib would junk it and misalign the diff.
coupled sites: build_hunks line pass and token pass (both autojunk=False)
family test-comment: defect form = a test comment stating a false fact
command: grep -n -e chars -e characters tests/skills/test_diffgate_script.py
before: 107:    ]  # 75 * 4 chars = 300 characters with spaces
coupled sites: test_one_changed_word_in_long_line_gives_that_word_only
after (input-limits): src/superclaude/skills/sc-diffgate/scripts/diffgate.py:38:MAX_DOC_BYTES = 2 * 1024 * 1024 src/superclaude/skills/sc-diffgate/scripts/diffgate.py:39:MAX_LINES = 100_000 src/superclaude/skills/sc-diffgate/scripts/diffgate.py:40:MAX_MACHINE_LINES = 1_000 src/superclaude/skills/sc-diffgate/scripts/diffgate.py:93:    if len(data) > MAX_DOC_BYTES: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:103:    if len(text.splitlines()) > MAX_LINES: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:106:            f"{what} over the {MAX_LINES} line limit: {path}", src/superclaude/skills/sc-diffgate/scripts/diffgate.py:473:        if machine > MAX_MACHINE_LINES: src/superclaude/skills/sc-diffgate/scripts/diffgate.py:476:                f"report over the {MAX_MACHINE_LINES} machine line limit " tests/skills/test_diffgate_script.py:186:    big.write_text("x\n" * (dg.MAX_LINES + 5), encoding="utf-8") tests/skills/test_diffgate_script.py:191:    exact.write_text("x\n" * dg.MAX_LINES, encoding="utf-8") tests/skills/test_diffgate_script.py:192:    assert dg.read_text(exact).count("\n") == dg.MAX_LINES  # at the limit, not over tests/skills/test_diffgate_script.py:197:        * (dg.MAX_MACHINE_LINES + 1), 
after (test-discrimination): src/superclaude/skills/sc-diffgate/scripts/diffgate.py:165:    sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False) src/superclaude/skills/sc-diffgate/scripts/diffgate.py:173:            None, [t.text for t in ot], [t.text for t in nt], autojunk=False tests/skills/test_diffgate_script.py:152:    # input (321 lines) "same line" is a popular element, so autojunk=True tests/skills/test_diffgate_script.py:156:    junk = difflib.SequenceMatcher(None, base, new, autojunk=True) 
after (test-comment): 106:    words = [f"w{i:03d}" for i in range(60)]  # 60 words of 4 characters 107:    old_line = " ".join(words) + " " + "x" * 61  # 239 + 1 + 61 characters 
after (test-discrimination, final): 152:    # default autojunk=True reports one block replacing every line. 155:    junk = difflib.SequenceMatcher(None, base, new, autojunk=True).get_opcodes() 
after (test-comment, final): 106:    words = [f"w{i:03d}" for i in range(59)] + ["xxxxx"]  # 59*4 + 5 + 59 spaces 
