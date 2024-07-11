from asterisk.manager import Manager
from asterisk.agi import AGI
import sys, re

# Funções
def main():
    agi.verbose("o Script AGI foi iniciado")

    # Capturar os números de origem e destino
   
    rege_number = re.compile(r'\d{4}')

    destination = agi.env['agi_extension']
    channel = agi.env['agi_channel']


    channel = rege_number.search(channel)
    if channel == None:
        ...
    else:
        channel = channel.group()

    agi.verbose(f"Destination: {destination}")
    agi.verbose(f"Channel: {channel}")

    origin_dest = [channel, destination]

    return origin_dest
def check_channel(event, manager):
    global state_channel

    # Expressão regular para capturar o número do Device
    try:
        regex = re.compile(r'\d{4}')
    
    finally:    

        # Subalgoritmo
        if event.name == 'DeviceStateChange':
            number = event.get_header('Device')
            number = regex.search(number)
            if number == None:
                ...
            else:
                number = number.group()

            state = event.get_header('State')

            if number == called:
                print(f'{number}  -->  {state}')
                
                if state == 'INUSE':
                    print('Este ramal está ocupado')
                    state_channel = 'y'
                    sys.exit()

global caller
global called

manager = Manager()
agi = AGI()
state_channel = ''

# Capturar o número chamador e o chamado
list_origin_dest = main()
caller = list_origin_dest[0]
called = list_origin_dest[1] 

# Verifica se o canal está em uso
try:
    # Login na central via AMI
    manager.connect('10.40.165.200', 5038)
    manager.login('ttag', 'panopreto')
    
    print('Monitorando o canal...\nPressione Ctrl + c para sair...')
    # Verifica o Status do canal

    action = {
        'Action': 'DeviceStateList'
    }
    manager.register_event('DeviceStateChange', check_channel)
    manager.send_action(action)

    try:
        while True:
            manager.event_dispatch()
          
    except SystemExit:
        print(f'O ramal {called} esta´ocupado. Deseja efetuar o callback?\nDigite 1 para Sim ou 2 para não.')

    # Logoff da Central
    manager.logoff()
    manager.close()
except Exception:
   print('Programa finalizado')
