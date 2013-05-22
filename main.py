#!/usr/bin/python3
import time, os, re, string, psycopg2
from collections import defaultdict, namedtuple

filename = '/var/log/icecast2/access.log'

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

def parse(line):
	match = format.match(line)
	if match:
		return LogItem( **match.groupdict() )

def connect():
	conn = psycopg2.connect(host='dbserver', database='icecast_logs', user='icecast_user', password='icecast_password')
	return conn

def get_mount_point(mount_point):
	url = mount_point.split(' ')[1][1:]
	cur.execute('SELECT id FROM mount_points WHERE (mount_point = %s) AND ((date_added <= now() AND date_retired >= now()) OR (date_added <= now() AND date_retired is NULL))', [url])
	if cur.rowcount == 0:
		return None
	else:
		id = cur.fetchone()[0]
		return id

def get_or_add_ua(ua):
	cur.execute('SELECT id FROM user_agents WHERE ua_string = %s', [ua])
	if cur.rowcount == 0:
		cur.execute('INSERT INTO user_agents (ua_string) VALUES (%s) RETURNING id', [ua])
		id = cur.fetchone()[0]
		if id:
			db.commit()
			return id
		else:
			raise Exception('cannot add user-agent: %s' % ua)
	else:
		id = cur.fetchone()[0]
		return id

def get_or_add_ref(url):
	cur.execute('SELECT id FROM referers WHERE url = %s', [url])
	if cur.rowcount == 0:
		cur.execute('INSERT INTO referers (url) VALUES (%s) RETURNING id', [url])
		id = cur.fetchone()[0]
		if id:
			db.commit()
			return id
		else:
			raise Exception('cannot add referer: %s' % url)
	else:
		id = cur.fetchone()[0]
		return id

def log(ip, mount, ref, ua, bytes):
	cur.execute('INSERT INTO log (ip, mount_point_id, referer_id, user_agent_id, bytes) VALUES (%s, %s, %s, %s, %s) RETURNING id', [ip, mount, ref, ua, bytes])
	id = cur.fetchone()[0]
	if id:
		db.commit()
		return id
	else:
		raise Exception('cannot log row: %s %s %s %s %s' % (id, mount, ref, ua, bytes))


def open_file(filename):
	file = open(filename, 'r')

	st_results = os.stat(filename)
	st_size = st_results[6]
	file.seek(st_size)

	return file

def read_loop(file):
	while 1:
		where = file.tell()
		line = file.readline()
		if not line:
			time.sleep(0.5)
			file.seek(where)
		else:
			data = parse(line)
			print(line)
			mount = get_mount_point(data.request)
			if mount is not None:
				ua = get_or_add_ua(data.user_agent)
				ref = get_or_add_ref(data.referer)
				id = log(data.host, mount, ref, ua, data.bytes)

db = connect()
cur = db.cursor()
file = open_file(filename)
read_loop(file)
