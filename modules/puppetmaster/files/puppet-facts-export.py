#!/usr/bin/python3
import configparser
import os
import shutil
import subprocess
import tempfile

import requests
import yaml

from datetime import datetime, timedelta


class PuppetDBApi(object):
    def __init__(self, puppetdb_config_file):
        config = configparser.ConfigParser()
        config.read(puppetdb_config_file)
        self.host = config['main']['server']
        self.port = config['main']['port']

    def url_for(self, endpoint):
        # TODO: use /pdb/query/v4 when we upgrade.
        return 'https://{h}:{p}/v4/{ep}'.format(h=self.host, p=self.port, ep=endpoint)

    def get(self, endpoint):
        return requests.get(self.url_for(endpoint)).json()


def main():
    date_format = '%Y-%m-%d %H:%M:%S.%s +00:00'
    datetime_facts = datetime.utcnow()
    ts = datetime_facts.strftime(date_format)
    exp = (datetime_facts + timedelta(days=365)).strftime(date_format)

    outfile = '/tmp/puppet-facts-export.tar.xz'
    tmpdir = tempfile.mkdtemp(dir='/tmp', prefix='puppetdb-export')
    factsdir = os.path.join(tmpdir, 'yaml', 'facts')
    print("Saving facts to {}".format(factsdir))
    os.makedirs(factsdir)
    conf = os.environ.get('PUPPETDB_CONFIG_FILE', '/etc/puppet/puppetdb.conf')
    pdb = PuppetDBApi(conf)
    for node in pdb.get('nodes/'):
        if node.get('deactivated', True) is not None:
            continue
        nodename = node['certname']
        yaml_data = {}
        facts = pdb.get('nodes/{}/facts'.format(nodename))
        for fact in facts:
            yaml_data[fact['name']] = fact['value']
        filename = os.path.join(factsdir, "{}.yaml".format(nodename))
        # Anonymize potentially reserved data
        yaml_data['uniqueid'] = '43434343'
        yaml_data['boardserialnumber'] = '4242'
        yaml_data['boardproductname'] = '424242'
        yaml_data['serialnumber'] = '42424242'
        del yaml_data['trusted']
        print('Writing {}'.format(filename))
        with open(filename, 'w') as fh:
            contents = yaml.dump({'name': nodename, 'values': yaml_data,
                                  'timestamp': ts, 'expiration': exp})
            fh.write('--- !ruby/object:Puppet::Node::Facts\n' + contents)
    subprocess.check_call(['tar', 'cJvf', outfile, '--directory', tmpdir, 'yaml'])
    shutil.rmtree(tmpdir)


if __name__ == '__main__':
    main()
