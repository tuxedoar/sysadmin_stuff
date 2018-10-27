#!/usr/bin/env python

# Copyright 2018 by tuxedoar@gmail.com .

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# DESCRIPTION

# This script allows you to query an LDAP server, based on a custom set of
# provided attributes. The results are given in CSV format, though they
# are not written to a CSV file unless explicitly specified.   

# ACKNOWLEDGMENT

# The pieces of code that implement LDAP queries with paged controls in this script, 
# are based on this Python snippet:
# 
# https://gist.github.com/mattfahrner/c228ead9c516fc322d3a#file-python-paged-ldap-snippet-2-4-py   

import argparse
import sys
import getpass
import ldap
from ldap.controls import SimplePagedResultsControl
from distutils.version import LooseVersion
import csv

class MenuHandler:
  parser = argparse.ArgumentParser(
      description='Get a CSV formatted list from an LDAP database, given a custom set of provided attributes.')
  parser.add_argument('-s', '--server', required=True, action='store', 
                      help='URI formatted address (IP or domain name) of the LDAP server')
  parser.add_argument('-b', '--basedn', required=True, action='store',
                      help='Specify the searchbase or base DN of the LDAP server')
  parser.add_argument('-u', '--userdn', required=False, action='store',
                      help='Distinguished Name (DN) of the user to bind to the LDAP directory')
  parser.add_argument('-a', '--userAttrs', required=True, action='store',
                      help='A set of comma separated LDAP attributes to list')
  parser.add_argument('-S', '--sizelimit', required=False, action='store',
                      help='Specify the maximum number of LDAP entries to display (Default: 500)')
  parser.add_argument('-f', '--filter', required=False, action='store',
                      help="Specify an LDAP filter (Default: 'objectClass=*')")
  parser.add_argument('-w', '--writetocsv', required=False, action='store',
                      help="Write results to a CSV file!.")

  # If no arguments are given, show the help!.
  if len(sys.argv[1:])==0:
    parser.print_help()
    sys.exit(1)


class LDAPhandler(MenuHandler):

  # Check if we're using the Python "ldap" 2.4 or greater API
  LDAP24API = LooseVersion(ldap.__version__) >= LooseVersion('2.4')

  ldapOptions = {'PAGESIZE':'500','SEARCHFILTER':'objectClass=*'}

  m = MenuHandler()
  args = m.parser.parse_args()
  
  server = args.server
  ldapadmin = args.userdn
  basedn = args.basedn
  userAttrs = args.userAttrs
  sizelimit = args.sizelimit
  filter = args.filter

  ATTRLIST = userAttrs.split(",") 

  if sizelimit != None:
    ldapOptions['PAGESIZE'] = sizelimit
  if filter != None:
    ldapOptions['SEARCHFILTER'] = filter

  ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
  ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
  ldap.set_option(ldap.OPT_REFERRALS, 0)

  l = ldap.initialize(server)


def LDAPsession():
  m = MenuHandler()
  args = m.parser.parse_args()

  lsession = LDAPhandler()

  server = args.server
  ldapadmin = args.userdn

  try:
    # If no '-u' argument is present, perform an anonymous LDAP query!.
    if ldapadmin:
      ask_creds = getpass.getpass('\nPlease, enter your LDAP credentials: ')
      LDAPConnection = lsession.l.simple_bind_s(ldapadmin, ask_creds)
      if LDAPConnection:
        print("\nSuccessful LDAP authentication!\n")
    else:
      print("\nWARNING: No user identity was given. Performing an anonymous query!\n")
  except ldap.SERVER_DOWN as e:
    print("ERROR - %s") % (e[0]['desc'])
  except ldap.UNWILLING_TO_PERFORM as e:
    print("ERROR - %s . %s ") % (e[0]['info'], e[0]['desc'])
    sys.exit()
  except ldap.INVALID_CREDENTIALS as e:
    print("ERROR - %s ") % (e[0]['desc'])
    sys.exit()
  except ldap.SIZELIMIT_EXCEEDED as e:
    print("ERROR - %s ") % (e[0]['desc'])
    sys.exit()

   
def create_controls(pagesize):
  """Create an LDAP control with a page size of "pagesize"."""
  # Initialize the LDAP controls for paging. Note that we pass ''
  # for the cookie because on first iteration, it starts out empty.
  lconn = LDAPhandler()
  if lconn.LDAP24API:
    return SimplePagedResultsControl(True, size=pagesize, cookie='')
  else:
    return SimplePagedResultsControl(ldap.LDAP_CONTROL_PAGE_OID, True,
      (pagesize,''))

def get_pctrls(serverctrls):
  """Lookup an LDAP paged control object from the returned controls."""
  # Look through the returned controls and find the page controls.
  # This will also have our returned cookie which we need to make
  # the next search request.
  lconn = LDAPhandler()

  if lconn.LDAP24API:
    return [c for c in serverctrls
             if c.controlType == SimplePagedResultsControl.controlType]
  else:
    return [c for c in serverctrls
             if c.controlType == ldap.LDAP_CONTROL_PAGE_OID]


def set_cookie(lc_object, pctrls, pagesize):
  """Push latest cookie back into the page control."""
  lconn = LDAPhandler()

  if lconn.LDAP24API:
    cookie = pctrls[0].cookie
    lc_object.cookie = cookie
    return cookie
  else:
    est, cookie = pctrls[0].controlValue
    lc_object.controlValue = (pagesize,cookie)
    return cookie


# This is essentially a placeholder callback function. You would do your real
# work inside of this. Really this should be all abstracted into a generator...
def process_entry(dn, attrs):
  """Process an entry. The two arguments passed are the DN and
     a dictionary of attributes."""

  lconn = LDAPhandler()
  userAttrs = lconn.ATTRLIST
  
  # Collect attributes that were previously selected by the user!.   
  collectedUserAttrs = []
  # Grab LDAP objects inside 'attrs', only IF they are a python list!. Then, 
  # for each LDAP entry, check if every user selected attribute, is present. If not,
  # a zero value will be placed, which is then used to determine if such attribute is
  # present. If yes, it's gonna be stored on the 'collectedUserAttrs' list!. 
  if isinstance(attrs, dict):
    for attr in userAttrs:
      attr = attrs.get(attr, 0) 
      if attr != 0:
        collectedUserAttrs.append(attr[0])
      else:
        collectedUserAttrs.append('NULL')
  
  print(','.join(collectedUserAttrs))


def writetoCSV(dn, attrs):
  """ Write retrieved results to a CSV file """
  lconn = LDAPhandler()
  userAttrs = lconn.ATTRLIST

  m = MenuHandler()
  args = m.parser.parse_args()
  
  # Collect attributes that were previously selected by the user!.   
  collectedUserAttrs = []
  # User selected attrs to be written to the CSV header.
  # user_attrs = lconn.userAttrs.split(',')
  # The same as in ldap_paging function, but to write results to a CSV file!. 
  if isinstance(attrs, dict):
    for attr in userAttrs:
      attr = attrs.get(attr, 0) 
      if attr != 0:
        collectedUserAttrs.append(attr[0])
      else:
        collectedUserAttrs.append('NULL')

  with open(args.writetocsv, 'a') as file:
    writer = csv.writer(file)
    writer.writerow(collectedUserAttrs)


def ldap_paging():

  # Necessary to write to CSV!. 
  m = MenuHandler()
  args = m.parser.parse_args()

  lconn = LDAPhandler()

  PAGESIZE = int(lconn.ldapOptions['PAGESIZE'])
  SEARCHFILTER = lconn.ldapOptions['SEARCHFILTER']

#  print("PAGESIZE: %i" % (PAGESIZE))
#  print("SEARCHFILTER: %s" % (lconn.filter))

  # Create the page control to work from
  lc = create_controls(PAGESIZE)

# Do searches until we run out of "pages" to get from
# the LDAP server.
  while True:
    # Send search request
    try:
        msgid = lconn.l.search_ext(lconn.basedn, ldap.SCOPE_SUBTREE, SEARCHFILTER,
                             lconn.ATTRLIST, serverctrls=[lc])
    except ldap.LDAPError as e:
        sys.exit('LDAP search failed: %s' % e)

    # Pull the results from the search request
    try:
        rtype, rdata, rmsgid, serverctrls = lconn.l.result3(msgid)
    except ldap.LDAPError as e:
        sys.exit('Could not pull LDAP results: %s' % e)

    # Each "rdata" is a tuple of the form (dn, attrs), where dn is
    # a string containing the DN (distinguished name) of the entry,
    # and attrs is a dictionary containing the attributes associated
    # with the entry. The keys of attrs are strings, and the associated
    # values are lists of strings.
    user_attrs = lconn.userAttrs.split(',')
    print(';'.join(user_attrs))
    for dn, attrs in rdata:
        process_entry(dn, attrs)

    # If '-w' argument was given, call function to write results to CSV!.
    if args.writetocsv:
      print("Results have been written to the %s CSV file!.\n" % (args.writetocsv))
      for dn, attrs in rdata:  
        writetoCSV(dn, attrs)

    # Get cookie for next request
    pctrls = get_pctrls(serverctrls)
    if not pctrls:
        print >> sys.stderr, 'Warning: Server ignores RFC 2696 control.'
        break

    # Ok, we did find the page control, yank the cookie from it and
    # insert it into the control for our next search. If however there
    # is no cookie, we are done!
    cookie = set_cookie(lc, pctrls, PAGESIZE)
    if not cookie:
        break

    # Clean up
    lconn.l.unbind()

    # Done!
    sys.exit(0)

def main():
  try:
    LDAPsession()
    ldap_paging()
  except KeyboardInterrupt:
    print("\nExecution has been interrupted!.")


if __name__ == "__main__":
  main() 
