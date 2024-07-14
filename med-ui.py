import tkinter as tk
from tkinter import filedialog
from pypdf import PdfWriter
import os

defaultfont = (
    "Roboto", 10, "bold"
)
class Knapp(tk.Button):
    def __init__(self, master = None, fontfamily = "Roboto", fontsize = 16, weight="bold", colour="black", background="white", padding=(10, 5), highlightbackgroundcolour="gray", highlightcolour = None, **kwargs):
        '''
            `fontfamily` er skrifttypen 

            `fontsize` er skriftstørrelsen

            `colour` er tekstens farge

            `background` er bakgrunnens farge

            `padding` er padding i `(x, y)` og er en tuple

            `highlightcolour` er den fargen knappens tekst har når musepekeren er over knappen 

            `highlightbackgroundcolour` er den fargen som knappens bakgrunn har når musepekeren er over knappen

            Kan også ha andre **kwargs
        '''
        super().__init__(master, **kwargs)
        
        self.config(
            relief=tk.FLAT, 
            bd=2, 
            highlightthickness=1,
            padx=padding[0],
            pady=padding[1],
            font=(fontfamily, fontsize, weight),
            foreground=colour,
            background=background,
        )
        self.colour = colour
        self.background = background
        self.highlightbackgroundcolour = highlightbackgroundcolour
        self.highlightcolour = highlightcolour

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        if self.highlightcolour != None:
            self.config(foreground=self.highlightbackgroundcolour)  # Change color on hover
        if self.highlightbackgroundcolour != None:
            self.config(background=self.highlightbackgroundcolour) 
    def on_leave(self, event):
        self.config(foreground=self.colour, background=self.background)

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
        '''
            Bare ikke spør...                           Dette er egentlig bare for å sørge for at disse variablene alltid eksisterer, men dette er stygt som bare det
        '''
        self.root: tk.Tk = tk.Tk()

        self.credit = None
        self.tittel = None
        self.statusText = ""
        self.unique = True

        self.startWindow()

    def renderBasic(self, startPaaNytt = True):
        '''
            Bare render alt basic ting som kommer til å være i alle vinduene

            Gjenbruk, whoooooooo
        '''
        self.credit = tk.Label(self.root, text="github@marie-yamasaki", font=("Roboto 10"))
        self.credit.pack()

        self.tittel = tk.Label(self.root, text=self.name, font=("Roboto 20"), height=3, width=0)
        self.tittel.pack()

        if startPaaNytt:
            self.abort = Knapp(self.root, text="Start på nytt", command=self.newbeginnings, fontsize=10)
            self.abort.pack(padx=10, pady=10)

        self.status = tk.Label(self.root, text=self.statusText, font=(defaultfont[0], 14, defaultfont[2]), height=3)
        self.status.pack(pady=10, padx=10)        
    
    def beGone(self, basic = True, startPaaNytt = True):
        for widget in self.root.winfo_children():
            widget.destroy()

        if basic:
            self.renderBasic(startPaaNytt=startPaaNytt)
    
    def newbeginnings(self):
        self.statusText = ""
        self.beGone(basic=False)
        self.startWindow()

    def startWindow(self):
        self.root.title(self.name)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}")

        self.renderBasic(startPaaNytt=False)

        self.startBtn = Knapp(self.root, text="Trykk her for å starte!", command=self.startProsess)
        self.startBtn.pack()

        self.root.mainloop()

    def startProsess(self):
        self.beGone()

        self.tittel.configure(text="Vennligst velg minst to filer ved hjelp av knappen nedenfor!")

        self.getfilesBtn = Knapp(self.root, text="Trykk her for å velge filer", command=self.getFiles)
        self.getfilesBtn.pack(padx=5, pady=5)

    def getFiles(self):
        self.getfilesBtn.pack_forget()
        self.status.configure(text="")
        
        self.file_paths = filedialog.askopenfilenames(title="Valgte filer" ,filetypes=[(".pdf filer", "*.pdf")])
        filepathslenght = len(self.file_paths)
        if filepathslenght <= 1:
            self.statusText = "Velg minst 2 filer!"
            self.startProsess()
            return 
        self.statusText = ""
        self.status.configure(text=f"Du har valgt {filepathslenght} filer. Vennligst gi den kombinerte filen et navn: ")
        self.getfilesBtn.configure(font=(defaultfont))
        self.filerStr = "Trykk på knappen nedenfor for å fortsette:"
        self.filnavnKnapp = Knapp(self.root, text="Trykk her for å fortsette", command=self.getName)
        self.filnavnKnapp.pack()

        self.filertuple = ("Du har valgt følgende filer:\n")
        for file in self.file_paths:
            self.filerStr += f"{file}, "
            self.filertuple = self.filertuple + (f"\t{file},\n")

        self.filerFrame = tk.Frame(self.root)
        self.filerFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) 
        self.filerText = tk.Text(self.filerFrame, wrap="word", height=1)
        self.filerText.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.filerscrollbar = tk.Scrollbar(self.filerFrame, orient="vertical", command=self.filerText.yview)
        self.filerscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.filerText.config(yscrollcommand=self.filerscrollbar.set)

        self.filerText.insert(tk.END, self.filertuple)

    def getName(self):
        if not self.unique:
            self.statusText = "Velg et annet navn! En annen fil eksisterer allerede med det navnet!"
            self.unique = True
        else:
            vennligts = "Vennligst skriv inn et unikt gyldig filnavn for den kombinerte filen!"
            self.name = vennligts
            self.status.configure(text=vennligts)
        self.beGone()

        self.filenameEntry = tk.Entry(self.root, width=20,font=defaultfont)
        self.filenameEntry.pack(padx=10, pady=10)

        self.confirmBtn = Knapp(self.root, text="Trykk her for å bekrefte", command=self.checkName)
        self.confirmBtn.pack()


    def checkName(self):
        #sjekk gyldigheten her
        rawname: str = self.filenameEntry.get()
        if rawname.isspace() or len(rawname) == 0:
            self.statusText = "Du kan ikke la filnavnet stå tomt!"
            self.getName()
            return

        for illegal in self.illegals:
            if illegal in rawname:
                self.statusText = f"På Windows er det ikke lov med `{illegal}` i filnavnet!"
                self.getName()
                return

        #sjekk om filen eksisterer fra før
        self.filnavn = f"{rawname}.pdf"
        if os.path.isfile(self.filnavn):
            self.unique = False
            self.getName()
            return 
        
        self.beGone()
        self.status.configure(text=f"Du valgte filnavnet `{self.filnavn.replace(".pdf", "")}`. Trykk på knappen under for å bekrefte dette valget og kombinere filene over!")

        self.velgAnnetNavn = Knapp(self.root, text="Trykk her for å velge et annet navn", fontsize=12, command=self.getName)
        self.velgAnnetNavn.pack(pady=10)

        self.kombinerBtn = Knapp(self.root, text="Trykk her for å kombinere filene over!", command=self.kombiner)
        self.kombinerBtn.pack()
        
    def kombiner(self):
        self.status.configure(text=f"Kombinerer filene...")
        writer = PdfWriter()
        errorfiles = []
        print(self.file_paths)
        for file in self.file_paths:
            try:
                with open(file, "rb") as f:
                    writer.append(fileobj=f)
            except Exception as e:
                errorfiles.append(file)

        errortext = "Kunne ikke kombinere disse filene: "
        if len(errorfiles) != 0:
            for errorfile in errorfiles:
                errortext += f"{errorfile}"

            self.status.configure(text=errortext)
        try:
            with open(self.filnavn, "w") as f:
                writer.write(self.filnavn)
        except Exception as e:
            self.status.configure(text=f"Noe gikk galt. Prøv på nytt! {e}")

        self.status.configure(text=f"Ferdig med å kombinere filene!")
        try:
            os.startfile(self.filnavn) #windows only
        except: 
            pass

        writer.close()

        self.statusText = ""
        self.newbeginnings()
        
if __name__ == "__main__":
    vindu = PdfMergerWindow()
