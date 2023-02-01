"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Settings, Plugin, xsd
from zeep.transports import Transport
from zeep.exceptions import Fault
import sys
import urllib3

# Edit .env file to specify your Webex site/user details
import os
from dotenv import load_dotenv
load_dotenv()

# Change to true to enable output of request/response headers and XML
DEBUG = True

# The WSDL is a local file in the working directory, see README
WSDL_FILE = 'schema/AXLAPI.wsdl'

PARTITION_NAME = 'test_PT'  # test_PT dCloud_PT

# This class lets you view the incoming and outgoing http headers and XML


class MyLoggingPlugin(Plugin):

    def egress(self, envelope, http_headers, operation, binding_options):

        # Format the request body as pretty printed XML
        xml = etree.tostring(envelope, pretty_print=True, encoding='unicode')

        print(f'\nRequest\n-------\nHeaders:\n{http_headers}\n\nBody:\n{xml}')

    def ingress(self, envelope, http_headers, operation):

        # Format the response body as pretty printed XML
        xml = etree.tostring(envelope, pretty_print=True, encoding='unicode')

        print(f'\nResponse\n-------\nHeaders:\n{http_headers}\n\nBody:\n{xml}')


# The first step is to create a SOAP client session
session = Session()

# We avoid certificate verification by default
# And disable insecure request warnings to keep the output clear
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# To enabled SSL cert checking (recommended for production)
# place the CUCM Tomcat cert .pem file in the root of the project
# and uncomment the line below

# session.verify = 'changeme.pem'

# Add Basic Auth credentials
session.auth = HTTPBasicAuth(
    os.getenv('AXL_USERNAME'), os.getenv('AXL_PASSWORD'))

# Create a Zeep transport and set a reasonable timeout value
transport = Transport(session=session, timeout=10)

# strict=False is not always necessary, but it allows zeep to parse imperfect XML
settings = Settings(strict=False, xml_huge_tree=True)

# If debug output is requested, add the MyLoggingPlugin callback
plugin = [MyLoggingPlugin()] if DEBUG else []

# Create the Zeep client with the specified settings
client = Client(WSDL_FILE, settings=settings, transport=transport,
                plugins=plugin)

# Create the Zeep service binding to AXL at the specified CUCM
service = client.create_service('{http://www.cisco.com/AXLAPIService/}AXLAPIBinding',
                                f'https://{os.getenv( "CUCM_ADDRESS" )}:8443/axl/')

try:
    resp = service.listRoutePartition(
        searchCriteria={'name': PARTITION_NAME}, returnedTags={'name': xsd.Nil})
except Fault as err:
    print(f'Zeep error: listRoutePartition: { err }')
    sys.exit(1)

if resp['return'] and 'routePartition' in resp['return']:
    theUUID = resp['return']['routePartition'][0]['uuid']
    print("The UUIDfor test_PT: ", theUUID)
    with open('dn_patterns.txt', 'r') as f:
        for line in f.readlines():
            thePattern = line.rstrip()
            theLen = len(thePattern)
            print(f'Pattern: {thePattern} length: {theLen}')
            # Execute the addLine request
            try:
                # resp = service.updateLine(pattern=thePattern, callForwardAll={
                #    'forwardToVoiceMail': 'false'})
                resp = service.updateLine(pattern=thePattern, newRoutePartitionName={
                    'uuid': theUUID})
            except Fault as err:
                print(f'Zeep error: updateLine: { err }')
                sys.exit(1)

    print('\nupdateLine response:\n')
    print(resp, '\n')
else:
    print(f'No route partition with name {PARTITION_NAME} found!')
