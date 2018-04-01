#!/usr/bin/python
import os
import time
import xmlrpclib

from download_drivefiles import search_filename
starttime = time.time()
image_dir = '/home/dek/another_dir/photos/'

HOST = "db_name.odoo.com"  # oe localhost:8069
DB = "db_name"
USER = "USERNAME"
PASSWORD = "PASSWORD"

url = 'http://%s/xmlrpc/' % (HOST)
common_proxy = xmlrpclib.ServerProxy(url + 'common')
object_proxy = xmlrpclib.ServerProxy(url + 'object')

uid = common_proxy.login(DB, USER, PASSWORD)
print "Logged in as %s (uid:%d)" % (USER, uid)


def source_execute(*args):
    return object_proxy.execute(DB, uid, PASSWORD, *args)


def normalize_imagenames(imagenames):
    default_codes = []
    for imagename in imagenames:
        try:
            default_codes.append(imagename[:imagename.rindex('.')].replace('_', '/').upper())
        except Exception, e:
            default_codes.append(imagename)
            print "Exception for ", imagename, e
    return default_codes

imagenames = os.listdir(image_dir)
default_codes = normalize_imagenames(imagenames)

print "Images in local filesystem: ", len(imagenames)

model = "product.template"
code_imagemap = dict(zip(default_codes, imagenames))
newproduct_data = source_execute(model, 'search_read', [], ['id', 'default_code'])

print "Product Templates in remote server:", len(newproduct_data)
notfound = []
found = []
total = 0
for productmap in newproduct_data:
    try:
        imagename = code_imagemap[productmap['default_code'].upper()]
        print image_dir + imagename
        print total, " Writing Image (Product -", productmap['default_code'], ", Image - ", imagename, ")"
        found.append(productmap['default_code'])
        with open(image_dir + imagename, 'rb') as binaryimage:
            image_base64 = binaryimage.read().encode("BASE64")
            updated_product_ids = source_execute(model, 'write', int(productmap['id']), {'image': image_base64})
        total = total + 1
    except IOError:
        print "Image '%s' not found" % imagename
    except Exception, e:
        print "No local image: ", productmap['default_code']
        notfound.append(productmap['default_code'])
print total, "Image(s) imported"
endtime = time.time()
print endtime - starttime
print found
print "Search notfound imagenames on google drive: checking if they exist/With similar names"

search_filename(notfound)

# Improvements
# Optimizations
# Naming conventions
# Removed time consuming search_read in loop, which takes much time
# compute base64 only for related images
