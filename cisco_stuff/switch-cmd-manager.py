#!/usr/bin/env python

"""
Copyright 2017 by tuxedoar@gmail.com .

LICENSE

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

It allows to execute several commands in different managed switches at once,
using SSH. 

"""

import paramiko
import argparse
from time import sleep
import sys
import re
import getpass
from socket import error

switches = []
user = ''
hosts_file = ''
cmd = []
port=22

def main():
  parser = argparse.ArgumentParser(
      description='Exceute remote commands on several managed switches or servers.')
  parser.add_argument('-f', '--file', required=True, action='store', 
                      help='Plain text file with list of hosts')
  parser.add_argument('-u', '--user', required=True, action='store',
                      help='User to login on remote hosts')
  parser.add_argument('-c', '--commands', required=True, action='store',
                      help='Comma separated commands to be executed on remote hosts')
  parser.add_argument('-p', '--port', required=False, action='store',
                      help='Specify SSH port to connect to hosts')
  args = parser.parse_args()

  if args.file != None and args.user != None and args.commands != None:
    user=args.user
    hosts_file=args.file
    cmd=args.commands
    if args.port:
      # Get rid of this global variable in the future!. 
      global port
      port=args.port
    try:
      ReadFile(hosts_file)
      SSHsession(user, cmd)
    except KeyboardInterrupt:
      print "\n\nExecution was interrupted!"
  else: 
    parser.print_help()


def SSHsession(user, cmd):

  cmd = cmd.split(',')
  pw = getpass.getpass('\n Please, enter your password to access hosts: ')

  # Start session on each IP address in the switches list.
  for ip in switches:
    try:
      print "\n Connecting to %s with the user %s ... \n" % (ip, user) 
      MySession = paramiko.SSHClient()
      MySession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      MySession.connect(ip, username=user, password=pw, port=port, look_for_keys=False, allow_agent=False, timeout=10)
      timeout_modifier = 1.1  # wait 10% longer than usual

      UserCommands = MySession.invoke_shell()
      sleep(2)
      for c in cmd:
        # Remove double quotes!.
        c = c.replace('\"','')
        UserCommands.send(c+'\n')
      
      # Wait 1 second before sending commands provided by user!.
      sleep(1)
      # Ouput buffer size in bytes!.
      output = UserCommands.recv(8000)

      # Split each line in output and store them in a list.
      output = output.splitlines()
      for lines in output:
        print lines

    except paramiko.ssh_exception.AuthenticationException, e:
            print "An authentication error ocurred when trying to connect to %s : %s" % (ip, e)
    except paramiko.SSHException, e:
            print "An error has ocurred while connecting to %s : %s " % (ip, e)
    except error:
            print "Connection timed out!. Check your network connection!."          

                                        
def ReadFile(hosts_file):
# Read the file, extract IP adresses and store them on a list.
  try:
    file = open(hosts_file, 'r')
    for line in file.readlines():
      line=line.strip()
      if line and not line.startswith('#'):
        valid_ip = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", line)
        if not valid_ip:
          print "WARNING: The IP %s is ignored for not being valid!" % (line)
        else:
          ip = line
          switches.append(ip)
          
    file.close()
  except IOError:
    print "Can't read the specified file. Make sure it exist!."
    sys.exit(2)     

if __name__ == "__main__":
  main()
