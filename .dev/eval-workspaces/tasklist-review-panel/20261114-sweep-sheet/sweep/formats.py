"""Format dictionaries of the plan reader (DESIGN section 3, REQ-37, REQ-38). Data only: no function, no import.

One dictionary per document format (`plan`, `spec`, `doc`) says how each of the six block kinds is recognised.
Adding a format is adding one dictionary to FORMATS (or passing one to `plan.parse`); sweep/plan.py has no
format-specific text and does not change.

A dictionary has these keys (all optional except `kinds`):

  front_matter   True when a leading `---` block is front matter and is skipped
  heads          {class: regex}. Heading lines are tried in this order, the first match wins. Classes:
                 `task` (its groups `id` and `title` name the task; no `id` group numbers tasks 1, 2, ...),
                 `phase` (group `id`), and any other name a rule refers to with `under`
  label          regex of the line inside a task that ends its body and starts its criteria
  citation       {label: regex with group `cites`, tokens: regex with group `ref`}: the citation sentence of a task
  kinds          {kind: [rule, ...]} for the kinds task, criterion, constraint, dictated_text, edit_target, gate

A rule is a dictionary with a `mode` (the names in plan.MODES) and the options of that mode:

  task_body            the body of every task section, up to its label
  after_label          the bullets after a label line (option `label`, default the format's label)
  bullets              the top-level bullets of every section of class `under`; `fallback: "section"` takes the
                       whole section as one block when it holds no bullet
  section              the whole body of every section of class `under`
  line                 every line that matches `pattern`; a group `text` is the block text; `id` fixes the id
  sentences            every sentence of the prose, kept when it holds a word of `words`
  quoted_span          the double-quoted spans of at least `min` characters in sentences that hold a word of `words`
  blockquote           runs of lines that start with `>`
  fence                fenced blocks, filtered by `info` (allowed info words) and `skip_info`
  last_task_criteria   the criteria of the last task when its title or body holds a word of `words`
  matching             blocks of kind `of` whose text matches `pattern` (ids in `skip` are left out)

Common options: `in: "task"` keeps rules inside task sections, `part: "body"` or `"criteria"` keeps them in one
half of a task, `explode_paths: true` makes one block per path token (with `path` and `creates`).
`words` is the name of a list in sweep/words.py (or a list of names and words).
"""

DEFAULT = "plan"

# Path-like token: at least one `/`, then a file name with an extension, or a trailing `/`
PATH_TOKEN = (
    r"(?<![\w/.\-*])(?:[\w.\-*]+/)+(?:[\w\-*][\w.\-*]*\.[A-Za-z0-9*]+)?(?![\w/])"
)

# End of a sentence: a full stop, `!` or `?` (and closing marks) before whitespace and the start of a new sentence
SENTENCE_END = r"[.!?][\"')\]`”]*(?=\s+[\"'(\[`“A-Z])"

# Quoted spans: straight and curly double quotes (group `q` is the text between the quotes)
QUOTED_SPANS = (
    r"\"(?P<q>[^\"]+)\"",
    r"“(?P<q>[^”]+)”",
)

SHELL_INFO = ("bash", "sh", "shell", "console", "zsh")
TEXT_INFO = ("", "text", "txt", "md", "markdown")

CITATION = {
    "label": r"^\s*Source sections?\s*:\s*(?P<cites>.*)$",
    "tokens": r"(?:§\s*|\bsections?\s+)?(?P<ref>[A-Z]{1,3}-?\d+(?:\.\d+)*|\d+(?:\.\d+)*)",
}

_NUMBER = r"(?:\d+(?:\.\d+)*\.?\s+)?"

FORMATS = {
    # the workflow-plan format of this repository
    "plan": {
        "front_matter": True,
        "heads": {
            "phase": r"^#{2,3}\s+Phase\s+(?P<id>\w+)\s*[:.\-]?\s*(?P<title>.*)$",
            "task": r"^#{2,3}\s+Task\s+(?P<id>\d+(?:\.\d+)*)\s*[:.\-]?\s*(?P<title>.*)$",
            "constraint": r"^#{2,3}\s+Constraints?\b",
            "gate": r"^#{2,3}\s+(?:Gate|Final checks?)\b",
        },
        "label": r"^Acceptance criteria\s*:\s*$",
        "citation": CITATION,
        "kinds": {
            "task": [{"mode": "task_body"}],
            "criterion": [
                {"mode": "after_label", "in": "task"},
                {
                    "mode": "line",
                    "pattern": r"^Goal\s*:\s*(?P<text>\S.*)$",
                    "id": "goal",
                },
            ],
            "constraint": [{"mode": "bullets", "under": "constraint"}],
            "dictated_text": [
                {"mode": "blockquote", "in": "task", "part": "body"},
                {"mode": "fence", "in": "task", "part": "body"},
                {
                    "mode": "quoted_span",
                    "in": "task",
                    "part": "body",
                    "words": "dictation_verbs",
                    "min": 25,
                },
            ],
            "edit_target": [
                {
                    "mode": "sentences",
                    "in": "task",
                    "part": "body",
                    "words": ["edit_verbs", "create_verbs"],
                    "explode_paths": True,
                }
            ],
            "gate": [
                {
                    "mode": "last_task_criteria",
                    "words": [
                        "run",
                        "runs",
                        "running",
                        "check",
                        "checks",
                        "checking",
                        "verify",
                        "verifies",
                        "verifying",
                        "sync",
                        "syncs",
                        "syncing",
                    ],
                },
                {"mode": "bullets", "under": "gate", "fallback": "section"},
                {
                    "mode": "matching",
                    "of": "criterion",
                    "pattern": r"`[^`\n]*\b(?:pytest|make)\b[^`\n]*`",
                    "skip": ["goal"],
                },
            ],
        },
    },
    # a numbered specification (draft until real specification fixtures exist, IMPLEMENTATION step 6)
    "spec": {
        "front_matter": True,
        "heads": {
            "gate": rf"^#{{1,4}}\s+{_NUMBER}Verification\b",
            "affects": rf"^#{{1,4}}\s+{_NUMBER}Affect(?:s|ed)\b",
            "example": rf"^#{{1,4}}\s+{_NUMBER}(?:Examples?|Message format)\b",
            "task": r"^#{1,4}\s+(?P<id>\d+(?:\.\d+)*)\.?\s+(?P<title>\S.*)$",
        },
        "citation": CITATION,
        "kinds": {
            "task": [{"mode": "task_body"}],
            "criterion": [{"mode": "line", "pattern": r"\b(?:shall|must|should)\b"}],
            "constraint": [
                {
                    "mode": "line",
                    "pattern": r"\b(?:applies to|apply to|governs|binds|holds for)\s+(?:every|all|each)\b",
                }
            ],
            "dictated_text": [
                {"mode": "fence", "skip_info": SHELL_INFO},
                {"mode": "section", "under": "example"},
            ],
            "edit_target": [
                {"mode": "bullets", "under": "affects", "explode_paths": True},
                {
                    "mode": "after_label",
                    "label": r"^\s*(?:\*\*)?Affect(?:s|ed)(?:\*\*)?\s*:\s*(?:\*\*)?\s*$",
                    "explode_paths": True,
                },
            ],
            "gate": [{"mode": "bullets", "under": "gate", "fallback": "section"}],
        },
    },
    # a how-to or other documentation (draft until real documentation fixtures exist, IMPLEMENTATION step 6)
    "doc": {
        "front_matter": True,
        "heads": {"task": r"^#{1,4}\s+(?P<title>\S.*)$"},
        "kinds": {
            "task": [{"mode": "task_body"}],
            "criterion": [
                {
                    "mode": "sentences",
                    "in": "task",
                    "words": ["set_completeness", "set_universal"],
                },
                {"mode": "fence", "in": "task", "info": SHELL_INFO},
            ],
            "dictated_text": [{"mode": "fence", "in": "task", "info": TEXT_INFO}],
        },
    },
}
