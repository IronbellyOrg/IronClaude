55c06cbabbe4d732e0fac71f24a2ad818d8a7024
family=claim-url-schemeless
defect form: a URL-shaped claim argument without the https scheme (github.com/..., www.github.com/..., git@github.com:...) is classified by a branch the docstring does not describe, so the code, the message and the docstring disagree
command: grep -n -e E-FOREIGN-REPO -e github.com/ -e git@ src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py tests/skills/test_issue_repo_resolution.py
before:
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:18:    https://github.com/<owner>/<repo>
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:19:    https://github.com/<owner>/<repo>.git
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:20:    git@github.com:<owner>/<repo>
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:21:    git@github.com:<owner>/<repo>.git
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:25:    ``https://github.com/<origin>/issues/302``  -> N = 302; a trailing ``/``,
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:28:    a URL naming any other owner or repo        -> E-FOREIGN-REPO
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:33:    ``https://github.com/<origin>/pull/302``    -> E-NOT-AN-ISSUE
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:42:    3  E-FOREIGN-REPO  the claim URL names a repository other than origin
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:61:    re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:95:    Raises ``ClaimError`` with ``E-FOREIGN-REPO`` or ``E-NOT-AN-ISSUE``.
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:104:        if "://" in arg or arg.lower().startswith(("git@", "github.com/", "www.github.com/")):
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:106:                "E-FOREIGN-REPO",
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:119:            "E-FOREIGN-REPO", EXIT_FOREIGN_REPO, f"{arg} names no repository"
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:127:            "E-FOREIGN-REPO",
  tests/skills/test_issue_repo_resolution.py:32:        "https://github.com/IronbellyOrg/IronClaude",  # https
  tests/skills/test_issue_repo_resolution.py:33:        "https://github.com/IronbellyOrg/IronClaude.git",  # https + .git suffix
  tests/skills/test_issue_repo_resolution.py:34:        "https://github.com/IronbellyOrg/IronClaude/",  # https + trailing /
  tests/skills/test_issue_repo_resolution.py:35:        "https://github.com/IronbellyOrg/IronClaude.git/",  # .git + trailing /
  tests/skills/test_issue_repo_resolution.py:36:        "git@github.com:IronbellyOrg/IronClaude",  # ssh
  tests/skills/test_issue_repo_resolution.py:37:        "git@github.com:IronbellyOrg/IronClaude.git",  # ssh + .git suffix
  tests/skills/test_issue_repo_resolution.py:38:        "git@github.com:IronbellyOrg/IronClaude/",  # ssh + trailing /
  tests/skills/test_issue_repo_resolution.py:39:        "https://github.com/IronbellyOrg/IronClaude\n",  # git output newline
  tests/skills/test_issue_repo_resolution.py:50:        "git@bitbucket.org:IronbellyOrg/IronClaude.git",
  tests/skills/test_issue_repo_resolution.py:51:        "https://github.com/IronbellyOrg",
  tests/skills/test_issue_repo_resolution.py:102:    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
  tests/skills/test_issue_repo_resolution.py:110:    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
  tests/skills/test_issue_repo_resolution.py:111:    _git(repo, "remote", "add", "origin", "git@github.com:IronbellyOrg/IronClaude.git")
  tests/skills/test_issue_repo_resolution.py:120:    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
  tests/skills/test_issue_repo_resolution.py:121:    result = _run(repo, "--claim", "https://github.com/IronbellyOrg/IronClaude/issues/302")
  tests/skills/test_issue_repo_resolution.py:128:    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
  tests/skills/test_issue_repo_resolution.py:129:    result = _run(repo, "--claim", "https://github.com/octocat/Hello-World/issues/1")
  tests/skills/test_issue_repo_resolution.py:132:    assert "E-FOREIGN-REPO" in result.stderr
  tests/skills/test_issue_repo_resolution.py:149:# --- claim argument versus origin (E-FOREIGN-REPO, design section 20 item 4) --
  tests/skills/test_issue_repo_resolution.py:157:        ("https://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # same repo
  tests/skills/test_issue_repo_resolution.py:158:        ("https://github.com/ironbellyorg/ironclaude/issues/302", 302),  # case-insensitive
  tests/skills/test_issue_repo_resolution.py:159:        ("https://github.com/IronbellyOrg/IronClaude/issues/302/", 302),  # trailing /
  tests/skills/test_issue_repo_resolution.py:160:        ("https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9", 302),  # fragment
  tests/skills/test_issue_repo_resolution.py:161:        ("https://github.com/IronbellyOrg/IronClaude/issues/302?x=1", 302),  # query
  tests/skills/test_issue_repo_resolution.py:171:        "https://github.com/octocat/IronClaude/issues/1",  # foreign owner
  tests/skills/test_issue_repo_resolution.py:172:        "https://github.com/IronbellyOrg/OtherRepo/issues/1",  # same owner, different repo
  tests/skills/test_issue_repo_resolution.py:173:        "https://github.com/IronbellyOrg/IronClaudeX/issues/1",  # repo-name prefix
  tests/skills/test_issue_repo_resolution.py:174:        "https://github.com/IronbellyOrg/IronClaud/issues/1",  # origin repo is a prefix of it
  tests/skills/test_issue_repo_resolution.py:175:        "https://github.com/IronbellyOrgX/IronClaude/issues/1",  # owner-name prefix
  tests/skills/test_issue_repo_resolution.py:176:        "https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999",
  tests/skills/test_issue_repo_resolution.py:178:        "https://github.com/IronbellyOrg",  # no repository
  tests/skills/test_issue_repo_resolution.py:184:    assert exc.value.code == "E-FOREIGN-REPO"
  tests/skills/test_issue_repo_resolution.py:191:        "https://github.com/IronbellyOrg/IronClaude/pull/302",
  tests/skills/test_issue_repo_resolution.py:192:        "https://github.com/IronbellyOrg/IronClaude/pull/302/",
  tests/skills/test_issue_repo_resolution.py:193:        "https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1",
  tests/skills/test_issue_repo_resolution.py:205:        orr.check_claim("https://github.com/octocat/Hello-World/pull/302", ORIGIN)
  tests/skills/test_issue_repo_resolution.py:206:    assert exc.value.code == "E-FOREIGN-REPO"
  tests/skills/test_issue_repo_resolution.py:212:        ("Org302/Repo456", "https://github.com/Org302/Repo456"),
  tests/skills/test_issue_repo_resolution.py:213:        ("Org302/Repo456", "https://github.com/Org302/Repo456/"),
  tests/skills/test_issue_repo_resolution.py:214:        ("Org302/Repo456", "https://github.com/Org302/Repo456/issues"),
  tests/skills/test_issue_repo_resolution.py:215:        ("IronbellyOrg/IronClaude302", "https://github.com/IronbellyOrg/IronClaude302/tree/main"),
  tests/skills/test_issue_repo_resolution.py:225:    assert orr.check_claim("https://github.com/Org302/Repo456/issues/7", "Org302/Repo456") == 7
  tests/skills/test_issue_repo_resolution.py:236:        "https://github.com/IronbellyOrg/IronClaude/issues/abc",
  tests/skills/test_issue_repo_resolution.py:237:        "https://github.com/IronbellyOrg/IronClaude/issues/302/comments",
coupled sites: origin_repo.py module docstring claim-argument rules (lines 23-36), check_claim's non-URL branch (lines 99-111), the _GITHUB_URL pattern (line 61); test_claim_url_on_another_repo_is_e_foreign_repo and test_claim_on_origin_returns_issue_number
after:
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:18:    https://github.com/<owner>/<repo>
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:19:    https://github.com/<owner>/<repo>.git
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:20:    git@github.com:<owner>/<repo>
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:21:    git@github.com:<owner>/<repo>.git
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:25:    ``https://github.com/<origin>/issues/302``  -> N = 302; a trailing ``/``,
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:28:    a GitHub URL naming any other owner or      -> E-FOREIGN-REPO
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:33:    a URL (``<scheme>://...`` or               -> E-FOREIGN-REPO
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:34:    ``git@<host>:...``) on any host other
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:36:    ``https://github.com/<origin>/pull/302``    -> E-NOT-AN-ISSUE
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:41:``www.``, and may be written ``git@github.com:<owner>/<repo>/...``; every form
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:49:    3  E-FOREIGN-REPO  the claim URL names a repository other than origin
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:68:    re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:71:    r"^(?:(?:https?://)?(?:www\.)?github\.com/|git@github\.com:)(?P<path>[^?#]*)",
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:105:    Raises ``ClaimError`` with ``E-FOREIGN-REPO`` or ``E-NOT-AN-ISSUE``.
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:114:        if "://" in arg or arg.lower().startswith("git@"):
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:116:                "E-FOREIGN-REPO",
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:129:            "E-FOREIGN-REPO", EXIT_FOREIGN_REPO, f"{arg} names no repository"
  src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:137:            "E-FOREIGN-REPO",
  tests/skills/test_issue_repo_resolution.py:32:        "https://github.com/IronbellyOrg/IronClaude",  # https
  tests/skills/test_issue_repo_resolution.py:33:        "https://github.com/IronbellyOrg/IronClaude.git",  # https + .git suffix
  tests/skills/test_issue_repo_resolution.py:34:        "https://github.com/IronbellyOrg/IronClaude/",  # https + trailing /
  tests/skills/test_issue_repo_resolution.py:35:        "https://github.com/IronbellyOrg/IronClaude.git/",  # .git + trailing /
  tests/skills/test_issue_repo_resolution.py:36:        "git@github.com:IronbellyOrg/IronClaude",  # ssh
  tests/skills/test_issue_repo_resolution.py:37:        "git@github.com:IronbellyOrg/IronClaude.git",  # ssh + .git suffix
  tests/skills/test_issue_repo_resolution.py:38:        "git@github.com:IronbellyOrg/IronClaude/",  # ssh + trailing /
  tests/skills/test_issue_repo_resolution.py:39:        "https://github.com/IronbellyOrg/IronClaude\n",  # git output newline
  tests/skills/test_issue_repo_resolution.py:50:        "git@bitbucket.org:IronbellyOrg/IronClaude.git",
  tests/skills/test_issue_repo_resolution.py:51:        "https://github.com/IronbellyOrg",
  tests/skills/test_issue_repo_resolution.py:102:    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
  tests/skills/test_issue_repo_resolution.py:110:    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
  tests/skills/test_issue_repo_resolution.py:111:    _git(repo, "remote", "add", "origin", "git@github.com:IronbellyOrg/IronClaude.git")
  tests/skills/test_issue_repo_resolution.py:120:    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
  tests/skills/test_issue_repo_resolution.py:121:    result = _run(repo, "--claim", "https://github.com/IronbellyOrg/IronClaude/issues/302")
  tests/skills/test_issue_repo_resolution.py:128:    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
  tests/skills/test_issue_repo_resolution.py:129:    result = _run(repo, "--claim", "https://github.com/octocat/Hello-World/issues/1")
  tests/skills/test_issue_repo_resolution.py:132:    assert "E-FOREIGN-REPO" in result.stderr
  tests/skills/test_issue_repo_resolution.py:149:# --- claim argument versus origin (E-FOREIGN-REPO, design section 20 item 4) --
  tests/skills/test_issue_repo_resolution.py:157:        ("https://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # same repo
  tests/skills/test_issue_repo_resolution.py:158:        ("https://github.com/ironbellyorg/ironclaude/issues/302", 302),  # case-insensitive
  tests/skills/test_issue_repo_resolution.py:159:        ("https://github.com/IronbellyOrg/IronClaude/issues/302/", 302),  # trailing /
  tests/skills/test_issue_repo_resolution.py:160:        ("https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9", 302),  # fragment
  tests/skills/test_issue_repo_resolution.py:161:        ("https://github.com/IronbellyOrg/IronClaude/issues/302?x=1", 302),  # query
  tests/skills/test_issue_repo_resolution.py:162:        ("http://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # http scheme
  tests/skills/test_issue_repo_resolution.py:163:        ("github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme
  tests/skills/test_issue_repo_resolution.py:164:        ("www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme, www.
  tests/skills/test_issue_repo_resolution.py:165:        ("https://www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # www.
  tests/skills/test_issue_repo_resolution.py:166:        ("git@github.com:IronbellyOrg/IronClaude/issues/302", 302),  # git@ form
  tests/skills/test_issue_repo_resolution.py:176:        "https://github.com/octocat/IronClaude/issues/1",  # foreign owner
  tests/skills/test_issue_repo_resolution.py:177:        "https://github.com/IronbellyOrg/OtherRepo/issues/1",  # same owner, different repo
  tests/skills/test_issue_repo_resolution.py:178:        "https://github.com/IronbellyOrg/IronClaudeX/issues/1",  # repo-name prefix
  tests/skills/test_issue_repo_resolution.py:179:        "https://github.com/IronbellyOrg/IronClaud/issues/1",  # origin repo is a prefix of it
  tests/skills/test_issue_repo_resolution.py:180:        "https://github.com/IronbellyOrgX/IronClaude/issues/1",  # owner-name prefix
  tests/skills/test_issue_repo_resolution.py:181:        "https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999",
  tests/skills/test_issue_repo_resolution.py:183:        "https://github.com/IronbellyOrg",  # no repository
  tests/skills/test_issue_repo_resolution.py:184:        "github.com/octocat/Hello-World/issues/1",  # no scheme, foreign
  tests/skills/test_issue_repo_resolution.py:185:        "www.github.com/IronbellyOrg/IronClaudeX/issues/1",  # no scheme, prefix
  tests/skills/test_issue_repo_resolution.py:186:        "git@github.com:octocat/Hello-World.git",  # git@ form, foreign
  tests/skills/test_issue_repo_resolution.py:187:        "git@bitbucket.org:IronbellyOrg/IronClaude.git",  # git@ form, not GitHub
  tests/skills/test_issue_repo_resolution.py:193:    assert exc.value.code == "E-FOREIGN-REPO"
  tests/skills/test_issue_repo_resolution.py:200:        "https://github.com/IronbellyOrg/IronClaude/pull/302",
  tests/skills/test_issue_repo_resolution.py:201:        "https://github.com/IronbellyOrg/IronClaude/pull/302/",
  tests/skills/test_issue_repo_resolution.py:202:        "https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1",
  tests/skills/test_issue_repo_resolution.py:214:        orr.check_claim("https://github.com/octocat/Hello-World/pull/302", ORIGIN)
  tests/skills/test_issue_repo_resolution.py:215:    assert exc.value.code == "E-FOREIGN-REPO"
  tests/skills/test_issue_repo_resolution.py:221:        ("Org302/Repo456", "https://github.com/Org302/Repo456"),
  tests/skills/test_issue_repo_resolution.py:222:        ("Org302/Repo456", "https://github.com/Org302/Repo456/"),
  tests/skills/test_issue_repo_resolution.py:223:        ("Org302/Repo456", "https://github.com/Org302/Repo456/issues"),
  tests/skills/test_issue_repo_resolution.py:224:        ("IronbellyOrg/IronClaude302", "https://github.com/IronbellyOrg/IronClaude302/tree/main"),
  tests/skills/test_issue_repo_resolution.py:234:    assert orr.check_claim("https://github.com/Org302/Repo456/issues/7", "Org302/Repo456") == 7
  tests/skills/test_issue_repo_resolution.py:245:        "https://github.com/IronbellyOrg/IronClaude/issues/abc",
  tests/skills/test_issue_repo_resolution.py:246:        "https://github.com/IronbellyOrg/IronClaude/issues/302/comments",
  tests/skills/test_issue_repo_resolution.py:247:        "github.com/IronbellyOrg/IronClaude",  # origin, no scheme, no issue path
  tests/skills/test_issue_repo_resolution.py:248:        "git@github.com:IronbellyOrg/IronClaude.git",  # origin remote URL, no issue path
