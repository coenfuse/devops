# Utility functions
# ------------------------------------------------------------------------------
function clear_or_create_directory($directory) {
    if (Test-Path $directory -PathType Container) {
        Write-Host "Directory $directory exists. Clearing contents..."
        Remove-Item $directory\* -Force -Recurse
    }
    else {
        Write-Host "Directory $directory does not exist. Creating directory..."
        New-Item -ItemType Directory -Path $directory | Out-Null
    }
}

$VERSION = ""
function get_project_version() {
    # Read the contents of metadata.py file
    $metadata = Get-Content lamina/metadata.py -Raw

    # Extract the values for __VER_MAJOR, __VER_MINOR, __VER_PATCH, and __VER_BUILD
    $MAJOR = [regex]::Match($metadata, '(?<=__MAJOR = )\d+').Value
    $MINOR = [regex]::Match($metadata, '(?<=__MINOR = )\d+').Value
    $PATCH = [regex]::Match($metadata, '(?<=__PATCH = )\d+').Value
    $BUILD = [regex]::Match($metadata, '(?<=__BUILD = )\d+').Value

    $IN_BETA = [regex]::Match($metadata, '(?<=__IN_BETA = )True|False').Value
    $BETA_BUILD = [regex]::Match($metadata, '(?<=__BETA_BUILD = )\d+').Value

    # Print the values
    if ($IN_BETA -eq "True") {
        $VERSION = "$MAJOR.$MINOR" + "b" + "-$BETA_BUILD"
    }
    else {
        $VERSION = "$MAJOR.$MINOR.$PATCH.$BUILD"
    }
}

# Build functions
# ------------------------------------------------------------------------------
function build_debug_pkg() {
    clear_or_create_directory "out/build"
}

function build_release_pkg() {
    get_project_version
    $RELEASE_ROOT = "out/release/lamina_$VERSION"

    clear_or_create_directory "out/build"
    clear_or_create_directory $RELEASE_ROOT
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/app" | Out-Null
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/config" | Out-Null
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/data" | Out-Null
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/docs" | Out-Null
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/extra" | Out-Null
    New-Item -ItemType File -Path "$RELEASE_ROOT/readme.md" | Out-Null
    New-Item -ItemType File -Path "$RELEASE_ROOT/launch.sh" | Out-Null

    # activating venv before running installer (IMPORTANT)
    Write-Host "Activating virtual environment ..."
    ./venv/Scripts/activate

    Write-Host "Building Lamina v$VERSION"
    pyinstaller `
        --specpath "out/build" `
        --workpath "out/build" `
        --distpath "$RELEASE_ROOT/app" `
        --noconfirm `
        --onedir `
        --onefile `
        --console `
        --name "lamina" `
        --clean `
        --log-level ERROR `
        "lamina/__main__.py"

    Write-Host "Lamina v$VERSION build SUCCESS"
}

# ------------------------------------------------------------------------------
# DRIVER
# ------------------------------------------------------------------------------
$args = $args[0]

if ($args -eq "release" -or $args -eq "-r") {
    Write-Host "Building release package"
    build_release_pkg
}
elseif ($args -eq "debug" -or $args -eq "-d") {
    Write-Host "Building debug package"
    build_debug_pkg
}
else {
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
}
