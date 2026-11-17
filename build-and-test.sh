#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"
echo "$(git describe --tags)" > ./src/templates/version_string.txt
podman build -t hxl32/indentationerror-net:latest -t hxl32/indentationerror-net:$(git describe --tags) .
podman run -it --rm -p 8080:8080 hxl32/indentationerror-net:latest
