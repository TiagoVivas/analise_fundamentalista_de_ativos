import pandas as pd
import os

# Ativo selecionado --------------------------------------------------------
ativo_selecionado = ''

# Lista de ativos ----------------------------------------------------------
if ('ativos.txt' in os.listdir()):
    with open('ativos.txt') as f:
        lista_de_ativos = f.readlines()
        lista_de_ativos = [x.replace('\n', '') for x in lista_de_ativos]
else:
    lista_de_ativos = []

# Dataframe com valores de infomações --------------------------------------
if ('df_infos.csv' in os.listdir()):
    df_infos = pd.read_csv('df_infos.csv', index_col=0)
else:
    estrutura_dados_infos = {
        'ativo': [],
        'data': [],
        'nome': [],
        'logo': [],
        'preco': [],
        'setor': [],
        'industria': [],
        'valor_mercado': [],
        'funcionarios': [],
        'proventos_12_meses': [],
        'div_12_meses': [],
        'data_com': [],
        'payout': [],
        'esg_total_min': [],
        'esg_total_max': [],
        'esg_total_med': [],
        'esg_total_atual': [],
        'esg_ambiental_min': [],
        'esg_ambiental_max': [],
        'esg_ambiental_med': [],
        'esg_ambiental_atual': [],
        'esg_social_min': [],
        'esg_social_max': [],
        'esg_social_med': [],
        'esg_social_atual': [],
        'esg_governanca_min': [],
        'esg_governanca_max': [],
        'esg_governanca_med': [],
        'esg_governanca_atual': [],
        'polemicas': []
    }

    df_infos = pd.DataFrame(estrutura_dados_infos)
    df_infos.to_csv('df_infos.csv')

# Dataframe com valores de finanças --------------------------------------
if ('df_financas.csv' in os.listdir()):
    df_financas = pd.read_csv('df_financas.csv', index_col=0)
else:
    estrutura_dados_financas = {
        'chave': [],
        'ativo': [],
        'tipo_periodo': [],
        'data': [],
        'receita_total': [],
        'custo_produtos_vendidos': [],
        'despesas_adm_vendas': [],
        'pesquisa_desenvolvimento': [],
        'despesas_juros': [],
        'ebit': [],
        'lucro_bruto': [],
        'lucro_antes_impostos': [],
        'lucro_liquido': []
    }

    df_financas = pd.DataFrame(estrutura_dados_financas)
    df_financas.to_csv('df_financas.csv')