import sys
import psycopg2
from datetime import datetime
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
	def __init__(self,data_list):
		self.data_list = data_list
		self.conn = psycopg2.connect(
			host="10.10.94.129",
			port=7777,
			database="gsm_ports",
			user="postgres",
			password="postgres")

		self.conn.autocommit = True
		self.cur = self.conn.cursor()

	def _truncate_old_data(self):
		self.cur.execute('''truncate table test restart identity;''')

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
				insert into test (gsm_ip,active_ports,inactive_ports,total_active,created) \
				values ('{0}','{1}','{2}',{3},'{4}')
				'''.format(gsm_ip,active_ports,inactive_ports,total_active,created_date))
		self.conn.commit()
		self.conn.close()