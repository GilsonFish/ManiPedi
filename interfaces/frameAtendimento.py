import tkinter as tk
# import tkinter.ttk as ttk
from tkinter import messagebox


class AtendimentoFrame(tk.Frame):
    def __init__(self, master, banco):
        tk.Frame.__init__(self, master)
        self.master = master
        self.bd = banco
        self.container1 = tk.Frame(self.master, bd=5)

        self.container1.pack(fill='both',
                             side="left",
                             expand=1,
                             padx=3,
                             pady=3)

        # VISUALIZAR ATENDIMENTOS
        self.container2 = tk.Frame(self.container1)
        self.container2.pack(fill='both', expand=1)

        barraV = tk.Scrollbar(self.container2, orient="vertical")
        barraH = tk.Scrollbar(self.container2, orient="horizontal")
        self.lista_atendimentos = tk.Listbox(self.container2,
                                             width=30,
                                             height=12,
                                             yscrollcommand=barraV.set,
                                             xscrollcommand=barraH.set,
                                             selectmode="SINGLE")
        barraV.config(command=self.lista_atendimentos.yview)
        barraV.pack(side="right", fill='both')

        self.container3 = tk.Frame(self.container1)
        self.container3.pack(side="bottom", fill='both', expand=1)

        barraH.config(command=self.lista_atendimentos.xview)
        barraH.pack(side="bottom", fill='both')

        self.lista_atendimentos.pack(fill='both', expand=1)
        self.btn_confirmar = tk.Button(
            self.container3,
            text="CONFIRMAR ATENDIMENTO",
            padx=5,
            pady=10,
            command=self.confirmar_atendimento
        )
        self.btn_confirmar.pack(side="left", expand=1, fill="x")
        self.listar_atendimentos()

    def listar_atendimentos(self):
        pesquisa = f"""SELECT id, id_cliente,
                    id_servico,data,horario, status
                    FROM atendimento;"""
        consulta = self.bd.exe(pesquisa)
        atendimentos = consulta.fetchall()
        self.lista_atendimentos.delete(0, tk.END)
        for atendimento in atendimentos:
            atendimento = [str(x) for x in atendimento]
            self.lista_atendimentos.insert(tk.END, " | ".join(atendimento))

    def confirmar_atendimento(self):
        index = self.lista_atendimentos.curselection()
        if index:
            id = self.lista_atendimentos.get(index, index)[0].split(" | ")[0].strip()
            self.bd.confirmar_atendimento(id)
            self.lista_atendimentos.select_clear(0, tk.END)
            self.listar_atendimentos()
            self.lista_atendimentos.select_set(0)
            messagebox.showinfo(title="Sucesso",
                                message="Atendimento marcado como concluído")
        else:
            messagebox.showinfo(title="Informação",
                                message="Nenhum registro foi selecionado")
