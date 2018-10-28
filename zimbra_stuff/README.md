
## zimbra-get-zdl-perms.py

This script allows to query permissions that Zimbra accounts have over a given 
Zimbra Distribution List (ZDL). You can also list all the existing ZDLs (both dynamic and static).  

Note that, in order for this script to work, you need to [setup the LDAP admin user](https://wiki.zimbra.com/wiki/Setting_zimbra_admin_password_in_LDAP), 
on your Zimbra server. Also, make sure to have the  [python-ldap](https://pypi.python.org/pypi/python-ldap/) package installed on it.     

#### How to use it?

##### Syntax

```
usage: zimbra-get-zdl-perms.py [-h] -s SERVER -b BASEDN -u USERDN
                               [-l ZDLPERMS] [-sa] [-L]

Query Zimbra Distribution Lists - ZDL

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        IP address or domain name of the Zimbra server
  -b BASEDN, --basedn BASEDN
                        Specify the searchbase or base DN of the Zimbra LDAP
                        server
  -u USERDN, --userdn USERDN
                        DN admin user of the Zimbra LDAP server
  -l ZDLPERMS, --zdlperms ZDLPERMS
                        Query which Zimbra accounts have permissions to send
                        mails to the given ZDL
  -sa, --sendas         Query which Zimbra accounts have the 'send as'
                        permission to send mails on behalf of the existing
                        ZDLs
  -L, --zdllists        List both static and dynamic existing ZDLs 
```
Note that the following arguments are mandatory:
 * `--server` / `-s`
 * `--basedn` / `-b`
 * `--userdn` / `-u`
In addition, you must specify either of these two options: 
 * `--zdlperms` / `-l` 
 * `--zdllists` / `-L` 
Otherwise, this script won't work!.   

##### Example
Query which Zimbra accounts have permissions to send mails to a ZDL ("Zimbra Distribution Lists") named "my-zdl-list":
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -l my-zdl-list
```
Query which Zimbra accounts have the "send as" permission over the ZDLs:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -sa
```
List all the existing ZDLs:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -L
```

## Descripción en Español

### zimbra-get-zdl-perms.py

Este script, permite consultar los permisos que las cuentas Zimbra tienen sobre una determinada "Zimbra Distribution List" (ZDL). También se 
pueden listar todas las ZDLs existentes (tanto dinámicas como estáticas).  

Para que este script funcione, se debe configurar el [usuario admin de LDAP](https://wiki.zimbra.com/wiki/Setting_zimbra_admin_password_in_LDAP), 
en el servidor de Zimbra. Además, asegurarse de tener instalado el paquete  [python-ldap](https://pypi.python.org/pypi/python-ldap/) en el servidor. 

#### ¿Cómo se usa?

##### Sintáxis
```
usage: zimbra-get-zdl-perms.py [-h] -s SERVER -b BASEDN -u USERDN
                               [-l ZDLPERMS] [-sa] [-L]

Query Zimbra Distribution Lists - ZDL

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        IP address or domain name of the Zimbra server
  -b BASEDN, --basedn BASEDN
                        Specify the searchbase or base DN of the Zimbra LDAP
                        server
  -u USERDN, --userdn USERDN
                        DN admin user of the Zimbra LDAP server
  -l ZDLPERMS, --zdlperms ZDLPERMS
                        Query which Zimbra accounts have permissions to send
                        mails to the given ZDL
  -sa, --sendas         Query which Zimbra accounts have the 'send as'
                        permission to send mails on behalf of the existing
                        ZDLs
  -L, --zdllists        List both static and dynamic existing ZDLs
```
Notar que los siguientes argumentos son obligatorios:
 * `--server` / `-s`
 * `--basedn` / `-b`
 * `--userdn` / `-u`
De forma adicional, se debe especificar cualquiera de las opciones siguientes: 
 * `--zdlperms` / `-l` 
 * `--zdllists` / `-L` 
De lo contrario, este script no funcionará!.   



##### Ejemplo
Consultar qué cuentas de Zimbra tienen permisos para envíar correos a una ZDL denominada "mi-lista":
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -l mi-lista
```
Consultar qué cuentas de Zimbra tienen el permiso "send as" ("envíar en nombre de...") sobre las ZDLs:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -sa 
```
Listar todas las ZDLs existentes:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -L
```
