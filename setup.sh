#!/bin/bash

echo "Setting up Life Calendar Wallpaper..."

# Check for Flatpak
if ! command -v flatpak &> /dev/null; then
    echo "Flatpak not found. Installing..."
    sudo apt-get update && sudo apt-get install -y flatpak
else
    echo "Flatpak is already installed."
fi

# Add Flathub repo
echo "Adding Flathub repository..."
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Install Hidamari
echo "Installing Hidamari..."
flatpak install -y flathub io.github.jeffshee.Hidamari

echo "Granting Hidamari access to the project folder..."
flatpak override --user --filesystem=$(pwd) io.github.jeffshee.Hidamari

echo "Granting Hidamari access to GPU devices..."
flatpak override --user --device=all io.github.jeffshee.Hidamari

echo "Installation complete!"
echo "Launching Hidamari..."
echo "Please add 'index.html' from $(pwd) to the Local tab in Hidamari."

flatpak run io.github.jeffshee.Hidamari &
