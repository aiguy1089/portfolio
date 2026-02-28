# Network Monitoring Scripts Flowchart
## Part E of D796 Assessment - Unix/Linux System Administration

### Overview
This document provides a flowchart diagram illustrating the planned code for the three network monitoring scripts that check network connections.

### Flowchart Diagram

```
                    START
                      |
                      v
              ┌─────────────────┐
              │  Initialize     │
              │  Script         │
              │  Variables      │
              └─────────────────┘
                      |
                      v
              ┌─────────────────┐
              │  Display        │
              │  Script Info    │
              │  & Purpose      │
              └─────────────────┘
                      |
                      v
              ┌─────────────────┐
              │  Check Network  │
              │  Target         │
              │  (google.com,   │
              │   8.8.8.8, or   │
              │   example.com)  │
              └─────────────────┘
                      |
                      v
              ┌─────────────────┐
              │  Execute        │
              │  Network        │
              │  Command        │
              │  (ping/nslookup)│
              └─────────────────┘
                      |
                      v
              ┌─────────────────┐
              │  Capture        │
              │  Command        │
              │  Output &       │
              │  Exit Code      │
              └─────────────────┘
                      |
                      v
              ┌─────────────────┐
              │  Analyze        │
              │  Results        │
              └─────────────────┘
                      |
                      v
                 ┌─────────┐
                 │ Success?│
                 └─────────┘
                   /       \
                  /         \
                YES         NO
                /             \
               v               v
    ┌─────────────────┐  ┌─────────────────┐
    │  Display        │  │  Display        │
    │  Success        │  │  Failure        │
    │  Message        │  │  Message        │
    │  "Network is    │  │  "Network       │
    │   up" or        │  │   issue         │
    │   equivalent    │  │   detected"     │
    └─────────────────┘  └─────────────────┘
              |                    |
              v                    v
    ┌─────────────────┐  ┌─────────────────┐
    │  Log Success    │  │  Log Failure    │
    │  Details        │  │  Details        │
    │  (timestamp,    │  │  (timestamp,    │
    │   response      │  │   error info)   │
    │   time, etc.)   │  │                 │
    └─────────────────┘  └─────────────────┘
              |                    |
              v                    v
    ┌─────────────────┐  ┌─────────────────┐
    │  Exit with      │  │  Exit with      │
    │  Status 0       │  │  Status 1       │
    │  (Success)      │  │  (Failure)      │
    └─────────────────┘  └─────────────────┘
              |                    |
              v                    v
                    END
```

### Script-Specific Logic

#### Script 1: check_google.sh (Ping google.com)
```
START → Initialize → Display Info → Execute: ping -c 4 google.com
  ↓
Check ping exit code (0 = success, non-zero = failure)
  ↓
If success: Display "Network is up" → Log success → Exit 0
If failure: Display error message → Log failure → Exit 1
```

#### Script 2: check_dns_ip.sh (Ping Google DNS 8.8.8.8)
```
START → Initialize → Display Info → Execute: ping -c 4 8.8.8.8
  ↓
Check ping exit code (0 = success, non-zero = failure)
  ↓
If success: Display "DNS IP reachable" → Log success → Exit 0
If failure: Display error message → Log failure → Exit 1
```

#### Script 3: check_dns_resolve.sh (DNS Resolution for example.com)
```
START → Initialize → Display Info → Execute: nslookup example.com
  ↓
Check nslookup exit code and parse output
  ↓
If DNS resolution successful: Display IP address → Log success → Exit 0
If DNS resolution failed: Display error message → Log failure → Exit 1
```

### Detailed Process Flow

#### 1. Initialization Phase
- Set color variables for output formatting
- Define log file location
- Set network targets (google.com, 8.8.8.8, example.com)
- Initialize timestamp variables

#### 2. Information Display Phase
- Show script name and purpose
- Display target being tested
- Show current timestamp
- Log script execution start

#### 3. Network Test Execution Phase
- Execute appropriate network command:
  - **Ping Tests**: `ping -c 4 <target>`
  - **DNS Test**: `nslookup <domain>`
- Capture command output
- Record command exit status
- Measure response time

#### 4. Result Analysis Phase
- Check command exit status
- Parse command output for relevant information
- Determine success/failure based on:
  - Exit code (0 = success)
  - Output content analysis
  - Response time thresholds

#### 5. Output and Logging Phase
- Display appropriate message to user
- Log detailed results to file
- Include timestamp, target, result, and diagnostic info
- Set appropriate exit code for script

#### 6. Error Handling
- Network unreachable
- DNS resolution failures
- Timeout conditions
- Invalid responses
- System command failures

### Success Criteria

#### Script 1 (Google Ping)
- **Success**: Ping receives responses from google.com
- **Output**: "Network is up"
- **Log**: Response time, packet loss, timestamp

#### Script 2 (DNS IP Ping)
- **Success**: Ping receives responses from 8.8.8.8
- **Output**: "DNS IP reachable" or similar
- **Log**: Response time, packet loss, timestamp

#### Script 3 (DNS Resolution)
- **Success**: nslookup successfully resolves example.com to IP
- **Output**: Display resolved IP address
- **Log**: Resolved IP, response time, timestamp

### Error Conditions and Responses

| Condition | Detection | Response |
|-----------|-----------|----------|
| Network Down | Ping fails with "Network unreachable" | Display network error message |
| DNS Server Down | nslookup fails or times out | Display DNS error message |
| Target Unreachable | Ping times out | Display timeout message |
| Invalid Domain | nslookup returns NXDOMAIN | Display domain not found message |
| Permission Issues | Command fails with permission error | Display permission error |

### Integration Points
- All scripts use common logging format
- Consistent error handling approach
- Standardized output formatting
- Common configuration variables

### Testing Scenarios
1. **Normal Operation**: All network services working
2. **Network Disconnected**: No internet connectivity
3. **DNS Issues**: Network up but DNS not working
4. **Partial Connectivity**: Some services reachable, others not
5. **Timeout Conditions**: Slow network responses

This flowchart provides the logical foundation for implementing the three network monitoring scripts with consistent behavior and comprehensive error handling.