from requests import *
from base64 import b64encode
from random import randint
from sys import argv
from time import time, sleep


# Endereço do Gateway
url = "http://192.168.0.1"
username = "NET_F2AA58"
password = "passhere"

# Headers da requisição
header = {
    "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://192.168.0.1/router.html"
}

ip = argv[1].split(".") # Separando os campos do IP pelos pontos(.)
oid = "1.3.6.1.4.1.4115.1.20.1.1.4.8.0=%24" + '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip)) + ";4;" # Parâmetro oid, onde leva também como parâmetro cada campo do IP em Hex
_n = str(randint(10000000, 99999999)) # Parâmetro _n é um número aleatório de 8 dígitos.
arg = b64encode(bytes("{}:{}".format(username, password), "utf-8")) # Parâmetro arg que é o campo do usuário e senha separados por um ":"
s = Session() # Inicia uma sessão
login = s.get("http://192.168.0.1/login?arg="+arg.decode("utf-8")+"=&_n="+_n+"&_=" + str(int(time() * 1000))) # Efetua Login
credential = login.content.decode('utf-8') # Página de login retorna as credenciais criptografada
cookies = {"credential" : credential} # Criando um dict que será usado como cookie. Esse dict carrega o campo credencial com o valor retornado na resposta da página de login.
c = s.get("http://192.168.0.1/snmpGet?oids=1.3.6.1.4.1.4115.1.20.1.1.5.14.0;&_n="+_n+"&_="+  str(int(time() * 1000)), cookies=cookies)# Pegando snmp
f = s.get("http://192.168.0.1/snmpSet?oid="+ oid +"&_n=" + _n + "&_=" + str(int(time() * 1000)), headers=header, cookies=cookies) # Requisição para alterar o DMZ, carregado dos cookies com credenciais e os headers

