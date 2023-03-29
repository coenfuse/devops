# Utility functions
# ------------------------------------------------------------------------------
F_clear_or_create_directory() {
  if [ -d "$1" ]
  then
    echo "Directory $1 exists. Clearing contents..."
    rm -rf "${1:?}/"*
  else
    echo "Directory $1 does not exist. Creating directory..."
    mkdir -p "$1"
  fi
}

VERSION=""
F_get_project_version() {
    # Read the contents of metadata.py file
    metadata=$(cat lamina/metadata.py)

    # Extract the values for __VER_MAJOR, __VER_MINOR, __VER_PATCH, and __VER_BUILD
    MAJOR=$(echo "$metadata" | grep -oP '__MAJOR = \K\d+')
    MINOR=$(echo "$metadata" | grep -oP '__MINOR = \K\d+')
    PATCH=$(echo "$metadata" | grep -oP '__PATCH = \K\d+')
    BUILD=$(echo "$metadata" | grep -oP '__BUILD = \K\d+')
    
    IN_BETA=$(echo "$metadata" | grep -oP '__IN_BETA = \K(True|False)')
    BETA_BUILD=$(echo "$metadata" | grep -oP '__BETA_BUILD = \K\d+')

    # Print the values
    if [ $IN_BETA == "True" ]
      then
      VERSION="$MAJOR.$MINOR"b"-$BETA_BUILD"
    else
      VERSION="$MAJOR.$MINOR.$PATCH.$BUILD"
    fi
}

# Build functions
# ------------------------------------------------------------------------------
F_build_debug_pkg() {
    F_clear_or_create_directory "out/build"
}

F_build_release_pkg() {
    F_get_project_version
    RELEASE_ROOT="out/release/lamina_$VERSION"

    F_clear_or_create_directory "out/build"
    F_clear_or_create_directory $RELEASE_ROOT
    mkdir "$RELEASE_ROOT/app"
    mkdir "$RELEASE_ROOT/config"
    mkdir "$RELEASE_ROOT/data"
    mkdir "$RELEASE_ROOT/docs"
    mkdir "$RELEASE_ROOT/extra"
    mkdir "$RELEASE_ROOT/out"
    touch "$RELEASE_ROOT/readme.md"
    touch "$RELEASE_ROOT/launch.sh"

    # activating venv before running installer (IMPORTANT)
    echo "Activating virtual environment..."
    source ./venv/bin/activate

    echo "Building Lamina v$VERSION"
    pyinstaller \
    --specpath "out/build" \
    --workpath "out/build" \
    --distpath "$RELEASE_ROOT/app" \
    --paths "venv/lib/python3.11/site-packages" \
    --noconfirm \
    --onedir \
    --onefile \
    --console \
    --name "lamina" \
    --clean \
    --log-level ERROR \
    "lamina/__main__.py"

    echo "Lamina v$VERSION build SUCCESS"
}

# ------------------------------------------------------------------------------
# DRIVER
# ------------------------------------------------------------------------------
args=$1

if [ $args == 'release' -o $args == '-r' ]
then
    echo "Building release package"
    F_build_release_pkg
elif [ $args == 'debug' -o $args == '-d' ]
then
    echo "Building debug package"
    F_build_debug_pkg
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
    echo "NOTE : This script requires Python 3.11 and PyInstaller 5.9.0 or higher"
    echo ""
fi