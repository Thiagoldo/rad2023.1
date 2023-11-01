from tkinter import messagebox
from datetime import datetime
from sqlite3 import *
from Contato import *
from os import path

class Conexao():

    def __init__(self) -> None:
        self.__db_caminho : str = path.dirname(path.realpath(__file__)) +"\contatos.db"
        self.__file_path : str = path.dirname(path.realpath(__file__)) +"\contatos.txt"

    def importar_txt(self) -> None:
        with open(self.__file_path, mode='r') as arquivo:
            for linha in arquivo.readlines():
                registro = linha.strip().split(',')   
                contato = Contato(nome=registro[0], telefone=registro[1], dt_nasc=registro[2])
                self.inserir(contato)

    def conectar(self) -> None:
        try:
            self.__conn = connect(self.__db_caminho)
            self.__cur = self.__conn.cursor()
            self.criar_tabela()
        except Exception as e:
            messagebox.showerror(title="Erro ao conectar com o banco de dados", message=e)

    def desconectar(self) -> None:
        try:
            self.__cur.close()
            self.__conn.close()
        except Exception as e:
            messagebox.showerror(title="Erro ao desconectar com o banco de dados", message=e)

    def criar_tabela(self) -> None:
        sql = '''CREATE TABLE IF NOT EXISTS tb_contatos (
        id INTEGER,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        dt_nasc NUMERIC NOT NULL,
        PRIMARY KEY (id)
        );'''
        self.__cur.execute(sql)

    def formatar_data(self, contato:Contato) -> None:
        date = datetime.strptime(contato.dt_nasc, "%d/%m/%Y")
        contato.dt_nasc = datetime.strftime(date, "%Y-%m-%d")

    def inserir(self, contato:Contato) -> bool:
        self.conectar()

        sql = '''INSERT INTO tb_contatos (nome, telefone, dt_nasc) VALUES (?, ?, ?);'''

        try:
            self.formatar_data(contato=contato)
            self.__cur.execute(sql, (contato.nome, contato.telefone, contato.dt_nasc))
            self.__conn.commit()
            return True
        except Exception as e:
            messagebox.showerror(title="Erro ao Inserir Registro no banco de dados", message=e)
        
        self.desconectar()

    def atualizar(self, contato:Contato) -> bool:
        self.conectar()

        sql = '''UPDATE tb_contatos SET nome = ? , telefone = ? , dt_nasc = ? WHERE id = ?;'''

        try:
            self.formatar_data(contato=contato)
            self.__cur.execute(sql, vars(contato))
            self.__conn.commit()
            return True
        except Exception as e:
            messagebox.showerror(title="Erro ao Inserir Registro no banco de dados", message=e)
        
        self.desconectar()
    
    def deletar(self, contato:Contato) -> bool:
        self.conectar()

        sql = f'''DELETE FROM tb_contatos WHERE id = {contato.id};'''

        try:
            self.__cur.execute(sql)
            self.__conn.commit()
            return True
        except Exception as e:
            messagebox.showerror(title="Erro ao Inserir Registro no banco de dados", message=e)
        
        self.desconectar()

    def select_all(self) -> list:
        self.conectar()

        sql = "SELECT id, nome, telefone, strftime(\"%d/%m/%Y\", tb_contatos.dt_nasc) FROM tb_contatos ORDER BY nome"
        rs = self.__cur.execute(sql)
        dados = rs.fetchall()

        self.desconectar()

        return dados
    
    def select_telefone(self, telefone:str) -> list:
        self.conectar()

        sql = "SELECT id, nome, telefone, strftime(\"%d/%m/%Y\", tb_contatos.dt_nasc) FROM tb_contatos WHERE telefone LIKE \'%" + telefone + "%\' LIMIT 1"
        rs = self.__cur.execute(sql)
        dados = rs.fetchall()
        
        self.desconectar()

        return dados
    
    def select_aniversariantes(self, mes:str) -> list:
        self.conectar()

        sql = "SELECT id, nome, telefone, strftime(\"%d\", tb_contatos.dt_nasc) as dia FROM tb_contatos WHERE strftime(\"%m\", tb_contatos.dt_nasc) = \""+ mes +"\" ORDER BY dia"
        rs = self.__cur.execute(sql)
        dados = rs.fetchall()
        
        self.desconectar()

        return dados

if __name__ == '__main__':
    pass