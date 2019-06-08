#!/usr/bin/python3

import jinja2,os,sys

# parse arguments
if len(sys.argv) != 3:
    print('Usage: ./generate-router-config.py template peer-count')
    print('Example: ./generate-exabgp-config.py templates/cisco.template 255')
    print('Valid number of peers is 1-255')
    sys.exit(1)

try:
    if int(sys.argv[2]) >= 1 and int(sys.argv[2]) <= 255:
        peer_count = int(sys.argv[2])
    else:
        print('Number of peers must be in range 1-255')
        sys.exit(1)
except ValueError:
    print('Number of peers must be in range 1-255')
    sys.exit(1)

# setup jinja2
templateLoader = jinja2.FileSystemLoader(searchpath='.')
templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True, trim_blocks=True)
templateFile = sys.argv[1]
template = templateEnv.get_template(templateFile)

# define variables for config generation
vars = {
    'interface':   'Ethernet1',
    'local_ipv4':  [],
    'local_ipv6':  [],
    'neighbors':   [],
    'local_as':    '1000',
}

for i in range(1,peer_count + 1):
    neighbor = {
        'ipv4': '10.0.' + str(i) + '.2',
        'ipv6': 'fd00::10:0:' + str(i) + ':2',
        'as':   '1' + str(i).zfill(3),
    }
    vars['local_ipv4'].append('10.0.' + str(i) + '.1')
    vars['local_ipv6'].append('fd00::10:0:' + str(i) + ':1')
    vars['neighbors'].append(neighbor)

config = template.render(vars)
print(config)

