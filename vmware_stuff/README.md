
## Descripción en Español

### vmware-get-vms-info-from-servers.py

Este script en Python tiene como objetivo listar información básica de VMs contenidas en hosts ESX o en vCenter. La idea es evitar
tener que ingresar las mismas credenciales para cada uno de ellos, repetidas veces. Se debe especificar una lista de hosts en un
archivo txt, con una dirección IP por línea. Se asume que las credenciales a usar, son las mismas para todos los hosts!.  

Este script, está basado en el siguiente código: 

https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/getallvms.py
https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/list_datastore_info.py


#### Requisitos previos

Para que este script funcione, se debe tener instalado el SDK de Python para la API de VMware vSphere!. Ver:

https://github.com/vmware/pyvmomi


#### Forma de uso

Ejemplo de uso:
```
./vmware-get-vms-info-from-servers.py -u root -f servers.txt
```

--


## English description

### vmware-get-vms-info-from-servers.py

This Python script is aimed for listing the VMs and retrieve basic info about them,
from a list of ESX / vCenter hosts. The main idea is to avoid having to enter the same
credentials for each of those, repeatedly. A list of hosts must be specified in a txt file,
with one IP address per line!. It's assumed that credentials to be used, are the same for all
the hosts!. 

This script is based on the following pieces of code:

https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/getallvms.py
https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/list_datastore_info.py

#### Prerequisites

In order for this script to work, you must have the Python SDK for the VMware vSphere API installed!. See:

https://github.com/vmware/pyvmomi

#### Usage

Usage example:
```
./vmware-get-vms-info-from-servers.py -u root -f servers.txt
```


