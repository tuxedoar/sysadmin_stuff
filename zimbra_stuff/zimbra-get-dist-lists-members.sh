#!/bin/bash
# Genera un archivo .txt por cada lista de correo de Zimbra (ya sea estática o dinámica) y lista en el archivo todos sus miembros!.
# It generates a .txt file per each Zimbra distribution List (both static and dynamic) and so it list all its members on each file. 

LISTAS=$(/opt/zimbra/bin/zmprov gadl)
NOMBRES_LISTAS=$(/opt/zimbra/bin/zmprov gadl | cut -d@ -f1)

for lista in [$LISTAS];
        do
                estaticas=$(echo $lista | tr -d "[]")

                for estatica in [$estaticas];
                        do
                                /opt/zimbra/bin/zmprov gdl $estaticas > /opt/zimbra/consultas/$(echo $lista | cut -d@ -f1 | tr -d "[]").txt
                        done

        done
