#!/usr/bin/env bash

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
  python3-mysql.connector \
  software-properties-common \
  unzip


# Install task if it isn't installed.
if command -v task &> /dev/null; then
    echo "Task is already installed: $(task --version)"
else
    echo "Task was not found, installing..."
    # Install `task`
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


# Install docker if it isn't installed
if command -v docker &> /dev/null; then
    echo "Docker is installed: $(docker --version)"
else
    echo "Docker is not installed. Installing Docker..."

    sudo apt-get update
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) \
      signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    sudo usermod -aG docker $USER
    echo "Installed docker successfully: $(docker --version)"
fi
