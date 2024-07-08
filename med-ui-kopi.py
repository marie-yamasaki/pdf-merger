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
        self.gjemDisse = []
        self.filerText = tk.Text
        self.filenameEntry = tk.Label
        self.filnavnKnapp = tk.Button
        self.confirmBtn = tk.Button
        self.abort = tk.Button
        self.filerFrame = tk.Frame
        self.velgAnnetNavn = Knapp 
        self.startWindow()

    def is_rendered(self, widget: tk.Widget):
        if widget.winfo_manager():
            return True
        return False
    
    def render(self, widget: tk.Widget, padx=0, pady=0, fill = None, expand = False, side=tk.TOP):
        '''
            For å være ærlig så tror jeg ikke at denne funker
        '''
        if not self.is_rendered(widget):
            widget.pack(padx=padx, pady=pady, fill=fill, expand=expand, side=side)

    def newbeginnings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.startWindow()

    def startWindow(self):
        self.root.title(self.name)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}")

        self.credit = tk.Label(self.root, text="github@marie-yamasaki", font=("Roboto 10"))
        self.render(self.credit) #for å være ærlig er dette så dårlig kode at jeg tror ikke at jeg burde ha dette her
        #i mitt forsvar så funker koden min
        self.tittel = tk.Label(self.root, text=self.name, font=("Roboto 20"), height=3, width=0)
        self.render(self.tittel)

        

        self.startBtn = Knapp(self.root, text="Trykk her for å starte!", command=self.startProsess)
        self.render(self.startBtn)

        self.root.mainloop()

    def gjemOgReset(self):
        if len(self.gjemDisse) != 0: #kanskje litt poengløst, men
            for hjem in self.gjemDisse:
                hjem.pack_forget()

    def startProsess(self):
        self.gjemOgReset()

        self.abort = Knapp(self.root, text="Start på nytt", command=self.newbeginnings, fontsize=10)
        self.render(self.abort, padx=10, pady=10)

        self.status = tk.Label(self.root, text="", font=(defaultfont[0], 14, defaultfont[2]), height=3)
        self.status.pack(pady=10, padx=10)
        if not self.abort in self.gjemDisse:
            self.gjemDisse.append(self.abort)
        
        self.startBtn.destroy()

        self.tittel.configure(text="Vennligst velg minst to filer ved hjelp av knappen nedenfor!")

        self.getfilesBtn = Knapp(self.root, text="Trykk her for å velge filer", command=self.getFiles)
        self.render(self.getfilesBtn, padx=5, pady=5)
        self.gjemDisse.append(self.getfilesBtn)

    def getFiles(self):
        self.getfilesBtn.pack_forget()
        self.status.configure(text="")
        
        self.file_paths = filedialog.askopenfilenames(title="Valgte filer" ,filetypes=[(".pdf filer", "*.pdf")])
        filepathslenght = len(self.file_paths)
        if filepathslenght <= 1:
            self.status.configure(text="Velg minst 2 filer!")
            self.startProsess()
            return 
        
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
        self.render(self.filerFrame, fill=tk.BOTH, expand=True, padx=10, pady=10) 
        self.filerText = tk.Text(self.filerFrame, wrap="word", height=1)
        self.render(self.filerText, side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.gjemDisse.append(self.filerFrame)

        self.filerscrollbar = tk.Scrollbar(self.filerFrame, orient="vertical", command=self.filerText.yview)
        self.filerscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.filerText.config(yscrollcommand=self.filerscrollbar.set)

        self.gjemDisse.append(self.filerscrollbar)
        self.filerText.insert(tk.END, self.filertuple)

        
    def getName2(self):
        self.filenameEntry.destroy()
        self.confirmBtn.destroy()
        self.velgAnnetNavn.destroy()
        self.confirmBtn.destroy()
        self.kombinerBtn.destroy()
        
        self.status.configure(text="Velg et annet navn")
        self.getName() #gud, dette er dårlig kode
    def getName(self):
        #jeg bør virkelig finne på noe bedre her
        self.filnavnKnapp.pack_forget()
        self.filerFrame.destroy()

        self.tittel.configure(text="Vennligst skriv inn et unikt gyldig filnavn for den kombinerte filen!")

        self.filenameEntry = tk.Entry(self.root, width=20,font=defaultfont)
        self.filenameEntry.pack(padx=10, pady=10)
        if not self.filenameEntry in self.gjemDisse:
            self.gjemDisse.append(self.filenameEntry)

        self.confirmBtn = Knapp(self.root, text="Trykk her for å bekrefte", command=self.checkName)
        self.render(self.confirmBtn)
        if not self.confirmBtn in self.gjemDisse:
            self.gjemDisse.append(self.confirmBtn)


    def checkName(self):
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
            self.tittel.configure(text=f"En fil med navnet `{self.filenameEntry.get()}` eksisterer allerede! Vennligst velg et annet navn!")
            self.getName2()
            return 
        
        self.filenameEntry.destroy()
        self.confirmBtn.destroy()

        self.status.configure(text=f"Du valgte filnavnet `{self.filnavn.replace(".pdf", "")}`. Trykk på knappen under for å bekrefte dette valget og kombinere filene over!")

        self.velgAnnetNavn = Knapp(self.root, text="Trykk her for å velge et annet navn", fontsize=12, command=self.getName2)
        self.render(self.velgAnnetNavn)

        self.kombinerBtn = Knapp(self.root, text="Trykk her for å kombinere filene over!", command=self.kombiner)
        self.kombinerBtn.pack()
        self.gjemDisse.append(self.kombinerBtn)
        
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

        self.newbeginnings()
        
if __name__ == "__main__":
    vindu = PdfMergerWindow()