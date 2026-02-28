#!/bin/bash

# archive_compress.sh - Script to archive and compress files and directories
# Part G of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
SOURCE_DIR="/etc"
OUTPUT_DIR="$HOME/D796/archives"
LOG_FILE="$HOME/D796/logs/archive_compress.log"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

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

# Function to setup logging and directories
setup_environment() {
    # Create output directory if it doesn't exist
    if [ ! -d "$OUTPUT_DIR" ]; then
        mkdir -p "$OUTPUT_DIR"
        log_message "Created output directory: $OUTPUT_DIR"
    fi
    
    # Create log directory if it doesn't exist
    local log_dir=$(dirname "$LOG_FILE")
    if [ ! -d "$log_dir" ]; then
        mkdir -p "$log_dir"
    fi
    
    # Create new log file
    touch "$LOG_FILE"
    log_message "Archive and compression script started"
    log_message "Source directory: $SOURCE_DIR"
    log_message "Output directory: $OUTPUT_DIR"
    log_message "Log file: $LOG_FILE"
}

# Function to display script information
display_info() {
    echo -e "${BLUE}=== File Archive and Compression Script ===${NC}"
    echo -e "${BLUE}D796 Assessment - File Archiving${NC}"
    echo -e "${BLUE}=======================================${NC}\n"
    
    echo -e "${YELLOW}Source Directory:${NC} $SOURCE_DIR"
    echo -e "${YELLOW}Output Directory:${NC} $OUTPUT_DIR"
    echo -e "${YELLOW}Timestamp:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    echo -e "${YELLOW}Archive Timestamp:${NC} $TIMESTAMP"
    echo ""
}

# 1. Function to find out the size of a file given as an argument
fileSize() {
    local file_path="$1"
    
    # Validate input
    if [ -z "$file_path" ]; then
        log_error "fileSize: No file path specified"
        return 1
    fi
    
    # Check if file exists
    if [ ! -f "$file_path" ]; then
        log_error "fileSize: File does not exist: $file_path"
        return 1
    fi
    
    # Get file size in bytes
    local size_bytes=$(stat -c%s "$file_path" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$size_bytes" ]; then
        echo "$size_bytes"
        return 0
    else
        log_error "fileSize: Unable to determine size of file: $file_path"
        return 1
    fi
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

# Function to check if we have necessary permissions
check_permissions() {
    echo -e "${BLUE}Checking permissions...${NC}"
    
    # Check if source directory is readable
    if [ ! -r "$SOURCE_DIR" ]; then
        log_error "Cannot read source directory: $SOURCE_DIR"
        echo -e "${RED}Error: Cannot read source directory. This script requires sudo privileges.${NC}"
        return 1
    fi
    
    # Check if output directory is writable
    if [ ! -w "$OUTPUT_DIR" ]; then
        log_error "Cannot write to output directory: $OUTPUT_DIR"
        return 1
    fi
    
    # Check if we need sudo for accessing /etc
    if [ "$SOURCE_DIR" = "/etc" ] && [ "$(id -u)" -ne 0 ]; then
        echo -e "${YELLOW}This script requires sudo privileges to access /etc directory.${NC}"
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
    
    log_message "Permission check completed successfully"
    return 0
}

# Function to analyze source directory
analyze_source_directory() {
    local source_dir="$1"
    
    echo -e "${BLUE}Analyzing source directory: $source_dir${NC}"
    
    if [ ! -d "$source_dir" ]; then
        log_error "Source directory does not exist: $source_dir"
        return 1
    fi
    
    # Count files and directories
    local file_count=$(sudo find "$source_dir" -type f 2>/dev/null | wc -l)
    local dir_count=$(sudo find "$source_dir" -type d 2>/dev/null | wc -l)
    local total_size=$(sudo du -sb "$source_dir" 2>/dev/null | awk '{print $1}')
    local total_size_human=$(format_bytes "$total_size")
    
    echo -e "${YELLOW}Source Analysis:${NC}"
    echo -e "  ${YELLOW}Files:${NC} $file_count"
    echo -e "  ${YELLOW}Directories:${NC} $dir_count"
    echo -e "  ${YELLOW}Total Size:${NC} $total_size_human ($total_size bytes)"
    
    log_message "Source directory analysis:"
    log_message "  Files: $file_count"
    log_message "  Directories: $dir_count"
    log_message "  Total size: $total_size_human ($total_size bytes)"
    
    return 0
}

# 2. Function to archive and compress using tar and gzip
create_gzip_archive() {
    local source_dir="$1"
    local output_file="$OUTPUT_DIR/etc_backup_${TIMESTAMP}.tar.gz"
    
    echo -e "\n${BLUE}Creating gzip compressed archive...${NC}"
    log_message "Starting gzip compression: $output_file"
    
    local start_time=$(date +%s)
    
    # Create tar.gz archive
    if sudo tar -czf "$output_file" -C "$(dirname "$source_dir")" "$(basename "$source_dir")" 2>/dev/null; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        echo -e "${GREEN}✓ Gzip archive created successfully${NC}"
        echo -e "  ${YELLOW}File:${NC} $output_file"
        echo -e "  ${YELLOW}Compression time:${NC} ${duration}s"
        
        log_message "Gzip archive created successfully in ${duration}s"
        log_message "Gzip archive location: $output_file"
        
        # Change ownership to current user if created with sudo
        if [ "$(id -u)" -ne 0 ]; then
            sudo chown "$(id -u):$(id -g)" "$output_file"
        fi
        
        echo "$output_file"
        return 0
    else
        log_error "Failed to create gzip archive"
        echo -e "${RED}✗ Failed to create gzip archive${NC}"
        return 1
    fi
}

# 3. Function to archive and compress using tar and bzip2
create_bzip2_archive() {
    local source_dir="$1"
    local output_file="$OUTPUT_DIR/etc_backup_${TIMESTAMP}.tar.bz2"
    
    echo -e "\n${BLUE}Creating bzip2 compressed archive...${NC}"
    log_message "Starting bzip2 compression: $output_file"
    
    local start_time=$(date +%s)
    
    # Create tar.bz2 archive
    if sudo tar -cjf "$output_file" -C "$(dirname "$source_dir")" "$(basename "$source_dir")" 2>/dev/null; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        echo -e "${GREEN}✓ Bzip2 archive created successfully${NC}"
        echo -e "  ${YELLOW}File:${NC} $output_file"
        echo -e "  ${YELLOW}Compression time:${NC} ${duration}s"
        
        log_message "Bzip2 archive created successfully in ${duration}s"
        log_message "Bzip2 archive location: $output_file"
        
        # Change ownership to current user if created with sudo
        if [ "$(id -u)" -ne 0 ]; then
            sudo chown "$(id -u):$(id -g)" "$output_file"
        fi
        
        echo "$output_file"
        return 0
    else
        log_error "Failed to create bzip2 archive"
        echo -e "${RED}✗ Failed to create bzip2 archive${NC}"
        return 1
    fi
}

# Function to verify archive integrity
verify_archive() {
    local archive_file="$1"
    local archive_type="$2"
    
    echo -e "${YELLOW}Verifying archive integrity: $(basename "$archive_file")${NC}"
    
    case "$archive_type" in
        "gzip")
            if tar -tzf "$archive_file" >/dev/null 2>&1; then
                echo -e "${GREEN}✓ Gzip archive integrity verified${NC}"
                log_message "Gzip archive integrity verified: $archive_file"
                return 0
            else
                echo -e "${RED}✗ Gzip archive integrity check failed${NC}"
                log_error "Gzip archive integrity check failed: $archive_file"
                return 1
            fi
            ;;
        "bzip2")
            if tar -tjf "$archive_file" >/dev/null 2>&1; then
                echo -e "${GREEN}✓ Bzip2 archive integrity verified${NC}"
                log_message "Bzip2 archive integrity verified: $archive_file"
                return 0
            else
                echo -e "${RED}✗ Bzip2 archive integrity check failed${NC}"
                log_error "Bzip2 archive integrity check failed: $archive_file"
                return 1
            fi
            ;;
        *)
            log_error "Unknown archive type for verification: $archive_type"
            return 1
            ;;
    esac
}

# Function to get compression statistics
get_compression_stats() {
    local original_size="$1"
    local compressed_size="$2"
    local compression_type="$3"
    
    local compression_ratio=$(echo "scale=2; ($original_size - $compressed_size) * 100 / $original_size" | bc)
    local size_ratio=$(echo "scale=2; $compressed_size * 100 / $original_size" | bc)
    
    echo -e "  ${YELLOW}Original size:${NC} $(format_bytes "$original_size")"
    echo -e "  ${YELLOW}Compressed size:${NC} $(format_bytes "$compressed_size")"
    echo -e "  ${YELLOW}Compression ratio:${NC} ${compression_ratio}%"
    echo -e "  ${YELLOW}Size ratio:${NC} ${size_ratio}%"
    
    log_message "$compression_type compression statistics:"
    log_message "  Original size: $(format_bytes "$original_size") ($original_size bytes)"
    log_message "  Compressed size: $(format_bytes "$compressed_size") ($compressed_size bytes)"
    log_message "  Compression ratio: ${compression_ratio}%"
    log_message "  Size ratio: ${size_ratio}%"
}

# Main function
main() {
    local start_time=$(date +%s)
    
    # Setup environment
    setup_environment
    
    # Display script information
    display_info
    
    # Check permissions
    if ! check_permissions; then
        log_error "Permission check failed"
        exit 1
    fi
    
    # Analyze source directory
    if ! analyze_source_directory "$SOURCE_DIR"; then
        log_error "Source directory analysis failed"
        exit 1
    fi
    
    # Get original size for comparison
    local original_size=$(sudo du -sb "$SOURCE_DIR" 2>/dev/null | awk '{print $1}')
    
    # 2. Archive and compress using tar and gzip
    local gzip_file
    if gzip_file=$(create_gzip_archive "$SOURCE_DIR"); then
        # Verify gzip archive
        verify_archive "$gzip_file" "gzip"
    else
        log_error "Gzip archive creation failed"
        exit 1
    fi
    
    # 3. Archive and compress using tar and bzip2
    local bzip2_file
    if bzip2_file=$(create_bzip2_archive "$SOURCE_DIR"); then
        # Verify bzip2 archive
        verify_archive "$bzip2_file" "bzip2"
    else
        log_error "Bzip2 archive creation failed"
        exit 1
    fi
    
    # 4. Calculate the size of the two compressed files using fileSize() function
    echo -e "\n${BLUE}Calculating archive sizes...${NC}"
    
    local gzip_size
    local bzip2_size
    
    if gzip_size=$(fileSize "$gzip_file"); then
        echo -e "${GREEN}✓ Gzip archive size calculated${NC}"
        log_message "Gzip archive size: $(format_bytes "$gzip_size") ($gzip_size bytes)"
    else
        log_error "Failed to calculate gzip archive size"
        exit 1
    fi
    
    if bzip2_size=$(fileSize "$bzip2_file"); then
        echo -e "${GREEN}✓ Bzip2 archive size calculated${NC}"
        log_message "Bzip2 archive size: $(format_bytes "$bzip2_size") ($bzip2_size bytes)"
    else
        log_error "Failed to calculate bzip2 archive size"
        exit 1
    fi
    
    # 5. Display the difference in size between the two compression algorithms
    echo -e "\n${BLUE}=== Compression Comparison ===${NC}"
    
    echo -e "\n${YELLOW}Gzip Compression (tar.gz):${NC}"
    get_compression_stats "$original_size" "$gzip_size" "Gzip"
    
    echo -e "\n${YELLOW}Bzip2 Compression (tar.bz2):${NC}"
    get_compression_stats "$original_size" "$bzip2_size" "Bzip2"
    
    # Calculate difference between compression methods
    local size_difference=$((gzip_size - bzip2_size))
    local size_difference_abs=${size_difference#-}  # Absolute value
    local percentage_difference
    
    if [ "$gzip_size" -gt 0 ]; then
        percentage_difference=$(echo "scale=2; $size_difference_abs * 100 / $gzip_size" | bc)
    else
        percentage_difference="0"
    fi
    
    echo -e "\n${BLUE}=== Size Difference Analysis ===${NC}"
    echo -e "${YELLOW}Gzip archive size:${NC} $(format_bytes "$gzip_size")"
    echo -e "${YELLOW}Bzip2 archive size:${NC} $(format_bytes "$bzip2_size")"
    
    if [ "$size_difference" -gt 0 ]; then
        echo -e "${YELLOW}Difference:${NC} Bzip2 is $(format_bytes "$size_difference_abs") smaller (${percentage_difference}% reduction)"
        echo -e "${GREEN}✓ Bzip2 provides better compression${NC}"
        log_message "Compression comparison: Bzip2 is $(format_bytes "$size_difference_abs") smaller than gzip"
    elif [ "$size_difference" -lt 0 ]; then
        echo -e "${YELLOW}Difference:${NC} Gzip is $(format_bytes "$size_difference_abs") smaller (${percentage_difference}% reduction)"
        echo -e "${GREEN}✓ Gzip provides better compression${NC}"
        log_message "Compression comparison: Gzip is $(format_bytes "$size_difference_abs") smaller than bzip2"
    else
        echo -e "${YELLOW}Difference:${NC} Both archives are the same size"
        log_message "Compression comparison: Both archives are the same size"
    fi
    
    # Additional analysis
    echo -e "\n${BLUE}=== Compression Algorithm Analysis ===${NC}"
    echo -e "${YELLOW}Gzip characteristics:${NC}"
    echo -e "  • Faster compression and decompression"
    echo -e "  • Lower CPU usage"
    echo -e "  • Good for frequently accessed archives"
    echo -e "  • Widely supported"
    
    echo -e "\n${YELLOW}Bzip2 characteristics:${NC}"
    echo -e "  • Better compression ratio (usually smaller files)"
    echo -e "  • Higher CPU usage"
    echo -e "  • Good for long-term storage"
    echo -e "  • Slower but more efficient compression"
    
    # Calculate and log execution time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo -e "\n${BLUE}=== Archive Summary ===${NC}"
    echo -e "${YELLOW}Source Directory:${NC} $SOURCE_DIR"
    echo -e "${YELLOW}Original Size:${NC} $(format_bytes "$original_size")"
    echo -e "${YELLOW}Gzip Archive:${NC} $(basename "$gzip_file") ($(format_bytes "$gzip_size"))"
    echo -e "${YELLOW}Bzip2 Archive:${NC} $(basename "$bzip2_file") ($(format_bytes "$bzip2_size"))"
    echo -e "${YELLOW}Output Directory:${NC} $OUTPUT_DIR"
    echo -e "${YELLOW}Total Duration:${NC} ${duration}s"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    
    # Final logging
    log_message "Archive creation completed successfully"
    log_message "Total execution time: ${duration}s"
    log_message "Gzip archive: $gzip_file ($(format_bytes "$gzip_size"))"
    log_message "Bzip2 archive: $bzip2_file ($(format_bytes "$bzip2_size"))"
    log_message "Script finished"
    
    echo -e "\n${GREEN}✓ Archive and compression completed successfully!${NC}"
    exit 0
}

# Function to show script usage
show_usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  --source <dir>     Specify source directory (default: $SOURCE_DIR)"
    echo -e "  --output <dir>     Specify output directory (default: $OUTPUT_DIR)"
    echo -e "  --test             Test with a smaller directory"
    echo -e "  --help             Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0                 Archive /etc directory (default)"
    echo -e "  $0 --source /var/log --output /tmp/archives"
    echo -e "  $0 --test          Test with /etc/systemd directory"
}

# Function to run test mode
run_test_mode() {
    echo -e "${BLUE}=== Test Mode ===${NC}"
    echo -e "${YELLOW}Using smaller test directory for demonstration${NC}\n"
    
    # Use a smaller subdirectory for testing
    SOURCE_DIR="/etc/systemd"
    
    if [ ! -d "$SOURCE_DIR" ]; then
        SOURCE_DIR="/etc/ssh"
    fi
    
    if [ ! -d "$SOURCE_DIR" ]; then
        echo -e "${RED}No suitable test directory found${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Test source directory:${NC} $SOURCE_DIR"
    main
}

# Handle command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE_DIR="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --test)
            run_test_mode
            exit 0
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

# Validate arguments
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: Source directory does not exist: $SOURCE_DIR${NC}"
    exit 1
fi

# Execute main function
main