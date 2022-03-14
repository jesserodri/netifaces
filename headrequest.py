#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz o testes de portas
  abertas, mais especificamente na porta
  80

  Modificado em 13 de dezembro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

# Importação das bibliotecas necessárias
import urllib2, argparse, sys

def host_test(filename):
    file = "headrequests.log" # Nome do arquivo a ser gerado
    bufsize = 0
    e = open(file, 'a', bufsize)
    print("[*] Lendo o arquivo %s") % (file)
    with open(filename) as f:
        hostlist = f.readlines()
    for host in hostlist:
        print("[*] Testando %s") % (str(host))
        target = "http://" + host
        target_secure = "https://" + host
        try:
            request = urllib2.Request(target)
            request.get_method = lambda : 'HEAD'
            response = urllib2.urlopen(request)
        except:
            print("[-] Nenhum servidor web em %s") % (str(target))
            response = None
        if response != None:
            print("[*] Resposta de %s") % (str(target))
            print(response.info())
            details = response.info()
            e.write(str(details))
        try:
            request_secure = urllib2.urlopen(target_secure)
            request_secure.get_method = lambda : 'HEAD'
            response_secure = urllib2.urlopen(request_secure)
        except:
            print("[-] Nenhum servidor web em %s") % (str(target_secure))
            response_secure = None
        if response_secure != None:
            print("[*] Resposta de %s") % (str(target_secure))
            print(response_secure.info())
            details = response_secure.info()
            e.write(str(details))
    e.close()

def main():
    # Se o script for executado no CLI
    usage = '''usage: %(prog)s [-t hostfile] -q -v -vv -vvv'''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-t", action="store", dest="targets", default=None, help="Nome do arquivo para testarem os hosts")
    parser.add_argument("-v", action="count", dest="verbose", default=1, help="Nível de verbosidade, padrão para um, este produz cada comando e resultado")
    parser.add_argument("-q", action="store_const", dest="verbose", const=0, help="Define os resultados como silenciosos")
    parser.add_argument('--version', action='version', version='%(prog)s 0.42b')
    args = parser.parse_args()

    # Validator Argumento
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if (args.targets == None):
        parser.print_help()
        sys.exit(1)

    verbose = args.verbose       # Nível de Verbosidade
    targets = args.targets       # Senha ou hash para testar contra padrão é admin

    host_test(targets)

if __name__ == '__main__':
    main()
