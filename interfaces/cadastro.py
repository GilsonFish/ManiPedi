import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from entry import CPFEntry, EmailEntry, FoneEntry


class TelaCadastro(tk.Frame):
    def __init__(self, master, banco):
        tk.Frame.__init__(self, master)
        self.master = master
        self.bd = banco

        self.master.title("Cadastro")

        self.container1 = tk.Frame(self.master, bd=5)
        self.container1.pack()

        tk.Label(self.container1, text="CADASTRAR USUÁRIO").pack(fill='x')

        self.container2 = tk.Frame(self.container1)
        self.container2.pack(fill='both', expand=1, padx=3, pady=3)

        tk.Label(self.container2, text="NOME:").grid(row=0,
                                                     column=0,
                                                     sticky="e",
                                                     padx=2,
                                                     pady=2)
        self.nome = tk.Entry(self.container2)
        self.nome.grid(row=0, column=1, sticky="e", padx=2, pady=2)

        tk.Label(self.container2, text="CPF:").grid(row=1,
                                                    column=0,
                                                    sticky="e",
                                                    padx=2,
                                                    pady=2)
        self.cpf = CPFEntry(self.container2)
        self.cpf.grid(row=1, column=1, sticky="e", padx=2, pady=2)

        tk.Label(self.container2, text="E-MAIL:").grid(row=2,
                                                       column=0,
                                                       sticky="e",
                                                       padx=2,
                                                       pady=2)

        self.email = EmailEntry(self.container2)
        self.email.grid(row=2, column=1, sticky="e", padx=2, pady=2)

        tk.Label(self.container2, text="TELEFONE:").grid(row=3,
                                                         column=0,
                                                         sticky="e",
                                                         padx=2,
                                                         pady=2)
        self.fone = FoneEntry(self.container2)
        self.fone.grid(row=3, column=1, sticky="e", padx=2, pady=2)

        tk.Label(self.container2, text="LOGIN:").grid(row=4,
                                                      column=0,
                                                      sticky="e",
                                                      padx=2,
                                                      pady=2)
        self.login = tk.Entry(self.container2)
        self.login.grid(row=4, column=1, sticky="e", padx=2, pady=2)

        tk.Label(self.container2, text="SENHA:").grid(row=5,
                                                      column=0,
                                                      sticky="e",
                                                      padx=2,
                                                      pady=2)
        self.senha = tk.Entry(self.container2, show="*")
        self.senha.grid(row=5, column=1, sticky="e", padx=2, pady=2)

        tk.Button(self.container2, text="...", font='Verdana 3', command=self.ver_senha).grid(
            row=5, column=2, sticky="w", padx=2, pady=2)

        self.btnLimpar = tk.Button(self.container1,
                                   text="LIMPAR",
                                   command=self.limpar_campos)
        self.btnLimpar.pack(side='left', fill='x', expand=1, padx=3)
        self.btnSalvar = tk.Button(self.container1,
                                   text="SALVAR",
                                   command=self.cadastrar_usuario)
        self.btnSalvar.pack(side='left', fill='x', expand=1, padx=3)

        self.nome.focus()

    def ver_senha(self):
        if self.senha['show'] == '*':
            self.senha.configure(show='')
        else:
            self.senha.configure(show='*')

    def get_dados(self):
        return {
            "nome": self.nome.get().strip(),
            "cpf": self.cpf.get().strip(),
            "email": self.email.get().strip(),
            "fone": self.fone.get().strip(),
            "login": self.login.get().strip(),
            "senha": self.senha.get().strip()
        }

    def limpar_campos(self):
        self.nome.delete(0, tk.END)
        self.cpf.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.fone.delete(0, tk.END)
        self.login.delete(0, tk.END)
        self.senha.delete(0, tk.END)
        self.nome.focus()

    def valida_dados(self):
        obrigatorios = [
            self.nome.get().strip(),
            self.cpf.get().strip(),
            self.fone.get().strip(),
            self.login.get().strip(),
            self.senha.get().strip(),
        ]
        if all([bool(x)for x in obrigatorios]):
            login = self.login.get().strip()
            cpf = self.cpf.get().strip()
            res = self.bd.cursor().execute("SELECT login, cpf FROM cliente;").fetchall()
            logins = [x[0] for x in res]
            cpfs = [x[1] for x in res]

            if login not in logins:
                if (cpf not in cpfs):
                    if len(cpf) == 11:
                        return True
                    else:
                        messagebox.showwarning(
                            "Aviso", f"O cpf '{cpf}' está incompleto!")
                        return False
                else:
                    messagebox.showwarning(
                        "Aviso", f"O cpf '{cpf}' já foi cadastrado!")
                    return False
            else:
                messagebox.showwarning(
                    "Aviso", f"O login '{login}' já foi cadastrado!")
                return False
        else:
            messagebox.showinfo(
                title="Aviso", message="Preencha todos os campos obrigatórios (nome, cpf, telefone, login, senha)")

    def cadastrar_usuario(self):
        if self.valida_dados():
            self.bd.cadastrar_usuario(self.get_dados())
            messagebox.showinfo("Sucesso", f"Cadastrado com sucesso!")


if __name__ == "__main__":
    bd = sqlite3.connect("teste.db")
    tela = tk.Tk()
    TelaCadastro(tela, bd)
    tela.mainloop()
