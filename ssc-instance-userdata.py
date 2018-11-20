# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
#import novaclient.v1_1.client as nvclient
#from credentials import get_nova_creds
import time, os, sys
import inspect
import glob 
#import novaclient.v3.client as nvclient
#from credentials import get_nova_creds
from os import environ as env
#import shade
import key as D
from  novaclient import client
import keystoneclient.v3.client as ksclient
#from credentials import get_credentials
#from credentials import get_nova_creds
from keystoneauth1 import loading
from keystoneauth1 import session
#from novaclient.client import Client
#import novaclient.v3.client as nvclient
#from credentials import get_nova_creds
#creds = get_nova_creds()

#credentials = get_nova_credentials_v2()
#nova_client = Client(**credentials)

#cloud = shade.openstack_cloud()    

#creds = get_nova_creds()
flavor = "ssc.small" 
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = "public"
floating_ip = None #"130.239.81.118" #"Public External IPv4 Network"
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
key = "zeelabkey"
loader = loading.get_plugin_loader('password')



loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default']

print "Creating instance ... "
instance = nova.servers.create(name="vm1", image=image, flavor=flavor, userdata=userdata, key_pair= key , nics=nics,security_groups=secgroups)
inst_status = instance.status
print "waiting for 10 seconds.. "
time.sleep(10)

while inst_status == 'BUILD':
    print "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more..."
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print "Instance: "+ instance.name +" is in " + inst_status + "state"