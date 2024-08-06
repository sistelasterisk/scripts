import ipaddress, re, subprocess, os

def get_ip_mask():
    ip = input('Qual o endereço IP?\n')
    mask = input('\nQual a máscara da rede?\n')

    return ip, mask

def get_network(ip, mask):
    rede = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)

    return rede.network_address, rede.netmask, rede.broadcast_address

def shell(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')

    return stdout

# --------- PATHS ---------------------
file_with_interfaces = 'teste_file'

# -------- VARIÁVEIS --------------------
# ------ > Declaração < ---------------
interfaces = ['ens192.600', 'ens192.605', 'ens192.603']

text_default_dhcp_conf = '''default-lease-time 43200;   
max-lease-time 43200;                               

authoritative;


'''
dic_mask = {
    '18':'255.255.192.0',
    '19':'255.255.224.0',
    '20':'255.255.240.0',
    '21':'255.255.248.0',
    '22':'255.255.252.0',
    '23':'255.255.254.0',
    '24':'255.255.255.0',
    '25':'255.255.255.128',
    '26':'255.255.255.192'
}

list_indices_with_int = []

list_inter_final = []

# ---- > Expressões Regulares < -------
re_interfaces = re.compile(r'(e.*\d+.*):')

re_ip_interface = re.compile(r'\d+:\s*(e.*):.*\n.*\n.*inet\s+(\d+\.\d+\.\d+\.\d+)/(\d+)\s+brd\s*(\d+\.\d+\.\d+\.\d+)')

# -------- ALGORITMO -------------------

# -- > Abre arquivo do comando ip a
with open('ipa', 'r') as f:
    text = f.read()

# -- > Armazena os dados do 'ip a' de todas as interfaces e coloca em lista 
list_text_ipa = re_ip_interface.findall(text)

# -- > Cria lista com o indice de todas interfaces com base em lista de interfaces definidas
for i, interface in enumerate(list_text_ipa):
    for item in interfaces:
        if re.search(item, interface[0]):
            list_indices_with_int.append(i)

# -- > Cria lista final com tupla com informações relevantes de cada interface definida
for i in list_indices_with_int:
    list_inter_final.append(list_text_ipa[i])

# --> Pega todos os valores das interfaces e inclui na variavel de texto padrão do dhcp.conf
t_int = len(list_inter_final)

for i, value in enumerate(list_inter_final):
    i += 1

    os.system('clear')
    eth = re.search(r'(e.*)@', value[0]).group(1)

    print(f'Configuração da interface {eth}')

    subnet, netmask, broad = get_network(value[1], dic_mask[value[2]])
    print(f'Interface {i}/{t_int}')

    print(f'Rede: {subnet}\nBroadcast: {broad}')

    rangeI = input('\nQual o primeiro IP do range?\n')
    rangeF = input('\nQual o último IP do range?\n')

    while True:
        user_input = input(f'\nO IP do TFTP e do NTP é {value[1]}? [s ou n]\n')

        if user_input == 's':
            ip_ntp = value[1]
            ip_tftp = value[1]
            break

        elif user_input == 'n':
            ip_ntp = input('\nInforme o IP do ntp:\n')
            ip_tftp = input('\nInforme o IP do tftp:\n')
            break
        else:
            print('Opçção incorreta. Pressione qualquer tecla para tentar novamente...')
            continue

print('\nDHCP foi configurado\n')
