#!/usr/bin/env python

"""
Copyright 2018 by tuxedoar@gmail.com .

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

DESCRIPTION

This script allows to query permissions that Zimbra accounts have over a given 
Zimbra Distribution List (ZDL). You can also list all 
the ZDLs available (both dynamic and static).

"""

import argparse
import ldap
import sys
import getpass

authorized_id = []
authorized_accounts = []
sendas_auth_accounts = []
lists = []

class MenuHandler:
  parser = argparse.ArgumentParser(
      description='Query Zimbra Distribution Lists - ZDL')
  parser.add_argument('-s', '--server', required=True, action='store', 
                      help='IP address or domain name of the Zimbra server')
  parser.add_argument('-b', '--basedn', required=True, action='store',
                      help='Specify the searchbase or base DN of the Zimbra LDAP server')
  parser.add_argument('-u', '--userdn', required=True, action='store',
                      help='DN admin user of the Zimbra LDAP server')
  parser.add_argument('-l', '--zdlperms', required=False, action='store',
                      help='Query which Zimbra accounts have permissions to send mails to the given ZDL')
  parser.add_argument('-sa', '--sendas', required=False, action='store_true',
                      help="Query which Zimbra accounts have the 'send as' permission to send mails on behalf of the existing ZDLs")
  parser.add_argument('-L', '--zdllists', required=False, action='store_true',
                      help='List both static and dynamic existing ZDLs')
  args = parser.parse_args()

  # Check if optional (but still either of them mandatory) arguments are present. 
  if args.zdlperms or args.zdllists or args.sendas:
    try:
      pw = getpass.getpass('\nPlease, enter your Zimbra credentials: ')
    except KeyboardInterrupt:
      print "\nExecution has been interrupted!."
      sys.exit()
  else:
    parser.print_help()
    sys.exit()
   

class LDAPhandler(MenuHandler):

  a = MenuHandler()
  
  server = a.args.server
  ldapadmin = a.args.userdn
  basedn = a.args.basedn

  try:
    l = ldap.open(server)
    l.simple_bind_s(ldapadmin, a.pw)
  except ldap.UNWILLING_TO_PERFORM, e:
    print "ERROR - %s . %s " % (e[0]['info'], e[0]['desc'])
    sys.exit()
  except ldap.INVALID_CREDENTIALS, e:
    print "ERROR - %s " % (e[0]['desc'])
    sys.exit()

  groupsBaseDN = "cn=groups,"+basedn   
  peopleBaseDN = "ou=people,"+basedn   

  users = l.search_s(peopleBaseDN, 
                   ldap.SCOPE_SUBTREE,
                   'objectClass=inetOrgPerson');
    
  dynamic_lists = l.search_s(groupsBaseDN, 
                       ldap.SCOPE_SUBTREE,
                       'objectClass=zimbraGroup',
                       ['cn','zimbraACE']);

  static_lists =  l.search_s(peopleBaseDN, 
                   ldap.SCOPE_SUBTREE,
                   'objectClass=zimbraDistributionList',
                   ['uid','zimbraACE']);


def main():

  m = LDAPhandler()
  server = m.args.server
  basedn = m.args.basedn
  ldapadmin = m.args.userdn

  getLists()

  if m.args.zdlperms:
    chosen_list = m.args.zdlperms
    list_properties(chosen_list)
    get_users()
  elif m.args.zdllists:
    get_lists()
  elif m.args.sendas:
    getLists()
    sendAsPermissions()
  else:
    pass

def getLists():
  L = LDAPhandler()
  dynamic_lists = L.dynamic_lists
  static_lists = L.static_lists
  # Get entries and attributes of groups.
  for i in dynamic_lists:
    dn = i[0]
    attrs = i[1]
        
    list = attrs['cn'][0]
    idsauth = attrs.get('zimbraACE','')
    for authorized in idsauth:
      authorized_id.append((list, authorized))
    lists.append(list)

  for i in static_lists:
    dn = i[0]
    attrs = i[1]

    list = attrs['uid'][0]
    idsauth = attrs.get('zimbraACE','')
    for authorized in idsauth:
      authorized_id.append((list, authorized))
    lists.append(list)

# Extract users IDs with permissions on the ZDL and store them on a list
def list_properties(chosen_list):
  # Check if chosen list is valid. 
  if chosen_list in lists:
    pass
  else:
    print "The list %s doesn't exist!." % (chosen_list)
    sys.exit(2)
  for props in authorized_id:
    if chosen_list in props:
      if not '-sendToDistList' in props[1] and 'sendToDistList' in props[1]:
        permission = props[1].split(' ')
        authorized = permission[0]
        authorized_accounts.append(authorized)


# With each gathered user ID, search those, among all the users and get their identities!.   
def get_users():
  u = LDAPhandler()
  users = u.users
  chosen_list = u.args.zdlperms
  print "\nAuthorized accounts to send mails to %s :\n " % (chosen_list)             

  for item in users:
    dn = item[0]
    attrs = item[1]
        
    for authorized in authorized_accounts:
      if authorized in attrs['zimbraId'] and 'uid' in attrs:
        account = attrs['uid']
        print account[0]
        break

def sendAsPermissions():
  u = LDAPhandler()
  users = u.users
  chosen_list = u.args.zdlperms
  print "Send as permissions:\n"             

  # Get 'Send as' permissions and store them on a list.
  for props in authorized_id:
    if 'sendAsDistList' in props[1]:
      sendasPerm = props[1].split(' ')
      sendasPermAuth = sendasPerm[0]
      sendas_auth_accounts.append((props[0], sendasPermAuth))

  for item in users:
    dn = item[0]
    attrs = item[1]

    for authorized in sendas_auth_accounts:
      if authorized[1] in attrs['zimbraId'] and 'uid' in attrs:
        account = attrs['uid']
        print "The user %s has the 'send as' permission for the list %s" % (account[0], authorized[0])
        break

def get_lists():
  for list in lists:
    print list

if __name__ == "__main__":
  main()
