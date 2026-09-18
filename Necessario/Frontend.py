import customtkinter as ctk
from Adaptação import *
from Funções_Despesa import Gasto

# ================== Configurações de tela =================

banco_de_dados_despesa = pd.read_excel('Despesa.xlsx')
banco_de_dados_receita = pd.read_excel('Receita.xlsx')
modo_escuro = False

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme("blue")

# ================== Cores de texto ========================

VERMELHO = '#FF5733'
VERDE = '#2ECC71'

# ================== Posições de mensagem ==================

erro_x = 150
erro_y = 20
posicao_botao_voltar = (75, 400)
posicao_botao_submit = (575, 400)

# ================== Configurações da janela ===============

def trocar_modo():
    global modo_escuro

    if modo_escuro:
        ctk.set_appearance_mode('Light')
        modo_escuro = False
        return

    if not modo_escuro:
        ctk.set_appearance_mode('Dark')
        modo_escuro = True
        return

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Finwesen")
        self.geometry("800x500")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.tela_gastos = TelaGastos(self.container, self)
        self.tela_inicial = TelaInicial(self.container, self)
        self.tela_bancos = TelaBancos(self.container, self)

        self.tela_gastos.grid(
            row=0,
            column=0,
            sticky="nsew"
            )

        self.tela_inicial.grid(
            row=0,
            column=0,
            sticky="nsew"
            )

        self.tela_bancos.grid(
            row=0,
            column=0,
            sticky="nsew"
        )


        self.mostrar_tela(self.tela_inicial)

    def mostrar_tela(self, tela):

        tela.tkraise()

class TelaInicial(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

        self.titulo_pagina1 = ctk.CTkLabel(
            self,
            text='Gestor Financeiro',
            font=('Arial', 24, 'bold')
        )

        verificar_gastos = ctk.CTkButton(
            self,
            text="Gastos",
            command=lambda: self.app.mostrar_tela(self.app.tela_gastos)
        )

        self.definir_banco = ctk.CTkButton(
            self,
            text="Receitas",
        )

        self.tabela_meses = ctk.CTkButton(
            self,
            text="Bancos",
            command=lambda: self.app.mostrar_tela(self.app.tela_bancos)
        )

        self.graficos = ctk.CTkButton(
            self,
            text="Gráficos",
        )

        self.switch = ctk.CTkSwitch(
            self,
            text='Modo Escuro',
            command=trocar_modo
        )

        self.titulo_pagina1.pack(pady=20)
        verificar_gastos.place(x=50, y=100)
        self.definir_banco.place(x=50, y=150)
        self.tabela_meses.place(x=50, y=200)
        self.graficos.place(x=50, y=250)
        self.switch.place(x=50, y = 50)

    def informar_planilha(self):
        pass

    def menu_lateral(self):
        pass

class TelaGastos(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

        self.texto = ctk.CTkLabel(
                self,
                text='',
                text_color='#FF5733',
                font=('Arial', 24, 'bold')
                )

        titulo = ctk.CTkLabel(
            self,
            text = 'Preencha os campos para inserir um novo gasto',
            font = ('Arial', 24, 'bold')
        )

        botao_retorno = ctk.CTkButton(
            self,
            text = 'Voltar',
            command =lambda: self.app.mostrar_tela(self.app.tela_inicial)
        )

        self.submit = ctk.CTkButton(
            self,
            text='Submit',
            command=self.inserir_gasto_front
        )

        self.nome_item = ctk.CTkEntry(
            self,
            placeholder_text='Item')

        self.categoria_item = ctk.CTkEntry(
            self,
            placeholder_text='Categoria')

        self.valor_item = ctk.CTkEntry(
            self,
            placeholder_text='Valor')

        self.forma_de_pagamento = ctk.CTkEntry(
            self,
            placeholder_text='Forma de pagamento')

        self.banco_item = ctk.CTkEntry(
            self,
            placeholder_text='Banco')

        self.data_compra = ctk.CTkEntry(
            self,
            placeholder_text='Data')

        self.submit = ctk.CTkButton(
            self,
            text='Submit',
            command=self.inserir_gasto_front
        )

        titulo.place(x=120, y=50)
        self.nome_item.place(x=75, y=150)
        self.categoria_item.place(x=325, y=150)
        self.valor_item.place(x=575, y=150)
        self.forma_de_pagamento.place(x=75, y=200)
        self.banco_item.place(x=325, y=200)
        self.data_compra.place(x=575, y=200)
        self.submit.place(x = posicao_botao_submit[0], y = posicao_botao_submit[1])

        botao_retorno.place(x = posicao_botao_voltar[0], y = posicao_botao_voltar[1])

    def inserir_gasto_front(self):

        base_valor_item = validar_valor_adaptado(self.valor_item.get())
        base_data = validar_data_adaptado(self.data_compra.get())

        lista_erros_data = [f'O Formato de data foi definido de maneira incorreta, corrija e tente novamente.',
                       f'O Dia foi definido de maneira incorreta, corrija e tente novamente.',
                       f'O mês foi definido de maneira incorreta, corrija e tente novamente.',
                       f'Formato de data incompreensivel, tente novamente.',
                        ]

        lista_erros_valor = [f'Erro, o valor deve ser um numero valido.',
                            f'Erro, algum caractere não foi reconhecido.',
                             f'Erro, você deve digitar um valor para o item.'
                             ]

        if base_data in lista_erros_data:

            self.mostrar_mensagem(base_data, VERMELHO, 3000)
            self.apagar_mensagem()

        elif base_valor_item in lista_erros_valor:

            self.mostrar_mensagem(str(base_valor_item), VERMELHO, 3000)

        elif self.nome_item.get() == '':

            self.mostrar_mensagem('Você deve definir o nome do item', VERMELHO, 3000)

        elif self.forma_de_pagamento.get() == '':

            self.mostrar_mensagem('Você deve definir uma forma de pagamento', VERMELHO, 3000)

        else:

            base_valor_item = float(base_valor_item)

            novo_gasto = Gasto(
                self.nome_item.get(),
                base_valor_item,
                self.forma_de_pagamento.get(),
                self.categoria_item.get(),
                base_data,
                self.banco_item.get()
            )

            inserir_gasto_adaptado(banco_de_dados_despesa,
                                   novo_gasto.nome,
                                   novo_gasto.valor,
                                   novo_gasto.forma_pagamento,
                                   novo_gasto.categoria,
                                   novo_gasto.data,
                                   novo_gasto.banco
                                   )

            self.mostrar_mensagem('Informações atualizadas com sucesso!', VERDE, 5000)

            self.limpar_campos()

    def limpar_campos(self):
        self.nome_item.delete(0, 'end')
        self.valor_item.delete(0, 'end')
        self.forma_de_pagamento.delete(0, 'end')
        self.categoria_item.delete(0, 'end')
        self.banco_item.delete(0, 'end')
        self.data_compra.delete(0, 'end')

    def apagar_mensagem(self):
        self.texto.configure(text='')

    def mostrar_mensagem(self, mensagem, cor, tempo_em_tela:int):

        self.texto.configure(text=mensagem,
                             text_color=cor)

        self.texto.place(x = erro_x, y = erro_y)
        self.after(tempo_em_tela, self.apagar_mensagem)

class TelaBancos(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

        self.posix = 75
        self.posiy = 50
        self.botoes_bancos = list()
        self.botoes_excluir = list()

        self.texto = ctk.CTkLabel(
            self,
            text='',
            text_color=VERMELHO,
            font=('Arial', 24, 'bold')
        )

        botao_retorno = ctk.CTkButton(
            self,
            text='Voltar',
            command=lambda: self.app.mostrar_tela(self.app.tela_inicial)
        )

        self.novo_banco = ctk.CTkEntry(
            self,
            placeholder_text='Novo banco'
        )

        self.botao_submit = ctk.CTkButton(
            self,
            text='Submit',
            command=self.inserir_novo_banco
        )

        self.lista_bancos = ler_quantidade_bancos()

        for banco in self.lista_bancos:
            self.botao = ctk.CTkButton(
                self,
                text=f'{banco}',
                width=140,
                anchor ='center',
                command=lambda banco=banco: self.tornar_banco_principal(banco)
            )



            self.botao_excluir = ctk.CTkButton(
                self,
                text="X",
                width=10,
                height=20,
                command=lambda banco=banco: self.remover_banco(banco)
            )

            self.botao.place(x = self.posix, y = self.posiy)
            self.botao_excluir.place(x=self.posix + 120, y=self.posiy)

            if self.posix <= 575:
                self.posix += 250

            if self.posix > 575:
                self.posix = 75
                self.posiy += 80

            self.botoes_excluir.append(self.botao_excluir)
            self.botoes_bancos.append(self.botao)

        self.posix -= 250

        self.atualizar_bancos()



        botao_retorno.place(x = posicao_botao_voltar[0], y = posicao_botao_voltar[1])
        self.novo_banco.place(x = posicao_botao_submit[0], y = 350)
        self.botao_submit.place(x = posicao_botao_submit[0], y = posicao_botao_submit[1])


    def atualizar_bancos(self):


        for botao in self.botoes_excluir:
            botao.destroy()

        for botao in self.botoes_bancos:
            botao.destroy()

        self.botoes_bancos.clear()
        self.botoes_excluir.clear()

        self.posix = 75
        self.posiy = 50


        for banco in self.lista_bancos:
            self.botao = ctk.CTkButton(
                self,
                text=f'{banco}',
                width=140,
                anchor ='center',
                command=lambda banco=banco: self.tornar_banco_principal(banco)
            )


            self.botao_excluir = ctk.CTkButton(
                self,
                text="X",
                width=10,
                height=20,
                command=lambda banco=banco: self.remover_banco(banco)
            )

            self.botao.place(x=self.posix, y=self.posiy)
            self.botao_excluir.place(x=self.posix + 120, y=self.posiy)

            if self.posix <= 575:
                self.posix += 250

            if self.posix > 575:
                self.posix = 75
                self.posiy += 80

            self.botoes_excluir.append(self.botao_excluir)
            self.botoes_bancos.append(self.botao)

        self.posix -= 250

    def tornar_banco_principal(self, banco):

        self.mostrar_mensagem(f'Seu banco principal foi definido como: {banco}', VERDE, 3000)
        definir_banco_principal(banco)

    def remover_banco(self, banco):

        banco = banco.capitalize()
        self.mostrar_mensagem(f'O banco {banco} foi removido com sucesso!', VERDE, 3000)
        apagar_banco(banco)
        print(self.lista_bancos)
        print(banco)
        self.lista_bancos.remove(banco)
        self.atualizar_bancos()

    def inserir_novo_banco(self):

        if self.novo_banco.get() != '':
            adicionar_banco(self.novo_banco.get().capitalize())
            self.botao = ctk.CTkButton(
                self,
                text=self.novo_banco.get().capitalize(),
                command=lambda banco=self.novo_banco.get(): self.tornar_banco_principal(banco)
                )

            self.botao_excluir = ctk.CTkButton(
                self,
                text="x",
                width=10,
                height=20,
                command=lambda banco=self.novo_banco.get(): self.remover_banco(banco)
                )

            self.botoes_excluir.append(self.botao_excluir)
            self.botoes_bancos.append(self.botao)

            if self.posix <= 575:
                self.posix += 250

            if self.posix > 575:
                self.posix = 75
                self.posiy += 80

            self.botao.place(x = self.posix, y = self.posiy)
            self.botao_excluir.place(x = self.posix + 120, y = self.posiy)
            self.lista_bancos.append(self.novo_banco.get().capitalize())
            self.limpar_campos()

        else:
            self.mostrar_mensagem('Você precisa inserir o nome do banco adicionado', VERMELHO, 3000)

    def apagar_mensagem(self):
        self.texto.configure(text='')

    def mostrar_mensagem(self, mensagem, cor, tempo_em_tela:int):

        self.texto.configure(text=mensagem,
                             text_color=cor)

        self.texto.place(x = erro_x, y = erro_y)
        self.after(tempo_em_tela, self.apagar_mensagem)

    def limpar_campos(self):
        self.novo_banco.delete(0, 'end')

teste = App()

teste.mainloop()
print(f'Encerrando...')