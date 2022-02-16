#/usr/bin/env bash
set -euo pipefail

#SCRIPT_NAME=$(basename "$0")
CURRENT_DIR_RELATIVE=$(dirname "$0")
CURRENT_DIR=$(cd "$CURRENT_DIR_RELATIVE" || exit 1;pwd)

pushd "$CURRENT_DIR" >/dev/null || exit 1
rc=0

for f in *.py; do
  echo ""
  echo "[$f]"
  /usr/bin/env python3 -m unittest $f --verbose
  rc=$?
  if [ "0" != "$rc" ]; then
    echo "Failed to run unittest for $f: $rc"
    exit 1
  else
    echo "Succeeded to run unittest for $f"
  fi
  echo ""
done

popd