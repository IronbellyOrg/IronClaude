#!/bin/bash
# install.sh — wire the ccsession skill into the user's environment.
#
# What this does:
#   1. Copies the skill folder to ~/.claude/skills/ccsession-tag/ (if not
#      already there), so the slash command is discovered in every workspace
#      and the install survives the source folder being deleted/moved.
#   2. Symlinks the shell wrapper into ~/.local/bin/ccsession, pointing at
#      the user-level copy.
#   3. Creates ~/.claude/ccsession.env from the template if it doesn't exist.
#   4. Registers the SessionStart hook in ~/.claude/settings.json (idempotent
#      merge — preserves existing hooks, backs up before writing, safe on
#      invalid JSON).
#
# Re-running is safe — files get refreshed, your env file is left untouched,
# and the hook is only added once.
# After install completes, the source folder you ran this from can be deleted.

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_SKILL_DIR="$HOME/.claude/skills/ccsession-tag"

echo "Installing ccsession skill"
echo "  source: $SKILL_DIR"
echo "  target: $TARGET_SKILL_DIR"
echo ""

# 1. Copy skill folder to user-level (idempotent)
if [ "$SKILL_DIR" = "$TARGET_SKILL_DIR" ]; then
  echo "[1/4] Source IS the user-level skill folder — skipping copy."
else
  mkdir -p "$(dirname "$TARGET_SKILL_DIR")"
  mkdir -p "$TARGET_SKILL_DIR"
  # Copy contents (incl. dotfiles) into the target; overwrite-on-conflict.
  cp -R "$SKILL_DIR"/. "$TARGET_SKILL_DIR"/
  echo "[1/4] Copied skill folder to: $TARGET_SKILL_DIR"
fi

# Make sure scripts in the target are executable
chmod +x "$TARGET_SKILL_DIR/ccsession"
chmod +x "$TARGET_SKILL_DIR/hooks/session-start.sh"
chmod +x "$TARGET_SKILL_DIR/install.sh"
echo ""

# 2. Symlink the shell wrapper from PATH → user-level skill copy
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ln -sfn "$TARGET_SKILL_DIR/ccsession" "$BIN_DIR/ccsession"
echo "[2/4] Linked shell wrapper:"
echo "      $BIN_DIR/ccsession -> $TARGET_SKILL_DIR/ccsession"
echo ""

# 3. Env file (user secrets, kept outside the skill folder so it's never
# accidentally distributed)
ENV_TARGET="$HOME/.claude/ccsession.env"
mkdir -p "$(dirname "$ENV_TARGET")"
if [ ! -f "$ENV_TARGET" ]; then
  cp "$TARGET_SKILL_DIR/ccsession.env.example" "$ENV_TARGET"
  chmod 600 "$ENV_TARGET"
  echo "[3/4] Created env file (edit to add your proxy/auth values):"
  echo "      $ENV_TARGET"
else
  echo "[3/4] Env file already exists (leaving untouched):"
  echo "      $ENV_TARGET"
fi
echo ""

# 4. Register the SessionStart hook in ~/.claude/settings.json (idempotent).
HOOK_SCRIPT="$TARGET_SKILL_DIR/hooks/session-start.sh"
SETTINGS="$HOME/.claude/settings.json"
echo "[4/4] Registering SessionStart hook:"
echo "      Script:   $HOOK_SCRIPT"
echo "      Settings: $SETTINGS"

python3 - "$SETTINGS" "$HOOK_SCRIPT" <<'PYEOF'
import json, os, sys, shutil

settings_path, hook_script = sys.argv[1], sys.argv[2]
hook_cmd = 'bash "%s"' % hook_script

# Load existing settings, or start fresh if absent.
data = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path) as f:
            data = json.load(f)
    except Exception:
        print("      WARNING: settings.json is not valid JSON — leaving it untouched.")
        print("      Add this manually under hooks.SessionStart:")
        print('        {"matcher": "startup|resume", "hooks": [{"type": "command",')
        print('          "command": %s, "timeout": 5}]}' % json.dumps(hook_cmd))
        sys.exit(0)

if not isinstance(data, dict):
    print("      WARNING: settings.json top-level is not a JSON object — leaving untouched.")
    sys.exit(0)

hooks = data.setdefault("hooks", {})
if not isinstance(hooks, dict):
    print("      WARNING: settings.json 'hooks' is not an object — leaving untouched.")
    sys.exit(0)
session_start = hooks.setdefault("SessionStart", [])
if not isinstance(session_start, list):
    print("      WARNING: settings.json 'hooks.SessionStart' is not a list — leaving untouched.")
    sys.exit(0)

# Idempotency: already registered if any SessionStart hook references our script.
for group in session_start:
    for h in (group.get("hooks", []) if isinstance(group, dict) else []):
        if isinstance(h, dict) and hook_script in h.get("command", ""):
            print("      Already registered — no change.")
            sys.exit(0)

# Back up an existing file before modifying it.
if os.path.exists(settings_path):
    shutil.copy2(settings_path, settings_path + ".bak")
    print("      Backed up existing settings to settings.json.bak")

session_start.append({
    "matcher": "startup|resume",
    "hooks": [{"type": "command", "command": hook_cmd, "timeout": 5}],
})

os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print("      Registered SessionStart hook.")
PYEOF
echo ""
echo "Install complete. The source folder ($SKILL_DIR)"
echo "can now be deleted — everything self-contained under ~/.claude/ and ~/.local/bin/."
echo ""
echo "Test with:"
echo "  ccsession --list"
echo "  ccsession --help"
