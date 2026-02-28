#!/bin/bash

# bashrc_updates.sh - Script to update .bashrc with custom configurations
# Part C of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to log messages
log_message() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

# Function to log error messages
log_error() {
    echo -e "${RED}[ERROR $(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" >&2
}

# Function to backup existing .bashrc
backup_bashrc() {
    local bashrc_file="$1"
    local backup_file="${bashrc_file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    if [ -f "$bashrc_file" ]; then
        cp "$bashrc_file" "$backup_file"
        log_message "Backed up existing .bashrc to $backup_file"
        return 0
    else
        log_message "No existing .bashrc found, creating new one"
        return 1
    fi
}

# Function to create custom prompt configuration
create_prompt_config() {
    cat << 'EOF'

# ============================================================================
# CUSTOM PROMPT CONFIGURATION - D796 Assessment
# ============================================================================

# Custom prompt with colors and escape sequences
# Format: [user@hostname:current_directory]$ 
# Colors: Username in cyan, hostname in yellow, directory in blue, $ in green

# Define color variables for prompt
PROMPT_USER_COLOR='\[\033[0;36m\]'      # Cyan for username
PROMPT_HOST_COLOR='\[\033[1;33m\]'      # Yellow for hostname  
PROMPT_DIR_COLOR='\[\033[0;34m\]'       # Blue for directory
PROMPT_SYMBOL_COLOR='\[\033[0;32m\]'    # Green for $ symbol
PROMPT_RESET='\[\033[0m\]'              # Reset color

# Set the custom prompt
# \u = username, \h = hostname, \w = current working directory
export PS1="${PROMPT_USER_COLOR}\u${PROMPT_RESET}@${PROMPT_HOST_COLOR}\h${PROMPT_RESET}:${PROMPT_DIR_COLOR}\w${PROMPT_RESET}${PROMPT_SYMBOL_COLOR}\$ ${PROMPT_RESET}"

# Alternative prompt with time stamp (commented out)
# export PS1="${PROMPT_USER_COLOR}\u${PROMPT_RESET}@${PROMPT_HOST_COLOR}\h${PROMPT_RESET}:${PROMPT_DIR_COLOR}\w${PROMPT_RESET} ${PROMPT_SYMBOL_COLOR}[\t]\$ ${PROMPT_RESET}"

EOF
}

# Function to create PATH configuration
create_path_config() {
    local bin_dir="$1"
    cat << EOF

# ============================================================================
# CUSTOM PATH CONFIGURATION - D796 Assessment
# ============================================================================

# Add custom bin directory to PATH for user management scripts
if [ -d "$bin_dir" ]; then
    export PATH="\$PATH:$bin_dir"
    echo "Added $bin_dir to PATH"
else
    echo "Warning: $bin_dir directory not found"
fi

EOF
}

# Function to create aliases configuration
create_aliases_config() {
    local aliases_file="$1"
    cat << EOF

# ============================================================================
# CUSTOM ALIASES CONFIGURATION - D796 Assessment
# ============================================================================

# Source custom aliases file
if [ -f "$aliases_file" ]; then
    source "$aliases_file"
else
    echo "Warning: Custom aliases file not found at $aliases_file"
fi

EOF
}

# Function to create additional shell configurations
create_additional_config() {
    cat << 'EOF'

# ============================================================================
# ADDITIONAL SHELL CONFIGURATIONS - D796 Assessment
# ============================================================================

# History configuration
export HISTSIZE=1000
export HISTFILESIZE=2000
export HISTCONTROL=ignoredups:erasedups

# Enable color support for ls and grep
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# Enable programmable completion features
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# Custom functions
# Function to create directory and navigate to it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Function to extract various archive formats
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"     ;;
            *.tar.gz)    tar xzf "$1"     ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.rar)       unrar x "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.tar)       tar xf "$1"      ;;
            *.tbz2)      tar xjf "$1"     ;;
            *.tgz)       tar xzf "$1"     ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *.7z)        7z x "$1"        ;;
            *)           echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Welcome message
echo "============================================================================"
echo "Welcome to the D796 Assessment Environment"
echo "Custom shell configuration loaded successfully!"
echo "============================================================================"

EOF
}

# Main function to update .bashrc
main() {
    log_message "Starting .bashrc update process..."
    
    # Determine the correct .bashrc location
    local bashrc_file
    if [ "$HOME" = "/root" ]; then
        bashrc_file="/root/.bashrc"
    else
        bashrc_file="$HOME/.bashrc"
    fi
    
    log_message "Using .bashrc file: $bashrc_file"
    
    # Create bin directory if it doesn't exist
    local bin_dir="$HOME/D796/bin"
    if [ ! -d "$bin_dir" ]; then
        mkdir -p "$bin_dir"
        log_message "Created bin directory: $bin_dir"
    fi
    
    # Move user management scripts to bin directory
    local script_dir="$HOME/D796/scripts/user_management"
    if [ -f "$script_dir/create_user.sh" ]; then
        cp "$script_dir/create_user.sh" "$bin_dir/"
        chmod +x "$bin_dir/create_user.sh"
        log_message "Copied create_user.sh to bin directory"
    fi
    
    if [ -f "$script_dir/delete_user.sh" ]; then
        cp "$script_dir/delete_user.sh" "$bin_dir/"
        chmod +x "$bin_dir/delete_user.sh"
        log_message "Copied delete_user.sh to bin directory"
    fi
    
    # Backup existing .bashrc
    backup_bashrc "$bashrc_file"
    
    # Check if our custom configuration already exists
    if grep -q "D796 Assessment" "$bashrc_file" 2>/dev/null; then
        log_message "Custom configuration already exists in .bashrc"
        echo -e "${YELLOW}Do you want to update the existing configuration? (y/n):${NC}"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            log_message "Update cancelled by user"
            exit 0
        fi
        
        # Remove existing D796 configuration
        sed -i '/# D796 Assessment/,/# End D796 Assessment/d' "$bashrc_file"
        log_message "Removed existing D796 configuration"
    fi
    
    # Append custom configurations to .bashrc
    {
        echo ""
        echo "# ============================================================================"
        echo "# D796 Assessment Custom Configuration"
        echo "# Added on $(date)"
        echo "# ============================================================================"
        
        create_prompt_config
        create_path_config "$bin_dir"
        create_aliases_config "$HOME/D796/scripts/environment_config/aliases.sh"
        create_additional_config
        
        echo "# ============================================================================"
        echo "# End D796 Assessment Custom Configuration"
        echo "# ============================================================================"
        
    } >> "$bashrc_file"
    
    log_message "Successfully updated .bashrc with custom configuration"
    
    # Make scripts executable
    chmod +x "$HOME/D796/scripts/user_management/"*.sh
    chmod +x "$HOME/D796/scripts/environment_config/"*.sh
    
    # Display summary
    echo -e "\n${BLUE}=== Configuration Summary ===${NC}"
    echo -e "${YELLOW}Updated file:${NC} $bashrc_file"
    echo -e "${YELLOW}Bin directory:${NC} $bin_dir"
    echo -e "${YELLOW}Aliases file:${NC} $HOME/D796/scripts/environment_config/aliases.sh"
    echo -e "${YELLOW}Scripts added to PATH:${NC} create_user.sh, delete_user.sh"
    
    echo -e "\n${BLUE}=== Next Steps ===${NC}"
    echo -e "${GREEN}1. Reload your shell configuration:${NC}"
    echo -e "   source $bashrc_file"
    echo -e "${GREEN}2. Or start a new shell session to see changes${NC}"
    echo -e "${GREEN}3. Test the new prompt and aliases${NC}"
    echo -e "${GREEN}4. Verify scripts can be run from any directory${NC}"
    
    log_message ".bashrc update completed successfully!"
}

# Function to demonstrate the changes
demonstrate_changes() {
    echo -e "\n${BLUE}=== DEMONSTRATION OF CHANGES ===${NC}"
    
    echo -e "\n${YELLOW}1. Custom Prompt:${NC}"
    echo -e "   ${CYAN}user${NC}@${YELLOW}hostname${NC}:${BLUE}/current/directory${NC}${GREEN}\$ ${NC}"
    
    echo -e "\n${YELLOW}2. Custom Aliases:${NC}"
    echo -e "   ll      - ls -lrt (long listing, sorted by time)"
    echo -e "   la      - ls -a (list all files including hidden)"
    echo -e "   cls/c   - clear (clear screen)"
    echo -e "   desktop - cd to Desktop directory"
    echo -e "   download - cd to Downloads directory"
    echo -e "   documents - cd to Documents directory"
    
    echo -e "\n${YELLOW}3. PATH Updates:${NC}"
    echo -e "   Added ~/D796/bin to PATH"
    echo -e "   Scripts can be run from any directory:"
    echo -e "   - create_user.sh"
    echo -e "   - delete_user.sh"
    
    echo -e "\n${YELLOW}4. Additional Features:${NC}"
    echo -e "   - Color support for ls and grep"
    echo -e "   - Enhanced history configuration"
    echo -e "   - Custom functions (mkcd, extract)"
    echo -e "   - Welcome message on login"
}

# Function to test the configuration
test_configuration() {
    echo -e "\n${BLUE}=== TESTING CONFIGURATION ===${NC}"
    
    # Test PATH
    echo -e "\n${YELLOW}Testing PATH configuration:${NC}"
    if command -v create_user.sh >/dev/null 2>&1; then
        echo -e "${GREEN}✓ create_user.sh found in PATH${NC}"
    else
        echo -e "${RED}✗ create_user.sh not found in PATH${NC}"
    fi
    
    if command -v delete_user.sh >/dev/null 2>&1; then
        echo -e "${GREEN}✓ delete_user.sh found in PATH${NC}"
    else
        echo -e "${RED}✗ delete_user.sh not found in PATH${NC}"
    fi
    
    # Test aliases file
    echo -e "\n${YELLOW}Testing aliases file:${NC}"
    local aliases_file="$HOME/D796/scripts/environment_config/aliases.sh"
    if [ -f "$aliases_file" ]; then
        echo -e "${GREEN}✓ Aliases file exists${NC}"
        if source "$aliases_file" >/dev/null 2>&1; then
            echo -e "${GREEN}✓ Aliases file can be sourced${NC}"
        else
            echo -e "${RED}✗ Error sourcing aliases file${NC}"
        fi
    else
        echo -e "${RED}✗ Aliases file not found${NC}"
    fi
    
    # Test bin directory
    echo -e "\n${YELLOW}Testing bin directory:${NC}"
    local bin_dir="$HOME/D796/bin"
    if [ -d "$bin_dir" ]; then
        echo -e "${GREEN}✓ Bin directory exists${NC}"
        echo -e "${BLUE}Contents:${NC}"
        ls -la "$bin_dir"
    else
        echo -e "${RED}✗ Bin directory not found${NC}"
    fi
}

# Check command line arguments
case "$1" in
    --demo)
        demonstrate_changes
        exit 0
        ;;
    --test)
        test_configuration
        exit 0
        ;;
    --help)
        echo "Usage: $0 [--demo|--test|--help]"
        echo "  --demo  Show demonstration of changes"
        echo "  --test  Test the configuration"
        echo "  --help  Show this help message"
        exit 0
        ;;
esac

# Execute main function
main "$@"