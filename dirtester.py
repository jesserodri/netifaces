#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo tenta encontrar 
  os arquivos ocultos em um site

  Modificado em 13 de dezembro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

# Importação das bibliotecas necessárias
import urllib2, argparse, sys

def host_test(filename, host):
    file = "dirtester.log" # Nome do arquivo a ser gerado
    bufsize = 0
    e = open(file, 'a', bufsize)
    print("[*] Lendo o arquivo %s") % (file)
    with open(filename) as f:
        locations = f.readlines()
    for item in locations:
        target = host + "/" + item
        try:
            request = urllib2.Request(target)
            request.get_method = lambda : 'GET'
            response = urllib2.urlopen(request)
        except:
            print("[-] %s é inválido") % (str(target.rstrip('\n')))
            response = None
        if response != None:
            print("[+] %s é válido") % (str(target.rstrip('\n')))
            details = response.info()
            e.write(str(details))
    e.close()

def main():
    usage = '''modo de usar: %(prog)s [-t http://127.0.0.1] [-f wordlist] -q -v -vv -vvv'''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-t", action="store", dest="target", default=None, help="Host para testar")
    parser.add_argument("-f", action="store", dest="filename", default=None, help="Nome do arquivo de diretórios ou páginas a serem testados")
    parser.add_argument("-v", action="count", dest="verbose", default=1, help="Nível de verbosidade, padrão para um, este produz cada comando e resultado")
    parser.add_argument("-q", action="store_const", dest="verbose", const=0, help="Define os resultados como silenciosos")
    parser.add_argument('--version', action='version', version='%(prog)s 0.42b')
    args = parser.parse_args()

    # Validator de Argumento
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if (args.target == None) or (args.filename == None):
        parser.print_help()
        sys.exit(1)

    # Definir Construtores
    verbose = args.verbose     # Nível de verbosidade
    filename = args.filename   # Os dados a usar para o ataque de dicionário
    target = args.target       # Senha ou hash para testar contra padrão é admin

    host_test(filename, target)

if __name__ == '__main__':
    main()
