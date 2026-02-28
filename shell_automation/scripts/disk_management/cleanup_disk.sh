#!/bin/bash

# cleanup_disk.sh - Script to assess and clean up disk space
# Part F of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
LOG_FILE="$HOME/D796/logs/disk_cleanup.log"
BACKUP_DIR="$HOME/D796/logs/cleanup_backups"

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

# Function to setup logging
setup_logging() {
    local log_dir=$(dirname "$LOG_FILE")
    if [ ! -d "$log_dir" ]; then
        mkdir -p "$log_dir"
    fi
    
    # Create backup directory
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
    fi
    
    # Create new log file
    touch "$LOG_FILE"
    log_message "Disk cleanup script started"
    log_message "Log file: $LOG_FILE"
    log_message "Backup directory: $BACKUP_DIR"
}

# Function to display script information
display_info() {
    echo -e "${BLUE}=== Disk Space Cleanup Script ===${NC}"
    echo -e "${BLUE}D796 Assessment - Disk Management${NC}"
    echo -e "${BLUE}=================================${NC}\n"
    
    echo -e "${YELLOW}Purpose:${NC} Assess and clean up disk space"
    echo -e "${YELLOW}Target Partition:${NC} / (root partition)"
    echo -e "${YELLOW}Timestamp:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    echo -e "${YELLOW}Backup Directory:${NC} $BACKUP_DIR"
    echo ""
}

# Function to get free disk space in bytes
get_free_disk_space() {
    local partition="$1"
    # Use df command to get free space in bytes (1K blocks * 1024)
    local free_space_kb=$(df "$partition" | tail -1 | awk '{print $4}')
    local free_space_bytes=$((free_space_kb * 1024))
    echo "$free_space_bytes"
}

# Function to format bytes to human readable format
format_bytes() {
    local bytes="$1"
    if [ "$bytes" -ge 1073741824 ]; then
        echo "$(echo "scale=2; $bytes / 1073741824" | bc)GB"
    elif [ "$bytes" -ge 1048576 ]; then
        echo "$(echo "scale=2; $bytes / 1048576" | bc)MB"
    elif [ "$bytes" -ge 1024 ]; then
        echo "$(echo "scale=2; $bytes / 1024" | bc)KB"
    else
        echo "${bytes}B"
    fi
}

# Function to display disk usage information
display_disk_usage() {
    local phase="$1"
    
    echo -e "\n${BLUE}=== Disk Usage ($phase Cleanup) ===${NC}"
    
    # Display overall disk usage
    echo -e "${YELLOW}Root Partition Usage:${NC}"
    df -h / | head -2
    
    # Display detailed usage of large directories
    echo -e "\n${YELLOW}Largest Directories in Root:${NC}"
    du -h --max-depth=1 / 2>/dev/null | sort -hr | head -10
    
    # Log disk usage information
    log_message "=== Disk Usage ($phase Cleanup) ==="
    df -h / >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    du -h --max-depth=1 / 2>/dev/null | sort -hr | head -10 >> "$LOG_FILE"
}

# Function to cleanDir() - deletes contents of directory given as first argument
cleanDir() {
    local target_dir="$1"
    local backup_important="$2"  # Optional: backup important files before deletion
    
    # Validate input
    if [ -z "$target_dir" ]; then
        log_error "cleanDir: No directory specified"
        return 1
    fi
    
    # Check if directory exists
    if [ ! -d "$target_dir" ]; then
        log_message "cleanDir: Directory does not exist: $target_dir"
        return 0
    fi
    
    # Check if directory is accessible
    if [ ! -r "$target_dir" ]; then
        log_error "cleanDir: Cannot read directory: $target_dir"
        return 1
    fi
    
    log_message "Cleaning directory: $target_dir"
    
    # Get initial size of directory
    local initial_size=$(du -sb "$target_dir" 2>/dev/null | awk '{print $1}')
    local initial_size_human=$(format_bytes "$initial_size")
    
    log_message "Initial size of $target_dir: $initial_size_human"
    
    # Create backup if requested and directory contains important files
    if [ "$backup_important" = "true" ]; then
        local backup_subdir="$BACKUP_DIR/$(basename "$target_dir")_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_subdir"
        
        # Backup configuration files and recent logs
        find "$target_dir" -name "*.conf" -o -name "*.cfg" -o -name "*.log" -mtime -7 2>/dev/null | \
        while IFS= read -r file; do
            if [ -f "$file" ]; then
                cp "$file" "$backup_subdir/" 2>/dev/null
                log_message "Backed up: $file"
            fi
        done
    fi
    
    # Count files before deletion
    local file_count=$(find "$target_dir" -type f 2>/dev/null | wc -l)
    local dir_count=$(find "$target_dir" -type d 2>/dev/null | wc -l)
    
    log_message "Files to delete: $file_count files, $dir_count directories"
    
    # Delete contents of directory (but not the directory itself)
    local deleted_files=0
    local deleted_dirs=0
    local errors=0
    
    # Delete files first
    find "$target_dir" -type f 2>/dev/null | while IFS= read -r file; do
        if rm -f "$file" 2>/dev/null; then
            ((deleted_files++))
        else
            ((errors++))
            log_error "Failed to delete file: $file"
        fi
    done
    
    # Delete empty directories
    find "$target_dir" -type d -empty 2>/dev/null | while IFS= read -r dir; do
        if [ "$dir" != "$target_dir" ]; then  # Don't delete the target directory itself
            if rmdir "$dir" 2>/dev/null; then
                ((deleted_dirs++))
            else
                log_error "Failed to delete directory: $dir"
            fi
        fi
    done
    
    # Get final size of directory
    local final_size=$(du -sb "$target_dir" 2>/dev/null | awk '{print $1}')
    local final_size_human=$(format_bytes "$final_size")
    local space_freed=$((initial_size - final_size))
    local space_freed_human=$(format_bytes "$space_freed")
    
    log_message "Cleanup completed for $target_dir"
    log_message "Final size: $final_size_human"
    log_message "Space freed: $space_freed_human"
    
    # Display results
    echo -e "${GREEN}✓ Cleaned: $target_dir${NC}"
    echo -e "  ${YELLOW}Initial size:${NC} $initial_size_human"
    echo -e "  ${YELLOW}Final size:${NC} $final_size_human"
    echo -e "  ${YELLOW}Space freed:${NC} $space_freed_human"
    
    return 0
}

# Function to get user confirmation for cleanup
get_cleanup_confirmation() {
    echo -e "\n${YELLOW}WARNING: This script will delete files from the following directories:${NC}"
    echo -e "${RED}  - /var/log (system logs)${NC}"
    echo -e "${RED}  - \$HOME/.cache (user cache files)${NC}"
    echo -e "${RED}  - /tmp (temporary files)${NC}"
    echo -e "${RED}  - /var/tmp (temporary files)${NC}"
    echo -e "${RED}  - /var/cache (package cache)${NC}"
    
    echo -e "\n${YELLOW}Important files will be backed up to: $BACKUP_DIR${NC}"
    echo -e "\n${RED}Are you sure you want to proceed? (yes/no):${NC}"
    
    read -r confirmation
    case "$confirmation" in
        [Yy][Ee][Ss]|[Yy])
            return 0
            ;;
        *)
            echo -e "${YELLOW}Cleanup cancelled by user.${NC}"
            return 1
            ;;
    esac
}

# Function to check if running as root for system directories
check_permissions() {
    local need_sudo=false
    
    # Check if we need sudo for system directories
    if [ ! -w /var/log ] || [ ! -w /var/cache ] || [ ! -w /var/tmp ]; then
        need_sudo=true
    fi
    
    if [ "$need_sudo" = true ]; then
        echo -e "${YELLOW}This script requires sudo privileges to clean system directories.${NC}"
        echo -e "${YELLOW}You may be prompted for your password.${NC}"
        
        # Test sudo access
        if ! sudo -n true 2>/dev/null; then
            echo -e "${YELLOW}Testing sudo access...${NC}"
            if ! sudo true; then
                log_error "Sudo access required but not available"
                return 1
            fi
        fi
    fi
    
    return 0
}

# Main function
main() {
    local start_time=$(date +%s)
    
    # Setup logging
    setup_logging
    
    # Display script information
    display_info
    
    # Check permissions
    if ! check_permissions; then
        log_error "Insufficient permissions to run cleanup"
        exit 1
    fi
    
    # 1. Find the free disk space in the root partition and store it in a variable
    echo -e "${BLUE}Step 1: Assessing initial disk space...${NC}"
    local initial_free_space=$(get_free_disk_space "/")
    local initial_free_space_human=$(format_bytes "$initial_free_space")
    
    log_message "Initial free disk space: $initial_free_space_human ($initial_free_space bytes)"
    echo -e "${YELLOW}Initial free space:${NC} $initial_free_space_human"
    
    # Display initial disk usage
    display_disk_usage "Before"
    
    # Get user confirmation
    if ! get_cleanup_confirmation; then
        log_message "Cleanup cancelled by user"
        exit 0
    fi
    
    # 3. Declare a variable containing a list of directories to clean
    echo -e "\n${BLUE}Step 2: Preparing directory list for cleanup...${NC}"
    
    # Define directories to clean
    local directories_to_clean=(
        "/var/log"
        "$HOME/.cache"
        "/tmp"
        "/var/tmp"
        "/var/cache"
    )
    
    log_message "Directories scheduled for cleanup:"
    for dir in "${directories_to_clean[@]}"; do
        log_message "  - $dir"
        echo -e "  ${YELLOW}→${NC} $dir"
    done
    
    # 4. Delete all files and subdirectories using for loop and cleanDir() function
    echo -e "\n${BLUE}Step 3: Cleaning directories...${NC}"
    
    local total_space_freed=0
    local successful_cleanups=0
    local failed_cleanups=0
    
    for directory in "${directories_to_clean[@]}"; do
        echo -e "\n${YELLOW}Processing: $directory${NC}"
        
        # Get space before cleanup
        local space_before=0
        if [ -d "$directory" ]; then
            space_before=$(du -sb "$directory" 2>/dev/null | awk '{print $1}')
        fi
        
        # Determine if we need sudo and if we should backup
        local use_sudo=false
        local backup_files=false
        
        case "$directory" in
            "/var/log")
                use_sudo=true
                backup_files=true
                ;;
            "/var/cache"|"/var/tmp"|"/tmp")
                use_sudo=true
                backup_files=false
                ;;
            "$HOME/.cache")
                use_sudo=false
                backup_files=false
                ;;
        esac
        
        # Clean the directory
        if [ "$use_sudo" = true ]; then
            # For system directories, we need a different approach
            if [ -d "$directory" ]; then
                log_message "Cleaning system directory: $directory (requires sudo)"
                
                # Backup important files if needed
                if [ "$backup_files" = true ]; then
                    local backup_subdir="$BACKUP_DIR/$(basename "$directory")_$(date +%Y%m%d_%H%M%S)"
                    mkdir -p "$backup_subdir"
                    
                    # Backup recent important log files
                    sudo find "$directory" -name "*.log" -mtime -7 -exec cp {} "$backup_subdir/" \; 2>/dev/null
                    log_message "Backed up recent log files to $backup_subdir"
                fi
                
                # Clean the directory contents
                if sudo find "$directory" -type f -delete 2>/dev/null && \
                   sudo find "$directory" -type d -empty -delete 2>/dev/null; then
                    ((successful_cleanups++))
                    echo -e "${GREEN}✓ Successfully cleaned: $directory${NC}"
                    log_message "Successfully cleaned system directory: $directory"
                else
                    ((failed_cleanups++))
                    echo -e "${RED}✗ Failed to clean: $directory${NC}"
                    log_error "Failed to clean system directory: $directory"
                fi
            else
                echo -e "${YELLOW}⚠ Directory does not exist: $directory${NC}"
                log_message "Directory does not exist: $directory"
            fi
        else
            # For user directories, use our cleanDir function
            if cleanDir "$directory" "$backup_files"; then
                ((successful_cleanups++))
            else
                ((failed_cleanups++))
            fi
        fi
        
        # Calculate space freed for this directory
        local space_after=0
        if [ -d "$directory" ]; then
            space_after=$(du -sb "$directory" 2>/dev/null | awk '{print $1}')
        fi
        
        local space_freed_this_dir=$((space_before - space_after))
        total_space_freed=$((total_space_freed + space_freed_this_dir))
        
        if [ $space_freed_this_dir -gt 0 ]; then
            local space_freed_human=$(format_bytes "$space_freed_this_dir")
            echo -e "  ${GREEN}Space freed: $space_freed_human${NC}"
        fi
    done
    
    # 5. Find free disk space after cleanup and report results
    echo -e "\n${BLUE}Step 4: Assessing final disk space...${NC}"
    
    local final_free_space=$(get_free_disk_space "/")
    local final_free_space_human=$(format_bytes "$final_free_space")
    local net_space_freed=$((final_free_space - initial_free_space))
    local net_space_freed_human=$(format_bytes "$net_space_freed")
    
    log_message "Final free disk space: $final_free_space_human ($final_free_space bytes)"
    log_message "Net space freed: $net_space_freed_human ($net_space_freed bytes)"
    
    # Display final disk usage
    display_disk_usage "After"
    
    # Report results
    echo -e "\n${BLUE}=== Cleanup Summary ===${NC}"
    echo -e "${YELLOW}Initial free space:${NC} $initial_free_space_human"
    echo -e "${YELLOW}Final free space:${NC} $final_free_space_human"
    echo -e "${YELLOW}Net space freed:${NC} $net_space_freed_human"
    echo -e "${YELLOW}Successful cleanups:${NC} $successful_cleanups"
    echo -e "${YELLOW}Failed cleanups:${NC} $failed_cleanups"
    
    # Determine response based on space freed
    if [ "$net_space_freed" -gt 0 ]; then
        echo -e "\n${GREEN}✓ Disk cleanup completed successfully!${NC}"
        echo -e "${GREEN}Freed $net_space_freed_human of disk space.${NC}"
        log_message "SUCCESS: Disk cleanup completed - freed $net_space_freed_human"
    else
        echo -e "\n${YELLOW}No significant disk space was freed${NC}"
        echo -e "${YELLOW}This may indicate:${NC}"
        echo -e "${YELLOW}  - Directories were already clean${NC}"
        echo -e "${YELLOW}  - Files were recreated during cleanup${NC}"
        echo -e "${YELLOW}  - Cleanup had limited effect${NC}"
        log_message "INFO: No significant disk space was freed"
    fi
    
    # Calculate and log execution time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo -e "\n${BLUE}=== Execution Summary ===${NC}"
    echo -e "${YELLOW}Duration:${NC} ${duration}s"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    echo -e "${YELLOW}Backup Directory:${NC} $BACKUP_DIR"
    
    log_message "Disk cleanup script completed - Duration: ${duration}s"
    log_message "Script finished"
    
    # Exit with appropriate code
    if [ "$failed_cleanups" -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Function to show script usage
show_usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  --dry-run          Show what would be cleaned without actually doing it"
    echo -e "  --force            Skip confirmation prompts"
    echo -e "  --no-backup        Don't backup important files"
    echo -e "  --help             Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0                 Run interactive cleanup"
    echo -e "  $0 --dry-run       Preview cleanup actions"
    echo -e "  $0 --force         Run cleanup without confirmation"
}

# Function to perform dry run
perform_dry_run() {
    echo -e "${BLUE}=== Dry Run Mode ===${NC}"
    echo -e "${YELLOW}This shows what would be cleaned without actually doing it${NC}\n"
    
    local directories_to_clean=(
        "/var/log"
        "$HOME/.cache"
        "/tmp"
        "/var/tmp"
        "/var/cache"
    )
    
    echo -e "${BLUE}Directories that would be cleaned:${NC}"
    for directory in "${directories_to_clean[@]}"; do
        if [ -d "$directory" ]; then
            local size=$(du -sh "$directory" 2>/dev/null | awk '{print $1}')
            local file_count=$(find "$directory" -type f 2>/dev/null | wc -l)
            echo -e "  ${YELLOW}→${NC} $directory (${size}, ${file_count} files)"
        else
            echo -e "  ${YELLOW}→${NC} $directory ${RED}(does not exist)${NC}"
        fi
    done
    
    echo -e "\n${YELLOW}Current disk usage:${NC}"
    df -h /
    
    echo -e "\n${GREEN}No files were actually deleted (dry run mode)${NC}"
}

# Handle command line arguments
DRY_RUN=false
FORCE=false
NO_BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --no-backup)
            NO_BACKUP=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# Execute based on mode
if [ "$DRY_RUN" = true ]; then
    perform_dry_run
else
    # Override confirmation function if force mode
    if [ "$FORCE" = true ]; then
        get_cleanup_confirmation() {
            echo -e "${YELLOW}Force mode enabled - skipping confirmation${NC}"
            return 0
        }
    fi
    
    # Execute main function
    main
fi