# Utility functions
# ------------------------------------------------------------------------------
function clear_or_create_directory($directory) {
    if (Test-Path $directory -PathType Container) {
        # Write-Host "Directory $directory exists. Clearing contents..."
        Remove-Item $directory\* -Force -Recurse
    }
    else {
        # Write-Host "Directory $directory does not exist. Creating directory..."
        New-Item -ItemType Directory -Path $directory | Out-Null
    }
}

$global:VERSION = ""
function get_project_version() {
    $global:VERSION = & python lamina/metadata.py
}

# Build functions
# ------------------------------------------------------------------------------
function build_release_pkg() {
    get_project_version
    Write-Host "Adding files to release bundle"

    $RELEASE_ROOT = "out/release/windows/lamina_$global:VERSION"
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

    Write-Host "Creating build environment"
    python -m venv ./temp/venv

    # (IMPORTANT)
    Write-Host "Activating build environment"
    ./temp/venv/Scripts/activate

    Write-Host "Installing dependencies"
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    Write-Host "Generating binaries"
    pyinstaller `
        --specpath "temp/build" `
        --workpath "temp/build" `
        --distpath "$RELEASE_ROOT/app" `
        --noconfirm `
        --onedir `
        --onefile `
        --console `
        --name "lamina" `
        --clean `
        --log-level ERROR `
        "lamina/__main__.py"

    Write-Host "Removing temporary files"
    deactivate
    Remove-Item -Path "./temp/" -Recurse -Force
}

# ------------------------------------------------------------------------------
# DRIVER
# ------------------------------------------------------------------------------
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    $pythonVersion = $pythonCmd.Version
    if ($pythonVersion -ge [Version]"3.11") {
        build_release_pkg
    } 
    else {
        Write-Host "Can't build binaries with Python version $version"
        Write-Host "Install Python 3.11 or higher and then retry."
        exit
    }
} 
else {
    Write-Host "Python is not installed!"
    Write-Host "Please install Python 3.11 or higher and then retry."
    exit
}