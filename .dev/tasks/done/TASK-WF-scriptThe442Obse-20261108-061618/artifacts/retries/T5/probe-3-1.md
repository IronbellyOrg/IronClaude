6fdae45fcfb2d8f73b7acb9b87a530ab57ee0517

# Family probe probe-3-1.md (failing review r3-1)

## family: body-text-fidelity
defect form: a template fill that paraphrases the runbook's required body text instead of carrying it verbatim, dropping the "Touch nothing else. Close without merging anything." instruction; and a test that never reads the body file, so the drop cannot be seen.
search command: grep -n -F -e 'Nothing yet' -e 'to be created' -e 'single line' -e 'not inspect the template' -e 'issue create' -- .dev/issues/442/scripts/setup-github.sh .dev/issues/442/scripts/setup-github-selftest.sh .dev/issues/442/scripts/selftest.sh
before-output (touched files):
  setup-github.sh:22: sed fill of "what was tried" = "Nothing yet: this is a disposable target ..." (paraphrase)
  setup-github.sh:23: "relevant files" = "ob-442/$t.txt (to be created)"
  setup-github.sh:24: "done when" = "ob-442/$t.txt exists holding the single line: ob-442 $t" (drops "The only change wanted", "Touch nothing else", "Close without merging anything")
  setup-github.sh:27: the create call uses --body-file "$tpl"
  setup-github-selftest.sh:71: comment says the test does not inspect the template content
  setup-github-selftest.sh:72: only counts `issue create` calls
  selftest.sh:66: the gh stub 'issue create' arm prints a URL and never reads the body file
coupled sites: setup-github.sh:25 (the fourth section fill, unchanged); setup-github-selftest.sh:70-71 (the comment must stay true after the test starts reading the body); selftest.sh:63-71 (the gh stub must capture the body file for the test to read).
after:
  setup-github.sh:22-25: the four sections carry the runbook's body sentences verbatim ("Disposable target for the #442 live observations ($t)." under what was tried; "The only change wanted: create the file ob-442/$t.txt holding the single line ob-442 $t. Touch nothing else. Close without merging anything." under done when).
  selftest.sh gh stub: copies the --body-file content to $L/bodies.txt on issue create.
  setup-github-selftest.sh: new case asserts four copies of the runbook sentence "Touch nothing else. Close without merging anything." and no remaining angle-bracket placeholder in the captured bodies; the 70-71 comment is rewritten to match.
