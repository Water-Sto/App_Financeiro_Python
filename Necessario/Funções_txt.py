from Cores import cor_texto
from datetime import datetime

def definir_banco_principal(banco_principal):
    with open("Banco_principal.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(banco_principal)
        print(f'Seu banco principal foi definido como: {banco_principal}')

def converter_data_numero(data):

    dia = data[0] + data[1]
    mes = data[3] + data[4]
    ano = data[6] + data[7] + data[8] + data[9]

    lista_retorno = [int(dia), int(mes), int(ano)]

    return lista_retorno

def lista_por_dia(banco_de_dados, intervalo_datas):

    data_inicio, data_fim = intervalo_datas
    nome_arquivo = 'Transações por período'

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        lista_final = list()
        valor_final = 0

        for indice, data in enumerate(banco_de_dados['Data']):

            data_atual = datetime.strptime(data, '%d/%m/%Y')

            if data_inicio <= data_atual <= data_fim:
                string_final = f'{indice+1:>6} || {banco_de_dados["Item"][indice]:^30} || R${banco_de_dados["Valor"][indice]:>8} || {banco_de_dados["Tipo_de_pagamento"][indice]:^17} || {banco_de_dados["Categoria"][indice]:^12} || {banco_de_dados["Data"][indice]:^11} || {banco_de_dados["Banco"][indice]}'
                valor_final += banco_de_dados['Valor'][indice]

                lista_final.append(string_final)

        for transacao in lista_final:
            arquivo.write(f'{transacao}\n')

        return nome_arquivo, valor_final

def ler_banco_principal():
    with open("Banco_principal.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            pass
        return linha

def ler_txt(nome_txt):
    quantidade_linhas = 0
    with open(nome_txt, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            quantidade_linhas += 1
        return quantidade_linhas

def gerenciamento_txt(categoria, valor, tipo_de_pagamento, item, data, banco, apagar = False):

    """Função genérica com diversos objetivos. Recebe como parâmetro toda a informação sobre o item em questão, que também
    é compartilhada com o documento Excel. Recebe também a informação sobre a necessidade de apagar aquela linha
    (parâmetro 'apagar' pode ser True ou False). Caso não encontre o arquivo, ela cria o mesmo. """

    registro = f'{categoria};{valor};{tipo_de_pagamento};{item};{data};{banco}\n'

    try:
        indice = ler_txt('Backup_gastos.txt')
        if not apagar:
            with open("Backup_gastos.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f'{indice};{registro}')
                return

        if apagar:
            indice = 0
            with open("Backup_gastos.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()

            with open("Backup_gastos.txt", "w", encoding="utf-8") as arquivo:
                for linha in linhas:
                    if linha != registro:
                        linha = linha.split(';', 1)
                        arquivo.write(f'{indice};{linha[1]}')
                    indice +=1

    except FileNotFoundError:
        with open("Backup_gastos.txt", "w", encoding="utf-8") as arquivo:
            if apagar:
                print(f'{cor_texto("vermelho")}Erro, nenhuma informação existente para ser apagada.{cor_texto("stop")}')
                return

            arquivo.write(f'0;{categoria};{valor};{tipo_de_pagamento};{item};{data};{banco}\n')

def backup_receita_txt(categoria, valor, tipo, data, banco = 'None', apagar = False):

    """Função genérica com diversos objetivos. Recebe como parâmetro toda a informação sobre o item em questão, que também
    é compartilhada com o documento Excel. Recebe também a informação sobre a necessidade de apagar aquela linha
    (parâmetro 'apagar' pode ser True ou False). Caso não encontre o arquivo, ela cria o mesmo. """

    registro = f'{categoria};{valor};{tipo};{data};{banco}\n'

    try:
        indice = ler_txt('Backup_ganhos.txt')
        if not apagar:
            with open("Backup_ganhos.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f'{indice};{registro}')
                return

        if apagar:
            with open("Backup_ganhos.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()

            with open("Backup_ganhos.txt", "w", encoding="utf-8") as arquivo:
                for linha in linhas:
                    if linha != registro:
                        arquivo.write(linha)

    except FileNotFoundError:
        with open("Backup_gastos.txt", "w", encoding="utf-8") as arquivo:
            if apagar:
                print(f'{cor_texto("vermelho")}Erro, nenhuma informação existente para ser apagada.{cor_texto("stop")}')
                return

            arquivo.write(f'0;{categoria};{valor};{tipo_de_pagamento};{item};{data};{banco}\n')

def apagar_linha_txt(indice_deletado):
    """Função genérica para apagar linhas de um documento txt. Recebe como parametro apenas o índice da linha
    que deve ser apagada no documento original. Reescreve todas as linhas do documento txt, renovando o índice de
    cada linha no processo. """

    indice = 0

    try:
        with open("Backup_gastos.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        with open("Backup_gastos.txt", "w", encoding="utf-8") as arquivo:
            for linha in linhas:
                if not linha.startswith(f'{indice_deletado};'):
                    linha = f'{indice}{linha[1:]}'
                    arquivo.write(f'{linha}')
                    indice += 1

    except FileNotFoundError:
        print(f'{cor_texto("vermelho")}Nenhuma linha existente para ser apagada.{cor_texto("stop")}')

