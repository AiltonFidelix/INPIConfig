:: Author: Ailton Fidelx
:: Date: 04/05/2024
:: Description: INPIConfig Windows deploy script

:: Convert ui files to python
pyside6-uic ui\inpiconfig.ui -o src\ui_inpiconfig.py

:: Build python code and generate executable
pyinstaller inpiconfig.spec

:: Generate the installer executable
ISCC innosetup.iss