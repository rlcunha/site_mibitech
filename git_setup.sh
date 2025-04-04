#!/bin/bash

# MibiTech Git Setup Script
# This script helps set up Git and push to GitHub

# Exit on error
set -e

# Display help message
show_help() {
    echo "MibiTech Git Setup Script"
    echo "Usage: ./git_setup.sh [OPTION]"
    echo "Options:"
    echo "  -h, --help              Display this help message"
    echo "  -i, --init              Initialize Git repository"
    echo "  -r, --remote REPO_URL   Add GitHub remote repository"
    echo "  -p, --push              Push to GitHub repository"
    echo "  -a, --all               Perform all actions (init, add, commit, push)"
    echo "  -m, --message MESSAGE   Commit message (default: 'Initial commit')"
}

# Initialize Git repository
init_repo() {
    echo "Initializing Git repository..."
    if [ -d ".git" ]; then
        echo "Git repository already initialized."
    else
        git init
        echo "Git repository initialized."
    fi
}

# Add remote repository
add_remote() {
    if [ -z "$1" ]; then
        echo "Error: Repository URL is required."
        show_help
        exit 1
    fi

    echo "Adding remote repository..."
    if git remote | grep -q "origin"; then
        git remote set-url origin "$1"
        echo "Remote repository updated."
    else
        git remote add origin "$1"
        echo "Remote repository added."
    fi
}

# Add all files and commit
commit_files() {
    local message=${1:-"Initial commit"}
    
    echo "Adding all files to Git..."
    git add .
    
    echo "Committing changes..."
    git commit -m "$message"
    echo "Changes committed."
}

# Push to GitHub
push_to_github() {
    echo "Pushing to GitHub..."
    git push -u origin main || git push -u origin master
    echo "Push completed."
}

# Perform all actions
do_all() {
    local repo_url="$1"
    local message=${2:-"Initial commit"}
    
    if [ -z "$repo_url" ]; then
        echo "Error: Repository URL is required for --all option."
        show_help
        exit 1
    fi
    
    init_repo
    add_remote "$repo_url"
    commit_files "$message"
    push_to_github
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

REPO_URL=""
COMMIT_MESSAGE="Initial commit"

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -i|--init)
            init_repo
            ;;
        -r|--remote)
            shift
            REPO_URL="$1"
            add_remote "$REPO_URL"
            ;;
        -p|--push)
            push_to_github
            ;;
        -a|--all)
            shift
            REPO_URL="$1"
            do_all "$REPO_URL" "$COMMIT_MESSAGE"
            ;;
        -m|--message)
            shift
            COMMIT_MESSAGE="$1"
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    shift
done

exit 0