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
	'infhosts' : [
      '172.24.9.169',
      '172.24.8.168',
      '172.24.12.158',
      '172.24.9.206',
      '172.24.14.39',
      '172.24.15.26',
      '172.24.15.195',
      '172.24.13.226',
      '172.24.10.110',
      '172.24.10.202',
      '172.24.10.120',
      '172.24.1.99',
      '172.24.11.185',
      '172.24.13.227',
      '172.24.14.26',
      '172.24.12.26',
      '172.24.15.168',
      '172.24.0.172',
      '172.24.15.201',
			],

	'umd' : [
      '172.24.10.84',
      '172.24.12.131',
      '172.24.9.196',
      '172.24.13.231',
      '172.24.14.61',
			],
	'icinga' : [
			'icinga01.example.com',
			],
  'stghosts'    : [
			'172.24.10.87',
			'172.24.11.10',
			'172.24.11.112',
			'172.24.11.157',
			'172.24.12.220',
			'172.24.12.32',
			'172.24.12.58',
			'172.24.13.101',
			'172.24.13.135',
			'172.24.13.169',
			'172.24.13.233',
			'172.24.15.155',
			'172.24.15.157',
			'172.24.8.205',
			'172.24.8.34',
			'172.24.9.10',
			'172.24.9.13',
			'172.24.9.21',
			],
  'qatest'    : [
      '172.24.10.148',
      ],
  'qahosts'    : [
      '172.24.10.148',
      '172.24.11.107',
      '172.24.11.111',
      '172.24.11.124',
      '172.24.12.252',
      '172.24.13.111',
      '172.24.13.123',
      '172.24.14.240',
      '172.24.14.248',
      '172.24.14.45',
      '172.24.14.61',
      '172.24.15.206',
      '172.24.15.219',
      '172.24.8.107',
      '172.24.8.146',
      '172.24.8.75',
      '172.24.8.85',
    ],
  'qa'  : [
      '172.24.12.131',
      '172.24.13.218',
      '172.24.15.10',
      '172.24.15.137',
      '172.24.15.219',
      '172.24.9.196',
      '172.24.9.91',
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
	'fukt' : [
			'172.24.1.150'
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

def mcorestart():
	try:
		sudo ("/etc/init.d/mcollective stop && /etc/init.d/mcollective start && /etc/init.d/mcollective status")
	except:
		print ("could not restart mcollective service")

def hostname():
	try:
		sudo ("hostname")
	except:
		print ("cannot get hostname")

@roles('qahosts')
def dockerlist():
	try:
		sudo ("hostname")
		sudo ("docker ps")
	except:
		print ("cannot list containers")

@roles('infhosts')
def chefversion():
	try:
		sudo ("hostname")
		sudo ("chef-client --version")
	except:
		print ("cannot list containers")

@roles('stghosts')
def updatechefversion():
	try:
		sudo ("chef-client --version")
		sudo ("install_sh='https://www.chef.io/chef/install.sh' ; version_string='-v 12.5.1' ; bash <(wget ${install_sh} -O -) ${version_string}")
		sudo ("chef-client --version")
	except:
		print ("cannot list containers")

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

@roles('qa')
def umd():
	try:
		sudo ("history | wc -l")
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


def puppetstate():
	try:
		sudo ("ls -alh /var/lib/puppet/state/*")
	except:
		print ("cannot get puppet state file list")

@roles('new_hypervisors')
def messages():
	try:
		sudo ("tail -n 20 /var/log/messages")
	except:
		print ("cannot tail messages")

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

@roles('fukt')
def stopchef():
#stop scribe kill related processes on the target machines
	try:
		sudo ("ps aux | grep chef-client | awk '{print $2}' | xargs kill -9")
	except:
		print ("nope")

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

@roles('icinga')
def kick_nagios():
	try:
		sudo("service ido2db status")
		sudo("service ido2db stop")
		sudo("rm -f /var/icinga/ido.sock")
		sudo("service ido2db start")
		sudo("service icinga checkconfig && service icinga restart")
		sudo("service ido2db status")
		sudo("service icinga status")

	except:
		print ("cannot cycle nagios services")

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

@roles('servicebox')
def java_len():
	try:
		sudo ("cd /home/mmedeiros/ && java Test")
	except:
		print ("cannot run encryption length test")

def hostinfo():
	try:
		run ("cat /etc/issue")
		run ("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")
		run ("\df -hP | column -t")
		run ("nproc")
	except:
		print ("cannot determine system info")


@roles('gooo')
def jvm_crypt_and_test():
	proddir = '/usr/java/current/jre/lib/security'
	homedir = '/home/mmedeiros'
	file1 = 'local_policy.jar'
	file2 = 'US_export_policy.jar'
	try:
		sudo ("cp %s/%s %s/%s.bak" % (proddir, file1, proddir, file1))
		sudo ("cp %s/%s %s/%s.bak" % (proddir, file2, proddir, file2))
		sudo ("ls -al %s/*policy.jar*" % (proddir))
		sudo ("cp %s/%s.new %s/%s" % (homedir, file1, proddir, file1))
		sudo ("cp %s/%s.new %s/%s" % (homedir, file2, proddir, file2))
		sudo ("cd %s && java Test" % (homedir))
	except:
		print ("move files and run test")

