#!/usr/bin/python
# Establece la cuota de correo en 50MB a usuarios que tengan menos que esa cifra!.
# Change the IMAP quota for those users that have less than 50MB.

import cyruslib
imap = cyruslib.CYRUS()
imap.login("manager", "pass")

for usuarios in imap.lm("user/%"):
       try:
               cuota = imap.lq(usuarios)
               if cuota[1] < 52000:
                       imap.sq(usuarios, "52000")
       except cyruslib.CYRUSError:
                       continue
