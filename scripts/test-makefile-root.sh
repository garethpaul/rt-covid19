#!/usr/bin/env sh
set -eu
ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TEMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/rt-covid19-root-control-XXXXXX")
ATTACKER_ROOT="$TEMP_ROOT/attacker-root"
trap 'rm -rf "$TEMP_ROOT"' EXIT HUP INT TERM
unset MAKEFILES MAKEFILE_LIST
CONTROL_DIR="$TEMP_ROOT/control"
CHECKOUT="$TEMP_ROOT/Rt Covid's [gate] \"quoted\" \`touch RT_COVID19_BACKTICK_MARKER\`"
COMMAND_LOG="$TEMP_ROOT/commands.log"
BAD_COMMAND_LOG="$TEMP_ROOT/bad-command.log"
FAKE_SHELL_LOG="$TEMP_ROOT/fake-shell.log"
mkdir "$CONTROL_DIR" "$CHECKOUT" "$CHECKOUT/scripts" "$CHECKOUT/bin" "$ATTACKER_ROOT"
CHECKOUT=$(CDPATH= cd -- "$CHECKOUT" && pwd -P)
MAKEFILE="$CHECKOUT/Makefile"
cp "$ROOT_DIR/Makefile" "$MAKEFILE"
cat >"$CHECKOUT/bin/python3" <<'EOF'
#!/bin/sh
printf '%s|%s|%s\n' "$PWD" "$0" "$*" >> "$RT_COVID19_COMMAND_LOG"
if [ -n "${RT_COVID19_FAIL_PATTERN:-}" ]; then
  case "$*" in
    *"$RT_COVID19_FAIL_PATTERN"*) printf 'injected failure for python3 %s\n' "$*" >&2; exit 70 ;;
  esac
fi
exit 0
EOF
cat >"$CHECKOUT/scripts/test-makefile-root.sh" <<'EOF'
#!/bin/sh
printf '%s|%s|root-test\n' "$PWD" "$0" >> "$RT_COVID19_COMMAND_LOG"
EOF
chmod +x "$CHECKOUT/bin/python3" "$CHECKOUT/scripts/test-makefile-root.sh"
BAD_COMMAND="$TEMP_ROOT/bad-command"
cat >"$BAD_COMMAND" <<EOF
#!/bin/sh
printf '%s\n' invoked >> '$BAD_COMMAND_LOG'
exit 91
EOF
chmod +x "$BAD_COMMAND"
FAKE_SHELL="$TEMP_ROOT/fake-shell"
cat >"$FAKE_SHELL" <<EOF
#!/bin/sh
printf '%s\n' invoked >> '$FAKE_SHELL_LOG'
exec /bin/sh "\$@"
EOF
chmod +x "$FAKE_SHELL"
assert_commands() {
  scenario=$1 target=$2
  [ -s "$COMMAND_LOG" ] || { printf '%s\n' "$scenario $target executed no quality command" >&2; exit 1; }
  while IFS= read -r command; do
    case "$command" in "$CONTROL_DIR|"*"$CHECKOUT"*|"$CHECKOUT|"*) ;; *) printf '%s\n' "$scenario $target escaped: $command" >&2; exit 1;; esac
  done <"$COMMAND_LOG"
}
run_case() {
  scenario=$1 target=$2 mode=$3
  rm -f "$COMMAND_LOG" "$BAD_COMMAND_LOG" "$FAKE_SHELL_LOG"
  output="$TEMP_ROOT/output"; set +e
  case "$mode" in
    default) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "$target") >"$output" 2>&1 ;;
    command-root) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "ROOT=$ATTACKER_ROOT" "$target") >"$output" 2>&1 ;;
    environment-root) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" ROOT="$ATTACKER_ROOT" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "$target") >"$output" 2>&1 ;;
    command-shell) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "SHELL=$FAKE_SHELL" "$target") >"$output" 2>&1 ;;
    environment-shell) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" SHELL="$FAKE_SHELL" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "$target") >"$output" 2>&1 ;;
    command-flags) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" '.SHELLFLAGS=-eu -c' "$target") >"$output" 2>&1 ;;
    environment-flags) (cd "$CONTROL_DIR" && env '.SHELLFLAGS=-eu -c' PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "$target") >"$output" 2>&1 ;;
    command-python) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "PYTHON=$BAD_COMMAND" "$target") >"$output" 2>&1 ;;
    environment-python) (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" PYTHON="$BAD_COMMAND" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" "$target") >"$output" 2>&1 ;;
  esac
  result=$?; set -e
  [ "$result" -eq 0 ] || { printf '%s\n' "$scenario $target failed" >&2; cat "$output" >&2; exit 1; }
  assert_commands "$scenario" "$target"
  [ ! -e "$BAD_COMMAND_LOG" ] || { printf '%s\n' "$scenario $target executed caller Python" >&2; exit 1; }
  [ ! -e "$FAKE_SHELL_LOG" ] || { printf '%s\n' "$scenario $target executed caller shell" >&2; exit 1; }
}
for target in build check dependencies lint root-test test verify; do
  for mode in default command-root environment-root command-shell environment-shell command-flags environment-flags command-python environment-python; do run_case "$mode" "$target" "$mode"; done
done
[ ! -e "$CONTROL_DIR/RT_COVID19_BACKTICK_MARKER" ] || exit 1
if (cd "$CONTROL_DIR" && /usr/bin/make --no-print-directory --file "$MAKEFILE" MAKEFILE_LIST=/tmp/untrusted check) >"$TEMP_ROOT/command-list.out" 2>&1; then exit 1; fi
grep -Fq "MAKEFILE_LIST must not be overridden" "$TEMP_ROOT/command-list.out"
if (cd "$CONTROL_DIR" && MAKEFILE_LIST=/tmp/untrusted /usr/bin/make --environment-overrides --no-print-directory --file "$MAKEFILE" check) >"$TEMP_ROOT/environment-list.out" 2>&1; then exit 1; fi
grep -Fq "MAKEFILE_LIST must not be overridden" "$TEMP_ROOT/environment-list.out"
PRELOADED="$TEMP_ROOT/preloaded.mk"; printf '%s\n' 'ROOT := /tmp/preloaded' >"$PRELOADED"
if (cd "$CONTROL_DIR" && MAKEFILES="$PRELOADED" /usr/bin/make --no-print-directory --file "$MAKEFILE" check) >"$TEMP_ROOT/preloaded.out" 2>&1; then exit 1; fi
grep -Fq "MAKEFILES must be empty" "$TEMP_ROOT/preloaded.out"
EARLIER="$TEMP_ROOT/earlier.mk"; printf '%s\n' '# earlier' >"$EARLIER"
if (cd "$CONTROL_DIR" && /usr/bin/make --no-print-directory --file "$EARLIER" --file "$MAKEFILE" check) >"$TEMP_ROOT/multiple.out" 2>&1; then exit 1; fi
grep -Fq "repository Makefile path could not be resolved" "$TEMP_ROOT/multiple.out"
LATER="$TEMP_ROOT/later.mk"; printf '%s\n' '# later' >"$LATER"
rm -f "$COMMAND_LOG"
if (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" /usr/bin/make --no-print-directory --file "$MAKEFILE" --file "$LATER" check) >"$TEMP_ROOT/later.out" 2>&1; then exit 1; fi
grep -Fq "multiple -f Makefiles are not supported" "$TEMP_ROOT/later.out"
[ ! -e "$COMMAND_LOG" ] || { printf '%s\n' "later multiple -f reached a quality command" >&2; exit 1; }
# Failure-injection propagation: prove each public alias actually INVOKES every quality
# runner and GATES on its verdict. A presence pin cannot see a severed prerequisite, a
# `cmd || true` suffix, or make's `-cmd` error-ignore prefix; executing the alias against a
# runner that fails on demand sees all three, because the alias must fail with the runner.
INJECTION_CASES=0
assert_gate_propagates() {
  target=$1 pattern=$2
  rm -f "$COMMAND_LOG"
  output="$TEMP_ROOT/injected.out"; set +e
  (cd "$CONTROL_DIR" && PATH="$CHECKOUT/bin:$PATH" RT_COVID19_COMMAND_LOG="$COMMAND_LOG" \
    RT_COVID19_FAIL_PATTERN="$pattern" \
    /usr/bin/make --no-print-directory --file "$MAKEFILE" "$target") >"$output" 2>&1
  result=$?; set -e
  # The runner must actually be dispatched by this target, with these arguments.
  if [ ! -s "$COMMAND_LOG" ] || ! grep -F -q -e "$pattern" "$COMMAND_LOG"; then
    printf '%s\n' "make $target never invoked a quality runner matching '$pattern'" >&2
    cat "$output" >&2
    exit 1
  fi
  # ...and the target must fail because the runner failed.
  if [ "$result" -eq 0 ]; then
    printf '%s\n' "make $target ignored a failing '$pattern' runner and still exited 0" >&2
    cat "$output" >&2
    exit 1
  fi
  INJECTION_CASES=$((INJECTION_CASES + 1))
}
for target in check verify; do
  assert_gate_propagates "$target" "scripts/check_notebook_provenance.py"
  assert_gate_propagates "$target" "-m ruff format"
  assert_gate_propagates "$target" "-m ruff check"
  assert_gate_propagates "$target" "-m unittest"
  assert_gate_propagates "$target" "-m json.tool"
done
assert_gate_propagates check "-m pip check"
assert_gate_propagates check "-m pip_audit"
[ "$INJECTION_CASES" -eq 12 ] || { printf '%s\n' "expected 12 injection cases, ran $INJECTION_CASES" >&2; exit 1; }
printf '%s\n' "Makefile root tests passed: 63 executed target/authority cases, 2 MAKEFILE_LIST rejections, 1 MAKEFILES rejection, and 2 multi-Makefile rejections"
printf '%s\n' "Gate propagation tests passed: $INJECTION_CASES injected runner failures each failed their alias"
