581eee20e6eff280e1326645bbc2aa81e08a52cb tree=none
F1.1 resolved
F1.2 resolved
F2.1 resolved
T1.AC1 unmet T1.AC1@aggregate/review.md:10 and T1.AC1@aggregate/review.md:9 (behind F2.2 F2.3 F2.4); the rest of T1.AC1 met (sections/section-01.md to section-14.md, aggregate/rows.json, issues/*.md)
F2.2 sev=blocking trigger=B2 ac=T1.AC1 at=issues/watcher.md:181 anchor=issues/watcher.md:108 chk=n,y,n,n family=review-vs-items fix=move W4 and W9 behind the live capture and say W7 and W13 wait for their triggers first=A2 origin=fix-induced: the review orders W4 and W9 before the coordinator work, but the items say not to build before real GitHub replies are captured
F2.3 sev=blocking trigger=B2 ac=T1.AC1 at=issues/dashboard.md:70 anchor=issues/dashboard.md:41 chk=n,y,n,n family=review-vs-items fix=say D3 starts with an owner decision and then needs a config change and a test first=A2 origin=fix-induced: the review says D3 is only an owner decision but its done-when asks for a config change and a test
F2.4 sev=blocking trigger=B2 ac=T1.AC1 at=issues/dashboard.md:70 anchor=issues/dashboard.md:51 chk=n,y,n,n family=review-vs-items fix=say D4 has a part that can be done now and a diff check that waits for the restore first=A2 origin=fix-induced: the review says D4 cannot be built before the restore, but D4's done-when can run while the skill is absent
F2.5 sev=minor ac=scope at=issues/coordinator.md:420 chk=n,n,n,n family=review-vs-items: C14 and the entry line of C8 need the same report-skill decision as D1, D2, D4 but the review did not list them
