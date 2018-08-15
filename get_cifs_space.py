import sys
sys.path.append("E:/01_Docu/ONTAP_dev/netapp-manageability-sdk-5.7/netapp-manageability-sdk-5.7/lib/python/NetApp")
from NaServer import *
import json
import xmltodict



class GET_CIFS_SPACE(object):
	"""
	function: initial this CLASS
	input args: None
	output: None
	"""
	def __init__(self):
		self.vol_list_api = NaElement("volume-space-list-info")
		self.qtree_list_api = NaElement("qtree-list")
		self.host_list = ["192.168.7.10"]
	"""
	function: create a connection
	input args: host name or host ip(better)
	output: a connection object
	"""
	def create_conn(self, host):
		conn = NaServer(host, 1 , 21)
		conn.set_server_type("FILER")
		conn.set_transport_type("HTTP")
		conn.set_port(80)
		conn.set_style("LOGIN")
		conn.set_admin_user("root", "root1234")
		return conn

	"""
	function: for invoking netapp storage api
	input args: connection object, api name
	output : invoke result object
	"""
	def invoke_api(self, conn, api):
		api = api
		conn = conn
		output = conn.invoke_elem(api)
		if (output.results_status() == "failed") :
			print ("Error:\n")
			print (xo.sprintf())
			sys.exit (1)
		return output
	"""
	function: get volume space info list
	input args: connection object
	output: a list of  vol-space-info objects
	"""
	def get_vol_list(self, conn):
		conn = conn
		invoke_result = self.invoke_api(conn, self.vol_list_api)
		volumesOb = invoke_result.child_get("vol-space-infos")
		vol_list = volumesOb.children_get()
		return vol_list
	"""
	function: get qtree list for check security sytle; if security style is ntfs, this volume is cifs volume
	input args: connection object
	output: qtree list
	"""
	def get_qtree_list(self, conn):
		conn = conn
		invoke_result = self.invoke_api(conn, self.qtree_list_api)
		qtreesOb = invoke_result.child_get("qtrees")
		qtree_list = qtreesOb.children_get()
		return qtree_list
	"""
	function: get cifs volume list by checking volume qtree's security style
	input args: qtree_list 
	output: a list of cifs volumes
	"""
	def get_cifs_list(self,qtree_list):
		cifs_list = []
		for qtree in qtree_list:
			if qtree.child_get_string("security-style") == "ntfs":
				cifs_list.append(qtree.child_get_string("volume"))
		return cifs_list
	"""
	function: get space info of cifs volumes; if volume is cifs volume append this vol space info to the cifs_space_list
	input args: cifs_list(cifs volumes list), vol_list(volumes space info list)
	output: a list of cifs volumes space info(vol space info is json style)
	"""
	def get_cifs_space(self, cifs_list, vol_list):
		cifs_space_list = []
		for vol in vol_list:
			if vol.child_get_string("volume") in cifs_list:
				xmlparse = xmltodict.parse(vol.sprintf())
				jsonstr = json.dumps(xmlparse, indent=1)
				cifs_space_list.append(jsonstr)
		return cifs_space_list
	"""
	funtcion: main function for combining all other functions together
	input args: None
	output: a list of all cifs volumes space info of all controllers
	"""
	def main(self):
		cifs_space_list_all = []
		for host in self.host_list:
			conn = self.create_conn(host)
			vol_list = self.get_vol_list(conn)
			qtree_list = self.get_qtree_list(conn)
			cifs_list = self.get_cifs_list(qtree_list)
			cifs_space_list = self.get_cifs_space(cifs_list,vol_list)
			cifs_space_list_all.extend(cifs_space_list)
		return cifs_space_list_all
"""
following:
create an instance of GET_CIFS_SPACE() object
get cifs_space_list_all
"""
get_cifs_space = GET_CIFS_SPACE()
cifs_space_list_all = get_cifs_space.main()
for cifs_space in cifs_space_list_all:	
	print (cifs_space)









