# define constants
$ROOT = ${pwd}

# $W_image = ""
# $W_container = ""
# $W_dockerfile = ""
$W_outpath = "$ROOT/out/release/windows/"

$L_image = "lamina_lin"
$L_container = "lamina_lin_ct"
$L_dockerfile = "$ROOT/tools/images/Dockerfile.lin"
$L_outpath = "$ROOT/out/release/linux/"


# define utility functions
# ------------------------------------------------------------------------------
function print_help() {
    Write-Host ""
    Write-Host "Lamina builder v1.0"
    Write-Host "----------------------------------------------------------------"
    Write-Host "Use powershell on Windows to use this script."
    Write-Host "Make sure to invoke this script from the root of Lamina repo only!"
    Write-Host "To build for Window, this script requires installation of Python 3.11 or higher."
    Write-Host "To build for Linux, this script requires installed and active Docker Engine."
    Write-Host ""
    Write-Host "Use one of the following flags to use this script"
    Write-Host "-w / window         - create release package for windows"
    Write-Host "-l / linux          - create release package for linux"
    Write-Host "-a / all            - create release package for all supported platforms"
    Write-Host "-h / help           - print usage help" 
    Write-Host ""
    Write-Host "HOW TO USE EXAMPLES"
    Write-Host "PS <script_path> -w"
    Write-Host "PS <script_path> linux"
}

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


# Build binaries for Linux
# ------------------------------------------------------------------------------
function build_linux(){
    Write-Host ""
    Write-Host "Starting building Lamina for Linux"
    docker build --tag $L_image --file $L_dockerfile .
    docker run --name $L_container $L_image
    
    Write-Host "Copying contents"
    clear_or_create_directory $L_outpath
    docker cp ${L_container}:"lamina/release/." $L_outpath

    # storing details in variabl to avoid printing them on console :)
    Write-Host "Removing temporary files"
    $VAR = & docker stop $L_container
    $VAR = & docker rm $L_container
    $VAR = & docker rmi $L_image

    Write-Host "Finished building Lamina for Linux"
}

# Build binaries for Windows
function build_windows(){
    Write-Host ""
    Write-Host "Starting building Lamina for Windows"
    clear_or_create_directory $W_outpath
    & "$ROOT/tools/builders/win_build.ps1"

    Write-Host "Finished building Lamina for Windows"
}

# ==============================================================================
# MAIN DRIVER
# ==============================================================================
$args = $args[0].ToLower()

if ($args -eq "window" -or $args -eq "-w") {
    build_windows

}
elseif ($args -eq "linux" -or $args -eq "-l") {
    build_linux
}
elseif ($args -eq "all" -or $args -eq "-a") {
    build_linux
    build_windows
}
elseif ($args -eq "help" -or $args -eq "-h") {
    print_help
}
else {
    Write-Host "ERROR : No build flags specified!"
    print_help
}