import os
import yaml
# Project configurations
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
servicedir = os.path.join(basedir, 'inventory')
confdir = os.path.join(basedir, 'docs')

print("Base dir:", basedir)
print("Serv dir:", servicedir)

conffile = os.path.join(confdir, 'conf.yaml')
with open(conffile, "r") as ymlconf:
    try:
        conf = yaml.safe_load(ymlconf)
    except yaml.YAMLError as exc:
        print(exc)


host = conf['Redis']['host']
port = conf['Redis']['port']
password = conf['Redis']['password']

print(host)
print(port)
print(password)