#!/usr/bin/env python 

"""
Copyright 2017 by tuxedoar@gmail.com .

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

"""

import argparse
import requests
import urllib
from datetime import datetime
from ConfigParser import SafeConfigParser

headers = {'user-agent': ' '}
url = {}
DateTime = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

def readConfigFile(iniFile):
  parser = SafeConfigParser()
  # Check if config file exist
  if parser.read(iniFile):
    TOKEN = parser.get('duckdns', 'token')
    DOMAIN = parser.get('duckdns', 'domain')
    VERBOSE="true"
    URL_BASE="https://www.duckdns.org/update?"
    PARAMS = urllib.urlencode({'domains': DOMAIN,'token': TOKEN,'verbose': VERBOSE})
    url['url'] = URL_BASE+PARAMS
  else:
    print "ERROR: Configuration file %s was not found!" % (iniFile)
    raise SystemExit  

def SendRequest(url):
  response_data = []
  try:
    # Make a HTTP GET request
    r = requests.get(url, verify=True, headers=headers, timeout=3.0)
    response = r.text
    # Convert unicode to ascii
    response = response.encode('ascii','ignore')
    response_data.append(response)
    response_data = response_data[0].split('\n')
    # Filter empty strings in list
    response_data = filter(None, response_data)
    # Assign a name for each element of response
    for element in response_data:
	query_response, ip_addr, state = response_data[0], response_data[1], response_data[2]

    if query_response == 'OK':
      if state == 'NOCHANGE':
        print "%s - Your IP %s has not changed. Nothing to update!." % ( DateTime, ip_addr )
      elif state == 'UPDATED':
        print "Your IP has been updated!. Your new IP is: %s ." % (ip_addr)
    elif query_response == 'KO':
      print "ERROR: bad response recieved. Check your parameters for the URL."

  except requests.exceptions.Timeout:
    print "Timed out for request!."   
  except requests.exceptions.ConnectionError, e:
    print "Connection error: %s ." % (e)

def GetArgs():
   parser = argparse.ArgumentParser(
       description='Update your IP address for your duckdns registered domain')
   parser.add_argument('-f', '--file', required=True, action='store',
                       help='The configuration file to use')

   args = parser.parse_args()
   return args

def main():
  args = GetArgs()
  readConfigFile(args.file)
  SendRequest(url['url'])

if __name__ == "__main__":
  main()

