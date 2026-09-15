def cor_texto(mensagem):

    lista_cores = [['preto', '\033[30m'],
                   ['vermelho', '\033[31m'],
                   ['verde', '\033[32m'],
                   ['amarelo', '\033[33m'],
                   ['azul', '\033[34m'],
                   ['magenta', '\033[35m'],
                   ['ciano', '\033[36m'],
                   ['cinza', '\033[37m'],
                   ['stop', '\033[m']]

    for cor in lista_cores:
        if mensagem.lower() == cor[0]:
            return cor[1]

    #Caso não encontre a cor na lista, a função retorna branco.
    return '\033[29m'

def cor_grafica(mensagem):
    lista_cores = [['BRANCO', (255, 255, 255)],
                    ['PRETO', (0, 0, 0)],
                    ['AZUL', (0, 120, 255)],
                    ['CINZA', (180, 180, 180)],
                    ['AZUL_PALIDO', (100, 149, 237)],
                    ['AZUL_CLARO', (0, 191, 255)],
                    ['TURQUOISE', (64, 224, 208)],
                    ['AZUL_ROYAL', (65, 105, 225)],
                    ['LIMA', (0, 255, 0)],
                    ['RED', (255, 0, 0)]]

    for cor in lista_cores:
        if mensagem == cor[0]:
            return cor[1]

    return False
