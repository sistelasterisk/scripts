from asterisk.manager import Manager
import time, subprocess, re

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

    for i, lines in enumerate(output_command):
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

def send_call(origin, dest):
    # Parâmetros de conexão com o Asterisk Manager Interface (AMI)
    AMI_HOST = '10.40.165.200'  # Endereço IP do servidor Asterisk
    AMI_PORT = 5038  # Porta do Asterisk Manager Interface
    AMI_USERNAME = 'ttag'  # Nome de usuário do AMI
    AMI_PASSWORD = 'panopreto'  # Senha do AMI

    manager = Manager()

    try:
        manager.connect(AMI_HOST, AMI_PORT)
        manager.login(AMI_USERNAME, AMI_PASSWORD)
        print("Conexão bem-sucedida com o Asterisk Manager Interface!")
    except Exception as e:
        print("Erro ao conectar ao Asterisk Manager Interface:", e)
        exit()
   
    # Criar a ação Originate
    action = {
        'Action': 'Originate',
        'Channel': f'PJSIP/{origin}',
        'Exten': dest,
        'Context': 'ramais',
        'Priority': 1,
        'CallerID': f'Callback para {dest}',
        'Timeout': 60000  # Timeout em milissegundos
    }

    # Enviar a ação
    try:
        response = manager.send_action(action)
        print("Resposta do Asterisk:", response)
    except Exception as e:
        print("Erro ao enviar a ação para o Asterisk:", e)

    # Desconectar do AMI
    manager.logoff()
    manager.close()

# Colhe o ramal de origem e de destino
origem = '%ORIGEM%'
ramal_destino = '%DEST%'

check_channel = ''

limit_time = 300

check_status_channel(ramal_destino)

initial_time = time.time()

while check_channel != 'free':
    time.sleep(10)
    decorr_time = time.time() - initial_time
    if decorr_time >= limit_time:
        break

    check_status_channel(ramal_destino)
    

if check_channel == 'free':
    send_call(origem, ramal_destino)
