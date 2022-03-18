#/usr/bin/env bash
set -euo pipefail

#SCRIPT_NAME=$(basename "$0")
CURRENT_DIR_RELATIVE=$(dirname "$0")
CURRENT_DIR=$(cd "$CURRENT_DIR_RELATIVE" || exit 1;pwd)

pushd "$CURRENT_DIR" >/dev/null || exit 1
rc=0

declare -A targets=(
        ["logger"]="$CURRENT_DIR/test_logger.py"
        ["notifier"]="$CURRENT_DIR/test_notifier.py"
        ["cifs_os_copier"]="$CURRENT_DIR/test_cifs_os_copier.py"
)

function show_help(){
  echo "以下のいずれかを指定してください"
  for target in "${!targets[@]}"; do
    echo "${target}"
  done
}


if [ $# -eq 0 ]; then
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
else
  matched=0
  arg_target=$1
  for target in "${!targets[@]}"; do
    if [ -n "${targets["$arg_target"]-}" ]; then
      /usr/bin/env python3 -m unittest ${targets["$arg_target"]} --verbose
      rc=$?
      if [ "0" != "$rc" ]; then
        echo "Failed to run unittest for $target: $rc"
        exit 1
      else
        echo "Succeeded to run unittest for $target"
      fi

      matched=1
      break
    fi
  done
  if [ "$matched" -eq 0 ]; then
    show_help
    exit 1
  fi
fi

popd 1>/dev/null
exit 0