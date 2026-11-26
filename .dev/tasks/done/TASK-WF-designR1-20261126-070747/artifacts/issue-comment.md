Status: not posted (needs the owner's approval)

No comment was posted on issue 826. Posting on the issue is an outward action; approval of a scratch repository is not approval to post, and the owner has given neither in this session.

The ready command (run from this package folder; it posts the local rehearsal log followed by the GitHub rehearsal status, once):

```bash
gh issue comment 826 --repo IronbellyOrg/IronClaude --body-file ./artifacts/issue-comment-body.md
```

After posting, record the comment URL on a line below this text.

Until the comment is posted and a GitHub-side rehearsal is run with the owner's approval, issue 826's rehearsal criterion ("a release rehearsal goes from `integration` to `master` following only the written steps") stays partly met: the git half was rehearsed locally, the GitHub half was not exercised.
