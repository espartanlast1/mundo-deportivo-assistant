#!/bin/bash

# Check if a commit message is provided as an argument
if [ $# -eq 0 ]; then
    echo "Please provide a commit message."
    exit 1
fi

# Add all changes (including untracked files) to the staging area
git add .

# Commit the changes with a GPG signature and the provided commit message
git commit -S -m "$@"

# Pull the latest changes from the remote "new_data_fantasy" branch
git pull new_data_fantasy

# Add all changes (including untracked files) to the staging area
git add .

# Commit the changes with a GPG signature and the provided commit message
git commit -S -m "$@"

# Push the committed changes to the "new_data_fantasy" branch
git push --set-upstream origin new_data_fantasy
