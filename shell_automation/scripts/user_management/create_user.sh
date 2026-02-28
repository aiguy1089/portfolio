#!/bin/bash

# create_user.sh - Script to create a new user with dev_group assignment
# Part A of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage information
usage() {
    echo -e "${BLUE}Usage: $0 <username>${NC}"
    echo -e "${YELLOW}Example: $0 johndoe${NC}"
    exit 1
}

# Function to log messages with timestamp
log_message() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

# Function to log error messages
log_error() {
    echo -e "${RED}[ERROR $(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" >&2
}

# Main script execution
main() {
    log_message "Starting user creation script..."
    
    # 1. Check if username argument is provided
    if [ $# -eq 0 ]; then
        log_error "No username provided!"
        echo -e "${RED}Error: Username argument is required.${NC}"
        usage
    fi
    
    USERNAME="$1"
    
    # Validate username format (alphanumeric and underscore only)
    if [[ ! "$USERNAME" =~ ^[a-zA-Z0-9_]+$ ]]; then
        log_error "Invalid username format: $USERNAME"
        echo -e "${RED}Error: Username must contain only letters, numbers, and underscores.${NC}"
        exit 1
    fi
    
    log_message "Creating user: $USERNAME"
    
    # Check if user already exists
    if id "$USERNAME" &>/dev/null; then
        log_error "User $USERNAME already exists!"
        echo -e "${RED}Error: User '$USERNAME' already exists in the system.${NC}"
        exit 1
    fi
    
    # 2. Check if dev_group exists, create if it doesn't
    if ! getent group dev_group &>/dev/null; then
        log_message "Group 'dev_group' does not exist. Creating it..."
        if sudo groupadd dev_group; then
            log_message "Successfully created group 'dev_group'"
        else
            log_error "Failed to create group 'dev_group'"
            exit 1
        fi
    else
        log_message "Group 'dev_group' already exists"
    fi
    
    # 3. Create the user and assign to dev_group
    log_message "Creating user '$USERNAME' and adding to 'dev_group'..."
    
    if sudo useradd -m -g dev_group -s /bin/bash "$USERNAME"; then
        log_message "Successfully created user '$USERNAME'"
    else
        log_error "Failed to create user '$USERNAME'"
        exit 1
    fi
    
    # Set a temporary password and force password change on first login
    TEMP_PASSWORD="TempPass123!"
    echo "$USERNAME:$TEMP_PASSWORD" | sudo chpasswd
    
    # Force password change on next login
    sudo chage -d 0 "$USERNAME"
    
    log_message "Temporary password set for '$USERNAME': $TEMP_PASSWORD"
    log_message "User will be forced to change password on first login"
    
    # 4. Display /etc/passwd file to verify user creation
    echo -e "\n${BLUE}=== Verifying user creation in /etc/passwd ===${NC}"
    if grep "^$USERNAME:" /etc/passwd; then
        log_message "User '$USERNAME' successfully added to /etc/passwd"
    else
        log_error "User '$USERNAME' not found in /etc/passwd"
        exit 1
    fi
    
    # Display user information
    echo -e "\n${BLUE}=== User Information ===${NC}"
    echo -e "${YELLOW}Username:${NC} $USERNAME"
    echo -e "${YELLOW}Group:${NC} dev_group"
    echo -e "${YELLOW}Home Directory:${NC} /home/$USERNAME"
    echo -e "${YELLOW}Shell:${NC} /bin/bash"
    echo -e "${YELLOW}Temporary Password:${NC} $TEMP_PASSWORD"
    echo -e "${YELLOW}Password Change Required:${NC} Yes (on first login)"
    
    # Show group membership
    echo -e "\n${BLUE}=== Group Membership ===${NC}"
    groups "$USERNAME"
    
    log_message "User creation completed successfully!"
    
    # Instructions for testing
    echo -e "\n${BLUE}=== Testing Instructions ===${NC}"
    echo -e "${YELLOW}To test the new user account:${NC}"
    echo -e "1. Switch to user: ${GREEN}su - $USERNAME${NC}"
    echo -e "2. Use temporary password: ${GREEN}$TEMP_PASSWORD${NC}"
    echo -e "3. You will be prompted to change the password"
    echo -e "4. After setting new password, you can verify the account works"
}

# Script execution demonstrations
demonstrate_script() {
    echo -e "\n${BLUE}=== DEMONSTRATION SCENARIOS ===${NC}"
    
    echo -e "\n${YELLOW}Scenario 1: Running script without arguments${NC}"
    echo -e "${GREEN}Command: $0${NC}"
    echo -e "${RED}Expected: Error message and usage information${NC}"
    
    echo -e "\n${YELLOW}Scenario 2: Running script with valid arguments${NC}"
    echo -e "${GREEN}Command: $0 testuser${NC}"
    echo -e "${GREEN}Expected: User creation with dev_group assignment${NC}"
    
    echo -e "\n${YELLOW}Scenario 3: Switch to new user and change password${NC}"
    echo -e "${GREEN}Command: su - testuser${NC}"
    echo -e "${GREEN}Expected: Password change prompt on first login${NC}"
}

# Check if script is being run for demonstration
if [ "$1" = "--demo" ]; then
    demonstrate_script
    exit 0
fi

# Execute main function
main "$@"