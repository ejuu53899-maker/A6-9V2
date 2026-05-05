#!/bin/bash

# GenX FX V4 Environment Setup Script
# This script configures VS Code/Cursor and provides guidance for JetBrains users.

set -e

echo "------------------------------------------------"
echo "🚀 GenX FX V4 Environment Setup"
echo "------------------------------------------------"

# 1. VS Code / Cursor Configuration
echo "Configuring VS Code / Cursor..."
mkdir -p .vscode

cat <<EOF > .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylint",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "golang.go",
    "ms-azuretools.vscode-docker",
    "mql5.mql5-syntax-highlighter"
  ]
}
EOF

cat <<EOF > .vscode/settings.json
{
  "python.defaultInterpreterPath": "python3",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/.git": true
  }
}
EOF

# 2. CLI Installation
echo "Installing Jules CLI..."
if [ -d "GenX_FX_V4" ]; then
    cd GenX_FX_V4
    pip install -e .
    cd ..
    echo "✅ jules-cli installed successfully."
else
    echo "⚠️ GenX_FX_V4 directory not found. Skipping CLI installation."
fi

# 3. JetBrains Toolbox Guidance
echo ""
echo "------------------------------------------------"
echo "💎 JetBrains Toolbox Guidance"
echo "------------------------------------------------"
echo "For PyCharm / IntelliJ IDEA users:"
echo "1. Open JetBrains Toolbox and ensure your IDE is up to date."
echo "2. Open this project folder in your IDE."
echo "3. Configure the Python Interpreter to use 'python3'."
echo "4. Install plugins: 'Python', 'Docker', and 'MQL5' (if available)."
echo "5. The 'jules-cli' can be run directly from the IDE's terminal."
echo "------------------------------------------------"

echo "✅ Setup complete!"
