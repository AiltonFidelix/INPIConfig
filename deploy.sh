# Author: Ailton Fidelx
# Date: 04/05/2024
# Description: INPIConfig Linux deploy script

# Convert ui files to python
pyside6-uic ui/inpiconfig.ui -o src/ui_inpiconfig.py

# Build python code and generate executable
pyinstaller inpiconfig.spec

# Create the necessary paths to the deploy application
mkdir INPIConfig
mkdir -p INPIConfig/DEBIAN
mkdir -p INPIConfig/usr/share/INPIConfig/bin
mkdir -p INPIConfig/usr/share/INPIConfig/icon
mkdir -p INPIConfig/usr/share/applications

# Copy all necessary files to the followed dirs
cp control INPIConfig/DEBIAN
cp dist/INPIConfig INPIConfig/usr/share/INPIConfig/bin
cp assets/icons/config.png INPIConfig/usr/share/INPIConfig/icon
cp inpiconfig.desktop INPIConfig/usr/share/applications

# Generate the .deb installer
dpkg --build INPIConfig