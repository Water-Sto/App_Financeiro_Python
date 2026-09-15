from Funções_Despesa import *
from Funções_de_validação import *
from Cores import cor_texto

try:
    despesa = pd.read_excel('Financeiro_novo.xlsx')
except FileNotFoundError:
    dados = {'Categoria': [],
             'Valor': [],
             'Tipo_de_pagamento': [],
             'Item': [],
             'Data': []}

    df = pd.DataFrame(dados)
    df.to_excel('Financeiro_novo.xlsx', index = False)
    despesa = pd.read_excel('Financeiro_novo.xlsx')

try:
    receita = pd.read_excel('Receita.xlsx')
except FileNotFoundError:
    dados = (
        {'Categoria': [],
         'Valor': [],
         'Tipo': [],
         'Lembrete': [],
         }
    )

    df = pd.DataFrame(dados)
    df.to_excel('Receita.xlsx', index=False)
    receita = pd.read_excel('Receita.xlsx')

# =============================== Listas com cada tipo de dado na planilha de gastos ===================================

categorias = despesa['Categoria']
lista_categorias = despesa['Categoria']
lista_valores = despesa['Valor']
tipo_de_pagamento = despesa['Tipo_de_pagamento']
lista_itens = despesa['Item']
lista_data = despesa['Data']

# ================================================ Loop Principal ======================================================

lista_opcoes = ['Sair', 'Verificar gastos gerais', 'Verificar gastos em produtos específicos', 'Adicionar gasto', 'Definir Banco Padrão', 'Apagar gastos', 'Verificar gastos por data']

try:
    banco_padrao = ler_banco_principal()
except FileNotFoundError:
    definir_banco_principal('None')
    banco_padrao = ler_banco_principal()

while True:

    try:
        print(f'{cor_texto("amarelo")} ======== PAINEL DE CONTROLE ======== {cor_texto("stop")}')
        for indice, opcao in enumerate(lista_opcoes):
            print(f'{indice} - {opcao}')
        print()

        opcao_atual = validar_inteiro('Selecione o numero da opção desejada: ')
        match opcao_atual:

            case 0:
                print(f'{cor_texto("verde")}Obrigado por participar! Encerrando...{cor_texto("stop")}')
                break

            case 1:
                ver_gastos(despesa)

            case 2:
                acessar_planilha(despesa)

            case 3:
                try:
                    inserir_gasto(despesa, banco_padrao)
                    despesa = atualizar_planilha()

                except PermissionError:
                    print(f'{cor_texto("vermelho")}Erro, o excel/bloco de notas deve ser fechado antes de acessar!{cor_texto("stop")}')

            case 4:
                banco_principal = input('Digite o nome do banco que deseja usar como principal (para cancelar a ação, apenas digite "-1"): ')
                if banco_principal != '-1':
                    definir_banco_principal(banco_principal)
                    banco_padrao = ler_banco_principal()

                else:
                    print(f'{cor_texto("azul")}Ação cancelada, retornando...{cor_texto("stop")}')
                    sleep(1)

            case 5:
                acessar_planilha(despesa, apagar = True)
                despesa = atualizar_planilha()

            case 6:
                lista_por_data, valor_total = ordenar(despesa)
                lista_teste = list()
                with open(lista_por_data, 'r', encoding = 'utf8') as arquivo:
                    for linha in arquivo:
                        print(linha.rstrip())

                print(f'{cor_texto("azul")}Valor total: R${valor_total:.2f}{cor_texto("stop")}')
            case _:
                print(f'{cor_texto("vermelho")} Erro, numero da opção inválido. {cor_texto("stop")}')

    except KeyboardInterrupt:
        print(f'{cor_texto("azul")}\nObrigado por participar! Encerrando...{cor_texto("stop")}')
        sleep(1)
        break