f6effbac955b52b796278cdf09476ba869788cbb
family height-rule: the layout choice measured the panes more than once per layout.
search: grep -n -F -e "plan(" src/superclaude/cli/observe/render.py
before: plan() called in two passes over three layouts
coupled sites: none
after: one call per layout, at most three
family width-80-text: the 80 column count line lost its short form.
search: grep -n -F -e screen_counts_line src/superclaude/cli/observe/view.py src/superclaude/cli/observe/render.py
before: no hit (the field was removed)
coupled sites: the constant QUESTIONS_CLOSED_SCREEN in view.py
after: the field and the constant are back; only the 80 column list line uses them
