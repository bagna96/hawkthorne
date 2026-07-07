#!/bin/bash
# Pubblica il gioco sul TUO GitHub + attiva GitHub Pages (URL giocabile online).
# Prerequisito: gh auth login  (una volta sola)
set -e
cd "$(dirname "$0")"

gh repo create hawkthorne --public --source . --push --description "Journey to the Center of Hawkthorne — tributo 8-bit a Community 3x20"

OWNER=$(gh api user -q .login)
gh api -X POST "repos/$OWNER/hawkthorne/pages" \
  -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || true

echo ""
echo "✅ Fatto! Il gioco sarà giocabile tra ~1 minuto su:"
echo "   https://$OWNER.github.io/hawkthorne/"
