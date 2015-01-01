__author__ = 'jgrinwis'

# import juniper module
from jnpr.junos import Device
from jnpr.junos.version import VERSION
from jnpr.junos.op.ethport import EthPortTable
from pprint import pprint

# our vsrx
juniper = "10.160.35.205"

# create connection to device, don't forget to allow NETCONF on juniper device!
dev = Device(host=juniper,user='root',password='password123')

# connect to device and open NETCONF connection
print("connecting to: %s using PyEz module version %s " % (juniper, VERSION))
dev.open()

# after opening a device, lets get the facts
# facts is a dictionary with info
# pprint(dev.facts)

# the EthPortTable is a class with a table and a view
# first connect class to device
eths = EthPortTable(dev)

# now get the view from this object
# view is defined by YAML file somewhere in PyEz library
# you can create your own YAML files to create your own tables and views.
eths.get()

# we can now access the class like a dictionary use items(), keys() and values()
# pprint("interface keys found: %s" % eths.keys())

# now let's pick one of the interface as a key
# interface = eths['ge-0/0/0']

# to show all items from this interface, keys() can again be used
# pprint(eths.keys())

# now print some facts from this device
print("Your connected to %s which is a %s running Junos version %s" % (dev.facts['hostname'], dev.facts['model'], dev.facts['version']))

# now check all interfaces on this device
for key in eths.keys():
    interface = eths[key]
    print("The state of interface %s is %s" % (interface.key, interface.admin))

# now close connection to device again.
dev.close()