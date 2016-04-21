# $SPLUNK_HOME/etc/apps/hello_mi/bin/puppetserver_api.py


import requests
import json
import logging

class PuppetserverEndpoint:
    def __init__(self,base_url):
        self.base_url = base_url
    
    def get(self,url,**kwargs):
        result = requests.get(url)

    def get_status(self,environment,rname):
        environment = environment
        rname = rname
        url = self.base_url + "/puppet/v3/status/{0}?environment={1}".format(rname,environment)

        # [root@pe-aio3-dev ~]# curl -k -X GET https://localhost:8140/puppet/v3/status/pe-aio3-dev?environment=production
        # {"is_alive":true,"version":"4.4.0"}[root@pe-aio3-dev ~]#

        result = self.get(url)
        return json.loads(result)
