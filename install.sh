#!/usr/bin/env bash
#
# Feature Planning DevKit — Quick Installer Script
# Installs the feature-planner skill and portable core into your active project.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/<your-org>/agentic-feature-planning-devkit/main/install.sh | bash
#   OR from a local clone:
#   ./install.sh
#

set -e

TARGET_DIR=".agents/skills/feature-planner"

echo "📦 Installing Agentic Feature Planning DevKit..."

# Detect if running from local repo or remote curl
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"

mkdir -p "$TARGET_DIR"

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/core" ] && [ -d "$SCRIPT_DIR/adapters/antigravity" ]; then
    echo "📂 Copying from local DevKit workspace: $SCRIPT_DIR"
    cp -r "$SCRIPT_DIR/adapters/antigravity/"* "$TARGET_DIR/"
    cp -r "$SCRIPT_DIR/core" "$TARGET_DIR/"
else
    echo "🌐 Downloading latest release from GitHub..."
    TMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/<your-org>/agentic-feature-planning-devkit.git "$TMP_DIR/devkit" 2>/dev/null
    cp -r "$TMP_DIR/devkit/adapters/antigravity/"* "$TARGET_DIR/"
    cp -r "$TMP_DIR/devkit/core" "$TARGET_DIR/"
    rm -rf "$TMP_DIR"
fi

echo "✅ DevKit successfully installed to $TARGET_DIR"
echo ""
echo "🚀 Next steps:"
echo "  1. Open your project in Antigravity (or run 'agy')"
echo "  2. Type: Plan feature: <your feature statement>"
echo "  3. Find generated plans in .devkit/plans/<feature-slug>/"
