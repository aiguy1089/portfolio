# Configuration Guide
## D796 Assessment - Unix/Linux System Administration

### Overview
This guide provides step-by-step instructions for configuring and running all shell scripts created for the D796 assessment. Follow these instructions to properly set up your environment and execute the scripts.

---

## Initial Setup

### 1. Directory Structure Setup
```bash
# Navigate to the project directory
cd ~/D796

# Verify directory structure
ls -la
# Should show:
# scripts/
# documentation/
# bin/
# logs/
```

### 2. Make Scripts Executable
```bash
# Make all scripts executable
chmod +x scripts/*/*.sh
chmod +x scripts/environment_config/*.sh

# Verify permissions
find scripts/ -name "*.sh" -exec ls -l {} \;
```

### 3. Create Required Directories
```bash
# Create logs directory if it doesn't exist
mkdir -p logs

# Create archives directory for Part G
mkdir -p archives

# Create bin directory for PATH scripts
mkdir -p bin
```

---

## Part A & B: User Management Scripts

### Configuration Steps

1. **Copy scripts to bin directory:**
```bash
cp scripts/user_management/create_user.sh bin/
cp scripts/user_management/delete_user.sh bin/
chmod +x bin/*.sh
```

2. **Test the scripts:**
```bash
# Test create_user.sh
./scripts/user_management/create_user.sh --demo

# Test delete_user.sh  
./scripts/user_management/delete_user.sh --demo
```

### Usage Examples

**Creating a user:**
```bash
# Basic usage
sudo ./scripts/user_management/create_user.sh testuser

# The script will:
# - Check if dev_group exists (create if needed)
# - Create user with temporary password
# - Add user to dev_group
# - Force password change on first login
# - Display verification information
```

**Deleting a user:**
```bash
# Basic usage
sudo ./scripts/user_management/delete_user.sh testuser

# The script will:
# - Ask for confirmation
# - Delete user and home directory
# - Verify deletion
# - Display summary
```

---

## Part C: Environment Configuration

### Configuration Steps

1. **Run the bashrc update script:**
```bash
./scripts/environment_config/bashrc_updates.sh
```

2. **Reload your shell configuration:**
```bash
source ~/.bashrc
```

3. **Verify the configuration:**
```bash
# Test custom prompt (should show colors)
# Test aliases
ll
la
cls
desktop

# Test PATH
which create_user.sh
which delete_user.sh
```

### Custom Prompt Configuration
The script configures a colored prompt with the format:
```
user@hostname:/current/directory$ 
```
- Username: Cyan
- Hostname: Yellow  
- Directory: Blue
- $ symbol: Green

### Available Aliases
```bash
# File listing
ll          # ls -lrt (long listing, sorted by time)
la          # ls -a (list all files including hidden)
cls, c      # clear (clear screen)

# Navigation
desktop     # cd to Desktop directory
download    # cd to Downloads directory  
documents   # cd to Documents directory
home        # cd to home directory
root        # cd to root directory
back        # cd to previous directory
..          # cd to parent directory
...         # cd to parent's parent directory

# System information
df          # df -h (human readable disk usage)
du          # du -h (human readable directory usage)
free        # free -h (human readable memory usage)
```

---

## Part D: Package Management Scripts

### Configuration Steps

1. **Install vim (if not already installed):**
```bash
./scripts/package_management/install_vim.sh

# Check if vim is already installed
./scripts/package_management/install_vim.sh --check
```

2. **Update all packages:**
```bash
./scripts/package_management/update_packages.sh

# Check for available updates without installing
./scripts/package_management/update_packages.sh --check

# View package statistics
./scripts/package_management/update_packages.sh --stats
```

### Log File Locations
- Package updates: `~/D796/logs/update.log`
- Installation logs: Included in script output

---

## Part E: Network Monitoring Scripts

### Configuration Steps

1. **Test Google connectivity:**
```bash
./scripts/network_monitoring/check_google.sh

# With custom options
./scripts/network_monitoring/check_google.sh --target yahoo.com --count 2
```

2. **Test DNS IP connectivity:**
```bash
./scripts/network_monitoring/check_dns_ip.sh

# With custom DNS IP
./scripts/network_monitoring/check_dns_ip.sh --dns-ip 8.8.4.4
```

3. **Test DNS resolution:**
```bash
./scripts/network_monitoring/check_dns_resolve.sh

# With custom domain
./scripts/network_monitoring/check_dns_resolve.sh --domain google.com
```

### Expected Outputs

**Successful network test:**
```
Network is up.
```

**Successful DNS IP test:**
```
DNS IP is reachable.
Direct IP connectivity confirmed - network layer is functional.
```

**Successful DNS resolution:**
```
DNS resolution is working.
Successfully resolved example.com to IP address: 93.184.216.34
```

### Log File Location
All network tests log to: `~/D796/logs/network_check.log`

---

## Part F: Disk Management Script

### Configuration Steps

1. **Run disk cleanup (requires sudo):**
```bash
sudo ./scripts/disk_management/cleanup_disk.sh
```

2. **Dry run mode (preview only):**
```bash
./scripts/disk_management/cleanup_disk.sh --dry-run
```

3. **Force mode (skip confirmations):**
```bash
sudo ./scripts/disk_management/cleanup_disk.sh --force
```

### Directories Cleaned
- `/var/log` - System logs (with backup)
- `$HOME/.cache` - User cache files
- `/tmp` - Temporary files
- `/var/tmp` - System temporary files
- `/var/cache` - Package cache

### Expected Output
```
✓ Disk cleanup completed successfully!
Freed 4.0GB of disk space.
```

Or if no significant space was freed:
```
No significant disk space was freed
```

### Log and Backup Locations
- Log file: `~/D796/logs/disk_cleanup.log`
- Backups: `~/D796/logs/cleanup_backups/`

---

## Part G: File Archiving Script

### Configuration Steps

1. **Run archive and compression (requires sudo for /etc):**
```bash
sudo ./scripts/file_archiving/archive_compress.sh
```

2. **Test with smaller directory:**
```bash
./scripts/file_archiving/archive_compress.sh --test
```

3. **Custom source and output directories:**
```bash
sudo ./scripts/file_archiving/archive_compress.sh --source /var/log --output /tmp/archives
```

### Expected Output
The script will create two archives and compare their sizes:
```
=== Size Difference Analysis ===
Gzip archive size: 8.2MB
Bzip2 archive size: 7.1MB
Difference: Bzip2 is 1.1MB smaller (13.44% reduction)
✓ Bzip2 provides better compression
```

### Output Locations
- Archives: `~/D796/archives/`
- Log file: `~/D796/logs/archive_compress.log`

---

## Troubleshooting

### Common Issues and Solutions

**Permission Denied Errors:**
```bash
# Make sure scripts are executable
chmod +x scripts/*/*.sh

# Use sudo for system operations
sudo ./script_name.sh
```

**PATH Issues:**
```bash
# Reload bashrc after configuration
source ~/.bashrc

# Verify PATH includes bin directory
echo $PATH | grep D796/bin
```

**Missing Dependencies:**
```bash
# Install required tools
sudo apt-get update
sudo apt-get install bc tar gzip bzip2 nslookup
```

**Log File Permissions:**
```bash
# Create logs directory with proper permissions
mkdir -p ~/D796/logs
chmod 755 ~/D796/logs
```

### Verification Commands

**Check script functionality:**
```bash
# Test all scripts are executable
find ~/D796/scripts -name "*.sh" -executable

# Test PATH configuration
which create_user.sh delete_user.sh

# Test aliases
alias | grep -E "(ll|la|cls|desktop)"

# Check log files
ls -la ~/D796/logs/
```

**System requirements check:**
```bash
# Check required commands are available
command -v tar && echo "tar: OK"
command -v gzip && echo "gzip: OK"  
command -v bzip2 && echo "bzip2: OK"
command -v nslookup && echo "nslookup: OK"
command -v ping && echo "ping: OK"
command -v df && echo "df: OK"
```

---

## Security Considerations

### File Permissions
- Scripts should be executable by owner: `chmod 755`
- Log files should be readable by owner: `chmod 644`
- Backup directories should be protected: `chmod 700`

### Sudo Usage
- Scripts requiring system access use sudo appropriately
- User is prompted for password when needed
- Sudo access is tested before proceeding

### Data Protection
- Important files are backed up before deletion
- User confirmation required for destructive operations
- Detailed logging for audit trails

---

## Performance Optimization

### Script Execution Tips
- Run disk cleanup during low-usage periods
- Archive operations may take time for large directories
- Network tests are quick but may timeout on slow connections
- Package updates duration depends on number of packages

### Resource Usage
- Archive operations are CPU and I/O intensive
- Disk cleanup frees space but may temporarily use more during backup
- Network tests use minimal resources
- Package updates require network bandwidth

---

## Maintenance

### Regular Tasks
1. **Weekly:** Run package updates
2. **Monthly:** Run disk cleanup
3. **Quarterly:** Create system archives
4. **As needed:** User management operations

### Log Rotation
```bash
# Rotate logs manually if they get large
cd ~/D796/logs
for log in *.log; do
    if [ -f "$log" ]; then
        mv "$log" "${log}.$(date +%Y%m%d)"
        touch "$log"
    fi
done
```

### Backup Cleanup
```bash
# Clean old backups (older than 30 days)
find ~/D796/logs/cleanup_backups -type f -mtime +30 -delete
find ~/D796/archives -name "*.tar.*" -mtime +90 -delete
```

This configuration guide ensures all scripts are properly set up and ready for demonstration and evaluation.