import pandas as pd
import os
from datetime import date

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

