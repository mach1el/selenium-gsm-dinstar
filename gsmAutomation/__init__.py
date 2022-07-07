import sys
import psycopg2
from datetime import datetime
from gsmAutomation.sites import getSite
from argparse import ArgumentParser,RawTextHelpFormatter

sys.dont_write_bytecode=True

def MainArguments():
	__script__ = sys.argv[0]
	parser = ArgumentParser(
		add_help=False,
		usage='%(prog)s  -site [Site name]',
		formatter_class=RawTextHelpFormatter,
		prog=__script__,
		epilog= '''\
Examples:
%(prog)s -site ql13
''')

	require = parser.add_argument_group("REQUIRE")
	require.add_argument("-site",metavar="",help="Specify site to check",default=None)
	args = parser.parse_args()

	if args.site == None:
		sys.exit("[-] Nothing to do at here")
	else:
		site = args.site
	return site

class UpdateDatabase:
	def __init__(self,site,data_list):
		self.site = site
		self.data_list = data_list
		self.getDBinfo()
		self.conn = psycopg2.connect(
			host=self.ip,
			port=self.port,
			database=self.db,
			user=self.username,
			password=self.password)

		self.conn.autocommit = True
		self.cur = self.conn.cursor()

	def getDBinfo(self):
		ip,port,username,password,db = getSite("database")[0].split(" ")
		self.ip = ip.split("=")[1]
		self.port = port.split("=")[1]
		self.username = username.split("=")[1]
		self.password = password.split("=")[1]
		self.db = db.split("=")[1]

	def _truncate_old_data(self):
		self.cur.execute('''truncate table {0} restart identity;'''.format(self.site))

	def _add_new_data(self):
		self._truncate_old_data()
		for data in self.data_list:
			gsm_ip,active_ports,inactive_ports,total_active = data.items()
			gsm_ip = gsm_ip[1]
			active_ports = ",".join([str(int) for int in active_ports[1]])
			inactive_ports = ",".join([str(int) for int in inactive_ports[1]])
			total_active = total_active[1][0]
			created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			self.cur.execute('''\
				insert into {0} (gsm_ip,active_ports,inactive_ports,total_active,created) \
				values ('{1}','{2}','{3}',{4},'{5}')
				'''.format(self.site,gsm_ip,active_ports,inactive_ports,total_active,created_date))
		self.conn.commit()
		self.conn.close()