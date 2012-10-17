from fabric.api import * 
import sys 



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
	'webservers' : [ 
			'webserver%02d.ma01.shuttercorp.net' % n for n in xrange(01,99)
			],
	}

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

@roles('webservers')
def httpd_status():
	try: 
		sudo ("service httpdv1-perl status && service httpdv1-proxy status && service httpdv1-ssl status")
	except: 
		print ("httpd service restarts failed") 

@roles('webservers')
def httpd_restart():
	try: 
		sudo ("service httpdv1-perl restart && service httpdv1-proxy restart && service httpdv1-ssl restart")
		sudo ("service httpdv1-perl status && service httpdv1-proxy status && service httpdv1-ssl status")
	except: 
		print ("httpd service restarts failed") 

def puppet(): 
	try: 
		sudo ("puppetd -tv")
	except: 
		print ("cannot run puppet")

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


@roles('zenoss')
def zenoss_remodel():
	try: 
		# this works, but is ugly
		sudo ("runuser -l zenoss -c 'for i in `cat /home/user/list`; do zenmodeler run -d $i; done'")

	except: 
		print ("cannot re-run zenoss monitor checks")

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
