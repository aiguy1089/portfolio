#!/bin/bash

# aliases.sh - Custom aliases for shell environment
# Part C of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# This file contains custom aliases that can be sourced in .bashrc
# Usage: source ~/D796/scripts/environment_config/aliases.sh

# Color definitions for ls commands
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
fi

# File listing aliases
alias ll='ls -lrt'          # Long listing, sorted by time (reverse)
alias la='ls -a'            # List all files including hidden
alias cls='clear'           # Clear screen (Windows-style)
alias c='clear'             # Short clear command

# Enhanced ls aliases with colors
alias ls='ls --color=auto'
alias lsl='ls -lrt --color=auto'    # Alternative to ll
alias lsa='ls -a --color=auto'      # Alternative to la
alias lsla='ls -la --color=auto'    # Long listing with all files

# Navigation aliases to root directory subdirectories
alias desktop='cd ~/Desktop 2>/dev/null || cd /root/Desktop 2>/dev/null || echo "Desktop directory not found"'
alias download='cd ~/Downloads 2>/dev/null || cd /root/Downloads 2>/dev/null || echo "Downloads directory not found"'
alias downloads='cd ~/Downloads 2>/dev/null || cd /root/Downloads 2>/dev/null || echo "Downloads directory not found"'
alias documents='cd ~/Documents 2>/dev/null || cd /root/Documents 2>/dev/null || echo "Documents directory not found"'
alias docs='cd ~/Documents 2>/dev/null || cd /root/Documents 2>/dev/null || echo "Documents directory not found"'

# Additional useful navigation aliases
alias home='cd ~'
alias root='cd /'
alias back='cd -'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# System information aliases
alias df='df -h'            # Human readable disk usage
alias du='du -h'            # Human readable directory usage
alias free='free -h'        # Human readable memory usage
alias ps='ps aux'           # Detailed process list

# Safety aliases
alias rm='rm -i'            # Interactive remove
alias cp='cp -i'            # Interactive copy
alias mv='mv -i'            # Interactive move

# Network aliases
alias ping='ping -c 4'      # Limit ping to 4 packets
alias ports='netstat -tuln' # Show listening ports

# Development aliases
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# Quick directory creation and navigation
alias mkcd='function _mkcd(){ mkdir -p "$1" && cd "$1"; }; _mkcd'

# System administration aliases
alias services='systemctl list-units --type=service'
alias logs='journalctl -f'
alias syslog='tail -f /var/log/syslog'

# Quick file editing
alias nano='nano -w'        # Disable line wrapping in nano
alias vi='vim'              # Use vim instead of vi

# Archive and compression shortcuts
alias tarzip='tar -czf'     # Create gzipped tar archive
alias tarunzip='tar -xzf'   # Extract gzipped tar archive
alias tarbzip='tar -cjf'    # Create bzip2 tar archive
alias tarunbzip='tar -xjf'  # Extract bzip2 tar archive

# Function to display all custom aliases
show_aliases() {
    echo "=== Custom Aliases ==="
    echo "File Listing:"
    echo "  ll      - ls -lrt (long listing, sorted by time)"
    echo "  la      - ls -a (list all files including hidden)"
    echo "  cls/c   - clear (clear screen)"
    echo ""
    echo "Navigation:"
    echo "  desktop   - cd to Desktop directory"
    echo "  download  - cd to Downloads directory"
    echo "  documents - cd to Documents directory"
    echo "  home      - cd to home directory"
    echo "  root      - cd to root directory"
    echo "  back      - cd to previous directory"
    echo "  ..        - cd to parent directory"
    echo ""
    echo "System:"
    echo "  df        - df -h (disk usage)"
    echo "  du        - du -h (directory usage)"
    echo "  free      - free -h (memory usage)"
    echo "  ps        - ps aux (process list)"
    echo "  services  - list systemd services"
    echo ""
    echo "Safety:"
    echo "  rm        - rm -i (interactive remove)"
    echo "  cp        - cp -i (interactive copy)"
    echo "  mv        - mv -i (interactive move)"
}

# Alias to show all custom aliases
alias aliases='show_aliases'

# Print confirmation message when aliases are loaded
echo "Custom aliases loaded successfully!"
echo "Type 'aliases' to see all available custom aliases."