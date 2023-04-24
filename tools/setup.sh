#!/bin/bash

# Check if python3.11 or above is present
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version | awk '{print $2}')
    major_version=$(echo $python_version | awk -F'.' '{print $1}')
    minor_version=$(echo $python_version | awk -F'.' '{print $2}')
    if (( $major_version > 3 || ($major_version == 3 && $minor_version >= 11) )); then
        echo "Python version $python_version is installed."
    else
        echo "Python version $python_version is not supported!"
        echo "Install Python 3.11 or higher and then restart this setup."
        exit
    #   read -p "Do you want to install the latest version of Python3? (Y/N): " -n 1 -r
    #    echo
    #    if [[ $REPLY =~ ^[Yy]$ ]]; then
    #        latest_version=$(apt-cache policy python3 | awk '/Candidate:/ {print $2}')
    #        sudo apt-get install -y python3="$latest_version"
    #    fi
    fi
else
    echo "Python3 is not installed!"
    echo "Install Python 3.11 or higher and then restart this setup."
    exit
    # read -p "Do you want to install the latest version of Python3? (Y/N): " -n 1 -r
    # echo
    # if [[ $REPLY =~ ^[Yy]$ ]]; then
    #    sudo apt-get update
    #    latest_version=$(apt-cache policy python3 | awk '/Candidate:/ {print $2}')
    #    sudo apt-get install -y python3="$latest_version"
    # fi
fi

echo "Creating dev virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies in virtual environment..."
pip3 install -r requirements.txt

echo ""
echo "Lamina dev environment setup SUCCESS"