import pandas as pd
from Funções_de_validação import *
from Funções_txt import *
from Cores import cor_texto
from datetime import date
import os

lista_textos = ['Índice', 'Item', 'Valor', 'Tipo de pagamento', 'Categoria', 'Data', 'Banco']

def inserir_gasto_adaptado(planilha: pd.DataFrame, objeto, valor_objeto, forma_pagamento, categoria_objeto, data, banco ='None', banco_padrao='None', dinheiro_fisico = False):
    """Função visando inserir dados linha a linha na planilha. Recebe uma planilha de Excel como parâmetro e
    uma confirmação de "banco padrão". Enquanto o mesmo for "None", o usuário terá que escrever qual banco será
    utilizado. Utiliza a biblioteca "datetime" para puxar a data atual caso o usuário não informe a data da transação."""

    objeto = objeto.title()
    forma_pagamento = forma_pagamento.title()
    categoria_objeto = categoria_objeto.title()
    banco = banco.title()

    if banco == 'None':
        banco = banco_padrao

    if dinheiro_fisico:
        banco = 'None'

    if data == '':
        data = date.today().strftime('%d/%m/%Y')
        adicionado = pd.DataFrame(
            [{'Item': objeto, 'Valor': valor_objeto, 'Tipo_de_pagamento': forma_pagamento,
              'Categoria': categoria_objeto, 'Data': data, 'Banco': banco}])
    else:
        adicionado = pd.DataFrame(
            [{'Item': objeto, 'Valor': valor_objeto, 'Tipo_de_pagamento': forma_pagamento,
              'Categoria': categoria_objeto, 'Data': data, 'Banco': banco}])

    gerenciamento_backups_txt('Despesa', categoria_objeto, valor_objeto, forma_pagamento, objeto, data, banco)
    planilha = pd.concat([planilha, adicionado], ignore_index=True)
    arquivo_temp = 'Despesa_temp.xlsx'
    planilha.to_excel(arquivo_temp, index=False)
    os.replace(arquivo_temp, 'Despesa.xlsx')
    return

def validar_data_adaptado(mensagem):
    """Função genérica para validação de datas. Recebe como parâmetro uma mensagem de texto, utilizada para
    informar a finalidade da data. Consegue converter o formato de ano resumido (XX/XX/XX) para (XX/XX/XXXX)."""

    while True:
        data = mensagem

        if data == '':
            return data

        if data.replace('/', '').isnumeric():
            dia = data[0] + data[1]
            mes = data[3] + data[4]

            if len(data) != 10 and len(data) != 8:
                return f'O Formato de data foi definido de maneira incorreta, corrija e tente novamente.'

            elif int(dia) > 31 or  int(dia) < 1:
                return f'O Dia foi definido de maneira incorreta, corrija e tente novamente.'

            elif int(mes) > 12 or int(mes) < 1:
                return f'O mês foi definido de maneira incorreta, corrija e tente novamente.'

            elif len(data) == 8:
                data_final = f'{dia}/{mes}/20{data[6]}{data[7]}'
                return data_final

            elif len(data) == 10:
                return data

        else:
            return f'Formato de data incompreensivel, tente novamente.'

def validar_valor_adaptado(mensagem):
    """ função genérica para validar um número float. Recebe uma mensagem como parâmetro, utilizada para
    informar a finalidade do valor. Pode substituir caracteres como virgula e barra por um ponto,
    facilitando o entendimento do sistema do que é um número float (ponto flutuante). """

    while True:

        valor = mensagem
        valor = valor.replace(',', '.')
        valor = valor.replace(' ', '.')
        valor = valor.replace('/', '.')
        validacao = valor

        if valor.isalpha():
            return f'Erro, o valor deve ser um numero valido.'

        elif valor == '':
            return f'Erro, você deve digitar um valor para o item.'

        elif valor.isalnum():
            try:
                validacao = float(valor)
                return valor

            except ValueError:
                return f'Erro, algum caractere não foi reconhecido.'

        elif not valor.isalnum():
            return valor

def buscar(planilha: pd.DataFrame, item):

    """Função visando filtrar o acesso à planilha com base em informações como o tipo do item ou a categoria
    do mesmo."""

    global lista_textos

    quantidade_produtos = 0
    str_quantidade_produtos = 'None'
    indice = 0
    valor_total = 0
    lista_produtos = list()
    busca = item

    for produto in planilha['Item']:
        if produto == busca.title():
            quantidade_produtos += 1

    if quantidade_produtos == 0:
        for categoria in planilha['Categoria']:
            if categoria == busca.title():
                quantidade_produtos += 1

    if quantidade_produtos == 0:
        lista_produtos.append('Nenhum produto ou categoria com este nome foi encontrado.')

    if quantidade_produtos > 0:
        str_quantidade_produtos = f'Foram encontradas {quantidade_produtos} correspondencias para este produto/serviço: '
        frase_inicial = f'{lista_textos[0]:>5} || {lista_textos[1]:^30} || {lista_textos[2]:^10} || {lista_textos[3]:^15} || {lista_textos[4]:^12} || {lista_textos[5]:^11} || {lista_textos[6]}'
        lista_produtos.append(frase_inicial)
        while indice < len(planilha['Item']):
            if busca.title() == planilha['Item'][indice] or busca.title() == planilha['Categoria'][indice]:
                produto_atual = f'{indice:>6} || {planilha["Item"][indice]:^30} || R${planilha["Valor"][indice]:>8} || {planilha["Tipo_de_pagamento"][indice]:^17} || {planilha["Categoria"][indice]:^12} || {planilha["Data"][indice]:^11} || {planilha["Banco"][indice]}'
                quantidade_produtos += 1
                valor_total += planilha['Valor'][indice]
                lista_produtos.append(produto_atual)

            indice += 1

    return str_quantidade_produtos, valor_total, lista_produtos

def apagar_linha(planilha: pd.DataFrame, variavel: int):

        while True:

            linha_apagada = variavel
            # =============== Tratar no frontend ======================
            #if linha_apagada == -1:
             #   return

            #if linha_apagada > len(planilha['Item']) or linha_apagada < 0:
             #   return

            apagar_linha_txt(linha_apagada)
            frase_resposta = f'{cor_texto("verde")}Item "{planilha["Item"][linha_apagada]}", correspondente ao valor R${planilha["Valor"][linha_apagada]} no dia {planilha["Data"][linha_apagada]} deletado com sucesso!{cor_texto("stop")}'
            planilha = planilha.drop(index = linha_apagada)
            arquivo_temp = 'Despesa_temp.xlsx'
            planilha.to_excel(arquivo_temp, index=False)
            os.replace(arquivo_temp, 'Despesa.xlsx')
            return frase_resposta

def ver_gastos(planilha: pd.DataFrame):

    global lista_textos
    gasto_total = 0
    lista_gastos = list()

    frase_inicial = f'{lista_textos[0]:>5} || {lista_textos[1]:^30} || {lista_textos[2]:^10} || {lista_textos[3]:^15} || {lista_textos[4]:^12} || {lista_textos[5]:^11} || {lista_textos[6]}'
    lista_gastos.append(frase_inicial)

    for indice, produto in enumerate(planilha['Item']):
        produto_atual = f'{indice+1:>6} || {planilha["Item"][indice]:^30} || R${planilha["Valor"][indice]:>8} || {planilha["Tipo_de_pagamento"][indice]:^17} || {planilha["Categoria"][indice]:^12} || {planilha["Data"][indice]:^11} || {planilha["Banco"][indice]}'
        gasto_total += planilha["Valor"][indice]
        lista_gastos.append(produto_atual)

    return gasto_total, lista_gastos

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

    return valor

def ordenar(planilha: pd.DataFrame):
    lista_dias = ordenar_por_data('Digite a data de inicio da busca: ', 'Digite a data final da busca: ')
    txt_final, valor_total = lista_por_dia(planilha, lista_dias)
    return txt_final, valor_total

def atualizar_planilha():

    try:
        planilha = pd.read_excel('Financeiro_novo.xlsx')
        return planilha

    except FileNotFoundError:
        print(f'{cor_texto("VERMELHO")}Erro, planilha não encontrada.{cor_texto("stop")}')