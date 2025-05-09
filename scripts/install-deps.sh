#!/usr/bin/env bash

# This script installs the dependencies needed to run the application.

# Exit on any error
set -e

# Error on undefined variable
set -u

# Update and install libraries
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
  ca-certificates \
  checkinstall \
  curl \
  git \
  python3 \
  python3-pip \
  python3-venv \
  software-properties-common \
  unzip


# Install task if it isn't installed.
if command -v task &> /dev/null; then
    echo "Task is already installed: $(task --version)"
else
    echo "Task was not found, installing..."
    task_pkg_arch=$(dpkg --print-architecture)
    task_pkg_path="$(mktemp -t --suffix ".deb" task-pkg.XXXXXXXXXX)"
    curl \
        --fail \
        --location \
        --output "$task_pkg_path" \
        --show-error \
        "https://github.com/go-task/task/releases/download/v3.42.1/task_linux_${task_pkg_arch}.deb"
    dpkg --install "$task_pkg_path"
    rm "$task_pkg_path"
fi