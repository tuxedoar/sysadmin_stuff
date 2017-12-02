
## zimbra-get-zdl-perms.py

This script allows to query which Zimbra accounts have permissions to send mails to a certain Zimbra Distribution List (ZDL). You can also 
list all the existing ZDLs (both dynamic and static).  

Note that, in order for this script to work, you need to [setup the LDAP admin user](https://wiki.zimbra.com/wiki/Setting_zimbra_admin_password_in_LDAP), 
on your Zimbra server. Also, make sure to have the  [python-ldap](https://pypi.python.org/pypi/python-ldap/) package installed on it.     

#### How to use it?

##### Syntax

```
Add help on usage here, later. 
```
Note that arguments such as `-s` (server), `-b` (basedn) and `-u` (admin LDAP user) , are mandatory when using this script!. Plus, you must specify either 
of the `-l` or `-L` arguments. Otherwise, it won't work!.    

##### Example
Query which Zimbra accounts have permissions to send mails to a ZDL named "my-zdl-list":
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -l my-zdl-list
```
List all the existing ZDLs:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -L
```

## Descripción en Español

### zimbra-get-zdl-perms.py

Este script, permite consultar qué cuentas de Zimbra tienen permisos para envíar correos a una determinada "Zimbra Distribution List" (ZDL). También se 
pueden listar todas las ZDLs existentes (tanto dinámicas como estáticas).  

Para que este script funcione, se debe configurar el [usuario admin de LDAP](https://wiki.zimbra.com/wiki/Setting_zimbra_admin_password_in_LDAP), 
en el servidor de Zimbra. Además, asegurarse de tener instalado el paquete  [python-ldap](https://pypi.python.org/pypi/python-ldap/) en el servidor. 

#### ¿Cómo se usa?

##### Sintáxis
```
Add help on usage here, later
```
Notar que los argumentos `-s` (server), `-b` (basedn) y `-u` (usuario admin de LDAP) , son obligatorios para utlizar este script!. Además, se debe utilizar 
cualquiera de los argumentos `-l` ó `-L`. De lo contrario, no funcionará!.

##### Ejemplo
Consultar qué cuentas de Zimbra tienen permisos para envíar correos a una ZDL denominada "mi-lista":
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -l mi-lista
```
Listar todas las ZDLs existentes:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -L
```
