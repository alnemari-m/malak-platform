#!/bin/bash
# Renode Installation Script for Malak Platform Validation
# Tested on Ubuntu 20.04+, Arch Linux

set -e  # Exit on error

echo "=========================================="
echo "Renode Installation for Malak Platform"
echo "=========================================="

# Detect OS
if [ -f /etc/arch-release ]; then
    OS="arch"
elif [ -f /etc/lsb-release ]; then
    OS="ubuntu"
else
    echo "Unsupported OS. This script supports Ubuntu and Arch Linux."
    exit 1
fi

echo "Detected OS: $OS"

# Install dependencies
echo ""
echo "Step 1: Installing dependencies..."
if [ "$OS" = "arch" ]; then
    sudo pacman -S --needed --noconfirm mono gtk-sharp-2 screen uml_utilities wget
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get update
    sudo apt-get install -y mono-complete gtk-sharp2 screen uml-utilities wget
fi

# Download Renode
echo ""
echo "Step 2: Downloading Renode..."
RENODE_VERSION="1.14.0"
RENODE_DEB="renode_${RENODE_VERSION}_amd64.deb"
RENODE_URL="https://github.com/renode/renode/releases/download/v${RENODE_VERSION}/${RENODE_DEB}"

if [ ! -f "${RENODE_DEB}" ]; then
    wget "${RENODE_URL}"
else
    echo "Renode package already downloaded."
fi

# Install Renode
echo ""
echo "Step 3: Installing Renode..."
if [ "$OS" = "ubuntu" ]; then
    sudo dpkg -i "${RENODE_DEB}" || sudo apt-get install -f -y
elif [ "$OS" = "arch" ]; then
    # Extract .deb manually on Arch
    ar x "${RENODE_DEB}"
    sudo tar -xf data.tar.xz -C /
fi

# Verify installation
echo ""
echo "Step 4: Verifying installation..."
if command -v renode &> /dev/null; then
    echo "✓ Renode installed successfully!"
    renode --version
else
    echo "✗ Renode installation failed."
    exit 1
fi

# Install ARM toolchain for cross-compilation
echo ""
echo "Step 5: Installing ARM GCC toolchain..."
if [ "$OS" = "arch" ]; then
    sudo pacman -S --needed --noconfirm arm-none-eabi-gcc arm-none-eabi-newlib
elif [ "$OS" = "ubuntu" ]; then
    sudo apt-get install -y gcc-arm-none-eabi libnewlib-arm-none-eabi
fi

# Verify ARM toolchain
if command -v arm-none-eabi-gcc &> /dev/null; then
    echo "✓ ARM toolchain installed successfully!"
    arm-none-eabi-gcc --version | head -n1
else
    echo "✗ ARM toolchain installation failed."
    exit 1
fi

# Set up Python environment for model export
echo ""
echo "Step 6: Setting up Python environment..."
if [ ! -d "venv_renode" ]; then
    python -m venv venv_renode
    source venv_renode/bin/activate
    pip install --upgrade pip
    pip install torch torchvision numpy onnx
    echo "✓ Python virtual environment created."
else
    echo "Python environment already exists."
fi

echo ""
echo "=========================================="
echo "✓ Renode setup complete!"
echo "=========================================="
echo ""
echo "To activate the Python environment:"
echo "  source venv_renode/bin/activate"
echo ""
echo "To start Renode:"
echo "  renode"
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/export_model.py"
echo "  2. Run: ./simulations/run_all_simulations.sh"
echo ""
