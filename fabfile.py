from fabric.api import * 
import sys 

# Define your classed machines here
# this allows you to run specific commands 
# against specific machine classes 
# (e.g. web servers, db servers)
env.roledefs = { 
	'hypervisors' : [
			'hypervisor01.example.com', 
			'hypervisor02.example.com', 
			'hypervisor03.example.com', 
			'hypervisor04.example.com', 
			'hypervisor05.example.com', 
			],
	'zenoss' : [ 
			'zenossserver01.nope.example.com',
			],
	'webservers_hard' : [ 
			'web05.example.com',
			],
	'webservers' : [ 
			'webserver%02d.example.com' % n for n in xrange(01,99)
			],
	'mogilefsnodes' : [ 
			'mogilefsnode%02d.example.com' % n for n in xrange(01,99)
			],
	}

# Define your global hosts here 
# this will run non-scoped commands 
# against all the hosts below 
env.hosts = [
		'workstation666.example.com',
		'master-server.example.com',
		'everything_else.example.com',
		]
def uptime(): 
	try: 
		sudo ("uptime")
	except: 
		print ("unable to get uptime")

def hostname():
	try: 
		sudo ("hostname")
	except: 
		print ("cannot get hostname")

@roles('webservers_hard')
def hard_httpd_restart():
	try: 
		run  ("echo Make sure you add hosts to the webservers_hard array\!")
		sudo ("for i in $(ls /etc/init.d/httpdv1-*); do sudo $i stop; done")
		sudo ("for pid in $(ps aux | grep httpd | grep -v grep | awk '{print $2}'); do kill -9 $pid; done ")
		sudo ("for i in $(ls /etc/init.d/httpdv1-*); do sudo $i start; done")
		sudo ("for i in $(ls /etc/init.d/httpdv1-*); do sudo $i status; done")
	except: 
		print ("httpd service restarts failed") 

@roles('webservers')
def httpd_status():
	try: 
		sudo ("service httpdv1-perl status && service httpdv1-proxy status && service httpdv1-ssl status")
	except: 
		print ("httpd service restarts failed") 

@roles('snmpd_boxes')
def snmpd_restart():
	try: 
		sudo ("service snmpd restart && service snmpd status") 
	except: 
		print ("httpd service restarts failed") 

@roles('webservers')
def httpd_restart():
	try: 
		sudo ("for i in $(ls /etc/init.d/httpdv1-*); do sudo $i restart; done")
		sudo ("for i in $(ls /etc/init.d/httpdv1-*); do sudo $i status; done")
		#sudo ("service httpdv1-perl restart && service httpdv1-proxy restart && service httpdv1-ssl restart")
		#sudo ("service httpdv1-perl status && service httpdv1-proxy status && service httpdv1-ssl status")
	except: 
		print ("httpd service restarts failed") 

def puppet(): 
	try: 
		sudo ("puppetd -tv")
	except: 
		print ("cannot run puppet")

@roles('scribe_boxes')
def startscribe(): 
#restart scribe processes on the target machines
	try: 
		sudo ("supervisorctl start scribe_node:scribe_node_0")
		sudo ("puppetd --enable")
		sudo ("/etc/init.d/scribed start")
		sudo ("/etc/init.d/scribed status")

	except: 
		print ("some scribe services could not be stopped")

@roles('search_boxes')
def stopscribe(): 
#stop scribe kill related processes on the target machines
	try: 
		sudo ("supervisorctl stop scribe_node:scribe_node_0")
		sudo ("puppetd --disable")
		sudo ("/etc/init.d/scribed stop")
		sudo ("for pid in $(ps aux | grep scribe | awk '{print $2}'); do kill -9 $pid; done ")
		sudo ("/etc/init.d/scribed status")
		# you can run this command on the target machine to confirm success 
		# clear; hostname; date;  supervisorctl status scribe_node:scribe_node_0 && /etc/init.d/scribed status ; puppetd -tv

	except: 
		print ("some scribe services could not be stopped")

@roles('activemq')
def kick_activemq(): 
	try: 
		sudo ("service activemq stop && sleep 3 && service activemq start")
	except: 
		print ("cannot get activemq status")

@roles('activemq')
def activemq(): 
	try: 
		sudo ("service activemq status")
	except: 
		print ("cannot get activemq status")

def activemqlog(): 
	try: 
		sudo ("tail -n 100 /var/log/activemq/activemq.log") 
	except: 
		print ("cannot read activemq log")

def resetldap():
	try:
		sudo ('service sssd stop && rm -f /var/lib/sss/db/cache_LDAP.ldb && service sssd start')
	except:
		print ( "could not reset ldap")

def ldapid():
	try:
		sudo ("id sys.argv[0]")
	except:
		print ("error")

def superup():
	try:
		sudo ("supervisorctl status | grep $regex | awk '{print \"supervisorctl start \"$1}' | sh")
	except:
		print("Could not restart supervisorctl")

@roles('ntp_servers')
def check_ntp():
	try:
		sudo ("/etc/init.d/ntpd status")
	except:
		print ("failed to update date")

@roles('ntp_servers')
def ntpdupdate():
	try:
		sudo ("/etc/init.d/ntpd stop && ntpdate ntpserver.example.com && sleep 3 && /etc/init.d/ntpd start")
	except:
		print ("failed to update date")

@roles('mogilefstrackers')
def mogile_status():
	try: 
		sudo ("echo '!jobs' | nc `hostname` 6001")
		sudo ("echo '=== only showing error entries ==='")
		sudo ("mogadm check | grep -v writeable")
	except: 
		print ("error checking mogilefs trackers")

@roles('mogilefsnodes')
def mogile():
	try: 
		sudo ("for dir in $(ls -al /var/mogdata/ | grep \"?\" |  awk '{print $NF}'); do umount $dir && sleep 3 && mount $dir; done")
	except: 
		print ("cannot re-mount mogilefs nodes")

@roles('zenoss')
def zenoss_remodel():
	try: 
		# this works, but is ugly
		sudo ("runuser -l zenoss -c 'for i in `cat /home/user/list`; do zenmodeler run -d $i; done'")
	except: 
		print ("cannot re-run zenoss monitor checks")

@roles('search_boxes')
def scribed_status(): 
	try: 
		sudo ("supervisorctl status scribe_node:scribe_node_0")
	except: 
		print ("cannot get scribed status") 

@roles('hypervisors')
def reboot_vms(): 
	try: 
		sudo ("for vm in `virsh list --all | grep \"shut off\" | awk '{print $2}'`; do virsh start $vm; done")
	except: 
		print ("cannot reboot vms on hypervisor")

@roles('hypervisors')
def list_vms(): 
	try: 
		sudo ("virsh list --all")
	except: 
		print ("cannot list vms on hypervisor")
