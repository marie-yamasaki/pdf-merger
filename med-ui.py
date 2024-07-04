import tkinter as tk
from tkinter import filedialog
from pypdf import PdfMerger
import os
'''
    For å gjøre om til en executable: 
        - `python -m PyInstaller --onefile -w "u.py"`
'''
class PdfMergerWindow:
    def __init__(self, name = "Kombiner pdf-filer!", size = (1280, 720)) -> None:
        self.name = name
        self.size = size

        self.illegals = [
            "/",
            "<",
            ">",
            '"',
            "\\",
            "|",
            "?",
            "*"
        ]

        self.root: tk.Tk = tk.Tk()
        self.gjemDisse = []
        self.filerLabel: tk.Label = tk.Label
        self.filenameEntry = tk.Label
        self.confirmBtn = tk.Button
        self.startWindow()

    def startWindow(self):
        self.root.title(self.name)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}")

        self.tittel = tk.Label(self.root, text=self.name, font=("Roboto 20"), height=3, width=0)
        self.tittel.pack()

        self.abort = tk.Button(self.root, text="Start på nytt", command=self.startProsess)
        self.abort.pack()

        self.startBtn = tk.Button(self.root, text="Trykk her for å starte!", command=self.startProsess)
        self.startBtn.pack()

        self.status = tk.Label(self.root, text="", font=("Roboto 14"), height=3)
        self.status.pack()

        self.root.mainloop()

    def gjemOgReset(self):
        if len(self.gjemDisse) != 0: #kanskje litt poengløst, men
            for hjem in self.gjemDisse:
                hjem.pack_forget()

    def startProsess(self):
        #self.status.configure(text="")
        self.gjemOgReset()
        
        self.startBtn.pack_forget()

        self.tittel.configure(text="Vennligst velg minst to filer ved hjelp av knappen nedenfor!")

        self.getfilesBtn = tk.Button(self.root, text="Trykk her for å velge filer", command=self.getFiles)
        self.getfilesBtn.pack()
        self.gjemDisse.append(self.getfilesBtn)

    def getFiles(self):
        self.status.configure(text="")
        self.getfilesBtn.pack_forget()
        
        self.file_paths = filedialog.askopenfilenames(title="Select files" ,filetypes=[(".pdf filer", "*.pdf")])
        if len(self.file_paths) <= 1:
            self.status.configure(text="Velg minst 2 filer!")
            self.startProsess()
            return 

        self.filerStr = "Du har valgt følgende filer: "
        for file in self.file_paths:
            self.filerStr += f"{file}, "
        self.filerLabel = tk.Label(self.root, text=self.filerStr, font=("Roboto 16"), height=3)
        self.filerLabel.pack()
        self.gjemDisse.append(self.filerLabel)

        self.getName()
        
    def getName(self):
        self.tittel.configure(text="Vennligst skriv inn et gyldig filnavn for den kombinerte filen!")

        self.filenameEntry = tk.Entry(self.root, width=20)
        self.filenameEntry.pack()
        if not self.filenameEntry in self.gjemDisse:
            self.gjemDisse.append(self.filenameEntry)

        self.confirmBtn = tk.Button(self.root, text="Trykk her for å bekrefte", command=self.checkName)
        self.confirmBtn.pack()
        if not self.confirmBtn in self.gjemDisse:
            self.gjemDisse.append(self.confirmBtn)


    def checkName(self):
        self.filenameEntry.pack_forget()
        self.confirmBtn.pack_forget()
        #sjekk gyldigheten her
        for illegal in self.illegals:
            if illegal in self.filenameEntry.get():
                self.status.configure(text=f"På Windows er det ikke lov med `{illegal}` i filnavnet!")
                self.getName()
                return

        #sjekk om filen eksisterer fra før
        self.filnavn = f"{self.filenameEntry.get()}.pdf"
        if os.path.isfile(self.filnavn):
            self.status.configure(text=f"En fil med navnet `{self.filenameEntry.get()}` eksisterer allerede! Vennligst velg et annet navn!")
            self.getName()
            return 

        self.status.configure(text=f"Du valgte filnavnet `{self.filenameEntry.get()}`. Trykk på knappen under for å bekrefte dette valget og kombinere filene over!")

        self.kombinerBtn = tk.Button(self.root, text="Trykk her for å kombinere filene over!", command=self.kombiner)
        self.kombinerBtn.pack()
        self.gjemDisse.append(self.kombinerBtn)
        
    def kombiner(self):
        self.status.configure(text=f"Kombinerer filene...")
        merger = PdfMerger()
        errorfiles = []
        print(self.file_paths)
        for file in self.file_paths:
            try:
                merger.append(file)
            except Exception as e:
                errorfiles.append(file)
                #print(e)

        errortext = "Kunne ikke kombinere disse filene: "
        if len(errorfiles) != 0:
            for errorfile in errorfiles:
                errortext += f"{errorfile}"

            self.status.configure(text=errortext)
        err = False
        try:
            merger.write(self.filnavn)
        except Exception as e:
            self.status.configure(text=f"Noe gikk galt. Prøv på nytt! {e}")
            err = True

        self.status.configure(text=f"Ferdig med å kombinere filene!")
        try:
            os.startfile(self.filnavn) #windows only
        except: 
            pass
        self.startProsess()
        
        
if __name__ == "__main__":
    vindu = PdfMergerWindow()
