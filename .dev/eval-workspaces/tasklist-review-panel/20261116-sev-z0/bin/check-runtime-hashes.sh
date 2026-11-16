#!/usr/bin/env bash
# Compare config/runtime-hashes.json with the files now (path per changed file, exit 1 on any difference). No git, no model.
set -u -o pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 2
rc=0
while IFS=$'\t' read -r f want; do
  got=$(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)
  [ "$got" = "$want" ] || { echo "CHANGED $f"; rc=1; }
done < <(jq -r '.files | to_entries[] | [.key, .value] | @tsv' config/runtime-hashes.json)
[ $rc = 0 ] && echo "runtime hashes match $(jq '.files|length' config/runtime-hashes.json) files"
exit $rc
