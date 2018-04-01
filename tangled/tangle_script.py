#!/usr/bin/python

# tangle/untangle - needed to do once for a problem with odoo database
# tangle/untangle could also be used for data migration

import untangle
import xmlrpclib

# Change these things as necessary
# *******************************
HOST = "localhost:8081"
DB = "db_name"
USER = "admin"
PASSWORD = "admin"
# *******************************

url = 'http://%s/xmlrpc/' % (HOST)
common_proxy = xmlrpclib.ServerProxy(url + 'common')
object_proxy = xmlrpclib.ServerProxy(url + 'object')

print "Authenticating..."
uid = common_proxy.login(DB, USER, PASSWORD)
print "Logged in as %s (uid:%d)" % (USER, uid)


def source_execute(*args):
    return object_proxy.execute(DB, uid, PASSWORD, *args)

obj = untangle.parse('./badge.xml')

# records = obj.odoo.data.record
# records = obj.odoo.record
records = obj.openerp.data.record

createdict = {}
for record in records:
    record_dict = record.__dict__
    record_dict_model = record_dict['_attributes']['model']
    fields = record.field
    for field in fields:
        createdict[field.__dict__['_attributes']['name']] = field.__dict__['cdata']
    try:
        print "Model: %s => %s" % (record_dict_model, createdict)
        server_data = source_execute(record_dict_model, 'create', createdict)
    except Exception, e:
        print "Exception ", e
