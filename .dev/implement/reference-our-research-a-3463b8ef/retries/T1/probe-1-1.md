581eee20e6eff280e1326645bbc2aa81e08a52cb
family review-vs-depends: the review text claims an order or independence that the items' Depends lines contradict
 command: grep -n -e "Depends on items" -e "independent hardening" .dev/implement/reference-our-research-a-3463b8ef/issues/watcher.md
 before: 4 hits in watcher.md, 17 in coordinator.md
 coupled sites: aggregate/review.md points 2 and 4 and the Order list; the line label in gen.py
family parse-leak: section summary text swallowed by the last row of a section
 command: grep -n -e "features\. [0-9]* COVERED" .dev/implement/reference-our-research-a-3463b8ef/issues/coordinator.md
 before: 1 hit in coordinator.md
 coupled sites: aggregate/rows.json extra keys on the last row of several sections
after (A2 fix): family review-vs-depends: 0 hits of "Depends on items" in all three issue bodies (label is now "Related items"); review.md points 2, 4 and the Order list rewritten
after (A2 fix): family parse-leak: 0 hits of the section-summary text in the three issue bodies; rows.json has no summary-leak keys (checked with a regex for keys like "62 rows")
