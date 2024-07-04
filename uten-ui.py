import tkinter as tk
from tkinter import filedialog
from pypdf import PdfMerger
import os
illegals = [
    "/",
    "<",
    ">",
    '"',
    "\\",
    "|",
    "?",
    "*"
]

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select files" ,filetypes=[(".pdf filer", "*.pdf")])
    return file_paths

def combineFiles(files, filename = "test.pdf"): #tror files er en tuple
    merger = PdfMerger()
    for file in files:
        try:
            merger.append(file)
        except: 
            print(f"Kunne ikke kombinere denne filen: {file}")

    try:
        merger.write(filename)
    except:
        print("Kunne ikke lagre fil...")


if __name__ == "__main__":
    selected_files = []
    while True:
        selected_files = select_files()
        if len(selected_files) <= 1:
            print("Vennligst velg mer enn 1 pdf-fil!")
        else:
            break

    while True:
        filnavn = input("Skriv inn filnavnet for den kombinerte filen: ")

        ill = False
        for illegal in illegals:
            if illegal in filnavn:
                print("Dette filnavnet er ikke gyldig!")
                ill = True
                break
        if ill: 
            continue

        if os.path.isfile(f"{filnavn}.pdf"):
            print("En fil med dette navnet eksisterer allerede! Velg et annet navn!")
            continue

        break
    
    filnavn += ".pdf"
    combineFiles(selected_files, filnavn)
