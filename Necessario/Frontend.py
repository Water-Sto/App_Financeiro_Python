import customtkinter as ctk
from Adaptação import *

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

        self.verificar_gastos = ctk.CTkButton(
            self,
            text="Gastos",
            command = self.mostrar_gastos
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

        self.titulo_pagina1 = ctk.CTkLabel(
            self,
            text = 'Gestor Financeiro',
            font = ('Arial', 24, 'bold')
        )

        self.submit = ctk.CTkButton(
            self,
            text = 'Submit',
            command = self.mostrar_gastos
        )

        self.switch = ctk.CTkSwitch(
            self,
            text = 'Modo Escuro',
            command = self.trocar_modo
        )

        self.entrada = ctk.CTkEntry(
            self,
            placeholder_text='Digite o valor')


        self.titulo_pagina1.pack(pady = 20)
        self.verificar_gastos.place(x = 50, y = 100)
        self.definir_banco.place(x = 50, y = 150)
        self.tabela_meses.place(x = 50, y = 200)
        self.graficos.place(x = 50, y = 250)
        self.entrada.place(x = 200, y = 100)
        self.submit.place(x = 500, y = 300)

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

    def mostrar_gastos(self):

        valor = self.entrada.get()
        print(valor)

    def informar_planilha(self):

        valor = self.entrada.get()
        buscar(banco_de_dados_despesa, item = valor)

class TelaInicial(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

        titulo = ctk.CTkLabel(
            self,
            text = 'Inserir gastos',
            font = ('Arial', 24, 'bold')
        )
        titulo.pack(pady = 30)

        botao = ctk.CTkButton(
            self,
            text = 'Ver gastos',
            command = lambda: self.app.verificar_gastos(self.app.tela_gastos)
        )

        botao.pack(pady = 20)

class TelaGastos(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text = 'Inserir gastos',
            font = ('Arial', 24, 'bold')
        )
        titulo.pack(pady = 30)

        texto = ctk.CTkLabel(
            self,
            text = 'Receita',
        )

        texto.pack()


teste = App()

teste.mainloop()
print(f'Encerrando...')