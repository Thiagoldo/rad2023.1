class Contato:

    def __init__(self, id:int = None, nome:str = "", telefone:str = "", dt_nasc:str = "") -> None:
        self.__id = id
        self.__nome = nome
        self.__telefone = telefone
        self.__dt_nasc = dt_nasc
    
    @property
    def id(self) -> int:
        return self.__id
    @property
    def nome(self) -> str:
        return self.__nome
    @property
    def telefone(self) -> str:
        return self.__telefone
    @property
    def dt_nasc(self) -> str:
        return self.__dt_nasc
    
    @id.setter
    def id(self, id:int) -> None:
        self.__id = id
    @nome.setter
    def nome(self, nome:str) -> None:
        self.__nome = nome
    @telefone.setter
    def telefone(self, telefone:str) -> None:
        self.__telefone = telefone
    @dt_nasc.setter
    def dt_nasc(self, dt_nasc:str) -> None:
        self.__dt_nasc = dt_nasc
        

if __name__ == '__main__':
    pass