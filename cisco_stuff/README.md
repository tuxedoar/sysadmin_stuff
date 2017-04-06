
## Descripción en Español

### switch-cmd-remoto.py

Este script, permite ejecutar varios comandos en diferentes switches administrables, por medio de SSH, ingresando las credenciales de acceso una única vez (asumiendo que las credenciales sean las mismas para todos los switches). Para su uso, se debe crear primero, un archivo de texto plano (un TXT, por ejemplo), que contenga la IP de cada switch (una por línea!). En este archivo, las líneas que comiencen con el caracter '#', serán ignoradas, por lo que puede utilizarse para incluír comentarios.   
<<<<<<< HEAD

Si bien este script fue pensado para usarse con switches administrables, debería funcionar con cualquier otro dispositivo que soporte el protocolo SSH!. 

#### ¿Cómo se usa?

##### Sintáxis

switch-cmd-remoto.py [OPCIONES]
=======
```
USO: switch-cmd-remoto.py [OPCIONES]
>>>>>>> 28a7d6ad85dd211bdabee2685518a6c2c05b0962

-u: Nombre de usuario     
-f [ARCHIVO]: Lee las IPs del archivo indicado. 
-c "comando1,comando2,comando3": Comando/s a ejecutar.
<<<<<<< HEAD

##### Ejemplo

switch-cmd-remoto.py -u fulano -f switches.txt -c "terminal length 0, sh port-security"
=======
```
Si bien este script fue pensado para usarse con switches administrables, debería funcionar con cualquier otro dispositivo que soporte el protocolo SSH!. 
>>>>>>> 28a7d6ad85dd211bdabee2685518a6c2c05b0962

--

## English description

This script, allows to execute various commands in different administrable switches through SSH, by giving access credentials once (assuming that credentials are the same for all the switches). For its usage, a plain text file (ie: a TXT file) must be created, containing the IP address of each switch (one IP per line). In such a file, lines starting with the '#' character will be ignored, so those can be used as comments.

<<<<<<< HEAD
Even though this script was aimed to be used with administrable switches, it should actually work with any other device that supports the SSH protocol!. 

#### How to use it?

##### Syntax

switch-cmd-remoto.py [OPTIONS]
=======
```
USAGE: switch-cmd-remoto.py [OPTIONS]
>>>>>>> 28a7d6ad85dd211bdabee2685518a6c2c05b0962

-u: User name.
-f [FILE]: text file that contains the IPs of the switches. 
-c "commmand1,command2,command3": Command/s to execute.
<<<<<<< HEAD
=======
``` 
Even though this script was aimed to be used with administrable switches, it should actually work with any other device that supports the SSH protocol!. 
>>>>>>> 28a7d6ad85dd211bdabee2685518a6c2c05b0962

##### Example

switch-cmd-remoto.py -u joe -f switches.txt -c "terminal length 0, sh port-security"
   

### copia-archivo-de-switch.py 

#### Descripción en Español

Modificacion del script "switch-cmd-remoto.py", para copiar el archivo de configuracion de varios switches administrables utilizando la operacion "scp" de SSH!.

REQUERIMIENTOS:
 * SSH configurado y habilitado en cada switch administrable.
 * SCP habilitado en cada switch: "ip scp server enable".
 * VER: https://github.com/jbardin/scp.py/raw/master/scp.py

--

#### English description

This is a derived script from the "switch-cmd-remoto.py", adapted to copy the config file of several switches, using the "scp" operation of SSH.  

REQUIREMENTS:
 * SSH configured and enabled in each switch.
 * SCP enabled in each switch: "ip scp server enable".
 * SEE: https://github.com/jbardin/scp.py/raw/master/scp.py 

