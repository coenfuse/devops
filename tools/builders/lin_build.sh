g_VERSION=""

# Utility functions
# ------------------------------------------------------------------------------
function fetch_project_version() {
    g_VERSION=$(python3 lamina/metadata.py)
}


# Build functions
# ------------------------------------------------------------------------------
function build_release_pkg() {
    fetch_project_version
    echo "Adding files to Lamina_$g_VERSION bundle ..."

    RELEASE_ROOT="release/lamina_$g_VERSION"
    
    mkdir -p "$RELEASE_ROOT/app"
    mkdir -p "$RELEASE_ROOT/config"

    config_raw=$(cat extra/artifacts/lamina.toml)
    config_raw=${config_raw//"<<VERSION>>"/$g_VERSION}
    echo "$config_raw" > "$RELEASE_ROOT/config/lamina.toml"

    # mkdir -p "$RELEASE_ROOT/data"
    # mkdir -p "$RELEASE_ROOT/docs"
    # mkdir -p "$RELEASE_ROOT/extra"
    cp extra/artifacts/launch.sh "$RELEASE_ROOT"

    echo "Building Lamina_$g_VERSION binaries for Linux ..."
    pyinstaller \
        --specpath "out/build/" \
        --workpath "out/build/" \
        --distpath "$RELEASE_ROOT/app" \
        --noconfirm \
        --onedir \
        --onefile \
        --console \
        --name "lamina" \
        --clean \
        --log-level ERROR \
        "lamina/__main__.py"

    echo "Lamina_$g_VERSION binaries build SUCCESS"
}

# ==============================================================================
# MAIN DRIVER
# ==============================================================================
build_release_pkg