import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog


class TelaPreferencias(tk.Frame):
    def __init__(self, master, arq_preferencias):
        tk.Frame.__init__(self, master)
        self.arq = arq_preferencias
        master.title("PREFERÊNCIAS")

        self.container1 = tk.Frame(master)
        self.container1.pack(fill="both", expand=1)

        self.container2 = tk.Frame(self.container1)
        self.container2.pack(fill="y", expand=1, padx=3, pady=3)

        self.btnOk = tk.Button(self.container1, text="OK \N{CHECK MARK}")
        self.btnOk.pack(side="bottom", anchor="e", padx=6, pady=6)

        tk.Label(self.container2,
                 text="Exportar banco de dados").grid(column=0,
                                                      row=0,
                                                      sticky="w",
                                                      padx=(8, 2),
                                                      pady=6)
        self.btn_exportar = tk.Button(
            self.container2, text="...", command=self.exportar)

        self.btn_exportar.grid(column=1, row=0, padx=2, pady=2, sticky="w")

        tk.Label(self.container2,
                 text="Importar banco de dados").grid(column=0,
                                                      row=1,
                                                      sticky="w",
                                                      padx=(8, 2),
                                                      pady=6)
        self.btn_importar = tk.Button(
            self.container2, text="...", command=self.importar)
        self.btn_importar.grid(column=1, row=1, padx=2, pady=2, sticky="w")

    def exportar(self):
        arq = filedialog.asksaveasfilename(
            title="Escolha onde exportar o banco",
            defaultextension=".db",
            filetypes=[("Banco de dados SQLITE", ".db")]
        )
        return arq

    def importar(self):
        arq = filedialog.askopenfilename(
            title="Escolha o arquivo para importar",
            defaultextension=".db",
            filetypes=[("Banco de dados SQLITE", ".db")]
        )
        return arq


if __name__ == "__main__":
    tela = tk.Tk()
    TelaPreferencias(tela, '')
    tela.mainloop()
