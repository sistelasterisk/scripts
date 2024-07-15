from asterisk.agi import AGI
import subprocess, re

def check_status_channel(ramal):
    global check_channel
    re_up = 'Up'
    re_free = 'Ring'
    re_ringing = 'Ringing'
    check_channel = ''

    command = subprocess.Popen(['asterisk -rx "pjsip show channels"'], stdout=subprocess.PIPE, shell=True)
    stdout, stderr = command.communicate()
    output_command = stdout.decode('utf-8')

    output_command = output_command.split('\n')

    for lines in output_command:
        channel_busy = re.search(re_up, lines)
        channel_free = re.search(re_free, lines)
        channel_ringing = re.search(re_ringing, lines)
        check_ramal = re.search(f'/{ramal}', lines)

        if channel_busy and check_ramal:
            #text = 'O ramal está ocupado'
            check_channel = 'busy'
            break

        elif channel_free and check_ramal:
            #text = 'O ramal está efetuando uma ligação'
            check_channel = 'ring'
            break

        elif channel_ringing and check_ramal:
             #text = 'O ramal está sendo chamado no momento'
             check_channel = 'ringing'
             break
         
        #text = 'O ramal está livre'
        check_channel = 'free'

agi = AGI()

reply_user = ''

# Capturando o ramal de origem e de destino
rege_number = re.compile(r'\d{4}')
ramal_destino = agi.env['agi_extension']
origem = agi.env['agi_channel']
origem = rege_number.search(origem).group()
origem = origem.strip()

check_status_channel(ramal_destino)

if check_channel == 'free':
    agi.verbose('Ramal está Livre')
    agi.verbose(f'Ligando para ramal {ramal_destino}')
    agi.set_priority(6)

if check_channel == 'busy' or check_channel == 'ring' or check_channel == 'ringing':
    agi.verbose('Ramal ocupado, oferecendo opções ao usuário')
    agi.answer()
    reply_user = agi.get_data('is-curntly-busy')

    if reply_user == '1':
        
# Modificando campo ramal de origem e ramal de destino de script
        with open('/home/ttag/originate.py', 'r') as f:
            texto = f.read()
            texto = re.sub('%ORIGEM%', origem, texto)
            texto = re.sub('%DEST%', ramal_destino, texto)
        
        with open('/home/ttag/originate1.py', 'w') as f:
            f.write(texto)
         #Executando o originate.py
        process = subprocess.Popen('/home/ttag/./originate1.py', shell=True ,stdout=subprocess.PIPE)

    elif reply_user == '2':
        agi.verbose('Opção 2 selecionada. Desligando chamada')
        agi.set_priority(7)

agi.verbose('Script encerrado')
