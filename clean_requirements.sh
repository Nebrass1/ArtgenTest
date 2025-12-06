#!/usr/bin/env bash
# Script to clean requirements for Render deployment

echo "Cleaning requirements.txt for Render..."

# Remove Windows-only packages
grep -v -E "pywin32|pyreadline|pywinpty" requirements.txt > requirements-clean.txt

# Count packages
echo ""
echo "Packages avant nettoyage: $(wc -l < requirements.txt)"
echo "Packages apres nettoyage: $(wc -l < requirements-clean.txt)"

# Create final file
mv requirements-clean.txt requirements.txt

echo ""
echo "✅ requirements.txt is now Render-compatible!"
echo "Run: pip install -r requirements.txt"
