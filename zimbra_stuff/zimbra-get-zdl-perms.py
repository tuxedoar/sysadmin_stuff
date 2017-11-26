#!/usr/bin/env python
"""
This script allows to query which Zimbra accounts has 'sendToDistList' permissions over a certain Zimbra Distribution List. You can also list all (both dynamic and static) the Zimbra Distribution Lists available. 

--

Permite consultar las cuentas de Zimbra autorizadas a realizar envios en una lista de correo determinada. Tambien se pueden listar todas las listas de correo existentes.
"""

import ldap
import sys
import getopt

server = 'zimbra.undominio.com.ar'
who = 'uid=zimbra,cn=admins,cn=zimbra'
cred = 'clave_secreta'

id_autorizados = []
autorizados = []
listas = []

lista_elegida=''

l = ldap.open(server)
l.simple_bind_s(who, cred)

usuarios = l.search_s('ou=people,dc=undominio,dc=com,dc=ar', 
                   ldap.SCOPE_SUBTREE,
                   'objectClass=inetOrgPerson');

listas_dinamicas = l.search_s('cn=groups,dc=undominio,dc=com,dc=ar', 
                   ldap.SCOPE_SUBTREE,
                   'objectClass=zimbraGroup',
                   ['cn','zimbraACE']);
listas_estaticas =  l.search_s('ou=people,dc=undominio,dc=com,dc=ar', 
                   ldap.SCOPE_SUBTREE,
                   'objectClass=zimbraDistributionList',
                   ['uid','zimbraACE']);

# Obtengo entradas y atributos de los grupos
for i in listas_dinamicas:
        dn = i[0]
        attrs = i[1]
        
        lista = attrs['cn'][0]
        if 'zimbraACE' in attrs:
                idsauth = attrs['zimbraACE']

        for autorizado in idsauth:
                id_autorizados.append((lista, autorizado))

        listas.append(lista)

for i in listas_estaticas:
        dn = i[0]
        attrs = i[1]

        lista = attrs['uid'][0]
        if 'zimbraACE' in attrs: 
                idsauth = attrs['zimbraACE']

        for autorizado in idsauth:
                id_autorizados.append((lista, autorizado))

        listas.append(lista)

# Extraigo el ID de los usuarios con  permisos en la lista y los almaceno en una lista. 
def propiedades_lista(lista_elegida):
        # Valido la lista elegida!. 
        if lista_elegida in listas:
                pass
        else:
                print "La lista indicada NO existe!."
                sys.exit(2)
        for props in  id_autorizados:
                if lista_elegida in props:
                        if not '-sendToDistList' in props[1] and 'sendToDistList' in props[1]:
                                permiso = props[1].split(' ')
                                autorizado = permiso[0]
                                autorizados.append(autorizado)

# Con el ID obtenido de cada usuario, busco ese ID entre todos los usuarios y obtengo la identidad de cada uno!.                
def obtener_usuarios():
        print "\nCuentas autorizadas a realizar envios a " + lista_elegida + ": \n"             

        for item in usuarios:
                dn = item[0]
                attrs = item[1]
        
                for autorizado in autorizados:
                        if autorizado in attrs['zimbraId'] and 'uid' in attrs:
                                cuenta = attrs['uid']
                                print cuenta[0]
                                break

def ver_listas():
        for lista in listas:
                print lista

def uso():
        print """
        USO: zimbra-query-list-perms.py -l [LISTA]

        -l: Consulta los permisos para la lista de correo indicada.
        -L: Muestra un listado de las listas de correo existentes.        
        """

try:
        myopts, args = getopt.getopt(sys.argv[1:],"l:L")
except:
        print "Uso incorrecto!"
        uso()
        sys.exit(2)
        
for o, a in myopts:
        if o == '-l':
                lista_elegida=sys.argv[2]
                propiedades_lista(lista_elegida)
                obtener_usuarios()
        elif o == '-L':
                print "\nListas de correo disponibles:\n"
                ver_listas()
