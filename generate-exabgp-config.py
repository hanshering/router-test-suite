#!/usr/bin/python3

import jinja2,os,sys


peer_count = 255
test_names = ["ROUTE-001","ROUTE-002","ROUTE-003"]

# setup jinja2
templateLoader = jinja2.FileSystemLoader(searchpath='.')
templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True)

# define variables for config generation
basedir = os.path.dirname(os.getcwd())
vars = {
    'local_ipv4':  '',
    'local_ipv6':  '',
    'remote_ipv4': '',
    'remote_ipv6': '',
    'local_as':    '',
    'remote_as':   '1000',
    'ssbgp_path':  basedir + '/ssbgp/ssbgp.py',
    'ssbgp_config_path': '../router-test-suite/configs/ssbgp/',
    'test_name':   '',
}

# create output folder for configs
for test_name in test_names:
    templateFile = 'templates/' + test_name + '.template'
    template = templateEnv.get_template(templateFile)
    vars['test_name'] = test_name
    config_path = 'configs/exabgp/' + vars['test_name'] + '/'
    if not os.path.exists(config_path):
        os.makedirs(config_path)


    for i in range(1,peer_count + 1):
        vars['local_ipv4']  = '10.0.' + str(i) + '.2'
        vars['local_ipv6']  = 'fd00::10:0:' + str(i) + ':2'
        vars['remote_ipv4'] = '10.0.' + str(i) + '.1'
        vars['remote_ipv6'] = 'fd00::10:0:' + str(i) + ':1'
        vars['local_as']    = '1' + str(i).zfill(3)
        config = template.render(vars)
        file_name = 'peer-' + str(i) + '.conf'
        f = open(config_path + file_name, 'w')
        f.write(config)

