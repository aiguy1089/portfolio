# D796 Assessment - Complete Video Script & Talking Points

## 🎬 Video Overview
**Total Time:** 35-40 minutes  
**Format:** Screen recording with narration  
**Audience:** WGU instructors evaluating D796 assessment  

---

## 📋 Pre-Recording Checklist
- [ ] Ubuntu WSL terminal open and sized properly
- [ ] Font size 14pt+ for visibility
- [ ] DEMO_COMMANDS.txt open for reference
- [ ] Screen recording software ready
- [ ] Audio levels tested
- [ ] Navigate to: `cd /mnt/c/Users/Admin/D796`

---

## 🎯 INTRODUCTION (3-4 minutes)

### Opening Statement:
> "Hello, my name is [Your Name], and welcome to my D796 assessment demonstration. Today I'll be showcasing my Unix/Linux system administration shell scripts that automate common administrative tasks. This project demonstrates my understanding of shell scripting, system administration, and Linux command-line operations."

### Commands to Run:
```bash
clear
pwd
whoami
date
```

### Talking Points:
> "I'm currently working in my D796 project directory on Ubuntu WSL. Let me show you the complete project structure I've created."

```bash
ls -la
```

> "As you can see, I have organized my project with scripts for each assessment requirement, documentation, logs, and archives directories. Let me show you the overall structure."

```bash
tree . || find . -type d
```

### Project Overview:
> "This project contains seven main components corresponding to parts A through G of the assessment:
> - User management scripts for creating and deleting users
> - Environment configuration with custom prompts and aliases  
> - Package management for vim installation and system updates
> - Network monitoring scripts with connectivity testing
> - Disk management with cleanup functions
> - File archiving with compression comparisons
> - Complete documentation and testing results"

```bash
find scripts/ -name "*.sh" -type f
```

> "All scripts are executable and include proper error handling, logging, and user validation. Now let me demonstrate each component."

---

## 🔧 PART A: USER CREATION SCRIPT (6-7 minutes)

### Navigation & Setup:
```bash
cd scripts/user_management
ls -la
```

### Talking Points:
> "Part A requires a user creation script that takes a username argument, creates a dev_group if it doesn't exist, adds the user with a password, and displays /etc/passwd for verification."

### Show Script Content:
```bash
cat create_user.sh | head -30
```

> "Let me walk you through the key components of this script. As you can see, it includes:
> - Input validation to ensure a username is provided
> - Error handling for various failure scenarios
> - Group creation logic for the dev_group
> - User creation with proper home directory setup
> - Password assignment functionality
> - Verification steps showing the user in /etc/passwd"

### Demonstrate Demo Mode:
```bash
sudo ./create_user.sh --demo
```

> "First, let me show you the demo mode which demonstrates the script logic without making actual system changes. This shows the validation, group checking, and user creation process."

### Execute Actual Script:
```bash
sudo ./create_user.sh testuser
```

> "Now I'll create an actual test user to demonstrate the script functionality."

### Verification:
```bash
grep testuser /etc/passwd
id testuser
groups testuser
```

> "As you can see, the user 'testuser' has been successfully created, assigned to the dev_group, and appears in the system password file. This meets all requirements for Part A."

---

## 🗑️ PART B: USER DELETION SCRIPT (5-6 minutes)

### Show Script Content:
```bash
cat delete_user.sh | head -30
```

### Talking Points:
> "Part B requires a user deletion script that takes a username argument, asks for confirmation, deletes the user and home directories, and shows verification. My script includes:
> - Username validation and existence checking
> - Interactive confirmation prompts for safety
> - Complete user and home directory removal
> - Verification that the user has been deleted"

### Demonstrate Demo Mode:
```bash
sudo ./delete_user.sh --demo
```

> "The demo mode shows the confirmation process and deletion logic without actually removing users."

### Execute Actual Deletion:
```bash
sudo ./delete_user.sh testuser
```

> "Now I'll delete the test user I just created. Notice the confirmation prompt for safety."

### Verification:
```bash
grep testuser /etc/passwd || echo "User successfully deleted"
ls /home/ | grep testuser || echo "Home directory removed"
```

> "Perfect! The user has been completely removed from the system, including the home directory. This satisfies all Part B requirements."

---

## ⚙️ PART C: ENVIRONMENT CONFIGURATION (6-7 minutes)

### Navigation:
```bash
cd ../environment_config
ls -la
```

### Talking Points:
> "Part C requires shell environment configuration including a custom prompt with colors and escape sequences, aliases for common commands, and updating ~/.bashrc to include the bin directory in PATH."

### Show Aliases File:
```bash
cat aliases.sh
```

> "Here are my custom aliases including:
> - 'll' for detailed file listings
> - 'la' for showing all files including hidden ones
> - 'cls' for clearing the screen
> - Navigation shortcuts like 'desktop' and 'docs'"

### Show Bashrc Updates Script:
```bash
cat bashrc_updates.sh | head -40
```

> "This script updates the .bashrc file with:
> - A colorized custom prompt showing username, hostname, and current directory
> - PATH updates to include our bin directory
> - Source commands for our aliases
> - Proper backup of the original .bashrc file"

### Execute Configuration:
```bash
./bashrc_updates.sh
```

> "Now I'll execute the configuration script to update my environment."

### Test Results:
```bash
source ~/.bashrc
ll
la
cls
```

> "Excellent! The aliases are working correctly, and you can see the custom prompt with colors. The PATH has been updated to include our scripts directory."

---

## 📦 PART D: PACKAGE MANAGEMENT (6-7 minutes)

### Navigation:
```bash
cd ../package_management
ls -la
```

### Talking Points:
> "Part D requires package management scripts including vim installation with existing package checking, and system updates with logging."

### Show Vim Installation Script:
```bash
cat install_vim.sh | head -40
```

> "This script includes:
> - Package existence checking before installation
> - Proper error handling for installation failures
> - User feedback throughout the process
> - Verification that vim was successfully installed"

### Check Vim Installation:
```bash
./install_vim.sh --check
```

> "The check mode shows whether vim is already installed and what actions would be taken."

### Show Update Script:
```bash
cat update_packages.sh | head -40
```

> "The system update script includes:
> - Package list updates
> - System upgrade functionality
> - Comprehensive logging to update.log
> - Statistics reporting on available updates"

### Execute Update Check:
```bash
./update_packages.sh --stats
```

> "This shows system update statistics and logs the information appropriately."

### Show Log File:
```bash
cat ../../logs/update.log | tail -20
```

> "As you can see, all package management activities are properly logged with timestamps."

---

## 🌐 PART E: NETWORK MONITORING (8-9 minutes)

### Navigation:
```bash
cd ../network_monitoring
ls -la
```

### Talking Points:
> "Part E requires network monitoring scripts with a flowchart diagram, including tests for Google connectivity, DNS IP connectivity, and DNS resolution functionality."

### Show Flowchart:
```bash
cat ../../documentation/flowchart_network.md | head -50
```

> "First, let me show you the flowchart I created that diagrams the planned network monitoring logic. This shows the decision flow for connectivity testing, error handling, and logging procedures."

### Show Google Connectivity Script:
```bash
cat check_google.sh | head -30
```

> "This script tests connectivity to google.com using ping commands with proper timeout handling and result logging."

### Execute Google Test:
```bash
./check_google.sh
```

> "As you can see, the connectivity test completed successfully with appropriate logging."

### Show DNS IP Script:
```bash
cat check_dns_ip.sh | head -30
```

> "This script tests connectivity to Google's DNS server at 8.8.8.8 to verify basic IP connectivity."

### Execute DNS IP Test:
```bash
./check_dns_ip.sh
```

### Show DNS Resolution Script:
```bash
cat check_dns_resolve.sh | head -30
```

> "This script tests DNS resolution functionality by resolving example.com to verify that DNS services are working properly."

### Execute DNS Resolution Test:
```bash
./check_dns_resolve.sh
```

### Show Network Logs:
```bash
cat ../../logs/network_check.log | tail -30
```

> "All network monitoring activities are logged with timestamps, results, and any error conditions. This provides a complete audit trail of network connectivity status."

---

## 💾 PART F: DISK MANAGEMENT (6-7 minutes)

### Navigation:
```bash
cd ../disk_management
ls -la
```

### Talking Points:
> "Part F requires disk space management including free disk space assessment using df command, a cleanDir() function for directory cleanup, variables with directories to clean, for loop implementation, and before/after disk space reporting."

### Show Script Content:
```bash
cat cleanup_disk.sh | head -50
```

> "This comprehensive disk cleanup script includes all required components. Let me highlight the key functions."

### Show cleanDir Function:
```bash
grep -A 25 "cleanDir()" cleanup_disk.sh
```

> "Here's the cleanDir() function that:
> - Takes a directory path as parameter
> - Checks if the directory exists and is accessible
> - Performs cleanup operations safely
> - Reports on space freed
> - Includes proper error handling"

### Show Directory Variables:
```bash
grep -A 10 "CLEANUP_DIRS=" cleanup_disk.sh
```

> "The script uses variables to define which directories to clean, making it easily configurable."

### Show For Loop Implementation:
```bash
grep -A 15 "for dir in" cleanup_disk.sh
```

> "The for loop iterates through each directory in the cleanup list and calls the cleanDir() function for each one."

### Execute Dry Run:
```bash
./cleanup_disk.sh --dry-run
```

> "I'm running this in dry-run mode for safety, which shows what would be cleaned without actually removing files. You can see the before and after disk space reporting using the df command."

### Show Disk Usage:
```bash
df -h
```

> "This shows current disk usage across all mounted filesystems, which the script uses for before/after comparisons."

---

## 📁 PART G: FILE ARCHIVING (7-8 minutes)

### Navigation:
```bash
cd ../file_archiving
ls -la
```

### Talking Points:
> "Part G requires file archiving and compression including a fileSize() function, tar + gzip compression, tar + bzip2 compression, and size comparison between compression algorithms."

### Show Script Content:
```bash
cat archive_compress.sh | head -50
```

> "This script implements all required archiving functionality with proper error handling and logging."

### Show fileSize Function:
```bash
grep -A 20 "fileSize()" archive_compress.sh
```

> "The fileSize() function:
> - Takes a file or directory path as parameter
> - Calculates total size including subdirectories
> - Returns size in human-readable format
> - Handles errors for non-existent paths"

### Show Compression Logic:
```bash
grep -A 30 "# Create gzip archive" archive_compress.sh
```

> "The script creates both gzip and bzip2 compressed archives of the /etc directory, then compares their sizes to demonstrate compression efficiency differences."

### Execute Test Mode:
```bash
./archive_compress.sh --test
```

> "I'm running this in test mode which uses a smaller directory for demonstration purposes while showing the complete functionality."

### Show Archive Results:
```bash
ls -la ../../archives/
```

> "Here you can see the created archives with their different sizes."

### Show Compression Comparison:
```bash
cat ../../logs/archive_compress.log | tail -20
```

> "The log file shows the detailed comparison between gzip and bzip2 compression, including original size, compressed sizes, and compression ratios."

---

## 🎯 MASTER DEMONSTRATION (4-5 minutes)

### Return to Main Directory:
```bash
cd ../..
pwd
```

### Show Complete Project:
```bash
find . -name "*.sh" -type f | wc -l
echo "Total shell scripts created:"
find . -name "*.sh" -type f
```

> "I've created a total of [X] shell scripts covering all assessment requirements."

### Show Documentation:
```bash
ls documentation/
cat documentation/testing_results.md | head -30
```

> "Complete documentation includes testing results, configuration guides, and the network monitoring flowchart."

### Run Master Script:
```bash
./run_assessment.sh
```

> "Finally, let me show you the master demonstration script that provides an interactive menu for testing all components."

### Navigate Menu:
> "This menu allows you to:
> - Set up the environment
> - Test each individual component
> - Run complete demonstrations
> - View documentation and logs"

---

## 🏁 CONCLUSION (3-4 minutes)

### Final Project Overview:
```bash
echo "=== D796 Assessment Complete ==="
date
whoami
pwd
```

### Summary Statement:
> "This completes my D796 assessment demonstration. I have successfully created and demonstrated:

> **Part A:** User creation script with dev_group functionality and /etc/passwd verification
> **Part B:** User deletion script with confirmation prompts and complete removal
> **Part C:** Shell environment configuration with custom prompts, aliases, and PATH updates
> **Part D:** Package management scripts for vim installation and system updates with logging
> **Part E:** Network monitoring scripts with flowchart documentation and comprehensive connectivity testing
> **Part F:** Disk management script with cleanDir() function, directory variables, and for loop implementation
> **Part G:** File archiving script with fileSize() function and compression algorithm comparison

> All scripts include proper error handling, user input validation, comprehensive logging, and meet the specified assessment requirements. The project demonstrates professional-level shell scripting skills and understanding of Unix/Linux system administration concepts."

### Technical Highlights:
> "Key technical achievements include:
> - Robust error handling and input validation across all scripts
> - Comprehensive logging with timestamps and audit trails
> - Safe execution modes for testing and demonstration
> - Professional code organization and documentation
> - Complete test coverage with verification steps
> - Security considerations with confirmation prompts and dry-run modes"

### Final Verification:
```bash
echo "All assessment requirements successfully completed"
ls -la logs/
ls -la archives/
echo "Thank you for reviewing my D796 assessment demonstration"
```

---

## 🎤 Speaking Tips During Recording

### Pace and Clarity:
- Speak clearly and at moderate pace
- Pause between major sections
- Explain what you're doing before executing commands
- Allow time for command output to be visible

### Technical Explanations:
- Highlight key functions and logic
- Explain error handling approaches
- Discuss security considerations
- Show verification steps clearly

### Professional Presentation:
- Maintain confident, professional tone
- Use technical terminology appropriately
- Explain complex concepts clearly
- Show enthusiasm for the technical work

### Time Management:
- Keep introduction concise but comprehensive
- Allow adequate time for each part demonstration
- Don't rush through code explanations
- Save time for proper conclusion

---

## ⏰ Time Allocation Summary

| Section | Time | Key Focus |
|---------|------|-----------|
| Introduction | 3-4 min | Project overview, structure |
| Part A (User Creation) | 6-7 min | Script demo, execution, verification |
| Part B (User Deletion) | 5-6 min | Safety features, confirmation |
| Part C (Environment) | 6-7 min | Aliases, prompts, PATH |
| Part D (Packages) | 6-7 min | Installation, updates, logging |
| Part E (Network) | 8-9 min | Flowchart, connectivity tests |
| Part F (Disk) | 6-7 min | cleanDir function, for loops |
| Part G (Archiving) | 7-8 min | fileSize function, compression |
| Master Demo | 4-5 min | Interactive menu, integration |
| Conclusion | 3-4 min | Summary, achievements |
| **Total** | **35-40 min** | **Complete demonstration** |

---

## 🚀 Ready to Record!

You now have a complete script with talking points, command sequences, and timing guidance. Follow this guide while referring to your DEMO_COMMANDS.txt for the exact commands to execute.

**Good luck with your recording!** 🎬