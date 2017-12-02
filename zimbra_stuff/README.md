
## zimbra-get-zdl-perms.py

This script allows to query which Zimbra accounts have permissions to send mails to a certain Zimbra Distribution List (ZDL). You can also 
list all the existing ZDLs (both dynamic and static).  

#### How to use it?

##### Syntax

```
Add help on usage here, later. 
```

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

#### ¿Cómo se usa?

##### Sintáxis
```
Add help on usage here, later
```

##### Ejemplo
Consultar qué cuentas de Zimbra tienen permisos para envíar correos a una ZDL denominada "mi-lista":
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -l mi-lista
```
Listar todas las ZDLs existentes:
```
./zimbra-get-zdl-perms.py -s zimbra.mydomain.com -b dc=mydomain,dc=com -u uid=zimbra,cn=admins,cn=zimbra -L
```
