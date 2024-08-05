import re, os



# ------- PATH DE ARQUIVOS ------------------
netplan_file = 'teste_file'
dhcp_conf = ''
isc_dhcpd = ''

# ----------- VARIÁVEIS ---------------------
# --> Expressões regulares
re_interfaces = re.compile(r'(en.+\..+):')

# --> Definição de variáveis
isc_dhcpd_text = '''INTERFACESv4="ens192.600 ens192.601 ens192.602 ens192.603 ens192.604 ens192.605"
INTERFACESv6=""'''

# ----------- ALGORÍTMO -----------------
with open(netplan_file, 'r') as f:
    text = f.read()

list_interfaces = re_interfaces.findall(text)

print(list_interfaces)
