#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if ! git -C "$ROOT" rev-parse --show-toplevel >/dev/null 2>&1; then
  printf '%s\n' 'This lab directory is not inside a Git repository.' >&2
  exit 1
fi
HOOKS="$(git -C "$ROOT" rev-parse --absolute-git-dir)/hooks"
mkdir -p "$HOOKS"
cat > "$HOOKS/pre-commit" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
if [[ -x "$ROOT/lab-03-case-study-local-ci/run_ci.sh" ]]; then
  exec "$ROOT/lab-03-case-study-local-ci/run_ci.sh"
fi
if [[ -x "$ROOT/run_ci.sh" ]]; then
  exec "$ROOT/run_ci.sh"
fi
printf '%s\n' 'Could not locate the Lab 3 CI runner.' >&2
exit 1
HOOK
chmod +x "$HOOKS/pre-commit"
printf 'Installed local pre-commit hook at %s\n' "$HOOKS/pre-commit"
printf '%s\n' 'This hook runs browser tests before commits and can slow down commits.'
