python -m PyInstaller --onefile --windowed --icon="ico.ico" "med-ui.py"
cd dist
ren "med-ui.exe" "kombiner-pdf.exe"
