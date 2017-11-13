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

This script allows to get relevant information of printers managed by 
the CUPS printing software. It also allows to list pending printing jobs
or list them ALL (together with the finished ones)!.

"""

import cups 
import datetime
import argparse

conn = cups.Connection ()
# It generates a dictionary with printers and their attirbutes.
printers = conn.getPrinters () 

jobs_selected = ''
pending_jobs='not-completed'
all_jobs='all'

# Set the printer's attributes to be looked for on a dict. 
attributes = {	'ID':'job-id',
		'Doc':'job-name',
		'User':'job-originating-user-name', 
		'Printer':'job-printer-uri',
		'IP source':'job-originating-host-name',
		'Pages':'job-media-sheets-completed',
		'State':'job-state-reasons',
		'Detailed state':'job-printer-state-message'
	}

# Function to list printers.
def list_printers():

  for printer in printers:
    shared = printers[printer]['printer-is-shared']
    ip_addr = printers[printer]['printer-info']
    model = printers[printer]['printer-make-and-model']
    uri = printers[printer]['device-uri']
    location = printers[printer]['printer-location']
    state = printers[printer]['printer-state']

    print "PRINTER:       ", "  %s\n" % (printer), \
          "MODEL:      ", "     %s\n" % (model),             \
          "LOCATION: ", "       %s\n" % (location),        \
          "IP:        ", "      %s\n" % (ip_addr),                      \
          "URI:        ", "     %s" % (uri)                     
    if state == 3:
      print "STATUS:      \tReady to print\n"        
    elif state == 4:
      print "STATUS:      Active\n"
    elif state == 5: 
      print "STATUS:      Paused\n"
    else:
      print "STATUS:      Unknown!\n"

# Argument passed to the function defines if printing pending jobs or all of them!. 
def jobs_handler(jobs_selected):
  # Set the selection by jobs_selected
  jobs_selected = conn.getJobs(which_jobs=jobs_selected)
  # Loop over jobs. 
  for jobs in jobs_selected:
    jobs_attrs = conn.getJobAttributes(jobs)
    # Loop over job's attributes.
    for attribute in jobs_attrs:
      key, value = attribute, jobs_attrs[attribute]
      # Loop for attributes that were set in the dictionary, early on!. 
      for looked_attrs in attributes:
        # Those attributes that matches with dict attrs, are shown by their keys!. 
        if attributes[looked_attrs] in key:
          print "%s = %s" % (looked_attrs, value)
          break
    print '\n'


def cancel_jobs():
  pending_jobs = conn.getJobs(which_jobs='not-completed') 
  for pending_job in pending_jobs:
    conn.cancelJob(pending_job, purge_job=False)
    print "Cancelling job: ", pending_job

  
def main():

  parser = argparse.ArgumentParser(
      description='Do minor management on printers managed by the CUPS printing software')
  parser.add_argument('-p', '--printers', required=False, action='store_true', 
                      help='List printers available')
  parser.add_argument('-j', '--jobs', required=False, action='store_true',
                      help='List pending jobs')
  parser.add_argument('-J', '--alljobs', required=False, action='store_true',
                      help='List all printers jobs')
  parser.add_argument('-C', "--cancel", required=False, action='store_true',
                      help='Cancel all pending jobs')
  args = parser.parse_args()


  if args.printers:
    list_printers()
  elif args.jobs:
    jobs_handler(pending_jobs)
  elif args.alljobs:
    jobs_handler(all_jobs)
  elif args.cancel:
    cancel_jobs()
  else: 
    parser.print_help()

if __name__ == "__main__":
  main()

