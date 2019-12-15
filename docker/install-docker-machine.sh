#! /bin/bash

# The only way to make USB devices available in Docker containers under Windows or macOS 
# is to use the Docker Machine that comes with the usual installer and uses VirtualBox.

# source
# http://gw.tnode.com/docker/docker-machine-with-usb-support-on-windows-macos/
# https://github.com/docker/machine
# https://docs.docker.com/machine/install-machine/

# run from c:/

base=https://github.com/docker/machine/releases/download/v0.16.0 
mkdir -p "$HOME/bin" 
curl -L $base/docker-machine-Windows-x86_64.exe > "$HOME/bin/docker-machine.exe" 
chmod +x "$HOME/bin/docker-machine.exe"