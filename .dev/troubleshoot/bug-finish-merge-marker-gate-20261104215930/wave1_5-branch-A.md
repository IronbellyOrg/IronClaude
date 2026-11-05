# Wave 1.5 Branch A (release docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

- release_slug: none under .dev/releases/ (controlling artifact: design package TASK-WF-design-20261104-164423 in .dev/tasks/done/)
- artifact_paths: [.dev/tasks/done/TASK-WF-design-20261104-164423/source.md]
- summary: Section 7.2 specifies finish-merge.sh commit step 4 as counting lines matching a fixed 7-character pattern `^(<{7}|\|{7}|={7}|>{7})( |$)` (index blob vs stage-1 blob) and step 5 as comparing index blob vs merge-tree blob by rev-parse blob id for non-manifest paths. Neither mentions the conflict-marker-size gitattribute or file mode, so both findings are design gaps the script follows faithfully. Mode changes are a Wave 0 halt only for the probed conflicted paths; nothing covers a mode change on an auto-merged path outside the manifest.
- confidence: 0.7
