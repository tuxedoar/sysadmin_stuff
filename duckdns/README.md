
## Descripción en Español

### duckdns-update-ip.py

Este script, te permite mantener tu dirección IP pública actualizada, con el servicio "duckdns". Ver: https://www.duckdns.org/ .  

##### Sintáxis
```
usage: duckdns-update-ip.py [-h] -f FILE

Update your IP address for your duckdns registered domain

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The configuration file to use
```
Se recomienda para su uso, crear una tarea diaria de cron!. 

##### Archivo de configuración

Se debe crear, previo a su uso, un archivo de configuración, tal como se muestra en el siguiente ejemplo:
```
[duckdns]
token = [TU_TOKEN]
domain = [TU_DOMINIO]

```

--

## English description

### duckdns-update-ip.py

This script allows you to keep your public IP address updated, when using the "duckdns" service. See: https://www.duckdns.org/ .  

##### Syntax
```
usage: duckdns-update-ip.py [-h] -f FILE

Update your IP address for your duckdns registered domain

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The configuration file to use
```
For its usage, it's recommended to create a daily cron job!.

##### Configuration file
Prior to its usage, a configuration file must be created, as shown in the following example:
```
[duckdns]
token = [YOUR_TOKEN]
domain = [YOUR_DOMAIN]

```
