2aab5a6c5929cd103f6e1043773364232a5bf8a5
family=m1-pin-red-on-head
defect: a pin listed under the M-1 bullet passes on the pre-change retry.md, so it cannot show red there
command: grep -n -F -e anchors-once -e ANCHOR_START -e ANCHOR_END -- tests/skills/test_implement_launch_alias.py
before:
40:ANCHOR_START = "**Escalation rule.**"
41:ANCHOR_END = "Worked example with the fallback ladder:"
65:    return _between(text, ANCHOR_START, ANCHOR_END, include_end=True)
73:    i = text.find(ANCHOR_END)
77:    for ln in text[i + len(ANCHOR_END) :].splitlines():
128:    "anchors-once": lambda t: t.count(ANCHOR_START) == 1 and t.count(ANCHOR_END) == 1,
182:        " " + ANCHOR_END,
183:        " Adviser B is spawned on `gpt-6.1-sol`. " + ANCHOR_END,
coupled sites: _region() (builds the region the two region pins read), the red check script output .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/t6-red-check.txt (re-recorded after the fix)

family=launch-label-line-start
defect: the Launch alias paragraph is found by a substring search anywhere in the file, not as a line start inside the Model ladder section
command: grep -n -F -e Launch\ alias -e _launch -- tests/skills/test_implement_launch_alias.py
before:
1:"""Launch alias of the retry-ladder advisers of sc-implement-protocol (issue 393).
60:def _launch(text: str) -> str:
61:    return _between(text, "**Launch alias.**", "### Cost and caps")
118:    "launch-rule": lambda t: RULE_PHRASE in _launch(t),
119:    "takes-only": lambda t: TAKES_ONLY in _launch(t),
120:    "never-full-id": lambda t: "never a full model id" in _launch(t),
121:    "family-fallback-token": lambda t: "`family-fallback: <reason>`" in _launch(t),
122:    "launch-header": lambda t: HEADER_FORM in _launch(t),
124:        bool(_launch(t))
125:        and not any(ln.startswith("GPT spawn path: ") for ln in _launch(t).splitlines())
127:    "alias-count": lambda t: _alias_count_ok(_launch(t)),
131:        bool(_launch(t))
133:        and not MODEL_ID.search(_launch(t))
140:        and "the header form given under Launch alias below" in _line_resolving_b(t)
442:def _raw_id_launch(tier: str, env: Env) -> dict[str, Pick]:
465:    [_raw_id_launch, _never_family_fallback, _t2model01_one_rung_up],
coupled sites: _launch() (every launch pin reads it), the module docstring line that names the paragraph

family=lint-type-evidence
defect: the ruff and mypy results the ACs ask for have no recorded evidence file
command: grep -n -i -E -e ruff -e mypy -- .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/retries/T6/prompt-1-1.md .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/t6-red-check.txt .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/t6-test.log
before:
.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/retries/T6/prompt-1-1.md:26:- The test file does not read `os.environ`, does not import `ALI
.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/retries/T6/prompt-1-1.md:27:- `uv run mypy tests/skills/test_implement_launch_alias.py` repo
(only the saved prompt mentions them; no result is recorded)
coupled sites: ./artifacts/t6-lint.log (new, holds both outputs)

after: family=m1-pin-red-on-head
after: 40:ANCHOR_START = "**Escalation rule.**"
after: 41:ANCHOR_END = "Worked example with the fallback ladder:"
after: 73:    if text.count(ANCHOR_START) != 1 or text.count(ANCHOR_END) != 1:
after: 75:    return _between(text, ANCHOR_START, ANCHOR_END, include_end=True)
after: 79:    i = text.find(ANCHOR_END)
after: 83:    for ln in text[i + len(ANCHOR_END) :].splitlines():
after: 187:        " " + ANCHOR_END,
after: 188:        " Adviser B is spawned on `gpt-6.1-sol`. " + ANCHOR_END,
after: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/t6-red-check.txt shows 'every pin fails on HEAD: yes'
after: family=launch-label-line-start
after: 67:    m = re.search(r"^\*\*Launch alias\.\*\*", sec, re.MULTILINE)
after: family=lint-type-evidence
after: 3:rc=0
after: 6:rc=0
after: 9:rc=0
