import datetime
import re
import tkinter as tk
import tkinter.ttk as ttk
from .frameServico import ServicoFrame
from .frameAtendimento import AtendimentoFrame


class TelaPrincipalAdmin(tk.Frame):
    def __init__(self, master, banco):
        tk.Frame.__init__(self, master)
        self.master = master
        self.bd = banco
        master.title("MENU PRINCIPAL")

        self.container1 = tk.Frame(master)
        self.container1.pack(fill="both", expand=1)

        self.menu = tk.Menu(self.container1, borderwidth=1)
        self.prog = tk.Menu(self.menu, tearoff=0)
        #self.prog.add_command(label="Preferências", command=self.pref)
        self.prog.add_command(label="Fechar")
        self.menu.add_cascade(label="Programa", menu=self.prog)

        master.config(menu=self.menu)

        self.abas = ttk.Notebook(self.container1)
        self.abas.pack(fill="both", expand=1, padx=3, pady=3)

        self.painel_servicos = tk.Frame(self.abas)
        self.painel_atendimentos = tk.Frame(self.abas)

        self.painel_servicos.pack(fill="both", expand=1)
        self.painel_atendimentos.pack(fill="both", expand=1)

        self.abas.add(self.painel_servicos, text="SERVIÇOS")
        self.abas.add(self.painel_atendimentos, text="ATENDIMENTOS")

        self.nomeAdm = tk.Label(self.container1,
                                text="Admin: ",
                                font="Default 10")
        self.nomeAdm.pack(side="left", fill="both", padx=3, pady=3)

        self.logout = tk.Button(self.container1, text="Logout")
        self.logout.pack(side="right", fill="both", padx=3, pady=3)

        # Serviços
        self.servicos = ServicoFrame(self.painel_servicos, self.bd)
        # Atendimentos
        self.atendimentos = AtendimentoFrame(self.painel_atendimentos, self.bd)

    def pref(self):
        pass

    def renomear(self, login):
        novo = self.bd.exe(
            "SELECT nome FROM admin WHERE login=" + repr(login)).fetchone()[0]
        self.nomeAdm.configure(text="Admin: " + str(novo))


if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("530x370")
    TelaPrincipalAdmin(app, '')
    app.mainloop()
