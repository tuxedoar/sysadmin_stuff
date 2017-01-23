#!/usr/bin/env python
# Quita el estado de 'pausa' en un servidor de impresión con CUPS.
# Quits the 'pause' state in a CUPS print server.

import cups 
import datetime

conn = cups.Connection ()
# Genera un diccionario con las impresoras y sus atributos
printers = conn.getPrinters () 

pending_jobs = conn.getJobs(which_jobs='not-completed')

# Listado de impresoras
for impresoras in printers:
        impresora = impresoras
        estado = printers[impresoras]['printer-state']
                             
        if estado != 5:
                pass
        else:
                for trabajos_pendientes in pending_jobs:
                        conn.cancelJob(trabajos_pendientes, purge_job=False)
                conn.enablePrinter(impresora)
