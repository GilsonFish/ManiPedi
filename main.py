import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring

from backend import BancoDeDados
from interfaces import (TelaLogin, TelaCadastro,
                        TelaPreferencias, TelaPrincipalAdmin,
                        TelaPrincipalCliente)

BANCO = "banco.db"


class App():
    def __init__(self, master, banco):
        self.master = master
        self.master.withdraw()
        if not os.path.isfile(banco):
            self.bd = BancoDeDados(banco)
            self.bd.exe_sql_file("backend/banco.sql")
        else:
            self.bd = BancoDeDados(banco)
        self.verifica_admin()

        self.topLogin = tk.Toplevel(self.master)
        self.topCadastro = tk.Toplevel(self.master)
        self.topTPAdmin = tk.Toplevel(self.master)
        self.topTPCliente = tk.Toplevel(self.master)
        self.topPref = tk.Toplevel(self.topTPAdmin)
        # -self.topFiltro = tk.Toplevel(self.topTPCliente)

        self.topCadastro.withdraw()
        self.topTPAdmin.withdraw()
        self.topTPCliente.withdraw()
        self.topPref.withdraw()
        # -self.topFiltro.withdraw()

        # LOGIN
        self.topLogin.protocol("WM_DELETE_WINDOW", self.fechar)
        self.login = TelaLogin(self.topLogin, self.bd)
        self.login.btnLogin.configure(command=self.logar)
        self.login.btnNovo.configure(command=self.abrir_cadastro)

        # CADASTRO
        self.topCadastro.protocol("WM_DELETE_WINDOW", self.fechar_cadastro)
        self.cadastro = TelaCadastro(self.topCadastro, self.bd)
        self.cadastro.btnSalvar.configure(command=self.cadastrar)

        # ADMIN
        self.topTPAdmin.protocol("WM_DELETE_WINDOW", self.fechar)
        self.admin = TelaPrincipalAdmin(self.topTPAdmin, self.bd)
        self.admin.prog.entryconfigure(0, command=self.abrir_pref)
        self.admin.prog.entryconfigure(1, command=self.fechar)
        self.admin.logout.configure(command=self.logoutAdm)

        # CLIENTE
        self.topTPCliente.protocol("WM_DELETE_WINDOW", self.fechar)
        self.cliente = TelaPrincipalCliente(self.topTPCliente, self.bd)
        self.cliente.prog.entryconfigure(0, command=self.fechar)
        # self.cliente.filtro.configure(command=self.abrir_filtro)
        self.cliente.logout.configure(command=self.logoutCliente)

        # PREFERENCIAS
        # self.topPref.protocol("WM_DELETE_WINDOW", self.fechar_pref)
        # self.pref = TelaPreferencias(self.topPref, self.bd)
        # self.pref.btnOk.configure(command=self.prefok)
        # self.pref.btn_importar.configure(command=self.importar_banco)
        # self.pref.btn_exportar.configure(command=self.exportar_banco)

        # FILTRO
        # -self.topFiltro.protocol("WM_DELETE_WINDOW", self.fechar_filtro)
        # -self.filtro = TelaFiltrar(self.topFiltro)
        # -self.filtro.btnOk.configure(command=self.filtroOk)

    def verifica_admin(self):
        quant_adms = len(self.bd.exe("SELECT * FROM admin").fetchall())
        if not quant_adms:
            if messagebox.askyesno(
                    title="Criar admin",
                    message="Nenhum admin foi encontrado, deseja criar?"):
                while True:
                    nome = askstring("Dados admin", "Nome do admin:")
                    login = askstring("Dados admin", "Login do admin:")
                    senha = askstring("Dados admin",
                                      "Senha do admin:",
                                      show='*')

                    if nome and login and senha:
                        self.bd.exe(f"""INSERT INTO admin(login, senha,nome)
                            VALUES ('{login}','{senha}','{nome}');""")
                        break
                    else:
                        if not messagebox.askokcancel(
                                title="Aviso",
                                message="Preencha todos os campos!\n"
                                "Deseja tentar novamente?"):
                            break

    def abrir_cadastro(self):
        self.topLogin.withdraw()
        self.topCadastro.deiconify()

    def fechar_cadastro(self):
        self.topCadastro.withdraw()
        self.topLogin.deiconify()

    def cadastrar(self):
        self.cadastro.cadastrar_usuario()
        self.topCadastro.withdraw()
        self.topLogin.deiconify()

    def logar(self):
        usuario = self.login.logar_usuario()
        if usuario:
            self.topLogin.withdraw()
            self.login.limpar_campos()
            if usuario[1] == "admin":
                self.topTPAdmin.deiconify()
                self.admin.renomear(usuario[0])
            else:
                self.cliente.trocar_usuario(usuario[0])
                self.topTPCliente.deiconify()

    def logoutAdm(self):
        self.topTPAdmin.withdraw()
        self.topLogin.deiconify()
        self.cliente.atualizar_registros()

    def logoutCliente(self):
        self.topTPCliente.withdraw()
        self.topLogin.deiconify()
        self.admin.servicos.atualizar_servico()
        self.admin.atendimentos.listar_atendimentos()

    def abrir_pref(self):
        self.topPref.deiconify()
        self.topPref.grab_set()

    def fechar_pref(self):
        self.topPref.grab_release()
        self.topPref.withdraw()

    def prefok(self):
        self.topPref.grab_release()
        self.topPref.withdraw()

    def abrir_filtro(self):
        self.topFiltro.deiconify()
        self.topFiltro.grab_set()

    def fechar_filtro(self):
        self.topFiltro.grab_release()
        self.topFiltro.withdraw()

    def filtroOk(self):
        self.topFiltro.grab_release()
        self.topFiltro.withdraw()

    def fechar(self):
        self.master.destroy()
        self.bd.close()
        exit()

    def importar_banco(self):
        pass

    def exportar_banco(self):
        pass


base = tk.Tk()
App(base, BANCO)
base.mainloop()
