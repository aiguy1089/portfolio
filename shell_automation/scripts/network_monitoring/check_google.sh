#!/bin/bash

# check_google.sh - Script to check if system can reach google.com by pinging it
# Part E.1 of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
TARGET="google.com"
PING_COUNT=4
TIMEOUT=10
LOG_FILE="$HOME/D796/logs/network_check.log"

# Function to log messages with timestamp
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [GOOGLE_PING] $message" >> "$LOG_FILE"
}

# Function to setup logging
setup_logging() {
    local log_dir=$(dirname "$LOG_FILE")
    if [ ! -d "$log_dir" ]; then
        mkdir -p "$log_dir"
    fi
    
    # Log script start
    log_message "Script started - checking connectivity to $TARGET"
}

# Function to display script information
display_info() {
    echo -e "${BLUE}=== Google Connectivity Check ===${NC}"
    echo -e "${BLUE}D796 Assessment - Network Monitoring${NC}"
    echo -e "${BLUE}===================================${NC}\n"
    
    echo -e "${YELLOW}Target:${NC} $TARGET"
    echo -e "${YELLOW}Ping Count:${NC} $PING_COUNT packets"
    echo -e "${YELLOW}Timeout:${NC} $TIMEOUT seconds"
    echo -e "${YELLOW}Timestamp:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    echo ""
}

# Function to perform ping test
perform_ping_test() {
    local target="$1"
    local count="$2"
    local timeout="$3"
    
    echo -e "${BLUE}Testing connectivity to $target...${NC}"
    log_message "Starting ping test to $target ($count packets, ${timeout}s timeout)"
    
    # Execute ping command and capture output
    local ping_output
    local ping_exit_code
    
    # Use timeout command to limit ping duration
    ping_output=$(timeout "$timeout" ping -c "$count" "$target" 2>&1)
    ping_exit_code=$?
    
    # Log the raw ping output
    log_message "Ping command output:"
    echo "$ping_output" | while IFS= read -r line; do
        log_message "  $line"
    done
    log_message "Ping exit code: $ping_exit_code"
    
    return $ping_exit_code
}

# Function to analyze ping results
analyze_ping_results() {
    local ping_output="$1"
    local exit_code="$2"
    
    # Extract statistics from ping output
    local packets_transmitted=$(echo "$ping_output" | grep "packets transmitted" | awk '{print $1}')
    local packets_received=$(echo "$ping_output" | grep "packets transmitted" | awk '{print $4}')
    local packet_loss=$(echo "$ping_output" | grep "packet loss" | awk '{print $6}')
    local avg_time=$(echo "$ping_output" | grep "rtt min/avg/max/mdev" | awk -F'/' '{print $5}')
    
    # Log detailed statistics
    log_message "Ping Statistics:"
    log_message "  Packets transmitted: ${packets_transmitted:-N/A}"
    log_message "  Packets received: ${packets_received:-N/A}"
    log_message "  Packet loss: ${packet_loss:-N/A}"
    log_message "  Average response time: ${avg_time:-N/A}ms"
    
    # Display results to user
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ Ping successful!${NC}"
        if [ -n "$packets_transmitted" ] && [ -n "$packets_received" ]; then
            echo -e "${YELLOW}Packets:${NC} $packets_received/$packets_transmitted received"
        fi
        if [ -n "$packet_loss" ]; then
            echo -e "${YELLOW}Packet Loss:${NC} $packet_loss"
        fi
        if [ -n "$avg_time" ]; then
            echo -e "${YELLOW}Average Response Time:${NC} ${avg_time}ms"
        fi
    else
        echo -e "${RED}✗ Ping failed!${NC}"
        echo -e "${RED}Error Details:${NC}"
        echo "$ping_output" | grep -E "(unreachable|timeout|failed|error)" | head -3
    fi
    
    return $exit_code
}

# Function to determine network status and display appropriate message
determine_network_status() {
    local exit_code="$1"
    local ping_output="$2"
    
    if [ $exit_code -eq 0 ]; then
        # Success case - network is up
        echo -e "\n${GREEN}Network is up.${NC}"
        log_message "SUCCESS: Network connectivity confirmed - $TARGET is reachable"
        return 0
    else
        # Failure case - analyze the type of failure
        echo -e "\n${RED}Network connectivity issue detected.${NC}"
        
        if echo "$ping_output" | grep -q "Name or service not known"; then
            echo -e "${RED}Issue: DNS resolution failed for $TARGET${NC}"
            log_message "FAILURE: DNS resolution failed for $TARGET"
        elif echo "$ping_output" | grep -q "Network is unreachable"; then
            echo -e "${RED}Issue: Network is unreachable${NC}"
            log_message "FAILURE: Network is unreachable"
        elif echo "$ping_output" | grep -q "Destination Host Unreachable"; then
            echo -e "${RED}Issue: Destination host unreachable${NC}"
            log_message "FAILURE: Destination host unreachable"
        elif echo "$ping_output" | grep -q "timeout"; then
            echo -e "${RED}Issue: Connection timeout${NC}"
            log_message "FAILURE: Connection timeout to $TARGET"
        else
            echo -e "${RED}Issue: Unknown network problem${NC}"
            log_message "FAILURE: Unknown network problem (exit code: $exit_code)"
        fi
        
        return 1
    fi
}

# Function to display troubleshooting suggestions
display_troubleshooting() {
    local exit_code="$1"
    
    if [ $exit_code -ne 0 ]; then
        echo -e "\n${BLUE}=== Troubleshooting Suggestions ===${NC}"
        echo -e "${YELLOW}1. Check network cable/WiFi connection${NC}"
        echo -e "${YELLOW}2. Verify network interface is up: ip link show${NC}"
        echo -e "${YELLOW}3. Check default gateway: ip route show default${NC}"
        echo -e "${YELLOW}4. Test DNS resolution: nslookup $TARGET${NC}"
        echo -e "${YELLOW}5. Try pinging local gateway first${NC}"
        echo -e "${YELLOW}6. Check firewall settings${NC}"
        echo -e "${YELLOW}7. Verify internet service provider connectivity${NC}"
    fi
}

# Function to run additional diagnostic tests
run_diagnostics() {
    local exit_code="$1"
    
    if [ $exit_code -ne 0 ]; then
        echo -e "\n${BLUE}=== Running Additional Diagnostics ===${NC}"
        
        # Check network interface status
        echo -e "${YELLOW}Network Interfaces:${NC}"
        ip link show | grep -E "^[0-9]+:" | head -3
        
        # Check default route
        echo -e "\n${YELLOW}Default Route:${NC}"
        ip route show default 2>/dev/null || echo "No default route found"
        
        # Check DNS configuration
        echo -e "\n${YELLOW}DNS Configuration:${NC}"
        if [ -f /etc/resolv.conf ]; then
            grep nameserver /etc/resolv.conf | head -2
        else
            echo "DNS configuration not found"
        fi
        
        # Log diagnostic information
        log_message "Diagnostic Information:"
        log_message "  Network interfaces: $(ip link show | grep -E '^[0-9]+:' | wc -l) found"
        log_message "  Default route: $(ip route show default 2>/dev/null | wc -l) found"
        log_message "  DNS servers: $(grep -c nameserver /etc/resolv.conf 2>/dev/null || echo 0) configured"
    fi
}

# Main function
main() {
    local start_time=$(date +%s)
    
    # Setup logging
    setup_logging
    
    # Display script information
    display_info
    
    # Perform ping test
    local ping_output
    local ping_exit_code
    
    ping_output=$(timeout "$TIMEOUT" ping -c "$PING_COUNT" "$TARGET" 2>&1)
    ping_exit_code=$?
    
    # Analyze results
    analyze_ping_results "$ping_output" "$ping_exit_code"
    
    # Determine and display network status
    determine_network_status "$ping_exit_code" "$ping_output"
    local final_status=$?
    
    # Run diagnostics if there were issues
    run_diagnostics "$ping_exit_code"
    
    # Display troubleshooting suggestions if needed
    display_troubleshooting "$ping_exit_code"
    
    # Calculate and log execution time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo -e "\n${BLUE}=== Test Summary ===${NC}"
    echo -e "${YELLOW}Target:${NC} $TARGET"
    echo -e "${YELLOW}Result:${NC} $([ $final_status -eq 0 ] && echo -e "${GREEN}SUCCESS${NC}" || echo -e "${RED}FAILURE${NC}")"
    echo -e "${YELLOW}Duration:${NC} ${duration}s"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    
    # Final logging
    log_message "Test completed - Duration: ${duration}s, Status: $([ $final_status -eq 0 ] && echo "SUCCESS" || echo "FAILURE")"
    log_message "Script finished"
    
    exit $final_status
}

# Function to show script usage
show_usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  --target <host>    Specify target host (default: $TARGET)"
    echo -e "  --count <num>      Number of ping packets (default: $PING_COUNT)"
    echo -e "  --timeout <sec>    Timeout in seconds (default: $TIMEOUT)"
    echo -e "  --quiet            Suppress detailed output"
    echo -e "  --help             Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0                 Test connectivity to google.com"
    echo -e "  $0 --target yahoo.com --count 2"
    echo -e "  $0 --quiet         Run with minimal output"
}

# Handle command line arguments
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --count)
            PING_COUNT="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --quiet)
            QUIET=true
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

# Validate numeric arguments
if ! [[ "$PING_COUNT" =~ ^[0-9]+$ ]] || [ "$PING_COUNT" -lt 1 ]; then
    echo -e "${RED}Error: Ping count must be a positive integer${NC}"
    exit 1
fi

if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]] || [ "$TIMEOUT" -lt 1 ]; then
    echo -e "${RED}Error: Timeout must be a positive integer${NC}"
    exit 1
fi

# Execute main function
main