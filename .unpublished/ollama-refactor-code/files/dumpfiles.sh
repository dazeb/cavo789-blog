#!/usr/bin/env bash

# ==============================================================================
# Script: dumpfiles.sh
# Description: Dynamically aggregates the codebase into a single file.
# ==============================================================================

OUTPUT_FILE="dumpfiles.txt"
SCRIPT_NAME=$(basename "$0")

# 1. Initialize the file with System Instructions
cat << 'EOF' > "$OUTPUT_FILE"
# SYSTEM INSTRUCTIONS - AI CODE REVIEWER PROJECT
This codebase represents a specialized Git Hook tool designed to perform 
automated code reviews using a local LLM (Ollama).

CORE REQUIREMENTS:
- Programming Language: Python 3.14 (Strict Type Hinting required).
- Software Architecture: SOLID principles, DRY, and Clean Code (Short functions).
- Language Policy: All comments, documentation, and variables MUST be in American English. French is strictly forbidden.
- Environment: Dockerized (Alpine Linux) with Dev Container support (uv, pyproject.toml).
- Portability: The script must check for Ollama availability and skip gracefully if unreachable.
- Functional Goal: Parse staged files, analyze them via LLM, block commits if flaws are found, and suggest improvements via colored diffs.

This document serves as the "Source of Truth" for the current state of the project.
================================================================================
EOF

echo "Gathering files and dumping into $OUTPUT_FILE..."

# 2. Dynamic file discovery
# We use 'find' to be future-proof. 
# - we include hidden folders like .devcontainer
# - we exclude .git and __pycache__
# - we exclude the output file and the script itself
find . -type f \
    ! -path "*/.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "./$OUTPUT_FILE" \
    ! -path "./$SCRIPT_NAME" \
    ! -path "*/.venv/*" \
    -print0 | while IFS= read -r -d '' FILE; do

    # Clean the path (remove ./ prefix for clarity)
    CLEAN_PATH="${FILE#./}"
    
    echo "Adding: $CLEAN_PATH"
    
    {
        echo -e "\n--- START OF FILE: $CLEAN_PATH ---"
        cat "$FILE"
        echo -e "\n--- END OF FILE: $CLEAN_PATH ---"
    } >> "$OUTPUT_FILE"
done

echo -e "\nSuccessfully created $OUTPUT_FILE with all current project files."