# D796 Final Submission Checklist
## Creating Shell Scripts in a Unix Environment - Complete Requirements

---

## 🎯 **SUBMISSION OVERVIEW**

### **What You Need to Submit:**
1. **📹 Panopto Video Recording** (Requirement H)
2. **💻 All Shell Scripts** (Requirements A-G)
3. **📄 Supporting Documentation** (Professional presentation)
4. **🔗 Panopto URL** (In Links section)
5. **📎 All Files** (In Attachments section)

---

## ✅ **REQUIREMENT CHECKLIST**

### **A. User Creation Script (create_user.sh)** ✅
- [x] Takes username argument with validation
- [x] Creates "dev_group" if it doesn't exist
- [x] Adds user and assigns password
- [x] Displays /etc/passwd for verification
- [x] **Executable demonstrations:**
  - [x] Run without arguments (error handling)
  - [x] Run with valid arguments (successful creation)
  - [x] Switch to new user and force password change

### **B. User Deletion Script (delete_user.sh)** ✅
- [x] Takes username argument with validation
- [x] Asks for confirmation before deletion
- [x] Deletes user and home directories
- [x] Displays /etc/passwd for verification
- [x] **Executable demonstrations:**
  - [x] Run without arguments (error handling)
  - [x] Run with valid arguments (successful deletion)
  - [x] Attempt to switch to deleted user (confirmation)

### **C. Shell Environment Configuration** ✅
- [x] **Prompt customization:**
  - [x] Changed prompt to $ symbol
  - [x] Used escape sequences for colors
  - [x] Different colors for shell text elements
- [x] **Aliases file created with shortcuts:**
  - [x] ls lrt, ls -a, clear
  - [x] Navigation aliases (desktop, download, documents)
- [x] **PATH configuration:**
  - [x] Created bin/ directory in root
  - [x] Moved create_user.sh and delete_user.sh to bin/
  - [x] Updated ~/.bashrc with bin directory in PATH
  - [x] Demonstrated execution from other directories

### **D. Package Management** ✅
- [x] **Vim installation script:**
  - [x] Checks if vim already installed
  - [x] Prints "Vim is already installed" if present
  - [x] Installs vim if not present
- [x] **System update script:**
  - [x] Updates all packages using package manager
  - [x] Saves output to update.log file

### **E. Network Monitoring Scripts** ✅
- [x] **Flowchart diagram** created and documented
- [x] **Script 1 - Google connectivity:**
  - [x] Pings google.com
  - [x] Prints "Network is up" on success
- [x] **Script 2 - DNS IP connectivity:**
  - [x] Pings Google DNS (8.8.8.8)
  - [x] Tests direct IP connectivity
- [x] **Script 3 - DNS resolution:**
  - [x] Uses nslookup for example.com
  - [x] Tests DNS resolution functionality

### **F. Disk Management Script** ✅
- [x] **Free disk space assessment:**
  - [x] Uses df command for root partition
  - [x] Stores result in variable
- [x] **cleanDir() function:**
  - [x] Deletes contents of given directory
  - [x] Takes directory as first argument
- [x] **Directory cleanup:**
  - [x] Variable with directories list (/var/log, $HOME/.cache)
  - [x] For loop implementation with cleanDir() function
- [x] **Before/after reporting:**
  - [x] Reports disk space freed
  - [x] "No significant disk space was freed" if zero

### **G. File Archiving Script** ✅
- [x] **fileSize() function:**
  - [x] Calculates size of given file argument
  - [x] Returns file size information
- [x] **Archive operations:**
  - [x] tar + gzip compression of /etc directory
  - [x] tar + bzip2 compression of /etc directory
  - [x] Both require sudo permissions
- [x] **Size comparison:**
  - [x] Uses fileSize() function for both archives
  - [x] Displays difference between compression algorithms

### **H. Video Recording** ✅
- [x] **Panopto recording completed**
- [x] **Clear view of yourself and screen**
- [x] **Demonstrates all tasks A-G**
- [x] **Uploaded to correct Panopto drop box:**
  - "Creating Shell Scripts in a Unix Environment – RQN1 | D796"

### **I. Academic Citations** ✅
- [x] **APA-formatted citations** (if applicable)
- [x] **Proper references** for any quoted/paraphrased content
- [x] **Academic integrity maintained**

### **J. Professional Communication** ✅
- [x] **Professional presentation**
- [x] **Clear documentation**
- [x] **Proper grammar and spelling**
- [x] **Organized file structure**

---

## 📋 **SUBMISSION PACKAGE CHECKLIST**

### **Files to Submit:**

#### **1. Shell Scripts (Requirements A-G)**
```
📁 scripts/
├── user_management/
│   ├── create_user.sh          ✅ (Requirement A)
│   └── delete_user.sh          ✅ (Requirement B)
├── environment_config/
│   ├── aliases.sh              ✅ (Requirement C)
│   └── bashrc_updates.sh       ✅ (Requirement C)
├── package_management/
│   ├── install_vim.sh          ✅ (Requirement D)
│   └── update_packages.sh      ✅ (Requirement D)
├── network_monitoring/
│   ├── check_google.sh         ✅ (Requirement E)
│   ├── check_dns_ip.sh         ✅ (Requirement E)
│   └── check_dns_resolve.sh    ✅ (Requirement E)
├── disk_management/
│   └── cleanup_disk.sh         ✅ (Requirement F)
└── file_archiving/
    └── archive_compress.sh     ✅ (Requirement G)
```

#### **2. Supporting Documentation**
```
📄 Documentation Files:
├── README.docx                 ✅ Project overview
├── Configuration_Guide.docx    ✅ Setup instructions
├── Testing_Results.docx        ✅ Test execution results
├── PROJECT_SUMMARY.docx        ✅ Complete project summary
└── Network_Flowchart.docx      ✅ Flowchart (Requirement E1)
```

#### **3. Additional Files**
```
📁 Supporting Files:
├── bin/                        ✅ Executable scripts directory
├── logs/                       ✅ Log files (update.log, etc.)
├── run_assessment.sh           ✅ Master demonstration script
└── archives/                   ✅ Compressed file outputs
```

---

## 🚀 **SUBMISSION STEPS**

### **Step 1: Verify All Requirements** ✅
- [x] All scripts created and tested
- [x] All demonstrations completed
- [x] Video recording uploaded to Panopto
- [x] Documentation completed

### **Step 2: Prepare Submission Package**
- [x] **Create project ZIP file:**
  ```bash
  # Complete D796 project folder
  zip -r D796_Complete_Project.zip D796/
  ```

### **Step 3: Submit to WGU**
- [ ] **Links Section:**
  - [ ] Paste Panopto video URL
- [ ] **Attachments Section:**
  - [ ] Upload D796_Complete_Project.zip
  - [ ] Upload individual Word documents
  - [ ] Upload any additional supporting files

### **Step 4: Final Verification**
- [ ] **Video accessible** in Panopto
- [ ] **All files uploaded** successfully
- [ ] **Requirements A-J** all addressed
- [ ] **Professional presentation** maintained

---

## 🎯 **QUALITY ASSURANCE CHECKLIST**

### **Before Submitting:**

#### **Technical Requirements:**
- [x] All scripts executable and tested
- [x] All demonstrations work as expected
- [x] Error handling implemented
- [x] Proper file permissions set

#### **Documentation Quality:**
- [x] Professional formatting applied
- [x] Clear explanations provided
- [x] All requirements explicitly addressed
- [x] Spell check and grammar check completed

#### **Video Quality:**
- [x] Clear audio and video
- [x] All tasks demonstrated
- [x] Professional presentation
- [x] Uploaded to correct location

#### **Academic Standards:**
- [x] Original work demonstrated
- [x] Understanding of concepts shown
- [x] Professional communication maintained
- [x] Academic integrity guidelines followed

---

## 📊 **SUBMISSION STATUS**

### **Current Status: READY FOR SUBMISSION** ✅

**Completed Requirements:**
- ✅ **A-G: All shell scripts** created and tested
- ✅ **H: Video recording** completed and uploaded
- ✅ **I: Academic citations** addressed
- ✅ **J: Professional communication** maintained

**Files Ready:**
- ✅ **All shell scripts** functional and documented
- ✅ **Word documents** professionally formatted
- ✅ **Supporting documentation** complete
- ✅ **Project archive** ready for upload

**Next Action:**
- 📤 **Submit to WGU portal** with Panopto URL and attachments

---

## 🏆 **FINAL CONFIRMATION**

### **Assessment Requirements Coverage: 100%** ✅

**You have successfully completed ALL requirements for D796:**

- ✅ **Part A:** User creation script with all demonstrations
- ✅ **Part B:** User deletion script with all demonstrations  
- ✅ **Part C:** Complete shell environment configuration
- ✅ **Part D:** Package management scripts (vim + updates)
- ✅ **Part E:** Network monitoring with flowchart + 3 scripts
- ✅ **Part F:** Disk management with cleanDir() function
- ✅ **Part G:** File archiving with compression comparison
- ✅ **Part H:** Professional Panopto video recording
- ✅ **Part I:** Academic integrity and citations
- ✅ **Part J:** Professional communication standards

**🎉 CONGRATULATIONS! Your D796 assessment is complete and ready for submission!**

---

## 📞 **Final Submission Instructions**

1. **Go to WGU Student Portal**
2. **Navigate to D796 Assessment**
3. **Links Section:** Paste your Panopto video URL
4. **Attachments Section:** Upload your project files
5. **Submit for evaluation**

**You've done excellent work! This submission demonstrates mastery of Unix/Linux system administration and shell scripting concepts.** 🚀