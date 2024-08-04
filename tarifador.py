import re, openpyxl
from datetime import datetime


#---- Expressões rgulares
# Horario
re_horarios = re.compile(r'\d{2}:\d{2}:\d{2}')
# Data
re_date = re.compile(r'\d{4}-\d{2}-\d{2}')
# Ramais (geral)
re_ramais = re.compile(r'"\d{4,}"')
# Ramais de Origem
re_origem = re.compile(r'"\d{4}"')
# Externo
re_dest = re.compile(r'"\d{8,}"')
# Local
re_local = re.compile(r'^\d{8,9}$')
# DDD
re_ddd = re.compile(r'^\d{10,11}$')
# DDI
re_ddi = re.compile(r'\d{12,}')
# Gratuito
#re_free = re.compile(r'0800')

#---- Variáveis
# Caminho de diretórios
path_master = '3 - Tarifador/Master.csv'
path_tarifacao_xlsx = '3 - Tarifador/tarifacao.xlsx'
path_tarifacao_save = '3 - Tarifador/bilhete.xlsx'

#Lista de linhas para serem acrescentadas à planilha
tipo_ligacao = ''
list_sheet = []
list_texto = []

#-----Algoritmo
with open(path_master, 'r') as f:
    linhas_texto = f.readlines()

for linha in linhas_texto:
    # Processa somente as linhas com ligações atendidas
    if 'ANSWERED' in linha:
        ramais = re_ramais.findall(linha)
        
        # Verifica se a linha tem um numero gratuito como destino e passa para proximo item do loop
        if len(ramais) >= 2:
            if '0800' in ramais[1]:
                continue 

        # Procura apenas por linhas ue tenham um ramal ligando para um número externo
        try:
            match_origem = re_origem.search(ramais[0])
            match_dest = re_dest.search(ramais[1])
            
        except IndexError as e:
            continue

        # Caso encontre a linha, processa as informações
        # Processamento ramais de origem e destino
        if match_origem and match_dest:
            match_origem = match_origem.group()
            match_origem = re.sub('"', '', match_origem)

            match_dest = match_dest.group()
            match_dest = re.sub('"', '', match_dest)
            
            if match_dest.startswith('10800'):
                match_dest=re.sub(r'^1', '', match_dest)
            
            elif match_dest.startswith('10'):
                match_dest = re.sub(r'^10', '', match_dest)

            else:
                match_dest=re.sub(r'^1', '', match_dest)

            # Processamento do Tipo de ligação
            if re_local.search(match_dest):
                tipo_ligacao = 'Local'

            elif re_ddd.search(match_dest) and not match_dest.startswith('0800'):
                tipo_ligacao = 'DDD'

            elif re_ddi.search(match_dest):
                tipo_ligacao = 'DDI'

            # Processamento data
            dates = re_date.findall(linha)
            
            try:
                initial_date = dates[1]
                final_date = dates[2]

            except IndexError as e:
                continue

            date_call = initial_date[-2] + initial_date[-1] + '/' + initial_date[-5] + initial_date[-4] + '/' + initial_date[0] + initial_date[1] + initial_date[2] + initial_date[3]
    
            # Processamento Inicio e Fim da Chamada
            times_call = re_horarios.findall(linha)
            _, initial_time, final_time = times_call

            # Processamento da Duração
            initial_time_date = datetime.strptime(f'{initial_date} {initial_time}', '%Y-%m-%d %H:%M:%S')
            final_time_date = datetime.strptime(f'{final_date} {final_time}', '%Y-%m-%d %H:%M:%S')
            
            duracao = final_time_date - initial_time_date
            duracao_str = str(duracao)
            initial_time = str(initial_time)
            final_time = str(final_time)

            # Processamento do valor da ligação

            if tipo_ligacao  == 'Local' and len(match_dest) == 8:
                duracao_str = duracao_str[2] + duracao_str[3]
                duracao_float = int(duracao_str)
                md = match_dest
                match_dest = f'{md[0]}{md[1]}{md[2]}{md[3]}-{md[4]}{md[5]}{md[6]}{md[7]}'

                calc_minutagem = (duracao_float + 1) * 0.03

            elif tipo_ligacao  == 'Local' and len(match_dest) == 9:
                duracao_str = duracao_str[2] + duracao_str[3]
                duracao_float = int(duracao_str)
                md = match_dest
                match_dest = f'{md[0]}{md[1]}{md[2]}{md[3]}{md[4]}-{md[5]}{md[6]}{md[7]}{md[8]}'
              
                calc_minutagem = (duracao_float + 1) * 0.55
            

            elif tipo_ligacao == 'DDD' and len(match_dest) == 10:
                duracao_str = duracao_str[2] + duracao_str[3]
                duracao_float = int(duracao_str)
                md = match_dest
                match_dest = f'({md[0]}{md[1]}) {md[2]}{md[3]}{md[4]}{md[5]}-{md[6]}{md[7]}{md[8]}{md[9]}'

                calc_minutagem = (duracao_float + 1) * 0.26

            elif tipo_ligacao == 'DDD' and len(match_dest) == 11:
                duracao_str = duracao_str[2] + duracao_str[3]
                duracao_float = int(duracao_str)
                md = match_dest
                match_dest = f'({md[0]}{md[1]}) {md[2]}{md[3]}{md[4]}{md[5]}{md[6]}-{md[7]}{md[8]}{md[9]}{md[10]}'

                calc_minutagem = (duracao_float + 1) * 1.62

            elif tipo_ligacao == 'DDI' and len(match_dest) > 11:
                duracao_str = duracao_str[2] + duracao_str[3]
                duracao_float = int(duracao_str)

                calc_minutagem = (duracao_float + 1) * 2.33

            # Armazena todos os dados em lista
            
            list_sheet.append([date_call, match_origem, match_dest, initial_time, final_time, str(duracao), tipo_ligacao, calc_minutagem]) 
####################################################################################################            
            # DELETAR APÓS TESTE
            list_texto.append([date_call, match_origem, match_dest, initial_time, final_time, str(duracao), tipo_ligacao, str(calc_minutagem)]) 

####################################################################
# SOMENTE PARA FASE DE TESTE (RETIRAR DEPOIS)                      #
texto = ''                                                         #             
for linhas in list_texto:
    contador = 1
    for dado in linhas:
        if contador == 8:
            texto += dado + '\n'
        else:
            texto += dado + ', '
        contador += 1                                              #
print(texto)                                                       #
####################################################################
# Armazenando dados na planilha
wb = openpyxl.load_workbook(path_tarifacao_xlsx)
ws = wb['Bilhetes']

row = 3
column = 1

for line in list_sheet:
    column = 1
    for data in line:
        ws.cell(row=row, column=column, value=data)
        column += 1
    row += 1

wb.save(path_tarifacao_save)
