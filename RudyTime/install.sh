#!/usr/bin/env bash
set -euo pipefail
PROJECT_NAME="RudyTime"
DEST_LIB="$HOME/.local/lib/$PROJECT_NAME"
DEST_BIN="$HOME/.local/bin"
VENV="$HOME/.rudytime_venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEEDED_SYS_CMDS=(xdotool xprintidle python3 python3-venv python3-pip)
detect_pkg_manager() {
  if command -v apt-get >/dev/null 2>&1; then echo "apt";
  elif command -v dnf >/dev/null 2>&1; then echo "dnf";
  elif command -v pacman >/dev/null 2>&1; then echo "pacman";
  elif command -v zypper >/dev/null 2>&1; then echo "zypper";
  elif command -v apk >/dev/null 2>&1; then echo "apk";
  else echo ""; fi
}
install_system_packages() {
  local pm="$1"
  case "$pm" in
    apt) sudo apt-get update && sudo apt-get install -y xdotool xprintidle python3-venv python3-pip;;
    dnf) sudo dnf install -y xdotool xprintidle python3-venv python3-pip;;
    pacman) sudo pacman -Sy --noconfirm xdotool xprintidle python-virtualenv python-pip;;
    zypper) sudo zypper install -y xdotool xprintidle python3-venv python3-pip;;
    apk) sudo apk add xdotool xprintidle python3 py3-virtualenv py3-pip;;
    *) return 1;;
  esac
}
echo "Installing RudyTime to ${DEST_LIB}"
mkdir -p "$DEST_LIB" "$DEST_BIN"
PM="$(detect_pkg_manager)"
MISSING=false
for cmd in "${NEEDED_SYS_CMDS[@]}"; do if ! command -v "$cmd" >/dev/null 2>&1; then MISSING=true; fi; done
if $MISSING; then
  echo "Some system utilities appear missing (xdotool/xprintidle/python3-venv/pip)."
  read -r -p "Attempt automatic install using package manager (requires sudo)? [Y/n] " ans
  ans=${ans:-Y}
  if [[ "$ans" =~ ^[Yy] ]] && [ -n "$PM" ]; then
    if ! install_system_packages "$PM"; then
      echo "Automatic system package install failed; continuing installer. Install required system packages manually."
    fi
  else
    echo "Skipping automatic system package install. Install xdotool and xprintidle manually for tracking to work."
  fi
fi
echo "Creating Python virtual environment at $VENV ..."
python3 -m venv "$VENV"
# shellcheck disable=SC1090
. "$VENV/bin/activate"
echo "Installing runtime Python package: colorama and argcomplete"
python -m pip install --upgrade pip setuptools wheel >/dev/null 2>&1 || true
python -m pip install --no-cache-dir colorama argcomplete >/dev/null 2>&1 || true
echo "Copying project files to $DEST_LIB ..."
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude '.rudytime_venv' "$SCRIPT_DIR"/ "$DEST_LIB/"
else
  cp -a "$SCRIPT_DIR"/. "$DEST_LIB/"
fi
CLI_SRC="$DEST_LIB/RudyTime.py"
WRAPPER="$DEST_BIN/RudyTime"
WRAPPER_LOWER="$DEST_BIN/rudytime"
cat > "$WRAPPER" <<EOF
#!/usr/bin/env bash
VENV="$VENV"
CLI="$CLI_SRC"
export PATH="\$HOME/.local/bin:\$PATH"
if [ -x "\$VENV/bin/python" ]; then
  exec "\$VENV/bin/python" "\$CLI" "\$@"
else
  exec python3 "\$CLI" "\$@"
fi
EOF
cp "$WRAPPER" "$WRAPPER_LOWER"
chmod +x "$WRAPPER" "$WRAPPER_LOWER"
# Install bash completion (simple static)
BASH_COMPLETION_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions"
ZSH_DIR="${HOME}/.local/share/zsh/site-functions"
mkdir -p "$BASH_COMPLETION_DIR" "$ZSH_DIR"
cat > "$BASH_COMPLETION_DIR/RudyTime" <<'BC'
#!/bin/bash
COMPREPLY=()
local cur="${COMP_WORDS[COMP_CWORD]}"
local cmds="start stop status today week purge export import config seed"
COMPREPLY=( $(compgen -W "$cmds" -- "$cur") )
return 0
BC
cat > "$ZSH_DIR/_RudyTime" <<'ZC'
#compdef RudyTime
_arguments "1:command:(start stop status today week purge export import config seed)"
ZC
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
  echo "Added ~/.local/bin to PATH in ~/.profile"
fi
echo "Installation complete. Use 'RudyTime start' to begin tracking."
echo "Don't Forget to give the ripo a sexy star"
