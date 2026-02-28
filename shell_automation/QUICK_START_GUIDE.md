# Quick Start Guide - Get Recording Ready in 5 Minutes

## 🚀 Immediate Solution: Replit (Recommended)

**Perfect for your D796 recording - Professional Linux environment in 2 minutes!**

### Step 1: Go to Replit
1. Open browser: https://replit.com
2. Sign up (free) or login
3. Click "Create Repl"
4. Select "Bash" template

### Step 2: Upload Your D796 Project
1. In Replit, click "Upload folder" or drag-and-drop
2. Select your entire D796 folder
3. Wait for upload (1-2 minutes)

### Step 3: Setup Environment
```bash
# In Replit terminal, run:
cd D796
find scripts/ -name "*.sh" -exec chmod +x {} \;
ls -la
```

### Step 4: Test Your Scripts
```bash
# Test master script
./run_assessment.sh

# Test individual scripts
cd scripts/user_management
cat create_user.sh | head -20
```

### Step 5: Start Recording!
- Full Linux terminal ready
- All your scripts working
- Professional environment
- Perfect for screen recording

## 🎬 Recording Commands Ready

**Copy these commands for your recording:**

```bash
# Initial setup
clear
pwd
ls -la

# Show project structure
tree . || find . -type d

# Run master demo
./run_assessment.sh

# Follow your DEMO_COMMANDS.txt for each part
```

## 🔄 Alternative: Continue WSL Setup

**If you prefer WSL, here's what to do:**

### Option A: Microsoft Store Method
1. Open Microsoft Store
2. Search "Ubuntu"
3. Install "Ubuntu"
4. Launch from Start Menu

### Option B: PowerShell Admin Method
```powershell
# Run as Administrator:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# Restart computer
# Then: wsl --install -d Ubuntu
```

## 🎯 Recommendation

**For immediate recording:** Use Replit now
**For long-term development:** Set up WSL later

Both give you professional Linux environments for your D796 assessment!

## ⏰ Time Comparison

| Method | Setup Time | Recording Ready |
|--------|------------|-----------------|
| Replit | 2-5 minutes | ✅ Immediately |
| WSL Store | 10-20 minutes | ✅ After setup |
| WSL PowerShell | 15-30 minutes | ✅ After restart |

**Choose based on your timeline!**