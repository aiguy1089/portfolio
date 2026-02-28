#!/bin/bash

# update_packages.sh - Script to update all installed packages
# Part D.2 of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LOG_FILE="$HOME/D796/logs/update.log"
BACKUP_COUNT=5

# Function to log messages with timestamp
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${GREEN}[$timestamp] $message${NC}"
    echo "[$timestamp] $message" >> "$LOG_FILE"
}

# Function to log error messages
log_error() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${RED}[ERROR $timestamp] $message${NC}" >&2
    echo "[ERROR $timestamp] $message" >> "$LOG_FILE"
}

# Function to log info messages (to file only)
log_info() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" >> "$LOG_FILE"
}

# Function to detect the package manager
detect_package_manager() {
    if command -v apt-get >/dev/null 2>&1; then
        echo "apt"
    elif command -v yum >/dev/null 2>&1; then
        echo "yum"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v zypper >/dev/null 2>&1; then
        echo "zypper"
    elif command -v pacman >/dev/null 2>&1; then
        echo "pacman"
    else
        echo "unknown"
    fi
}

# Function to setup log file
setup_logging() {
    # Create logs directory if it doesn't exist
    local log_dir=$(dirname "$LOG_FILE")
    if [ ! -d "$log_dir" ]; then
        mkdir -p "$log_dir"
        log_message "Created log directory: $log_dir"
    fi
    
    # Rotate old log files
    if [ -f "$LOG_FILE" ]; then
        for i in $(seq $((BACKUP_COUNT-1)) -1 1); do
            if [ -f "${LOG_FILE}.$i" ]; then
                mv "${LOG_FILE}.$i" "${LOG_FILE}.$((i+1))"
            fi
        done
        mv "$LOG_FILE" "${LOG_FILE}.1"
    fi
    
    # Create new log file
    touch "$LOG_FILE"
    log_message "Package update session started"
    log_info "Log file: $LOG_FILE"
    log_info "System: $(uname -a)"
    log_info "User: $(whoami)"
}

# Function to get system information
get_system_info() {
    log_info "=== System Information ==="
    log_info "Hostname: $(hostname)"
    log_info "OS: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"' || uname -s)"
    log_info "Kernel: $(uname -r)"
    log_info "Architecture: $(uname -m)"
    log_info "Uptime: $(uptime)"
    log_info "Memory: $(free -h | grep Mem:)"
    log_info "Disk Space: $(df -h / | tail -1)"
}

# Function to update packages using apt (Debian/Ubuntu)
update_apt() {
    log_message "Updating packages using apt package manager..."
    
    # Update package list
    log_message "Updating package list..."
    if sudo apt-get update 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Package list updated successfully"
    else
        log_error "Failed to update package list"
        return 1
    fi
    
    # Show upgradable packages
    log_message "Checking for upgradable packages..."
    local upgradable=$(apt list --upgradable 2>/dev/null | wc -l)
    log_message "Found $((upgradable-1)) upgradable packages"
    
    # List upgradable packages in log
    log_info "=== Upgradable Packages ==="
    apt list --upgradable 2>/dev/null >> "$LOG_FILE"
    
    # Upgrade packages
    log_message "Upgrading packages..."
    if sudo apt-get upgrade -y 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Packages upgraded successfully"
    else
        log_error "Some packages failed to upgrade"
        return 1
    fi
    
    # Clean up
    log_message "Cleaning up package cache..."
    sudo apt-get autoremove -y 2>&1 | tee -a "$LOG_FILE"
    sudo apt-get autoclean 2>&1 | tee -a "$LOG_FILE"
    
    return 0
}

# Function to update packages using yum (RHEL/CentOS 7 and older)
update_yum() {
    log_message "Updating packages using yum package manager..."
    
    # Check for updates
    log_message "Checking for available updates..."
    yum check-update 2>&1 | tee -a "$LOG_FILE"
    local update_count=$(yum check-update 2>/dev/null | grep -v "^$" | grep -v "Loaded plugins" | wc -l)
    log_message "Found $update_count available updates"
    
    # Update packages
    log_message "Updating all packages..."
    if sudo yum update -y 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Packages updated successfully"
    else
        log_error "Some packages failed to update"
        return 1
    fi
    
    # Clean up
    log_message "Cleaning up package cache..."
    sudo yum clean all 2>&1 | tee -a "$LOG_FILE"
    
    return 0
}

# Function to update packages using dnf (RHEL/CentOS 8+ and Fedora)
update_dnf() {
    log_message "Updating packages using dnf package manager..."
    
    # Check for updates
    log_message "Checking for available updates..."
    dnf check-update 2>&1 | tee -a "$LOG_FILE"
    
    # Update packages
    log_message "Updating all packages..."
    if sudo dnf update -y 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Packages updated successfully"
    else
        log_error "Some packages failed to update"
        return 1
    fi
    
    # Clean up
    log_message "Cleaning up package cache..."
    sudo dnf clean all 2>&1 | tee -a "$LOG_FILE"
    
    return 0
}

# Function to update packages using zypper (openSUSE)
update_zypper() {
    log_message "Updating packages using zypper package manager..."
    
    # Refresh repositories
    log_message "Refreshing repositories..."
    if sudo zypper refresh 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Repositories refreshed successfully"
    else
        log_error "Failed to refresh repositories"
        return 1
    fi
    
    # Update packages
    log_message "Updating all packages..."
    if sudo zypper update -y 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Packages updated successfully"
    else
        log_error "Some packages failed to update"
        return 1
    fi
    
    return 0
}

# Function to update packages using pacman (Arch Linux)
update_pacman() {
    log_message "Updating packages using pacman package manager..."
    
    # Update package database and upgrade packages
    log_message "Synchronizing package database and upgrading packages..."
    if sudo pacman -Syu --noconfirm 2>&1 | tee -a "$LOG_FILE"; then
        log_message "Packages updated successfully"
    else
        log_error "Some packages failed to update"
        return 1
    fi
    
    # Clean up
    log_message "Cleaning up package cache..."
    sudo pacman -Sc --noconfirm 2>&1 | tee -a "$LOG_FILE"
    
    return 0
}

# Function to get package statistics
get_package_stats() {
    local pkg_manager="$1"
    
    log_info "=== Package Statistics ==="
    
    case "$pkg_manager" in
        "apt")
            local installed=$(dpkg -l | grep "^ii" | wc -l)
            local upgradable=$(apt list --upgradable 2>/dev/null | wc -l)
            log_info "Installed packages: $installed"
            log_info "Upgradable packages: $((upgradable-1))"
            ;;
        "yum")
            local installed=$(yum list installed 2>/dev/null | wc -l)
            log_info "Installed packages: $installed"
            ;;
        "dnf")
            local installed=$(dnf list installed 2>/dev/null | wc -l)
            log_info "Installed packages: $installed"
            ;;
        "zypper")
            local installed=$(zypper search --installed-only 2>/dev/null | wc -l)
            log_info "Installed packages: $installed"
            ;;
        "pacman")
            local installed=$(pacman -Q | wc -l)
            log_info "Installed packages: $installed"
            ;;
    esac
}

# Function to check disk space before and after update
check_disk_space() {
    local phase="$1"
    log_info "=== Disk Space ($phase Update) ==="
    df -h >> "$LOG_FILE"
}

# Function to show update summary
show_summary() {
    local start_time="$1"
    local end_time="$2"
    local status="$3"
    
    echo -e "\n${BLUE}=== Update Summary ===${NC}"
    echo -e "${YELLOW}Start Time:${NC} $start_time"
    echo -e "${YELLOW}End Time:${NC} $end_time"
    echo -e "${YELLOW}Duration:${NC} $((end_time - start_time)) seconds"
    echo -e "${YELLOW}Status:${NC} $status"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    
    # Log summary
    log_info "=== Update Summary ==="
    log_info "Start Time: $(date -d @$start_time)"
    log_info "End Time: $(date -d @$end_time)"
    log_info "Duration: $((end_time - start_time)) seconds"
    log_info "Status: $status"
}

# Main function
main() {
    local start_time=$(date +%s)
    
    echo -e "${BLUE}=== Package Update Script ===${NC}"
    echo -e "${BLUE}D796 Assessment - Package Management${NC}"
    echo -e "${BLUE}====================================${NC}\n"
    
    # Setup logging
    setup_logging
    
    # Get system information
    get_system_info
    
    # Detect package manager
    local pkg_manager=$(detect_package_manager)
    log_message "Detected package manager: $pkg_manager"
    
    if [ "$pkg_manager" = "unknown" ]; then
        log_error "Could not detect a supported package manager"
        echo -e "${RED}Supported package managers: apt, yum, dnf, zypper, pacman${NC}"
        echo -e "${YELLOW}Please update packages manually using your system's package manager${NC}"
        exit 1
    fi
    
    # Check if we have sudo privileges
    if ! sudo -n true 2>/dev/null; then
        echo -e "${YELLOW}This script requires sudo privileges to update packages.${NC}"
        echo -e "${YELLOW}You may be prompted for your password.${NC}"
    fi
    
    # Get initial package statistics
    get_package_stats "$pkg_manager"
    
    # Check initial disk space
    check_disk_space "Before"
    
    # Update packages based on detected package manager
    local update_status="SUCCESS"
    case "$pkg_manager" in
        "apt")
            if ! update_apt; then
                update_status="FAILED"
            fi
            ;;
        "yum")
            if ! update_yum; then
                update_status="FAILED"
            fi
            ;;
        "dnf")
            if ! update_dnf; then
                update_status="FAILED"
            fi
            ;;
        "zypper")
            if ! update_zypper; then
                update_status="FAILED"
            fi
            ;;
        "pacman")
            if ! update_pacman; then
                update_status="FAILED"
            fi
            ;;
    esac
    
    # Check final disk space
    check_disk_space "After"
    
    # Get final package statistics
    get_package_stats "$pkg_manager"
    
    local end_time=$(date +%s)
    
    # Show summary
    show_summary "$start_time" "$end_time" "$update_status"
    
    if [ "$update_status" = "SUCCESS" ]; then
        log_message "Package update completed successfully!"
        echo -e "\n${GREEN}✓ All packages have been updated successfully${NC}"
        echo -e "${GREEN}✓ Update log saved to: $LOG_FILE${NC}"
        exit 0
    else
        log_error "Package update completed with errors"
        echo -e "\n${RED}✗ Package update completed with errors${NC}"
        echo -e "${YELLOW}Check the log file for details: $LOG_FILE${NC}"
        exit 1
    fi
}

# Function to show script usage
show_usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  --check     Check for available updates without installing"
    echo -e "  --log       Show the location of the log file"
    echo -e "  --stats     Show package statistics"
    echo -e "  --help      Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0          Update all packages (default behavior)"
    echo -e "  $0 --check  Check for available updates"
    echo -e "  $0 --stats  Show package statistics"
}

# Function to check for updates without installing
check_updates() {
    local pkg_manager=$(detect_package_manager)
    
    echo -e "${BLUE}=== Checking for Available Updates ===${NC}"
    echo -e "${YELLOW}Package Manager:${NC} $pkg_manager"
    
    case "$pkg_manager" in
        "apt")
            echo -e "${YELLOW}Updating package list...${NC}"
            sudo apt-get update >/dev/null 2>&1
            local upgradable=$(apt list --upgradable 2>/dev/null | wc -l)
            echo -e "${YELLOW}Upgradable packages:${NC} $((upgradable-1))"
            if [ $((upgradable-1)) -gt 0 ]; then
                echo -e "\n${BLUE}Available updates:${NC}"
                apt list --upgradable 2>/dev/null
            fi
            ;;
        "yum")
            echo -e "${YELLOW}Checking for updates...${NC}"
            yum check-update
            ;;
        "dnf")
            echo -e "${YELLOW}Checking for updates...${NC}"
            dnf check-update
            ;;
        "zypper")
            echo -e "${YELLOW}Checking for updates...${NC}"
            zypper list-updates
            ;;
        "pacman")
            echo -e "${YELLOW}Checking for updates...${NC}"
            pacman -Qu
            ;;
        *)
            echo -e "${RED}Unsupported package manager${NC}"
            exit 1
            ;;
    esac
}

# Function to show package statistics
show_stats() {
    local pkg_manager=$(detect_package_manager)
    
    echo -e "${BLUE}=== Package Statistics ===${NC}"
    echo -e "${YELLOW}Package Manager:${NC} $pkg_manager"
    
    case "$pkg_manager" in
        "apt")
            local installed=$(dpkg -l | grep "^ii" | wc -l)
            local upgradable=$(apt list --upgradable 2>/dev/null | wc -l)
            echo -e "${YELLOW}Installed packages:${NC} $installed"
            echo -e "${YELLOW}Upgradable packages:${NC} $((upgradable-1))"
            ;;
        "yum")
            local installed=$(yum list installed 2>/dev/null | wc -l)
            echo -e "${YELLOW}Installed packages:${NC} $installed"
            ;;
        "dnf")
            local installed=$(dnf list installed 2>/dev/null | wc -l)
            echo -e "${YELLOW}Installed packages:${NC} $installed"
            ;;
        "zypper")
            local installed=$(zypper search --installed-only 2>/dev/null | wc -l)
            echo -e "${YELLOW}Installed packages:${NC} $installed"
            ;;
        "pacman")
            local installed=$(pacman -Q | wc -l)
            echo -e "${YELLOW}Installed packages:${NC} $installed"
            ;;
        *)
            echo -e "${RED}Unsupported package manager${NC}"
            exit 1
            ;;
    esac
}

# Handle command line arguments
case "$1" in
    --check)
        check_updates
        exit 0
        ;;
    --log)
        echo -e "${YELLOW}Log file location:${NC} $LOG_FILE"
        if [ -f "$LOG_FILE" ]; then
            echo -e "${YELLOW}Log file size:${NC} $(du -h "$LOG_FILE" | cut -f1)"
            echo -e "${YELLOW}Last modified:${NC} $(stat -c %y "$LOG_FILE")"
        else
            echo -e "${RED}Log file does not exist${NC}"
        fi
        exit 0
        ;;
    --stats)
        show_stats
        exit 0
        ;;
    --help)
        show_usage
        exit 0
        ;;
    "")
        # Default behavior - run main function
        main
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac