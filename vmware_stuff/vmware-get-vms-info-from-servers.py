#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
05/09/2017 - Put together by tuxedoar@gmail.com. 

DESCRIPTION
-----------

This Python program is aimed for listing the vms and retrieve basic info about them,
from a list of ESX / vCenter hosts. The main idea is to avoid having to enter the same
credentials for each of those, repeatedly. A list of hosts must be specified in a txt file,
with one IP address per line!. It's assumed that credentials are the same for all the hosts!. 

This script is based on the following pieces of code:

https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/getallvms.py
https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/list_datastore_info.py

PREREQUISITES
-------------

In order for this script to work, you must have the Python SDK for the VMware vSphere API installed!. See:

https://github.com/vmware/pyvmomi

USAGE
-----

Usage example:

./vmware-get-vms-info-from-servers.py -u root -f servers.txt

 
"""

from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVim import connect
from pyVmomi import vmodl 
from pyVmomi import vim
from pyVmomi import VmomiSupport 

import sys, re
import argparse
import atexit
import getpass
import ssl

switches = []

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for retrieving all the Virtual Machines')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=False, action='store',
                       help='Password to use when connecting to host')
   parser.add_argument('-f', "--myfile", required=True, action='store',
                       help='File that stores the IP of each host')
   args = parser.parse_args()
   return args


# http://stackoverflow.com/questions/1094841/
def sizeof_fmt(num):
    """
    Returns the human readable version of a file size
    :param num:
    :return:
    """
    for item in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def ReadFile(myfile):
# It reads the specified file, retrieves IP addresses and store them in a list.
        try:
                readfile = open(myfile, 'r')
                for line in readfile.readlines():
                        line=line.strip()
                        if line and not line.startswith('#'):
                                valid = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", line)
                                if not valid:
                                        print("WARNING: The IP %s is being ignored because is not valid!" % (line))
                                else:
                                        ip = line
                                        switches.append(ip)
                
                readfile.close()
        except IOError:
                print("ERROR: Can not open The specified file!.")
                sys.exit(2)     
        except:
                sys.exit(2)


def PrintVmInfo(vm, depth=1):
   """
   Print information for a particular virtual machine or recurse into a folder
   or vApp with depth protection
   """
   maxdepth = 10

   # if this is a group it will have children. if it does, recurse into them
   # and then return
   if hasattr(vm, 'childEntity'):
      if depth > maxdepth:
         return
      vmList = vm.childEntity
      for c in vmList:
         PrintVmInfo(c, depth+1)
      return

   # if this is a vApp, it likely contains child VMs
   # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
   if isinstance(vm, vim.VirtualApp):
      vmList = vm.vm
      for c in vmList:
         PrintVmInfo(c, depth + 1)
      return

   # Search for all ESXi hosts
   objview = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
   esxi_hosts = objview.view
   objview.Destroy()

   datastores = {}

   for esxi_host in esxi_hosts:       
     esxihostname = esxi_host.name
     # All Filesystems on ESXi host
     storage_system = esxi_host.configManager.storageSystem
     host_file_sys_vol_mount_info = \
     storage_system.fileSystemVolumeInfo.mountInfo

     datastore_dict = {}
            # Map all filesystems
     for host_mount_info in host_file_sys_vol_mount_info:
                # Extract only VMFS volumes
       if host_mount_info.volume.type == "VMFS":
         extents = host_mount_info.volume.extent
         DatastoreName = host_mount_info.volume.name
	 capacity = host_mount_info.volume.capacity
	 capacity = sizeof_fmt(capacity)
#        print(name, sizeof_fmt(capacity))

   summary = vm.summary
   print("%s, %s, %s, %s, %s" % (host, summary.config.name, summary.runtime.powerState, DatastoreName, capacity))
#   print("Name       : ", summary.config.name)


def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """

   args = GetArgs()
   myfile = args.myfile

   ReadFile(myfile)

   if args.password:
     password = args.password
   else:
     password = getpass.getpass(prompt='Enter password for hosts : ')

   try:
     for host in switches:
       global host

       context = None
       if hasattr(ssl, '_create_unverified_context'):
	 context = ssl._create_unverified_context()

       si = SmartConnect(host=host,
			 user=args.user,
			 pwd=password,
			 port=int(args.port),
			 sslContext=context)
       if not si:
	 print("Could not connect to the specified hosts using specified "
	       "username and password")
	 return -1

       atexit.register(Disconnect, si)

       content = si.RetrieveContent()
       global content

       for child in content.rootFolder.childEntity:
	 if hasattr(child, 'vmFolder'):
	   datacenter = child
	   vmFolder = datacenter.vmFolder
	   vmList = vmFolder.childEntity
	   for vm in vmList:
	     PrintVmInfo(vm)

     return 0
   except vim.fault.InvalidLogin:
     print("Cannot complete login due to an incorrect user name or password.") 

# Start program
if __name__ == "__main__":
   main()
