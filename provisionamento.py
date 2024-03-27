#! /usr/bin/env python3
import openpyxl, re, shutil, subprocess


# Definiçoes
def replace_pat(filename, pattern, replacement):
    with open(filename, 'r') as file:
        text = file.read()

    text = re.sub(pattern, replacement, text)

    with open(filename, 'w') as file:
        file.write(text)

# Variáveis
file_gxp2170 = '/srv/tftp/gxp2170_default.xml'
file_gxp1615 = '/srv/tftp/gxp1615_default.xml'
# Abrindo Planilha e Página

workbook_alunos = openpyxl.load_workbook('/srv/tftp/COMPREP.xltx')
sheet_alunos = workbook_alunos['COMPREP']

for indice, linha in enumerate(sheet_alunos.iter_rows(min_row=3)):
    
    modelo = linha[0].value 
    mac_ramal = linha[1].value 
    num_ramal = linha[2].value
    rtcaer_ramal = linha[3].value
    tf3_ramal = linha[4].value
    nome_ramal = linha[5].value 
    modelo = modelo.lower()
    num_ramal_bool = bool(num_ramal)
    rtcaer_condicao = bool(rtcaer_ramal)
    tf3_ramal_bool = bool(tf3_ramal)

    if num_ramal_bool == True or rtcaer_condicao == True or tf3_ramal_bool == True :
        if modelo == 'gxp2170':
       
            new_name = mac_ramal.lower() 
            new_name = '/srv/tftp/cfg' + new_name + '.xml'
            new_name = new_name.replace(' ','')
       
            shutil.copy(file_gxp2170, new_name)

            if num_ramal_bool == True:
                replace_pat(new_name, '%RAMAL%', str(num_ramal))
                replace_pat(new_name, '%ASTER%', '10.228.117.9')
                replace_pat(new_name, '%PASS%', 'Ast3r.C0mpr3p')

                if bool(nome_ramal) == True:
                    replace_pat(new_name, '%NOME%', nome_ramal)
                else:
                    replace_pat(new_name, '%NOME%', '')
            
            else:
                replace_pat(new_name, '%RAMAL%', '')
                replace_pat(new_name, '%NOME%', '')
                replace_pat(new_name, '%ASTER%', '')
                replace_pat(new_name, '%PASS%', '')

        
            if rtcaer_condicao == True:
                replace_pat(new_name, '%RAMAL2%', str(rtcaer_ramal))
                replace_pat(new_name, '%ASTER2%', '10.228.117.9')
                replace_pat(new_name, '%PASS2%', 'Ast3r.C0mpr3p')
    
            else:
                replace_pat(new_name, '%RAMAL2%', '')
                replace_pat(new_name, '%ASTER2%', '')
                replace_pat(new_name, '%PASS2%', '')

            if tf3_ramal_bool == True:
                replace_pat(new_name, '%RAMAL3%', str(tf3_ramal))
                replace_pat(new_name, '%ASTER3%', '10.228.11.202')
                replace_pat(new_name, '%PASS3%', 'Ast3r.D@ct41')
            else:
                replace_pat(new_name, '%RAMAL3%', '')
                replace_pat(new_name, '%ASTER3%', '')
                replace_pat(new_name, '%PASS3%', '')

        elif modelo == 'gxp1615':
            if bool(mac_ramal) == True:

                new_name = mac_ramal.lower() 
                new_name = '/srv/tftp/cfg' + new_name + '.xml'
                new_name = new_name.replace(' ','')

                shutil.copy(file_gxp1615, new_name)

                if num_ramal_bool == True:
                    replace_pat(new_name, '%RAMAL%', str(num_ramal))
               
                    replace_pat(new_name, '%ASTER%', '10.228.117.9')
                    replace_pat(new_name, '%PASS%', 'Ast3r.C0mpr3p')
                
                    if bool(nome_ramal) == True:
                        replace_pat(new_name, '%NOME%', nome_ramal)

                    else: 
                        replace_pat(new_name, '%NOME%', '')

                else:
                    replace_pat(new_name, '%RAMAL%', '')
                    replace_pat(new_name, '%NOME%', '')
                    replace_pat(new_name, '%ASTER%', '')
                    replace_pat(new_name, '%PASS%', '')

                if rtcaer_condicao == True: 
                    replace_pat(new_name, '%RAMAL2%', str(rtcaer_ramal))
                    replace_pat(new_name, '%PASS2%', 'Ast3r.C0mpr3p')
                else:
                    replace_pat(new_name, '%RAMAL2%', '')
                    replace_pat(new_name, '%PASS2%', '')
            else:
                print('* * * * Não Existe MAC associado * * * *')
        else:
            print(f'O modelo {modelo} é inválido')

    else:
        print(f'* * * * O MAC {mac_ramal} não possui ramal associado * * * *')    



