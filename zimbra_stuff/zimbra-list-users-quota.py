#!/usr/bin/env python

"""
It generates a list with the size of the quota and its usage, of each zimbra account. Before using this script, you must generate a temporal list with the following command:

zmprov gqu `zmhostname`|awk {'print " "$3" "$2" "$1'} > list-quotas.txt

--

Genera un listado con el espacio total y el usado de cada casilla de Zimbra (Open Source Edition).
Se debe generar un listado previo con el siguiente comando (recordar usar el usuario apropiado - ej: zimbra):

zmprov gqu `zmhostname`|awk {'print " "$3" "$2" "$1'} > listado-quotas.txt

"""

import sys

try:
        archivo = open('listado-quota.txt', 'r')

        print "CUENTA,USADO,TOTAL"

        for linea in archivo.readlines():
                linea=linea.split(' ')
                linea.pop(0)

                usado = linea[0]
                usado = float(usado)
                usado = usado/1024.00/1024.00

                total = linea[1]
                total = float(total)
                total = total/1024.00/1024.00

                cuenta = linea[2]
                cuenta = cuenta.strip('\n')

                print "%s,%.2f MB,%.2f MB" % (cuenta, usado, total)

        archivo.close()
except:
        print "Ocurrio un error al generar el listado. Asegurarse que el archivo exista o tenga el formato correcto!." 
