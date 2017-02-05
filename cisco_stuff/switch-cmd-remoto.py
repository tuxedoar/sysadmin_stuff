#!/usr/bin/env python

# Permite ejecutar comandos de forma remota en switches u otros equipos, utilizando SSH!.
# It allows to execute several commands in different switches at once, using SSH. 

import paramiko
from time import sleep
import sys, re, getopt
import getpass
from socket import error

switches = []
user = ''
archivo = ''
cmd = []

def sesionSSH(user, cmd):

        # cmd lo toma como una lista con cada elemento separado, asi que los uno. 
        cmd = ' '.join(cmd)
        cmd = cmd.split(',')
        pw = getpass.getpass('\n Introduzca clave de acceso a los hosts: ')

        # Inicio sesion para cada una de las IP en la lista de switches
        for ip in switches:
                try:
                        print "\n Conexion a %s con el usuario %s ... \n" % (ip, user) 
                        sesion = paramiko.SSHClient()
                        sesion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        sesion.connect(ip, username=user, password=pw, look_for_keys=False, allow_agent=False, timeout=10)
                        timeout_modifier = 1.1  # wait 10% longer than usual

                        comando = sesion.invoke_shell()
                        sleep(2)
                        for c in cmd:
                                # Si las hay, remuevo comillas dobles!.
                                c = c.replace('\"','')
                                comando.send(c+'\n')

                        
                        # No funciona si no le doy 1 seg de retardo para el envio del comando!.
                        sleep(1)
                        # Tamanio del buffer de salida en bytes!.
                        salida = comando.recv(8000)

                        # Divido la salida 1 x linea y la guardo en una lista
                        salida = salida.splitlines()
                        # Ignoro las primeras 12 lineas (elementos de la lista)!.
#                       salida = salida[12:]
                        for lineas in salida:
                                print lineas


                except paramiko.ssh_exception.AuthenticationException, e:
                        print "Ocurrio un error de autenticacion al conectarse a %s : %s" % (ip, e)
                except paramiko.SSHException, e:
                        print "Ocurrio un error al conectarse  a %s : %s " % (ip, e)
                except error:
                        print "Expiro el tiempo de conexion!. Revise la conectividad con el host de destino!."          
                                        
def LeerArchivo(archivo):
# Leo el archivo, extraigo las IP y las almaceno en una lista.
        try:
                lectura = open(archivo, 'r')
                for linea in lectura.readlines():
                        linea=linea.strip()
                        if linea and not linea.startswith('#'):
                                valida = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", linea)
                                if not valida:
                                        print "ATENCION: Se ignora la IP %s por NO ser valida!" % (linea)
                                else:
                                        ip = linea
                                        switches.append(ip)
                
                lectura.close()
        except IOError:
                print "No se puede leer el archivo especificado!."
                uso()
                sys.exit(2)     
        except:
                uso()
                sys.exit(2)

def uso():
        print """
        USO: switch-cmd-remoto.py [OPCIONES]

        -u: Nombre de usuario       
        -f [ARCHIVO]: Lee las IPs de un archivo
        -c "comando1,comando2,comando3": Comando/s a ejecutar
        """

try:
        myopts, args = getopt.getopt(sys.argv[1:],"u:f:c:")
except:
        print "Uso incorrecto!"
        sys.exit(2)
        
for o, a in myopts:
        if o == '-u':
                user=sys.argv[2]
        elif o == '-f':
                archivo=sys.argv[4]
        elif o == '-c':
                cmd=sys.argv[6:]

LeerArchivo(archivo)
sesionSSH(user, cmd)
