#!/usr/bin/env python
#

import os, sys
from optparse import OptionParser
from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http

api_name = "androidenterprise"
api_version = "v1"
scope = "https://www.googleapis.com/auth/%s" % (api_name)

parser = OptionParser()
parser.add_option("-e","--email",dest="email",type="string",
                  help="Client email to use for credentials when requesting access token")
parser.add_option("-k","--keyfile",dest="keyfile",type="string",
                  help="PKCS12 keyfile holding the encoded secret key for authenticating the credentials token request")
parser.add_option("-d","--domain",dest="domain",type="string",
                  help="Domain of the enterprise to query for")
(opts,args) = parser.parse_args()

with open(opts.keyfile, "rb") as fd:
    key = fd.read()

credentials = SignedJwtAssertionCredentials(opts.email, key, scope)

http = credentials.authorize(Http())

androidenterprise = build(api_name, api_version, http=http)

response = androidenterprise.enterprises().list(domain=opts.domain).execute(http=http)
print response

