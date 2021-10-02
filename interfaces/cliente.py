import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

DATA_DE_HOJE = datetime.date.today()


class TelaPrincipalCliente(tk.Frame):
    def __init__(self, master, banco):
        global DATA_DE_HOJE
        tk.Frame.__init__(self, master)
        self.master = master
        self.bd = banco
        self.id_cliente = '0'
        self.master.title("MENU PRINCIPAL")
        self.master.geometry("250x276")

        self.container1 = tk.Frame(master)
        self.container1.pack(fill="both", expand=1)

        self.menu = tk.Menu(self.container1, borderwidth=1)
        self.prog = tk.Menu(self.menu, tearoff=0)
        self.prog.add_command(label="Fechar", command=self.fechar)
        self.menu.add_cascade(label="Programa", menu=self.prog)

        self.master.config(menu=self.menu)

        self.abas = ttk.Notebook(self.container1, height=17)
        self.abas.pack(fill="both", expand=1, padx=3, pady=3)

        self.painel_novo = tk.Frame(self.abas)
        self.painel_visualizar = tk.Frame(self.abas)

        self.painel_novo.pack(fill="both", expand=1)
        self.painel_visualizar.pack(fill="both", expand=1)

        self.abas.add(self.painel_novo, text="NOVO")
        self.abas.add(self.painel_visualizar, text="VISUALIZAR")

        self.nomeUser = tk.Label(self.container1,
                                 text="Usuário: ",
                                 font="Default 10")
        self.nomeUser.pack(side="left", fill="both", padx=3, pady=3)

        self.logout = tk.Button(self.container1, text="Logout")
        self.logout.pack(side="right", fill="both", padx=3, pady=3)

        # Contratos

        self.containerC1 = tk.Frame(self.painel_novo, bd=5)

        self.containerC2 = tk.Frame(self.painel_visualizar, bd=5)
        self.containerC1.pack(fill='both',
                              side="left",
                              expand=1,
                              padx=3,
                              pady=3)
        self.containerC2.pack(fill='both',
                              side="left",
                              expand=1,
                              padx=3,
                              pady=3)

        # INSERÇÃO
        self.container3 = tk.Frame(self.containerC1)
        self.container3.pack(fill='both', expand=1, padx=3, pady=3)

        tk.Label(self.container3, text="SERVIÇO:").grid(row=0,
                                                        column=0,
                                                        sticky="w")
        self.servico = ttk.Combobox(
            self.container3, width=25, state="readonly")
        self.servico.grid(row=1, column=0, padx=3, pady=3, columnspan=2)

        #self.filtro = tk.Button(self.container3, text="Filtro")
        #self.filtro.grid(row=0, column=1, sticky="e", pady=3, padx=(0, 3))

        # tk.Label(self.container3, text="VALOR:").grid(
        #     row=2, column=0, sticky="e")

        # self.valor = tk.Entry(self.container3, state="readonly", width=10)
        # self.valor.grid(row=2, column=1, pady=3, sticky="w")

        tk.Label(self.container3, text="DATA:").grid(
            row=3, column=0, sticky="e"
        )
        self.data = DateEntry(
            self.container3,
            DATA_DE_HOJE.strftime("%d/%m/%Y"),
            width=10)
        self.data.grid(row=3, column=1, pady=3, sticky="w")

        tk.Label(self.container3, text="HORÁRIO:").grid(
            row=4, column=0, sticky="e"
        )

        self.horario = ttk.Combobox(self.container3, width=5, state="readonly")
        self.horario.configure(
            values=[
                "7h30", "8h00", "8h30", "9h00",
                "9h30", "10h00", "10h30", "11h00",
                "11h30", "12h00", "13h30", "14h00",
                "14h30", "15h00", "15h30", "16h00",
                "16h30", "17h00", "17h30"
            ]
        )
        self.horario.grid(row=4, column=1, pady=3, sticky="w")

        self.container4 = tk.Frame(self.containerC1)
        self.container4.pack(fill='both', expand=1, padx=3, pady=3)
        self.btn_inserir = tk.Button(
            self.container4, text="MARCAR ATENDIMENTO", command=self.marcar_atendimento)
        self.btn_inserir.pack(side="left", expand=1, fill="both")

        # VISUALIZAR REGISTROS
        self.container5 = tk.Frame(self.containerC2)
        self.container5.pack(fill='both', expand=1)

        barraV = tk.Scrollbar(self.container5, orient="vertical")
        barraH = tk.Scrollbar(self.container5, orient="horizontal")
        self.lista_atendimentos = tk.Listbox(self.container5,
                                             width=20,
                                             height=7,
                                             yscrollcommand=barraV.set,
                                             xscrollcommand=barraH.set,
                                             selectmode="SINGLE")
        barraV.config(command=self.lista_atendimentos.yview)
        barraV.pack(side="right", fill='y', )

        self.container6 = tk.Frame(self.containerC2)
        self.container6.pack(side="bottom", fill='both', expand=1)

        barraH.config(command=self.lista_atendimentos.xview)
        barraH.pack(side="bottom", fill='x')

        self.lista_atendimentos.pack(fill='both', expand=1)
        self.cancelar = tk.Button(
            self.container6, text="CANCELAR ATENDIMENTO", command=self.cancelar_atendimento)
        self.cancelar.pack(expand=1, fill="both")
        self.atualizar_registros()

    def trocar_usuario(self, login):
        nome, id = self.bd.cursor.execute(
            "SELECT nome, id FROM CLIENTE WHERE login=" +
            repr(login)).fetchone()
        self.nomeUser.configure(text="Usuário: " + nome)
        self.id_cliente = str(id)
        self.atualizar_registros()

    def fechar(self):
        self.master.destroy()

    def atualizar_registros(self):
        self.limpar_campos()
        self.listar_servicos()
        self.listar_atendimentos()

    def cancelar_atendimento(self):
        index = self.lista_atendimentos.curselection()
        if index:
            id = self.lista_atendimentos.get(index, index)[
                0].split("|")[0].strip()
            if messagebox.askokcancel(
                title="Cancelamento",
                message="Tem certeza que deseja cancelar o atendimento selecionado?"
            ):
                self.bd.cancelar_atendimento(id)
                self.lista_atendimentos.delete(index)
                self.lista_atendimentos.select_clear(0, tk.END)
                self.lista_atendimentos.select_set(0)
                self.atualizar_registros()
        else:
            messagebox.showinfo(title="Informação",
                                message="Nenhum registro foi selecionado")

    def limpar_campos(self):
        self.servico.set('')
        self.data.delete(0, tk.END)
        self.horario.set('')

    def valida_dados(self):
        obrigatorios = [
            self.servico.get().strip(),
            self.data.get().strip(),
            self.horario.get().strip(),
        ]
        if all([bool(x)for x in obrigatorios]):
            data = self.data.get().strip()
            if len(data) == 10:
                return True
        else:
            messagebox.showinfo(
                title="Aviso", message="Preencha todos os campos obrigatórios (servico, dia, horário)")

    def marcar_atendimento(self):
        if self.valida_dados():
            self.bd.marcar_atendimento(self.get_dados())
            messagebox.showinfo("Sucesso", f"Marcado com sucesso!")
            self.atualizar_registros()

    def listar_atendimentos(self):
        atendimentos = []
        for atendimento in self.bd.listar_atendimentos(self.id_cliente):
            atendimento = [str(x) for x in atendimento]
            atendimentos.append(" | ".join(atendimento))
        self.lista_atendimentos.delete(0, tk.END)
        self.lista_atendimentos.insert(0, *atendimentos)

    def listar_servicos(self):
        servicos = []
        for servico in self.bd.listar_servicos():
            servico = [str(x) for x in servico]
            servicos.append(" | ".join(servico))
        self.servico.option_clear()
        self.servico.configure(values=servicos)

    def get_dados(self):
        return {
            "id_cliente": self.id_cliente,
            "id_servico": self.servico.get().split('|')[0].strip(),
            "data": self.data.get().strip(),
            "horario": self.horario.get().strip(),
            "status": "Pendente"
        }


class DateEntry(tk.Entry):
    def __init__(self, mst, data_base=DATA_DE_HOJE, **kwargs):
        tk.Entry.__init__(self, master=mst, **kwargs)
        self.data_base = data_base

        self.bind("<KeyPress>", self.__inserir)
        self.bind("<KeyRelease>", self.__inserir)
        self.bind("<FocusIn>", self.__cursor)
        self.bind("<ButtonRelease>", self.__cursor)
        self.cursorpos = 0

    def __cursor(self, e):
        self.icursor(self.cursorpos)

    def __inserir(self, e):
        if e.keysym in "0123456789":
            if len(self.get()) == 2:
                if self.get()[:2] > "31":
                    self.delete(0, tk.END)
                    self.insert(tk.END, "31")
                elif self.get()[:2] == "00":
                    self.delete(0, tk.END)
                    self.insert(0, "01")
                self.insert(tk.END, "/")

            elif len(self.get()) == 5:
                if self.get()[3:5] > "12":
                    self.delete(3, tk.END)
                    self.insert(tk.END, "12")
                elif self.get()[3:5] in ("04", "06", "09",
                                         "11") and self.get()[:2] == "31":
                    self.delete(1)
                    self.insert(1, "0")
                elif self.get()[3:5] == "02":
                    if self.get()[:2] > "29":
                        self.delete(0, 2)
                        self.insert(0, "29")
                elif self.get()[3:5] == "00":
                    self.delete(3, tk.END)
                    self.insert(tk.END, "01")

                self.insert(tk.END, "/")

            elif len(self.get()) >= 10:
                if self.get()[6:10] <= self.data_base[6:10]:
                    self.delete(6, tk.END)
                    self.insert(tk.END, self.data_base[6:10])

                    if self.get()[3:5] <= self.data_base[3:5]:
                        self.delete(3, 5)
                        self.insert(3, self.data_base[3:5])

                        if self.get()[:2] <= self.data_base[:2]:
                            self.delete(0, 2)
                            self.insert(0, self.data_base[:2])
                if self.get()[3:5] == "02":
                    if DateEntry.ehbissexto(int(self.get()[6:10])):
                        dm = "29"
                    else:
                        dm = "28"

                    if self.get()[:2] > dm:
                        self.delete(0, 2)
                        self.insert(0, dm)

                self.delete(10, tk.END)
            self.cursorpos = self.index(tk.INSERT)
        elif e.keysym == "BackSpace":
            self.delete(tk.END)
            self.cursorpos = self.index(tk.INSERT)
        elif e.keysym in ("Tab", "ISO_Left_Tab"):
            self.select_clear()
        else:
            return "break"

    def ehbissexto(ano):
        return ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0


if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("310x260")
    TelaPrincipalCliente(app, '')
    app.mainloop()
