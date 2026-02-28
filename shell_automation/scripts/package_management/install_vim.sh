#!/bin/bash

# install_vim.sh - Script to install vim package
# Part D.1 of D796 Assessment - Unix/Linux System Administration
# Author: System Administrator
# Date: $(date)

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages with timestamp
log_message() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

# Function to log error messages
log_error() {
    echo -e "${RED}[ERROR $(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" >&2
}

# Function to detect the package manager
detect_package_manager() {
    if command -v apt-get >/dev/null 2>&1; then
        echo "apt"
    elif command -v yum >/dev/null 2>&1; then
        echo "yum"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v zypper >/dev/null 2>&1; then
        echo "zypper"
    elif command -v pacman >/dev/null 2>&1; then
        echo "pacman"
    else
        echo "unknown"
    fi
}

# Function to check if vim is already installed
check_vim_installed() {
    if command -v vim >/dev/null 2>&1; then
        return 0  # vim is installed
    else
        return 1  # vim is not installed
    fi
}

# Function to get vim version if installed
get_vim_version() {
    if check_vim_installed; then
        vim --version | head -n 1 | cut -d' ' -f5
    else
        echo "Not installed"
    fi
}

# Function to install vim using appropriate package manager
install_vim() {
    local pkg_manager="$1"
    
    log_message "Installing vim using $pkg_manager package manager..."
    
    case "$pkg_manager" in
        "apt")
            # Debian/Ubuntu systems
            log_message "Updating package list..."
            if sudo apt-get update; then
                log_message "Package list updated successfully"
            else
                log_error "Failed to update package list"
                return 1
            fi
            
            log_message "Installing vim..."
            if sudo apt-get install -y vim; then
                log_message "Vim installed successfully using apt"
                return 0
            else
                log_error "Failed to install vim using apt"
                return 1
            fi
            ;;
            
        "yum")
            # RHEL/CentOS 7 and older
            log_message "Installing vim using yum..."
            if sudo yum install -y vim; then
                log_message "Vim installed successfully using yum"
                return 0
            else
                log_error "Failed to install vim using yum"
                return 1
            fi
            ;;
            
        "dnf")
            # RHEL/CentOS 8+ and Fedora
            log_message "Installing vim using dnf..."
            if sudo dnf install -y vim; then
                log_message "Vim installed successfully using dnf"
                return 0
            else
                log_error "Failed to install vim using dnf"
                return 1
            fi
            ;;
            
        "zypper")
            # openSUSE
            log_message "Installing vim using zypper..."
            if sudo zypper install -y vim; then
                log_message "Vim installed successfully using zypper"
                return 0
            else
                log_error "Failed to install vim using zypper"
                return 1
            fi
            ;;
            
        "pacman")
            # Arch Linux
            log_message "Installing vim using pacman..."
            if sudo pacman -S --noconfirm vim; then
                log_message "Vim installed successfully using pacman"
                return 0
            else
                log_error "Failed to install vim using pacman"
                return 1
            fi
            ;;
            
        *)
            log_error "Unsupported package manager: $pkg_manager"
            log_error "Please install vim manually using your system's package manager"
            return 1
            ;;
    esac
}

# Function to verify vim installation
verify_installation() {
    log_message "Verifying vim installation..."
    
    if check_vim_installed; then
        local vim_version=$(get_vim_version)
        log_message "Vim is successfully installed!"
        echo -e "${BLUE}=== Vim Installation Details ===${NC}"
        echo -e "${YELLOW}Version:${NC} $vim_version"
        echo -e "${YELLOW}Location:${NC} $(which vim)"
        echo -e "${YELLOW}Installation Date:${NC} $(date)"
        
        # Show vim features
        echo -e "\n${BLUE}=== Vim Features ===${NC}"
        vim --version | grep -E "^\+|^-" | head -10
        
        return 0
    else
        log_error "Vim installation verification failed"
        return 1
    fi
}

# Function to create a simple vim configuration
create_vim_config() {
    local vimrc_file="$HOME/.vimrc"
    
    if [ ! -f "$vimrc_file" ]; then
        log_message "Creating basic vim configuration..."
        
        cat > "$vimrc_file" << 'EOF'
" Basic vim configuration for D796 Assessment
" Created by install_vim.sh script

" Enable syntax highlighting
syntax on

" Show line numbers
set number

" Enable auto-indentation
set autoindent
set smartindent

" Set tab width to 4 spaces
set tabstop=4
set shiftwidth=4
set expandtab

" Enable search highlighting
set hlsearch
set incsearch

" Show matching brackets
set showmatch

" Enable mouse support
set mouse=a

" Show current position
set ruler

" Enable file type detection
filetype on
filetype plugin on
filetype indent on

" Set color scheme (if available)
try
    colorscheme desert
catch
    " Default colors if desert is not available
endtry

" Status line configuration
set laststatus=2
set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [POS=%l,%v][%p%%]\ %{strftime(\"%d/%m/%y\ -\ %H:%M\")}

" Enable backspace in insert mode
set backspace=indent,eol,start

" Save backup files in a specific directory
set backup
set backupdir=~/.vim/backup//
set directory=~/.vim/swap//
set undodir=~/.vim/undo//

" Create backup directories if they don't exist
if !isdirectory($HOME."/.vim")
    call mkdir($HOME."/.vim", "", 0770)
endif
if !isdirectory($HOME."/.vim/backup")
    call mkdir($HOME."/.vim/backup", "", 0700)
endif
if !isdirectory($HOME."/.vim/swap")
    call mkdir($HOME."/.vim/swap", "", 0700)
endif
if !isdirectory($HOME."/.vim/undo")
    call mkdir($HOME."/.vim/undo", "", 0700)
endif
EOF
        
        log_message "Basic vim configuration created at $vimrc_file"
    else
        log_message "Vim configuration already exists at $vimrc_file"
    fi
}

# Main function
main() {
    echo -e "${BLUE}=== Vim Installation Script ===${NC}"
    echo -e "${BLUE}D796 Assessment - Package Management${NC}"
    echo -e "${BLUE}===================================${NC}\n"
    
    log_message "Starting vim installation process..."
    
    # Check if vim is already installed
    if check_vim_installed; then
        local vim_version=$(get_vim_version)
        echo -e "${YELLOW}Vim is already installed${NC}"
        echo -e "${BLUE}=== Current Vim Installation ===${NC}"
        echo -e "${YELLOW}Version:${NC} $vim_version"
        echo -e "${YELLOW}Location:${NC} $(which vim)"
        
        # Show some vim details
        echo -e "\n${BLUE}=== Vim Information ===${NC}"
        vim --version | head -5
        
        log_message "Vim installation check completed - already installed"
        
        # Ask if user wants to create/update vim configuration
        echo -e "\n${YELLOW}Would you like to create/update vim configuration? (y/n):${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            create_vim_config
        fi
        
        return 0
    fi
    
    log_message "Vim is not installed. Proceeding with installation..."
    
    # Detect package manager
    local pkg_manager=$(detect_package_manager)
    log_message "Detected package manager: $pkg_manager"
    
    if [ "$pkg_manager" = "unknown" ]; then
        log_error "Could not detect a supported package manager"
        echo -e "${RED}Supported package managers: apt, yum, dnf, zypper, pacman${NC}"
        echo -e "${YELLOW}Please install vim manually using your system's package manager${NC}"
        exit 1
    fi
    
    # Check if we have sudo privileges
    if ! sudo -n true 2>/dev/null; then
        echo -e "${YELLOW}This script requires sudo privileges to install packages.${NC}"
        echo -e "${YELLOW}You may be prompted for your password.${NC}"
    fi
    
    # Install vim
    if install_vim "$pkg_manager"; then
        # Verify installation
        if verify_installation; then
            # Create basic vim configuration
            create_vim_config
            
            echo -e "\n${GREEN}=== Installation Summary ===${NC}"
            echo -e "${GREEN}✓ Vim has been successfully installed${NC}"
            echo -e "${GREEN}✓ Installation verified${NC}"
            echo -e "${GREEN}✓ Basic configuration created${NC}"
            
            echo -e "\n${BLUE}=== Next Steps ===${NC}"
            echo -e "${YELLOW}1. Test vim by running:${NC} vim --version"
            echo -e "${YELLOW}2. Create a test file:${NC} vim test.txt"
            echo -e "${YELLOW}3. Customize ~/.vimrc as needed${NC}"
            
            log_message "Vim installation completed successfully!"
        else
            log_error "Vim installation verification failed"
            exit 1
        fi
    else
        log_error "Vim installation failed"
        exit 1
    fi
}

# Function to show script usage
show_usage() {
    echo -e "${BLUE}Usage: $0 [OPTIONS]${NC}"
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  --check     Check if vim is installed without installing"
    echo -e "  --version   Show vim version if installed"
    echo -e "  --config    Create/update vim configuration only"
    echo -e "  --help      Show this help message"
    echo -e "\n${YELLOW}Examples:${NC}"
    echo -e "  $0          Install vim (default behavior)"
    echo -e "  $0 --check  Check vim installation status"
    echo -e "  $0 --config Create vim configuration"
}

# Handle command line arguments
case "$1" in
    --check)
        echo -e "${BLUE}=== Vim Installation Check ===${NC}"
        if check_vim_installed; then
            echo -e "${GREEN}✓ Vim is installed${NC}"
            echo -e "${YELLOW}Version:${NC} $(get_vim_version)"
            echo -e "${YELLOW}Location:${NC} $(which vim)"
            exit 0
        else
            echo -e "${RED}✗ Vim is not installed${NC}"
            exit 1
        fi
        ;;
    --version)
        if check_vim_installed; then
            vim --version
            exit 0
        else
            echo -e "${RED}Vim is not installed${NC}"
            exit 1
        fi
        ;;
    --config)
        create_vim_config
        exit 0
        ;;
    --help)
        show_usage
        exit 0
        ;;
    "")
        # Default behavior - run main function
        main
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_usage
        exit 1
        ;;
esac