681a7a5b17599131b735aee558a8d7b80726f372
family gh-repo-flag: a statement that every gh call passes --repo, where a gh api call names the repo in its path
  cmd: grep -n -e "--repo" -e "gh api" docs/designs/issue-pipeline-fu1.md
  coupled sites: section 3 bullet on gh calls; steps j and k
family recipe-placeholder: a step with an unspecified placeholder that the verb rejects
  cmd: grep -n -e "<record id>" -e "<hash>" docs/designs/issue-pipeline-fu1.md
  coupled sites: step e
family dangling-ref: a reference to a step number that does not exist
  cmd: grep -n -e "step 0" -e "before step" docs/designs/issue-pipeline-fu1.md
  coupled sites: section 2
