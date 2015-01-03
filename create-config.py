# First PyEz test with YAML and jinja2 template engine
# YAML file should contain juniper devices to configre

import yaml
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# create datastructure from YAML file.
# yaml.load takes a stream so open file object from yaml file.
myvars = yaml.load(open('configuration.yml').read())

# myvars has become a python dictionary thanx to YAML lib.
pprint(myvars)

# now create juniper device object from Device class and open this device.
for juniper in myvars['juniper_devices']:
    print "Configuring %s" % juniper
    device = Device(host=juniper, user='root', password='password123')
    output = device.open()

    # now bind Config class to this device which makes it a property of the :class:Device instance
    device.bind(cfg=Config)

    # load can take our jinja2 template with our myvars from YAML file
    # The following parameters are needed for the load command:
    # 1: template_path (str): path to jinja2 template file
    # 2: template_vars (dict): dictionary build from YAML file, same vars are in jinja2 template
    # 3: set format to text, otherwise you will see errors
    device.cfg.load(template_path='config-template.j2', template_vars=myvars, format='text')

    # print configuration differences
    device.cfg.pdiff()

    # now check configuration and if it's all OK, just commit.
    if device.cfg.commit_check():
        device.cfg.commit()
    else:
        print("something wrong")

    # no close connection to juniper device
    device.close()

print "configuration of devices done"