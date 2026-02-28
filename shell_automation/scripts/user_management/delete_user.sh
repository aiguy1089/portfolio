#!/bin/bash

# delete_user.sh - Script to delete a user and their home directory
# Part B of D796 Assessment - Unix/Linux System Administration
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

# Function to ask for confirmation
confirm_deletion() {
    local username="$1"
    echo -e "${YELLOW}WARNING: This will permanently delete the user '$username' and their home directory.${NC}"
    echo -e "${YELLOW}This action cannot be undone!${NC}"
    echo -e "\n${BLUE}User Information:${NC}"
    
    # Display user info if exists
    if id "$username" &>/dev/null; then
        echo -e "${YELLOW}Username:${NC} $username"
        echo -e "${YELLOW}UID:${NC} $(id -u "$username")"
        echo -e "${YELLOW}GID:${NC} $(id -g "$username")"
        echo -e "${YELLOW}Groups:${NC} $(groups "$username" 2>/dev/null | cut -d: -f2)"
        echo -e "${YELLOW}Home Directory:${NC} $(getent passwd "$username" | cut -d: -f6)"
        echo -e "${YELLOW}Shell:${NC} $(getent passwd "$username" | cut -d: -f7)"
    fi
    
    echo -e "\n${RED}Are you sure you want to delete user '$username'? (yes/no):${NC}"
    read -r confirmation
    
    case "$confirmation" in
        [Yy][Ee][Ss]|[Yy])
            return 0
            ;;
        *)
            echo -e "${YELLOW}User deletion cancelled.${NC}"
            return 1
            ;;
    esac
}

# Main script execution
main() {
    log_message "Starting user deletion script..."
    
    # 1. Check if username argument is provided
    if [ $# -eq 0 ]; then
        log_error "No username provided!"
        echo -e "${RED}Error: Username argument is required.${NC}"
        usage
    fi
    
    USERNAME="$1"
    
    # Validate username format
    if [[ ! "$USERNAME" =~ ^[a-zA-Z0-9_]+$ ]]; then
        log_error "Invalid username format: $USERNAME"
        echo -e "${RED}Error: Username must contain only letters, numbers, and underscores.${NC}"
        exit 1
    fi
    
    log_message "Preparing to delete user: $USERNAME"
    
    # Check if user exists
    if ! id "$USERNAME" &>/dev/null; then
        log_error "User $USERNAME does not exist!"
        echo -e "${RED}Error: User '$USERNAME' does not exist in the system.${NC}"
        exit 1
    fi
    
    # Store user info before deletion for verification
    USER_HOME=$(getent passwd "$USERNAME" | cut -d: -f6)
    USER_UID=$(id -u "$USERNAME")
    
    # 2. Ask for confirmation
    if ! confirm_deletion "$USERNAME"; then
        log_message "User deletion cancelled by user"
        exit 0
    fi
    
    # Check if user is currently logged in
    if who | grep -q "^$USERNAME "; then
        echo -e "${YELLOW}Warning: User '$USERNAME' is currently logged in.${NC}"
        echo -e "${YELLOW}You may want to terminate their sessions first.${NC}"
        echo -e "${BLUE}Current sessions:${NC}"
        who | grep "^$USERNAME "
        echo -e "\n${RED}Continue with deletion anyway? (yes/no):${NC}"
        read -r force_confirmation
        case "$force_confirmation" in
            [Yy][Ee][Ss]|[Yy])
                log_message "Proceeding with deletion despite active sessions"
                # Kill user processes
                sudo pkill -u "$USERNAME" 2>/dev/null || true
                ;;
            *)
                echo -e "${YELLOW}User deletion cancelled.${NC}"
                exit 0
                ;;
        esac
    fi
    
    # 3. Delete the user and home directory
    log_message "Deleting user '$USERNAME' and home directory '$USER_HOME'..."
    
    # Use userdel with -r flag to remove home directory and mail spool
    if sudo userdel -r "$USERNAME" 2>/dev/null; then
        log_message "Successfully deleted user '$USERNAME' and home directory"
    else
        # If userdel fails, try to clean up manually
        log_message "Standard deletion failed, attempting manual cleanup..."
        
        # Delete user account
        if sudo userdel "$USERNAME" 2>/dev/null; then
            log_message "User account deleted"
        else
            log_error "Failed to delete user account"
        fi
        
        # Remove home directory if it exists
        if [ -d "$USER_HOME" ]; then
            if sudo rm -rf "$USER_HOME"; then
                log_message "Home directory '$USER_HOME' removed"
            else
                log_error "Failed to remove home directory '$USER_HOME'"
            fi
        fi
        
        # Remove mail spool if it exists
        if [ -f "/var/mail/$USERNAME" ]; then
            if sudo rm -f "/var/mail/$USERNAME"; then
                log_message "Mail spool removed"
            else
                log_error "Failed to remove mail spool"
            fi
        fi
    fi
    
    # 4. Display /etc/passwd file to verify user deletion
    echo -e "\n${BLUE}=== Verifying user deletion in /etc/passwd ===${NC}"
    if grep "^$USERNAME:" /etc/passwd; then
        log_error "User '$USERNAME' still exists in /etc/passwd!"
        exit 1
    else
        log_message "User '$USERNAME' successfully removed from /etc/passwd"
    fi
    
    # Verify home directory deletion
    echo -e "\n${BLUE}=== Verifying home directory deletion ===${NC}"
    if [ -d "$USER_HOME" ]; then
        log_error "Home directory '$USER_HOME' still exists!"
    else
        log_message "Home directory '$USER_HOME' successfully removed"
    fi
    
    # Check if user ID is still in use
    if getent passwd "$USER_UID" &>/dev/null; then
        log_error "UID $USER_UID is still in use by another account"
    else
        log_message "UID $USER_UID is now available"
    fi
    
    log_message "User deletion completed successfully!"
    
    # Display summary
    echo -e "\n${BLUE}=== Deletion Summary ===${NC}"
    echo -e "${YELLOW}Deleted User:${NC} $USERNAME"
    echo -e "${YELLOW}Removed Home Directory:${NC} $USER_HOME"
    echo -e "${YELLOW}Released UID:${NC} $USER_UID"
    echo -e "${YELLOW}Status:${NC} ${GREEN}Successfully Deleted${NC}"
}

# Script execution demonstrations
demonstrate_script() {
    echo -e "\n${BLUE}=== DEMONSTRATION SCENARIOS ===${NC}"
    
    echo -e "\n${YELLOW}Scenario 1: Running script without arguments${NC}"
    echo -e "${GREEN}Command: $0${NC}"
    echo -e "${RED}Expected: Error message and usage information${NC}"
    
    echo -e "\n${YELLOW}Scenario 2: Running script with valid arguments${NC}"
    echo -e "${GREEN}Command: $0 testuser${NC}"
    echo -e "${GREEN}Expected: Confirmation prompt and user deletion${NC}"
    
    echo -e "\n${YELLOW}Scenario 3: Attempt to switch to deleted user${NC}"
    echo -e "${GREEN}Command: su - testuser${NC}"
    echo -e "${GREEN}Expected: 'No such user' or authentication failure${NC}"
}

# Function to test user deletion
test_deletion() {
    local username="$1"
    echo -e "\n${BLUE}=== Testing User Deletion ===${NC}"
    
    # Try to switch to the user
    echo -e "${YELLOW}Testing if user '$username' can still be accessed...${NC}"
    
    if id "$username" &>/dev/null; then
        echo -e "${RED}FAIL: User '$username' still exists in the system${NC}"
        return 1
    else
        echo -e "${GREEN}PASS: User '$username' no longer exists in the system${NC}"
    fi
    
    # Try to access home directory
    local home_dir="/home/$username"
    if [ -d "$home_dir" ]; then
        echo -e "${RED}FAIL: Home directory '$home_dir' still exists${NC}"
        return 1
    else
        echo -e "${GREEN}PASS: Home directory '$home_dir' has been removed${NC}"
    fi
    
    echo -e "${GREEN}User deletion verification completed successfully!${NC}"
    return 0
}

# Check if script is being run for demonstration
if [ "$1" = "--demo" ]; then
    demonstrate_script
    exit 0
fi

# Check if script is being run for testing
if [ "$1" = "--test" ] && [ -n "$2" ]; then
    test_deletion "$2"
    exit $?
fi

# Execute main function
main "$@"