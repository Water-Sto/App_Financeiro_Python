from Cores import cor_texto
from datetime import datetime

def validar_inteiro(mensagem, apagar = False):

    """Função genérica para validar um número inteiro. Não aceita números negativos, pois o seu principal objetivo
    é retornar um índice da planilha do Excel. Caso o parâmetro "apagar" seja True, a função também aceita
    como resposta "-1", utilizado para parar a ação na função de apagar gastos."""

    while True:
        numero_inteiro = input(mensagem)

        if apagar:
            if numero_inteiro == '-1':
                numero_inteiro = int(numero_inteiro)
                return numero_inteiro

        if numero_inteiro.isalpha():
            print(f'{cor_texto("vermelho")}Erro, digite um indice válido. {cor_texto("STOP")}')

        elif numero_inteiro.isnumeric():
            try:
                numero_inteiro = int(numero_inteiro)
                return numero_inteiro

            except ValueError:
                print(f'{cor_texto("vermelho")}Erro, Valor inválido. {cor_texto("STOP")}')

        elif numero_inteiro.isalnum():
            print(f'{cor_texto("vermelho")}Erro, digite apenas o indice da linha.{cor_texto("STOP")}')

        elif not numero_inteiro.isalnum():
            print(f'{cor_texto("vermelho")}Erro, tipo de dado incompreensivel, tente novamente. {cor_texto("STOP")}')

def validar_data(mensagem):
    """Função genérica para validação de datas. Recebe como parâmetro uma mensagem de texto, utilizada para
    informar a finalidade da data. Consegue converter o formato de ano resumido (XX/XX/XX) para (XX/XX/XXXX)."""

    while True:
        data = input(mensagem)

        if data == '':
            return data

        if data.replace('/', '').isnumeric():
            dia = data[0] + data[1]
            mes = data[3] + data[4]

            if len(data) != 10 and len(data) != 8:
                print(f'{cor_texto("VERMELHO")}Formato de data incorreto, tente novamente.{cor_texto("STOP")}')

            elif int(dia) > 31 or  int(dia) < 1:
                print(f'{cor_texto("Vermelho")}Dia incorreto, tente novamente.{cor_texto("STOP")}')

            elif int(mes) > 12 or int(mes) < 1:
                print(f'{cor_texto("vermelho")}Mês incorreto, tente novamente.{cor_texto("STOP")}')

            elif len(data) == 8:
                data_final = f'{dia}/{mes}/20{data[6]}{data[7]}'
                return data_final

            elif len(data) == 10:
                return data

        else:
            print(f'{cor_texto("VERMELHO")}Formato de data incompreensivel, tente novamente.{cor_texto("STOP")}')

def ordenar_por_data(mensagem, mensagem2):
    """Função genérica para validação de datas. Recebe como parâmetro uma mensagem de texto, utilizada para
    informar a finalidade da data. Consegue converter o formato de ano resumido (XX/XX/XX) para (XX/XX/XXXX)."""

    while True:
        data_inicial = input(mensagem)
        data_final = input(mensagem2)

        if data_inicial.replace('/', '').isnumeric() and data_final.replace('/', '').isnumeric():
            dia_inicial = data_inicial[0] + data_inicial[1]
            dia_final = data_final[0] + data_final[1]

            mes_inicial = data_inicial[3] + data_inicial[4]
            mes_final = data_final[3] + data_final[4]

            ano_inicial, ano_final = 'none', 'none'

            if len(data_inicial) != 10 and len(data_inicial) != 8 or len(data_final) != 10 and len(data_final) != 8:
                print(f'{cor_texto("VERMELHO")}Formato de data incorreto, tente novamente.{cor_texto("STOP")}')

            elif int(dia_inicial) > 31 or  int(dia_inicial) < 1 or int(dia_final) > 31 or int(dia_final) < 1:
                print(f'{cor_texto("Vermelho")}Dia incorreto, tente novamente.{cor_texto("STOP")}')

            elif int(mes_inicial) > 12 or int(mes_inicial) < 1 or int(mes_final) > 12 or int(mes_final) < 1:
                print(f'{cor_texto("vermelho")}Mês incorreto, tente novamente.{cor_texto("STOP")}')

            elif len(data_inicial) == 8 and len(data_final) == 8:
                ano_inicial = '20' + data_inicial[6] + data_inicial[7]
                ano_final = '20' + data_final[6] + data_final[7]

            elif len(data_inicial) == 10 and len(data_final) == 8:
                ano_final = '20' + data_final[6] + data_final[7]

            elif len(data_inicial) == 8 and len(data_final) == 10:
                ano_inicial = '20' + data_inicial[6] + data_inicial[7]

            if ano_inicial != 'none' and ano_final != 'none':

                data_inicio = datetime(
                    int(ano_inicial),
                    int(mes_inicial),
                    int(dia_inicial),
                )

                data_fim = datetime(
                    int(ano_final),
                    int(mes_final),
                    int(dia_final),
                )

                if data_inicio > data_fim:
                    print(f'{cor_texto("VERMELHO")}A data inicial não pode ser maior que a data final.{cor_texto("STOP")}')
                    continue

                return data_inicio, data_fim

        else:
            print(f'{cor_texto("VERMELHO")}Formato de data incompreensivel, tente novamente.{cor_texto("STOP")}')

def validar_valor(mensagem):
    """ função genérica para validar um número float. Recebe uma mensagem como parâmetro, utilizada para
    informar a finalidade do valor. Pode substituir caracteres como virgula e barra por um ponto,
    facilitando o entendimento do sistema do que é um número float (ponto flutuante). """

    while True:
        valor = input(mensagem)
        valor = valor.replace(',', '.')
        valor = valor.replace(' ', '.')
        valor = valor.replace('/', '.')

        if valor.isalpha():
            print(f'{cor_texto("VERMELHO")}Erro, o valor deve ser um numero valido. {cor_texto("STOP")}')

        elif valor.isalnum():
            try:
                valor = float(valor)
                return valor

            except ValueError:
                print(f'{cor_texto("VERMELHO")}Erro, algum caractere não foi reconhecido. {cor_texto("STOP")}')

        elif not valor.isalnum():
            valor = float(valor)
            return valor
