#!/bin/bash

# check_dns_resolve.sh - Script to test DNS resolution for example.com using nslookup
# Part E.3 of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
TARGET_DOMAIN="example.com"
TIMEOUT=10
LOG_FILE="$HOME/D796/logs/network_check.log"

# Function to log messages with timestamp
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [DNS_RESOLVE] $message" >> "$LOG_FILE"
}

# Function to setup logging
setup_logging() {
    local log_dir=$(dirname "$LOG_FILE")
    if [ ! -d "$log_dir" ]; then
        mkdir -p "$log_dir"
    fi
    
    # Log script start
    log_message "Script started - testing DNS resolution for $TARGET_DOMAIN"
}

# Function to display script information
display_info() {
    echo -e "${BLUE}=== DNS Resolution Test ===${NC}"
    echo -e "${BLUE}D796 Assessment - Network Monitoring${NC}"
    echo -e "${BLUE}===================================${NC}\n"
    
    echo -e "${YELLOW}Target Domain:${NC} $TARGET_DOMAIN"
    echo -e "${YELLOW}Timeout:${NC} $TIMEOUT seconds"
    echo -e "${YELLOW}Timestamp:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}Log File:${NC} $LOG_FILE"
    echo -e "${YELLOW}Purpose:${NC} Test DNS resolution functionality"
    echo -e "${YELLOW}Method:${NC} nslookup command"
    echo ""
}

# Function to validate domain name format
validate_domain() {
    local domain="$1"
    local domain_regex="^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
    
    if [[ $domain =~ $domain_regex ]] && [ ${#domain} -le 253 ]; then
        return 0
    else
        return 1
    fi
}

# Function to perform DNS resolution test
perform_dns_resolution_test() {
    local domain="$1"
    local timeout="$2"
    
    echo -e "${BLUE}Testing DNS resolution for $domain...${NC}"
    log_message "Starting DNS resolution test for $domain (${timeout}s timeout)"
    
    # Validate domain format
    if ! validate_domain "$domain"; then
        echo -e "${RED}Error: Invalid domain name format: $domain${NC}"
        log_message "ERROR: Invalid domain name format: $domain"
        return 2
    fi
    
    # Execute nslookup command and capture output
    local nslookup_output
    local nslookup_exit_code
    
    # Use timeout command to limit nslookup duration
    nslookup_output=$(timeout "$timeout" nslookup "$domain" 2>&1)
    nslookup_exit_code=$?
    
    # Log the raw nslookup output
    log_message "nslookup command output:"
    echo "$nslookup_output" | while IFS= read -r line; do
        log_message "  $line"
    done
    log_message "nslookup exit code: $nslookup_exit_code"
    
    return $nslookup_exit_code
}

# Function to analyze DNS resolution results
analyze_dns_results() {
    local nslookup_output="$1"
    local exit_code="$2"
    local domain="$3"
    
    # Extract IP addresses from nslookup output
    local ip_addresses=$(echo "$nslookup_output" | grep -E "^Address: [0-9]" | awk '{print $2}' | tr '\n' ' ')
    local authoritative_server=$(echo "$nslookup_output" | grep "Server:" | awk '{print $2}')
    local server_port=$(echo "$nslookup_output" | grep "Server:" -A1 | grep "Address:" | awk '{print $2}')
    
    # Check for specific DNS errors
    local dns_error=""
    if echo "$nslookup_output" | grep -q "NXDOMAIN"; then
        dns_error="Domain does not exist (NXDOMAIN)"
    elif echo "$nslookup_output" | grep -q "SERVFAIL"; then
        dns_error="DNS server failure (SERVFAIL)"
    elif echo "$nslookup_output" | grep -q "connection timed out"; then
        dns_error="DNS query timeout"
    elif echo "$nslookup_output" | grep -q "No answer"; then
        dns_error="No DNS records found"
    fi
    
    # Log detailed DNS information
    log_message "DNS Resolution Analysis:"
    log_message "  Target domain: $domain"
    log_message "  DNS server used: ${authoritative_server:-N/A}"
    log_message "  Server address: ${server_port:-N/A}"
    log_message "  Resolved IP addresses: ${ip_addresses:-None}"
    log_message "  DNS error: ${dns_error:-None}"
    
    # Display results to user
    if [ $exit_code -eq 0 ] && [ -n "$ip_addresses" ]; then
        echo -e "${GREEN}✓ DNS resolution successful!${NC}"
        echo -e "${YELLOW}Domain:${NC} $domain"
        if [ -n "$authoritative_server" ]; then
            echo -e "${YELLOW}DNS Server:${NC} $authoritative_server"
        fi
        if [ -n "$server_port" ]; then
            echo -e "${YELLOW}Server Address:${NC} $server_port"
        fi
        echo -e "${YELLOW}Resolved IP Addresses:${NC}"
        for ip in $ip_addresses; do
            echo -e "  ${GREEN}→${NC} $ip"
        done
    else
        echo -e "${RED}✗ DNS resolution failed!${NC}"
        if [ -n "$dns_error" ]; then
            echo -e "${RED}Error:${NC} $dns_error"
        fi
        if [ -n "$authoritative_server" ]; then
            echo -e "${YELLOW}DNS Server Used:${NC} $authoritative_server"
        fi
    fi
    
    return $exit_code
}

# Function to determine DNS resolution status
determine_dns_status() {
    local exit_code="$1"
    local nslookup_output="$2"
    local domain="$3"
    
    if [ $exit_code -eq 0 ] && echo "$nslookup_output" | grep -q "Address: [0-9]"; then
        # Success case - DNS resolution working
        local resolved_ip=$(echo "$nslookup_output" | grep -E "^Address: [0-9]" | head -1 | awk '{print $2}')
        echo -e "\n${GREEN}DNS resolution is working.${NC}"
        echo -e "${GREEN}Successfully resolved $domain to IP address: $resolved_ip${NC}"
        log_message "SUCCESS: DNS resolution confirmed - $domain resolved to $resolved_ip"
        return 0
    else
        # Failure case - analyze the type of DNS failure
        echo -e "\n${RED}DNS resolution issue detected.${NC}"
        
        if echo "$nslookup_output" | grep -q "NXDOMAIN"; then
            echo -e "${RED}Issue: Domain name does not exist${NC}"
            echo -e "${YELLOW}The domain '$domain' is not registered or has no DNS records${NC}"
            log_message "FAILURE: Domain does not exist (NXDOMAIN) - $domain"
        elif echo "$nslookup_output" | grep -q "SERVFAIL"; then
            echo -e "${RED}Issue: DNS server failure${NC}"
            echo -e "${YELLOW}The DNS server encountered an error processing the request${NC}"
            log_message "FAILURE: DNS server failure (SERVFAIL) for $domain"
        elif echo "$nslookup_output" | grep -q "connection timed out"; then
            echo -e "${RED}Issue: DNS query timeout${NC}"
            echo -e "${YELLOW}Unable to reach DNS server or query took too long${NC}"
            log_message "FAILURE: DNS query timeout for $domain"
        elif echo "$nslookup_output" | grep -q "No answer"; then
            echo -e "${RED}Issue: No DNS records found${NC}"
            echo -e "${YELLOW}Domain exists but has no A records${NC}"
            log_message "FAILURE: No DNS records found for $domain"
        elif [ $exit_code -eq 124 ]; then
            echo -e "${RED}Issue: Command timeout${NC}"
            echo -e "${YELLOW}DNS resolution took longer than $TIMEOUT seconds${NC}"
            log_message "FAILURE: Command timeout for $domain"
        elif [ $exit_code -eq 2 ]; then
            echo -e "${RED}Issue: Invalid domain name format${NC}"
            log_message "FAILURE: Invalid domain name format"
        else
            echo -e "${RED}Issue: Unknown DNS resolution problem${NC}"
            echo -e "${YELLOW}Check DNS server configuration and network connectivity${NC}"
            log_message "FAILURE: Unknown DNS problem (exit code: $exit_code)"
        fi
        
        return 1
    fi
}

# Function to perform additional DNS tests
perform_additional_dns_tests() {
    local exit_code="$1"
    local domain="$2"
    
    echo -e "\n${BLUE}=== Additional DNS Tests ===${NC}"
    
    # Test different record types
    echo -e "${YELLOW}Testing different DNS record types for $domain:${NC}"
    
    # Test MX records
    local mx_records=$(timeout 5 nslookup -type=MX "$domain" 2>/dev/null | grep "mail exchanger" | head -2)
    if [ -n "$mx_records" ]; then
        echo -e "${GREEN}✓ MX Records found:${NC}"
        echo "$mx_records" | while IFS= read -r line; do
            echo -e "  ${YELLOW}→${NC} $line"
        done
        log_message "MX records found for $domain"
    else
        echo -e "${YELLOW}⚠ No MX records found${NC}"
        log_message "No MX records found for $domain"
    fi
    
    # Test NS records
    local ns_records=$(timeout 5 nslookup -type=NS "$domain" 2>/dev/null | grep "nameserver" | head -3)
    if [ -n "$ns_records" ]; then
        echo -e "${GREEN}✓ NS Records found:${NC}"
        echo "$ns_records" | while IFS= read -r line; do
            echo -e "  ${YELLOW}→${NC} $line"
        done
        log_message "NS records found for $domain"
    else
        echo -e "${YELLOW}⚠ No NS records found${NC}"
        log_message "No NS records found for $domain"
    fi
    
    # Test with different DNS servers if main resolution failed
    if [ $exit_code -ne 0 ]; then
        echo -e "\n${YELLOW}Testing with alternative DNS servers:${NC}"
        
        # Test with Google DNS
        local google_dns_result=$(timeout 5 nslookup "$domain" 8.8.8.8 2>/dev/null | grep -E "^Address: [0-9]" | head -1 | awk '{print $2}')
        if [ -n "$google_dns_result" ]; then
            echo -e "${GREEN}✓ Google DNS (8.8.8.8): $google_dns_result${NC}"
            log_message "Alternative DNS test successful using Google DNS: $domain -> $google_dns_result"
        else
            echo -e "${RED}✗ Google DNS (8.8.8.8): Failed${NC}"
            log_message "Alternative DNS test failed using Google DNS"
        fi
        
        # Test with Cloudflare DNS
        local cloudflare_dns_result=$(timeout 5 nslookup "$domain" 1.1.1.1 2>/dev/null | grep -E "^Address: [0-9]" | head -1 | awk '{print $2}')
        if [ -n "$cloudflare_dns_result" ]; then
            echo -e "${GREEN}✓ Cloudflare DNS (1.1.1.1): $cloudflare_dns_result${NC}"
            log_message "Alternative DNS test successful using Cloudflare DNS: $domain -> $cloudflare_dns_result"
        else
            echo -e "${RED}✗ Cloudflare DNS (1.1.1.1): Failed${NC}"
            log_message "Alternative DNS test failed using Cloudflare DNS"
        fi
    fi
}

# Function to check DNS configuration
check_dns_configuration() {
    echo -e "\n${BLUE}=== DNS Configuration Check ===${NC}"
    
    # Check /etc/resolv.conf
    if [ -f /etc/resolv.conf ]; then
        echo -e "${YELLOW}DNS Servers configured in /etc/resolv.conf:${NC}"
        local dns_servers=$(grep "^nameserver" /etc/resolv.conf | awk '{print $2}')
        if [ -n "$dns_servers" ]; then
            echo "$dns_servers" | while IFS= read -r server; do
                echo -e "  ${GREEN}→${NC} $server"
            done
            log_message "DNS servers configured: $(echo "$dns_servers" | tr '\n' ' ')"
        else
            echo -e "${RED}✗ No nameservers found in /etc/resolv.conf${NC}"
            log_message "No nameservers found in /etc/resolv.conf"
        fi
        
        # Check search domains
        local search_domains=$(grep "^search" /etc/resolv.conf | cut -d' ' -f2-)
        if [ -n "$search_domains" ]; then
            echo -e "${YELLOW}Search domains:${NC} $search_domains"
            log_message "Search domains configured: $search_domains"
        fi
    else
        echo -e "${RED}✗ /etc/resolv.conf not found${NC}"
        log_message "/etc/resolv.conf not found"
    fi
    
    # Check if systemd-resolved is running
    if command -v systemctl >/dev/null 2>&1; then
        if systemctl is-active systemd-resolved >/dev/null 2>&1; then
            echo -e "${GREEN}✓ systemd-resolved is running${NC}"
            log_message "systemd-resolved service is active"
        else
            echo -e "${YELLOW}⚠ systemd-resolved is not running${NC}"
            log_message "systemd-resolved service is not active"
        fi
    fi
}

# Function to display troubleshooting suggestions
display_troubleshooting() {
    local exit_code="$1"
    
    if [ $exit_code -ne 0 ]; then
        echo -e "\n${BLUE}=== Troubleshooting Suggestions ===${NC}"
        echo -e "${YELLOW}DNS Resolution Issues:${NC}"
        echo -e "${YELLOW}1. Check DNS server configuration: cat /etc/resolv.conf${NC}"
        echo -e "${YELLOW}2. Test with specific DNS server: nslookup $TARGET_DOMAIN 8.8.8.8${NC}"
        echo -e "${YELLOW}3. Flush DNS cache: sudo systemctl restart systemd-resolved${NC}"
        echo -e "${YELLOW}4. Check network connectivity: ping 8.8.8.8${NC}"
        echo -e "${YELLOW}5. Verify firewall allows DNS (port 53): iptables -L${NC}"
        echo -e "${YELLOW}6. Test with dig command: dig $TARGET_DOMAIN${NC}"
        echo -e "${YELLOW}7. Check /etc/hosts file for conflicts${NC}"
        echo -e "${YELLOW}8. Restart network service: sudo systemctl restart networking${NC}"
    else
        echo -e "\n${BLUE}=== DNS Status ===${NC}"
        echo -e "${GREEN}✓ DNS resolution is working correctly${NC}"
        echo -e "${GREEN}✓ Can resolve domain names to IP addresses${NC}"
        echo -e "${GREEN}✓ DNS servers are responding${NC}"
        echo -e "${YELLOW}Your DNS configuration appears to be healthy${NC}"
    fi
}

# Main function
main() {
    local start_time=$(date +%s)
    
    # Setup logging
    setup_logging
    
    # Display script information
    display_info
    
    # Perform DNS resolution test
    local nslookup_output
    local nslookup_exit_code
    
    nslookup_output=$(timeout "$TIMEOUT" nslookup "$TARGET_DOMAIN" 2>&1)
    nslookup_exit_code=$?
    
    # Analyze results
    analyze_dns_results "$nslookup_output" "$nslookup_exit_code" "$TARGET_DOMAIN"
    
    # Determine and display DNS resolution status
    determine_dns_status "$nslookup_exit_code" "$nslookup_output" "$TARGET_DOMAIN"
    local final_status=$?
    
    # Perform additional DNS tests
    perform_additional_dns_tests "$nslookup_exit_code" "$TARGET_DOMAIN"
    
    # Check DNS configuration
    check_dns_configuration
    
    # Display troubleshooting suggestions
    display_troubleshooting "$nslookup_exit_code"
    
    # Calculate and log execution time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo -e "\n${BLUE}=== Test Summary ===${NC}"
    echo -e "${YELLOW}Target Domain:${NC} $TARGET_DOMAIN"
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
    echo -e "  --domain <domain>  Specify target domain (default: $TARGET_DOMAIN)"
    echo -e "  --timeout <sec>    Timeout in seconds (default: $TIMEOUT)"
    echo -e "  --quiet            Suppress detailed output"
    echo -e "  --help             Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0                 Test DNS resolution for example.com"
    echo -e "  $0 --domain google.com --timeout 15"
    echo -e "  $0 --quiet         Run with minimal output"
}

# Handle command line arguments
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            TARGET_DOMAIN="$2"
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
if ! validate_domain "$TARGET_DOMAIN"; then
    echo -e "${RED}Error: Invalid domain name format: $TARGET_DOMAIN${NC}"
    exit 1
fi

if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]] || [ "$TIMEOUT" -lt 1 ]; then
    echo -e "${RED}Error: Timeout must be a positive integer${NC}"
    exit 1
fi

# Execute main function
main