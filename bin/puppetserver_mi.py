# $SPLUNK_HOME/etc/apps/hello_mi/bin/puppetserver_mi.py

import sys
import xml.dom.minidom, xml.sax.saxutils
import requests
import puppetserver_api

SCHEME = """<scheme>
    <title>puppetserver Status</title>
    <description>Load puppetserver status information from HTTP status API endpoint</description>
    <use_external_validation>false</use_external_validation>
    <streaming_mode>simple</streaming_mode>
    <use_single_instance>false</use_single_instance>
    <endpoint>
        <args>
            <arg name="base_url">
                <title>Base URL</title>
                <description>The base URL to use to access the puppetserver instance. e.g. https://localhost:8140</description>
                <required_on_create>true</required_on_create>
                <required_on_edit>false</required_on_edit>
            </arg>
            <arg name="environment">
                <title>Environment</title>
                <description>String provided for the environment parameter of the API request</description>
                <required_on_create>true</required_on_create>
                <required_on_edit>false</required_on_edit>
            </arg>
            <arg name="rname">
                <title>Name</title>
                <description>String provided for the name parameter of the API request</description>
                <required_on_create>true</required_on_create>
                <required_on_edit>false</required_on_edit>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

# Empty introspection routine
def do_scheme(): 
    print SCHEME

# Empty validation routine. This routine is optional.
def validate_arguments(): 
    pass

def validate_conf(config, key):
    if key not in config:
        raise Exception, "Invalid configuration received from Splunk: key '%s' is missing." % key

#read XML configuration passed from splunkd
def get_config():
    config = {}

    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            logging.debug("XML: found configuration")
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    logging.debug("XML: found stanza " + stanza_name)
                    config["name"] = stanza_name

                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        logging.debug("XML: found param '%s'" % param_name)
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data
                            logging.debug("XML: '%s' -> '%s'" % (param_name, data))

        if not config:
            raise Exception, "Invalid configuration received from Splunk."

        # just some validation: make sure these keys are present (required)
        validate_conf(config, "base_url")
        validate_conf(config, "rname")
        validate_conf(config, "environment")
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config

def run_script(): 
    # Example from Puppet HTTP API docs
    # GET /puppet/v3/status/whatever?environment=env

    # HTTP 200 OK
    # Content-Type: text/pson

    # {"is_alive":true,"version":"3.3.2"}

    # Status schema spec from docs
    # {
    #     "$schema":     "http://json-schema.org/draft-04/schema#",
    #     "title":       "Master status",
    #     "description": "Information about a running master",
    #     "type":        "object",
    #     "properties": {
    #         "is_alive": {
    #             "description": "This will always be true since the master must be running to retrieve the object",
    #             "type": "boolean"
    #         },
    #         "version": {
    #             "description": "The version of the master",
    #             "type": "string"
    #         }
    #     },
    #     "required": ["is_alive", "version"],
    #     "additionalProperties": false
    # }

    config = get_config()
    
    base_url = config["base_url"]
    environment = config["environment"]
    rname = config["rname"]

    endpoint = PuppetserverEndpoint(base_url=base_url)
    endpoint.get_status(environment=environment,rname=rname)

# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            validate_arguments()
        else:
            pass
    else:
        run_script()

    sys.exit(0)
