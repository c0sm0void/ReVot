#!/bin/bash

# Detect the operating system
if [[ -f /etc/debian_version ]]; then
    #Debian

    echo "Debian based System Detected"
    echo "Updating and upgrading system"

    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3 python3-pip git

    echo "All tasks completed successfully!"

elif [[ -f /etc/arch-release ]]; then
    #Arch Linux

    echo "Arch-Linux Detected"
    echo "Updating and upgrading system."

    sudo pacman -Syu --noconfirm
    sudo pacman -S --noconfirm python python-pip git

    echo "All tasks completed successfully!"

elif [[ -f /etc/fedora-release ]]; then
    #RHEL

    echo "Red Hat Linux Detected"
    echo "Updating and upgrading system"

    sudo dnf update -y
    sudo dnf install -y python3 python3-pip git

    echo "All tasks completed successfully"

else
    echo "Unsupported Linux distribution"
fi
