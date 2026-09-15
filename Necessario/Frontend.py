import customtkinter as ctk
from Adaptação import *

# ================== Configurações de tela =================

banco_de_dados = pd.read_excel('Financeiro_novo.xlsx')
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

        self.switch = ctk.CTkSwitch(
            self,
            text = 'Modo Escuro',
            command = self.trocar_modo
        )


        self.titulo_pagina1.pack(pady = 20)
        self.verificar_gastos.place(x = 50, y = 100)
        self.definir_banco.place(x = 50, y = 150)
        self.tabela_meses.place(x = 50, y = 200)
        self.graficos.place(x = 50, y = 250)

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

        ver_gastos(banco_de_dados)

    def acessar_gastos(self):

        entrada = ctk.CTkEntry(
            self,
            placeholder_text="Digite o nome do item",
            command = self.informar_planilha
        )

    def informar_planilha(self):

        valor = self.entrada.get()
        buscar(banco_de_dados, item = valor)




teste = App()

teste.mainloop()
print(f'Encerrando...')