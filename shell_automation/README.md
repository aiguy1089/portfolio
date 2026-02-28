## Unix/Linux Shell Automation Scripts

This repository contains a suite of Bash scripts automating common system administration tasks: user management, environment configuration, package handling, network monitoring, disk cleanup, and file archiving.

### Directory Structure
```
D796/
├── README.md                    # This file - project overview and instructions
├── scripts/                     # Main scripts directory
│   ├── user_management/         # User creation and deletion scripts
│   │   ├── create_user.sh      # Script to create new users
│   │   └── delete_user.sh      # Script to delete users
│   ├── environment_config/      # Environment configuration files
│   │   ├── aliases.sh          # Custom aliases
│   │   └── bashrc_updates.sh   # Script to update .bashrc
│   ├── package_management/      # Package installation and update scripts
│   │   ├── install_vim.sh      # Install vim package
│   │   └── update_packages.sh  # Update all packages
│   ├── network_monitoring/      # Network connectivity scripts
│   │   ├── check_google.sh     # Ping google.com
│   │   ├── check_dns_ip.sh     # Ping Google DNS (8.8.8.8)
│   │   └── check_dns_resolve.sh # Test DNS resolution for example.com
│   ├── disk_management/         # Disk space management
│   │   └── cleanup_disk.sh     # Assess and clean up disk space
│   └── file_archiving/          # File compression and archiving
│       └── archive_compress.sh # Archive and compress files
├── documentation/               # Supporting documentation
│   ├── flowchart_network.md    # Network monitoring flowchart
│   ├── testing_results.md      # Test execution results
│   └── configuration_guide.md  # Environment configuration guide
├── bin/                        # Executable scripts directory (for PATH)
└── logs/                       # Log files directory
    └── update.log              # Package update log
```

### Usage

1. **Setup Environment:**
   ```bash
   chmod +x scripts/*/*.sh
   cp scripts/user_management/*.sh bin/
   ```

2. **Update PATH (add to ~/.bashrc):**
   ```bash
   export PATH="$PATH:$HOME/D796/bin"
   ```

3. **Execute Scripts:**
   ```bash
   # User management
   create_user.sh testuser
   delete_user.sh testuser
   
   # Package management
   ./scripts/package_management/install_vim.sh
   ./scripts/package_management/update_packages.sh
   
   # Network monitoring
   ./scripts/network_monitoring/check_google.sh
   ./scripts/network_monitoring/check_dns_ip.sh
   ./scripts/network_monitoring/check_dns_resolve.sh
   
   # Disk management
   sudo ./scripts/disk_management/cleanup_disk.sh
   
   # File archiving
   sudo ./scripts/file_archiving/archive_compress.sh
   ```

### Testing and Verification
Each script includes built-in testing scenarios and error handling. Refer to `documentation/testing_results.md` for detailed test execution results.

<!-- This README has been cleaned of academic-specific details for public presentation. -->