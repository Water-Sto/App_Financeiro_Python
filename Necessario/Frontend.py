import customtkinter as ctk
from Adaptação import *
from Funções_Despesa import Gasto
from Funções_de_validação import *
from time import sleep

# ================== Configurações de tela =================

banco_de_dados_despesa = pd.read_excel('Despesa.xlsx')
banco_de_dados_receita = pd.read_excel('Receita.xlsx')
modo_escuro = False

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme("blue")

# ================== Configurações da janela ===============

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Controle de testes")
        self.geometry("800x500")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.tela_gastos = TelaGastos(self.container, self)
        self.tela_inicial = TelaInicial(self.container, self)

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
        )

        self.graficos = ctk.CTkButton(
            self,
            text="Gráficos",
        )

        self.switch = ctk.CTkSwitch(
            self,
            text='Modo Escuro',
            command=self.trocar_modo
        )

        self.entrada = ctk.CTkEntry(
            self,
            placeholder_text='Digite o valor')

        self.titulo_pagina1.pack(pady=20)
        verificar_gastos.place(x=50, y=100)
        self.definir_banco.place(x=50, y=150)
        self.tabela_meses.place(x=50, y=200)
        self.graficos.place(x=50, y=250)
        self.entrada.place(x=200, y=100)

    def mostrar_gastos(self):
        valor = self.entrada.get()
        print(valor)

    def informar_planilha(self):
        valor = self.entrada.get()
        buscar(banco_de_dados_despesa, item=valor)

    def menu_lateral(self):
        pass

    def trocar_modo(self):

        global modo_escuro

        if modo_escuro:
            ctk.set_appearance_mode('Light')
            modo_escuro = False
            return

        if not modo_escuro:
            ctk.set_appearance_mode('Dark')
            modo_escuro = True
            return

class TelaGastos(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

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
        self.submit.place(x=575, y=400)

        botao_retorno.place(x=75, y=400)

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

            texto = ctk.CTkLabel(
                self,
                text=base_data,
                text_color='#FF5733',
                font=('Arial', 24, 'bold')
                )

            texto.place(x=200, y=20)

            self.after(3000, lambda: texto.configure(text=''))

        elif base_valor_item in lista_erros_valor:

            texto = ctk.CTkLabel(
                self,
                text=str(base_valor_item),
                text_color='#FF5733',
                font=('Arial', 24, 'bold')
            )

            texto.place(x=200, y=20)

            self.after(3000, lambda: texto.configure(text=''))

        elif self.nome_item.get() == '':

            texto = ctk.CTkLabel(
                self,
                text='Você deve definir o nome do item',
                text_color='#FF5733',
                font=('Arial', 24, 'bold')
            )

            texto.place(x=200, y=20)

            self.after(3000, lambda: texto.configure(text=''))

        elif self.forma_de_pagamento.get() == '':
            texto = ctk.CTkLabel(
                self,
                text='Você deve definir uma forma de pagamento',
                text_color='#FF5733',
                font=('Arial', 24, 'bold')
            )

            texto.place(x=200, y=20)

            self.after(3000, lambda: texto.configure(text=''))

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

            texto = ctk.CTkLabel(
                self,
                text='Informações atualizadas com sucesso!',
                text_color='#2ECC71',
                font=('Arial', 24, 'bold')
            )

            texto.place(x=200, y=20)
            self.after(5000, lambda: texto.configure(text=''))

            self.limpar_campos()

    def limpar_campos(self):
        self.nome_item.delete(0, 'end')
        self.valor_item.delete(0, 'end')
        self.forma_de_pagamento.delete(0, 'end')
        self.categoria_item.delete(0, 'end')
        self.banco_item.delete(0, 'end')
        self.data_compra.delete(0, 'end')





teste = App()

teste.mainloop()
print(f'Encerrando...')