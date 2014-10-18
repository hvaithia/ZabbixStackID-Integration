#!/usr/bin/python -u

import os
import sys
import shutil
from pyzabbix import ZabbixAPI

zapi = ZabbixAPI("http://10.13.1.64/zabbix")
zapi.login("dc_hvaithianathan", "Venkiboy200")
print "Connected to Zabbix API Version %s" % zapi.api_version()


def get_zabbix_hosts():
  host_list = []
  for h in zapi.host.get(output='extend'):
    b=h['host'].encode("utf-8")
    host_list.append(b)
  return host_list

def get_host_groups():
  host_groups=[]
  for hg in zapi.hostgroup.get(output='extend'):
    a=hg['name'].encode("utf-8")
    host_groups.append(a)
  return host_groups

def parse_stackID(csvfile):
  List=[]
  f=open(csvfile,'rU')
  for line in f.readlines():
    #list method
    y = line.strip().split(",")
    List.append(y)

  return List

def create_hostgroups(List_zabbix,List_csv):

  #List Assignments
  hostgroups = get_host_groups()
  Host_csv=[item[0] for item in List_csv]
  stack_csv=[item[2] for item in List_csv]

  #convert each list to lower case
  hostgroups=[x.lower() for x in hostgroups]
  Host_csv=[x.lower() for x in Host_csv]
  stack_csv= [x.lower() for x in stack_csv]
  List_zabbix= [x.lower() for x in List_zabbix]
  #print List_zabbix
  #print "-----------------hostgroups Host_csv stack_csv----------------"
  #print hostgroups
  #print Host_csv
  #print stack_csv
  #print "-----------------hostgroups Host_csv stack_csv----------------"
  

  for index, host_zabbix in enumerate(List_zabbix):
    if (host_zabbix in Host_csv) and (stack_csv[Host_csv.index(host_zabbix)]) != '': # The and condition is not reqd --- and (stack_csv[Host_csv.index(host_zabbix)] not in hostgroups):
     ##########if (stack_csv[Host_csv.index(host_zabbix)]) != '':
      #create host groups with item[1] value and add item[0] as host in that group
      try:
        #print "try block"
        #Create & Add host to the hostgroup
        zapi.hostgroup.create({"name":stack_csv[Host_csv.index(host_zabbix)]})
        group_id = zapi.hostgroup.get(output='extend',filter={"name":stack_csv[Host_csv.index(host_zabbix)]})
        #host_id = zapi.host.get(output='extend',filter={"host":host_zabbix})
        try:
          host_id = zapi.host.get(output='extend',filter={"host":host_zabbix})
          zapi.hostgroup.massadd(hosts={"hostid":host_id[0]['hostid']},groups={"groupid":group_id[0]['groupid']}) 
        except:
          host_id = zapi.host.get(output='extend',filter={"host":host_zabbix.upper()})  
          zapi.hostgroup.massadd(hosts={"hostid":host_id[0]['hostid']},groups={"groupid":group_id[0]['groupid']}) 
        print "TRY: Adding the host to the host group. host is %s and group is %s" %(host_zabbix,stack_csv[Host_csv.index(host_zabbix)]) 
      except:
        #print "Except block"
        #Only Add host to the hostgroup
        group_id = zapi.hostgroup.get(output='extend',filter={"name":stack_csv[Host_csv.index(host_zabbix)]})
        print "CATCH:Host group might already exist, Adding the host to the host group. host is %s and group is %s" %(host_zabbix,stack_csv[Host_csv.index(host_zabbix)]) 
        try:
          host_id = zapi.host.get(output='extend',filter={"host":host_zabbix})
          zapi.hostgroup.massadd(hosts={"hostid":host_id[0]['hostid']},groups={"groupid":group_id[0]['groupid']})
        except:
          host_id = zapi.host.get(output='extend',filter={"host":host_zabbix.upper()})
          print "printing hostid: "
	  print host_id
          print "~~~~~~"
          zapi.hostgroup.massadd(hosts={"hostid":host_id[0]['hostid']},groups={"groupid":group_id[0]['groupid']})
        #host_id = zapi.host.get(output='extend',filter={"host":host_zabbix})
        #zapi.hostgroup.massadd(hosts={"hostid":host_id[0]['hostid']},groups={"groupid":group_id[0]['groupid'].lower()}) 
    #elif:
      #check to see if the host is added to the host group. If added exit else below step
      #Host group is already created. Just add host to the host group
    else:
      sys.exit()
      
def main():
  args=sys.argv[1:]

  if not args:
    print 'usage: stackID.py <csvfilelocation/filename.csv>'
    print 'where the csv is the file from OMS which has server,display_name,name,description parameters'
    sys.exit(1)
  elif len(args)>1:
    print 'Too many arguements:'
    print 'usage: stackID.py <csvfilelocation/filename.csv>'
    print 'where the csv is the file from OMS which has server,display_name,name,description parameters'
    sys.exit(1)
  List_zabbix=get_zabbix_hosts()
  print "------List_zabbix List_csv------"
  List_csv=parse_stackID(args[0])
  #print List_csv
  print "No of items in the list is: %d" %(len(List_csv))
  print "------List_zabbix List_csv------"
  # Do A tolower on both lists before passing

  #change Sep 23. Strip the domain from hostnames
  strip_List_zabbixhost=[]
  for strings in List_zabbix:
   y=strings.strip().split(".")[0]
   strip_List_zabbixhost.append(y)
  print strip_List_zabbixhost
  print List_zabbix

  #create_hostgroups(strip_List_zabbixhost,List_csv)
  create_hostgroups(List_zabbix,List_csv)

if __name__ == '__main__':
    main()

