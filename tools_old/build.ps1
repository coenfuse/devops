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

$global:VERSION = ""
function get_project_version() {
    $global:VERSION = & python lamina/metadata.py
}

# Build functions
# ------------------------------------------------------------------------------
function build_debug_pkg() {
    clear_or_create_directory "out/build"
}

function build_release_pkg() {
    get_project_version
    $RELEASE_ROOT = "out/release/lamina_$global:VERSION"

    clear_or_create_directory "out/build"
    clear_or_create_directory $RELEASE_ROOT
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/app" | Out-Null
    New-Item -ItemType Directory -Path "$RELEASE_ROOT/config" | Out-Null

    $config_raw = Get-Content extra/artifacts/lamina.toml -Raw
    $config_raw = $config_raw.Replace("<<VERSION>>", $global:VERSION)
    Set-Content -Path "$RELEASE_ROOT/config/lamina.toml" -Value $config_raw

    # New-Item -ItemType Directory -Path "$RELEASE_ROOT/data" | Out-Null
    # New-Item -ItemType Directory -Path "$RELEASE_ROOT/docs" | Out-Null
    # New-Item -ItemType Directory -Path "$RELEASE_ROOT/extra" | Out-Null
    Copy-Item -Path extra/artifacts/launch.bat -Destination $RELEASE_ROOT
    # New-Item -ItemType File -Path "$RELEASE_ROOT/readme.md" | Out-Null

    Write-Host "Creating build environment ..."
    python -m venv buildenv

    # (IMPORTANT)
    Write-Host "Activating build environment ..."
    ./buildenv/Scripts/activate

    Write-Host "Installing dependencies in build environment"
    python -m pip install --upgrade pip
    pip install -r requirements.txt

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

    Write-Host "Cleaning up"
    deactivate
    Remove-Item -Path "./buildenv/" -Recurse -Force

    Write-Host "Lamina v$VERSION build SUCCESS"
}

# ------------------------------------------------------------------------------
# DRIVER
# ------------------------------------------------------------------------------
$args = $args[0]

$pythonCmd = Get-Command python
if ($pythonCmd.Version -lt [Version]"3.11") {
    $version = $pythonCmd.Version
    Write-Host "Can't build binaries in Python version $version"
    Write-Host "Install Python 3.11 or higher and then retry"
    exit
}

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
    echo "NOTE : This script requires Python 3.11 or higher"
    echo ""
}
