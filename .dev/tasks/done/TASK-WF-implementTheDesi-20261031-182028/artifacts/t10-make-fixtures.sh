#!/usr/bin/env bash
# Build slim Codex fixtures from the recorded live poll snapshots (read-only inputs).
# Codex-authored bodies are kept verbatim; other bodies are cut to 160 chars.
set -euo pipefail
A="$1"; OUT="$2"
slim='def cut: if (.body|type)=="string" then .body |= .[0:160] else . end;
  def codex: ((.user.login // .author.login // "") | startswith("chatgpt-codex-connector"));
  (.comments |= map(select(codex))) |
  (.reviews |= map(if codex then . else cut end)) |
  (.threads |= map(if (.comments.nodes[0] | codex) then . else (.comments.nodes[0] |= cut) end))'
marker_head='[.comments[] | select(.body|test("codex-review-state:v1")) | .body | capture("\"commit_sha\":\"(?<s>[0-9a-f]{40})\"").s][0]'
jq --arg prov "PR 334 poll snapshot 2026-10-31, head set to the Codex marker commit" \
  "$slim | .head_sha = ($marker_head) | ._provenance = \$prov" "$A/t7-pr334-snapshot.json" > "$OUT/codex-clean-pr334.json"
jq --arg prov "PR 336 poll snapshot 2026-10-31, head set to the Codex marker commit, Codex threads re-opened" \
  "$slim | .head_sha = ($marker_head) | (.threads |= map(if (.comments.nodes[0].author.login|startswith(\"chatgpt-codex\")) then .isResolved = false else . end)) | ._provenance = \$prov" \
  "$A/t7-pr336-snapshot.json" > "$OUT/codex-findings-pr336.json"
