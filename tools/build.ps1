# define constants
$ROOT = ${pwd}

# $W_image = ""
# $W_container = ""
# $W_dockerfile = ""
$W_outpath = "$ROOT/out/release/win/"

$L_image = "lamina_lin"
$L_container = "lamina_lin_ct"
$L_dockerfile = "$ROOT/tools/images/Dockerfile.lin"
$L_outpath = "$ROOT/out/release/lin/"


# define utility functions
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


# Build binaries for Linux
function build_linux(){
    Write-Host ""
    Write-Host "Starting building Lamina for Linux"
    docker build --tag $L_image --file $L_dockerfile .
    docker run --name $L_container $L_image
    
    Write-Host "Copying contents"
    clear_or_create_directory $L_outpath
    docker cp ${L_container}:"lamina/release/." $L_outpath

    Write-Host "Removing temporary files"
    docker stop $L_container
    docker rm $L_container
    docker rmi $L_image

    Write-Host "Finished building Lamina for Linux"
}

# Build binaries for Windows
function build_windows(){
    Write-Host ""
    Write-Host "Starting building Lamina for Windows"
    clear_or_create_directory $W_outpath
    Write-Host "Finished building Lamina for Windows"
}

# ==============================================================================
# MAIN DRIVER
# ==============================================================================
Write-Host "What platform do want to build for?"
Write-Host "Press W for Windows"
Write-Host "Press L for Linux"
Write-Host "Press B for Both"
$platform = Read-Host
$platform = $platform.ToUpper()

switch($platform) {
    "B" {
        build_linux
        build_windows
    }
    "W" { 
        build_windows 
    }
    "L" { 
        build_linux 
    }
    default { 
        Write-Host "Invalid input. Please type 'W', 'L', or 'B'." 
    }
}