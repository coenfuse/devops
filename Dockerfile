# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the entire host directory into the container at /app/Lamina
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Build the release package
RUN VERSION=$(python lamina/metadata.py) && \
    mkdir -p out/release/lamina_$VERSION/app && \
    mkdir -p out/release/lamina_$VERSION/config && \
    cp extra/artifacts/launch.sh out/release/lamina_$VERSION/ && \
    cp extra/artifacts/lamina.toml out/release/lamina_$VERSION/config/lamina.toml && \
    sed -i "s/<<VERSION>>/$VERSION/g" out/release/lamina_$VERSION/config/lamina.toml && \
    pyinstaller --specpath "out/build" --workpath "out/build" --distpath "out/release/lamina_$VERSION/app" \
        --noconfirm --onedir --onefile --console --name "lamina" --clean --log-level ERROR "lamina/__main__.py" && \
    rm -rf out/build

# THIS STUFF BARELY WORKS
# 1. Build the image
# 2. Run the container and prevent it from exiting using sleep inifinity
# 3. Copy build binaries from container to host using docker cp lamina_built:builder/out/release ./out/release/lin