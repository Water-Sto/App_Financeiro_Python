import pandas as pd
from Funções_de_validação import *
from Funções_txt import *
from Cores import cor_texto
from time import sleep
from datetime import date
import os

if '__init__' == '__main__':
    from Backend import planilha_despesa

class Gasto:
    def __init__(self, nome, valor, forma_pagamento, categoria, data, banco):
        self.nome = nome
        self.valor = valor
        self.forma_pagamento = forma_pagamento
        self.categoria = categoria
        self.data = data
        self.banco = banco

    def descrever(self):
        print(f'{self.nome} | {self.valor} | {self.forma_pagamento} | {self.categoria} | {self.data} | {self.banco}')
        return self.nome, self.valor, self.forma_pagamento, self.categoria, self.data, self.banco

lista_textos = ['Índice', 'Item', 'Valor', 'Tipo de pagamento', 'Categoria', 'Data', 'Banco']

def inserir_gasto(planilha: pd.DataFrame, banco_padrao='None'):
    """Função visando inserir dados linha a linha na planilha. Recebe uma planilha de Excel como parâmetro e
    uma confirmação de "banco padrão". Enquanto o mesmo for "None", o usuário terá que escrever qual banco será
    utilizado. Utiliza a biblioteca "datetime" para puxar a data atual caso o usuário não informe a data da transação."""

    possibilidades_pagamento = ['Débito', 'Crédito', 'Pix', 'Saldo']

    novo_gasto = Gasto(input('Digite o nome do produto/serviço: ').title(),
                        validar_valor('Digite um valor para o pagamento: '),
                        input('Digite o tipo do pagamento: ').title(),
                        input('Digite a categoria do item: ').title(),
                        validar_data('Digite a data do pagamento (XX/XX/XXXX): '),
                        input('Digite o banco responsável pela transação: ').title())

    if novo_gasto.banco == '' and banco_padrao == 'None' or novo_gasto.forma_pagamento not in possibilidades_pagamento:
        novo_gasto.banco = 'None'

    if novo_gasto.banco == '' and banco_padrao != 'None':
        novo_gasto.banco = banco_padrao

    if novo_gasto.data == '':
        novo_gasto.data = date.today().strftime('%d/%m/%Y')

    adicionado = pd.DataFrame(
        [{'Item': novo_gasto.nome, 'Valor': novo_gasto.valor, 'Tipo_de_pagamento': novo_gasto.forma_pagamento,
            'Categoria': novo_gasto.categoria, 'Data': novo_gasto.data, 'Banco': novo_gasto.banco}])

    planilha = pd.concat([planilha, adicionado], ignore_index=True)
    arquivo_temp = 'Despesa_temp.xlsx'
    planilha.to_excel(arquivo_temp, index=False)
    os.replace(arquivo_temp, planilha_despesa)
    novo_gasto.descrever()
    gerenciamento_backups_txt('Despesa', novo_gasto.categoria, novo_gasto.valor, novo_gasto.forma_pagamento, novo_gasto.data, novo_gasto.banco, item = novo_gasto.nome)
    return

def acessar_planilha_despesa(planilha: pd.DataFrame, apagar = False, item ='None'):

    """Função visando filtrar o acesso à planilha com base em informações como o tipo do item ou a categoria
    do mesmo. Também é a função utilizada para apagar itens do Excel com base no índice das suas posições"""

    global lista_textos

    quantidade_produtos = 0
    indice = 0
    valor_total = 0

    if item == 'None':
        busca = input(f'Digite o nome do item ou sua categoria: ')

    else:
        busca = item

    for produto in planilha['Item']:
        if produto == busca.title():
            quantidade_produtos += 1

    if quantidade_produtos == 0:
        for categoria in planilha['Categoria']:
            if categoria == busca.title():
                quantidade_produtos += 1

    if quantidade_produtos > 0:
        print(f'Foram encontradas {quantidade_produtos} correspondencias para este produto/serviço: \n')
        print(f'{lista_textos[0]:>5} || {lista_textos[1]:^30} || {lista_textos[2]:^10} || {lista_textos[3]:^15} || {lista_textos[4]:^12} || {lista_textos[5]:^11} || {lista_textos[6]}')
        print('-'*115)
        while indice < len(planilha['Item']):
            if busca.title() == planilha['Item'][indice] or busca.title() == planilha['Categoria'][indice]:
                print(f'{indice:>6} || {planilha["Item"][indice]:^30} || R${planilha["Valor"][indice]:>8} || {planilha["Tipo_de_pagamento"][indice]:^17} || {planilha["Categoria"][indice]:^12} || {planilha["Data"][indice]:^11} || {planilha["Banco"][indice]}')
                quantidade_produtos += 1
                valor_total += planilha['Valor'][indice]

            indice += 1

        print('-'*115)

        print(f'{cor_texto("azul")}Valor total gasto em "{busca}" é: R${valor_total:.2f}. {cor_texto("stop")}')

    if apagar:

        if quantidade_produtos == 0:
            print(f'{cor_texto("vermelho")}Nenhum item correspondente a sua busca foi encontrado, tente novamente.{cor_texto("stop")}')
            sleep(0.5)
            return

        while True:
            linha_apagada = validar_inteiro('Digite o índice da linha que deseja apagar (tecle "-1" para cancelar a ação): ', apagar = True)
            if linha_apagada == -1:
                print(f'{cor_texto("azul")}Ação cancelada, voltando ao painel de controle...{cor_texto("stop")}')
                sleep(0.5)
                break

            if linha_apagada > len(planilha['Item']) or linha_apagada < 0:
                print(f'{cor_texto("vermelho")}Linha não encontrada, tente novamente.{cor_texto("stop")}')
                break


            print(f'{cor_texto("verde")}Item "{planilha["Item"][linha_apagada]}", correspondente ao valor R${planilha["Valor"][linha_apagada]} no dia {planilha["Data"][linha_apagada]} deletado com sucesso!{cor_texto("stop")}')
            planilha = planilha.drop(index = linha_apagada)
            arquivo_temp = 'Despesa_temp.xlsx'
            planilha.to_excel(arquivo_temp, index=False)
            try:
                os.replace(arquivo_temp, 'Financeiro_novo.xlsx')

            except PermissionError:
                print(f'{cor_texto("vermelho")}Tentativa de transferência de dados do backup para a planilha principal falhou, feche o programa e tente novamente.{cor_texto("stop")}')
                break

            apagar_linha_txt('Despesa', linha_apagada)
            break

def ver_gastos(planilha: pd.DataFrame):

    global lista_textos
    gasto_total = 0

    print(
        f'{lista_textos[0]:>5} || {lista_textos[1]:^30} || {lista_textos[2]:^10} || {lista_textos[3]:^15} || {lista_textos[4]:^12} || {lista_textos[5]:^11} || {lista_textos[6]}')
    print('-' * 115)

    for indice, produto in enumerate(planilha['Item']):
        print(f'{indice+1:>6} || {planilha["Item"][indice]:^30} || R${planilha["Valor"][indice]:>8} || {planilha["Tipo_de_pagamento"][indice]:^17} || {planilha["Categoria"][indice]:^12} || {planilha["Data"][indice]:^11} || {planilha["Banco"][indice]}')
        gasto_total += planilha["Valor"][indice]
    print('-' * 115)
    print(f'Valor total gasto: R${gasto_total:.2f}')

def carregar_categorias(planilha: pd.DataFrame):
    quantidade_categorias = len(planilha['Categoria'])
    contagem_categorias = 0
    categorias_totais = list()

    while contagem_categorias < quantidade_categorias:
        if planilha['Categoria'][contagem_categorias] not in categorias_totais:
            categorias_totais.append(planilha['Categoria'][contagem_categorias])
            contagem_categorias += 1

    return categorias_totais

def quantidade_gasta(planilha: pd.DataFrame, valor_verificado):
    quantidade_linhas = len(planilha['Item'])
    indice = 0
    valor = 0

    while indice < quantidade_linhas:
        if valor_verificado.title() == planilha['Item'][indice] or valor_verificado == planilha['Categoria'][indice]:
            valor += planilha['Valor'][indice]

        indice +=1

    print(f'Valor total gasto em "{valor_verificado}" é: R${valor}')

def ordenar(planilha: pd.DataFrame):
    lista_dias = ordenar_por_data('Digite a data de inicio da busca: ', 'Digite a data final da busca: ')
    txt_final, valor_total = lista_por_dia(planilha, lista_dias)
    return txt_final, valor_total

def atualizar_planilha(planilha_para_atualizar):

    try:
        planilha = pd.read_excel(planilha_para_atualizar)
        return planilha

    except FileNotFoundError:
        print(f'{cor_texto("VERMELHO")}Erro, planilha não encontrada.{cor_texto("stop")}')