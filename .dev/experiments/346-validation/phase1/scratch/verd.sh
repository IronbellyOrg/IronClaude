#!/bin/bash
# usage: verd.sh FILE [width] : lines of real msgs mentioning verdict FAIL/PASS, with a context snippet around the match
F="$1"; W="${2:-170}"
$(dirname $0)/txt.sh "$F" 100000 | rg -i -o "^[0-9]+\t(user|assistant)\t[^\t]*\t|.{0,60}verdict[^a-z]{0,14}(fail|pass).{0,$W}" | paste -sd' ' | sed 's/ \([0-9]\+\t\(user\|assistant\)\t\)/\n\1/g' | cut -c1-$((W+160))
