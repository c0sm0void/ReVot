#!/bin/bash

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install -y python3 python3-pip

# Install additional packages
sudo apt-get install -y git
sudo apt install -y python3-pip

echo "All tasks completed successfully!"
