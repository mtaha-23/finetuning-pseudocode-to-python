#!/bin/bash
# Setup script for Streamlit Cloud to handle Git LFS properly

echo "Setting up Git LFS for HTTPS..."

# Configure Git LFS to use HTTPS
git config lfs.url "https://github.com/mtaha-23/finetuning-pseudocode-to-python.git/info/lfs"

# Pull LFS files if available
if command -v git-lfs &> /dev/null; then
    echo "Git LFS found, pulling large files..."
    git lfs pull
else
    echo "Git LFS not found, but continuing..."
fi

echo "Setup complete!"

