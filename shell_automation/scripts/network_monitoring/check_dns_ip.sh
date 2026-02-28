#!/bin/bash

# check_dns_ip.sh - Script to check if local machine can connect to Google DNS IP (8.8.8.8)
# Part E.2 of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
DNS_IP="8.8.8.8"
PING_COUNT=4
TIMEOUT=10
LOG_FILE="$HOME/D796/logs/network_check.log"

# Function to log messages with timestamp
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [DNS_IP_PING] $message" >> "$LOG_FILE"
}

# Function to setup logging
setup_logging() {
    local log_dir=$(dirname "$LOG_FILE")
    if [ ! -d "$log_dir" ]; then
        mkdir -p "$log_dir"
    fi
    
    # Log script start
    log_message "Script started - checking connectivity to Google DNS IP $DNS_IP"
}

# Function to display script information
display_info() {
    echo -e "${BLUE}=== Google DNS IP Connectivity Check ===${NC}"
    echo -e "${BLUE}D796 Assessment - Network Monitoring${NC}"
    echo -e "${BLUE}=======================================${NC}\n"
    
    echo -e "${YELLOW}Target DNS IP:${NC} $DNS_IP (Google Public DNS)"
    echo -e "${YELLOW}Ping Count:${NC} $PING_COUNT packets"
    echo -e "${YELLOW}Timeout:${NC} $TIMEOUT seconds"
    echo -e "${YELLOW}Timestamp:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    echo -e "${YELLOW}Purpose:${NC} Test direct IP connectivity (bypasses DNS resolution)"
    echo ""
}

# Function to validate IP address format
validate_ip() {
    local ip="$1"
    local valid_ip_regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"
    
    if [[ $ip =~ $valid_ip_regex ]]; then
        # Check each octet is between 0-255
        IFS='.' read -ra ADDR <<< "$ip"
        for i in "${ADDR[@]}"; do
            if [ "$i" -gt 255 ] || [ "$i" -lt 0 ]; then
                return 1
            fi
        done
        return 0
    else
        return 1
    fi
}

# Function to perform ping test to DNS IP
perform_dns_ip_test() {
    local dns_ip="$1"
    local count="$2"
    local timeout="$3"
    
    echo -e "${BLUE}Testing direct IP connectivity to $dns_ip...${NC}"
    log_message "Starting ping test to DNS IP $dns_ip ($count packets, ${timeout}s timeout)"
    
    # Validate IP address format
    if ! validate_ip "$dns_ip"; then
        echo -e "${RED}Error: Invalid IP address format: $dns_ip${NC}"
        log_message "ERROR: Invalid IP address format: $dns_ip"
        return 2
    fi
    
    # Execute ping command and capture output
    local ping_output
    local ping_exit_code
    
    # Use timeout command to limit ping duration
    ping_output=$(timeout "$timeout" ping -c "$count" "$dns_ip" 2>&1)
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
    local min_time=$(echo "$ping_output" | grep "rtt min/avg/max/mdev" | awk -F'/' '{print $4}')
    local avg_time=$(echo "$ping_output" | grep "rtt min/avg/max/mdev" | awk -F'/' '{print $5}')
    local max_time=$(echo "$ping_output" | grep "rtt min/avg/max/mdev" | awk -F'/' '{print $6}')
    
    # Log detailed statistics
    log_message "DNS IP Ping Statistics:"
    log_message "  Target IP: $DNS_IP"
    log_message "  Packets transmitted: ${packets_transmitted:-N/A}"
    log_message "  Packets received: ${packets_received:-N/A}"
    log_message "  Packet loss: ${packet_loss:-N/A}"
    log_message "  Min/Avg/Max response time: ${min_time:-N/A}/${avg_time:-N/A}/${max_time:-N/A}ms"
    
    # Display results to user
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ DNS IP ping successful!${NC}"
        if [ -n "$packets_transmitted" ] && [ -n "$packets_received" ]; then
            echo -e "${YELLOW}Packets:${NC} $packets_received/$packets_transmitted received"
        fi
        if [ -n "$packet_loss" ]; then
            echo -e "${YELLOW}Packet Loss:${NC} $packet_loss"
        fi
        if [ -n "$min_time" ] && [ -n "$avg_time" ] && [ -n "$max_time" ]; then
            echo -e "${YELLOW}Response Time:${NC} min/avg/max = ${min_time}/${avg_time}/${max_time}ms"
        fi
    else
        echo -e "${RED}✗ DNS IP ping failed!${NC}"
        echo -e "${RED}Error Details:${NC}"
        echo "$ping_output" | grep -E "(unreachable|timeout|failed|error)" | head -3
    fi
    
    return $exit_code
}

# Function to determine DNS IP connectivity status
determine_dns_ip_status() {
    local exit_code="$1"
    local ping_output="$2"
    
    if [ $exit_code -eq 0 ]; then
        # Success case - DNS IP is reachable
        echo -e "\n${GREEN}DNS IP is reachable.${NC}"
        echo -e "${GREEN}Direct IP connectivity confirmed - network layer is functional.${NC}"
        log_message "SUCCESS: DNS IP connectivity confirmed - $DNS_IP is reachable"
        return 0
    else
        # Failure case - analyze the type of failure
        echo -e "\n${RED}DNS IP connectivity issue detected.${NC}"
        
        if echo "$ping_output" | grep -q "Network is unreachable"; then
            echo -e "${RED}Issue: Network is unreachable${NC}"
            echo -e "${YELLOW}This indicates a routing or network interface problem${NC}"
            log_message "FAILURE: Network is unreachable to $DNS_IP"
        elif echo "$ping_output" | grep -q "Destination Host Unreachable"; then
            echo -e "${RED}Issue: Destination host unreachable${NC}"
            echo -e "${YELLOW}This indicates a routing problem or the target is down${NC}"
            log_message "FAILURE: Destination host unreachable for $DNS_IP"
        elif echo "$ping_output" | grep -q "timeout"; then
            echo -e "${RED}Issue: Connection timeout${NC}"
            echo -e "${YELLOW}This may indicate firewall blocking or network congestion${NC}"
            log_message "FAILURE: Connection timeout to $DNS_IP"
        elif [ $exit_code -eq 2 ]; then
            echo -e "${RED}Issue: Invalid IP address format${NC}"
            log_message "FAILURE: Invalid IP address format"
        else
            echo -e "${RED}Issue: Unknown network problem${NC}"
            echo -e "${YELLOW}Check network configuration and connectivity${NC}"
            log_message "FAILURE: Unknown network problem (exit code: $exit_code)"
        fi
        
        return 1
    fi
}

# Function to perform additional DNS-related tests
perform_dns_tests() {
    local exit_code="$1"
    
    echo -e "\n${BLUE}=== Additional DNS Tests ===${NC}"
    
    # Test if we can resolve the DNS server's hostname
    echo -e "${YELLOW}Testing reverse DNS lookup for $DNS_IP:${NC}"
    local reverse_lookup=$(nslookup "$DNS_IP" 2>/dev/null | grep "name =" | awk '{print $4}' | sed 's/\.$//')
    if [ -n "$reverse_lookup" ]; then
        echo -e "${GREEN}✓ Reverse DNS: $reverse_lookup${NC}"
        log_message "Reverse DNS lookup successful: $DNS_IP -> $reverse_lookup"
    else
        echo -e "${YELLOW}⚠ Reverse DNS lookup failed or not available${NC}"
        log_message "Reverse DNS lookup failed for $DNS_IP"
    fi
    
    # Test DNS functionality if IP is reachable
    if [ $exit_code -eq 0 ]; then
        echo -e "\n${YELLOW}Testing DNS resolution using $DNS_IP:${NC}"
        local dns_test=$(nslookup google.com "$DNS_IP" 2>/dev/null | grep "Address:" | tail -1 | awk '{print $2}')
        if [ -n "$dns_test" ]; then
            echo -e "${GREEN}✓ DNS resolution working: google.com -> $dns_test${NC}"
            log_message "DNS resolution test successful using $DNS_IP: google.com -> $dns_test"
        else
            echo -e "${YELLOW}⚠ DNS resolution test failed${NC}"
            log_message "DNS resolution test failed using $DNS_IP"
        fi
    fi
}

# Function to display troubleshooting suggestions
display_troubleshooting() {
    local exit_code="$1"
    
    if [ $exit_code -ne 0 ]; then
        echo -e "\n${BLUE}=== Troubleshooting Suggestions ===${NC}"
        echo -e "${YELLOW}Since this is a direct IP test (no DNS involved):${NC}"
        echo -e "${YELLOW}1. Check network interface status: ip link show${NC}"
        echo -e "${YELLOW}2. Verify IP configuration: ip addr show${NC}"
        echo -e "${YELLOW}3. Check routing table: ip route show${NC}"
        echo -e "${YELLOW}4. Test local network first: ping gateway${NC}"
        echo -e "${YELLOW}5. Check firewall rules: iptables -L${NC}"
        echo -e "${YELLOW}6. Verify network cable/WiFi connection${NC}"
        echo -e "${YELLOW}7. Try alternative DNS IP: ping 8.8.4.4${NC}"
        echo -e "${YELLOW}8. Check if ICMP is blocked by ISP/firewall${NC}"
    else
        echo -e "\n${BLUE}=== Network Status ===${NC}"
        echo -e "${GREEN}✓ Direct IP connectivity is working${NC}"
        echo -e "${GREEN}✓ Network routing is functional${NC}"
        echo -e "${GREEN}✓ Can reach external DNS servers${NC}"
        echo -e "${YELLOW}If you have DNS resolution issues, the problem is likely:${NC}"
        echo -e "${YELLOW}  - DNS server configuration${NC}"
        echo -e "${YELLOW}  - /etc/resolv.conf settings${NC}"
        echo -e "${YELLOW}  - DNS service not running${NC}"
    fi
}

# Function to run network diagnostics
run_network_diagnostics() {
    local exit_code="$1"
    
    echo -e "\n${BLUE}=== Network Diagnostics ===${NC}"
    
    # Check network interfaces
    echo -e "${YELLOW}Active Network Interfaces:${NC}"
    ip link show | grep -E "^[0-9]+:" | grep "state UP" | head -3
    
    # Check IP addresses
    echo -e "\n${YELLOW}IP Addresses:${NC}"
    ip addr show | grep "inet " | grep -v "127.0.0.1" | head -3
    
    # Check default route
    echo -e "\n${YELLOW}Default Gateway:${NC}"
    ip route show default 2>/dev/null || echo "No default route found"
    
    # Check if we can reach the gateway
    local gateway=$(ip route show default 2>/dev/null | awk '{print $3}' | head -1)
    if [ -n "$gateway" ]; then
        echo -e "\n${YELLOW}Testing gateway connectivity ($gateway):${NC}"
        if timeout 5 ping -c 1 "$gateway" >/dev/null 2>&1; then
            echo -e "${GREEN}✓ Gateway is reachable${NC}"
            log_message "Gateway connectivity test successful: $gateway"
        else
            echo -e "${RED}✗ Gateway is not reachable${NC}"
            log_message "Gateway connectivity test failed: $gateway"
        fi
    fi
    
    # Log diagnostic information
    log_message "Network Diagnostic Information:"
    log_message "  Active interfaces: $(ip link show | grep -c "state UP")"
    log_message "  IP addresses: $(ip addr show | grep -c "inet ")"
    log_message "  Default gateway: ${gateway:-Not found}"
}

# Main function
main() {
    local start_time=$(date +%s)
    
    # Setup logging
    setup_logging
    
    # Display script information
    display_info
    
    # Perform DNS IP ping test
    local ping_output
    local ping_exit_code
    
    ping_output=$(timeout "$TIMEOUT" ping -c "$PING_COUNT" "$DNS_IP" 2>&1)
    ping_exit_code=$?
    
    # Analyze results
    analyze_ping_results "$ping_output" "$ping_exit_code"
    
    # Determine and display DNS IP connectivity status
    determine_dns_ip_status "$ping_exit_code" "$ping_output"
    local final_status=$?
    
    # Perform additional DNS tests
    perform_dns_tests "$ping_exit_code"
    
    # Run network diagnostics
    run_network_diagnostics "$ping_exit_code"
    
    # Display troubleshooting suggestions
    display_troubleshooting "$ping_exit_code"
    
    # Calculate and log execution time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo -e "\n${BLUE}=== Test Summary ===${NC}"
    echo -e "${YELLOW}Target DNS IP:${NC} $DNS_IP"
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
    echo -e "  --dns-ip <ip>      Specify DNS IP address (default: $DNS_IP)"
    echo -e "  --count <num>      Number of ping packets (default: $PING_COUNT)"
    echo -e "  --timeout <sec>    Timeout in seconds (default: $TIMEOUT)"
    echo -e "  --quiet            Suppress detailed output"
    echo -e "  --help             Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0                 Test connectivity to Google DNS (8.8.8.8)"
    echo -e "  $0 --dns-ip 8.8.4.4 --count 2"
    echo -e "  $0 --quiet         Run with minimal output"
}

# Handle command line arguments
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dns-ip)
            DNS_IP="$2"
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

# Validate arguments
if ! validate_ip "$DNS_IP"; then
    echo -e "${RED}Error: Invalid DNS IP address format: $DNS_IP${NC}"
    exit 1
fi

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