#!/bin/bash

# This command in Bash that enables the shell's 'exit immediately' option. When 
# this option is set, if any command in the script exits with a non-zero status 
# (i.e., an error), the script will immediately exit and return the same error 
# status. This can be useful for ensuring that your script fails fast and doesn't 
# continue running after an error has occurred.
set -e

# create a temporary build directory
mkdir dist

# Install dependencies
pip3 install -r requirements.txt

# Build Windows binary
pyinstaller --distpath "/dist" --noconfirm --onedir --onefile --console --name "lamina" --clean "lamina/__main__.py"

# Package Windows binary
cd dist
zip lamina.zip lamina.exe
cd ..
mkdir -p out
mv dist/lamina.zip out/