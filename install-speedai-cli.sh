#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
while [ -L "$SCRIPT_PATH" ]; do
  SCRIPT_DIR="$(cd -P "$(dirname "$SCRIPT_PATH")" >/dev/null 2>&1 && pwd)"
  SCRIPT_PATH="$(readlink "$SCRIPT_PATH")"
  case "$SCRIPT_PATH" in
    /*) ;;
    *) SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH" ;;
  esac
done

SCRIPT_DIR="$(cd -P "$(dirname "$SCRIPT_PATH")" >/dev/null 2>&1 && pwd)"
CLI_SCRIPT="$SCRIPT_DIR/speedai_cli.py"

if [ ! -f "$CLI_SCRIPT" ]; then
  echo "speedai_cli.py not found: $CLI_SCRIPT" >&2
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  else
    echo "Python 3 is required. Install Python first, then rerun this script." >&2
    exit 1
  fi
fi

INSTALL_DIR="${SPEEDAI_CLI_INSTALL_DIR:-$HOME/.speed-ai/bin}"
mkdir -p "$INSTALL_DIR"

SPEEDAI_BIN="$INSTALL_DIR/speedai"
cat > "$SPEEDAI_BIN" <<EOF
#!/usr/bin/env bash
exec "$PYTHON_BIN" "$CLI_SCRIPT" "\$@"
EOF
chmod +x "$SPEEDAI_BIN"

add_path_line='export PATH="$HOME/.speed-ai/bin:$PATH"'
if [ "${SPEEDAI_CLI_SKIP_PROFILE:-}" != "1" ]; then
  profile_file=""
  shell_name="$(basename "${SHELL:-}")"
  if [ "$shell_name" = "zsh" ]; then
    profile_file="$HOME/.zshrc"
  elif [ "$shell_name" = "bash" ]; then
    if [ "$(uname -s)" = "Darwin" ]; then
      profile_file="$HOME/.bash_profile"
    else
      profile_file="$HOME/.bashrc"
    fi
  else
    profile_file="$HOME/.profile"
  fi

  touch "$profile_file"
  if ! grep -F "$add_path_line" "$profile_file" >/dev/null 2>&1; then
    {
      echo ""
      echo "# Speed AI CLI"
      echo "$add_path_line"
    } >> "$profile_file"
  fi
fi

echo "Installed speedai CLI: $SPEEDAI_BIN"
echo "If the current terminal cannot find speedai, open a new terminal or run:"
echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
