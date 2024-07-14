python -m PyInstaller --onefile --windowed --icon="ico.ico" "med-ui.py"
cd dist
set filnavn="kombiner-pdf.exe"
IF EXIST [%filnavn%] (
    del [%filnavn%]
)
ren "med-ui.exe" "kombiner-pdf.exe"
