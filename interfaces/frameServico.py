import tkinter as tk
import tkinter.ttk as ttk
from .funcs import *
from tkinter import messagebox


class ServicoFrame(tk.Frame):
    def __init__(self, master, banco):
        tk.Frame.__init__(self, master)
        self.bd = banco
        self.master = master
        self.container1 = tk.Frame(self.master, bd=5)

        self.container2 = tk.Frame(self.master, bd=5)
        self.container1.pack(fill='both',
                             side="left",
                             expand=1,
                             padx=3,
                             pady=3)
        self.container2.pack(fill='both',
                             side="left",
                             expand=1,
                             padx=3,
                             pady=3)

        # INSERÇÃO E PESQUISA
        self.container3 = tk.Frame(self.container1)
        self.container3.pack(fill='x', expand=1, padx=3, pady=3)

        tk.Label(self.container3, text="ID:").grid(row=0,
                                                   column=0,
                                                   sticky="e",
                                                   padx=2,
                                                   pady=2)
        self.id = tk.Entry(self.container3, state="readonly")
        self.id.grid(row=0, column=1, sticky="w", padx=2, pady=2)

        tk.Label(self.container3, text="NOME:").grid(row=1,
                                                     column=0,
                                                     sticky="e",
                                                     padx=2,
                                                     pady=2)
        self.nome = tk.Entry(self.container3)
        self.nome.grid(row=1, column=1, sticky="w", padx=2, pady=2)

        tk.Label(self.container3, text="PREÇO:").grid(row=2,
                                                      column=0,
                                                      sticky="e",
                                                      padx=2,
                                                      pady=2)
        self.preco = tk.Entry(self.container3, width=19, validate="key")
        self.preco.configure(
            validatecommand=(self.preco.register(valida_valor), '%P'))
        self.preco.grid(row=2, column=1, sticky="w", padx=2, pady=2)

        tk.Label(self.container3, text="TEMPO:").grid(row=3,
                                                      column=0,
                                                      sticky="e",
                                                      padx=2,
                                                      pady=2)
        self.tempo = ttk.Spinbox(
            self.container3, from_=1, to=60, state="readonly", width=3)
        self.tempo.grid(row=3, column=1, sticky="w", padx=2, pady=2)

        tk.Label(self.container3, text="TIPO:").grid(row=4,
                                                     column=0,
                                                     sticky="e",
                                                     padx=2,
                                                     pady=2)

        self.tipo = ttk.Combobox(self.container3, values=[
                                 'Manicure', 'Pedicure'], state="readonly", width=10)
        self.tipo.grid(row=4, column=1, sticky="w", padx=2, pady=2)

        tk.Label(self.container3, text="DESCRIÇÃO:").grid(row=5,
                                                          column=0,
                                                          padx=2,
                                                          pady=2)
        self.descricao = tk.Text(self.container3, width=31, height=4)
        self.descricao.grid(row=6, column=0,
                            padx=2, pady=2, columnspan=2)

        self.container4 = tk.Frame(self.container1)
        self.container4.pack(fill='both', expand=1, padx=3, pady=3)
        self.btn_inserir = tk.Button(self.container4,
                                     text="INSERIR",
                                     padx=5,
                                     pady=10,
                                     command=self.inserir_servico)
        self.btn_inserir.pack(side="left", expand=1, fill="x")

        self.btn_pesquisar = tk.Button(self.container4,
                                       text="PESQUISAR",
                                       padx=5,
                                       pady=10,
                                       command=self.pesquisar_servico)
        self.btn_pesquisar.pack(side="left", expand=1, fill="x")

        # VISUALIZAR REGISTROS
        self.container5 = tk.Frame(self.container2)
        self.container5.pack(fill='both', expand=1)

        barraV = tk.Scrollbar(self.container5, orient="vertical")
        barraH = tk.Scrollbar(self.container5, orient="horizontal")
        self.lista_servicos = tk.Listbox(self.container5,
                                         width=30,
                                         height=11,
                                         yscrollcommand=barraV.set,
                                         xscrollcommand=barraH.set,
                                         selectmode="SINGLE")
        barraV.config(command=self.lista_servicos.yview)
        barraV.pack(side="right", fill='y')

        self.container6 = tk.Frame(self.container2)
        self.container6.pack(side="bottom", fill='both', expand=1)

        barraH.config(command=self.lista_servicos.xview)
        barraH.pack(side="bottom", fill='x')

        self.lista_servicos.pack(fill='both', expand=1)
        self.btn_deletar = tk.Button(
            self.container6,
            text="DELETAR",
            padx=5,
            pady=10,
            command=self.deletar_servico
        )
        self.btn_deletar.pack(side="left", expand=1, fill="x")
        self.btn_editar = tk.Button(
            self.container6,
            text="EDITAR",
            padx=5,
            pady=10,
            command=self.editar_servico
        )
        self.btn_editar.pack(side="left", expand=1, fill="x")
        self.atualizar_servico()

    def valida_dados(self):
        self.obrigatorios = [
            self.nome.get().strip(),
            str(self.preco.get().strip()),
            str(self.tempo.get().strip()),
            self.tipo.get().strip(),
            self.descricao.get("1.0", "end-1c").strip()
        ]
        if all([bool(x)for x in self.obrigatorios]):
            return True
        else:
            messagebox.showinfo(
                "Aviso", f"Preencha todos os campos obrigatórios (nome, preço, tempo, tipo, descrição)")
            return False

    def limpar_campos(self):
        self.id["state"] = "normal"
        self.id.delete(0, tk.END)
        self.id["state"] = "readonly"

        self.nome.delete(0, tk.END)
        self.preco.delete(0, tk.END)
        self.tempo.set('')
        self.tipo.set('')
        self.descricao.delete("1.0", "end-1c")

    def get_dados(self):
        return {
            "id": self.id.get().strip(),
            "nome": self.nome.get().strip(),
            "preco": str(self.preco.get()).strip(),
            "tempo": str(self.tempo.get()).strip(),
            "tipo": self.tipo.get().strip(),
            "descricao": self.descricao.get('1.0', 'end-1c').strip()
        }

    def consulta_dados(self, delimitadores={}):
        pesquisa = """SELECT id, nome,preco,
                    tempo,tipo,descricao
                    FROM servico"""
        if delimitadores:
            pesquisa += " WHERE "
            parcelas = []
            for key, value in delimitadores.items():
                parcelas.append(f"{key} like '%{value}%'")
            pesquisa += " AND ".join(parcelas)
        consulta = self.bd.exe(pesquisa+";")
        return consulta.fetchall()

    def update(self, novos_dados):
        comando = f"""
        UPDATE servico SET 
        nome='{novos_dados['nome']}',
        preco='{novos_dados['preco']}',
        tempo='{novos_dados['tempo']}',
        tipo='{novos_dados['tipo']}',
        descricao='{novos_dados['descricao']}'
        WHERE id={novos_dados['id']};"""
        self.bd.exe(comando)

    def insert(self, dados):
        sql = f"""
        INSERT INTO
        servico({','.join(dados.keys())})
        VALUES('{"','".join(dados.values())}')
        """
        self.bd.exe(sql)

    def delete(self, id):
        sql = f"DELETE FROM servico WHERE id={id};"
        self.bd.exe(sql)

    def inserir_servico(self):
        if self.valida_dados():
            dados = self.get_dados()
            del dados['id']
            self.insert(dados)
            messagebox.showinfo(title="Sucesso", message="Registro incluído!")
            self.limpar_campos()
            self.atualizar_servico()

    def pesquisar_servico(self):
        dados = self.get_dados()
        resultado = self.consulta_dados(dados)
        self.listar_servicos(resultado)
        self.limpar_campos()

    def editar_servico(self):
        index = self.lista_servicos.curselection()
        if index:
            dados = self.lista_servicos.get(index, index)[0].split("|")
            dados = [x.strip() for x in dados]

            self.limpar_campos()

            self.id["state"] = "normal"
            self.id.insert(0, dados[0])
            self.id["state"] = "readonly"

            self.nome.insert(0, dados[1])
            self.preco.insert(0, dados[2])
            self.tempo.set(dados[3])
            self.tipo.set(dados[4])
            self.descricao.insert('1.0', dados[5])

            self.btn_inserir['text'] = "SALVAR"
            self.btn_inserir['command'] = self.salvar
            self.btn_pesquisar['text'] = "CANCELAR"
            self.btn_pesquisar['command'] = self.cancelar
            self.btn_deletar.configure(state="disabled")
            self.btn_editar.configure(state="disabled")

            self.lista_servicos.select_clear(0, tk.END)
        else:
            messagebox.showinfo(title="Informação",
                                message="Nenhum registro foi selecionado")

    def deletar_servico(self):
        index = self.lista_servicos.curselection()
        if index:
            id = self.lista_servicos.get(index)[0].split("|")[0].strip()
            self.delete(id)

            self.lista_servicos.delete(index)
            self.lista_servicos.select_clear(0, tk.END)
            self.lista_servicos.select_set(0)
        else:
            messagebox.showinfo(title="Informação",
                                message="Nenhum registro foi selecionado")

    def cancelar(self):
        self.btn_deletar.configure(state="normal")
        self.btn_editar.configure(state="normal")
        self.btn_inserir['text'] = "INSERIR"
        self.btn_inserir['command'] = self.inserir_servico
        self.btn_pesquisar['text'] = "PESQUISAR"
        self.btn_pesquisar['command'] = self.pesquisar_servico
        self.editlogin = ''
        self.editcpf = ''
        self.limpar_campos()

    def salvar(self):
        if self.valida_dados():
            dados = self.get_dados()
            self.update(dados)
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
            self.cancelar()
            self.atualizar_servico()

    def atualizar_servico(self):
        resultado = self.consulta_dados()
        self.listar_servicos(resultado)

    def listar_servicos(self, servicos):
        self.lista_servicos.delete(0, tk.END)
        for servico in servicos:
            servico = [str(x) for x in servico]
            self.lista_servicos.insert(tk.END, " | ".join(servico))
        self.lista_servicos.select_clear(0, tk.END)
