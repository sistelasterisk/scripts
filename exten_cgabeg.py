import openpyxl

def line_exten(filename, text):
    with open(filename, 'a') as file:
        file.write('\n')

        file.write(text)
    

workbook = openpyxl.load_workbook('CGABEG.xltx')
sheet_alunos = workbook['CGABEG']
num_linha = 1

for indice, linha in enumerate(sheet_alunos.iter_rows(min_row=3)):
     
    ramal_ext = linha[3].value 
    ramal_int = linha[2].value
    ramal_ext_str = str(ramal_ext)
    ramal_int_str = str(ramal_int)
    ramal_int_bool = bool(ramal_int)
    ramal_ext_bool = bool(ramal_ext)
    num_linha += 1

    if ramal_int_bool == True and ramal_ext_bool == True :
        exten = f'exten => {ramal_int_str},1,dial(pjsip/{ramal_ext_str},60,tT)'

        line_exten('extensions.internos', exten)

    else:
        print(f'Ramal externo ou interno está vazio na linha {str(num_linha)} ')
