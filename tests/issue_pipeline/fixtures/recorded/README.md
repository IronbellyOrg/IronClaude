# Recorded GitHub responses (plan Task 4, O-1)

Recorded on 2026-11-16 for issue 452 of IronbellyOrg/IronClaude, the one issue the owner named in `OWNER-INPUT.md` (`ISSUE: 452`). The issue is closed and was written by the owner. Every call below is a read-only GET, except the fixed edits GraphQL query (a POST that only reads, as `tests/issue_watch/test_security_invariants.py` already allows). No `jq` projection was passed, so each file is the raw response (pretty-printed with sorted keys; nothing else was changed).

| File | Call (argv shape of `src/superclaude/cli/issue_watch/github.py`) |
|---|---|
| `comments-page1.json` | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/452/comments -F per_page=100 -F page=1` (the shape `argv_comments` builds, without its `--jq`) |
| `events-page1.json` | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/452/events -F per_page=100 -F page=1` (the shape `argv_events` builds, without its `--jq`) |
| `edits-page1.json` | `gh api graphql -f query=<EDITS_QUERY> -F number=452` (the call `argv_edits(452)` builds; GraphQL, reads only) |

What the files show (field names, for the predicate and read tests):

- A comment has `id`, `user.login`, `user.id`, `user.type`, `created_at`, `updated_at`, `author_association` and `body`.
- An event has `id`, `event`, `actor.login`, `actor.id`, `actor.type`, `created_at` and, for a label event, `label.name`. This issue's events hold no label event: the kinds seen are `added_to_project_v2`, `project_v2_item_status_changed` (actor type `Bot`), `assigned`, `mentioned`, `subscribed` and `closed`.
- The edits reply holds `data.repository.issue.lastEditedAt`, and per comment `databaseId`, `author.login`, `createdAt` and `lastEditedAt` (all `null` here: nothing was edited).
- The recorded issue has no approval label, no plan reply and no `approved` comment, so label and approval-comment cases are covered by hand-built evidence in the tests; a field name still has to match these files, and FU-1 (Task 8) re-checks the label event and the web-editor comment on a live test issue.
