# Author: Ailton Fidelx
# Date: 04/05/2024
# Description: INPIConfig Windows deploy script

# Create virtual env and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Convert ui files to python
pyside6-uic ui/inpiconfig.ui -o src/ui_inpiconfig.py

# Build python code and generate executable
pyinstaller inpiconfig.spec

# Deactivate venv
deactivate

rm -rf venv
rm -rf build
rm -rf dist