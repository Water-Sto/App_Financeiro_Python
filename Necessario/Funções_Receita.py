import pandas as pd
import os
from datetime import date
from time import sleep
from Funções_de_validação import validar_inteiro
from Funções_txt import *

lista_textos = ['Índice', 'Categoria', 'Valor', 'Tipo de transferência', 'Data', 'Banco']

def inserir_ganho(planilha: pd.DataFrame, categoria, valor, tipo, data, banco = 'None', banco_padrao = 'None'):
    if banco_padrao != 'None' and banco == 'None':
        banco = banco_padrao

    if data == '':
        data = date.today().strftime('%d/%m/%Y')

    adicionado = pd.DataFrame([{'Categoria': categoria, 'Valor': valor, 'Tipo': tipo, 'Data': data, 'Banco': banco}])
    planilha = pd.concat([planilha, adicionado])
    excel_temp = 'Receita_temp.xlsx'
    planilha.to_excel(excel_temp, index=False)
    os.replace(excel_temp, 'Receita.xlsx')
    return

def acessar_planilha(planilha: pd.DataFrame, apagar = False, item = 'None'):

    """Função visando filtrar o acesso à planilha com base em informações como o tipo do item ou a categoria
    do mesmo. Também é a função utilizada para apagar itens do Excel com base no índice das suas posições"""

    global lista_textos

    quantidade_produtos = 0
    indice = 0
    valor_total = 0

    if item == 'None':
        busca = input(f'Digite a categoria ou o banco responsável pela transferência: ')

    else:
        busca = item

    for produto in planilha['Banco']:
        if produto == busca.title():
            quantidade_produtos += 1

    if quantidade_produtos == 0:
        for categoria in planilha['Categoria']:
            if categoria == busca.title():
                quantidade_produtos += 1

    if quantidade_produtos > 0:
        print(f'Foram encontradas {quantidade_produtos} correspondencias para esta transferência: \n')
        print(f'{lista_textos[0]:>5} || {lista_textos[1]:^30} || {lista_textos[2]:^10} || {lista_textos[3]:^15} || {lista_textos[4]:^12} || {lista_textos[5]:^11}')
        print('-'*115)
        while indice < len(planilha['Categoria']):
            if busca.title() == planilha['Categoria'][indice] or busca.title() == planilha['Banco'][indice]:
                print(f'{indice:>6} || {planilha["Categoria"][indice]:^30} || R${planilha["Valor"][indice]:>8} || {planilha["Tipo"][indice]:^17} || {planilha["Data"][indice]:^11} || {planilha["Banco"][indice]}')
                quantidade_produtos += 1
                valor_total += planilha['Valor'][indice]

            indice += 1

        print('-'*115)

        print(f'{cor_texto("azul")}Valor arrecadado por "{busca}" é: R${valor_total:.2f}. {cor_texto("stop")}')

    if apagar:

        if quantidade_produtos == 0:
            print(f'{cor_texto("vermelho")}Nenhuma transferência correspondente a sua busca foi encontrado, tente novamente.{cor_texto("stop")}')
            sleep(0.5)
            return

        while True:
            linha_apagada = validar_inteiro('Digite o índice da linha que deseja apagar (tecle "-1" para cancelar a ação): ', apagar = True)
            if linha_apagada == -1:
                print(f'{cor_texto("azul")}Ação cancelada, voltando ao painel de controle...{cor_texto("stop")}')
                sleep(0.5)
                break

            if linha_apagada > len(planilha['Categoria']) or linha_apagada < 0:
                print(f'{cor_texto("vermelho")}Linha não encontrada, tente novamente.{cor_texto("stop")}')
                break

            apagar_linha_txt(linha_apagada)
            backup_receita_txt(planilha['Categoria'][linha_apagada], planilha['Valor'][linha_apagada], planilha['Tipo'][linha_apagada], planilha['Data'][linha_apagada], planilha['Banco'][linha_apagada], apagar = True)
            print(f'{cor_texto("verde")}Item "{planilha["Item"][linha_apagada]}", correspondente ao valor R${planilha["Valor"][linha_apagada]} no dia {planilha["Data"][linha_apagada]} deletado com sucesso!{cor_texto("stop")}')
            planilha = planilha.drop(index = linha_apagada)
            arquivo_temp = 'Financeiro_novo_temp.xlsx'
            planilha.to_excel(arquivo_temp, index=False)
            os.replace(arquivo_temp, 'Financeiro_novo.xlsx')
            break
