#!/bin/bash

podman build -t hxl32/indentationerror-net:latest -t hxl32/indentationerror-net:$(git describe --tags) .
podman run -it --rm -p 8080:8080 hxl32/indentationerror-net:latest
