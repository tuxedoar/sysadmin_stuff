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
  print "ID\t PRINTER\t IP\t DOCUMENT\t USER\t PAGES\t STATE\t DETAILED"
  for jobs in jobs_selected:
    jobs_attrs = conn.getJobAttributes(jobs)

    id = jobs_attrs.get('job-id')
    doc = jobs_attrs.get('job-name')
    user = jobs_attrs.get('job-originating-user-name') 
    printer =jobs_attrs.get('job-printer-uri')
    IP = jobs_attrs.get('job-originating-host-name')
    pages = jobs_attrs.get('job-media-sheets-completed')
    state = jobs_attrs.get('job-state-reasons')
    detailed_state = jobs_attrs.get('job-printer-state-message')
    print "%s\t %s\t %s\t %s\t %s\t %s\t %s\t %s\t" % (id, printer, IP, doc, user, pages, state, detailed_state)

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

