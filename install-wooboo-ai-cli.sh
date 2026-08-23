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
LOCAL_CLI_SCRIPT="$SCRIPT_DIR/wooboo_ai_cli.py"
RAW_BASE="${WOOBOO_AI_CLI_RAW_BASE:-https://raw.githubusercontent.com/FUTUREWORKER/wooboo-ai-cli/main}"

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

INSTALL_ROOT="${WOOBOO_AI_CLI_HOME:-$HOME/.wooboo-ai}"
INSTALL_DIR="${WOOBOO_AI_CLI_INSTALL_DIR:-$INSTALL_ROOT/bin}"
LIB_DIR="$INSTALL_ROOT/lib"
mkdir -p "$INSTALL_DIR"
mkdir -p "$LIB_DIR"

CLI_SCRIPT="$LIB_DIR/wooboo_ai_cli.py"
if [ -f "$LOCAL_CLI_SCRIPT" ]; then
  cp "$LOCAL_CLI_SCRIPT" "$CLI_SCRIPT"
else
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$RAW_BASE/wooboo_ai_cli.py" -o "$CLI_SCRIPT"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$CLI_SCRIPT" "$RAW_BASE/wooboo_ai_cli.py"
  else
    echo "curl or wget is required to download wooboo_ai_cli.py." >&2
    exit 1
  fi
fi

WOOBOO_BIN="$INSTALL_DIR/wooboo"
cat > "$WOOBOO_BIN" <<EOF
#!/usr/bin/env bash
exec "$PYTHON_BIN" "$CLI_SCRIPT" "\$@"
EOF
chmod +x "$WOOBOO_BIN"

add_path_line='export PATH="$HOME/.wooboo-ai/bin:$PATH"'
if [ "${WOOBOO_AI_CLI_SKIP_PROFILE:-}" != "1" ]; then
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
      echo "# Wooboo AI CLI"
      echo "$add_path_line"
    } >> "$profile_file"
  fi
fi

echo "Installed Wooboo AI CLI (wooboo command): $WOOBOO_BIN"
echo "If the current terminal cannot find wooboo, open a new terminal or run:"
echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
