b0c108f0b013dfe9fb8c39a63c81db0363faee02
A1 r1-1 F1.1 note tests/observe/test_render.py:33 ac=T18.AC1 amiss:n,false:n,harm:n,constraint:n the frame-aware reads go through one screen_lines wrapper that turns each top border into its title row, so the desk checks still read DESK_TITLE in lines (equivalent to title_of); title_of is used where a test needs the border titles
A1 r1-1 F1.2 note tests/observe/test_height_budget.py:30 ac=T18.AC1 amiss:n,false:n,harm:n,constraint:n the diagnostic height 8 allows 4 rows over while scores.json says up to 3; height 8 is not a guaranteed height
