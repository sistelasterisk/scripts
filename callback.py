from asterisk.manager import Manager
from asterisk.agi import AGI
import re

def send_call(origin, dest):
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
        'CallerID': origin,
        'Timeout': 10000  # Timeout em milissegundos
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


# Parâmetros de conexão com o Asterisk Manager Interface (AMI)
AMI_HOST = '10.40.165.200'  # Endereço IP do servidor Asterisk
AMI_PORT = 5038  # Porta do Asterisk Manager Interface
AMI_USERNAME = 'ttag'  # Nome de usuário do AMI
AMI_PASSWORD = 'panopreto'  # Senha do AMI

# Conectando ao Asterisk Manager Interface (AMI)

agi = AGI()
rege_number = re.compile(r'\d{4}')

destino = agi.env['agi_extension'].strip()
origem = agi.env['agi_channel']
origem = rege_number.search(origem).group()
origem = origem.strip()

agi.verbose(f'Ligação de {origem} para {destino}')

send_call(origem, destino)

agi.verbose('Efetuando ligação entre os ramais...')