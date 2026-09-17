import customtkinter as ctk
from Adaptação import *
from Funções_Despesa import Gasto

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
            text = 'Inserir gastos',
            font = ('Arial', 24, 'bold')
        )

        texto = ctk.CTkLabel(
            self,
            text = 'Receita',
        )

        botao_retorno = ctk.CTkButton(
            self,
            text = 'Voltar a tela anterior',
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

        self.data_compra = ctk.CTkEntry(
            self,
            placeholder_text='Data')

        self.banco_item = ctk.CTkEntry(
            self,
            placeholder_text='Banco')

        self.submit = ctk.CTkButton(
            self,
            text='Submit',
            command=self.inserir_gasto_front
        )

        titulo.place(x=50, y=50)
        texto.place(x=50, y=100)
        self.nome_item.place(x=50, y=150)
        self.categoria_item.place(x=50, y=200)
        self.valor_item.place(x=50, y=250)
        self.forma_de_pagamento.place(x=50, y=300)
        self.banco_item.place(x=50, y=350)
        self.data_compra.place(x=50, y=400)
        self.submit.place(x=300, y=400)

        botao_retorno.place(x=600, y=400)

    def inserir_gasto_front(self):
        novo_gasto = Gasto(
            self.nome_item.get(),
            self.valor_item.get(),
            self.forma_de_pagamento.get(),
            self.categoria_item.get(),
            self.data_compra.get(),
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



teste = App()

teste.mainloop()
print(f'Encerrando...')