#! /usr/bin/python
# -*- coding: UTF-8 -*-


#============================================================#
#                                                            #
# $ID:$                                                      #
#                                                            #
# hello_ontapi.py                                            #
#                                                            #
# "Hello_world" program which prints the ONTAP version       #
# number of the destination filer                            #
#                                                            #
# Copyright 2011 Network Appliance, Inc. All rights    	     #
# reserved. Specifications subject to change without notice. #
#                                                            #
# This SDK sample code is provided AS IS, with no support or #
# warranties of any kind, including but not limited to       #
# warranties of merchantability or fitness of any kind,      #
# expressed or implied.  This code is subject to the license #
# agreement that accompanies the SDK.                        #
#                                                            #
# tab size = 8                                               #
#                                                            #
#============================================================#

import sys
sys.path.append("..\\NetApp")
from NaServer import *


def print_usage():
    print ("Usage: hello_ontapi.py <filer> <user> <password> \n")
    print ("<filer> -- Filer name\n")
    print ("<user> -- User name\n")
    print ("<password> -- Password\n")
    sys.exit (1)

args = len(sys.argv) - 1

if(args < 3):
   print_usage()

filer = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]


s = NaServer(filer, 1, 1)
s.set_server_type("Filer")
s.set_admin_user(user, password)
s.set_transport_type("HTTP")
#ss = s.invoke("aggr-list-info","aggregate","aggr1")
''''
#获取aggr信息
aggr = s.invoke("aggr-list-info")
aggregates = aggr.child_get("aggregates")
result = aggregates.children_get() #返回一个列表
for aggregate in result:
  print ("home-name: " + aggregate.child_get_string("home-name") + "\n")
  print ("name: " + aggregate.child_get_string("name") + "\n")
  print ("disk-count: " + aggregate.child_get_string("disk-count") + "\n")
    
'''
vol_cre = s.invoke("volume-create","volume","vol2","containing-aggr-name","aggr0","size","5g")
vol = s.invoke("volume-list-info")
volumes = vol.child_get("volumes")
vol_list = volumes.children_get()
for vol_single in vol_list:
  print ("name: " + vol_single.child_get_string("name") + "\n" )
  print ("size-total: " + vol_single.child_get_string("size-total") + "\n")




#output = s.invoke("system-get-version")  #获取系统版本信息

"""
if(output.results_errno() != 0):
   r = output.results_reason()
   print("Failed: \n" + str(r))

else :
   #r = output
   r = output.child_get_string("version")
   print (r + "\n")
"""

