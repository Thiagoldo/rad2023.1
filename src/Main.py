import PySimpleGUI as sg
from Contato import *
from Banco import *

class Main():
    def __init__(self) -> None:
        sg.theme('Topanga')
        self.contatos = list()
        self.connDb = Conexao()
        self.janela_principal()

    def atualizar_contatos(self) -> list:
        self.contatos = self.connDb.select_all()
        if not self.contatos:
            self.connDb.importar_txt()
            self.contatos = self.connDb.select_all()

    def janela_principal(self) -> None:
        menu = [["Buscar", ['Por Telefone', 'Aniversariantes do mês',]], ['Sistema', ['Sair']]]

        self.atualizar_contatos()

        self.header = ['Id', 'Nome', 'Telefone', 'Dt_Nascimento']
        self.tabela_contatos = sg.Table(values=self.contatos, headings=self.header, auto_size_columns=True, display_row_numbers=False,
                                        key='-TABLE-', justification='center', enable_events=True, enable_click_events=True,
                                        selected_row_colors='black on yellow')

        layout = [
            [sg.Menu(menu)],
            [sg.Text("Lista de Contato")],
            [self.tabela_contatos],
            [sg.Button(button_text='Novo'), sg.Button(button_text='Editar'), sg.Button(button_text='Excluir')]
        ]

        self.main_window = sg.Window('Contatos', layout=layout, finalize=True)

        self.c1 = Contato()
    
        while True:
            event, values = self.main_window.read()
            if event in (sg.WIN_CLOSED, 'Sair'):
                break
            elif event == 'Novo':
                self.janela_detalhe()
            elif event == '-TABLE-':
                if values[event]:
                    linha_selecionada = values[event][0]
                    self.c1.id = int(self.contatos[linha_selecionada][0])
                    self.c1.nome = self.contatos[linha_selecionada][1]
                    self.c1.telefone = self.contatos[linha_selecionada][2]
                    self.c1.dt_nasc = self.contatos[linha_selecionada][3]

            elif event == 'Editar':
                if self.c1.nome != "":
                    self.janela_detalhe(self.c1)
                else:
                    sg.popup_ok('Selecione um contato.', title="Atenção")

            elif event == 'Excluir':
                if self.c1.nome != "":
                    if self.connDb.deletar(self.c1):
                        self.atualizar_contatos()
                        self.main_window['-TABLE-'].update(values=self.contatos)
                        sg.popup_ok(self.c1.nome + " Excluído com Sucesso!", title="Sucesso")
                else:
                    sg.popup_ok('Selecione um contato.', title="Atenção")

            elif event == "Por Telefone":
                telefone: str = sg.popup_get_text( "Digite uma parte ou todo o telefone que deseja procurar", title="Buscar Contato por Telefone")
                retorno = self.connDb.select_telefone(telefone)
                try:
                    contato = retorno[0]
                    c1 = Contato()
                    c1.id = contato[0]
                    c1.nome = contato[1]
                    c1.telefone = contato[2]
                    c1.dt_nasc = contato[3]
                    self.janela_detalhe(c1)
                except:
                    sg.popup_error("Nenhum contato encontrado!", title="Erro")

            elif event == "Aniversariantes do mês":
                self.mes: str = sg.popup_get_text(
                    "Digite o mês que deseja buscar no formato 00", title="Buscar Aniversariantes do Mês")
                contatos = self.connDb.select_aniversariantes(mes=self.mes)
                self.janela_aniversariantes(contatos=contatos)

        self.main_window.close()

    def janela_aniversariantes(self, contatos: list):
        self.tabela_aniversariantes = sg.Table(values=contatos, headings=self.header, auto_size_columns=True, display_row_numbers=False,
                                               key='-TABLE-', justification='center', enable_events=True, enable_click_events=True,
                                               selected_row_colors='black on yellow')

        layout = [
            [sg.Text("Aniversariantes do Mes " + self.mes)],
            [self.tabela_aniversariantes],
            [sg.Exit(button_text='Sair')]
        ]

        self.aniversariantes_window = sg.Window(
            'Contatos', layout=layout, finalize=True)

        while True:
            event, values = self.aniversariantes_window.read()
            if event in (sg.WIN_CLOSED, 'Sair'):
                break

        self.aniversariantes_window.close()

    def janela_detalhe(self, contato: Contato = None) -> None:
        def limpar_campos():
            self.detail_window['-INPUT_NOME-'].update("")
            self.detail_window['-INPUT_TELEFONE-'].update("")
            self.detail_window['-INPUT_DT_NASC-'].update("")
            self.detail_window['-INPUT_NOME-'].set_focus(True)

        layout = [
            [sg.Text("Novo Contato")],
            [sg.Text('Nome: ', size=(15, 1)), sg.InputText(
                size=(25, 1), key='-INPUT_NOME-')],
            [sg.Text('Telefone: ', size=(15, 1)), sg.InputText(
                size=(25, 1), key='-INPUT_TELEFONE-')],
            [sg.Text('Data de Nascimento: ', size=(15, 1)), sg.InputText(key='-INPUT_DT_NASC-', size=(19, 1), readonly=True), sg.CalendarButton('Data', format="%d/%m/%Y", target='-INPUT_DT_NASC-')],
            [sg.Button(button_text='Inserir', key='-BTN_INSERIR-'),
             sg.Button(button_text='Limpar'), sg.Exit(button_text='Cancelar')]
        ]

        if contato:
            layout = [
                [sg.Text("Editar Contato")],
                [sg.Text('Nome: ', size=(15, 1)), sg.InputText(
                    size=(25, 1), key='-INPUT_NOME-', default_text=contato.nome)],
                [sg.Text('Telefone: ', size=(15, 1)), sg.InputText(
                    size=(25, 1), key='-INPUT_TELEFONE-', default_text=contato.telefone)],
                [sg.Text('Data de Nascimento: ', size=(15, 1)), sg.InputText(key='-INPUT_DT_NASC-', size=(19, 1),
                                                                             default_text=contato.dt_nasc), sg.CalendarButton('Data', format="%d/%m/%Y", target='-INPUT_DT_NASC-')],
                [sg.Button(button_text='Editar', key='-BTN_UPDATE-'),
                 sg.Button(button_text='Limpar'), sg.Exit(button_text='Cancelar')]
            ]

        self.detail_window = sg.Window('Contato', layout=layout)

        while True:
            event, values = self.detail_window.read()
            if event in (sg.WIN_CLOSED, 'Cancelar'):
                break

            elif event == "Limpar":
                limpar_campos()

            elif event == '-BTN_INSERIR-':
                novo_contato = Contato(
                    nome=values['-INPUT_NOME-'],
                    telefone=values['-INPUT_TELEFONE-'],
                    dt_nasc=values['-INPUT_DT_NASC-']
                )

                if self.connDb.inserir(novo_contato):
                    limpar_campos()
                    self.atualizar_contatos()
                    self.main_window['-TABLE-'].update(values=self.contatos)
                    sg.popup_ok(novo_contato.nome +
                                " Inserido com Sucesso!", title="Sucesso")

            elif event == '-BTN_UPDATE-':

                contato.nome = values['-INPUT_NOME-']
                contato.telefone = values['-INPUT_TELEFONE-']
                contato.dt_nasc = values['-INPUT_DT_NASC-']

                if self.connDb.atualizar(contato):
                    limpar_campos()
                    self.atualizar_contatos()
                    self.main_window['-TABLE-'].update(values=self.contatos)
                    sg.popup_ok(contato.nome +
                                " Atualizado com Sucesso!", title="Sucesso")

        self.detail_window.close()

if __name__ == '__main__':
    Main()