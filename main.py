#!/usr/bin/python3
import sys, time, os, re, string, configparser, logging, psycopg2
from collections import defaultdict, namedtuple
from daemon import Daemon

class IceKing(Daemon):

	format = re.compile( 
		r"(?P<host>[\d\.]+)\s" 
		r"(?P<identity>\S*)\s" 
		r"(?P<user>\S*)\s"
		r"\[(?P<time>.*?)\]\s"
		r'"(?P<request>.*?)"\s'
		r"(?P<status>\d+)\s"
		r"(?P<bytes>\S*)\s"
		r'"(?P<referer>.*?)"\s'
		r'"(?P<user_agent>.*?)"\s*' 
	)

	LogItem = namedtuple('LogItem',
		['host', 'identity', 'user', 'time', 'request',
		'status', 'bytes', 'referer', 'user_agent'])

	timeout = 0.5

	def parse(self, line):
		match = self.format.match(line)
		if match:
			return self.LogItem( **match.groupdict() )

	def connect(self, host, port, db, user, pw):
		conn = psycopg2.connect(host=host, port=port, database=db, user=user, password=pw)
		return conn

	def get_mount_point(self, mount_point):
		url = mount_point.split(' ')[1][1:]
		self.cur.execute('SELECT id FROM mount_points WHERE (mount_point = %s) AND ((date_added <= now() AND date_retired >= now()) OR (date_added <= now() AND date_retired is NULL))', [url])
		if self.cur.rowcount == 0:
			return None
		else:
			id = self.cur.fetchone()[0]
			return id

	def get_or_add_ua(self, ua):
		self.cur.execute('SELECT id FROM user_agents WHERE ua_string = %s', [ua])
		if self.cur.rowcount == 0:
			self.cur.execute('INSERT INTO user_agents (ua_string) VALUES (%s) RETURNING id', [ua])
			id = self.cur.fetchone()[0]
			if id:
				self.db.commit()
				return id
			else:
				raise Exception('cannot add user-agent: %s' % ua)
		else:
			id = self.cur.fetchone()[0]
			return id

	def get_or_add_ref(self, url):
		self.cur.execute('SELECT id FROM referers WHERE url = %s', [url])
		if self.cur.rowcount == 0:
			self.cur.execute('INSERT INTO referers (url) VALUES (%s) RETURNING id', [url])
			id = self.cur.fetchone()[0]
			if id:
				self.db.commit()
				return id
			else:
				raise Exception('cannot add referer: %s' % url)
		else:
			id = self.cur.fetchone()[0]
			return id

	def log(self, ip, mount, ref, ua, bytes):
		self.cur.execute('INSERT INTO log (ip, mount_point_id, referer_id, user_agent_id, bytes) VALUES (%s, %s, %s, %s, %s) RETURNING id', [ip, mount, ref, ua, bytes])
		id = self.cur.fetchone()[0]
		if id:
			self.db.commit()
			return id
		else:
			raise Exception('cannot log row: %s %s %s %s %s' % (id, mount, ref, ua, bytes))

	def process_line(self, line):
		data = self.parse(line)
		print(line)
		mount = self.get_mount_point(data.request)
		if mount is not None:
			ua = self.get_or_add_ua(data.user_agent)
			ref = self.get_or_add_ref(data.referer)
			id = self.log(data.host, mount, ref, ua, data.bytes)


	def open_file(self, filename):
		file = open(filename, 'r')
		return file

	def read_loop(self, file):
		if self.process_all:
			for line in file:
				self.process_line(line)

		if self.watch:
			st_results = os.stat(file.name)
			st_size = st_results[6]
			file.seek(st_size)

			while 1:
				where = file.tell()
				line = file.readline()
				if not line:
					time.sleep(self.timeout)
					file.seek(where)
				else:
					self.process_line(line)


	def run(self):
		config = configparser.SafeConfigParser()
		config.read('config.ini')

		logfile = config.get('main','log')

		if not logfile:
			import os.getcwd
			logfile = '%s/iceking.log' % os.getcwd()

		loglevel = config.get('main','log_level')

		if loglevel == 'critical':
			loglevel = logging.CRITICAL
		elif loglevel == 'error':
			loglevel = logging.ERROR
		elif loglevel == 'warning':
			loglevel = logging.WARNING
		elif loglevel == 'info':
			loglevel = logging.INFO
		elif loglevel == 'debug':
			loglevel = logging.DEBUG
		else:
			loglevel = logging.WARNING

		logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', filename=logfile, level=logging.INFO)
		logging.info('IceKing starting...')

		logger = logging.getLogger('root')
		logger.setLevel(loglevel)

		if sys.argv[1] == 'no-daemon':
			log_con = logging.StreamHandler()
			log_con.setLevel(loglevel)
			log_con.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
			logger.addHandler(log_con)

		self.db = self.connect(
			config.get('database', 'host'),
			config.get('database','port'),
			config.get('database','db_name'),
			config.get('database','user'),
			config.get('database', 'password')
		)

		self.cur = self.db.cursor()
		file = self.open_file(config.get('main','filename'))
		self.timeout = config.getfloat('main','timeout')
		self.process_all = config.getboolean('main', 'process_all')
		self.watch = config.getboolean('main','watch')
		self.read_loop(file)

	def stop(self):
		logger = logging.getLogger('root')
		logger.setLevel(logging.INFO)
		logging.info('Shutting down.')
		super(Daemon, self).stop()

	def restart(self):
		logger = logging.getLogger('root')
		logger.setLevel(logging.INFO)
		logging.info('Restarting...')
		super(Daemon, self).restart()

if __name__ == "__main__":
	daemon = IceKing('/var/run/iceking.pid')

	if len(sys.argv) == 2:
			if 'start' == sys.argv[1]:
				daemon.start()
			elif 'stop' == sys.argv[1]:
				daemon.stop()
			elif 'restart' == sys.argv[1]:
				daemon.restart()
			elif 'no-daemon':
				daemon.run()
			else:
				print("Unknown command")
				sys.exit(2)
			sys.exit(0)
	else:
		print("usage: %s start|stop|restart|no-daemon" % sys.argv[0])
		sys.exit(2)
