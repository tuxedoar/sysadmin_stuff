#!/usr/bin/env python

'''
Modificacion del script "cmd-switch-remoto.py", para copiar el archivo de configuracion de varios switches administrables utilizando la operacion "scp" de SSH!.
--
Derived version of the "cmd-switch-remoto.py" script, aimed to copy the config file of several (administrable) switches using the "scp" operation of SSH.
'''
import paramiko
from scp import SCPClient
from time import sleep
import os, sys, re, getopt
import getpass
from socket import error
import warnings

switches = []
user = ''
archivo = ''

scp_target_file=''

def sesionSSH(user, scp_target_file):

#       Ignoro un warning introducido por el modulo scp !. 
        warnings.filterwarnings("ignore")
#       Declaro un contador para anexarlo al nombre de cada archivo que copio para que no se sobreescriban!. 
        cont = 0        
        pw = getpass.getpass('\n Introduzca clave de acceso a los hosts: ')

        # Inicio sesion para cada una de las IP en la lista de switches
        for ip in switches:
                try:
                        cont += 1
                        print "\n Conexion a %s con el usuario %s ... \n" % (ip, user) 
                        sesion = paramiko.SSHClient()
                        sesion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        sesion.connect(ip, username=user, password=pw, look_for_keys=False, allow_agent=False, timeout=10)
                        timeout_modifier = 1.1  # wait 10% longer than usual
                        
                        scp = SCPClient(sesion.get_transport())
                        print "Copiando archivo ", scp_target_file[0]
                        scp.get(scp_target_file)
                        sleep(1)
                        scp.close()     
                        # Renombro cada archivo copiado porque el modulo scp no lo soporta
                        new_filename = os.path.basename(scp_target_file[0])
                        # Convierto temporalmente el contador a cadena y lo vuelvo a convertir en entero, para que pueda luego seguir con el conteo!!.
                        cont = str(cont)
                        os.rename(new_filename, new_filename+'_'+cont)
                        cont = int(cont)                
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
        USO: scp-grab-file.py [OPCIONES]

        -u: Nombre de usuario       
        -f [ARCHIVO]: Lee las IPs de un archivo
        -t Archivo a copiar del host remoto
        """

try:
        myopts, args = getopt.getopt(sys.argv[1:],"u:f:t:")
except:
        print "Uso incorrecto!"
        sys.exit(2)
        
for o, a in myopts:
        if o == '-u':
                user=sys.argv[2]
        elif o == '-f':
                archivo=sys.argv[4]
        elif o == '-t':
                scp_target_file=sys.argv[6:]

LeerArchivo(archivo)
sesionSSH(user, scp_target_file)
