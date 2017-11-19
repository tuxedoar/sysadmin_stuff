
## switch-cmd-manager.py

This script, allows to execute various commands in different managed switches through SSH, by giving access credentials once (assuming that credentials are the same for all the switches). For its usage, a plain text file (ie: a TXT file) must be created, containing the IP address of each switch (one IP per line). In such a file, lines starting with the '#' character will be ignored, so those can be used as comments.

Even though this script was aimed to be used with managed switches, it should actually work with any other device that supports the SSH protocol!. 

#### How to use it?

##### Syntax

```
usage: switch-cmd-manager.py [-h] -f FILE -u USER -c COMMANDS [-p PORT]

Exceute remote commands on several managed switches or servers.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Plain text file with list of hosts
  -u USER, --user USER  User to login on remote hosts
  -c COMMANDS, --commands COMMANDS
                        Comma separated commands to be executed on remote
                        hosts
  -p PORT, --port PORT  Specify SSH port to connect to hosts
```

##### Example
```
switch-cmd-manager.py -u joe -f switches.txt -c "terminal length 0, sh port-security"
```

## Descripción en Español

### switch-cmd-remoto.py

Este script, permite ejecutar varios comandos en diferentes switches administrables, por medio de SSH, ingresando las credenciales de acceso una única vez (asumiendo que las credenciales sean las mismas para todos los switches). Para su uso, se debe crear primero, un archivo de texto plano (un TXT, por ejemplo), que contenga la IP de cada switch (una por línea!). En este archivo, las líneas que comiencen con el caracter '#', serán ignoradas, por lo que puede utilizarse para incluír comentarios.   

Si bien este script fue pensado para usarse con switches administrables, debería funcionar con cualquier otro dispositivo que soporte el protocolo SSH!. 

#### ¿Cómo se usa?

##### Sintáxis
```
usage: switch-cmd-manager.py [-h] -f FILE -u USER -c COMMANDS [-p PORT]

Exceute remote commands on several managed switches or servers.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Plain text file with list of hosts
  -u USER, --user USER  User to login on remote hosts
  -c COMMANDS, --commands COMMANDS
                        Comma separated commands to be executed on remote
                        hosts
  -p PORT, --port PORT  Specify SSH port to connect to hosts
```

##### Ejemplo

switch-cmd-manager.py -u fulano -f switches.txt -c "terminal length 0, sh port-security"


### copia-archivo-de-switch.py 

#### Descripción en Español

Modificacion del script original, "switch-cmd-remoto.py", para copiar el archivo de configuracion de varios switches administrables utilizando la
operacion "scp" de SSH!.

REQUERIMIENTOS:
 * SSH configurado y habilitado en cada switch administrable.
 * SCP habilitado en cada switch: "ip scp server enable".
 * VER: https://github.com/jbardin/scp.py/raw/master/scp.py

--

#### English description

This is a derived script from the original, "switch-cmd-remoto.py", adapted to copy the config file of several managed switches, using the "scp" operation of SSH.  

REQUIREMENTS:
 * SSH configured and enabled in each switch.
 * SCP enabled in each switch: "ip scp server enable".
 * SEE: https://github.com/jbardin/scp.py/raw/master/scp.py 

