import re
import sqlite3


class BancoDeDados:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except Exception:
            print('Erro ao se conectar com o banco de dados')

    def exe_sql_file(self, filename):
        ###
        # Direitos para
        # nobeing -- no site -> ti-enxame.com
        ###
        command = ""
        for line in open(filename):
            if re.match(r'--', line):
                continue

            if not re.search(r'[^-;]+;', line):
                command += line
            else:
                command += line
                try:
                    self.cursor.execute(command)
                except (sqlite3.OperationalError,
                        sqlite3.ProgrammingError) as e:
                    return False

                command = ""

    def exe(self, sql: str):
        resultado = self.cursor.execute(sql)
        self.commit_db()
        return resultado

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

    def cadastrar_usuario(self, dados):
        sql = f"""
        INSERT INTO
        cliente({','.join(dados.keys())})
        VALUES('{"','".join(dados.values())}')
        """
        self.exe(sql)

    def listar_servicos(self, delimitadores={}):
        pesquisa = """SELECT id, nome,
                    tempo,tipo,descricao
                    FROM servico"""
        if delimitadores:
            pesquisa += " WHERE "
            parcelas = []
            for key, value in delimitadores.items():
                parcelas.append(f"{key} like '%{value}%'")
            pesquisa += " AND ".join(parcelas)
        consulta = self.exe(pesquisa+";")
        return consulta.fetchall()

    def listar_atendimentos(self, id):
        pesquisa = f"""SELECT id, id_cliente,
                    id_servico,data,horario, status
                    FROM atendimento
                    WHERE status='Pendente' AND id_cliente={id};"""
        consulta = self.exe(pesquisa)
        return consulta.fetchall()

    def cancelar_atendimento(self, id):
        sql = f"""
        UPDATE atendimento SET status='Cancelado'
        WHERE id={id};
        """
        self.exe(sql)

    def marcar_atendimento(self, dados):
        sql = f"""
        INSERT INTO
        atendimento({','.join(dados.keys())})
        VALUES('{"','".join(dados.values())}')
        """
        self.exe(sql)

    def confirmar_atendimento(self, id):
        sql = f"""
        UPDATE atendimento SET status='Concluído'
        WHERE id={id};
        """
        self.exe(sql)
