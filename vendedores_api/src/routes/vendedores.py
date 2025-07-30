import pandas as pd
import json
from datetime import datetime


def process_excel_file(file_path):
    '''
    Processa o arquivo Excel e retorna os dados estruturados
    '''
    try:
        try:
            campanhas_df = pd.read_excel(file_path, sheet_name='CAMPANHAS')
        except ValueError:
            raise ValueError("A aba 'CAMPANHAS' nao foi encontrada na planilha.")

        try:
            gatilhos_df = pd.read_excel(file_path, sheet_name='Gatilhos')
        except ValueError:
            raise ValueError("A aba 'Gatilhos' nao foi encontrada na planilha.")
        
        expected_campanhas_cols = [
            'CODIGO VENDEDOR', 'Nome Vendedor', 'Indústria', 'COTA',
            'REALIZADO', 'SALDO', 'PREMIO VALOR', 'PREMIO STATUS'
        ]
        for col in expected_campanhas_cols:
            if col not in campanhas_df.columns:
                raise KeyError(f"Coluna '{col}' nao encontrada na aba CAMPANHAS.")

        expected_gatilhos_cols = [
            'CODIGO VENDEDOR', 'Gatilho', 'Meta Gatilho', 'Realizado Gatilho', 'Falta Gatilho'
        ]
        for col in expected_gatilhos_cols:
            if col not in gatilhos_df.columns:
                raise KeyError(f"Coluna '{col}' nao encontrada na aba Gatilhos.")

        vendedores_data = {}
        
        for _, row in campanhas_df.iterrows():
            codigo_vendedor = str(row['CODIGO VENDEDOR'])
            
            if codigo_vendedor not in vendedores_data:
                vendedores_data[codigo_vendedor] = {
                    'codigo_vendedor': codigo_vendedor,
                    'nome_vendedor': row['Nome Vendedor'],
                    'campanhas': [],
                    'gatilhos': [],
                    'total_premiacao': 'R$ 0.00'
                }
            
            campanha = {
                'CODIGO VENDEDOR': row['CODIGO VENDEDOR'],
                'Nome Vendedor': row['Nome Vendedor'],
                'Indústria': row['Indústria'],
                'COTA': row['COTA'] if pd.notna(row['COTA']) else 0,
                'REALIZADO': row['REALIZADO'] if pd.notna(row['REALIZADO']) else 0,
                'SALDO': row['SALDO'] if pd.notna(row['SALDO']) else 0,
                'PREMIO VALOR': row['PREMIO VALOR'] if pd.notna(row['PREMIO VALOR']) else 0,
                'PREMIO STATUS': row['PREMIO STATUS'] if pd.notna(row['PREMIO STATUS']) else 'N/A'
            }
            vendedores_data[codigo_vendedor]['campanhas'].append(campanha)
        
        for _, row in gatilhos_df.iterrows():
            codigo_vendedor = str(row['CODIGO VENDEDOR'])
            if codigo_vendedor in vendedores_data:
                gatilho = {
                    'Gatilho': row['Gatilho'] if pd.notna(row['Gatilho']) else 'N/A',
                    'Meta Gatilho': row['Meta Gatilho'] if pd.notna(row['Meta Gatilho']) else 0,
                    'Realizado Gatilho': row['Realizado Gatilho'] if pd.notna(row['Realizado Gatilho']) else 0,
                    'Falta Gatilho': row['Falta Gatilho'] if pd.notna(row['Falta Gatilho']) else 0
                }
                vendedores_data[codigo_vendedor]['gatilhos'].append(gatilho)
        
        for codigo, vendedor in vendedores_data.items():
            total = 0
            for campanha in vendedor['campanhas']:
                premio_str = str(campanha['PREMIO VALOR']).replace('R$', '').replace('.', '').replace(',', '.').strip()
                try:
                    total += float(premio_str)
                except ValueError:
                    pass
            vendedor['total_premiacao'] = f"R$ {total:.2f}".replace('.', ',')
        
        return vendedores_data
        
    except Exception as e:
        print(f"Erro ao processar arquivo Excel: {e}")
        raise e


def get_all_vendedores():
    pass


def get_vendedor_by_code(codigo):
    pass
