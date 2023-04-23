# THIS IS WORK IN OROGRESS. DO NOT USE!
#!/bin/bash

# Utility functions
# ------------------------------------------------------------------------------
function clear_or_create_directory {
    if [ -d "$1" ]; then
        echo "Directory $1 exists. Clearing contents..."
        rm -rf "$1/*"
    else
        echo "Directory $1 does not exist. Creating directory..."
        mkdir -p "$1"
    fi
}

VERSION=""
function get_project_version() {
    VERSION=$(python3 lamina/metadata.py)
}

# Build functions
# ------------------------------------------------------------------------------
function build_debug_pkg() {
    clear_or_create_directory "out/build"
}

function build_release_pkg() {
    get_project_version
    RELEASE_ROOT="out/release/lamina_$VERSION"

    clear_or_create_directory "out/build"
    clear_or_create_directory "$RELEASE_ROOT/app"
    clear_or_create_directory "$RELEASE_ROOT/config"

    config_raw=$(cat extra/artifacts/lamina.toml)
    config_raw=${config_raw//"<<VERSION>>"/$VERSION}
    echo "$config_raw" > "$RELEASE_ROOT/config/lamina.toml"

    # mkdir -p "$RELEASE_ROOT/data"
    # mkdir -p "$RELEASE_ROOT/docs"
    # mkdir -p "$RELEASE_ROOT/extra"
    cp extra/artifacts/launch.bat "$RELEASE_ROOT"

    echo "Creating build environment ..."
    python3.11 -m venv buildenv

    # (IMPORTANT)
    echo "Activating build environment ..."
    source ./buildenv/bin/activate

    echo "Installing dependencies in build environment"
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "Building Lamina v$VERSION"
    pyinstaller \
        --specpath "out/build" \
        --workpath "out/build" \
        --distpath "$RELEASE_ROOT/app" \
        --noconfirm \
        --onedir \
        --onefile \
        --console \
        --name "lamina" \
        --clean \
        --log-level ERROR \
        "lamina/__main__.py"

    echo "Cleaning up"
    deactivate
    rm -rf "./buildenv/"

    echo "Lamina v$VERSION build SUCCESS"
}

# ------------------------------------------------------------------------------
# DRIVER
# ------------------------------------------------------------------------------
args=$1

python_version=$(python -c 'import sys; print(sys.version_info[:2])')
if [ $python_version != "(3, 11)" ]; then
    echo "Can't build binaries in Python version $python_version"
    echo "Install Python 3.11 or higher and then retry"
    exit
fi

if [ "$args" == "release" ] || [ "$args" == "-r" ]; then
    echo "Building release package"
    build_release_pkg
elif [ "$args" == "debug" ] || [ "$args" == "-d" ]; then
    echo "Building debug package"
    build_debug_pkg
else
    echo ""
    echo "Lamina builder v1.0"
    echo "-------------------------------------------------"
    echo "Use one of the following flag to use this script"
    echo "-r / release      - create a release build with packaging"
    echo "-d / debug        - create a debug build"
    echo "-h / help         - print this help"
    echo ""
    echo "usage examples" 
    echo "<path_to_script> -r"
    echo "<path_to_script> release"
    echo "<path_to_script> debug"
    echo ""
    echo "NOTE : Call this script from the root of the Lamina repository only!"
    echo "NOTE : This script requires Python 3.11 or higher"
    echo ""
fi