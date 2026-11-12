8fc83479317c38b204ad28b696ba32606601e4a5 tree=aa7386e7657b5cb0917c169956ff9c2c3beec684
T17.AC1 unmet (F1.1 F1.2 F1.3)
T17.AC2 unmet (F1.1 F1.4)
F1.1 F1.2 F1.3 F1.4 open after the A2 fix pass (see review-1.md for the finding lines). The unmet marks follow from the plan text: the plan expects an owner-named Run and a template-only argv log; the owner instead told the executor to choose its own Run. The fix pass could only relabel the departure honestly.
