import os
import sleekxmpp.componentxmpp
import logging
import httpd

import configparser
from optparse import OptionParser
#import sleekxmpp.xmlstream.xmlstream

#sleekxmpp.xmlstream.xmlstream.HANDLER_THREADS = 5

class Bot(sleekxmpp.ClientXMPP):
	
	def __init__(self, jid, password):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self.add_event_handler("session_start", self.start)
	
	def start(self, event):
		self.getRoster()
		self.sendPresence()

if __name__ == '__main__':
	#parse command line arguements

	optp = OptionParser()
	optp.add_option('-q','--quiet', help='set logging to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
	optp.add_option('-d','--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
	optp.add_option('-v','--verbose', help='set logging to COMM', action='store_const', dest='loglevel', const=5, default=logging.INFO)
	optp.add_option("-c","--config", dest="configfile", default="config.ini", help="set config file to use")
	opts,args = optp.parse_args()

	config = configparser.RawConfigParser()
	config.read(opts.configfile)
	
	f = open(config.get('general', 'pidfile'), 'w')
	f.write("%s" % os.getpid())
	f.close()
	
	logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
	xmpp = Bot(config.get('xmpp', 'jid'), config.get('xmpp', 'password'))
	xmpp.registerPlugin('xep_0004')
	xmpp.registerPlugin('xep_0030')
	xmpp.registerPlugin('xep_0045')
	xmpp.registerPlugin('xep_0050')
	httpserver = httpd.HTTPD(xmpp, config)
	if xmpp.connect():
		xmpp.process(threaded=False)
	else:
		print("Unable to connect.")
