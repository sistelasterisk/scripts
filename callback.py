from asterisk.manager import Manager
import sys, re

# Funções

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

            if number == '7444':
                print(f'{number}  -->  {state}')
                
                if state == 'INUSE':
                    print('Este ramal está ocupado')
                    state_channel = 'y'
                    sys.exit()

                    
manager = Manager()
state_channel = ''

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
        print('Informe o usuário que o ramal está ocupado e pergunte se deseja efetuar o callback')

    # Logoff da Central
    manager.logoff()
    manager.close()
except Exception:
   print('Programa finalizado')
