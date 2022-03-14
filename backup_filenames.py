#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz escaneamento 
  de portas abertas em um range de 
  endereços IP's

  Modificado em 15 de dezembro de 2016
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

# Importa as bibliotecas necessárias
import socket, sys

def main():
	ports = [21,23,22]  #  Quais portas você quer testar
	ips = "192.168.1."  # Range de endereços IP's
	for octet in range(0,255):
		for port in ports:
			ip = ips + str(octet)
			#print("[*] Testando a porta %s no IP %s") % (port, ip)
			try:
				socket.setdefaulttimeout(1)
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((ip,port))
				output = s.recv(1024)
				print("[+] O banner: %s para o IP: %s na Porta: %s") % (output,ip,port)
			except KeyboardInterrupt:  # Para interromper o programa aperte Crtl+C
				print 'Programa Interrompido'
				sys.exit()
			except:
				print("[-] Falha ao conectar-se a %s:%s") % (ip, port)
			finally:
				s.close()
		

if __name__ == "__main__":
	main()






